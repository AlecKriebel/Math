# Independent review of PR1314 / problem 2800905

**Verdict: the full negative answer for the original unspiked Gaussian
positive-PCA SDP is valid, with explicit standard imports and correct
credit to Bandeira–Kunisky–Wein. One qualified existing-paper row is
proposed; no new publication is warranted.**

For independent upper entries N(0,1/n), the trace-one, entrywise-nonnegative,
positive-semidefinite relaxation has value tending to2 in probability and
expectation. The nonnegative unit-vector optimum is at most√2+o(1) with
high probability. Thus every rank-one SDP optimizer is excluded with
probability tending to one. No blocking mathematical gap was found.

## Exact original target

The [original 2015 author post](https://afonsobandeira.wordpress.com/2015/11/28/10l42psbm/)
identifies Problem9.5. The actual [October2016 lecture notes](https://people.math.ethz.ch/~abandeira/TenLecturesFortyTwoProblems.pdf),
printed130–131, give the Gaussian model and equations103–104. They ask
whether the expected SDP value is√2+o(1) and whether an SDP solution has
rank one with high probability. The constraints are trace one, matrix
positive semidefiniteness, and entrywise nonnegativity. There is no spike.
Both original conjectures receive negative answers.

The read-only cached original statement matches the compact catalog hash
`09b9c2bbf51c340918ec6cdc22d79224ea8344db1f6a06876967f1331f871571`.
Its later research summary introduces a planted positive spike. That
summary does not change the actual original question. The present proof
also does not substitute diagonal-one constraints for trace one.

## Independent mathematical assessment

[INDEPENDENT_ARGUMENT.md](INDEPENDENT_ARGUMENT.md) supplies a checkable
unbounded argument, including the essential proof behind the credited
witness. The application of Sudakov–Fernique checks the increment
inequality explicitly, rather than requiring equal pointwise variances.
The exceptional all-negative linear Gaussian vector is handled by an
inequality. Gaussian concentration uses coefficient norm√(2/n).

The Haar-projector entry estimate is reconstructed from chi-square mgfs
and polarization, so the published Proposition5 is not an unsupported
black box. The construction uses r=⌊δn⌋ and fixed positive parameters.
The all-ones correction dominates the negative off-diagonal entries after
division by r. The global semicircle law is needed only on a fixed
interval with positive limiting mass. Parameters are chosen before the
dimension limit; no edge rigidity or eigenvalue/projector independence
is presumed. The expectation lower bound uses the feasible trace floor
Tr(G)/n and its second moment, avoiding an unjustified uniform-integrability
step. A diagonal operator-norm coupling is small in probability and L1,
and transfers all necessary conclusions to the original ensemble.

Compactness and the spectral theorem justify existence and deterministic
operator-norm stability. Rank-one feasibility is exactly a common-sign
condition, including zero coordinates, so a strict value gap excludes all
rank-one optimizers without requiring uniqueness.

The remaining explicit imports are Gaussian concentration,
Sudakov–Fernique, and the global semicircle law. Their relevant statements
and hypotheses were inspected. This review does not recursively reprove
these classical theorems. The full Montanari–Richard limit of the true
optimum is attributed in the PR and is unnecessary here; its AMP lower
bound is not independently certified by this review.

## Prior publication and normalization qualification

The [actual PMLR paper](https://proceedings.mlr.press/v145/bandeira22a/bandeira22a.pdf),
Theorem4 and its complete Section2 proof, was independently read. It
explicitly connects the limit question to Problem9.5. The original
[2020 v1](https://arxiv.org/pdf/2012.02243v1) contains the same projector
argument as Theorem3. The official [publisher citation](https://proceedings.mlr.press/v145/bandeira22a.html)
uses2022, volume145, pages153–171; the conference/PDF header uses2021.
These are versions of one credited work by Bandeira, Kunisky, and Wein.

Both source PDFs visibly reverse the defining GOE diagonal/off-diagonal
variances. This is a substantive literal normalization defect, not OCR.
The displayed model would give limiting SDP value2√2. The reconstruction
explicitly uses invariant GOE with off-diagonal variance1/n and diagonal
variance2/n, then proves the transfer to the original diagonal variance1/n.
The published Haar argument and quadratic-form variance identify this
intended convention. The diagnosis is mathematical and **not an
author-confirmed erratum**. Nothing in this review treats the contradictory
literal variance display as a valid theorem hypothesis.

The paper's probability-limit theorem, once correctly normalized, is the
credited prior resolution. The expectation estimate and precise original
diagonal transfer are supplied explicitly by the reconstruction; they
are not falsely quoted as the entire wording of Theorem4. The unrelated
low-degree hardness section and the shrinking-parameter rate remark are
outside this review.

The authenticating arXiv DOI is
[10.48550/arXiv.2012.02243](https://doi.org/10.48550/arXiv.2012.02243).
DataCite identifies it as a2020 arXiv preprint, with matching title and
three authors. It is used in the proposed DOI cell as an identifier of
the same published work, not represented as a publisher-assigned PMLR
DOI. No PMLR-specific DOI was authenticated. The row separately links the
canonical PMLR publication and explains the version/normalization limits.
No claim of novelty or first priority is made.

## New exact diagnostics and input provenance

The new standard-library checker passes identically in normal,-O,-OO
modes. It checks6,724 exact covariance/comparison pairs on82 rational
unit vectors,240 rational spectral projectors,1,200 corrected witnesses,
1,800 exact Chernoff exponent identities, and six conservative
fixed-parameter domination certificates. Seventeen targeted controls
pass per mode,51 in total. Controls detect reversed variance invariance,
incorrect comparison direction, wrong correction/normalization, a
rare-event expectation failure, and rank/sign/constraint changes. These
are exact finite diagnostics, not Monte Carlo evidence or proof of
asymptotic feasibility from a finite sample. No practical finite-n
cutoff is claimed.

Before mathematics, a fresh numeric-gid43-column read-only GWS query
returned191 nonempty response rows and no exact target/source-family
lead. Additional DOI/title/source aliases were checked in that snapshot.
This bounded duplicate evidence is not a comprehensive priority proof.

The entire PR body and eight attempt files were read at head
`a152d17e5f264c596db883e73babaa58222e4c84`, against base
`6a36452c2227b071ecfdf8c88ae8feca70473247`. The complete QUEUE blob is
byte-pinned; only its relevant exact diff is reviewed. All nine blobs
and all seven entries of the nested attempt manifest match. The added
claimed_solved status is a claim under review, not evidence of correctness.
Historical39 mutation controls and original-manuscript bytes behind the
PR were not supplied as executable inputs and are not claimed reproduced.
The present diagnostics are independently authored.

Four actual source PDFs are retained privately with fresh hashes, matching
the PR's source pins: original notes, published BKW, BKWv1, and semicircle
v3. Relevant extracted pages and original130–131/published154,158 page
renders were inspected. Only the specified source sections are claimed
read; not the whole lecture books, hardness argument, or AMP proof.
Full source, ledger, and PR bodies remain private. Public receipts state
the precise imports, identities, and access limits.

This is an AI-assisted independent review. The existing paper, rather
than this reconstruction, receives the publication credit. The proposed
four literal strings have B exactly blank and include PR1314's exact URL.
No sheet, Git, QUEUE, CASE, readiness, publication, or other external state
was changed. No people or other agents were contacted. All ten earlier
own review seals, including PR1297, are rechecked unchanged. The complete
closing seal includes every own file and nested manifest, excluding only
its exact own filename.
