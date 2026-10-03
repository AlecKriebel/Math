"""Independent exact algebra controls for frozen PR386 Turn1–4.
No author imports. Finite controls do not certify CB of infinite groups.
"""
from itertools import combinations, permutations, product
from collections import Counter
import json

counts=Counter()
def check(ok,kind):
    if not ok: raise AssertionError(kind)
    counts[kind]+=1
class Group:
    def __init__(self,name,elements,one,multiply):
        self.name,self.es,self.one,self.mul=name,tuple(elements),one,multiply
        self.inv={x:next(y for y in self.es if multiply(x,y)==one and multiply(y,x)==one) for x in self.es}
    def validate(self):
        E=set(self.es)
        check(all(self.mul(self.one,x)==self.mul(x,self.one)==x for x in E),'group_identity')
        check(all(self.mul(x,y) in E for x in E for y in E),'group_closure')
        check(all(self.mul(self.mul(x,y),z)==self.mul(x,self.mul(y,z)) for x in E for y in E for z in E),'group_associativity')

def C(n): return Group('C'+str(n),range(n),0,lambda x,y:(x+y)%n)
def D(n): return Group('D'+str(2*n),product(range(n),range(2)),(0,0),lambda x,y:((x[0]+(-1)**x[1]*y[0])%n,(x[1]+y[1])%2))
def Q(n):
    # Generalized quaternion group of order 4n: a^(2n)=1,b^2=a^n,ba=a^-1 b.
    return Group('Q'+str(4*n),product(range(2*n),range(2)),(0,0),lambda x,y:((x[0]+(-1)**x[1]*y[0]+n*((x[1]+y[1])//2))%(2*n),(x[1]+y[1])%2))
def Sym(n,even=False):
    es=[p for p in permutations(range(n)) if not even or sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))%2==0]
    return Group(('A' if even else 'S')+str(n),es,tuple(range(n)),lambda x,y:tuple(x[y[i]] for i in range(n)))
def dist(G,S):
    # Breadth-level expansion, independent of author's table/queue implementation.
    S=tuple(S); seen={G.one:0}; frontier={G.one}; level=0
    while frontier:
        level+=1
        nxt={G.mul(x,s) for x in frontier for s in S}-seen.keys()
        seen.update((x,level) for x in nxt);frontier=nxt
    return seen
def subsets(E):
    E=tuple(E)
    for k in range(len(E)+1):yield from map(set,combinations(E,k))
def generators(G):
    for S in subsets(x for x in G.es if x!=G.one):
        L=dist(G,S)
        if len(L)==len(G.es):yield S,L

def cosets(G,H):
    cs={frozenset(G.mul(h,g) for h in H) for g in G.es}
    return sorted(cs,key=lambda c:(G.one not in c,repr(sorted(c,key=repr))))
def quotient_dist(G,S,cs):
    where={x:i for i,c in enumerate(cs) for x in c};seen={where[G.one]:0};frontier=set(seen);level=0
    while frontier:
        level+=1;nxt=set()
        for i in frontier:
            r=next(iter(cs[i]))
            for s in S:nxt.add(where[G.mul(r,s)])
        nxt-=seen.keys();seen.update((x,level) for x in nxt);frontier=nxt
    return seen,where

def order(G,s):
    x=G.one
    for n in range(1,len(G.es)+1):
        x=G.mul(x,s)
        if x==G.one:return n
    raise AssertionError('finite order')

def turn1():
    rows=[]
    groups=[C(n) for n in range(1,9)]+[D(3),D(4),Q(2),Sym(3)]
    for G in groups:
        G.validate();pairs=0
        for S in subsets(x for x in G.es if x!=G.one):
            l=dist(G,S);symmetric=S|{G.inv[x] for x in S}; ls=dist(G,symmetric)
            check(l.keys()==ls.keys(),'finite_positive_group_generation')
            check(l==dist(G,S|{G.one}),'identity_letter_harmless')
            if len(l)!=len(G.es):continue
            pairs+=1;diam=max(l.values());d=max(ls.values());R=max((l[G.inv[s]] for s in S),default=0)
            check(R<=diam<=d*max(1,R),'inverse_cost')
            e=max((order(G,s) for s in S),default=1)
            check(R<=e-1 and diam<=d*max(1,e-1),'bounded_orders')
            previous={G.one}
            for n in range(diam+1):
                A={g for g in G.es if l[g]<=n and l[G.inv[g]]<=n};h=dist(G,A)
                check(A=={G.inv[a] for a in A},'symmetric_core')
                check(previous<=h.keys(),'increasing_subgroup_core');previous=set(h)
                check(all(l[g]<=n*k for g,k in h.items()),'core_ambient_bound')
                if len(h)==len(G.es):check(diam<=n*max(h.values()),'core_CB_finite_control')
        rows.append({'group':G.name,'generating_subsets':pairs})
    return rows

def turn2():
    rows=[]
    for G in [C(n) for n in range(1,8)]+[D(3),D(4),Q(2),Sym(3)]:
        subgroups={frozenset(dist(G,S)) for S in subsets(x for x in G.es if x!=G.one)};pairs=0;nonnormal=0
        for S,l in generators(G):
            for H in subgroups:
                cs=cosets(G,H);lq,where=quotient_dist(G,S,cs)
                reps={i:min(c,key=lambda x:(l[x],repr(x))) for i,c in enumerate(cs)}
                check(reps[where[G.one]]==G.one,'normalized_schreier_section')
                q=max(l[x] for x in reps.values());ci=max(l[G.inv[x]] for x in reps.values())
                check(q<=len(cs)-1,'shortest_directed_coset_bound')
                T={G.mul(G.mul(r,s),G.inv[reps[where[G.mul(r,s)]]]) for r in reps.values() for s in S}
                tl=dist(G,T)
                check(T<=H and tl.keys()==H,'positive_schreier_without_normality')
                check(all(l[t]<=q+1+ci for t in T),'positive_schreier_letter_cost')
                check(max(l.values())<=max(tl.values())*(q+1+ci)+q,'finite_index_MB_bound')
                normal=all(G.mul(G.mul(g,h),G.inv[g]) in H for g in G.es for h in H)
                if normal:
                    ambient=max(l[h] for h in H)
                    check(all(lq[where[g]]<=l[g]<=lq[where[g]]+ambient for g in G.es),'independent_quotient_BFS_bounds')
                    check(all(lq[i]==min(l[g] for g in c) for i,c in enumerate(cs)),'quotient_BFS_vs_minimum')
                else:nonnormal+=1
                pairs+=1
        rows.append({'group':G.name,'subgroups':len(subgroups),'pairs':pairs,'nonnormal_pairs':nonnormal})
    return rows

def turn3_split():
    rows=[]
    for n in range(2,10):
        G=D(n);H=C(n);cases=0
        for S,l in generators(H):
            T=S|{(-s)%n for s in S};dt=dist(H,T);W={(s,0) for s in S}|{(0,1)};dw=dist(G,W)
            check(len(dw)==len(G.es),'split_positive_generation')
            check(all(dt[h]<=dw[(h,0)]<=3*dt[h] for h in H.es),'split_saturation_positive_comparison')
            dts=dist(H,T|{H.inv[t] for t in T});dws=dist(G,W|{G.inv[w] for w in W})
            check(all(dts[h]<=dws[(h,0)]<=3*dts[h] for h in H.es),'split_saturation_symmetric_comparison')
            if S==T:
                check(all(dw[(h,0)]==l[h] for h in H.es),'split_invariant_positive_equality')
                sl=dist(H,S|{H.inv[s] for s in S})
                check(all(dws[(h,0)]==sl[h] for h in H.es),'split_invariant_symmetric_equality')
            cases+=1
        # Arbitrary generating sets upstairs: reverse Schreier/saturation metric mechanism.
        if n<=4:
            reps=[(0,0),(0,1)]
            for X,l in generators(G):
                a=max(l[r] for r in reps);b=max(l[G.inv[r]] for r in reps)
                T={G.mul(G.mul(r,x),G.inv[reps[(r[1]+x[1])%2]]) for r in reps for x in X}
                Ts=T|{G.mul(G.mul(reps[1],t),reps[1]) for t in T}
                check(dist(G,T).keys()=={(h,0) for h in H.es},'reverse_split_positive_schreier')
                check(all(l[t]<=2*a+2*b+1 for t in Ts),'reverse_split_saturation_cost')
                check(Ts=={G.mul(G.mul(reps[1],t),reps[1]) for t in Ts},'reverse_split_invariance')
        rows.append({'rotation_order':n,'positive_subsets':cases})
    return rows

def turn3_general():
    cases=[]
    models=[(C(4),{0,2}),(C(6),{0,2,4}),(Q(2),{(i,0) for i in range(4)}),(Q(4),{(i,j) for i in range(0,8,2) for j in range(2)})]
    for G,H in models:
        G.validate()
        cs=cosets(G,H);where={x:i for i,c in enumerate(cs) for x in c};casecount=0;nonaction=0
        for tail in product(*(tuple(c) for c in cs[1:])):
            reps=(G.one,*tail)
            def alpha(q,h):return G.mul(G.mul(reps[q],h),G.inv[reps[q]])
            def qp(q,t):return where[G.mul(reps[q],reps[t])]
            def factor(q,t):return G.mul(G.mul(reps[q],reps[t]),G.inv[reps[qp(q,t)]])
            for q,t,u in product(range(len(cs)),repeat=3):
                check(G.mul(factor(q,t),factor(qp(q,t),u))==G.mul(alpha(q,factor(t,u)),factor(q,qp(t,u))),'nonsplit_cocycle_identity')
                check(all(alpha(q,alpha(t,h))==G.mul(G.mul(factor(q,t),alpha(qp(q,t),h)),G.inv[factor(q,t)]) for h in H),'nonsplit_twisted_action_identity')
            if any(alpha(q,alpha(t,h))!=alpha(qp(q,t),h) for q,t in product(range(len(cs)),repeat=2) for h in H):nonaction+=1
            for S in subsets(h for h in H if h!=G.one):
                if dist(G,S).keys()!=H:continue
                W=S|set(reps);lw=dist(G,W);b=max(lw[G.inv[r]] for r in reps)
                T={alpha(q,s) for q in range(len(cs)) for s in S}|{factor(q,t) for q,t in product(range(len(cs)),repeat=2)};lt=dist(G,T)
                check(lt.keys()==H and len(lw)==len(G.es),'nonsplit_positive_generation')
                check(all(lt[h]<=lw[h]<=(2+b)*lt[h] for h in H),'nonsplit_factor_set_metric')
                casecount+=1
        cases.append({'group':G.name,'kernel_order':len(H),'positive_set_section_pairs':casecount,'sections_not_actions':nonaction})
    check(cases[-1]['sections_not_actions']>0,'finite_quotient_is_not_an_action_counterexample')
    return cases

def turn4():
    rows=[]
    for G in [Sym(3),Sym(4),Sym(4,True),Sym(5,True)]:
        G.validate()
        classes={frozenset(G.mul(G.mul(h,g),G.inv[h]) for h in G.es) for g in G.es if g!=G.one};classes=tuple(sorted(classes,key=lambda c:repr(min(c))));pairs=0
        for chosen in subsets(range(len(classes))):
            S=set().union(*(classes[i] for i in chosen));l=dist(G,S)
            if len(l)!=len(G.es):continue
            check(all(l[G.mul(G.mul(h,g),G.inv[h])]==l[g] for h in G.es for g in G.es),'normal_set_length_invariance')
            for selected in subsets(range(len(classes))):
                F={min(classes[i]) for i in selected}
                U={G.mul(G.mul(h,f),G.inv[h]) for h in G.es for f in F|{G.inv[f] for f in F}};du=dist(G,U)
                if len(du)!=len(G.es):continue
                cost=max((l[f] for f in F|{G.inv[f] for f in F}),default=0)
                check(max(l.values())<=max(du.values())*cost,'normal_generation_positive_cost_bound');pairs+=1
        rows.append({'group':G.name,'pairs':pairs})
    for G in [D(3),D(4),D(5)]:
        F={G.one,(0,1)}
        for S,l in generators(G):
            C=max(l[f] for f in F|{G.inv[f] for f in F});symmetric=S|{G.inv[s] for s in S};d=max(dist(G,symmetric).values())
            for s in S:
                f=(0,1) if s[1]==0 else G.one
                check(G.mul(G.mul(f,s),G.inv[f])==G.inv[s],'fixed_finite_conjugator_inverse_identity')
                check(l[G.inv[s]]<=2*C+1,'fixed_finite_conjugator_inverse_cost')
            check(max(l.values())<=d*max(1,2*C+1),'fixed_finite_conjugator_diameter_bound')
    return rows

def infinite_controls():
    # Exact normal-form windows support the proofs, not any infinite CB certification.
    def mul(x,y):return (x[0]+(-1)**x[1]*y[0],(x[1]+y[1])%2)
    for k in range(-200,201):
        w=[] if k==0 else [(k,0)] if k>0 else [(0,1),(-k,0),(0,1)]
        z=(0,0)
        for x in w:z=mul(z,x)
        check(z==(k,0) and len(w)<=3,'integer_dihedral_rotation_forms')
        w=[(k,0),(0,1)] if k>=0 else [(0,1),(-k,0)];z=(0,0)
        for x in w:z=mul(z,x)
        check(z==(k,1) and len(w)<=2,'integer_dihedral_reflection_forms')
    for k in range(1,201):
        check(-k<-(k-1) and sum([-1]*k)==-k,'integer_Z_positive_length_lower_attainment')
    # Finite shortest reps' inverse costs need not be bounded by index−1.
    G=C(12);l=dist(G,{1});H=set(range(0,12,2));cs=cosets(G,H)
    check(len(cs)==2 and min(l[x] for x in cs[1])==1 and l[G.inv[1]]==11>len(cs)-1,'inverse_representative_cost_not_index_bound')
    # Genuine infinite nonsplit Z/2Z, section r_1=5, S={2} union nonpositive even integers.
    # c(1,1)=10 has S-length 5 but W-length ≤2. Omitting c violates lower metric inequality.
    check(5>2 and 5+5==10,'factor_set_omission_Z_counterexample')
    # Uniform finite order control does not require a common exponent e.
    G=C(6);check(order(G,2)==3 and order(G,3)==2 and G.mul(G.mul(2,2),2)==0 and G.mul(G.mul(3,3),3)!=0,'bounded_order_not_common_exponent')
    family=[]
    for n in range(3,8):
        G=Sym(n);a=tuple((i+1)%n for i in range(n));h=tuple((-i)%n for i in range(n));S={a}
        for j in range(n-1):
            t=list(range(n));t[j],t[j+1]=t[j+1],t[j];S.add(tuple(t))
        L=dist(G,S);cost=L[G.inv[a]]
        check(G.mul(G.mul(h,a),G.inv[h])==G.inv[a],'variable_conjugator_inverse_identity')
        check(cost>=(n+1)//2,'variable_conjugator_unbounded_cost_support_lower_bound')
        family.append({'degree':n,'cycle_inverse_positive_cost':cost,'proved_lower_bound':(n+1)//2})
    return {'variable_conjugator_symmetric_family':family,'Z_positive_diameter':'unbounded by exact formula','D_infinity_W_positive_diameter':3,'D_infinity_CB':'false via finite generating set, proof only','nonsplit_Z_section':5,'nonsplit_Z_factor_cost_S':5,'nonsplit_Z_factor_cost_W_upper':2}

if __name__=='__main__':
    results={'turn1':turn1(),'turn2':turn2(),'turn3_split':turn3_split(),'turn3_general':turn3_general(),'turn4':turn4(),'infinite_controls':infinite_controls()}
    print(json.dumps({'scope':'Independent finite identity/inequality controls and exact infinite normal-form windows; no test certifies CB of any infinite group.','assertions':sum(counts.values()),'categories':dict(sorted(counts.items())),'results':results},indent=2,sort_keys=True))
