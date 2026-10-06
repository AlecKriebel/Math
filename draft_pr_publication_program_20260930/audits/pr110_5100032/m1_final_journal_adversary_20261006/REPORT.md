# Independent final-journal priority adjudication: PR110 / 5100032

**Conclusion:** the supplied complete journal final does not state or prove the submitted all-period focal antipedal equality, does not cite a proof of that equality, and its spatial-average mechanism does not establish the required finite odd-period identity. This closes the missing-final source hold for this particular comparison. It supplies bounded clearance against this paper, not a claim of novelty or a comprehensive priority clearance.

## Exact comparison and source envelope

The submitted claim fixes an outer ellipse with semiaxes `a>b>0`, foci `(±c,0)`, and a strictly nested confocal elliptical caustic with `0<lambda<b^2`. For each directed chord `AB`, `Q_sigma` is the intersection of the lines through `A,B` perpendicular to their respective focal radius vectors, and `q_sigma=|Q_sigma-f_sigma|` is an ordinary positive norm. The claim is `sum q_+=sum q_-` for every regular closed orbit, including odd primitive periods and star orbits on one tangent branch. Its proposed bridge is `q_+-q_-=Gamma(y_B-y_A)` with a coefficient fixed by the ellipses. It does not claim either individual sum is invariant through the Poncelet family.

The final is Garcia, Koiller, Reznik, *Estimating Elliptic Billiard Invariants with Spatial Integrals*, [DOI 10.1007/s10883-022-09608-y](https://doi.org/10.1007/s10883-022-09608-y). The supplied PDF has 11 pages, 1,150,664 bytes, SHA-256 `8df802b8b6255aae648934fd83aab4079a5d6b4c66382a9b1b26a6cd3237eac3`. PDF p.1 records receipt 9 November 2021, revision 7 April 2022, acceptance 24 June 2022, and online publication 10 August 2022. Page references below are PDF ordinal pages because this supplied final has no ordinary article page numbers.

I independently read its complete layout extraction and visually inspected every page, including all definitions, numbered equations, theorem statements, table rows, figures, questions, and references. I also read and visually inspected all 9 pages of Koiller, Reznik, Garcia, *Average Elliptic Billiard Invariants with Spatial Integrals*, [arXiv:2102.10899v1](https://arxiv.org/abs/2102.10899v1), dated 22 February 2021 in the margin. That precursor is 582,323 bytes, SHA-256 `18fb6887aac5137b54a72baa802d698a40ab6b3ea93ce3404e10d3faf2ebd5a0`. The printed January 2020 date inside the precursor must not replace the authenticated arXiv version date.

For the journal's two main proof citations I independently read the complete local primary PDFs of [Akopyan, Schwartz, Tabachnikov](https://doi.org/10.1007/s40879-020-00426-9) (15 pages) and [Bialy, Tabachnikov](https://doi.org/10.1007/s40879-020-00428-7) (14 pages). These were text reads; I do not claim all-page visual review of those two ancillary papers. No earlier audit conclusion was used as a premise.

## Complete page and mechanism mapping

| Final location | Result or definition checked | Consequence for the exact claim |
|---|---|---|
| pp.1-2, introduction and §1.1 | Integrals of motion; Poncelet closure; aim of computing aperiodic averages | Shared billiard geometry. No statement about antipedal norms. The dependence-on-integrals footnote is not a theorem that arbitrary finite sums are constant. |
| p.3, §2 and Table 1 | Confocal ellipses and `J=sqrt(lambda)/(ab)`; rows for perimeter, cosine sum, curvature two-thirds sum, outer cosine product | Table has four mathematical rows despite its three-invariant caption. None is `k603`, a focal antipedal sum, or a difference of two such sums. |
| p.4, equations (1)-(3), §2.1 and Fig.3 | Endpoints of a caustic tangent; asymptotic average; translation coordinate with measure `kappa_c^(2/3) ds` | Supplies chord coordinates and an invariant measure. Fig.3's external vertex is an intersection of outer-ellipse tangents, not the intersection of lines perpendicular to focal radii. |
| p.5, equation (4), §2.2 | Spatial integral for the aperiodic average; curvature and elliptic integral definitions | This is an asymptotic averaging rule, not a finite rational-orbit quadrature theorem. |
| pp.5-6, §3, Theorem 1 and Fig.4 | Average sidelength, compared with `L/N` | No focal quantity or finite norm-difference identification. Fig.4 compares selected non-intersecting periods numerically. |
| pp.7-8, §4, Theorem 2, equation (5), §4.1 and Fig.5 | Average cosine; independently known finite identity `sum cos(theta_i)=JL-N` | The focal radii `d1,d2` occur through their product at one outer vertex. They are not the two-endpoint radius product divided by focal side height needed for an antipedal vertex. |
| pp.8-9, §5, Theorem 3, equation (6) | Average outer curvature to the two-thirds power; finite curvature invariant cited as a cosine corollary | Different summand. The precursor already contains the curvature corollary. No antipedal reduction. |
| p.9, §6 | Outer tangential-polygon cosine product, log of absolute cosine, spatial average | Tangential outer polygon differs from focal antipedal polygon; a product of cosines differs from a sum of ordinary focal norms. The final's all-`N` proof citations here are for this cosine product. |
| pp.9-10, §7 and Fig.6 | Questions on cosine proximity, hyperbolic caustics, and area invariants | No unprinted antipedal extension; numerical comparisons shown concern selected non-intersecting orbits. |
| pp.10-11, complete references | All 20 references and their uses checked | No citation identified as a proof of `k603`. Reference [18] is the experimental invariant list, rather than a new proof asserted by this final. |

The actual cited finite proofs are AST Theorems 1.1/2.4 (cosine sum), 1.2/5.1 (outer cosine product), and 1.3/§7 (odd-period area ratio), and BT Corollary 3.2 and Theorem 3.3 (cosine sum/product). AST's variants in §6 do not identify focal antipedal norms. BT Theorem 4.1 concerns squared distances to feet on the *vertex tangent lines*. BT Lemma 4.2, printed pp.1349-1350 (PDF pp.9-10), gives the product of the two focal *side heights*. BT Theorem 4.3 gives different focal pedal products for even periods, and an origin-distance product when the period is divisible by four. None states the all-period ordinary antipedal radial-sum equality. BT's side-height lemma is relevant background, but the missing two-endpoint antipedal calculation remains necessary.

## Why the spatial rule does not give odd-period equality

Normalize the Poritsky coordinate to `x mod 1`. The map is a rotation `T(x)=x+tau`. For an irrational `tau`, the spatial average of a continuous function is its orbit average. For rational `tau=p/N` in lowest terms, the orbit average is instead

`S_N(g,x)=(1/N) sum_{j=0}^{N-1} g(x+j p/N)`.

The spatial mean is the average of `S_N` over starting phase `x`; it need not equal every `S_N(g,x)`. For example, for any odd `N>=3` take positive analytic functions

`g_+(x)=2+cos(2*pi*N*x)`, `g_-(x)=2-cos(2*pi*N*x)`.

Both spatial means are 2. They swap under `x -> x+1/2`, as focal quantities do under central inversion. Yet along `T(x)=x+p/N` their finite sums differ by `2N cos(2*pi*N*x)`, which equals `2N` at `x=0`. Thus equal spatial averages, positivity, and half-turn focal interchange together still do not force finite odd-period equality. This is a counterexample to the proposed *generic inference*, not a counterexample to the geometric antipedal theorem.

The same example rules out transferring by continuity from irrational rotation numbers: the infinite-time averages are 2 on irrational rotations approaching `p/N`, but the `N`-step average at the limit phase `x=0` is 3 or 1. The long-time limit and the rational-parameter limit cannot be interchanged without additional information. For primitive even periods, half-turn pairing can provide cancellation; that argument does not settle odd primitive periods or repetitions of them.

There are two sufficient bridges: independently prove that the finite difference sum is constant over starting phase and then integrate that constant, or exhibit a coboundary `q_+-q_-=H(B)-H(A)`. The submitted proof uses `H(P)=Gamma*y(P)`. The journal does neither for this summand. Its endpoint formulas allow a fresh antipedal calculation to be attempted, but geometric data sufficient for a new derivation do not constitute an earlier published proof of that derivation. In particular, no identification of an antipedal norm with a journal cosine/curvature invariant has been supplied.

## Actual version changes and transfer cautions

The final changes title and author order, expands the classical/history discussion, replaces the precursor's description of the map as an involution with a translation-linearization account, and explicitly cites Birkhoff for the averaging step. It splits preliminaries into §§2.1-2.2; promotes the existing sidelength and cosine formulas to Theorems 1-2; separates the already-present curvature discussion (precursor p.7) into §5, adds its explicit Theorem 3/equation (6), and adds the curvature row to Table 1. It relabels Fig.6's horizontal axis from `b_c=1-lambda` to `b_c=sqrt(1-lambda)` when `b=1`, removes the question about an outer-ellipse universal measure, and adds references and context to the remaining hyperbola/area questions. These are real changes; none introduces focal antipedal distances or an all-period transfer theorem.

Two formula cautions were verified independently rather than treating the final as automatically error-free. The final p.7 (precursor p.5, equation (7)) prints `cos(theta)=lambda/(2 d1 d2)-1` alongside `J=sqrt(lambda)/(ab)`. With the stated reflection law and this `J`, the value is `2 lambda/(d1 d2)-1`. For `a=3,b=2,lambda=1` and a tangent chord with endpoints `(sqrt(8),±2/3)`, `d1*d2=41/9` and the reflection angle gives `cos(theta)=-23/41`; the printed formula gives `-73/82`. Also the final p.8 and precursor p.7 curvature chain adds a trailing `-1` to the curvature expression; the exact geometric relation is `kappa^(2/3)=(ab)^(-4/3)(1+cos(theta))/(2J^2)`. This audit does not attempt a full repair of the paper's average formulas. The defects are inherited or ancillary to this priority verdict, which remains unchanged even granting the intended averaging results.

The earlier local object named `GKR_spatial_final.pdf` is HTML, 291,790 bytes, SHA-256 `7194e38a4706e3b3e140aaa2dbbdc47cc25a9e414794a79da3bc2bb04d7caf43`. It cannot authenticate a full final PDF read. The newly supplied eleven-page PDF resolves that precise source-access issue. Its copyrighted body, extraction, and images remain private and are not part of this public payload.

## Bounded disposition and reproducibility

**Candidate survives this final-version comparison.** No complete covering theorem was found in the final, its precursor, or the two explicitly invoked primary proof papers. This is not an independent full verification of the submitted candidate proof, not a claim that the target remains open globally, and not first-proof attribution. The broader literature remains outside this narrowly assigned comparison.

`INPUT_PINS.json` binds all actually read primary inputs and private source derivatives; `VERIFICATION.json` records the actual normal and optimized runs. `verify.py` checks full-byte pins, the exact rational-rotation obstruction, and the reflection/curvature consistency control using rational arithmetic. `OUTPUT_MANIFEST.json` binds every public payload file by full bytes; `SEAL_RECEIPT.json` binds that manifest after final verification. No Git mutation, outside communication, release, or publication was performed.
