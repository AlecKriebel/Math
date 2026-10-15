"""Independent selected Bernstein check using direct cardinal derivatives.

The transformed part uses an independently implemented Fejer rule and the
source's analytic quadrature remainder theorem, whose hypotheses and proof
are audited in SOURCE_REVIEW.md. No supplied certificate code is imported.
This checks all 2,436 finite Bernstein coefficients. It does not certify
matrix inversion, residuals, approximation errors, or unbounded tails.
"""
from pathlib import Path
from math import factorial, comb
import hashlib, json, datetime
import flint
from flint import arb, acb, ctx
ctx.prec = 192
ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT/'target_b/sources/openai_090'
pi = arb.pi()
b = arb(3).sqrt()/2
h = arb(2)/5
ii = acb(0,1)
P = [acb(5),-1+2*ii*b,1+2*ii*b,acb(-2),-arb(1)/2+ii*b,
     -1-2*ii*b,acb(1)]
ts = [arb(k)/6 for k in range(7)]
rows = [[int(x) for x in line.split()] for line in
        (SRC/'verification/data/coefficients.tsv').read_text().splitlines()]
lists = [{0:(arb(1),arb(44)/100)}, {0:(arb(0),-arb(368)/1000)}]
for row in rows:
    for j in range(2):
        lists[j][row[0]] = (arb(row[1+2*j])/10**10, arb(row[2+2*j])/10**10)
constants = [-arb(13)/1000,arb(17)/1000]

def phase(x):
    return (ii*pi*x).exp()

def direct_jet(index,m,ell):
    aa = []
    for k in range(ell+3):
        # Full frequency list is obtained by conjugate reflection.
        value = P[0] if k==0 else acb(0)
        for j in range(1,7):
            term = P[j]*phase(ts[j]*m)*(ii*pi*ts[j])**k
            value += term + term.conjugate()
        aa.append(value.real/factorial(k))
    cc,dd = lists[index].get(m,(arb(0),arb(0)))
    ans = cc*aa[ell+2]+dd*aa[ell+1]
    for k in range(2,ell+1):
        r = ell-k
        rr = constants[index] if r==0 else arb(0)
        rr += (-1)**r*sum((r+1)*c/arb(m-n)**(r+2)+d/arb(m-n)**(r+1)
                         for n,(c,d) in lists[index].items() if n!=m)
        ans += aa[k]*rr
    return ans

def transformed_jets(index,m,y,maxell):
    # Tabulated input is supported through 100; list norm < 3, |C|<1.
    result = [acb(0) for _ in range(maxell+1)]
    N = 256
    grid = []
    for v in range(N):
        alpha = arb(2*v+1)/(2*N)
        weight = (1-2*sum((2*a*pi*alpha).cos()/arb(4*a*a-1)
                         for a in range(1,N//2)))/N
        assert weight > 0
        grid.append((alpha,weight))
    for j in range(1,7):
        # Combine finite density columns analytically before evaluation.
        l0 = {n:sum(P[k]*phase(ts[k]*n) for k in range(j,7)) for n in lists[index]}
        l1 = {n:sum(ts[k]*P[k]*phase(ts[k]*n) for k in range(j,7)) for n in lists[index]}
        for alpha,weight in grid:
            t = (arb(2*j-1)+(pi*alpha).cos())/12
            density = 2*pi*sum(phase(-t*n)*(-pi*c*(l1[n]-t*l0[n])+ii*d*l0[n])
                               for n,(c,d) in lists[index].items())
            lam = ii/(b*(t+ii*h))
            z = -(arb(4)/3)/(t+ii*h)-ii*h
            base = weight/6*density*lam*phase(z*m)
            current = acb(1)
            for ell in range(maxell+1):
                result[ell] += base*current
                current *= ii*pi*z*y/(ell+1)
    for j,t in enumerate(ts):
        mass = constants[index]*P[j]*(1 if j==0 else 2)
        lam = ii/(b*(t+ii*h))
        z = -(arb(4)/3)/(t+ii*h)-ii*h
        base = mass*lam*phase(z*m)
        current = acb(1)
        for ell in range(maxell+1):
            result[ell] += base*current
            current *= ii*pi*z*y/(ell+1)
    return [v.real+arb(0,'1e-22') for v in result]

centers = [0]+[row[0] for row in rows if row[0]<=40]
node_order = [0]+[row[0] for row in rows]
triples=[]
for index in range(2):
    for m in centers:
        pos=node_order.index(m)
        offsets=[(node_order[pos+1]-m,2)]
        if m>0:
            offsets.append((node_order[pos-1]-m,2))
        for ys in offsets:
            if index==0 and (m==0 or (m==1 and ys[0]<0)):
                continue
            nu=0 if m==0 else (1 if index==0 and m==1 else 2)
            triples.append((index,m,ys,nu))
assert len(triples)==84

def grouped_lower(index,m):
    if m==0: return arb('0.762')
    if m==1: return arb('0.314' if index==0 else '0.191')
    if m<=4: return arb('0.028' if index==0 else '0.024')
    if m<=9: return arb('0.114' if index==0 else '0.112')
    if m<=16: return arb('0.0105' if index==0 else '0.0094')
    if m<=21: return arb('0.123' if index==0 else '0.113')
    if m<=28: return arb('0.0111' if index==0 else '0.0113')
    if m<=33: return arb('0.121' if index==0 else '0.126')
    return arb('0.0107' if index==0 else '0.0115')

checks=[]
for index,m,ys,nu in triples:
    y = arb(ys[0])/ys[1]
    transformed = transformed_jets(1-index,m,y,28+nu)
    power=[]
    sigma = -1 if index==0 else 1
    for r in range(29):
        ell = r+nu
        power.append(sigma*(y**r*direct_jet(index,m,ell)+transformed[ell]/y**nu))
    bs=[]
    for k in range(29):
        value=sum(arb(comb(k,r))/comb(28,r)*power[r] for r in range(k+1))
        assert value > grouped_lower(index,m), (index,m,str(y),k,str(value))
        bs.append(str(value))
    checks.append({'function_index':index+1,'center':m,'y':str(y),'order':nu,
                   'claimed_group_lower':str(grouped_lower(index,m)),
                   'all_29_bernstein_enclosures':bs})
receipt={
 'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'implementation_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'coefficient_table_sha256':hashlib.sha256((SRC/'verification/data/coefficients.tsv').read_bytes()).hexdigest(),
 'arithmetic':'python-flint '+flint.__version__+' Arb/Acb at 192 bits',
 'direct_part':'Independent node-Taylor cardinal formula, no quadrature',
 'transformed_part':'Independent Fejer N=256 implementation; manuscript analytic moment radius 1e-22',
 'coverage':'All 84 half-gaps and 2436 Bernstein coefficients. Does not verify full global signs or matrix inversion.',
 'status':'pass_all_finite_bernstein_grouped_claims',
 'checks':checks,
}
Path(__file__).with_name('independent_arb_bernstein_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k!='checks'},indent=2))
print('Confirmed',len(checks),'half-gaps and',len(checks)*29,'coefficient inequalities.')
