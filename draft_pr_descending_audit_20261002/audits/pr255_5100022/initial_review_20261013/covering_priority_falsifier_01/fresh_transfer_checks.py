"""Independent polynomial checks of the earlier covering lemmas.

These certify displayed finite algebra; the arbitrary-period closure,
central-pairing, and meromorphic theorem are justified in REPORT.md.
No numeric experiment is used as proof.
"""
from pathlib import Path
from datetime import datetime, timezone
import json
import sympy as s

out = Path(__file__).resolve().parent
a,b,c,x,y,C,S,lam,U = s.symbols('a b c x y C S lambda U')
ring = s.groebner([c*c-a*a+b*b, y*y+x*x-1, S*S+C*C-1],
                 c,y,S,a,b,x,C,lam,order='lex',domain=s.QQ)
checks = []

def polynomial(name, expression):
    remainder = ring.reduce(s.expand(expression))[1]
    assert remainder == 0, (name, remainder)
    checks.append({'name': name, 'result': 'PASS', 'remainder': '0'})

def rational(name, expression):
    remainder = s.factor(s.cancel(expression))
    assert remainder == 0, (name, remainder)
    checks.append({'name': name, 'result': 'PASS', 'remainder': '0'})

def det(p,q):
    return p[0]*q[1]-p[1]*q[0]

P = s.Matrix([a*(x*C+y*S), b*(y*C-x*S)])
Q = s.Matrix([a*(x*C-y*S), b*(y*C+x*S)])
F = s.Matrix([c,0])
p,q = P-F,Q-F
W = b*b*x*x+a*a*y*y
z = c*x
polynomial('actual original edge determinant', det(P,Q)-2*a*b*S*C)
polynomial('actual focal edge determinant', det(p,q)-2*b*S*(a*C-z))
polynomial('focal squared-distance formula at P', p.dot(p)-(a-c*(x*C+y*S))**2)
polynomial('focal squared-distance formula at Q', q.dot(q)-(a-c*(x*C-y*S))**2)
numerator = p.dot(p)*q.dot(q)-(p.dot(p)+q.dot(q))*p.dot(q)/2
H = (2*b*b-W)*(a-z*C)**2+W*(W-b*b)*S*S
polynomial('actual antipedal grouped-area numerator', numerator-2*S*S*H)
sin2Q = 2*(x*C-y*S)*(y*C+x*S)
sin2P = 2*(x*C+y*S)*(y*C-x*S)
polynomial('weighted midpoint-angle telescope', det(P,Q)*(x*x-y*y)-a*b*(sin2Q-sin2P)/2)

A,B,Z,V = s.symbols('alpha beta z V')
Hp=(2*B-U)*(a-Z*C)**2+U*(U-B)*(1-C*C)
Hm=(2*B-U)*(a+Z*C)**2+U*(U-B)*(1-C*C)
pair_n=(2*B-U)*(a*a+Z*Z*C*C-2*Z*Z)+U*(U-B)*(1-C*C)
rational('opposite-edge common-denominator combination', Hp*(a*C+Z)+Hm*(a*C-Z)-2*a*C*pair_n)
ratio=pair_n/(B*(a*a*C*C-Z*Z))
ratio=ratio.subs({a*a:A,Z*Z:A-U,C*C:1-lam*U/(A*B)},simultaneous=True)
rational('antipedal opposite-edge ratio', ratio-(2-(A*B-(A+B)*lam)*U/(A*B*(B-lam))))
R=2-(A+B)*(A*B-(A+B)*lam)/(2*A*B*(B-lam))
rational('summed antipedal constant R',R-(A*B*(3*B-A)+lam*(A-B)**2)/(2*A*B*(B-lam)))
polynomial('pedal frame-bracket simplification',
            a*b*b*(a-c*x)*W+c**3*x*y*y*(a-c*x)*W
            +(a-c*x)**2*(c*c*y*y*(W-lam)-b*b*lam)
            -(a-c*x)*(a*(W-lam)+c*x*lam)*W)
polynomial('velocity-coordinate telescope numerator',
            c*c*(b*b*x*x-a*a*y*y)-(2*a*a*b*b-(a*a+b*b)*W))
Wp=a*a-c*c*x*x
rational('centrally paired focal-pedal local terms',
         (a*a-lam+a*c*x)/(a+c*x)**2+(a*a-lam-a*c*x)/(a-c*x)**2
         -2*((a*a+lam)/Wp-2*a*a*lam/Wp**2))
rational('focal pedal positive coefficient after telescope',
         A+lam-2*A*lam*(A+B)/(2*A*B)-A*(B-lam)/B)

report={'status':'PASS','checked_utc':datetime.now(timezone.utc).isoformat(),
        'sympy_version':s.__version__,'exact_check_count':len(checks),
        'checks':checks,'finite_checks_prove_all_periods':False,
        'claim':'Fresh independent algebra for the original-source covering corollary; full general-period argument is written separately.'}
(out/'FRESH_TRANSFER_CHECKS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
