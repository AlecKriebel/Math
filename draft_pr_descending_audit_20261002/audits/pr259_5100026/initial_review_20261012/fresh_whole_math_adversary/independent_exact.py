#!/usr/bin/env python3
"""Independent exact raw-line tests; no submitted or prior-case helper imports."""
from pathlib import Path
from datetime import datetime,timezone
import sys,json,hashlib
V=Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr261_5100021/initial_review_20261012/reproduction_source_adversary/vendor')
sys.path.insert(0,str(V))
import sympy as sp
O=Path(__file__).resolve().parent
results={}
def check(name,x):
    z=sp.factor(sp.cancel(x))
    assert z==0,(name,z)
    results[name]=str(z)
def antipedal(X,Y,M):
    Q=X-M;T=Y-M
    # Direct side equation (X-M).U=(X-M).X, with absolute U coordinates.
    return sp.Matrix([list(Q),list(T)]).inv()*sp.Matrix([Q.dot(X),T.dot(Y)])
h,l,m,n=sp.symbols('h l m n',nonzero=True)
M=sp.Matrix([m,n]);rect=[sp.Matrix([h,l]),sp.Matrix([-h,l]),sp.Matrix([-h,-l]),sp.Matrix([h,-l])]
C=sum((antipedal(rect[i],rect[(i+1)%4],M) for i in range(4)),sp.zeros(2,1))/4
check('rectangle_Cx',C[0]-m/2*((l*l-n*n)/(h*h-m*m)-1))
check('rectangle_Cy',C[1]-n/2*((h*h-m*m)/(l*l-n*n)-1))
# General triangle suitable for exact reflected/double-traversal witness.
f,H,L,q=sp.symbols('f H L q',nonzero=True)
tri=[sp.Matrix([H,1]),sp.Matrix([-H,1]),sp.Matrix([0,-L])];M=sp.Matrix([f,0])
Cs=sum((antipedal(tri[i],tri[(i+1)%3],M) for i in range(3)),sp.zeros(2,1))/3
Hx=4*(1+q)/(1-q)
# Cancellation before substitution avoids branch-sensitive radical simplification.
def rational_sub(x,subs):
    num,den=sp.fraction(sp.cancel(x))
    return sp.factor(sp.expand(num).subs(subs)/sp.expand(den).subs(subs))
Cx=f*rational_sub(Cs[0]/f,{H**2:Hx,L:1/q,f**2:3})
Cy=rational_sub(Cs[1],{H**4:Hx**2,H**2:Hx,L:1/q,f**4:9,f**2:3})
check('triangle_Cx_reduction',Cx-f*(2-q)/(3*q))
check('triangle_Cy_polynomial_reduction',Cy+2*(2*q-1)*(3*q+1)/(3*q*(q-1)))
qr=(4-sp.sqrt(13))/3
check('triangle_Cx_exact',Cx.subs({q:qr,f:sp.sqrt(3)})-(7*sp.sqrt(3)+2*sp.sqrt(39))/3)
check('triangle_Cy_exact',Cy.subs(q,qr)+6)
# Confocal caustic: original ellipse axes 2,1; caustic axes sqrt(3+q^2),q.
caustic_slant=(3+q*q)*(1+q)**2/(4*(1-q*q))+q*q-1
check('same_confocal_caustic_slant',caustic_slant.subs(q,qr))
check('witness_ellipse_points',4*(1-qr*qr)/4+qr*qr-1)
check('witness_q_division_polynomial',(3*q*q-8*q+1).subs(q,qr))
# Independently verify tangent formula and determinant in the Jacobi algebra.
S,C,D,s,c,d,k,kp=sp.symbols('S C D s c d k kp')
constraints=[C*C+S*S-1,D*D+k*k*S*S-1,c*c+s*s-1,d*d+k*k*s*s-1,kp*kp+k*k-1]
gb=sp.groebner(constraints,C,D,c,d,kp,S,s,k)
def modzero(name,x):
    num=sp.fraction(sp.cancel(x))[0]
    z=gb.reduce(sp.expand(num))[1]
    assert z==0,(name,sp.factor(z));results[name]='0'
D0=1-k*k*s*s*S*S
a=d/c;b=kp/c;A=d*d/(c*c);B=kp/(c*c)
rm=sp.Matrix([-A*(S*c*d-s*C*D)/D0,B*(C*c+S*s*D*d)/D0]);rp=sp.Matrix([-A*(S*c*d+s*C*D)/D0,B*(C*c-S*s*D*d)/D0]);mf=sp.Matrix([k,0])
Rc=sp.Matrix([-A*S,B*C])
for sign in (-1,1):
    ss=(S*c*d+sign*s*C*D)/D0;cc=(C*c-sign*S*s*D*d)/D0
    modzero('outer_tangent_'+str(sign),-ss*Rc[0]/a+cc*Rc[1]/b-1)
modzero('antipedal_original_focus_determinant',sp.det(sp.Matrix.hstack(rm-mf,rp-mf))-2*B*s*d*D*(a+k*S)/D0)
# Residue from raw leading equations, including actual opposite pole vector -L.
lx,ly,qx,qy,mx,my=sp.symbols('lx ly qx qy mx my')
LV=sp.Matrix([lx,ly]);QV=sp.Matrix([qx,qy]);MV=sp.Matrix([mx,my])
def residue(Lv,Qv,Mv):
    return sp.Matrix([list(Lv),list(Qv-Mv)]).inv()*sp.Matrix([Lv.dot(Lv),0])
Res=residue(LV,QV,MV)+residue(LV,-QV,MV)+residue(-LV,-QV,MV)+residue(-LV,QV,MV)
check('four_actual_edge_residues_x',Res[0]);check('four_actual_edge_residues_y',Res[1])
results['exact_counterexample']={'original_ellipse':'x^2/4+y^2=1','q':'(4-sqrt(13))/3','original_vertices':['(0,1)','(2sqrt(1-q^2),-q)','(-2sqrt(1-q^2),-q)'],'caustic_axes':['sqrt(3+q^2)','q'],'focus':'(sqrt(3),0)','outer_vertices':['(H,1)','(-H,1)','(0,-1/q)'],'H2':'4(1+q)/(1-q)','centroid':'((7sqrt(3)+2sqrt(39))/3,-6)','reflected_centroid':'((7sqrt(3)+2sqrt(39))/3,+6)','listed_even_N':'double each period-3 orbit to N=6'}
results['runtime']={'python':sys.version,'sympy':sp.__version__,'vendor':str(V)}
results['utc']=datetime.now(timezone.utc).isoformat()
(O/'INDEPENDENT_EXACT.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
