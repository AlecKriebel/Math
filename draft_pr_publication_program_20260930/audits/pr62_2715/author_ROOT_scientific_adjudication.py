"""Record ROOT's personally completed bounded PR62 mathematical adjudication."""
from pathlib import Path
import datetime, hashlib, json, os, stat, sys

A = Path(__file__).resolve().parent
R = A.parents[2]
def need(value, message):
    if not value:
        raise ValueError(message)
def ref(path):
    need(path.is_file() and not path.is_symlink(), 'Regular evidence body')
    body = path.read_bytes()
    return {'path': path.relative_to(R).as_posix(), 'bytes': len(body),
            'sha256': hashlib.sha256(body).hexdigest(), 'full_mode': stat.S_IMODE(path.stat().st_mode)}
def capture(name):
    folder = R / 'draft_pr_publication_program_20260930/audits/pr45_9900007' / name
    c = json.loads((folder / 'CAPTURE.json').read_bytes())
    need(c['status'] == 'PASS' and c['actual_execution'] is True and c['completed'] is True
         and c['exit_code'] == 0 and type(c['pid']) is int, 'Genuine successful ROOT custody')
    for stream in ['stdout', 'stderr']:
        r = ref(folder / (stream + '.bin'))
        need(c[stream]['bytes'] == r['bytes'] and c[stream]['sha256'] == r['sha256'], 'Complete actual streams')
    return {'actual_pid': c['pid'], 'started_utc': c['started_utc'], 'finished_utc': c['finished_utc'],
            'whole_capture_files': [ref(p) for p in sorted(folder.iterdir())]}

need(sys.argv[1:] == ['--record-personally-completed-bounded-audit'] and __debug__, 'Explicit scientific record')
proofs = ['original_preparation_family/SOURCE.json', 'original_preparation_family/ORIGINAL_INTAKE_REPORT.md',
          'original_preparation_family/SOURCE_PRECISION_QUALIFICATION.md', 'original_preparation_family/original/OBSTRUCTION.md',
          'original_preparation_family/original/SOURCE_AUDIT.md', 'original_preparation_family/original/source_record.json',
          'original_preparation_family/original/turns.json', 'ROOT_ORIGINAL_PREPARATION_CLOSE_20261003.json',
          'floer_map_algebra_adversary_family/INDEX.json', 'floer_map_algebra_adversary_family/READY.json',
          'floer_map_algebra_adversary_family/MANIFEST.json', 'floer_map_algebra_adversary_family/REPORT.md',
          'floer_map_algebra_adversary_family/PROOF.md', 'floer_map_algebra_adversary_family/VERDICT.json',
          'floer_map_algebra_adversary_family/algebra_controls.py', 'floer_map_algebra_adversary_family/captures/algebra_controls.stdout',
          'ribbon_knot_geometry_adversary_family/SOURCE.json', 'ribbon_knot_geometry_adversary_family/REPORT.md',
          'ribbon_knot_geometry_adversary_family/VERDICT.json', 'ribbon_knot_geometry_adversary_family/independent_controls.py',
          'ROOT_GEOMETRY_SOURCE_READBACK_20261003.json', 'ROOT_INITIAL_READING_20261003.json']
operations = [capture('root_pr62_' + n + '_actual_capture') for n in
              ['original_SOURCE_verify', 'original_SOURCE_close', 'original_SOURCE_readback',
               'floer_SOURCE_close', 'floer_SOURCE_readback', 'geometry_SOURCE_readback']]
obj = {
 'schema': 'ROOT-pr62-scientific-partial-result-adjudication/v1', 'PR': 62, 'problem_id': 2715,
 'problem_code': 'KP-1.56', 'head': '98cc2821e9376507caf2d2c57414f7c7e7719c1b',
 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'actual_writer_pid': os.getpid(),
 'scientific_verdict': 'VALID_ATTRIBUTED_PARTIAL_REDUCTION_TARGET_UNSOLVED', 'status': 'unsolved',
 'original_budget': '1/5', 'new_attempts': 0, 'audit_attempts': 0, 'novelty_credit': 0,
 'ROOT_bounded_mathematical_applicability_audit_percent': 100, 'general_problem_solved': False,
 'claims_and_scope': {
  'literal_target': 'Actual ribbon-comparable knots with isomorphic hat HFK: must the endpoint knots be isotopic? Usual absolute Maslov/Alexander bigraded F2 convention.',
  'universal_algebra': 'Actual graded split injection f with gf=id between finite-dimensional spaces and equal total ranks forces all nonnegative graded deficits to vanish; f is an isomorphism and g its inverse. Thus the target is equivalent to strict total HFK-rank increase for strict ribbon comparisons.',
  'geometric_gap': 'Reverse ordinary annulus can have maxima; an inverse Floer map supplies no reverse ribbon concordance. Agol antisymmetry requires both geometric ribbon arrows. Formal posets and filtered-complex controls do not realize knots or settle the equality case.',
  'known_gate': 'Gordon Lemma3.4 as restated in Boninger Lemma4.1: residually nilpotent successor knot-group COMMUTATOR subgroup, equal Alexander degree and J<=K imply endpoint isotopy. Equal bigraded HFK gives equal Alexander polynomials; fibered and specified pseudoalternating prime-power classes remain imported prior results.',
  'band_twist_exclusion': 'Wang nontrivial-band full-twist family has fixed nonzero finite Kh tail shifted by(2n,4n). Finite support and coordinatewise cancellation give distinct graded profiles while total ranks agree. Corrected Levine-Zemke graded ribbon injection excludes both ribbon directions. A common ribbon predecessor does not compare the twists.',
  'conditional_chain_bound': 'HFK total rank is odd by Euler characteristic at1. If the desired equality case were proved, strict downward steps would decrease rank by at least2, giving at most(R-1)/2. Without that missing premise only ranks eventually stabilize.',
  'recent_scope': 'Selected 2026 fibered-predecessor finiteness, same-companion cable rigidity and specified ribbon-minimal knots do not solve arbitrary equal-HFK ribbon-comparable pairs.'
 },
 'primary_ROOT_reading': {
  'literal_question_and_both_remarks': 'Pinned K3 author text LF2867-2893, printed55-56; no new PDF pixels.',
  'selected_sources': [
   'https://annals.math.princeton.edu/wp-content/uploads/annals-v190-n3-p05-s.pdf',
   'https://arxiv.org/html/2405.08103v1', 'https://arxiv.org/html/2006.01070v1',
   'https://arxiv.org/html/1903.01546v2', 'https://arxiv.org/html/2201.03626v1',
   'https://arxiv.org/html/2602.21109v1', 'https://arxiv.org/html/2608.06625v1', 'https://arxiv.org/html/2606.20802v1'],
  'read_scope': 'Zemke intro/grading and full selected Section3 proof including Lemma3.1; Boninger relevant Section4; Wang selected statements/formula; Levine-Zemke full short main proof and selected grading propositions; Agol core/appendix text; stated 2026 theorem scopes. No complete reconstruction of foundational Floer/TQFT, group or all recent technical proofs.',
  'access_limits': 'Full Gordon1981 proof and Wang journal typeset PDF were not recovered. Boninger author HTML read by ROOT; the geometry family separately recovered its published PDF. Bounded search is not an exhaustive proof of no later result.'
 },
 'reproduction': {'original': 564, 'historical_checker': 20223, 'fresh_algebra': 15026, 'fresh_geometry': 3273,
  'scope': 'Exact finite algebra/logical diagnostics only; no actual knot Floer computation or ribbon movie search. Universal deductions are written proofs dependent on attributed primary theorems.',
  'environment': 'Original first captures did not measure optimization; later separate exact-body -E -B replays with same-flags optimize0/debugtrue probes reproduce outputs. Algebra family sanitized child environment excludes PYTHONOPTIMIZE. Geometry independent checker explicitly refuses optimized execution.'},
 'mandatory_current_precision': ['Endpoint isotopy is the target, not product isotopy of a chosen annulus.',
  'Boninger Pacific J.Math.335(2025) correct pages81-95; original81-93 archived unchanged.',
  'Raw KP-1.56 report ABSENT/selectednull differs from SQL TEXT literal{} missing-report fallback; source and original unsolved1/5 accounting remain intact.',
  'Geometry dated original-authentication descriptor0644 is followed by exact unchanged original SOURCE freeze0444; current geometry family itself remains exact0644. No fabricated historical mode equality.'],
 'proof_artifacts': [ref(A / n) for n in proofs], 'actual_ROOT_custody_operations': operations,
 'original_science_bodies_unchanged': 17, 'native_acceptance_completed': False,
 'remaining_program_gap': 'Current qualification package and later ordered native acceptance after PR48 recovery and intervening PRs.',
 'paper_DOI_tracker': False, 'AI_used_extensively': True, 'human_peer_reviewed': False,
 'unrefereed': True, 'external_individuals_contacted': False
}
body = (json.dumps(obj, indent=2, sort_keys=True) + '\n').encode()
output = A / 'ROOT_SCIENTIFIC_ADJUDICATION_20261003.json'
with output.open('xb') as stream:
    stream.write(body); os.fchmod(stream.fileno(), 0o444); stream.flush(); os.fsync(stream.fileno())
print(json.dumps({'scientific_verdict': obj['scientific_verdict'], 'receipt': ref(output)}))
