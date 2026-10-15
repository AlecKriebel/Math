# Fresh Roydor-source and geometric-scope support review

Checkpoint: 2026-10-07 15:38:55 UTC. Completion estimate for this assigned review slice: 100%. This is support for the parent's independent whole-package review, not a separate completed whole-package cycle. No production files, Git state, or external communications were changed.

## Scope and independence

I first read `research/PROJECT_BRIEF.txt` and the applicable independent-research instructions. I then read all 26 physical pages of the supplied Roydor source through its complete reading copy, made a fresh direct extraction from the PDF, and visually inspected physical pages 2, 10-13, 15, and 20-23 to check the theorem hypotheses and potentially ambiguous formulas. I read the current `manuscript/main.tex` to test the actual proposed extension. I did not read earlier review reports or research summaries. The upstream cohomology proof, literature priority, redistribution/license selection, deposit files, and whole-package reproducibility are outside this support assignment and are not certified here.

Exact reviewed inputs:

| Input | SHA-256 |
| --- | --- |
| `/Users/alec/Downloads/roydor2020.pdf` | `2320e92723841bd9414c4d846a489bbe78d01a03403b8078ca43354407cfacb4` |
| `sources/roydor/roydor2020_reading_text.txt` | `66cd604671be8249af91b4009fb1d8c13a4f47f9448552d239aa5a44dba5342b` |
| `manuscript/main.tex` | `46a02c0cd03f798459a9cfd8fb1cd5e03c4e599208a2a53750d3b218b7e96dc4` |

The fresh `pdftotext -layout` extraction has 26 page breaks. After removing only the two recurring institutional/download watermark lines and all whitespace, it agrees exactly with the reading copy after removal of its physical-page marker lines: both have 48,783 characters and normalized SHA-256 `872937640be0d54986acb7c226660c44fca0599e243a7ea0e0dc562a5b144626`. Scratch evidence is confined to `tmp/final_licensed_package_freshreview_20261007/roydor_support/`, including `direct_primary.txt`, `text_comparison.json`, and rendered source-page PNGs.

## Verdict

I found no substantive mathematical concern in the reviewed manuscript's use of Roydor's lower-level geometric results or in the fixed-source extension to arbitrary von Neumann algebras, conditional on the stated all-algebra ordinary bounded cohomology input. The printed Roydor Theorem 1.2 by itself does **not** prove the arbitrary-predual target; the manuscript accurately says so and supplies the extra argument. The exact algebra/predual, complex-field, ordinary-norm, Jordan/opposite, strict-distance, and zero-boundary conventions are consistent.

The strongest checked conclusion in this slice is the following conditional result: if every complex von Neumann algebra has ordinary bounded self-coefficient cohomology vanishing in degrees 2 and 3, the manuscript's fixed-source argument gives, for every such algebra M, a positive threshold depending on M that works for every von Neumann comparison algebra N, for both algebra and canonical-predual ordinary Banach-Mazur distances. This review does not independently establish that cohomological premise.

## Exact primary theorem and cohomology conventions

Physical page 2, printed Theorem 1.2 (reading-copy line 80), requires that the **source M have separable predual**. It requires H^2(M,M)=0 and that B^3(M,M) be closed in Z^3(M,M). For a fixed such M it concludes that, for every von Neumann algebra N, Jordan *-isomorphism, algebra-space linear isometry, canonical-predual linear isometry, and the two strict distance inequalities are equivalent. N is a von Neumann algebra, not an arbitrary Banach space. The theorem's threshold is existential and source-dependent; page 3 expressly discusses that dependence.

Physical page 20, Section 4.2.1 (reading-copy lines 939 onward), defines the cochain spaces as **all bounded multilinear maps** with the ordinary multilinear norm, with the algebra acting on itself on the left and right. B^k is the actual range of the differential and Z^k its kernel. No closure is placed in the quotient denominator. These are neither completely bounded nor normal-only cochains. The ambient C*-algebras are complex, and the unitaries argument on physical page 5 explicitly uses complex scalar phases. There is no real-field reinterpretation in the source theorem.

For the standard bounded complex Hochschild differential used in the manuscript, H^3=0 implies B^3=Z^3, and Z^3 is closed because the differential is a bounded linear map of cochain Banach spaces. Thus ordinary H^2=H^3=0 supplies the exact qualitative conditions of the printed theorem. Completely bounded vanishing, restricted-normal vanishing, or different coefficients would not supply this implication.

Two defects in the supplied source were independently authenticated visually and correctly disclosed by the manuscript:

1. The differential on physical page 20 prints the adjacent-merge sum only through k-1 and the last sign as (-1)^k. The standard formula sums through k and has last sign (-1)^(k+1). This cannot be a genuinely different consistent convention: in degree 1 the printed formula is a f(b)-f(a)b, and on M_2(C), with degree-zero b=e_12, a=e_11, and c=e_22, the printed degree-one operator applied to the degree-zero coboundary gives -2e_12 rather than zero. The text's assertion that successive differentials compose to zero therefore identifies a printing error. The manuscript's displayed standard differential repairs it explicitly and matches the intended Hochschild groups.
2. Physical page 15, the heading of Claim 4, prints h_ij in the off-diagonal decomposition; the immediately preceding computation and physical page 16, Claim 7, use h_ji. The transpose map on M_2(C) is a direct falsification of the heading as printed: for i=1,j=2, g_12=0 and h_12=e_12, whereas T(e_12)=e_21=h_21. The corrected relation is T(e_ij) approximately g_ij+h_ji. The manuscript uses the corrected orientation.

The general involution-preserving stability claim is not being silently extracted from the specially quantified last part of source Theorem 4.5. The manuscript gives its own symmetric cochain iteration, with open-mapping constants attached to a fixed algebra. Qualitative cohomology vanishing alone does not justify selecting universal primitive constants K=L=1, and the current argument does not do that.

## Geometric inputs and constants

The inputs actually used have no separable-predual hypothesis in their statements or mechanisms:

| Roydor input | Physical pages | Checked content |
| --- | --- | --- |
| Corollary 2.4 | 6 | Normalizes a small ordinary distortion to a unital self-adjoint isomorphism with both norms tending to 1; the displayed upper estimate is 1+10 sqrt(distance-1). |
| Lemma 2.5 | 7 | Approximate order bound with gamma(t)=2(1+t)sqrt(2t+t^2); it applies to T and T^{-1}. |
| Proposition 2.13 | 10-11 | Projection rounding radius 140 sqrt(t); center projection correspondence and center *-isomorphism; commutativity recognition. Projection rounding requires t<10^{-5}; the center conclusion requires t<10^{-8}. |
| Lemma 3.1 | 11-13 | Unital self-adjoint corner isomorphisms, with norm at most 1+142 sqrt(t), inverse norm at most 1+988 sqrt(t), and central-block approximation; hypothesis t<10^{-8}. |
| Theorem 3.2 | 13-17 | Central multiplicative/anti-multiplicative splitting when the source unit halves; ordinary bilinear defects bounded by 3,147,585 sqrt(t); hypothesis t<5 times 10^{-13}. |

The manuscript copies the relevant displayed constants and their square-root dependence accurately. Its main conclusion uses their convergence to zero rather than deriving a universal numerical threshold. I checked the proofs for scope and mechanism; this is not an independent optimized arithmetic certificate of every integer in the article's long estimate chain. Small enlargements of intermediate rough constants would leave the existential fixed-source argument unchanged.

These proofs use spectral functional calculus, norm perturbation of bounded maps, the center-projection lattice, and a finite 2-by-2 matrix-unit system. None enumerates a dense set or assumes a countably generated predual. The corner-surjectivity step can be understood directly as perturbing the range projections: R_p(x)=pxp and Q_q(y)=qyq satisfy T R_p T^{-1} approximately Q_q, by the Jordan triple estimate and T(p) approximately q. For sufficiently small distortion, the restriction Q_q T:pMp to qNq is onto and boundedly invertible by a Neumann-series argument. Thus no separability or noncentral-cohomology premise is hidden in the compression lemma.

The source's proof of Theorem 1.2, physical pages 22-23, writes its type-I decomposition with degrees indexed by a subset of the positive integers plus a single infinity symbol. This is exactly the part not to transplant to arbitrary Hilbert-space cardinalities. The current manuscript avoids that argument, source Theorem 1.1, and the compressed-map invocation in source Lemma 4.3.

## Independent tests of the nonseparable extension

**Fixed halving source.** For a fixed V whose unit halves, the central block map F from Theorem 3.2 has inverse norm at most 1+988 sqrt(t). The target product y diamond z=qyz+(1-q)zy is associative and involution-compatible because q is central; its second summand is the opposite C*-algebra. Its norm is still the original C*-norm. Centrality also gives the maximum, rather than a sum, of the two block defects. Therefore the pulled-back multiplication differs from the original by at most

`(1+988 sqrt(t)) 3147585 sqrt(t)`,

which tends to zero. The deformation lemma is applied once to fixed V, so no varying central projection receives an unjustified uniform deformation constant. The resulting *-isomorphism to the modified target is a Jordan *-isomorphism to its original target.

**Carrier test.** For h with central carrier 1, q approximately T(h), w=c(q), and z=theta^{-1}(w), inverse approximate order gives

`h-z <= [2(1+t) 140 sqrt(t) + gamma(t)] 1`.

Both approximation errors correctly carry a factor 1+t from T^{-1}. If the bracket is below 1, compression by 1-z makes h(1-z), a projection, have norm below 1, so it vanishes. Full carrier then forces z=1 and w=1. The same computation works for complements since T is unital. The paper's carrier lemma has the correct constants, sign, and full-carrier conclusion.

**Odd finite degrees.** On every fixed odd degree n>=3, the rank-(n-1) source projection e and its rank-one complement both have full central carrier. The first corner E=eOe has even finite homogeneous degrees and halves, while the complement is abelian. These remain true after a bounded central product over all odd finite degrees and arbitrary abelian centers. Compression and the carrier test yield q and 1-q with full carrier; the latter corner is abelian. A full abelian projection makes the target D type I.

Applying the fixed-source halving lemma to E yields an exact Jordan *-isomorphism E to qDq. Full corners identify their centers with the original centers. A Jordan *-isomorphism preserves homogeneous finite degree, whether its central pieces preserve or reverse multiplication. On the image w_n of each source degree-n central support, w_n q consequently splits into n-1 equivalent abelian projections, each with carrier w_n in D. The abelian complement w_n(1-q) also has carrier w_n. In a type-I von Neumann algebra abelian projections with the same central carrier are equivalent. Hence w_n splits into n equivalent abelian projections and w_nD is homogeneous degree n with the required center. Finite homogeneous matrix classification reconstructs each source summand and their bounded central product.

This reasoning excludes a hidden infinite-dimensional target summand without attempting cancellation of infinite cardinalities: on each w_n it reconstructs the entire unit as a sum of exactly n rank-one projections. The source degree supports exhaust the center and their images exhaust the target center. No direct-integral measurability or separability choice is needed.

**Global threshold.** The source is divided into only three fixed central algebras A, P, O. A is the abelian part; P contains the even finite type-I, all infinite type-I, type-II, and type-III parts and halves; E=eOe is the second fixed halving source. Universal vanishing is applied directly to P and E, both von Neumann algebras. The proof does not deduce a noncentral corner's cohomology from a central-restriction lemma. Only finitely many inequalities and at most two fixed deformation thresholds must be met. Every relevant geometric error tends to zero with the initial distortion. This proves the quantifier order: for each fixed M there exists a positive epsilon_M working for all N. It gives no uniform epsilon for all M.

## Predual, isometry, opposite, and zero checks

For a bounded complex-linear isomorphism S:M_* to N_*, the adjoint S^*:N to M is complex-linear and has the same norm as S; its inverse is (S^{-1})^* with the same inverse norm. Symmetry of the ordinary distance then gives d_BM(M,N)<=d_BM(M_*,N_*). Thus the algebra threshold itself works for the predual implication. There is no normality requirement on the initial algebra near-isomorphism.

A bijective Jordan *-map is a positive order isomorphism, with positive inverse. It preserves all existing suprema by the definition of least upper bound. In particular it preserves suprema of increasing bounded positive nets, so it is normal for von Neumann algebras even without separability. It is also isometric and induces an isometry on canonical preduals. Conversely, a predual linear isometry adjoints to an algebra-space linear isometry. Kadison's theorem gives a Jordan *-isomorphism after the unitary multiplier is removed. The manuscript asserts existence of a Jordan *-isomorphism, not that every arbitrary isometry itself preserves the involution or unit.

The identity between an algebra and its opposite is complex-linear, isometric, and Jordan *-preserving. It need not be an associative *-isomorphism. The central reversed product in the proof respects that limitation exactly.

For nonzero Banach spaces, every isomorphism has distortion at least 1. With the literal infimum convention in the manuscript, the unique zero-to-zero map and its inverse have norm 0, giving d_BM(0,0)=0. There is no isomorphism from zero to a nonzero space, so the mixed distances are infinity. Since a von Neumann algebra is the dual of its canonical predual, nonzero algebras have nonzero canonical preduals. For M=0 either strict hypothesis forces N=0; any positive threshold works. Strict inequalities for nonzero spaces provide an actual map below the stated threshold even if the infimum is not attained. No equality-case claim is being smuggled into the theorem.

## Remaining source-version limits

The supplied PDF is a complete 26-page publisher-formatted article carrying DOI `10.1142/S1793525321500151`, the accepted date August 26, 2020, and the printed publication date December 11, 2020. Its metadata creation/modification dates are December 9/12, 2020; it visibly carries a `2nd Reading` heading and internal pagination 1-26. Therefore the exact checked statements are those in this supplied DOI-bearing version. This file alone does not independently authenticate the later 14(3), 767-792 issue pagination, determine whether later typesetting corrected its slips, or rule out later errata. Those are bibliographic/source-access limitations, not a newly found gap in the current conditional proof.

The institutional watermark expressly restricts redistribution of the supplied source. I did not republish or place its PDF in a deliverable. Any review of whether third-party source bytes/text are excluded from the intended licensed package remains with the whole-package reviewer.

No substantive correction request arises from this assigned slice. The theorem remains dependent on independent verification of the ordinary bounded all-algebra H^2/H^3 input and on the other whole-package review gates outside this report.
