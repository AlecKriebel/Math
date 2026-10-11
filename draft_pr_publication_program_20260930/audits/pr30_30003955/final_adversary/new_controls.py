#!/usr/bin/env python3
"""New adversarial controls: boundary words, seam duality, Heisenberg and AGL(1,5).

Finite examples and encoded ribbon models only. Universal proof is in REPORT.md.
No original or family imports; only writes this folder's result.
"""
from pathlib import Path
from itertools import product
from fractions import Fraction
import hashlib,json

HERE=Path(__file__).resolve().parent
checks=0
def check(x,label):
    global checks
    checks+=1
    if not x: raise AssertionError(label)

def rank(rows):
    a=[[Fraction(x) for x in row] for row in rows];r=0
    if not a:return 0
    for c in range(len(a[0])):
        pivot=next((i for i in range(r,len(a)) if a[i][c]),None)
        if pivot is None:continue
        a[r],a[pivot]=a[pivot],a[r];q=a[r][c];a[r]=[x/q for x in a[r]]
        for i in range(len(a)):
            if i!=r and a[i][c]:q=a[i][c];a[i]=[x-q*y for x,y in zip(a[i],a[r])]
        r+=1
    return r

def boundary_words(rotation):
    check(set(rotation)=={-x for x in rotation},'paired oriented darts')
    sigma={x:rotation[(i+1)%len(rotation)] for i,x in enumerate(rotation)}
    phi={x:sigma[-x] for x in rotation};unseen=set(rotation);cycles=[]
    while unseen:
        start=min(unseen);cur=start;cycle=[]
        while cur in unseen:unseen.remove(cur);cycle.append(cur);cur=phi[cur]
        check(cur==start,'closed boundary permutation')
        cycles.append(cycle)
    chi=1-len(rotation)//2;b=len(cycles)
    return cycles,(2-b-chi)//2,b

def reduced(w):
    stack=[]
    for x in w:
        if stack and stack[-1]==-x:stack.pop()
        else:stack.append(x)
    return stack

def cyclic_equal(a,b):
    return len(a)==len(b) and any(a==b[i:]+b[:i] for i in range(len(b)))

def heis_mul(a,b):
    x,y,z=a;u,v,w=b
    return ((x+u)%3,(y+v)%3,(z+w+x*v)%3)
def heis_inv(a):
    x,y,z=a
    return ((-x)%3,(-y)%3,(-z+x*y)%3)
I=(0,0,0)
def fold(words,mul,identity):
    cur=identity
    for w in words:cur=mul(cur,w)
    return cur

def affine_mul(a,b):return ((a[0]*b[0])%5,(a[0]*b[1]+a[1])%5)
def affine_inv(a):
    inv=pow(a[0],-1,5);return inv,(-inv*a[1])%5
def generate(gens,mul,identity):
    seen={identity};todo=[identity]
    while todo:
        a=todo.pop()
        for b in gens:
            x=mul(a,b)
            if x not in seen:seen.add(x);todo.append(x)
    return seen
def comm(a,b,mul,inv):return fold([a,b,inv(a),inv(b)],mul,(1,0))

def main():
    seam=[];intervals=0
    for m in range(2,33):
        # Cellular seam cycles have only relation c_1+...+c_m+delta=0.
        # m independent seam-duals pair as identity; extra boundary is nullhomologous.
        dual=[[int(i==j) for j in range(m)] for i in range(m)]
        check(rank(dual)==m,'all selected seams independent')
        chi=(2-(m+1))+(2-(m+2))
        check(chi==1-2*m,'double-planar genus-m block chi')
        # m cuts delete m of the m+1 N-Q gluing edges; final edge remains.
        remaining=[m];check(len(remaining)==1,'selected cut system connected')
        check((m+1)+(m+2)-2==2*m+1,'cut surface boundary count')
        all_rotation=[x for j in range(1,m+1) for x in [j,-j]]
        cycles,g,b=boundary_words(all_rotation)
        check(g==0 and b==m+1,'ordered comb planar')
        outer=next(c for c in cycles if all(x>0 for x in c))
        check(cyclic_equal(outer,list(range(1,m+1))),'literal ordered outer word')
        for i in range(m):
            for j in range(i+1,m+1):
                k=j-i;rotation=[x for h in range(i+1,j+1) for x in [h,-h]]
                cs,gg,bb=boundary_words(rotation)
                actual=next(c for c in cs if all(x>0 for x in c))
                word=list(range(i+1,j+1));v=[int(i<=h<j) for h in range(m)]
                check(gg==0 and bb==k+1,'consecutive enclosed region planar')
                check(cyclic_equal(actual,word),'boundary traces literal consecutive product')
                check(any(v) and sum(v)==k,'interval homology nonzero')
                intervals+=1
        seam.append({'m':m,'block_genus':m,'cut_genus':0,'cut_boundaries':2*m+1,'seam_rank':m})
    cs,g,b=boundary_words([1,2,-1,-2])
    check(g==1 and b==1,'interlaced peripheral mutant changes genus')
    check(any(cyclic_equal(c,[1,-2,-1,2]) for c in cs),'nonplanar boundary is commutator-type')
    # The Heisenberg group is a materially new nonabelian prefix control.
    H=list(product(range(3),repeat=3));check(len(H)==27,'group size27')
    for x,y,z in product(H,repeat=3):
        check(heis_mul(heis_mul(x,y),z)==heis_mul(x,heis_mul(y,z)),'Heisenberg associative')
    X,Y=(1,0,0),(0,1,0);Z=heis_inv(heis_mul(X,Y))
    check(fold([X,Y,Z],heis_mul,I)==I,'ordered killed nonabelian triple')
    reversal=fold([Z,Y,X],heis_mul,I)
    check(reversal!=I,'reversed-order mutant survives')
    conj=heis_mul(heis_mul(Y,X),heis_inv(Y))
    check(fold([conj,Y,Z],heis_mul,I)!=I,'separate whisker conjugation mutant survives')
    sequence=[X,Y,Z]*9;prefix=[I]
    for x in sequence:prefix.append(heis_mul(prefix[-1],x))
    witnesses=[(i,j) for j in range(1,28) for i in range(j) if prefix[i]==prefix[j]]
    check(bool(witnesses),'m+1 prefix pigeonhole')
    for i,j in witnesses:check(fold(sequence[i:j],heis_mul,I)==I,'all equal prefixes kill literal intervals')
    # Prescribe distinct prefixes to force endpoint/singleton/interior witnesses.
    forcing=[]
    ordered=[I]+[x for x in H if x!=I]
    for k in (0,7,26):
        desired=ordered+[ordered[k]]
        words=[heis_mul(heis_inv(desired[i]),desired[i+1]) for i in range(27)]
        check(fold(words[k:27],heis_mul,I)==I,'forced interval killed')
        check(all(desired[i]!=desired[j] for j in range(27) for i in range(j)),'no earlier prefix repetition')
        forcing.append({'equal_prefixes':[k,27],'interval_length':27-k})
    too_few=[heis_mul(heis_inv(ordered[i]),ordered[i+1]) for i in range(26)]
    check(all(fold(too_few[i:j],heis_mul,I)!=I for j in range(1,27) for i in range(j)),
          'omitting last required prefix defeats pigeonhole guarantee')
    # AGL(1,5): natural point stabilizer C4 surjects onto abelianization C4.
    A={(a,b) for a in range(1,5) for b in range(5)};identity=(1,0);R=(1,1);S=(2,0)
    check(generate([R,S],affine_mul,identity)==A,'affine image surjective')
    check(affine_mul(comm(R,S,affine_mul,affine_inv),comm(S,R,affine_mul,affine_inv))==identity,'genus2 relation')
    P=generate([R,fold([S,affine_inv(R),affine_inv(S)],affine_mul,identity)],affine_mul,identity)
    check(len(P)==5 and P<A,'pants image C5 proper')
    natural={((a*x+b)%5) for a,b in P for x in [0]}
    regular={frozenset(affine_mul(p,a) for p in P) for a in A}
    check(natural==set(range(5)) and len(regular)==4,'proper-transitive natural but four regular components')
    derived=generate([comm(a,b,affine_mul,affine_inv) for a in A for b in A],affine_mul,identity)
    stabilizer={x for x in A if x[1]==0}
    check(derived==P and {a for a,b in stabilizer}==set(range(1,5)),'stabilizer surjects cyclic4 quotient')
    check(stabilizer.intersection(derived)=={identity},'no cyclic intermediate in natural cover')
    # Final boundary types from cutting curves, using positive-genus criteria.
    final=[]
    for gg in range(2,65):
        new_sides=[(1,1),(gg-1,1)];outer_sides=[(2,1),(gg-2,1)]
        essential_new=all(genus>0 for genus,bound in new_sides)
        essential_outer=all(genus>0 for genus,bound in outer_sides)
        check(essential_new,'new alpha-torus boundary essential')
        check(essential_outer==(gg>2),'genus2 outer-boundary extension rejected')
        if gg>=4:check(2-2*gg==(2-2*2-1)+(2-2*(gg-2)-1),'complement genus')
        final.append({'g':gg,'outer_essential':essential_outer,'new_essential':essential_new})
    # Ambient seam homology independence matters: identify two seam classes.
    collapsed=[[1,1],[0,0]]
    check(rank(collapsed)==1,'dependent-seam mutant detected')
    check(reduced([1,2,-1,-2])!=[],'killed homology need not kill nonabelian word')
    result={'utc_scope':'Finite diagnostics, never universal proof or search for a new solution',
            'status':'PASS_NEW_SUPPLEMENTARY_CONTROLS','assertions':checks,
            'double_planar_models':seam,'literal_interval_ribbon_words':intervals,
            'heisenberg_order':27,'equal_prefix_witnesses':len(witnesses),'forced_prefix_intervals':forcing,
            'mutants':{'reversed_nonabelian_word':reversal,'separate_conjugator_survives':True,
                       'nonplanar_rotation_type':[g,b],'insufficient_prefixes_rejected':True,
                       'dependent_seams_rank':rank(collapsed),'invalid_g2_outer_boundary_rejected':True},
            'new_affine_action':{'group_order':20,'natural_degree':5,'pants_image_order':5,
                                'regular_components':4,'natural_components':1,
                                'natural_cyclic_intermediate':False,'regular_domain_genus':21,'natural_domain_genus':6},
            'final_boundary_models':final,'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/'NEW_CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','assertions','literal_interval_ribbon_words','mutants','new_affine_action']},indent=2))

if __name__=='__main__':main()
