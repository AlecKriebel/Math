"""Exact polynomial check of source-comparison substitutions; Python standard library."""
import json
from pathlib import Path
class P:
    def __init__(self, terms=None): self.t = {m:c for m,c in (terms or {}).items() if c}
    @staticmethod
    def coerce(v): return v if isinstance(v,P) else P({(0,0,0,0):v})
    def __add__(self,v):
        r=self.t.copy()
        for m,c in self.coerce(v).t.items(): r[m]=r.get(m,0)+c
        return P(r)
    __radd__=__add__
    def __neg__(self): return P({m:-c for m,c in self.t.items()})
    def __sub__(self,v): return self+-self.coerce(v)
    def __rsub__(self,v): return self.coerce(v)+-self
    def __mul__(self,v):
        r={}
        for m,c in self.t.items():
            for n,d in self.coerce(v).t.items():
                z=tuple(i+j for i,j in zip(m,n)); r[z]=r.get(z,0)+c*d
        return P(r)
    __rmul__=__mul__
    def __pow__(self,n):
        r=P.coerce(1)
        for _ in range(n): r=r*self
        return r
    def derivative(self,k):
        r={}
        for m,c in self.t.items():
            if m[k]:
                n=list(m); n[k]-=1; r[tuple(n)]=c*m[k]
        return P(r)
a,b,c,s=(P({tuple(int(j==i) for j in range(4)):1}) for i in range(4))
D=a*(b+c)
results={}
for name,N,Q in [('negative',-a*(b+c)+c*(a-b)*s**2,(b+c)+(a-b)*s**2),('positive',a*c*(1-s**2),a+c*s**2)]:
    W=N.derivative(3)*Q-N*Q.derivative(3)
    R=N*(N+a*Q)*(N+b*Q)*(N-c*Q)
    residue=W**2*(1-s**2)*(D-c*(a-b)*s**2)+4*R
    results[name+'_jacobian_square_exact']=not residue.t
results['connection_rhs_exact']=not ((a+c)**2-(b+c+a-b)*(a+c)).t
results['scope']='Exact multivariate polynomial verification of rational substitutions only.'
Path(__file__).with_name('equivalence_check.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results))
assert all(v for k,v in results.items() if k.endswith('_exact'))
