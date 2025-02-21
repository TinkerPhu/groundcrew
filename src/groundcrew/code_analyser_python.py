import ast

def extract_python_from_file(file_text, node_types):
    file_lines = file_text.split('\n')
    texts = {}

    class NodeVisitor(ast.NodeVisitor):
        def __init__(self):
            self.current_class = None

        def update_texts(self, node, key):
            texts[key] = {
                'text': '\n'.join(file_lines[node.lineno - 1:node.end_lineno]),
                'start_line': node.lineno,
                'end_line': node.end_lineno,
                'is_method': self.current_class is not None,
                'is_class': isinstance(node, ast.ClassDef)
            }

        def visit_ClassDef(self, node):
            if ast.ClassDef == node_types:
                self.update_texts(node, node.name)
            self.current_class = node.name
            self.generic_visit(node)
            self.current_class = None

        def visit_FunctionDef(self, node):
            if ast.FunctionDef == node_types:
                key = f"{self.current_class}.{node.name}" if self.current_class else node.name
                self.update_texts(node, key)
            self.generic_visit(node)

    visitor = NodeVisitor()
    visitor.visit(ast.parse(file_text))

    return texts


