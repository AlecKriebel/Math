# Independent adversarial audit: class-space and extension reductions

Checkpoint: **2026-10-24T17:21:32Z**. Reviewer: an independent AI subagent that did not author `../root_class_space.md` or `constructions_solvable_review.md`. Audit completion estimate: **100% for the restricted claims examined here**. The parent note's unrestricted discovery estimate is 10%; this review does not increase that estimate to a solved status.

Read the governing AGENTS instructions. No external individuals were contacted, and no Git, publication, tracker, queue, or unrelated PR operation was performed.

## Verdict and scope

**PASS:** the countably based quotient reduction, Polish infinite-order class space, relative isolated-class deduction, and procyclic normalizer openness condition are correct as stated. No continuum hypothesis or finite-generation hypothesis has entered them.

**PASS:** if A is a closed normal abelian subgroup of a profinite G, G/A is torsion, and G has fewer than continuum conjugacy classes of infinite-order elements, then G is torsion. The finite-derived-length soluble corollary follows. The alternative proof below removes even the proposed use of Wilson's finite-prime lemma.

**PASS after an additional independent check:** the stronger extension principle for a closed normal **abstract locally nilpotent** kernel in `constructions_solvable_review.md` is correct. This must not be substituted for pronilpotence or for local nilpotence only in a dense subgroup.

**PASS:** the additional category deductions communicated by the parent are valid. None proves that the set of infinite-order elements is empty. No result in this review resolves unrestricted 21.136, establishes originality, or licenses publication as a complete solution.

## 1. Countably based quotient preserving the actual counterexample

For an infinite-order x, its orders in the finite continuous quotients are unbounded. A common bound M would imply x raised to lcm(1,...,M) is trivial in every finite quotient, hence in G. Choose open normal U_i with the order of xU_i greater than i, set N_i equal to the first i intersections, and N equal to their intersection.

The natural map G to the inverse limit of G/N_i is onto: the closed cosets specifying any coherent point have the finite intersection property, so compactness gives a common lift. Its kernel is N. The resulting quotient is countably based and compact metrizable, and the image of x retains unbounded finite quotient orders.

The infinite-order class bound passes to every continuous quotient. More precisely, restrict the original class set to those classes whose image has infinite order. Mapping their images to quotient classes is well defined and surjective. This handles the fact that some infinite-order elements can become torsion in a quotient. There is no claim that the bound passes to an arbitrary closed subgroup.

## 2. Orbit metric and Polish infinite-order classes

A countably based profinite group admits a compatible bi-invariant ultrametric from a descending sequence of open normal subgroups with trivial intersection. Conjugation acts isometrically. The minimum orbit distance

    delta([x],[y]) = min_g d(x,g^-1 y g)

exists by compactness. Conjugation invariance makes it representative independent and symmetric; composition of conjugators proves the triangle inequality. A zero minimum means two representatives actually coincide after conjugation. Thus this is a metric, not merely a pseudometric. The quotient projection is continuous because delta([x],[y]) <= d(x,y). Compactness then identifies the metric topology with the quotient topology.

For each positive n the torsion set E_n={g:g^n=1} is compact and conjugacy invariant. Its image in the compact metric class space is closed. The infinite-order class space J is the complement of the countable union of these closed images, and is therefore G_delta and Polish.

The perfect-set theorem applies to J itself. An uncountable Polish space contains a Cantor set and hence at least continuum points; a separable metric space has at most continuum points. Therefore the strict continuum bound makes J countable. This argument works equally in models where there are uncountable cardinals strictly below the continuum; it does not replace a strict cardinal bound by countability without proof.

A nonempty countable Polish space has an isolated point by Baire: otherwise its closed singleton sets would give a countable union of nowhere dense sets. Pulling a relative neighborhood of that point back to G gives an open set U in which every infinite-order element belongs to that one ambient conjugacy class. A clopen coset can be chosen inside U. This is relative openness among infinite-order elements, not openness of the class in G.

## 3. Arbitrary procyclic groups and normalizer images

Write a procyclic group C as the product of its characteristic cyclic p-primary factors, of order p^e(p), with e(p) a positive integer or infinity. Its continuous automorphism group is the product of the unit groups of Z/p^e(p)Z, using Z_p for an infinite exponent. The topological generators of C are precisely the product of the local generator sets. These form a closed, hence compact, subset of C: local generation is the closed condition of being a unit. Evaluation at one generator identifies this set homeomorphically with Aut(C).

The normalizer N_G(C) is closed, and evaluation shows that its action image H in Aut(C) is compact and closed. Two generators of C can be G-conjugate only through a conjugator normalizing C, since they generate the same closed subgroup. Conversely every action in H effects precisely such a conjugacy. The class count on the generators is exactly [Aut(C):H].

Aut(C) is abelian and profinite. If the closed subgroup H had infinite index, Aut(C)/H would be an infinite profinite group. Such a group has at least continuum points: it has no isolated points, and successive binary clopen splittings give distinct points along all infinite binary branches by compactness. This construction requires neither metrizability nor CH. Thus H has finite index and is open.

For C=Z_p an open image contains a principal unit subgroup, giving the parent's displayed power-conjugation relation. The general argument never assumes an ordinary integer greater than 1 is a unit simultaneously at every prime. For example, C with all primes in its order requires the full product unit ring, not arbitrary integer powers.

## 4. The abelian normal kernel lemma

First the requested Wilson-based argument passes. [Wilson's published paper](https://api.repository.cam.ac.uk/server/api/core/bitstreams/6d58eaf2-5e39-415a-a1db-83a5ce3921cf/content), Lemma 4.2, imposes no finite-generation hypothesis and yields a finite set of primes under the strict class bound. An infinite-order element of closed abelian A then has a Z_p factor in its procyclic closure. For C equal to that factor, each g normalizing C has some power g^m in A. Therefore its action u in Z_p^times satisfies u^m=1. Torsion in this unit group is finite, including order 2 rather than p-1 at p=2. Thus the normalizer image is finite, contradicting its required openness in the infinite group Z_p^times. If A is torsion, the torsion quotient already makes G torsion element by element.

Here is an independent simplification that does not need the finite-prime result. Suppose A contains any infinite-order x and let C be its procyclic closure. The same g^m argument makes the normalizer image H a torsion group. The class bound makes H open by Section 3. It follows that all of Aut(C) is torsion, since every automorphism has a positive power in the finite-index subgroup H. But Aut(C) contains an infinite-order element whenever C is infinite:

* If some p-primary factor of C is Z_p, use multiplication by 1+p there (or 5 when p=2) and the identity on every other factor. This is a product unit; it is not an assertion about that integer being a unit globally.
* Otherwise infinitely many distinct primes occur, each with finite positive exponent. At each such odd p choose a unit whose residue in F_p^times has order p-1. The product automorphism has finite-coordinate orders at least p-1, which are unbounded, so it has infinite order.

This contradiction makes A torsion. For each g in G, a power g^m lies in A and a further positive power is trivial, so G is torsion. No uniform exponent is claimed.

Induction on a finite series of closed G-normal subgroups with abelian factors gives the finite-derived-length soluble conclusion. The quotient at each step inherits the original class bound. The derived series supplies characteristic closed subgroups, so the normality needed for the quotient induction is available. Arbitrary prosoluble groups need not have such a finite series.

## 5. Independent check of the stronger locally nilpotent extension

The proof in `constructions_solvable_review.md` handles the genuine extra obstruction correctly. If C has a Z_p factor, use that factor's generator x. For a conjugator g preserving this factor, choose m with h=g^m in A. Abstract local nilpotence makes the two-generator abstract subgroup generated by x,h nilpotent of some finite class c. The iterated commutator identity gives

    [x,h,...,h] = x^((u^m-1)^c) = 1.

The exponent lies in Z_p, an integral domain, so u^m=1 and the finite fusion argument applies.

If all Sylow factors of C are finite and infinitely many primes occur, the same identity holds in the product exponent ring. One cannot conclude u^m=1 there because finite p-primary rings contain nilpotents. Reducing each coordinate modulo p does give residue units of order dividing the same integer m. The residue image K of H is consequently torsion, compact, and abelian.

Such a compact abelian torsion group has bounded exponent: it is the union of its closed n!-torsion subgroups, one of which is open by Baire; its finite quotient then provides a global exponent bound. The full product of F_p^times for infinitely many distinct primes has unbounded exponent. It follows that its quotient by K is infinite profinite and has at least continuum points. The induced surjection from Aut(C)/H onto that quotient proves the required continuum ambient class bound. This argument is valid at arbitrary cardinality and does not depend on Wilson's finite-prime lemma.

The nilpotency assumption concerns the actual abstract subgroup generated by x and h. Pronilpotence alone does not supply a finite class c. The proposed proof explicitly respects this distinction. Its finite-series extension should be stated for closed G-normal terms, rather than an unspecified arbitrary subnormal series whose intermediate subgroups may fail to inherit the bound.

## 6. Additional category deductions

An infinite-order conjugacy class has empty interior in any profinite group. Indeed, suppose a coset Nx lies in x^G for an open normal N. For every open normal L contained in N, its finite quotient image has at least [N:L] elements all in the class of xL. The finite class formula bounds

    |C_(G/L)(xL)| <= [G:N].

The image of the closed centralizer C_G(x) satisfies the same bound in every such quotient. Thus C_G(x) is finite, contradicting its containment of the infinite procyclic closure of x. Any nonempty interior of a conjugacy class provides a coset of this type, after choosing a point in that interior. Compactness makes classes closed, so infinite-order classes are nowhere dense.

In the countably based strict-class-bound reduction there are countably many such classes. Hence the infinite-order element set I is meagre, and the torsion element set T is comeagre. T is also F_sigma, being the union of the E_n. This does not say that I is empty.

Every nonempty clopen coset U is a Baire space. If every E_n intersection U had empty relative interior, their union T intersection U would be meagre in U, contradicting its comeagreness. Therefore some E_n contains a nonempty open subset of U. It follows that the union of the interiors of the E_n is dense and open. No classification of finite simple groups, Sylow argument, or finite-generation result is used in this deduction.

Conversely, if the interior of T is dense, each open set contains a compact open torsion coset. Baire applied inside that coset again produces an E_n with nonempty interior there. Thus density of the interior of T is equivalent to density of the union of the interiors of E_n. This is a necessary category condition, not a torsion theorem.

## 7. Exact remaining obstruction and validation limits

None of these arguments forces an arbitrary profinite group to have an abelian or abstract locally nilpotent closed normal kernel with torsion quotient, or a finite normal series of such kernels. None excludes a meagre nonempty G_delta set of infinite-order elements whose classes are isolated only relative to that set. The arguments do not pass the ambient class bound to arbitrary finitely generated closed subgroups, so Wilson's finite-generation theorem cannot simply finish the proof.

All claimed deductions above have explicit proofs. No computation was used as evidence for an infinite statement. The review is an AI mathematical audit, not human peer review, formal proof verification, or an extensive priority audit. Unrestricted 21.136 remains **unsolved by this work**.
