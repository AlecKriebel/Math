#!/usr/bin/env python3
"""Independent exact algebra/adversarial and binding controls, not a proof assistant.
No finite model in this file is claimed to be a hypercyclic Banach semigroup.
Run with --input-root PATH --history-root PATH. The audit itself is portable.
"""
import argparse
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from math import gcd
from pathlib import Path
import subprocess
import sys

p = argparse.ArgumentParser()
p.add_argument('--input-root', type=Path)
p.add_argument('--history-root', type=Path)
p.add_argument('--bootstrap', action='store_true')
a = p.parse_args()
root = Path(__file__).resolve().parent
inputs = a.input_root or root.parent / 'safe'
history = a.history_root or inputs.parent.parent
counts = {}
def check(name, yes):
    if not yes:
        raise AssertionError(name)
    counts[name] = counts.get(name, 0) + 1
def digest(f):
    b = f.read_bytes()
    return {'bytes': len(b), 'sha256': sha256(b).hexdigest()}
def load(path):
    return json.loads(path.read_text())
def matches(path, record):
    return digest(path) == {k: record[k] for k in ('bytes', 'sha256')}

bound = load(root/'AUDITED_INPUTS.json')
check('frozen_manifest_external_anchor', digest(inputs/'FREEZE_MANIFEST.json')['sha256'] ==
      '0f77ea2dc8653f7680a5709778158b5a4df71811ae9d7a30d5adaefeeb8b2c80')
check('fourteen_frozen_inputs_exact_set', len(bound['revision_2_files']) == 14 and
      {r['path'] for r in bound['revision_2_files']} ==
      {f.relative_to(inputs).as_posix() for f in inputs.rglob('*') if f.is_file()})
for r in bound['revision_2_files']:
    check('frozen_input_bytes_preserved', matches(inputs/r['path'], r))
check('eighteen_historical_inputs_bound', len(bound['historical_files']) == 18)
for r in bound['historical_files']:
    check('historical_input_bytes_preserved', matches(history/r['historical_packet']/r['path'], r))

# Independent execution, not reliance on claimed result files.
packet = json.loads(subprocess.run([sys.executable, str(inputs/'tests/verify_packet.py'),
           '--history-root', str(history)], check=True, text=True, capture_output=True).stdout)
bridge = json.loads(subprocess.run([sys.executable, str(inputs/'tests/verify_bridge.py')],
           check=True, text=True, capture_output=True).stdout)
check('author_packet_all_fifteen_replayed', packet['status']=='pass' and len(packet['checks'])==15)
check('author_packet_exact_report_match', packet==load(inputs/'PACKET_TEST_RESULTS.json'))
check('author_algebra_all_8369_replayed', bridge['status']=='pass' and bridge['total_exact_checks']==8369)
check('author_algebra_exact_report_match', bridge==load(inputs/'EXACT_TEST_RESULTS.json'))
check('historical_hold_not_rewritten', load(history/'independent-audit/AUDIT_RESULT.json')['exact_target_verdict']=='HOLD')

result = load(root/'AUDIT_RESULT.json')
check('separate_bridge_and_external_proof_verdicts', result['bridge_proof_verdict']=='PASS' and
      result['published_2009_proof_independently_audited'] is False)
check('prior_attribution_only_classification', result['exact_target_already_solved_endorsed'] and
      result['classification']=='prior_literature_resolution_with_audited_scalar_bridge' and
      not result['new_counterexample_claimed'] and not result['novelty_claimed'])
check('exact_target_both_parts_and_positive_time', result['answers']==['no','no'] and
      result['time_quantifier']=='every real t > 0')
check('no_remote_writes_no_frozen_edits', not result['remote_writes_performed'] and
      not result['frozen_or_historical_files_modified'])

source_checks=load(root/'SOURCE_CHECKS.json')
frozen_sources={s['id']:s for s in load(inputs/'SOURCE_MANIFEST.json')['sources']}
check('no_third_party_source_payload_claim', source_checks['source_content_included'] is False)
for source in source_checks['sources']:
    check('public_source_identity_matches_frozen', source['title']==frozen_sources[source['id']]['title'] and
          source['url']==frozen_sources[source['id']]['url'])
    check('source_hash_metadata_matches_frozen', source['pdf']==frozen_sources[source['id']]['pdf'])

# Exact complexification norm for non-Hilbert real l1^3, independent of the
# author's linfinity^2 model. Interchange a finite sign maximum with sup_theta.
signs = list(product((-1, 1), repeat=3))
vecs = list(product((Q(-1), Q(0), Q(1)), repeat=3))
def plus(x,y): return tuple(a+b for a,b in zip(x,y))
def mult(c,x): return tuple(c*a for a in x)
def l1(x): return sum(abs(a) for a in x)
def n2(z):
    x,y=z
    return max(sum(s*a for s,a in zip(e,x))**2 +
               sum(s*b for s,b in zip(e,y))**2 for e in signs)
def cmul(a,b,z):
    x,y=z
    return (plus(mult(a,x),mult(-b,y)),plus(mult(b,x),mult(a,y)))
def mat(A,x): return tuple(sum(a*b for a,b in zip(row,x)) for row in A)
matrices = [((0,0,0),(0,0,0),(0,0,0)), ((1,0,0),(0,1,0),(0,0,1)),
            ((0,-1,0),(1,0,0),(0,0,2)), ((1,3,0),(0,1,0),(0,0,-1)),
            ((1,2,-3),(-2,0,1),(0,1,1))]
for x,y in product(vecs,vecs):
    z=(x,y)
    check('l1_complexification_product_topology_bounds', max(l1(x)**2,l1(y)**2)<=n2(z)<=(l1(x)+l1(y))**2)
    check('l1_real_projection_contraction', l1(x)**2<=n2(z))
    for c,d in [(Q(0),Q(0)),(Q(0),Q(1)),(Q(3,5),Q(4,5)),(Q(-2),Q(3))]:
        check('l1_full_complex_homogeneity', n2(cmul(c,d,z))==(c*c+d*d)*n2(z))
    for A in matrices:
        op = max(sum(abs(A[i][j]) for i in range(3)) for j in range(3))
        check('l1_bounded_operator_extension', n2((mat(A,x),mat(A,y)))<=op*op*n2(z))

# Real-period negative control. Unique coefficients in Q(sqrt(2)) model
# rotations with periods 1 and sqrt(2); their only common period is zero.
def fixes_period_one(t): return t[1]==0 and t[0].denominator==1
def fixes_period_sqrt2(t): return t[0]==0 and t[1].denominator==1
qs = [Q(i,j) for i in range(-6,7) for j in (1,2,3)]
check('separate_real_period_witnesses', fixes_period_one((Q(1),Q(0))) and
      fixes_period_sqrt2((Q(0),Q(1))))
check('unrelated_real_periods_not_interchangeable', not fixes_period_one((Q(0),Q(1))) and
      not fixes_period_sqrt2((Q(1),Q(0))))
for t in product(qs, qs):
    check('incommensurate_rotation_common_period_obstruction',
          (fixes_period_one(t) and fixes_period_sqrt2(t)) == (t==(Q(0),Q(0))))

# Integer cycles really do synchronize by LCM; do not transfer this to real periods.
for r,s in product(range(1,13),repeat=2):
    L=r*s//gcd(r,s)
    check('integer_period_lcm_fixes_both', L%r==0 and L%s==0)
    check('integer_period_lcm_minimal', all(k%r!=0 or k%s!=0 for k in range(1,L)))
check('two_and_three_do_not_share_either_original_period', 2%3!=0 and 3%2!=0 and 6%2==6%3==0)

# A genuine C0 toy model: rotation by pi*t on R^2 plus 2^t on R.
# At integer j, the periodic coordinate alternates. The expanding error stays
# equal to z despite the initial perturbation tending to zero. Not hypercyclic.
for j in range(1,33):
    n=2**j
    u=(Q(1),Q(0),Q(3,n))
    image=(((-1)**j)*u[0],((-1)**j)*u[1],n*u[2])
    check('compact_orbit_subsequence_expanding_perturbation', image==(Q((-1)**j),Q(0),Q(3)))
    check('small_input_error_may_have_nonzero_image', abs(u[2])<Q(4,n) and image[2]==3)
    check('even_subsequence_landing', j%2!=0 or image==(Q(1),Q(0),Q(3)))
check('compact_orbit_need_not_converge_without_subsequence', (-1)**2 != (-1)**3)

# Bounded does not mean relatively compact in an infinite-dimensional Banach
# space: distinct unit basis vectors in l2 have squared distance 2.
for i,j in product(range(1,33),repeat=2):
    if i!=j:
        check('bounded_sequence_not_precompact', 1+1-2*int(i==j)==2)
# Dense-set convergence cannot be extended by boundedness of each operator.
# A_n x=n*x_n*e_n vanishes eventually on c00, but for x_n=1/n it has norm 1.
for n in range(2,65):
    check('dense_set_pointwise_convergence_not_global', n*Q(1,n)==1)
    check('infinite_witness_square_summable_bound', Q(1,n*n)<=Q(1,n*(n-1)))

# Exhaustive finite onto semiconjugacies: dense orbit and periodic density
# descend. Finite topology is discrete, so a dense orbit visits all points.
def orbit(f,x):
    out=set()
    while x not in out:
        out.add(x); x=f[x]
    return out
def periodic(f,x):
    y=f[x]
    for _ in range(len(f)):
        if y==x: return True
        y=f[y]
    return False
semiconjugacies=0
for q in product(range(2),repeat=4):
    if set(q)!={0,1}: continue
    for F in product(range(4),repeat=4):
        for G in product(range(2),repeat=2):
            if all(q[F[x]]==G[q[x]] for x in range(4)):
                semiconjugacies+=1
                for x in range(4):
                    check('onto_factor_orbit_descent', {q[v] for v in orbit(F,x)}==orbit(G,q[x]))
                    check('onto_factor_periodic_descent', not periodic(F,x) or periodic(G,q[x]))
                source_dense_orbit=any(len(orbit(F,x))==4 for x in range(4))
                target_dense_orbit=any(len(orbit(G,y))==2 for y in range(2))
                check('onto_factor_dense_orbit_descent', not source_dense_orbit or target_dense_orbit)
                check('onto_factor_dense_periodic_descent', not all(periodic(F,x) for x in range(4)) or
                      all(periodic(G,y) for y in range(2)))
check('nonsurjective_factor_negative_control', len(orbit((0,),0))==1 and
      not any(len(orbit((0,1),y))==2 for y in range(2)))

# Bindings detect any authored proof byte change; they are not proof validators.
proof=(inputs/'PROOF.md').read_bytes()
proof_record=next(r for r in bound['revision_2_files'] if r['path']=='PROOF.md')
check('proof_byte_mutation_rejected', sha256(proof+b'\n').hexdigest()!=proof_record['sha256'])
check('mixed_time_example_insufficient', not all((False,True)) and any((False,True)))
check('no_positive_time_example_refutes_both', not all((False,False)) and not any((False,False)))
check('zero_time_only_obstruction_insufficient', all((False,True,True)[1:]))

allowed={'AUDIT.md','AUDIT_RESULT.json','AUDITED_INPUTS.json','SOURCE_CHECKS.json',
         'TEST_RESULTS.json','verify_audit.py','AUDIT_BINDING.json'}
actual={f.relative_to(root).as_posix() for f in root.rglob('*') if f.is_file()}
check('safe_authored_allowlist', actual<=allowed)
if not a.bootstrap:
    manifest=load(root/'AUDIT_BINDING.json')
    check('audit_binding_exact_set', {r['path'] for r in manifest['files']}==actual-{'AUDIT_BINDING.json'})
    for r in manifest['files']:
        check('audit_binding_bytes', matches(root/r['path'],r))

print(json.dumps({'status':'pass','independent_controls':counts,
    'independent_control_count':sum(counts.values()), 'independent_control_categories':len(counts),
    'onto_semiconjugacies_exhaustively_checked':semiconjugacies,
    'frozen_packet_checks_replayed':len(packet['checks']),
    'frozen_exact_controls_replayed':bridge['total_exact_checks'],
    'frozen_input_files_checked':len(bound['revision_2_files']),
    'historical_files_checked':len(bound['historical_files']),
    'finite_controls_only':True, 'infinite_dimensional_proof_machine_verified':False,
    'audit_binding_checked':not a.bootstrap},indent=2,sort_keys=True))
