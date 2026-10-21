# Independent audit of the five Hermite finiteness approaches

Date: 21 October 2026.

## Verdict and hash binding

**ACCEPT the revised report as a set of reductions, conditional criteria, and proof obstructions only. It does not prove or disprove the general degree-at-least-five conjecture.** No outstanding mathematical correction was found in the revised text within the scope of this audit.

Reviewed file: `FIVE_APPROACHES.md`.

- Accepted SHA256: `0ee0023339a007fbcfc735ad6fa1078cd8f70273a535907c483d14a23fb6c9f6`.
- Original independently inspected SHA256: `7e3d6f1c6dea0cfee93f2fe9500b60abcd8f622de65e75c190c599086ea8d755`.
- Original verdict: **REVISE**, for two root-versus-polynomial classification issues described below.

The accepted hash was recomputed after reading the revised report. Acceptance is specific to that hash; later edits require review. The reviewer did not edit the target report, change the queue, commit, push, or publish anything. The two corrections were made in the target report before its final review.

## Scope and primary sources

The audited target is Conjecture 4.2 for primitive irreducible integral polynomials generating one fixed number field K of degree n at least five. Nonmonic polynomials are included. A split class means a Hermite class containing at least two polynomial GL2(Z)-classes.

The primary-source checks used:

- [Evertse, Orders with few rational monogenizations, arXiv:2301.01552v2](https://arxiv.org/abs/2301.01552v2): definitions (1.1)–(1.3), discriminant identity (1.4), the fixed-discriminant finiteness statement on printed page 5, Theorems 1.1–1.2, Lemmas 2.4–2.6, section 3 including case b4, and the statement and proof of Proposition 5.1.
- [Bhargava, Evertse, Győry, Remete, and Swaminathan, Hermite equivalence of polynomials, arXiv:2109.02932v3](https://arxiv.org/abs/2109.02932v3): Conjecture 4.2, section 5.1, and Theorem 5.1. In particular, the original quartic proof explicitly uses the S4 hypothesis to eliminate a different conjugate root before applying its degree obstruction.

The supplied source gate was inspected for the intended scope. Its wider literature search, retrieval history, and statements about later papers were not independently repeated. This audit therefore does not certify that no subsequent solution exists. It checks the five mathematical arguments against the identified versioned sources, not the entire proofs of every external theorem they invoke.

## The classification boundary

For generating elements a,b in K, polynomial GL2(Z)-equivalence holds exactly when

    b = gamma(sigma(a))

for some sigma in Aut_Q(K) and gamma in GL2(Z). To see the nontrivial direction, apply the inverse fractional-linear transformation to b. It gives a root a' of the minimal polynomial of a inside K. The map a to a' extends to a Q-embedding K into K and hence, by finite dimension, to an automorphism. The reverse implication follows by transforming the minimal polynomial and using primitivity, up to its allowed sign.

Consequently:

- Polynomial inequivalence implies inequivalence of the particular chosen roots. This is the safe implication used in Attempt 2.
- Inequivalence of particular roots need not imply polynomial inequivalence.
- If Aut_Q(K) is trivial, the second implication does hold.

These distinctions matter even for monic polynomials and mutually integral polynomial expressions.

## Review of Attempt 1

**Accepted.** Homothetic power lattices have the same multiplier order in the identified field. Evertse's identity (1.4) equates its order discriminant with the discriminant of the primitive minimal polynomial, including the nonmonic case. Thus the stated discriminant is an invariant of the Hermite class.

The fixed-degree, fixed-nonzero-discriminant finiteness theorem gives finitely many polynomial GL2(Z)-classes for each of finitely many possible discriminants. Since polynomial GL2(Z)-equivalence implies Hermite equivalence, this gives finitely many Hermite classes. Conversely, finitely many classes obviously give bounded discriminant. Finally, D(O)=D(K)[O_K:O]^2 gives the asserted equivalence with an index bound when K is fixed.

The report correctly restricts this criterion to orders arising from split Hermite classes. It does not replace the original locus with all orders having multiple rational monogenizations, and it does not mistake a bound within one order for a bound on the number of exceptional orders. No missing index estimate is supplied or claimed.

## Review of Attempt 2

**Accepted as a conditional criterion.** The ratio of cross ratios is a unit by Lemma 2.4; taking its inverse relative to the lemma's displayed convention does not change this fact. For four distinct conjugates, both complementary cross ratios are nonzero. The two linear equations yield

    c_q(a) = (e_q' - 1)/(e_q' - e_q)

when the denominator is nonzero. If e_q=e_q', their common value must be 1, so the report correctly avoids division in the degenerate case.

For any fixed ordered anchor triple, the n-3 cross ratios determine the remaining labelled points after normalizing the anchors to a fixed projective triple. The coordinate as a function of the remaining point is a nonconstant fractional-linear function and is therefore injective. A finite set of possible values for each coordinate yields finitely many normalized configurations; there are only finitely many anchor triples. Equality of configurations gives equality of all cross ratios, and Lemma 2.5 supplies the descent from projective equivalence over the normal closure to GL2(Q)-equivalence of the generators.

The selected a are special in Evertse's terminology: their witnesses have equal multiplier order and are in a different polynomial GL2(Z)-class, so in particular the chosen roots are GL2(Z)-inequivalent. Proposition 5.1 is explicitly stated for every number field of degree at least three, with no transitivity hypothesis. Its proof uses fixed rational-class cross ratios, unit equations, and Proposition 4.1, not the 5-transitivity assumption of Proposition 3.1. It therefore legitimately reduces the special elements in each of the finitely many rational classes to finitely many integral root classes. Mapping these to polynomial classes can identify classes, not create more of them.

The hypotheses remain substantial: the same finite unit set must work across all selected witnesses, and each anchor ratio used in the reconstruction must be unequal. The report explicitly does not establish either requirement. Hence this is a rigorous sufficient criterion, not a proof of general finiteness.

## Review of Attempt 3

**Accepted as an obstruction to the cited proof step.** In A6, any prescribed ordered images of four distinct letters have exactly two possible completions in S6, one even and one odd. Thus the natural action is 4-transitive. A permutation interchanging 2 and 3 while fixing 1,4,5 must also fix 6, so it is the odd transposition (2 3) and is not in A6.

Evertse's case b4 explicitly requests that exact transport; related transports also occur in case c. Thus 4-transitivity alone does not supply the permutation used in that argument. Earlier in section 3, propagating one cross-ratio equality to every tuple is a separate use of transitivity. For groups with several orbits on four-element subsets, the listed Galois and cross-ratio symmetries do not themselves connect all those subsets.

The report correctly limits the conclusion to failure of a proof step. It neither claims an arithmetic exceptional pair from this permutation calculation nor rules out a different argument, including one exploiting additional relations among cross ratios.

## Review of Attempt 4 and its required correction

**Accepted after the classification correction.** If rs>1, Q(P(X))-X is nonzero of degree rs; its divisibility by the minimal polynomial gives n<=rs. In particular, mutually quadratic expressions cannot occur for a generator of degree at least five.

For deg(P)=r>=2 and n>r+1, a rational Möbius relation for the chosen a and b would give a vanishing polynomial of degree at most r+1. It would have to vanish identically. If the denominator coefficient w is nonzero, its leading term has degree r+1 and cannot cancel. If w=0, invertibility forces z nonzero, leaving a nonzero degree-r term. This proves the claimed chosen-root obstruction.

The original report then used the phrase "the degree test gives inequivalence" in its proposed polynomial-counterexample design window without requiring the extra conjugate-root check. That inference was insufficient. The accepted revision explicitly says the test proves only chosen-root inequivalence and requires exclusion of all b=gamma(sigma(a)), or the sufficient hypothesis Aut_Q(K)={1}.

### Exact quintic regression case

Let

    f(X) = X^5 + X^4 - 4X^3 - 3X^2 + 3X + 1,
    P(X) = X^2 - 2,
    Q(X) = -X^4 - X^3 + 3X^2 + 2X - 1.

The following polynomial identities hold over Z:

    Q(P(X)) - X = -(X^3 - X^2 - 2X + 1) f(X),
    P(Q(X)) - X =  (X^3 + X^2 - 2X - 1) f(X),
    f(P(X)) = (X^5 - X^4 - 4X^3 + 3X^2 + 3X - 1) f(X).

For a root a of f, set b=P(a). The first identity gives a=Q(b), so Z[a]=Z[b]. The third shows that b has the same minimal polynomial f. Irreducibility follows modulo 2: f becomes X^5+X^4+X^2+X+1, has no root in F2, and has remainder 1 modulo the sole monic irreducible quadratic X^2+X+1. A reducible quintic over F2 must have a factor of degree one or two, so these checks suffice.

Thus n=5, r=2, s=4 satisfy r+1<n<=rs. The chosen roots are not rationally Möbius-equivalent by the degree argument, but their minimal polynomials are identical. This is a regression counterexample to the discarded inference, not a counterexample to the Hermite conjecture. It can also be realized with a=2 cos(2 pi/11), but the exact polynomial identities above establish the regression without requiring that identification.

The revised report additionally retains the necessary fixed-field and unbounded-index requirements. Equal generated integral orders imply equal power lattices in this monic setting, hence Hermite equivalence; they alone do not establish splitting or an infinite collection of classes.

## Review of Attempt 5 and its required correction

**Accepted after the matrix-classification correction.** Evaluating polynomials of degree less than n at a identifies Q[X]/(f) with K. If p_0(a) is nonzero, each congruence gives

    p_i(a)/p_0(a) = (p_1(a)/p_0(a))^i.

The evaluated columns of U are a Q-basis, and common nonzero scaling preserves that property. Hence the recovered powers of b are a basis and b generates K. Unimodularity gives equality of the Z-lattices, rather than merely a finite-index containment. Conversely, a homothety of two such lattices gives a unimodular change of their power bases; its first coordinate forces the scale to be p_0(a)^(-1). This establishes both directions of the exact criterion.

The displayed Möbius construction has coefficient matrix given by the degree-(n-1) symmetric power, in the stated monomial order. Its determinant is (AD-BC)^(n(n-1)/2), so it is unimodular for GL2(Z) input. The report's determinant formula and polynomial congruences are correct.

The original statement that the exceptional solutions are "the others" could wrongly classify matrices outside this symmetric-power family as split-class witnesses. The accepted text replaces that criterion with actual polynomial GL2(Z)-inequivalence and explicitly warns about lattice units and conjugate roots.

### Exact lattice-unit regression case

Use the same quintic f and any root a. Since f is monic with constant term 1, a is a unit of Z[a]. Multiplication by a on the power basis gives the integral unimodular matrix

    U = [[0, 0, 0, 0, -1],
         [1, 0, 0, 0, -3],
         [0, 1, 0, 0,  3],
         [0, 0, 1, 0,  4],
         [0, 0, 0, 1, -1]].

It has determinant -1. Its columns correspond to

    p_0=X, p_1=X^2, p_2=X^3, p_3=X^4,
    p_4=-X^4+4X^3+3X^2-3X-1.

All three required congruences hold modulo f. Nevertheless, the recovered b=p_1(a)/p_0(a) is just a. Moreover, in degree five every displayed symmetric-power matrix has determinant (AD-BC)^10=1, so this U lies outside that family. This supplies an explicit reason a matrix-shape test is insufficient.

The revised report correctly states that the encoding alone gives no uniform control over unbounded U or varying orders. A fixed-a search remains within one homothety class and cannot enumerate infinitely many Hermite classes.

## Computational corroboration and limits

The supplied `check_reductions.py` was independently rerun normally and under Python optimization; both executions passed. Its SHA256 was `72d77a69a30aac05e8fd0476d2b06fd5a8903aad1ac815d384667463a048503c`. Its reported check-result JSON has SHA256 `a30a6bce4460b9c4ddc2679b90b8d439f4eb230b95117e8931e01541243d36bb`.

The inspected `ROOT_POLYNOMIAL_REGRESSION.json` records the same quintic regression, with SHA256 `4a87e380b03348bd79807ecb2b1b5cac002516d70ffadc0ad3cc08f1ea1abaed`.

Those checks corroborate a symmetric-power example, a quartic inverse example, and the A6 permutation count. They are not completeness proofs. The quintic regression identities and lattice-unit example above were separately expanded and checked exactly; the accompanying algebraic explanations, rather than numerical experiments, justify their conclusions.

The final disposition is therefore accepted precisely as stated: five checked partial approaches, two corrected classification hazards, no general solution, and no novelty or external peer-review certification claimed.
