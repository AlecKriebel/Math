# Construction attempt: translation-equivariant exponential families

Date: 2026-10-20 UTC. Queue 1820 / AMR-036-0006.

## Outcome

No counterexample to the unrestricted problem is constructed. There is, however, a rigorous obstruction to a large natural family of construction attempts:

**Proposition.** Let P be a nonconstant complex polynomial and let

f(z) = z + P(exp z).

Then f has no completely invariant attracting or parabolic Fatou component. In particular, f cannot have two completely invariant Fatou components.

This includes every affine-exponential deformation f(z)=z+a+b exp(z), b nonzero, including parameters with genuine attracting fixed points. The argument uses the valid singular-value condition in Rempe–Sixsmith, not Baker's invalid planar argument. This is a special-family result, not a resolution of the queue problem. No novelty claim is made.

## Primary input and inspection

L. Rempe-Gillen and D. Sixsmith, *On Connected Preimages of Simply-Connected Domains Under Entire Functions*, GAFA 29 (2019), 1579–1615, https://doi.org/10.1007/s00039-019-00488-2 ; author preprint https://arxiv.org/pdf/1801.06359 . Inspected the author preprint, Theorems 1.2–1.3, Corollary 1.4 and Proposition 8.6.

Theorem 1.3(b) says: if G1,G2 are disjoint simply connected domains, f^{-1}(G1) is connected, and G1 intersect S(f) is compactly contained in G1, then f^{-1}(G2) is disconnected. Corollary 1.4 and the following paragraph show that if there are multiple completely invariant Fatou components, all must be attracting or parabolic. In particular no use is made of the false assertion that arbitrary disjoint simply connected domains cannot both have connected preimages.

## Proof of the proposition

Write T=2πi and d=degree P≥1.

### 1. Translation symmetry really is dynamical

f(z+kT)=f(z)+kT for every integer k, and induction gives

f^n(z+kT)=f^n(z)+kT.

Consequently translation by kT preserves the Fatou set and sends each Fatou component to a Fatou component. If U is completely invariant, then so is U+kT: explicitly,

f^{-1}(U+kT)=f^{-1}(U)+kT=U+kT.

If U is an invariant attracting or parabolic basin, iterates on U converge to a finite fixed point p (for parabolic U, p may be on its boundary). Iterates on U+kT converge to p+kT. Therefore U and U+kT are distinct, hence disjoint, for every nonzero integer k. This argument does not infer complete invariance from normality or from a trapping region.

### 2. There are no finite asymptotic values

Suppose, to the contrary, a continuous curve z(t) tends to infinity while f(z(t)) tends to A in C. Write z=x+iy and let c_d be the leading coefficient of P. The equation

P(exp z) = -z + O(1)

first implies x→+∞: if x remained bounded above along any subsequence, the polynomial P(exp z) would remain bounded there, contradicting |z|→∞. Therefore along the entire tail of the curve,

P(exp z)=c_d exp(dz)(1+o(1)),

and hence

x=(log|z|−log|c_d|)/d+o(1).

Thus x/|z|→0 and |y|/|z|→1. In particular |y|→∞. Continuity implies that y has a constant sign on a sufficiently long tail, so arg z tends to either π/2 or −π/2. From c_d exp(dz)/(-z)→1 it follows that exp(idy) converges to a point of the unit circle.

This is impossible for a continuous real-valued function y(t) with |y(t)|→∞: by the intermediate value theorem it crosses arbitrarily large consecutive values whose phases differ by π. Equivalently, eventual confinement of exp(idy) to a sufficiently small arc would confine y to one bounded component of that arc's inverse image. This contradiction proves the assertion.

### 3. Singular values form finitely many translation orbits

Critical points satisfy

1 + w P'(w)=0, where w=exp z.

This degree-d polynomial has at most d distinct roots and none at zero. Choose one logarithm z_j of each root w_j. The critical points are exactly z_j+kT, and their critical values are

v_j+kT, where v_j=z_j+P(w_j).

There are no finite asymptotic values by Step 2. A finite union of vertical arithmetic progressions is closed and has no finite accumulation point. Therefore S(f) is exactly this finite union of critical-value orbits, with coincidences allowed.

### 4. Each attracting/parabolic component contains only finitely many singular values

If two distinct members v_j+kT and v_j+lT of one orbit lay in U, then U and U+(k−l)T would intersect. Step 1 rules this out. Hence U contains at most one point from each critical-value orbit, and U intersect S(f) has at most d points. Every finite subset of the open domain U is compactly contained in U.

### 5. Complete invariance leads to the contradiction

Suppose U were completely invariant and attracting/parabolic. Then V=U+T is a disjoint completely invariant Fatou component. Both are simply connected, as periodic Fatou components of a transcendental entire function. Complete invariance supplies connectedness of f^{-1}(U)=U. Step 4 supplies the compact-containment hypothesis of Theorem 1.3(b). That theorem says f^{-1}(V) is disconnected, contradicting f^{-1}(V)=V.

This proves that there is no completely invariant attracting/parabolic U. If f had two completely invariant Fatou components, the cited Corollary 1.4 and discussion would force each to be attracting or parabolic, which has just been excluded. This completes the proposition.

## A fully explicit attracting deformation and its failure

Take f_a(z)=z+a−a exp(z), with 0<a<2 real. Its fixed points are p_k=2πik, all attracting because f_a'(p_k)=1−a has modulus less than one. Thus this deformation genuinely creates the desired type of local dynamics, rather than merely replacing arbitrary topological domains with names for basins.

The horizontal lines Im z=(2k+1)π are invariant. On such a line the real coordinate evolves as

x ↦ x+a+a exp(x) > x+a,

so every point there escapes to infinity. No such point can lie in an attracting basin of a finite fixed point. The immediate basin U_k containing p_k is connected and therefore lies in the open strip between its two neighboring lines.

Nevertheless p_0=0 has preimages in arbitrarily distant strips. For positive integers n sufficiently large, set y in (2πn,2πn+π/2) and

x=log(y/(a sin y)).

Then the imaginary part of f_a(x+iy)=0 holds automatically. The real part is equivalent to

H(y)=y cot y−log(y/(a sin y))−a=0.

As y decreases to 2πn, H(y)→+∞. As y increases to 2πn+π/2, H(y) tends to −log((2πn+π/2)/a)−a<0 for large n. Continuity gives a root in every such interval. These preimages of 0 lie outside U_0's strip. Therefore f_a^{-1}(U_0)≠U_0. Translating proves the same for each U_k.

This provides a direct witness of failure of complete invariance, independently of the singular-value argument for these real parameters. The witness does not require a numerical picture or an unproved description of the entire Fatou set.

For a=0 in the unnormalized affine-exponential family f(z)=z+b exp(z), b≠0, there are no finite fixed points at all. Thus the literal exp(z)+z example used for the topological counterexample cannot already provide an invariant attracting or parabolic basin. A genuine deformation is essential, but the polynomial-exponential deformations above remain obstructed.

## What a more general equivariant or surgery construction would need

The central obstruction extends beyond polynomials: if a transcendental entire f commutes with translation by T≠0 and S(f) is contained in finitely many T-orbits, the same argument forbids completely invariant attracting/parabolic components. Each such component is disjoint from its translates and contains at most one singular value per orbit.

Thus any successful translation-equivariant construction with two completely invariant Fatou components must have infinitely many singular-value translation orbits. More strongly, in each candidate component U, U intersect S(f) must fail to be compactly contained in U, by Theorem 1.3(b). It must also lack an access to infinity, by Theorem 1.3(f). A construction retaining an invariant ray or half-plane in a candidate component would fail this latter test.

For example, replacing P by a transcendental function h in z+h(exp z) escapes the finite-orbit proof only if it actually creates the required noncompact distribution of singular values. Such a replacement does not by itself establish a counterexample. No h satisfying all the dynamical requirements was found here.

An approximation or surgery plan must simultaneously prove:

1. Two distinct invariant Fatou components with attracting/parabolic limits, not just forward-invariant chosen subdomains.
2. Every preimage of every point of each entire component lies in that same component. It is not enough to keep finitely many enumerated preimages connected at finite construction stages.
3. Fatou-component maximality and connectedness survive the limit or straightening.
4. Neither component acquires an access to infinity, and both contain a singular-value set not compactly contained in the component.
5. The final straightened map is entire, not meromorphic or quasiregular, and complete invariance is transported by an actual global conjugacy rather than by a one-sided semiconjugacy.

The 2019 topological recursive domains do not supply these dynamical properties. This investigation does not claim that a suitable approximation/surgery scheme is impossible; it identifies missing requirements and excludes the natural finite-polynomial exponential ansatz rigorously.

## Acceptance boundary

Verified result: exclusion of two completely invariant Fatou components for z+P(exp z), with the stronger exclusion of any completely invariant attracting/parabolic component in that family. This relies on the published valid Theorem 1.3(b) and its dynamical corollary.

Not established: the unrestricted at-most-one conjecture, an entire counterexample, an infinite-singular-orbit construction, or a general obstruction for every translation-equivariant entire map.

## Verified extension: finite Laurent/Fourier families

The proposition extends to every nonconstant Laurent polynomial

P(w)=sum_{j=m}^{n} c_j w^j,

and to every f(z)=z+P(exp(λz)) with λ≠0. Negative powers introduce no poles in the z-plane because exp(λz) never vanishes. This is still only a finite Laurent/Fourier family, not an assertion about general holomorphic functions on C*.

Here is the complete additional verification for λ=1.

Suppose z(t)→∞ along a continuous curve and f(z(t))→A in C. As before, P(exp z)=-z+O(1). If |Re z| failed to tend to infinity, there would be a subsequence on which Re z lies in one fixed bounded interval. The values exp z would then lie in a fixed compact annulus in C*, on which P is bounded, contradicting |z|→∞. Therefore |Re z|→∞. By continuity, Re z has one eventual sign and tends either to +∞ or to −∞.

At the +∞ end, if P has no positive exponent, P(exp z) is bounded, already a contradiction. Otherwise its highest exponent k>0 dominates. At the −∞ end, if P has no negative exponent, boundedness is again a contradiction. Otherwise its lowest exponent k<0 dominates. In either permissible case,

P(exp z)=c_k exp(kz)(1+o(1)), with k a nonzero integer,

so

Re z=(log|z|−log|c_k|)/k+o(1).

Consequently |Im z|/|z|→1, Im z has one eventual sign, and c_k exp(kz)/(-z)→1 forces exp(ik Im z) to converge. The same continuity/intermediate-value argument used above rules this out. Thus there are no finite asymptotic values, including in the two-ended Laurent case.

The critical-point equation 1+wP'(w)=0 is a nonzero Laurent-polynomial equation: its constant coefficient is 1, because wP'(w) has zero constant coefficient. Multiplying by a sufficiently large power of w gives a nonzero ordinary polynomial. Hence there are only finitely many roots in C*. Critical values therefore form finitely many 2πi-translation orbits, a closed discrete set. Steps 1, 4 and 5 of the proof apply without change: there is no completely invariant attracting/parabolic component, and at most one completely invariant Fatou component in total.

Finally, for λ≠0 use the linear conjugacy L(z)=λz. Then

L composed with f composed with L^{-1}(w)=w+λP(exp w).

The Laurent-polynomial result applies to the nonconstant Laurent polynomial λP. A linear conjugacy preserves Fatou components, their types, and complete invariance. This establishes the claimed extension without imposing any reality or sign condition on λ or the coefficients.

As above, this is a standard-method special-family deduction using the published singular-value criterion; no novelty or unrestricted-conjecture claim is made.
