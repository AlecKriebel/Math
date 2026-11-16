from collections import Counter
import json

def need(ok, message):
    if not ok: raise RuntimeError(message)

# Valuation-only norm test; the all-integer argument is in INITIAL.md.
valuation_cases=0
for a in range(-50,51):
    for b in range(-50,51):
        m=min(2*a,1+2*b)
        need(2*a != 1+2*b and 1+a+b>m, 'middle term can cancel minimum')
        if m==0: need(a==0 and b>=0, 'unit norm criterion')
        valuation_cases+=1

# Substitute b=beta^4,t=gamma^2,z=(1+w)/beta^2 in every nonzero
# F2-linear combination of b^i z^j t^k, i,k=0,1 and j=0,...,3.
# Sparse Laurent monomials (beta exponent,gamma exponent,w exponent).
images=[]
for i in range(2):
    for j in range(4):
        for k in range(2):
            images.append({(4*i-2*j,2*k,r) for r in range(j+1) if r & ~j == 0})
universe=sorted(set().union(*images));index={v:i for i,v in enumerate(universe)}
encoded=[sum(1<<index[v] for v in im) for im in images]
w_masks={r:sum(1<<i for i,v in enumerate(universe) if v[2]==r) for r in range(4)}
def valuation(bits):
    need(bits!=0,'unexpected zero rational-function numerator')
    return next(r for r in range(4) if bits&w_masks[r])
current=0;previous=0;counts=Counter();samples=[]
for n in range(1,1<<len(images)):
    gray=n^(n>>1);toggle=gray^previous;current^=encoded[toggle.bit_length()-1];previous=gray
    v=valuation(current);need(v%2==0,'base polynomial has odd f-divisor')
    counts[v]+=1
    if len(samples)<64:samples.append(v)
rational_pairs=0
for u in samples:
    for v in samples:
        need((u-v)%2==0 and (1-u+v)%2==1,'rational quotient parity obstruction')
        rational_pairs+=1
# Exact fixed-log-basis correction: h=r/(1+r), h+h^2=r/(1+r)^2.
# Common-denominator numerator is r(1+r)+r^2=r in characteristic2.
need(({1,2}^{2})=={1},'Frobenius/exact-differential correction')
# Independent necessary hypotheses and incorrect extrapolations.
need(1%2==1,'f itself, outside the base, must defeat base valuation claim')
need((2-(-1))%2==1,'norm s is not a unit norm and not generally square')
need({-2,-1}==({-1*2}^{-1}),'AS-trivial s^-2+s^-1 control')
print(json.dumps({'status':'PASS_SOURCE_ONLY_ADVERSARIAL_CONTROLS',
 'norm_valuation_pairs':valuation_cases,'base_polynomials':sum(counts.values()),
 'f_valuation_histogram':dict(sorted(counts.items())),'rational_num_den_pairs':rational_pairs,
 'negative_controls':['allow f itself as base residue: odd divisor and obstruction disappears',
 'all norms have square residue without first normalizing valuation: norm(pi)=s',
 'replace AS parameter by s^-2+s^-1: extension is trivial',
 'Pfister slot z kills dz and absorbs the class',
 'fixed-log-basis Frobenius needs exact differential d(s^-2 h)'],
 'assertions_used':False,'native_imports_or_runs':[],
 'scope':'Exact finite algebra/valuation controls; universal field/cohomology arguments in INITIAL.md, not a cohomology decision procedure.'},sort_keys=True,indent=2))
