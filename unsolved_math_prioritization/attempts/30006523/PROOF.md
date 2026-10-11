# Schubert support convexity under skew sums

## Result and scope

This note gives a structural reduction and an exact obstruction to a support-based divided-difference induction for Conjecture 3 in Anna Weigandt's contribution, joint with Judy (Hsin-Hui) Chiang, to Oberwolfach Report 2/2026 [1]. The conjecture asserts that the Schubert-basis support of each ordinary Grothendieck polynomial is convex in **left weak order**.

The general conjecture is **not resolved here**. The proved results are:

1. The Schubert support of a skew sum is exactly the Cartesian product of the two supports, embedded by skew sum. Consequently, its left-weak convexity is equivalent to convexity for both factors.
2. In particular, iterated skew sums of 132 give an explicit unbounded family with Boolean-interval support. A smallest counterexample to the general conjecture, if one exists, must be skew indecomposable.
3. A polynomial with exactly the same Schubert support, coefficient signs, and descent-set restrictions as a genuine Grothendieck polynomial can lose left-weak convexity after the same K-theoretic divided-difference step. Exact coefficient magnitudes cannot be discarded in such an induction.

Exact finite controls found no counterexample for any permutation in S_n, 1 <= n <= 6. These controls support the implementation; they do not prove the general conjecture or establish novelty of the restricted theorem.

This AI-assisted manuscript is unrefereed. Acceptance means an independent internal AI audit, not external human peer review, journal acceptance, or formal proof-assistant certification.

The complete written universal proofs and displayed analytical identities are retained. This is not a computational reproduction package: raw expansion datasets, detailed computational certificate tables, executable code, copied source documents and images, and private coordination material are omitted. Historical finite checks support the work but are not premises of the universal theorem. The exhaustive finite checks cannot be reproduced from this edition alone.

The general Schubert-support left-weak convexity conjecture remains unresolved by this work. No novelty, priority, exhaustive literature survey, or current-openness claim is made.

## Conventions and the stable ambient group

Permutations are functions, written in one-line notation, with (ab)(i)=a(b(i)). The simple reflection s_i exchanges the **values** i and i+1 when multiplied on the left, and exchanges **positions** i and i+1 when multiplied on the right. Coxeter length is the number of inversions.

We use

    a <=_L b  iff  length(b)=length(a)+length(b a^{-1}).

Equivalently, a saturated increasing left-weak chain consists of steps a -> s_i a that increase length by one. For ordinary position-pair inversion sets

    Inv(a)={(r,s): r<s and a(r)>a(s)},

this is equivalent to Inv(a) being contained in Inv(b). Right weak order instead uses length(a^{-1}b), or the inversion sets of inverse permutations.

The divided-difference operators used here are

    partial_i f = (f-s_i f)/(x_i-x_{i+1}),
    pi_i f = partial_i((1-x_{i+1})f)
           = f+(1-x_i) partial_i f.

For a right descent of w,

    S_{w s_i}=partial_i S_w,    G_{w s_i}=pi_i G_w.

At w_0 in S_n both polynomials equal x_1^{n-1} x_2^{n-2} ... x_{n-1}. These are polynomial identities, not identities only after passing to a coinvariant quotient. The conventions agree with [2, equations (2.1)-(2.2)]. The isolated preceding recursive sentence in the retained v1 PDF has its ascent inequality reversed; the displayed descent cases and the starting monomial determine the convention used here.

Appending a fixed largest letter leaves both polynomials unchanged. For w in S_n, both lie in the free module spanned by monomials x^a with 0 <= a_i <= n-i. The S_u, u in S_n, are an integral basis of this module, by their unitriangular Lehmer-code monomials. Thus the expansion in this finite basis is the same as the unique expansion indexed by S_infinity; no larger-index terms have been omitted.

Moreover, an interval with endpoints in S_n acquires no new elements in S_infinity. Its upper endpoint has no inversions involving positions beyond n, so neither can an intermediate permutation. Such a finite permutation fixes every position beyond n. All statements below therefore use ordinary stability, without any back-stable or inverse-permutation reinterpretation.

## The skew sum theorem

For a in S_p and b in S_q, define

    a skew b = (q+a(1), ..., q+a(p), b(1), ..., b(q)).

Let X=(x_1,...,x_p), Y=(x_{p+1},...,x_{p+q}), and R=(x_1 ... x_p)^q.

**Lemma 1.** For H equal to either S or G,

    H_{a skew b}(X,Y) = R H_a(X) H_b(Y).

**Proof.** The longest permutation of S_{p+q} is w_0^{(p)} skew w_0^{(q)}, and its starting monomial factors exactly as the right-hand side. Obtain a from w_0^{(p)} and b from w_0^{(q)} through right-descent steps internal to their respective blocks. The concatenated steps take w_0^{(p+q)} to a skew b, and every step remains a right descent.

For an operator within the first block, R is symmetric in the two affected variables and H_b(Y) is independent of them. Both partial_i and pi_i commute with multiplication by such a symmetric factor. Therefore the operator acts only on H_a(X). The same reasoning applies within the second block, using the shifted index p+j; R H_a(X) is then independent of the affected variables. Applying the two descent sequences to the initial factorization proves the identity. This proves both polynomial factorizations without using an unproved support property. End of proof.

**Lemma 2.** The map (a,b) -> a skew b is an isomorphism of the product of the two left weak orders onto the set

    B_{p,q}={w in S_{p+q}: w({1,...,p})={q+1,...,q+p}}.

This set is an upper order ideal in S_{p+q}. Consequently,

    [a skew b, a' skew b']_L
      = {c skew d: c in [a,a']_L, d in [b,b']_L}.

**Proof.** At every permutation in B_{p,q}, the value q+1 appears before q. Hence left multiplication by s_q is a descent, never an increasing step. Every other simple reflection exchanges two values in the same block and preserves B_{p,q}. An increasing left-weak chain starting in B_{p,q} therefore stays in B_{p,q}.

The reflections s_{q+i}, 1 <= i < p, act on the first factor exactly as s_i; the reflections s_j, 1 <= j < q, act on the second factor exactly as s_j. Length is

    length(a skew b)=pq+length(a)+length(b).

Thus an increasing step is exactly an increasing step in one factor. Chains project to increasing chains in the factors, and chains in the factors may be interleaved to give a chain in B_{p,q}. This proves the product-order statement and the interval formula. End of proof.

**Theorem 3.** If

    G_a=sum_u A_u S_u,    G_b=sum_v B_v S_v,

then

    G_{a skew b}=sum_{u,v} A_u B_v S_{u skew v}.

In particular,

    Supp_S(G_{a skew b})=Supp_S(G_a) skew Supp_S(G_b),

and this support is left-weak convex if and only if both factor supports are left-weak convex.

**Proof.** Substitute the two expansions in Lemma 1 and apply that lemma for S. Distinct pairs give distinct skew sums, so no two summands can cancel each other; over the integers A_u B_v is nonzero exactly when both coefficients are nonzero. Lemma 2 shows that products of convex supports are convex. Conversely, fix any supported element in the second factor. The interval between u skew v and u' skew v is precisely [u,u']_L skew {v}; convexity of the product forces convexity of the first support. Fixing a supported first factor proves the other implication. Both supports are nonempty because their polynomials are nonzero. End of proof.

A minimal-size counterexample must therefore be skew indecomposable. This is a genuine reduction, but does not settle the skew-indecomposable case. Source-reported convex families, such as Grassmannian and 1 times dominant permutations in [1], can also be combined using the theorem; the source itself is not claimed to state this closure result.

### A self-contained infinite family

Let w_r be the skew sum of r copies of 132, so w_1=132 and w_2=465132. Directly from the defining recurrences,

    G_132=x_1+x_2-x_1 x_2=S_132-S_231.

The support {132,231} is the left-weak cover interval [132,231]_L. Theorem 3 gives

    G_{w_r}=sum_{epsilon in {0,1}^r} (-1)^{sum epsilon_i} S_{z_epsilon},

where z_epsilon is the skew sum whose i-th factor is 132 for epsilon_i=0 and 231 for epsilon_i=1. Its support is a Boolean interval with exactly 2^r elements. For example,

    G_465132 = S_465132 - S_465231 - S_564132 + S_564231.

This is an unconditional family proved here, not a novelty claim.

## Why a support-only divided-difference induction fails

Consider the ordinary Grothendieck polynomial for the simple reflection s_3=1243:

    G_1243 = S_1243 - S_1342 + S_2341
           = e_1(x_1,x_2,x_3)-e_2(x_1,x_2,x_3)+e_3(x_1,x_2,x_3).

For completeness, a pipe dream with Demazure product s_3 uses a nonempty subset of the three positions carrying generator s_3. Any other generator would introduce an inversion that cannot subsequently disappear in a Demazure product. This gives the displayed formula by summing the nonempty subsets. The Schubert identities S_1243=e_1, S_1342=e_2, and S_2341=e_3 also follow by the ordinary divided-difference recurrence.

Now change only the last coefficient:

    F=S_1243-S_1342+2 S_2341 = G_1243 + x_1 x_2 x_3.

The support of F is exactly the chain interval

    1243 <_L 1342 <_L 2341.

Indeed its first step is left multiplication by s_2 and its second is left multiplication by s_1; its inversion sets successively add (2,4) and (1,4). There is no other intermediate element. All three permutations have right descent set {3}. Thus F has the same convex support, degree-sign pattern, unique lowest Schubert term, and right-descent-set restriction as G_1243. Its monomial coefficients likewise alternate with degree.

Nevertheless, pi_3 G_1243=1, whereas

    pi_3(x_1 x_2 x_3)=x_1 x_2.

To display the direct polynomial calculation explicitly, put A=x_1+x_2-x_1 x_2 and B=(1-x_1)(1-x_2). Then A+B=1 and G_1243=A+B x_3. Since A and B are independent of x_3 and x_4,

    partial_3 G_1243=B,
    pi_3 G_1243=A+B x_3+(1-x_3)B=A+B=1,
    partial_3(x_1 x_2 x_3)=x_1 x_2,
    pi_3(x_1 x_2 x_3)=x_1 x_2 x_3+(1-x_3)x_1 x_2=x_1 x_2.

Consequently,

    pi_3 F=1+x_1 x_2=S_1234+S_2314.

The left-weak interval contains

    1234 <_L 1324 <_L 2314,

and the coefficient of S_1324 is zero. Therefore pi_3 F has nonconvex left-weak support.

This is a counterexample to preservation of convex support under pi_i, even when the listed additional input invariants hold. It is **not** a counterexample to the original conjecture: F is not G_1243 or any other ordinary G_w, and pi_3 F is not asserted to be a Grothendieck polynomial. The example explains exactly where an induction that forgets coefficient magnitudes breaks.

## Two further safeguards against wrong formulations

### Support need not be one interval or lie above its index

An independently recomputed identity, already given in [2, Example 1.4], is

    G_2143=S_2143-S_3142-S_2341+S_3241.

The support has two minimal elements in left weak order, 2143 and 2341. In particular, 2143 is not below 2341: its inversion (1,2) is absent in 2341. Hence neither a single-interval description nor containment in the principal upper set of w is a valid general shortcut. This support is still left-weak convex.

### Right weak order gives an actually false statement

For w=13254 the complete expansion is

    G_13254 = S_13254 - S_13452 - S_14253 + S_14352
              - S_23154 + 2 S_23451 + S_24153 - 2 S_24351
              - S_34152 + S_34251.

The coefficients at 13452 and 34152 are both -1, but the coefficient at 31452 is zero. Right multiplication gives increasing covers

    13452 --s_1--> 31452 --s_2--> 34152.

Their lengths are 3,4,5. Thus right-weak convexity fails. The two endpoints are incomparable in left weak order: for example, (3,5) belongs to Inv(13452) but not Inv(34152). This is a convention check, not a counterexample to Conjecture 3.

## A general descent restriction

For every supported u in G_w,

    Des_R(u) is contained in Des_R(w).

To prove it, let i be a right ascent of w. The K-theoretic recurrence gives pi_i G_w=G_w. The identity pi_i f=f+(1-x_i)partial_i f and the absence of zero divisors imply partial_i G_w=0. Applying partial_i to the Schubert expansion sends each S_u with right descent i to S_{u s_i} and all other terms to zero. These surviving indices are distinct, so each associated coefficient must vanish. This proves the restriction. The stronger failed-induction example above satisfies this restriction at the input, so adding it to a support-only invariant does not repair that argument.

## Historical finite controls and reproduction boundary

The candidate and independent audit used separately authored Python standard-library implementations with sparse integer polynomials. The independent audit reconstructed polynomials through right-descent recurrences and through a column-first triangular pipe-grid sweep using right Demazure products; it did not import or execute candidate or paper-author programs. Exact integral leading-monomial elimination reconstructed every Schubert expansion before candidate certificates were consulted.

All 873 permutations in S1 through S6 were independently reconstructed: 1,746 complete recursive-versus-pipe polynomial matches, all 873 Schubert-expansion comparisons, and all 873 left-convexity checks passed. The right-descent restriction held throughout. Three left-order descriptions were checked on 533,417 ordered pairs, and 8,332 operator identities covered right ascent and descent branches. Skew checks covered all positive block sizes with p+q<=6: 930 polynomial factorizations, 465 coefficient factorizations, and 5,447 upper-ideal members with the product-order checks.

The separate dual-extraction comparison and stability suites cover S1 through S5 only: 15,017 dual coefficient comparisons and 306 polynomial stability checks. The audit did not rerun the candidate's S6 dual extraction or S6-to-S7 stability tests, and does not claim every secondary count in the candidate report was independently reproduced. Each independent final run checked 83,859 divided-difference numerator identities.

Normal Python, -O, and -OO all passed. The final independent mathematical JSON is equal after removing the python_optimization field; the complete receipt bytes and their hashes differ. Explicit exception checks, rather than assert statements, survive optimization. Six semantic negative-control categories detected the wrong operator, changed decisive magnitude, an inserted intermediate coefficient, a deleted true interval middle, principal-upper-set containment, and right weak order.

The displayed formulas for F and the Boolean family have complete written derivations here. The G2143 identity is attributed to [2, Example 1.4]. The ten-term G13254 expansion is retained as an independently checked analytical identity for the convention example, but the complete recursive calculation and finite computation certificate establishing that expansion are omitted. Its interval conclusion follows from the displayed expansion; reproducing that expansion from first principles requires applying the stated polynomial recurrences. This finite example is not a premise of the universal skew-sum theorem.

The complete written universal proofs and displayed analytical identities are retained. This is not a computational reproduction package: raw expansion datasets, detailed computational certificate tables, executable code, copied source documents and images, and private coordination material are omitted. Historical finite checks support the work but are not premises of the universal theorem. The exhaustive finite checks cannot be reproduced from this edition alone. No new mathematical program, source retrieval, source text extraction, visual source inspection, or literature search was performed when preparing this edition. Preparation only checked editorial preservation and byte integrity.

## Sources and current public status

[1] Anna Weigandt, joint work with Judy (Hsin-Hui) Chiang, *On the Schubert Support of Grothendieck Polynomials*, in *Enumerative Combinatorics*, Oberwolfach Report 2/2026, contribution on printed pages 132-133. DOI: https://doi.org/10.4171/owr/2026/2. The complete two-page contribution was read and visually inspected. It reports all three conjectures for Grassmannian permutations and for 1 times dominant permutations; its inverse-fireworks claim covers only Conjectures 1 and 2.

[2] Anna Weigandt, *Changing Bases with Pipe Dream Combinatorics*, arXiv:2506.07306v1, https://arxiv.org/pdf/2506.07306v1. The retained v1 PDF has internal date June 10, 2025; the arXiv v1 submission date is June 8, 2025. Relevant portions inspected: introduction and Example 1.4, definitions and equations (2.1)-(2.2), stability, and the triangular pipe-dream formula, Theorem 4.3. This supplies conventions and existing formulas, not a proof of the target conjecture.

[3] Judy (Hsin-Hui) Chiang, public research page, https://sites.google.com/view/judy-chiang/research, retrieved October 11, 2026 UTC. The relevant project still lists its paper as in progress. This public status is not evidence that the conjecture is currently open, that no unpublished solution exists, or that the restricted results above are new.
