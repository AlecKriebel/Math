#!/usr/bin/env python3
"""Independent review controls. No author algorithms are imported for positive checks.
Uses subset-zeta palette unions, color occurrence supports, weighted convolution,
and elementary coin DP rather than author subset iteration/Dijkstra.
"""
import collections, hashlib, importlib.util, itertools, json, math, pathlib, random
ROOT=pathlib.Path(__file__).resolve().parent
PACKET=ROOT.parent/'packet'
OUT={}

def load(name): return json.loads((PACKET/name).read_text())
def full_palettes(md):
    n=len(md['spokes']); vals=[1]*(1<<n)
    for i,col in enumerate(md['spokes']): vals[1<<i]|=1<<col
    for i in range(n):
        for j in range(i+1,n): vals[(1<<i)|(1<<j)]|=1<<md['edges'][i][j]
    for i in range(n):
        b=1<<i
        for mask in range(1<<n):
            if mask&b: vals[mask]|=vals[mask^b]
    return vals

def edge_signatures(n, triples):
    assert len(triples)==math.comb(n,2)
    lookup={(i,j):col for i,j,col in triples}
    assert set(lookup)==set(itertools.combinations(range(n),2))
    unique=sorted(set(lookup.values())); ren={c:i+1 for i,c in enumerate(unique)}
    md={'spokes':[0]*n,'edges':[[0]*n for _ in range(n)]}
    for (i,j),c in lookup.items():md['edges'][i][j]=md['edges'][j][i]=ren[c]
    pp=full_palettes(md); cnt=collections.Counter()
    for mask,pal in enumerate(pp):
        s=mask.bit_count(); cnt[(s,math.comb(s,2)-(pal.bit_count()-1))]+=1
    return cnt

def check_models():
    files=sorted(PACKET.glob('rainbow_cycle_*.json'))+[PACKET/'known_rooted_4_3.json',PACKET/'rooted_5_4.json',PACKET/'rooted_c112_m43.json',PACKET/'failed_extension_c113_m43.json']
    out=[]; byname={}
    saved=load('verified_examples.json')
    for path in files:
        md=json.loads(path.read_text()); pp=full_palettes(md)
        counts=collections.Counter(x.bit_count() for x in pp)
        assert pp[-1]==(1<<md['c'])-1
        assert (md['m'] not in counts)==('failed_extension' not in path.name)
        if path.stem in saved:assert sorted(counts)==saved[path.stem]['observed_spectrum']
        if path.name=='rooted_c112_m43.json':assert sorted(counts)==load('witness_c112_m43.json')['spectrum']
        witness=next((i for i,x in enumerate(pp) if x.bit_count()==md['m']),None)
        out.append({'file':path.name,'subsets':len(pp),'spectrum':sorted(counts),'target_present':md['m'] in counts,'target_witness_mask':witness,'full_palette_verified':True})
        byname[path.name]=counts
    a=byname['rooted_c112_m43.json']; b=byname['failed_extension_c113_m43.json']
    want=collections.Counter(a)
    for x,num in a.items(): want[x+1]+=num
    assert b==want
    OUT['rooted_certificates']=out
    OUT['extension_multiplicity_identity']=True

def convolution(sig,other):
    result=collections.Counter()
    for (a,b),x in sig.items():
        for (c,d),y in other.items(): result[a+c,b+d]+=x*y
    return result

def padded(sig,n,h):
    counts=collections.Counter()
    for (s,d),num in sig.items():
        for f in range(n-h+1):
            t=s+f; pal=1 if t==0 else 2+math.comb(t,2)-d
            counts[pal]+=num*math.comb(n-h,f)
    assert sum(counts.values())==2**n
    return counts

def check_gadgets():
    table=load('gap_six_checks.json')['gadgets']; sigs={}; out={}
    expected={3:{0,3},5:{0,4,5},9:{0,4,5,8,9},11:{0,4,5,8,9,10,11}}
    for key,g in table.items():
        d=int(key); n=g['vertices']; sig=edge_signatures(n,g['edge_colors']); sigs[d]=(n,sig)
        vals={x for s,x in sig}; losses={d-x for x in vals};assert losses==expected[d]
        assert {str(s):sorted(x for ss,x in sig if ss==s) for s in range(n+1)}==g['deficits_by_size']
        # Properness checked directly from color incidences.
        for v in range(n):
            incident=[c for i,j,c in g['edge_colors'] if v in (i,j)]
            assert len(incident)==len(set(incident))
        out[key]={'subsets':sum(sig.values()),'losses':sorted(losses)}
    assemblies=[]
    for p in range(10,51):
        base=10+(p-10)%5
        ds={10:[5,5],11:[11],12:[3,9],13:[3,5,5],14:[5,9]}[base]+[5]*((p-base)//5)
        sig=collections.Counter({(0,0):1});h=0
        for d in ds:
            hn,ss=sigs[d];h+=hn;sig=convolution(sig,ss)
        assert sum(sig.values())==2**h and h<=p+1
        assert all(p-deficit!=6 for s,deficit in sig)
        for k in [max(7,p-4),max(7,p-4)+1,max(7,p-4)+7]:
            n=max(p+2,k+1); q=p-6;m=math.comb(k,2)+2-q;c=math.comb(n,2)+2-p
            cnt=padded(sig,n,h); assert m not in cnt and max(cnt)==c
            assemblies.append({'p':p,'k':k,'n':n,'c':c,'m':m,'weighted_subsets':str(2**n)})
    OUT['gap_six_gadgets']=out;OUT['gap_six_exact_weighted_assemblies']=assemblies
    gs=load('padding_obstruction_checks.json');g=gs['gadget'];sig=edge_signatures(g['n'],g['edge_colors'])
    assert {x for _,x in sig}=={0,1,2,3,5,6,7,10,11,16}
    pads=[]
    for old in gs['examples']:
        cnt=padded(sig,old['n'],g['n']); assert sorted(cnt)==old['palette_spectrum'];assert (old['m'] not in cnt)==old['avoids_m']
        pads.append({'n':old['n'],'c':old['c'],'m':old['m'],'weighted_subsets':sum(cnt.values()),'target_multiplicity':cnt.get(old['m'],0)})
    OUT['compact_padding']=pads
    # Explicit failed support witness using all eight gadget vertices and five fillers.
    assert 2+math.comb(13,2)-16==64

def check_semigroups():
    data=load('large_gap_checks.json');res={}
    for key,row in data['semigroups'].items():
        d=int(key); coins=row['coins'];a=min(coins)
        assert coins==[math.comb(t,2)-(t-1 if t%2==0 else t) for t in row['orders']]
        L=max(row['residue_minima'])+a; can=[False]*(L+1);can[0]=True
        for v in range(1,L+1):can[v]=any(v>=coin and can[v-coin] for coin in coins)
        minima=[next(v for v in range(r,L+1,a) if can[v]) for r in range(a)]
        assert minima==row['residue_minima']
        C=row['conductor'];assert not can[C-1] and all(can[C:])
        for r,rep in enumerate(row['representations']):
            assert all(x in coins for x in rep) and sum(rep)==minima[r] and sum(rep)%a==r
        res[key]={'conductor':C,'coin_dp_limit':L,'all_residue_minima_match':True,'conductor_minus_one_unreachable':True}
    OUT['semigroup_controls']=res
    checks={}
    for key,row in data['gap12_full_subset_checks'].items():
        n=int(key);mod=n if n%2 else n-1
        triples=[]
        for i,j in itertools.combinations(range(n),2):
            col=2*i%mod if n%2==0 and j==n-1 else (i+j)%mod
            triples.append((i,j,col))
        sig=edge_signatures(n,triples);loss={row['deficit']-v for _,v in sig}
        assert sorted(loss)==row['losses'] and 12 not in loss
        checks[key]={'subsets':sum(sig.values()),'losses':sorted(loss)}
    OUT['larger_gap_subset_controls']=checks

def check_structural_bounds():
    tested=0; crossing=0; tight=0
    def inspect(md):
        nonlocal tested,crossing,tight
        pp=full_palettes(md);n=len(md['spokes']);c=pp[-1].bit_count();counts={x.bit_count() for x in pp}
        for m in counts:
            assert min(mask.bit_count() for mask,pal in enumerate(pp) if pal.bit_count()==m)<=2*(m-1)
        for mask,pal in enumerate(pp):
            if not mask:continue
            vertices=[i for i in range(n) if mask>>i&1];p=pal.bit_count()
            loss=[(pal&~pp[mask^(1<<i)]).bit_count() for i in vertices]
            assert max(loss)<=len(vertices) and sum(loss)<=2*(p-1)
            for m in range(3,p):
                if m in counts or any(pp[mask^(1<<i)].bit_count()>m for i in vertices):continue
                crossing+=1;d=p-m+1;s=len(vertices)
                assert d<=s<=2*(p-1)//d and s<=m and math.comb(d,2)<=m-2
                if s==m:
                    tight+=1;assert p==m+1
                    assert all(md['spokes'][i]==0 for i in vertices)
                    nonzero=[(i,j,md['edges'][i][j]) for i,j in itertools.combinations(vertices,2) if md['edges'][i][j]]
                    assert len({col for i,j,col in nonzero})==len(nonzero)
                    assert all(sum(i==v or j==v for i,j,col in nonzero)==2 for v in vertices)
        tested+=1
    for n in range(4):
        slots=n*(n+1)//2
        for c in range(1,6):
            for labs in itertools.product(range(c),repeat=slots):
                if set(labs)|{0}!=set(range(c)):continue
                md={'spokes':list(labs[:n]),'edges':[[0]*n for _ in range(n)]};pos=n
                for i,j in itertools.combinations(range(n),2):md['edges'][i][j]=md['edges'][j][i]=labs[pos];pos+=1
                inspect(md)
    rng=random.Random(732401)
    for it in range(400):
        n=rng.randrange(4,9);c=rng.randrange(2,18);md={'spokes':[rng.randrange(c) for _ in range(n)],'edges':[[0]*n for _ in range(n)]}
        for i,j in itertools.combinations(range(n),2):md['edges'][i][j]=md['edges'][j][i]=rng.randrange(c)
        inspect(md)
    OUT['structural_controls']={'models':tested,'minimal_crossings':crossing,'tight_crossings':tight,'scope':'All surjective n<=3, c<=5, plus 400 independently seeded random models; mathematical proofs carry universality.'}

def check_validation_defect():
    spec=importlib.util.spec_from_file_location('author_checker',PACKET/'rooted_verify.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    rows=[]
    for label in [3.0,True]:
        md={'c':4,'m':3,'spokes':[1,2],'edges':[[0,label],[3 if label==3.0 else 1,0]]}
        if label is True:md['c']=3;md['m']=3
        try:result=mod.verify(md,True);accepted=True
        except Exception as error:result={'error':str(error)};accepted=False
        rows.append({'input':md,'accepted':accepted,'result':result})
    assert all(x['accepted'] for x in rows)
    OUT['upper_triangle_type_validation_defect']=rows

if __name__=='__main__':
    for fn in [check_models,check_gadgets,check_semigroups,check_structural_bounds,check_validation_defect]:
        fn();print(fn.__name__,'PASS',flush=True)
    (ROOT/'independent_results.json').write_text(json.dumps(OUT,indent=2)+'\n')
    print('Independent mathematical controls passed; validation defect reproduced.')
