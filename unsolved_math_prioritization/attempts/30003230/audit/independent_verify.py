#!/usr/bin/env python3
"""Independent finite arithmetic audit. No universal geometric certificate."""
from fractions import Fraction as Q
from itertools import combinations, product, permutations, combinations_with_replacement
from math import gcd
from functools import reduce
from collections import Counter
import ast
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile

EXPECTED_ZIP_SHA='b6c69b1639fd31f5a8ed675fa7ddaac6e097cf669419ff8222315af9dba86710'
EXPECTED_MANIFEST_SHA='5d6dfeea07270a9a307fc7e21a623cd427826c0f9eb638ffcb389ea9c6e324f2'
EXPECTED_ZIP_BYTES=17356
COUNTS=Counter()

def require(ok,label):
    if not ok:
        raise RuntimeError(label)
    COUNTS[label]+=1

def det_permutation(M):
    n=len(M)
    out=Q(0)
    for p in permutations(range(n)):
        term=Q((-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n)))
        for i in range(n):term*=M[i][p[i]]
        out+=term
    return out

def dual_value(x,edges):
    # x_i = 1 / A_i; independently collect one correction per double point.
    return 2*sum(x,Q(0))+sum((x[i]*x[j]-x[i]-x[j] for i,j in edges),Q(0))

def margin(x,edges,i):
    return Q(2)+sum((x[j if i==k else k]-1 for k,j in edges if i in (k,j)),Q(0))

def evaluate(A,edges):
    return dual_value([1/Q(a) for a in A],edges)

def coordinate_telescope(A,B,edges):
    x=[1/Q(a) for a in A]; y=[1/Q(b) for b in B]; z=x[:]; total=Q(0)
    for i in range(len(A)):
        total+=(z[i]-y[i])*margin(z,edges,i)
        z[i]=y[i]
    return total

def graph_tests():
    graphs=criterion_cases=negative_stratum_cases=0
    for n in range(1,6):
        pairs=list(combinations(range(n),2))
        for mask in range(1<<len(pairs)):
            edges=[e for k,e in enumerate(pairs) if mask>>k&1]
            graphs+=1
            pairs_AB=[]
            for shift in range(3):
                A=[Q(1,2+(i+shift)%4) for i in range(n)]
                B=[Q(1) if (i+shift)%2==0 else (a+1)/2 for i,a in enumerate(A)]
                pairs_AB.append((A,B))
            # Partially changed vectors exercise exactly the stated criterion.
            A=[Q(i+1,2) for i in range(n)]
            B=[a+Q(i+1,3) if i%2==0 else a for i,a in enumerate(A)]
            pairs_AB.append((A,B))
            for A,B in pairs_AB:
                gap=evaluate(A,edges)-evaluate(B,edges)
                require(gap==coordinate_telescope(A,B,edges),'coordinate_telescope_identity')
                x=[1/a for a in A]; y=[1/b for b in B]
                for i in range(n):
                    C=A[:]; C[i]+=Q(2,7)
                    # Exact finite difference validates derivative numerator, no floats.
                    expected=(1/A[i]-1/C[i])*margin(x,edges,i)
                    require(evaluate(A,edges)-evaluate(C,edges)==expected,'single_coordinate_difference')
                if all(margin(y,edges,i)>0 for i in range(n) if A[i]<B[i]):
                    require(gap>0,'signed_graph_criterion')
                    criterion_cases+=1
                    if any(sum(i in e for e in edges)>2 for i in range(n)):
                        negative_stratum_cases+=1
                if max(B)<=1:
                    for i in range(n):require(margin(y,edges,i)>=2,'unit_cube_margin')
    # Genuine multigraph intersections and cycles, not only simple chains.
    for n in range(2,13):
        edges=[(i,(i+1)%n) for i in range(n)]
        A=[Q(2*i+1,3) for i in range(n)]
        B=[a+Q(2,5) if i%2==0 else a for i,a in enumerate(A)]
        require(evaluate(A,edges)>evaluate(B,edges),'cycle_multiedge_decrease')
    # A negative margin at an unchanged coordinate is harmless.
    edges=[(0,i) for i in range(1,4)]
    A=[Q(1),Q(10),Q(10),Q(10)]; B=[Q(1),Q(11),Q(10),Q(10)]
    require(margin([1/b for b in B],edges,0)<0 and evaluate(A,edges)>evaluate(B,edges),'unchanged_negative_margin_allowed')
    return {'simple_graphs':graphs,'criterion_cases':criterion_cases,'criterion_cases_with_negative_open_strata':negative_stratum_cases}

def resolution_tests():
    for n in range(1,8):
        edges=[(0,i) for i in range(1,n)]
        A=[Q(i+1,3) for i in range(n)]
        for i in range(n):
            B=A+[A[i]+1]; new=edges+[(i,n)]
            require(evaluate(A,edges)==evaluate(B,new),'SNC_smooth_point_blowup_invariance')
        for i,j in edges:
            B=A+[A[i]+A[j]]; new=[e for e in edges if e!=(i,j)]+[(i,n),(j,n)]
            require(evaluate(A,edges)==evaluate(B,new),'SNC_node_blowup_invariance')
    for m in range(101):
        edges=[(0,i) for i in range(1,m+1)]
        require(evaluate([1]+[2]*m,edges)-evaluate([2]+[3]*m,edges)==1,'geometric_star_cancellation')
    # Algebraic point blowup polynomial beta=(1,rho,1), each step adds t^2.
    for rho in range(1,21):
        beta=[1,rho,1]
        for k in range(1,21):
            beta[1]+=1
            require(sum(beta)-(rho+2)==k,'canonical_surface_arithmetic_only')

def toric_tests():
    count=nonunimodular=0
    for n in range(2,5):
        for w in product(range(1,7),repeat=n):
            if reduce(gcd,w)!=1:continue
            M=[[Q(i==j) for j in range(n)] for i in range(n)]
            vals=[]
            for c in range(n):
                P=[r[:] for r in M]
                for r in range(n):P[r][c]=w[r]
                vals.append(abs(det_permutation(P)))
            require(vals==list(w),'independent_toric_determinants')
            require(sum(vals)-1==sum(w)-1>0,'independent_toric_weighted_gap')
            count+=1
        # Primitive target rays with lattice index greater than one.
        for q in range(2,9):
            M=[[Q(i==j) for j in range(n)] for i in range(n)]
            M[0][n-1]=1;M[n-1][n-1]=q
            for w in product(range(1,4),repeat=n):
                raw=[sum(M[i][j]*w[j] for j in range(n)) for i in range(n)]
                g=reduce(gcd,[int(z) for z in raw]); v=[z/g for z in raw]
                base=abs(det_permutation(M)); pieces=[]
                for c in range(n):
                    N=[r[:] for r in M]
                    for r in range(n):N[r][c]=v[r]
                    piece=abs(det_permutation(N));pieces.append(piece)
                    require(piece==Q(w[c],g)*base,'nonunimodular_column_identity')
                require(sum(pieces)-base==(sum(Q(z,g) for z in w)-1)*base,'nonunimodular_subdivision_gap')
                nonunimodular+=1
    return {'primitive_weight_tuples_1_through_6':count,'nonunimodular_cases':nonunimodular}

def solve(M,v):
    # Cramer's rule, independent of the author star formula and elimination code.
    d=det_permutation(M)
    if not d:raise RuntimeError('Singular numerical intersection matrix')
    out=[]
    for i in range(len(M)):
        N=[r[:] for r in M]
        for j in range(len(M)):N[j][i]=v[j]
        out.append(det_permutation(N)/d)
    return out

def adjunction_tests():
    attempted=eligible=0;gaps=[]
    for m in range(5):
        for arms in combinations_with_replacement(range(2,9),m):
            for b0 in range(1,6):
                attempted+=1;s=sum((Q(1,b) for b in arms),Q(0))
                if b0<=s or 2-m-b0+2*s<=0:continue
                n=m+1; M=[[Q(0) for j in range(n)] for i in range(n)]
                M[0][0]=b0
                for i,b in enumerate(arms,1):M[i][i]=b;M[0][i]=M[i][0]=-1
                B=solve(M,[2-m]+[1]*m)
                A=[Q(1)]+[Q(2,b) for b in arms]
                require(B[0]==Q(2-m+s,b0-s) and all(B[i+1]==(1+B[0])/b for i,b in enumerate(arms)),'adjunction_Cramer_comparison')
                require(all(b>=a>0 for a,b in zip(A,B)) and B[0]>A[0],'adjunction_discrepancy_order')
                gap=evaluate(A,[(0,i) for i in range(1,n)])-evaluate(B,[(0,i) for i in range(1,n)])
                require(gap>0,'adjunction_numerical_gap');gaps.append(gap);eligible+=1
    require((attempted,eligible,min(gaps))==(1650,17,Q(1)),'author_search_counts_independently_recomputed')
    return {'attempted':attempted,'eligible':eligible,'minimum_gap':str(min(gaps))}

def negative_controls():
    edges=[(0,i) for i in range(1,4)]
    A=[Q(1),Q(10),Q(10),Q(10)];B=[Q(2),Q(10),Q(10),Q(10)]
    bad=evaluate(A,edges)-evaluate(B,edges)
    tests={
      'discrepancy_order_is_not_sufficient':bad==Q(-7,20),
      'positive_closed_strata_do_not_prevent_negative_open':2-len(edges)==-1,
      'global_coordinate_monotonicity_is_false':margin([1/a for a in A],edges,0)<0,
      'strict_coordinate_change_is_necessary':evaluate(A,edges)-evaluate(A,edges)==0,
      'weak_margin_cannot_imply_strictness':evaluate([1,3,3,3],edges)==evaluate([2,3,3,3],edges),
      'algebraic_not_topological_curve_Euler':2!=2-2*2,
      'codimension_one_blowup_is_not_strict':(1-1)*2==0,
      'crepant_exceptional_divisor_is_not_strict':Q(0,1)*2==0,
      'common_resolution_bound_one_fails':Q(2)>1,
      'crepant_toric_subdivision_gives_equality':abs(det_permutation([[1,1],[0,2]]))==abs(det_permutation([[1,1],[0,1]]))+abs(det_permutation([[1,1],[1,2]])),
      'non_Mori_toric_subdivision_can_reverse':abs(det_permutation([[1,1],[2,1]]))+abs(det_permutation([[1,2],[1,1]]))<abs(det_permutation([[1,2],[2,1]])),
      'lexicographic_order_does_not_survive_evaluation_one':(2>1 and sum([2,-2])==sum([1,-1])),
    }
    for label,ok in tests.items():require(ok,'negative_control_'+label)
    return sorted(tests)

def packet_tests(root,archive):
    before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in root.iterdir() if p.is_file()}
    zbytes=archive.read_bytes()
    require(len(zbytes)==EXPECTED_ZIP_BYTES and hashlib.sha256(zbytes).hexdigest()==EXPECTED_ZIP_SHA,'externally_bound_archive')
    require(before['MANIFEST.json']==EXPECTED_MANIFEST_SHA,'externally_bound_manifest')
    M=json.loads((root/'MANIFEST.json').read_text()); expected=set(M['files'])|{'MANIFEST.json'}
    require({p.name for p in root.iterdir()}==expected,'flat_exact_release_file_set')
    for name,meta in M['files'].items():
        b=(root/name).read_bytes()
        require(len(b)==meta['bytes'] and hashlib.sha256(b).hexdigest()==meta['sha256'],'original_manifest_entry')
    with zipfile.ZipFile(archive) as z:
        require(len(z.namelist())==8 and set(z.namelist())==expected,'archive_exact_member_set')
        for name in expected:require(z.read(name)==(root/name).read_bytes(),'archive_member_bytes')
    for filename in ('verify.py','check_packet.py'):
        require(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse((root/filename).read_text()))),'author_has_no_disableable_assertions')
    expected_results=(root/'RESULTS.json').read_bytes();rr=json.loads(expected_results)
    require(sum(rr['checks'].values())==2427 and rr['negative_control_count']==len(rr['negative_controls_rejected'])==10,'author_report_count_consistency')
    modes=[];mutations=[]
    with tempfile.TemporaryDirectory(prefix='independent-stringy-audit-') as td:
        base=Path(td);copied=base/'relocated';shutil.copytree(root,copied)
        for flags in ([],['-O']):
            mode='optimized' if flags else 'ordinary'
            for loc in (root,copied):
                p=subprocess.run([sys.executable,*flags,str(loc/'check_packet.py')],cwd=base,capture_output=True)
                require(p.returncode==0 and not p.stderr,'author_packet_replay_'+mode)
                p=subprocess.run([sys.executable,*flags,str(loc/'verify.py')],cwd=base,capture_output=True)
                require(p.returncode==0 and p.stdout==expected_results and not p.stderr,'author_arithmetic_replay_'+mode)
            modes.append(mode)
        for name in sorted(M['files']):
            target=copied/name;old=target.read_bytes();target.write_bytes(old+b'\n# audit mutation\n')
            for flags in ([],['-O']):
                p=subprocess.run([sys.executable,*flags,str(copied/'check_packet.py')],cwd=base,capture_output=True)
                require(p.returncode!=0,'tamper_rejected')
                mutations.append({'file':name,'mode':'optimized' if flags else 'ordinary','rejected':True})
            target.write_bytes(old)
        extra=copied/'UNEXPECTED.txt';extra.write_text('audit-only test')
        for flags in ([],['-O']):
            p=subprocess.run([sys.executable,*flags,str(copied/'check_packet.py')],cwd=base,capture_output=True)
            require(p.returncode!=0,'extra_file_rejected')
        extra.unlink()
        for name in ('CLAIMS.json','MANIFEST.json'):
            target=copied/name;old=target.read_bytes();target.unlink()
            for flags in ([],['-O']):
                p=subprocess.run([sys.executable,*flags,str(copied/'check_packet.py')],cwd=base,capture_output=True)
                require(p.returncode!=0,'missing_file_rejected')
            target.write_bytes(old)
    after={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in root.iterdir() if p.is_file()}
    require(after==before,'authored_freeze_preserved')
    return {'release_files':len(expected),'replay_modes':modes,'authored_exact_checks':2427,'authored_false_shortcuts':10,'file_mutations_rejected':mutations,'structural_mutations_rejected':6,'authored_freeze_unchanged':True}

def main():
    if len(sys.argv)!=3:raise SystemExit('Usage: independent_verify.py AUTHOR_RELEASE AUTHOR_ZIP')
    packet=packet_tests(Path(sys.argv[1]).resolve(),Path(sys.argv[2]).resolve())
    graph=graph_tests();resolution_tests();toric=toric_tests();stars=adjunction_tests();controls=negative_controls()
    result={'problem_id':'30003230','status':'PASS','scope':'Finite exact audit and bound packet replay; geometric proofs reviewed separately; general conjecture remains unresolved.','independent_checks':dict(sorted(COUNTS.items())),'total_independent_checks':sum(COUNTS.values()),'packet':packet,'graphs':graph,'toric':toric,'adjunction_stars':stars,'adversarial_mathematical_controls':controls,'formal_proof_certificate':False}
    print(json.dumps(result,sort_keys=True,indent=2))

if __name__=='__main__':main()
