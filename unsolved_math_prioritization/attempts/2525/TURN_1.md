# Turn 1: exact inverse-cost and exhaustion obstructions

## Target and outcome

We test whether Cayley boundedness (CB) can coexist with an unbounded positive word metric from a genuinely monoid-generating set. The first direction reduces such a witness to an unusually strong subgroup exhaustion and excludes uniformly bounded-order witnesses. These are scoped necessary conditions and sufficient criteria, not a full answer. The uncountable-cofinality argument is explicitly credited to Bergman; the quantitative organization below does not assert novelty.

Let S be a monoid-generating subset of a group G. Adjoin1, harmlessly. Let l(g) be the minimum nonnegative number of S letters in g, B_n={g:l(g)<=n}, and d the diameter for the symmetric generating set S union S^{-1}. For CB groups d is finite for this S. Unless G is trivial we may take d>=1.

## 1. Inverse cost is the exact remaining obstruction

Set R=sup_{s in S} l(s^{-1}). Then

    R <= sup_g l(g) <= d max(1,R),

where the upper bound is asserted when R<infinity. Indeed a symmetric word of length at most d becomes a positive word by replacing each inverse letter with a positive expression of length at most R. The first inequality is immediate. Thus, for this S in a CB group, positive diameter is infinite exactly when the inverse costs of individual generators are unbounded. Large positive costs of arbitrary group elements alone are a less targeted test.

Consequences:
- If all elements of S have finite order at most e, then R<=e-1, hence positive diameter<=d max(1,e-1). No common exponent identity is needed for this statement; only a uniform order bound on the chosen generators.
- Therefore every CB group with uniformly bounded element orders is MB. Every separating S in a periodic CB group must contain elements of unbounded order. In a general CB group, S must either have unbounded finite orders or contain infinite-order elements.
- More generally it is enough that the inverses of S have uniformly bounded positive expressions, including any finitely many exceptional letters. Merely knowing each inverse has some finite expression is exactly monoid generation and gives no uniform conclusion.

## 2. A canonical chain which cannot be finitely supplemented

Put A_n=B_n intersect B_n^{-1}, and H_n=<A_n> as a subgroup. The A_n are symmetric, contain1, increase and exhaust G; hence so do H_n. For a CB group the following are equivalent:

(a) l is bounded on G;
(b) H_n=G for some n;
(c) G=<H_n union F> for some n and some finite F subset G.

(a) implies (b) because sufficiently large A_n=G. If (b) holds, CB applied to the symmetric generating set A_n gives G=A_n^k for some finite k; therefore l(g)<=nk. If (c) holds, every element of the finite set F and its inverse belongs to B_m for some common m>=n. Then H_n and F are both contained in H_m, so H_m=G and (b) applies. This argument makes no assumption that the individual H_n are CB.

It follows that a separating S produces an increasing exhaustion by proper subgroups H_n, **none of which can be supplemented to G by finitely many elements**. In particular each H_n has infinite index: a finite set of right-coset representatives would otherwise supplement it. This sharpens the useful form of the standard countable-cofinality obstruction for a particular witness. The chain may repeat terms, which does not affect the conclusion or exhaustion.

This also recovers Bergman's credited implication CB plus uncountable cofinality => MB: a proper countable exhaustion is then impossible. It does not prove the converse, and a countable exhaustion chosen independently of S need not arise in this form.

## 3. Failure modes checked

The conclusion does not follow from finite symmetric diameter for just the same set S. In the additive group Z take

    S={0,1,2,...} union {-1}.

S generates Z as a monoid and S union (-S)=Z, so its symmetric diameter is1. Its exact positive length is l(n)=1 for n>0, l(0)=0, l(-n)=n for n>0: a sum with k letters is at least -k, and k copies of -1 attain -k. Thus R is infinite. This is not a separating group because the different symmetric generating set {-1,1} has infinite diameter. For this S, A_1 contains1 and-1, and H_1=Z; the failed implication H_1=G => bounded l pinpoints where the **all-generating-set** CB hypothesis was used above.

A proper positive cone which only group-generates G is also insufficient: before measuring finite positive distances one must prove every element has a positive expression.

## 4. Exact finite controls and next gap

The independent-from-symbolic-reasoning checker enumerates every nonempty subset of the nonidentity elements of C2 through C9, D6, D8, C2×C2 and C3×C3. It computes directed BFS lengths and symmetric lengths from the multiplication tables; tests positive/group generation agreement for finite groups; verifies the inverse-cost bound, the bounded-order bound, all symmetric-core subgroup closures and their quantitative diameter bound. These finite controls do not certify any infinite group has CB or produce a counterexample.

The next attempt examines whether finite-index or extension constructions can preserve an unbounded positive witness while making every symmetric generating set bounded. The exact inverse-cost criterion is the invariant to track; no full candidate has been obtained in this turn.
