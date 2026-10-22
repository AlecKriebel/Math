from pathlib import Path
import sympy as z,json
k,t,s=z.symbols("k t s");h,C,d,x,y,kp=z.symbols("h C d x y kp")
G=z.groebner([h*h-t,C*C-(1-t),d*d-(1-k*k*t),x*x-(1-s*s),y*y-(1-k*k*s*s),kp*kp-(1-k*k)],h,C,d,x,y,kp,domain=z.QQ.frac_field(k,t,s))
D=1-k*k*t*s*s;sm=(s*C*d-h*x*y)/D;sp=(s*C*d+h*x*y)/D;cm=(x*C+s*h*y*d)/D;cp=(x*C-s*h*y*d)/D;q=1-t
U=1-2*k*k*t+k*k*t*t;V=1-2*t+k*k*t*t;W=1-k*k*t*t;Ao=d*d/q;Bo=kp/q;L0=(U*U-k*k*V*V*t)/d;L1=(V*V-U*U*t)/C;Z=W*W-4*k*k*t*t*q*d*d
rawdet=((-Ao*sm-k)*(Bo*cp)-(Bo*cm)*(-Ao*sp-k))/2
checks={"distance":(-Ao*s-k)**2+(Bo*x)**2-(1+k*s)*(U+k*V*s)/q**2,"factor1":(1+k*sm)*(1+k*sp)-(d+k*C*s)**2/D,"factor2":(U+k*V*sm)*(U+k*V*sp)-(d+k*C*s)*(L0+k*L1*s)/D,"determinant":rawdet-Bo*h*d*y*(d+k*C*s)/(C*D),"middle_coefficient":d*d*(V*V-U*U*t)+q*(U*U-k*k*V*V*t)-2*U*V*q*d*d,"triple_D":U*U-k*k*V*V*t-d*d*(U*W-2*k*k*t*q*V),"triple_C":V*V-U*U*t-q*(V*W-2*t*d*d*U),"L_gap":L0*L0-k*k*L1*L1-(1-k*k)*Z*Z}
out={}
for name,ex in checks.items():
 n=z.fraction(z.cancel(ex))[0];r=G.reduce(n)[1];out[name]=str(z.factor(r));assert r==0,name
result={"independently_recomputed_residuals":out,"normalization":"alpha=1; homogeneity restores alpha; square-root quotient ring over Q(k,t,s)","exact":True,"meaning":"Rational identities after clearing denominators; domain nonvanishing and universal meromorphic claims are separately proved in DERIVATION.md"}
Path(__file__).with_name("SYMBOLIC_RESULTS.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
