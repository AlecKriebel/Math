#!/usr/bin/env python3
"""Independent audit controls; no network and no writes to the frozen input.
Usage: python adversarial_checks.py /path/to/safe_output [result_path]
Analytic proofs and scope limitations are in INDEPENDENT_AUDIT.md.
"""
from fractions import Fraction as R
from pathlib import Path
import hashlib, json, subprocess, sys, tempfile
import sympy as S

EXPECTED_MANIFEST = 'cf78e841bb4c939d8dadefd05f76447a6a5b18629748290a047c9fb03996f932'
root = Path(sys.argv[1]).resolve()
output = Path(sys.argv[2]) if len(sys.argv)>2 else Path(__file__).with_name('ADVERSARIAL_RESULTS.json')
checks=[]
def check(name, assertion):
    if not bool(assertion): raise AssertionError(name)
    checks.append(name)
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

before={p.name:(len(p.read_bytes()),sha(p)) for p in root.iterdir() if p.is_file()}
check('exact frozen manifest binding',sha(root/'MANIFEST.json')==EXPECTED_MANIFEST)
manifest=json.loads((root/'MANIFEST.json').read_text())
for item in manifest['files']:
    p=root/item['path']
    check('frozen bytes and hash: '+item['path'],len(p.read_bytes())==item['bytes'] and sha(p)==item['sha256'])
with tempfile.TemporaryDirectory() as td:
    script=Path(td)/'exact_controls.py'
    script.write_bytes((root/'exact_controls.py').read_bytes())
    proc=subprocess.run([sys.executable,str(script)],capture_output=True,text=True,check=True)
    replay=json.loads(proc.stdout)
    check('original controls replay all 48',replay['status']=='passed' and replay['checks_passed']==48)
    check('original exact result byte-identical', (Path(td)/'EXACT_RESULTS.json').read_bytes()==(root/'EXACT_RESULTS.json').read_bytes())

z,w,t,a,x=S.symbols('z w t a x',real=True)
I=S.I
E=z-(S.exp(2*I*z)-1-2*I*z)/40
T=z+(1-S.cos(2*z))/40
Ep=S.diff(E,z)
check('E derivative sign and denominator',S.simplify(Ep-1-(S.exp(2*I*z)-1)/(20*I))==0)
check('E derivative globally periodic, not entire-plane injective',S.simplify(Ep.subs(z,z+S.pi)-Ep)==0)
check('E reflected derivative conjugation',S.simplify(S.conjugate(Ep)-(1+(S.exp(-2*I*z)-1)/(-20*I)))==0)
check('T normalized and unchanged positive a2',T.subs(z,0)==0 and S.diff(T,z).subs(z,0)==1 and S.diff(T,z,2).subs(z,0)/2==S.Rational(1,20))
check('T derivative two-point collision formula',S.trigsimp(S.diff(T,z).subs(z,S.pi/4+t)-S.diff(T,z).subs(z,S.pi/4-t))==0)
check('T critical point simple',S.diff(T,z,2).subs(z,S.pi/4)==0 and S.diff(T,z,3).subs(z,S.pi/4)==-S.Rational(1,5))

# Independent pi enclosure: atan(1/2)+atan(1/3)=pi/4.
# Each argument is positive and the tangent addition formula is exactly 1.
def atan_interval(v, terms=40):
    v=R(v)
    total=sum(((-1)**k*v**(2*k+1)/R(2*k+1) for k in range(terms)),R(0))
    following=total+(-1)**terms*v**(2*terms+1)/R(2*terms+1)
    return min(total,following),max(total,following)
check('independent atan addition identity',(R(1,2)+R(1,3))/(1-R(1,2)*R(1,3))==1)
lo1,hi1=atan_interval(R(1,2));lo2,hi2=atan_interval(R(1,3))
pi_lo,pi_hi=4*(lo1+lo2),4*(hi1+hi2)
check('independent pi enclosure',R(28,9)<pi_lo<pi_hi<R(22,7))
check('symmetrized derivative collision pair strictly in disk',0<pi_lo/4-R(1,10) and pi_hi/4+R(1,10)<1)
check('E period larger than disk diameter',pi_lo>2)

# Independent e bound via the series for e rather than the supplied e^2 series.
e_lower=sum((R(1,S.factorial(k)) for k in range(9)),R(0))
e_upper=e_lower+R(1,S.factorial(9))/(1-R(1,10))
check('independent e bound implies e squared below 8',e_upper**2<8)
check('sharper E derivative disk bound',(e_upper**2-1)/20<R(7,20)<1)

P=z+2*a*(1/(1-z)+S.log(1-z)-1)
check('P derivative numerator for arbitrary a',S.simplify(S.diff(P,z)*(1-z)**2-(z*z+(2*a-2)*z+1))==0)
check('P second derivative no interior zero formula',S.simplify(S.diff(P,z,2)-2*a*(1+z)/(1-z)**3)==0)
Pa=P.subs(a,S.Rational(9,5))
check('P 9/5 derivative boundary factorization',S.expand((z+S.Rational(4,5)-3*I/5)*(z+S.Rational(4,5)+3*I/5))==z*z+S.Rational(8,5)*z+1)
check('P 9/5 collision threshold rigorously passed',R(9,5)*(pi_lo-2)>2)
def J_box(r):
    l,h=atan_interval((1-r)/(1+r))
    atanlo,atanhi=pi_lo/4-h,pi_hi/4-l
    c=r+R(18,5)*r/(1+r*r)
    return c-R(18,5)*atanhi,c-R(18,5)*atanlo
jl,jr=J_box(R(19,20)),J_box(R(49,50))
check('independent positive collision endpoint',jl[0]>0)
check('independent negative collision endpoint',jr[1]<0)
check('collision endpoints strictly interior',0<R(19,20)<R(49,50)<1)

C=(2+S.sqrt(13))/3
check('C is positive quadratic root',S.simplify(3*C*C-4*C-3)==0 and C>0)
check('C strictly above counterexample parameter',C>S.Rational(9,5))
check('C below 2, no accidental endpoint substitution',C<2)
check('triangle equality coefficients',S.simplify(C*C-4*C/3)==1)
# Equality in area theorem for the odd transform yields the Koebe coefficients.
b2,b3=S.symbols('b2 b3')
u=S.series((1+b2*z*z+b3*z**4)**(-S.Rational(1,2)),z,0,6).removeO()
check('odd transform exterior first coefficient',S.expand(u).coeff(z,2)==-b2/2)
check('odd transform exterior next coefficient',S.expand(u).coeff(z,4)==3*b2*b2/8-b3/2)
check('Koebe equality next coefficient',S.solve(S.Eq((3*b2*b2/8-b3/2).subs(b2,2),0),b3)==[3])

# Explicit controls for compactification and the nonzero lower coefficient bound.
epsilon=S.symbols('epsilon',positive=True)
f_eps=z+epsilon*z*z
check('identity approximant normalized derivative affine',S.diff(f_eps,z)==1+2*epsilon*z and S.diff(f_eps,z,2)==2*epsilon)
f0=z/(1-z)
check('lower model derivative collision factorization',S.simplify(S.diff(f0,z)-S.diff(f0,z).subs(z,w)-(z-w)*(2-z-w)/((1-z)**2*(1-w)**2))==0)
for n in [2,3,8]:
    check('lower model coefficient one n='+str(n),S.expand(S.series(f0,z,0,9).removeO()).coeff(z,n)==1)

# Independently match the integral-form candidate using its logarithmic derivative.
# At the origin log((1+iz)/(1-iz))=0; coefficient checks fix the analytic branch.
log_series=S.series((S.log(1+I*z)-S.log(1-I*z))/I,z,0,10).removeO()
expected_log=sum(S.Rational(2*(-1)**k,2*k+1)*z**(2*k+1) for k in range(5))
check('candidate logarithmic integrand sign and parity',S.expand(log_series-expected_log)==0)
Q=sum(S.Rational(2*(-1)**k,(2*k+1)**2)*x*z**(2*k+1) for k in range(5))
check('candidate Q derivative integral equivalence',S.expand(z*S.diff(Q,z)-x*expected_log)==0)
# Exponential coefficients via recurrence, independent of exp-series expansion.
h=[S.Integer(1)]
for n in range(1,9):
    h.append(S.expand(sum(j*Q.coeff(z,j)*h[n-j] for j in range(1,n+1))/n))
coeff={n:S.expand(sum((2*(n-1-j)+1)*h[j] for j in range(n))/n) for n in range(2,9)}
known={2:S.Rational(3,2)+x,3:S.Rational(5,3)+2*x+S.Rational(2,3)*x*x,
       4:S.Rational(7,4)+S.Rational(22,9)*x+S.Rational(3,2)*x*x+x**3/3}
for n in known:check('candidate independent recurrence coefficient n='+str(n),S.expand(coeff[n]-known[n])==0)
for n in [1,2,10,100]:
    check('dominated convergence weights bounded n='+str(n),all(R(0)<R(2*n-2*j-1,n)<2 for j in range(n)))
check('candidate norm constant',S.simplify((2/S.pi)*(S.pi**2/8)-S.pi/4)==0)

outcome=json.loads((root/'READINESS_AND_OUTCOME.json').read_text())
check('frozen full-solution claim correctly false',outcome['full_target_solved'] is False)
check('five-approach exhaustion recorded',outcome['attempt_status']=='exhausted' and outcome['turns_used']==5)
check('frozen remote-write claim false',outcome['remote_state_changed'] is False)
after={p.name:(len(p.read_bytes()),sha(p)) for p in root.iterdir() if p.is_file()}
check('frozen inputs byte-for-byte preserved',before==after)
result={'status':'passed','frozen_manifest_sha256':EXPECTED_MANIFEST,
        'original_replay_checks_passed':48,'independent_checks_passed':len(checks),
        'sympy_version':S.__version__,'checks':checks,
        'interval_metadata':{'pi_lower':str(pi_lo),'pi_upper':str(pi_hi),
                             'e_upper':str(e_upper),'collision_left_lower':str(jl[0]),'collision_right_upper':str(jr[1])},
        'frozen_inputs_unchanged':before==after,
        'limits':'Computational checks establish algebra and rational bounds, not compactness, global injectivity, candidate membership, sharpness, novelty, or current open status.'}
output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','original_replay_checks_passed','independent_checks_passed','frozen_inputs_unchanged']}))
