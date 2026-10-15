# KP-4.100: fixed-form ruled case and formal reductions

Date: 10 October 2026.

This AI-assisted manuscript is unrefereed. The accompanying acceptance records a mathematical audit, not external human peer review, journal acceptance, or formal proof-assistant certification. Scholarly inspection and bounded-search observations below describe the recorded proof review; preparation of this edition performed no new source retrieval, source-file rehash, inspection, literature search, or mathematical-check rerun.

## Status and exact target

This document does **not** solve or refute the universal assertion. It proves a fixed-form product-ruled special case, records the precise formal-immersion reduction, and rules out a particular class of gauge-theoretic counterexample searches. The product case belongs to the established rational/ruled literature; no novelty is claimed.

The target is a closed connected symplectic four-manifold `(X, omega)`, an integral class `c`, and a connected oriented smoothly embedded closed surface `S` of genus `g` with

    omega(c) > 0,
    c1(TX,omega)(c) = 2 - 2g + c^2.

Equivalently, with `K = -c1(TX,omega)`,

    2g - 2 = c^2 + K(c).

The question is the existence of **some embedded connected omega-symplectic surface in the same integral class c**. Neither isotopy of the input embedding nor changing omega is requested. Immersed, disconnected, or multiple-class conclusions are insufficient.

The original statement was checked against actual PDF pages 272–273 of the K3 problem list. Its pairing typography and the sign above are unambiguous. A later remark uses “canonical class” for `c1`; the displayed equality, rather than that phrase, fixes the sign.

## 1. What the hypotheses actually give formally

**Proposition 1.** Under the target hypotheses, the given embedding has a formal isosymplectic deformation of its differential, and `c` has a connected omega-symplectic immersion of the same genus. After a generic symplectic-preserving perturbation, its numbers of positive and negative transverse double points satisfy

    d_plus = d_minus.

**Proof.** Write `i:S -> X` for the embedding and fix an omega-compatible almost-complex structure `J`. Give `S` a compatible complex structure `j`. A complex-linear bundle monomorphism

    F: TS -> i^*TX

exists: the zero locus of a generic section of the complex rank-two bundle `Hom_C(TS,i^*TX)` is empty on the real two-dimensional base. Its quotient complex line bundle has Euler number

    c1(TX,J)(c) - chi(S) = c^2.

The quotient of `di` also has Euler number `c^2`. The real-monomorphism classification in Li, Remark 2.5, therefore places `F` and `di` in the same component. Equivalently, the sole two-dimensional obstruction, the quotient Euler-number difference, vanishes. The relevant real Stiefel fiber is simply connected and has second homotopy group Z; the Euler-number change is twice the associated obstruction.

Choose a positive area form `sigma` on `S` of total area `omega(c)`. Since `F^*omega` is positive, pointwise multiplication of `F` by the positive square root of the ratio `sigma/(F^*omega)` makes it isosymplectic. This multiplication is through monomorphisms. The cohomological condition `i^*[omega]=[sigma]` holds because their integrals agree. Gromov's immersion h-principle, in the form recorded by Li, Theorem 2.7 and Proposition 2.8, yields the claimed same-genus symplectic immersion `f` homotopic to `i`.

Its symplectic normal bundle has Euler number

    e(N_f) = c1(TX,omega)(c) - chi(S) = c^2.

The signed self-intersection formula is

    c^2 = e(N_f) + 2(d_plus - d_minus).

Thus the signed sum vanishes. Symplecticity is C1-open, so self-transversality can be achieved without losing it. This proves the proposition. QED.

**The missing step is geometric, not arithmetic.** Equality of the two double-point counts does not imply that both are zero. One cannot apply the codimension-at-least-four embedding h-principle to a surface in a four-manifold.

Nor do symplectic sheets automatically have positive intersections. In standard symplectic R4 with

    omega0 = dx1 wedge dx2 + dx3 wedge dx4,

let the oriented planes have bases

    P: (e1,e2),
    Q: (e1+e3, 2e2-e4).

The omega0-area of each displayed ordered basis is 1, while the determinant of the concatenated ordered bases is -1. The intersection is negative. Thus an arbitrary symplectic immersion need not be holomorphic for a single ambient omega-tame J at its double points.

A same-genus, self-transverse symplectic immersion having only positive double points would indeed be embedded by Proposition 1. No theorem supplying that positivity in this generality has been established here.

## 2. A complete fixed-form special case

**Theorem 2.** Let `X=S^2 x Sigma_h`, where `Sigma_h` is a closed connected oriented surface of genus `h >= 0`, and let

    omega = pi1^*sigma + pi2^*tau

be any split symplectic form, with both area forms positive. Then the assertion of KP-4.100 holds for every integral class in `H2(X;Z)`.

This includes negative-square section classes and nonprimitive square-zero classes. The proof constructs a representative for the original fixed form.

Put

    F = [S^2 x {point}],     B = [{point} x Sigma_h],
    lambda = integral_S2 sigma > 0,
    mu = integral_Sigma tau > 0.

Write `c=aF+bB`, with `a,b` integral. Since `F^2=B^2=0` and `F.B=1`,

    c^2 = 2ab,
    K(c) = -2a + (2h-2)b,
    g = 1 + a(b-1) + b(h-1),
    omega(c) = lambda*a + mu*b.

We first give two constructions.

### 2.1. Every positive-area section class

For every integer `a` with `mu+a*lambda>0`, the class `aF+B` has a symplectic graph representative.

If `a>=0`, take a smooth map `f:Sigma_h -> S^2` of degree `a` with `f^*sigma >= 0`; its graph has pullback form `tau+f^*sigma>0`.

Such a map can be constructed on `a` pairwise disjoint discs, mapping each disc onto the sphere with degree +1 and collapsing a collar of its boundary to a point, and extending constantly over the complement. Smooth radial maps flat at the collar boundary make this a smooth map with nonnegative Jacobian. The degree-zero case is constant. Reversing the orientation in each disc gives the analogous degree `-k` map with nonpositive Jacobian, for every `k>=1`.

For `a=-k<0`, choose such a map and put `rho=-f^*sigma>=0`. Its integral is `k*lambda`. The assumed area inequality is `mu>k*lambda`. Hence

    t = (mu-k*lambda)/mu > 0,
    tau_prime = rho + t*tau

is a positive area form with the same integral as `tau`. Moser's theorem gives an orientation-preserving diffeomorphism `phi`, isotopic to the identity, with `phi^*tau_prime=tau`. The graph of `f composed with phi` then has pullback form

    tau + phi^*f^*sigma
       = phi^*(tau_prime-rho)
       = t*phi^*tau > 0.

Its degree, and therefore its integral homology class, is unchanged. Notice that the ambient omega has not been changed.

### 2.2. Connected pure multisections when h>=1

For each `b>=1`, choose a smooth map `theta:Sigma_h -> S^1` inducing a surjection on fundamental groups. Inside a small disc in the S2 factor form

    C_b = { (z,x) : z^b = epsilon^b theta(x) }.

Here `|z|=epsilon`; the derivative of `z -> z^b` is nonzero, so this is an embedded unbranched `b`-fold cover of the base. It is connected because the monodromy onto Z/b is surjective. Its projection to S2 has image in a circle, so its homology class is `bB`.

The vertical derivative of a local sheet has real rank at most one, so the pullback of `sigma` is zero. Therefore the restriction of the split omega is the positive pullback of `tau`. Its genus is

    g(C_b) = 1 + b(h-1).

For any `a>=0`, add `a` distinct sphere fibers. Arrange `theta` to be constant on small neighborhoods of their base points. Each fiber meets the multisection in exactly `b` positive, product-orthogonal points. The standard local symplectic smoothing of these `ab` nodes yields an embedded connected symplectic representative of `aF+bB`. The genus is

    1 + b(h-1) + a(b-1),

as required. Connectedness holds because `C_b` is connected and each added fiber meets it.

### 2.3. Exhaustion of the hypotheses for h>=1

Assume a connected smooth representative has the specified adjunction genus and positive area.

If `b<0`, positive area forces `a>=1`. Therefore

    g = 1+b(h-1)+a(b-1) <= b*h < 0,

a contradiction.

If `b=0`, positive area forces `a>=1`, and `g=1-a>=0` forces `a=1`. The sphere fiber represents this class symplectically.

If `b=1`, the section construction applies for every allowed `a`.

If `b>=2`, projection of the smooth representative to `Sigma_h` has degree `b`. The Kneser degree inequality gives

    g >= 1+b(h-1).

Comparing with the prescribed genus forces `a(b-1)>=0`, hence `a>=0`. The multisection-and-fiber construction applies. This exhausts every integral class when `h>=1`.

### 2.4. Exhaustion when h=0

Now `g=(a-1)(b-1)>=0`. If both `a,b>=1`, smooth the positive product grid of `a` sphere fibers and `b` horizontal spheres; its graph of components is connected and the genus is `(a-1)(b-1)`.

Otherwise both `a,b<=1`. Positive area excludes `a,b<=0` simultaneously, so `a=1` or `b=1`. These are section classes for one of the two product projections. Apply the section construction above, interchanging the factors if necessary. This also includes the pure fiber classes. QED.

The Kneser inequality used here is the classical bound for nonzero degree maps of oriented closed surfaces; a modern elementary proof is Ryabichev, arXiv:2401.01041. The ruled-surface context is already covered by the work of Li–Li, Li–Liu, Lalonde–McDuff, and later Dorfmeister–Li–Wu. Theorem 2 is an explicit restricted verification, not evidence of new progress on the general four-manifold case.

## 3. A counterexample strategy that the smooth hypothesis blocks

**Proposition 3.** Suppose the target hypotheses hold, `b2^+(X)>1`, and `g(S)>0`. For every Seiberg–Witten basic class `L`,

    |L(c)| <= K(c).

In particular `K(c)>=0`. If an integral class `A` has `K-2PD(A)` basic, then

    0 <= A.c <= K(c).

**Proof.** Symplectic four-manifolds with `b2^+>1` have Seiberg–Witten simple type. For `c^2>=0`, apply the usual adjunction inequality; for `c^2<0`, apply Ozsvath–Szabo, Corollary 1.7, whose positive-genus and simple-type hypotheses are now satisfied. In either case

    |L(c)| + c^2 <= 2g(S)-2 = K(c)+c^2.

Taking `L=K` gives `K(c)>=0`. Taking `L=K-2PD(A)` gives

    -K(c) <= K(c)-2A.c <= K(c),

which is the asserted interval. QED.

Consequently one cannot refute the target in this positive-genus, `b2^+>1` range by exhibiting negative intersection with a Taubes class of this basic-class form: that purported input already violates a smooth adjunction inequality. This proposition makes no corresponding claim for genus zero, arbitrary stable classes, or `b2^+=1` chambers.

## 4. Literature checks and remaining gap

Primary sources checked during this attempt include:

- K3, Problem 4.100, actual PDF pages 272–273: https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf
- Tian-Jun Li, *Existence of symplectic surfaces*, Proposition 2.8, Remark 2.5, Theorems 2.6–2.7, Section 3: https://arxiv.org/abs/0812.4929
- Ozsvath–Szabo, *The symplectic Thom conjecture*, Theorem 1.1, Corollary 1.7 and Section 3: https://arxiv.org/abs/math/9811087
- Bang-He Li and Tian-Jun Li, *Symplectic genus, minimal genus and diffeomorphisms*, Theorems A–C and Section 3: https://arxiv.org/abs/math/0108227
- Dorfmeister–Li–Wu, *Stability and existence of surfaces in symplectic 4-manifolds with b^+=1*, Theorems 1.3, 1.8–1.9: https://arxiv.org/abs/1407.1089
- Li–Usher, *Symplectic forms and surfaces of negative square*, Section 2: https://arxiv.org/abs/math/0601540
- Ryabichev, *Short proof of the Kneser–Edmonds theorem on the degree of a map between closed surfaces*: https://arxiv.org/abs/2401.01041

The recorded bounded searches for the exact question, adjunction-equality sufficiency, converse symplectic Thom formulations, surface stability counterexamples, and same-class symplectic representability did not identify an exact general resolution. This is not a certificate of openness.

DLW Theorem 1.3 still requires a preexisting symplectic curve configuration. Its Theorem 1.8 does give exact sufficiency for square -4 smooth spheres in rational manifolds; Theorem 1.9 gives exact sufficiency for smooth sphere classes in irrational ruled manifolds. Those are credited special cases, not counterexamples or proofs of the arbitrary-manifold assertion.

No concrete input satisfying all target hypotheses and obstructing every same-class omega-symplectic embedding was found. Conversely, the balanced-double-point reduction contains no method for removing those points in general. The universal statement therefore remains unresolved by this attempt.
