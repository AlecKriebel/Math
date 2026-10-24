# FC-centre, finite-width and marginal routes for21.122

UTC: 2026-10-24T23:27:04.497453+00:00. Supporting deductions and failed-route countermodels only. **No solution or originality claim.** Discovery estimate toward full21.122 **2%**. These notes use none of the other current original approach families' mathematics.

Write X=G_w, K=w(G) for the closed verbal subgroup, Y=X∪X^-1∪{1}, and D=<X>_abstract=union_(n>=0)Y^n. The exact target concerns X, not K.

## 1. What finite width would give, and the exact missing step

Assume |X|<continuum. Then |D|<=max(aleph0,|X|)<continuum. If D is closed in G, it is a profinite group. Every infinite profinite group has cardinality at least continuum, so D must be finite. In particular X and K are finite.

Here closedness of D is equivalent to finite width of w in G. One direction is immediate: D=Y^m is compact, hence closed, for a finite width bound m. Conversely, if D is closed, then it is compact and is the countable union of closed subsets Y^n. By Baire some Y^n has interior in D. Translate an interior point g∈Y^n back to1; an identity neighbourhood in D is contained in Y^(2n). Choose an open subgroup U of D inside it. Finitely many cosets d_jU cover D, and each d_j belongs to some finite power of Y. Taking the maximum of those finitely many lengths gives a finite global width bound.

Equivalently, a uniform bound m on the word widths in **all finite quotients of G** would give K=Y^m by compactness: every element of K belongs to Y^m modulo every open normal subgroup; since Y^m is closed, it belongs to Y^m in G. Under the small-image hypothesis K would then be finite.

Thus a genuine counterexample must have an abstract verbal subgroup that is proper dense and nonclosed in K, and must have unbounded word widths in its finite quotients. The word-value cardinalities in those finite quotients must also be unbounded. One can choose a descending countable chain of open normal subgroups along which both bounds grow, by intersecting successive finite separating quotients. This is only a necessary shape, not a construction of a counterexample.

**Gap.** No arbitrary-word finite-width theorem applies under the present hypotheses. Assuming D closed merely reinstates the main missing conclusion through a stronger condition. DKS1907.01344v2 Corollary4.2 explicitly retains pro-p verbal subgroup and local finite-width assumptions; it does not provide the missing width bound in general. This route is blocked at that unsupported width assertion, absent a new mechanism.

## 2. Marginality reformulates the set target exactly

The closed marginal subgroup w*(G) consists of elements n such that inserting n on either side of any one input of w leaves every value unchanged. The following equivalence is elementary for profinite G:

    X finite  <=>  w*(G) is open.                    (1)

For the reverse implication, an open marginal subgroup makes the word map factor through the finite set of its coset tuples. For the forward implication, a continuous map from compact G^k into its finite image is uniformly locally constant. More explicitly, each tuple has a product coset neighbourhood contained in its value fibre. Take a finite cover by such product neighbourhoods and intersect their open normal subgroups to obtain N normal open in G. Every coordinatewise N-perturbation of any tuple remains in a covering fibre, so N<=w*(G). Normality converts right insertions to left insertions as well.

The small-image topological lemma supplies constancy on **one** nonempty product coset box. It does not supply uniform constancy on every box, hence does not prove openness in(1). The exact missing structural assertion is propagation of this local coset identity to one global open marginal subgroup. The dense-equationally-Noetherian theorem of de las Heras–Zozaya2502.07427 obtains precisely such a marginal subgroup using its irreducible component; that hypothesis is not available for arbitrary G.

## 3. A compact small normal FC-set need not have finite commutator closure

Let P=product_(n>=1)S3. Let X0 consist of1 and all elements supported at exactly one coordinate, where that coordinate is a transposition. Then:

* X0 is countable and compact: all but finitely many of its points lie in every identity neighbourhood, and its other points are isolated.
* X0 is invariant under conjugation by P; every element has a finite conjugacy class and a finite normal closure, of order at most6.
* Its abstract subgroup is the restricted direct sum of the S3 factors. Its closed generated subgroup is all of P.
* [P,P]=product_(n>=1)A3 is infinite.

Indeed, a nontrivial element of S3 is noncentral. An element of P with infinitely many nonidentity coordinates has continuum many independent coordinatewise conjugates. Thus FC(P) is exactly the restricted direct sum, and P has dense FC-centre despite its infinite derived group.

This disproves the abstract shortcut

    compact small conjugacy-invariant FC-set
       => finite [closed generated subgroup,ambient group].

It is **not** a word-value counterexample. For any fixed word v, the value set in P is the product of the identical finite value sets v(S3). Such a product is either a singleton or has cardinality continuum. Thus X0 cannot be a word-value set. The missing word-map structure matters and cannot be replaced by the FC property of values alone.

## 4. Finite iterated verbal subgroup alone does not settle the set

Let Q=product_(n>=1)D8, where D8=<r,s|r^4=s²=1,srs=r^-1>. For w=x², the value set is the whole central elementary abelian subgroup

    Q_w=product_(n>=1){1,r²}.

Consequently K=w(Q)=Q_w is infinite, but w(K)=1. The same example works for w=[x,y]: every coordinate commutator belongs to {1,r²}, both possibilities occur, and all combinations occur independently. Then K is central and w(K)=1 as well.

These examples have continuum many values. They do not refute21.122, but they show exactly why the unconditional structural output w(w(G)) finite, even combined with centrality of w(G), cannot by itself replace the small-image argument. The actual small-image hypothesis still has to be used to make the original value set finite.

## 5. Remaining central-valued route

`CENTRAL_NONPOLYNOMIAL.md`, now independently reviewed, gives a separate pro-3 solvable-length-three example where δ2 is central-valued but nonpolynomial of every finite Passi degree. Its value set is exactly9Z3. This closes only the **unconditional** extension of the metabelian central-polynomial theorem. A theorem using centrality **and the small-image hypothesis** might still exist; that statement is not contradicted by the example and must not be marked false.

A general finite-central-quotient route would require proving [w(G),G] finite from the exact word-value hypothesis, then establishing the set dichotomy for arbitrary central-valued words without deleting the small-image assumption. Neither step has been proved here. Zozaya2608.02237v1 Proposition3.2 proves the first only in metabelian groups, and Theorem4.4 proves polynomiality there. The compact FC-set example prevents deriving the first step from compactness/FC-generation alone; the Heisenberg-by-Z3 example prevents deriving the second from unconditional polynomiality alone.

No statement in these notes gives a complete affirmative or negative resolution of21.122. No paper, publication or priority claim is warranted.
