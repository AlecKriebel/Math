"""Exact algebra and rational interval checks; no floating-point proof steps."""
import sympy as S
import json
from pathlib import Path
x,t,z=S.symbols('x t z', nonzero=True)
a_pieces=[(-1,0,(2+x)**2),(0,2,(2-x)**2)]
b_pieces=[(-1,1,2+x)]

def moment(pieces,n):
    return sum(S.integrate(x**n*p,(x,l,u)) for l,u,p in pieces)
def integral(pieces):
    return sum(S.integrate(x*p*S.exp(-t*x),(x,l,u)) for l,u,p in pieces)
A=(t**3+t**2-2*t-6)*S.exp(3*t)+16*t*S.exp(2*t)+4*t+6
B=(t*t-2)*S.exp(2*t)+3*t*t+4*t+2
assert S.simplify(integral(a_pieces)*t**4*S.exp(2*t)+A)==0
assert S.simplify(integral(b_pieces)*t**3*S.exp(t)+B)==0
assert moment(a_pieces,0)==5
assert moment(b_pieces,0)==4
assert moment(a_pieces,1)==S.Rational(5,12)
assert moment(b_pieces,1)==S.Rational(2,3)

def enclosure(pieces,at,range_radius,abs_integral_bound,N=30):
    # |remainder exp(-at*x)| <= 3 (at*radius)^(N+1)/(N+1)!
    # because |at*x|<1 and exp(1)<3.
    at=S.Rational(at)
    assert at>0 and at*range_radius<1
    center=sum((-at)**k/S.factorial(k)*moment(pieces,k+1) for k in range(N+1))
    error=3*abs_integral_bound*(at*range_radius)**(N+1)/S.factorial(N+1)
    return center-error,center+error

out={}
for name,pieces,radius,M,lo,hi in [
    ('a',a_pieces,2,24,'0.27379184','0.27379185'),
    ('b',b_pieces,1,6,'0.52761951','0.52761953')]:
    lower=enclosure(pieces,lo,radius,M)
    upper=enclosure(pieces,hi,radius,M)
    assert lower[0]>0,(name,lo,lower)
    assert upper[1]<0,(name,hi,upper)
    out[name]={'root_bracket':[lo,hi],'moment_at_left_enclosure':[str(S.N(u,15)) for u in lower],
        'moment_at_right_enclosure':[str(S.N(u,15)) for u in upper],
        'certification':'Exact rational Taylor sums and exact rational remainder bounds; decimal values only display bounds.'}

normals=[(1,0),(0,1),(-1,1),(0,-1)]
assert all(S.det(S.Matrix([normals[i],normals[(i+1)%4]]))==1 for i in range(4))
assert len({1,2,3,4})==4
# F1 exponential polynomial coefficients cannot both vanish.
assert S.gcd(t*t-2,3*t*t+4*t+2)==1
# Optional finite spot checks of the general proof, NOT its replacement.
resultants=[]
for p,q in [(1,1),(1,2),(2,1),(3,2),(2,3)]:
    r=S.Rational(p,q)
    Az=((r*t)**3+(r*t)**2-2*r*t-6)*z**(3*p)+16*r*t*z**(2*p)+4*r*t+6
    Bz=(t*t-2)*z**(2*q)+3*t*t+4*t+2
    res=S.resultant(Az,Bz,z)
    assert res!=0
    resultants.append({'p':p,'q':q,'resultant_degree':int(S.degree(res,t))})
out['checks']={'A_exponential_identity':True,'B_exponential_identity':True,'unweighted_moments':['5/12','2/3'],
               'DH_masses':[5,4],'toric_fan_unimodular':True,'B_coefficients_coprime':True,
               'sample_resultants_nonzero':resultants,'all_ratios_proof':'See irrationality lemma in authored proof; no bounded-search inference.'}
Path(__file__).with_name('CHECK_RESULTS.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
