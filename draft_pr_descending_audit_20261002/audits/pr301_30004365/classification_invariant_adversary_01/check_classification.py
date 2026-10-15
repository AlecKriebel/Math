#!/usr/bin/env python3
"""Independent finite algebra controls; not an implementation of the surface algorithm."""
import collections, itertools, json, math, pathlib
ROOT=pathlib.Path(__file__).resolve().parent
checks=collections.Counter()
evaluations=collections.Counter()
def check(condition,family):
    checks[family]+=1
    if not condition: raise AssertionError(family)
def pair2(x,y,g):
    return sum(((x>>(2*i))&1)*((y>>(2*i+1))&1)+((x>>(2*i+1))&1)*((y>>(2*i))&1) for i in range(g))%2
def q2(e,x,g):
    return ((e&x).bit_count()+sum(((x>>(2*i))&1)*((x>>(2*i+1))&1) for i in range(g)))%2
arf_results=[]
for g in range(1,4):
    d=1<<(2*g)
    distribution=collections.Counter()
    for e in range(d):
        arf=sum(((e>>(2*i))&1)*((e>>(2*i+1))&1) for i in range(g))%2
        distribution[arf]+=1
        zeros=sum(q2(e,x,g)==0 for x in range(d))
        check(zeros==2**(2*g-1)+(-1)**arf*2**(g-1),'arf_zero_count')
        for x,y in itertools.product(range(d),repeat=2):
            check(q2(e,x^y,g)==q2(e,x,g)^q2(e,y,g)^pair2(x,y,g),'quadratic_identity')
        for a in range(1,d):
            basis=[(1<<i)^ (a if pair2(a,1<<i,g) else 0) for i in range(2*g)]
            transformed=sum(q2(e,basis[2*i],g)*q2(e,basis[2*i+1],g) for i in range(g))%2
            check(transformed==arf,'symplectic_transvection_arf')
            for i,j in itertools.product(range(2*g),repeat=2):
                check(pair2(basis[i],basis[j],g)==pair2(1<<i,1<<j,g),'transvection_symplectic')
    arf_results.append({'genus':g,'refinement_distribution':dict(distribution)})

# The radical makes a handle-only Arf formula depend on the lift precisely when q(r)=1.
radical_changes=0
for e in range(16):
    old=sum(((e>>(2*i))&1)*((e>>(2*i+1))&1) for i in range(2))%2
    for rvalue in [0,1]:
        for basis_index in range(4):
            bits=[(e>>i)&1 for i in range(4)]; bits[basis_index]^=rvalue
            new=(bits[0]*bits[1]+bits[2]*bits[3])%2
            if rvalue==0: check(new==old,'radical_zero_lift_arf')
            else: radical_changes+=new!=old
check(radical_changes>0,'radical_nonzero_arf_is_not_invariant')

# Full mod-4 quadratic refinement orbit controls for genus two and one independent peripheral class.
g=2; handle_states=list(itertools.product(range(4),repeat=4))
vectors=[a for a in itertools.product(range(4),repeat=5) if any(v%2 for v in a[:4])]
def q4(c,r,a):
    return (sum(c[i]*a[i] for i in range(4))+r*a[4]+2*(a[0]*a[1]+a[2]*a[3]))%4
orbit_results=[]
for r in range(4):
    unseen=set(handle_states); orbits=[]
    while unseen:
        first=min(unseen); unseen.remove(first); orbit={first}; queue=[first]
        while queue:
            c=queue.pop()
            for a in vectors:
                k=(q4(c,r,a)+2)%4
                p=(-a[1],a[0],-a[3],a[2])
                new=tuple((c[i]+k*p[i])%4 for i in range(4))
                evaluations['mod4_orbit_edges']+=1
                if new not in orbit:
                    orbit.add(new); queue.append(new); unseen.discard(new)
        parity={any(v%2 for v in c) or bool(r%2) for c in orbit}
        check(len(parity)==1,'mod4_orbit_parity')
        if r==0 and not next(iter(parity)):
            arfs={(c[0]//2*c[1]//2+c[2]//2*c[3]//2)%2 for c in orbit}
            check(len(arfs)==1,'mod4_spin_orbit_arf')
        orbits.append(len(orbit))
    expected=([6,10,240] if r==0 else [16,240] if r==2 else [256])
    check(sorted(orbits)==expected,'lp_mod4_orbit_classes')
    orbit_results.append({'q_peripheral':r,'orbit_sizes':sorted(orbits)})

# Rank-two winding ideal invariance under unimodular shears, swaps/signs, and peripheral detours.
for x,y,t in itertools.product(range(-7,8),range(-7,8),range(-5,6)):
    d=math.gcd(x,y,t)
    for k in range(-3,4):
        check(math.gcd(x,y+k*x,t)==d,'gcd_unimodular_shear')
        check(math.gcd(x+k*t,y,t)==d,'gcd_peripheral_detour')
    check(math.gcd(y,-x,t)==d,'gcd_orientation_basis_swap')
check(math.gcd(0,0,0)==0,'gcd_all_zero')
check(math.gcd(6,12)==6 and math.gcd(6,12,4,-4)==2 and math.gcd(10,12)==2,'peripheral_terms_cannot_be_omitted')

def witness(m,n):
    vertices=[('a',i) for i in range(m)]+[('b',i) for i in range(n)]
    arrows={f'u{i}':(('a',i),('a',(i+1)%m)) for i in range(m)}
    arrows.update({f'v{i}':(('b',i),('b',(i+1)%n)) for i in range(n)})
    arrows['z']=(('a',0),('b',0))
    relations={(f'u{i}',f'u{(i+1)%m}') for i in range(m)}|{(f'v{i}',f'v{(i+1)%n}') for i in range(n)}
    incoming={v:[a for a,e in arrows.items() if e[1]==v] for v in vertices}
    outgoing={v:[a for a,e in arrows.items() if e[0]==v] for v in vertices}
    for v in vertices: check(len(incoming[v])<=2 and len(outgoing[v])<=2,'witness_gentle_degree')
    for a,(s,t) in arrows.items():
        for rel in [False,True]:
            check(sum(((a,b) in relations)==rel for b in outgoing[t])<=1,'witness_gentle_continuation')
            check(sum(((b,a) in relations)==rel for b in incoming[s])<=1,'witness_gentle_predecessor')
    paths=[(a,) for a in arrows]; counts=[len(vertices),len(paths)]
    maximal=[]
    while paths:
        nxt=[]
        for p in paths:
            continuation=[b for b in outgoing[arrows[p[-1]][1]] if (p[-1],b) not in relations]
            if not continuation and not any((b,p[0]) not in relations for b in incoming[arrows[p[0]][0]]): maximal.append(p)
            nxt.extend(p+(b,) for b in continuation)
        paths=nxt
        if paths: counts.append(len(paths))
        check(len(counts)<=5,'witness_no_infinite_permitted_path')
    check(counts==[m+n,m+n+1,2,1],'witness_path_counts')
    check(len(maximal)==m+n-1,'witness_maximal_thread_count')
    # Topological and winding deductions are proved in PRINTED_RANGE_COUNTEREXAMPLE.md, not inferred by this code.
    return {'m':m,'n':n,'dimension':sum(counts),'path_counts':counts,'maximal_permitted_paths':maximal,'deduced_key':{'g':0,'b':1,'p':2,'records':sorted([(m+n-1,m+n-2),(0,-m),(0,-n)])}}
w=[witness(3,5),witness(4,4)]
check(w[0]['deduced_key']['records']!=w[1]['deduced_key']['records'],'witness_candidate_distinguishes')
check(sorted([n for n,_ in w[0]['deduced_key']['records']])==sorted([n for n,_ in w[1]['deduced_key']['records']]),'witness_printed_n_match')
check(len([z for n,z in w[0]['deduced_key']['records'] if n])==1 and [z for n,z in w[0]['deduced_key']['records'] if n]==[z for n,z in w[1]['deduced_key']['records'] if n],'witness_printed_original_boundary_match')

# Marginal equality does not imply equality of paired records.
a=[(2,2),(3,-2)]; b=[(2,-2),(3,2)]
check(sorted(n for n,_ in a)==sorted(n for n,_ in b) and sorted(w for _,w in a)==sorted(w for _,w in b) and sorted(a)!=sorted(b),'paired_record_trap')
result={'status':'PASS','meaning':'Finite exact algebraic controls only; proofs and external theorem inputs remain separately necessary.','total_assertions':sum(checks.values()),'families':dict(checks),'non_assertion_evaluations':dict(evaluations),'arf_refinements':arf_results,'mod4_orbits':orbit_results,'nonzero_radical_handle_arf_changes':radical_changes,'exact_quiver_witnesses':w}
(ROOT/'CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
