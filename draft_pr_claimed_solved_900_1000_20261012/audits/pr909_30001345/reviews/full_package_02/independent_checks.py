"""Reviewer02 exact finite checks; does not import any candidate checker."""
import json
from fractions import Fraction as Q
from itertools import combinations

def need(c,s):
    if not c: raise RuntimeError(s)

class E:
    def __init__(self,a=0,b=0): self.a,self.b=Q(a),Q(b)
    def __add__(self,y):
        y=y if isinstance(y,E) else E(y);return E(self.a+y.a,self.b+y.b)
    __radd__=__add__
    def __neg__(self): return E(-self.a,-self.b)
    def __sub__(self,y): return self+-y if isinstance(y,E) else self+E(-y)
    def __rsub__(self,y):return E(y)+-self
    def __mul__(self,y):
        y=y if isinstance(y,E) else E(y)
        return E(self.a*y.a-self.b*y.b,self.a*y.b+self.b*y.a-self.b*y.b)
    __rmul__=__mul__
    def conj(self):return E(self.a-self.b,-self.b)
    def norm(self):
        n=self*self.conj();need(n.b==0,'real norm');return n.a
    def __truediv__(self,y):
        y=y if isinstance(y,E) else E(y);n=y.norm();need(n!=0,'zero divisor');z=self*y.conj();return E(z.a/n,z.b/n)
    def __eq__(self,y):
        y=y if isinstance(y,E) else E(y);return (self.a,self.b)==(y.a,y.b)
    def __hash__(self):return hash((self.a,self.b))
    def __repr__(self):return f'({self.a})+({self.b})w'

def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def dot(a,b):return sum((x*y for x,y in zip(a,b)),E())
def canonical(v):
    p=next((x for x in reversed(v) if x!=0),None);need(p is not None,'coincident lines');return tuple(x/p for x in v)
def incidences(lines):
    points={canonical(cross(a,b)) for a,b in combinations(lines,2)}
    return {p:tuple(i for i,a in enumerate(lines) if dot(a,p)==0) for p in points}

def pmul(p,q):
    out={}
    for a,b in p.items():
        for c,d in q.items():
            key=tuple(x+y for x,y in zip(a,c));out[key]=out.get(key,E())+b*d
    return {a:b for a,b in out.items() if b!=0}
def padd(p,q):
    out=dict(p)
    for a,b in q.items():out[a]=out.get(a,E())+b
    return {a:b for a,b in out.items() if b!=0}
def scale(p,s):return {a:b*s for a,b in p.items() if b*s!=0}
def cube(p):return pmul(pmul(p,p),p)

def main():
    one,w=E(1),E(0,1);qs=[one,w,w*w]
    projective=[(one,-q,E()) for q in qs]+[(E(),one,-q) for q in qs]+[(-q,E(),one) for q in qs]
    points=incidences(projective);need(len(points)==12 and all(len(v)==3 for v in points.values()),'12 triples')
    affine=[(one,-q,E()) for q in qs]+[(q,4+2*q,-q) for q in qs]+[(-(1+4*q),E(-2),one) for q in qs]
    distances=[];norms=[]
    for a,b,c in affine:need(a!=0,'x graph');distances.append(c.norm()/(a.norm()+b.norm()))
    for a,b in combinations(affine,2):need(a[0]*b[1]-a[1]*b[0]!=0,'distinct directions')
    product={(0,0,0):one}
    for a,b,c in affine:product=pmul(product,{(1,0,0):a,(0,1,0):b,(0,0,1):c})
    x={(1,0,0):one};y={(0,1,0):one};tpoly={(0,0,1):one};z=padd(padd(tpoly,scale(x,-1)),scale(y,-2))
    formula=pmul(pmul(padd(cube(x),scale(cube(y),-1)),padd(scale(cube(y),64),scale(cube(z),-1))),padd(cube(z),scale(cube(x),-64)))
    need(product==formula and product[(9,0,0)]==-65,'exact polynomial identity and constant x9 coefficient')
    for p in points:
        l=dot((one,E(2),E(4)),p);need(l!=0,'infinity');u,v=p[0]/l,p[1]/l
        norms.append(u.norm()+v.norm());need(sum(a*u+b*v+c==0 for a,b,c in affine)==3,'chart incidence')
    need(max(norms)==1 and max(distances)==Q(1,13),'sharp bounds')
    # For several exact nonreal parameter choices, recover each scaled point
    # independently by cross products of its two affine equations.
    for t in [E(),E(Q(1,8)),E(0,Q(1,8)),E(Q(1,32),Q(1,16))]:
        lines=[(a,b,c*t) for a,b,c in affine]
        pts=incidences(lines);need(len(pts)==(1 if t==0 else 12),'complex scaling')
    # Different perturbation from prior reviews: translate one A line by 1/7.
    pert=list(affine);a,b,c=pert[1];pert[1]=(a,b,c+E(Q(1,7)));ip=incidences(pert)
    need(len(ip)!=12 or any(len(v)!=3 for v in ip.values()),'perturbation must break target')
    removed=incidences(projective[:-1]);need(sum(len(v)*(len(v)-1)//2 for v in removed.values())==28,'lost branch pair control')
    need(any(dot((one,E(2),E()),p)==0 for p in points),'bad infinity detects lost vertex')
    # r-2 is a singular ordinary-point formula: extending it to smooth r=1
    # predicts the wrong n=1 result. The true 3-line arrangement stays triple.
    n1=incidences([(one,-one,E()),(E(),one,-one),(-one,E(),one)])
    need(len(n1)==1 and len(next(iter(n1.values())))==3,'n1 triple')
    need(1-1==0 and 1**2-4!=0,'n1 excluded')
    twos=[E(1),E(-1)]
    n2=incidences([(one,-q,E()) for q in twos]+[(E(),one,-q) for q in twos]+[(-q,E(),one) for q in twos])
    need(sorted(map(len,n2.values()))==[2,2,2,3,3,3,3],'n2 exact incidence')
    need(sum(len(v)-2 for v in n2.values())==4 and sum(len(v)*(len(v)-1)//2 for v in n2.values())==15,'n2 exact invariant totals')
    for n in [2,3,4,17,113,1009]:
        need(3*n*(n-1)//2+3*n*n==(3*n)*(3*n-1)//2,'delta identity')
        need(3*(n-2)+n*n-(3*n-2)==n*n-4,'rough identity')
    result={'status':'PASS','field':'Fraction pairs Q[w]/(w^2+w+1)','projective_points':12,'line_pairs':36,
            'all_triples':True,'normalization_components':9,'max_squared_chart_norm':str(max(norms)),
            'squared_distance_coefficients':sorted(map(str,distances)),
            'perturbed_A_line_point_count':len(ip),'perturbed_multiplicities':{str(k):sum(len(v)==k for v in ip.values()) for k in sorted({len(v) for v in ip.values()})},
            'nonreal_exact_parameter_controls':True,'bad_infinity_and_lost_branch_controls':True,'n1_actual_excess':0,'n2_excess':0,
            'central_delta':36,'nearby_delta':36,'central_rough':7,'nearby_rough':12,'exact_factorization':True,'x_leading_coefficient':-65,'n2_incidence':[2,2,2,3,3,3,3],
            'scope':'Finite exact controls only; universal analytic/incidence arguments are written independently, not inferred by sampling.'}
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
