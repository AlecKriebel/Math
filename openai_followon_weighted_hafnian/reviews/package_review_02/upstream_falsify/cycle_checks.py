"""Independent transcription of pinned family-113 main.tex 1393-1955.
No project implementation or prior audit implementation is imported.
"""
from collections import Counter, deque
from itertools import product
from pathlib import Path
import json, hashlib, datetime
OUT=Path(__file__).parent
stats=Counter()
def run_tree(adj,max_m=10):
    dist={}
    for a in adj:
        q=deque([(a,0)]); seen={a}
        while q:
            v,d=q.popleft();dist[a,v]=d
            for w in adj[v]-seen:seen.add(w);q.append((w,d+1))
    def check(labels):
        m=len(labels);S=[{labels[(i-1)%m],labels[i]} for i in range(m)]
        def edge(u,v,c):return (min(u,v),max(u,v),c)
        def cyc_edge(u,v):
            k=u if (u+1)%m==v else v
            assert (k+1)%m in (u,v)
            return edge(u,v,labels[k])
        chords={(min(i,(i+1)%m),max(i,(i+1)%m)):cyc_edge(i,(i+1)%m) for i in range(m)}
        def chord(J):
            key=tuple(sorted((J[0],J[-1])))
            if key not in chords:chords[key]=edge(*key,min(S[J[0]]&S[J[-1]]))
            return chords[key]
        def good(J):return len(J)==2 or bool(S[J[1]]&S[J[-2]])
        def exterior(J):
            d=1 if (J[1]-J[0])%m==1 else -1
            ans=[J[-1]]
            while ans[-1]!=J[0]:ans.append((ans[-1]+d)%m)
            return ans
        cells=[]
        def split(J):
            s=len(J)-1
            if s==1:return
            P=min(S[J[0]]&S[J[-1]]);E=exterior(J)
            if good(E):
                a=[cyc_edge(J[i],J[i+1])[2] for i in range(s)]
                if P not in a:P=a[0];assert a[-1]==P
                odd=[i for i in range(1,s,2) if a[i]==P]
                if odd:p1=odd[0];p2=p1+1
                elif a.index(P)>0:p2=a.index(P);p1=p2-1
                elif max(i for i,x in enumerate(a) if x==P)<s-1:
                    p1=max(i for i,x in enumerate(a) if x==P)+1;p2=p1+1
                else:p1=1;p2=s-1
            else:
                if P in S[E[-2]]:J=list(reversed(J));E=exterior(J)
                a=[cyc_edge(J[i],J[i+1])[2] for i in range(s)]
                assert a[0]==P
                if a[-1]==P:p1=1;p2=s-1
                else:
                    t=max(i for i,x in enumerate(a) if x==P)+1
                    if t%2==0:p1=1;p2=t
                    else:p1=t;p2=s-1
            assert 0<p1<p2<s and p1%2==1 and p2%2==0
            C=[J[:p1+1],J[p1:p2+1],J[p2:],E]
            for A in C:assert (len(A)-1)%2==1 and S[A[0]]&S[A[-1]]
            gs=[good(A) for A in C];ls=[len(A)>2 for A in C]
            assert (gs[0] and gs[2]) or (gs[1] and gs[3])
            for z in [0,1]:
                if ls[z] and ls[z+2]:assert gs[1-z] and gs[3-z]
            cells.append(C)
            for A in C[:3]:split(A)
        split(list(range(m)))
        assert len(cells)==(m-2)//2
        O=[frozenset(cyc_edge(i,(i+1)%m) for i in range(z,m,2)) for z in (0,1)]
        def pats(J):
            T=frozenset(cyc_edge(J[i],J[i+1]) for i in range(0,len(J)-1,2))
            N=frozenset(cyc_edge(J[i],J[i+1]) for i in range(1,len(J)-1,2))
            return T,N,N|{chord(J)}
        def repair(J):return None if len(J)==2 else edge(J[1],J[-2],min(S[J[1]]&S[J[-2]]))
        def matching(A):
            deg=Counter(v for e in A for v in e[:2]);assert len(A)==m//2 and deg==Counter({i:1 for i in range(m)})
        def lin(*terms):
            d=Counter()
            for a,M in terms:d[M]+=a
            return d
        total=Counter()
        def add(d,sgn):
            for k,v in d.items():total[k]+=sgn*v
        def union(A,B):return Counter(A)+Counter(B)
        orig=union(*O)
        def changes(A,B):
            out=union(A,B);ad=out-orig;dr=orig-out
            assert sum(ad.values())==sum(dr.values())<=4
            restored=out-ad+dr;assert restored==orig
        for C in cells:
            stats['cells']+=1
            ps=[pats(J) for J in C]
            P=[i for i,(T,N,CX) in enumerate(ps) if T<=O[0]];Q=[i for i in range(4) if i not in P]
            assert len(P)==len(Q)==2 and (P[1]-P[0])==2
            AA=[]
            for Z in [P,Q]:
                A=frozenset(e for _,N,_ in ps for e in N)|frozenset(chord(C[i]) for i in Z);matching(A);AA.append(A)
            local=lin((1,AA[0]),(-1,AA[1]))
            # Compare all explicitly modified edges' label distances.
            es=[chord(J) for J in C]+[e for J in C for e in (cyc_edge(J[0],J[1]),cyc_edge(J[-2],J[-1]))]
            es += [repair(J) for J in C if good(J) and len(J)>2]
            assert max(dist[e[2],f[2]] for e in es for f in es)<=6
            good_pair=P if all(good(C[i]) for i in P) else Q
            def repair_through(Z,base):
                b=set(base)
                for i in Z:
                    J=C[i];b.discard(cyc_edge(J[0],J[1]));b.discard(cyc_edge(J[-2],J[-1]))
                    if len(J)>2:b.add(repair(J))
                return frozenset(b)
            B=repair_through(good_pair,frozenset(e for T,_,_ in ps for e in T));matching(B);changes(AA[0],B)
            for z,Z in enumerate([P,Q]):
                Y,X=Z;TY,NY,CY=ps[Y];TX,NX,CX=ps[X]
                H_Y=(O[z]-TY)|CY;H_X=(O[z]-TX)|CX;H_XY=(H_Y-TX)|CX
                for A in [H_Y,H_X,H_XY]:matching(A)
                err=lin((1,H_Y),(-1,H_XY),(-1,O[z]),(1,H_X))
                if len(C[Y])==2 or len(C[X])==2:assert all(v==0 for v in err.values())
                else:
                    stats['error_demands']+=1
                    other=Q if z==0 else P
                    assert all(good(C[i]) for i in other)
                    B0=repair_through(other,(O[1-z]|CX|CY))
                    # Inserting CX,CY requires their N patterns already present.
                    matching(B0);assert CX<=B0 and CY<=B0;changes(O[z],B0)
                    B1=(B0-CY)|TY;matching(B1);assert CX<=B1
                    assert union(H_Y,B1)==union(O[z],B0)
                    changes(H_Y,B1)
                    for A,G in [(O[z],B0),(H_Y,B1)]:
                        assert TX<=A and CX<=G
                        # The X+chord discrepancy component is isolated in pair.
                        vs=set(C[X]);esx=TX|CX
                        assert {e for e in A|G if e[0] in vs or e[1] in vs}==esx
                for k,v in err.items():local[k]+=(1 if z==0 else -1)*v
            add(local,1)
        assert {k:v for k,v in total.items() if v}=={O[0]:1,O[1]:-1}
        stats['walks']+=1
    for m in (4,6,8,10):
        def walks(seq):
            if len(seq)==m:
                if seq[0] in adj[seq[-1]]|{seq[-1]}:check(seq)
                return
            for v in sorted(adj[seq[-1]]|{seq[-1]}):walks(seq+[v])
        for v in adj:walks([v])
run_tree({0:{1},1:{0,2},2:{1}})
run_tree({0:{1,2,3},1:{0},2:{0},3:{0}})
result={'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','scope':'exhaustive closed label walks at lengths 4,6,8,10 on path3 and star4; deterministic source splitting; legality, good-side conditions, comparability, exact symbolic global cell identity, multiset repair count, guide condition and isolated swap component','counts':dict(stats),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(OUT/'cycle_check_result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
