"""Generate exact polynomial certificates; verification needs no SymPy."""
import sympy as s
import json
from pathlib import Path

x,t=s.symbols('x t')
P=lambda z,r:s.prod(z+i for i in range(1,r+1))
rows=[]
for r in range(3,7):
    for u in range(1,r):
        for v in range(1,r-u):
            width=r-u-v
            shift=1 if (r,u,v)==(6,2,3) else 0
            A=x+shift;B=A+1+t
            poly=P(A,r)**width*P(B+v,width)**r-P(B,r)**width*P(A+u,width)**r
            const,factors=s.factor_list(poly)
            const=int(const);out=[]
            for f,e in factors:
                pp=s.Poly(f,x,t)
                if all(c<=0 for c in pp.coeffs()):
                    f=-f;const*=(-1)**e;pp=s.Poly(f,x,t)
                assert all(c>=0 for c in pp.coeffs())
                assert pp.coeff_monomial(1)>0
                out.append({'power':int(e),'terms':[[int(a),int(b),int(c)] for (a,b),c in pp.terms()]})
            rows.append({'r':r,'u':u,'v':v,'s':width,'A_shift':shift,'prefactor':const,'positive_factors':out})
data={'description':'D=P_r(A)^s P_s(B+v)^r-P_r(B)^s P_s(A+u)^r, B=A+1+t. All factors have nonnegative coefficients and positive constant. Exceptional(6,2,3) uses A=x+1; A=0 handled separately.','cases':rows,
      'boundary_quartic_coefficients_ascending':[-9620,-8672,-2523,-230,1]}
Path(__file__).with_name('TURN_2_CERTIFICATES.json').write_text(json.dumps(data,separators=(',',':'),sort_keys=True)+'\n')
print('generated',len(rows),'certificates')
