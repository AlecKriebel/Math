# Verification, source scope, and priority supplement

Companion to *Full stress stratifications determine a labelled graph*, Alec
Kriebel, 12 October 2026. Independent AI reviews and retrievals took place
12 October PDT / 13 October UTC. This is authored verification material for an
unrefereed preprint, with extensive AI use; it is not human peer review.

## Exact claim and success criteria

For every positive integer n and d, take a simple graph on the common labelled
vertex set [n]. Its base is all of (R^d)^n. The stress fibre has one real weight
per unordered edge and the symmetric equilibrium equations. Fibre equivalence
means a homeomorphism preserving each coordinate's positive, zero and negative
sign. A stratum is a connected component of an equivalence class. The theorem
recovers the edge set from this partition: a pair is an edge if and only if its
collision diagonal is a union of entire strata. Thus two such partitions are
equal as collections of subsets exactly when their labelled graphs are equal.

The original primary question is Problem 4, printed p.22, in O. Karpenkov,
*Open Problems on Configuration Spaces of Tensegrities*, Arnold Math. J. 4
(2018), 19–25, [DOI](https://doi.org/10.1007/s40598-018-0080-7). Definitions
1.1–1.3, printed p.20, fix the full Cartesian space and connected sign strata;
the adjoining examples explicitly include collisions. The problem asks which
subgraphs of K_n define the same stratifications. It gives no separate
cross-graph abstract or ambient equivalence. We completely answer literal
equality of the defined partitions, and explicitly identify this as the
comparison used. This source reading does not certify the author's unwritten
intent or every possible meaning of “same.”

The source's redundant n-by-n stress-array convention gives the same data:
nonedge entries are zero, and the two entries for an unordered edge agree.
Our edge coordinates remove this fixed redundancy without changing signs.

## Proof mechanism and attempted falsification

A present edge admits a positive stress supported only on that edge precisely
when its endpoints coincide. A sign-preserving homeomorphism preserves the
existence of that support. Its collision diagonal is therefore a union of
equivalence classes and hence of connected strata. This is a known observation
of Panina, not a new stress detector.

For a missing edge ij, place i at t a and j at 0, with nonzero a, and all other
vertices at distinct scalar positions at least 2 times a. For t in [-1/2,1/2],
no actual graph edge collapses. The equilibrium operator is an incidence
matrix B times the diagonal D_t of oriented scalar edge differences. Positive
diagonal transport D_t^(-1)D_0 is invertible and carries the stress kernel at 0
onto the kernel at t, preserving all coordinate signs, including zero.
The entire continuous path is inside one equivalence class, so its connected
image is inside one stratum. It contains a point in the missing pair's
collision diagonal and a point outside it. That diagonal is not a union of
whole strata. Endpoint equivalence alone would not suffice; the proof uses
the full path and connected-component argument.

Independent review checked orientation changes, all symmetric endpoint
forces, the direction of the length ratio, both inverse maps, n=1, n=2, empty
and disconnected graphs, forests and dense graphs, deficient affine spans,
and preservation of zero coordinates. Positive dimension and graph simplicity
are explicit assumptions. No result is asserted for loops, parallel edges,
d=0, deleted collisions, generic-only domains, or arbitrary ambient comparison.
For K3 on a line, one pair collision and separation have the same stress
dimension one but different support; dimensions cannot replace coordinate
sign information. This also isolates an arithmetic slip in a source example
without using it as a premise of the proof.

The path/star boundary is independently checkable. For the path 12,23,34 and
star 12,13,14, set q1=p1, q2=p2, q3=p1+p3-p2, q4=p1+p4-p3. Its inverse is
p1=q1, p2=q2, p3=q2+q3-q1, p4=q2+q3+q4-2q1. The three corresponding edge
differences agree. Leaf elimination shows that any forest stress is supported
only on collapsed edges, with independent arbitrary weights there. Hence this
map identifies full fibre classes and connected strata of these nonisomorphic
trees, despite their unequal partitions in the original fixed labelled base.
The note therefore does not claim uniqueness under arbitrary ambient linear
equivalence or homeomorphism.

## Priority and primary-source credit

The partition and coordinate-sign conventions originate in Doray, Karpenkov
and Schepers, *Geometry of configuration spaces of tensegrities*, Discrete
Comput. Geom. 43 (2010), 436–466,
[DOI](https://doi.org/10.1007/s00454-009-9229-4),
[author preprint v2](https://arxiv.org/abs/0806.4976v2). The final journal's
relevant numbering is Definition 2.7, Theorem 2.10 and Lemma 2.12; the preprint
numbering differs. Both bodies were inspected. Their surgery comparisons
require particular graph/configuration hypotheses and do not state the full
partition reconstruction proved here.

G. Panina, *A universality theorem for stressable graphs in the plane*, Ars
Math. Contemp. 18 (2020), 137–148,
[DOI](https://doi.org/10.26493/1855-3974.641.e06),
[author preprint v4](https://arxiv.org/abs/1902.07212v4), already supplies the
collapsed-edge singleton detector in published Lemma 3.1 / preprint Section 3,
Lemma 4. Published Appendix A.3 / preprint Section 4.1 observes collinear
vertex-order invariance of the stress matroid. Strong/weak equivalence is also
prior machinery (published Proposition 3.2 / preprint Proposition 4). The note
does not claim a new equivalence theorem or priority for these ingredients.
Panina's affine-quotient/noncollapsed-edge framework elsewhere is not
substituted for the full Cartesian space in the present theorem.

Incidence normalization on the line is elementary established machinery;
the independent priority audit also inspected Section 2 of Clay, Jordán and
Tóth, *Minimally Rigid Tensegrity Frameworks*,
[DOI](https://doi.org/10.1007/s00454-025-00786-7), published online in 2025.
The contribution evaluated here is the full-partition reconstruction
consequence combining the known detector with a connected path for a nonedge.

The independent priority search used 54 exact-question, reconstruction,
partition, collision, sign-equivalence, collinearity and citation-chain queries.
It inspected original bodies across the 1983 White–Whiteley pure-condition
paper, DKS preprint/final journal, KSS preprint, Karpenkov's problem paper,
2016 handbook author draft and 2015/2021 geometric-condition paper, Panina
preprint and published text, and later stress papers through September 2026.
The evidence folder contains its complete query log, source-access record,
report and verdict. No earlier exact full-partition reconstruction theorem
was located. This is a bounded search, not a proof of originality. It leaves
the final KSS journal body and final handbook chapter uninspected (earlier
bodies were inspected), varying terminology and all-language coverage gaps,
and original author intent unverified. No external inquiry was prepared or
initiated.

White–Whiteley's 1983 p.505 Remark 3 concerns reconstruction from equal
pure-condition polynomials for generically isostatic graphs. That conjecture
compares different data and is not resolved by this note. No first-priority
claim is made for the cited ingredients or an exhaustive novelty guarantee
for the reconstruction consequence.

## Executable verification and provenance

The original submitted head was f333d06cc161b1b8ae8422bf413ed1ffae31e614,
[PR #1001](https://github.com/AlecKriebel/Math/pull/1001), catalogue problem
6900004. Input snapshots and hashes are preserved separately from fresh review
findings. Earlier interpretation holds are retained as history; independent
source reconciliation supported promoting the precise literal theorem to the
new full-resolution workflow. The stale QUEUE label did not certify an outcome.

`check_collision_witness.py` checks exact equilibrium-column identities,
positive invertibility, distinguishing singleton supports, all unordered
different graph pairs through n=4, all missing edges through n=4, selected
larger families and explicit negative controls. `independent_kernel_check.py`
constructs kernels by incremental constraint intersection and independently
tests both transport directions, cycle nullity and sign supports.

`independent_exact_check.py` was written by a fresh reviewer without reading or
importing either submitted checker, historical audit, or other current review
findings. Its exact row reduction and matrix checks cover all 1,099 simple
graphs through n=5, 5,325 missing-edge witnesses, 71,280 transport/singleton
case checks, and 24 ambient path/star tests. The accompanying input manifest
records that provenance and limitations.

The package runner executes all three programs in normal, -O and -OO modes
and requires all mathematical JSON fields to match the pinned references.
Execution requires Python 3.10 or later on a POSIX system such as macOS or
Linux: the unchanged kernel checker calls the POSIX API `os.getuid()`.
The recorded fresh package executions used macOS with Python 3.14.6; exact
current environment identity is in `evidence/EXECUTION_ENVIRONMENT.json`.
It separately records execution UID and verifies optimization mode. Six actual
source mutations are then executed in every mode: reverse or omit the length
ratio, negate it, erase the zero sign distinction, replace the singleton
witness by zero, and use the same force sign at both endpoints. Each must exit
with the specified mathematical rejection and empty stderr; a syntax error
or unrelated crash does not count. These are actual altered source programs,
separate from the programs' built-in negative controls.

Original reference files reported UID1000. Fresh root execution reports UID501.
Full raw outputs and the expressly separated environment fields are retained.
No claim is made to replay the historical UID1000 permission-control harness.
The package runner's isolated interpreter flags are not a general security
sandbox. All arithmetic is exact rational, with no tolerance or floating point.

Finite calculations corroborate explicit formulas and expose selected defects.
The written proof establishes universal quantifiers and connectedness.
No formal proof-assistant certificate, source-intent determination, novelty
certificate, conventional human peer review or journal acceptance is claimed.

## Publication review gate

Before immutable upload, the complete manuscript, metadata, supplement and
verification package undergo fresh adversarial review. Every actionable issue
must be fixed across all corresponding artifacts, followed by another new
reviewer. The final acceptance record and reviewer reports are added to the
evidence set before publication. Earlier staged review records retain their
stage-specific limitations; they are not rewritten as independent priority
or human review certificates.

The published deposit and tracker entry must say **literal equality of full
fixed-labelled connected sign partitions**, retain collision inclusion, credit
known ingredients, and retain the unrefereed/extensive-AI disclosure.

The [portable evidence index](evidence/README.md) maps stage-specific names and
historical machine-local paths to the included records. Original reports and
input pins remain unchanged; omitted raw source bodies are explicitly marked
as provenance records with public primary URLs, not included archive files.
