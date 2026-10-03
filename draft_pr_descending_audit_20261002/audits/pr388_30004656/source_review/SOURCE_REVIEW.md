# PR388 independent source, attribution and target-coverage audit

**Verdict: PASS for the scoped UNSOLVED partial-result disposition.** No
blocking attribution or target-substitution error was found. This verdict means
that the packet has not resolved the original problem and correctly describes its
restricted results. It is not a proof of present-day global open status, a
priority/novelty certificate, or a recertification of Shmalo's full proof. The
other independent reviewers are responsible for the complete proof and replay
audits. No paper or Zenodo release is recommended for this unsolved disposition.

Review date: 2026-10-02 PDT. Candidate is the snapshot under
`snapshot/problems/30004656_robustness`. All candidate files were read without
editing their contents. The independent source downloads are retained under
ignored `raw_sources/`, with receipts in SOURCE_RECEIPTS.json. This reviewer
performed no Git/index/service mutation and no external human communication.

## 1. Exact original target, reconstructed before comparing the candidate

The short OWR contribution on printed page 862 names Bubeck, Li and Nagaraj and
points to arXiv:2009.14444. It announces the conjecture rather than giving a
deterministic assertion about all interpolated data. The official report is
OWR 15/2021; EMS gives publication as 15 March 2022. Printed page 862 was rendered
and visually inspected. [OWR primary report](https://ems.press/content/serial-article-files/46893),
[EMS record](https://ems.press/journals/owr/articles/4990384).

BLN defines, for a fixed Lipschitz activation,

\[
\mathcal F_k(\psi)=\left\{x\mapsto\sum_{j=1}^k a_j\psi(w_j\cdot x+b_j):
a_j,b_j\in\mathbb R,\quad w_j\in\mathbb R^d\right\}.
\]

Conjecture 1 asks for a simultaneous lower bound on every exact interpolant of
generic random data:

\[
\operatorname{Lip}_{S^{d-1}}(f)\ge c\sqrt{n/k}.
\]

The models use uniform spherical or normalized Gaussian inputs and random signs.
The failure probability is not numerically specified. Approximate fitting is
discussed in a footnote; Conjecture 2 is a separate upper-construction question.
PDF page 3 was visually checked, including both footnotes. The candidate matches
this target. [Published BLN source](https://proceedings.mlr.press/v134/bubeck21a/bubeck21a.pdf).

The literal displayed norm is the sphere norm even when the preceding data
definition permits Gaussian points off the sphere. The candidate expressly
preserves that ambiguity. It does not use its global Gaussian result to assert
the displayed sphere-norm claim. This is an essential and correct scope choice.

## 2. Adversarial target-coverage test

The following comparison is a logical audit of the candidate's own claimed
theorems; it does not rely on an assertion that omitted cases have no proof in
all of the literature.

| Candidate result | Actual scope recorded in packet | Exact gap relative to the full target |
| --- | --- | --- |
| Turn 1 | All interpolating functions on the random circle; exact interpolation and exact distribution for the optimum | Fixed spherical dimension 2; no width-constrained attainment claim |
| Turn 2 | Fixed chart constants and dimension; geometric birthday floor for every interpolant | Not uniform as dimension grows. Only spherical dimensions at most 4 force the target for every width. Gaussian conclusion concerns a global/domain-containing norm |
| Turn 3 | All sphere functions factoring through an adaptive rank-r projection; fixed fitting accuracy, n at least 8d | Gives sqrt(d/r), not sqrt(n/r). For n/d tending to infinity the missing factor is sqrt(n/d) |
| Turn 4 | Bias-free ReLU, independent first-layer rows, k at most d, fixed fitting accuracy | Dependent rows, overcomplete widths, hidden biases and other activations are excluded |
| Turn 5 | Quadratic-on-sphere functions with rank(A) at most k, arbitrary biases/width, fixed accuracy | A special activation subclass. The Lipschitz quadratic-core realization covers units remaining in the core, not arbitrary networks for that activation |

One uncovered architecture family makes the non-exhaustion explicit: high
dimensional biased ReLU networks of width k greater than d, with n much greater
than d. Turns 1 and 2 do not supply dimension-uniform architecture-sensitive
control; Turn 3 loses the n/d factor; Turn 4 excludes the family; Turn 5 is
quadratic. Thus combining the five results is not a logical proof of the full
target. The UNSOLVED outcome is justified as an outcome of this research packet.

The partials involving fitting error at most 1/256 also apply to exact
interpolation, whose error is zero; they do not silently weaken the target on
their allowed subclasses. Parameters may be selected after observing the data,
which is explicitly covered by each relevant uniform event.

## 3. BLN credit, norm domains and circularity checks

The candidate credits the primary projection and tensor mechanisms and never
states that all five mechanisms are historically new. The relevant original
statements were checked directly:

| BLN item | Primary-source scope | Candidate treatment |
| --- | --- | --- |
| Theorem 5, pp. 7-8 | Spectral-weight upper proxy; lower proxy under zero hidden biases | Explicitly credited as a proxy; not turned into an actual sphere-norm lower bound |
| Theorem 6, pp. 8-9 | Differentiable projection factorization; global Lipschitz floor sqrt(d/k) | Turn 3 reconstructs the mechanism, supplies its sphere-fiber bridge and explicit nonsmooth/adaptive scope |
| Theorems 7-8, pp. 9-10 | Tensor/polynomial regimes; the Lipschitz conclusion is on the unit ball | Credited without replacing the domain by the sphere |
| Theorem 9, p. 11 | Homogeneous quadratic rank bound on the matrix operator norm | Credited; Turn 5 addresses radial constants before claiming an actual sphere-norm bound |

These are precisely the relevant parts of the [published source](https://proceedings.mlr.press/v134/bubeck21a/bubeck21a.pdf).
The source's introductory informal descriptions are broader than some formal
norm-specific theorems; the candidate follows the formal statements.

The radial-constant test is decisive for attribution/scope: q(x)=lambda times
||x|| squared has operator norm |lambda| but is constant on the unit sphere.
Consequently a lower operator-norm bound cannot by itself imply a sphere-norm
bound. Turn 5 explicitly uses spectral spread and a trace-zero random matrix.
It therefore does not simply relabel BLN's matrix proxy as an actual norm.

The Turn 3 lift is independently checkable: for ||u||,||v|| at most 1/2 and a
unit z in ker(P), the vectors u+sqrt(1-||u|| squared)z lie on the sphere. Their
distance is at most (2/sqrt(3))||u-v||. This avoids an off-sphere-segment argument.
Shmalo section 8 uses the same fiber-transport idea with a looser constant 2;
the candidate expressly credits that source as well as BLN. Neither an
uncertified theorem from Shmalo nor an assumption that the full conjecture is
true is a premise of the candidate proof.

## 4. Later literature and possible status/credit contradictions

Bubeck-Sellke's general parameterized theorem retains polynomial-size
parameters. Its discussion expressly distinguishes its result from the
arbitrary-weight two-layer conjecture. The candidate says exactly this.
[Primary arXiv v4](https://arxiv.org/abs/2105.12806v4).

Wu's coauthors are Heng Huang and Hongyang Zhang. Both arXiv v2 and the official
ICML record confirm them and the polynomial-weight scope of the cited
conjecture discussion. Thus the correction of the catalog's Wu-Sahai attribution
is justified. No full arbitrary-weight solution follows from this citation.
[arXiv v2](https://arxiv.org/abs/2202.11592v2),
[official ICML/PMLR record](https://proceedings.mlr.press/v202/wu23g.html).

Shmalo v1 is a real 8 July 2026 primary preprint, not merely a secondary summary.
Its Theorem 1.2 permits arbitrary coefficients, hidden biases and an affine
skip, with finitely piecewise-linear activation. On the sphere it requires d
at least 3. Gaussian model (G) uses B2 and an additional dimension/localization
condition. The principal bound has one logarithmic loss. Section 7 changes that
logarithm; sections 8-10 retain gaps for general activation and the full log-free
claim. Its sphere rigidity excludes d=2, not elementary circle geometry.
These scopes match the candidate's limited contextual use.
[Exact Shmalo v1](https://arxiv.org/abs/2607.07778v1).

The pinned author repository's supplementary-note description also says the
central multiplier estimate remains open. This confirms contextual scope only;
neither its numerical scripts nor the supplement were treated as a certificate
of a full result. [Pinned author README](https://github.com/yspennstate/law-of-robustness-two-layer/blob/6b1f35f7f70a9d98f1c0251cfb5a5dd8f0115b1f/README.md).

Primary-source search also returned restricted random-feature/NTK and
weight-bounded work. These concern smaller model classes. This audit made no
exhaustive survey/current-open certification, in agreement with the packet's
express disclaimer. No source examined contradicts acceptance of the reported
UNSOLVED outcome.

## 5. Exact frozen-source retrieval map

The candidate SOURCE_MANIFEST.json and review/SOURCE_BINDINGS.json give hashes
and file paths, not a statement that every file was fetched from its linked
proceedings endpoint. The following map supplies the missing reproduction
provenance without changing any historical binding.

| Candidate-bound name | Exact retrieval endpoint/version | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| sources/bln2020.pdf | https://arxiv.org/pdf/2009.14444v2 | 388277 | b745d68e5614af6eb0fcb57223829a465cb5775828f585bc12fd83a0da26f248 |
| sources/bln2021-published.pdf | https://proceedings.mlr.press/v134/bubeck21a/bubeck21a.pdf | 400803 | 5b0f9f36c71eb2bc29fbf029e9d63447b312879d5a10319d141bd0d49d8eadc1 |
| sources/owr2021-15.pdf | https://ems.press/content/serial-article-files/46893 | 439010 | debce92073567ab20aa8f019dc635c8baf5e09291b8076b7759454dbb2e4610c |
| sources/shmalo2026.pdf | https://arxiv.org/pdf/2607.07778v1 | 540989 | 2bd4930430b851298717540a8a6cde0cff0f2bb883d7a62ecb53489f126bfa25 |
| sources/wu2023.pdf | https://arxiv.org/pdf/2202.11592v2 | 302343 | 51100211cf9ea607f4f01e4b5d8915e75c9071c5fea60f9f879ad42fab225e62 |

All five PDF byte hashes were independently reproduced. **The frozen Wu file
is arXiv v2 under the local name wu2023.pdf.** The official proceedings PDF
at https://proceedings.mlr.press/v202/wu23g/wu23g.pdf instead has 345162 bytes and
SHA-256 d78924eb42898db89ee0a3e59c1a761d3e4d699ad5f2933d90b2f73c4cfcba53.
That byte difference is not a contradiction: both were read for the relevant
author/weight-scope facts. Downloading the official PDF and naming it wu2023.pdf
will intentionally fail the frozen optional raw-source check.

The sixth frozen source item, sources/printed862.png (299842 bytes;
SHA-256 7766db51bcb2eb27832e139b08338423aecc5642ee43681739b0092e36efe4d4),
is a **noncanonical rendered image**, not a directly downloadable source PDF.
The author manifest does not provide its renderer/options. This review rendered
page 10 of the official OWR PDF and visually verified printed page 862; it makes
no claim of reproducing the historical PNG byte hash. Renderer/version/options
can alter pixels and bytes while leaving the source page identical. The ordinary
public proof/review replay requires no raw PDFs or PNG, so this does not obstruct
it. For optional exact-source replay, preserve the historical image bytes or
supply its exact historical rendering recipe; do not pretend an arbitrary new
render must match its hash.

## 6. Disposition and remaining limits

No mandatory mathematical repair or source-attribution correction is requested
by this review. The additive deterministic-chaining clarification already in the
candidate remains required for the Turn 4 theorem; this source review does not
supersede that requirement. The parent audit should treat the present conclusion
as a source/scope PASS alongside its independent proof and replay checks.

Accept the PR as an unsolved partial-results package if those checks pass.
The strongest outcome here is the specific collection of scoped partials; the
exact remaining central gap is arbitrary activation/parameters in the growing
dimensional sqrt(n/k) law. Do not label this as a solved original conjecture,
novelty certification or externally peer-reviewed result. Audit completion:
100% for the assigned source/attribution/coverage scope, 0% claim to an exhaustive
current-open or full-solution-priority audit.
