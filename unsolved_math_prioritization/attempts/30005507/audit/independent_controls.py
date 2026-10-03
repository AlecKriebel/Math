#!/usr/bin/env python3
"""Independent exact controls. Standard library; no network or source corpus needed.

Checks 2-groups with cyclic/dihedral/quaternion presentations, their marked
index-two extensions, complex character values, noncentral square correction,
central quotients, and a product-character numerical obstruction. Does not
claim to test arbitrary nilpotent blocks. Optional frozen replay reads files only.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import runpy

if not __debug__:
    raise RuntimeError("Run without -O: this verifier requires assertions.")

# Q(zeta_8), in the basis 1,z,z^2,z^3 with z^4=-1.
def c(x=0): return (F(x),F(0),F(0),F(0))
O=c(); U=c(1)
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def neg(a): return tuple(-x for x in a)
def sub(a,b): return add(a,neg(b))
def scale(a,n): return tuple(x*n for x in a)
def mul(a,b):
    out=[F(0)]*4
    for i,x in enumerate(a):
        if not x: continue
        for j,y in enumerate(b):
            if y: out[(i+j)%4]+=(-1 if i+j>=4 else 1)*x*y
    return tuple(out)
def root(k):
    k%=8; out=[F(0)]*4; out[k%4]=F(-1 if k>=4 else 1); return tuple(out)
def conj(a):
    out=O
    for i,x in enumerate(a): out=add(out,scale(root(-i),x))
    return out
def total(xs):
    out=O
    for x in xs: out=add(out,x)
    return out
def integer(a):
    assert a[1:]==(0,0,0) and a[0].denominator==1, a
    return int(a[0])
def zero(n): return tuple(tuple(O for _ in range(n)) for _ in range(n))
def ident(n): return tuple(tuple(U if i==j else O for j in range(n)) for i in range(n))
def ma(a,b): return tuple(tuple(add(x,y) for x,y in zip(ar,br)) for ar,br in zip(a,b))
def ms(a,k): return tuple(tuple(scale(x,k) for x in row) for row in a)
def mm(a,b):
    return tuple(tuple(total(mul(a[i][k],b[k][j]) for k in range(len(b))) for j in range(len(b[0]))) for i in range(len(a)))
def tr(a): return total(a[i][i] for i in range(len(a)))
def tensor(a,b):
    return tuple(tuple(mul(a[i][j],b[k][l]) for j in range(len(a)) for l in range(len(b))) for i in range(len(a)) for k in range(len(b)))
def mp(a,n):
    out=ident(len(a))
    for _ in range(n): out=mm(out,a)
    return out

# Adjoin omega with omega^2+omega+1=0 to Q(zeta_8).
def qa(a,b): return (add(a[0],b[0]),add(a[1],b[1]))
def qm(a,b):
    x,y=a; z,w=b
    return (sub(mul(x,z),mul(y,w)),sub(add(mul(x,w),mul(y,z)),mul(y,w)))
def qc(a): return (sub(conj(a[0]),conj(a[1])),neg(conj(a[1])))
def qs(a,k): return (mul(a[0],k),mul(a[1],k))
def qt(xs):
    ans=(O,O)
    for x in xs: ans=qa(ans,x)
    return ans
OMEGA=((U,O),(O,U),(neg(U),neg(U)))

def make_group(n,q=None):
    cyclic=q is None
    el=tuple(range(n)) if cyclic else tuple(product(range(n),range(2)))
    one=0 if cyclic else (0,0)
    def gm(x,y):
        if cyclic: return (x+y)%n
        a,b=x; d,e=y
        return ((a+(-1 if b else 1)*d+q*b*e)%n,(b+e)%2)
    def pw(x,k):
        out=one
        for _ in range(k): out=gm(out,x)
        return out
    inv={x:next(y for y in el if gm(x,y)==one) for x in el}
    assert all(gm(gm(x,y),z)==gm(x,gm(y,z)) for x,y,z in product(el,repeat=3))
    reps=[]
    if cyclic:
        reps=[{x:((root((8//n)*k*x),),) for x in el} for k in range(n)]
        autos=[{x:pw(r,x) for x in el} for r in el if len({pw(r,k) for k in range(n)})==n]
    else:
        for a,b in product((1,-1),repeat=2):
            reps.append({(i,j):((c(a**i*b**j),),) for i,j in el})
        for k in range(1,n//2):
            R=((root(8*k//n),O),(O,root(-8*k//n)))
            S=((O,c((-1)**k if q else 1)),(U,O))
            reps.append({(i,j):mm(mp(R,i),mp(S,j)) for i,j in el})
        autos=[]
        for r,s in product(el,repeat=2):
            if pw(r,n)!=one or pw(s,2)!=pw(r,q) or gm(gm(s,r),inv[s])!=inv[r]: continue
            a={x:gm(pw(r,x[0]),pw(s,x[1])) for x in el}
            if len(set(a.values()))==len(el): autos.append(a)
    assert len({tuple(a[x] for x in el) for a in autos})==len(autos)
    for a in autos: assert all(a[gm(x,y)]==gm(a[x],a[y]) for x,y in product(el,repeat=2))
    chars=[{x:tr(r[x]) for x in el} for r in reps]
    assert sum(len(r[one])**2 for r in reps)==len(el)
    assert all(total(mul(a[x],conj(b[x])) for x in el)==c(len(el) if i==j else 0)
               for i,a in enumerate(chars) for j,b in enumerate(chars))
    for r in reps:
        assert all(mm(r[x],r[y])==r[gm(x,y)] for x,y in product(el,repeat=2))
    return el,one,gm,pw,inv,reps,chars,autos

cases=[('C1',1,None),('C2',2,None),('C4',4,None),('C8',8,None),
       ('D8',4,0),('D16',8,0),('Q16',8,4)]
metrics=Counter(); summaries=[]; mutations={}; witnesses=[]
for name,n,q in cases:
    el,one,gm,pw,inv,reps,chars,autos=make_group(n,q)
    ordinary=[integer(scale(total(ch[gm(x,x)] for x in el),F(1,len(el)))) for ch in chars]
    assert set(ordinary)<={-1,0,1}
    # Principal 2-blocks of 2-groups have a single Brauer character and d_chi=degree.
    for u in el:
        if not all(gm(u,x)==gm(x,u) for x in el): continue
        lhs=total(scale(ch[u],e) for ch,e in zip(chars,ordinary))
        phim=sum(e*len(r[one]) for r,e in zip(reps,ordinary))
        barphim=sum(e*len(r[one]) for r,e in zip(reps,ordinary) if r[u]==ident(len(r[one])))
        assert lhs==c(2*barphim-phim)
        assert integer(lhs)==sum(gm(x,x)==u for x in el)
        metrics['central_quotient_character_identities']+=1
    count=0; vectors=Counter()
    for alpha in autos:
        for z in el:
            if alpha[z]!=z or any(alpha[alpha[x]]!=gm(gm(z,x),inv[z]) for x in el): continue
            count+=1
            ext=tuple(product(el,(0,1))); eid=(one,0)
            def em(x,y):
                a,b=x; d,e=y
                ans=gm(a,alpha[d] if b else d)
                return (gm(ans,z) if b and e else ans,(b+e)%2)
            assert all(em(em(x,y),w)==em(x,em(y,w)) for x,y,w in product(ext,repeat=3))
            metrics['extension_associativity_triples']+=len(ext)**3
            assert all(any(em(x,y)==eid==em(y,x) for y in ext) for x in ext)
            sq=Counter(em(x,x)[0] for x in ext if x[1])
            gow=[]
            for rep,ch in zip(reps,chars):
                dim=len(rep[one]); size=dim*dim
                g=integer(scale(total(scale(ch[x],v) for x,v in sq.items()),F(1,len(el))))
                gow.append(g); assert g in (-1,0,1)
                twisted=all(ch[alpha[x]]==conj(ch[x]) for x in el)
                assert (g!=0)==twisted
                S=tuple(tuple(U if (i,j)==(l,k) else O for k in range(dim) for l in range(dim)) for i in range(dim) for j in range(dim))
                P=zero(size)
                pi={x:tensor(rep[x],rep[alpha[x]]) for x in el}
                for x in el: P=ma(P,pi[x])
                P=ms(P,F(1,len(el)))
                R=mm(tensor(ident(dim),rep[z]),S)
                assert mm(P,P)==P
                assert integer(tr(P))==int(twisted)
                assert mm(R,P)==mm(P,R)
                assert mm(mm(R,R),P)==P
                assert integer(tr(mm(P,R)))==g
                assert all(mm(R,pi[x])==mm(pi[alpha[x]],R) for x in el)
                # Bidual action and j=rho(z) intertwining, with no assumed central z.
                tau=lambda x:inv[alpha[x]]
                assert tau(z)==inv[z]
                assert all(mm(rep[z],rep[x])==mm(rep[tau(tau(x))],rep[z]) for x in el)
                metrics['exact_tensor_and_biduality_controls']+=1
                metrics['complex_character_controls']+=int(any(v!=conj(v) for v in ch.values()))
                if name=='D8' and dim==2 and z==(1,0) and alpha[(0,1)]==(1,1):
                    wrong=mm(tensor(ident(dim),rep[inv[z]]),S)
                    assert integer(tr(mm(P,wrong)))==-g and g==1
                    assert mm(P,S)!=mm(S,P)
                    assert any(rep[x]!=rep[tau(tau(x))] for x in el)
                    mutations['uncorrected_flip_rejected']=True
                    mutations['inverse_square_correction_rejected']=True
                    mutations['identity_biduality_map_rejected']=True
                    witnesses.append({'case':'D8','alpha_r':'r','alpha_s':'rs','z':'r',
                                      'correct_indicator':g,'inverse_correction_indicator':-g,
                                      'plain_flip_preserves_invariants':False})
            vectors[tuple(gow)]+=1
            assert sum(g*len(r[one]) for g,r in zip(gow,reps))==sq[one]
            for x in el:
                assert total(scale(ch[x],g) for ch,g in zip(chars,gow))==c(sq[x])
                metrics['pointwise_fourier_controls']+=1
            # Independent direct induced-character square sums in C3 semidirect E.
            ainv={v:k for k,v in alpha.items()}
            model=tuple(product(range(3),ext))
            def mprod(x,y):
                a,e=x; b,f=y
                return ((a+(-1 if e[1] else 1)*b)%3,em(e,f))
            def induced(ch,x):
                a,(d,b)=x
                if b: return (O,O)
                return qa(qs(OMEGA[a],ch[d]),qs(OMEGA[-a%3],ch[ainv[d]]))
            vals=[[induced(ch,x) for x in model] for ch in chars]
            for k,ch in enumerate(chars):
                assert qt(induced(ch,mprod(x,x)) for x in model)==(c(len(model)*gow[k]),O)
                metrics['independent_model_indicator_sums']+=1
                for l in range(len(chars)):
                    assert qt(qm(a,qc(b)) for a,b in zip(vals[k],vals[l]))==(c(len(model) if k==l else 0),O)
                    metrics['independent_model_inner_products']+=1
            # Direct root counting in every central cyclic quotient.
            for u in el:
                if alpha[u]!=u or not all(gm(u,x)==gm(x,u) for x in el): continue
                cyc={one}; v=u
                while v!=one: cyc.add(v); v=gm(v,u)
                outside=[x for x in ext if x[1]]
                cosets={frozenset(em(x,(v,0)) for v in cyc) for x in outside}
                invol_cosets=sum(em(next(iter(cc)),next(iter(cc)))[0] in cyc for cc in cosets)
                lhs=sq[u]; rhs=2*invol_cosets-sq[one]
                assert lhs==rhs
                metrics['central_quotient_root_identities']+=1
                if name=='C4' and alpha=={x:x for x in el} and z==1 and u==1:
                    assert lhs==2 and invol_cosets==1 and sq[one]==0
                    assert invol_cosets-sq[one]!=lhs
                    mutations['missing_factor_two_rejected']=True
                    witnesses.append({'case':'C4 inside C8','u':'generator of C4','roots_of_u':lhs,
                                      'outside_involutions':sq[one],'quotient_outside_involutions':invol_cosets})
            metrics['extensions']+=1
    summaries.append({'group':name,'order':len(el),'automorphisms':len(autos),
                      'compatible_marked_extensions':count,'irreducible_characters':len(reps),
                      'indicator_patterns':[{'vector':list(v),'count':k} for v,k in sorted(vectors.items())]})

# Independent numerical obstruction: explicit product character table, not only degrees.
el,one,gm,pw,inv,reps,chars,autos=make_group(4,2)
fs=[integer(scale(total(ch[gm(x,x)] for x in el),F(1,len(el)))) for ch in chars]
pairs=list(product(range(len(chars)),repeat=2))
deg=[len(reps[a][one])*len(reps[b][one]) for a,b in pairs]
signs=[fs[a]*fs[b] for a,b in pairs]
assert Counter(zip(deg,signs))==Counter({(1,1):16,(2,-1):8,(4,1):1})
solutions=[(a,b) for a in range(9) for b in range(2) if a+2*b==8]
assert solutions==[(6,1),(8,0)]
alt=signs.copy(); alt[pairs.index((0,4))]=1; alt[pairs.index((1,4))]=1; alt[pairs.index((4,4))]=-1
assert sum(d*s for d,s in zip(deg,signs))==sum(d*s for d,s in zip(deg,alt))==4
assert Counter(zip(deg,alt))==Counter({(1,1):16,(2,1):2,(2,-1):6,(4,-1):1})
assert all(s==1 for d,s in zip(deg,alt) if d==1)
changed=0
for x,y in product(el,repeat=2):
    qvalue=sum(gm(t,t)==x for t in el)*sum(gm(t,t)==y for t in el)
    actual=total(scale(mul(chars[a][x],chars[b][y]),s) for (a,b),s in zip(pairs,signs))
    fake=total(scale(mul(chars[a][x],chars[b][y]),s) for (a,b),s in zip(pairs,alt))
    assert actual==c(qvalue)
    changed+=fake!=actual
assert changed>0
metrics['Q8_product_pointwise_controls']=len(el)**2
mutations['alternate_assignment_fails_full_fourier_data']=True
assert len(mutations)==5

out={'status':'PASS_SCOPED_PARTIAL','scope':'Finite exact controls of local algebra and existing model mechanisms; no arbitrary-block theorem.',
     'arithmetic':'Exact fractions in Q(zeta_8), and adjoining a primitive cube root for the model characters; standard-library implementation.',
     'counts':dict(metrics),'families':summaries,'mutation_controls':mutations,'witnesses':witnesses,
     'numerical_obstruction':{'two_integer_negative_count_solutions':solutions,'common_scalar':4,
                             'differing_full_fourier_entries_for_fixed_assignment':changed},
     'frozen_replay':{'status':'not requested'}}
# Optional integration replay. run_name differs from __main__, so frozen output is not rewritten.
here=Path(__file__).resolve().parent
release=here.parent/'release'; manifest=here.parent/'FROZEN_AUTHOR_MANIFEST.local.json'
if release.is_dir() and manifest.exists():
    m=json.loads(manifest.read_text())['release_files']
    def hashes(): return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in release.iterdir() if p.is_file()}
    before=hashes(); assert before=={k:v['sha256'] for k,v in m.items()}
    assert all((release/k).stat().st_size==v['bytes'] for k,v in m.items())
    replay=runpy.run_path(str(release/'check_indicators.py'))['result']
    assert replay==json.loads((release/'exact_results.json').read_text())
    assert hashes()==before
    out['frozen_replay']={'status':'passed without writes','manifest_file_count':len(m),
                          'original_extension_presentations':replay['compatible_presentations'],
                          'original_model_indicators':replay['model_character_indicator_checks'],
                          'original_model_inner_products':replay['model_character_inner_product_checks']}
(here/'independent_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='families'},indent=2))
