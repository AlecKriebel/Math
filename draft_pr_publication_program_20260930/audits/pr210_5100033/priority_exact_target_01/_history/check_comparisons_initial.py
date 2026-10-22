"""Independent finite exact comparison controls; no network and no inherited checkers."""
import sys
sys.path.insert(0, "/Users/alec/Library/Python/3.11/lib/python/site-packages")
import sympy as S
import json, hashlib
from pathlib import Path
from datetime import datetime, timezone
OUT=Path(__file__).resolve().parent
rows=[]
def zero(name, expr):
    r=S.factor(S.cancel(expr))
    assert r==0,(name,str(r))
    rows.append({"name":name,"residual":"0","pass":True})
B,c,l,x,y,X,Y=S.symbols("B c lambda x y X Y", real=True)
A=B+c*c
den=A+c*x
T=S.Matrix([A*(x+c)/den,A*y/den])
n=S.Matrix([x/A,y/B]); focus=S.Matrix([c,0])
foot=focus+(1-(n.dot(focus)))*n/(n.dot(n))
def on_boundary(e):
    num,de=S.fraction(S.cancel(e))
    return S.cancel(num.subs(y*y,B*(1-x*x/A))/de)
for i in range(2):zero("projection_equals_projectivity_"+str(i),on_boundary(foot[i]-T[i]))
zero("auxiliary_circle",on_boundary(T.dot(T)-A))
Rminus=S.Matrix([x+c,y])/((x+c)**2+y*y)
for i in range(2):zero("opposite_inverse_variable_multiplier_"+str(i),on_boundary(T[i]-den*Rminus[i]))
# Homogeneous image caustic and its radius-a polar.
ac2=A-l; bc2=B-l
M=S.Matrix([[A*A/ac2-c*c,0,-c*A*l/ac2],[0,B*B/bc2,0],[-c*A*l/ac2,0,-A*A*bc2/ac2]])
pv=S.Matrix([X,Y,-A])
dual=S.factor((pv.T*M.adjugate()*pv)[0])
expected=X*X+Y*Y+2*c*l*X/bc2+(c*c*l*l-ac2*B*B)/(bc2*bc2)
factor=S.Poly(dual,X,Y).coeff_monomial(X*X)
zero("dual_circle_negative_center",dual-factor*expected)
zero("image_caustic_noncircular_coefficient_difference",M[0,0]-M[1,1]+c*c*l*l/(ac2*bc2))
# Actual finite triangle phases, original foci/outer tangent lines and both images.
a=S.sqrt(21); b=S.Integer(4); cc=S.sqrt(5); lam=S.Rational(336,25)
aa2=a*a-lam;bb2=b*b-lam
d=-cc*lam/bb2; R=S.sqrt(aa2)*b*b/bb2; rr=a
H=[S.Matrix([a,0]),S.Matrix([-3*a/5,S.Rational(16,5)]),S.Matrix([-3*a/5,-S.Rational(16,5)])]
V=[S.Matrix([0,b]),S.Matrix([-S.Rational(21,5),-S.Rational(8,5)]),S.Matrix([S.Rational(21,5),-S.Rational(8,5)])]
def area(vs):return S.simplify(sum(vs[j].det(S.Matrix.hstack(vs[(j+1)%len(vs)])) if False else S.det(S.Matrix.hstack(vs[j],vs[(j+1)%len(vs)])) for j in range(len(vs)))/2)
summary=[]
for label,vs in [("H",H),("V",V)]:
    normals=[S.Matrix([p[0]/a**2,p[1]/b**2]) for p in vs]
    outer=[S.Matrix.vstack(normals[j].T,normals[(j+1)%3].T).inv()*S.ones(2,1) for j in range(3)]
    pedals={}
    invs={}
    for sign in [1,-1]:
        f=S.Matrix([sign*cc,0])
        q=[S.simplify(f+(1-nn.dot(f))*nn/(nn.dot(nn))) for nn in normals]
        inv=[S.simplify((p-f)/((p-f).dot(p-f))) for p in vs]
        pedals[sign]=area(q);invs[sign]=area(inv)
        zero(label+"_pedal_inverse_area_transfer_"+str(sign),pedals[sign]-S.Rational(2016,5)*invs[-sign]) if -sign in invs else None
    # Both opposite-focus equalities now that both labels are present.
    for sign in [1,-1]:
        zero(label+"_opposite_focus_ratio_"+str(sign),pedals[sign]-S.Rational(2016,5)*invs[-sign])
    zero(label+"_outer_product",pedals[1]*pedals[-1]-S.Rational(12544,25))
    zero(label+"_inverse_product",invs[1]*invs[-1]-S.Rational(1,324))
    transformed_outer=[S.simplify(S.Matrix([a*a*(p[0]+cc)/(a*a+cc*p[0]),a*a*p[1]/(a*a+cc*p[0])])) for p in outer]
    for j,p in enumerate(transformed_outer):
        zero(label+"_bicentric_outer_circle_"+str(j),(p[0]-d)**2+p[1]**2-R**2)
    zero(label+"_contact_area_ratio",pedals[1]-rr**2/(R**2-d*d)*area(transformed_outer))
    summary.append({"phase":label,"Bplus":str(pedals[1]),"Bminus":str(pedals[-1]),"Dplus":str(invs[1]),"Dminus":str(invs[-1]),"bicentric_area":str(area(transformed_outer)),"same_focus_ratio":str(S.simplify(pedals[1]/invs[1]))})
assert summary[0]["same_focus_ratio"]!=summary[1]["same_focus_ratio"],"Negative control must reject same-focus proportionality."
rows.append({"name":"same_focus_ratio_wrong_transfer_negative_control","pass":True,"observed":[q["same_focus_ratio"] for q in summary]})
out={"schema":"pr210-priority-independent-finite-comparisons-v1","utc":datetime.now(timezone.utc).isoformat(),"scope":"Finite exact comparison/control evidence, not universal proof or promotion authority.","sympy":S.__version__,"checks":rows,"all_pass":all(z["pass"] for z in rows),"count":len(rows),"fixtures":summary,"server_or_service_mutations":False}
(OUT/"CHECKABLE_COMPARISON_RESULTS.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"all_pass":out["all_pass"],"count":len(rows),"fixtures":summary},indent=2))
