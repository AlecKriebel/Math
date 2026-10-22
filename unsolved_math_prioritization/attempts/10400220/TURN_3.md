# Substantive turn3: the marked-cover surgery certificate

## Route and outcome

This turn pursued the precise information lost by a double-branched-cover obstruction. It proves an equivariant surgery-certificate characterization of ordinary unknotting number, extending the classical Montesinos crossing-change correspondence to simultaneous crossing balls. The certificate retains the deck involution. No mutant pair with distinct certificate lengths or usable new lower bound is established, so the original question remains unresolved.

The basic one-crossing cover construction is classical and appears explicitly in Livingston2002 Section2 and in Gordon–Luecke's introduction. The multiple-component formulation and slope normalization below are direct deductions, not a claimed new topological invariant or a historical-priority assertion.

## 1. Exact certificate

Let Sigma(K) be the double branched cover of a knot K in S3, with its specified deck involution tau_K. Consider the standard branched-cover pair(S3,tau_U) over the unknot U. Define an admissible r-component certificate to consist of:

- r pairwise disjoint invariant solid-torus neighborhoods in this standard S3, each core preserved by tau_U and meeting its fixed circle transversely in exactly two points
- on each boundary torus, the original meridional filling slope alpha_i and a new primitive slope beta_i with geometric intersection Delta(alpha_i,beta_i)=2
- equivariant fillings by solid tori with the standard two-fixed-arc quotient, producing a pair equivariantly homeomorphic to(Sigma(K),tau_K), with orientations and quotient markings compatible with the knot category

Then

u(K)<=r if and only if an admissible certificate with at most r components exists. (1)

The integer being minimized is ordinary unknotting number, not equivariant unknotting number of a separately chosen strong inversion of K in the original S3. The involution in(1) acts on the **branched cover**, and is part of the certificate.

## 2. Forward direction

By the diagram definition of u(K), choose a diagram in which at most r crossing switches give the unknot. Small balls around the chosen crossings are pairwise disjoint. Reverse these switches, starting from the resulting unknot diagram.

The double cover of each crossing ball branched along its two trivial arcs is a solid torus. Its core is preserved by the standard covering involution and meets the branch axis twice. Switching the crossing replaces one rational tangle by the opposite crossing tangle. In the torus cover, the two meridian slopes have distance2. Taking the covers of all disjoint balls at once gives exactly the simultaneous equivariant surgery certificate above. The result retains the covering involution of K, rather than only its underlying3-manifold.

This uses simultaneous crossing changes in a diagram, not an unproved claim that arbitrary crossing disks can be made disjoint from a chosen mutation sphere. The mutation sphere plays no role in selecting these crossing balls.

## 3. Converse and the distance-two issue

The quotient of each invariant solid torus is a3-ball with a rational two-string tangle. The exterior quotient is S3 with those disjoint balls removed. An equivariant filling is a rational-tangle replacement in each ball.

Why is distance2 an **ordinary crossing switch**, rather than merely an arbitrary rational replacement? Represent the two rational slopes by primitive integer vectors a,b up to sign, with determinant of absolute value2. There is an SL(2,Z) matrix sending a to(1,0). Change the sign of b if necessary; its image is(p,2) with p odd. A meridian-preserving shear sends(p,2) to(1,2). The standard pair of opposite crossings, with slopes(1,1) and(-1,1), is also carried to this pair by an SL(2,Z) change of marking. The mapping class action of the four-punctured sphere is the corresponding projective integral action on slopes, so the two rational tangles are simultaneously equivalent to the two crossing tangles in a suitable ball diagram.

Their endpoint pairing is unchanged: primitive vectors with determinant even have the same nonzero reduction in F2², and that reduction records one of the three rational-tangle connectivities. Thus replacing these tangles preserves the single knot component. In the quotient of the filled standard cover, the original branch knot U is changed by one ordinary crossing switch in each ball. The specified equivariant identification at the end identifies the branch knot with K. This proves u(K)<=r and hence(1).

Without the distance condition, an equivariant rational-tangle filling would instead bound a rational unknotting count, a different invariant. Without the equivariant identification, it need not be a certificate for K at all.

## 4. Consequence for a proposed mutation proof

Mutants have homeomorphic underlying double covers. A theorem about the least number of half-integral surgeries producing that unmarked manifold may give a common lower bound for their unknotting numbers. It does not identify the two sets of admissible certificates in(1), because their deck involutions need not be conjugate in the required marked surgery description.

In particular, a homeomorphism of the final3-manifolds does not by itself transport the initial standard involution, the invariant surgery link and its quotient markings. An equivariant homeomorphism of the entire final branched-cover pairs would already identify the quotient knots up to the corresponding ambient homeomorphism; it is much stronger than ordinary mutation invariance of the cover.

A viable cover-based attack must therefore retain the involution and prove an obstruction for every equivariant link certificate of a given length, or explicitly transport a minimal certificate between the two relevant actions. The usual unmarked linking forms and correction terms cannot supply that extra step. This is an exact characterization of the missing data, not a claim that the resulting minimization problem has been solved or made algorithmically effective.

## 5. Checks, limits and next route

The exact checker verifies the primitive slope normalization and connectivity statement for a finite exhaustive set of rational slopes, including both determinant signs and nonstandard meridians. These arithmetic checks support the converse's slope step; they do not replace the equivariant tangle-cover argument.

No new knot-identification program, source executable or unverified equivariant Floer bound has been used. A lower bound for symmetry-preserving crossing changes of a strongly invertible knot cannot silently be substituted for the ordinary u(K) in this problem. The present turn yields no concrete separating mutant pair. Two substantive author turns remain, and the next route must either exploit the marked action or produce independent upper/lower certificates in a mutation-sensitive family.
