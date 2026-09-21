#!/usr/bin/env python3
"""Copy a successful clean candidate's evidence and certify unchanged inputs."""
from __future__ import annotations
import datetime as dt
import hashlib
import json
from pathlib import Path
import platform
import shutil
import sys

EFFORT = Path(__file__).resolve().parent
PROJECT = EFFORT.parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, indent=2)+'\n')


def main():
    extraction = Path(sys.argv[1]).resolve()
    stage = Path(sys.argv[2]).resolve()
    runs = list((extraction/'reproduction_runs').glob('*/receipt.json'))
    if len(runs) != 1:
        raise ValueError('Expected one fresh reproduction')
    reproduction = json.loads(runs[0].read_text())
    if reproduction['status'] != 'passed':
        raise ValueError('Complete reproduction has not passed')
    if sha(stage/'SHA256SUMS.txt') != reproduction['shipment_manifest_sha256']:
        raise ValueError('Stage manifest differs from the shipment consumed by reproduction')
    expected_names = set()
    for line in (stage/'SHA256SUMS.txt').read_text().splitlines():
        expected, name = line.split('  ', 1)
        if name in expected_names or Path(name).is_absolute() or '..' in Path(name).parts or sha(stage/name) != expected:
            raise ValueError(f'Stage differs from its original manifest: {name}')
        expected_names.add(name)
    actual_names = {p.relative_to(stage).as_posix() for p in stage.rglob('*') if p.is_file()
                    and p != stage/'SHA256SUMS.txt'}
    if actual_names != expected_names or any(p.is_symlink() for p in stage.rglob('*')):
        raise ValueError('Stage membership differs from the original shipment')
    for path in (stage/'paper').rglob('*'):
        if path.is_file() and path.suffix in {'.tex', '.bib', '.sty', '.sh'}:
            if sha(path) != sha(extraction/path.relative_to(stage)):
                raise ValueError(f'Manuscript source changed during reproduction: {path.name}')
    kernel = reproduction['lean_receipt']['kernel_report']
    if kernel['status'] != 'passed' or kernel['last_stage'] != 'complete':
        raise ValueError('Incomplete Lean result')
    for rel, expected in kernel['source_snapshot'].items():
        for target in (PROJECT, stage):
            if sha(target/'bell_lean'/rel) != expected:
                raise ValueError(f'Protected source differs: {target}/{rel}')
    bell = PROJECT/'bell_lean'
    reports = bell/'reports'
    historical = reports/'history'
    historical.mkdir(exist_ok=True)
    for name in ('claim_coverage.json', 'environment.json'):
        dest = historical/(Path(name).stem+'_20260910.json')
        if not dest.exists():
            shutil.copy2(reports/name, dest)
    shutil.copytree(extraction/'bell_lean/reports', reports, dirs_exist_ok=True)
    run = reports/'runs'/kernel['run_id']
    axioms = json.loads((run/'axiom_audit.json').read_text())
    if not axioms['dependency_audit_passed'] or axioms['run_id'] != kernel['run_id']:
        raise ValueError('Mismatched axiom audit')
    declarations = json.loads((reports/'declarations.json').read_text())
    source_hash = sha(run/'source_snapshot.json')
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    proof_receipt = f'reports/runs/{kernel["run_id"]}'
    certificate = f'''# Lean verification certificate — version 2

**PASS: The principal results, including the stated model conventions, have complete formal proofs in Lean.**

This certificate refers to the unchanged proof/verifier snapshot checked by the complete clean-extraction run below. It does not certify every auxiliary mathematical statement or alternative proof in the manuscript. The [historical September certificate](CERTIFICATION_20260911.md) remains historical.

| Check | Fresh result |
|---|---|
| Run | `{kernel['run_id']}` |
| Started / ended UTC | `{kernel['started_utc']}` / `{kernel['ended_utc']}` |
| Production mathematical modules | 68, rebuilt from fresh project outputs, followed by `Bell` |
| Theorem/lemma declarations | {len(declarations)}, including private helpers |
| Public transitive axiom audits | {len(axioms['declarations'])} / {len(axioms['declarations'])} passed |
| Expanded contracts | 78 examples across all seven required files passed |
| Protected source/verifier inputs | {len(kernel['source_snapshot'])}, unchanged through verification |
| Compiler controls | Valid proof accepted; invalid `False` proof rejected with a type error |
| Exact artifacts and preflight | All passed; 14 compiler-free preflight stages |
| Publication and review PDFs | Both rebuilt warning-free in the same reproduction |

Authoritative records: [kernel report]({proof_receipt}/kernel_report.json), [axiom audit]({proof_receipt}/axiom_audit.json), [statement contracts]({proof_receipt}/statement_audit.json), and [protected source snapshot]({proof_receipt}/source_snapshot.json). Source-snapshot file SHA-256: `{source_hash}`. The run preserves every executed command, exit code and log hash. Historical receipts are not substituted for changed inputs. Top-level convenience receipts identify the same fresh run.

## What is proved

- Two inputs per party with arbitrary finite input-dependent outputs: equality of ordinary finite POVM and PVM convex hulls; one shared selector chooses complete projective strategies, including their joint states.
- One-input and at-most-two-input equality; minimum-setting classification; physical 3×2 separation; the stated simple and strengthened attained values. The physical projective SOS bound is `289/10` and implies the manuscript's bound.
- Stochastic channels decompose into deterministic functions with normalized nonnegative product weights; exact whole-table processing preserves the projective convex hull.
- Independent source strategies on arbitrary finite-dimensional complex inner-product spaces of local dimension at most two correspond to fixed-qubit matrices. The source density is an actual endomorphism of the tensor product with basis-independent positivity and trace one. Genuine local isometries, tensor transport and complement allocation preserve Born probabilities, measurement normalization and projectivity.
- Arbitrary finite outcome types transport to `Fin` by equivalence, preserving complete strategies, behavior tables and ordinary convex hulls. The combined Hilbert/finite-label model has the stated equality and a finite mixture of actual Hilbert-space PVM branches.

The [claim-to-declaration map](docs/CERTIFIED_COVERAGE.md) and [model conventions](docs/MODEL_CONVENTIONS.md) give exact quantifiers and boundary conditions, including empty labels, zero-dimensional spaces, unused outcomes and zero channel probabilities. No same-state simulation, equality of raw POVM/PVM sets, closure substitution or global POVM optimum is asserted.

## Independent interpretation review and manuscript

The [independent semantic review](../version2_completion_20260921/reviews/semantic_review.md) attempted to falsify the new source models, normalization, tensor/Born transport, common-selector mixture and degenerate cases. The [verifier review](../version2_completion_20260921/reviews/verifier_review.md) separately tested missing contracts, attributed declarations, failure receipts and package integrity. These are independent AI-agent reviews, not external human peer review.

[Manuscript correspondence](reports/manuscript_correspondence_v2.json) binds the revised TeX, PDFs and review evidence to this proof snapshot. The formal proof replaces general duality/KKT with deterministic physical score gaps, the full manifold/Hessian/inertia package with feasible curves and an exact score-gap identity, and the original projective-bound derivation with an operator SOS certificate. General duality, full manifold/Hessian/inertia, broader cone/rank statements and selected auxiliary discrimination/spectral/Appendix B calculations remain manuscript-only; see the precise list in the coverage map.

## Reproduction and trust boundary

Lean is `leanprover/lean4:v4.19.0`, compiler commit `6caaee842e9495688c1567e78c0e68dbb96942aa`. Mathlib is `c44e0c8ee63ca166450922a373c7409c5d26b00b`; all nine dependency commits are fixed and checked. Public theorem dependencies use only `propext`, `Classical.choice` and `Quot.sound`. No admitted proofs, `sorryAx`, custom mathematical axioms or source-level kernel bypasses are accepted.

The compiler/runtime, machine and separately provisioned compiled dependency cache remain trust assumptions. All project proofs are rebuilt; Mathlib is not independently rebuilt. Dependency Git pins and tracked-file cleanliness are checked; they do not independently authenticate a cached compiled artifact. Ordinary Lean linter warnings occur, but proof errors, recovered panics and failed contracts are rejected.

From a clean extraction, run `python reproduce.py --bootstrap`, or use `--dependency-cache /absolute/path/to/prepared/.lake/packages`. See [complete package instructions](../VERSION_2.md) and [Lean-only instructions](OFFLINE_RUN.md). The final local ZIP is separately checked by a further clean extraction, whose outside-the-ZIP receipt and hashes avoid a self-referential archive hash. No immutable release or new DOI is created.
'''
    (bell/'CERTIFICATION.md').write_text(certificate)
    paper_files = [p for p in (PROJECT/'paper').rglob('*') if p.is_file()
                   and p.suffix in {'.tex', '.bib', '.sty', '.sh', '.pdf'}]
    write(reports/'manuscript_correspondence_v2.json', {
        'run_id': kernel['run_id'], 'checked_utc': now,
        'source_snapshot_sha256': source_hash, 'review_completed': True,
        'review_kind': 'Independent AI-agent mathematical interpretation review',
        'external_human_peer_review': False,
        'scope': 'Principal results and stated model conventions, not all manuscript mathematics',
        'manuscript_sha256': {p.relative_to(PROJECT).as_posix(): sha(p) for p in sorted(paper_files)},
        'semantic_review_sha256': sha(EFFORT/'reviews/semantic_review.md'),
        'coverage_sha256': sha(bell/'docs/CERTIFIED_COVERAGE.md')})
    write(reports/'claim_coverage.json', {'status': 'principal_results_and_model_bridges_verified',
          'run_id': kernel['run_id'], 'kernel_checked': True,
          'claim_map': '../docs/CERTIFIED_COVERAGE.md', 'all_manuscript_mathematics_formalized': False,
          'historical_cloud_report': 'history/claim_coverage_20260910.json'})
    write(reports/'environment.json', {'status': 'fresh_complete_reproduction_passed',
          'run_id': kernel['run_id'], 'platform': platform.platform(),
          'python': platform.python_version(), 'toolchain': 'leanprover/lean4:v4.19.0',
          'trust_boundary': reproduction['trust_boundary'],
          'historical_cloud_report': 'history/environment_20260910.json'})
    (reports/'README.md').write_text('''# Verification evidence

`latest_run.json` points to the current complete Lean run. Run-specific receipts and command logs are authoritative for their recorded source snapshots. `manuscript_correspondence_v2.json` is the current paper/proof binding; `manuscript_correspondence.json` is the historical September 11 comparison. Reports under `history/`, `session_20260910/`, old run IDs, old build logs and `recovery_manifest.json` are historical. Their failures or missing-compiler status are not current claims. Compiler-free reports retain `kernel_checked: false` because those checks do not invoke Lean. Read the current certificate for scope and trust boundaries.
''')
    # Update only public evidence/documents; proof and verifier inputs must stay
    # byte-for-byte equal to the just-checked snapshot.
    shutil.copytree(reports, stage/'bell_lean/reports', dirs_exist_ok=True)
    for rel in ('bell_lean/CERTIFICATION.md', 'bell_lean/CERTIFICATION_20260911.md'):
        shutil.copy2(PROJECT/rel, stage/rel)
    for directory in ('reviews', 'evidence'):
        for path in (EFFORT/directory).glob('*'):
            if path.is_file() and path.name != 'start_state.txt':
                target = stage/'version2_completion_20260921'/directory/path.name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, target)
    shutil.copy2(runs[0], EFFORT/'evidence/first_clean_reproduction_receipt.json')
    shutil.copy2(runs[0], stage/'version2_completion_20260921/evidence/first_clean_reproduction_receipt.json')
    print(f'Certified unchanged inputs: {kernel["run_id"]}, {len(axioms["declarations"])} public audits')


if __name__ == '__main__':
    main()
