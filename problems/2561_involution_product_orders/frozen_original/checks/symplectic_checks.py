"""Direct finite-field checks of the transvection/affine-hyperplane proof."""
from colored_involutions import *

class Field:
    def __init__(self,q,poly):self.q=q;self.poly=poly
    def mul(self,a,b):
        c=0
        while b:
            if b&1:c^=a
            b>>=1;a<<=1
            if a&self.q:a^=self.poly
        return c

def check(q,poly,dim,enumerate_aut=False):
    F=Field(q,poly)
    V=[x for x in product(range(q),repeat=dim) if any(x)]
    pos={x:i for i,x in enumerate(V)}
    def B(x,y):
        t=0
        for i in range(0,dim,2):t^=F.mul(x[i],y[i+1])^F.mul(x[i+1],y[i])
        return t
    D=[]
    for v in V:
        p=[]
        for x in V:
            b=B(x,v);p.append(pos[tuple(xi^F.mul(b,vi) for xi,vi in zip(x,v))])
        D.append(tuple(p))
    M,C=tables(D);N=[{j for j in range(len(V)) if B(v,V[j])==1} for v in V]
    for i,v in enumerate(V):
        assert len(N[i])==q**(dim-1)
        assert order(D[i])==2
        for j,w in enumerate(V):
            assert (M[i][j]==3)==(B(v,w)==1)
            if i!=j:assert (M[i][j]==2)==(B(v,w)==0)
            if i<j:
                prop=any(tuple(F.mul(c,t) for t in v)==w for c in range(1,q))
                assert (not(N[i]&N[j]))==prop
    result={'q':q,'dimension':dim,'vertices':len(V),'colors':sorted(set(sum(M,[]))),'all_pair_order_and_hyperplane_tests_pass':True}
    if enumerate_aut:result['full_colored_graph']=solve(M,C)
    return result

if __name__=='__main__':
    out=[]
    for args in [(2,3,4,False),(2,3,6,False),(4,7,2,True),(8,11,2,True)]:
        r=check(*args);out.append(r);print(json.dumps(r),flush=True)
    json.dump(out,open('symplectic_results.json','w'),indent=2)
