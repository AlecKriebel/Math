"""Independent exact braid/count controls, not a transverse realization test."""
from pathlib import Path
from itertools import product
import hashlib,json

root=Path(__file__).resolve().parent
EXPECTED='b40a0e54e88291f7e9fbd07d0798f2eb6da3a6c927115afee8fe2ea5e5c0ef3c'
assert hashlib.sha256((root/'author_replay/OBSTRUCTION.md').read_bytes()).hexdigest()==EXPECTED
counts={}
def ck(v,k):
    assert v,k
    counts[k]=counts.get(k,0)+1

def reduce(w):
    out=[]
    for a in w:
        if out and out[-1]==-a:out.pop()
        else:out.append(a)
    return tuple(out)
def inverse(w):return tuple(-a for a in reversed(w))
def sub(w,images):
    out=[]
    for a in w:out.extend(images[abs(a)-1] if a>0 else inverse(images[-a-1]))
    return reduce(out)
def compose(A,B):return tuple(sub(w,A) for w in B)
def artin(n,k):
    i=abs(k);out=[(j,) for j in range(1,n+1)]
    if k>0:out[i-1]=(i,i+1,-i);out[i]=(i,)
    else:out[i-1]=(i+1,);out[i]=(-(i+1),i,i+1)
    return tuple(out)
def action(n,w):
    out=tuple((i,) for i in range(1,n+1))
    for k in w:out=compose(out,artin(n,k))
    return out
def cycles(n,w):
    p=list(range(n))
    for k in w:
        i=abs(k)-1;p[i],p[i+1]=p[i+1],p[i]
    seen=set();number=0
    for i in range(n):
        if i not in seen:
            number+=1;j=i
            while j not in seen:seen.add(j);j=p[j]
    return number
def exp(w):return sum(1 if a>0 else -1 for a in w)

# Check the complete free-group substitutions, not just permutations.
for n in range(2,8):
    identity=tuple((i,) for i in range(1,n+1))
    for i in range(1,n):
        for j in range(i+1,n+1):
            conjugator=tuple(range(j-1,i,-1))
            band=conjugator+(i,)+inverse(conjugator)
            auto=action(n,band);back=action(n,inverse(band))
            ck(compose(auto,back)==identity,'full_artin_inverse_identity')
            ck(exp(band)==1 and exp(inverse(band))==-1,'band_exponent')
            ck(cycles(n,band)==n-1,'band_transposition_component_control')

# All short Artin words here are also adjacent-band words.
for length in range(5):
    for w in product([-2,-1,1,2],repeat=length):
        n=3;bp=sum(k>0 for k in w);bn=len(w)-bp
        chi=n-len(w);sl=exp(w)-n
        ck(-chi-sl==2*bn,'word_defect')
        for sign in [-1,1]:
            w2=w+(sign*n,)
            chi2=(n+1)-len(w2);sl2=exp(w2)-(n+1)
            ck(chi2==chi,'stabilization_surface_euler')
            ck(sl2-sl==(0 if sign>0 else -2),'stabilization_self_linking')
            ck(cycles(n+1,w2)==cycles(n,w),'stabilization_components')

for ep,em,hp,hm in product(range(5),repeat=4):
    chi=ep+em-hp-hm;sl=-ep+em+hp-hm
    ck(chi+sl==2*(em-hm),'all_signed_count_identity')
    ck((sl==-chi)==(em==hm),'sharp_signed_count_criterion')

# A repeated cancelling pair changes this displayed surface, not the braid.
for N in range(17):
    w=(1,1,1)+(1,-1)*N
    ck(reduce(w)==(1,1,1),'trefoil_exact_word_reduction')
    ck(2-len(w)==-1-2*N and exp(w)-2==1,'trefoil_surface_control')
for genus in range(9):
    allowed=[(tau,g4) for tau in range(-genus,genus+1) for g4 in range(genus+1)
             if 2*genus-1<=2*tau-1<=2*g4-1<=2*genus-1]
    ck(allowed==[(genus,genus)],'canonical_route_squeeze')

r={'all_pass':True,'assertions':sum(counts.values()),'counts':counts,
   'artifact_sha256':EXPECTED,
   'scope':'Exact free-group braid substitutions, Euler/self-linking accounting, components, signed counts and scalar inequality controls. No surface-realization or transverse-isotopy certificate.'}
(root/'independent_results.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))
