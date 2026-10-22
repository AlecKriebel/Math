# Dini spaces and amenable primitive spectra: five scoped approaches

Target: 30002395 / OWR-12591-005. Disposition: **UNSOLVED after 5/5 substantive approaches**. This report contains complete proofs of the stated partial results and failure certificates. It does not prove or refute the universal question, and it makes no novelty claim.

## 1. The exact mathematical target and conventions

The target asks whether every Dini space can occur, up to homeomorphism, as Prim(A) for a separable amenable complex C*-algebra A. The primary source is Kirchberg's contribution to the 2013 Oberwolfach report, printed p. 2456 [OWR]. The complete meaning of Dini used here is:

- X is T0;
- X has a countable base;
- X is sober: each nonempty irreducible closed subset is the closure of a unique point;
- X is locally quasicompact: whenever x belongs to an open V, some quasicompact K satisfies x in int(K) and K contained in V.

Quasicompact means that every open cover has a finite subcover; no Hausdorff property is implicit. Second countability does not mean that X has countably many points. The term "point-complete" in [HK] means sober. Its older use of "spectral" must not be confused with the more restrictive Hochster terminology.

A primitive ideal is the kernel of a nonzero irreducible *-representation. Prim(A) carries the hull-kernel (Jacobson) topology: the closed sets are hulls {P:I contained in P} of closed two-sided ideals I. The corresponding open set is {P:I not contained in P}. This space is not the set of irreducible representations modulo unitary equivalence with an unrelated Borel structure.

Amenable here means amenable as a C*-algebra, equivalently nuclear. We use the standard nuclearity characterization by pointwise norm approximation of the identity through finite-dimensional C*-algebras using completely positive contractions. No unitality or simplicity assumption is imposed. The empty space is allowed and realized by the zero algebra.

For the function formulation, a Dini function is a nonnegative lower-semicontinuous f satisfying

sup_{intersection_m F_m} f = inf_m sup_{F_m} f

for every decreasing sequence of closed sets F_m, with sup(empty)=0. Under the second-countable hypotheses this agrees with the directed-family formulation in [K06]. The positive loci {f>0}, called supports in these papers, form a base for a Dini space. They are not the closed supports of an ordinary continuous function.

### Scope safeguard: sobriety is essential

The short definition sentence on [OWR] p. 2456 omits the word sober although its immediately preceding characterization starts in the sober T0 setting. The rigorous definition in [K06, Definition 1.4 and p. 242], [HK, pp. 2 and 42–43], and the current survey [STW, Section 20] explicitly includes it. This report addresses that established intended problem.

Dropping sobriety would give a spurious easy negative answer: the cofinite topology on a countably infinite set is second countable, T1 and locally quasicompact, but the whole space is irreducible closed and is not the closure of a point. It cannot be Prim(A) for separable A, whose primitive space is sober. This is an excluded definition check, not a counterexample to the actual question.

## 2. Literature status and the precise external theorem

[HK] is a manuscript dated July 10, 2005, uploaded in January 2024. Its topological characterization does not establish that all Dini spaces satisfy the characterization. Section 6 says that the universal question remains open. [STW] v2, revised May 2026, still states it as Problem LXXI(1), alongside the weaker question for arbitrary separable C*-algebras. Its discussion also records equivalence of exact and nuclear realizability. The targeted search and inspected sources found no later universal solution; this is a bounded literature finding, not an exhaustive proof of current nonexistence.

We use the following credited theorem as a dependency, not as something proved here:

**Harnisch–Kirchberg realization criterion.** A sober T0 space X admits a separable nuclear primitive-spectrum realization exactly when there is a locally compact Polish space P and an injective map Psi:O(X)->O(P) preserving top, bottom, arbitrary unions, and arbitrary lattice infima. The latter are interiors of set-theoretic intersections, not bare intersections. Equivalently one has a continuous pseudo-open pseudo-epimorphic map P->X. See [HK, Definition 1.1, Theorem 1.4, Corollary 1.5, Proposition A.11].

For use below: for continuous pi:P->X put R={(p,q):pi(q) belongs to closure{pi(p)}}. Pseudo-openness requires the first projection R->P to be open and the image of each open R-invariant subset to be open in pi(P). Invariant means q in V and (p,q) in R imply p in V. Pseudo-epimorphism means pi(P) meets every nonempty difference of nested open subsets of X, equivalently has dense intersection with every closed subset. These conditions are stronger than simply being continuous with dense image.

Additional standard dependencies are: the equivalence between nuclearity and amenability for C*-algebras; the open-ideal correspondence for Prim; permanence of nuclearity for ideals; the commutative C_0(U) realization for locally compact Hausdorff U; and basic irreducible-representation theory of finite-dimensional algebras. The explicit AF example below checks nuclearity by finite-dimensional factorizations rather than invoking an AF classification theorem.

## 3. Mathematical approach ledger and proofs

The following five sections occur in their actual investigative order. Source recovery, definition checking, literature search, checking computations, and packaging were not counted as mathematical approaches.

# Turn 1: A discrete locally compact cover

Substantive approach: try to supply the locally compact Polish domain in the Harnisch–Kirchberg criterion directly by making the underlying set discrete. The mathematical derivation was carried out first, after source and inherited-attempt checks; this record is its first saved version.

Let X be a countable sober Alexandrov T0 space. "Alexandrov" means that arbitrary intersections of open sets are open. Put P=X with the discrete topology and let pi:P->X be the identity on underlying sets. P is locally compact Polish: the discrete 0/1 metric is complete and the countable underlying set is dense. The map pi is continuous and onto. Its inverse-image map Psi:O(X)->O(P) is injective, preserves arbitrary unions, and preserves arbitrary lattice infima. Indeed both infima are the set-theoretic intersections, since X is Alexandrov and P is discrete. It preserves top and bottom. The Harnisch–Kirchberg realization theorem therefore supplies a separable nuclear C*-algebra with primitive ideal space X. Nuclear is equivalent to amenable here.

A countable Alexandrov T0 space is locally quasicompact. The intersection U_x of all open neighborhoods of x is open. Every open cover of U_x has a member containing x, and this member contains U_x by minimality. Thus U_x is quasicompact; the U_x form a countable base. Sobriety remains a separate assumption. Every finite T0 space is sober: a nonempty irreducible closed set in a finite space has a generic point, since otherwise it would be the finite union of its proper point closures, contradicting irreducibility. Consequently all finite T0 spaces lie in the proved subclass. In fact every second-countable Alexandrov T0 space is countable: each minimal neighborhood U_x must itself be a member of any base, and T0 makes the neighborhoods U_x distinct for distinct x. Hence this covers every Alexandrov Dini space.

The construction has an exact limitation. If pi is any surjection from a discrete space P onto X, its inverse-image map preserves arbitrary lattice infima if and only if X is Alexandrov. For any family (U_i) of opens, preservation says

pi^{-1}(int_X(intersection_i U_i)) = intersection_i pi^{-1}(U_i).

Surjectivity makes this equivalent to int_X(intersection_i U_i)=intersection_i U_i. Requiring this for every family is precisely the Alexandrov property.

For example take X={0} union {1/n:n>=1} with its usual convergent-sequence topology. Let V_m={0} union {1/n:n>=m}. The V_m are open and their intersection is {0}, whose interior is empty. With a discrete domain and identity map, the intersection of the preimages is {0}, whose interior in P is nonempty. This X is compact metrizable and already has the commutative realization C(X); it is the proposed discrete cover that fails.

Outcome: a complete sufficient-condition proof and an exact characterization of this construction's limit. No solution for arbitrary Dini spaces. This is a consequence of a credited realization theorem, with no novelty claim.


# Turn 2: Replace a Polish cover by a locally compact one

Substantive approach: start from an open continuous Polish presentation of a Dini space, then precede it by a locally compact Polish presentation. The missing local compactness looks at first like an auxiliary coding issue. The following argument proves that this generic repair is impossible.

Lemma. If f:Q->P is continuous, open, and onto, Q is locally quasicompact, and P is Hausdorff, then P is locally compact. For p=f(q) choose an open neighborhood V of q inside a quasicompact neighborhood K. Then f(V) is open, contains p, and lies in f(K). The latter is quasicompact by continuity and is compact and closed because P is Hausdorff. Thus p has a compact neighborhood. The same argument works inside any preassigned open neighborhood of p by first restricting to its preimage.

For a T1 target, a continuous pseudo-epimorphic map is surjective: apply density in the closed singleton {p}. A pseudo-open map to a T1 target is open. To see the latter directly, its pseudo-graph is the equivalence relation R={(q,r):f(q)=f(r)}. For open V in Q, the saturation f^{-1}f(V) is pr_1(R intersect (Q times V)), open by the projection condition. It is invariant, so its image f(V) is open in f(Q), by the invariant-image condition. If f is onto, this is open in P.

Take P=N^N with the product of discrete topologies. It is Polish under the usual complete first-disagreement metric. It is not locally compact. Every neighborhood contains a cylinder C fixing finitely many coordinates. Such a cylinder is closed and is covered by the pairwise disjoint cylinders obtained by fixing the next coordinate; there is no finite subcover. If a compact neighborhood K existed, it would contain some such closed cylinder C, making C compact, a contradiction.

Therefore no locally quasicompact Q admits a continuous pseudo-open pseudo-epimorphic map onto N^N. In particular, an arbitrary Polish source cannot be repaired by a preceding locally compact pseudo-open cover. Choosing a universal Polish presentation and then applying this nonexistent repair is invalid.

This does not produce a counterexample to the question: N^N is not itself a Dini space because it is not locally quasicompact. It obstructs only the general two-stage construction. A different locally compact domain mapping directly to a particular Dini X remains possible.

Outcome: exact failure certificate for this route. The underlying obstacle is already noted in Harnisch–Kirchberg Section 6; the proof here reconstructs it rather than claiming new discovery.


# Turn 3: Construct an algebra from the Dini functions

Substantive approach: the Dini functions determine X. Try to turn them into a commutative function algebra, or try to use failure of compact intersections as an obstruction to nuclear realization. An explicit realization shows why both inferences fail.

## The space and its topology

Let X=N disjoint union {a,b}. Each n is isolated. A set containing a or b is open exactly when it contains all but finitely many natural numbers (and it may contain either or both endpoints). Sets contained in N are arbitrary open sets. This is the convergent sequence with two distinct limit points.

X is T1 and second countable. Every point has a quasicompact neighborhood: a tail together with its chosen endpoint is a convergent sequence, and isolated points have singleton neighborhoods. It is sober. Indeed, if a closed irreducible F contains n and some other point, the closed subsets {n} and F minus {n} cover F properly; F minus {n} is closed because {n} is open. Thus an irreducible closed F that meets N is a singleton. If it misses N, it is a nonempty subset of the finite T1 space {a,b}, so irreducibility again forces a singleton. Each singleton is its own generic-point closure. Hence X is a Dini space in the intended sense.

K_a=N union {a} and K_b=N union {b} are compact: an open cover has a member containing the specified endpoint, hence all but finitely many n. Finitely many additional members suffice. Each K is open, and therefore a G_delta. Their intersection N is not compact, as its singleton open cover has no finite subcover. X is not coherent.

## A direct separable nuclear realization

Set

A={ (z_n) in product_n M_2(C) : z_n converges in norm to diag(alpha,beta) for some alpha,beta in C }.

The norm is the supremum norm. This is a closed *-subalgebra of bounded matrix sequences. For m>=0 let A_m consist of sequences that equal their diagonal limit after coordinate m. Then A_m is isomorphic to M_2(C)^m direct-sum C direct-sum C. The inclusion into A_{m+1} copies diag(alpha,beta) into the next matrix coordinate and retains alpha,beta as the new tail coordinates. These are injective *-homomorphisms. The union of A_m is norm dense in A because each convergent sequence can be replaced by its limit after finitely many coordinates. Thus A is separable and AF.

Nuclearity can be checked without a classification theorem: E_m:A->A_m retains the first m entries and replaces the rest by the diagonal limit. E_m is a *-homomorphism, the inclusion A_m->A is a *-homomorphism, and ||E_m(z)-z|| tends to zero for every z. These completely positive contractive factorizations through finite-dimensional algebras establish nuclearity directly.

Let J=c_0(N,M_2), an ideal of A. We have A/J=C direct-sum C. Its two characters give primitive ideals P_a and P_b, the kernels of alpha and beta. Coordinate evaluation at n gives a primitive ideal P_n. There are no others. To prove this, let pi be an irreducible representation. If pi(J)=0, it factors through C direct-sum C. Otherwise some central coordinate projection e_n has pi(e_n) nonzero: if all pi(e_n)=0, density of finite-support matrices in J forces pi(J)=0. Since e_n is central and pi is irreducible, pi(e_n)=1. Thus pi factors through the n-th copy of M_2, and its kernel is P_n.

The bijection X->Prim(A) sending n,a,b to these kernels is a homeomorphism. The basic open support of z is the set of n with z_n nonzero together with a if alpha is nonzero and b if beta is nonzero. Convergence forces the support to contain cofinitely many n whenever an endpoint is present. Conversely every specified open O is such a support. If O is contained in N, choose z_n=2^{-n}1_{M_2} for n in O and zero otherwise. If O contains endpoints, let D be the diagonal matrix with a 1 precisely at each included endpoint, and take z_n=D for n in O, zero otherwise; only finitely many n are omitted. Its limit is D. This proves exactly the stated topology.

## The function-algebra obstruction

Let f=1_{K_a} and g=1_{K_b}. They are lower semicontinuous because K_a and K_b are open. Both are Dini functions under the decreasing-closed-set definition: if closed decreasing F_m all meet K_a, compactness of K_a and the finite intersection property imply that their intersection meets K_a; otherwise one supremum is already zero. The same proof applies to K_b.

Their minimum and product equal h=1_N. Let F_m={a,b} union {n:n>=m}. These are decreasing closed subsets of X, their intersection is {a,b}, and sup_{F_m} h=1 for every m whereas sup_{intersection F_m} h=0. Thus h is not Dini. Also f+g is not Dini: its successive suprema are 2 and its supremum on the intersection is 1.

Outcome: noncoherence does not obstruct even AF realization, and Dini functions cannot generally be treated as an algebra closed under products, sums, or minima. This reconstructs the explicit AF example already supplied by Kirchberg in the 2013 report, with complete spectrum and function calculations; it is not a new counterexample or a solution of the universal question.


# Turn 4: Upgrade monotone lattice data

Substantive approach: exploit the available maps into open-set lattices that preserve arbitrary infima and increasing countable suprema, and try to upgrade them to the complete-lattice embedding needed for realization. The missing finite-join property is a genuine extra condition.

Let X={1,2} be discrete and P={u,v,w} be discrete. Define Psi on the four-element lattice O(X) by

Psi(empty)=empty, Psi({1})={u}, Psi({2})={v}, Psi(X)=P.

This map is injective and preserves top, bottom, and arbitrary infima. For a family of subsets of X, the only nontrivial meet is {1} intersection {2}=empty, and its images also meet in the empty set; top, bottom, repetitions, and empty families cause no exception. Every nonempty upward directed family in the finite lattice O(X) has a largest member: successive upper bounds within the family absorb its finitely many distinct elements. Hence Psi preserves its supremum. In particular it preserves increasing countable suprema.

But Psi({1} union {2})=P, whereas Psi({1}) union Psi({2})={u,v}. Thus these hypotheses do not imply preservation of even binary joins. Nor is Psi an inverse-image map: if some function P->X induced it, the value of w would be either 1 or 2, forcing w into one of the two indicated preimages.

Adding the missing union {u,v} to the image does not repair the map with the same range lattice. The enlarged lattice has five elements rather than four. In this example the enlarged lattice is the open-set lattice of a different three-point T0 space, with opens empty,{u},{v},{u,v},P. Thus simply closing the range under joins can change the space one is trying to realize.

There is an exact upgrade lemma. Suppose X is second countable and Psi:O(X)->O(P) preserves binary unions and increasing countable unions. Then Psi preserves every nonempty union. If it also preserves the empty set, it preserves all unions. For any family (U_i), choose countably many members U_{i_n} with the same union: select one containing each basis element that lies in some U_i. Put W_n=U_{i_1} union ... union U_{i_n}. Then

Psi(union_i U_i)=union_n Psi(W_n)=union_n union_{k<=n} Psi(U_{i_k}).

Monotonicity follows from binary-union preservation, so each Psi(U_i) lies in Psi(union_i U_i); this gives equality with union_i Psi(U_i). Finite and empty families are handled directly. Thus, for an already injective top/bottom and arbitrary-infimum preserving map with increasing-union continuity, binary-union preservation is precisely the additional property sufficient for the required complete-lattice embedding.

Harnisch–Kirchberg Remark 6.2 records a map for every Dini space with the weaker monotone-union conditions. The finite example proves that the stronger join condition is not a formal consequence of those listed axioms. It does not show that a better map cannot exist, since the particular finite X here already has a commutative realization.

Outcome: an exact missing-axiom reduction, plus a finite falsification of the attempted automatic upgrade. No construction of the required binary-join preserving map for arbitrary Dini X was found.


# Turn 5: Glue locally available realizations

Substantive approach: avoid constructing a global witness from scratch by joining locally compact Polish witnesses on open neighborhoods. The complete-lattice criterion gives a full local-to-global theorem.

## Open-cover theorem

Let X be a sober second-countable T0 space with a countable open cover (U_n). Suppose each U_n is homeomorphic to the primitive ideal space of a separable nuclear C*-algebra. For each n, the Harnisch–Kirchberg characterization supplies a locally compact Polish P_n and a top/bottom preserving complete-lattice embedding

Psi_n:O(U_n)->O(P_n).

Let P be the topological disjoint union of the P_n. It is locally compact and Polish. For completeness, choose a compatible complete metric on each P_n, cap it at 1, and put distance 2 between distinct components. This is a complete metric inducing the disjoint-union topology; a union of countably many countable dense sets is countable and dense. Local compactness is componentwise.

For V open in X define Psi(V) by

Psi(V) intersect P_n = Psi_n(V intersect U_n).

The cover ensures injectivity. If V and W differ, take x in their symmetric difference and choose U_n containing x. Their intersections with U_n differ; injectivity of Psi_n then distinguishes their images. Top and bottom are preserved. Arbitrary unions are preserved componentwise.

For arbitrary families (V_i), the crucial identity is

U_n intersect int_X(intersection_i V_i) = int_{U_n}(U_n intersect intersection_i V_i).

One inclusion is immediate. For the other, a relatively open neighborhood in U_n is open in X because U_n is open; if it lies in every V_i it lies in the left-hand interior. Taking this identity through Psi_n proves preservation of arbitrary lattice infima. Interiors and intersections in a disjoint union are also computed componentwise. Therefore Psi is the complete-lattice embedding required by the characterization, and X has a separable nuclear realization.

Conversely, each open subspace of Prim(A) is Prim(I) for the corresponding closed ideal I of A. Ideals of separable nuclear C*-algebras are separable and nuclear. Thus the property is local on open covers among the spaces in question. An arbitrary open cover reduces to a countable subcover by second countability.

## A useful full subclass

Every locally Hausdorff Dini space has a separable nuclear realization. Choose an open Hausdorff neighborhood at each point. Each such open subspace remains second countable and locally quasicompact, hence is locally compact Hausdorff. It has the commutative realization C_0(U); separability follows from second countability and nuclearity from commutativity. Choose a countable subcover and apply the theorem. This includes the non-Hausdorff doubled-limit space from Turn 3.

The empty space is realized by the zero algebra and can be separated off throughout.

## The exact unresolved step

A general Dini space is not assumed locally Hausdorff. Nor do its axioms assert that each point has an open neighborhood with a complete-lattice embedding into the opens of a locally compact Polish space. The proof therefore does not extend to all Dini spaces without a new local-existence argument. It also does not justify gluing closed covers: the displayed interior identity used openness essentially.

Outcome: a complete open-cover permanence theorem and an affirmative result for locally Hausdorff Dini spaces, obtained as consequences of the established characterization. These are credited consequences with no novelty claim. After five substantive approaches, the universal source problem remains unresolved.


## 4. Final dependency and gap audit

1. The Alexandrov result and the open-cover theorem genuinely satisfy every assumption of [HK]; they remain consequences of that deep external theorem. They are not self-contained proofs of [HK] itself.
2. The doubled-limit AF algebra has exactly the asserted primitive ideals. Its topology, quasicompactness, sobriety, noncoherence, and failure of Dini-function algebra operations are all proved above. This example was already in Kirchberg's papers, and is explicitly credited.
3. The Baire-space obstruction applies to the auxiliary Polish source. Baire space is not Dini and is never offered as a counterexample to the universal target.
4. The weak lattice map supplies a counterexample only to a purported implication between axioms. Its target space has a realization. The failure of this particular map does not show that all maps fail.
5. Open-cover gluing uses an actual open cover and existing local witnesses. It does not prove that arbitrary Dini spaces have such local witnesses, or that closed-set decomposition gives the same result.
6. The residual target is unchanged: for an arbitrary sober second-countable locally quasicompact T0 space, construct the complete-lattice embedding into O(P) for some locally compact Polish P, or prove that no such embedding exists for an explicit space. No such universal construction or explicit nonrealizable Dini space was obtained.

The finite controls in check_controls.py exhaust labeled finite T0 orders on up to four points and check lattice, generic-point, open-cover, missing-join, and finite-dimensional connecting-map identities. They are sanity checks only. Their large assertion count reflects elementary exhaustive enumeration; it is not a proof of any infinite theorem. No proof assistant, independent reviewer, or human peer review is claimed in this author packet.

## 5. References

[OWR] Eberhard Kirchberg, "C*-correspondences related to Dini spaces," in *C*-Algebren*, Oberwolfach Reports 10 (2013), pp. 2423–2500, contribution p. 2456. Published 2014. https://doi.org/10.4171/OWR/2013/43 . Publisher page: https://ems.press/journals/owr/articles/12591 .

[HK] Hergen Harnisch and Eberhard Kirchberg, *The inverse problem for primitive ideal spaces*, manuscript dated July 10, 2005; arXiv:2401.05917v1, posted January 11, 2024. https://arxiv.org/abs/2401.05917v1 .

[STW] Christopher Schafhauser, Aaron Tikuisis and Stuart White, *Nuclear C*-algebras: 99 problems*, arXiv:2506.10902v2, revised May 8, 2026. Section 20, printed pp. 64–65, Problem LXXI. https://arxiv.org/abs/2506.10902v2 .

[K06] Eberhard Kirchberg, *The range of generalized Gelfand transforms on C*-algebras*, Journal of Operator Theory 55:2 (2006), 239–251. Definitions 1.1, 1.3–1.4; Question 1.6; the matrix-sequence example on p. 241. https://jot.theta.ro/jot/archive/2006-055-002/2006-055-002-002.pdf .
