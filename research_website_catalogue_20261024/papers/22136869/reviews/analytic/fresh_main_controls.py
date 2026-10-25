"""Fresh graph/automatic-differentiation controls, written before supplied code read.
Exact algebraic fields and rational interval bounds; no submitted code imports.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product,permutations
import sympy as sp
import json,datetime,hashlib,time

checks=[];details={};t0=time.time()
def ck(name,ok):
    assert bool(ok),name
    checks.append(name)
def phase(name):print(name,flush=True)
chars=[[1,1,1,1],[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,1]]
arcs=[('rho','l1','E'),('rho','u','R'),('u','p','U'),('u','q','V'),
      ('p','r2','A2'),('q','r2','B2'),('p','r3','A3'),('q','r3','B3'),
      ('r2','l2','D2'),('r3','l3','D3')]
graphs=[]
for a,b in product(['p','q'],repeat=2):
    kept=[e for e in arcs if not(e[1]=='r2' and e[0]!=a) and not(e[1]=='r3' and e[0]!=b)]
    child={}
    for u,v,n in kept:child.setdefault(u,[]).append((v,n))
    def leaves(v):
        if v.startswith('l'):return [int(v[1])-1]
        return sum((leaves(w) for w,n in child.get(v,[])),[])
    labels=[(n,leaves(v)) for u,v,n in kept]
    graphs.append((a,b,child,labels))

def fq(par,xyz):
    zero=par['E'][0]-par['E'][0];one=par['E'][0]
    if xyz[0]^xyz[1]^xyz[2]:return zero
    out=zero
    for a,b,child,labels in graphs:
        w=(par['d2'] if a=='p' else one-par['d2'])*(par['d3'] if b=='p' else one-par['d3'])
        for name,ls in labels:
            g=0
            for i in ls:g^=xyz[i]
            w=w*par[name][g]
        out=out+w
    return out
def row(a):return [sum((a[g]*chars[g][i] for g in range(4)),a[0]-a[0])/4 for i in range(4)]
def ordinary(par,ijk):
    one=par['E'][0];zero=one-one;out=zero
    mats={name:row(par[name]) for name in ['E','R','U','V','A2','B2','A3','B3','D2','D3']}
    for a,b,child,labels in graphs:
        def message(v):
            if v.startswith('l'):return [one if z==ijk[int(v[1])-1] else zero for z in range(4)]
            result=[one]*4
            for w,name in child.get(v,[]):
                m=message(w)
                for z in range(4):result[z]*=sum((m[t]*mats[name][z^t] for t in range(4)),zero)
            return result
        weight=(par['d2'] if a=='p' else one-par['d2'])*(par['d3'] if b=='p' else one-par['d3'])
        out+=weight*sum(message('rho'),zero)/4
    return out
def tree_ordinary(tree,ijk):
    zero=tree[0][0]-tree[0][0];rr=list(map(row,tree))
    return sum((rr[0][a^ijk[0]]*rr[1][a^ijk[1]]*rr[2][a^ijk[2]] for a in range(4)),zero)/4
def invert(qq,ijk):
    zero=qq[0,0,0]-qq[0,0,0]
    return sum((q*chars[x][ijk[0]]*chars[y][ijk[1]]*chars[z][ijk[2]] for (x,y,z),q in qq.items()),zero)/64
def parmake(K,U,V,S,T):return dict(E=K,R=K,U=U,V=V,A2=S,B2=T,A3=S,B3=T,D2=K,D3=K,d2=K[0]/2,d3=K[0]/2)
def imul(a,b):
    v=[x*y for x in a for y in b];return min(v),max(v)
def iadd(a,b):return a[0]+b[0],a[1]+b[1]
def bound(a,interval):
    out=Q(0),Q(0)
    for c in a.to_list():
        q=Q(int(c.numerator),int(c.denominator));out=iadd(imul(out,interval),(q,q))
    return out
def admissible(name,par,tree,interval,ct=False):
    edges={k:par[k] for k in ['E','R','U','V','A2','B2','A3','B3','D2','D3']}
    edges['effectiveE']=[par['E'][g]*par['R'][g] for g in range(4)]
    edges.update({'tree'+str(i):a for i,a in enumerate(tree)})
    for edge,a in edges.items():
        for g in range(1,4):
            ck(name+edge+' eig'+str(g),bound(a[g],interval)[0]>0 and bound(a[0]-a[g],interval)[0]>0)
        for g,v in enumerate(row(a)):ck(name+edge+' probability'+str(g),bound(v,interval)[0]>0)
        if ct:
            for g in range(1,4):
                others=[t for t in range(1,4) if t!=g]
                ck(name+edge+' CT'+str(g),bound(a[g]-a[others[0]]*a[others[1]],interval)[0]>0)
def collision(name,par,tree,interval,prune=True):
    qq={xyz:fq(par,xyz) for xyz in product(range(4),repeat=3)}
    zero=par['E'][0]-par['E'][0]
    for xyz,v in qq.items():
        want=tree[0][xyz[0]]*tree[1][xyz[1]]*tree[2][xyz[2]] if xyz[0]^xyz[1]^xyz[2]==0 else zero
        ck(name+' Fourier'+str(xyz),v==want)
    pp=[]
    for ijk in product(range(4),repeat=3):
        v=invert(qq,ijk);pp.append(v);ck(name+' positive pattern'+str(ijk),bound(v,interval)[0]>0)
        if prune:
            ck(name+' literal pruning'+str(ijk),ordinary(par,ijk)==v)
            ck(name+' tree pruning'+str(ijk),tree_ordinary(tree,ijk)==v)
    ck(name+' normalization',sum(pp,zero)==par['E'][0]);return qq,pp

class Dual:
    def __init__(self,v,g):self.v=v;self.g=g
    def wrap(self,x):return x if isinstance(x,Dual) else Dual(x,[self.v-self.v]*len(self.g))
    def __add__(self,x):
        x=self.wrap(x);return Dual(self.v+x.v,[a+b for a,b in zip(self.g,x.g)])
    __radd__=__add__
    def __neg__(self):return Dual(-self.v,[-a for a in self.g])
    def __sub__(self,x):return self+-self.wrap(x)
    def __rsub__(self,x):return self.wrap(x)+-self
    def __mul__(self,x):
        x=self.wrap(x);return Dual(self.v*x.v,[a*x.v+self.v*b for a,b in zip(self.g,x.g)])
    __rmul__=__mul__
    def __truediv__(self,x):return Dual(self.v/x,[a/x for a in self.g])
def jacobian(par,rows,cols,k2=False):
    n=len(cols);zero=par['E'][0]-par['E'][0];one=par['E'][0]
    def seed(name,g,val):
        ds=[]
        for en,eg in cols:ds.append(one if name==en and (g==eg or (k2 and g==3 and eg==1)) else zero)
        return Dual(val,ds)
    pp={name:([seed(name,g,v) for g,v in enumerate(value)] if isinstance(value,list) else seed(name,None,value)) for name,value in par.items()}
    return [fq(pp,xyz).g for xyz in rows]
def det(A):
    A=[r[:] for r in A];one=A[0][0]/A[0][0] if A[0][0] else next(v for r in A for v in r if v)/next(v for r in A for v in r if v)
    out=one
    for i in range(len(A)):
        p=next((p for p in range(i,len(A)) if A[p][i]),None)
        if p is None:return out-out
        if p!=i:A[i],A[p]=A[p],A[i];out=-out
        pivot=A[i][i];out*=pivot
        for j in range(i+1,len(A)):
            if A[j][i]:
                q=A[j][i]/pivot
                for k in range(i+1,len(A)):A[j][k]-=q*A[i][k]
                A[j][i]=pivot-pivot
    return out
letters='ACGT'
coords=lambda names:[tuple(letters.index(c) for c in n) for n in names.split()]
r2=coords('ACC AGG CAC CCA CGT CTG GAG GCT GGA')
c2=[('E',1),('E',2),('U',1),('U',2),('V',1),('V',2),('A2',1),('A2',2),('B2',1)]
r3=coords('ACC AGG ATT CAC CCA CGT CTG GAG GCT GGA GTC TAT TCG TGC TTA')
c3=[('E',1),('E',2),('E',3),('U',2),('A2',1),('A2',2),('B2',1),('B2',2),('A3',1),('A3',2),('B3',1),('B3',2),('D2',3),('D3',3),('d3',None)]

phase('simple K2P: exact fields, graph, state pruning and derivative rank')
F=sp.QQ.algebraic_field(sp.sqrt(71));eta=F.from_sympy(sp.sqrt(71));f=lambda a,b=1:F.convert(sp.Rational(a,b));one=f(1)
K=[one,f(1,2),f(1,2),f(1,2)];U=[one,f(4,5),f(19,30),f(4,5)];V=[one,f(7,240),f(239,360),f(7,240)];S=[one,f(1,4),f(1,2),f(1,4)];T=[one,f(1,3),f(1,27),f(1,3)]
P=[one,f(151)/(36*eta),f(107,162),f(151)/(36*eta)];B=[one,eta/40,f(31,120),eta/40]
tree=[[K[g]*K[g]*P[g] for g in range(4)],[K[g]*B[g] for g in range(4)],[K[g]*B[g] for g in range(4)]];par=parmake(K,U,V,S,T)
admissible('simple',par,tree,(Q(8),Q(9)))
qq,pp=collision('simple',par,tree,(Q(8),Q(9)))
minimum=min(pp,key=lambda a:float(F.to_sympy(a)))
ck('simple exact minimum pattern',minimum==f(1188799,79626240))
jd=det(jacobian(par,r2,c2,True));expected=-f(7**2*11**2*19*107*151**2*15013,2**60*3**25*5**10)
ck('simple rank9 exact determinant',jd==expected);details['simple_rank9']=str(F.to_sympy(jd))
# Comparison tree attachment square roots are justified by strict CT margins.
for ai,a in enumerate(tree):
    for g in range(1,4):
        z=[i for i in range(1,4) if i!=g];ck('simple tree CT '+str((ai,g)),bound(a[g]-a[z[0]]*a[z[1]],(Q(8),Q(9)))[0]>0)

phase('quartic K3P: graph, ordinary states, rank15 and exact IFT tangent')
hs=sp.root(sp.Rational(1,5),4);F=sp.QQ.algebraic_field(hs);h=F.from_sympy(hs);f=lambda a,b=1:F.convert(sp.Rational(a,b));one=f(1);zero=f(0)
K=[one,f(1,2),f(1,2),f(1,2)];U=[one,h/3,h,f(1,3)];V=[one,h,h/3,f(1,3)];S=[one,3*h*h/4,f(1,4),f(3,10)];T=[one,f(1,4),3*h*h/4,f(3,10)]
aa=(5*h**3+h)/16;tt=h*h/4;tree=[[one,aa,aa,tt],[one,tt,tt,tt],[one,tt,tt,tt]];par=parmake(K,U,V,S,T);hi=(Q(2,3),Q(7,10))
admissible('quartic',par,tree,hi)
qq,pp=collision('quartic',par,tree,hi)
ck('quartic U three distinct values',len(set(U[1:]))==3)
ck('quartic output is not JC',qq[1,1,0]!=qq[3,3,0])
for xyz in qq:
    swap=tuple({0:0,1:2,2:1,3:3}[a] for a in xyz);ck('quartic C G observable symmetry'+str(xyz),qq[xyz]==qq[swap])
J=jacobian(par,r3,c3);jd=det(J);ck('quartic exact rank15 determinant',jd==h*(10*h*h+1)/f(2**61*3**4*5**14));details['quartic_rank15']=str(F.to_sympy(jd))
tangent=[-3*h/19-375*h**3/304,-621*h/152+1875*h**3/304,zero,-f(6,19)+60*h*h/19,
         -117*h/304+459*h**3/608,-75*h/608-195*h**3/304,-255*h/608+135*h**3/304,9*h/304-9*h**3/608,
         -117*h/304+459*h**3/608,-75*h/608-195*h**3/304,-255*h/608+135*h**3/304,9*h/304-9*h**3/608,zero,zero,zero]
free=jacobian(par,r3,[('U',1),('V',2)])
for i in range(15):ck('IFT tangent row'+str(i),sum((J[i][j]*tangent[j] for j in range(15)),zero)+sum(free[i],zero)==zero)
margin=one-tangent[3]*U[3]
ck('first inward margin identity',margin==(21-20*h*h)/19 and margin==(10*h*h-1)/(one+10*h*h))
ck('first inward margin positive',bound(margin,hi)[0]>0)
details['second_inward_margin']='Exactly1: V_G has free derivative1, while V_C and V_T are absent from the pivot/free lists and remain fixed.'
for name,a in {**{k:par[k] for k in ['E','R','U','V','A2','B2','A3','B3','D2','D3']},**{'tree'+str(i):a for i,a in enumerate(tree)}}.items():
    for g in range(1,4):
        others=[i for i in range(1,4) if i!=g];z=a[g]-a[others[0]]*a[others[1]]
        if (name,g) in [('U',1),('V',2)]:ck('only saturated '+name,z==zero)
        else:ck('strict remaining CT '+str((name,g)),bound(z,hi)[0]>0)

# The contextual reading of the p12 ratio statement is valid with equal B coordinates.
dd,ee=sp.symbols('d e',positive=True)
ck('fixed equal B requires ratio6/5',sp.solve(sp.Eq(4*dd**2/5,5*ee**2/9),ee)==[6*dd/5])

out={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':len(checks),'labels':checks,'details':details,'seconds':time.time()-t0,
     'scope':'Exact simple K2P/quartic K3P graph and state likelihoods, positivity, rank minors, IFT tangent; remaining CT cubic/family/sign/source checks separately recorded. No imported supplied code.'}
out['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest();Path(__file__).with_name('fresh_main_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','checks','seconds']}),flush=True)
