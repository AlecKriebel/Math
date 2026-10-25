#!/usr/bin/env python3
"""Independent finite controls for the sealed all-size proof, standard library.

No supplied verification functions are imported. No originals are written.
Tree counts are checked independently by the exact matrix-tree determinant.
"""
from pathlib import Path
from fractions import Fraction
from collections import deque, Counter
import datetime
import hashlib
import itertools
import json
import platform
import sys

HERE = Path(__file__).resolve().parent
COUNTS = Counter()

def check(test, label):
    if not test:
        raise AssertionError(label)
    COUNTS[label] += 1

def normalize(raw):
    raw = tuple(tuple(c) for c in raw)
    for c in raw:
        check(len(c) <= 3 and all(type(x) is int and x != 0 for x in c), 'valid_source_CNF')
    if any(len(c) == 0 for c in raw):
        return 'no', (), ()
    cleaned = tuple(tuple(sorted(set(c))) for c in raw if not any(-x in c for x in c))
    if not cleaned:
        return 'yes', (), ()
    labels = tuple(sorted({abs(x) for c in cleaned for x in c}))
    index = {x:i+1 for i,x in enumerate(labels)}
    return 'ordinary', tuple(tuple(index[abs(x)]*(1 if x>0 else -1) for x in c) for c in cleaned), labels

def build(raw):
    kind, cs, labels = normalize(raw)
    if kind != 'ordinary':
        val = int(kind == 'no')
        return {'kind':kind,'N':2,'E':((0,1),),'c':{(r,a,b):val for r in (0,1) for a,b in ((0,1),(1,0))},'K':val,'clauses':cs,'labels':labels}
    n,m = len(labels),len(cs)
    N=n+m+2
    E={(0,1)}|{(h,i+2) for i in range(n) for h in (0,1)}
    E|={(abs(lit)+1,n+j+2) for j,c in enumerate(cs) for lit in c}
    E=tuple(sorted(E))
    c={(r,a,b):0 for r in range(N) for u,v in E for a,b in ((u,v),(v,u))}
    for u,v in E:
        base=0 if (u,v)==(0,1) else (2 if v>=n+2 else 1)
        c[0,u,v]=c[0,v,u]=base
    for j,clause in enumerate(cs):
        r=n+j+2
        for lit in clause:
            c[r,abs(lit)+1,1 if lit>0 else 0]=1
    return {'kind':kind,'N':N,'E':E,'c':c,'K':n+2*m,'clauses':cs,'labels':labels,'n':n,'m':m}

def adjacency(N,T):
    d=[[] for _ in range(N)]
    for a,b in T:
        d[a].append(b);d[b].append(a)
    return d

def all_trees(N,E):
    for T in itertools.combinations(E,N-1):
        d=adjacency(N,T);seen={0};todo=[0]
        for a in todo:
            for b in d[a]:
                if b not in seen:
                    seen.add(b);todo.append(b)
        if len(seen)==N:
            yield T

def arcs(N,T,r):
    d=adjacency(N,T);seen={r};q=deque([r]);answer=[]
    while q:
        a=q.popleft()
        for b in d[a]:
            if b not in seen:
                answer.append((a,b));seen.add(b);q.append(b)
    check(len(answer)==N-1 and len(seen)==N,'whole_tree_orientation')
    return answer

def root_totals(I,T,transpose=False,inward=False):
    c=I['c'];out=[]
    for r in range(I['N']):
        aa=arcs(I['N'],T,r)
        if inward: aa=[(b,a) for a,b in aa]
        if transpose: aa=[(b,a) for a,b in aa]
        out.append(sum(c[r,a,b] for a,b in aa))
    return out

def cut_totals(I,T):
    N=I['N'];out=[0]*N
    for a,b in T:
        remaining=[e for e in T if e!=(a,b)];d=adjacency(N,remaining)
        side={a};todo=[a]
        for v in todo:
            for w in d[v]:
                if w not in side:side.add(w);todo.append(w)
        check(b not in side,'proper_tree_edge_cut')
        for r in range(N):out[r]+=I['c'][r,a,b] if r in side else I['c'][r,b,a]
    return out

def matrix_tree_count(N,E):
    L=[[Fraction(0) for _ in range(N)] for _ in range(N)]
    for a,b in E:
        L[a][a]+=1;L[b][b]+=1;L[a][b]-=1;L[b][a]-=1
    M=[row[:-1] for row in L[:-1]];det=Fraction(1)
    for k in range(N-1):
        pivot=next((i for i in range(k,N-1) if M[i][k]),None)
        if pivot is None:return 0
        if pivot!=k:M[k],M[pivot]=M[pivot],M[k];det=-det
        v=M[k][k];det*=v
        for i in range(k+1,N-1):
            scale=M[i][k]/v
            for j in range(k,N-1):M[i][j]-=scale*M[k][j]
    check(det.denominator==1,'integral_matrix_tree_count')
    return int(det)

def sat_assignments(cs,n):
    return [a for a in itertools.product((False,True),repeat=n) if all(any(a[abs(x)-1]==(x>0) for x in c) for c in cs)]

def inspect(raw):
    I=build(raw);N,E,K=I['N'],I['E'],I['K'];trees=list(all_trees(N,E));feasible=0;minimum=None;nonstructured=0
    check(len(trees)==matrix_tree_count(N,E),'all_tree_census_equals_matrix_tree_theorem')
    shifted=dict(I,c={key:v+1 for key,v in I['c'].items()},K=K+N*(N-1))
    for T in trees:
        totals=root_totals(I,T);F=sum(totals)
        check(totals==cut_totals(I,T),'BFS_equals_independent_cut_total')
        check(totals==root_totals(I,T,transpose=True,inward=True),'inward_transpose_exact')
        check(root_totals(shifted,T)==[x+N-1 for x in totals],'uniform_shift_each_root')
        check((sum(root_totals(shifted,T))<=shifted['K'])==(F<=K),'uniform_shift_decision')
        minimum=F if minimum is None else min(minimum,F)
        feasible+=int(F<=K)
        if I['kind']!='ordinary':continue
        n,m=I['n'],I['m'];h=int((0,1) in T);q=sum(v>=n+2 for u,v in T);p=len(T)-h-q
        check(q>=m and p+q+h==n+m+1,'edge_partition_and_clause_degree')
        check(totals[0]==p+2*q==K+(1-h)+(q-m),'unrestricted_base_identity')
        structured=h==1 and q==m
        if not structured:
            nonstructured+=1;check(F>=K+1,'every_unstructured_tree_has_strict_gap')
        else:
            assignment=tuple((0,i+2) in T for i in range(n));penalty=0
            for i in range(n):check(((0,i+2) in T)+((1,i+2) in T)==1,'one_hub_attachment')
            for j,C in enumerate(I['clauses']):
                neighbours=[a for a,b in T if b==n+j+2]
                check(len(neighbours)==1,'clause_leaf')
                v=neighbours[0];lit=next(x for x in C if abs(x)+1==v)
                false=int(assignment[abs(lit)-1]!=(lit>0));penalty+=false
                check(totals[n+j+2]==false,'individual_literal_root_identity')
            check(F==K+penalty,'structured_total_identity')
    if I['kind']=='ordinary':
        sats=sat_assignments(I['clauses'],I['n'])
        check(bool(feasible)==bool(sats),'SAT_iff_threshold_tree')
        for assignment in sats:
            T={(0,1)}|{(0 if val else 1,i+2) for i,val in enumerate(assignment)}
            for j,C in enumerate(I['clauses']):
                lit=next(x for x in C if assignment[abs(x)-1]==(x>0));T.add((abs(lit)+1,I['n']+j+2))
            check(tuple(sorted(T)) in trees and sum(root_totals(I,tuple(sorted(T))))==K,'explicit_satisfying_witness')
    else:check(bool(feasible)==(I['kind']=='yes'),'fixed_yes_no_boundary')
    return I,{'raw_formula':[list(c) for c in raw],'N':N,'E_count':len(E),'cost_table_entries':len(I['c']),'tree_count':len(trees),'matrix_tree_count':len(trees),'minimum':minimum,'K':K,'feasible_count':feasible,'unstructured_count':nonstructured}

def structured_tree(I,assignment,selections):
    T={(0,1)}|{(0 if val else 1,i+2) for i,val in enumerate(assignment)}
    T|={(abs(lit)+1,I['n']+j+2) for j,lit in enumerate(selections)}
    return tuple(sorted(T))

def fractional_lift_witness(I,integer_min):
    """Root-specific convex mixtures with the same fractional edge marginals.

    This verifies the manuscript's caution about integral projection versus
    the joint lift; it is not used as the NP-hardness proof.
    """
    N,E=I['N'],I['E'];z={};common_x={e:Fraction(1) if e==(0,1) else Fraction(1,2) for e in E}
    check(sum(common_x.values())==N-1,'lift_total_edge_cardinality')
    for r in range(N):
        ensemble=[]
        if r<4:
            for a in itertools.product((False,True),repeat=2):
                for sel in itertools.product(*I['clauses']):ensemble.append(structured_tree(I,a,sel))
        else:
            j=r-4;C=I['clauses'][j]
            for selected in C:
                selected_var=abs(selected)-1
                # Selected variable satisfies its literal; the other variable
                # falsifies its literal. Switching selection balances both.
                a=tuple((x>0) if abs(x)-1==selected_var else (x<0) for x in sorted(C,key=abs))
                for other in itertools.product(*(I['clauses'][k] for k in range(4) if k!=j)):
                    sel=list(other);sel.insert(j,selected);ensemble.append(structured_tree(I,a,sel))
        weight=Fraction(1,len(ensemble));zr={(a,b):Fraction(0) for u,v in E for a,b in ((u,v),(v,u))}
        xm={e:Fraction(0) for e in E}
        for T in ensemble:
            for e in T:xm[e]+=weight
            for a,b in arcs(N,T,r):zr[a,b]+=weight
        check(xm==common_x,'root_mixture_common_edge_marginals')
        for a,b in E:check(zr[a,b]+zr[b,a]==common_x[a,b],'lift_pair_sum_equals_x')
        for v in range(N):
            incoming=sum(zr.get((u,v),0) for u in range(N))
            check(incoming==(0 if v==r else 1),'lift_root_and_other_indegrees')
        check(all(v>=0 for v in zr.values()),'lift_nonnegative')
        z[r]=zr
    obj=sum(I['c'][r,a,b]*v for r,zr in z.items() for (a,b),v in zr.items())
    check(obj==I['K'] and obj<integer_min,'strict_exact_joint_lift_gap')
    integer_witness=structured_tree(I,(True,True),(1,1,2,-1))
    integer_roots=root_totals(I,integer_witness)
    check(sum(integer_roots)==integer_min,'explicit_integer_minimum_witness')
    artifact={'status':'EXACT_RATIONAL_FEASIBLE_WITNESS','formula':[list(c) for c in I['clauses']],'N':N,'K':I['K'],'integer_all_tree_minimum':integer_min,'explicit_integer_tree':[list(e) for e in integer_witness],'explicit_integer_tree_root_costs':integer_roots,'integer_tree_assignment':[True,True],'integer_tree_selected_literals':[1,1,2,-1],'joint_lift_cost':str(obj),'edge_order':[list(e) for e in E],'x':[str(common_x[e]) for e in E],'arc_order':[list(a) for u,v in E for a in ((u,v),(v,u))],'root_arc_z':[[str(z[r][a]) for u,v in E for a in ((u,v),(v,u))] for r in range(N)],'constraints_verified':['z_r(u,v)+z_r(v,u)=x_uv','root indegree zero','all other indegrees one','z>=0','sum_e x_e=N-1'],'mechanism':'Each root has its own convex mixture of genuine structured-tree orientations, all with the same edge marginals. Each clause-root mixture selects a true literal, while balancing its two variable assignments. This is a counterexample to integrality of the full joint lift, consistent with the integral projection onto x.'}
    (HERE/'EXACT_JOINT_LIFT_WITNESS.json').write_text(json.dumps(artifact,indent=2)+'\n')
    return {'objective':str(obj),'integer_minimum':integer_min,'gap':str(integer_min-obj),'witness_file':'EXACT_JOINT_LIFT_WITNESS.json'}

def main():
    cases=[[],[()],[(1,-1)],[(1,-1),()],[(1,1)],[(10000001,10000001),(-41,),(41,10000001)]]
    choices=[(1,),(-1,),(2,),(-2,),(1,2),(1,-2),(-1,2),(-1,-2)]
    cases += [list(x) for m in (1,2) for x in itertools.combinations_with_replacement(choices,m)]
    cases += [[(1,2,3),(-1,-2,-3)],[(1,),(-2,),(2,3)],[(1,2,3),(-1,-2,-3),(1,-2,3)],[(1,2),(1,-2),(-1,2),(-1,-2)]]
    results=[]
    for cs in cases:
        I,res=inspect(cs);results.append(res)
    unsat=build([(1,2),(1,-2),(-1,2),(-1,-2)])
    last=results[-1];check(last['tree_count']==384 and last['minimum']==11 and last['K']==10,'four_clause_exact_integer_fixture')
    gap=fractional_lift_witness(unsat,last['minimum'])
    one={'N':1,'E':(),'c':{}}
    check(root_totals(one,())==cut_totals(one,())==[0] and list(all_trees(1,()))==[()],'single_vertex_boundary')
    # Essential orientation control and a deliberately corrupted base table.
    single=build([(1,)]);T=structured_tree(single,(False,),(1,))
    outward=root_totals(single,T);wrong_inward=root_totals(single,T,inward=True)
    check(sum(outward)==single['K']+1 and sum(wrong_inward)==single['K'],'untransposed_orientation_changes_instance')
    broken=dict(single,c=dict(single['c']));broken['c'][0,0,1]+=1
    check(root_totals(broken,T)[0]!=single['K'],'corrupt_base_cost_detected')
    symmetric=dict(unsat,c={(r,a,b):(r+1)*(min(a,b)+max(a,b)+1) for r,a,b in unsat['c']})
    for T in all_trees(symmetric['N'],symmetric['E']):
        independent=sum(sum(symmetric['c'][r,a,b] for r in range(symmetric['N'])) for a,b in T)
        check(sum(root_totals(symmetric,T))==independent,'symmetric_root_tables_reduce_to_edge_additive_MST')
    receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_ALL_INDEPENDENT_EXACT_CONTROLS','python':sys.executable,'python_version':platform.python_version(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'formula_cases':len(results),'enumerated_tree_formula_cases':sum(r['tree_count'] for r in results),'checks':dict(sorted(COUNTS.items())),'case_results':results,'joint_lift_gap':gap,'negative_controls':{'wrong_inward_without_transpose':{'outward_root_costs':outward,'inward_same_table_root_costs':wrong_inward,'detected':True},'corrupted_base_cost_detected':True},'finite_checks_prove_NP_hardness':False,'universal_proof':'EARLY_DERIVATION.md','supplied_code_imported':False}
    (HERE/'CHECK_RESULTS.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({k:receipt[k] for k in ['utc','status','formula_cases','enumerated_tree_formula_cases','joint_lift_gap','negative_controls']},indent=2))

if __name__=='__main__':main()
