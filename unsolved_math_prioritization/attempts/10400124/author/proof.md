# Flat-connection exponents: an exact cancellation obstruction and a verified family

**Problem:** AMR-103-0124, Conjecture 7.9 in T. Ohtsuki (ed.), *Problems on invariants of knots and 3-manifolds*.

**Status:** Partial result and formulation audit. This note does not claim a proof or a counterexample to the conditional growth-rate conjecture for nonzero asymptotic sectors. No novelty is claimed.

## 1. What must be distinguished

For a closed oriented three-manifold and a fixed compact gauge group, write an asymptotic sector in the form

\[
 e^{2\pi i r c}r^{d_c}(b_c+O(r^{-1})),\qquad b_c\ne0.
\]

Here the sector has already combined all contributions with the same Chern–Simons value modulo integers. A nonzero leading exponent exists only for a nonzero sector. The prediction under examination is

\[
 d_c=\tfrac12\operatorname{gmax}_{[A]\in\mathcal M_c}(h_A^1-h_A^0).
\]

The generic maximum is over values attained constantly on a nonempty Zariski-open subset of the phase fiber. It is not the maximum over individual points in a singular positive-dimensional space.

The original Conjecture 7.7 uses a positive real amplitude for every Chern–Simons value, and Conjecture 7.9 refers to the resulting exponents. We show why an absent sector must be allowed or separately addressed. We also verify the formula in a simple infinite family in the original normalization.

## 2. Exact absent sector for L(25,2)

Use SU(2), level k and r=k+2, all integral r at least 2, and the canonical two-framing. The lens-space orientation and notation are those of Lisa C. Jeffrey, *Chern-Simons-Witten invariants of lens spaces and torus bundles, and the semiclassical approximation*, Communications in Mathematical Physics 147 (1992), 563–604, Theorem 3.4, printed page 577. Put e_m(x)=exp(2πix/m). Her exact formula is

\[
 Z(L(p,q),r;0)=\frac{-i}{\sqrt{2rp}}e_{4r}(12s(q,p))
 \sum_{\epsilon=\pm1}\epsilon e_{2rp}(\epsilon)
 \sum_{n\bmod p}e_p(qrn^2)e_p(n(q+\epsilon)),                 \tag{1}
\]

where s is the Dedekind sum. The formula imposes no coprimality condition on r and p. It is a finite exact identity, not a stationary-phase approximation. Source: [Jeffrey, Theorem 3.4](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/jeffrey.pdf).

For p=25 and q=2, the phase attached to n is c=2n²/25 modulo 1. Its zero-phase fiber in the summation index is exactly

\[
 N_0=\{0,5,10,15,20\}.
\]

Indeed, 25 divides 2n² if and only if 5 divides n. Let ζ=exp(2πi/5). For ε=1 and ε=−1 respectively,

\[
 \sum_{n\in N_0}e_{25}(n(2+\epsilon))
 =\sum_{a=0}^4\zeta^{(2+\epsilon)a}=0.                     \tag{2}
\]

Both exponents 3 and 1 are units modulo 5, so each sum is the complete sum of the fifth roots of unity. Thus the entire zero-phase contribution in (1) is identically zero, for every allowed r. Every coefficient of its expansion vanishes. This is stronger than cancellation of its leading coefficient alone.

The factor preceding the sum in (1) is a nonzero constant times r^(−1/2) times a convergent power series in 1/r with constant term 1. Consequently it neither creates a missing phase nor changes the presence of the cancellation. The same is true of a fixed change of two-framing: for SU(2) that multiplier is a fixed integer power of exp(2πi(3−6/r)/24), a nonzero constant times a unit power series in 1/r.

### Cohomology of the zero-phase fiber

The fundamental group of L(25,2) is cyclic of order 25. Every SU(2) representation is conjugate to one sending its generator to

\[
 \operatorname{diag}(e^{2\pi im/25},e^{-2\pi im/25}),
\]

with m identified with −m. Jeffrey's equation (5.3), printed page 588, gives its Chern–Simons invariant as q* m²/25 modulo 1, where q*=13 is the inverse of 2 modulo 25. Substituting m=2n reconciles this labeling with (1). The zero-phase moduli fiber therefore contains exactly the three classes represented by m=0,5,10.

For completeness, h¹=0 at all these classes. Let T be the adjoint action of a generator on V=su(2), and N=1+T+⋯+T²⁴. A crossed homomorphism of the cyclic group is specified by v in ker N, whereas coboundaries constitute im(T−1). Since T²⁵=1 in characteristic zero, V splits into its T-fixed subspace and its complement; N is 25 times the identity on the first and zero on the second, while T−1 is invertible on the second. Hence ker N=im(T−1). Twisted cohomology in degree one agrees with this crossed-homomorphism calculation; this degree-one fact requires a simply connected universal cover, not an aspherical manifold.

The dimension h⁰ is the dimension of the invariant part of su(2), equivalently the infinitesimal centralizer of the holonomy. It is 3 at m=0 and 1 at m=5,10. Therefore the three values of h¹−h⁰ are −3,−1,−1. This is a finite moduli space; each of its points is open in its Zariski topology. Its generic maximum is consequently −1, and half of it is −1/2.

**Conclusion.** The topological prediction is the finite number −1/2, but the combined zero-phase series is zero and has no nonzero leading exponent.

### Exact logical consequence

This disproves the requirement that every classical Chern–Simons value in this example have a nonzero asymptotic sector, as in the original Conjecture 7.7 with strictly positive amplitudes. It also defeats an unconditional reading of Conjecture 7.9 that identifies a finite leading exponent at every classical phase.

It is **not** a counterexample to the implication “if the stipulated nonzero-sector expansion exists, then its exponents have the predicted values”: that hypothesis fails here. Nor does it disprove a modern convention that permits a zero coefficient and assigns a merely formal exponent to that zero summand. Such an assigned exponent cannot be recovered from the invariant.

There is no hidden zero-phase term recoverable by regrouping the other phases. To see uniqueness here, use the 25 residue classes of r. At any largest power of r in the difference of two putative expansions, restriction to r=25j+a and passage to the limit gives the discrete Fourier transform of the coefficients at that power. Its vanishing for every a forces every coefficient to vanish. Repeat at each subsequent power. The rational exponents in finitely many integer-step series form a discrete set, so this induction applies to every fixed order. This proves that a nonzero zero-phase leading coefficient cannot be inserted into (1).

This argument does not assert that the invariant itself is identically zero. For a unit n modulo 25, the solutions of n'²=n² modulo 25 are n'=±n. The leading coefficient of that paired phase, inside the sum in (1), is

\[
 2\cos(6\pi n/25)-2\cos(2\pi n/25)
 =-4\sin(4\pi n/25)\sin(2\pi n/25)\ne0.
\]

Thus ten nonzero phases have leading exponent −1/2. The missing zero phase does not contradict a global O(r^(−1/2)) bound.

### An infinite version of the obstruction

Let ℓ≥5 be an odd prime, p=ℓ², and choose q coprime to ℓ with q not congruent to ±1 modulo ℓ. The zero-phase summation indices are n=ℓa. Both coefficients in (1) vanish because

\[
 \sum_{a=0}^{\ell-1}e_\ell((q\pm1)a)=0.
\]

The zero-phase moduli fiber consists of the trivial class and (ℓ−1)/2 noncentral classes. Its generic half-difference is again −1/2 by the same cyclic cohomology calculation. This supplies the same precise formulation obstruction, with the same limitation on its interpretation.

## 3. An exact positive family: connected sums of S¹×S²

Let M_g=#^g(S¹×S²) for g≥1 and M_0=S³. Use the WRT normalization

\[
 Z_k(S^1\times S^2)=1,\qquad
 Z_k(S^3)=\sqrt{2/r}\sin(\pi/r),\qquad r=k+2.
\]

**Theorem.** For every integer g≥0 and every flat SU(2) connection A on M_g,

\[
 h_A^1-h_A^0=3(g-1),\qquad
 Z_k(M_g)=\big(\sqrt{2/r}\sin(\pi/r)\big)^{1-g}.
\]

All these flat connections have Chern–Simons value zero. The unique sector has nonzero leading exponent d_0=3(g−1)/2, exactly the claimed generic half-difference.

**Proof.** For g≥1, the fundamental group is free of rank g. A crossed homomorphism into V=su(2) is determined freely by its values at the g free generators, so its space has dimension 3g. Coboundaries are the image of

\[
 V\longrightarrow V^g,\qquad
 v\longmapsto((\operatorname{Ad}\rho(x_i)-1)v)_{i=1}^g.
\]

Its kernel has dimension h⁰, and its rank is 3−h⁰. Degree-one twisted cohomology therefore has dimension 3g−3+h⁰. No irreducibility or smoothness assumption has been used. For g=0, simple connectivity gives h¹=0 and h⁰=3 directly, with the same answer.

For g≥1 the representation space is SU(2)^g, which is path connected. Its quotient is connected. The Chern–Simons functional is constant along a path of flat connections: its variation is proportional to the pairing of the variation of A with its curvature, which vanishes. Equivalently it is locally constant on the algebraic flat moduli space. All points thus have the value of the trivial connection, zero. The g=0 case is immediate.

The TQFT gluing rule along S², whose state space is one-dimensional, gives

\[
 Z_k(M\#N)=Z_k(M)Z_k(N)/Z_k(S^3).
\]

Using Z_k(S¹×S²)=1 proves the asserted exact value by induction. The displayed value of Z_k(S³) is the vacuum entry of the SU(2) modular S-matrix, also given by Jeffrey's Proposition 2.1. Hence

\[
 Z_k(M_g)=(\pi\sqrt2)^{1-g}r^{3(g-1)/2}
 \left(\frac{\sin(\pi/r)}{\pi/r}\right)^{1-g}.
\]

The last factor is analytic in 1/r near zero, equals 1 there, and has a convergent expansion in even powers. This proves the complete asymptotic expansion with a nonzero leading coefficient, not just an upper bound. Since h¹−h⁰ is constant at every class, the generic maximum equals the ordinary value. ∎

The normalization matters: an invariant divided by Z_k(S³), with value 1 on S³, has every nonzero leading exponent shifted upward by 3/2. Such exponents must not be substituted into the formula above unchanged.

## 4. The exact missing step in a componentwise argument

Suppose, as an additional hypothesis, that the contribution of each of finitely many components with phase c has an expansion

\[
 r^{a_C}(b_C+o(1)),\quad b_C\ne0,
 \qquad a_C=\tfrac12\operatorname{gmax}_{A\in C}(h_A^1-h_A^0).
\]

Write a=max_C a_C. Then the combined contribution is

\[
 r^a\left(\sum_{C:a_C=a}b_C+o(1)\right).
\]

Consequently a is its leading exponent if and only if that sum is nonzero. If the sum vanishes, the growth is o(r^a), possibly identically zero. This elementary fact explains why proving a local stationary-phase formula alone does not establish a phasewise maximum formula. In addition, singular strata may invalidate the assumed componentwise exponent itself. Neither hypothesis is proved in general here.

The lens-space calculation above is an actual WRT cancellation, rather than only a toy model of this logical gap. A general theorem requires an explicit convention for absent sectors and, for a nonzero leading-exponent assertion, an adequate noncancellation statement.
