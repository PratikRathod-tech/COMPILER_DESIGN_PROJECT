import re
from typing import Dict, Union, List, Tuple

def parse_linear_side(expr_str: str) -> Dict[str, float]:
    """
    Parses an expression string like '2*x + 5', '2*x + y', '15', 'x - y'
    Returns a dict mapping variable name to coefficient, with '' (empty string) for constant.
    """
    expr = expr_str.replace(" ", "")
    # Add explicit plus for leading sign if not present
    if not expr.startswith("+") and not expr.startswith("-"):
        expr = "+" + expr
    
    # Pattern to match terms: (+/-)(number*var | number | var)
    term_pattern = re.compile(r'([+-])(?:(\d+(?:\.\d+)?)\*([a-zA-Z_]\w*)|(\d+(?:\.\d+)?)|([a-zA-Z_]\w*))')
    
    coeffs: Dict[str, float] = {}
    pos = 0
    for match in term_pattern.finditer(expr):
        if match.start() != pos:
            raise ValueError(f"Could not parse term around '{expr[pos:match.start()]}'")
        pos = match.end()
        
        sign = -1.0 if match.group(1) == '-' else 1.0
        
        if match.group(2) and match.group(3):  # number*var
            coef = sign * float(match.group(2))
            var = match.group(3)
            coeffs[var] = coeffs.get(var, 0.0) + coef
        elif match.group(4):  # pure number
            val = sign * float(match.group(4))
            coeffs[''] = coeffs.get('', 0.0) + val
        elif match.group(5):  # pure var
            var = match.group(5)
            coeffs[var] = coeffs.get(var, 0.0) + sign * 1.0

    if pos != len(expr):
        raise ValueError(f"Invalid characters in linear expression: '{expr[pos:]}'")
        
    return coeffs

def solve_single_equation(eq_str: str) -> Tuple[Dict[str, float], List[str]]:
    """
    Solves a single linear equation e.g., '2*x + 5 = 15'
    Returns (solution_dict, explanation_steps)
    """
    if '=' not in eq_str:
        raise ValueError("Equation must contain '='")
    left_str, right_str = eq_str.split('=', 1)
    
    left_coeffs = parse_linear_side(left_str)
    right_coeffs = parse_linear_side(right_str)
    
    # Bring all variables to left, all constants to right:
    # left_vars - right_vars = right_const - left_const
    all_vars = set(k for k in left_coeffs if k != '') | set(k for k in right_coeffs if k != '')
    if not all_vars:
        raise ValueError("No variable found in linear equation.")
    if len(all_vars) > 1:
        raise ValueError(f"Single equation contains multiple variables: {list(all_vars)}. For system, use 'solve:' block.")
        
    var = list(all_vars)[0]
    total_coef = left_coeffs.get(var, 0.0) - right_coeffs.get(var, 0.0)
    total_const = right_coeffs.get('', 0.0) - left_coeffs.get('', 0.0)
    
    if abs(total_coef) < 1e-12:
        if abs(total_const) < 1e-12:
            raise ValueError("Equation has infinitely many solutions (tautology).")
        else:
            raise ValueError("Equation has no solution (inconsistent).")
            
    val = total_const / total_coef
    
    steps = [
        eq_str.strip(),
        f"{total_coef:g}*{var} = {total_const:g}" if total_coef != 1 else f"{var} = {total_const:g}",
        f"{var} = {val:g}"
    ]
    return {var: val}, steps

def solve_system_2x2(eq1_str: str, eq2_str: str) -> Tuple[Dict[str, float], List[str]]:
    """
    Solves a 2-equation linear system e.g.
    '2*x + y = 10'
    'x - y = 2'
    Returns (solution_dict, explanation_steps)
    """
    c1_left = parse_linear_side(eq1_str.split('=')[0])
    c1_right = parse_linear_side(eq1_str.split('=')[1])
    c2_left = parse_linear_side(eq2_str.split('=')[0])
    c2_right = parse_linear_side(eq2_str.split('=')[1])
    
    v1 = set(k for k in c1_left if k != '') | set(k for k in c1_right if k != '')
    v2 = set(k for k in c2_left if k != '') | set(k for k in c2_right if k != '')
    all_vars = sorted(list(v1 | v2))
    
    if len(all_vars) != 2:
        raise ValueError(f"System must have exactly 2 distinct variables, found {len(all_vars)}: {all_vars}")
        
    x_var, y_var = all_vars[0], all_vars[1]
    
    a1 = c1_left.get(x_var, 0.0) - c1_right.get(x_var, 0.0)
    b1 = c1_left.get(y_var, 0.0) - c1_right.get(y_var, 0.0)
    c1 = c1_right.get('', 0.0) - c1_left.get('', 0.0)
    
    a2 = c2_left.get(x_var, 0.0) - c2_right.get(x_var, 0.0)
    b2 = c2_left.get(y_var, 0.0) - c2_right.get(y_var, 0.0)
    c2 = c2_right.get('', 0.0) - c2_left.get('', 0.0)
    
    # Determinant of 2x2 system
    det_sys = a1 * b2 - a2 * b1
    if abs(det_sys) < 1e-12:
        raise ValueError("System does not have a unique solution (singular).")
        
    x_val = (c1 * b2 - c2 * b1) / det_sys
    y_val = (a1 * c2 - a2 * c1) / det_sys
    
    steps = [
        f"[1] {eq1_str.strip()}  =>  {a1:g}*{x_var} + {b1:g}*{y_var} = {c1:g}",
        f"[2] {eq2_str.strip()}  =>  {a2:g}*{x_var} + {b2:g}*{y_var} = {c2:g}",
        f"Determinant D = ({a1:g} * {b2:g}) - ({a2:g} * {b1:g}) = {det_sys:g}",
        f"{x_var} = {x_val:g}",
        f"{y_var} = {y_val:g}"
    ]
    return {x_var: x_val, y_var: y_val}, steps
