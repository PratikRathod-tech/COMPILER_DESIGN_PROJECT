from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.ir.ir_generator import IRGenerator

def test_ir_generation():
    source = "x = (a + b) * c"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    generator = IRGenerator()
    ir_prog = generator.generate(ast)
    instructions = ir_prog.get_instructions()

    assert len(instructions) == 3

    # Instruction 1: t1 = a + b
    assert instructions[0].op == "+"
    assert instructions[0].arg1 == "a"
    assert instructions[0].arg2 == "b"
    assert instructions[0].result == "t1"

    # Instruction 2: t2 = t1 * c
    assert instructions[1].op == "*"
    assert instructions[1].arg1 == "t1"
    assert instructions[1].arg2 == "c"
    assert instructions[1].result == "t2"

    # Instruction 3: x = t2
    assert instructions[2].op == "ASSIGN"
    assert instructions[2].arg1 == "t2"
    assert instructions[2].result == "x"
