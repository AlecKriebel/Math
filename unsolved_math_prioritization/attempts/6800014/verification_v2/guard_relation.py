"""Check the exact original-to-current AST relation; no assertions are used."""
import ast

PATH_COUNTS = {"verify.py": 19, "check_hessian.py": 2,
               "audit/independent_checks.py": 18}
RUNTIME_COUNTS = {"verify.py": 24, "check_hessian.py": 2,
                  "audit/independent_checks.py": 28}


def relation(original, candidate, path):
    before = ast.parse(original)
    nodes = sorted((n for n in ast.walk(before) if isinstance(n, ast.Assert)),
                   key=lambda n: (n.lineno, n.col_offset))
    if len(nodes) != PATH_COUNTS[path] or any(n.msg is not None for n in nodes):
        raise RuntimeError("unexpected original checkpoint inventory: " + path)
    ordinal = {id(n): i for i, n in enumerate(nodes, 1)}

    class Replace(ast.NodeTransformer):
        def visit_Assert(self, node):
            return ast.If(
                test=ast.UnaryOp(op=ast.Not(), operand=node.test),
                body=[ast.Raise(exc=ast.Call(
                    func=ast.Name(id="AssertionError", ctx=ast.Load()),
                    args=[ast.Constant(value="mandatory checkpoint " + path + ":" +
                                       str(ordinal[id(node)]))], keywords=[]), cause=None)],
                orelse=[])

    expected = Replace().visit(before)
    after = ast.parse(candidate)
    if any(isinstance(n, ast.Assert) for n in ast.walk(after)):
        raise RuntimeError("removable current assertion: " + path)
    if ast.dump(expected, include_attributes=False) != ast.dump(after, include_attributes=False):
        raise RuntimeError("current code differs beyond mandatory guard replacement: " + path)
    return {"path": path, "static_checkpoints": len(nodes),
            "runtime_checkpoints": RUNTIME_COUNTS[path],
            "exact_ast_relation": True, "original_messages": "none",
            "evaluation": "same predicate once, original short circuit; diagnostic only on failure"}
