"""Preserve the rejected source reading and clarify the sound original proof."""
import datetime
import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
original = ROOT / 'original_head_authentication_20261006/original_attempt/COUNTEREXAMPLE.md'
v1 = ROOT / 'repaired_diagnostics_v1/COUNTEREXAMPLE.md'
pdf = ROOT / 'lyapunov_dimension_adversary_20261006/tmp/pdfs/km.pdf'
crop = ROOT / 'lyapunov_dimension_adversary_20261006/tmp/pdfs/km_eq5_crop.png'

def pin(path):
    data = path.read_bytes()
    return {'path': str(path.relative_to(ROOT)), 'bytes': len(data),
            'sha256': hashlib.sha256(data).hexdigest()}

if hashlib.sha256(original.read_bytes()).hexdigest() != 'a9ea8220014aed7c082c995023a3bc7cdd10014544a85376d99267d908323266':
    raise RuntimeError('Original candidate changed')
if hashlib.sha256(v1.read_bytes()).hexdigest() != '4943f2c38effe24e0aa049242f035091df100c1089612cd2ae4c585abc161ddb':
    raise RuntimeError('Rejected v1 changed')
if not crop.is_file():
    raise RuntimeError('Independent high-resolution crop missing')

utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
rejection = {
    'schema': 'pr111-rejected-source-reading/v1', 'UTC': utc,
    'actual_root_PID': os.getpid(),
    'status': 'WITHDRAWN; rejected as a source-framing error',
    'original': pin(original), 'rejected_v1': pin(v1),
    'decisive_high_resolution_crop': pin(crop),
    'pinned_pdf_sha256': 'ed0ca54b5839cad99c88295b5b1a77bdeb6b7563bb8d2c7ccd412160bee7c168',
    'correct_observation': 'Kuznetsov-Mokaev 2018 Eq(5) displays a nonnegative partial-sum inequality, >=0. The lower bar is visible at original resolution.',
    'cause': 'An avoidable misreading of a downsampled rendering; the original extracted text and an independently rendered high-resolution crop agree on >=0.',
    'false_proposed_correction': 'V1 incorrectly claimed a strict positive partial-sum index and an unspecified zero-leading convention in the printed equation.',
    'original_math_changed': False, 'new_central_proof_search_turns': 0,
    'historical_v1_records_preserved': True,
    'promotion_authorized_for_v1': False,
}
out = ROOT / 'repaired_diagnostics_v1/REJECTED_AFTER_HIGH_RESOLUTION_SOURCE_CHECK.json'
if out.exists():
    raise RuntimeError('Rejection record already exists; preserve it')
out.write_text(json.dumps(rejection, indent=2, sort_keys=True) + '\n')

old = "Finally, for the finite-time singular-value definition discussed by Kuznetsov–Mokaev, the torus and all equilibrium/periodic cases have the exact exponential singular values already computed. Their pointwise finite-time Kaplan–Yorke values equal(5) for every t>0. Hence at every positive time the supremum over A exceeds all equilibrium/periodic values. In particular inf_(t>0) sup_A dim_L(t,x) is at least203/50. We do not claim an equality for this infimum by silently interchanging it with a pointwise limit; no such interchange is needed for the strict comparison of candidate orbits."
new = "Finally, use the finite-time singular-value Kaplan–Yorke convention with j=max({0} union {k: the sum of the first k logarithmic singular-value rates is nonnegative}), and dimension0 when the first rate is negative. Kuznetsov–Mokaev's printed equation(5) uses the nonnegative inequality, consistent with the zero exponents included here. For the torus and all equilibrium/periodic cases, the singular values are the exact exponentials already computed. Their finite-time pointwise values equal their corresponding entries in(5) for every t>0. Hence at every positive time the supremum over A exceeds all equilibrium/periodic values. In particular inf_(t>0) sup_A dim_L(t,x) is at least203/50. We assert no equality for this infimum and interchange no spatial supremum with a pointwise time limit.\n\nThe finite-time spatial supremum need not equal the asymptotic maximum203/50 at each time. For example, at a point with |z1|^2=|z2|^2=3/4, one has f=-13/25 and g'=2243/625. As t decreases to0, the logarithmic singular-value rates approach two copies of(2243/625,-13/25) together with-100. The leading four have positive sum3836/625, so the finite-time pointwise dimension tends to63459/15625=4.061376, strictly above203/50 by43/31250. Continuity gives the strict excess for sufficiently small positive times. This boundary control reinforces the limited finite-time claim; it neither computes the time infimum nor changes the asymptotic classification."
body = original.read_text()
if body.count(old) != 1:
    raise RuntimeError('Expected unique original finite-time paragraph missing')
v2dir = ROOT / 'repaired_diagnostics_v2'
v2dir.mkdir(exist_ok=False)
proof = v2dir / 'COUNTEREXAMPLE.md'
proof.write_text(body.replace(old, new))
record = {
    'schema': 'pr111-corrected-diagnostic/v2', 'UTC': utc,
    'actual_root_PID': os.getpid(), 'original_head': '8a7270989d7064a4b97badecaa4b311db5e6d49f',
    'original': pin(original), 'corrected_diagnostic': pin(proof),
    'rejected_v1_record': pin(out),
    'changes': ['Make the existing nonnegative finite-time index explicit, agreeing with printed Eq(5).',
                'Add the independently derived exact transient control and retain only the finite-time lower bound.'],
    'original17files_mutated': False,
    'required_original_mathematical_defect_found': False,
    'new_central_proof_search_turns': 0,
    'priority_cleared': False, 'publication_package_cleared': False,
}
(v2dir / 'CLARIFICATION.json').write_text(json.dumps(record, indent=2, sort_keys=True) + '\n')
print(json.dumps(record, sort_keys=True))
