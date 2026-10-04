"""Independent necessary-invariant diagnostics; no manuscript/checker imports."""
from pathlib import Path
from itertools import product,permutations
import subprocess,sys,json,datetime,hashlib,random
a=Path(__file__).resolve().parent
dest=a/'private/extracted'

def invariant(n,word):
    # Follow each upper endpoint through every crossing, then identify it with
    # the upper endpoint at its lower slot. This computes closure components
    # by an independent union-find mechanism rather than cycle traversal.
    slots=list(range(n)); events=[]
    for typ,idx,sign in word:
        l,r=slots[idx-1],slots[idx]
        if typ=='s': events.append((l,r,sign) if sign==1 else (r,l,sign))
        slots[idx-1],slots[idx]=r,l
    parent=list(range(n))
    def find(x):
        while parent[x]!=x:x=parent[x]
        return x
    for lower,upper in enumerate(slots):
        x,y=find(lower),find(upper)
        if x!=y:parent[max(x,y)]=min(x,y)
    roots=sorted(set(map(find,range(n))));ids={r:i for i,r in enumerate(roots)}
    m=[[0]*len(roots) for _ in roots]
    for over,under,e in events:
        i,j=ids[find(over)],ids[find(under)]
        if i!=j:m[i][j]+=e
    return tuple(map(tuple,m))

def equivalent_matrix(x,y):
    return len(x)==len(y) and any(all(x[i][j]==y[p[i]][p[j]] for i in range(len(x)) for j in range(len(x))) for p in permutations(range(len(x))))

def fox(n,word):
    total=0
    for xs in product(range(3),repeat=n):
        ys=list(xs)
        for typ,idx,e in word:
            assert typ=='s'
            u,v=ys[idx-1],ys[idx]
            ys[idx-1:idx+1]=[(2*u-v)%3,u] if e==1 else [v,(2*v-u)%3]
        total+=ys==list(xs)
    return total

left=[(('s',2,1),('s',1,-1),('s',2,1),('s',1,1)),(('s',2,1),('v',1,1),('s',2,1),('v',1,1))]
buffered=[w+(('s',3,1),) for w in left]
wrong=[(('s',1,1),('s',1,-1),('s',1,1),('s',1,1)),(('s',1,1),('v',1,1),('s',1,1),('v',1,1))]
wrong_buffered=[w+(('s',3,1),) for w in wrong]
assert [invariant(4,w) for w in left]==[((0,0),(0,0))]*2
assert [invariant(4,w) for w in buffered]==[((0,),)]*2
assert not equivalent_matrix(*[invariant(4,w) for w in wrong])
assert not equivalent_matrix(*[invariant(4,w) for w in wrong_buffered])
assert fox(2,(('s',1,1),)*3)==9
assert fox(2,(('s',1,1),))==fox(2,(('s',1,-1),))==3
assert invariant(2,(('s',1,1),)*2)==((0,1),(1,0))
assert invariant(2,(('s',1,1),('v',1,1),('s',1,1),('v',1,1)))==((0,2),(0,0))

tex=(dest/'even_strand_markov.tex').read_text()
contracts=[r'(N,s(a)\sig_1^{-1}s(b)\sig_1)',r'(N,s(a)v_1s(b)v_1)',r'(N,s(a)\sig_1^{-1}s(b)\sig_1\sig_{N-1})',r'(N,s(a)v_1s(b)v_1\sig_{N-1})',r'a,b\in\WB{N}{N-2}',r'a,b\in\WB{N}{N-3}']
assert all(c in tex for c in contracts)
assert not all(c in tex.replace('s(a)','a').replace('s(b)','b') for c in contracts)

original=(dest/'verify_even_calculus.py').read_text()
needle='def shift(w): return tuple((t, i + 1, e) for t, i, e in w)'
assert original.count(needle)==1
mutant=original.replace(needle,'def shift(w): return tuple((t, i, e) for t, i, e in w)')
path=a/'private/zero_shift_mutant.py';path.write_text(mutant)
b=a/'private/commands/zero_shift_mutant'
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with b.with_suffix('.stdout').open('wb') as out,b.with_suffix('.stderr').open('wb') as err:
    child=subprocess.Popen([sys.executable,'-B',str(path)],stdin=subprocess.DEVNULL,stdout=out,stderr=err,cwd=a);rc=child.wait()
rec={'argv':[sys.executable,'-B',str(path)],'pid':child.pid,'cwd':str(a),'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':rc,'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'stdin':'empty; DEVNULL'}
b.with_suffix('.json').write_text(json.dumps(rec,indent=2)+'\n');b.with_suffix('.stdin').write_bytes(b'');b.with_suffix('.source.py').write_bytes(path.read_bytes())
assert rc==1
assert 'primary literal unrestricted left index shift' in b.with_suffix('.stderr').read_text()

print(json.dumps({'status':'PASS_INDEPENDENT_CONTROLS','source_contracts':len(contracts),'correct_L_matrices':[invariant(4,w) for w in left],'correct_BL_matrices':[invariant(4,w) for w in buffered],'zero_shift_L_matrices':[invariant(4,w) for w in wrong],'zero_shift_BL_matrices':[invariant(4,w) for w in wrong_buffered],'fox_counts':[9,3,3],'mutant':rec,'limits':'Necessary invariants and literal source contracts; no link-equivalence oracle or theorem proof'},indent=2))
