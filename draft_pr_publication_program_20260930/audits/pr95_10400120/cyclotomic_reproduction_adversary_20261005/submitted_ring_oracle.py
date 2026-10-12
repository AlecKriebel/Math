import ast,json,random,itertools
from pathlib import Path
import sympy as sp
src=Path(__file__).parent/'private_original/verify.py'
sel=[]
for n in ast.parse(src.read_text()).body:
 if isinstance(n,(ast.Import,ast.ImportFrom)):sel.append(n)
 if isinstance(n,ast.FunctionDef) and n.name in {'red','mul','shift','conj'}:sel.append(n)
 if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='MON' for t in n.targets):sel.append(n)
ns={};exec(compile(ast.Module(body=sel,type_ignores=[]),str(src),'exec'),ns)
x=sp.Symbol('x');phi=sp.Poly(sp.cyclotomic_poly(100,x),x);rng=random.Random(95);checks=0
def verify(p,label):
 global checks
 if not p:raise RuntimeError(label)
 checks+=1
def vec(p):return [int(p.nth(j)) for j in range(40)]
def poly(a):return sp.Poly(sum(int(c)*x**j for j,c in enumerate(a)),x)
for j in range(100):verify(list(ns['MON'][j])==vec(sp.rem(sp.Poly(x**j,x),phi)),'monomial reduction')
for _ in range(50):
 a=[rng.randrange(-100,101) for i in range(rng.randrange(40,140))];b=[rng.randrange(-10,11) for i in range(40)]
 ar=ns['red'](a);verify(list(ar)==vec(sp.rem(poly(a),phi)),'high degree reduction')
 verify(list(ns['mul'](ar,b))==vec(sp.rem(poly(a)*poly(b),phi)),'convolution product')
 verify(list(ns['conj'](ar))==vec(sp.rem(sp.Poly(sum(int(c)*x**((-j)%100) for j,c in enumerate(ar)),x),phi)),'conjugation')
 for k in [-10001,-1,0,37,10000]:verify(list(ns['shift'](ar,k))==vec(sp.rem(poly(ar)*sp.Poly(x**(k%100),x),phi)),'cyclic shift')
print(json.dumps({'status':'PASS','explicit_oracle_checks':checks,'oracle':'Native SymPy1.14 independently generated Phi100 and polynomial remainder; submitted function AST excerpts only, no matrix author execution.'}))
