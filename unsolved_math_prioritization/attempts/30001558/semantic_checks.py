"""Independent finite regression controls; not a substitute for the infinite proof."""
import ast

def require(ok, label):
    if not ok: raise ValueError(label)

def function(source, name):
    tree = ast.parse(source)
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name]
    require(len(nodes) == 1, 'unique function '+name)
    ns = {}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), '<independent-control>', 'exec'), ns)
    return ns[name]

def check(name, source):
    if name == 'frozen32.py':
        app = function(source, 'app')
        for s in ['', '0', '01', '010', '012', '01201', '01021']:
            for a in '012':
                v = s+a
                want = not any(v[-2*p:-p] == v[-p:] for p in range(1,len(v)//2+1))
                require(app(s,a) == want, 'suffix square predicate')
    elif name == 'backward.py':
        prep = function(source, 'prep')
        for s in ['', '0', '01', '010', '012', '01201', '01021']:
            for a in '012':
                v = a+s
                want = not any(v[:p] == v[p:2*p] for p in range(1,len(v)//2+1))
                require(prep(a,s) == want, 'prefix square predicate')
    elif name == 'linear.py':
        zfun = function(source, 'zfun')
        for s in ['', '0', '00000', '012012', '212012101202', 'abacaba']:
            expected = [0]*len(s)
            for i in range(1,len(s)):
                while i+expected[i] < len(s) and s[expected[i]] == s[i+expected[i]]:
                    expected[i] += 1
            require(zfun(s) == expected, 'Z-array oracle')
