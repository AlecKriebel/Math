# Independent mathematical review: fixed-edge polyhedron CLT

Date: 2026-10-21 (UTC)

## Decision and scope

**ACCEPT the exact target CLT as mathematically established, conditional on the stated classical published enumeration and asymmetry theorems.** No substantive gap was found in the chain from those inputs to the fixed-edge, uniform-unlabelled-combinatorial-type conclusion. This is a scoped mathematical assessment, not a claim that the 2026 manuscript has been peer reviewed or accepted by a journal, and not a certification of every stronger theorem in that manuscript.

Target: if V is the vertex count of a uniformly chosen combinatorial type of convex three-dimensional polytope with e edges, then sqrt(e)(V/(e+2)-1/2) converges in distribution to the centered normal law with variance 1/32, as e tends to infinity through admissible edge counts. The separately claimed variance asymptotic also passes this review.

Reviewed: manuscript Sections 2–4, the central local-law implication used in Section 5, and Section 6.3. Classical theorem statements and conventions were checked against the supplied published-source PDFs/texts. Their underlying classical proofs were not reconstructed in full.

## Classical-source checks

1. Bender and Wormald, *The number of rooted convex polyhedra*, Canadian Mathematical Bulletin 31 (1988), printed page 100, Theorem 2. The page was rendered and inspected visually, rather than trusting the damaged OCR formula. The coefficient is 1/(3^5 i j), not 1/(3 i j) or 1/(3^2 i j). The binomial factors are C(2i,j+3) and C(2j,i+3). The indices count i+1 vertices and j+1 faces. The theorem states uniformity as max(i,j) grows, without a compact-ratio qualification. The same page prints the corresponding unlabelled asymptotic with denominator 4·3^5·i·j·(i+j). DOI: https://doi.org/10.4153/CMB-1988-015-2

2. Bender and Wormald, *Almost all convex polyhedra are asymmetric*, Canadian Journal of Mathematics 37 (1985), printed page 863, Theorem 4.1, and page 869, Corollary 4.2. The theorem page was rendered and inspected visually. The symmetric unrooted count is exponentially negligible relative to the rooted count, uniformly for 1/2 < f/v < 2; the exponential parameter is the vertex count v. The corollary uses the divisor 4(v+f−2), hence 4e. The surrounding source convention explicitly includes orientation-reversing automorphisms, so replacing 4e by 2e would not match these counts. DOI: https://doi.org/10.4153/CJM-1985-046-0

The source's statement about zero counts also supports the manuscript's interior-support inference: outside a finite exceptional range, a positive displayed binomial expression cannot correspond to a zero rooted count. Thus the support argument is not silently assuming an unproved positivity theorem.

## Model and support audit

Euler gives v+f=e+2. Minimum degrees in the primal and dual give e/3+2 <= v,f <= 2e/3. Consequently i=v−1 lies between e/3+1 and 2e/3−1, and every feasible state lies strictly within the classical asymmetry ratio range. In fact 2f−v and 2v−f are both at least 4. Thus approaching the feasible endpoints does not leave the range of that uniform theorem.

The center is exactly (e+2)/2, not e/2 for V. With X=V−(e+2)/2=i−e/2, the lattice is Z for even e and Z+1/2 for odd e. Polar duality is a bijection of combinatorial types, establishes exact centering, and makes the odd centered moments vanish. The permitted edge counts {6} union {e>=8} are consistent with the construction and degree constraints in the manuscript.

For any fixed compact density interval strictly inside (1/3,2/3), both shifted binomial factors are positive for all sufficiently large e. Classical uniformity therefore supplies every central lattice point needed for the Gaussian sums, including the half-integer parity case. This addresses the possible failure mode of approximating a lattice with holes by a full Gaussian mesh.

## Rooted-to-unrooted audit

For the source's root convention, a polyhedral map has 4e flags. A flag stabilizer is trivial, so a type with automorphism-group size a contributes 4e/a rooted objects. Subtracting q/(4e) from the unrooted count leaves a nonnegative deficit bounded by the number of symmetric types.

The classical bound gives relative deficit o(e c^v). Since v>=e/3+2, choosing rho strictly between c^(1/3) and 1 absorbs the polynomial e. This proves uniform exponential relative accuracy over the entire feasible slice. Normalizing counts changes the ratio by another factor 1+O(rho^e), not an uncontrolled global error. In particular it is legitimate to use the uniform-unlabelled model rather than silently substituting a rooted or labelled model.

## Independent diagonal calculation

Write alpha=i/e. Removing the +3 shifts from each binomial yields the product of three consecutive numerator/denominator ratios. On compact interior density intervals these contribute

((3alpha−1)/(1−alpha))^3 ((2−3alpha)/alpha)^3 (1+O(1/e)).

Uniform Stirling for the unshifted product contributes the reciprocal prefactor pi e sqrt((3alpha−1)(2−3alpha)) and exponential exp(e Phi(alpha)). Combining with 1/(4·3^5·i·j·e) yields e^(−4)h(alpha)exp(e Phi(alpha)), with exactly the manuscript's h=G/(4·3^5·pi). In particular G(1/2)=8 and h(1/2)=2/(243 pi).

I independently checked the differentiation and expansion algebra, including a symbolic check:

- I''(alpha)=2/[alpha(1−alpha)(3alpha−1)(2−3alpha)].
- I''(1/2)=32.
- I(1/2+d)=16d^2+(320/3)d^4+(23296/15)d^6+O(d^8).

Thus the central mass profile has exponent −16x^2/e and variance scale e/32.

The Gaussian lattice sum is asymptotic to sqrt(pi e)/4 for either parity. Multiplication by the central count prefactor gives total unlabelled count 4^e/(486 sqrt(pi) e^(7/2)). After normalization the central atom is 4/sqrt(pi e) times exp(−16x^2/e). All constants, powers of e, shifts, and the 4e unrooting factor are mutually consistent.

## Normalization, tails, and moments

The manuscript does not assume that a central local approximation alone normalizes the entire distribution. It supplies the needed controls:

- On a fixed central density interval, strict convexity gives a Gaussian upper bound with a bounded smooth prefactor.
- Outside that interval, entropy bounds on the binomial coefficients and the global source uniformity give a polynomial times 4^e exp(−kappa e), uniformly to the feasible endpoints. This avoids applying the vanishing interior prefactor at a boundary.
- With w=e^(1/2+eta), 0<eta<1/4, the Taylor-exponent error is O(e^(−1+4eta))=o(1), uniformly on the central window. The remaining inner Gaussian tails are negligible; the outer region is exponentially negligible even after its O(e) lattice-point count.

For Z=X/sqrt(e/32), the resulting local law has mesh Delta=sqrt(32/e) and atoms phi(z)Delta(1+o(1)) on compact intervals. The Gaussian envelope implies tightness, so compact-interval Riemann sums imply the full CLT rather than merely convergence on a restricted window.

For each fixed even moment, multiply that envelope by the corresponding power of |z|. Its summable Gaussian tails vanish uniformly as the truncation grows. The outer density region remains negligible since the maximal standardized coordinate is O(sqrt(e)), only polynomially large. This proves uniform integrability and justifies Var(V)~e/32; variance convergence has not been inferred from weak convergence alone.

Finally sqrt(e)(V/(e+2)−1/2)=[e/(e+2)]Z/sqrt(32), which has the stated limiting variance 1/32.

## Additional diagnostic and caveats

A numerical diagnostic normalized the explicit binomial asymptotic weights, not exact polyhedron counts. At e=100,300,1000,3000 its variance/e was approximately 0.029376, 0.030633, 0.031066, 0.031189, consistent with approach to 0.03125. The corresponding total-weight/asymptotic-total ratios were approximately 0.67758, 0.87794, 0.96165, 0.98705. This is only an arithmetic sanity check and is not treated as evidence replacing the analytic argument or classical enumeration theorem.

Minor editorial point: describing the CLT and the variance asymptotic as “equivalent” is not true as a general logical implication. The manuscript separately proves moment convergence, so this wording does not invalidate the result and requires no mathematical repair for the exact target.

No claim is made here about priority, journal acceptance, or independent verification of the entirety of the 1985/1988 proofs. No external publication or queue changes were performed in this review.
