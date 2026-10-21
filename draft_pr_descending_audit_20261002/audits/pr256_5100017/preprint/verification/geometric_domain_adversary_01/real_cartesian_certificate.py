"""All-real local identity certificate derived from Cartesian projections.
General normals and support numbers, with no orbit sampling or submitted checker.
"""
import sympy as S
import json
from pathlib import Path
c,s,u,w,h,k,X,Y,D,H,e,beta=S.symbols('c s u w h k X Y D H e beta',real=True)
K=c*w-s*u; C=c*u+s*w; Zi=c*c-s*s;Zj=u*u-w*w; Yi=2*c*s;Yj=2*u*w
qx=h*c+X*s*s-Y*c*s;qy=h*s-X*c*s+Y*c*c
rx=k*u+X*w*w-Y*u*w;ry=k*w-X*u*w+Y*u*u
wedge=S.expand(qx*ry-qy*rx)
Tx=S.expand(wedge*(qx+rx));Ty=S.expand(wedge*(qy+ry))
def halfpair(p):return S.expand((p+p.xreplace({h:-h,k:-k}))/2)
# The summed paired polynomial is the same as summed halfpair(edge), because
# the cyclic sum contains both antipodal copies. No extra factor of two occurs.
area=S.Poly(halfpair(wedge)/2,X,Y)
tx=S.Poly(halfpair(Tx),X,Y);ty=S.Poly(halfpair(Ty),X,Y)
unit=S.groebner([c*c+s*s-1,u*u+w*w-1],c,u,s,w,domain='EX')
def reduce(p):
    return S.expand(unit.reduce(S.expand(p))[1])
def eliminate(p):
    p=S.Poly(S.expand(p),h,k)
    out=0
    for (i,j),coef in p.terms():
        if (i,j)==(2,0):out+=coef*(H+e*Zi)
        elif (i,j)==(0,2):out+=coef*(H+e*Zj)
        elif (i,j)==(1,1):out+=coef*((D+e)*c*u+(D-e)*s*w)
        elif (i,j)==(0,0):out+=coef
        else:raise AssertionError((i,j))
    return reduce(out)
def coboundary(residual):
    f=S.expand(residual.subs({u:1,w:0}))
    fj=f.xreplace({c:u,s:w})
    return f,reduce(residual-f+fj)

# Squared support relation and the unit-circle edge identities.
square=(H+e*Zi)*(H+e*Zj)-((D+e)*c*u+(D-e)*s*w)**2
assert reduce(square-(H*H-e*e-(D*D-e*e)*C*C+e*(H-D)*(Zi+Zj)))==0
dotZ=Zi*Zj+Yi*Yj;crossZ=Zi*Yj-Yi*Zj
assert reduce(crossZ-2*K*C)==0
assert reduce(crossZ*(Zi+Zj)-(1+dotZ)*(Yj-Yi))==0
assert reduce(crossZ*(Yi+Yj)+(1+dotZ)*(Zj-Zi))==0

# Direct area terms.
assert reduce(area.coeff_monomial(X*X)-K*C/4-(c*s-u*w)/4)==0
assert reduce(area.coeff_monomial(Y*Y)-K*C/4+(c*s-u*w)/4)==0
assert reduce(area.coeff_monomial(X*Y)-(Zj-Zi)/4)==0
assert reduce(eliminate(area.coeff_monomial(1))-D*K*C/2-e*(u*w-c*s)/2)==0

# For diagonal linear moments use the circle-moment relation
# sum K*C*(Zi+Zj)=beta*Sz and sum K*C=Sz.
linear_targets={
 ('x',(1,0)):K*C*((D-H-S.Rational(3,2)*e)-(D+e/2)*(Zi+Zj)),
 ('y',(0,1)):K*C*((D-H+S.Rational(3,2)*e)+(D-e/2)*(Zi+Zj)),
}
output={}
for (name,power),target in linear_targets.items():
    p=[tx,ty][name=='y']; actual=eliminate(p.coeff_monomial(X**power[0]*Y**power[1]))
    f,rem=coboundary(actual-target)
    assert rem==0,(name,power,S.factor(rem))
    output[name+'_linear_'+str(power)]={'cyclic_part':str(S.factor(target)),'telescoping_potential':str(S.factor(reduce(f)))}

# For off-diagonal linear moments, find the multiple of the circle y-moment
# that leaves a telescoping potential. That circle moment is zero.
for name,p,power in [('x',tx,(0,1)),('y',ty,(1,0))]:
    actual=eliminate(p.coeff_monomial(X**power[0]*Y**power[1]))
    A=S.symbols('A')
    target=A*K*C*(Yi+Yj)
    f,rem=coboundary(actual-target)
    solution=S.solve(S.Poly(rem,c,u,s,w).coeffs(),A)
    assert solution
    value=solution[A];f=S.factor(f.subs(A,value));rem=reduce(rem.subs(A,value));assert rem==0
    output[name+'_crosslinear_'+str(power)]={'cyclic_part':str(S.factor(target.subs(A,value))),'telescoping_potential':str(S.factor(reduce(f)))}

# Every cubic coefficient is support-free. Solve its cyclic part in the basis
# KC, KC*(Zi+Zj), KC*(Yi+Yj); any residual must telescope.
for name,p in [('x',tx),('y',ty)]:
    for power in [(3,0),(2,1),(1,2),(0,3)]:
        actual=eliminate(p.coeff_monomial(X**power[0]*Y**power[1]))
        A,B,E=S.symbols('A B E')
        target=K*C*(A+B*(Zi+Zj)+E*(Yi+Yj))
        f,rem=coboundary(actual-target)
        sol=S.solve(S.Poly(rem,c,u,s,w).coeffs(),[A,B,E])
        assert sol,(name,power,S.factor(rem))
        rem=reduce(rem.subs(sol));assert rem==0
        output[name+'_cubic_'+str(power)]={'cyclic_part':str(S.factor(target.subs(sol))),'telescoping_potential':str(S.factor(reduce(f.subs(sol)))),'summed_coefficient_over_Sz':str(S.simplify(sol[A]+sol[B]*beta))}

# Pairing makes constant and every degree-two moment coefficient zero exactly.
for p in [tx,ty]:
    for i,j in [(0,0),(2,0),(1,1),(0,2)]:assert p.coeff_monomial(X**i*Y**j)==0
# Summed direct Cartesian moment quotient equals the submitted complex
# formula expressed in real coordinates, for arbitrary X,Y,D,H,e,beta.
r2=X*X+Y*Y
lx=D-H-S.Rational(3,2)*e-beta*(D+e/2)
ly=D-H+S.Rational(3,2)*e+beta*(D-e/2)
cx=X*(lx+(3-beta)*r2/4)/(6*(D/2+r2/4))
cy=Y*(ly+(3+beta)*r2/4)/(6*(D/2+r2/4))
px=X/2-X*((D+2*H+e*beta)+(2*D*beta+3*e+beta*r2/2))/(3*(2*D+r2))
py=Y/2-Y*((D+2*H+e*beta)-(2*D*beta+3*e+beta*r2/2))/(3*(2*D+r2))
assert S.factor(cx-px)==0 and S.factor(cy-py)==0
Path('CARTESIAN_CERTIFICATE.json').write_text(json.dumps({'status':'PASS','mechanism':'Direct real Cartesian edge projections, antipodal pairing, support square/bilinear relations, unit-normal polynomial reduction, and explicitly telescoping residuals','unit_constraints':['c^2+s^2=1','u^2+w^2=1'],'support_constraints':['h^2=H+e(c^2-s^2)','k^2=H+e(u^2-w^2)','hk=(D+e)cu+(D-e)sw'],'circle_sum_constraints':['sum KC=Sz','sum KC(Zi+Zj)=beta Sz','sum KC(Yi+Yj)=0'],'coefficients':output,'limitations':'An exact all-real polynomial certificate for moment reduction, conditional only on the geometric constraints proved in the report; not a numerical argument.'},indent=2)+'\n')
print('PASS all-real Cartesian identity certificate')
