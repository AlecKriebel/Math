# Independent adversarial review — Zenodo 22770864, version 1.1.0

## Verdict

**PASS: no mathematical defect found in the published claim within this review's scope.** The manuscript's exact example is supported by the independently checked argument and exact computations: for the specified prime (p=1009), lattice (L), and depth (i=1689), the BCH group has

\[
|G|=|\operatorname{Aut}(G)|=1009^{52359}.
\]

The strongest conclusion is the stated existence of this explicitly specified finite odd-order group, together with the Lie-ring automorphism formula (1009^{30i+1689}) for every (i\ge7). This is not a theorem for all odd primes, a minimum-size result, a Cayley-table enumeration, a proof-assistant formalization, or external human peer review. No source correction was needed or made.

## Identity and independence

- Reviewed all 13 pages of `kourovka_16_63_v1.1.0.pdf`, DOI `10.5281/zenodo.22770864`.
- Published PDF SHA-256: `9d94db98b4b599a176e95bc74ae8048f69db81d852cf8d557e22f2191c298248`.
- Source bundle: `kourovka_16_63_v1.1.0_source-and-certificates.zip`, SHA-256 `33560d8879bbe3df578f92a8e6311010e504b7d2b669af6678163a7c8f96a7a4`.
- Fresh text was extracted from that exact PDF to `manuscript.txt` after reading the available complete PDF text.
- No archived review verdicts, audit reports, or current parallel review conclusions were consulted. Reviewed the actual manuscript, defining coefficient data, certificate, and executable source.
- All new work is confined to this review directory. No website, spreadsheet, Git, Zenodo, or outreach changes.

## Adversarial mathematical checks

### 1. Integral algebra and generators

The transvectant normalization is fully specified and the seven radical products have compatible target degrees. The only nontrivial radical Jacobi type is (U,U,U\to T); the stated character decomposition has dimensions (13+9+7+5+1=35=\binom73), with no (V_2). More decisively for this explicit algebra, a new arbitrary-integer implementation reconstructed every coefficient directly from monomial differentiation and checked all 4,495 distinct basis triples over the integers, both before and after the adapted basis change. It matched the published coefficient list and the exported finite Lie-ring presentation exactly.

The weight separation in (y=e+f+U_1+V_0+R_2) is correct: its weights are (2,-2,4,0). Once (e,f) are isolated, the Casimir eigenvalues 48 and 24 separate (U_1,V_0). Every denominator used here is a unit at 1009. An independently computed closure in the adapted basis has dimension 31 modulo 1009, so finitely many Lie words span the integral lattice over \(\mathbb Z_{1009}\). This is what the later lifting argument needs; merely having a dense subalgebra would not have sufficed.

The center and perfectness are also directly checked: inner rank 30, bracket-span rank 31. Thus the one-dimensional center is compatible with a perfect algebra and supplies the required codimension-one derivation space. No characteristic-zero theorem is silently transported to positive characteristic.

### 2. Full automorphism classification and discrete components

The radical is characteristic because its quotient is the simple three-dimensional algebra and every solvable ideal maps to a solvable ideal there. The complement-removal argument uses two genuinely abelian layers: (N/N') and (N'). The displayed H1 calculation applies to their module constituents. The fresh H1 computations give cocycle/coboundary dimensions (0/0,3/3,5/5,7/7) for highest weights 0,2,4,6.

After removal of the quotient automorphism and complement graph, equivariance permits exactly the displayed mixing on equal-weight summands. Characteristic (N') prevents a reverse (W\to U) term. In ([\phi U,\phi U]), the cross contribution to (T) really is (2abP_5): the odd transvectant and Lie skew symmetry give the same sign in the two cross terms. Hence (b=0). The equations (M^tM=a^3I) and (wM=a^2w), with (w=(1,1)), imply (2a^4=2a^3). Invertibility and odd characteristic force (a=1). The remaining orthogonal action on the perpendicular line is exactly identity or swap. The central action is fixed by the (V,R\to Z) bracket. The involution was independently checked on all 961 ordered basis pairs.

There is no omitted field-automorphism component, since the field is the prime field \(\mathbb F_{1009}\). The representation \(\operatorname{Sym}^m\otimes\det^{-m/2}\) is well defined on PGL2 for each even highest weight used here. The transvectant determinant character gives precisely the required compatibility.

### 3. The finite flag stabilizer, not just its tangent space

Preserving the line (F_3\cap N\) forces the quotient action into the upper Borel because the (U_0) pure-power line is fixed. Preserving the plane (\langle h,e+f\rangle) further leaves only (1\) and \(\operatorname{diag}(-1,1)\) projectively. I independently enumerated the (1008\cdot1009) upper-Borel representatives against the quotient-plane equation and obtained exactly those two survivors.

For each of the four combinations of quotient sign and swap, I solved the necessary modulo-(N') flag equations. Only quotient identity/no swap survives. For the negative sign, the required (U)-component is (-2U_1), whereas a weight-zero (U_3) vector maps under (e+f) to the span of (U_2,U_4). For the swap at positive sign, the target has forbidden weight-four/weight-zero components. These are actual finite-component obstructions, not conclusions inferred from a zero Lie-algebra stabilizer. The remaining inner map fixes both generators, so generation forces it to be the identity. The separate linear flag rank is 30, agreeing with the infinitesimal assertion.

### 4. Lifting all finite automorphisms

The valuation losses in Lemma 5.2 are consistent. From error on (A\times A) contained in (p^{i-2}A), the inclusions (p^2B\subset A\subset B) give error on (B\times B) contained in (p^{i-6}A\subset p^{i-6}B). At (i\ge6) this permits induction on Lie words starting from (x,y\in A); their images are integral before preservation of (B) is known. A finite family of those words spans (B), hence the representative preserves (B). Its unit determinant then gives equality for an automorphism representative.

At (i\ge7), reduction modulo (p) is a genuine automorphism preserving both lattice-derived flag steps, so it is identity. The identical reasoning for a derivation solution uses the Leibniz error and the infinitesimal flag assertion. Consequently every finite automorphism, and every derivation solution, lies in the stated (1+J\) or (J) domain. There is no assumption here that a finite automorphism already lifts to an exact lattice automorphism; the lift is an integral matrix representative satisfying an approximate bracket identity. Additive maps of \((\mathbb Z/p^i)^{31}\) are automatically \(\mathbb Z/p^i\)-linear, so no additive automorphisms are lost by the matrix formulation.

### 5. Integral logarithm/exponential and congruence precision

I checked the potential failure point caused by (E\) not being contained in (E_0\). The bounds (p^2E_0\subset E\subset p^{-2}E_0\) give (X^r\in p^{r-2}E\) for (X\in J\), while powers also preserve (A) outright. For (r<p), denominators are units. For (r\ge p=1009), the factorial valuation loss is far smaller than (r-2\), so the series preserve (E\), lie in (pE_0\) after subtracting the constant term, and converge. The geometric inverse preserves (A) as required.

For differences in (p^iE\), telescoping products have both the direct (p^iE\) bound and the (p^{i+r-5}E\) bound. The latter absorbs denominator losses in the tail, proving congruence preservation in both directions. The threshold (i\ge3\) ensures (p^iE\subset J\); the application has (i\ge7\).

For bracket tensors, the asymmetric lattice loses six powers, not two. The manuscript uses this correctly: (X^r\in p^{r-6}\operatorname{End}(T)\), and (X^7\) is zero modulo (p\). Therefore (U(X)=\sum X^r/(r+1)!\) is an integral invertible endomorphism of (T\): modulo (p\) it is a polynomial in a nilpotent operator with constant term one, and the tail terms have positive valuation. Since (U(X)\) commutes with (X\), the condition (XU(X)\nu\in p^iT\) is equivalent to (X\nu\in p^iT\) with no loss of precision. This supplies the bijection on the entire automorphism set. It is not assumed to be an isomorphism of additive groups.

### 6. Exact Smith data and hidden higher invariants

The (14415\times961\) derivation matrix formula was rebuilt independently. Two fresh executions agree:

| valuation | 0 | 1 | 2 | 3 | 4 |
|---|---:|---:|---:|---:|---:|
| multiplicity | 87 | 55 | 758 | 6 | 25 |

One execution uses the archived C++ source, freshly compiled; the other uses new Python standard-library code with arbitrary integers, no imported archived implementation or precomputed coefficient table. The proposed pivot plan is checked, not trusted. Both verify exact divisibility, local minimality, pivot normalization, clearing, distinct pivot indices, and zero residual block at precision six. The Python implementation verifies each valuation transition over the entire active block; elimination cannot introduce a smaller valuation within a level because all operations remain integral.

Importantly, a zero residual block modulo (p^6\) alone would not exclude additional invariants of valuation at least six. Here integer Jacobi and 30 independent inner derivations give rational rank at most 931. The 931 pivots give the reverse inequality. That independent upper bound rules out hidden higher invariants. Consequently the finite exact computation determines all nonzero Smith valuations, whose sum is 1689. For (i\ge7\), all valuations are below (i\), so the kernel order is (p^{30i+1689}\).

Negative controls rejected (a) a first-pivot valuation altered from zero to five, in both implementations, and (b) a skew-preserving perturbation of the (h,U_0\) coefficient, which violates Jacobi. These test meaningful failure modes rather than only expected-output strings.

### 7. BCH construction and equality

The lattice is integral: the scaled coefficient exponent (2+w_i+w_j-w_k\) is nonnegative. The additive quotient has order (p^{31\cdot1689}=p^{52359}\). Independently checking the endpoint calculation gives
\(\gamma_{847}(L)\subset p^{1694}B\subset p^{1693}B\subset p^{1689}L\), hence class at most 846. All BCH denominators through this degree are units at 1009. The canonical unexpanded Lie polynomial is a valid exact specification; practical expansion of its enormous word list is unnecessary for existence.

The directly inspected primary Lazard source explicitly covers finite Lie rings of prime-power order and class less than (p\), preserves the common underlying set, and identifies the full automorphism groups. No exponent-(p\) restriction is required. Its hypotheses therefore hold. Combining it with the full-set correspondence and Smith count yields (30\cdot1689+1689=31\cdot1689=52359\), exactly as claimed.

## Primary sources checked

- [Omirov–Ruan, arXiv:2605.04602v1, Theorem 4.8](https://arxiv.org/html/2605.04602v1): the six highest weights and radical bracket pattern match the template. The source works over \(\mathbb C\); the reviewed manuscript supplies the needed integral and finite-characteristic arguments itself.
- [Cicalò–de Graaf–Vaughan-Lee, author-hosted published manuscript](https://iris.unitn.it/retrieve/e3835192-3015-72ef-e053-3705fe0ad821/lazard.pdf), pp. 430 and 433–434: the class bound, denominator condition, and preservation of full automorphism groups apply exactly here.
- [Lazard's original NUMDAM publication record](https://www.numdam.org/item/ASENS_1954_3_71_2_101_0/): bibliographic identity verified; the operative finite-ring formulation was read in the preceding source.
- [González-Sánchez–Jaikin-Zapirain, Theorem 1](https://arxiv.org/html/1406.5772v2): the (40/41\) asymptotic theorem concerns smaller automorphism groups, not exact equality. It does not supersede or imply this explicit equality example.
- [Shabani-Attar, accepted manuscript](https://math.usm.my/bulletin/pdf/acceptedpapers/2012-10-027-R1.pdf), Proposition 2.5, Theorem 2.6 and Theorem 2.8: the exclusions are restricted to the stated classes. They do not contradict the present construction.
- The exact September 2026 Kourovka PDF URL could not be fetched through the browser tool during this review. The [publisher-hosted earlier edition](https://alglog.org/20tkt.pdf) independently locates the same 16.63 equality question and cross-reference. This access limitation affects checking the manuscript's precise edition/page metadata, not the mathematical existence claim. No global priority or exhaustive current-literature certification is made.

## Reproduction artifacts and boundaries

- `fresh_exact_checks.py`, `.json`, `.log`: complete new reconstruction and checks.
- `auxiliary_controls.py`, `.json`: independent discrete involution and H1 equations.
- `cpp_build.log`, `cpp_verification.log`: fresh strict C++ build and successful run.
- `corrupt_plan.txt`, `cpp_negative.log`: deliberate invalid certificate and expected rejection.
- `small_group_controls.json`: fresh archived exhaustive generating-pair checks for (H_p\), giving ((|H_p|,|\operatorname{Aut}H_p|)=(27,54),(125,500),(343,2058)\). These are controls against Sylow-only counting, not finite samples offered as proof of the constructed group's theorem.
- `input_identity.json`, `verdict.json`, `RESEARCH_LOG.md`: identity, machine-readable result, and timestamped checkpoints.

The ordinary system compiler wrapper initially failed because the Xcode license had not been accepted. No license or system setting was changed. The unmodified source then compiled using the separately installed Command Line Tools compiler with explicit existing SDK/header paths. The full archived Python regeneration workflow was not run because SymPy was unavailable in the bundled runtime; independent stdlib reconstruction covers the exact mathematical input and certificate instead.

To rerun the new checks from this directory: `python3 fresh_exact_checks.py` and `python3 auxiliary_controls.py`. To reproduce the strict archived C++ run, use its source under `../../sources/published-source/kourovka_16_63/scripts/independent_verify.cpp` and pass `../../sources/published-source/kourovka_16_63/data/smith_pivot_plan.txt` to the resulting executable. The successful compiler flags on this host were `-std=c++17 -O2 -Wall -Wextra -Werror`, with compiler `/Library/Developer/CommandLineTools/usr/bin/clang++`, `-isysroot /Library/Developer/CommandLineTools/SDKs/MacOSX.sdk`, `-isystem /Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include/c++/v1`, and `-B/Library/Developer/CommandLineTools/usr/bin`.

No finite computation enumerates (G\) or all of its automorphisms. The conclusion combines exhaustive checks for finite certificate assertions with separately reviewed universal arguments in the manuscript. No formal proof verification or external expert endorsement is asserted.
