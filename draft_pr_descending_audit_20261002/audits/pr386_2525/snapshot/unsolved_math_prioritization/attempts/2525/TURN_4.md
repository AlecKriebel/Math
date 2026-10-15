# Turn 4: normal-generation and inverse-producing symmetries

## Direction and outcome

We test two natural ways to obtain CB examples: simple or finitely normally generated groups, and constructions which make inverses accessible by conjugation. These yield substantive exclusions for proposed witnesses. Neither argument supplies uniform control for an arbitrary positive generating set, and the original remains unresolved.

## 1. Conjugacy-invariant witnesses in finitely normally generated CB groups

Assume G is CB and a finite set F normally generates G. Its symmetric conjugacy saturation

    U={h f h^{-1},h f^{-1}h^{-1}:h in G,f in F}

is a group-generating set, so CB gives G=(U union {1})^b for some finite b. Now let S be a **conjugation-invariant** monoid-generating set. Its positive length satisfies

    l(h g h^{-1})=l(g),                         (1)

because conjugating a shortest positive word gives an S word of the same length, and conjugating back proves equality. Let C=max_{f in F}(l(f),l(f^{-1})), finite by positive generation. Every U letter has positive cost at most C, hence

    sup_G l <= b C.                            (2)

Thus any conjugation-invariant monoid-generating set has bounded positive diameter in a finitely normally generated CB group. In particular this applies to every nontrivial simple CB group, by taking F={f} for any nonidentity f. Finite normal generation is an explicit hypothesis; it has not been proved for every CB group here.

The same proof requires less than full invariance: it suffices that the positive costs of all conjugates of the finitely many f and f^{-1} are uniformly bounded. A useful verifiable condition is

    l(h s h^{-1})<=K for every h in G and s in S. (3)

Then conjugating fixed positive expressions for F and F^{-1} shows all U letters have cost at most KC, yielding diameter<=bKC. For the trivial group the conclusion is immediate; otherwise K may be taken at least1.

Consequently a separating witness in a finitely normally generated CB group has unbounded conjugacy distortion: for every finite normally generating F, at least one of the families of conjugates of F union F^{-1} has unbounded positive cost. In particular the saturation of S by all conjugates can have bounded positive diameter even when S itself does not. It is invalid to replace S by that saturation and infer its original positive metric was bounded.

## 2. Uniform finite-conjugator inverse relations rule out a witness

Let S monoid-generate a CB group and let d be its symmetric diameter. Suppose a fixed finite F subset G and integer k have the following property: for every s in S there are m<=k and f_1,...,f_m in F such that

    s^{-1}=(f_1 s f_1^{-1})...(f_m s f_m^{-1}).  (4)

Set C=max_{f in F} max(l(f),l(f^{-1})), taking C=0 when F is empty. Each conjugate in(4) costs at most2C+1. Hence R<=k(2C+1) and turn1 gives

    sup_G l <= d max(1,k(2C+1)).                (5)

More generally the relation can use at most k positive S letters, not necessarily the same s, with the same finite list of conjugators. The same bound holds by direct substitution. A fixed finite list of exceptional generators also causes no problem because their inverse costs have a finite maximum.

Special cases include bounded-order generators (use f=1 and m=order(s)-1), or a finite list of symmetries which conjugates every generator to its inverse. This explains a construction hazard: imposing uniformly short inverse-producing relations using a **fixed finite** supply of stable letters destroys the required inverse-cost divergence. An infinite supply of conjugators, or lengths growing with the generator, is not covered. CB of G alone does not bound their positive costs.

The relation may hold with conjugators depending on s, but all must lie in the fixed finite F for this conclusion. Generalized torsion with no common relation-length or conjugator-cost bound does not suffice.

## 3. Why normal-generation width does not finish the target

For arbitrary S the quantity l(h f h^{-1}) can grow with h, even though l(f) is fixed. The elementary upper bound

    l(h f h^{-1})<=l(h)+l(f)+l(h^{-1})

is circular for a proposed unbounded witness. Bounded normal generation controls the number of conjugate factors, but not the positive cost of their conjugators. Equation(2) cannot be used without(1) or another uniform bound. Similarly a normal closure statement is weaker than a bounded-width statement until CB is applied to its actual generating set.

This direction therefore excludes normal or uniformly conjugation-controlled witnesses in the stated group class. It leaves open highly non-normal positive sets with unbounded inverse costs, including possible countable-cofinality constructions.

## 4. Exact controls

The checker constructs S3,S4,A4 and A5 as permutation groups, computes their full conjugacy classes, enumerates every nonempty conjugacy-invariant subset of nonidentity classes and every finite set of class representatives used for normal generation. It checks exact conjugacy invariance of positive lengths and the bound bC for all applicable pairs. It additionally tests the generalized conjugacy-cost bound for all generating subsets of D8. Every finite group already satisfies the target's two boundedness properties; these are exact identity and inequality controls, not existence evidence.

The additive turn3 control clarification corrects a test-description overstatement while preserving every frozen file and every mathematical conclusion. The fifth and final direction will examine countable directed unions and the remaining witness construction obstruction.
