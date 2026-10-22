# Independent exact-source, model and dependency review: PR946 / 6000001

## Result and custody

**PASS within this family's remit.** No required mathematical or source-alignment correction was found in the frozen candidate. This is an independent review of the original argument, not a new proof-attempt response, and makes no novelty or publication-readiness judgment.

The reviewed Git head is `7d3adb0e500b0414a49a449e7981d34ade329427`. The proof SHA-256 is `a26c1755bc6f61085db4c01b6579701ff380822f2cc58a3ffbfb4acfa49370a2`. I independently compared all 33 original files, byte for byte, with their actual Git objects and with the snapshot SHA-256 values; all comparisons passed. The actual fixed-head queue row says `claimed_solved`, `4/5`. Its hash without a trailing newline matches the eligibility gate. The live checkout is on `main`; its queue has an earlier state, so it was not substituted for the fixed-head row. See `INPUT_AUTHENTICATION.json`.

I read the root and queue instructions, queue README, selected queue row, complete source record and prior report, eligibility gate, identity preflight, snapshot, charter, and entire frozen proof. I did not import original acceptance reports or other review-family verdicts as evidence, run original scripts, modify the shared index or native queue, or communicate externally. All new files are confined to this family directory. Raw primary PDFs, text, screenshots and HTML are private and excluded from the curated manifest.

## Exact source and definition map

The actual [FMU1998 scan](https://www.jstage.jst.go.jp/article/iis/4/2/4_2_125/_pdf/-char/en), printed p.125, item1(a), starts with a Riemannian manifold and mutually dual affine connections. It asks for higher-dimensional dually flat realization and, conditionally on failure, a finite-dimensional realization condition. Its footnote concerns affine-space realization; items1(b)-1(e) are separate questions. No continuation of item1(a) occurs on p.126. I visually inspected all three pages, including the bibliography. The cached record is a reasonable shortened description, but the source's general dual-pair wording must remain visible.

The cited [Amari1997 primary scan](https://bsi-ni.brain.riken.jp/database/file/166/169.pdf), printed pp.83-85, explicitly supplies torsion-free and curvature-free flatness and local dual affine coordinates. Its p.87 embedding question requires the induced dual structure. Thus the candidate's flat-connection interpretation, allowing a nonconvex domain and local dual coordinates, agrees with the underlying definitions. It does not have to supply a probability model, complete metric, complete affine connection, globally injective Legendre map, convex ambient domain, or minimal codimension.

| Source requirement | Candidate treatment | Independent assessment |
| --- | --- | --- |
| Riemannian metric | Smooth positive-definite `g`; positive-definite ambient Hessian | Matches the source's metric class |
| Specified ordered dual pair | Sections2,5,7 recover the first connection and then its unique metric-dual | Both connections are recovered, not merely the metric or their average |
| General dual-pair source wording | Both torsions must vanish; this is also sufficient | Handles the broader wording instead of silently assuming it away |
| Higher finite dimension | `N = binomial(2n+4,3) > n` for `n >= 1` | Explicit, uniform dimensional bound |
| Entire manifold as submanifold | One proper embedding into one open Hessian domain | Stronger than pointwise local realization |
| Conditional finite-realization question | Necessity and sufficiency of the two zero torsions in the stated smooth category | No further invariant is needed within that category |
| Other Amari subitems | Not asserted to be solved | They are distinct source questions |

The source uses the ordinary finite-dimensional manifold setting. Hausdorffness, second countability and no boundary are explicit candidate conventions, consistent with that setting. Indefinite, nonsmooth and boundary versions remain outside the theorem. The zero-dimensional case is separately correct: a countable discrete manifold embeds properly into an integer subset of a line and has no nonzero tangent data.

## Torsion is an actual condition

For an immersion into a torsion-free ambient connection, the induced torsion is its tangential torsion. Indeed,

`f_*(T^ind(X,Y)) = P(D_X f_*Y - D_Y f_*X - f_*[X,Y]) = 0`.

Apply this separately to both ambient dual connections. Thus the source's general dual pairs cannot all occur, and the candidate's conditional answer has content. For example, on Euclidean `R^2`, set only `Gamma^1_12 = 1` nonzero, and define the metric-dual by `Gamma*^k_ij = -Gamma^j_ik`. This gives a smooth mutually dual pair but `T(partial_1,partial_2)=partial_1`, so no realization in a torsion-free dually flat target is possible. The dual in this example is torsion-free. Interchanging the connections shows why requiring only one torsion to vanish is insufficient.

This obstruction is verified by the displayed coordinate formulas. It is not a new route or proposed change to the candidate: it checks the necessity claim already in Section7.

## Foundational dependencies

The [actual Whitney1936 scan](https://people.math.osu.edu/davis.12/courses/6701/whitney36.pdf), printed p.665, Lemma19 and footnote32, supports the `2n+1` embedding with finite limit points removed by inversion. I checked his countable/disconnected manifold conventions at pp.646-649. The smooth proper Whitney theorem is a legitimate standard input. A proper embedding has closed image; retaining its linear coordinates in the polynomial feature map retains properness and the embedding topology.

Whitney's pp.667-668, especially Lemma21 and the normal-neighborhood discussion preceding it, use a varying positive radius, not a compactness-dependent uniform radius. In the smooth case the normal planes themselves vary smoothly. This is the precise Euclidean tubular input required here. Nontrivial normal bundles cause no problem: normal projection and squared Euclidean normal norm are intrinsic bundle operations.

For an additional check of the smooth noncompact embedding mechanics, I read the complete seven-page [lecture proof](https://www.math.wustl.edu/~victor/classes/pmf/WhitEmb-Lec09.pdf). Its p.6 writes an incorrect formula for the bounded radial diffeomorphism; the correct map is `x/sqrt(1+|x|^2)`. This ancillary source is not cited by the candidate and is not treated as an unqualified proof certificate. The source map marks it ancillary. The standard argument survives this typographical error: after bounding an injective immersion, append a positive proper exhaustion and project along a generic nonvertical direction; the unbounded exhaustion term dominates the bounded term, preserving properness in dimension `2n+1`.

Existence of a smooth jet-bundle metric follows from paracompactness. The candidate's right inverse uses only fiberwise surjectivity and smooth matrix inversion, so no uniform bound is a dependency. All external inputs are ordinary differential topology, not a hidden statistical realization theorem.

## Lauritzen terminology and local-equivalence dependency

I read [Marugame v1](https://arxiv.org/pdf/2103.10102v1), Introduction, Sections2.1-2.4 and the entire proof of Theorem2.2 (pp.4-6), not only the theorem statement. The induced metric/connection convention agrees with the candidate. Definition2.1 has the same pair equations as its (5.1)-(5.2); Theorem2.2 is explicitly local. Its proof extends first-jet data and adds normal quadratic terms to gain positivity.

The candidate does not invoke this local theorem to assert globalization. It constructs the global exact pair and global variable-radius extension itself. Its description as a “Lauritzen-type pair” is appropriately qualified: the candidate establishes `f` is a global embedding and `phi` is an immersion, but does not claim `phi` is globally injective. The final Hessian realization does not require that extra property. Historical attribution to Lauritzen is checked as Marugame's attribution; I have not certified the body of Lauritzen's original 1987 workshop article.

## Independent reconstruction of the critical bridges

These calculations are my checks of the frozen proof, not conclusions borrowed from the dependency papers.

1. Put `A = nabla-L`, where `L` is Levi-Civita. Its first two indices are symmetric. Metric duality makes the dual difference its negative metric adjoint. Torsion-freeness of the dual supplies the remaining symmetry, hence `C = nabla g = -2 g(A(.,.),.)` is symmetric and `Gamma_ijk = L_ijk - C_ijk/2`.

2. At any point, choose `n` linear ambient functions with independent restricted differentials. They give coordinates near the point. Every scalar3-jet is a polynomial of degree at most3 in these coordinates, hence a restriction of a single element of the fixed finite polynomial space. This proves surjectivity of `E_p` without a finite chart cover. The matrix `E E^dagger` is smoothly invertible pointwise, giving the global smooth right inverse.

3. In Levi-Civita normal coordinates the prescribed scalar3-jet has value0, gradient0, Hessian `g` and third derivative `-C/2`. Under an arbitrary coordinate change, the third derivative gains the three connection-Hessian terms. Their sum is `1/2(partial_i g_jk + partial_j g_ik + partial_k g_ij)`. Thus the ordinary third derivative is exactly `Q_ijk = partial_k g_ij + Gamma_ijk`. No tensoriality of `Q` alone is assumed.

4. From the four scalar-jet identities `a f=0`, `a f_i=0`, `a f_ij=g_ij`, `a f_ijk=partial_k g_ij+Gamma_ijk`, differentiate only after the pointwise equations are established. With `phi=-a` this gives `f_i partial_j phi=g_ij` and `f_ij partial_k phi=Gamma_ijk`. The zero one-form `phi df=0` removes global period obstructions. The coefficients `a(p)` are held fixed only when evaluating the scalar jet; their derivatives are correctly included in the later identities.

5. The tubular formula `Psi_0(z)=phi_r(z)(nu(z))` has `dPsi_0|S=phi`. Therefore for any tangent direction `v`, `Hess(Psi_0)(f_*v,.)=dphi(v)`, an identity in all ambient covector components. Its tangent block is `g`, its normal-normal block is0, and the mixed block is unconstrained. Adding `lambda(r)|nu|^2` preserves value and gradient and adds `2lambda I` to the normal block. The pointwise Schur estimate in Section6 is valid; the positive-Hessian locus is an open neighborhood of the whole image, even with no uniform radius or lower bound.

6. In that open locus let `eta=dPsi`. Its derivative is the invertible positive Hessian, so it gives local coordinates. The formula `Gamma*^C_AB=G^{CD} partial_A G_BD` is the metric-dual of the standard connection. It is symmetric in `A,B`, and the covariant Hessian of each `eta_E` vanishes. Thus the dual is torsion-free and flat, without global injectivity of `eta`.

7. Along the image, `G(f_k,.)=partial_k phi`. Consequently the projected first connection has lowered coefficients `G(f_ij,f_k)=Gamma_ijk`, recovering the specified ordering. Projection of ambient duality makes the projected second connection the unique metric-dual of the first. Properness into the open target follows because its compact subsets are compact in the ambient Euclidean space.

I found no equivalent-hard unsupported realization assertion in this chain. Its geometric construction, rather than a numerical example or a local theorem, provides the global existence evidence.

## Version check, findings and exact remaining gap

The actual [Lê v6 PDF](https://arxiv.org/pdf/math/0506163v6), printed Theorems5.1 and5.6 at pp.15 and22, requires compactness; the proof surrounding5.1 uses it to choose one uniform scaling constant. The [arXiv version record](https://arxiv.org/abs/math/0506163v6) explicitly records compactness added in v6. This confirms the candidate's cautious citation scope. I did not audit every line of Lê's Theorem5.5 or use an older abstract to close the noncompact case.

**Required findings:** none.

**Optional editorial improvement:** cite Amari1997 directly at the source-interpretation paragraph, with pp.84-85 and87. It makes the torsion and local-coordinate reading directly checkable and prevents readers from treating the cached word “statistical” as an extra hypothesis silently added to the broader source quadruple.

**Strongest verified claim:** the frozen construction supplies, for every smooth positive-definite boundaryless statistical manifold with the stated standard manifold hypotheses, one finite-dimensional positive Hessian domain and a proper statistical embedding inducing the prescribed ordered dual pair. In the broader smooth Riemannian dual-pair category, both zero torsions are necessary and sufficient for this torsion-free dually flat realization. This resolves all of item1(a) in that explicitly stated category.

**Exact remaining gap:** none identified in source alignment, model definitions, standard dependencies or the reconstructed bridges. Historical novelty, optimal dimension, stronger target classes, original-script replay and independent whole-package acceptance are not established by this family. No paper, merge, release, native status promotion, external message or outreach was made.

`SOURCE_MAP.json` gives exact retrieval dates, URLs, byte counts, SHA-256 hashes and inspected page/body scope. Raw source bodies are intentionally absent from the curated packet. `MANIFEST.json` is an explicit allowlist of the review's final public files; it excludes `private/`, raw copyright material and temporary files.
