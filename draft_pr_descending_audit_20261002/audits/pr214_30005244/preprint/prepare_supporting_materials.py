"""Prepare owned local package files only; no Git or provider mutations."""
from pathlib import Path
import hashlib
import json
import shutil

R = Path(__file__).resolve().parent
D = R.parent / 'initial_review_20261015'
S = D / 'submitted/unsolved_math_prioritization/attempts/30005244'
V = R / 'verification'
U = R / 'pr_update/30005244'
A = U / 'history/original_submission_20261015'
for p in [V, U, A]:
    p.mkdir(parents=True, exist_ok=True)
intake = json.loads((D / 'INTAKE.json').read_text())
archive_rows = []
prefix = intake['native_source_prefix']
for row in intake['original_source_files']:
    rel = row['native_path'].removeprefix(prefix)
    p = S / rel
    raw = p.read_bytes()
    assert len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256']
    dest = A / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        assert dest.read_bytes() == raw
    else:
        dest.write_bytes(raw)
    archive_rows.append(dict(row, archive_path=str(dest.relative_to(U))))
(U / 'ORIGINAL_SUBMISSION_MANIFEST.json').write_text(json.dumps({
    'original_PR_head': intake['head'], 'all_original_files_preserved': True,
    'historical_status': 'Original claims and readiness records are history, not current publication clearance.',
    'files': archive_rows,
}, indent=2) + '\n')
header = '''# Current scope and priority qualification (15 October 2026)

This original analytical derivation remains valid under the explicit voxel-volume condition (G). The current result answers the OWR off-interval approximation question for that class, including bounded Lipschitz particles; it does not classify every irregular compact or bounded-open support. The compact-support example refutes an unrestricted extrapolation, not convergence for regular particles. See SOURCE_AUDIT.md, the standalone research note and its version-bound review records for the operative source and priority statement.

The static interval is Costabel--Dauge--Nedaiasl's established result. Cubic consistency, compact approximation, continuum poles, ball perturbation and center-value dependence have substantial prior literature. No first-priority or new general spectral principle claim is made. A named 2022/2023 dynamic manuscript remains unavailable, and Rahola's full paper and one forward-citing thesis were not fully read. The credited exact-model proof is independently verified within those explicit limits.

The entire original 31-file submission, including its original version of this file and historical reviews/readiness claims, is preserved byte-for-byte under history/original_submission_20261015. Those reviews retain their original input bindings. Publication and merge are pending final sequential manuscript reviews and later explicit receipts.

---

'''
original_candidate = (S / 'CANDIDATE.md').read_text()
old_status = '**Unreviewed.** One substantive author research turn. No novelty assertion.'
old_review = 'Independent review and a broader novelty check remain required.'
assert original_candidate.count(old_status) == original_candidate.count(old_review) == 1
qualified_candidate = original_candidate.replace(old_status,
    'Original analytical derivation. Current validation, scope and bounded priority assessment are recorded in the opening notice and accompanying reports. This file does not confer publication clearance. No first-priority assertion.')
qualified_candidate = qualified_candidate.replace(old_review,
    'Independent mathematical review and bounded priority assessment are recorded in the accompanying version-bound reports. Their source-access limitations remain explicit; publication clearance requires the later sequential manuscript review and final acceptance record.')
(U / 'CANDIDATE.md').write_text(header + qualified_candidate)
scope = '''# Source, credit and scope

The exact question is Costabel's OWR43/2022 contribution, Section 4, printed p.2582: description and proof of the observed off-real-interval eigenvalue approximation. The current affirmative theorem concerns bounded measurable representatives whose center-selected cubic voxel unions satisfy |Omega_h triangle Omega| -> 0. This includes all bounded boundary-null and Lipschitz particles for arbitrary translated cubic grids. This geometric sufficient condition is explicit here and is not printed in the source; no necessary-and-sufficient geometry classification is claimed. No result inside the exact static lattice interval, convergence rate, varying frequency limit or individual Jordan-block preservation is asserted.

The convention is K_kappa=-(D^2+kappa^2 I)e^(i kappa r)/(4 pi r), S_kappa=A_kappa-I/3, with exact zero diagonal matrix blocks. The OWR report has a material-contrast sign inconsistency; this package uses the declared operator convention without importing that conversion. The intrinsic ball gap and rank calculation precede whole-space zero extensions.

Prior ingredients: Costabel--Dauge--Nedaiasl 2023/arXiv2302.13159v3 establish the bounded static lattice operator, Ewald construction and exact interval bound. Yurkin--Maltsev--Hoekstra 2006, with 2015 erratum, already develop cubic cancellation and DDA consistency; their Eq.(65) assumes inverse control. Anselone--Palmer 1968, Anselone--Treuden 1985 and Descloux--Nassif--Rappaz 1978 supply classical compact/stable spectral approximation machinery. Budko--Samokhin, Zhou and Ammari--Li--Zou precede this work on continuum operator decomposition and poles. Rahola, Ammari--Millien and Tzarouchis--Yla-Oijala--Sihvola precede its sphere-spectrum, perturbation and radiation ingredients. Yurkin--Mishchenko 2018 Section IX and footnote22 discuss center-value dependence and continuity issues.

The note's purpose is an independent, credited proof for the actual sampled matrix on a common Hilbert space: strong static consistency, Hilbert--Schmidt norm consistency of the sampled dynamic remainder and changing masks, followed by the classical spectral argument. The compact positive-volume empty-interior support is an assembly of classical ingredients, with explicit frequency 1/10000 and an existential finite mask index. It is not a regular-particle obstruction or a new mechanism for continuum nonreal poles.

Priority limitations remain substantive. Costabel--Dauge--Nedaiasl announced a time-harmonic DDA stability manuscript in 2022/2023; its full proof was not located in the bounded public audit through 2026-10-15. The exact scope of unavailable work cannot be excluded. Rahola's publisher abstract was read but its full article was unavailable. Goepfert's 2024 forward-citing thesis was screened at metadata/abstract level only. Some broader classical originals were unavailable, though the three named approximation papers were read at proof level. None of these access limitations is silently treated as exclusion. The note makes no first-priority, wholly-new-theory or absolute novelty claim. Authored audit reports and precise source-read maps are supplied; entire third-party source payloads are excluded.

The research note is an unrefereed preprint, with extensive AI use and internal independent AI-assisted adversarial review. No external human peer review, formal proof-assistant certification, endorsement by cited authors or outreach is asserted.
'''
(R / 'SOURCE_CREDIT_SCOPE.md').write_text(scope)
(U / 'SOURCE_AUDIT.md').write_text(scope)
(U / 'README.md').write_text('''# Discrete-dipole spectral approximation: current qualified result

Problem 30005244 / OWR-11101924-008. The affirmative result is the off-interval convergence theorem under (G), including every bounded Lipschitz particle. The compact empty-interior example diagnoses an unrestricted support extension. See CANDIDATE.md, SOURCE_AUDIT.md and the separately prepared note, Off-interval spectral convergence for geometrically consistent discrete dipoles.

The current source adds explicit credit and scope qualifications. All 31 original files are archived with native blob, size and SHA256 pins. Historical files are not current review verdicts. The external manuscript package contains the portable verification runner and fresh sequential whole-manuscript reviews when completed. Mathematical review and qualified preparation have passed; publication remains pending those reviews and explicit final clearance.
''')
(U / 'ACCEPTANCE.json').write_text(json.dumps({
    'status': 'claimed_solved', 'mathematics': 'verified under explicit (G)',
    'scope': 'OWR off-interval phenomenon for geometrically consistent center-selected voxels; compact-support obstruction supplementary',
    'priority': 'credited exact-model independent proof; first priority not certified; named unavailable dynamic manuscript retained',
    'preprint_title': 'Off-interval spectral convergence for geometrically consistent discrete dipoles',
    'preprint_review_clearance': False, 'published_DOI': None,
    'original_head': intake['head'], 'author_ORCID': '0009-0001-9320-500X',
    'AI_tools_used_extensively': True, 'external_human_peer_review': False,
}, indent=2) + '\n')
copies = [
    ('kernel_consistency_adversary_01/controls.py', 'kernel_controls.py'),
    ('ball_counterexample_adversary_01/exact_controls.py', 'ball_exact_controls.py'),
    ('spectral_fredholm_adversary_01/checks.py', 'spectral_illustration.py'),
]
for source, dest in copies:
    shutil.copyfile(D / 'root_reproduction/new_independent_controls' / source, V / dest)
original_checks = [
    ('verify.py', 'author'),
    ('independent_review/independent_check.py', 'inherited_review'),
    ('scope_continuation/verify_scope.py', 'author_scope'),
    ('scope_continuation/independent_review/independent_scope_check.py', 'inherited_scope_review'),
]
checks = []
for source, family in original_checks:
    raw = (S / source).read_bytes()
    expected = D / 'root_reproduction' / family / 'stdout.json'
    dest = V / 'expected' / (family + '.json')
    dest.parent.mkdir(exist_ok=True)
    shutil.copyfile(expected, dest)
    checks.append({'script': source, 'sha256': hashlib.sha256(raw).hexdigest(),
                   'expected': str(dest.relative_to(V)), 'reported_exact_assertions': json.loads(expected.read_text())['exact_assertions']})
(V / 'ORIGINAL_CHECKS.json').write_text(json.dumps(checks, indent=2) + '\n')
(V / 'requirements.txt').write_text('numpy==2.3.4\nsympy==1.14.0\n')
(V / 'README.md').write_text('''# Reproducible finite controls

Use Python3.14.6 with NumPy2.3.4 and SymPy1.14.0 (recorded replay versions). From the extracted archive root, install verification/requirements.txt in a disposable environment and run:

    python verification/run_checks.py --output verification_run.json

All seven programs execute in temporary working directories; the archived originals and scripts are unchanged. The first four run unchanged original programs, check their pinned script bytes and compare every JSON field against the root replay, allowing at most 1e-12 absolute/relative drift in floating numbers. They report 301+625+482+748=2156 exact assertions, alongside explicitly illustrative floating tables in the first two programs. These counts are program-reported checks, not independent proof obligations.

The new ball program performs 1244 rational/integer controls without floating eigenvalue calculations. The kernel program checks symbolic differentiation, expansions, scaling and 427 complete integer shells through squared radius512, plus illustrative static Gaussian and dynamic refinement tables. The final spectral program illustrates a defective cluster with norm-convergent Riesz projections while full resolvent norms do not converge. Its finite matrices and contour quadrature are not proof certificates.

The executable controls do not prove Hilbert-space completeness, continuum or mesh limits, Fredholm continuation, source coverage, historical priority or the existence of a finite effective index in the compact-support construction. Those conclusions require the written proof and source reading. The analytic support index is existential and is not computed. PACKAGE_FILES.json verifies archive bytes, not mathematical truth. Historical manifests may contain absolute provenance paths; execution here uses only archive-relative paths and temporary directories. No network access is needed for the checks.
''')
(R / 'README.md').write_text('''# Off-interval spectral convergence for geometrically consistent discrete dipoles

Alec Kriebel, independent researcher. ORCID: https://orcid.org/0009-0001-9320-500X.

This research note gives an independent proof of the OWR43/2022 off-interval discrete-dipole spectral approximation question under the explicit voxel-volume condition (G). It includes all bounded Lipschitz particles and arbitrary translated cubic meshes, with every complex frequency fixed. The actual zero-diagonal matrices have off-interval spectral stability, no pollution and convergence of isolated eigenvalues with algebraic multiplicity, norm Riesz projections and generalized spectral subspaces. A separate compact positive-volume empty-interior support has a nonreal continuum pole at frequency1/10000 while all rational-grid matrices are 3x3 zero.

The static lattice interval, cubic consistency, abstract spectral approximation, continuum pole theory and sphere perturbation mechanisms are credited prior work. No first-priority claim is made. A named 2022/2023 dynamic manuscript remains unavailable; Rahola's full article and one forward-citing thesis were not fully read. SOURCE_CREDIT_SCOPE.md and the authored audits preserve these specific limitations. The theorem does not assert convergence for every irregular compact support, necessary geometry conditions, interval-interior correctness or rates.

- dipole_spectrum.tex: standalone editable LaTeX; first run `mkdir -p output/pdf`, then `tectonic --outdir output/pdf dipole_spectrum.tex`.
- output/pdf/dipole_spectrum.pdf: compiled eleven-page note, supplied separately from the verification ZIP.
- verification/: portable finite controls and execution instructions.
- pr_update/30005244/: current qualified source with all 31 original files archived byte-for-byte.
- metadata.json and deposit.json: one identical metadata object for the repository Zenodo tool.

The verification archive includes source, finite controls, original-submission provenance and selected authored mathematical and priority audits. Full third-party PDFs/text/images and raw search payloads are excluded. Historical audit manifests retain their original input bindings and absolute provenance paths; those paths are not runtime dependencies.

This is an unrefereed preprint. AI tools were used extensively in argument development, computation, source research, writing and internal independent adversarial review. No external human peer review, proof-assistant formalization or endorsement by cited researchers is asserted. The named human author is responsible for the work.

Preparation is not release clearance. Fresh sequential whole-manuscript/package reviews, global fixes and later explicit final clearance are required before publication. Only verified provider receipts establish publication or merge.
''')
metadata = {
    'title': 'Off-interval spectral convergence for geometrically consistent discrete dipoles',
    'upload_type': 'publication', 'publication_type': 'preprint',
    'description': '''We give an independent proof of the off-interval eigenvalue approximation described in Costabel's OWR43/2022 discrete-dipole question, under an explicit geometric condition: center-selected cubic voxel unions converge in volume to the bounded measurable particle. This includes every bounded Lipschitz particle, for arbitrary grid translations. At every fixed complex frequency, the actual zero-diagonal matrices have no spectral pollution outside the exact static lattice interval, uniform resolvent stability there, and approximation of isolated eigenvalues with algebraic multiplicity, norm-convergent embedded Riesz projections and generalized spectral subspaces. The proof combines Costabel--Dauge--Nedaiasl's established static lattice interval with strong static consistency, Hilbert--Schmidt convergence of the actual sampled dynamic correction and classical compact spectral approximation. A separate compact positive-volume empty-interior support has a nonreal continuum pole at frequency1/10000 while every matrix on the rational meshes is 3x3 zero; its support index is existential. This does not refute convergence for regular particles or establish a necessary geometry condition. Cubic DDA consistency, general spectral principles, continuum pole theory and sphere perturbation are credited prior work. A named 2022/2023 time-harmonic DDA manuscript was not located in the bounded audit, Rahola's full article was unavailable, and a forward-citing thesis was screened only at metadata/abstract level. These priority limitations remain explicit; no first-priority, new general theory or unrestricted compact-support resolution is claimed. The deposit contains an analytical research note and a source/verification archive with original artifacts, exact symbolic/rational controls, illustrative numerical diagnostics and authored adversarial audits. Finite computations supplement rather than replace the proof and do not certify historical priority. AI tools were used extensively in development, derivation, computation, literature research, writing and independent internal adversarial checking. This is an unrefereed preprint without external human peer review or proof-assistant formalization.''',
    'creators': [{'name': 'Kriebel, Alec', 'affiliation': 'Independent researcher', 'orcid': '0009-0001-9320-500X'}],
    'access_right': 'open', 'license': 'cc-by-4.0', 'publication_date': '2026-10-15', 'version': '1.0',
    'keywords': ['discrete dipole approximation', 'spectral approximation', 'strongly singular integral operators', 'Riesz projections', 'Hilbert-Schmidt consistency', 'geometric consistency', 'OWR-11101924-008'],
}
(R / 'metadata.json').write_text(json.dumps(metadata, indent=2) + '\n')
print(json.dumps({'original_files_preserved': len(archive_rows), 'support_prepared': True, 'publication_cleared': False}))
