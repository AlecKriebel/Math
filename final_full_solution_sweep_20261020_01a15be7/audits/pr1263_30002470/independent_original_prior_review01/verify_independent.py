"""New stdlib-only graph checks. No source-author program imported/executed.

Circular metric construction, transfer-state independent-set enumeration,
generic ordinary embedding and bipartiteness tests are separate checks.
Guards are explicit exceptions and survive -O/-OO.
"""
from functools import lru_cache
from itertools import combinations
import json


def need(ok, why):
    if not ok:
        raise ValueError(why)


def edge(a,b):
    need(a != b, "loop is not a simple edge")
    return tuple(sorted((a,b)))


def validate(n, es):
    need(type(n) is int and n > 0, "positive order")
    need(all(len(e)==2 and 0 <= e[0] < e[1] < n for e in es), "bad simple graph edge")


def square(n):
    need(type(n) is int and n >= 7 and n % 2 == 1, "original odd n>=7 required")
    return {e for e in combinations(range(n),2) if min(e[1]-e[0],n-e[1]+e[0])<=2}


def degrees(n, es):
    validate(n,es)
    return [sum(v in e for e in es) for v in range(n)]


def target(n, reading):
    s=(n-1)//2
    sq=square(n)
    order=list(range(n)) if reading==1 else [(2*i)%n for i in range(n)]
    need(reading in (1,2), "unknown reading")
    deleted={edge(order[2*j],order[2*j+1]) for j in range(s-1)}
    return sq-deleted


def host(n):
    square(n)
    s=(n-1)//2
    es={edge(a,b) for a in range(s+1) for b in range(s+1,n)}
    start=0
    if s % 2 == 0:
        es|={edge(0,1),edge(1,2)}
        start=3
    es|={edge(i,i+1) for i in range(start,s+1,2)}
    return es


def pattern(n, es):
    ds=degrees(n,es)
    need(sorted(ds)==[3]*(n-3)+[4]*3, "target degree pattern")
    need(len(es)==(3*n+3)//2, "target edge count")


def matching(n, deleted, size):
    validate(n,deleted)
    need(len(deleted)==size and len({v for e in deleted for v in e})==2*size,
         "deletion is not the required matching")


def independent_sets_local(n, es, k):
    """Exhaust binary circular words, using only the actual edges and 2-step
    bandwidth. A cached feasibility transfer avoids exponential dead branches.
    It does not use the claimed run/gap classification.
    """
    need(all(min(b-a,n-b+a)<=2 for a,b in es), "transfer bandwidth assumption")
    out=[]
    for first in range(4):
        b0,b1=first&1,(first>>1)&1
        if b0 and b1 and (0,1) in es:
            continue

        @lru_cache(None)
        def possible(i, prev2, prev1, remaining):
            if remaining<0 or remaining>n-i:
                return False
            if i==n:
                return (remaining==0 and not (prev1 and b0 and edge(n-1,0) in es)
                        and not (prev2 and b0 and edge(n-2,0) in es)
                        and not (prev1 and b1 and edge(n-1,1) in es))
            if possible(i+1,prev1,0,remaining):
                return True
            if ((not prev1 or edge(i-1,i) not in es) and
                (not prev2 or edge(i-2,i) not in es)):
                return possible(i+1,prev1,1,remaining-1)
            return False

        def collect(i,prev2,prev1,remaining,mask):
            if i==n:
                out.append(mask)
                return
            if possible(i+1,prev1,0,remaining):
                collect(i+1,prev1,0,remaining,mask)
            if ((not prev1 or edge(i-1,i) not in es) and
                (not prev2 or edge(i-2,i) not in es) and
                possible(i+1,prev1,1,remaining-1)):
                collect(i+1,prev1,1,remaining-1,mask|(1<<i))
        if possible(2,b0,b1,k-b0-b1):
            collect(2,b0,b1,k-b0-b1,first)
    return sorted(out)


def predicted(n):
    s=(n-1)//2
    if s%2:
        t=(s-1)//2
        return sorted([sum(1<<v for k in range(t) for v in (4*k,4*k+1))|(1<<(n-3)),
                       sum(1<<v for k in range(t) for v in (4*k+2,4*k+3))|(1<<(n-1))])
    return [sum(1<<v for k in range(s//2) for v in (4*k,4*k+1))]


def adjacency(n, es):
    a=[0]*n
    for u,v in es:
        a[u]|=1<<v
        a[v]|=1<<u
    return a


def witness(n,h,g,perm,induced=False):
    need(sorted(perm)==list(range(n)), "embedding must be a spanning bijection")
    for u,v in combinations(range(n),2):
        image=edge(perm[u],perm[v])
        if (u,v) in h:
            need(image in g, "target edge does not map to host edge")
        elif induced:
            need(image not in g, "induced convention forbids extra host edge")


def embedding(n,h,g,induced=False):
    """Generic injection search: only required edges are constrained unless
    induced=True. Twin pruning is a literal transposition automorphism of host
    vertices not yet used; it does not use the independent-side reduction.
    """
    validate(n,h);validate(n,g)
    ha,ga=adjacency(n,h),adjacency(n,g)
    hd=[a.bit_count() for a in ha];gd=[a.bit_count() for a in ga]
    perm=[-1]*n
    full=(1<<n)-1
    nodes=0

    def search(used):
        nonlocal nodes
        nodes+=1
        if used==full:
            return tuple(perm)
        best=None
        for u in range(n):
            if perm[u]>=0:
                continue
            cs=[]
            for v in range(n):
                if used>>v&1 or hd[u]>gd[v]:
                    continue
                ok=True
                for j in range(n):
                    if perm[j]>=0:
                        req=bool(ha[u]>>j&1);got=bool(ga[v]>>perm[j]&1)
                        if (req and not got) or (induced and req!=got):
                            ok=False;break
                if ok:
                    cs.append(v)
            if not cs:
                return None
            key=(len(cs),-sum(perm[j]>=0 for j in range(n) if ha[u]>>j&1),-hd[u],u)
            if best is None or key<best[0]:
                best=(key,u,cs)
        _,u,cs=best
        reps=[]
        for v in cs:
            if any((ga[v]&~(1<<w))==(ga[w]&~(1<<v)) for w in reps):
                continue
            reps.append(v)
            perm[u]=v
            result=search(used|(1<<v))
            if result is not None:
                return result
            perm[u]=-1
        return None
    result=search(0)
    if result is not None:
        witness(n,h,g,result,induced)
    return result,nodes


def bipartite(n, es, removed):
    a=adjacency(n,es)
    color={removed:-1}
    for root in range(n):
        if root in color:
            continue
        color[root]=0;todo=[root]
        while todo:
            u=todo.pop()
            for v in range(n):
                if v==removed or not(a[u]>>v&1):
                    continue
                if v in color:
                    if color[v]==color[u]:
                        return False
                else:
                    color[v]=1-color[u];todo.append(v)
    return True


def nine_certificate(deleted, removed=0, bad_cycle=False):
    sq=square(9)
    d={edge((u-removed)%9,(v-removed)%9) for u,v in deleted}
    triangles=[{edge(i,i+1),edge(i,i+2),edge(i+1,i+2)} for i in range(1,7)]
    untouched=[t for t in triangles if not t&d]
    if untouched:
        need(untouched[0]<=sq-d and all(0 not in e for e in untouched[0]), "bad triangle certificate")
        return "triangle"
    need(d=={(2,3),(4,5),(6,7)}, "triangle cover does not force claimed matching")
    cycle=[1,3,5,7,8] if not bad_cycle else [1,2,3,5,8]
    ce={edge(cycle[i],cycle[(i+1)%5]) for i in range(5)}
    need(ce<=sq-d and 0 not in cycle, "bad surviving five-cycle certificate")
    return "five_cycle"


def check_nine_order(n):
    need(n==9, "nine-vertex theorem cannot be replaced by n7 broad theorem")


def rank_f2(vectors):
    pivots={}
    for x in vectors:
        while x:
            b=x.bit_length()-1
            if b in pivots:
                x^=pivots[b]
            else:
                pivots[b]=x;break
    return len(pivots)


def main():
    orders=[]
    for n in range(7,52,2):
        s=(n-1)//2;g=host(n)
        need(min(degrees(n,g))==s+1, "host minimum degree")
        row={"n":n,"minimum_degree":s+1}
        for reading in (1,2):
            h=target(n,reading);pattern(n,h)
            matching(n,square(n)-h,s-1)
            js=independent_sets_local(n,h,s)
            need(js==(predicted(n) if reading==1 else []), "complete independent-set classification")
            for mask in js:
                rem={e for e in h if not any(mask>>v&1 for v in e)}
                F={v for v,d in enumerate(degrees(n,h)) if d==4}
                need(len(rem)==3-sum(mask>>v&1 for v in F), "edge double count")
                if s%2:
                    need(max(degrees(n,rem))==2, "residual path obstruction")
                else:
                    need(len(rem)==3 and sorted(d for d in degrees(n,rem) if d)==[2,2,2], "residual triangle obstruction")
            row['R'+str(reading)+'_independent_sets']=js
        orders.append(row)
    direct=[]
    for n in (7,9,11,13):
        for reading in (1,2):
            h=target(n,reading)
            emb,nodes=embedding(n,h,host(n))
            need(emb is None,"unexpected ordinary spanning embedding")
            # Relabeled target plus every possible extra host edge is a
            # positive control specifically distinguishing ordinary semantics.
            perm=tuple((2*i+1)%n for i in range(n))
            rel={edge(perm[u],perm[v]) for u,v in h}
            witness(n,h,rel,perm)
            found,pos_nodes=embedding(n,h,set(combinations(range(n),2)))
            need(found is not None,"positive complete-host control failed")
            direct.append({'n':n,'reading':reading,'negative_search_nodes':nodes,
                           'positive_search_nodes':pos_nodes})
    sq=square(9);ms=[]
    for es in combinations(sorted(sq),3):
        if len({v for e in es for v in e})==6:
            ms.append(set(es))
    need(len(ms)==177,"all matching count")
    cert={"triangle":0,"five_cycle":0}
    for d in ms:
        h=sq-d;pattern(9,h)
        for v in range(9):
            need(not bipartite(9,h,v),"bipartite singleton deletion would evade obstruction")
            cert[nine_certificate(d,v)]+=1
    need(cert=={'triangle':1584,'five_cycle':9},"complete certificate distribution")
    k441={edge(u,v) for u,v in combinations(range(9),2)
          if (0 if u<4 else 1 if u<8 else 2)!=(0 if v<4 else 1 if v<8 else 2)}
    need(min(degrees(9,k441))==5,"K441 minimum degree")
    need(all(bipartite(9,k441,8) for _ in [0]),"host singleton-deletion necessity")
    broad7=square(7)-{(0,1),(3,5)}
    foil,foil_nodes=embedding(7,broad7,host(7))
    need(foil is not None,"n7 broad positive foil")
    broad_periphery=(2,4,6,1,0,5,3)
    need({edge(broad_periphery[i],broad_periphery[(i+1)%7]) for i in range(7)}<=square(7),
         "broad n7 periphery is not Hamilton in the squared cycle")
    need({edge(broad_periphery[i],broad_periphery[i+1]) for i in (3,5)}=={(0,1),(3,5)},
         "broad n7 alternate peripheral deletion")
    # Exact transcribed Definition28 graph X, independent of the family labels.
    xe={(a-1,b-1) for a,b in [(1,2),(1,3),(1,6),(1,7),(2,3),(2,6),(2,7),
                            (3,4),(3,5),(4,5),(4,6),(4,7),(5,6),(5,7)]}
    xperm=(0,1,4,2,3,5,6)
    witness(7,xe,host(7),xperm,True)
    cycles=[(1,2,3,4,7,5,6),(1,2,3,4,6,5,7),(1,2,6,5,7,4,3),
            (1,2,6,5,3,4,7),(1,2,6,4,7,5,3),(1,2,6,4,3,5,7),
            (1,2,7,4,6,5,3),(1,7,2,6,5,4,3)]
    basis=[];ordered=sorted(xe)
    for cy in cycles:
        es={edge(cy[i]-1,cy[(i+1)%7]-1) for i in range(7)}
        need(es<=xe and len(set(cy))==7,"Heinig Hamilton circuit transcription")
        basis.append(sum(1<<ordered.index(e) for e in es))
    need(rank_f2(basis)==len(xe)-7+1==8,"positive cycle-space basis control")
    # Fourteen actual corruptions/boundary misclaims, required to fail.
    special={(2,3),(4,5),(6,7)}
    identity=tuple(range(7))
    bad=[
        ('even_order',lambda:square(8)),
        ('out_of_range_edge',lambda:validate(9,{(0,9)})),
        ('overlapping_deletions',lambda:matching(9,{(0,1),(1,2),(3,4)},3)),
        ('too_few_deletions',lambda:pattern(9,sq-{(0,1),(2,3)})),
        ('wrong_five_cycle',lambda:nine_certificate(special,bad_cycle=True)),
        ('wrong_order_for_broad_claim',lambda:check_nine_order(7)),
        ('false_n7_broad_negative',lambda:need(foil is None,'n7 broad negative is false')),
        ('induced_equals_ordinary',lambda:witness(7,target(7,1),set(combinations(range(7),2)),identity,True)),
        ('invalid_embedding_bijection',lambda:witness(7,target(7,1),host(7),(0,0,2,3,4,5,6))),
        ('missing_wrap_edge',lambda:need((1,8) in sq-{(1,8)},'wrap edge removed')),
        ('wrong_R1_classification',lambda:need(independent_sets_local(7,target(7,1),3)==predicted(7)[:1],'one independent set omitted')),
        ('R2_adjacent_deletions',lambda:pattern(9,sq-{(0,2),(2,4),(6,8)})),
        ('host_internal_edges_removed',lambda:need(min(degrees(7,{e for e in host(7) if e[1]>=4}))==4,'host threshold fails')),
        ('wrong_basis_cycle',lambda:need(edge(0,4) in xe,'invented circuit edge')),
    ]
    rejected=[]
    for name,fn in bad:
        try:
            fn()
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('corruption accepted: '+name)
    print(json.dumps({'status':'PASS','structural_orders':orders,'direct_ordinary_embedding_checks':direct,
        'all_nine_matchings':len(ms),'all_nine_singleton_deletions':9*len(ms),
        'certificate_distribution':cert,'broad_n7_embedding':foil,'broad_n7_search_nodes':foil_nodes,
        'broad_n7_periphery':broad_periphery,
        'Heinig_X_isomorphism':xperm,'Heinig_Hamilton_basis_rank':8,
        'negative_controls_rejected':rejected,'optimization_safe_guards':True,
        'source_author_programs_executed':False,'floating_point_used':False},indent=2,sort_keys=True))


if __name__=='__main__':
    main()
