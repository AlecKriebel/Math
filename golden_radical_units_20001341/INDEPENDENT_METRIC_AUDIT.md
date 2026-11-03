# Independent mathematical audit

Audit date: 2026-10-21. Scope: independently check the proposed elementary radical-unit results and their limits. This is not an originality or global shortest-unit certificate.

Let n≥1, phi=(1+sqrt(5))/2, a=log(phi), alpha=phi^(1/n), K=Q(sqrt(5)), L=Q(alpha).

## Algebraic checkpoints: pass

The binomial irreducibility criterion over a characteristic-zero field says X^n−b is irreducible if b is not a pth power for each prime p dividing n, and, when 4 divides n, b is not −4 times a fourth power. A root in K of b=phi would be an integral unit; O_K^×={±phi^j} excludes such prime powers. The positive real embedding excludes phi=−4c^4. Consequently [L:K]=n and [L:Q]=2n. Since alpha satisfies X^(2n)−X^n−1, that polynomial is its minimal polynomial.

A primary author-hosted reference recalling the criterion, including the exceptional condition, is Sawin, Shusterman and Stoll, *Irreducibility of polynomials with a large gap*, printed page 2: https://www.mathe2.uni-bayreuth.de/stoll/papers/SaShSt.pdf . A direct finite-exponent statement also appears in Dubickas, *Irreducibility of a Polynomial Shifted by a Power of Another Polynomial*, DOI https://doi.org/10.1155/2020/8869499 .

The signature is (2,n−1) for both parities. Roots of unity are ±1 because L has a real embedding. The unit inverse is alpha^(2n−1)−alpha^(n−1). These conclusions do not require identifying the maximal order with Z[alpha].

## Metrics: pass with conventions explicit

There are n conjugates of modulus exp(a/n) and n of modulus exp(−a/n). Therefore:

- Canonical Minkowski squared length, counting all embeddings: 2n cosh(2a/n).
- House: exp(a/n).
- Absolute logarithmic Weil height: a/(2n).
- Intrinsic Mahler measure: phi.
- Logarithmic squared length with sqrt(2) complex-place weighting: 2a²/n.
- Logarithmic squared length with 2 complex-place weighting: (4n−2)a²/n².
- Unweighted place-log squared length: (n+1)a²/n².

At n=156, independently evaluated using 60-digit mpmath arithmetic:

- Minkowski length: 17.6636898064457244806169560506698549.
- Universal unit lower bound sqrt(312): 17.6635217326556937095280854539185079.
- Ratio to that lower bound: 1.00000951530462467415065334233941128.
- House: 1.00308945374188222413842097802782451.
- Weil height: 0.00154234559313975463941589395328323213.
- Mahler measure: 1.61803398874989484820458683436563812.
- sqrt(2)-weighted logarithmic length: 0.0544865098073795849796211351550934924.
- 2-weighted logarithmic length: 0.0769319755534064159841929681327682009.

AM–GM gives the stated universal lower bound. Equality implies every conjugate has modulus one, hence torsion by Kronecker. Thus the ratio bounds approximation to the non-torsion Minkowski optimum, but is not an exact optimum certificate and gives no ratio for the logarithmic objective.

## Relative norm reduction: pass

Write N_{L/K}(u)=±phi^{r(u)}. Then N_{L/K}(alpha)=(-1)^(n−1)phi, so r(alpha)=1, including n=156 where the norm is −phi. The homomorphism r:O_L^×→Z is onto, and

O_L^× = <alpha> × ker(r).

The kernel has rank n−1; at n=156 its rank is 155. It is the kernel of the norm exponent, meaning norm in {±1}, not necessarily the literal norm-one subgroup. Modulo torsion, alpha is primitive and can be extended to an abstract Z-basis, but this supplies no computed full basis.

The two blocks of n embeddings over K have log sums ra and −ra. Block AM–GM, Cauchy–Schwarz and positive-part bounds give respectively

- Minkowski squared length ≥2n cosh(2ra/n).
- sqrt(2)-weighted logarithmic squared length ≥2r²a²/n.
- House ≥exp(|r|a/n).
- Weil height ≥|r|a/(2n).

All are attained by alpha^r. Hence alpha is an exact minimizer outside ker(r), not globally among non-torsion units. For the first two metrics, equality at the overall outside-kernel minimum implies r=±1 and u=±alpha^r by Kronecker. No corresponding uniqueness claim for house or height is certified here. The result is not automatically transferable to the 2-weighted logarithmic Euclidean norm.

The intrinsic Mahler lower bound outside ker(r) also passes. For F=Q(u), if K is not contained in F, quadratic Galois K/Q gives linear disjointness and N_{KF/K}(u)=N_{F/Q}(u)=±1, implying r=0. Thus r≠0 forces K⊂F. Put e=[L:F]. Then N_{F/K}(u)=±phi^s gives r=e s and deg(u)=2n/e. The height bound yields log M(u)≥|s|a≥a. Thus the outside-kernel Mahler minimum is phi, without uniqueness.

A concrete non-torsion kernel element for n>1 is alpha(1−alpha): 1−alpha is a unit, N_{L/K}(1−alpha)=1−phi=−phi^−1, and its product with alpha has exponent zero. Its distinguished real value lies strictly between −1 and 0. This is not a shortest-kernel certificate.

## Powers: degree-drop correction essential

For k≠0 and g=gcd(n,|k|), Q(alpha^k)=Q(phi^(1/(n/g))) and deg(alpha^k)=2n/g. Indeed Q(phi^m)=K for every nonzero integer m, and Bezout recovers the reduced radical. Therefore intrinsic M(alpha^k)=phi^(|k|/g). Its minimum phi over non-torsion powers occurs for every |k| dividing n, not only |k|=1. The fixed-field conjugate product is instead phi^|k|. All the other displayed metrics on non-torsion powers are strictly minimized at |k|=1, with signs and inversion giving the expected ties.

## Acceptance boundary

These proofs establish explicit units, exact metric calculations, power-subgroup minima, and exact optimization outside the norm-exponent kernel. They do not bound the shortest non-torsion vector in that kernel, compute a full unit basis, certify saturation of a proposed full-rank unit system or determine the regulator, resolve the original unspecified meaning of “short”, or certify novelty. The primary source/status gate remains applicable.

## Draft and executable review

The full RESEARCH.md and verify_exact.py were independently inspected after drafting. No substantive mathematical correction was required. In particular, the relative-norm intrinsic-Mahler argument, the orthogonal sqrt(2)-log splitting, and the explicit divisor-unit inverse signs all pass. The executable was independently rerun successfully: seven n-cases (including n=156), all 24 divisor-unit inverse identities at n=156, and 21 small-degree power-field degree checks. Numerical output is correctly labeled high-precision approximation, not an interval certificate. This acceptance is scoped to the stated elementary results, not a global shortest-unit, maximal-order, full unit-basis, regulator, or novelty claim.
