"""Independent exact supporting checks, not a proof of the open conjecture.

No third-party packages, floating point, network, assert statements, or writes.
--mutant selects a deliberate semantic corruption which must exit nonzero.
"""
import argparse
import itertools as it
import json
import os
import sys
from collections import deque
from fractions import Fraction

class AuditFailure(Exception):
    pass

CHECKS = 0
MUTANT = None

def check(condition, label):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise AuditFailure(label)

def dot(a, b):
    return sum(x*y for x,y in zip(a,b))

def mm(a,b):
    return tuple(tuple(dot(row,col) for col in zip(*b)) for row in a)

def mv(a,v):
    return tuple(dot(row,v) for row in a)

def eye(n):
    return tuple(tuple(int(i==j) for j in range(n)) for i in range(n))

def tp(a):
    return tuple(zip(*a))

def ptrim(p):
    p=list(p)
    while len(p)>1 and p[-1]==0:
        p.pop()
    return tuple(p)

def padd(a,b):
    return ptrim(tuple((a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))))

def pscale(a,c):
    return ptrim(tuple(c*x for x in a))

def pmul(a,b):
    out=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            out[i+j]+=x*y
    return ptrim(out)

def padd_all(ps):
    out=(0,)
    for p in ps:
        out=padd(out,p)
    return out

def pshift(p):
    out=(0,)
    power=(1,)
    for a in p:
        out=padd(out,pscale(power,a))
        power=pmul(power,(1,1))
    return out

def test_reflections():
    b=((1,-1,-1),(-1,1,-1),(-1,-1,1))
    reflections=[]
    for i in range(3):
        reflections.append(tuple(tuple(int(j==k)-2*int(j==i)*b[i][k] for k in range(3)) for j in range(3)))
    s,t,u=reflections
    if MUTANT=='reflection_entry':
        s=((-1,3,2),(0,1,0),(0,0,1))
    for r in (s,t,u):
        check(mm(r,r)==eye(3),'each generator is an involution')
        check(mm(mm(tp(r),b),r)==b,'each generator preserves the exact Gram form')
    a=mm(t,s) if MUTANT=='reverse_st' else mm(s,t)
    check(a==((3,-2,6),(2,-1,2),(0,0,1)),'column-vector product is rho(s)rho(t)')
    ps=((0,2,4),(0,-2,4),(1,))
    if MUTANT=='root_polynomial':
        ps=((0,1,4),(0,-2,4),(1,))
    check(tuple(p[0] for p in ps)==(0,0,1),'polynomial initial value')
    for row,p in zip(a,ps):
        check(padd_all(pscale(q,k) for q,k in zip(ps,row))==pshift(p),'coefficient-wise universal recurrence A v(n)=v(n+1)')
    norm=padd_all(pscale(pmul(ps[i],ps[j]),b[i][j]) for i in range(3) for j in range(3))
    check(norm==(1,),'coefficient-wise universal norm identity')
    pair=padd_all(pscale(p,k) for p,k in zip(ps,b[1]))
    claimed=(-1,4) if MUTANT=='pairing_sign' else (-1,-4)
    check(pair==claimed,'coefficient-wise pairing B(e_t,v(n))=-1-4n')
    v=(0,0,1)
    for n in range(257):
        check(v==(2*n*(2*n+1),2*n*(2*n-1),1),'independent recurrence sample')
        check(dot(v,mv(b,v))==1,'sample norm')
        if n:
            check(abs(dot((0,1,0),mv(b,v)))>1,'all sampled positive powers violate Gram invariance')
        v=mv(a,v)
    # n=0 must not be called an obstruction; the identity is implementable.
    check(abs(dot((0,1,0),mv(b,(0,0,1))))==1,'zero-power boundary')
    # Positive powers occur in any finite-index subgroup, even if nonnormal.
    for permutation in it.permutations(range(5)):
        j=permutation[0]
        k=1
        while j!=0:
            j=permutation[j]
            k+=1
        check(1<=k<=5,'coset action returns to H at a positive power')


def connected(vertices,edges):
    vertices=set(vertices)
    if not vertices:
        return False
    seen={next(iter(vertices))}
    while True:
        more={v for edge in edges for v in edge if v in vertices and any(u in seen for u in edge)}
        new=seen|more
        if new==seen:
            return seen==vertices
        seen=new

def cycle_partition(n,edges):
    adj={v:set() for v in range(n)}
    for u,v in edges:
        adj[u].add(v);adj[v].add(u)
    cycle=None
    def dfs(v,path):
        nonlocal cycle
        for w in sorted(adj[v]):
            if w==path[0] and len(path)>=3:
                cycle=path[:]
                return True
            if w not in path and dfs(w,path+[w]):
                return True
        return False
    for v in range(n):
        if dfs(v,[v]):
            break
    if cycle is None:
        raise AuditFailure('cycle required')
    parts=[-1]*n
    parts[cycle[0]]=0;parts[cycle[1]]=1
    for v in cycle[2:]:
        parts[v]=2
    queue=deque(cycle)
    while queue:
        v=queue.popleft()
        for w in sorted(adj[v]):
            if parts[w]<0:
                parts[w]=parts[v]
                queue.append(w)
    return parts

def triangle_check(n,edges,d,parts):
    check(d>=3,'triangle must have d at least 3')
    check(all(m%d==0 for m in edges.values()),'common divisor must divide every finite label')
    check(set(parts)=={0,1,2},'three nonempty parts cover the vertices')
    for p in range(3):
        check(connected([i for i,x in enumerate(parts) if x==p],edges),'each contracted part is connected')
    pairs={tuple(sorted((parts[i],parts[j]))) for i,j in edges if parts[i]!=parts[j]}
    check(pairs=={(0,1),(0,2),(1,2)},'every target generator pair has a finite source edge')
    check(3*Fraction(1,d)<=1,'Euclidean or hyperbolic triangle, not spherical')

def test_triangle_partitions():
    edges={(0,1):3,(1,2):6,(2,3):9,(3,4):12,(0,4):15}
    d=2 if MUTANT=='spherical_triangle' else 3
    if MUTANT=='nondivisible_label':
        edges[(1,2)]=4
    parts=[0,0,0,1,2]
    if MUTANT=='disconnected_part':
        parts=[0,1,0,1,2]
    triangle_check(5,edges,d,parts)
    count=0
    for n in range(3,6):
        all_edges=list(it.combinations(range(n),2))
        for mask in range(1<<len(all_edges)):
            edges={e:3*(i+1) for i,e in enumerate(all_edges) if mask>>i&1}
            if len(edges)>=n and connected(range(n),edges):
                triangle_check(n,edges,3,cycle_partition(n,edges))
                count+=1
    check(count==626,'exhaustive connected cyclic graphs on 3,4,5 labeled vertices')
    return count


def reduced_c2_word(word):
    out=[]
    for x in word:
        if out and out[-1]==x:
            out.pop()
        else:
            out.append(x)
    return tuple(out)

def test_odd_component_quotient():
    # Odd components {0,1}, {2,3}, {4}; kill 4. Cross-edges to 4 are even.
    edges={(0,1):3,(2,3):5,(1,4):6,(3,4):8}
    images={0:(0,),1:(0,),2:(1,),3:(1,),4:()}
    if MUTANT=='kill_partial_odd_component':
        images[1]=()
    if MUTANT=='separated_even_cross_edge':
        edges[(1,2)]=2
    for (i,j),m in edges.items():
        check(reduced_c2_word((images[i]+images[j])*m)==(), 'each original relator survives in D_infinity')
    check(set(images.values())>={(0,),(1,)},'D_infinity images contain both reflections')
    if MUTANT=='invent_missing_edge':
        check(reduced_c2_word((0,1)*2)==(),'missing edges must not be given order-two relations')
    for n in range(1,101):
        check(len(reduced_c2_word((0,1)*n))==2*n,'D_infinity translation words have infinite order')
    # A killed endpoint of an odd edge kills the other endpoint, unlike an even edge.
    check(reduced_c2_word((0,)*3)==(0,),'odd killing propagation is real')
    check(reduced_c2_word((0,)*4)==(),'even edge tolerates killing the other endpoint')


def perm_mul(p,q):
    return tuple(p[q[i]] for i in range(len(p)))

def perm_inv(p):
    return tuple(p.index(i) for i in range(len(p)))

S3=tuple(it.permutations(range(3)))
ID=(0,1,2)
A=(1,0,2)
C=(0,2,1)

def test_amalgam_local_centralizer():
    h={ID,A}
    central={p for p in S3 if perm_mul(p,A)==perm_mul(A,p)}
    normal={p for p in S3 if {perm_mul(perm_mul(p,x),perm_inv(p)) for x in h}==h}
    claimed={ID} if MUTANT=='trivial_overlap_centralizer' else h
    check(central==claimed,'transposition centralizer has order two, not one')
    check(normal==h,'normalizer of amalgam edge subgroup is itself')
    cosets={frozenset(perm_mul(p,x) for x in h) for p in S3}
    fixed={k for k in cosets if frozenset(perm_mul(A,x) for x in k)==k}
    check(len(cosets)==3 and fixed=={frozenset(h)},'one fixed incident edge at each base-edge endpoint')
    check({p for p in S3 if all(perm_mul(p,x)==perm_mul(x,p) for x in S3)}=={ID},'S3 anchor center is trivial')
    # Tree recursion: w_child is in w_parent C_edge. No inversion changes cardinality.
    for k in range(1,9):
        tuples={tuple(bits) for bits in it.product(range(2),repeat=k-1)}
        check(len(tuples)==2**(k-1),'finite tree product bound for two-element overlap choices')


def fp_reduce(word):
    out=[]
    for factor,value in word:
        if (factor==0 and value==ID) or (factor!=0 and value==0):
            continue
        if out and out[-1][0]==factor:
            old=out.pop()[1]
            v=perm_mul(old,value) if factor==0 else old^value
            if v!=(ID if factor==0 else 0):
                out.append((factor,v))
        else:
            out.append((factor,value))
    return tuple(out)

def fp_mul(*words):
    return fp_reduce(x for w in words for x in w)

def fp_inv(w):
    return tuple((f,perm_inv(v) if f==0 else v) for f,v in reversed(w))

def fp_conj(w,x):
    return fp_mul(w,x,fp_inv(w))

aw=((0,A),);cw=((0,C),);bw=((1,1),);dw=((2,1),)

def tau(w):
    return fp_mul(*(fp_conj(aw,(x,)) if x[0]==1 else (x,) for x in w))

def test_cocycle():
    check(perm_mul(perm_mul(A,C),perm_mul(perm_mul(A,C),perm_mul(A,C)))==ID,'(ac)^3 in S3')
    for w in [aw,cw,bw,dw,fp_mul(aw,bw,cw,dw),fp_mul(bw,dw,bw)]:
        check(tau(tau(w))==w,'partial conjugation is its own inverse')
    candidate=bw if MUTANT=='homomorphic_conjugator' else fp_conj(aw,bw)
    for x in (aw,cw):
        check(tau(fp_conj(bw,x))==fp_conj(candidate,x),'anchor conjugator satisfies crossed composition law')
    check(candidate!=bw,'unique conjugator map is not a homomorphism')
    check(tau(aw)==aw and tau(cw)==cw and tau(dw)==dw,'partial conjugation fixes the other free factors')
    # c(fg) = f(c(g)) c(f); here f=tau, g=inner_b and c(f)=1.
    check(candidate==tau(bw),'twisted rather than untwisted conjugator identity')


def gf2_apply(rows,x):
    return sum(((row&x).bit_count()%2)<<i for i,row in enumerate(rows))

def test_factor_surjectivity_and_index_warning():
    autos=[]
    for rows in it.product(range(8),repeat=3):
        if len({gf2_apply(rows,x) for x in range(8)})==8:
            autos.append(rows)
    check(len(autos)==168,'GL(3,2) exact order')
    factor=set(range(4))
    stabilizer=[r for r in autos if {gf2_apply(r,x) for x in factor}==factor]
    images={tuple(gf2_apply(r,x) for x in range(4)) for r in stabilizer}
    spe=[r for r in autos if all(gf2_apply(r,x)==x for x in range(8))]
    if MUTANT=='replace_full_stabilizer_by_spe':
        images={tuple(gf2_apply(r,x) for x in range(4)) for r in spe}
    check(len(stabilizer)==24 and len(images)==6,'full stabilizer has full Aut(C2^2) restriction image')
    for rows in it.product(range(4),repeat=2):
        if len({gf2_apply(rows,x) for x in range(4)})==4:
            ext=(rows[0],rows[1],4)
            check(ext in stabilizer,'every factor automorphism extends by identity')
    check(len(spe)==1,'special automorphisms need not restrict onto the full automorphism group')
    # D_infinity as affine maps x -> epsilon*x+k, with translation subgroup Z.
    def mul(x,y):
        return x[0]*y[0], x[1]+x[0]*y[1]
    s=(-1,0);t=(-1,1)
    check(mul(s,s)==(1,0) and mul(t,t)==(1,0),'affine involution generators')
    translation=mul(t,s)
    check(translation==(1,1),'index-two orientation-preserving subgroup has a unit translation')
    images=[(1,n) for n in range(-30,31)]
    candidate_has_reflection=any(x[0]==-1 for x in images)
    if MUTANT=='finite_index_image_is_coxeter':
        check(candidate_has_reflection,'infinite cyclic finite-index image is not an infinite Coxeter group')
    check(not candidate_has_reflection,'translation subgroup has no reflections')
    check(all(mul(x,x)!=(1,0) for x in images if x!=(1,0)),'sample nonidentity translations are not involutions')

MUTANTS=(
    'reflection_entry','reverse_st','root_polynomial','pairing_sign',
    'spherical_triangle','nondivisible_label','disconnected_part',
    'kill_partial_odd_component','separated_even_cross_edge','invent_missing_edge',
    'trivial_overlap_centralizer','homomorphic_conjugator',
    'replace_full_stabilizer_by_spe','finite_index_image_is_coxeter',
)

def main():
    global MUTANT
    parser=argparse.ArgumentParser()
    parser.add_argument('--mutant',choices=MUTANTS)
    args=parser.parse_args()
    MUTANT=args.mutant
    check(os.getuid()==1000 and os.geteuid()==1000,'audit must actually run at UID/EUID 1000')
    test_reflections()
    count=test_triangle_partitions()
    test_odd_component_quotient()
    test_amalgam_local_centralizer()
    test_cocycle()
    test_factor_surjectivity_and_index_warning()
    print(json.dumps({'result':'PASS','checks':CHECKS,'cyclic_graphs':count,'uid':os.getuid(),'euid':os.geteuid(),'optimization':sys.flags.optimize,'mutant':MUTANT},sort_keys=True))

if __name__=='__main__':
    try:
        main()
    except AuditFailure as exc:
        print(json.dumps({'result':'FAIL','check':str(exc),'checks':CHECKS,'uid':os.getuid(),'euid':os.geteuid(),'optimization':sys.flags.optimize,'mutant':MUTANT},sort_keys=True))
        sys.exit(1)
