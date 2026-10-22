"""Independent direct-pair-sum audit; no imports from research solver."""
import itertools, json, hashlib
from pathlib import Path

def sidon(a, modulus=None):
    sums=[(x+y) if modulus is None else (x+y)%modulus for x,y in itertools.combinations_with_replacement(a,2)]
    return len(sums)==len(set(sums))

def blocked(a,x):
    return any(x==u+v-w for u,v in itertools.combinations_with_replacement(a,2) for w in a if w!=u and w!=v) or any(2*x==u+v for u,v in itertools.combinations(a,2))

def maximal(a,n):
    return sidon(a) and all(not sidon(tuple(a)+(x,)) for x in range(n) if x not in a)

counts=[]
for n in range(1,16):
    total=maxima=0; least=n; examples=[]
    for mask in range(1<<n):
        a=tuple(x for x in range(n) if mask>>x&1)
        if not sidon(a): continue
        total+=1
        for x in range(n):
            if x not in a:
                assert blocked(a,x)==(not sidon(a+(x,))), (n,a,x)
        if maximal(a,n):
            maxima+=1; k=len(a); e=sum(x%2==0 for x in a); o=k-e
            assert 2*n<=k**3+k-2*e*o
            if k<least: least=k; examples=[a]
            elif k==least: examples.append(a)
    counts.append(dict(N=n,sidon_sets=total,maximal_sets=maxima,g=least,example=examples[0]))
a=(0,1)
assert sidon(a,5) and all(not sidon(a+(x,),5) for x in range(2,5))
assert sidon(a+(3,)) and not maximal(a,5)
assert maximal((0,3,4),7) and not maximal((0,),3)
result={'method':'Exhaust all subsets; independent ordinary pair-sum uniqueness oracle; interval {0,...,N-1}.','checks':'Blocker equivalence and parity-sensitive inequality on all ordinary Sidon subsets for N=1,...,15; modular and truncation counterexamples.','counts':counts}
out=Path(__file__).with_name('independent_audit_results.json')
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
print('script_sha256',hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
print('results_sha256',hashlib.sha256(out.read_bytes()).hexdigest())

# Audit externally generated finite certificate without using its blocker generator.
certificate=Path(__file__).with_name('certificate_N144.json')
if certificate.exists():
    c=json.loads(certificate.read_text()); a=tuple(c['A']); n=c['N']
    assert n==144 and len(a)==8 and len(set(a))==8 and all(1<=x<=n for x in a)
    assert sidon(a)
    sums=sorted(u+v for u,v in itertools.combinations_with_replacement(a,2))
    assert c['pair_sums']==sums and len(sums)==36
    assert set(map(int,c['witnesses']))==set(range(1,n+1))-set(a)
    for key,w in c['witnesses'].items():
        x=int(key)
        assert not sidon(a+(x,))
        assert w['a'] in a and w['b'] in a
        if w['kind']=='triple':
            assert w['c'] in a and w['c'] not in (w['a'],w['b'])
            assert x==w['a']+w['b']-w['c']
        else:
            assert w['kind']=='midpoint' and w['a']<w['b'] and 2*x==w['a']+w['b']
    result['N144_certificate']={'sha256':hashlib.sha256(certificate.read_bytes()).hexdigest(),'distinct_pair_sums':36,'verified_external_blockers':136,'scope':'Existence of saturated size-eight set only; no optimality.'}
    authored=Path(__file__).with_name('checks_results.json')
    if authored.exists():
        r=json.loads(authored.read_text())
        assert [v['g_N'] for v in r['exact_finite_values'][:15]]==[v['g'] for v in counts]
        result['crosscheck_author_results_sha256']=hashlib.sha256(authored.read_bytes()).hexdigest()
    out.write_text(json.dumps(result,indent=2)+'\n')
    print('final_script_sha256',hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    print('final_results_sha256',hashlib.sha256(out.read_bytes()).hexdigest())
    print('certificate',result['N144_certificate'])
