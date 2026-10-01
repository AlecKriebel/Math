# Independent full review: 30000156 / birational cycle distributions

**Verdict: PASS_COMPLETE_LITERAL_SOURCE_TARGET.** The unchanged candidate proves the stated counterexample to the broad, unaveraged birational-map limit assertion in Vivaldi's OWR Conjecture 1. A claimed-solved, 1/5 disposition is supported, with the explicit affine normalization, admissible prime class and rational-inverse scope preserved. No mandatory mathematical correction is required. Historical novelty is not certified.

Binding files: PROOF.md SHA256 ba5fc8850a665da5130e3791fb49015c998ed0eee317576712ad3b66bc228c05; FROZEN_MANIFEST.json SHA256 4423e8d47a82c17f63e30d31a71f5fc232b37781f5486f5e414259aecf032345. I had no role in constructing the candidate. I independently read the complete proof, original two-page contribution, exact published mean input and the relevant later-source distinctions.

## 1. Source and admissible-map audit

The original is Vivaldi, joint work with Roberts, *Maps over finite fields: integrability and reversibility*, OWR54/2004, printed pp.2944–2945. Both the full report contribution and the author's two-page copy give the same definition: uniformly weight affine points, divide their count by p², and use the threshold px. The first conjecture asks for an unaveraged limit for any birational map. The integral and inverse may be rational; neither a polynomial inverse nor constant Jacobian is imposed in that universal assertion.

The candidate L(u,v)=(u,(u²+1)v) is a polynomial forward map with rational inverse (u,v/(u²+1)). Their two compositions agree on the dense open set u²+1≠0, so this is birational over Q. Its first integral u is nonconstant and rational. Its iterates multiply v by (u²+1)^k, so it has infinite order in characteristic zero. Its generic level curve is genus zero, which the broad source allows. It is not a polynomial automorphism over C and the packet states that limitation accurately.

For every p≡3 mod4, u²+1 is nonzero for every u∈F_p. Both maps are therefore defined at every affine point and are inverse permutations. This is one fixed prime class of density 1/2. It meets the source's permitted positive-density reduction setup and avoids ambiguity about transient points or exceptional rational lines. The two incompatible subsequences remain inside this class. The universal unaveraged assertion cannot require convergence after every value is defined while fail on this valid fixed class. A different assertion permitting arbitrary after-the-fact prime subsequences chosen specifically to force convergence would be different from the displayed source conjecture.

I separately read the 2006 elliptic-foliation discussion and the 2009 random-involution Theorems A/B. Those involve different hypotheses or averaging. The candidate neither refutes their proved ensemble theorem nor claims to settle every narrower polynomial-automorphism or elliptic-foliation conjecture. The source's second conjecture explicitly introduces a different p² period scale and a prime average; it is not substituted for the first.

## 2. Exact dynamics and normalization

On a vertical fiber, L multiplies the second coordinate by a=u²+1. The zero point is fixed; each nonzero point has least period ord_p(a), independent of that point's nonzero v-coordinate. A primitive multiplier therefore contributes p−1 full-period points, not one point or one cycle.

With N=p−1 and any fixed x∈[1/2,1), every proper divisor of N is at most N/2≤px, whereas N>px for all sufficiently large p. The zero section is also included. Consequently the exact eventual formula

D_p(x)=1−(p−1)P_p/p²

is correct, where P_p counts u with primitive multiplier. At x=1/2 the proper-divisor inequality remains valid; no excluded endpoint issue occurs. The threshold needed to exclude N depends on fixed x, which is sufficient for both the pointwise and weak-limit conclusions.

## 3. Character estimate, including multiplicities

I checked the primitive-element indicator by writing a=g^k in the cyclic multiplicative group and factoring its squarefree divisor sum. At each prime divisor ℓ of N, the corresponding Ramanujan sum is ℓ−1 when ℓ divides k and −1 otherwise. Thus the product vanishes exactly for nonprimitive exponents, and the prefactor φ(N)/N normalizes the primitive case to one.

For a nontrivial multiplicative character χ, square-root counting gives a sum with multiplicity 1+η(t). Its trivial-in-t part vanishes, and substituting t=−s produces η(−1)J(η,χ). All characters are extended by zero at zero. In the chosen prime class η(−1)=−1; the trivial multiplicative character in the primitive-element expansion nevertheless contributes exactly p, because u²+1 never vanishes.

The Gauss-sum calculation yields modulus sqrt(p) when χ≠η, and the inverse-character Jacobi identity yields modulus one for χ=η. I checked the latter sign as well: the quadratic sum is −1 in this case. For every squarefree divisor d>1 there are exactly φ(d) characters of exact order d; this cancels the denominator in the triangle bound. Counting the remaining squarefree divisors gives the candidate's bound

|P_p/p−φ(N)/N|≤[φ(N)/N](2^omega(N)−1)/sqrt(p).

The six primes below16 are 2,3,5,7,11,13; for every prime at least17, 2≤ℓ^(1/4). Hence the elementary bound 2^omega(N)≤64N^(1/4) is valid uniformly. Together with the exact point count it gives an eventual error at most 1/p+64p^(−1/4). This tends to zero along every admissible sequence, not merely on average. No fixed-base primitive-root conjecture is hidden in this estimate.

## 4. Unconditional mean and the two subsequences

I read equation (1) and the complete Lemma 2 proof in the published Menici–Pehlivan article, pp.255 and262–263. In their notation r=m=1 gives exactly the prime average of φ(p−1)/(p−1), with limit Artin's Euler product A. Their proof uses the unconditional Siegel–Walfisz theorem. The nearby discussion of GRH concerns a different fixed subgroup question and does not enter this specialization.

The candidate also reconstructs the needed mean independently from the standard theorem. Möbius inversion exchanges the sum with primes p≡1 mod d. The tail d>(log X)^6 is O(X/(log X)^6), using the elementary progression count ≤X/d. The small-divisor Siegel–Walfisz error with exponent4 sums to O(X log log X/(log X)^4), hence is negligible compared with π(X). The bound φ(d)≥sqrt(d/2) proves absolute convergence of the coefficient series. All limit and sum passages are justified by these uniform bounds.

The rational lower bound A≥7/24 is valid: keep the factor1/2 at2, bound the sum of odd-prime factors by the telescoping sum over integers n≥3 except4, and apply product(1−a_i)≥1−sum a_i. No decimal approximation is used.

For the small-totient subsequence, let Q be an odd primorial. The CRT residue can even be written explicitly as 2Q+1 modulo4Q: it is3 mod4,1 modQ and coprime to4Q. Dirichlet provides arbitrarily large primes in every such fixed class. Choosing a successive prime for each longer primorial gives theta_p→0 by Euler's prime product. There is no need for a uniform estimate on the least prime in progressions with growing modulus.

For the opposite subsequence, theta_p≤1/2 for every odd p. If eventually theta_p<1/24 on p≡3 mod4, the fixed-modulus prime number theorem would force the full prime average to be at most13/48. This contradicts A≥14/48. Thus infinitely many admissible primes have theta_p≥1/24. This class split is essential; a positive mean over all primes alone would not imply the needed conclusion in the selected half of the primes.

The uniform character estimate now transfers these two arithmetic subsequences to D_p(x): one tends to1, while the other has limsup at most23/24. The same two prime subsequences work for each fixed x in the stated interval, since only the eventual threshold for formula (1) changes with x. The limsup and liminf claims follow.

## 5. Failure of a weak limit

Every normalized period lies in a fixed compact interval, since all periods divide p−1 apart from the already shorter fixed points. More generally, weak convergence of probability measures would imply convergence of their distribution functions at every continuity point of the limiting distribution. Such a function has at most countably many discontinuities. The candidate proves nonconvergence at every point of the uncountable interval [1/2,1), so it cannot be dismissed as failure at one possible limiting atom. The no-weak-limit conclusion is valid.

## 6. Independent checks and boundaries of the verdict

All nine author files and five pinned primary PDF hashes match. The author's local standard-library/SymPy checker was read and replayed; its output is byte-identical, with 101,073 exact controls.

I wrote a separate checker. It performs whole-plane cycle traversal using an array permutation for24 admissible primes below200, checks all zero and nonzero fiber periods and five rational thresholds, and verifies the character identities in each character's own cyclotomic order ring. It also checks the explicit CRT residue, rational constant separation and the uniform elementary inequalities. All **301,761** independent assertions pass. These do not prove infinite prime statements; those rest on the written argument and the credited unconditional arithmetic theorems.

The review supports the explicit theorem and the literal universal OWR target. It certifies neither historical originality, a classification of all birational maps, a polynomial-inverse counterexample, nor a refutation of the narrower later conjectures. Those restrictions must remain visible in publication. No mandatory change to the frozen packet is required, and the parent retains the publication gate.
