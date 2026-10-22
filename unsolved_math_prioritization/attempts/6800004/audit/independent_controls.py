#!/usr/bin/env python3
"""Independent symbolic controls for the Chen--Zhang source-resolution audit.

Uses a second-derivative formula for the covariant curvature tensor rather
than the frozen diagnostic's differentiated upper Christoffel computation.
The base-metric check is symbolic in both chart coordinates and epsilon.
It is corroboration for the independently reviewed global analytic proof.
"""
import itertools, json
import sympy as S
u,v,e=S.symbols('u v e',real=True)
D=1+u*u+v*v
X1=S.Matrix([-u*v,(u*u-v*v-1)/2]); X2=S.Matrix([(1+u*u-v*v)/2,u*v]); X3=S.Matrix([-v,u])
z=(1-u*u-v*v)/D
P=S.eye(4); P[:2,2]=-e*X1; P[:2,3]=-e*X2
Pinv=S.eye(4); Pinv[:2,2]=e*X1; Pinv[:2,3]=e*X2
g=(P.T*S.diag(4/D**2,4/D**2,1,1)*P).applyfunc(S.cancel)
gi=(Pinv*S.diag(D**2/4,D**2/4,1,1)*Pinv.T).applyfunc(S.cancel)
E=Pinv*S.diag(D/2,D/2,1,1)
pairs=list(itertools.combinations(range(4),2))
def simp(x): return S.cancel(x)
def diff(x,i): return S.diff(x,(u,v)[i]) if i<2 else S.Integer(0)
def curvature_cov(metric,inverse):
    low=[[[simp((diff(metric[a,j],i)+diff(metric[a,i],j)-diff(metric[i,j],a))/2) for j in range(4)] for i in range(4)] for a in range(4)]
    C=S.zeros(6)
    for I,(i,j) in enumerate(pairs):
        for J,(k,l) in enumerate(pairs):
            value=(diff(diff(metric[k,j],l),i)+diff(diff(metric[i,l],k),j)-diff(diff(metric[j,l],k),i)-diff(diff(metric[i,k],l),j))/2
            value+=sum(inverse[a,b]*(low[a][j][k]*low[b][i][l]-low[a][i][k]*low[b][j][l]) for a in range(4) for b in range(4))
            C[I,J]=simp(value)
    return C

def exterior(frame):
    return S.Matrix(6,6,lambda I,J: frame[pairs[I][0],pairs[J][0]]*frame[pairs[I][1],pairs[J][1]]-frame[pairs[I][1],pairs[J][0]]*frame[pairs[I][0],pairs[J][1]])

def hodge(C,sign):
    T=S.zeros(6,3); T[0,0]=1;T[5,0]=sign;T[1,1]=1;T[4,1]=-sign;T[2,2]=1;T[3,2]=sign
    return (T.T*C*T/2).applyfunc(simp)

# Check the coordinate fields independently against their ambient definitions.
point=S.Matrix([2*u/D,2*v/D,z]); J=point.jacobian((u,v))
assert (J.T*J-4*S.eye(2)/D**2).applyfunc(simp)==S.zeros(2)
for i,X in enumerate((X1,X2,X3)):
    axis=S.eye(3)[:,i]
    assert (J*X-axis.cross(point)).applyfunc(simp)==S.zeros(3,1)
assert simp(S.Matrix.hstack(J[:,0],J[:,1],point).det()-4/D**2)==0
assert (g*gi-S.eye(4)).applyfunc(simp)==S.zeros(4)
assert (E.T*g*E-S.eye(4)).applyfunc(simp)==S.zeros(4)
C=curvature_cov(g,gi)
W=exterior(E)
R=(W.T*C*W).applyfunc(simp)
f=-2*e**2*X3/D; d1=-2*e**3*X2/D; d2=2*e**3*X1/D; q=-e**2*z; rho=simp(f.dot(f))
expected=S.zeros(6)
def put(i,j,value): expected[i,j]=expected[j,i]=value
put(0,0,1); put(5,5,-3*rho/4); put(0,5,q)
for i in (1,2):put(i,i,f[0]**2/4)
for i in (3,4):put(i,i,f[1]**2/4)
put(1,3,f[0]*f[1]/4);put(2,4,f[0]*f[1]/4);put(1,4,q/2);put(2,3,-q/2)
put(5,1,-d1[0]/2);put(5,2,-d2[0]/2);put(5,3,-d1[1]/2);put(5,4,-d2[1]/2)
assert (R-expected).applyfunc(simp)==S.zeros(6)
# Bianchi, sphere calibration, and zero-parameter controls.
assert simp(R[0,5]-R[1,4]+R[2,3])==0
assert R.subs(e,0)==S.diag(1,0,0,0,0,0)
blocks=[]
for sign in (1,-1):
    A=hodge(R,sign)
    b=S.Matrix([(-sign*d1[0]+d2[1])/4,(-sign*d2[0]-d1[1])/4])
    a=S.Rational(1,2)-3*rho/8+sign*q; c=rho/8-sign*q/2
    B=S.Matrix([[a,b[0],b[1]],[b[0],c,0],[b[1],0,c]])
    assert (A-B).applyfunc(simp)==S.zeros(3)
    blocks.append(A)
assert simp(sum(A[0,1]**2+A[0,2]**2 for A in blocks)-e**6*(1+z*z)/8)==0
assert simp(rho-e**4*(1-z*z))==0
# Coordinate divergence-form Laplacian, independent of the source's frame proof.
volume=4/D**2
lap_z2=simp(sum(diff(volume*gi[i,j]*diff(z*z,j),i) for i in range(4) for j in range(4))/volume)
assert simp(lap_z2-(1+e*e)*(2-6*z*z))==0
U=1+e**4*z*z/(24*(1+e*e))
Phi=(1-z*z)/8
lapU=simp(sum(diff(volume*gi[i,j]*diff(U,j),i) for i in range(4) for j in range(4))/volume)
assert simp(lapU/2-e**4*(Phi-S.Rational(1,12)))==0
# Conformal-curvature computation at exact, asymmetric points with nonzero dU.
# To avoid a costly second symbolic full-tensor pass, differentiate first and
# substitute exact jets into the independent covariant-curvature formula.
ghat=(U**2*g).applyfunc(simp)
def conformal_point(uu,vv,ee):
    sub={u:S.Rational(uu),v:S.Rational(vv),e:S.Rational(ee)}
    gg=ghat.subs(sub); inv=gg.inv()
    dg=[ghat.diff(x).subs(sub) for x in (u,v)]+[S.zeros(4),S.zeros(4)]
    ddg=[[ghat.diff(x).diff(y).subs(sub) for y in (u,v)] for x in (u,v)]
    def dd(i,j,a,b): return ddg[i][j][a,b] if i<2 and j<2 else S.Integer(0)
    low=[[[ (dg[i][a,j]+dg[j][a,i]-dg[a][i,j])/2 for j in range(4)] for i in range(4)] for a in range(4)]
    C=S.zeros(6)
    for I,(i,j) in enumerate(pairs):
        for J,(k,l) in enumerate(pairs):
            C[I,J]=(dd(i,l,k,j)+dd(j,k,i,l)-dd(i,k,j,l)-dd(j,l,i,k))/2 + sum(inv[a,b]*(low[a][j][k]*low[b][i][l]-low[a][i][k]*low[b][j][l]) for a in range(4) for b in range(4))
    U0=U.subs(sub); frame=E.subs(sub)/U0
    assert frame.T*gg*frame==S.eye(4)
    W=exterior(frame); RF=W.T*C*W
    assert RF==RF.T
    delta=lapU.subs(sub)/(2*U0)
    # The entire Hodge block gets a scalar shift; this checks every plane.
    for sign,A in zip((1,-1),blocks):
        assert hodge(RF,sign)==(A.subs(sub)-delta*S.eye(3))/U0**2
    return {'coordinates':[str(uu),str(vv)],'epsilon':str(ee),'full_hodge_conformal_law':True}

results={'ambient_rotation_fields_and_outward_orientation':True,'symbolic_base_curvature_all_36_entries':True,'symbolic_parameters':['u','v','epsilon'],
 'both_complete_hodge_blocks':True,'bianchi_control':True,'epsilon_zero_round_flat_control':True,
 'symbolic_laplacian_and_conformal_correction':True,
 'exact_conformal_checks':[conformal_point(S.Rational(1,2),S.Rational(1,3),S.Rational(1,4)),conformal_point(2,-1,S.Rational(1,8))],
 'scope':'Symbolic chart identities extend across the omitted sphere pole by smoothness; inequalities and all-plane global quantifiers are reviewed analytically in the audit report.'}
print(json.dumps(results,indent=2))
