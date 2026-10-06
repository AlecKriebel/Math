# Mathematical audit for public safe version 2

Date: 2026-10-06 UTC. Problem ID 2303023; rank 677; Hayman-Lingham Problem 3.23.

## Verdict

PASS_DEDUCTION_WITH_DECLARED_EXTERNAL_PREMISE. The known affirmative result remains credited to prior work; no new approach or new theorem is claimed. The upper deduction and complete lower-bound arguments were re-read for this version. No mathematical correction is required. The source-assessment wording and artifact bindings have changed, so this is a fresh acceptance of version 2, not reuse of an earlier artifact's acceptance.

## Current input binding

AUDIT_RESULT.json binds the actual version-2 author archive, its manifest and its proof. SAFE_AUDIT_MANIFEST.json binds this directory. The separate external acceptance binds the complete publication manifest, which covers both archives, their unpacked files, the replay wrapper and documentation. None of those current bindings certifies excluded evidence.

## Source limits

The cited primary update records an affirmative answer to Problem 3.23. This derivative review does not freshly verify that source assertion or the covering theorem's source wording. The whole-disk theorem stated in PROOF.md is a declared external premise. The derivative provides public bibliographic citations, but no source-retrieval evidence. No image-level reading of Eiderman or independent proof of Govorov's theorem is certified here. No corpus-byte or exact-record verification is performed. These limits narrow the public verification evidence, not the conditional mathematical statement.

## Mathematical review

The following mathematical points were rechecked for this derivative:

- **Target and quantifiers:** one universal function for every normalized nonnegative Green potential, and also for every normalized positive harmonic function, at every threshold t≥0. Covers may depend on the function and threshold. No containment of the covering disks in D is required by the problem.
- **Conventions:** Green potential means the nonnegative potential of a nonnegative measure. The proof is not an assertion about arbitrary signed Green integrals. Infinite potential values are permitted.
- **Truncation and subharmonicity:** for t>28, L=t+1 and v=2−min(u,L) are legitimate pointwise, including where u=+∞. A finite maximum of subharmonic functions is subharmonic. Since v(0)=1, the function is not identically −∞.
- **Actual supremum:** M=sup v satisfies 1≤M≤2; it need not equal 2 or be attained. For example u≡1 gives M=1. No theorem hypothesis is replaced by an unsupported equality.
- **Theorem parameters:** P=(t−2)/18>1. Its whole-unit-disk endpoint is explicitly available; the proof does not infer the endpoint from an interior estimate or take a limit of disk families.
- **Off-cover implication:** u_L≤2+9PM≤t. Because L>t, its strict superlevel set equals the original strict superlevel set at every point. There is no omitted polar set or almost-everywhere substitution.
- **Radius budget:** the theorem gives B=18/(t−2), and g(t)−B=9(t−4)/((t−1)(t−2))>0. Countable radius increments summing to at most half this gap convert any closed disks into an open cover. Empty and finite families are handled too.
- **Small thresholds and decay:** D itself gives radius budget 1 on [0,28]; the large branch tends to zero and agrees with 1 at the branch point.
- **Lower examples:** the harmonic Poisson kernel has an exact disk superlevel set of radius 1/(t+1). Normalized Green atoms have disk radii tending to that value as the pole approaches the boundary, for each fixed t. Projection length gives the covering lower bounds. Thus neither class admits a universal o(1/t) budget. No claim that 27 is an optimal coefficient follows.

`DEDUCTION_AND_LOWER_BOUNDS.md` gives the complete reasoning rather than treating computational samples as a proof.


## Reproducible controls

The arithmetic program was rerun and its new version-2 report matched: 16,452 assertions on 1,028 thresholds. Its only semantic report-label change clarifies that arithmetic alone does not assess a mathematical audit.

The independent mathematical-control program was rerun with its symbolic and rational control body unchanged. It passes 3,340 assertions on 98 thresholds and rejects seven deliberately incorrect mathematical variants. Its old optional artifact-binding mode has been removed; the new portable wrapper supplies binding for actual public files only. Run python audit/verify_independent.py for standalone controls, or the externally pinned portable replay command in README.md for full integrity and both programs.

The written proof, rather than sampled assertions, supplies the universal argument. The finite maximum property for subharmonic functions, the imported theorem, and projection subadditivity are not mechanically proved by these programs. This is an internal mathematical audit, not formal verification or journal peer review.

## Derivative scope

Only source-assessment metadata, obsolete history, bindings and publication wording were revised. The deduction from the theorem and the lower-bound calculations are preserved. New archives were created from the actual version-2 text and code; earlier archives are not embedded. Source documents, copied source text, dataset contents and private coordination material are excluded. No remote mutation was performed in this derivative task.
