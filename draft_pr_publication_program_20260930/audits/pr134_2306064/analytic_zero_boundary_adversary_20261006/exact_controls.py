#!/usr/bin/env python3
"""Small exact algebra controls supplementing the independent analytic proof.
No original checker is imported or executed; finite controls do not prove the
all-functions/all-real-parameter analytic assertion.
"""
from fractions import Fraction as F
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os

count = 0
def check(value):
    global count
    count += 1
    if not value:
        raise AssertionError(f'Exact control {count} failed')

def j(alpha, c, z):
    x = c*z
    return (1-(4+alpha)*x+4*x*x)/((1-x)*(1-2*x))

ks = [F(1,10**12),F(1,100),F(1,3),F(1,2),F(1),F(3,2),F(10),F(10**6)]
records=[]
for k in ks:
    alphas = [('negative', -2*k*k/(3*k+1))]
    if k <= 1:
        alphas.append(('between_endpoints',2*k*k/(k+1)))
    if k > 1:
        alphas.append(('above_one',2*k*(k+1)/(3*k+1)))
    for family,alpha in alphas:
        a,b=abs(1-alpha),abs(alpha)
        d=a+2*b-1
        check(2*k*k-d*k-b==0)
        check(a/(1+2*k)+b/k==1)
        check(k>0 and b>0 and d>0)
        check(d/2<k<d/2+b/d)
        records.append({'family':family,'k':str(k),'alpha':str(alpha)})
        for n in [2,3,1000]:
            w=n*(1+k*(n-1))
            check(w-1==(n-1)*(1+k*n))
            check(w-n==k*n*(n-1))
        if 0<alpha<=1:
            cstar=1/(2*(1+k))
            check(0<cstar<F(1,2))
            check(j(alpha,cstar,F(1))==0)
            check(j(alpha,cstar,F(99,100))>0)
            lam=k/2
            upper=min(F(1,2),1/(2*(1+lam)))
            c=(cstar+upper)/2
            z=(1+cstar/c)/2
            check(cstar<c<upper)
            check(0<z<1)
            check(2*(1+lam)*c<1)
            check(j(alpha,c,z)<0)

check(j(F(1,2),F(8,25),F(31,32))==F(-53,1311))
check(2*(1+F(1,2))*F(8,25)==F(24,25))
for alpha,c in [(F(0),F(1,2)),(F(1),F(1,4))]:
    z=F(99,100)
    check(j(alpha,c,z)==(1-z)/(1-z/2))
    check(j(alpha,c,z)>0)
# Exact telescoping first moments for the infinite-second-moment example.
for N in [2,3,10,100]:
    B=sum((F(1,n*(n-1)) for n in range(2,N+1)),F(0))
    check(B==1-F(1,N))

receipt={
    'schema':'pr134-independent-analytic-supplemental-controls/v1',
    'UTC':datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),
    'actual_operator_PID':os.getpid(),
    'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'assertions':count,
    'all_passed':True,
    'exact_parameter_cases':records,
    'purpose':'algebra, endpoint boundary witnesses, naive-interpolation counterexample, telescoping first moment',
    'analytic_claim_proved_by':'AUDIT.md disk-local proof, not finite sampling',
    'original_checker_imported_or_executed':False,
    'new_central_proof_search_turns':0,
}
Path(__file__).with_name('EXACT_CONTROLS.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'UTC':receipt['UTC'],'actual_operator_PID':os.getpid(),'assertions':count,'all_passed':True},indent=2))
