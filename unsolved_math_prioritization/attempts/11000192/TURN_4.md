# Author turn 4: a genuine branched-cover pseudo-Anosov and a transverse gap

**Outcome: scoped dynamical partial; original unresolved 4/5.** This turn leaves the blocked trace-polynomial invariant and investigates the branched-cover route suggested in Goldman's original paragraph. It constructs a genuine closed genus-two pseudo-Anosov and a smooth fixed character lying on an invariant two-dimensional surface with stable elliptic dynamics. The missing condition is stability or another nonergodicity mechanism in the four transverse dimensions. Invariant sets on the two-dimensional surface have zero ambient Goldman measure.

## 1. Fix the base automorphism and character action

Let F2=<a,b> be the fundamental group of a once-punctured torus, and c=[a,b]=aba^(-1)b^(-1). Use the automorphism

 φ(a)=ab,   φ(b)=bab.

Direct free reduction gives φ(c)=c. In the ordered abelian basis a,b its matrix is [[1,1],[1,2]], a hyperbolic determinant-one matrix with larger eigenvalue λ=(3+√5)/2. This is a cat-map convention; interchanging the customary matrix basis gives the alternative [[2,1],[1,1]] notation in the literature. The actual words, rather than that name, fix our convention.

For precomposition ρ↦ρ∘φ, coordinates x=tr ρ(a), y=tr ρ(b), z=tr ρ(ab) transform as

 T(x,y,z)=(z, zy−x, z(zy−x)−y).

The commutator trace κ=x²+y²+z²−xyz−2 is preserved. The opposite group-action convention uses T^(-1); fixed-point stability, nonergodicity and pseudo-Anosov type are unchanged by that inversion. This is the polynomial map treated in the complete primary Forni–Goldman–Lawton–Matheus paper, Sections 4–6. We use its corrected Rüssmann-based argument, not Brown's original unchecked twist step.

## 2. An exact Brjuno elliptic point on the admissible level κ=−1

Let ξ be the unique root in (−723/1000,−722/1000) of

 p(X)=X⁴−3X³+2X²+2X−1.

Put η=ξ/(ξ−1) and P=(ξ,η,ξ). Substitution gives T(P)=P and κ(P)=−1. All three coordinates lie in (−2,2), so the SU(2) Fricke description gives an actual irreducible character on the smooth relative sphere. For clarity, an explicit pair of unit quaternions can also be obtained by taking

 A=(ξ/2, sqrt(1−ξ²/4),0,0),
 B=(η/2, (ξη/4−ξ/2)/sqrt(1−ξ²/4), d,0),

where d is the positive square root making |B|=1. The Fricke identity at κ=−1 makes d² strictly positive. Their traces and product trace are ξ,η,ξ, and their commutator is noncentral with trace −1.

Since κ is a regular first integral at P, the ambient derivative has an eigenvalue 1 in the quotient normal to the level. The tangent determinant is 1. Direct differentiation gives the trace of its two-dimensional tangent restriction:

 τ=2ξη−1=2−√13.

In particular −2<τ<2. The two tangent multipliers α,α^(-1) are nonreal unit-modulus algebraic numbers. They are not roots of unity: τ has irreducible polynomial τ²−4τ−9, whose other conjugate 2+√13 exceeds 2. Every conjugate of the sum of a root of unity and its inverse lies in [−2,2]. This contradiction excludes roots of unity of every order, not just a finite resonance list.

The needed arithmetic statement is stronger than mere irrationality. The Baker–Wüstholz logarithm bound implies that the argument θ=Arg(α)/(2π) is Diophantine. Indeed, the nonzero linear form q Log α−2p Log(−1) has a bound C q^(−K) when p is a nearest integer to qθ; division by 2πq gives a polynomial lower bound on |θ−p/q|. This standard consequence is proved explicitly in Ferreira–Ribas, arXiv:2602.23597v1, Theorem 1.1 and Section 3, which was read in full for this implication. It does not follow by simply applying Roth's theorem to α, since the rotation angle and the multiplier are different numbers. Diophantine angles satisfy the Brjuno sum: the continued-fraction denominator growth bound makes Σ(log q_(n+1))/q_n converge.

Rüssmann's real-analytic area-preserving stability theorem, as precisely stated and applied in Forni–Goldman–Lawton–Matheus Theorem 4.8, now makes P a stable elliptic fixed point of T on κ=−1. There are arbitrarily small invariant neighborhoods, so the two-dimensional relative action is nonergodic. The same neighborhoods are invariant for T³. No unverified nonzero first Birkhoff coefficient is required in this two-dimensional application. This claim is credited to those standard arithmetic and stability results, with the exact algebraic point supplied here as a diagnostic construction, not a novelty claim.

## 3. Explicit covers on which a cat-map power lifts

For any odd n≥3, define a permutation representation of F2 on Z/nZ by

 a↦r, r(j)=j+1;   b↦s, s(j)=−j.

Permutations in the displayed algebra are composed right-to-left. The image is transitive, and [r,s]=r² is an n-cycle. Thus the associated connected n-sheeted cover of the punctured torus has one boundary component, covering the base boundary with degree n. Its Euler characteristic is −n. Capping its boundary gives a branched cover of the closed torus, with local model w↦w^n over the puncture and genus g=(n+1)/2.

The action of φ on the monodromy pair is (P,Q)↦(PQ,QPQ). The following is an exact symbolic calculation in the dihedral group, not a finite-degree search:

 (r,s) → (rs,r^(-1)) → (r²s,rs) → (r,s).

Hence φ³ fixes the monodromy homomorphism, including the chosen sheet stabilizer, and lifts to the cover. Its closed extension f_n is pseudo-Anosov: the two linear invariant measured foliations of the torus cat map pull back, with expansion λ³ and contraction λ^(−3). At the single branched preimage, the original regular two-prong point becomes a 2n-prong singularity. These are valid closed-surface pseudo-Anosov foliations, with no one-prong issue. In particular n=3 gives an explicit closed genus-two pseudo-Anosov f_3.

This construction actually establishes the pseudo-Anosov requirement, unlike the reducible subgroup in the first three turns.

## 4. Which representations extend, and equivariance

Write H for the finite-index subgroup defining the punctured cover. Its peripheral element is conjugate in F2 to c^n. The restriction ρ|H extends across the capped disk if and only if ρ(c)^n=I. Consequently the admissible SU(2) boundary traces are the finite set 2cos(2πj/n), with repetitions identified. For n=3 the nontrivial value is precisely −1, the level used in Section 2. Cayley–Hamilton gives C²+C+I=0 for a unitary determinant-one matrix of trace −1, so C³=I and C≠I.

Restriction and filling therefore define a semialgebraic character map

 R: X_(−1)(Σ_(1,1),SU(2)) → X(Σ_2,SU(2)).

By φ³(H)=H, its equivariance is exact:

 R∘T³ = f_3^*∘R.

The fixed character P pulls back to a fixed character R(P). It is a smooth irreducible point of the closed character variety, as verified next.

The polynomial p is irreducible over Q: modulo 2 it is X⁴+X³+1, which has no linear factor and is not divisible by the only irreducible quadratic X²+X+1. It has exactly two real roots and two nonreal roots, as an exact Sturm count confirms. If A had finite order, every algebraic conjugate of tr(A)=ξ would be real, since it would be a sum of roots of unity. Therefore A has infinite order. A proper closed infinite subgroup of SU(2) is contained in the normalizer of a circle: this follows from the proper Lie subalgebra classification, since a positive-dimensional proper connected subgroup is a circle. In that normalizer every element outside the circle has trace zero. Here η≠0 and the commutator is nontrivial, so A and B cannot both lie in such a subgroup. Their image is dense in SU(2).

Restriction of a dense representation to a finite-index subgroup remains dense: the closure of the image of a finite-index normal core is a closed finite-index subgroup of the connected group SU(2), and must equal SU(2). Thus ρ|H is irreducible and R(P) lies in the smooth closed locus.

The map is locally an immersion at P. One way to check the differential is restriction in twisted first cohomology. Restriction to a finite-index subgroup is injective over R, by the restriction–transfer identity multiplying by the index. Filling injects closed-surface cohomology into punctured-cover cohomology. Hence the differential of the relative two-dimensional tangent space has zero kernel. Equivalently, choose parabolic infinitesimal representatives vanishing near the base boundary after a gauge adjustment; their pullbacks extend over the capped disk and their Goldman pairing is three times the original pairing, by integration over the degree-three cover. This also proves that the immersed local surface is symplectic. The finite-dimensional analytic constant-rank theorem makes it embedded after restricting to a sufficiently small neighborhood of P.

For completeness, no global quotient-by-conjugation ambiguity is being assumed away at dense points. If two dense representations agree after restriction to H, compare them on the normal core. Their values on any group element differ by ±I, producing a sign character trivial on H. An index-three subgroup cannot be contained in an index-two kernel, so that character is trivial. Thus the restriction is injective on the dense-image locus in this odd-degree case.

## 5. Why this is still not the requested example

The image of R has real semialgebraic dimension at most 2. The smooth irreducible character space of a closed genus-two surface has real dimension 6, and Goldman volume is a smooth nonvanishing top-degree form there. Every semialgebraic subset of dimension at most 2 therefore has zero Goldman measure. This includes all the invariant neighborhoods transported from the relative sphere, irrespective of their positive area measured within that sphere.

More generally, this n-sheeted one-boundary construction gives a closed space of dimension 6g−6=3n−3, while each admissible fixed-boundary source level has dimension at most 2. Even allowing the entire three-dimensional punctured-torus character ball could not produce an ambient positive-volume set for genus≥2 through this restriction map. A countable union of such fixed-cover images on a fixed target surface is still null. Neither dimension counting nor this particular null locus proves ergodicity of f_3 on its ambient space.

The missing substantive step is transverse. At R(P), the closed tangent space is six-dimensional, with a known invariant symplectic two-plane carrying the elliptic base dynamics and an invariant symplectic four-dimensional complement. No spectrum, nonresonance condition, normal-form nondegeneracy or stable neighborhood has yet been established in that complement. The two-dimensional Rüssmann theorem cannot simply be applied to the six-dimensional germ. A normally hyperbolic transverse direction would obstruct this particular local-stability repair; an elliptic spectrum alone would still not prove a higher-dimensional KAM conclusion.

## 6. Other branch checked, evidence, and final-turn direction

A separate rational-invariant shortcut was examined but not promoted. In a global UFD with only constant units, an invariant reduced fraction forces numerator and denominator to be scalar eigenfunctions; finite multicurve support would then obstruct a nonconstant rational invariant of a pseudo-Anosov. But the retrieved Bellamy–Schedler Theorem 1.3 gives local factoriality with an explicit genus-two SL2 exception, and Q-factoriality is not global unique factorization or triviality of the Picard group. Those hypotheses are not established here. Thus this does not extend Turn 3 to all rational functions.

The exact checker verifies the free-group boundary word, the trace polynomial and κ identity, the algebraic fixed point and tangent trace elimination, root isolation and irreducibility certificate, the dihedral monodromy cycle for a reproducible finite range, and the universal symbolic dihedral calculation. Finite computations do not replace Baker–Wüstholz, Rüssmann stability, covering theory or the dimension argument.

The fifth author turn will test the actual four-dimensional transverse dynamics of this explicit degree-three candidate, rather than count the lower-dimensional stable locus as an ambient nonergodicity proof. The original target remains unresolved after **4/5** substantive turns. No full source critique or PR precedes the independent audit.
