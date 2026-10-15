#!/usr/bin/env python3
"""Independent exact 4D connection/curvature checks; no author-code imports."""
from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path
D=4
ZERO=Q(0)
COUNT=0

def require(condition, message):
    global COUNT
    COUNT += 1
    if not condition:
        raise RuntimeError(message)

class Jet:
    def __init__(self,v,g=None,h=None):
        self.v=Q(v)
        self.g=[ZERO]*D if g is None else list(g)
        self.h=[[ZERO]*D for _ in range(D)] if h is None else [list(x) for x in h]
    def __add__(self,o):
        if not isinstance(o,Jet): o=Jet(o)
        return Jet(self.v+o.v,[self.g[i]+o.g[i] for i in range(D)],[[self.h[i][j]+o.h[i][j] for j in range(D)] for i in range(D)])
    __radd__=__add__
    def __neg__(self): return self*(-1)
    def __sub__(self,o): return self+(-o if isinstance(o,Jet) else -Q(o))
    def __rsub__(self,o): return -self+o
    def __mul__(self,o):
        if not isinstance(o,Jet): o=Jet(o)
        return Jet(self.v*o.v,[self.g[i]*o.v+self.v*o.g[i] for i in range(D)],[[self.h[i][j]*o.v+self.v*o.h[i][j]+self.g[i]*o.g[j]+self.g[j]*o.g[i] for j in range(D)] for i in range(D)])
    __rmul__=__mul__
    def recip(self):
        v=self.v
        return Jet(1/v,[-x/v**2 for x in self.g],[[2*self.g[i]*self.g[j]/v**3-self.h[i][j]/v**2 for j in range(D)] for i in range(D)])
    def __truediv__(self,o): return self*(o.recip() if isinstance(o,Jet) else 1/Q(o))
    def __rtruediv__(self,o): return self.recip()*o
    def __pow__(self,k):
        if k<0: return self.recip()**(-k)
        out=Jet(1)
        for _ in range(k): out=out*self
        return out

def curvature(a,r,A,B,n):
    rhog=[ZERO]+list(n)
    rhoh=[[ZERO]*D for _ in range(D)]
    for i,j in product(range(3),repeat=2):rhoh[i+1][j+1]=(Q(i==j)-n[i]*n[j])/r
    rho=Jet(r,rhog,rhoh)
    phi=1-a/rho
    N=A+B*(rho+a)/(rho-a)
    diag=[-N*N]+[phi**4]*3
    inv=[x.recip() for x in diag]
    # A diagonal metric has Gamma^l_ij = 1/2 g^ll(d_i g_jl + d_j g_il - d_l g_ij).
    C=[[[ZERO]*D for _ in range(D)] for _ in range(D)]
    dC=[[[[ZERO]*D for _ in range(D)] for _ in range(D)] for _ in range(D)]
    for l,i,j in product(range(D),repeat=3):
        q=(diag[l].g[i] if j==l else ZERO)+(diag[l].g[j] if i==l else ZERO)-(diag[i].g[l] if i==j else ZERO)
        C[l][i][j]=inv[l].v*q/2
        for k in range(D):
            dq=(diag[l].h[i][k] if j==l else ZERO)+(diag[l].h[j][k] if i==l else ZERO)-(diag[i].h[l][k] if i==j else ZERO)
            dC[k][l][i][j]=(inv[l].g[k]*q+inv[l].v*dq)/2
    Ric=[[ZERO]*D for _ in range(D)]
    for i,j in product(range(D),repeat=2):
        Ric[i][j]=sum(dC[k][k][i][j]-dC[j][k][i][k] for k in range(D))+sum(C[k][i][j]*C[l][k][l]-C[l][i][k]*C[k][j][l] for k,l in product(range(D),repeat=2))
    R=sum(inv[i].v*Ric[i][i] for i in range(D))
    Gcov=[[Ric[i][j]-(diag[i].v*R/2 if i==j else ZERO) for j in range(D)] for i in range(D)]
    Gmix=[[inv[i].v*Gcov[i][j] for j in range(D)] for i in range(D)]
    ph=phi.v
    nv=N.v
    require(R==0,'scalar curvature')
    for i,j in product(range(D),repeat=2):
        expected=ZERO if i==0 or j==0 else A/nv*a/(r**3*ph**6)*(6*n[i-1]*n[j-1]-2*Q(i==j))
        require(Gmix[i][j]==expected,'mixed Einstein component')
        require(Ric[i][j]==Ric[j][i],'Ricci symmetry')
    density=nv*ph**6
    for k in range(D):require(sum(Gmix[i][j]*C[j][i][k] for i,j in product(range(D),repeat=2))==0,'total connection contraction cancellation')
    # Arbitrary vector values and first derivatives test index placement and density.
    vec=[Q(2),Q(-3),Q(5,2),Q(-7,3)]
    partial=[[Q((i+1)*(j+2)-5,7) for j in range(D)] for i in range(D)]
    nabla=[[partial[i][j]+sum(C[j][i][k]*vec[k] for k in range(D)) for j in range(D)] for i in range(D)]
    scalar=sum(Gmix[i][j]*nabla[i][j] for i,j in product(range(D),repeat=2))
    raised=sum(Gcov[i][j]*inv[i].v*nabla[i][j] for i,j in product(range(D),repeat=2))
    target=sum(a*A/r**3*(6*n[i-1]*n[j-1]-2*Q(i==j))*partial[i][j] for i,j in product(range(1,D),repeat=2))
    require(scalar==raised,'covariant/mixed scalar equality')
    require(density*scalar==target,'arbitrary-field density')
    if A==0: require(all(x==0 for row in Gcov for x in row),'vacuum endpoint')
    if A==B==Q(1,2):
        square=sum(inv[i].v*inv[j].v*Ric[i][j]**2 for i,j in product(range(D),repeat=2))
        require(square==6*a*a/(r**6*ph**10),'candidate invariant blow-up coefficient')
    return {'a':str(a),'r':str(r),'A':str(A),'B':str(B),'direction':[str(x) for x in n],'density':str(density),'full_scalar_density':str(target)}

def main():
    records=[]
    directions=[(Q(1),Q(0),Q(0)),(Q(3,5),Q(4,5),Q(0)),(Q(2,3),Q(-2,3),Q(1,3))]
    for a,ratio,(A,B),n in product([Q(1),Q(2,3)], [Q(1001,1000),Q(3,2),Q(5)], [(Q(1,2),Q(1,2)),(Q(0),Q(1)),(Q(1),Q(0)),(Q(2),Q(3))],directions):
        records.append(curvature(a,a*ratio,A,B,n))
    # Independent radial surface flux, divergence, and near-boundary individual terms.
    for a,r,A in product([Q(1),Q(2,3)],[Q(1001,1000),Q(3,2),Q(7)], [Q(0),Q(1,2),Q(2)]):
        r=a*r
        Dr=4*A*a/r**3; Dt=-2*A*a/r**3
        require(-12*A*a/r**4+2*(Dr-Dt)/r==0,'Euclidean divergence')
        require(-(4*A*a/a**3)*a*a==-4*A,'inner boundary flux per solid angle')
        require(4*A*a*((-1/r**2))==-4*A*a/r**2,'constant radial test density')
    # N=phi^-1: for chi=1 the radial and two angular connection densities
    # are respectively 4a phi'/(rho phi), -2a phi'/(rho phi) each.
    for a,x in product([Q(1),Q(2,3)],[Q(1,100),Q(1,1000),Q(1,10000)]):
        r=a+x; ph=x/r; dp=a/r**2
        radial=4*a*dp/(r*ph); angular=-2*a*dp/(r*ph)
        require(radial+2*angular==0,'divergent connection summand cancellation')
        require(x*radial==4*a*a/r**2,'radial logarithmic-divergence coefficient')
        require(x*angular==-2*a*a/r**2,'angular logarithmic-divergence coefficient')
    result={'verdict':'PASS','check_count':COUNT,'metric_points':len(records),'approach':'Exact rational second-order metric jets, full four-dimensional Christoffel and Ricci contraction in exterior Cartesian coordinates','author_imports':False,'proof_limit':'Finite checks supplement the independent analytical derivation; they do not certify universal identities by themselves.','records':records}
    Path(__file__).with_name('DIRECT_CONNECTION_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))

if __name__=='__main__':main()
