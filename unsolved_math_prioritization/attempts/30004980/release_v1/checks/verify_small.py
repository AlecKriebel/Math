"""Independent red/black-state checker for pair-first certificates.
Does not call twinwidth.red, width, or merge when verifying a sequence.
"""
import hashlib,json,itertools,random
from pathlib import Path
import twinwidth as search

def verify(adj,sequence,bound):
    parts=[1<<i for i in range(len(adj))]
    state={tuple(sorted((1<<i,1<<j))):int(bool(adj[i]>>j&1)) for i,j in itertools.combinations(range(len(adj)),2)}
    peak=0
    sequence=list(sequence)
    while len(parts)>1:
        if sequence:x,y=sequence.pop(0)
        else:x,y=parts[:2]
        assert x in parts and y in parts and x!=y
        rest=[v for v in parts if v not in (x,y)];z=x|y
        updates={}
        for v in rest:
            a=state[tuple(sorted((x,v)))];b=state[tuple(sorted((y,v)))]
            updates[tuple(sorted((z,v)))]=2 if a==2 or b==2 or a!=b else a
        state={uv:a for uv,a in state.items() if x not in uv and y not in uv};state.update(updates);parts=sorted(rest+[z])
        degree={v:0 for v in parts}
        for (a,b),c in state.items():
            if c==2:degree[a]+=1;degree[b]+=1
        peak=max(peak,max(degree.values(),default=0))
        assert peak<=bound,(adj,sequence,parts,degree,bound)
    assert not sequence
    return peak

def main():
    out={};digest=hashlib.sha256()
    for n in range(1,7):
        peak=0;count=0
        for code in range(1<<(n*(n-1)//2)):
            a=search.graph(n,code);s=search.pair_only(a,0 if n<=3 else (n-1)//2)
            assert s is not None
            v=verify(a,s,0 if n<=3 else (n-1)//2);peak=max(peak,v);count+=1
            digest.update(json.dumps([n,code,s],separators=(',',':')).encode()+b'\n')
        out[n]={'labeled_graphs':count,'upper_bound_verified':peak}
    rng=random.Random(481)
    for n in range(7,13):
        peak=0
        for z in range(250):
            code=rng.getrandbits(n*(n-1)//2);a=search.graph(n,code);s=search.pair_only(a,0 if n<=3 else (n-1)//2)
            assert s is not None;peak=max(peak,verify(a,s,(n-1)//2))
        out['random_'+str(n)]={'samples':250,'largest_certificate_width':peak,'seed':481}
    out['exhaustive_certificate_sha256']=digest.hexdigest()
    out['method']='Search uses original-graph partitions; verifier independently updates black/nonedge/red trigraph states.'
    out['lower_bound_witnesses']={'n=4':'P4, min disagreement 1','n=5':'C5, min disagreement 2','n=6':'C5 plus an isolated vertex, min disagreement 2'}
    Path(__file__).with_name('verification_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
