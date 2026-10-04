# Function Theory 5.66: verified published negative answer

## Exact target and result

Let D = {z in C : |z| < 1}. The question asks whether every infinite Blaschke product B on D admits a number delta > 0 such that B^{-1}({w}) is infinite for every w in D with |w| < delta.

The answer is **no**. There is an infinite Blaschke product B for which the set of w having a finite fiber is dense in D. In particular, there are nonzero w_n tending to 0 with finite fibers, while B^{-1}({0}) itself is infinite.

This is a verification of an existing result, not a new solution. The essential construction is Kenneth Stephenson's published 1988 construction; the reduction below makes every quantifier needed for Problem 5.66 explicit.

## Published input and its scope

**Stephenson's construction theorem.** There exists an inner function f on D with infinitely many zeros and with a dense subset A of D such that f^{-1}({a}) is finite for each a in A.

Source: K. Stephenson, *Construction of an Inner Function in the Little Bloch Space*, Transactions of the American Mathematical Society 308 (1988), 713–720, DOI [10.1090/S0002-9947-1988-0951624-3](https://doi.org/10.1090/S0002-9947-1988-0951624-3). The construction and its boundary property are proved in Sections 1–3, pp. 714–717; Section 4, pp. 717–718, explicitly performs the Blaschke reduction. The complete article text was inspected through this [publicly readable copy](https://www.academia.edu/60898917/Construction_of_an_Inner_Function_in_the_Little_Bloch_Space).

The input is not the false assertion that every little-Bloch inner function has dense finite range. Only the existence of the constructed example is used. The cited construction theorem is an external mathematical dependency, not a lemma proved by the finite controls in this package.

## 1. Disk automorphisms and fiber transport

For alpha in D put

    phi_alpha(u) = (u - alpha)/(1 - conjugate(alpha) u).

The denominator is nonzero on D, since |conjugate(alpha) u| < 1. Direct algebra gives

    1 - |phi_alpha(u)|^2
      = (1 - |alpha|^2)(1 - |u|^2) / |1 - conjugate(alpha)u|^2 > 0,

and its inverse is

    psi_alpha(v) = (v + alpha)/(1 + conjugate(alpha) v).

Thus phi_alpha is a biholomorphic self-map of D. If B = phi_alpha composed with f, then for every v in D,

    B^{-1}({v}) = f^{-1}({psi_alpha(v)}).                 (1)

In particular, B^{-1}({phi_alpha(a)}) = f^{-1}({a}). Homeomorphisms preserve density, so phi_alpha(A) is dense in D and every one of its fibers under B is finite.

## 2. The almost-everywhere shift lemma

We give an elementary proof of the portion of Frostman's theorem needed here. We use the standard canonical factorization of a nonconstant inner function into a unimodular constant, a Blaschke product, and a singular inner factor. The stronger statement that the exceptional set has logarithmic capacity zero is unnecessary.

**Lemma.** If f is a nonconstant inner function, phi_alpha composed with f is a Blaschke product for planar-almost-every alpha in D.

**Proof.** Write dA for unnormalized planar area. For u in D the Green-kernel identity is

    integral_D -log |(u-alpha)/(1-conjugate(alpha)u)| dA(alpha)
      = (pi/2)(1-|u|^2).                                (2)

Here is a derivation. Rotate u so |u| = s. The angular mean of log|rho e^{it}-u| is log max(rho,s), and the angular mean of log|1-rho e^{-it}u| is zero. Consequently the first mean integrated against 2 pi rho d rho is

    2 pi [ integral_0^s rho log s d rho
             + integral_s^1 rho log rho d rho ]
      = (pi/2)(s^2-1).

The same formula follows at s=0 by taking the limit, so (2) holds throughout D.

For 0<r<1 set

    L_alpha(r) = (1/(2 pi)) integral_0^{2 pi}
                  log|phi_alpha(f(r e^{it}))| dt <= 0.

The logarithm has only locally integrable isolated zero singularities. Its circular mean is nondecreasing in r by subharmonicity. Hence its limit L_alpha as r increases to 1 exists in [-infinity,0]. Tonelli's theorem and (2) imply

    integral_D -L_alpha(r) dA(alpha)
      = (pi/2) [1 - (1/(2 pi)) integral_0^{2 pi}|f(r e^{it})|^2 dt].

The right side tends to zero: f has boundary modulus one almost everywhere and |f|<=1, so dominated convergence applies. Fatou's lemma for the nonnegative functions -L_alpha(r) now gives integral_D -L_alpha dA = 0. Therefore L_alpha=0 for almost every alpha.

For completeness, canonical factorization says that for the inner function g=phi_alpha composed with f,

    g = eta P S_mu,

where P is a Blaschke product and mu is a finite positive singular measure on the unit circle. The circular mean of log|S_mu| is -mu(T) for every r. The circular mean of log|P| tends to zero: for its zeros a_j, Jensen's formula expresses it as a finite zero-at-origin term plus sum_j log max(r,|a_j|), which tends to zero by dominated convergence and the Blaschke condition. Thus L_alpha=-mu(T). When L_alpha=0, positivity forces mu=0, and g is a Blaschke product. This proves the lemma. QED.

## 3. Why the chosen Blaschke product is infinite

Apply the lemma to the f in Stephenson's construction theorem and choose any alpha in its full-area set of good shifts. Set B=phi_alpha composed with f.

This B cannot be a finite Blaschke product. A nonconstant finite Blaschke product is a rational function with finitely many solutions to B(z)=c for each c in D. But (1) with v=phi_alpha(0)=-alpha gives

    B^{-1}({-alpha}) = f^{-1}({0}),

which is infinite. Nor can B be constant, since f is not constant. Therefore B is an infinite Blaschke product.

The phrase "almost every" is used only to ensure a good alpha exists. No assertion is made that every shift works, and no explicit numerical value of alpha is required for this existence problem.

## 4. Negating the original quantifiers

For any delta>0 choose a point

    v in phi_alpha(A) intersect {0<|v|<min(delta,1)}.

The punctured disk is a nonempty open subset of D, so the density proved in Section 1 supplies such a v. Its fiber under B is finite by (1). Thus the same fixed infinite Blaschke product B defeats every proposed delta.

Equivalently choose one such v_n with 0<|v_n|<1/n. Then v_n tends to zero and all its fibers are finite. The zero fiber of B is infinite because B is an infinite Blaschke product. There is no contradiction: finiteness of each nearby fiber does not give a uniform bound on their cardinalities.

This proves the exact negative answer, conditional only on the stated published construction theorem and standard one-variable function-theory facts identified above. No part of Problem 5.66 remains unresolved in this verification.

## 5. A useful positive statement and the quantifier trap

For every infinite Blaschke product B and every positive integer N, there does exist delta_N>0 such that every |w|<delta_N has at least N distinct preimages.

Indeed, choose N distinct zeros of B. Around them choose pairwise disjoint closed disks lying in D with no zeros on their boundary circles. The minimum of |B| over the union of those circles is a positive number eta. If |w|<eta, Rouche's theorem gives at least one zero of B-w in each disk. The disks are disjoint, so there are at least N distinct preimages.

This establishes

    for every N there exists delta_N > 0 such that for all |w|<delta_N,
    #B^{-1}({w}) >= N.

It does not establish a single positive delta that works for all N. The counterexample shows why this interchange of quantifiers is invalid.

## Verification limits

The exact rational controls validate the automorphism identities, conjugation convention, and finite combinatorial/numerical analogues described in their output. They neither construct the infinite Riemann surface nor formally verify Stephenson's theorem, canonical factorization, or Rouche's theorem. The existence result is supported by the complete published mathematical argument; this package does not claim a machine-checked proof or a novel theorem.
