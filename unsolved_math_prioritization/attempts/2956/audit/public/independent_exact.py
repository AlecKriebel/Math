#!/usr/bin/env python3
"""Independent exact checks; RREF subspaces and permutation matrices, no imports from candidate."""
import argparse,itertools,json,math
from collections import Counter
from pathlib import Path


def require(ok,message):
    if not ok:raise AssertionError(message)


def reduce_vector(v,rows):
    for r in rows:
        pivot=(r & -r).bit_length()-1
        if v & (1<<pivot):v^=r
    return v


def rref_spaces(n):
    for k in range(n+1):
        for piv in itertools.combinations(range(n),k):
            available=[(i,j) for i,p in enumerate(piv) for j in range(p+1,n) if j not in piv]
            for mask in range(1<<len(available)):
                rows=[1<<p for p in piv]
                for bit,(i,j) in enumerate(available):
                    if mask&(1<<bit):rows[i]|=1<<j
                yield tuple(rows)


def permute_bits(v,perm):
    return sum(((v>>i)&1)<<j for i,j in enumerate(perm))


def modules():
    answers=[]
    for n in range(2,9):
        inspected=0;invariant=[]
        permutations=[]
        for i in range(n-1):
            p=list(range(n));p[i],p[i+1]=p[i+1],p[i];permutations.append(p)
        for basis in rref_spaces(n):
            inspected+=1
            if reduce_vector((1<<n)-1,basis):continue
            if all(reduce_vector(permute_bits(v,p),basis)==0 for v in basis for p in permutations):invariant.append(basis)
        dims=sorted({len(w) for w in invariant})
        ranks=sorted({n-k for k in dims})
        require(ranks==sorted({0,n-1} if n%2 else {0,1,n-1}),'independent module theorem mismatch')
        # Compute invariant functionals by evaluation on each vector of the diagonal line.
        characters=0
        for coeff in itertools.product((0,1),repeat=n):
            f=lambda v:sum(c*b for c,b in zip(coeff,v))%2
            diag=tuple([1]*n)
            if f(diag):continue
            if all(coeff[i]==coeff[i+1] for i in range(n-1)):characters+=1
        answers.append({'n':n,'all_rref_subspaces_examined':inspected,'invariant_relation_bases':[list(w) for w in invariant],'invariant_relation_space_dimensions':dims,'permitted_twist_group_ranks':ranks,'permutation_invariant_F2_scalar_characters':characters})
    return answers


def permutation_matrix(p):
    r=len(p)-1;columns=[]
    for j in range(r):
        ambient=[0]*(r+1);ambient[p[j]]+=1;ambient[p[j+1]]-=1
        columns.append(tuple(sum(ambient[:i+1]) for i in range(r)))
    return tuple(tuple(columns[j][i] for j in range(r)) for i in range(r))


def matmul(a,b):return tuple(tuple(sum(x*y for x,y in zip(row,col)) for col in zip(*b)) for row in a)


def perm_order(p):
    seen=set();o=1
    for i in range(len(p)):
        if i in seen:continue
        size=0;j=i
        while j not in seen:seen.add(j);size+=1;j=p[j]
        o=math.lcm(o,size)
    return o


def roots():
    out=[]
    for r in range(1,6):
        perms=list(itertools.permutations(range(r+1)));matrices={permutation_matrix(p) for p in perms}
        require(len(matrices)==math.factorial(r+1),'root representation not faithful')
        q=tuple(tuple(-2 if i==j else 1 if abs(i-j)==1 else 0 for j in range(r)) for i in range(r))
        generators=[]
        for j in range(r):
            p=list(range(r+1));p[j],p[j+1]=p[j+1],p[j]
            matrix=permutation_matrix(p);generators.append(matrix)
            predicted=tuple(tuple(int(i==k)+(q[j][k] if i==j else 0) for k in range(r)) for i in range(r))
            require(matrix==predicted,'Picard-Lefschetz reflection mismatch')
        one=permutation_matrix(tuple(range(r+1)))
        for m in matrices:
            require(matmul(matmul(tuple(zip(*m)),q),m)==q,'form preservation mismatch')
        coxeter=one
        for m in generators:coxeter=matmul(coxeter,m)
        pwr=one;order=None
        for k in range(1,r+2):
            pwr=matmul(pwr,coxeter)
            if pwr==one:order=k;break
        require(order==r+1,'Coxeter order mismatch')
        out.append({'rank':r,'negative_cartan_matrix':[list(row) for row in q],'generated_matrix_group_order':len(matrices),'expected_symmetric_group_order':math.factorial(r+1),'coxeter_element_order':order,'identity_matrix_count':sum(m==one for m in matrices),'element_order_histogram':dict(sorted(Counter(perm_order(p) for p in perms).items()))})
    return out


def expected_bf():
    out=[]
    for n in range(2,9):
        cases=[]
        # Formal truncated multiplication: eta has degree one; degree four and above vanish.
        for a in range(1,n):
            b=n-a
            value=lambda k:'eta^3_nonzero_order_2' if (-16*k)%32==16 and 1+a+b<4 else 'zero'
            cases.append({'left_summands':a,'right_summands':b,'spin_choice_left':value(a),'spin_choice_right':value(b)})
        out.append({'summands':n,'neck_cases':cases,'basis':'KM Proposition 5.1 plus connected-sum product and imported eta^4=0'})
    return out


def validate(data,computed):
    require(data['problem_id']==2956,'wrong problem')
    require(data['all_assertions_passed'] is True,'candidate run did not pass')
    require(len(data['permutation_modules'])==7,'module coverage truncated')
    for actual,expect in zip(data['permutation_modules'],computed['modules']):
        for key in actual:require(actual[key]==expect[key],'module field mismatch: '+key)
    require(len(data['A_type_reflection_groups'])==5,'root coverage truncated')
    for actual,expect in zip(data['A_type_reflection_groups'],computed['roots']):
        for key in actual:require(actual[key]==expect[key],'reflection field mismatch: '+key)
    require(data['nonequivariant_BF_arithmetic']==expected_bf(),'BF arithmetic or scope mismatch')
    k3=[{'summands':n,'b2':22*n,'euler_characteristic':24*n-2*(n-1),'signature':-16*n} for n in range(1,9)]
    require(data['K3_sums']==k3,'K3 connected-sum arithmetic mismatch')
    # Explicit map F2^3 -> F2^2 sends e1,e2,e3 to 1,2,3.
    image=lambda v:((v&1) ^ ((v>>2)&1)) | (((((v>>1)&1)^((v>>2)&1)))<<1)
    reps=data['triple_quotient']['representatives'];gens=data['triple_quotient']['neck_generators']
    require(reps==[0,1,2,3] and len({image(v) for v in reps})==4,'wrong quotient representatives')
    require(gens==[1,2,3],'wrong quotient generators')
    table=[[image(a)^image(b) for b in reps] for a in reps]
    require(data['triple_quotient']['addition_table']==table,'wrong quotient addition')


def main():
    p=argparse.ArgumentParser();p.add_argument('--candidate',type=Path,required=True);p.add_argument('--output',type=Path);p.add_argument('--cached',type=Path);args=p.parse_args()
    data=json.loads(args.candidate.read_text())
    computed=json.loads(args.cached.read_text()) if args.cached else {'modules':modules(),'roots':roots()}
    validate(data,computed)
    computed['candidate_all_fields_validated']=True
    computed['limits']='Finite algebra only. Stable-stem relations and geometric formulas are imported; no smooth isotopy decision.'
    result=json.dumps(computed,indent=2,sort_keys=True)+'\n'
    if args.output:args.output.write_text(result)
    else:print(result,end='')

if __name__=='__main__':main()
