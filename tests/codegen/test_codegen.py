import pytest
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.ir.ir_generator import IRGenerator
from src.codegen.python_generator import PythonGenerator

def test_code_generation_syntax():
    source = "x = (10 + 20) * 5"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    generator = IRGenerator()
    ir_prog = generator.generate(ast)

    codegen = PythonGenerator()
    py_code = codegen.generate(ir_prog)

    # Verify that the generated code is syntactically valid Python
    compile(py_code, "<string>", "exec")

def test_execution(capsys):
    source = """
    radius = 10
    area = pi * radius^2
    show area
    """
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    generator = IRGenerator()
    ir_prog = generator.generate(ast)

    codegen = PythonGenerator()
    py_code = codegen.generate(ir_prog)

    global_env = {}
    exec(py_code, global_env)

    captured = capsys.readouterr()
    assert "314.159" in captured.out
