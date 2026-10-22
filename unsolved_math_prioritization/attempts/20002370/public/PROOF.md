# Quantifier complexity for two real rational-function fields

Problem 20002370 / AIM-LOGIC-0146, corresponding to Zahidi's Question 34 in the AIM Hilbert's tenth problem list.

## Disposition

**Partial only. The exact minimum total number of variables is not determined.** In the pure ring language, the minimum prenex block-alternation count is one, by established results. For the number of leading universals in a prenex universal-existential separator the verified bounds are 2 and 3. This report does not improve those bounds or claim a new resolution. It reconstructs the known separator with consistent indexing and gives rigorous obstructions to several tempting simplifications.

The substantive conclusions are mathematical; finite checks below only audit arithmetic and logical transformations. No finite field is used as a model for the two characteristic-zero function fields.

## 1. The question and conventions

Set k = Q-bar intersect R, the field of real algebraic numbers, and K = R. Write F = k(t) and E = K(t), where t is an indeterminate. The original AIM question asks for the smallest quantifier complexity, and separately the smallest number of variables, of a sentence distinguishing F and E. It records that the base fields are elementarily equivalent, the function fields are not, and their existential theories agree.

We use L = {0,1,+,-,multiplication}, with equality, and no other named constants. In particular t is NOT a language symbol. Inequalities below concern the unique order of a real closed constant field; they are not additional predicates in F or E. Subtraction is a ring operation. Rational numbers in formulas can be expressed by clearing fixed nonzero integer denominators.

The AIM wording does not specify a fine-grained syntactic convention. We distinguish:

1. **Prenex alternations:** adjacent equal quantifiers are combined into blocks; a purely existential or universal sentence has zero alternations.
2. **Leading universals:** a prenex sentence forall x_1 ... x_n exists y_1 ... y_m theta, with theta quantifier-free, has n leading universals. The number m is unrestricted.
3. **Finite-variable width:** the number of distinct variable symbols anywhere in a formula, allowing reuse in nested or disjoint scopes.
4. **Quantifier occurrences:** the number of quantifier symbols before any optional transformation. This is not width or quantifier rank.
5. **Branched universal height:** the hierarchy generated from existential formulas by positive Boolean combinations and one extra outer universal at each level. Vollprecht denotes this with a SUPERSCRIPT on forall. It is different from the SUBSCRIPT that bounds the universal block in prenex normal form.

The last distinction is essential: a height-two formula in that hierarchy need not have a two-universal prenex form. Adding a symbol naming t changes the problem.

## 2. Known lower bound, proved directly

### Lemma 2.1 (coefficient transfer)

If k is existentially closed in a field K, then k(t) is existentially closed in K(t).

**Proof.** Fix an existential formula with parameters in k(t), and a witnessing tuple of rational functions over K. Replace the quantifier-free matrix by a true conjunction in disjunctive normal form. Fix the actual finite degrees of the chosen numerator and denominator polynomials. Replace their coefficients by unknown field elements. Clear denominators in each equation. An identity in t is equivalent to the vanishing of its finitely many coefficients. For every denominator, and for every numerator required to be nonzero, select a coefficient that was nonzero in the original solution and impose that nonvanishing condition. The resulting finite existential system has coefficients in k and a solution in K. Existential closedness gives a solution in k, which reconstructs all rational functions and all original equations and inequations. The converse direction is immediate from inclusion. QED.

### Lemma 2.2 (one universal, Anscombe--Fehm)

F and E satisfy exactly the same parameter-free forall-one-exists sentences.

**Proof.** Quantifier elimination for real closed fields makes k elementary in K. Hence Lemma 2.1 applies. It gives the downward direction E to F for every universal-existential sentence: fix a tuple in F and descend its existential witnesses.

For the upward direction with only one universal, let sigma = forall x exists y-bar theta(x,y-bar) hold in F, and fix b in E. If b belongs to k, use witnesses already in F. Otherwise b is transcendental over k: K is relatively algebraically closed over its real-closed subfield k, and adjoining an indeterminate introduces no element algebraic over K. Consequently the k-embedding F -> E defined by t -> b exists. Apply it to witnesses for x=t in F. This preserves the quantifier-free matrix and produces witnesses for b. QED.

This is the specialization of [AF, Lemma 5.2], not a new transfer theorem. Negation gives equality of the exists-one-forall theories. Lemma 2.1 also gives agreement of existential theories, even when t is named, and negation gives universal agreement.

**Consequences.** Zero prenex alternations cannot separate. Neither a single leading universal nor a single leading existential in a two-block sentence can separate in the respective orientations. Every sentence using at most two quantifier occurrences agrees, since its dependent case has a two-quantifier prefix and its independent case is a Boolean combination of one-quantifier sentences.

### Lemma 2.3 (one variable symbol)

F and E satisfy the same sentences using only one variable symbol, however often it is rebound.

**Proof.** In a one-variable formula, every quantified proper subformula is a sentence: binding that one symbol leaves no free variable. Inductively replace closed subformulas by their truth values. To compare a sentence across two structures, these truth values agree by induction, and the next closed quantified subformula becomes a purely existential or universal one-variable sentence. Their truths agree by Lemma 2.1 and negation. Boolean operations preserve agreement. QED.

Thus finite-variable width is at least two. This does NOT prove that two symbols suffice, or that width two agrees. A lower bound on quantifier occurrences also does not imply a width bound of three.

## 3. Consistently normalized cut

Define factorial digits d_i = 1 when i=m! for some integer m>=1, and d_i=0 otherwise. Define

lambda = sum_{m>=1} 2^(-m!),
s_n = sum_{1<=i<=n} d_i 2^(-i),
A_n = 2^n,
B_n = sum_{1<=i<=n} d_i 2^(n-i).

The repetitions 0!=1! are excluded: lambda starts at m=1. These definitions imply s_n=B_n/A_n, with integer A_n,B_n. The set S={(A_n,B_n):n>=1} is computable, hence recursively enumerable.

For every n>=1,

0 < lambda-s_n < 2^(-n).                                                    (3.1)

Indeed infinitely many positive digits remain, but not all later digits are 1, so the tail is strictly smaller than the full geometric tail sum_{i>n}2^(-i).

The number lambda is transcendental. For m>=2 put q_m=s_{m!}, whose denominator divides Q_m=2^(m!). The next nonzero digit occurs at (m+1)!, and

0 < lambda-q_m < 2 * 2^(-(m+1)!) = 2 Q_m^(-(m+1)).

If lambda were algebraic of degree d, Liouville's approximation lower bound would give c Q_m^(-d) <= |lambda-q_m| for all rational q_m distinct from lambda and a fixed c>0 (using unreduced denominators only weakens that lower bound). For m+1>d, the displayed upper bound eventually contradicts it. Thus lambda is not in k.

For each real c,

c != lambda iff there exists n>=1 with |A_n c-B_n| >= 1.                    (3.2)

If c=lambda, (3.1) proves all the strict inequalities. Conversely, if |c-s_n|<2^(-n) for every n, the convergence of s_n to lambda forces c=lambda. Taking the contrapositive proves (3.2), including the non-strict boundary >=1. This proof is stated for real subfields, which is enough for F and E; no non-Archimedean extension is needed here.

## 4. Reconstructing the established separator

### 4.1 The constant-field predicate

Let H(x,v) be the quantifier-free equation v^2=1+x^4, and put C(x)=exists v H(x,v).

For every real closed field L, C defines L inside L(t). If x is constant, 1+x^4 is positive and has a square root in L. Conversely a nonconstant rational solution (x(t),v(t)) would give a nonconstant map from the projective line to the smooth projective curve v^2=1+x^4. The polynomial 1+x^4 is squarefree and the curve has genus one. In characteristic zero the Riemann--Hurwitz formula prohibits such a map: -2=degree*0+nonnegative ramification. Therefore x is constant, and then v is algebraic over L and belongs to L as well. This is the standard positive-genus constant-definition argument underlying Robinson's result.

In particular,

H(x,v) implies C(x) and C(v).                                               (4.1)

### 4.2 Existential arithmetic input

Denef's established theorem provides a uniform existential definition of the ordinary integers inside L(t), with t named, for real closed L. Combined with the four-square definition of nonnegative integers and the DPRM theorem, it supplies a fixed parameter-free existential formula D(a,b,u) such that

L(t) satisfies D(a,b,t) iff (a,b) belongs to S.                              (4.2)

Every arithmetic quantifier introduced in this composition is existential. The formula is fixed and finite, though this report does not expand the particular Denef and DPRM coding polynomials or count their auxiliary variables. This is precisely the kind of input verified in [V, Lemma 6.1.1 and Section 6.3]. It is not a new Diophantine definition.

Define the existential formula

G(x,u) := C(x) and exists a,b,z [D(a,b,u) and C(a) and C(b)
                                and 1+z^2=(a*x-b)^2].

For c in L contained in R, equation (4.2) and real closedness give

L(t) satisfies G(c,t) iff c != lambda.                                    (4.3)

The equality 1+z^2=(A_n*c-B_n)^2 has a solution exactly when the right hand square is at least 1. Any such z is algebraic over L and is constant. Thus it encodes the non-strict inequality in (3.2), including equality with z=0.

Whenever c belongs to L and G(c,t) holds, G(c,u) also holds for every u in L(t)\L. Apply the L-isomorphism L(t)->L(u), t->u, to the existential witnesses, then include L(u) in L(t). No assertion is made that u itself generates the full field, or that D(-,-,u) defines the same set without restricting to these transported solutions.

### 4.3 Parameter elimination

The sentence

Sigma := forall x forall v forall u [not H(x,v) or C(u) or G(x,u)]           (4.4)

is equivalent to a pure prenex forall-three-exists sentence. Every predicate besides the negated quantifier-free H is existential, so all its witnesses can be renamed and moved to a single final existential block. Nonempty field domains justify unused witnesses in other disjuncts. Only integer coefficients occur.

**F satisfies Sigma.** If H(x,v) fails, the first disjunct works. If it holds, (4.1) gives x in k. Since lambda is transcendental, x != lambda and G(x,t) holds by (4.3). If u is constant C(u) holds; otherwise the preceding embedding transfers G(x,t) to G(x,u).

**E does not satisfy Sigma.** Set x=lambda, take v=sqrt(1+lambda^4) in R, and set u=t. Now H(x,v) holds, C(t) fails, and G(lambda,t) fails by (4.3).

This reconstructs the established strategy in [V, Lemmas 6.3.5 and 6.3.14]. Combined with Section 2 it proves:

- Minimum prenex block-alternation count: exactly one.
- Minimum number n of leading universals in a prenex forall-n-exists separator: 2<=n<=3.
- Minimum total variable-symbol count: at least two and finite; no exact value or useful explicit numerical upper bound is supplied here.

Negation reverses the separator and gives the analogous leading existential bounds for exists-n-forall. These upper and lower bounds are prior-result consequences; this packet claims no priority.

### 4.4 Source normalization caution

The inspected PDF of [V], printed p.117, defines ell_p=sum_{i>=0}p^(-i!), then identifies it with 1+sum d_i p^(-i). With the ordinary factorial convention the latter identity has a rational offset: ell_p=p^(-1)+sum d_i p^(-i). For p=2 the difference is 1/2. The center 2+sum d_i p^(-i) in the subsequent displayed polynomial is likewise a rational translate of either convention, rather than literally the labeled ell_p-1.

These are local normalization discrepancies, not a refutation of the existence theorem: whether a field realizes a real rational cut is invariant under any fixed rational translation. Equations (3.1)--(4.4) avoid the offsets altogether. This is our source check, not an author-issued erratum.

## 5. Attempts to reduce the universal block

### 5.1 Branching is not prenex compression

The sentence

forall x [(forall v not H(x,v)) or (forall u (C(u) or G(x,u)))]               (5.1)

is equivalent to (4.4). It belongs to the branched universal-height-two fragment: after the outer forall x, each disjunct has only one universal layer above an existential formula. This is the superscript-two fragment in [V]. Distributing disjunction across universal quantification over two independent variables creates three leading universals. Calling (5.1) a prenex forall-two-exists sentence is incorrect.

### 5.2 Diagonal identification destroys the separator

A tempting shortcut is to identify v and u in (4.4), leaving

forall x forall u [not H(x,u) or C(u) or G(x,u)].                            (5.2)

But (4.1) proves not H(x,u) or C(u) identically. Therefore (5.2) is TRUE in every L(t) for L real closed, regardless of G. It cannot separate the fields. This is an exact mathematical obstruction to this particular compression, not a proof that every two-universal separator is impossible.

The accompanying finite truth-table checks illustrate the logical error even before imposing field axioms. Their structures are only controls for the transformation, never proposed approximations to F or E.

### 5.3 No existential nonconstant guard over constants

For every infinite field L, the constant subfield L is existentially closed in L(t). To see this, specialize t to a value in L avoiding the finitely many zeros and poles in a witnessing tuple of rational functions and the finitely many nonzero numerators whose nonvanishing must be preserved.

Consequently no nonempty existentially L-definable subset of L(t) can be disjoint from L: an existential sentence asserting that it is nonempty would already have a solution in L. In particular L(t)\L has no existential definition using only parameters from L.

Thus replacing the universally quantified negation of C(x) in (5.1) by an existential parameter-free nonconstant guard is impossible. A guard with t named is a different situation, because t is not in the constant subfield. A two-argument guard N(x,u) that behaves correctly for every nonconstant u is not ruled out by this lemma, and no such construction is supplied here.

## 6. Why bounded searches cannot settle this pair

### Proposition 6.1 (bounded-degree transfer)

Fix a ring formula with integer coefficients. For each quantified variable occurrence impose a fixed finite bound on the degrees of its numerator and denominator in t. The resulting bounded-semantics sentence has the same truth over k(t) and R(t).

**Proof.** Represent a degree-at-most-d rational function by 2(d+1) coefficients with a nonzero denominator. Polynomial identities after clearing denominators are finite coefficient conditions. Nonidentity is a finite disjunction saying that at least one coefficient is nonzero. Recursively translate every bounded existential quantifier into existential quantification over coefficient tuples with valid denominators; translate every bounded universal into universal quantification over coefficient tuples with the validity condition as an implication. Representation need not be unique: equality of rational functions is encoded by cross multiplication, so all representatives give the same truth. Terms with addition and multiplication have finite degree bounds determined syntactically. The resulting sentence is first-order over the real closed constant field, and therefore has the same truth in k and R. QED.

This does not identify a fixed-degree truncation with the full function field, nor interchange an unbounded union with a universal quantifier. It explains why no single finite degree experiment can distinguish the pair.

### Proposition 6.2 (unbounded cut-witness index)

Let m>=2 and q_m=s_{m!}, a rational number. The smallest integer n>=1 for which

|A_n q_m-B_n|>=1

holds is n=(m+1)!.

**Proof.** For n<=m!, q_m-s_n is a finite sum of later binary digits, strictly between or equal to 0 and 2^(-n). For m!<n<(m+1)!, there are no new nonzero digits, so s_n=q_m. At n=(m+1)!, exactly one new digit appears, and A_n(s_n-q_m)=1. QED.

Hence any finite prefix of the cut conditions has rational, therefore real-algebraic, solutions. Their infinitely quantified limit isolates lambda, but no finite prefix does. The required arithmetic index grows without bound even on rational constants. This is not a lower bound on the total number of coding variables: one fixed existential Diophantine formula can have unbounded witnesses.

## 7. Remaining gaps and evidence boundaries

Five substantive approaches were completed: transfer/lower bounds; an independently normalized cut separator; prenex compression; constant-guard and finite-variable barriers; and bounded-degree/arithmetic tests. The original total-variable minimization is unresolved by this work. We also do not decide whether the leading-universal minimum is two or three.

[AF, Remark 5.4] explicitly leaves a two-leading-universal question unresolved for R(t) versus a proper elementary extension R*(t). That is a RELATED pair, not literally the AIM pair. Our bounded literature search found no primary-source exact determination for the AIM pair; this is not a certification that no such result exists.

No field-separation claim follows from the finite controls. No quantifier-rank optimum, two-variable equivalence, expansion-of-language invariant, optimal Denef/DPRM variable count, or novelty claim is made.

## References

- [AIM] B. Poonen and T. Scanlon (moderators), J. Demeyer (notes), *Problems related to Extensions of Hilbert's Tenth Problem*, Question 34, printed p.7: https://aimath.org/WWN/hilberts10th/hilberts10th.pdf .
- [AF] S. Anscombe and A. Fehm, *Universal-existential theories of fields*, Proceedings of the Edinburgh Mathematical Society 69 (2026), 95--124; online 3 September 2025. https://doi.org/10.1017/S0013091525100771 . Readable author preprint v3, 9 May 2025: https://arxiv.org/html/2405.12771v3 . Lemma 5.2 and Remark 5.4.
- [V] M. A. Vollprecht, *Model Theory of Rings and Fields Finitely Generated over Local Fields*, TU Dresden dissertation, submitted 28 January 2025, defended 15 April 2025. https://d-nb.info/1364825406/34 . Definition 3.2.1; Lemma 6.1.1; Lemmas 6.3.5, 6.3.14. Original PDF independently downloaded and the cut-formula page visually inspected.
- [D] J. Denef, *The Diophantine problem for polynomial rings and fields of rational functions*, Transactions of the AMS 242 (1978), 391--399, Proposition 2. https://doi.org/10.1090/S0002-9947-1978-0491583-7 . Publisher metadata retrieved; theorem scope additionally verified through [V], Lemma 6.1.1. Direct publisher PDF retrieval was blocked.
- [R] R. M. Robinson, *The undecidability of pure transcendental extensions of real fields*, 1964, pp.275--282. https://doi.org/10.1002/malq.19640101803 . Attribution verified through [V]; the constant-definition argument needed here is supplied above rather than claiming a fresh full-source reading of [R].

Classical quantifier elimination for real closed fields, DPRM, Liouville's inequality, and Riemann--Hurwitz are explicitly used as theorem inputs, not machine-verified here.
