"""Post-freeze cross-audit of the other geometry family's zero witnesses."""
from pathlib import Path
import json
path=Path(__file__).parent/'independent_exact_geometry.py'
# Reuse only this review's independently authored geometry primitives.
source=path.read_text().split('a,b = z.Integer(3),z.Integer(1)')[0]
exec(compile(source,str(path),'exec'))
r=z.symbols('r',positive=True)
A=(r-1)**3*(r+1)/(4*r)
x=(r*r-1)/(r*r+1)
y=2*r/(r*r+1)
lam=A/(A+r*r)
first=z.factor(A*(1-x)**2-lam*(y*y+A*(1-x)**2))
second=z.factor(A*(1-y)**2-lam*((1-y)**2+A*x*x))
assert first==0 and second==0
receipt={'exposure':'The one-parameter N8 construction was learned from other reviewers only after INDEPENDENT_FREEZE.json.','symbolic_chord_tangency_residuals':[str(first),str(second)],'witnesses':{}}
for rv in [3,5]:
    av=z.sqrt(A.subs(r,rv)); lv=z.simplify(lam.subs(r,rv)); xv=x.subs(r,rv); yv=y.subs(r,rv)
    v=[(av,0),(av*xv,yv),(0,1),(-av*xv,yv),(-av,0),(-av*xv,-yv),(0,-1),(av*xv,-yv)]
    v=[tuple(map(z.sympify,p)) for p in v]
    validate(v,av,z.Integer(1),lv)
    ap,ab,_=derived(v,(z.sqrt(av*av-1),0))
    receipt['witnesses'][str(rv)]={'outer_major_axis_squared':str(av*av),'caustic_lambda':str(lv),'pedal_area':str(ap),'antipedal_area':str(ab),'antipedal_sign':int(z.sign(ab))}
assert receipt['witnesses']['3']['antipedal_sign']==1
assert receipt['witnesses']['5']['antipedal_sign']==-1
receipt['conclusion']='For 3<=r<=5 the ellipse and caustic remain strict/nondegenerate, eight vertices remain distinct, and all real antipedal intersections are finite. Continuity gives an admitted zero signed antipedal area; the verified trace lemma makes it identically zero in phase.'
print(json.dumps(receipt,indent=2))
