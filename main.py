import sys
import os
import json
import http.server
import socketserver
import webbrowser
import threading
from src.compiler.compiler import Compiler
from src.lexer.lexer import LexerError
from src.parser.parser import ParserError
from src.semantic.semantic_analyzer import SemanticError

compiler = Compiler()

def print_terminal_pipeline(phases: dict):
    print("\n" + "=" * 40)
    print("          ML MATH COMPILER")
    print("========================================")
    
    print("\n[1] SOURCE CODE")
    print("-" * 40)
    print(phases.get("source", ""))

    print("\n[2] LEXICAL ANALYSIS")
    print("-" * 40)
    print(phases.get("tokens", ""))

    print("\n[3] SYNTAX ANALYSIS")
    print("-" * 40)
    print(phases.get("syntax", ""))

    print("\n[4] AST")
    print("-" * 40)
    print(phases.get("ast", ""))

    print("\n[5] SEMANTIC ANALYSIS")
    print("-" * 40)
    print(phases.get("semantic", ""))

    print("\n[6] SYMBOL TABLE")
    print("-" * 40)
    print(phases.get("symbols", ""))

    print("\n[7] ML CLASSIFICATION")
    print("-" * 40)
    print(phases.get("ml_text", ""))

    print("\n[8] INTERMEDIATE REPRESENTATION")
    print("-" * 40)
    print(phases.get("ir", ""))

    print("\n[9] OPTIMIZATION")
    print("-" * 40)
    print(phases.get("opt_ir", ""))

    print("\n[10] EXECUTION")
    print("-" * 40)
    print(phases.get("execution", ""))

    print("\n" + "=" * 40)
    print("FINAL RESULT")
    print("========================================")
    print(phases.get("execution", ""))
    print("=" * 40 + "\n")

class CompilerHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        web_dir = os.path.join(os.path.dirname(__file__), "web")
        super().__init__(*args, directory=web_dir, **kwargs)

    def do_POST(self):
        if self.path == "/api/compile":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length).decode("utf-8")
            try:
                req_json = json.loads(post_data)
                source_code = req_json.get("source", "")
                
                phase_data = compiler.get_phase_outputs(source_code)
                print_terminal_pipeline(phase_data)

                response = {
                    "success": True,
                    "data": phase_data
                }
            except (LexerError, ParserError, SemanticError) as err:
                response = {
                    "success": False,
                    "error": str(err)
                }
                print("\n[COMPILATION ERROR]")
                print(str(err))
            except Exception as e:
                response = {
                    "success": False,
                    "error": f"Runtime / Compilation Error: {str(e)}"
                }
                print(f"\n[ERROR] {e}")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))
        else:
            self.send_error(404, "Endpoint not found")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

def start_server(port: int = 5000):
    handler = CompilerHTTPHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"\n* ML Math Compiler Web Server running at http://localhost:{port}")
        print("* Ready to compile programs from the browser!\n")
        httpd.serve_forever()

def main():
    if len(sys.argv) > 1 and not sys.argv[1].startswith("--") and os.path.exists(sys.argv[1]):
        # File mode (CLI)
        with open(sys.argv[1], "r") as f:
            source = f.read()
        try:
            phases = compiler.get_phase_outputs(source)
            print_terminal_pipeline(phases)
        except Exception as e:
            print(f"\nError: {e}")
            sys.exit(1)
        return

    # Web App mode (Default)
    port = 5000
    print("Starting ML Math Compiler...")
    start_server(port)

if __name__ == "__main__":
    main()
