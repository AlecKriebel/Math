"""Model transport, marked chord law, primary-table and public-coefficient linkage."""
from pathlib import Path
import datetime,hashlib,json
import sympy as S
root=Path(__file__).resolve().parent
audit=root.parents[3]
x,xi,lam,b,v,A,B,C=S.symbols('x xi lambda beta v A B C');r=S.sqrt(5)
phi=(1+r)/2;c=(11+5*r)/2;d=5+2*r;m=5-2*r
alpha=1-r/5;gamma=2*r/5;e=gamma-alpha
beta=(11-5*r)*lam/(2*(lam+5*r));k=4*(lam+5*r)/r;q=d*k*k
a0=m;a1=(-26+10*r)*lam-20*r
a2=(42-86*r/5)*lam**2+(-100+100*r)*lam+500+200*r
a3=(-112+48*r)*lam**2*(lam+5*r)/5
T=4*x**3+(b*b-6*b+1)*x*x+2*(b*b-b)*x+b*b
checks=[]
def ck(n,a,z=0):
    diff=S.simplify(S.cancel(a-z,extension=r))
    if diff!=0:raise AssertionError(n+': '+str(diff))
    checks.append(n)
ck('Complete cubic equation transport',q**3*T.subs({b:beta,x:xi/q+beta})/4,xi**3+a2*xi*xi+a1*a3*xi+a0*a3*a3)
Delta=b**5*(b*b-11*b-1)
Dl=S.factor(Delta.subs(b,beta),extension=r)
assert S.Poly(S.together(Dl).as_numer_denom()[0],lam).degree()==6
ck('delta conjugate infinity slope square',5/d,m)
F0=2*x*(x**4-10*x*x+5)
ck('F0 factorization',F0,2*x*(x*x-d)*(x*x-m))
ck('Infinity X-partial at slope zero',S.diff(F0,x).subs(x,0),10)
for dd,expected in [(d,160+80*r),(m,160-80*r)]:
    ck('Infinity X-partial at square '+str(dd),10*dd**2-60*dd+10,expected)
# Tangent P0 has slope zero and third point (beta,0); generalized negation
# gives 2P0=(beta,beta^2). Secant P0,2P0 has slope beta.
slope=b;xx=S.expand(slope*slope+(1-b)*slope+b-0-b)
yy=S.expand(-(slope+1-b)*xx+b)
ck('Direct 3P0 abscissa',xx,b);ck('Direct 3P0 ordinate',yy,0)
ck('2P0 and 3P0 are negatives',b*b+(1-b)*b-b,0)
# Decode our fresh coefficient output; compare all generic fields to public record.
raw=(root/'native/kernel_exact_v01/stdout.bin').read_text();dec=json.JSONDecoder();_,n=dec.raw_decode(raw);own,_=dec.raw_decode(raw[n:].lstrip())
public=Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr329_20000450/preprint_review_02/phase3/archive_replay')
expected=json.loads((public/'expected/division_chord.json').read_text())
c0,c1,c2=S.symbols('c0 c1 c2');subs={c2:A,c1:B,c0:C}
loc={'x':x,'c0':c0,'c1':c1,'c2':c2,'A':A,'B':B,'C':C}
ck('Public generic psi3 agrees with fresh Vieta derivation',S.sympify(expected['third_from_chord'],locals=loc).subs(subs),S.sympify(own['generic_psi3'],locals=loc))
ck('Public generic H6 agrees with fresh Vieta derivation',S.sympify(expected['fourth_over_2v_from_chord'],locals=loc).subs(subs),S.sympify(own['generic_H6'],locals=loc))
for j,(old,new) in enumerate(zip(expected['generic_fifth_coefficients'],own['generic_Q5_coefficients'])):
    ck('Public generic Q5 coefficient x^'+str(12-j),S.sympify(old,locals=loc).subs(subs),S.sympify(new,locals=loc))
# Independently transcribed all eleven rows from visually read actual Morton v4 p5.
oldb=S.symbols('old_b')
morton=[5,5+25*oldb+5*oldb**2,1+38*oldb+44*oldb**2+7*oldb**3+oldb**4,
9*oldb+127*oldb**2+26*oldb**3+3*oldb**4-oldb**5,
36*oldb**2+248*oldb**3+19*oldb**4-3*oldb**5+oldb**6,
84*oldb**3+322*oldb**4+71*oldb**5+3*oldb**6-oldb**7,
126*oldb**4+293*oldb**5+94*oldb**6+12*oldb**7+oldb**8,
125*oldb**5+180*oldb**6+50*oldb**7+5*oldb**8,80*oldb**6+65*oldb**7+10*oldb**8,30*oldb**7+10*oldb**8,5*oldb**8]
for j,co in enumerate(morton):ck('Morton v4 p5 residual row x^'+str(10-j),co.subs(oldb,-b),S.sympify(own['residual_coefficients'][str(10-j)],locals={'beta':b}))
print(json.dumps({'status':'EXACT_PASS','checks':checks,'Tate_discriminant_lambda_factor':str(Dl),
 'Morton_v4_source_path':'/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr329_20000450/preprint_review_02/phase3/morton_v4.pdf',
 'Morton_v4_source_sha256':hashlib.sha256(Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr329_20000450/preprint_review_02/phase3/morton_v4.pdf').read_bytes()).hexdigest(),
 'scope':'Exact transport, infinity smoothness/slopes, symbolic marked group law, every generic exported coefficient and Morton v4 residual coefficient. Existing source PDF independently inspected; no claim of a second independent network retrieval for Morton.'},indent=2))
