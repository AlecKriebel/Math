"""Fresh polynomial incidence checks written after candidate exposure; no author checker read."""
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'_python'))
import sympy as t
k,s,c,d,kp,S,C,D=t.symbols('k s c d kp S C D')
L=1-k*k*s*s*S*S;H=1-2*k*k*s*s+k*k*s**4
r=(-(H*S+k*(c*c-d*d*S*S))/(c*c*L),C*(2*kp*kp-H*(1+k*S))/(kp*c*c*L))
pminus=(-d*(S*c*d-s*C*D)/(c*L),kp*(C*c+S*s*D*d)/(c*L))
pplus=(-d*(S*c*d+s*C*D)/(c*L),kp*(C*c-S*s*D*d)/(c*L))
relations=[(c,c*c-1+s*s),(d,d*d-1+k*k*s*s),(kp,kp*kp-1+k*k),(C,C*C-1+S*S),(D,D*D-1+k*k*S*S)]
def reduce(expr):
    num,den=t.fraction(t.cancel(expr))
    num=t.expand(num)
    for root,relation in relations:num=t.rem(num,relation,root)
    return t.expand(num),den
checks={}
for name,p in [('minus',pminus),('plus',pplus)]:
    expr=(p[0]-k)*(r[0]-p[0])+p[1]*(r[1]-p[1])
    remainder,den=reduce(expr);assert remainder==0
    checks['original_antipedal_line_'+name]={'remainder':str(remainder),'clearing_denominator':str(t.factor(den))}
q0=(pminus[0]-k,pminus[1]);q1=(pplus[0]-k,pplus[1])
actual=q0[0]*q1[1]-q0[1]*q1[0]
expected=2*kp*s*d*D*(1+k*S)/(c*L)
remainder,den=reduce(actual-expected);assert remainder==0
checks['normal_determinant']={'remainder':str(remainder),'clearing_denominator':str(t.factor(den))}
q=((k-S)/(1-k*S),kp*C/(1-k*S))
remainder,den=reduce(q[0]*q[0]+q[1]*q[1]-1);assert remainder==0
checks['pedal_fixed_circle']={'remainder':str(remainder),'clearing_denominator':str(t.factor(den))}
n=(-S,C/kp);foot=(k+(1+k*S)*n[0]/(n[0]**2+n[1]**2),(1+k*S)*n[1]/(n[0]**2+n[1]**2))
for i in (0,1):
    remainder,den=reduce(q[i]-foot[i]);assert remainder==0
    checks['pedal_projection_'+str(i)]={'remainder':str(remainder),'clearing_denominator':str(t.factor(den))}
result={'provenance':'Written after complete PROOF.md exposure and independent pre-exposure artifact freeze; no author or previous reviewer checker read or run. Reused only our independently derived line equations and standard algebra reductions.','relations':[(str(a),str(b)) for a,b in relations],'checks':checks}
Path('POST_EXPOSURE_LINE_IDENTITIES.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
