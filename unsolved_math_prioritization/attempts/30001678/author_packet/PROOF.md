# Smoothness on perfect products: proved restricted results and obstructions

## 0. Target and disposition

Work in ZFC. The source problem concerns a Borel equivalence relation E on R^omega admitting a Borel reduction to the orbit relation of a Borel action of a Polish group. The desired domain is P = product_n P_n, with EVERY P_n nonempty, closed, and without isolated points. The conclusion is a Borel classifier c:P -> 2^omega satisfying x E y iff c(x)=c(y). Here smoothness is descriptive-set-theoretic. No differentiability, Whitney jets, C^k, or C-infinity assumption or conclusion is involved.

The general question is UNRESOLVED IN THIS ATTEMPT. The five routes below give restricted results and precise obstructions. None is presented as new, a complete solution, or an admissible counterexample to the source question. Source attribution and inspection limits are in SOURCE_STATUS.md.

A Borel reduction is a Borel map f with x E y iff f(x) F f(y); it need not be injective. A perfect subset of the entire sequence space need not be a product. All countable products have their product topology, not the box topology.

### Elementary Cantor extraction

Every nonempty perfect subset A of R contains a Cantor set, and does so in every nonempty relatively open portion of A. Here and below “Cantor set” means a space homeomorphic to 2^omega and compact in the ambient real line. To construct one, choose a bounded closed interval with interior meeting that portion. Inductively, inside the interior of each current interval choose two distinct points of A and disjoint closed intervals around them, with closures in the parent interior and diameters at most 2^(-k) at level k. This is possible because no point of the relatively open portion is isolated. Require each child interior to meet A. Each infinite branch has a unique limit, in A because A is closed. Distinct branches give distinct limits, by disjoint children. The resulting continuous injection of compact 2^omega is a homeomorphism to a compact subset of A, with no isolated points.

Consequently, all existential positive results may choose compact Cantor factors. This never substitutes a singleton for a perfect factor. Passing from the Cantor-space formulation to R^omega is done by coordinatewise embeddings, not an arbitrary Borel isomorphism of the whole space.

## 1. Orbit-closure separation

### Proposition 1

Let a Polish group G act continuously on a Polish space Y. If every orbit is closed, the orbit relation F is smooth. Every Borel equivalence relation Borel reducible to F is therefore smooth on its whole domain, and in particular on any perfect product in its domain.

**Proof.** Choose a countable base (U_k) for Y and a countable dense subset D of G. Define

    c(y)(k) = 1 iff there is d in D with d.y in U_k.

For each fixed d, the map y -> d.y is continuous. Each coordinate of c is Borel, being the indicator of a countable union of open sets. Density of D and continuity of g -> g.y show that the bit is 1 exactly when G.y meets U_k. Thus c(y) records exactly which basic open sets meet the orbit closure. Two closed subsets of a metrizable space are equal iff they meet the same basic open sets: a point outside one closed set has a basic open neighborhood disjoint from it. Hence c(y)=c(z) iff the orbit closures agree. Under the closed-orbit assumption this is equivalent to G.y=G.z. Composing with a Borel reduction proves the last assertion. QED.

For a continuous action of a compact group, every orbit is compact and hence closed, so the proposition applies. No compactness of Y is needed.

**Exact obstruction.** Closed orbits are absent from the general source assumptions. The countable discrete group Fin(omega) acts on 2^omega by flipping finitely many bits. Every orbit is dense: any prescribed finite prefix can be obtained by finitely many flips. Therefore the orbit-closure code is constant on all of 2^omega. The orbit relation is E0, eventual equality of bits, and is not smooth by Section 4. The failure is separation of distinct dense orbits, not failure of Borelness of the code. Making an arbitrary reduction continuous does not fix it: the identity reduction to E0 is already continuous.

## 2. Independent-coordinate antichains

### Lemma 2.1 (countable Borel sections are meager)

If C is a Cantor space and A is a Borel subset of C x C whose vertical sections A_x are countable, then A is meager.

**Proof.** Borel sets have the Baire property. This follows because sets equal to an open set modulo a meager set form a sigma-algebra containing the open sets. If A were nonmeager, the Baire property would give nonempty open U,V in C such that A is comeager in U x V. Cover its complement there by closed nowhere dense sets F_i relative to U x V. Set D_i=(U x V)\F_i. For each nonempty basic open W in V, the set

    O_i,W = {x in U : D_i intersects {x} x W}

is open and dense in U: openness follows from openness of D_i, and density from density of D_i in U x V. Choose x in the intersection of the countably many O_i,W; this intersection is comeager and nonempty in the Baire space U. Each section (D_i)_x is open dense in V. Therefore A_x contains their intersection, a comeager subset of V. A countable set is meager in the nonempty perfect Baire space V, so it cannot contain a comeager subset. Contradiction. QED.

### Lemma 2.2 (perfect antichain construction)

If a relation R on a Cantor space C is meager as a subset of C x C, there is a Cantor set K subset C such that no two distinct elements of K are R-related.

**Proof.** Cover R by closed nowhere dense F_0,F_1,... . Construct nonempty clopen sets V_s in C indexed by finite binary strings. At each level split every current V_s into two disjoint nonempty clopen children, of diameter at most 2^(-|s|-1). For each ordered pair of distinct leaves at the new level, shrink those two clopen sets so their product misses F_0 union ... union F_n. Such a nonempty subrectangle exists because the union is closed nowhere dense. There are only finitely many ordered pairs; shrink successively. Every previously imposed exclusion survives subsequent shrinking, and all leaf sets remain nonempty. Nestedness and splitting persist.

Let K be the intersection over levels of the union of their leaves. Compactness and shrinking diameters identify K with 2^omega. If x != y belong to K, their branch labels differ from some level onward. At any sufficiently large level, their distinct leaf rectangle misses a specified F_i, so (x,y) is outside every F_i and hence outside R. QED.

### Proposition 2

For each n let A_n be a nonempty perfect subset of R, and let E_n be a Borel equivalence relation on A_n with countable classes. Define E on product_n A_n by

    x E y iff, for every n, x_n E_n y_n.

There are Cantor sets P_n subset A_n such that E restricted to product_n P_n is equality.

**Proof.** Choose a Cantor subset C_n of A_n. Restrict E_n to C_n. Lemma 2.1 makes it meager, and Lemma 2.2 supplies P_n. For x,y in the resulting product, x_n E_n y_n iff x_n=y_n. Taking all coordinates proves E is equality. It has a continuous classifier into 2^omega: choose homeomorphisms h_n:P_n -> 2^omega and interleave their bits using any fixed bijection omega x omega -> omega. QED.

This applies to the native coordinatewise action of product_n Gamma_n when each Gamma_n is a countable discrete group acting continuously on A_n. The product group is Polish, its coordinatewise action is continuous, and its orbits are exactly the coordinatewise orbit relations. The existence of a group element from a sequence of individual witnesses uses countable choice, available in ZFC.

**Exact obstruction.** The assertion is about the given coordinate structure. A general Polish group action, or a general Borel reduction to one, need not decompose into independent countable-coordinate relations. Pulling back a convenient target rectangle is invalid without another argument. For example, the continuous injection

    f(x_0,x_1,...) = (x_0,x_0,x_1,x_2,...)

has image constrained by y_0=y_1. Its image contains no full product of nonempty perfect factors. Indeed a product contained in y_0=y_1 would force its first two factors to be the same singleton. A target product with disjoint first two factors even has empty preimage. This refutes the proposed rectangle-transfer step, not the original conjecture.

## 3. Small boxes inside translation orbits

### Proposition 3 (box criterion)

Let H be an additive subgroup of R^omega. Suppose there are delta_n>0 such that product_n [-delta_n,delta_n] is contained in H. For any product of nonempty perfect A_n subset R there are Cantor P_n subset A_n for which every pair in product_n P_n differs by an element of H. Thus the relation x-y in H is the one-class relation on that product.

**Proof.** Choose, in each A_n, a nonempty relatively open interval portion of diameter at most delta_n, and extract a Cantor subset P_n. If x,y belong to the product then |x_n-y_n|<=delta_n for every n. The hypothesis gives x-y in H. A constant map is the required Borel classifier. QED.

### Corollary 3.1

The criterion applies to the usual translation actions of l^p on R^omega for every real 1<=p<infinity, and of c_0 on R^omega. It also applies to the weighted space H={z: sum_n w_n |z_n|^p < infinity}, with every w_n>0, endowed with its weighted l^p norm topology.

**Proof.** In the weighted case choose delta_n=(2^(-n-1)/w_n)^(1/p). Then sum_n w_n delta_n^p=1. In the c_0 case take delta_n=2^(-n-1); any sequence dominated by delta_n tends to zero. The weighted l^p space is isometric to ordinary l^p via z_n -> w_n^(1/p)z_n, so is a Polish group. Its inclusion into R^omega is continuous because each coordinate is norm-continuous. Coordinatewise addition consequently defines a continuous action on R^omega. The same assertions hold for c_0 with its sup norm. The l^p membership condition is Borel: it is a union over integer bounds of intersections of finite partial-sum inequalities. The c_0 condition is a countable intersection/union of coordinate inequalities. These are admissible Borel orbit relations. QED.

**Exact obstruction.** The method proves the stronger one-class conclusion, which need not be possible even for admissible coordinatewise actions. For the Polish group Q^omega, with each copy of Q discrete, acting on R^omega by translations, a single orbit has only a countable rational translate in each coordinate. It contains no nonempty perfect product. Proposition 2 nevertheless gives a perfect product on which its orbit relation is equality. Thus absence of an H-box is not a counterexample to smooth canonization. Conversely the finite-support subgroup cannot contain a positive-width full box: choosing a nonzero value in every coordinate gives infinite support. Its eventual-equality relation is examined next; one may not declare this subgroup with its inherited topology to be a Polish group and thereby manufacture a counterexample.

## 4. Tail equivalence: exact rejection of three shortcuts

On 2^omega let a E0 b mean that a(k)=b(k) for all sufficiently large k. On R^omega let x E1 y mean that x_n=y_n for all sufficiently large n.

### Lemma 4.1

E0 is not smooth.

**Proof.** A Borel subset B of 2^omega invariant under finite changes is meager or comeager. If it is nonmeager, its Baire property makes it comeager in some basic cylinder [s]. Finite bit flips transport that cylinder to every cylinder of the same length and leave B invariant. There are finitely many such cylinders, so B is comeager everywhere.

Suppose c:2^omega -> 2^omega is a Borel classifier for E0. For each k, the invariant Borel set {a:c(a)(k)=1} is meager or comeager. Choose its comeager bit value b(k). The intersection of the countably many comeager bit fibers is comeager and nonempty. All its points have code b, so it lies in one E0 class. But each E0 class is countable, being obtained by countably many finite flips, and hence meager. A nonempty Baire space cannot have a comeager subset contained in a meager set. Contradiction. QED.

### Proposition 4

E1 restricted to ANY product of nonempty perfect real sets is nonsmooth.

**Proof.** In each factor P_n choose two distinct points a_n^0,a_n^1. The coordinatewise map

    i:2^omega -> product_n P_n,  i(b)_n=a_n^(b(n))

is continuous and satisfies i(b) E1 i(c) iff b E0 c. A Borel classifier for the restriction of E1 would compose with i to classify E0, contradicting Lemma 4.1. QED.

In fact, by choosing a Cantor subset of each P_n and its coordinatewise homeomorphism from 2^omega, one embeds the full Cantor-coordinate version of E1 into the restriction. No cardinal hypothesis beyond ZFC is used.

Three false shortcuts are now explicitly excluded.

1. **Arbitrary perfect set versus product.** For any Cantor C subset R, the diagonal D={(t,t,...):t in C} is compact perfect, and E1 on D is equality. D contains no nonempty perfect product: its first two coordinates would force singleton factors. Thus an arbitrary perfect smooth restriction does not answer the product question.
2. **Increasing unions.** Define F_N by equality in every coordinate n>=N. Each F_N is closed and has the continuous tail classifier. These equivalence relations increase, but their union is E1 and fails on every perfect product. There is no valid inference from closed or smooth finite-tail stages to a smooth limit.
3. **Finite testing.** On a finite coordinate set, eventual equality of coordinates is the universal relation, since all differences are finitely supported. Its behavior cannot diagnose the infinite-product obstruction. More concretely, sequences y^N consisting of N ones followed by zeroes satisfy y^N E1 0 and converge coordinatewise to the constant-one sequence, which is not E1-related to 0. Thus the E1 graph is not closed.

**Why this is not a counterexample to the source question.** Kechris–Louveau, 1997, Theorem 4.2 proves that the Cantor-coordinate E1 is not Borel reducible to any orbit relation of a Borel Polish-group action. That theorem is an imported, explicitly attributed result; it is not reproved here. A reduction of real-coordinate E1 would restrict along a coordinatewise Cantor embedding to a reduction of their E1, so their obstruction applies. The source's orbit-reducibility hypothesis excludes precisely this example. Section 4 is a negative control on proof methods, not a purported source resolution.

## 5. Rectangular fusion and an equivalent closed-restriction goal

The following proof isolates exactly what an attempted fusion argument still has to achieve. It also explains why continuous reading of an existing classifier is legitimate, but assuming such a classifier at the start is circular.

### Lemma 5.1 (comeager rectangular fusion)

Let K=product_n K_n, where each K_n is a Cantor set. Every comeager subset of K contains a product of Cantor subsets of the K_n.

**Proof.** It is enough to meet a sequence O_0,O_1,... of dense open subsets of K, since every meager set is contained in a countable union of closed nowhere dense sets. Maintain finitely many nonempty clopen leaf sets in each of finitely many active coordinates; in each inactive coordinate maintain one nonempty clopen reservoir. At a finite stage all but finitely many reservoirs are the entire factor. The union of leaves in each coordinate, together with the reservoirs, is a product restriction. Every choice of one leaf in each active coordinate specifies a nonempty open cylinder in K.

At stage m, activate coordinate m if necessary. Split each leaf in coordinates 0,...,m into two nonempty disjoint clopen children, small enough to have diameter at most 2^(-m). (Earlier refinements may have restricted some higher coordinates' reservoirs, but have not yet required them to split.) There are finitely many combinations of the active leaves. Process these combinations successively. For a current combination, density and openness of O_m yield a nonempty basic open subrectangle lying inside both its cylinder and O_m. Replace each selected leaf by a nonempty clopen subset of the corresponding subrectangle coordinate. Restrict any inactive coordinate mentioned by that subrectangle by shrinking its single reservoir to a nonempty clopen subset. No unselected leaf is removed. Previously processed rectangles stay inside O_m after these shrinkings; every remaining combination stays nonempty and open, so the process continues.

At the end of stage m the entire current product restriction is contained in O_m: its finitely many active-leaf cylinders cover it, and each was processed. In each fixed coordinate, take the intersection of its descending compact unions of leaves/reservoirs over all stages. The intersection is nonempty by compactness. From the coordinate's activation onward every leaf splits at each later stage, no leaf is lost, and diameters tend to zero. The binary-branch argument identifies that intersection P_n with Cantor space. Later shrinkings preserve every earlier O_m inclusion. Therefore product_n P_n is contained in every O_m. QED.

### Lemma 5.2 (continuous reading on a product)

If f:K -> Y is Borel, with K as in Lemma 5.1 and Y second-countable metrizable, some product of Cantor subsets of K has continuous restriction of f.

**Proof.** For a countable base (U_i) of Y, use the Baire property to write f^(-1)(U_i) equal to an open V_i modulo a meager set M_i. Outside the union of all M_i, the preimage of each U_i agrees with the relatively open V_i. Thus f restricted to this comeager set is continuous. Lemma 5.1 supplies a Cantor product inside it. QED.

### Lemma 5.3 (closed compact equivalence relations)

Let K be compact metrizable and nonempty, and let E be a closed equivalence relation in K x K. Then E is smooth.

**Proof.** Each class [x]_E is nonempty compact. Fix a compatible bounded metric d and a countable dense sequence (a_i) in K. For every rational r>=0, the set

    {x: distance(a_i,[x]_E)<=r}

is the projection onto K of the compact set {(x,z):x E z and d(a_i,z)<=r}, so is closed. Hence the functions h_i(x)=distance(a_i,[x]_E) are Borel. Encode them by the countable bits 1[h_i(x)<q] for all i and positive rational q, giving a Borel map to 2^omega.

Equal classes plainly give equal codes. Conversely equal codes give equal h_i for every i. Distance to a nonempty closed set is a 1-Lipschitz function; agreement on the dense sequence gives agreement everywhere in K. Its zero set is exactly that closed set, so the two classes agree. Equivalence classes either coincide or are disjoint, and x belongs to its own class, completing the classifier proof. QED.

### Proposition 5 (exact existential reformulation)

For a Borel equivalence relation E on R^omega, the following are equivalent:

(A) Some product of nonempty perfect real sets has smooth restriction of E.
(B) Some product of Cantor real sets has restriction of E whose graph is closed in the square of that product.

**Proof.** Under (A), choose Cantor subsets of all the factors. Restrict the Borel classifier c to this compact product, and apply Lemma 5.2 to find a smaller Cantor product on which c is continuous. The inverse image of the closed equality relation in 2^omega x 2^omega under c x c is exactly the restricted graph of E, proving (B). Conversely, a countable product of compact metrizable spaces is compact metrizable. Apply Lemma 5.3 to the product in (B), whose factors are admissible perfect sets, obtaining (A). QED.

**Exact remaining obligation.** For an arbitrary Borel E reducible to a Polish-group orbit relation, prove that some full Cantor product makes its graph closed, or construct a qualifying E for which every such product fails. The lemmas above do neither. They thin a pre-existing Borel classifier; they do not construct one from arbitrary orbit reducibility. An arbitrary Borel reduction into an action can be made continuous by Lemma 5.2, but the target orbit relation can still have nonclosed graph and nonclosed orbits. Section 1's E0 example exhibits that defect. Section 4 shows why separate closed finite-tail approximations cannot supply the missing uniform conclusion.

## 6. Claim boundary

The retained propositions have complete proofs above, using only elementary topology, Baire category, compactness, and the standard completeness/separability of the classical sequence spaces. The source-exclusion fact for E1 is imported from the explicitly identified Kechris–Louveau theorem. The broader KSZ results are literature context, not proofs supplied by this packet. All examples are source-compatible where stated; E1 and the finite-support translation presentation are explicitly marked non-admissible as counterexamples.

No result asserts a Borel selector with values in the original domain. A classifier and a selector are different requirements. No positive-measure factor, interior, interval factor, all-coordinate equality normal form, arbitrary-function regularity, finite-dimensional replacement, CH, determinacy, or large-cardinal hypothesis is silently added. The finite example checker validates arithmetic and explicit model distinctions only; it cannot certify the infinite fusion or the general unresolved target.
