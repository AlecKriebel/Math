# Compact-core audit: PSC concordance composition

## Verdict

There is a rigorous **fixed-exterior partial result**, with an actual relative classification theorem available. It does not solve the Bohlen–Schrohe problem for all compatible metrics or for unrestricted Lie concordance.

The missing reference is Rosenberg–Stolz, *Metrics of positive scalar curvature and connections with surgery*, Theorem 5.1, author PDF pp. 20–21, with its relative construction on pp. 23–24. Thus one need not assert a boundary-relative version merely by analogy with the closed case. The author-hosted PDF is https://www.math.umd.edu/~jmr/psc.pdf .

## 1. Precise fixed-exterior setup

Let `(M,A)` be a Lie manifold and let `X = int(M)`. Let `g0` be a compatible complete PSC metric. Choose a smooth connected compact codimension-zero submanifold `W ⊂ X`, with ordinary smooth boundary `Y`, and a two-sided collar of `Y` on which

`g0 = dr² + h`, with `scal(h) > 0`.

This collar hypothesis is an additional assumption, not a consequence of arbitrary compatibility. Fix the collar germ, the identification of the exterior, and, for the spin formulation below, a spin structure on `W`.

Let `R⁺(W;h)` consist of smooth PSC metrics equal to `dr²+h` near `Y`. A relative concordance is a PSC metric `H` on `W×[0,L]` with temporal product collars and with the side fixed to `dr²+h+dt²` near `Y×[0,L]`. Collar widths may be shrunk while keeping the germ fixed; all gluing assertions below are made in this germ convention. One may fix numerical collar widths using a separate collar-normalization convention, but this is not needed for the claim.

Let `C_W(X;g0)` be the metrics on `X` obtained by extending elements of `R⁺(W;h)` by `g0` on `X\W`, modulo concordances which likewise equal `g0+dt²` on the exterior and on a neighborhood of the side. The duration `L` is allowed to vary; no artificial unit-length condition is imposed.

**Proposition 1.** Restriction and extension give inverse bijections

`C_W(X;g0) ≅ π̃₀ R⁺(W;h)`.

**Proof.** At the metric level, the common product germ makes extension smooth. Over the interior of a Lie manifold the anchor identifies `A` with the ordinary tangent bundle. A change on `W`, glued to `g0` on a neighborhood of its boundary, therefore extends to a smooth positive-definite metric on `A` without changing the germ at infinity. Positivity of scalar curvature is local, so it survives this gluing. Completeness survives a smooth change on a compact set. If uniform PSC is required, the positive minimum on the compact changed region and the unchanged exterior lower bound provide a positive global lower bound.

Exactly the same argument applies to `H` on `W×[0,L]`, adjoining `g0+dt²` outside. Conversely, an exterior-fixed concordance restricts to a relative concordance on `W`. The two operations are inverse before passing to concordance and preserve precisely the equivalence relations just defined. ∎

**Crucial distinction.** If the endpoints alone agree with `g0` outside `W`, but the intervening concordance may change the exterior, Proposition 1 does not identify their equivalence relation with relative concordance. There is only a natural surjection from `C_W(X;g0)` onto the set of unrestricted Lie-concordance classes represented by these metrics. Its injectivity requires an additional theorem. Likewise, a concordance supported in some larger compact core need not be supported in this fixed `W`.

## 2. The precise relative classification input

The following is a concise paraphrase of the applicable part of Rosenberg–Stolz Theorem 5.1. For a connected smooth compact `n`-manifold, `n≥5`, possibly with boundary, fix a PSC boundary metric which has a product-collar PSC extension. The relative concordance classes of such extensions are a torsor for `R_{n+1}(γ(W))`. Here `γ(W)` uses the actual fundamental group, the first Stiefel–Whitney character, and the extension encoding the second Stiefel–Whitney class. In the spin case, after fixing spin/classifying data, this is `γ=(π1W,0,π1W×Z/2)`, equivalently the spin `R`-group over `Bπ1W`. The proof explicitly works with `π̃₀R⁺(W rel h)` and its difference cylinder has side metric `h+dt²`. See [Rosenberg–Stolz, Theorem 5.1 and pp. 23–24](https://www.math.umd.edu/~jmr/psc.pdf).

No hypothesis that `Y→W` induce an isomorphism on fundamental groups is present. Nor is a Baum–Connes assumption needed. It would be incorrect to replace the actual `π1W` by an arbitrary reference group and retain a torsor conclusion without checking the corresponding connectivity/normal-type hypotheses.

## 3. Unconditional compact-core group law under explicit hypotheses

**Corollary 2.** Add to Proposition 1 the assumptions that `n=dim W≥5` and `W` is spin, with fixed spin structure and classifying data for `π=π1W`. Then `C_W(X;g0)` is a torsor for `R^{spin}_{n+1}(Bπ)`. The class of `g0` determines an abelian group structure on this set.

**Construction and proof.** Write `A=R^{spin}_{n+1}(Bπ)`, `S=π̃₀R⁺(W;h)`, and `s0=[g0|W]`. Apply the cited relative classification theorem to obtain its free transitive action. Let

`a:S→A`, defined by `a(s)·s0=s`.

The function `a` is a bijection, with `a(s0)=0`. Define

`s ⋆ t = a⁻¹(a(s)+a(t))`, and `s⁻¹ = a⁻¹(−a(s))`.

This gives associativity, commutativity, inverses and identity by transport from the abelian group `A`. Transport once more through Proposition 1. This is a geometric classification-based operation on endpoint concordance classes, not concatenation of concordances. Its geometric input is the relative surgery/classification theorem; the argument does not prove a new surgery theorem at infinity. ∎

A sign convention for an explicitly written difference cylinder may replace `a` by `−a`. This does not change the transported binary law, provided the convention is used consistently.

The nonspin version may be stated with the full canonical `γ(W)` and its corresponding `R`-group, but the spin statement above is sufficient and avoids suppressing essential normal-type data.

**Scope.** This is a standard compact relative theorem transferred into the unchanged interior of a Lie manifold. It is not a claim of a new classification of Lie PSC metrics. Any claim of independence from `W`, agreement with unrestricted Lie concordance, or compatibility with an intended groupoid/secondary-invariant construction still needs its own argument.

## 4. What doubling does and does not prove

Let `DW=W∪Y(−W)` with collars glued. Two different maps should not be confused:

1. The based-half extension sends `g` to `g∪g0|W` on `DW`.
2. The symmetric double sends `g` to `g∪g`.

Both are smooth PSC metrics because of the common product collar. A relative concordance extends to a closed concordance, using `g0|W+dt²` on the second half for map 1 or the reflected concordance for map 2. Consequently each gives a well-defined map from relative concordance classes to closed concordance classes.

The naive doubling argument supplies **no converse**: a closed concordance of doubles need not preserve the gluing hypersurface metrically, keep the reference half fixed, or yield a product-collar relative concordance upon restriction. A restriction of a PSC ambient metric to an arbitrary hypersurface need not have PSC. Therefore injectivity is not a consequence of gluing alone. This audit does not assert a counterexample or rule out proving injectivity of a particular doubling map with additional relative-theory/naturality arguments.

Even an injective set map into the closed based group does not automatically transfer a group law: one must also establish that its image is a subgroup and that the chosen doubling convention respects the intended geometric operation. Corollary 2 bypasses these gaps by applying the actual relative theorem directly. In particular, a citation only to Xie–Yu–Zeidler Proposition 4.1, which addresses closed spin manifolds, is not a substitute for the relative input.

## 5. Why variable boundary data in the b-category remain outside this partial

For an exact cylindrical b-metric near a boundary hypersurface,

`g = dx²/x² + h`, equivalently `g = dr²+h` for `r=−log x`,

a change from `h0` to a different `h1` persists arbitrarily far down the cylindrical end. It is not supported in any compact interior `W`. Thus the fixed-exterior theorem does not compare such endpoints.

Furthermore:

- Agreement of the leading b-boundary metric is weaker than agreement of the entire metric on an end. Nonzero smooth b-perturbations can decay as `x→0` without vanishing on any collar.
- A general b-metric can have a varying normal coefficient and mixed normal/tangential terms. It is not legitimate to assume it is exactly `dr²+h` without a proved deformation that preserves the required PSC and concordance conditions.
- Allowing the end data to vary during a concordance changes the equivalence relation. A relative compact classification does not show that the newly identified classes form a congruence for `⋆`.
- A PSC path of boundary metrics, when it exists, can often be stretched to make a PSC cylindrical interpolation. Arbitrary pairs need not admit such a path, and choices of interpolation and their coherences are additional data. Boundary concordance is also different from choosing an isotopy.
- A general Lie structure may not reduce to one ordinary cylindrical boundary. Corner compatibility, anchor degeneracy, and asymptotic structure remain outside the compact construction.

Consequently this partial result neither defines the operation for arbitrary compatible b-PSC endpoints nor provides the requested general Lie-manifold surgery theorem.

## 6. Separate check: boundary reduction of a uniformly b-PSC concordance

The following calculation supports a distinct proposed test case; it is not used in Corollary 2.

Assume `X=Y×R` has its standard two-ended b-compactification and a concordance `G` is smooth as a metric on the product b-tangent bundle, uniformly PSC, and temporally product near endpoints `dr²+h_i`. At either spatial b-face, freezing coefficients yields an `R`-invariant metric

`G∞=f²(dr+α)²+H`

on `R×B`, where `B=Y×[0,L]`, `f>0`, and `m=dim B≥2`. In a convention where the squared curvature term is `f²|dα|²/4`, the one-dimensional submersion formula and conformal scalar-curvature formula give

`scal(G∞)=scal(H)−2f⁻¹Δ_H f−f²|dα|²/4`,

`f^{2/(m−1)} scal(f^{2/(m−1)}H) = scal(G∞)+f²|dα|²/4+[m/(m−1)]|d log f|²`.

Here `Δ=div grad`; a different norm convention for two-forms may alter the displayed `1/4`, but the sign stays nonnegative. Uniform positivity of `G`, together with smooth convergence of its b-coefficients and curvature, supplies `scal(G∞)>0`. The conformally modified base metric is therefore PSC. At temporal collars `f=1` and `α=0`, so it equals `h_i+dt²`. This produces a closed PSC concordance between `h0` and `h1` on `Y`.

The algebra checks out. The uniform boundary-positive assumption is indispensable to this argument: mere strict positivity at interior points can have zero boundary limit. The quotient formula does not require a compact circle fiber; it is local for an invariant one-dimensional fiber. This check does not supply a group law for all b-metrics.

## Source and inspection record

- Bohlen–Schrohe report in *Oberwolfach Report* 36/2017, pp. 2275–2278: original open problem read from the recovered source, especially p. 2278. The target is composition of endpoint-metric concordance classes relative to a reference metric, not temporal concatenation.
- Xie–Yu–Zeidler, *On the range of the relative higher index and the higher rho-invariant for positive scalar curvature*, Section 4, Proposition 4.1: https://arxiv.org/abs/1712.03722 . Read from the recovered source. It concerns the closed spin case and identifies the two cited closed constructions.
- Rosenberg–Stolz, *Metrics of positive scalar curvature and connections with surgery*, Theorem 5.1: https://www.math.umd.edu/~jmr/psc.pdf . Freshly retrieved and inspected on 2026-10-20; 338,398 bytes; SHA-256 `8d1c41dcffbea9202b102a2a8ab9f856bfbb3b77537fe4c5f9946a6cc38e59e4`. Theorem numbering is 5.1 in both the author PDF and the inspected collected-volume copy. Author-PDF pp. 21 and 23 were also visually inspected. The file contains a proof sketch, not a new full proof supplied by this audit.

All prose and deductions in this audit are authored analysis. No copied source-document pages or dataset contents are included.
