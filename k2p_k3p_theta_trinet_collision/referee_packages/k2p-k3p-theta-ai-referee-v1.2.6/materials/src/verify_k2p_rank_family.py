#!/usr/bin/env python3
"""Exact K2P rank and collision-family audit (standard library only)."""
from __future__ import annotations
import importlib.util,itertools,math,sys
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from strict_json import load_canonical_certificate
spec=importlib.util.spec_from_file_location('k2pext',ROOT/'src/verify_k2p_extended.py');m=importlib.util.module_from_spec(spec);sys.modules['k2pext']=m;spec.loader.exec_module(m)
SIMPLE=load_canonical_certificate(ROOT/'certificate_k2p_simple.json')
def need(c,msg):
    if not c:raise AssertionError(msg)
def verify_q71_field():
    field=SIMPLE['field'];need(field['minimal_polynomial']=='s^2-71','Q(sqrt(71)) minimal polynomial');need(field['basis']==['1','sqrt(71)'],'Q(sqrt(71)) basis')
    lo,hi=map(F,field['positive_root_interval']);need(F(0)<lo<hi,'positive ordered sqrt(71) interval');need(lo*lo<F(71)<hi*hi,'interval isolates positive sqrt(71)');need(math.isqrt(71)**2!=71,'71 is nonsquare')
    print('[field] PASS  Q(sqrt(71)) and its positive embedding are certified')
ROWS=[(0,1,1),(0,2,2),(1,0,1),(1,1,0),(1,2,3),(1,3,2),(2,0,2),(2,1,3),(2,2,0)]
COLS=['rho_1.C','rho_1.G','u_p.C','u_p.G','u_q.C','u_q.G','p_r2.C','p_r2.G','q_r2.C']
@dataclass(frozen=True)
class Dual:
    v:object;d:tuple
    def __add__(self,o):return Dual(self.v+o.v,tuple(a+b for a,b in zip(self.d,o.d)))
    def __neg__(self):return Dual(-self.v,tuple(-a for a in self.d))
    def __sub__(self,o):return self+(-o)
    def __mul__(self,o):return Dual(self.v*o.v,tuple(self.v*b+a*o.v for a,b in zip(self.d,o.d)))
    def scale(self,q):return Dual(self.v.scale(q) if hasattr(self.v,'scale') else self.v*F(q),tuple(x.scale(q) if hasattr(x,'scale') else x*F(q) for x in self.d))
def dual_matrix(values,zero,one,d2,d3):
    n=9
    def constvec(e):return [Dual(x,(zero,)*n) for x in e]
    def lift(e,prefix):
        out=[]
        for i,x in enumerate(e):
            cls='C' if i in (1,3) else ('G' if i==2 else '');key=prefix+'.'+cls if cls else ''
            out.append(Dual(x,tuple(one if key==c else zero for c in COLS)))
        return out
    K,U,V,A,B=values['K'],values['U'],values['V'],values['A'],values['B']
    Kr1=lift(K,'rho_1');Kru=constvec(K);K2=constvec(K);K3=constvec(K);UU=lift(U,'u_p');VV=lift(V,'u_q');A2=lift(A,'p_r2');A3=constvec(A);B2=lift(B,'q_r2');B3=constvec(B)
    out=[]
    for x,y,z in ROWS:
        core=(A2[y]*A3[z]*UU[y^z]).scale(d2*d3)+(A2[y]*B3[z]*UU[y]*VV[z]).scale(d2*(1-d3))+(B2[y]*A3[z]*VV[y]*UU[z]).scale((1-d2)*d3)+(B2[y]*B3[z]*VV[y^z]).scale((1-d2)*(1-d3));q=Kr1[x]*Kru[x]*K2[y]*K3[z]*core;out.append(list(q.d))
    return out

TREE_ROWS=[(0,1,1),(0,2,2),(1,0,1),(1,1,0),(1,2,3),(2,0,2)]
TREE_COLS=['alpha.C','alpha.G','beta.C','beta.G','gamma.C','gamma.G']

def model_dimensions():
    # The 16 consistent K3P coordinates are indexed by x xor y xor z = 0.
    # K2P additionally identifies the global C<->T character swap.  Count
    # those orbits directly, then remove the normalized all-A coordinate.
    swap={0:0,1:3,2:2,3:1}
    consistent=[triple for triple in itertools.product(range(4),repeat=3)
                if triple[0]^triple[1]^triple[2]==0]
    orbits={frozenset((triple,tuple(swap[index] for index in triple)))
            for triple in consistent}
    ambient_dimension=len(orbits)-1
    tree_dimension=len(TREE_COLS)
    need((len(consistent),len(orbits),ambient_dimension)==(16,10,9),
         'K2P consistent-coordinate orbit count')
    need(SIMPLE['network_rank']['ambient_dimension']==ambient_dimension,
         'stored K2P ambient dimension')
    need(SIMPLE['tree_rank']['dimension']==tree_dimension,
         'stored K2P tree dimension')
    print('[K2P dimensions] PASS  16 consistent coordinates form 10 C<->T orbits; normalization gives ambient dimension 9; the certified tree minor gives dimension 6')
    return ambient_dimension,tree_dimension

@dataclass(frozen=True)
class Q71:
    a:F; b:F=F(0)
    def __add__(self,o): return Q71(self.a+o.a,self.b+o.b)
    def __neg__(self): return Q71(-self.a,-self.b)
    def __sub__(self,o): return self+(-o)
    def __mul__(self,o): return Q71(self.a*o.a+71*self.b*o.b,self.a*o.b+self.b*o.a)
    def inv(self):
        den=self.a*self.a-71*self.b*self.b
        need(den!=0,'Q(sqrt(71)) inverse')
        return Q71(self.a/den,-self.b/den)
    def __truediv__(self,o): return self*o.inv()
    def is_zero(self): return self.a==0 and self.b==0
    def interval(self):
        lo,hi=map(F,SIMPLE['field']['positive_root_interval'])
        return ((self.a+self.b*lo,self.a+self.b*hi) if self.b>=0 else (self.a+self.b*hi,self.a+self.b*lo))
def det_q71(A):
    A=[row[:] for row in A]; det=Q71(F(1)); sgn=1; n=len(A)
    for k in range(n):
        piv=next(i for i in range(k,n) if not A[i][k].is_zero())
        if piv!=k: A[k],A[piv]=A[piv],A[k]; sgn*=-1
        q=A[k][k]; det=det*q
        for i in range(k+1,n):
            f=A[i][k]/q
            for j in range(k+1,n): A[i][j]=A[i][j]-f*A[k][j]
            A[i][k]=Q71(F(0))
    return -det if sgn<0 else det
def tree_rank():
    def parse(z): return Q71(F(z[0]),F(z[1]))
    edges={name:tuple(parse(z) for z in SIMPLE['comparison_tree'][name]) for name in ('alpha','beta','gamma')}
    n=len(TREE_COLS); z=Q71(F(0)); o=Q71(F(1))
    def lift(edge,prefix):
        out=[]
        for i,val in enumerate(edge):
            cls='C' if i in (1,3) else ('G' if i==2 else '')
            key=prefix+'.'+cls if cls else ''
            out.append(Dual(val,tuple(o if key==c else z for c in TREE_COLS)))
        return out
    aa,bb,gg=lift(edges['alpha'],'alpha'),lift(edges['beta'],'beta'),lift(edges['gamma'],'gamma')
    M=[]
    for x,y,zidx in TREE_ROWS:
        q=aa[x]*bb[y]*gg[zidx]
        M.append(list(q.d))
    det=det_q71(M)
    want=SIMPLE['tree_rank']['determinant']
    need(det==Q71(F(want[0]),F(want[1])),'tree rank determinant')
    lo,hi=det.interval(); need(lo>0,'tree rank determinant positive')
    print(f'[K2P tree rank] PASS  exact 6x6 minor is positive; det = ({det.a}) + ({det.b}) sqrt(71)')

def solve3(A,b):
    A=[list(row)+[rhs] for row,rhs in zip(A,b)]
    for k in range(3):
        p=next(i for i in range(k,3) if A[i][k])
        if p!=k:A[k],A[p]=A[p],A[k]
        q=A[k][k];A[k]=[x/q for x in A[k]]
        for i in range(3):
            if i==k:continue
            q=A[i][k]
            if q:A[i]=[x-q*y for x,y in zip(A[i],A[k])]
    return [A[i][3] for i in range(3)]
def inv_alg(x):
    need(all(c==0 for c in x.c[3:]),'rank entries lie in Q(ell)');basis=[m.Alg.one(),m.Alg.ell(),m.Alg.ell()**2];cols=[(x*z).c[:3] for z in basis];A=[[cols[j][i] for j in range(3)] for i in range(3)];b=solve3(A,[F(1),F(0),F(0)]);y=m.Alg((b[0],b[1],b[2],F(0),F(0),F(0)));need(x*y==m.Alg.one(),'field inverse');return y
def det_alg(A):
    A=[row[:] for row in A];det=m.Alg.one();sgn=1;n=len(A)
    for k in range(n):
        p=next(i for i in range(k,n) if not A[i][k].is_zero())
        if p!=k:A[k],A[p]=A[p],A[k];sgn*=-1
        piv=A[k][k];det=det*piv;inv=inv_alg(piv)
        for i in range(k+1,n):
            f=A[i][k]*inv
            for j in range(k+1,n):A[i][j]=A[i][j]-f*A[k][j]
            A[i][k]=m.Alg.zero()
    return -det if sgn<0 else det
def determinant_formula(values,scale):
    K,U,V,A,B=values['K'],values['U'],values['V'],values['A'],values['B'];kc,kg=K[1],K[2];u,v=U[1],U[2];w,x=V[1],V[2];a,b=A[1],A[2];c,d=B[1],B[2]
    f=-b*v+b+d*x-d;g=a*a*d*v*x-a*b*c*u*v*w+a*c*d*u*w*x-b*c*c*v*x
    return a*a*b*c*c*d*(kc**15)*(kg**11)*u*u*v*w*w*f*f*g*scale(F(1,1024)),f,g
def simple_rank():
    mixing={name:F(value) for name,value in SIMPLE['mixing_parameters'].items()};need(mixing=={'r2':F(1,2),'r3':F(1,2)},'simple rank inheritance weights')
    raw=SIMPLE['network_vectors']
    def q(name):return tuple(m.Alg.rat(F(z[0])) for z in raw[name])
    values={'K':q('K'),'U':q('U'),'V':q('V'),'A':q('S'),'B':q('T')};A=dual_matrix(values,m.Alg.zero(),m.Alg.one(),mixing['r2'],mixing['r3']);det=det_alg(A);formula,f,g=determinant_formula(values,lambda q:m.Alg.rat(q));need(det==formula,'simple determinant factorization');need(det.c[1:]==(F(0),)*5 and str(det.c[0])==SIMPLE['network_rank']['determinant'],'simple determinant');f.require_positive('first rank factor');(-g).require_positive('negative final factor');print('[K2P rank] PASS  simple witness rank 9 with det =',det.c[0])
def continuous_rank():
    need(m.MIXING=={'r2':F(1,2),'r3':F(1,2)},'continuous rank inheritance weights');values={k:m.network_vectors[k] for k in ('K','U','V','A','B')};A=dual_matrix(values,m.Alg.zero(),m.Alg.one(),m.MIXING['r2'],m.MIXING['r3']);det=det_alg(A);formula,f,g=determinant_formula(values,lambda q:m.Alg.rat(q));need(det==formula,'continuous determinant factorization');f.require_positive('continuous squared factor');(-g).require_positive('continuous final factor');lo,hi=det.interval();need(hi<0,'continuous determinant negative');print(f'[K2P rank] PASS  edgewise-strict-continuous-time witness rank 9; det in [{float(lo):.6e},{float(hi):.6e}]')
def fixed_output_fiber_dimension(ambient_dimension,tree_dimension):
    semi=SIMPLE['semi_directed']
    core_edges={frozenset((a,b)) for path in semi['theta_paths'] for a,b in zip(path,path[1:])}
    incident_edges={frozenset(edge) for edge in semi['incident_leaf_edges']}
    need(len(core_edges)==6,'six effective theta-core edges')
    need(len(incident_edges)==3 and core_edges.isdisjoint(incident_edges),'three distinct incident leaf edges')
    effective_edge_count=len(core_edges|incident_edges)
    reticulation_count=len(semi['reticulations'])
    parameter_dimension=2*effective_edge_count+reticulation_count
    rank=ambient_dimension
    fiber_dimension=parameter_dimension-rank
    need((effective_edge_count,reticulation_count,parameter_dimension,rank)==(9,2,20,9),'K2P dimension inputs')
    need(fiber_dimension==11,'local fixed-output K2P fiber dimension')
    collision_dimension=parameter_dimension-ambient_dimension+tree_dimension
    collision_codimension=ambient_dimension-tree_dimension
    need((collision_dimension,collision_codimension)==(17,3),'K2P collision-locus dimension and codimension')
    print('[K2P fiber] PASS  local fixed-output theta fiber has dimension 11 (20-9) at both rank-9 witnesses')
    print('[K2P geometry] PASS  derived collision-locus dimension 17 = 20-9+6 (codimension 3)')
def family():
    @dataclass(frozen=True)
    class D2:
        v:F;d:tuple[F,F]
        def __add__(self,o):return D2(self.v+o.v,tuple(a+b for a,b in zip(self.d,o.d)))
        def __neg__(self):return D2(-self.v,tuple(-a for a in self.d))
        def __sub__(self,o):return self+(-o)
        def __mul__(self,o):return D2(self.v*o.v,tuple(self.v*b+a*o.v for a,b in zip(self.d,o.d)))
        def scale(self,q):q=F(q);return D2(q*self.v,tuple(q*x for x in self.d))
        def __pow__(self,n):
            z=D2(F(1),(F(0),F(0)))
            for _ in range(n):z=z*self
            return z
    family_data=SIMPLE['symmetric_collision_family'];variables=family_data['variables'];equations=family_data['equations']
    need(variables==['u','v','w','x','a','b','c','d'],'symmetric-family variable order');need(len(equations)==2,'two symmetric-family equations');need(family_data['jacobian_variables']==['v','x'],'symmetric-family Jacobian variables');need(family_data['local_dimension']==len(variables)-len(equations)==6,'derived symmetric-family local dimension')
    u=D2(F(4,5),(0,0));v=D2(F(19,30),(1,0));w=D2(F(7,240),(0,0));x=D2(F(239,360),(0,1));a=D2(F(1,4),(0,0));b=D2(F(1,2),(0,0));c=D2(F(1,3),(0,0));d=D2(F(1,27),(0,0))
    MAC=(a*u+c*w).scale(F(1,2));MAG=(b*v+d*x).scale(F(1,2));MCC=(a*a+(a*c*u*w).scale(2)+c*c).scale(F(1,4));MGG=(b*b+(b*d*v*x).scale(2)+d*d).scale(F(1,4));MCG=(a*b*u+a*d*u*x+b*c*v*w+c*d*w).scale(F(1,4));MCT=(a*a*v+(a*c*u*w).scale(2)+c*c*x).scale(F(1,4));F1=MCG*MCG-MAC*MAC*MGG;F2=MCT*MCT*MGG-MAG*MAG*MCC*MCC;need(F1.v==0 and F2.v==0,'family equations');jac=F1.d[0]*F2.d[1]-F1.d[1]*F2.d[0];want=F(family_data['jacobian_determinant_at_witness']);need(jac==want and jac>0,'family Jacobian');print('[K2P family] PASS  exact two-equation core has rank 2; derived local positive family dimension 6')
if __name__=='__main__':m.require_python();verify_q71_field();m.verify_field();dimensions=model_dimensions();simple_rank();tree_rank();continuous_rank();fixed_output_fiber_dimension(*dimensions);family();print('\nALL K2P RANK/FAMILY CHECKS PASSED')
