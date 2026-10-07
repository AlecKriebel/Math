# Porous-medium particle scheme: scoped partial results

Problem **30004633 / OWR-4990379-003**, queue rank 942. Status: **unsolved, 5/5 author approaches used**. This package records partial convergence theorems and an obstruction; it does not resolve convergence for general irregular solutions.

## Accepted mathematical scope

The four manuscripts concern the original Gallouët–Mérigot–Natale compact-domain, frozen-proximal Lagrangian particle scheme, not a substituted particle algorithm. One AI reviewer, independent of the author, produced four separate mathematical audit reports accepting their stated claims without a mathematical correction patch:

- [Approach 2](APPROACH_02_COMPACT_DOMAIN.md): positive-time Barenblatt profiles with support strictly separated from the physical wall, for every fixed dimension and exponent m>1.
- [Approach 3](APPROACH_03_REGULAR_FREE_BOUNDARIES.md): smooth, uniformly nondegenerate moving free boundaries with uniform tubular geometry and wall clearance. The exact reference-solution regularity is a hypothesis.
- [Approach 4](APPROACH_04_REFLECTING_WALLS.md): the specified symmetric orthant-box reflecting-wall Barenblatt solutions, including permanent symmetric wall contact.
- [Approach 5](APPROACH_05_COMPACTNESS_AND_PINNING.md): exact stationary microbumps at ε=c h². Every proximal minimizer has stationary particle barycenters. Their limiting curve is not a porous-medium solution, but δ_N²/ε is a fixed positive number. This is an obstruction to an unconditional energy-only compactness argument, not a counterexample under δ_N²/ε→0.

For Approaches 2–4, the proved squared material-map error plus integrated squared material-velocity error is bounded by C(δ_N²/ε+ε+τ/ε), with 0<ε≤1 and τ≤ε. Convergence follows when ε→0, δ_N²/ε→0 and τ/ε→0. This does not assert the same rate for the discontinuous, zero-extended physical velocity evaluated at particle positions.

Arbitrary irregular weak solutions, singular or degenerate interfaces, topology changes, waiting-time interfaces, generic first wall impact, and the general nonlinear-flux identification remain open here. The exact hypotheses and conclusions in the manuscripts control the scope of every summary.

## Attempts and review provenance

One historical whole-space attempt plus the four new substantive author approaches accounts for 5/5. The historical first-attempt bytes were unavailable: they are neither reconstructed nor published, and are not a premise of any accepted argument. Retrieval, diagnostics, audits and packaging do not count as additional proof attempts.

[Acceptance report](ACCEPTANCE_REPORT.md) and [audit manifest](AUDIT_MANIFEST.json) link the four separately reasoned reports by that one reviewer to exact author hashes. These are AI-assisted mathematical assessments, not human peer review or formal proof certification. No novelty or literature-priority claim is made.

The original author packet's pending-review wording and the audit's publication-not-performed wording are preserved historical statements. Current review status is the scoped acceptance above. Audit snapshots named FROZEN_APPROACH_02.md through FROZEN_APPROACH_05.md are omitted as redundant copies: their equality with the published manuscripts was checked, and the frozen manuscript hashes remain recorded in the audit manifest.

## Sources and preserved bytes

The authored proof files, original author ZIP, author manifests, audits and acceptance are unchanged. The author ZIP is 25,960 bytes with SHA-256 `b506b44a188cea5a787ef4736affc74efc5ed5bda1516ab72617401b920b42c5`. Its 12 members are also distributed individually and checked byte for byte.

[Source-verification metadata](SOURCE_VERIFICATION_MANIFEST.json) records public URLs, exact versions, PDF hashes/sizes and inspection history. Primary references are the [OWR report, printed pages 519–522](https://ems.press/content/serial-article-files/46885), [GMN arXiv:2105.12605v2](https://arxiv.org/pdf/2105.12605v2), and [Natale arXiv:2304.05069v2](https://arxiv.org/pdf/2304.05069v2). The latter studies a different scheme and does not substitute for these proofs. Raw third-party documents, extracted source text, page images, dataset contents and private coordination files are excluded.

## Reproduce checks

Python 3 and SymPy are required for the symbolic/finite diagnostics. The integrity checks themselves use only the Python standard library. From this directory, run:

```sh
python3 verify_publication.py
python3 -O verify_publication.py
python3 -I verify_publication.py
python3 -I -O verify_publication.py
python3 negative_controls.py
python3 -O negative_controls.py
python3 -I negative_controls.py
python3 -I -O negative_controls.py
```

The verifier checks the complete public file set, hashes and byte counts, every author archive member, frozen proof pins, audit-output pins, and the two included diagnostics (669 and 50,030 checks), including all seven author mutations. The publication negative controls test missing, added and altered files, a malformed manifest, a corrupted archive, and tampered proof/audit pins. Explicit exceptions remain active under Python optimization. Tests run from relocated copies as well as the prepared package; no source files or prior attempt are required. [Validation results](VALIDATION_RESULTS.json) record local results. These are finite/symbolic consistency and packaging tests, not a numerical PDE convergence study or a substitute for the proofs.

The publication manifest is an integrity inventory, not a digital signature or an independent trust root. Immutable Git commit verification separately compares the remotely retrieved bytes with the checked local packet. Repository CI, if absent, is not a passing result.

Only this problem's Status, Turns and Findings cells change in QUEUE.md; all other existing queue bytes, including inherited notes, links and header, are preserved. No queue regeneration is performed for this scoped draft PR.
