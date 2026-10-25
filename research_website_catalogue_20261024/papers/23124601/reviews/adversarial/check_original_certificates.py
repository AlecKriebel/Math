"""Independent adversarial validation of the original finite certificates.

Uses only stdlib. No release code import, compiler, group solver or output copy.
20-letter universe: midpoint join, not producer's depth20 recursion.
30-letter proof: untrusted supplied action potential, complete edge audit.
All permanent output is the small stdout summary. Full streams stay original.
"""
from pathlib import Path
from itertools import product,combinations
from collections import defaultdict,deque
from hashlib import sha256
import gzip,json,time

C=Path(__file__).resolve().parents[2]/'sources/published-source/verification/certificates'
def req(c,why):
    if not c:raise RuntimeError(why)

def reduce_word(w):
    out=[]
    for x in w:
        if out and out[-1]==-x:out.pop()
        else:out.append(x)
    return tuple(out)
def inverse(w):return tuple(-x for x in reversed(w))
def substitute(w,A):
    out=[]
    for x in w:
        part=A[x-1] if x>0 else inverse(A[-x-1])
        for y in part:
            if out and out[-1]==-y:out.pop()
            else:out.append(y)
    return tuple(out)
def compose(A,B):return tuple(substitute(w,B) for w in A)
def identity(n):return tuple((i,) for i in range(1,n+1))
def action(word,ops,n):
    out=identity(n)
    for i in word:out=compose(out,ops[i])
    return out

# Exact literal manuscript tables transcribed independently, before any code read.
A={1:((1,),(1,2),(1,3),(1,4)),
   2:((1,-2,1),(1,),(3,),(4,)),
   3:((1,),(2,-3,2),(2,),(4,)),
   4:((1,),(2,),(3,-4,3),(3,)),
   5:((1,),(2,),(3,),(3,-2,1,4)),
   -1:((1,),(-1,2),(-1,3),(-1,4)),
   -2:((2,),(2,-1,2),(3,),(4,)),
   -3:((1,),(3,),(3,-2,3),(4,)),
   -4:((1,),(2,),(4,),(4,-3,4)),
   -5:((1,),(2,),(3,),(-1,2,-3,4))}
T={}
for i in range(1,6):
    f=list(identity(6));f[i-1]=(i,i+1,-i);f[i]=(i,);T[i]=tuple(f)
    f=list(identity(6));f[i-1]=(i+1,);f[i]=(-(i+1),i,i+1);T[-i]=tuple(f)
c=(1,2,3,4)*5;h=(5,4,3,2,1,1,2,3,4,5);z=(1,2,3,4,5)*6

def presentation(ops,n,quotient=False):
    for i in range(1,6):
        req(compose(ops[i],ops[-i])==identity(n),'right inverse '+str(i))
        req(compose(ops[-i],ops[i])==identity(n),'left inverse '+str(i))
    for i in range(1,5):req(action((i,i+1,i),ops,n)==action((i+1,i,i+1),ops,n),'braid relator')
    for i,j in combinations(range(1,6),2):
        if j-i>1:req(compose(ops[i],ops[j])==compose(ops[j],ops[i]),'distant commutation')
    if quotient:req(action(c,ops,n)==action(h,ops,n),'quotient relator c=h')

def integer_links():
    rows=[]
    for m in [0,10,20,30,40]:
        total=m//10-4;C0=(total+2)//2;D=total//2
        U=[(4*C0+D-total)//4]*5+[(5*D-total)//4]
        L=[total-sum(U)+u for u in U];solutions=[];patterns=set()
        if all(l<=u for l,u in zip(L,U)):
            for first in product(*(range(L[i],U[i]+1) for i in range(5))):
                t=first+(total-sum(first),)
                if not L[5]<=t[5]<=U[5]:continue
                links=tuple((2 if j<5 else 0)+total-2*(t[i]+t[j]) for i,j in combinations(range(6),2))
                if min(links)>=0:solutions.append(t);patterns.add(links)
        req(len(solutions)=={0:0,10:0,20:6,30:1,40:6}[m],'complete integer linking census')
        rows.append({'length':m,'rigorous_lower_box':L,'rigorous_upper_box':U,'solutions':solutions,'distinct_link_vectors':len(patterns)})
    return rows

def midpoint_candidates():
    candidates=set();counts=[]
    for center in range(6):
        groups=defaultdict(list);frontier=[(center,(0,)*5,())]
        for depth in range(10):
            nxt=[]
            for p,used,w in frontier:
                for d in [-1,1]:
                    p2=p+d
                    if not 0<=p2<6:continue
                    edge=min(p,p2)
                    if used[edge]>=4:continue
                    u=list(used);u[edge]+=1;nxt.append((p2,tuple(u),w+(edge+1,)))
            frontier=nxt
        for p,u,w in frontier:groups[p,u].append(w)
        current=set()
        for (p,u),left in groups.items():
            right=groups.get((p,tuple(4-x for x in u)),())
            for a in left:
                for b in right:current.add(a+b[::-1])
        for w in current:req((center+1,w) not in candidates,'duplicate candidate key');candidates.add((center+1,w))
        counts.append(len(current))
    req(counts==[81,162,162,162,162,81] and len(candidates)==810,'midpoint universe')
    req(len({w for k,w in candidates})==810,'same literal word has multiple centers')
    return candidates,counts

def check20():
    presentation(A,4,True);candidates,counts=midpoint_candidates();record_keys=set();passed=[]
    target=action(c+c,A,4)
    with gzip.open(C/'20_full_actions.jsonl.gz','rt') as stream:
        for line in stream:
            rec=json.loads(line);w=tuple(rec['word']);key=(rec['center'],w)
            req(key in candidates and key not in record_keys,'20 record universe/duplicate');record_keys.add(key)
            computed=action(w,A,4);stored=tuple(tuple(x) for x in rec['images'])
            req(computed==stored,'20 original full reduced image')
            if computed==target:passed.append(key)
    req(record_keys==candidates,'all810original records accounted')
    rotations={h[k:]+h[:k] for k in range(len(h))};rotations={v+v for v in rotations}
    req({w for k,w in passed}==rotations and len(passed)==10,'literal surviving rotations')
    bystart=[sum(k==i for k,w in passed) for i in range(1,7)]
    req(bystart==[1,2,2,2,2,1],'survivor start census')
    poisoned=dict(A);poisoned[5]=((1,),(2,),(3,),(3,-2,-1,4))
    try:presentation(poisoned,4,True)
    except RuntimeError:rejected=True
    else:rejected=False
    req(rejected,'corrupt quotient action falsely accepted')
    return {'candidate_method':'join of length10 halfwalks with same midpoint/complementary edge counts',
            'candidates_per_start':counts,'full_original_action_records_checked':len(record_keys),
            'survivors_per_start':bystart,'surviving_words':[list(w) for w in sorted(rotations)],
            'all_inverse_braid_commutation_quotient_relations':True,'poisoned_A5_rejected':True}

PAIRS=list(combinations(range(6),2));POW=[3**i for i in range(15)];IDX={frozenset(p):i for i,p in enumerate(PAIRS)}
IDPACK=sum(i<<(3*i) for i in range(6));FULL=3**15-1
def adjacent(pack,i):
    a=(pack>>(3*i))&7;b=(pack>>(3*(i+1)))&7
    return IDX[frozenset((a,b))],pack^((a^b)<<(3*i))^((a^b)<<(3*(i+1)))
def artin_step(signature,i):return compose(signature,T[i])

def track(word):
    q=0;pack=IDPACK
    for i in word:
        k,pack=adjacent(pack,i-1);q+=POW[k]
    return q,pack

def check30():
    presentation(T,6);R={0:IDPACK};todo=deque([0]);edgeR=0
    while todo:
        q=todo.popleft();p=R[q]
        for i in range(5):
            k,p2=adjacent(p,i);power=POW[k]
            if q//power%3==2:continue
            v=q+power;edgeR+=1
            if v in R:req(R[v]==p2,'permutation not determined by counts')
            else:R[v]=p2;todo.append(v)
    req(len(R)==234368 and edgeR==711342,'complete forward DAG')
    S={q for q in R if FULL-q in R};back={FULL};todo=deque([FULL])
    while todo:
        q=todo.popleft();p=R[q]
        for i in range(5):
            k,p2=adjacent(p,i);power=POW[k]
            if not q//power%3:continue
            prev=q-power
            if prev not in R:continue
            req(R[prev]==p2,'reverse graph permutation')
            if prev not in back:back.add(prev);todo.append(prev)
    req(back==S and len(S)==90921,'independent backward graph withinR')
    potentials={};digest=sha256();size=0;last=-1
    with gzip.open(C/'30_action_records.txt.gz','rb') as f:
        for line in f:
            digest.update(line);size+=len(line);fields=line.decode('ascii').rstrip('\n').split('|')
            req(len(fields)==9 and fields[0]=='S','record schema')
            q=int(fields[1]);p=int(fields[2]);req(q>last and q in S and R[q]==p,'state stream coverage/order/pack');last=q
            U=tuple(tuple(map(int,x.split(','))) for x in fields[3:])
            req(all(w and all(1<=abs(x)<=6 for x in w) and reduce_word(w)==w for w in U),'literal reduced free words')
            potentials[q]=U
    req(set(potentials)==S and potentials[0]==identity(6),'complete state potential/initial condition')
    req(size==15258431 and digest.hexdigest()=='af2b8ec569d613e4f3d8ba3b72d18e85e8c612f4265057b7f4c485d544d159bf','stream integrity')
    edges=0;tested_mutations=[]
    selected=set(sorted(S)[::10000])|{0,FULL};mutated_rejected=set()
    for q in S:
        p=R[q];U=potentials[q]
        for i in range(5):
            k,p2=adjacent(p,i);power=POW[k]
            if q//power%3==2:continue
            v=q+power
            if v not in S:continue
            new=artin_step(U,i+1);req(new==potentials[v],'all-edge Artin cocycle failed');edges+=1
            if q in selected and q not in mutated_rejected:
                corrupt=list(potentials[v]);corrupt[0]=reduce_word(corrupt[0]+(1,))
                req(new!=tuple(corrupt),'changed target-potential falseaccept');mutated_rejected.add(q)
    req(edges==261810,'every coaccessible edge checked')
    req(potentials[FULL]==action(z,T,6),'exact final braid action')
    q1,p1=track((1,1,2,2));q2,p2=track((2,2,1,1))
    req(q1==q2 and p1==p2 and action((1,1,2,2),T,6)!=action((2,2,1,1),T,6),'equal-count distinct-braid negative control')
    req(q1 in R and q1 not in S,'negative prefixes must be noncoaccessible')
    req(action(c+h,T,6)==action(z,T,6)==action(h+c,T,6),'full twist decomposition')
    for i in range(1,6):req(action(z+(i,),T,6)==action((i,)+z,T,6),'central full twist')
    d=(1,2,3,4,5)
    for i in range(1,5):req(action(d+(i,)+inverse(d),T,6)==T[i+1],'shift conjugation')
    return {'forward_states':len(R),'forward_edges':edgeR,'coaccessible_states':len(S),
            'coaccessible_edges_full_literal_checked':edges,'independent_backward_within_forward_graph_equal':True,
            'original_stream_bytes':size,'original_stream_SHA256':digest.hexdigest(),
            'mutated_target_potentials_rejected':len(mutated_rejected),
            'negative_equal_count_prefixes_distinct_and_outside_coaccessible':True,
            'central_fulltwist_decomposition_and_shift_conjugation':True,
            'certificate_method':'supplied stream treated as untrusted cocycle; exact complete coverage, local edge conditions, initial/final actions establish every path'}

def permgroup(gens):
    identityp=tuple(range(6));seen={identityp};todo=[identityp]
    while todo:
        p=todo.pop()
        for i in gens:
            q=list(p);q[i-1],q[i]=q[i],q[i-1];q=tuple(q)
            if q not in seen:seen.add(q);todo.append(q)
    return seen

def main():
    started=time.monotonic();links=integer_links();small=check20();print(json.dumps({'checkpoint':'integer and length20 complete','elapsed_seconds':time.monotonic()-started}),flush=True)
    large=check30();g1=permgroup([1,2,3,4]);g2=permgroup([2,3,4,5]);req(len(g1)==len(g2)==120 and g1!=g2,'strict generated subgroup distinction')
    result={'method':'Independent adversarial integer/midpoint/untrusted-cocycle validation; stdlib only, no archived code executed','integer_link_classification':links,'length20':small,'length30':large,
            'length40_permutation_subgroups':{'sizes':[len(g1),len(g2)],'exact_sets_different':True,'fixed_labels':[6,1]},
            'limits':'Mapping-class bound/injective chain and classical Artin faithfulness/positive monoid embedding are separately authenticated primary imports. Computation does not prove those inputs. Acceptance atlength20 separately follows from central cyclic rotations; equalF4images are not assumed sufficient.',
            'elapsed_seconds':time.monotonic()-started}
    print(json.dumps(result,indent=2),flush=True)

if __name__=='__main__':main()
