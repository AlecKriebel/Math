# Attempt 5: homomorphism preservation and the missing nonstandard obstruction

## Strategy

The previous attempts did not construct a definition. This final attempt searches for a nondefinability certificate using preservation of positive formulas. Let T=Th(Q;0,1,+,P₂). A positive-existential formula is preserved by every homomorphism of structures in this language. Thus a map between models of T that sends a nonsquare to a square would disprove the desired definition. We first examine standard-model maps, then formulate exactly what a nonstandard construction would have to achieve.

## Every finite-power standard homomorphism is a projection

**Proposition.** For every finite r≥1, every homomorphism

h:M^r→M, where M=(Q;0,1,+,P₂),

is a coordinate projection.

**Proof.** Preservation of addition makes h an additive-group homomorphism. Divisibility and torsion-freeness imply Q-linearity: for n>0, n h(v/n)=h(v), and hence h((m/n)v)=(m/n)h(v). Therefore

h(v₁,...,v_r)=sum_i c_i v_i,

where c_i=h(e_i) and e_i is the i-th standard basis vector. Each e_i lies in P₂^{M^r}, since all its coordinates are 0 or 1. Thus each c_i is a rational square. Preservation of the named constant 1 gives sum_i c_i=h(1,...,1)=1.

If two coefficients c_i,c_j are nonzero, take the input vector whose i-th coordinate is 1/c_i, j-th coordinate is 1/c_j, and all other coordinates are zero. Since the reciprocal of a nonzero rational square is a rational square, this vector belongs to P₂^{M^r}. Its image is 2, which is not a rational square. This contradicts preservation of P₂. Exactly one c_i is therefore nonzero, and the sum condition forces it to equal 1. This is precisely a projection. □

In particular every endomorphism of M is the identity. Thus searching for a standard self-map that sends a nonsquare to a square must fail. Likewise all finite-arity polymorphisms are projections, so they preserve every relation whatsoever and cannot distinguish N from definable relations. We do not invoke an incorrect general equivalence between polymorphism preservation and positive-existential definability: product preservation is naturally tied to primitive-positive formulas, and disjunction requires separate care. Here the projection calculation simply renders all these standard tests vacuous.

## A precise model-theoretic criterion

The general criterion is standard: compare Manuel Bodirsky, *Complexity of Infinite-Domain Constraint Satisfaction*, Theorem 2.5.2, author text https://wwwpub.zih.tu-dresden.de/~bodirsky/Book.pdf. The proof below specializes it to the present target rather than claiming a new preservation theorem.

**Proposition.** The set N is positive-existentially definable in M if and only if every homomorphism h:A→B between models A,B of T reflects P₂, meaning P₂(h(a)) implies P₂(a).

**Proof of the forward direction.** A defining formula θ(x) satisfies T ⊨ θ(x)↔¬P₂(x). Homomorphisms preserve θ, so a nonsquare in A cannot map to a square in B.

**Proof of the converse.** This is a relative homomorphism-preservation argument; we spell it out to identify its scope. Let φ(x)=¬P₂(x), and let Γ(x) consist of all positive-existential consequences of φ modulo T. Suppose B⊨T and b∈B satisfies Γ. We claim B⊨φ(b).

Consider the theory in a distinguished constant c consisting of T, φ(c), and the negations of all positive-existential formulas ψ(c) that are false of b in B. Every finite part is consistent: otherwise T and φ would imply a finite disjunction of such ψ, itself a positive-existential consequence in Γ, contradicting its falsity at b. By compactness this theory has a model (A,a). Every positive-existential formula true of a in A is therefore true of b in B.

Now take the positive atomic diagram of A, identify its constant for a with b, and combine it with the full elementary diagram of B. Every finite part is satisfiable: existentially quantify the finitely many extra A-constants in that part to obtain a positive-existential formula true of a; by the preceding paragraph it is true of b in B. Compactness supplies an elementary extension B* of B and a homomorphism h:A→B* with h(a)=b. Since A,B* model T and A⊨φ(a), the assumed reflection property gives B*⊨φ(b), hence B⊨φ(b).

Thus T∪Γ entails φ. Compactness reduces this to finitely many formulas from Γ. Their conjunction is positive-existential and equivalent to φ modulo T. It therefore defines N in M. □

The argument allows noninjective homomorphisms in general. In the present theory the prior positive definition of inequality actually forces every homomorphism between T-models to be injective. Its positive definition of strict order also forces order preservation. These facts narrow the target but do not force multiplication preservation, since multiplication is not yet definable in the language by a positive formula.

## Why obvious extension examples do not work

The inclusion Q→R preserves addition, constants and squares, and sends the nonsquare 2 to a square. This is not a counterexample: (R;0,1,+,P₂) is not a model of T, since it satisfies P₂(2) while M does not. The same defect affects Q→Q(sqrt 2). Homomorphism preservation of a putative definition concerns its equivalent interpretation in models of T, not arbitrary extensions in which the claimed equivalence is unavailable.

Nor does an order-preserving Q-linear injection of nonstandard additive groups automatically preserve P₂. One must preserve every square-predicate incidence in the full positive diagram. Gaussian elimination alone controls only the additive part.

## An ultrapower starting point, and its exact gap

Enumerate primes p₁,p₂,... and let a_n=1+(4p₁...p_n)². Each a_n is a positive rational nonsquare. For each fixed finite place p, a_n is a square in Q_p once p occurs in the product. In a nonprincipal ultrapower M*, the element a=[a_n] is still a nonsquare by Łoś's theorem.

Moreover, every fixed quadratic-image formula from Attempt 3 whose rational solution set avoids squares is false of a. That formula has a single fixed local obstruction v; for all sufficiently large n, a_n is square in Q_v, so it cannot belong to that image. This gives an explicit nonstandard element evading all the restricted square-free templates from Attempt 3.

To obtain a full counterexample, however, one would need to realize the entire positive-existential type of a at a square in an elementary extension of M. The argument above only excludes each individual square-disjoint quadratic-image test. It does not prove finite satisfiability of even the restricted positive type at a square: a finite conjunction of these tests can reintroduce simultaneous diagonal systems. Simultaneous diagonal systems may impose genuinely global obstructions. No proof of compatibility for those systems, and no required homomorphism, was obtained. Claiming that local squareness at every fixed prime suffices would simply repeat the unjustified local-global step identified in Attempt 3.

## Final attempt outcome

All standard finite-power homomorphisms were classified, and the correct nonstandard obstruction criterion was proved with compactness. The natural ultrapower construction does not yet satisfy that criterion. Therefore neither a positive definition of all nonsquares nor a nondefinability certificate has been established.

Fresh substantive attempt count: 5/5. Full AIM Question 6 remains unresolved by this investigation. The rigorous restricted lower bounds, exact normal form, conditional genus-two/Büchi implication, and standard-homomorphism classification are retained without a novelty claim.
