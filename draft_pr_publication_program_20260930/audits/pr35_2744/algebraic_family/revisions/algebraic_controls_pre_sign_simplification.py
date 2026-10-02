#!/usr/bin/env python3
"""Exact diagnostics for original PR35; no knot arc or universal solution follows.

External inputs are mandatory, read-only, and hash-bound. Only --output and
--scratch are written. Original actual verifiers are reproduced unchanged;
the actual-program mutants below must fail their relevant mathematical checks.
"""
from pathlib import Path
from itertools import product
import argparse
import hashlib
import json
import subprocess
import sys
import sympy as s


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True, type=Path)
    ap.add_argument('--snapshot', required=True, type=Path)
    ap.add_argument('--metadata', required=True, type=Path)
    ap.add_argument('--sources', required=True, type=Path)
    ap.add_argument('--source-bindings', required=True, type=Path)
    ap.add_argument('--output', required=True, type=Path)
    ap.add_argument('--scratch', required=True, type=Path)
    args = ap.parse_args()
    checks = {}
    def ck(name, value):
        if not bool(value):
            raise AssertionError(name)
        checks[name] = 'PASS'
    def simp(M):
        return M.applyfunc(s.simplify)

    meta = json.loads(args.metadata.read_text())
    ck('exact_head', meta['head'] == 'ecef51f6dd0b60be6e3c37f7d89b69ef89da276d')
    ck('exact_base', meta['base'] == 'c6975ca76f9f667f1250ba403d0e6da2aafe14d0')
    ck('original_numeric_count', len(meta['files']) == 15)
    for row in meta['files']:
        b = (args.snapshot/row['path']).read_bytes()
        ck('snapshot_'+row['path'], len(b) == row['size'] and sha(b) == row['sha256'])
        blob = subprocess.run(['git','show',meta['head']+':unsolved_math_prioritization/attempts/2744/'+row['path']], cwd=args.repo, capture_output=True)
        ck('actual_git_'+row['path'], blob.returncode == 0 and blob.stdout == b)
    sources = json.loads(args.source_bindings.read_text())
    for row in sources['files']:
        b = (args.sources/row['path']).read_bytes()
        ck('fresh_source_'+row['path'], len(b) == row['bytes'] and sha(b) == row['sha256'])
    hp = (args.sources/'hp-v2.txt').read_text()
    porti = (args.sources/'porti2017.txt').read_text()
    br = (args.sources/'boyle-rouse.txt').read_text()
    k3 = (args.sources/'k3.txt').read_text()
    ck('hp_liftable_scope_before_proposition', 'Let R(Γ) ⊂ R(Γ) denote the set of representations' in hp and 'that lift to' in hp)
    ck('hp_obstruction_and_knot_example', 'Remark 4.1' in hp and 'Example 4.6 If M is a knot exterior in S' in hp)
    ck('hp_exceptional_branching_explicit', 'cardinality of p−1 (χ) is strictly' in hp and 'Ad-reducible characters' in hp)
    ck('porti_complete_holonomy_smooth_curve', 'Theorem 3.1. The character χ0 of a lift of the holonomy' in porti and 'smooth point of X(K)' in porti)
    ck('boyle_rouse_same_orientation', 'corresponding to the same' in br and 'orientation.' in br and '10157' in br)
    ck('literal_projective_target', 'Problem 1.85. Let K be a hyperbolic knot in S' in k3 and 'arc of representations to SOp3q' in k3)
    record = json.loads((args.snapshot/'source_record.json').read_text())
    turns = json.loads((args.snapshot/'turns.json').read_text())
    ck('source_target_id', record['id'] == 2744)
    ck('original_budget_metadata', turns['substantive_turns_used'] == 1 and turns['turn_limit'] == 5)

    # Universal real polynomial unit-quaternion identities, before specializing.
    a,b,c,d = s.symbols('a b c d', real=True)
    norm = a*a+b*b+c*c+d*d
    U = s.Matrix([[a+s.I*b,c+s.I*d],[-c+s.I*d,a-s.I*b]])
    ck('universal_quaternion_gram', simp(U.conjugate().T*U) == norm*s.eye(2))
    ck('universal_quaternion_determinant', s.expand(U.det()-norm) == 0)
    P = [s.Matrix([[0,1],[1,0]]), s.Matrix([[0,-s.I],[s.I,0]]), s.diag(1,-1)]
    def adj_poly(V):
        return s.Matrix(3,3,lambda i,j:s.expand(s.trace(P[i]*V*P[j]*V.conjugate().T)/2))
    R = adj_poly(U)
    ck('universal_adjoint_real', simp(R.conjugate()-R) == s.zeros(3))
    ck('universal_adjoint_orthogonality', simp(R.T*R-norm**2*s.eye(3)) == s.zeros(3))
    ck('universal_adjoint_orientation', s.factor(R.det()-norm**3) == 0)
    ck('universal_central_sign_invisibility', adj_poly(-U) == R)

    # Source HP Example4.4 invariant W is essential, with exceptional orbits.
    def inv(v):
        x,y,z = v
        return x*x,y*y,z*z,x*y*z
    def orbit(v):
        x,y,z = v
        return {(e*x,f*y,e*f*z) for e,f in product((-1,1), repeat=2)}
    for j,v in enumerate([(2,3,5),(0,3,5),(0,0,5),(0,0,0)]):
        x,y,z,w = inv(v)
        ck('quotient_relation_'+str(j), w*w == x*y*z)
        ck('quotient_orbits_'+str(j), all(inv(q) == inv(v) for q in orbit(v)))
        ck('quotient_exceptional_fibres_'+str(j), len(orbit(v)) == (4,4,2,1)[j])
    ck('squares_alone_do_not_separate_fibres', inv((1,1,1))[:3] == inv((1,1,-1))[:3] and inv((1,1,1))[3] != inv((1,1,-1))[3] and (1,1,-1) not in orbit((1,1,1)))

    # Nonliftability genuinely occurs without the vanishing H2 knot hypothesis.
    A = s.Matrix([[0,-1],[1,0]])
    ck('c2_projective_involution', A*A == -s.eye(2))
    ck('c2_neither_lift_respects_order_two', all((e*A)**2 != s.eye(2) for e in (-1,1)))
    # GIT semisimplification differs from naive raw conjugacy, even for Z.
    N = s.Matrix([[0,1],[0,0]])
    J = s.eye(2)+N
    n = s.symbols('n', integer=True)
    ck('unipotent_nilpotent_identity', N*N == s.zeros(2) and N != s.zeros(2))
    ck('all_unipotent_word_traces_match_identity', s.trace(s.eye(2)+n*N) == 2 and J != s.eye(2))

    # Finite quotient model: two sign-exchanged affine lines have one image.
    t = s.symbols('t', real=True)
    ck('two_components_one_quotient', 1*t == (-1)*(-t))
    ck('faithful_fibre_model_two_points', {(1,0),(-1,0)} == {(z,0) for z in (-1,1)})
    L = s.diag(1+s.I, (1-s.I)/2)
    ck('sign_and_conjugation_are_distinct', L.det() == 1 and s.trace(-L) != s.trace(L.conjugate()) and s.trace(-L)**2 == s.trace(L)**2 and s.trace(L.conjugate())**2 != s.trace(L)**2)

    # The original acnode's irreducibility and isolation, with meaningful bad signs.
    x,y = s.symbols('x y', real=True)
    f = y*y+x*x*(1+x)
    disc = s.discriminant(f,y)
    ck('discriminant_simple_zero_at_minus_one', disc.subs(x,-1) == 0 and s.diff(disc,x).subs(x,-1) != 0)
    ck('acnode_isolation_identity', s.expand(f-y*y-x*x/2-x*x*(x+s.Rational(1,2))) == 0)
    ck('distant_real_arc_identity', s.expand(f.subs({x:-1-t*t,y:t*(1+t*t)})) == 0)
    ck('wrong_sign_gives_branch_through_origin', s.expand((y*y-x*x*(1+x)).subs({x:t*t-1,y:t*(t*t-1)})) == 0)
    D = s.diag(2,s.Rational(1,2))
    B = D*A*D.inv()
    ck('real_elliptic_generators_separately_conjugate', A.trace() == B.trace() == 0 and A.det() == B.det() == 1)
    ck('real_elliptic_pair_noncompact_product', A*B == s.diag(-s.Rational(1,4),-4) and s.trace(A*B) < -2)
    # A torsion-free F2 index-three subgroup countercontrol to source Lemma2.6's
    # gamma^n claim: map F2 onto S3 and take a point stabilizer preimage.
    tau = (1,0,2)
    def compose(p,q):
        return tuple(p[q[j]] for j in range(3))
    tau3 = compose(compose(tau,tau),tau)
    tau6 = compose(tau3,tau3)
    ck('index_three_cube_not_in_stabilizer', tau3[0] != 0)
    ck('factorial_power_in_stabilizer', tau6 == (0,1,2))

    # Actual unchanged source programs, then actual mathematical mutants.
    args.scratch.mkdir(parents=True,exist_ok=True)
    replays = []
    specifications = [
        ('check_controls.py','check_results.json','check_results.json'),
        ('independent_review/submitted_check_controls.py','check_results.json','independent_review/submitted_results.json'),
        ('independent_review/independent_checks.py','independent_results.json','independent_review/independent_results.json'),
    ]
    for j,(script,output,expected) in enumerate(specifications):
        folder=args.scratch/('replay_'+str(j));folder.mkdir(exist_ok=True)
        dst=folder/Path(script).name
        raw=(args.snapshot/script).read_bytes();dst.write_bytes(raw)
        proc=subprocess.run([sys.executable,str(dst)],capture_output=True,text=True)
        actual=folder/output
        ck('unchanged_replay_'+str(j),proc.returncode == 0 and proc.stderr == '' and actual.read_bytes() == (args.snapshot/expected).read_bytes())
        replays.append({'script':script,'script_sha256':sha(raw),'exit':proc.returncode,'stderr':proc.stderr,'result_sha256':sha(actual.read_bytes()),'byte_identical':True,'assertions':json.loads(actual.read_text())['passed']})

    mutations=[
        ('acnode_sign','check_controls.py','f=y*y+x*x*(1+x)','f=y*y-x*x*(1+x)','isolation_remainder'),
        ('compact_pair','check_controls.py','B=s.Matrix([[0,-4],[s.Rational(1,4),0]])','B=s.Matrix([[0,-1],[1,0]])','noncompact_product'),
        ('quaternion_not_normalized','check_controls.py','qs=[(1,0,0,0)','qs=[(2,0,0,0)','unitary_0'),
        ('ordinary_trace_sign','check_controls.py','s.trace(U)**2==s.trace(-U)**2','s.trace(U)==s.trace(-U)','sign_quotient_trace_square_0'),
        ('wrong_conjugator','check_controls.py','D=s.diag(2,s.Rational(1,2))','D=s.eye(2)','generators_conjugate'),
        ('dropped_mixed_invariant','independent_review/independent_checks.py','return (x*x,y*y,z*z,x*y*z)','return (x*x,y*y,z*z,0)','quotient_relation_0'),
        ('incorrect_sign_action','independent_review/independent_checks.py','(a*x,b*y,a*b*z)','(a*x,b*y,a*z)','quotient_sign_orbit_0'),
        ('all_fibres_free','independent_review/independent_checks.py','(4,4,2,1)[k]','4','quotient_fiber_size_2'),
        ('orientation_reversed','independent_review/independent_checks.py','R=adjoint(U); matrices.append(U)','R=-adjoint(U); matrices.append(U)','adjoint_orientation_0'),
    ]
    rejected=[]
    for name,script,old,new,failedcheck in mutations:
        raw=(args.snapshot/script).read_text()
        ck('mutation_unique_'+name,raw.count(old) == 1)
        mutated=raw.replace(old,new)
        folder=args.scratch/name;folder.mkdir(exist_ok=True)
        dst=folder/'mutated_program.py';dst.write_text(mutated)
        proc=subprocess.run([sys.executable,str(dst)],capture_output=True,text=True)
        ck('actual_mutant_rejected_'+name,proc.returncode != 0 and ('AssertionError: '+failedcheck) in proc.stderr)
        rejected.append({'name':name,'original_program':script,'old':old,'new':new,'mutated_sha256':sha(mutated.encode()),'exit':proc.returncode,'expected_failed_check':failedcheck,'stdout':proc.stdout,'stderr':proc.stderr.replace(str(folder.resolve()),'<private>').replace(str(folder),'<private>')})

    result={'passed':len(checks),'failed':0,'sympy_version':s.__version__,'checks':checks,'original_replays':replays,'actual_program_mutations_rejected':rejected,'source_bindings_sha256':sha(args.source_bindings.read_bytes()),'snapshot_metadata_sha256':sha(args.metadata.read_bytes()),'scope':'Universal symbolic normalization diagnostics plus finite countercontrols and actual-program replay; no new knot, compact arc, global literature certification, or solution of KP-1.85. Original attempt remains unsolved 1/5.'}
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'passed':len(checks),'failed':0,'original_replays':len(replays),'actual_mutants_rejected':len(rejected)}))


if __name__ == '__main__':
    main()
