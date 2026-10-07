# Classical dependency and scope audit

Audit timestamp: 2026-10-06 21:13 PDT (2026-10-07 04:13 UTC).
Reviewer: independent subagent `classical_scope`.
Scope: exact classical hypotheses, normalization, correction and citation chain. This is not a certification of the upstream universal-optimality theorem or a completed priority audit.

Dependency checkpoint estimate: mathematical resolution 15%; publication package 1%. These conservative project-level estimates count the known universality transfer as validated, while the decisive new lower bound and upstream input remain unverified here.

## Strongest verified result

For every fixed `s>2`, the classical Hardin–Saff theorem yields

\[
\lim_{N\to\infty} \frac{E_s(M,N)}{N^{1+s/2}}
 = C_{s,2}\,\mathcal H^2(M)^{-s/2}
\]

for every compact smooth embedded surface of positive area, including smooth boundary. Distances and `E_s` are exactly the ambient Euclidean distances and the ordered-pair sum in the task. The classical theorem alone does not identify `C_{s,2}`; that remains the core gap.

## Hardin–Saff dependency

Primary source: D. P. Hardin and E. B. Saff, *Minimal Riesz energy point configurations for rectifiable d-dimensional manifolds*, Adv. Math. 193(1) (2005), 174–204, DOI [10.1016/j.aim.2004.05.006](https://doi.org/10.1016/j.aim.2004.05.006). Verified source: [arXiv:math-ph/0311024v3](https://arxiv.org/abs/math-ph/0311024v3), whose current PDF contains the four-page addendum followed by the paper. Local PDF hash and download source are in `sources/classical/SOURCE_MANIFEST.json`.

Exact locations: equation (2) defines the ordered-pair energy; Section 2 fixes Hausdorff measure so the unit `d`-cube has measure one; Theorem 2.1 and equation (9) give the Euclidean compact-set constant; equation (10) defines `C_{s,d}` by the unit-cube limit; definition (19) and Theorem 2.4 provide the manifold transfer. This is an actual limit, not merely a liminf. For `d=2`, the stated normalization of Hausdorff measure is ordinary surface area.

The precise class in definition (19) is a finite union of images `φ_k(K_k)`, with each `K_k` compact in `R^d` and `φ_k` bi-Lipschitz on an open neighborhood `G_k` of `K_k`. Theorem 2.4 invokes this class for `s>d`; its additional containment in a `C^1` manifold applies only to `s=d`. The addendum explicitly defines that latter auxiliary smooth manifold without boundary. That clause does not restrict the hypersingular branch used here.

The energy is invariant under ambient rigid motions and rescales by `E_s(aM,N)=a^{-s}E_s(M,N)`. Thus an isometric planar embedding into any `R^p`, `p≥2`, gives the same constant. On a curved surface the norm is the ambient chord norm, not geodesic distance.

### Why smooth boundary fits (independent check)

Take a smooth embedded manifold with boundary in its usual local parametrization sense. At an interior point, a parametrization is defined on a planar open set. At a boundary point, a smooth parametrization on a half-neighborhood extends smoothly to a full neighborhood, with injective derivative at the point. Let `T` be that derivative, and shrink a convex ball in the full parameter plane so that the derivative of the extension differs from `T` by less than half the smallest singular value of `T`. Integrating the derivative along a straight segment gives both a positive lower Lipschitz bound and a finite upper bound. Hence the extension is bi-Lipschitz on this full open ball. Compactness of `M` provides finitely many smaller compact chart patches covering `M`; their parameter preimages are compact subsets of these open balls. They satisfy (19). The extension's off-boundary image need not lie in `M`, because only the images of the chosen compact preimages need constitute `M`.

Consequently the paper should say explicitly “compact smooth embedded surface, possibly with smooth boundary,” and cite the hypersingular branch of Theorem 2.4 with definition (19). Disconnected compact surfaces are also covered. Positive area excludes the degenerate zero-area case, for which the classical normalized limit is infinite.

### Applicable correction and audit

The relevant addendum repairs the construction of relatively open `G_i` satisfying inequality (83) in Proposition 8.3. For `s>d`, it passes to a `d`-regular neighborhood and uses a deletion/projection estimate. The correction is not a change to the theorem's energy convention or manifold definition. The paper's footnote directing the reader to `arXiv:math-ph/0412053` is a broken identifier: that ID belongs to an unrelated scalar-field paper. Cite the addendum included in `math-ph/0311024v3`, rather than the erroneous footnote.

The current PDF was typeset with dates in November 2018 while the arXiv submission history still labels v3 as 15 December 2004. Such generated interior dates are not reliable public-priority dates. The arXiv history is the checked record for this version identifier.

The printed auxiliary Lemma 1 should be used with **compact closure of the neighborhood**. Its proof chooses `γ=dist(cl G,Ã\V)>0`, which is valid when `cl G` is compact. An unrestricted unbounded `G` would make the lemma false: in `Ã=R^d`, adjoin to `K` tiny open balls whose centers tend to infinity, with total measure below `δ`; the resulting unbounded set has minimal finite Riesz energy zero. This wording issue does not invalidate the needed compact application. Here is an explicit way to ensure compactness:

1. For each finite chart, cover `K_k` by finitely many closed cubes `Q` with `Q⊂G_k`.
2. Put `Ã` equal to the finite union of their images. It is compact. Each bi-Lipschitz cube image has uniform local upper/lower `d`-measure bounds; finite union preserves an upper bound by summing the bounds and a lower bound by selecting a component containing the center. Thus `Ã` is `d`-regular at sufficiently small uniform radii.
3. Choose an open neighborhood `H` of the compact piece within this compact `Ã`, with arbitrarily small `H^d(cl H\K)`. Apply the lemma to `H`; then intersect with `A` to obtain a relative neighborhood `G`. Since `cl_A G⊂cl_{Ã}H`, monotonicity gives the same lower estimate.

For completeness, the addendum's quantitative mechanism retains at least

\[
N\bigl(1-k\rho^s-2\delta/[c_0(\nu\rho)^d]\bigr)
\]

well-separated points within `νρN^{-1/d}` of `K`. Move them to `K`; their distances shrink by at most the factor `1-2ν`. This gives

\[
\underline g_{s,d}(G)\ge (1-2\nu)^s
\bigl(1-k\rho^s-2\delta/[c_0(\nu\rho)^d]\bigr)_+^{1+s/d}
\underline g_{s,d}(K).
\]

Setting `ρ=ν=δ^{1/(4d)}` makes the factor tend to one for `s>d`. The proof uses `k>\overline g_{s,d}(K)` to obtain its eventual energy bound; thus no illicit liminf-to-eventual-upper-bound conversion is required. The compact pieces with positive measure have finite upper normalized energy by bi-Lipschitz comparison with Theorem 2.1. This is a check of the relevant corrected argument, not a reproof of all of Hardin–Saff.

## Brauchart–Hardin–Saff exact conjecture

Primary source: J. S. Brauchart, D. P. Hardin and E. B. Saff, *The next-order term for optimal Riesz and logarithmic energy asymptotics on the sphere*, Contemp. Math. 578 (2012), 31–61. Verified both [the supplied author-hosted PDF](https://math.vanderbilt.edu/saffeb/texts/235.pdf) and [arXiv:1202.4037v1](https://arxiv.org/abs/1202.4037v1). The latter has one version submitted 17 February 2012 at 23:14:31 UTC.

Section 3.1, Proposition 1, supplies the lattice upper bound. Conjecture 2 states

\[
C_{s,d}=|\Lambda_d|^{s/d}\zeta_{\Lambda_d}(s),\qquad s>d,
\]

for dimensions `2,4,8,24`, with the respective hexagonal, `D_4`, `E_8` and Leech lattices. Thus this project's exact conjectural target is the **dimension-two case** of Conjecture 2. The rest of that conjecture and Conjecture 3's further asymptotic terms are outside this project.

There is an apparent coordinate typo in both checked BHS PDFs: the displayed basis uses `(0,1)` and `(1/2,√3/2)` while the text calls it hexagonal and assigns covolume `√3/2`. Those two vectors actually have determinant magnitude `1/2` and angle 30 degrees. The intended lattice is unambiguous from the covolume, the hexagonal name, Hardin–Saff (22), and the original Kuijlaars–Saff definition. Do not copy that basis typo.

## Original conjecture and normalization (primary citation-chain check)

Checked author-hosted primary paper: A. B. J. Kuijlaars and E. B. Saff, *Asymptotics for minimal discrete energy on the sphere*, Trans. Amer. Math. Soc. 350(2) (February 1998), 523–538, DOI [10.1090/S0002-9947-98-02119-9](https://doi.org/10.1090/S0002-9947-98-02119-9). Its Conjecture 1, page 527, is the original `s>2` sphere leading coefficient conjecture, and Theorem 5 proves the corresponding limsup upper bound. It counts **unordered** pairs in (1.1). Its source defines

\[
L=\mathbb Z(1,0)+\mathbb Z(1/2,\sqrt3/2),\qquad |L|=\sqrt3/2,
\]

and conjectures the unordered sphere coefficient

\[
\frac12\left(\frac{\sqrt3}{8\pi}\right)^{s/2}\zeta_L(s).
\]

The journal records receipt on 9 October 1995. The [University of Amsterdam institutional catalogue](https://dare.uva.nl/id/2e67074c-72a4-4908-bcf2-2a2957caca0a) records the same title/authors as mathematical preprint series 95-22, publication year 1995. These establish an earlier bibliographical disclosure trail but do not by themselves prove the exact conjecture was publicly accessible in that report's 1995 text: no digitized report text was available in the checked record. The exact checked public content is the 1998 journal PDF.

## Independent scaling reconciliation

Define the density-one/covolume-one triangular lattice explicitly by

\[
\Lambda=\sqrt{2/\sqrt3}\,L.
\]

Then `|Λ|=1` and

\[
\zeta_\Lambda(s)=(\sqrt3/2)^{s/2}\zeta_L(s).
\]

Doubling the Kuijlaars–Saff unordered coefficient and substituting this relation gives precisely

\[
\frac{\zeta_\Lambda(s)}{(4\pi)^{s/2}}.
\]

Likewise Hardin–Saff (23) is `C_{s,2}≤ζ_Λ(s)`. If the new lower-bound bridge establishes the reverse inequality, Hardin–Saff immediately supplies the surface conclusion, with no additional microscopic crystallization claim.

## Publication and validation boundaries

- A proof of `C_{s,2}=ζ_Λ(s)` settles a previously explicit exact constant conjecture, conditional on validation of the new input. Hardin–Saff already proved existence and area universality. The transfer to surfaces is inherited machinery, not an independent invention here.
- Saved PDFs and extracted texts are internal research copies of third-party primary sources. Do not include them in the Zenodo upload-kit without a redistribution basis; publish bibliographic links and hashes instead.
- No complete current novelty claim is made by this note. Searches were primary-source discovery and citation-chain checks, not a full audit of recent upstream companions or all equivalent formulations.
- No human external contact occurred. No Git staging, commits, pushes, branch operations, PR operations, or edits to other projects occurred.

## Reproduction of this audit

Read the manifest's exact local PDFs and use `pdftotext -layout <pdf> <output>` to inspect text. Search the theorem/conjecture numbers above. PDF interior dates can be generated at retypesetting time; use the arXiv history for public version timing. The downloaded source bytes, not a mutable URL alone, identify what was read.
