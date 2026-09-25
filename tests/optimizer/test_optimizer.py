from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.ir.ir_generator import IRGenerator
from src.optimizer.optimizer import IROptimizer

def test_constant_folding():
    source = "x = 10 + 20"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    generator = IRGenerator()
    ir_prog = generator.generate(ast)

    optimizer = IROptimizer()
    opt_ir = optimizer.optimize(ir_prog)
    instructions = opt_ir.get_instructions()

    assert len(instructions) == 2
    assert instructions[0].op == "ASSIGN"
    assert instructions[0].arg1 == 30
    assert instructions[0].result == "t1"
    assert instructions[1].op == "ASSIGN"
    assert instructions[1].arg1 == 30
    assert instructions[1].result == "x"

def test_algebraic_simplification():
    source = "y = x + 0"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    generator = IRGenerator()
    ir_prog = generator.generate(ast)

    optimizer = IROptimizer()
    opt_ir = optimizer.optimize(ir_prog)
    instructions = opt_ir.get_instructions()

    assert len(instructions) == 2
    assert instructions[0].op == "ASSIGN"
    assert instructions[0].arg1 == "x"
    assert instructions[0].result == "t1"
    assert instructions[1].op == "ASSIGN"
    assert instructions[1].arg1 == "t1"
    assert instructions[1].result == "y"

def test_constant_propagation():
    source = """
    x = 10
    y = x + 5
    """
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    generator = IRGenerator()
    ir_prog = generator.generate(ast)

    optimizer = IROptimizer()
    opt_ir = optimizer.optimize(ir_prog)
    instructions = opt_ir.get_instructions()

    # The resulting code should propagate x=10 into x+5, folding it to 15.
    # Instruction 1: x = 10
    # Instruction 2: y = 15
    assert len(instructions) == 3
    assert instructions[0].op == "ASSIGN"
    assert instructions[0].arg1 == 10
    assert instructions[0].result == "x"
    
    assert instructions[1].op == "ASSIGN"
    assert instructions[1].arg1 == 15
    assert instructions[1].result == "t1"

    assert instructions[2].op == "ASSIGN"
    assert instructions[2].arg1 == 15
    assert instructions[2].result == "y"
