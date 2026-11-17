# Checkable interface derivations

These deductions supplement the complete consumed upstream argument recorded in WORKING_PROOF_CHECKS.md. They do not use another current review family's findings. All groups below are discrete. The target is the actual original note, not a stronger claim about arbitrary abstract overgroups or full group C*-algebras.

## Nonempty finite left Følner sets

The upstream proof uses this precise direction: an amenable group has, for every finite S and ε>0, a nonempty finite A with |sA△A|<ε|A| for all s∈S. Nonemptiness is indispensable; the empty set cannot be used in a ratio. Moore's published Theorem 1.2 states the finite-boundary criterion with a sum over the fixed generators and its footnote specifies the left convention. The following standard separation/coarea argument checks the needed convention directly rather than relying on an omitted word in a printed criterion.

Let M be a positive normalized left-invariant mean on bounded real functions. Consider the convex set of tuples ((s·f−f))_(s∈S) in the finite direct sum of ℓ¹(G), where f ranges over finitely supported probability functions and (s·f)(x)=f(s⁻¹x). If zero were outside its norm closure, Hahn–Banach separation would give bounded real φ_s and c>0 such that

    ∑_(s∈S) ∑_x φ_s(x)[f(s⁻¹x)−f(x)] ≥ c

for every such f. In particular, setting f=δ_g gives ∑_s[φ_s(sg)−φ_s(g)]≥c for every g. Applying M gives 0≥c, a contradiction. Thus choose a finitely supported probability f with ∑_s||s·f−f||₁<ε. Set A_t={x:f(x)>t}. The finite layer-cake identities give

    ∫₀∞ |A_t| dt=1,
    ∫₀∞ ∑_s|sA_t△A_t| dt=∑_s||s·f−f||₁<ε.

Consequently some t has A_t nonempty and ∑_s|sA_t△A_t|<ε|A_t|. Each individual boundary is no larger than the sum. This checks exactly the finite cancellation input used by the pinned proof. Hahn–Banach is an accepted classical foundation here, not a newly claimed theorem.

## Standard interval F, line F and the full circle action

Define an increasing piecewise-affine φ:ℝ→(0,1) by

    φ(n)=2^(n−1)                      (integer n≤0),
    φ(n)=1−2^(−n−1)                  (integer n≥0),

and extend affinely on each [n,n+1]. Both formulas give φ(0)=1/2. The slopes on these intervals are powers of two; every integer has dyadic image; inverse charts have the same dyadic property. The breaks are locally finite on ℝ.

Conjugating a standard interval f∈F by φ gives a line homeomorphism h=φ⁻¹fφ. Near zero f(x)=2^k x, so h(t)=t+k on a sufficiently negative ray, using φ(t+k)=2^kφ(t) there. Near one f(x)=1−2^l(1−x), so h(t)=t−l on a sufficiently positive ray. On the remaining compact interval it has finitely many dyadic linear pieces with slopes powers of two. Conversely a dyadic PL line homeomorphism eventually equal to integer translations conjugates to a finite-piece element of standard interval F: the infinitely many tail cells collapse to the two endpoint-linear pieces. Thus this is the precise standard line model needed in LMB Theorem 4.3, Brin and BCR; it is not an arbitrary abstract copy.

Every homeomorphism of ℝ is monotone, increasing or decreasing. Conjugate it by φ and extend to [0,1] using the appropriate one-sided limits. An increasing element fixes both endpoints; a decreasing one interchanges them. Identifying the endpoints gives a circle homeomorphism in either case. This construction is a faithful homomorphism Homeo(ℝ)→Homeo(S¹); faithfulness follows by restricting to the open interval. The line F above maps onto the specified standard circle F. Therefore a countable line overgroup, including orientation-reversing elements, falls under the countable circle statement.

The reflection r(t)=−t normalizes line F: it exchanges the two tails, changes the signs of their integer translations and preserves dyadic PL structure. Hence it supplies the reversing automorphism explicitly. Brin's normalizer is in full Homeo(ℝ), not only its increasing subgroup; BCR likewise includes decreasing realizers and explicitly displays the positive subgroup of index two. Published LMB's adjacent positive-slope PL notation and missing minus in a tail threshold must not silently shrink the full groups in Corollary 4.4. The full line-homeomorphism formulation and these primary realizations resolve the notation without changing a source.

## Local rigid stabilizers and the hypotheses actually used

For any nonempty open U⊂S¹ choose a closed dyadic interval [a,b] lying in U and avoiding the identified endpoint. Rescaling [0,1] affinely to [a,b] conjugates F to a group supported in [a,b]; slopes of each rescaled element are unchanged and its breakpoints remain dyadic. Extending by identity outside [a,b] gives elements of the actual standard circle F. This is the local copy used by CFP Lemma 4.4 and LMB Theorem 4.1.

Once F is nonamenable, the rigid stabilizer G_U contains a nonamenable subgroup for every such U. Amenability passes to subgroups, so G_U is nonamenable. The action is faithful because G is a subgroup of Homeo(S¹). The space is Hausdorff. LMB Theorem 3.7 requires countability and these rigid-stabilizer hypotheses; it does not demand minimality. In particular, the fixed point of standard F on the circle is not a counterexample to the criterion. This is not an assertion that arbitrary abstract overgroups of F are C*-simple.

## Countability, full Aut(F) and full Comm(F)

Finite lists of dyadic breakpoints, dyadic values and integer exponents show F and T are countable. The actual CFP normal-form argument and Corollary 2.6 give a two-element generating set for F. An endomorphism, hence an automorphism, is determined by the two generator images, giving countable Aut(F).

For any fixed n, a subgroup H of index n yields a transitive homomorphism F→S_n and a chosen point stabilizer. A finite generating set has only finitely many possible images in S_n, so there are finitely many index-n subgroups. Schreier's rewriting gives each H a finite generating set (at most n(d−1)+1 generators from a transversal when F has d generators). There are therefore countably many finite-index subgroups in total and countably many homomorphisms between each ordered pair. The set of finite-index isomorphisms is countable; quotienting it by agreement on a further finite-index subgroup cannot increase cardinality. Thus full Comm(F) is countable, including its reversing coset.

Brin's Theorem 1(i) identifies full Aut(F) with the normalizer in full Homeo(ℝ), using the stated reconstruction theorem after checking its dynamical hypotheses. BCR's Theorem 3.1 identifies full Comm(F) with its subgroup of monotone line realizers; uniqueness in reconstruction makes the realization well defined after restricting an isomorphism and makes it faithful. Multiplication can be expressed with either conjugation convention provided the inverse is changed consistently. We use hfh⁻¹; no conclusion depends on mixing the two conventions. These groups contain standard line F (inner conjugations in the automorphism case), so the previous circle derivation applies.

For the reverse equivalences, F is centerless: if a nonidentity commuting homeomorphism moves a small interval to a disjoint one, a nontrivial F element supported in the first interval would have a disjoint-support conjugate, contradicting commutation. Thus Inn(F)≅F is normal in Aut(F). For Comm(F), the actual BCR 2013 addendum Theorem 1 gives

    F′ ◁ K ◁ Comm⁺(F) ◁ Comm(F).

BKKO's normal-subgroup inheritance of C*-simplicity can be applied repeatedly along this subnormal chain. Nontrivial amenable groups cannot be C*-simple: amenability weakly contains the trivial representation in the regular one, giving a noninjective augmentation quotient of the reduced algebra. Consequently simplicity of either full automorphism/commensurator reduced algebra forces F, or its nontrivial subgroup F′, to be nonamenable. No inheritance to arbitrary subgroups is asserted.

## HO reverse implication and unconditional trace attribution

For T acting on the dyadic points modulo one, the stabilizer of zero is F. If F were amenable, the associated quasi-regular permutation representation π on ℓ²(T/F) would be weakly contained in λ_T, yielding a unital quotient from C*_r(T). Choose the nontrivial commuting a,b with disjoint supports used in HO. For every dyadic point the unordered pair of its a- and b-images equals that of its ab- and identity-images. Hence π(a+b−ab−e)=0. The four distinct group elements are linearly independent in the regular representation, so λ_T(a+b−ab−e)≠0. This makes the quotient kernel nonzero and proper. Thus C*-simplicity of T implies F is nonamenable. This is the published HO Theorem 5.5 (arXiv v1 Theorem 4.5), not a new reverse reduction.

HO's following discussion explicitly records the already unconditional unique trace of T and credits Dudko–Medynets. The note correctly separates it from consequences requiring the new input. Published Remark 5.6 (arXiv Remark 4.6) records the equivalence between nonamenability of F and unique trace for F. The final journal edition states weak containment correctly; an earlier edition's abbreviated wording should not be read as literal subrepresentation containment.

## Reduced versus full algebras; action-level negative control

For any nontrivial G, the universal unitaries u_g in C*(G) have an augmentation character ε(u_g)=1. For g≠e, u_g−1 has nonzero regular image λ_g−1, so it is a nonzero element in ker ε. The kernel is proper. The trace τ_r pulled back from C*_r(G) differs from ε on u_g, where its value is zero. Thus full C*(G) is neither simple nor uniquely tracial. This does not contradict any target conclusion, which is explicitly reduced.

An abstract overgroup F×C₂ is a useful negative control: it contains a copy of F but has a nontrivial finite amenable normal subgroup and cannot be C*-simple or reduced uniquely tracial by BKKO. It cannot contain standard circle F through a faithful action with that F-factor realized in its specified action, since the extra central involution would have to centralize every local F element; moving a small arc to a disjoint one contradicts local support. This confirms why the actual geometric containment hypothesis is indispensable.

## Trace conclusion and the exact algebraic scope

For each of F,T,Aut(F),Comm(F), and for each specified countable circle overgroup separately, the checked LMB route gives C*-simplicity. BKKO then gives trivial amenable radical. Its actual trace theorem says every tracial state vanishes at λ_g outside that radical. If the radical is trivial, all tracial states have value δ_(g,e) on every λ_g. By linearity and norm continuity, the dense group algebra determines the unique state to be the canonical trace. Simplicity and uniqueness of trace for arbitrary non-group C*-algebras are not inferred.
