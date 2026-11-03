# Fixed-field split Hermite classes: five approaches

Date: 21 October 2026. Target: BEGyRS Conjecture 4.2 for a fixed number field K of degree n >= 5, with all primitive irreducible integer polynomials PI(K), including nonmonic ones. The conjecture asserts finiteness of Hermite classes that contain more than one GL2(Z)-class. This report does not solve the conjecture. All lemmas below are elementary reductions or consequences of cited results; no novelty is claimed.

## Sources and scope

[E] J.-H. Evertse, *Orders with few rational monogenizations*, arXiv:2301.01552v2, https://arxiv.org/abs/2301.01552v2 . Relevant portions inspected: Lemmas 2.4–2.6; section 3 and its five-index argument; Proposition 4.1; Proposition 5.1 and its proof; proofs of Theorems 1.1 and 1.2.

[B] Bhargava, Evertse, Győry, Remete, Swaminathan, *Hermite equivalence of polynomials*, arXiv:2109.02932v3, https://arxiv.org/abs/2109.02932v3 . Source-gate inspection establishes Conjecture 4.2 and the fixed-quartic-field counterexamples. The quartic examples are known results, not a disproof in degree >= 5.

The source gate and metadata accompany this investigation. The bounded literature check does not certify universal absence of subsequent work. [E] Theorem 1.2 proves the target when the normal closure acts 5-transitively. The general case is not settled here.

Write M(a)=Z+Za+...+Za^(n-1), and O(a)={x in K: xM(a) subset M(a)}. Hermite equivalence admits generating roots a,b in K and lambda != 0 with M(b)=lambda M(a). This implies O(a)=O(b), but the converse must not be assumed. Root-based equivalence can distinguish choices of embeddings that the polynomial forgets; the arguments below use implications in the safe direction.

## Attempt 1: bound the discriminant/index on the correct locus

For a split Hermite class H let D(H) be its polynomial discriminant. It is also the discriminant of O(a), by [E] (1.4), and is well-defined because homothetic modules have the same multiplier order (up to the field isomorphism implicit in the choice of roots).

**Exact criterion.** The target conjecture is equivalent to bounded |D(H)| over split H in PI(K), and hence to bounded [O_K:O(a)] over orders represented by such split classes.

Proof. If there are finitely many H, their discriminants form a finite set. Conversely, bounded absolute discriminant permits only finitely many nonzero integer discriminants. For each fixed discriminant, the fixed-degree finiteness theorem for GL2(Z)-classes of integral binary forms, recalled in [E] page 5, gives finitely many polynomial classes, hence finitely many Hermite classes. Finally D(O)=D(K)[O_K:O]^2 for each full order O in K.

This is an exact criterion for the original Hermite locus, NOT a replacement by the stronger conjecture about every order with multiple rational monogenizations. It gives a necessary diagnostic for any counterexample: invariant-order indices must be unbounded, even in a fixed field. Fixing the field discriminant alone does not bound them. Uniform bounds for the number of rational monogenizations of one order do not bound the number of exceptional orders.

Outcome: a rigorous necessary-and-sufficient reduction, with no bound obtained. The principal missing estimate is uniformity over orders on the split-module locus.

## Attempt 2: finite cross-ratio charts, followed by the integral upgrade

Fix the n embeddings K -> L, where L is the normal closure, and write
c_ijkl(a)=((a_i-a_j)(a_k-a_l))/((a_i-a_k)(a_j-a_l)).
For a,b with equal multiplier order put e_ijkl=c_ijkl(b)/c_ijkl(a). These are units of O_L by [E] Lemma 2.4. For q=(i,j,k,l), let q'=(i,l,k,j). Then c_q+c_q'=1 and c_q e_q+c_q' e_q'=1. If e_q != e_q',

c_q(a)=(e_q'-1)/(e_q'-e_q).

If e_q=e_q', both are 1, and the two equations are identical; division is forbidden. In particular e_q != 1 implies e_q != e_q'.

**Conditional chart criterion.** Suppose there is a finite set S subset O_L^* such that for every split Hermite class one can choose a generating root a and a witness b from a different polynomial GL2(Z)-class, with M(b) homothetic to M(a), and choose three distinct anchor indices i,j,k, such that, for every l outside those anchors, e_ijkl and e_ilkj lie in S and e_ijkl != 1. Then the desired Hermite finiteness follows.

Proof. There are finitely many anchor triples. The displayed formula puts all n-3 anchor cross ratios in a finite set. A fractional linear map sending the three distinct anchor coordinates to a fixed triple identifies the remaining coordinates injectively with these cross ratios. Therefore finitely many normalized labelled configurations occur. Equality of configurations implies equality of all cross ratios, hence GL2(Q)-equivalence by [E] Lemma 2.5. The chosen a are special in [E]'s sense because equal multiplier order and polynomial inequivalence imply root inequivalence. Proposition 5.1 of [E], valid for every number field of degree >= 3 without a transitivity assumption, turns each such rational class of special elements into finitely many integral classes. A root integral class determines a polynomial integral class and thus a Hermite class.

This explicitly closes the rational-to-integral step; claiming only GL2(Q)-finiteness would leave a gap without Proposition 5.1. However, the finite-unit and unequal-anchor hypotheses have not been proved for arbitrary K. Equal cross ratios can occur on some Galois orbits without forcing equality on all orbits. The conditional criterion is not a claim that witnesses meeting its hypotheses always exist.

Outcome: a rigorous sufficient criterion locating the missing uniform input.

## Attempt 3: remove 5-transitivity from the unit-equation proof

The five-index relation in [E] (3.8) is an identity among six units. Lemma 3.3 reduces its solutions to a finite-coordinate case or special multiplicative degeneracies. The proof then transports identities by Galois permutations, including transposing two indices while keeping three other indices fixed. These transports are not formal consequences of the unit equation.

A concrete group-theoretic obstruction to reusing that argument verbatim is the natural action of A6 on six letters. It is 4-transitive: after prescribing four distinct images, the two unused images can be ordered to produce an even permutation. But it contains no permutation interchanging 2 and 3 while fixing 1,4,5: the sole remaining letter 6 must also be fixed, leaving an odd transposition. This is precisely a transport used in [E]'s case b4 (and related cases). Thus even replacing 5-transitivity by 4-transitivity requires a new argument, not a notation change.

For still smaller permutation groups, there is an earlier obstruction: one equality c_q(a)=c_q(b) propagates only through its Galois orbit and the usual cross-ratio permutations. It need not reach all four-index subsets. Consequently the nonvanishing used to derive (3.5) for every tuple is not available merely from global inequivalence.

The A6 observation is a failure of a proof step, not a counterexample to the conjecture, and not evidence that no different group argument works. We do not assert existence of arithmetic exceptional pairs from the permutation calculation.

Outcome: exact location of two independent uses of transitivity; no replacement lemma established.

## Attempt 4: lift the known quartic polynomial-inverse mechanism

The known quartic construction uses mutually quadratic expressions b=a^2-r and a=b^2-s. Could the same mechanism produce counterexamples of degree >= 5?

**Degree obstruction.** If a has degree n over Q, b=P(a), a=Q(b), with nonconstant P,Q in Q[X] of degrees r,s and rs>1, then n <= rs.

Proof. The nonzero polynomial Q(P(X))-X has degree rs and vanishes at a, so the degree-n minimal polynomial divides it. Thus mutually quadratic polynomial expressions force n <= 4. This excludes a literal transplantation of the quartic construction to the intended target.

For r,s >= 2, b cannot be rationally Möbius-equivalent to a whenever n>r+1: if b=(u a+v)/(w a+z), then (wX+z)P(X)-(uX+v) vanishes at a and has degree at most r+1. If n>r+1 it must vanish identically. This would make the polynomial P a degree-one rational function, impossible when r>=2 and uz-vw !=0.

This supplies a possible counterexample design window: choose r,s with r+1<n<=rs, and try to realize infinitely many mutually polynomial generating pairs in one fixed field and with equal integral orders. If P,Q have integer coefficients and a,b are integral, mutual expressions do give Z[a]=Z[b], hence Hermite equivalence, while the degree test gives inequivalence of the chosen roots only. It does NOT by itself give inequivalence of their minimal polynomials: those polynomials can be identical when a and b are distinct conjugate generators. One must additionally exclude b=gamma(sigma(a)) for every Q-automorphism sigma of K and every gamma in GL2(Z). If Aut_Q(K) is trivial, root inequivalence suffices; otherwise each conjugate identification must be checked. But varying an integer polynomial Q(P(X))-X normally varies the field, and a single pair or infinitely many pairs in one order is not an infinite family of Hermite classes. Such a construction must verify a fixed field and unbounded order indices. No such family is constructed here.

Outcome: the quadratic route is rigorously blocked; higher-degree inverse mechanisms remain a search direction, not a counterexample.

## Attempt 5: exploit full homothetic-module data rather than only orders

The stronger order theorem discards information that the target retains. Here is an exact algebraic encoding of that extra information. Fix a generator a of K, let f be its minimal polynomial over Q, and put v(a)=(1,a,...,a^(n-1)) as a row vector. Given U in GL_n(Z), write v(a)U=(p_0(a),...,p_(n-1)(a)), with p_i in Z[X] of degree <=n-1.

**Exact module criterion.** If p_0(a) != 0, there is a generator b with
v(b)=p_0(a)^(-1)v(a)U
if and only if, in Q[X]/(f),
p_i p_0^(i-1)=p_1^i for i=2,...,n-1.
In this case b=p_1(a)/p_0(a), and M(b)=p_0(a)^(-1)M(a).

Proof. Necessity follows by taking powers of b. Conversely the identities give p_i(a)/p_0(a)=b^i, with the i=0,1 identities automatic. Since U is invertible, its n columns evaluate to a Q-basis of K; multiplying by p_0(a)^(-1) preserves independence. Thus 1,b,...,b^(n-1) is a basis and b generates K. The unimodular integral basis change gives precisely the asserted homothety. Conversely every homothety of the two power lattices has such a unimodular change of bases, so this encoding does not silently enlarge the problem.

Möbius substitutions b=(A a+B)/(C a+D) with matrix in GL2(Z) give the familiar solutions p_i(X)=(AX+B)^i(CX+D)^(n-1-i). Their coefficient matrix is unimodular because the determinant of this symmetric-power representation is (AD-BC)^(n(n-1)/2). The desired exceptional witnesses are solutions whose resulting primitive minimal polynomial is actually GL2(Z)-inequivalent to that of a. Merely lying outside the displayed symmetric-power matrices does not certify this: alternative lattice-unit scalings in a homothety, or different generating conjugate roots, can yield additional matrices for the same polynomial class. The encoding must therefore be followed by the actual polynomial-equivalence test, not by a matrix-shape test.

This converts a witness search for fixed a into explicit congruences plus det U=+1 or -1. It also shows why a naive dimension or height argument is insufficient: U is unbounded; modulo f the multiplicative identities have many rational solutions, while integrality/unimodularity are the essential restrictions. A finite search in U does not prove completeness. Moreover fixing a fixes its multiplier order and cannot itself produce infinitely many split Hermite classes. To prove the conjecture by this route one needs uniform arithmetic control as a and its order vary; that estimate is not provided.

Outcome: exact encoding preserving the original module condition, but no uniform rigidity theorem.

## Final disposition

Five distinct mathematical routes were carried through to explicit reductions, verifiable obstructions, or conditional criteria. None proves or disproves the general fixed-field degree-at-least-five conjecture. The 5-transitive case is credited to [E], and known quartic counterexamples do not settle the intended target. No queue change, commit, push, or publication was performed in this analysis.
