# No finite additive intersection constant for general plane domains

**Problem:** Hayman–Lingham, Problem 7.73 (W. H. J. Fuchs); problem 2307073, queue row 1664.  
**Result:** For every radius R > 0, the requested finite upper constant does not exist.  
**Credit:** This is the obstruction proved by Yixin He and Quanyu Tang, *On Fuchs's additive intersection problem for the hyperbolic metric*, arXiv:2603.16676v1 (17 March 2026), Theorem 1.2 and Section 3. The argument below is an independently checked exposition of that existing result, not a novelty claim. [Versioned manuscript](https://arxiv.org/abs/2603.16676v1).

## 1. Exact question and conventions

Write D_R = {z in C : |z| < R}, and let D denote the unit disk. The original question permits arbitrary plane domains D_1, D_2 contained in D_R; it does not impose simple connectivity, boundary regularity, or absence of punctures. It asks for a number A = A(R) making

\[
\lambda_{D_1\cap D_2}(z)
 < A\bigl(\lambda_{D_1}(z)+\lambda_{D_2}(z)\bigr)
\tag{1}
\]

hold for every allowed pair and every common point z. Here a domain is a nonempty connected open set. If an intersection has more than one component, its density at z means the density of the component containing z. The examples below have connected intersections, so the conclusion also holds if the question is restricted to pairs with connected intersection. See Hayman–Lingham, *Research Problems in Function Theory (New Edition)*, arXiv:1809.07200v2, Problem 7.73, printed p. 183 / PDF p. 184. [Original source](https://arxiv.org/pdf/1809.07200v2#page=184).

Use the complete hyperbolic metric of curvature -4, with disk density

\[
\lambda_{\mathbb D}(\zeta)=\frac1{1-|\zeta|^2}.
\]

This is the normalization used by He–Tang. Multiplying all densities by the same positive normalization constant leaves the quotient in (1) unchanged.

## 2. Standard metric facts, with the needed justifications

For a hyperbolic plane domain G, a universal covering map pi : D -> G satisfies

\[
\lambda_G(\pi(\zeta))\,|\pi'(\zeta)|
 =\frac1{1-|\zeta|^2}.
\tag{2}
\]

These statements use the standard uniformization theorem for Riemann surfaces, existence of universal covers of plane domains, and the disk Schwarz lemma. The hyperbolicity assertion for the twice-punctured plane can also be justified from uniformization and Little Picard, as explained below; no assertion from the parts of He–Tang outside this audit is required.

**Covering and conformal invariance.** If p : G -> H is a holomorphic covering of hyperbolic domains, composing a universal cover of G with p in (2) gives

\[
\lambda_H(p(w))|p'(w)|=\lambda_G(w).
\tag{3}
\]

In particular this applies to biholomorphisms. Taking p(w)=tw, for t>0, gives

\[
\lambda_{tG}(tw)=t^{-1}\lambda_G(w).
\tag{4}
\]

**Domain monotonicity.** If G is contained in a hyperbolic domain H and G is hyperbolic, then lambda_G(z) >= lambda_H(z) for z in G. To check the direction, fix z and choose universal covers pi_G, pi_H taking 0 to z. The composition of pi_G with the inclusion lifts through pi_H to a holomorphic f : D -> D with f(0)=0. Differentiating pi_H composed with f = pi_G and applying |f'(0)| <= 1 yields |pi_G'(0)| <= |pi_H'(0)|. Equation (2) at 0 gives the stated inequality. Only this non-strict version is needed.

**Positive density on the twice-punctured plane.** Put H = C minus {-1,1}. This is a connected plane domain whose complement on the sphere is {-1,1,infinity}. Its universal cover is D. Indeed, uniformization makes the cover conformally a sphere, C, or D. A sphere cannot cover this noncompact domain, because its continuous image is compact. A cover by C would be a nonconstant entire map omitting -1 and 1, contrary to Little Picard. Thus (2) applies to H. Taking a cover pi with pi(0)=0 gives

\[
 m:=\lambda_H(0)=1/|\pi'(0)|\in(0,\infty),
\tag{5}
\]

because a holomorphic covering is locally biholomorphic, and its derivative at an interior point is finite and nonzero. The value m is fixed, independent of the parameter used below. No numerical formula for m is needed. The same standard hyperbolicity criterion applies to the punctured disks used below, whose sphere complements contain at least three points.

## 3. Compute the one-puncture densities

Let L = {w : Re(w) < 0}. The Cayley map c(w)=(w+1)/(w-1) maps L biholomorphically to D. Since

\[
 |c'(w)|=\frac2{|w-1|^2},\qquad
 1-|c(w)|^2=\frac{-4\operatorname{Re}w}{|w-1|^2},
\]

conformal invariance gives lambda_L(w)=1/(-2 Re(w)). The map p(w)=exp(w) is a surjective, unbranched universal covering L -> D minus {0}, and |p'(w)|=|exp(w)|. Equation (3), with z=exp(w), therefore yields

\[
 \lambda_{\mathbb D\setminus\{0\}}(z)
 =\frac1{2|z|\log(1/|z|)},\qquad 0<|z|<1.
\tag{6}
\]

Now fix a real number a with 0<a<1/2 and set

\[
 G_a=\mathbb D\setminus\{a\},\qquad
 K_a=\mathbb D\setminus\{-a\},\qquad
 U_a=G_a\cap K_a=\mathbb D\setminus\{-a,a\}.
\]

The disk automorphism phi_a(z)=(z-a)/(1-az) maps G_a bijectively and conformally to D minus {0}. It satisfies phi_a(0)=-a and phi_a'(0)=1-a^2. Thus (3) and (6) give

\[
 \lambda_{G_a}(0)=\frac{1-a^2}{2a\log(1/a)}.
\tag{7}
\]

Replacing a by -a gives the same value for lambda_{K_a}(0). Consequently,

\[
 \lambda_{G_a}(0)+\lambda_{K_a}(0)
 =\frac{1-a^2}{a\log(1/a)}>0.
\tag{8}
\]

Every displayed domain is nonempty and open. Removing one or two points from a disk leaves it path connected: any two remaining points can be joined by two line segments through an intermediate disk point chosen off the finitely many lines that would force a segment through an excluded point. Convexity keeps the segments inside the disk. The domains are bounded and hyperbolic, and 0 is an interior point of each because a>0. In particular U_a itself is the intersection component containing 0.

## 4. Lower-bound the intersection density and conclude

The inclusion U_a contained in C minus {-a,a} has a hyperbolic domain on each side. Monotonicity and dilation by a in (4)-(5) imply

\[
 \lambda_{U_a}(0)
 \ge\lambda_{\mathbb C\setminus\{-a,a\}}(0)
 =\frac1a\lambda_{\mathbb C\setminus\{-1,1\}}(0)
 =\frac ma.
\tag{9}
\]

Divide (9) by the positive quantity (8). The result is

\[
 \frac{\lambda_{U_a}(0)}{\lambda_{G_a}(0)+\lambda_{K_a}(0)}
 \ge\frac{m\log(1/a)}{1-a^2}
 \longrightarrow+\infty\qquad(a\downarrow0).
\tag{10}
\]

For complete quantifier control, given any finite A>0, choose
0<a<min(1/2,exp(-A/m)). Then m log(1/a)>A and 1-a^2<1, so the ratio in (10) is strictly larger than A. Thus even the non-strict inequality with upper constant A fails, and in particular the original strict inequality (1) fails. Nonpositive A are already impossible since all densities are positive.

Finally, for any fixed R>0, take

\[
 G_{R,a}=\mathbb D_R\setminus\{Ra\}=R G_a,
 \qquad K_{R,a}=\mathbb D_R\setminus\{-Ra\}=R K_a.
\]

Their intersection is R U_a. By (4), all three densities at 0 are their unit-radius counterparts multiplied by 1/R; their quotient is exactly the quotient in (10). It is therefore unbounded for every fixed R>0. No finite A(R) satisfies the printed general-domain question. Equivalently, the supremum of the quotient over its allowed configurations is +infinity. This completes the proof.

## Scope of acceptance

This exposition establishes only the general-domain nonexistence assertion matching He–Tang Theorem 1.2. It makes no acceptance claim for the paper's simply connected upper bound, endpoint attainability, sharp lower bound, equality characterizations, or capacity arguments. Those claims are unnecessary for the conclusion above.
