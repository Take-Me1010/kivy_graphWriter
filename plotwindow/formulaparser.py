
from typing import Callable, Dict, List, Tuple, Union
import sympy

from core.exceptions import FormulaParseError, VariableError

from libs.ply_tex2sym.tex2sym_parser import tex2sym


class FormulaFormatter:
    def remove_spaces(formula:str) -> str:
        """文字列から空白を除去した文字列を返す

        Args:
            formula (str): 文字列

        Returns:
            str: 空白が存在しない文字列
        """        
        return formula.replace(' ','').replace('　', '')

    def poly2numpy(poly:sympy.Poly, args:List[sympy.Symbol]=None) -> callable:
        """Polyをnumpy形式の関数に変換する

        Args:
            poly (sympy.Poly): Polyインスタンス
            args (List[sympy.Symbol], optional): 変数のリスト。. Defaults to None.

        Returns:
            callable: numpy形式の数式
        """
        if args is None:
            args = list(poly.atoms(sympy.Symbol))
        f = poly.as_expr()
        # print(f'[INFO\t] [FormulaFormatter\t] [poly2numpy\t] expr : {f}, args : {args}')

        return sympy.lambdify(args, f, ["numpy"])

class VariableFactory:
    _z = sympy.Symbol('z')
    variables : Dict[sympy.Symbol, float] = {}
    estimate_variables : List[sympy.Symbol] = []
    MAX_ESTIMATE : int = 4
    def init():
        """登録を初期化する
        """
        VariableFactory.variables = {}
        VariableFactory.estimate_variables = []

    def register_variable(name:sympy.Symbol, value:float):
        VariableFactory.variables[name] = value

        # print(f'[VariableFactory\t] [register_variable] registered {name} : {value}')
    
    def register_estimate_variables(variables:List[str]):
        if len(variables) >= VariableFactory.MAX_ESTIMATE:
            print(f'[WARNING\t] [VariableFactory\t] [register_estimate_variables] Too may estimate variables : {variables}')
        
        for i, val in enumerate(variables):
            if i >= VariableFactory.MAX_ESTIMATE-1:
                break

            VariableFactory.estimate_variables.append(
                sympy.Symbol(val)
            )

    def register_variable_from_formula(formula:str):
        lhs = FormulaParser.get_left_side(formula)
        lhs, _ = sympy.poly_from_expr(tex2sym(lhs))
        name = list(lhs.atoms(sympy.Symbol))[0]

        rhs = FormulaParser.get_right_side(formula)
        rhs = rhs + '+z'
        rhs, _ = sympy.poly_from_expr(tex2sym(rhs))     # 定数のみのPolyは生成できなかったため、仮の変数zを使用。
        rhs = rhs.subs({VariableFactory._z:0}).subs(VariableFactory.variables)
        value = rhs.as_expr().evalf()

        VariableFactory.register_variable(name, value)
    
    def change_variable_value(name:sympy.Symbol, value:float):
        try:
            VariableFactory.variables[name] = value
        except KeyError:
            raise VariableError(f'No {name} has been registered.')

class FormulaParser:

    def check_equal(formula:str) -> int:
        """数式内の'='の場所を確認し、また二個以上存在しないかを確認する

        Args:
            formula (str): 数式

        Raises:
            FormulaParseError: =が二個以上存在した場合

        Returns:
            int: =のindexを返却する。=が存在しない場合は-1を返す
        """
        index = -1
        has_equal = False
        n = len(formula)
        for i in range(n):
            if formula[i] == '=':
                if not has_equal:
                    index = i
                    has_equal = True
                else:
                    raise FormulaParseError('Two or more equals exist.')

        return index

    def get_left_side(formula:str) -> str:
        """formulaの左辺を得る

        Args:
            formula (str): 数式

        Returns:
            str: 左辺
        """
        index = FormulaParser.check_equal(formula)
        ret = ''
        if index != -1:
            ret = formula[:index]
        
        # print(f'[FormulaParser\t] [get_left_side\t] return {ret}, index = {index}')
        return ret

    def get_right_side(formula:str) -> str:
        """数式の右辺を得る

        Args:
            formula (str): 数式

        Returns:
            str: 右辺
        """
        index = FormulaParser.check_equal(formula)

        ret = ''
        if index != -1:
            ret = formula[index+1:]
            
        # print(f'[FormulaParser\t] [get_right_side\t] return {ret}, index = {index}')
        return ret

    def get_poly(formula:str) -> sympy.Poly:
        """文字列の数式からPolyを得る

        Args:
            formula (str): 数式

        Returns:
            sympy.Poly: Polyインスタンス
        """
        formula += '+z'
        poly, _ = sympy.poly_from_expr(tex2sym(formula))
        poly = poly.subs({sympy.Symbol('z'):0})
        # print(f'[INFO\t] [FormulaParser\t] [get_poly\t] return {poly}, vals : {poly.atoms(sympy.Symbol)}')
        return poly

    def estimate_parse(s:str) -> Dict[str, List[str]]:
        """#: estimate = a, b, c の=以降の部分を解析して登録する。

        Args:
            s (str): a,b,cなどの変数名のカンマ区切り文字列

        Returns:
            Dict[str, List[str]]: {'estimate' : est_vals} est_valsは推定する文字の名前
        """
        n = len(s)
        est_vals = [v for v in s.split(',')]
        # i = 0
        # for j in range(n):
        #     if s[j] == ',':
        #         est_vals.append(
        #             s[i:j]
        #         )
        #         i = j+1

        VariableFactory.register_estimate_variables(est_vals)

        return {'estimate' : est_vals}

    def comment_parse(formula:str) -> Union[Dict[str, str], None]:
        """コメントの数式を解析する

        Args:
            formula (str): 数式

        Returns:
            Union[Dict[str, str], None]: labelの場合は辞書、それ以外はNone
        """
        ret = None
        # 機能付きコメント #: の場合 
        if formula[1] == ':':
            i = FormulaParser.check_equal(formula)
            if formula[2:i] == 'label':
                ret = {formula[2:i] : formula[i+1:]}
            
            elif formula[2:i] == 'estimate':
                ret = FormulaParser.estimate_parse(formula[i+1:])

        else:
            pass

        return ret

    def parse(formula:str) -> Union[sympy.Poly, Dict[str, str], None]:
        """受け取った数式を適切に処理する。変数定義ならNoneを返し、数式ならそのPolyインスタンスを返す。

        Args:
            formula (str): 解析対象の数式

        Returns:
            Union[sympy.Poly, Dict[str, str], None]: 数式ならPolyを返し、特殊コメントならDict, 変数定義ならNoneを返す
        """
        ret = None
        formula = FormulaFormatter.remove_spaces(formula)
        try:
            h = formula[0]
        except IndexError as e:
            print(f'[WARNING\t] [FomulaParser\t] {e}')
            return None

        if h == '#':       # コメントの場合
            ret = FormulaParser.comment_parse(formula)

        else:
            index = FormulaParser.check_equal(formula)
            # 変数定義の場合
            if index != -1:
                VariableFactory.register_variable_from_formula(formula)

            # 数式定義の場合
            else:
                poly = FormulaParser.get_poly(formula)
                ret = sympy.poly(poly.subs(VariableFactory.variables))
        
        # print(f'[INFO\t] [FormulaPerser\t] [parse\t] return {ret}')
        
        return ret
