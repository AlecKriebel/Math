# Complete bounded adversarial review: Irreducibility of exposed-point varieties of discotopes

The complete actual four-page manuscript survives this independent adversarial review. I found no mathematical counterexample or indispensable unsupported step in either universal exposed-point irreducibility (Theorem 1) or the stated GP equality theorem (Theorem 4). This is a bounded assessment with no promotion authority. Historical first priority remains unproved; that is different from a mathematical defect, and the manuscript does not assert first priority.

## Target, edition and independence

The target is row 91, Zenodo record 23074543, DOI [10.5281/zenodo.23074543](https://doi.org/10.5281/zenodo.23074543), version 1.0. I read all four actual PDF pages through complete layout-preserving text extraction and the complete controlling `sources/published-source/paper.tex`. The historical `verification/source_snapshot/proof.tex` was not substituted for the current paper, and historical review/priority opinions were not read. Current root, scope, analytic or sibling review opinions were not read. Another worker supplied only raw cited-primary paths/hashes after my substantive early independence seal.

Actual PDF: 79,805 bytes, SHA256 `c13dc861e8e5b5c1d980bdd78d14aff8e4b1a130800c4f942b3bedafbc5f6b2a`. Actual source ZIP: 692,895 bytes, SHA256 `55941d26dbadc3b244a6ba191e9e4503201c0deb3e2cde43178d5f0799564027`. Controlling TeX SHA256: `3576dcc78bf1a9188ee8a8b5c56f5914357d90d437767e29dc42e3a85ceedab4`. `ORIGINAL_BINDING_RECEIPT.json` independently rehashes all 97 source-ready objects and reads all 87 ZIP members with CRC validation and exact equality to the frozen extracted originals. No original code was run and no original was altered or repacked.

The PDF and metadata declare September 30, 2026. Record creation is October 1, 2026 at 04:23:09.001448 UTC, which is September 30 at 21:23:09.001448 in America/Los_Angeles. These timestamps are consistent as dates; the declaration itself is not independent priority certification. The record's updated timestamp is October 10, 2026. The review is bound to the supplied fresh current bytes, not to an unsupported assertion that these bytes were immutable since initial creation.

`EARLY_LEDGER.md` was made read-only and sealed before external primary mathematical bodies were read: ledger SHA256 `ccb8ca132f4156da95fc089fd47157b11e54c6c36254df8bfa13cc3ede13e443`; `EARLY_SEAL.json` SHA256 `7d2f1a1698c7146af31c3b857df8e0e3d6b2d1420751acf645ba125b4593d0a4`. It fixed seven distinct attack families. The final mechanism/evidence/gap mapping is `ATTACK_LEDGER.md`.

## Independent reconstruction of Theorem 1

The literal claim concerns a finite sum of centered ellipsoidal balls, each of actual span dimension at least two. Write each as `D_i=A_i B^{m_i}` with injective `A_i`, and put `Q_i=A_i A_i^T`. This representation is available for every disc in the definition by restricting to the nonzero singular directions; it does not require an orthonormal ellipsoid matrix.

For each real normal `u`, maximizing `u^T A_i v` over the unit ball is the elementary Cauchy-Schwarz maximization. If `A_i^T u != 0`, the only maximizer is

`p_i(u) = A_i(A_i^T u)/||A_i^T u|| = Q_i u / sqrt(u^T Q_i u)`.

If `A_i^T u=0`, every point in `D_i` maximizes. The face exposed by `u` on the sum is exactly the Minkowski sum of the individual faces: the difference between the sum of support values and the support value of a chosen decomposition is a sum of nonnegative deficits, so equality forces every deficit to vanish. A sum of nonempty faces is a singleton exactly when every face is a singleton. To see the nontrivial direction, fix one point in every other face; adding them translates a nonsingleton face injectively into the total face. Nonunique decompositions cannot defeat this argument.

Consequently the *exact* exposed-point set is `F(U)`, where

`U = R^d \ union_i ker A_i^T`, and `F(u)=sum_i p_i(u)`.

Every excluded kernel has codimension `m_i>=2`. A finite union of proper linear subspaces cannot exhaust real space, as witnessed by a product of nonzero vanishing linear forms. For any two points `x,y` in the complement, choose `z` outside all the proper subspaces `ker A_i^T + R x` and `ker A_i^T + R y`. They have dimension at most `d-1`. An intersection of the segment from `x` to `z` with a forbidden kernel would force `z` into its corresponding enlarged subspace; likewise for `y`. Thus `U` is nonempty, open and path connected. Zero is excluded, so every normal used is nonzero, including when the total sum is in a proper ambient span.

On `U`, every radicand is strictly positive. The ordinary positive real inverse square root is real analytic on `(0,infinity)`, so `F` is real analytic throughout this real connected domain. No complex continuation of an individual radical is needed.

Let `I` be the ideal of complex polynomials vanishing on `F(U)`. It is proper because `F(U)` is nonempty. If `P Q` lies in `I` but `P` does not, continuity gives a nonempty open set on which `P o F != 0`. There `Q o F=0`. The real and imaginary parts of `Q o F` are real analytic; the real-analytic identity theorem on connected open `U` makes both identically zero. Therefore `I` is prime, and the complex Zariski closure is irreducible.

All universal quantifiers are accounted for. There is no dependence on the differential rank of `F`, injectivity, independence of quadratic radicals, genericity, distinctness of spans, or full dimensionality. For example, two identical rank-two discs in a larger ambient space simply have a scaled conic as their exposed-point closure. For a single rank-two disc, the complex conic is irreducible: a factorization into affine linear factors would homogenize to a rank-at-most-two quadratic form, whereas the homogenized circle quadratic has rank three. These boundary cases are consistent with the general proof.

## Independent reconstruction of Theorem 4 and genericity

The target `S` uses the *relative* boundary in each summand span, followed by intersection with the ambient boundary of the full-dimensional total sum. Every exposed point is a sum of its unique summand support points, each on its relative boundary, so `E` is contained in `S` after taking complex Zariski closure.

Conversely, take a generator `x=sum_i x_i` of `S` with each `x_i` on its relative summand boundary. A nonzero supporting normal `u` exists because `D` is a compact full-dimensional convex body and `x` is on its boundary. Adding support deficits forces every `x_i` to maximize `u` on `D_i`. Let `J` be exactly the indices for which `A_j^T u=0`. All other `x_i` are `p_i(u)`.

The sum of the spans in `J` lies in `u-perp`, so its dimension is at most `d-1`. GP then forces the sum of the individual dimensions in `J` to be at most `d-1` as well: otherwise GP would give dimension `d`, a contradiction. GP further says the actual dimension is their sum. Thus the concatenated `A_J` has independent columns and its transpose is onto the product of the coordinate spaces.

Since `A_j` is injective, there is a unique unit `v_j` with `x_j=A_j v_j`. Surjectivity supplies a common real vector `w` satisfying `A_j^T w=v_j` for all `j` in `J`. For positive `epsilon`,

`A_j^T(u+epsilon w)=epsilon v_j`, hence `p_j(u+epsilon w)=A_j v_j=x_j`.

For every other index the transpose product remains nonzero for all sufficiently small epsilon and its support point converges to `p_i(u)=x_i`. The finite number of summands supplies one common epsilon bound. Therefore these perturbed normals are in `U`, and the exposed points `F(u+epsilon w)` converge to `x`. When `J` is empty, `x` is exposed already. A complex algebraic set is Euclidean closed, so every generator of `S` lies in `E`; closing yields `S=E`. No orthonormality assumption was used.

For every subset of blocks, failure of maximal concatenated rank is a determinantal algebraic condition. There are only finitely many subsets. To see the union of the failures is proper *simultaneously over the reals*, choose distinct real values `t` and columns `(1,t,...,t^{d-1})`, then partition them into the prescribed block sizes. Every collection of `r<=d` columns is independent: use its first `r` rows and the Vandermonde determinant `product_{k<l}(t_l-t_k) != 0`. Larger collections contain `d` independent columns. This gives GP for every subset at once. If the total number of columns is at least `d`, full dimensionality follows. Otherwise a generic concatenation is independent and one restricts to the total span, where GP is the direct-sum condition. There is no hidden nonexistent-generic-type exception.

## Exact diagnostics and adversarial controls

`checks.py` was read before execution and uses only the existing shared Python/SymPy runtime. Its original package is never imported or executed. `EXACT_CONTROLS.json` records Python 3.12.14 and SymPy 1.14.0. Every exact assertion passed.

The non-orthonormal perturbation control uses three rank-two maps in R5:

`A1=[(2,0,0,0,0)^T,(1,3,0,0,0)^T]`,

`A2=[(0,0,1,0,0)^T,(0,0,2,2,0)^T]`,

`A3=[(1,1,1,1,1)^T,(2,2,2,2,3)^T]`.

Each pair has concatenated rank four and the triple has rank five. For `u=e5`, both first maps are annihilated. The unit targets `(3/5,4/5)` and `(5/13,12/13)` are realized simultaneously by

`w=(3/10,1/6,5/13,1/13,0)`.

The support formulas for both annihilated blocks are symbolically constant at the prescribed boundary points for all positive epsilon; the third converges to its original support point. This control detects replacing `A_j^T w=v_j` by an inappropriate primal condition, and treating multiple annihilated blocks independently without a joint rank argument. A second rational Vandermonde control checks all seven nonempty block subsets for sizes `(2,3,4)` in dimension five. The universal rank proof is the determinant argument above, not this finite check.

The manuscript's repeated-xy-disc separation is valid. At normal `e3`, its support face is the translate of the radius-two xy-disc by `e3`, and `e3=e1+(-e1)+e3` is a sum of relative boundary points. For regular normals let `a=2u1/sqrt(u1^2+u2^2)`, `b=u1/sqrt(u1^2+u3^2)`. Then `X=a+b`, `a^2+Y^2=4`, `b^2+Z^2=1`. Substitution makes the quartic residual exactly zero, while its value at `e3` is exactly sixteen. Hence `e3` lies in `S` and outside the entire Zariski closure `E`. A deliberately wrong coefficient in the quartic gives residual `3 a^2 b^2`, which is nonzero at `a=b=1`; the checker detects it. Repeated identical xy maps with opposite target coordinates also give a constraint matrix of rank two but augmented rank three, exposing exactly why the GP perturbation cannot be used indiscriminately.

Two conceptual negative controls isolate essential hypotheses. On the disconnected open domain `R\{0}`, the analytic map `sign(t)` has reducible closure `{−1,1}`. On connected R, define the smooth flat function `g(t)=exp(-1/t^2)` for `t>0`, zero otherwise. The smooth map `(g(t),g(-t))` has Zariski closure the union of the two coordinate axes, which is reducible. Thus connectedness alone and smoothness alone would not justify the analytic lemma. The manuscript uses both needed conditions. Its rank-one interval and stadium controls are also correct: the stadium has two distinct complex circle components, with the open semicircle arcs Zariski dense in their respective conics.

Reproduction without overwriting frozen evidence: load `checks.py` with Python `runpy.run_path`, call its `diagnostic_checks()` function and print the returned dictionary. Calling `custody()` similarly repeats the complete original binding and ZIP checks without writing. The default script entry point intentionally refuses to overwrite the retained evidence files.

## Primary interfaces and bounded novelty

The [Gesmundo–Meroni arXiv v2 journal-version copy](https://arxiv.org/abs/2111.01241v2) defines the same `S` in Definition 3.3, uses bases as its generic parameter space, and allows restriction to the total span. Theorems 4.3/6.1 and Remark 3.4 match the credited special cases; Section 5 already uses support gradients; Conjecture 8.2 is the generic `S` irreducibility claim. The independent publisher-PDF request timed out, so no byte-level equality with the publisher edition is asserted.

The actual [Oberwolfach report](https://ems.press/content/serial-article-files/47009?nt=1), printed p.830, defines `E` from exposed points and states the generic all-ranks-at-least-two conjecture. The actual [Kucharz–Kurdyka institutional PDF](https://dspace.uni.lodz.pl/bitstream/handle/11089/23776/W.%20Kucharz%2C%20K.%20Kurdyka%2C%2085-96.pdf?isAllowed=y&sequence=1), p.95, records analytic-image real Zariski irreducibility in the proof of Proposition 4.3. The manuscript acknowledges that precursor. `PRIMARY_INTERFACES.json` binds the raw files and independently generated ignored extractions.

These checks support the manuscript's positioning relative to its three cited primary sources. They do not establish an exhaustive absence of earlier equivalent results or later resolutions. The independent conclusion is that the elementary analytic lemma is a credited known ingredient, the support-gradient idea is also credited, and the manuscript's surviving contribution is their use to prove the complete literal irreducibility statement and the GP identification. No specific bibliographic omission was discovered, and unknown historical priority is not being promoted into a defect.

## Disposition

Strongest surviving original result: Theorem 1 in full stated generality, Theorem 4 under full dimensionality and GP, the GP nonemptiness proof, and the exact distinction/necessity examples. No substantive mathematical gap was found; no theorem repair or narrower replacement was undertaken. The prescribed defer-and-move-on rule for a substantive defect therefore has no trigger from this worker's findings. Root retains catalogue disposition authority.

The review is complete within this bounded assignment; the 203-paper goal remains ongoing. Remaining limits are historical-priority exhaustiveness, independent human refereeing/formal certification, and the publisher-byte acquisition limitation already stated. No external contact or outreach draft occurred, no new environment was installed, and no shared source, configuration, public catalogue/site, UI, branch, commit, push, release or deployment was changed by this worker. All authored files are inside this new adversarial namespace, and complete foreign texts remain only in preignored caches.
