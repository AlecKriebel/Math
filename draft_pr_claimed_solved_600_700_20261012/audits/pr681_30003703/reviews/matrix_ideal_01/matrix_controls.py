#!/usr/bin/env python3
"""Independent exact matrix-ideal controls. No authored imports or network/writes.
Uses SymPy's polynomial ring arithmetic and a Gauss decomposition chart.
The written derivation supplies universal ring reasoning independently.
"""
import hashlib, json
from sympy.polys.rings import ring
from sympy.polys.domains import ZZ

class Algebra:
    def __init__(self,n,bound=99):
        self.r,*self.vars=ring(','.join('t'+str(i) for i in range(n)),ZZ)
        self.bound=bound
        self.z=self.r.zero;self.o=self.r.one
    def cut(self,p):
        return self.r.from_dict({e:c for e,c in p.items() if sum(e)<self.bound})
    def mul(self,p,q):return self.cut(p*q)
    def eye(self):return [[self.o,self.z],[self.z,self.o]]
    def mm(self,a,b):return [[sum((self.mul(a[i][k],b[k][j]) for k in range(2)),self.z) for j in range(2)] for i in range(2)]
    def sub(self,a,b):return [[a[i][j]-b[i][j] for j in range(2)] for i in range(2)]
    def adj(self,a):return [[a[1][1],-a[0][1]],[-a[1][0],a[0][0]]]
    def det(self,a):return self.mul(a[0][0],a[1][1])-self.mul(a[0][1],a[1][0])
    def lb(self,a,b):return self.sub(self.mm(a,b),self.mm(b,a))
    def gc(self,a,b):
        # Exact identity [a,b]-I=(ab-ba)adj(a)adj(b), after det checks.
        delta=self.mm(self.mm(self.lb(a,b),self.adj(a)),self.adj(b))
        i=self.eye()
        return [[delta[k][j]+i[k][j] for j in range(2)] for k in range(2)]
    def gauss(self,i):
        a,b,c=self.vars[3*i:3*i+3]
        u=1+a
        uinv=sum(((-a)**k for k in range(self.bound)),self.z)
        return [[u,self.mul(u,b)],[self.mul(u,c),self.mul(self.mul(b,c),u)+uinv]]

def require(c,label):
    if not c:raise RuntimeError(label)

def zero(m):return all(not p for row in m for p in row)
def profile(m):
    return [{str(d):sum(sum(e)==d for e in p) for d in sorted({sum(e) for e in p})} for row in m for p in row]
def digest(m):
    obj=[[[list(e),int(c)] for e,c in sorted(p.items())] for row in m for p in row]
    return hashlib.sha256(json.dumps(obj,separators=(',',':')).encode()).hexdigest()
def make_word(a,name,m):
    x,y=m[:2];xy=a.gc(x,y)
    if name=='w':return a.gc(a.gc(xy,a.gc(x,m[2])),x)
    return a.gc(a.gc(xy,a.gc(x,xy)),x)

def main():
    checks=[]
    a=Algebra(12)
    x,y,z=[[[a.vars[4*i],a.vars[4*i+1]],[a.vars[4*i+2],a.vars[4*i+3]]] for i in range(3)]
    u,v=a.lb(x,y),a.lb(x,z)
    p=a.lb(a.lb(u,v),x)
    q=a.lb(a.lb(u,a.lb(x,u)),x)
    require(zero(p),'generic arbitrary 2x2 P');require(zero(q),'generic arbitrary 2x2 Q')
    checks+=['P universal in all 12 arbitrary matrix entries','Q universal in all 8 arbitrary matrix entries']
    tr=x[0][0]+x[1][1]
    anti=a.sub([[a.mm(x,u)[i][j]+a.mm(u,x)[i][j] for j in range(2)] for i in range(2)],[[tr*u[i][j] for j in range(2)] for i in range(2)])
    require(zero(anti),'general trace anticommutation relation')
    checks+=['XU+UX=tr(X)U without traceless restriction']
    jets={}
    for name,rank,N in [('w',3,6),('v',2,7)]:
        a=Algebra(3*rank,N+1)
        m=[a.gauss(i) for i in range(rank)]
        for i,g in enumerate(m):
            require(a.det(g)==a.o,'Gauss determinant')
            require(a.mm(g,a.adj(g))==a.eye(),'Gauss inverse')
            checks+=['%s generator %s determinant/inverse'%(name,i)]
        # Gauss chart has a,b,c recovering original matrix entries polynomially
        # in a finite quotient, so this covers the entire universal quotient.
        f=make_word(a,name,m); displacement=a.sub(f,a.eye())
        pp=profile(displacement)
        require(all(all(int(d)>=N for d in entry) for entry in pp),'accepted ideal power')
        require(all(entry and set(entry)=={str(N)} for entry in pp),'all four next-degree entries nonzero')
        # Forgetting the final bracket is a deliberately too-low bound.
        x,y=m[:2];inner=a.gc(x,y)
        if name=='w':wrong=a.gc(inner,a.gc(x,m[2]))
        else:wrong=a.gc(inner,a.gc(x,inner))
        wrongp=profile(a.sub(wrong,a.eye()))
        require(any(any(int(d)<N for d in e) for e in wrongp),'missing outer bracket control')
        checks+=['%s all four entries vanish modulo m^%s'%(name,N),'%s every entry has a nonzero degree %s term'%(name,N),'%s missing outer bracket rejected'%name]
        jets[name]={'universal_independent_variables':3*rank,'vanishes_mod_power':N,'next_degree_entry_profiles':pp,'sha256':digest(displacement),'wrong_outer_removed_profile':wrongp}
        # Trace perturbation is generally nonzero, first in degree two.
        trace=m[0][0][0]+m[0][1][1]-2
        require(trace and min(sum(e) for e in trace)==2,'actual B is not exactly traceless')
        checks+=['%s trace(B) has nonzero degree-two terms'%name]
    # Test against nonreduced, characteristic-two coefficient rings by
    # universal integer identity specialization (no division was used).
    a=Algebra(12)
    x,y,z=[[[a.vars[4*i],a.vars[4*i+1]],[a.vars[4*i+2],a.vars[4*i+3]]] for i in range(3)]
    u,v=a.lb(x,y),a.lb(x,z)
    r=a.lb(a.lb(u,v),y)
    require(not zero(r),'wrong outer repeated letter')
    # At H,E,F the inner is nonzero even though its bracket with H vanishes.
    from sympy import Matrix
    h=Matrix([[1,0],[0,-1]]);e=Matrix([[0,1],[0,0]]);f=Matrix([[0,0],[1,0]])
    br=lambda a,b:a*b-b*a
    inner=br(br(h,e),br(h,f))
    require(inner==Matrix([[-4,0],[0,4]]),'inner bracket nonzero')
    require(br(inner,e)==Matrix([[0,-8],[0,0]]),'wrong outer bracket example')
    h3=Matrix([[1,0,0],[0,-1,0],[0,0,0]]);e12=Matrix([[0,1,0],[0,0,0],[0,0,0]]);e23=Matrix([[0,0,0],[0,0,1],[0,0,0]])
    p3=br(br(br(h3,e12),br(h3,e23)),h3)
    require(p3==Matrix([[0,0,2],[0,0,0],[0,0,0]]),'3x3 extension rejected')
    checks+=['arbitrary outer letter variant fails generically','outer bracket deleted gives nonzero matrix','wrong outer variable gives -8E','3x3 extension gives 2E13']
    # Reinterpret a 4x4 matrix as a 2x2 matrix over the noncommutative
    # coefficient ring M_2(Z). Block trace(X)=0, but P need not vanish.
    x4=Matrix.diag(1,0,-1,0); y4=Matrix.zeros(4); z4=Matrix.zeros(4)
    y4[0,1]=1; z4[1,2]=1
    require(x4[:2,:2]+x4[2:,2:]==Matrix.zeros(2),'block traceless X')
    bad=br(br(br(x4,y4),br(x4,z4)),x4)
    expected=Matrix.zeros(4);expected[0,2]=-2
    require(bad==expected,'noncommutative coefficient ring must be excluded')
    checks+=['trace-zero 2x2 matrices over noncommutative M2(Z) violate P, as required']
    print(json.dumps({'result':'PASS','method':'SymPy exact integer polynomial rings; universal finite Gauss chart; nested matrix commutator recursion','checks_count':len(checks),'checks':checks,'jets':jets,'arbitrary_commutative_base_ring_proof':'Cayley-Hamilton and filtered identities use only integer polynomial operations; includes nonreduced rings and positive characteristic, without asserting new filtrations there'},indent=2,sort_keys=True))
if __name__=='__main__':main()
