# Elementary scope and bridge lemmas

These lemmas explain the formulation defect and the precise limit of the counterexample. No priority is claimed. Work in a kappa-saturated o-minimal expansion of a real closed field, with every family and parameter set used below smaller than kappa.

## Lemma 1. A definable decreasing intersection stabilizes

Suppose D_0 contains D_1 contains ... are definable subsets of a definable set X and C = intersection_j D_j is itself definable. Then D_j=C for some j.

Proof. If every D_j\C were nonempty, the partial type consisting of x in D_j for all j and x not in C would be finitely satisfiable, since the family is decreasing. Saturation would realize it, giving a point in their intersection outside C, a contradiction. Because C is contained in each D_j, the eventual equality follows. QED.

Thus constant decreasing sequences are not a technical evasion: any such representation of a definable fiber in a saturated structure has an eventually constant subsequence, in fact an eventually constant tail. A strict-decrease convention would exclude all definable fibers and is not the weak-inclusion convention used here.

In particular, a nonisolated singleton cannot be a countable decreasing intersection of definable open subsets of X. Otherwise one of those open subsets would already be the singleton. This rules out the exceptional fiber of the sphere counterexample under an open-approximant repair.

## Lemma 2. Finite definable quotients and continuity

Let E be a definable equivalence relation on X with finitely many classes C_1,...,C_r. The logic quotient Y=X/E is discrete. The map q:X -> Y is continuous if and only if every C_i is open in X, equivalently every C_i is clopen in X. If X is definably connected and all C_i are nonempty, continuity implies r=1.

Proof. Each C_i is definable using a representative as parameter, and every subset of Y has a finite union of classes as inverse image, hence a definable inverse image. Every subset of Y is therefore logic-closed and logic-open. Continuity is equivalent to openness of the inverse images of the singleton subsets. Since there are only finitely many classes, an open class has open complement when all classes are open. Finally, if r>1, C_1 and its complement would be a partition into nonempty relatively definable open subsets, contradicting definable connectedness. QED.

If the classes have open approximants as in Lemma 1, all classes are open and the same conclusion holds. If instead all classes are topologically closed, their complements are finite unions of closed classes, so they are also open. Neither observation establishes a comparison theorem for infinite quotients.

## Lemma 3. Countable fiber presentations yield countable local bases

Let E be type-definable of bounded index on definable X, and put Y=X/E with its logic topology. Suppose every fiber C_y is the intersection of a decreasing sequence D_(y,j) of definable sets. No openness or contractibility is required. Then Y is first countable.

Proof. First note that q(D) is logic-closed whenever D is definable. To check this directly, write E(x,z) as a small conjunction of formulas e_i(x,z), closing the family under finite conjunction. Then

    q^(-1)(q(D)) = {x : there exists z in D with E(x,z)}
                 = intersection_i {x : there exists z in D with e_i(x,z)}.

For the nontrivial inclusion, fix x in every set on the right and realize the resulting finitely satisfiable small type in z by saturation. This proves type-definability of the inverse image and hence the claim.

Now fix y and set

    U_j = Y \ q(X \ D_(y,j)).

Each U_j is open, contains y, and q^(-1)(U_j) is contained in D_(y,j). Given an open neighborhood V of y, the set T=q^(-1)(Y\V) is type-definable. If every D_(y,j) met T, saturation applied to the decreasing family and the formulas defining T would give a point in C_y intersect T, impossible. Thus some D_(y,j) is contained in q^(-1)(V), which implies U_j is contained in V. Therefore {U_j} is a countable neighborhood base at y. QED.

The closed-image fact used in this proof is also standard in the subject; compare [AB18, Proposition 3.1]. The argument is supplied to make the countable-local-base conclusion checkable.

## What these lemmas do and do not bridge

The literal target has a fully verified two-class counterexample. For a strengthened target, a conservative explicit formulation is:

- M is sufficiently saturated and expands a real closed field;
- X is definable, E is type-definable of bounded index, and Y=X/E has the logic topology;
- Y is locally contractible;
- each fiber is a countable decreasing intersection of definably contractible **open** subsets of X.

Open approximants already force continuity in this setting; [AB18, Proposition 3.4] gives this implication. For the finite-fiber obstruction it follows directly from Lemmas 1-2.

[AB18, Assumption 12.1 and Theorem 12.2] settles the stronger case in which Y is **triangulable**, meaning in that paper a compact space homeomorphic to a finite simplicial complex. The verified theorem is due to Achille and Berarducci. This note does not prove that local contractibility of Y under the remaining hypotheses implies that triangulability condition; Lemma 3 only yields countable local bases, not a global countable base or a triangulation. Nor does this note replace their triangulation/good-cover argument by a comparison construction for arbitrary locally contractible Y.

Accordingly, one must either prove the missing implication, produce a comparison theorem that avoids it, or locate a later primary theorem with exactly the required weaker hypotheses before calling that strengthened target resolved. Adding only continuity while retaining nonopen approximants is a further distinct variant; no equivalence of that variant with the open-approximant version is claimed.

[AB18] Alessandro Achille and Alessandro Berarducci, DOI https://doi.org/10.1007/s00029-018-0413-3 ; accepted postprint https://arpi.unipi.it/retrieve/e0d6c92a-cebc-fcf8-e053-d805fe0aa794/selecta-2nd-revision.pdf .
