"""Independent audit: byte-vector/permutation states, terminal inverse propagation.
No candidate code imported. Every record and every coaccessible edge is compared.
"""
from pathlib import Path
from itertools import combinations
import datetime,gzip,hashlib,json
D=Path(__file__).resolve().parent
C=D/'isolation/verification/certificates'
def inv(w): return tuple(-x for x in w[::-1])
def free(w):
    out=[]
    for x in w:
        if out and out[-1]+x==0: out.pop()
        else: out.append(x)
    return tuple(out)
def apply(images,table):
    return tuple(free(x for letter in word for x in (table[letter-1] if letter>0 else inv(table[-letter-1]))) for word in images)
def word_action(w,tables,rank):
    result=tuple((i,) for i in range(1,rank+1))
    for i in w: result=apply(result,tables[i-1])
    return result
A=(((1,),(1,2),(1,3),(1,4)),((1,-2,1),(1,),(3,),(4,)),
   ((1,),(2,-3,2),(2,),(4,)),((1,),(2,),(3,-4,3),(3,)),
   ((1,),(2,),(3,),(3,-2,1,4)))
AI=(((1,),(-1,2),(-1,3),(-1,4)),((2,),(2,-1,2),(3,),(4,)),
    ((1,),(3,),(3,-2,3),(4,)),((1,),(2,),(4,),(4,-3,4)),
    ((1,),(2,),(3,),(-1,2,-3,4)))
identity4=tuple((i,) for i in range(1,5))
assert all(apply(A[i],AI[i])==identity4==apply(AI[i],A[i]) for i in range(5))
for i,j in combinations(range(1,6),2):
    lhs,rhs=((i,j,i),(j,i,j)) if j-i==1 else ((i,j),(j,i))
    assert word_action(lhs,A,4)==word_action(rhs,A,4)
c=(1,2,3,4)*5;h=(5,4,3,2,1,1,2,3,4,5)
assert word_action(c,A,4)==word_action(h,A,4)
target4=word_action(c+c,A,4)
mutant=list(A);mutant[4]=((1,),(2,),(3,),(3,-2,4))
assert word_action(c,mutant,4)!=word_action(h,mutant,4)
# Direct labelled-strand recursion, tracking actual pair partners instead of edge caps.
expected20={}
counts20=[];kept20=[]
for center in range(6):
    rows=[]
    def search(order,partners,w,action):
        if len(w)==20:
            if order!=tuple(range(6)): return
            assert all(partners[i]==4 for i in range(6) if i!=center)
            rows.append((w,action));return
        position=order.index(center)
        for neighbour in (position+1,position-1):
            if not 0<=neighbour<6: continue
            label=order[neighbour]
            if partners[label]>=4: continue
            nextpartners=list(partners);nextpartners[label]+=1
            nextorder=list(order);nextorder[position],nextorder[neighbour]=nextorder[neighbour],nextorder[position]
            gen=min(position,neighbour)+1
            search(tuple(nextorder),tuple(nextpartners),w+(gen,),apply(action,A[gen-1]))
    search(tuple(range(6)),(0,)*6,(),identity4)
    counts20.append(len(rows));kept20.append(sum(im==target4 for _,im in rows))
    for w,im in rows:
        assert (center+1,w) not in expected20
        expected20[(center+1,w)]=(im,im==target4)
seen20=set()
with gzip.open(C/'20_full_actions.jsonl.gz','rt') as inp:
    for line in inp:
        r=json.loads(line);key=(r['center'],tuple(r['word']))
        assert key not in seen20;seen20.add(key)
        assert expected20[key]==(tuple(map(tuple,r['images'])),r['survives'])
assert seen20==expected20.keys() and len(seen20)==810
survivors={w for (_,w),(im,keep) in expected20.items() if keep}
assert survivors=={(h+h)[i:]+(h+h)[:i] for i in range(20)}
assert counts20==[81,162,162,162,162,81] and kept20==[1,2,2,2,2,1]
rank_results=[]
for n in range(1,7):
    pairs=list(combinations(range(n),2));m=len(pairs)
    pair_index={pair:j for j,pair in enumerate(pairs)}
    root=bytes(m)+bytes(range(n));terminal=bytes([2])*m+bytes(range(n))
    # Count bytes plus order bytes form the key: no merging by count code.
    def edges(state,sign):
        for g in range(n-2,-1,-1):
            a,b=state[m+g],state[m+g+1]
            j=pair_index[(min(a,b),max(a,b))]
            if (sign==1 and state[j]==2) or (sign==-1 and state[j]==0): continue
            out=bytearray(state);out[j]+=sign;out[m+g],out[m+g+1]=b,a
            yield bytes(out),g+1
    def explore(seed,sign):
        visited={seed};queue=[seed];numedges=0
        for state in queue:
            for nextstate,g in edges(state,sign):
                numedges+=1
                if nextstate not in visited:visited.add(nextstate);queue.append(nextstate)
        return visited,queue,numedges
    forward,forward_queue,fe=explore(root,1)
    backward,back_queue,be=explore(terminal,-1)
    co=forward & backward
    # Passive verification of complement, never used to construct coaccessibility.
    assert co=={state for state in forward if bytes(2-x for x in state[:m])+state[m:] in forward}
    tables=[];inverse_tables=[]
    for i in range(1,n):
        t=[(j,) for j in range(1,n+1)];ti=list(t)
        t[i-1]=(i,i+1,-i);t[i]=(i,)
        ti[i-1]=(i+1,);ti[i]=(-i-1,i,i+1)
        tables.append(tuple(t));inverse_tables.append(tuple(ti))
    identity=tuple((j,) for j in range(1,n+1))
    assert all(apply(tables[i],inverse_tables[i])==identity==apply(inverse_tables[i],tables[i]) for i in range(n-1))
    boundary=tuple(range(1,n+1))
    target=tuple(free(boundary+(j,)+inv(boundary)) for j in range(1,n+1))
    assert target==word_action(tuple(range(1,n))*n,tables,n)
    # Propagate backwards from the closed full-twist conjugation formula.
    images={terminal:target};suffix_count={terminal:1};comparisons=0
    for state in back_queue:
        if state not in co: continue
        for previous,g in edges(state,-1):
            if previous not in co: continue
            proposed=apply(images[state],inverse_tables[g-1])
            if previous in images:assert images[previous]==proposed
            else:images[previous]=proposed
            assert apply(images[previous],tables[g-1])==images[state]
            suffix_count[previous]=suffix_count.get(previous,0)+suffix_count[state]
            comparisons+=1
    assert len(images)==len(co) and images[root]==identity
    # Match every literal distributed record using a separately derived inverse action.
    expected_path=C/('30_action_records.txt.gz' if n==6 else f'rank{n}_action_records.txt.gz')
    encoded={sum(state[j]*3**j for j in range(m)):state for state in co}
    assert len(encoded)==len(co)
    digest=hashlib.sha256();raw_bytes=0;records=0
    with gzip.open(expected_path,'rb') as inp,gzip.GzipFile(filename=str(D/f'terminal_rank{n}_records.txt.gz'),mode='wb',mtime=0) as out:
        for code in sorted(encoded):
            state=encoded[code];packed=sum(a<<(3*i) for i,a in enumerate(state[m:]))
            literal=('S|'+str(code)+'|'+str(packed)+'|'+'|'.join(','.join(map(str,w)) for w in images[state])+'\n').encode()
            assert literal==inp.readline();out.write(literal);digest.update(literal);raw_bytes+=len(literal);records+=1
        assert inp.read()==b''
    if n==6:
        assert len(forward)==234368 and fe==711342 and len(co)==90921 and comparisons==261810
        assert raw_bytes==15258431
        def prefix(w):
            state=root
            for g in w:
                transitions=dict((i,s) for s,i in edges(state,1));state=transitions[g]
            return state
        left=(1,1,2,2);right=(2,2,1,1);collision=prefix(left)
        assert collision==prefix(right) and collision in forward and collision not in co
        assert word_action(left,tables,n)!=word_action(right,tables,n)
    result={'rank':n,'forward_states':len(forward),'forward_edges':fe,'backward_states':len(backward),
            'backward_edges':be,'intersection_states':len(co),'inverse_edge_equalities':comparisons,
            'literal_records_equal':records,'raw_bytes':raw_bytes,'sha256':digest.hexdigest(),
            'complete_words':suffix_count[root]}
    rank_results.append(result);print(json.dumps(result),flush=True)
report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS',
        'mechanism':'Explicit count/order byte-state DAG; genuine predecessors; full-twist terminal inverse-action propagation; no candidate imports or forward action-parent reuse',
        'F4_both_inverse_compositions':10,'F4_Artin_relations':10,'F4_relator':True,
        'all810_literal_images_compared':True,'twenty_counts':counts20,'twenty_survivors_by_center':kept20,
        'relator_mutation_rejected':True,'outside_coaccessible_equal_count_unequal_braid_control':True,'ranks':rank_results}
(D/'INDEPENDENT_TERMINAL_RECEIPT.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2),flush=True)
