"""Exact source-scope control; Python -B, existing Sympy only."""
import sys, json
from pathlib import Path
from datetime import datetime,timezone
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'pr200_5100007/math_algebra_family_01/runtime_packages'))
import sympy as s
R=s.Rational
def det(p,q): return s.expand(p[0]*q[1]-p[1]*q[0])
def area(v): return s.simplify(sum(det(v[i],v[(i+1)%len(v)]) for i in range(len(v)))/2)
beta=s.sqrt(5)/3; alpha=4*s.sqrt(2)/3
right=[(2,0),(R(4,3),beta),(-R(4,3),beta),(-2,0),(-R(4,3),-beta),(R(4,3),-beta)]
top=[(0,1),(-alpha,R(1,3)),(-alpha,-R(1,3)),(0,-1),(alpha,-R(1,3)),(alpha,R(1,3))]
results=[]
for name,P in [('right',right),('top',top)]:
    Q=[];checks=[]
    for i,p in enumerate(P):
        q=P[(i+1)%6]; z=det(p,q); n=((q[1]-p[1])/z,(p[0]-q[0])/z)
        n2=s.simplify(n[0]**2+n[1]**2);Q.append(tuple(s.simplify(x/n2) for x in n))
        checks.append(s.simplify(alpha**2*n[0]**2+beta**2*n[1]**2-1))
        assert checks[-1]==0
        assert s.simplify(s.sympify(p[0])**2/4+s.sympify(p[1])**2-1)==0
    A=area(P);B=area(Q);D=s.simplify(area(P+P)*area(Q+Q))
    results.append({'phase':name,'A':str(A),'B_0':str(B),'twelve_entry_product':str(D),'tangency_residuals':[str(x) for x in checks]})
assert s.simplify(s.sympify(results[1]['twelve_entry_product'])-s.sympify(results[0]['twelve_entry_product']))==R(448,243)
out={'utc':datetime.now(timezone.utc).isoformat(),'sympy':s.__version__,'outer_axes':[2,1],'caustic_axes':[str(alpha),str(beta)],'lambda':'4/9','primitive_period':6,'displayed_list_length':12,'M':[0,0],'phases':results,'exact_product_difference':'448/243','scope':'Refutes broader displayed-list-length reading, not the explicit primitive theorem.'}
Path(__file__).with_name('exact_repeated_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
