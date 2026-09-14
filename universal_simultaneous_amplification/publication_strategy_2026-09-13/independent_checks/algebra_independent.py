"""Independent exact checks of the paper's reduced chain and rational witness.

Uses only the response formulas and the four-rate macro chain stated in the
paper; does not import any paper verifier. This does not verify the analytic
derivation of those formulas from the original population process.
"""
import sympy as s


def require(condition, message):
    if not bool(condition):
        raise RuntimeError(message)


r, sigma, lam = s.symbols('r sigma lam', real=True)
B = 2*(sigma-1)/(1+sigma*(r*r-1)) + lam/(r-1)
D = 2*(r*(2-r)-sigma)/(sigma+2*r*(r-1)) - lam
br = s.factor(B.subs({sigma:s.Rational(19,137),lam:s.Rational(20,27)}))
dr = s.factor(D.subs({sigma:s.Rational(19,137),lam:s.Rational(20,27)}))
bn = s.Poly(s.fraction(br)[0],r)
dn = s.Poly(s.fraction(dr)[0],r)
# A rational interval where both numerator signs stay strictly positive.
# Denominators are manifestly positive for r>1.
right = s.Rational(15017,10000)
for poly in (bn,dn):
    require(poly.count_roots(1,right)==0, 'response numerator has a zero')
    require(poly.eval(s.Rational(3,2))>0, 'response sign is nonpositive')
require(right>s.Rational(3,2), 'interval does not cross 3/2')
print('PASS rational witness: both corrections positive on (1, 1.5017]')

# Exact finite q chain: solve independently, including arbitrarily many
# adverse center reversals, rather than replacing a sweep by survival.
for q in range(1,8):
    for A,dd,bb,cp in [(s.Rational(2,3),s.Rational(3,7),s.Rational(4,5),s.Rational(1,11)),
                        (s.Rational(1,7),s.Rational(8,3),s.Rational(1,20),s.Rational(4,3))]:
        states=[(h,k) for h in (0,1) for k in range(q+1)]
        transient=[state for state in states if state not in [(0,0),(1,q)]]
        variables=s.symbols('x:'+str(len(transient)))
        f=dict(zip(transient,variables)); f[(0,0)]=s.Integer(0); f[(1,q)]=s.Integer(1)
        equations=[]
        for h,k in transient:
            rates=[((1,k),k*A),((0,k-1),k*dd)] if h==0 else [((1,k+1),(q-k)*bb),((0,k),(q-k)*cp)]
            equations.append(sum(rate*(f[target]-f[(h,k)]) for target,rate in rates))
        solution=s.solve(equations,variables)
        ph=f[(1,0)].subs(solution)
        pp=f[(0,1)].subs(solution)
        require(s.factor(pp-A/(A+dd)*(bb+cp)/bb*ph)==0,'macro identity failed')
        require(1-ph<=q*cp/(bb+cp),'global sweep union bound failed')
        require(0<=ph<=1 and 0<=pp<=1,'committor outside [0,1]')
print('PASS macro chain: exact identities and sweep bound for q=1,...,7 and two rate regimes')
