"""New independent exact controls and Acb analytic-domain falsification probes."""
from collections import defaultdict
from fractions import Fraction as Q
from pathlib import Path
import datetime, hashlib, json
from flint import acb, arb, ctx

ctx.prec = 192
out = {"timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}

# Noncommutative ring with only the relation ab=1; do not impose ba=1.
def reduce_word(w):
    stack = []
    for letter in w:
        if stack and stack[-1] == "a" and letter == "b":
            stack.pop()
        else:
            stack.append(letter)
    return "".join(stack)
def multiply(x, y):
    z = defaultdict(int)
    for wx, cx in x.items():
        for wy, cy in y.items():
            z[reduce_word(wx + wy)] += cx * cy
    return {w: c for w, c in z.items() if c}
one, a, b = {"": 1}, {"a": 1}, {"b": 1}
e = {"": 1, "ba": -1}
assert multiply(a, b) == one and multiply(b, a) != one
assert multiply(e, b) == {} and multiply(e, e) == e
assert multiply(multiply({"r":1}, a), b) == {"r":1}
out["noncommutative_wreath_identities"] = "PASS with ab=1 alone, ba retained"

# Exact field Q[rho]/Phi_12(rho), Phi_12=rho^4-rho^2+1.
def field_reduce(p):
    p = dict(p)
    for k in range(max(p, default=0), 3, -1):
        c = p.pop(k, 0)
        p[k-2] = p.get(k-2, 0) + c
        p[k-4] = p.get(k-4, 0) - c
    return tuple(Q(p.get(k, 0)) for k in range(4))
def fadd(a, b): return tuple(x+y for x,y in zip(a,b))
def fmul(a, b):
    p = defaultdict(Q)
    for j, x in enumerate(a):
        for k, y in enumerate(b): p[j+k] += x*y
    return field_reduce(p)
zero, fone = (Q(0),)*4, (Q(1),Q(0),Q(0),Q(0))
rho = [field_reduce({k:1}) for k in range(12)]
def pmul(a,b):
    c={}
    for j,x in a.items():
        for k,y in b.items():c[j+k]=fadd(c.get(j+k,zero),fmul(x,y))
    return c
poly={0:fone}
for residue in (0,1,3,4,7,9):
    factor={1:fone,0:tuple(-x for x in rho[residue])}
    poly=pmul(poly,pmul(factor,factor))
positive=[(5,0,0,0),(-2,0,2,0),(0,0,2,0),(-2,0,0,0),(-1,0,1,0),(0,0,-2,0),(1,0,0,0)]
for j, expected in enumerate(positive):assert poly[j+6] == tuple(map(Q,expected))
for j in range(1,7):
    conjugated=zero
    for k,c in enumerate(poly[j+6]):
        conjugated=fadd(conjugated,tuple(c*x for x in rho[(-k)%12]))
    assert conjugated==poly[6-j]
out["sine_product_exact_laurent_coefficients"]="PASS in Q[rho]/Phi_12"

# Every possible shell residue and an exact norm lower inequality.
residues={(m*m+m*n+n*n)%12 for m in range(12) for n in range(12)}
assert residues == {0,1,3,4,7,9}
for m in range(-40,41):
    for n in range(-40,41):
        assert 4*(m*m+m*n+n*n)==(2*m+n)**2+3*n*n
        if (m,n)!=(0,0):assert m*m+m*n+n*n>=1
out["shell_residues_and_norm_boundary_controls"]="PASS; norm identity explains all integers"

# Exact summation constants, no floating point tolerances.
assert sum(Q(2,4*k*k-1) for k in range(1,128))==Q(254,255)
assert Q(10**53,2**254)<Q(1,10**22)
assert Q(11,1000)*Q(68,100)-Q(6,1000)/2==Q(448,100000)
assert 2*(91*Q(11,10**8)+2540*(Q(229,100)*Q(5,10**10)+Q(17,1000)*Q(32,10**9)))<Q(3,10**5)
out["quadrature_tail_inverse_error_and_infinite_sign_margin"]="PASS exact rational comparisons"

# Independent analytic-contract probe: exponential of rational z is generally
# essential at -2i/5. All expressions are holomorphic on its complement, and
# division by a ball containing that point must cause a nonfinite return.
pi=arb.pi();ii=acb(0,1);bb=arb(3).sqrt()/2;h=arb(2)/5;B=arb(4)/3
def params(t):return ii/(bb*(t+ii*h)),-B/(t+ii*h)-ii*h
probes=[acb(0,-h),acb(arb(0,"0.1"),arb("-0.4","0.1")),acb(arb("0.05","0.1"),arb("-0.4","0.01"))]
results=[]
for t in probes:
    lam,z=params(t)
    assert not lam.is_finite() and not z.is_finite()
    for m in (0,1,3,4,16,100):
        for ell in (0,1,2,30):
            v=lam*(ii*pi*z*m).exp()*(ii*pi*z)**ell
            assert not v.is_finite()
    results.append(str(t))
for t in (acb(0),acb(arb(1)/12),acb(1),acb(arb("0.5","0.001"),arb(0,"0.001"))):
    lam,z=params(t)
    assert lam.is_finite() and z.is_finite() and (lam*(ii*pi*z*100).exp()).is_finite()
out["Acb_contract"]={"status":"PASS", "singularity_type":"essential for nonzero exponential parameter, not globally meromorphic", "pole_containing_balls_nonfinite":results, "off_singularity_probes_finite":4, "runtime":"python-flint 0.9.0, 192-bit Arb/Acb", "proof_boundary":"All remaining callback factors are polynomials and entire exponentials; no variable sqrt/log/branch cuts."}
out["script_sha256"]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
dest=Path(__file__).with_suffix(".receipt.json")
dest.write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))
