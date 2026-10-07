# Independent family 126 and exact-lift bridge audit

Audit time: 2026-10-06 22:16 PDT (America/Los_Angeles). Auditor: internal independent AI research subagent. This is a source audit and finite falsification check, not conventional human peer review or a claim of full Lean verification.

## Input and exact statement

The upstream repository is read-only and remains at `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. The inspected paper is family 126, *Exponential PSD rank of positively shifted matching matrices*, author OpenAI, dated October 5, 2026. Its manuscript-specific supplied citation must be used. I read its full introduction, normalization and matching transfer proof, local averaging proof, orthogonal splitting proof, product Fourier smoothing proof, and parity-functional proof. The optional matching-smoothing appendix is not needed for the exponential argument and was not audited here.

For even n≥4, rows are all odd subsets U of [n], columns are perfect matchings M of K_n, and

`A_n(ρ)[U,M] = |M ∩ δ(U)| − 1 + ρ`.

The exact real PSD rank is the least positive order r of real symmetric PSD factors F_U,G_M with `tr(F_U G_M)=A_n(ρ)[U,M]` for every entry. No symmetry, rank-one, sparsity or precision restriction is imposed. The source theorem states: there is an absolute c>0 such that for each fixed 0<ρ<1 there is n₀(ρ) with rank_psd(A_n(ρ))≥2^{cn} for every even n≥n₀(ρ). The rate c is independent of ρ; its threshold need not be. The endpoint ρ=1 has a polynomial diagonal edge factorization and cannot be included.

The source corollary states: there are absolute c₀>0,n₁ such that for every even n≥n₁, A_n(0), the full edge-plus-odd-cut slack matrix T_n(0), and every exact real affine PSD lift of the perfect matching polytope have order at least 2^{c₀n}.

## Shift-to-unshifted calculation: verified

If `A_n(0)[U,M]=tr(F_U G_M)` with r×r PSD factors, then

`F'_U = diag(F_U,ρ)` and `G'_M=diag(G_M,1)`

are PSD of order r+1 and satisfy `tr(F'_U G'_M)=A_n(0)[U,M]+ρ` exactly. Therefore

`rank_psd A_n(ρ) ≤ rank_psd A_n(0)+1`.

Choose the fixed shift ρ=1/2. The source exponential estimate gives rank_psd A_n(0)≥2^{cn}−1. Once 2^{cn}≥4, this is ≥2^{cn/2}; thus c₀=c/2 is valid. Adding edge rows cannot decrease PSD rank. This argument is an exact equality of affine slacks, not a transfer of an approximation or robustness claim.

## Exact affine lifts: verified, including all equalities and size

Size r means one PSD cone S⁺_r, whose matrices have r rows and columns, not its vector-space dimension r(r+1)/2 or the number of affine constraints. The lift is `P=T(L∩S⁺_r)` with affine subspace L and affine map T. Multiple PSD blocks can be embedded in a single block-diagonal cone of order equal to the sum of their orders. The lower bound does not separately count lifted equalities.

Edmonds's perfect-matching description uses x_e≥0, x(δ(U))≥1 for odd U, and x(δ(v))=1. Every inequality row is tight at some perfect matching: for an odd cut, pair all but one vertex within each side and use one crossing edge; for an edge e and n≥4, choose a perfect matching avoiding e. Singleton and complementary-singleton odd-cut rows are identically zero, causing no issue. Nonfacet valid tight rows are nonnegative combinations of facet slack rows after restricting to the affine hull. Thus redundant tight rows do not alter factorization order.

The source's proper-lift argument is sound. Restricting a feasible section to its minimal containing PSD face gives a cone isomorphic to S⁺_s with s≤r and an affine slice meeting the relative interior. Since the target is bounded and not a singleton, the affine slice cannot contain zero: if it did, the feasible section would be a cone, and its affine image could be bounded only if the linear part vanished on it, giving one point. A linear functional identically one on an affine slice not containing zero absorbs the affine translation without increasing matrix order.

There is also a direct exact row-factor proof, independently reconstructed from the actual Lean certificate rather than requiring Slater conditions. Choose PSD lift matrices B_v∈L for every vertex v, and let g be a valid affine slack composed with T, tight at B_v₀. The finite evaluation cone

`C_B={ (tr(A B_v))_v : A≥0 }`

is closed. To prove this, compress to the span of the supports of B_v. J=Σ_v B_v is positive definite there; bounded evaluation coordinates bound `tr(AJ)`, hence `tr(A)`, and then all entries of compressed A. A convergent subsequence supplies a PSD limit with the desired evaluation vector. If all B_v vanish, the evaluation cone is simply {0}.

For any real coefficient vector c with `Σ_v c_v B_v≥0`, let s=Σ_v c_v, t=|s|+1 and q=s+t>0. The matrix

`X=q⁻¹(Σ_v c_v B_v+t B_v₀)`

is PSD and belongs to L, because its affine-combination coefficients sum to one. Thus `0≤q g(X)=Σ_v c_v g(B_v)`. Separation of the closed cone C_B and self-duality of the PSD cone yield A≥0 with `tr(A B_v)=g(B_v)` for every vertex. Apply this to every tight slack row. This supplies a factorization of the same order r, including arbitrary lifted equalities and arbitrary affine T, with no additional scalar block. The block added above belongs only to the shift calculation.

## Source proof scrutiny: no substantive defect identified

The normalization lemma compresses to the joint column support, chooses a determinant-maximizing positive definite J in the compact column hull, and uses the one-sided log-determinant derivative. It gives `tr F_U≤n` and `tr G_M≤r` with unchanged pairings. This is a valid finite-dimensional argument.

The orthogonal splitting lemma was checked independently. For two PSD matrices A,B, the spectral sign projection P of A−B and Q=I−P have A₁₂=B₁₂, A₁₁≥B₁₁ and B₂₂≥A₂₂, hence

`tr(AB)≥||PBP||²_F+||QAQ||²_F`.

In the induction, compression introduces overlaps at most `2 tr(A_j A_j')+2 tr(A_j P A_j' P)`. The sum of the latter terms is bounded by `||P(Σ_{j≥2}A_j)P||²_F≤tr(A₁Σ_{j≥2}A_j)`. The source's ordered-pair convention and C_L=2^{L−1} therefore suffice.

The product-smoothing theorem's tagged y row blocks are essential and work as stated. They eliminate products from unequal y values. The overlap identity has factor 1/L², diagonal expectations have bound L⁻² E||Z||², and nonmatching character expectations have bound θL⁻² E||Z||². Old projections can depend on unprocessed input x but not on the new independent averaging parameter m, so the matrix variance assumption applies conditionally. Orthogonal splitting preserves the sum-of-squares identity. The potential grows by at most 2 per coordinate under the stated `Lλ²C_Lθ≤1`. The final Gram rank is at most the column count rL^t, regardless of its enormous row count; this gives exactly the displayed weighted Fourier mass estimate. No uncounted matrix-dimension factor was found.

The local channel proof has uniform marginals by permutation transitivity. Its two-sample trace formula, binomial comparison, O_d(√k log k) trace bound and nonconstant eigenspace multiplicity ≥k/2 together prove the needed θ_d(k)→0. The elementary invariant-subspace argument using disjoint transpositions and three-cycles is valid for sufficiently large even k. The source uses fixed d=100 and an astronomically large but finite fixed k; no effective useful numerical value of c is asserted.

The parity functional is signed and only positive on the stated low block degree squares. The small-side construction avoids the global inconsistent parity relation: pair sums have a cut side ≤t/5, and triple symmetric differences have size <t, forcing the empty side by connectivity. Its edge disagreement values and L^t operator norm bound are valid. The expander union bound accommodates parallel edges and bipartiteness, and the matching construction uses distinct terminals for each incidence.

Finally, with r≤2^t, the source discarded-tail bound is

`E_t(y)^2≤n(4 L²/λ^τ)^t≤n(4L)^(−2t)`.

Its uniform error is `2n(4L)^(−t)+n(4L)^(−2t)`. Multiplying by the functional norm L^t gives `2n4^(−t)+n(16L)^(−t)→0`, since n<k(t+2) and k is fixed. For a fixed ε=1−ρ>0 this contradicts D(f)=−ε and D(f*)≥0. These estimates justify excluding every factorization r≤2^t, and t≥n/(2k) eventually yields the claimed absolute exponential rate. None of the gaps in the follow-on reduction can be filled merely by the existence of this manuscript; they require their own proof.

## Actual Lean semantics and build scope

I inspected `lean/docs/126.md`, the two comparator files, actual `Model.lean`, `Main.lean`, `AffineModel.lean`, `AffineLift.lean`, `AffineFactorization.lean`, `AffineCertificate.lean`, `PSDDuality.lean`, `OrthogonalCone.lean`, `PSDCompression.lean`, and `CellLowerBound.lean`.

The comparator files contain `sorry` by design and are not certification. The actual declarations are:

- `OAI.PerfectMatchingPSD.main : MainClaim`, in `OAI/Combinatorics/MatchingPSD/Main.lean`.
- `OAI.PerfectMatchingPSD.affine_lift_lower_bound`, in `OAI/Combinatorics/MatchingPSD/AffineLift.lean`.

`MainClaim` is `∀ C>0, ∃ n₀≥4, ∀ even n≥n₀, (n:ℝ)^C < psdRank n`. The slack matrix contains edge rows and unshifted odd cuts. `HasFactorization` uses real matrices and `Matrix.PosSemidef` (real Hermitian means real symmetric), exact traces, and no equivariance restrictions. `HasAffineLift` uses an arbitrary affine subspace of all real square matrices and an arbitrary affine map; PSD feasibility itself restricts feasible matrices to symmetric PSD matrices. This matches the intended arbitrary exact affine-lift class.

These declarations establish only superpolynomial growth if fully built. They do not state or formalize the paper's exponential positive-shift theorem. `Main.lean` uses cell size growing with t and brackets n by t^6; it is a distinct, weaker quantitative proof route. The source docs explicitly say so.

The actual import closure of those two proof declarations comprises 66 OAI modules plus the external import Mathlib. A comment-stripped static scan of the closure found no `sorry` or custom `axiom` tokens. All 66 files were copied locally and hashed in `checks/source_bridge_receipt.json`; upstream was not modified. Static absence of tokens is not a kernel build or an axiom audit.

Lean 4.34.1 is installed and `lean --version` was run successfully from the local snapshot: arm64-apple-darwin24.6.0, commit 5045d0056413266e57c625dcd7c365b10e377c52. Upstream has no `.lake` directory, and the applicable proof has not been rebuilt in this audit. The snapshot supplies a minimal Lake configuration using the exact upstream Mathlib pin d13f23b723b8a846827a245b89c10fc7d3f11612, together with the original toolchain and, if available, separately named upstream manifest. Building would require obtaining the Mathlib source/build cache, then building the copied modules. This is optional support for the superpolynomial input, not verification of the exponential source theorem or the follow-on TSP theorem. No formal-verification claim should appear in the follow-on headline.

## Reproducible finite checks

Run `python3 checks/source_bridge_audit.py` from the project folder. The script uses only the Python standard library and reads upstream solely for the static source snapshot. Receipt: `checks/source_bridge_receipt.json`.

- Exact rational block-diagonal +ρ pairing check passes (ρ=1/2).
- Exact rational local marginal and K² trace-formula checks pass all 12 cases with d=2, k=4,6,8, both charges and both compatible incidence assignments. Some small k channels have no contraction; the asymptotic lemma requires sufficiently large k and does not claim otherwise.
- Orthogonal splitting passes 320 seeded noncommuting PSD test cases, dimensions 1–8, L=2–6. The stronger two-matrix inequality also passes. Maximum projector error is 3.75×10⁻¹⁵; this is floating-point falsification evidence, not a proof.

## Supported result and exact remaining scope

The shift-to-unshifted and exact-affine-lift obstruction are rigorously justified, with matrix order and parity convention tracked. No substantive flaw was identified in the pivotal elementary source proofs audited here. The exponential matching theorem remains an attributed mathematical dependency on an unrefereed OpenAI manuscript, independently audited in this effort but not formally certified. The actual Lean proof scope is superpolynomial and its build remains unverified. The explicit linear-city matching-to-TSP face reduction, all-city padding, upper order, priority audit and publication package require separate verification by the root and other independent approach families. This audit alone is not a certificate that the follow-on core target or publication objective is complete.

## Follow-up: full quantifier audit of the finite-evaluation lemma

Follow-up checked 2026-10-06 22:19 PDT, at root's request for replacing the manuscript's proper-face bridge with the direct proof. This reconstruction is from the inspected mathematical reasoning of actual `AffineCertificate.lean`, `PSDDuality.lean`, `OrthogonalCone.lean` and `PSDCompression.lean`; it is not a new lower-bound method and does not claim a Lean build.

**Lemma.** Let I be a finite nonempty index set, L an affine subspace of S^r, and B_i∈L∩S⁺_r for every i∈I. Let g:S^r→R be affine, nonnegative on L∩S⁺_r, and suppose g(B_i₀)=0 for some i₀∈I. Then there is A∈S⁺_r such that `tr(A B_i)=g(B_i)` for every i∈I.

There are no assumptions of linearity of g, Slater conditions, boundedness of L∩S⁺_r, independence of B_i, nondegeneracy of individual B_i, or nonnegative affine-combination coefficients. Arbitrary lifted equalities are part of L. Matrix order is unchanged.

**Complete proof.** Put J=Σ_i B_i and H=(ker J)^⊥. If z∈ker J, then `0=zᵀJz=Σ_i zᵀB_i z`; all summands are nonnegative, and PSD implies B_i z=0 for each i. Thus each B_i is supported on H. Orthogonal compression of A to H is PSD and preserves every `tr(A B_i)`.

Define `C={ (tr(A B_i))_i : A∈S⁺_r }`. It is a convex cone, and every coordinate of every point of C is nonnegative. If H=0, then all B_i=0 and C={0}, which is closed. Otherwise J|_H is positive definite with smallest eigenvalue λ>0. For any convergent sequence y^(k)∈C, choose representing PSD A_k and compress them to H. The sum of their evaluation coordinates satisfies `tr(A_k J)=Σ_i y_i^(k)` and is bounded. Since J−λI_H is PSD, `λ tr(A_k)≤tr(A_k J)`. PSD also gives `||A_k||_F≤tr(A_k)`. Thus A_k is bounded in the finite-dimensional symmetric matrix space and has a convergent subsequence. Its limit is PSD and represents the limit of y^(k), proving that C is closed.

The dual cone under the ordinary coordinate inner product is

`C*={ c∈R^I : Σ_i c_i B_i∈S⁺_r }`.

Indeed, `c·(tr(A B_i))_i=tr(A Σ_i c_i B_i)`; self-duality of S⁺_r follows either from spectral decomposition or testing rank-one matrices A=xxᵀ. Negative coefficients c_i are expressly permitted.

Let y_i=g(B_i) and take any c∈C*. Put `s=Σ_i c_i`, `t=|s|+1>0`, `q=s+t≥1`, and

`X=q⁻¹(Σ_i c_i B_i+tB_i₀)`.

Both matrices in the numerator are PSD. Its coefficients, with t added at index i₀, sum to q, so X is an affine combination of the B_i and lies in L. This is true even when some individual coefficients are negative. Affineness yields

`qg(X)=Σ_i c_i g(B_i)+t g(B_i₀)=c·y`.

Validity gives c·y≥0. Thus y∈C**=C by the finite-dimensional bipolar theorem for closed convex cones, or equivalently by separation of y from C if y were outside. The resulting A≥0 gives the exact claimed trace values for all i simultaneously.

To apply the lemma to an arbitrary exact polytope lift, choose one feasible lift B_v for each vertex, compose any valid target slack with the affine output map, and select a vertex where that slack is zero. Its row factor is supplied by the lemma. Applying this independently to all odd-cut rows gives an exact factorization of A_n(0) of order r. It does not require adjoining any constant column, using facets, or altering the original lifted section. The sole +1 order cost in this project is the earlier positive-shift construction.
