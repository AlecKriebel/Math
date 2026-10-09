# Scoped results and exact obstructions

This note does **not** solve the action-dependence question. References and the precise source category are fixed in EXACT_STATEMENT_AND_SOURCES.md. The results below are deductions and proof checks supporting five attempted routes; no novelty claim is made.

## 1. A nonfree false positive, with the freeness repair checked

**Proposition 1.** There is a countable group with an ergodic p.m.p. nonfree action whose relation is FI and a free ergodic p.m.p. action whose relation is non-FI. This does not answer the source question. In the construction below no free action of the chosen group can be FI.

**Proof.** Let H = F_2 x F_2 and Gamma = H * Z. The group H is nonamenable and has beta_1^(2)(H) = 0, by the direct-product formula for two infinite groups. Let H act by its Bernoulli shift on X = [0,1]^H with product Lebesgue measure. This is a standard atomless probability space. The shift is free: for h not equal to the identity, a fixed point must have equal coordinates at two distinct indices, a null event. It is mixing because any two cylinder events become independent when their finite coordinate supports separate under a sufficiently far translate. Thus it is ergodic. Its relation is FI by [AG, Corollary 4.20].

Let q: Gamma -> H be the homomorphism that is the identity on H and kills the Z factor, and let alpha(g)x = q(g)x. Its orbit relation is exactly the preceding H relation and it remains ergodic and p.m.p. But every element of the Z factor fixes every point. Essential freeness fails on a set of full measure.

For comparison take the Bernoulli shift beta of Gamma on Y = [0,1]^Gamma. The same cylinder and fixed-coordinate arguments show that beta is free, mixing, p.m.p. and ergodic. For **any** free p.m.p. Gamma-action gamma, its relation splits as

R_gamma = R_(gamma restricted to H) * R_(gamma restricted to Z).

Generation is immediate. An alternating cycle would give a nonempty reduced word in the abstract free product fixing a point, which is excluded on the common free conull set. Both factor relations have the full domain and infinite classes. The split is essential: if it were inessential, [AG, Proposition 4.4(3)] applied to the first full-domain aperiodic factor would give R_gamma = R_(gamma restricted to H) almost everywhere. But for a nonidentity z in the Z factor, the pair (x,zx) cannot be an H-pair at any point in the free set, since hx = zx would imply that h^(-1)z fixes x. This is a contradiction.

Finally consider the often-used freeness repair delta = alpha x beta, with the diagonal Gamma-action on X x Y. It is p.m.p. and free since its second coordinate is free. It is ergodic since alpha is ergodic and beta is mixing (in particular weakly mixing). Nevertheless the preceding argument applies to delta, so its relation is non-FI. The quotient FI relation does not survive as an FI certificate for this extension. QED.

**Related failed rigidity inference.** Even an ergodic full-domain FI subrelation does not force the containing relation to be FI. In the free Bernoulli Gamma-action just used, restriction to the infinite subgroup H is mixing: the finite-coordinate separation argument works along H. It is free and FI by the H criterion. Its ambient Gamma relation is still the essential free product above. Thus inserting an ergodic FI subgroup action into a free product cannot create the missing FI action.

## 2. Invariant mixing and ergodic extraction

We first record an elementary recurrence fact for measured relations. If R is an aperiodic p.m.p. countable relation and A is Borel, then R restricted to A has infinite classes almost everywhere on A. Indeed let A_f be the points of A whose R-class has a finite, nonzero intersection with A, and saturate A_f under R. On that saturation send from each x equal total mass 1 to the finitely many points of its class in A_f. Each x sends mass 1, while each point of A_f receives infinite mass because its R-class is infinite. The mass-transport identity for a p.m.p. relation forces A_f to be null. Its saturation is null as well. This argument does not assume that R is ergodic.

**Proposition 2 (canonical trivialization test).** Let R be an aperiodic p.m.p. countable Borel relation with a fixed countable decomposition R = *_(i in I) R_i. Put

E_i = {x in the domain of R_i : the R_i-class of x is infinite}, and E = union_i E_i.

The fixed decomposition is inessential if and only if, modulo null sets:

1. the E_i are pairwise disjoint;
2. each E_i is invariant for R restricted to E, and R restricted to E_i equals R_i restricted to E_i;
3. E is a complete section for R.

**Proof.** Sufficiency is exactly the definition, taking U_i = E_i and U = E. For necessity begin with a trivializing partition U = disjoint union U_i. By [AG, Proposition 4.4(1)] replace each U_i by its R_i-saturation, keeping a trivialization. By [AG, Proposition 4.4(2)], R_i outside U_i is smooth and therefore has finite classes almost everywhere in the finite-measure-preserving setting. Thus E_i is contained in U_i modulo null sets. On U_i one has R_i restricted to U_i = R restricted to U_i; the recurrence fact makes this relation aperiodic almost everywhere. Since U_i is R_i-saturated, U_i is contained in E_i modulo null sets. Consequently U_i = E_i modulo null sets, and the three properties of the original trivialization give the assertion. All sets involved are Borel (class cardinalities in a countable Borel relation are Borel). Countably many exceptional null sets can be discarded together with their R-saturations. QED.

**Corollary 2.1 (countable mixtures).** For free p.m.p. actions alpha_n of the same group on standard atomless probability spaces, and positive weights t_n with sum 1, their action on the weighted disjoint union is FI if and only if every alpha_n is FI.

**Proof.** For the forward direction restrict to a positive-measure invariant summand and use FI restriction invariance [AG, Proposition 4.10]. Conversely, take any decomposition of the union relation. Its restriction to each invariant summand is a free-product decomposition. Choose a trivializing partition on each summand, using FI there. For each factor index, take the union of its corresponding partition pieces over the countably many summands. This gives a Borel trivialization of the original decomposition. The union of all the complete sections meets every orbit outside one null set. Normalizing a positive summand's measure does not change its null sets or the definition of FI. QED.

**Corollary 2.2 (non-FI ergodic extraction).** If a countably infinite group has a non-FI free p.m.p. action in the source category, it has such an action that is additionally ergodic.

**Proof.** Choose an essential binary decomposition, available by [AG, Proposition 4.8]. Disintegrate the invariant measure into invariant ergodic probability measures for the group action. Almost every conditional measure gives the free set full measure. Every partial Borel isomorphism in an R_i is piecewise a group element; therefore it preserves almost every conditional measure. The fixed splitting and all its combinatorial identities remain valid on the corresponding conditional conull sets.

For this fixed splitting, Proposition 2 expresses inessentiality by the vanishing of countably many measures of fixed Borel sets: intersections of the E_i; violations of invariance or of equality of the restricted relations; and the complement of the R-saturation of E. Violations involving pairs can be projected to the domain using countable uniformizations of R. If these tests held for almost every conditional measure, integrating would make them hold for the original measure. Essentiality therefore persists for a positive set of conditional measures. Choose one such ergodic conditional measure. It is atomless: any atom of positive mass in a free action of an infinite group would have infinitely many distinct translates of the same mass, impossible for a probability measure. This yields an ergodic free atomless p.m.p. non-FI action. QED.

The deduction agrees with the ergodic-extraction observation immediately preceding [TW, Proposition 5.4]. It does not assert the different claim that every FI action has FI relations on almost all of its ergodic components. That claim would require controlling a measurable choice among varying decompositions. The proven countable-mixture statement is enough to rule out the attempted construction by countably patching known non-FI actions.

## 3. The exact common-extension obstruction

**Proposition 3.** Let alpha and beta be free p.m.p. actions of a countable group Gamma, on standard atomless probability spaces. If beta has a non-FI relation, then the diagonal product alpha x beta has a non-FI relation. More generally, any measure-preserving equivariant extension of a free non-FI action is non-FI.

**Proof.** For an equivariant factor map p from a free action tilde-alpha to a free action beta, fix a point x in the common free conull set. The map on orbits is surjective by equivariance. If p(gx) = p(hx), freeness of beta gives g = h. Hence p induces a bijection on each orbit. It is therefore a locally bijective morphism in the precise sense of [AG, Lemma 4.15]. That lemma says that an FI source relation would force the target relation to be FI. Its contrapositive gives the assertion. For a diagonal product, coordinate projections are measure-preserving equivariant factor maps, and the product is free. Ergodicity of the product is neither needed nor asserted. QED.

**Corollary 3.1 (reformulation of the target).** The source question has a positive answer if and only if there is a free FI p.m.p. action alpha of a countable group Gamma and a free non-FI p.m.p. extension of alpha, on standard atomless probability spaces.

**Proof.** Such an extension and alpha are already the requested pair. Conversely, given an FI action alpha and a non-FI action beta, take alpha x beta. It is non-FI by Proposition 3, and its projection onto alpha is the required extension. QED.

This is an equivalence for the original category without an ergodicity requirement; it is not a claim that a common product is ergodic. Crucially, [AG, Lemma 4.15] has the direction “FI extension implies FI factor.” It gives no FI preservation from factor to extension. Asserting that missing direction for all free same-group extensions is, by Corollary 3.1, already a negative solution of the target. The common-extension trick therefore does not resolve the question.

## 4. Finite-index and finite-factor transport

**Proposition 4.1 (finite-index induction).** Let H be a subgroup of finite index n in Gamma. Every FI/non-FI type achieved by a free p.m.p. H-action is achieved by a free p.m.p. Gamma-action. If the input is ergodic, the induced action is ergodic. Thus a mixed pair for H would give a mixed pair for Gamma.

**Proof.** Choose representatives C of the left cosets Gamma/H, including the identity. Given H acting on (X,mu), use C x X with measure (1/n) times counting measure times mu. Write uniquely gc = c' h with c' in C and h in H, and define

g.(c,x) = (c', h.x).

The cocycle identity from multiplication makes this a group action. It permutes the n fibers and preserves the measure in each fiber, so it is p.m.p. If g fixes (c,x), then c' = c and c^(-1)gc fixes x; freeness of the H-action gives g = identity. Standardness and atomlessness are preserved by the finite union.

The slice {identity} x X is a complete section of measure 1/n, and its restricted Gamma relation is precisely the original H relation. Normalize its restricted measure to mu. FI and non-FI therefore correspond by [AG, Proposition 4.11]. Finally an invariant measurable subset of C x X has H-invariant intersection with the identity slice and has conjugate equal-measure intersections with all slices, proving ergodicity equivalence. QED.

The identical coset formula for infinite index gives an invariant counting-times-mu measure of infinite total mass. No probability measure can assign the same positive mass to countably infinitely many transitive coset fibers. This does not forbid other forms of coinduction; it identifies why simple coset induction is not a p.m.p. construction in that case.

**Proposition 4.2 (finite normal quotient, one direction).** Let K be a finite normal subgroup of Gamma. Any free p.m.p. Gamma-action has a quotient free p.m.p. Gamma/K-action with the same FI/non-FI type. Ergodicity is preserved.

**Proof.** Let p:X -> Y = X/K be the quotient and give Y the pushforward measure. Finite Borel quotients are standard. Because the K-action is free, choose a Borel transversal S for its finite orbits. The sets kS, k in K, partition X and have equal measure, so mu(S) = 1/|K|. The map p restricted to S identifies normalized restricted measure with the quotient probability measure. It follows in particular that the quotient is atomless.

If gK fixes p(x), then gx = kx for some k in K. Freeness gives g = k, proving quotient freeness. The slice S is a complete section for R_Gamma, and p restricted to S identifies its restricted relation with the quotient orbit relation: representatives are Gamma-related exactly when their K-orbits are Gamma/K-related. The FI types agree by complete-section invariance. Invariant sets upstairs and downstairs correspond, proving the ergodicity statement. QED.

**Corollary 4.3 (split finite direct factor).** For every finite group K, Gamma and Gamma x K have the same set of attainable FI/non-FI types among free p.m.p. actions in the source category, and likewise among free ergodic actions.

**Proof.** One inclusion is Proposition 4.2. For the other, given a Gamma-action on X, let Gamma x K act on X x K by (g,k).(x,l) = (gx,kl), with uniform measure on K. This action is free and p.m.p.; the slice X x {identity} is a complete section with the original Gamma relation. Ergodicity is equivalent. QED.

We do not extend this converse without proof to arbitrary nonsplit finite group extensions. Lifting a quotient action through a nonsplit extension is an additional cocycle problem. The proved operations transport a seed but supply no seed. Similarly, measure equivalence invariance of MFI only transports the existence of some non-FI action in its contrapositive form; it must not be read as an all-actions matching theorem for FI witnesses.

## 5. A conditional action-specific FI criterion

Call a p.m.p. Gamma-action **Z-cocycle superrigid** when every measurable cocycle c:Gamma x X -> Z can be written, modulo null sets, as

c(g,x) = b(gx) - b(x) + rho(g),

where b:X -> Z is measurable and rho:Gamma -> Z is a homomorphism. The convention for cocycles is c(gh,x) = c(g,hx) + c(h,x).

**Proposition 5.** Let Gamma be a nonamenable countable group with Hom(Gamma,Z) = 0. Let alpha be a free **ergodic** p.m.p. action on a standard atomless probability space. If alpha is Z-cocycle superrigid, then its orbit relation is FI.

**Proof.** Suppose its relation R is non-FI. It is an ergodic, nowhere-amenable p.m.p. relation: the latter property for a free action of a nonamenable group is the interface also used in [AG, Corollary 4.20]. By [AG, Proposition 4.8] it has an essential binary splitting. All hypotheses of **[TW v3, Lemma 5.1]**, including ergodicity, are now satisfied. That lemma provides an aperiodic amenable subrelation S, with domain all of X, which is a free factor: R = S * Q for some Q.

An aperiodic amenable p.m.p. countable relation is hyperfinite and is generated, modulo null sets, by a free p.m.p. Z-action. Let T be its generating automorphism. Define on S the integer cocycle d(T^n x,x) = n. It is well defined by freeness of T. Define the zero cocycle on Q. The free-product normal form extends these uniquely to a cocycle d on R: sum the assigned values along the reduced alternating path. This is measurable because finite paths have countable Borel enumerations; the free-product property ensures that reducing a path does not change the sum.

Set c(g,x) = d(gx,x). This is a measurable Gamma-cocycle. Superrigidity and Hom(Gamma,Z) = 0 imply c(g,x) = b(gx) - b(x). Since Gamma is countable, take a conull set where this identity holds for all g at once. Because T belongs to the full group of R and alpha is free, there is a Borel choice gamma(x) in Gamma with Tx = gamma(x)x. Substituting this choice yields

b(Tx) - b(x) = d(Tx,x) = 1

almost everywhere. But T preserves a probability measure. Thus the distribution of the Z-valued random variable b is invariant under translation by 1: all level sets {b=k} have the same measure. Their countable disjoint union has measure 1, which is impossible. This contradiction proves FI. QED.

**Precise remaining realization problem.** To turn this criterion into a positive answer, one would still need a group Gamma with Hom(Gamma,Z) = 0 which admits both (i) such a free ergodic Z-cocycle-superrigid action and (ii) a free p.m.p. non-FI action, the latter with an explicitly essential decomposition. No such pair is provided here. More generally, an FI action might be found by a different criterion; Proposition 5 is sufficient, not necessary.

A natural attempted realization using a U_fin-cocycle-superrigid Bernoulli action cannot work. [PS, Corollary 1.2] gives beta_1^(2)(Gamma) = 0 in that case. Nonamenability then makes **every** free p.m.p. action FI by [AG, Corollary 4.20], contradicting requirement (ii). This blocks the stronger Bernoulli realization. It does **not** prove that the weaker Z-only condition, or all other action-specific FI criteria, are impossible at positive first L2-Betti number.

## Conclusion

Five substantive approaches produced the scoped results above. No two free p.m.p. actions of the same group with different FI behavior were constructed, and no theorem excluding all such pairs was proved. The target remains unresolved by this work. No numerical test, sampled orbit, or finite graph calculation is used as a substitute for a measured-equivalence-relation argument.
