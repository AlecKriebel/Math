# Fresh independent adversarial proof review 01

Review checkpoint: 2026-10-17 20:25 UTC (13:25 America/Los_Angeles).

Reviewed artifact: `../CANDIDATE_PROOF.md`, headed “Candidate proof: a two-tail order automorphism,” version timestamp 2026-10-17 20:24 UTC. This reviewer did not author that proof. No source proof edits or version-control operations were made by this reviewer.

## Verdict

**No substantive mathematical objection found to the explicit theorem for the two stated master groups `A_I` and `A_R`, after the minor interval-definition correction below.** I independently reconstructed every step and attempted to break the proof using unbounded action components, nonuniform endpoint germs, reversed embeddings, arbitrary slope groups, and infinite local breakpoint sets.

This is not a certification that Kourovka 21.149 is solved or that the theorem is original. The candidate itself makes the passage from its explicit master groups to *all* intended Dlab groups conditional. I did not close that primary-definition gap. Nor is this a review of a final preprint package, which does not yet exist in the reviewed materials. The source-definition, priority, and final-package gates remain substantive.

Best-guess completion estimate for my assigned adversarial proof audit: **100% of this review pass**. Best-guess completion toward a publishable original complete solution of the Notebook problem: **not independently estimable until the scope and priority gates are closed**.

## Required minor correction

Section 1 says “for every relatively compact open L in (0,1)” before declaring `G(L)` simple and affine-isomorphic to `G`. This must say **every nonempty open interval L=(a,b) with 0<a<b<1**. A disconnected relatively compact open set need not give a simple local group. All subsequent applications, including the bump intervals and the four-point transitivity argument, use intervals, so this correction does not alter the mechanism.

For publication, define group support as the union of supports of its elements and specify that individual support means the open moved-point set. The present use is consistent but implicit.

## Detailed independent checks

### 1. Ambient groups and support order

The stated classes are groups. If `f` and `g` have positive affine right germs at every relevant finite point, then so do `fg` and `f^-1`: an increasing map sends a sufficiently small right neighborhood to a right neighborhood. The eventual affine condition on the initial real ray is likewise closed under composition and inversion.

The well-order assertion for support components is valid. For a nonempty chosen subfamily, let `a` be the infimum of its left endpoints. If `a` is finite and `q(a) != a`, continuity gives an open neighborhood of `a` inside a single support component, excluding left endpoints arbitrarily close to `a`. Hence `q(a)=a`. If its affine right germ has slope 1, that germ is the identity, again excluding chosen endpoints approaching `a`. Otherwise the germ determines a support component beginning at `a`. A chosen subfamily omitting that component cannot have infimum `a`, because every other component starts at or to the right of its right endpoint. Thus it is the first chosen member.

For a real target, an eventual nonidentity affine map moves every point in some initial ray, so there is an initial support component. Omitting it bounds the other components below. An eventual identity bounds all support below. These are enough to cover the possible infimum `-infinity` and do not presuppose a left endpoint for arbitrary action components of a subgroup.

I specifically checked that support components can accumulate from the left at finite points or at the right boundary. This is permitted and does not defeat well-ordering. The excluded phenomenon is an infinite descent of components toward a finite point from its right, exactly what the right-germ condition forbids.

At a common finite fixed point, right slope is a homomorphism to the abelian group of positive reals. The eventual real affine germ is a homomorphism to `Aff_+(R)`, whose derived subgroup is contained in the abelian translation group. A perfect group's image in either target is trivial. Thus every element of `e(G)` fixes some initial real ray, or some interval after 0 in the interval case. **No common initial ray for the entire subgroup is claimed or needed.** This distinction is essential and the candidate respects it.

### 2. Simplicity of the source and its interval subgroups

Dlab's original Section 2 defines the compact-support group by identity in neighborhoods of both interval endpoints, and Theorem 4.3 asserts its algebraic simplicity. The particular group with slopes in `2^Z` is nonabelian: finite bumps can be conjugated by finite bumps that move their supports. It is therefore perfect. For an interval `L=(a,b)` as corrected above, affine conjugation between `[0,1]` and `[a,b]`, followed by identity extension, identifies this group exactly with `G(L)`. Affine conjugation leaves slopes unchanged even when `a,b` are not dyadic. Each local group is therefore also simple and perfect.

I read the locally-right-affine definition and the cited simplicity/order statements in the archived original Dlab text. Their use here does not impose an unmentioned dyadic-breakpoint restriction.

### 3. Perfect centralizers

If `p` commutes with `q`, it maps the moved-point set of `q` to itself and induces an increasing bijection of its support components. Every increasing bijection of a well-ordered set fixes every element. Thus a perfect centralizing subgroup `P` fixes each component `J=(a,b)` setwise and fixes its finite left endpoint `a`.

Perfection kills the right-slope homomorphism at `a`. Every `p` is consequently identity on a right neighborhood of `a`; the neighborhood may depend on `p`. Since `q|J` has no fixed point, either its forward or its backward iterates send each point of `J` toward `a`. Commutation propagates this identity to every point of `J`. This proof works for either displacement sign of `q` and for `b=+infinity`.

For disjoint source intervals `L,M`, apply this statement to any `q in e(G(L))` and the entire perfect subgroup `e(G(M))`. It follows that the unions of their moved-point sets are disjoint, not merely that selected individual supports are disjoint. No target order or slope-rank assumption enters.

### 4. Least global and local action components

An action component is invariant under the acting group because its finite endpoints lie in the common fixed set. The restriction kernel on a nontrivial component is a proper normal subgroup of the simple source, so restriction is faithful.

Fixing one nonidentity `f in G` is enough to select the least global action component: faithfulness implies that every action component contains a support component of `e(f)`. Since those individual components are well ordered, the one lying furthest left determines the least action component `J0`.

Within `J0`, every nontrivial `G(L)` acts nontrivially by global faithfulness. Its nontrivial action components are faithful by local simplicity. Apply the same fixed-element argument to a local nonidentity element to obtain `K(L)`. The boundary of `J0` is fixed by the whole source, so these components are also global local-subgroup components; no component is cut spuriously by restriction to `J0`.

I tested the case `J0=(-infinity,b)` even though each individual source element fixes an initial ray. The argument still works and makes no unsupported assertion that the subgroup's entire support is bounded below. The same observation covers potentially unbounded `K(L)`.

Equivariance is exact: conjugation by `g` sends `G(L)` onto `G(gL)` because homeomorphisms carry compact subsets of `L` onto compact subsets of `gL`. Since `e(g)` preserves `J0` and is increasing, it sends the least local component to the least local component.

### 5. Four-point transitivity and uniform orientation

The explicit interpolation calculation is correct. For a source segment of length `s` and target length `t`, put `r=t/s` and `p=2^k` with `p<=r<=2p`. The proposed proportions are

`lambda=(2p-r)/p`, `1-lambda=(r-p)/p`.

They are nonnegative, add to one, and give average slope

`p*lambda+2p*(1-lambda)=r`.

Choosing common fixed exterior points and interpolating between all successive prescribed coordinates gives a finite piecewise-affine group element with support in the interior. Cases `r=p` or `r=2p` simply omit a zero-length piece. Thus four-point transitivity on endpoints of positively separated interval pairs holds.

The relative order of `K(L)` and `K(M)` is therefore the same for every ordered separated pair `L<M`: one group element carries the four source endpoints to any other such four endpoints; its image in the target preserves the order of the disjoint selected components. Either the global choice preserves this interval order or it reverses it. No continuity, cofinality, or target-order compatibility of the interval-to-component map is assumed.

As an ancillary arithmetic check, I independently tested 10,000 exact-rational source/target length pairs. Every resulting interpolation proportion and average-slope identity passed. These finite checks are not used as a replacement for the displayed identity.

### 6. The two-tail normalizer and the automorphism

The two formulas for each bump agree at `a+(b-a)/3`, with image `a+2(b-a)/3`; they fix the endpoints, have slopes 2 and 1/2, and are strictly above the identity inside. The `C_m` and `D_m` have positive intervening gaps and accumulate only at 0 and 1. On every compact subset of `(0,1)`, there are only finitely many bumps. Identity outside them and vanishing bump lengths give a continuous increasing homeomorphism on the closed interval. The inverse has the same interior locally finite piecewise-affine property.

For arbitrary `f in G`, including elements with infinitely many breakpoints, `h^-1 f h` is identity near both endpoints because `f` is and `h` preserves endpoint neighborhoods. On every interior point, composition of the three positive affine right germs is again a positive affine right germ with slope in `2^Z`. The same holds in the reverse direction, so this is an automorphism of the full locally-right-affine source, not only its finite PL subgroup.

Let `a` be the leftmost support endpoint of `f`, and `y=h^-1(a)`. If `h` has right slope `mu` at `y` and `f` has right slope `lambda` at `a`, then the conjugate's right slope is `mu^-1*lambda*mu=lambda`. The support is transported increasingly. Dlab's classification of the two source orders consequently gives order preservation for both.

Since each bump interval is setwise fixed by `h`, its local subgroup is invariant. The restriction of the automorphism is nontrivial: choose a compact interval `V` small enough that `V` and `h^-1(V)` are disjoint and a nonidentity finite bump inside `V`. Its conjugate has a different support. This choice is possible by continuity at any nonfixed point of the bump.

I also checked the breakpoint and gap identities using exact rational arithmetic for the first 20 bump intervals. The displayed general formulas prove them for every index.

### 7. The contradiction for a purported target conjugator

The equation `e(alpha(f))=u^-1 e(f)u` makes `u` a normalizer of the global image and, for each designated bump interval, its local image. Hence `u` fixes `J0` and `K(L)` setwise. This does not require the whole families of global/local action components to be well ordered; their existence of a least member suffices.

If `u` is identity on `K(L)`, then so is its inverse, and every `e(f)` for `f in G(L)` preserves `K(L)`. The conjugation equation restricted there gives `e(alpha(f))|K(L)=e(f)|K(L)`. Both source elements lie in the local group, whose restriction is faithful. This forces `alpha(f)=f` for every local element, contradicting the constructed nontrivial local restriction.

Therefore `u` moves a point in every `K(L)`. As its boundary is fixed by `u`, a global support component of `u` through that point is contained in `K(L)`, including when an endpoint is infinite. In the preserving orientation, the `C_m` yield a strictly descending sequence of such components. In the reversing orientation, the `D_m` do. This contradicts the proved well-ordering of the individual support components of `u`.

## Counterexample and scope stress tests

1. **Higher-rank slopes in the target:** harmless. Only perfection, positive finite germs, and the initial affine germ are used.
2. **Embeddings reversing the geometric interval order:** harmless. The second bump tail handles exactly this case.
3. **Source or target elements with infinitely many breakpoints:** harmless under the pointwise right-germ assumptions; no uniform local finiteness of an arbitrary source element was used.
4. **Subgroup support unbounded below:** harmless. Individual support well-ordering and restriction faithfulness supply the least action components.
5. **Dropping the initial affine condition on the real target:** genuinely unsafe. The germ reduction and component well-ordering need not survive. The candidate explicitly retains this hypothesis and does not prove a theorem for that larger class.
6. **Disconnected local supports or interval unions:** genuinely unsafe for the simplicity claim. This is why the interval definition above must be repaired.

## Exact Notebook and primary-scope finding

The archived current authoritative Notebook statement, lines 9574–9576 of the October 6, 2026 text, includes conjugation in a “possibly bigger” Dlab group. The proof's arbitrary embedding quantifier is strong enough to address that feature if all intended target groups belong to the two explicit master classes up to coordinate identification.

[Dlab 1968](https://doi.org/10.1017/S1446788700006261) directly gives the interval locally-right-affine setting. I independently attempted to retrieve [Zenkov–Medvedev 1999](https://www.mathnet.ru/rus/al2480), including its primary full-text endpoint. The metadata and indexed primary excerpts were accessible, but direct full-text opening failed. I did **not** inspect a definition page or PDF image establishing the initial real affine germ for every intended extended-real Dlab family. Therefore this review does not replace the pending primary-scope audit with an inference from terminology or a later author's restricted theorem.

The September 2026 Gong–Yang–Zeng argument is relevant prior art. I did not conduct a full independent novelty audit here, and my mathematical verdict must not be represented as an originality verdict.

## Disposition

After correcting “open L” to “open interval L,” this reviewer has **no outstanding substantive objection to the explicit master-group theorem**. The checkable derivations above record why. Promotion to an original complete resolution of 21.149 still requires the already identified scope and priority work and the later fresh review of the complete paper and reproducibility package.
