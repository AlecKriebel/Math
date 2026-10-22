# A qualitative pre-Schwarzian improvement for real schlicht functions

Author: Alec Kriebel, independent researcher. ORCID: https://orcid.org/0009-0001-9320-500X

This is an unrefereed research note and verification package for the qualitative fixed-point interpretation of Hayman–Lingham Problem 6.86 (research candidate 2306086, PR 662). AI tools were used extensively in developing, auditing, reproducing, and writing the work. Internal AI reviews do not constitute human peer review.

## Exact result and limits

For normalized real-coefficient holomorphic injections of the unit disk, put A_f(z)=(1-|z|²)f''(z)/f'(z)−2 conjugate(z). At each fixed nonreal point, max_f |A_f(z)| is strictly below 4. The gap is uniform over the whole function class, and on each compact subset of the nonreal disk. On the real diameter the maximum is 4. The original source expression at zero is identically zero and differs from the auxiliary A_f(0).

The paper gives the analytic proof. The sharp numerical radius, an explicit upper-gap formula, general extremizers, and the full variability region are not determined. Its methods are classical. No historical firstness, exhaustive novelty clearance, or present-openness guarantee is claimed. Read CURRENT_PRIORITY_AND_STATUS.md for the remaining primary-source limits.

## Contents

- The five-page PDF and its standalone LaTeX source.
- The complete original 24-file candidate under native/unsolved_math_prioritization/attempts/2306086, with its original byte bindings and two authored archives.
- Independent analytic/geometric and covariance/source reviews, including exact controls and explicitly uncertified saved numerical replays.
- Two distinct bounded priority reviews, the historical-source access report, and the recovered Rodemich argument-bound addendum. That addendum's locally univalent countermodel is outside the globally univalent target class and does not refute the paper.
- Parent acceptance and reproduction records, the exact publication metadata, machine-readable claim scope, and PACKAGE_MANIFEST.json.

The candidate's historical author files intentionally retain their original partial/pending labels. Keep its SCOPE_CLARIFICATION.md attached: it controls their qualitative interpretation. CURRENT_PRIORITY_AND_STATUS.md and the paper describe this package's current scope; dated research logs and earlier report passages describe their respective checkpoints.

Full third-party PDFs, copied article text, page images, temporary environments, and operational credentials are excluded. Source URLs, hashes, and original comparison arguments remain available in the ledgers.

## Reproduce

Python 3.12.14 with SymPy 1.14.0 and mpmath 1.3.0 was used for the exact/symbolic replays. From the unpacked archive, install the pinned packages in requirements.txt into a local environment, then run:

```sh
python verify_package.py
python verify_package.py --replay
```

The first command verifies the complete manifest and exact claim scope. The second runs copied temporary inputs: the candidate's 3,558 exact controls in ordinary and optimized modes, 32 supplied symbolic controls, 24 candidate mutation controls, 87 separately authored algebra/binding checks, seven geometric shortcut checks, and nine exact Rodemich-addendum margins. Analytic proofs remain written arguments, not formal proof certificates.

Optional numerical reproduction requires requirements_numerical.txt:

```sh
python verify_package.py --replay --numerical
```

This re-evaluates the four saved controls using the supplied RK45 procedure and a separately authored alternative-state DOP853 procedure. It does not rerun optimization. Agreement is floating-point reproducibility evidence, without interval error enclosures, certified strict improvements, a sharp upper bound, or a global extremality assertion. If the numerical construction is excerpted, its endpoint tail parameter +1 gives k_minus, and −1 gives k_plus.

The verifier does not edit the unpacked package. Use TMPDIR to choose its temporary scratch location. A separate metadata/header check or archive checksum is not a substitute for reading the proof and source qualifications. The LaTeX file can be compiled with a standard AMS-capable LaTeX distribution; the supplied PDF was compiled with Tectonic and visually inspected page by page.

## Reuse

The authored paper and supporting materials are released under CC BY 4.0. This does not grant rights in third-party works identified in the source ledgers; their full texts are not included. The source candidate was captured from immutable commit e31701151c331a6eed9224fb37a75a374ea1043e. The associated PR is https://github.com/AlecKriebel/Math/pull/662.
