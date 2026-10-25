# Independent analytic review: Zenodo 22770864, version 1.1.0

Review date: 24 October 2026 Pacific / 25 October 2026 UTC.

## Verdict and strongest supported claim

**No mathematical defect was identified in the stated theorem.** The published proof, its exact computational certificate, and a fresh reconstruction of the bracket data support the existence of the explicitly specified finite group

\[
G=\operatorname{BCH}(L/1009^{1689}L),\qquad
|G|=|\operatorname{Aut}(G)|=1009^{52359}.
\]

Here `Aut` denotes the full automorphism group. The stronger intermediate statement checked is

\[
|\operatorname{Aut}_{\mathrm{Lie}}(L/p^iL)|=p^{30i+1689}
\quad(p=1009, i\ge7).
\]

This is an AI-assisted analytic review with exact computation, **not external human peer review, proof-assistant formalization, or a novelty/priority certificate**. No unresolved mathematical gap was found within this review's scope. The paper still requires independent human scrutiny before it can be represented as a community-confirmed resolution.

The current Kourovka Notebook explicitly lists this manuscript at Problem 16.63 as an **unverified AI solution**. Its preface says that problems with that designation remain unsolved pending human confirmation. A public landing page should preserve that distinction. [Current notebook, printed pp. 4 and 106](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21tkt-3.pdf).

## Exact artifact and independence

- Title: *An explicit odd-order p-group with as many automorphisms as elements*.
- Edition: version 1.1.0, 15 September 2026; DOI `10.5281/zenodo.22770864`.
- Published PDF SHA-256: `9d94db98b4b599a176e95bc74ae8048f69db81d852cf8d557e22f2191c298248`.
- Source ZIP SHA-256 supplied with intake: `33560d8879bbe3df578f92a8e6311010e504b7d2b669af6678163a7c8f96a7a4`.
- All 13 PDF pages and the entire matching TeX source were read. The downloaded PDF and PDF inside the extracted archive have identical SHA-256 hashes. Fresh extraction reproduced the inventory text hash `0b5df64e05dee3913a22b4ddce9dedd56c55d2d86ea36bc126f33d278c9913ea`.
- Relevant manuscript, C++ source, pivot plan, and exported presentation hashes match the archive's manifest. See `source_identity.json` and `source_checksums.json`.
- No archived review reports or parallel reviewers' conclusions were read before this verdict. The bibliography, published manuscript, published verifier source, coefficient presentation, and proposed pivot certificate were treated as mathematical inputs, not trusted conclusions.
- Work was confined to this review directory. No website, spreadsheet, Git, Zenodo, or source-archive edits were made; no external individual was contacted.

## Reconstruction of the argument

### 1. The integral Lie algebra and generation

The ambient rank-31 lattice is `sl_2` together with modules of highest weights `6,4,6,2,4,0`, denoted `U,V,W,T,R,Z`. The standard action and seven raw transvectant brackets specify every integer structure constant.

The only possibly nonzero Jacobi expression on three radical inputs has three `U` inputs and values in `T=V_2`. I independently computed the exterior-cube character and obtained

\[
\Lambda^3V_6=V_{12}\oplus V_8\oplus V_6\oplus V_4\oplus V_0.
\]

There is no `V_2` component. Equivariance therefore proves this Jacobi identity over the rationals, hence over the integers. The remaining Jacobi expressions follow from the representation action or vanish by the bracket table. Fresh arbitrary-precision integer computation also checked all 4,495 distinct basis triples directly.

At `p=1009`, the action coefficients and required transvectant coefficients are units. The center is exactly `Z`, the ambient Lie lattice is perfect, and the radical lower-central terms are `W+T+Z`, then `T`, then zero. There is no silent transfer from complex representation theory to an arbitrary small characteristic.

For `x=h` and `y=e+f+U_1+V_0+R_2`, interpolation in `ad h` separates the weights `2,-2,4,0`; the weight-four term is `U_1+V_0`. The Casimir eigenvalues 48 and 24 separate those two terms. Raising/lowering operations then recover `U,V,R`, and their brackets recover `W,T,Z`. All divisions are units at the chosen prime. Consequently finitely many Lie words in `x,y` span the full lattice over `Z_p`, a fact later needed in the lifting argument, not merely generation over `Q_p`.

### 2. Full finite-field automorphism classification

The proof of `H^1(sl_2,V_m)=0` for `m=0,2,4,6` is valid at 1009: after removing nonzero weights from the value on `h`, the remaining cocycle equations force the weight-zero term to vanish and identify the two remaining coefficients as a coboundary. Its uses of `r`, `r+1`, and weight differences involve units.

The radical is characteristic because its quotient is the simple Lie algebra `sl_2`. Quotient automorphisms are induced by `PGL_2(F_p)`; no field automorphisms need to be added because the base field is the prime field. Successive graph-cocycle elimination modulo `N'` and then inside the abelian ideal `N'` removes an arbitrary complement to the Levi factor. Since `N` has class three, these inner exponentials are valid finite polynomials with invertible denominators.

For an automorphism fixing `sl_2` pointwise, equivariance and preservation of `N'` leave the scalar/shear on `U+W`, a scalar on `T`, and a two-by-two mixing matrix on `V+R`. The `T` component of `[aU+bW,aU+bW]` forces `b=0`; `[U,W]` fixes the `T` scalar as `a^3`. The remaining relations are

\[
M^TM=a^3I,\qquad (1,1)M=a^2(1,1).
\]

Using `(1,1)(1,1)^T=2` forces `a=1`. The orthogonal matrix then acts as either sign on the one-dimensional orthogonal complement, giving exactly the identity or swap of `V,R`; the center scalar is its determinant. Thus the classification includes the disconnected involution, not only inner automorphisms or a Sylow subgroup.

The parallel derivation argument is also valid: it first proves preservation of `N`, rather than assuming that all positive-characteristic derivations preserve a solvable radical. The quotient cocycle and radical cocycle can then be removed. The linearized mixing relations force the remaining derivation to vanish. The derivation space consequently has dimension 30 over both `F_p` and `Q_p`.

### 3. The rigid flag

The flag is `<x,y> < <x,y,U_0>`. Its projected plane is `<h,e+f>`, and its radical line is `<U_0>`. The highest-weight line forces the `PGL_2` factor into the upper Borel. Preserving the Killing-orthogonal line `<e-f>` then leaves only the identity and `diag(-1,1)`.

For the latter, the required image of `y` is `-y`, although its `U_1` component is fixed by the twisted degree-six representation. Fixing `h` forces the radical correction to have weight zero, and applying `e+f` to `U_3` yields only `U_2,U_4`. It cannot supply `-2U_1`. If the `PGL_2` factor is identity but the swap is present, the analogous required correction has weight-four and weight-zero terms; a weight-zero input under `e+f` supplies only weights two and minus two. That is also impossible. The remaining inner automorphism fixes `x,y` and hence the entire generated lattice.

The infinitesimal argument separately eliminates the projected `sl_2` element, then uses generation to eliminate the inner derivation. This is essential: a trivial finite stabilizer alone would not automatically establish a trivial infinitesimal stabilizer in positive characteristic.

### 4. Lattice lifting

In the adapted unimodular basis the weights are `0,0,1,2,...,2`; set `A=sum Z_p p^{w_j}b_j` and `L=p^2 A`. The containments `p^2B subset A subset B` make `L` a Lie lattice although `A` need not be a Lie subring.

For a lift of a finite Lie-ring automorphism, the unscaled bracket error is in `p^{i-2}A` on `A` and therefore in `p^{i-6}B` on `B`. For `i>=7` it is both integral and zero modulo `p`. Although the lift need not initially preserve `B`, it already takes `x,y` into `A subset B`; word induction and the error bound show that it takes all of `B` into `B`. Its determinant is a unit, so it preserves `B` bijectively. Preservation of `A,B` preserves both reductions defining the rigid flag; its reduction on `B` is identity.

The identical induction with Leibniz error applies to every derivation solution. This proves the domains `Q in 1+J`, `D in J`, with `J=End(A) intersect p End(B)`, for **all** finite automorphisms and all kernel solutions. There is no circular assumption of `B`-integrality.

### 5. Logarithm/exponential and exact precision

The containments `p^2 End(B) subset End(A) subset p^{-2} End(B)` give `X^r in p^{r-2}End(A)` for `X in J`. Small-degree denominators are units; at degrees at least 1009 the factorial valuations are far below the gained powers of `p`. The exponential and logarithm are convergent and integral in the required lattices.

For two representatives differing by `p^i End(A)`, telescoping the powers gives the additional bound `p^{i+r-5}End(A)`. This absorbs all large-degree denominators, while small-degree denominators are units. Thus neither direction loses the congruence precision. The condition `i>=3` ensures `p^i End(A) subset J`; the theorem uses `i>=7`.

For bracket tensors, the lattice width is six: `p^2 T_0 subset T subset p^{-4}T_0`. The differential `X` of the tensor action preserves `T` and is divisible by `p` on `T_0`, so `X^7 in p End(T)`. In

\[
\exp(X)-I=XU(X),\qquad U(X)=\sum_{r\ge0}X^r/(r+1)!,
\]

the terms with factorials divisible by `p` remain integral and vanish modulo `p`. Modulo `p`, `U(X)` is a polynomial in a nilpotent operator with constant term identity, hence invertible. This makes nonlinear bracket preservation exactly equivalent to the derivation congruence. The resulting correspondence is a bijection of sets; no false claim that it is an additive-group isomorphism is needed.

### 6. Exact certificate and arithmetic

I read the complete published C++ verifier, then freshly compiled and ran it. Its structure constants, adapted-basis conversion, and 14,415-by-961 derivation matrix are reconstructed from formulas rather than read from the exported coefficient tables.

The certificate replay checks minimum pivot valuation at each new level, exact divisibility, unit normalization, elimination, and zero residual modulo `1009^6`. Its nonzero Smith valuations and multiplicities are

| Valuation | 0 | 1 | 2 | 3 | 4 |
|---|---:|---:|---:|---:|---:|
| Multiplicity | 87 | 55 | 758 | 6 | 25 |

Their count is 931 and their sum is 1689. Finite precision alone would leave open higher-valuation nonzero invariants. The proof correctly closes that issue with 30 independent rational inner derivations, which force rational rank at most 931; the nonzero certified local pivots force rank at least 931. The matrix therefore has exactly 30 zero invariants and no unseen higher-valuation ones.

The arithmetic uses an exact modulus below `2^64`, with products in unsigned 128-bit integers. Its largest modular products are below `2^128`. The independently generated scaled presentation contains 199 nonzero integer coefficients, all matching the published JSON exactly. The supplementary fresh Python script imports no published implementation.

For `i>=7`, each zero Smith invariant supplies `p^i` kernel elements and each valuation `v<=4` supplies `p^v`. This proves the intermediate count without an assumption about the size of a known subgroup.

### 7. BCH transfer and boundaries

The additive quotient has exact order `p^{31*1689}`. Since `gamma_m(L) subset p^{2m}B` and `p^{1689}L` contains `p^{1693}B`, its 847th lower-central term is zero. Its class is at most 846, which is strictly below 1009.

BCH denominators through degree 846 involve only primes at most 846. They are invertible modulo `1009^{1689}`. The Lazard correspondence therefore supplies a group on the same set, with the same full automorphism group. The equality is `30*1689+1689 = 31*1689 = 52359`.

Scope is correctly restricted to one prime and one explicitly constructed example. The paper does not claim a minimal order, minimal class, minimal prime, or a result for every odd prime. Its all-`i>=7` formula concerns Lie-ring automorphisms; it does not assert applicability of class-<p BCH correspondence at every larger quotient depth. Neither an exponent-p hypothesis nor a Cayley-table enumeration is needed.

## Primary-reference checks

1. **Cicalo, de Graaf, Vaughan-Lee (2012), pp. 433-434:** the downloaded primary manuscript states the class-<p correspondence for finite Lie rings of arbitrary p-power order, explains denominator invertibility, and explicitly identifies the full automorphism groups. This is exactly the transfer used here. The local PDF has SHA-256 `001caff44a29391a30187e3d1b383d4aaba2cdb07b7051b6d18a8cb7d4e1a5fe`. [Author-hosted PDF](https://iris.unitn.it/retrieve/e3835192-3015-72ef-e053-3705fe0ad821/lazard.pdf), [journal record](https://www.sciencedirect.com/science/article/pii/S0021869311007009).
2. **Lazard (1954):** original publication identity checked in the NUMDAM archive; the applicable theorem's hypotheses were verified through the explicit primary exposition above, rather than claiming a full rereading of Lazard's 90-page article. [Original archive](https://www.numdam.org/item/ASENS_1954_3_71_2_101_0/).
3. **Omirov-Ruan, Theorem 4.8:** the primary version has the same six module degrees and radical bracket pattern, and sets `n=6` to get dimension 31. It works over the complex numbers. The present paper does not rely on transferring its derivation theorem to positive characteristic; the necessary finite-characteristic facts are established directly. The arXiv version and 6 May 2026 date are verified. [Theorem and manuscript](https://arxiv.org/html/2605.04602v1), [version record](https://arxiv.org/abs/2605.04602v1).
4. **Gonzalez-Sanchez-Jaikin-Zapirain:** Theorem 1 gives the `40/41` upper-growth exponent and examples with fewer automorphisms than elements. It does not itself settle equality. [Primary manuscript](https://arxiv.org/html/1406.5772v2).
5. **Shabani-Attar:** Proposition 2.5 and Theorems 2.6 and 2.8 concern maximal class, cyclic Frattini subgroup, and class two with cyclic center, respectively, as represented in the paper. These are restricted-class exclusions, not a general odd-prime nonexistence theorem. [Accepted primary manuscript](https://math.usm.my/bulletin/pdf/acceptedpapers/2012-10-027-R1.pdf).
6. **Kourovka Notebook:** the current primary edition preserves the exact equality question and expressly names this edition as an unverified AI solution. The September notebook URL in the manuscript returned HTTP 404 in this review, a nonmathematical link-availability issue. It does not invalidate the construction; use the DOI for the paper and the current notebook for current status. [October edition](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21tkt-3.pdf), [editors' status explanation](https://kourovkanotebookorg.wordpress.com/2026/10/06/october-2026-update-2-for-the-21st-edition/).

This was a targeted verification of the cited primary sources and current problem status. It was not an exhaustive literature search or priority determination.

## Fresh computational evidence and limitations

- `cpp_verification.log`: all 4,495 original and 4,495 adapted Jacobi checks; inner rank 30; perfect rank 31; generator rank 31; zero infinitesimal flag stabilizer; cohomology dimensions `(0,0),(3,3),(5,5),(7,7)`; unscaled derivation rank 931; all five Smith multiplicities; final `ALL_CHECKS_PASSED`.
- `negative_certificate.log`: changing the first claimed pivot valuation from 0 to 5 was rejected with nonzero exit and `pivot valuation mismatch`.
- `independent_arithmetic.py` / `.json`: fresh arbitrary-precision reconstruction of the bracket, integer Jacobi, all exported presentation terms, exterior-cube character decomposition, exact order arithmetic, and initial denominator bounds through degree 199,999. The infinite denominator bounds are established analytically; the finite range is a supplementary check.
- The normal `c++` launcher failed because of an unaccepted Xcode license. A strict build succeeded using the already installed CommandLineTools compiler and explicit SDK14.4 include/sysroot paths. No license was accepted and no verifier source was changed.
- No complete Cayley table, complete automorphism enumeration, proof-assistant formalization, or independent third implementation of the full Smith elimination was produced in this analytic review. The certificate's source was inspected and replayed; the bracket/presentation was independently rebuilt.

## Exact gap and disposition

**Identified mathematical gap: none.** The proof and computational checks support the explicit theorem at its stated scope. No defect was repaired or hidden. The only identified source issue is the dead September notebook link, and the current external status must remain explicit: this is a proposed solution with reproducible AI-assisted checks, still designated unverified by the notebook.

The remaining epistemic limitation is independent human acceptance and possible errors not exposed by this review, not a known missing mathematical step. External expert scrutiny would be useful; no outreach was prepared or initiated.
