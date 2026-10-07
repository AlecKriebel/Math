"""Independent exact controls; no author module imports. Python standard library.
Run python3 -B audit/supplemental_controls.py from the packet directory.
These finite controls support, and do not replace, the written proofs.
"""
import itertools,json,math
from collections import defaultdict
from fractions import Fraction as F
from functools import cache
import independent_rank_audit as I
COUNTS=defaultdict(int)
def demand(ok,name):
    if not ok:raise AssertionError(name)
    COUNTS[name]+=1

def scale(a,k):return {w:x*k for w,x in a.items() if x*k}
def plus(a,b):return I.subtract(a,scale(b,-1))

@cache
def shuffle_words(u,v):
    if not u:return {v:1}
    if not v:return {u:1}
    out=defaultdict(int)
    for w,x in shuffle_words(u[1:],v).items():out[(u[0],)+w]+=x
    for w,x in shuffle_words(u,v[1:]).items():out[(v[0],)+w]+=x
    return dict(out)

def shuffle(a,b):
    out=defaultdict(int)
    for u,x in a.items():
        for v,y in b.items():
            for w,z in shuffle_words(u,v).items():out[w]+=x*y*z
    return {w:x for w,x in out.items() if x}

def alternating_control(m):
    n=2*m;p={():1}
    for i in range(0,n,2):p=shuffle(p,{(i,i+1):1,(i+1,i):-1})
    omega={w:(-1)**sum(w[i]>w[j] for i in range(n) for j in range(i+1,n)) for w in itertools.permutations(range(n))}
    for i in range(n):demand(not I.delete(omega,i),'alternating_deletion')
    demand(not I.cyclic(omega),'alternating_cyclic_zero')
    pair=sum(x*p.get(w,0) for w,x in omega.items())
    demand(pair==2**m*math.factorial(m),'recursive_shuffle_pairing')
    return {'m':m,'shuffle_terms':len(p),'pairing':pair}

def matrix_for_polynomial(poly,d,m):
    # Independent action evaluator: apply each word directly to each basis vector.
    # Letter adjacency prepends it or removes it when it is the first letter.
    basis=[w for k in range(m+1) for w in itertools.product(range(d),repeat=k)]
    out={}
    for source in basis:
        column=defaultdict(int)
        for word,coefficient in poly.items():
            state={source:coefficient}
            for letter in reversed(word):
                nxt=defaultdict(int)
                for w,x in state.items():
                    if len(w)<m:nxt[(letter,)+w]+=x
                    if w and w[0]==letter:nxt[w[1:]]+=x
                state={w:x for w,x in nxt.items() if x}
            for w,x in state.items():column[w]+=x
        for target,x in column.items():
            if x:out[target,source]=x
    return out,len(basis)

def trace_controls():
    rows=[]
    for d,maxm in ((2,5),(3,4)):
        for m in range(2,maxm+1):
            polys=[I.lie(w) for w in itertools.product(range(d),repeat=m) if I.lyndon(w)]
            mixture={}
            for i,p in enumerate(polys):mixture=plus(mixture,scale(p,(-1)**i*(i+1)))
            for k,p in enumerate(polys+[mixture]):
                mat,size=matrix_for_polynomial(p,d,m);eps=(-1)**(m-1)
                demand({w:x for (w,v),x in mat.items() if v==() and len(w)==m}==p,'matrix_top_word_coefficients')
                demand(mat=={(v,w):eps*x for (w,v),x in mat.items()},'matrix_transpose_parity')
                norm=sum(x*x for x in mat.values());tr=sum(x*mat.get((v,w),0) for (w,v),x in mat.items())
                demand(tr==eps*norm and tr!=0,'matrix_trace_square_nonzero')
                demand(bool(I.cyclic(I.multiply(p,p))),'lie_square_cyclic_nonzero')
                rows.append({'d':d,'m':m,'polynomial':k,'matrix_size':size,'trace_square':tr})
    return rows

def truncated_product(a,b,N):
    out=defaultdict(F)
    for u,x in a.items():
        for v,y in b.items():
            if len(u)+len(v)<=N:out[u+v]+=x*y
    return {w:x for w,x in out.items() if x}

def path_control(m):
    segments=[(0,1),(1,1),(0,-1),(1,-1)];p={(0,1):1,(1,0):-1}
    for _ in range(2,m):
        segments=[(0,1)]+segments+[(0,-1)]+[(a,-s) for a,s in reversed(segments)]
        p=I.subtract(I.multiply({(0,):1},p),I.multiply(p,{(0,):1}))
    N=2*m;sig={():F(1)}
    for a,s in segments:
        e={(a,)*k:F(s**k,math.factorial(k)) for k in range(N+1)}
        sig=truncated_product(sig,e,N)
    demand(all(sum(s for a,s in segments if a==b)==0 for b in (0,1)),'path_closed')
    demand(not any(x for w,x in sig.items() if 0<len(w)<m),'path_lower_terms_zero')
    demand({w:x for w,x in sig.items() if len(w)==m}==p,'path_leading_term')
    for n in range(m,2*m):
        for a in range(n+1):
            c=(a,n-a);v={w:x for w,x in sig.items() if len(w)==n and w.count(0)==a}
            den=math.lcm(*(x.denominator for x in v.values()))
            z={w:int(x*den) for w,x in v.items()}
            bs=list(I.brackets(c));rank=I.integer_rank(bs)
            demand(I.integer_rank(bs+[z])==rank,'path_below_2m_bracket_membership')
    cyc=I.cyclic({w:x for w,x in sig.items() if len(w)==2*m})
    demand(bool(cyc),'path_degree_2m_cyclic_detection')
    leadingcyc=I.cyclic(scale(I.multiply(p,p),F(1,2)))
    demand(cyc==leadingcyc,'path_degree_2m_half_square_cyclic')
    return {'m':m,'segments':len(segments),'degree_2m_nonzero_cyclic_orbits':len(cyc)}

def main():
    out={'alternating':[alternating_control(m) for m in range(1,5)],'matrix_controls':trace_controls(),'paths':[path_control(m) for m in range(3,6)]}
    odd={(0,1,2):1,(0,2,1):-1,(1,0,2):-1,(1,2,0):1,(2,0,1):1,(2,1,0):-1}
    demand(bool(I.delete(odd,0)) and bool(I.cyclic(odd)),'negative_odd_alternation')
    demand(I.integer_rank([{0:2,1:4},{0:3,1:6}])==1,'negative_rank_dependence')
    demand(I.integer_rank([{0:2,1:4},{0:3,1:7}])==2,'positive_rank_independence')
    out['counts']=dict(sorted(COUNTS.items()));out['total_controls']=sum(COUNTS.values());out['status']='PASS_SUPPORTING_FINITE_CONTROLS'
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
