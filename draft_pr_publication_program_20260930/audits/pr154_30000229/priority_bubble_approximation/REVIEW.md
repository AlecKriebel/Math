# Priority audit: cubic edge bubbles and best P0 approximation

Audit family: negative-norm approximation / stable biorthogonal residuals. Original PR head: `58bee8514677549ee5a7cd699028a5f3a616c5bc`. Historical claimed-solved field: `2/5`. Mathematical validity of the PR construction is inherited from the separate completed audit. This audit assesses historical priority and theorem scope.

## Verdict

**The proposed bubble bridge and the original endpoint disproof are prior results. No independently verified novel mathematical contribution is established.**

Kreuzer–Veeser have the exact cubic edge test, including P0 annihilation, in their public 2019 preprint and published 2021 article. Their Lemma 21 already states a budget-uniform best-P0 endpoint obstruction for the CDN example. Lemma 4(ii) immediately transfers their localized obstruction to the actual global Dirichlet H^-1 norm.

The PR's explicit `c log(N)/sqrt(N)` lower bound is stronger than the literal `L_N/sqrt(N)` statement of KV Lemma 21. However, it follows from the same fixed-coefficient CDN construction and the same allocation quantities by a further elementary Cauchy inequality (or a sharper count in CDN's own two-half argument). This is a checkable sharpening/re-exposition of prior machinery, not an established novel research result.

## Exact claims compared

PR154 considers square Dirichlet Poisson, one compatibly labeled shape-regular NVB master forest, best conforming P1 energy approximation, and all real P0 coefficients on competitor meshes. Its construction has `u ∈ A^(1/2)`, `f=-Delta u ∈ H^-1 \ L2`, and

`E_N = inf_{#T≤N} inf_{g∈P0(T)} ||f-g||_{H^-1(Ω)} ≥ c log(N)/sqrt(N)`.

The endpoint conclusion to compare is that the implication `u∈A^(1/2) => E_N=O(N^-1/2)` fails. It is not a claim about subcritical exponents, unrestricted anisotropy, or a computable data algorithm.

KV's setting uses the same homogeneous Dirichlet Poisson problem, gradient-norm H10 dual, conforming simplicial meshes, and shape-regular constants. Lemma 21 restricts to the square and the CDN initial NVB mesh. Its budget infima run over all recursive/iterative NVB meshes in that family. A finite mesh has finitely many arbitrary real coefficients, so KV's notation `P0(T) ⊂ L∞` imposes no uniform bound on coefficients and does not weaken the PR competitor class.

## Decisive primary evidence

**Kreuzer–Veeser**: *Oscillation in a posteriori error estimation*, arXiv:1903.05915v1, submitted 14 March 2019; published *Numerische Mathematik* 148 (2021), 43–78, DOI [10.1007/s00211-021-01194-8](https://doi.org/10.1007/s00211-021-01194-8). Complete [published primary text](https://link.springer.com/article/10.1007/s00211-021-01194-8) and PDF were inspected. Stable locators: §3.2 Lemma 4, printed pp51–52; §3.4 (3.15), (3.19b), Lemma 7, pp56–58; §3.6 Theorem 15, pp62–63; §3.8 Lemma 21, pp66–68. The preprint has the same essential claims at (3.19b), Lemma 7, Theorem 15 and Lemma 21 (printed pp10–11, 14–15, 17–18).

**Cohen–DeVore–Nochetto**: *Convergence Rates of AFEM with H^-1 Data*, *Foundations of Computational Mathematics* 12 (2012), 671–718, DOI [10.1007/s10208-012-9120-1](https://doi.org/10.1007/s10208-012-9120-1). Complete [author preprint](https://math.umd.edu/~rhn/papers/pdf/afemH-1.pdf), dated 20 April 2011, was inspected, particularly §6.4, (6.19)–(6.25), printed pp29–31. The publisher preview confirms metadata and describes the endpoint logarithmic factor. The subscription version of record's full §6.4 was not inspected; no access barrier was circumvented.

### 1. The bubble is identical, not analogous

Let F be an interior edge AB with opposite vertex C on an incident triangle, and distinguish KV's normalized face test by a superscript. Substituting d=2 into their (3.19b) gives

`ψ_F^KV = (6/|F|) λ_A λ_B (1-5λ_C)`.

PR154 uses

`ψ_e^PR = 4λ_Aλ_B -20λ_Aλ_Bλ_C = (2|e|/3) ψ_e^KV`.

The equality holds separately on each of the two incident triangles. KV Lemma 7 supplies exact biorthogonality with element integration and face integration distributions. In particular, `<χ_K,ψ_F^KV>=0` for every element and `<χ_E,ψ_F^KV>=δ_EF` for every interior face. Thus the PR elementwise mean cancellation and isolation of one edge are already proved in precisely the relevant distribution space, not merely for L2 data or bounded coefficients.

### 2. The global quotient estimate is contained in the prior mechanism

For `ℓ = Σ_F J_F χ_F - g`, KV biorthogonality gives `<ℓ,ψ_F^KV>=J_F` for every real P0 g. Put `q_F=ψ_F^KV/||∇ψ_F^KV||` and `a_F=<ℓ,q_F>`. For any selected edge set take `v=Σ_F a_F q_F`. At most three face patches overlap inside a triangle. Consequently,

`<ℓ,v>=Σ_F a_F²`,  `||∇v||²≤3Σ_F a_F²`,

and `||ℓ||_{H^-1}²≥(1/3)Σ_F a_F²`.

KV (3.20) plus two-dimensional shape-regular scaling gives `||∇ψ_F^KV||≤C/|F|`. Hence

`||Σ_F J_Fχ_F-g||_{H^-1} ≥ c (Σ_{selected F} J_F²|F|²)^(1/2)`.

This is the PR bridge. It is a global version of the bounded-overlap lower-bound proof of KV Theorem 15. That proof explicitly allows arbitrary H^-1 functionals for the lower bound; its discrete-residual assumption is only needed for its upper bound. No saturation assumption is needed. Neither stability of an L2 projection nor a local estimator comparison is being guessed here.

### 3. The endpoint disproof follows directly from stated prior theorems

Define

`D_T(ℓ)²=Σ_{z∈V(T)} ||ℓ||_{H^-1(ω_z)}²`.

KV Lemma 4(ii), for **every** functional ℓ, says `D_T(ℓ)²≤3||ℓ||_{H^-1(Ω)}²`. KV Lemma 21(3.32b) says

`inf_{#T≤N} inf_{g∈P0(T)} D_T(f-g) ≥ L_N/sqrt(N)`,

where `L_N→∞` and `L_N≲log N`; (3.32a) supplies the A^(1/2) solution bound. Applying Lemma 4(ii) to ℓ=f-g pointwise and then taking infima yields

`E_N ≥ L_N/(sqrt(3)*sqrt(N))`.

The inequality direction is essential: the *sum of local norms is bounded above by the global norm*, so a lower bound on that sum forces a global lower bound. The reverse direction, Lemma 4(i), requires Galerkin orthogonality and is not used. The meshes in the sum may depend on g; the pointwise inequality has the same factor 3 on every mesh, so both infima are legitimate. KV introduction (1.5), printed p45, already singles out the global best-P0 quantity and points to Lemma 21.

## Adversarial issue in the printed proof, and its resolution

KV Lemma 21's proof on printed p68 uses the energy term `||∇(u-U_T)||` on an arbitrary competitor mesh, then cites the **minimum** bound (3.32a). A minimum energy error bound does not by itself upper-bound the error on every competitor mesh. This is a real missing intermediate justification in the printed argument. It does not invalidate the above deduction from the theorem's stated conclusion, but an independent derivation should not repeat the step unqualified.

A standard same-forest overlay repairs it. Given any competitor T with budget N, overlay T with CDN's good approximation mesh T_good of O(N) cardinality and O(N^-1/2) energy error. The overlay T* has O(N) elements, inherits g as P0, and has no larger Galerkin error. The biorthogonal/local estimate applied on T* therefore subtracts a uniformly small energy tail. The global norm already dominates D_T*(f-g)/sqrt(3), so no comparison with the original mesh's local norms is necessary. Equivalently, the PR's finite-truncation bubble argument avoids this presentation gap outright. This repair uses the already published NVB overlay and CDN construction, and establishes no new central mechanism.

CDN's prose also has ancillary issues identified in the separate mathematical audit: square-boundary jumps can exist, and edge subdivisions from completion must be counted. Restricting to one interior spoke per micro-square and charging all distinct final overlay edges resolves both without requiring unsupported cancellation or a refinement-origin assertion.

## The explicit logarithmic factor

KV's written condition `L_N≲log N`, `L_N→∞` is insufficient **by itself** to conclude `L_N≳log N`. That distinction must remain visible.

Nevertheless, CDN (6.19) has exactly the PR amplitudes: `2^-j ψ_j`, where `ψ_j=2^-j Σ_{i=1}^{4^j} φ_{Q_ij}`; thus each hat coefficient is `4^-j`. The jump-length weight of a chosen spoke in each micro-square is a fixed constant times `4^-j`. Across n levels their absolute weight sum is a fixed constant times n. If m_ij counts fine edges on these distinct selected segments and F=O(4^n) is the overlay element count, then `Σm_ij≤3F/2`. From the edge splitting Cauchy inequality already used in CDN (6.22)–(6.24), one more Cauchy inequality gives

`Σ_{j=1}^n Σ_{i=1}^{4^j} 4^-2j/m_ij ≥ (Σ_{j,i}4^-j)² / Σm_ij ≥ c n²4^-n`.

Apply the exact prior KV bubble lower bound. Either subtract the O(2^-n) tail as in CDN, or use the support separation verified in the PR audit, obtaining `E_{4^n}≥c n2^-n` for large n. Monotonic interpolation then gives `c log(N)/sqrt(N)`.

The author preprint's final p31 line explicitly prints the weaker squared-norm bound `n4^(-n-2)`; the visual rendering confirmed the absence of an n² there. Its preceding two-half argument already implies n²4^(-n-2): at least n/2 levels each contribute at least n4^-n/8. Thus the explicit logarithmic bound is not literally stated as a lower bound in the examined source, but is an elementary sharpening of its own quantities. The PR's second Cauchy inequality is cleaner and repairs counting by using final overlay edges. None of this supports a novelty claim from a constant, omitted algebra, or a standard overlay detail.

## Strongest verified outcome and exact remaining gap

The strongest verified outcome is a source-grounded reconstruction of a prior endpoint counterexample, with an explicit logarithmic lower bound, direct support handling, and clarified all-mesh counting. It is suitable as an independently checkable explanatory or verification artifact.

No novel theorem, new counterexample, new bubble, or new endpoint resolution is established. The original endpoint problem should not be described as newly solved. An assertion that the precise log lower bound is historically unstated in **all** earlier literature would require substantially broader source comparison; the CDN version of record was not inspected and no oldest-predecessor claim is made. This access limitation does not weaken the decisive KV2019/2021 priority finding. The scope is a bounded decisive-prior-art audit, not an exhaustive bibliography.

No external communication, Git/index/ref mutation, shared MAIN mutation, PR/service mutation, paper drafting, or publication action was performed. All downloaded copyrighted source bytes, text extractions, and renderings are retained only in the locally ignored `private_cache/`.
