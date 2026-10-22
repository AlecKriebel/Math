#!/usr/bin/env python3
"""Independent, bounded exact corroboration of the complete recognition proof.

No author program, graph package, numerical solver, or historical receipt is used.
All rejection guards are explicit exceptions and survive optimized Python.
"""
from collections import deque
from fractions import Fraction as F
import copy
import itertools as it
import json
import math


class Rejected(ValueError):
    pass


def need(ok, reason):
    if not ok:
        raise Rejected(reason)


def integer_square(A, nonempty=True):
    need(isinstance(A, (tuple,list)), 'matrix container')
    n=len(A)
    need((n>0 or not nonempty) and all(len(row)==n for row in A), 'square dimension')
    need(all(type(x) is int for row in A for x in row), 'integer entries')
    return n


def determinant(A):
    """Rational Gaussian elimination, independent of the permutation route."""
    n=integer_square(A,False)
    a=[[F(x) for x in row] for row in A]
    out=F(1)
    for col in range(n):
        pivot=next((i for i in range(col,n) if a[i][col]),None)
        if pivot is None:return 0
        if pivot!=col:a[col],a[pivot]=a[pivot],a[col];out=-out
        value=a[col][col];out*=value
        for i in range(col+1,n):
            scale=a[i][col]/value
            for j in range(col+1,n):a[i][j]-=scale*a[col][j]
            a[i][col]=F(0)
    need(out.denominator==1,'integer determinant')
    return out.numerator


def det_permutation(A):
    n=integer_square(A,False)
    return sum((-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))
               *math.prod(A[i][p[i]] for i in range(n)) for p in it.permutations(range(n)))


def transpose(A):return [list(c) for c in zip(*A)]


def product(A,B):
    return [[sum(a*b for a,b in zip(row,col)) for col in zip(*B)] for row in A]


def adjugate(A):
    n=integer_square(A)
    return [[(-1)**(i+j)*det_permutation([row[:i]+row[i+1:]
             for k,row in enumerate(A) if k!=j]) for j in range(n)] for i in range(n)]


def member(v,M):
    n=integer_square(M);d=determinant(M)
    need(d!=0,'nonsingular input')
    need(len(v)==n and all(type(x) is int for x in v),'integer membership vector')
    adj=adjugate(M)
    return all(sum(v[i]*adj[i][j] for i in range(n))%abs(d)==0 for j in range(n))


def multiplier(M,L):
    d=determinant(M);need(d!=0,'nonsingular input')
    p=product(L,adjugate(M))
    need(all(x%d==0 for row in p for x in row),'row lattice membership')
    return [[x//d for x in row] for row in p]


def pair_list(n):return list(it.combinations(range(n+1),2))


def laplacian(n,weights,loops=None):
    need(type(n) is int and n>=0,'nonnegative graph rank')
    pairs=pair_list(n)
    need(len(weights)==len(pairs),'all edge classes')
    need(all(type(w) is int and w>=0 for w in weights),'nonnegative integer weights')
    loops=[0]*(n+1) if loops is None else loops
    need(len(loops)==n+1 and all(type(w) is int and w>=0 for w in loops),'loop weights')
    A=[[0]*(n+1) for _ in range(n+1)]
    for (i,j),w in zip(pairs,weights):A[i][j]=A[j][i]=w
    for i,w in enumerate(loops):A[i][i]=w
    full=[[int(i==j)*sum(A[i])-A[i][j] for j in range(n+1)] for i in range(n+1)]
    reduced=[row[:n] for row in full[:n]]
    return reduced,full


def root_gram(n,weights):
    rows=[[0]*n for _ in range(n)]
    for (i,j),w in zip(pair_list(n),weights):
        e=[int(i==k)-int(j==k) for k in range(n)]
        for a in range(n):
            for b in range(n):rows[a][b]+=w*e[a]*e[b]
    return rows


def connected(n,weights):
    adj=[[] for _ in range(n+1)]
    for (i,j),w in zip(pair_list(n),weights):
        if w:adj[i].append(j);adj[j].append(i)
    seen={n};todo=[n]
    while todo:
        i=todo.pop()
        for j in adj[i]:
            if j not in seen:seen.add(j);todo.append(j)
    return len(seen)==n+1


def prufer_trees(n):
    """Trees on nonsinks0..n-1 and sink n, via bijective Prüfer decoding."""
    if n==0:return [()]
    answer=[]
    for code in it.product(range(n+1),repeat=max(0,n-1)):
        degrees=[1]*(n+1)
        for x in code:degrees[x]+=1
        edges=[]
        for x in code:
            leaf=next(i for i,d in enumerate(degrees) if d==1)
            edges.append(tuple(sorted((leaf,x))))
            degrees[leaf]-=1;degrees[x]-=1
        final=[i for i,d in enumerate(degrees) if d==1]
        need(len(final)==2,'Prüfer terminal pair')
        edges.append(tuple(final));answer.append(tuple(sorted(edges)))
    need(len(set(answer))==len(answer),'Prüfer uniqueness')
    return answer


def graph_checks():
    out=[];diag_larger_than_D=False;checked=0
    for n,maxweight in [(0,3),(1,4),(2,4),(3,3),(4,1)]:
        pairs=pair_list(n);index={p:i for i,p in enumerate(pairs)};trees=prufer_trees(n)
        cases=alive=maxdet=0
        for weights in it.product(range(maxweight+1),repeat=len(pairs)):
            L,full=laplacian(n,weights)
            need(L==root_gram(n,weights),'adjacency versus root Gram')
            d=determinant(L)
            need(d==det_permutation(L),'two determinant methods')
            tau=sum(math.prod(weights[index[e]] for e in T) for T in trees)
            need(d==tau,'Prüfer weighted tree count')
            conn=connected(n,weights);need(conn==(d>0),'connectivity equivalence')
            need(laplacian(n,weights,[i+100 for i in range(n+1)])==(L,full),'loop cancellation')
            need(all(sum(row)==0 for row in full),'full singular row sums')
            need(determinant(full)==0,'full Laplacian singularity')
            for i in range(n):need(full[i]==L[i]+[-sum(L[i])],'fixed full lattice embedding')
            if n:need(full[n]==[-sum(full[i][j] for i in range(n)) for j in range(n+1)],'sink row redundant')
            if conn:
                alive+=1
                need(all(w<=d for w in weights),'tree multiplicity bound')
                need(all(0<L[i][i]<=n*d for i in range(n)),'diagonal nD bound')
                need(all(0<=sum(row)<=d for row in L),'sink-edge bound')
                diag_larger_than_D |= any(L[i][i]>d for i in range(n))
                for pair,w in zip(pairs,weights):
                    if w:need(any(pair in T and all(weights[index[e]] for e in T) for T in trees),'edge extends to tree')
            cases+=1;maxdet=max(maxdet,d)
        checked+=cases
        out.append({'n':n,'weight_max':maxweight,'assignments':cases,'connected':alive,'maxdet':maxdet,'simple_complete_trees':len(trees)})
    need(diag_larger_than_D,'negative control: diagonal bound D is false')
    return {'families':out,'assignments':checked,'diagonal_can_exceed_D':True}


def egcd(a,b):
    if b==0:return abs(a),1 if a>=0 else -1,0
    g,x,y=egcd(b,a%b)
    return g,y,x-(a//b)*y


def hnf2(M):
    need(len(M)==2 and determinant(M)!=0,'rank two HNF')
    (x,y),(z,t)=M
    k,u,v=egcd(y,t);need(k>0,'nonzero y projection')
    D=abs(determinant(M));need(D%k==0,'HNF index divisor')
    h=D//k;r=(u*x+v*z)%h
    H=[[h,0],[r,k]]
    need(all(member(row,H) for row in M),'derived HNF includes original rows')
    need(all(member(row,M) for row in H),'original includes derived HNF rows')
    return h,r,k


def hmember(v,H):
    h,r,k=H;x,y=v
    return y%k==0 and (x-(y//k)*r)%h==0


def triple_member(a,b,c,H):
    h,r,k=H
    return c%k==0 and b%k==0 and (a+c+(c//k)*r)%h==0 and (c+((b+c)//k)*r)%h==0


def triples_cube(D,cap=None):
    return {(a,b,c) for a,b,c in it.product(range((D if cap is None else cap)+1),repeat=3) if a*b+a*c+b*c==D}


def triples_division(D):
    out=set()
    for a,b in it.product(range(D+1),repeat=2):
        if a+b and D>=a*b and (D-a*b)%(a+b)==0:
            c=(D-a*b)//(a+b)
            if 0<=c<=D:out.add((a,b,c))
    return out


def triple_L(a,b,c):return [[a+c,-c],[-c,b+c]]


def residue_subgroup(M,D):
    n=len(M);zero=(0,)*n;seen={zero};todo=deque([zero])
    while todo:
        x=todo.popleft()
        for row in M:
            y=tuple((a+b)%D for a,b in zip(x,row))
            if y not in seen:seen.add(y);todo.append(y)
    return seen


TABLE=[(1,0,1,(0,1,1)),(1,0,2,(1,0,2)),(2,0,1,(0,1,2)),(2,1,1,(0,2,1)),
       (1,0,3,(1,0,3)),(3,0,1,(0,1,3)),(3,1,1,(1,1,1)),(3,2,1,(0,3,1)),
       (1,0,4,(1,0,4)),(2,0,2,(0,2,2)),(2,1,2,None),(4,0,1,(0,1,4)),
       (4,1,1,None),(4,2,1,None),(4,3,1,(0,4,1))]


def rank_two_checks():
    out=[];lattices=membership_checks=triple_checks=0
    results={}
    for D in range(1,25):
        triples=triples_cube(D);need(triples==triples_division(D),'independent triple enumerations')
        if D<=12:need(triples==triples_cube(D,2*D),'no additional solutions beyond D')
        from_graphs={hnf2(triple_L(*t)) for t in triples}
        count=positive=0
        for h in range(1,D+1):
            if D%h:continue
            k=D//h
            for r in range(h):
                H=(h,r,k);M=[[h,0],[r,k]];sg=residue_subgroup(M,D)
                need(len(sg)*D==D*D,'index in finite quotient')
                for v in it.product(range(D),repeat=2):
                    x=hmember(v,H);need(x==member(v,M)==(v in sg),'three membership routes')
                    membership_checks+=1
                actual={t for t in triples if all(member(row,M) for row in triple_L(*t))}
                for t in triples:
                    need((t in actual)==triple_member(*t,H),'expanded rank two congruences');triple_checks+=1
                need(bool(actual)==(H in from_graphs),'membership versus independently derived HNF')
                results[H]=actual;positive+=bool(actual);count+=1;lattices+=1
        out.append({'D':D,'normal_forms':count,'graphical':positive,'weight_triples':len(triples)})
    for h,r,k,w in TABLE:
        witnesses=results[(h,r,k)]
        need((w is None and not witnesses) or w in witnesses,'all fifteen displayed rows')
    expected4=set(it.permutations((0,1,4)))|set(it.permutations((0,2,2)))
    need(len(expected4)==9 and triples_cube(4)==expected4,'nine complete index-four triples')
    need(all(results[H] for H in results if H[0]*H[2]<=3),'all smaller rank two indices positive')
    # Direct obstruction congruences checked on residues, independently of any cap on weights.
    for H in [(2,1,2),(4,1,1),(4,2,1)]:
        for a,b,c in it.product(range(8),repeat=3):
            both=all(hmember(row,H) for row in triple_L(a,b,c))
            if H==(2,1,2):formula=c%2==0 and (2*a+3*c)%4==0 and (b+3*c)%4==0
            elif H==(4,1,1):formula=(a+2*c)%4==0 and (b+2*c)%4==0
            else:formula=(a-c)%4==0 and (2*b+3*c)%4==0
            need(formula==both,'all direct obstruction congruences')
            if both and a*b+a*c+b*c:need(a*b+a*c+b*c>=8,'direct positive determinant minimum')
    return {'range':[1,24],'normal_forms':lattices,'residue_membership_comparisons':membership_checks,
            'triple_congruence_comparisons':triple_checks,'displayed_rows':15,'index_four_triples':9,'counts':out}


def validate_certificate(M,weights,L=None,U=None):
    n=integer_square(M);d=determinant(M);need(d!=0,'nonsingular input')
    D=abs(d);actual,_=laplacian(n,weights)
    need(all(w<=D for w in weights),'edge multiplicity cap')
    L=actual if L is None else L
    integer_square(L)
    need(L==actual,'matrix matches graph weights')
    need(determinant(L)==D,'determinant equals lattice index')
    R=multiplier(M,L)
    need(abs(determinant(R))==1,'left multiplier unimodular')
    need(product(R,M)==L,'left multiplier identity')
    if U is not None:
        integer_square(U);need(abs(determinant(U))==1,'provided multiplier unimodular')
        need(product(U,M)==L,'provided multiplier identity')
    return R


def recognize(M):
    n=integer_square(M);d=determinant(M);need(d!=0,'nonsingular input')
    D=abs(d)
    for weights in it.product(range(D+1),repeat=n*(n+1)//2):
        L,_=laplacian(n,weights)
        if determinant(L)==D and all(member(row,M) for row in L):
            U=validate_certificate(M,weights,L)
            return {'weights':weights,'L':L,'U':U}
    return None


def semantic_checks():
    bad=[[2,0],[1,2]];good=[[1,0],[0,4]]
    need(recognize(bad) is None and recognize(good) is not None,'same Smith differing graphicality')
    need(math.gcd(*sum(bad,[]))==math.gcd(*sum(good,[]))==1 and determinant(bad)==determinant(good)==4,'Smith factors (1,4)')
    need(member((1,2),bad) and not member((1,2),transpose(bad)),'row-column distinction')
    nonsymmetric=[[1,4],[2,4]]
    need(hnf2(nonsymmetric)==(1,0,4) and hnf2(transpose(nonsymmetric))==(2,1,2),
         'transpose changes the embedded lattice')
    need(recognize(nonsymmetric) is not None and recognize(transpose(nonsymmetric)) is None,
         'wrong input transpose changes recognition answer')
    right=[[1,2],[0,-1]];changed=product(bad,right)
    need(determinant(right)==-1 and hnf2(changed)==(1,0,4),'ambient right operation changes answer')
    need(recognize(changed) is not None,'ambient right operation is material')
    strict=[[4,0],[0,4]]
    need(all(member(row,bad) for row in strict) and determinant(strict)==16,'row inclusion alone insufficient')
    wrong=triple_L(1,0,4)
    need(determinant(wrong)==4 and not all(member(row,bad) for row in wrong),'equal determinant alone insufficient')
    basis_changes=[[[1,0],[0,1]],[[0,1],[1,0]],[[-1,0],[0,1]],[[1,7],[0,1]],[[2,1],[1,1]],[[1,0],[-9,1]]]
    for S in basis_changes:
        need(abs(determinant(S))==1,'test basis unimodular')
        for M in [bad,good]:
            changed=product(S,M)
            need((recognize(changed) is not None)==(M==good),'left basis operation invariance')
    for D in range(1,21):
        result=recognize([[-D]])
        need(result is not None and result['weights']==(D,) and result['U']==[[-1]],'rank one negative orientation')
    # Additional higher-rank actual recognition; all are known weighted-star lattices.
    high=[]
    for diagonal in [(1,1,1),(2,1,1),(1,1,1,1),(1,1,1,1,1)]:
        n=len(diagonal);M=[[int(i==j)*diagonal[i] for j in range(n)] for i in range(n)]
        answer=recognize(M);need(answer is not None,'higher rank star recognition')
        high.append({'n':n,'D':abs(determinant(M)),'witness':answer})
    need(determinant([])==1 and connected(0,()) and laplacian(0,())[0]==[], 'natural rank zero extension')
    return {'basis_changes_per_lattice':len(basis_changes),'rank_one_negative_inputs':20,
            'same_Smith_pair':True,'transpose_answer_counterexample':nonsymmetric,
            'ambient_change_counterexample':right,'higher_rank_recognition':high,
            'rank_zero':'excluded by theorem n>=1; natural empty convention checked'}


def general_membership_checks():
    matrices=[[[2,0,0],[1,1,0],[1,0,3]],[[1,3,2],[0,2,1],[0,0,1]],
              [[0,0,-3],[1,0,2],[0,1,1]],
              [[1,2,0,0],[0,1,1,0],[0,0,1,2],[0,0,0,2]]]
    count=0;receipts=[]
    for M in matrices:
        n=len(M);d=determinant(M);D=abs(d);adj=adjugate(M)
        identity=[[int(i==j)*d for j in range(n)] for i in range(n)]
        need(product(M,adj)==identity==product(adj,M),'both adjugate identities')
        subgroup=residue_subgroup(M,D)
        need(len(subgroup)*D==D**n,'higher rank residue index')
        for v in it.product(range(D),repeat=n):
            expected=v in subgroup
            need(member(v,M)==expected,'higher rank adjugate versus residue membership')
            translated=tuple(a-D for a in v)
            need(member(translated,M)==expected,'signed membership residues')
            count+=2
        receipts.append({'n':n,'det':d,'subgroup_size':len(subgroup)})
    return {'cases':receipts,'membership_comparisons':count}


def corruption_checks():
    M=[[1,0],[0,4]];weights=(4,1,0);L,_=laplacian(2,weights);U=validate_certificate(M,weights)
    results=[]
    def reject(name,call):
        try:call()
        except Rejected as e:results.append({'name':name,'rejected':True,'reason':str(e)})
        else:raise Rejected('corruption survived: '+name)
    reject('negative_weight',lambda:validate_certificate(M,(-1,1,0)))
    reject('fractional_weight',lambda:validate_certificate(M,(F(1,2),1,0)))
    reject('weight_above_D',lambda:validate_certificate(M,(5,1,0)))
    reject('missing_edge_class',lambda:validate_certificate(M,(4,1)))
    reject('disconnected_support',lambda:validate_certificate(M,(4,0,0)))
    reject('wrong_equal_index',lambda:validate_certificate(M,(4,4,4)))
    reject('changed_lattice_same_det',lambda:validate_certificate([[2,0],[1,2]],weights))
    reject('wrong_matrix_entry',lambda:validate_certificate(M,weights,[[6,-4],[-4,4]]))
    reject('right_multiplier_in_place_of_left',lambda:validate_certificate(M,weights,U=[[x//4 for x in row] for row in product(adjugate(M),L)]))
    reject('wrong_unimodular_certificate',lambda:validate_certificate(M,weights,U=[[1,0],[0,1]]))
    reject('singular_input',lambda:validate_certificate([[1,1],[1,1]],weights))
    reject('fractional_input',lambda:validate_certificate([[F(1,2),0],[0,4]],weights))
    # Explicitly test a valid but noncommuting negative-determinant input.
    signM=[[0,4],[1,0]]
    need(determinant(signM)<0,'negative determinant test fixture')
    validate_certificate(signM,weights)
    return results


def main():
    result={'schema':'fresh-exact-undirected-lattice-review-1','arithmetic':'integers and exact fractions',
            'guard_style':'explicit exceptions','author_code_executed':False,'source_code_executed':False,
            'solver_used':False,'graph_checks':graph_checks(),'rank_two':rank_two_checks(),
            'semantics':semantic_checks(),'general_membership':general_membership_checks(),
            'negative_controls':corruption_checks()}
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':main()
