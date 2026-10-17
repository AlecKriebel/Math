# Independent acceptance: actual cusp vanishing and compactification

14 October 2026 UTC. Row 1777 / 30005572. Review within the final shared PASS 5/5; no additional mathematical pass. The original construction remains **UNSOLVED**.

## Verdict and pins

**ACCEPT the frozen restricted package:**

- `pass5_cusp_compactification/CUSP_REFLECTION_AND_COMPACTIFICATION.md`, SHA-256 `8eb42f475cce66348c6de51990112bbd011eb703b7425483d79fd98f9a380993`.
- `pass5_cusp_compactification/EXPLICIT_REMAINING_FIVE_CUSP.md`, SHA-256 `e7a45fbba22523dc48e3903bbcc5b16b34b4b0d9caf4bf37d9fbc4e863fd70ea`.

The first gives genuine zero values of every existing arithmetic homomorphism at cusps admitting a strict reflection, an exact all-cusp topological criterion for the ordinary and Gaussian unit groups, a general-unit criterion, and a sign-trivial target compactification theorem for locally shallow levels. The second isolates two genuine but unevaluated five-primary cusp values in an explicit Gaussian example where smoothing and arithmetic integrality are already available. It is neither a nonzero value computation nor a counterexample.

## 1. Source lattice and the global reflection

The column lattice a_r^{-1} direct-sum O has automorphism matrices with upper-right entry in a_r^{-1} and lower-left entry in a_r, matching the source row-action group convention. Its marking lambda=(0,1) yields exactly c=0 and d=1 modulo N for the strict subgroup, and c=0 with d a unit for Gamma0. The source enlargement by central global units has the same coarse quotient. Even at unit-noninjective levels the intersection with the strict group causes no error: its order divides six, and no direct-product decomposition is asserted.

For a cusp line, its saturated intersection I with the lattice has projective rank-one quotient J over the Dedekind ring. The splitting Lambda=I direct-sum J therefore exists without principalizing either summand. The reduction map for Hom(J,I) is surjective. Consequently the required off-diagonal entries lift to global integral lattice automorphisms; this is stronger than merely displaying compatible local matrices.

The ideal D determined by lambda(I)=D/N is independent of the complement. Its local exponents r_q are exactly the truncated valuations of the first marked coordinate. Local trivializations of the two projective modules modulo N are legitimate because the finite quotient ring has trivial Picard group.

For a primitive marked row (u,v), the two strict involutions give exactly the alternatives

- 2u=0, equivalently r_q>=n_q-e_q at every level prime;
- ub=2v solvable, equivalently r_q<=e_q at every level prime,

where n_q=v_q(N) and e_q=v_q((2)). When u is not locally a unit, v is, so the second divisibility criterion is exact. The off-diagonal entry cancels in the square of each reflection. Both conjugate the full strict unipotent lattice T to its negative.

For any homomorphism to an R=Z[1/6] module, conjugate elements have the same value, while inverse unipotents have opposite values. Thus the actual value is zero, including on the two lattice generators. This argument operates on the already constructed specialized homomorphism; it does not need to specialize a new geometric comparison cochain at a possibly singular point. The finite cusp quotient has order supported at two and three, so the same vanishing holds on the entire cusp stabilizer.

## 2. Exact topological scope and units

For units {+1,-1}, every nontrivial action on the cusp unipotent lattice comes from one of the reflected diagonal pairs. If neither condition holds, all stabilizers act trivially on T. The homology sequence of the finite quotient then identifies H_1 of that cusp stabilizer with T tensor R, of rank two. This is an ambient boundary statement, not a computation of the image of that boundary in H_1(Y).

The two valuation boxes cover all possible cusp vectors exactly when at most one prime has n_q>e_q and at that prime n_q<=2e_q+1. If two primes are active, one can choose an endpoint at each in opposite directions. If only one is active, a missed integer exists precisely when n_q>=2e_q+2. Every vector is realized already in the principal component, using the primitive cusp vector (1,c) with gcd((c),N)=D. No unproved all-component realization theorem is required for the converse.

The all-unit criterion is likewise correct: an unequal diagonal pair epsilon,delta occurs precisely in the displayed box determined by v_q(epsilon-1) and v_q(delta-1). Its ratio acts on T, and one minus that ratio is invertible after inverting six. This annihilates the coinvariants. For Q(i), all additional boxes lie in the +/-1 boxes. For Q(sqrt(-3)), the cube-root rotations produce the separately stated levels through the cube of the prime above three, with a middle boundary lattice at the fourth power. The proof does not make incompatible independent global-unit choices at different primes.

Under the all-cusp condition the actual boundary H_1 is zero. The accepted compactification exact sequence then makes H_1(Y,R)->H_1(X,R) an isomorphism. Its naturality preserves every already established correspondence relation. It supplies no new bad-U identity.

These topological statements hold at small levels independently of unit-injectivity. Their application to arithmetic maps remains limited to levels where such maps actually exist. Invertible unit orders are not being used as a substitute for the missing marked-CM descent.

## 3. Diamond reflections and the target projector

If each local cusp exponent lies in the union of the two local intervals, a single global reflection of the form [[-1,b],[0,1]] can be constructed. Its marking multiplier is a CRT collection of local signs: a=-1 where ub=-2v is solved, and a=1 where 2u=0. The projective Hom reduction supplies one global b. This avoids the false assertion that a strict global reflection may independently switch its two diagonal eigenvalues at different primes.

The subgroup W_N is the image of the local-sign subgroup under the principal ray map, with global-unit identifications already quotiented out. It has exponent two; its averaging projector lies in R[Gal(F(N)/F)]. This averages no five-group and introduces no source-character action by assumption.

For the actual Gamma0 crossed homomorphism, the unipotent acts trivially on coefficients. In conjugation by the reflection the two terms involving the value on the reflection cancel. The exact equation is

(1+R_N(a)) z(n)=0.

After applying the W_N-invariant target projector, the coefficient is two, hence the value vanishes. The assertion is unchanged if one replaces the cocycle by a cohomologous representative, since coboundaries restrict to zero on Gamma1.

If n_q<=2e_q+1 at every prime, the local intervals cover every cusp exponent. Thus the W_N-trivial target summand of every existing Gamma0 class compactifies. For a prime-to-p full-ray character this means chi restricted to W_N is trivial. It leaves the p-primary ray action intact, including p=5. On a sign-odd summand the displayed equation can be vacuous; no division by zero or nonunit occurs.

This is a direct parabolicity theorem with its own explicit hypotheses. It neither deletes the residual-character hypotheses from the source's different spectral argument nor proves that every source-covered character is included here.

## 4. The explicit Gaussian stopping point

For pi=2+i in Z[i], N=(pi)^2 is unit-injective. The residue-unit quotient has order20/4=5, so the ray group is C_5. The conjugate prime above five is absent from N, hence the squared-cyclotomic exception does not factor through this ray group. The accepted full unaugmented open R-map exists.

The prime-power arithmetic residue module has exponent Norm(pi)-1=4, so it disappears over R. The existing map therefore has its values in K_2(O_L) tensor R. This uses the unconditional residue-module calculation at its actual coefficient scope, not an imported five-primary map from the original source.

The stated conjugation by tau=[[1,0],[pi,1]] gives

gamma(z)=[[1-pi z,z],[-pi^2 z,1+pi z]].

For z in pi O these are strict level elements; pi and i pi give two Z-basis loops. The middle cusp exponent is one at depth two. Since all distinct Gaussian units remain distinct modulo pi, its stabilizer has no nontrivial diagonal rotation. Its ambient boundary H_1 has rank two.

For arbitrary t in O, gamma(t) lies in Gamma0 and commutes with these loops. Its lower-right residue 1+pi t ranges over the principal-unit subgroup, which maps bijectively to the ray C_5. The crossed-homomorphism identity therefore places both actual values in the Galois invariant subgroup. Existing p>=7 compactification applies because no level prime lies above p and the source exclusions are automatic; source comparison identifies those components. Thus the two unknown values are specifically in (K_2(O_L) tensor Z_5)^{C_5}.

The report correctly stops there. Invariants under a degree-five cover are not identified with descent, and multiplication by five from restriction/transfer is not canceled. Neither value has been shown nonzero or zero. Compactification also requires the other cusp restrictions, so this is not asserted to be the sole missing test.

## 5. Norm kernels, source calibration, and checks

The earlier bad-U norm-zero theorem remains restricted to proper lower level and its declared inverse correspondence. Inflated characters and prime-to-p norm degree are still needed for actual cancellation. The reflection theorem does not change those hypotheses, handle the pure prime-power origin, or eliminate wild norm kernels.

All vanishing statements are homogeneous under the accepted inverse-tame sign transport. This is sufficient for the present group-theoretic reasoning. It does not identify differently signed nonzero theta-symbol values or supply the missing Cremona-edge orientation. Nor is literal invariance of independently chosen mixed-coordinate primitives used anywhere in this proof.

The final author checker was copied into the review directory to avoid writing its output into the frozen proof directory, then replayed under Python -O and -OO. Both outputs agree and the complete output matches the frozen author result. It passes 1,922 integer conjugation identities, 3,599 primitive modular rows, 8,628 diamond solutions, 111,150 valuation boxes, 48 depth thresholds, 48 exceptional-unit level cases, and seven Gaussian ray checks. An independently written checker passes 28,679 primitive local rows and 538,083 valuation vectors across 6,174 boxes. These finite tests do not calculate K_2 values or replace the global projective-module proof.

The retained LSSW author manuscript was inspected at Section5.2, including its cusp-stabilizer description, prime-level involution observation, and restricted compactification theorem: https://www.math.ucla.edu/~sharifi/publ/imagquad.pdf . Earlier acceptances and both sign/model-transport clarifications were read at their frozen scope.

No unrestricted compactification, new arithmetic small-level construction, all-character auxiliary removal, prime-power residue cancellation, full bad-U theorem, or genuine full relative theta calibration follows. The full construction remains UNSOLVED.
