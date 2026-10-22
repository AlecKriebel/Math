# Independent mathematical audit: Dietzel Problem 3

## Decision

**PASS: complete under the axioms printed in Definition 2 of the workshop report.** The frozen candidate proves the claimed classification, including arbitrary infinite meet-semilattices. No mathematical repair is required. This is an AI-assisted independent audit of the complete proof, not journal peer review, an external acceptance, or a claim of historical novelty. This unrefereed report carries no human or formal certification.

Original audited candidate: 6,872 bytes, SHA-256 `46c340870fc038943d939a0abbd82703a87e9e6a7dacd060b32857da143b76ac`. The public editorial edition is [PROOF_CLASSIFICATION.md](PROOF_CLASSIFICATION.md); its mathematical sections are byte-identical to that candidate. The input was read only and its hash was rechecked after inspection. The auditor reconstructed the full necessity and sufficiency arguments from the source and proposed operation before reading the frozen manuscript.

The conclusions are:

1. Every nonempty meet-semilattice admits the four printed semibrace axioms.
2. It admits those axioms and the printed L-algebra axioms together exactly when it has a greatest element. In any such realization the distinguished element is the greatest element, and the two orders coincide.
3. Under the separately attested convention requiring the meet operation to have identity e, the first conclusion restricts to meet-semilattices having a greatest element. The second conclusion remains unchanged.

## Primary-source inspection

Carsten Dietzel, *Some problems on L-algebras*, in *Mini-Workshop: Skew Braces and the Yang–Baxter Equation*, Oberwolfach Report 9/2023, pp. 544–547, DOI 10.4171/OWR/2023/9. Primary public PDF: <https://ems.press/content/serial-article-files/47003>.

The local primary PDF has 286,244 bytes and SHA-256 `0ba13c573755289bb62e119df381d19e03a31cb3fff8e1ff3e240dce8dfeeefc`. All four printed pages of the Dietzel contribution were read as text and visually inspected from locally rendered PDF pages 8–11 (one-based). The live official URL was independently opened and returned the same workshop title and page count. No independent byte-for-byte re-download is claimed.

The p. 544 footnote defines the meet operation by idempotence, associativity, and commutativity. Definition 1 requires the unit/diagonal laws, cycloid identity, and separation law. Definition 2 on p. 545 lists exactly these four equations:

- x·(y∧z) = (x·y)∧(x·z)
- e·x = x
- (x∧y)·z = (x·y)·(x·z)
- x·e = e

It does not state that e is a meet identity. Problem 3 separately asks for semibraces and for those also satisfying the L-algebra axioms. No finiteness, distributivity, joins, least element, nontriviality, cancellation, or self-similarity hypothesis is added there. The preceding discussion of self-similar closures concerns other structures; it does not modify Definition 2. The remark concerning the lack of an obvious trivial construction is context, not an additional equation.

Definition 3.1 of Dietzel, Menchón, and Vendramin, *On the enumeration of finite L-algebras*, arXiv:2206.04955v4, p. 5, was separately read and visually inspected. That definition starts with a commutative monoid with identity e and imposes the same four equations. Public source: <https://arxiv.org/abs/2206.04955v4>. Local inspected PDF: 429,694 bytes, SHA-256 `cd5551caffcc3c69959fbc72bbcdc1b0d2d736aa14569fd5df34a257dd435ea6`. The public record identifies v4 as the July 2023 postprint; earlier versions predate the workshop, so no historical claim that the monoid convention first appeared later is made. This convention difference is explicit in the candidate and does not defeat the classification.

The 2008 source cited by the workshop as reference [6] was not independently inspected in this audit. Consequently this report establishes the theorem for the printed workshop axioms and the separately inspected monoid convention; it does not attribute unstated assumptions or authorial intent to the 2008 paper.

## Independent proof

Let ≤ denote the order x≤y iff x∧y=x. The standard order properties follow from the associative, commutative, idempotent meet laws. In particular x≤y∧z iff both x≤y and x≤z.

### All nonempty semilattices satisfy the printed semibrace equations

Choose any e in a nonempty semilattice and put x·y=y. The first equation has y∧z on both sides. The third has z on both sides. The two unit/absorption equations hold immediately. The empty set cannot contain the required distinguished element. On a set with more than one element, this particular operation does not satisfy x·x=e; it is not being used to prove the second part.

### Necessity of a greatest element and equality of orders

Assume both structures are present. Write T_a(z)=a·z. If T_a=T_b, evaluating at a and b gives b·a=e and a·b=e, respectively, by the diagonal law. L-algebra separation gives a=b. Thus the map a↦T_a is injective.

Using the third semibrace equation with y=e gives

T_(x∧e)(z) = (x·e)·(x·z) = e·(x·z) = T_x(z).

Injectivity gives x∧e=x for every x, so e is greatest in the meet order.

If x∧y=x, the same semibrace equation with z=y gives

x·y = (x·y)·(x·y) = e.

Conversely, if x·y=e, then for every z,

T_(x∧y)(z) = e·(x·z) = T_x(z),

and injectivity gives x∧y=x. This proves that the meet order and the L-algebra order agree, with no appeal to a finiteness argument.

### Sufficiency of a greatest element

Let e be greatest. Define x·y=e when x≤y and x·y=x∧y when x≰y.

The identity e·y=y follows by separating y=e from y≠e. The diagonal and absorption identities follow from x≤x and x≤e. Also x·y=e iff x≤y: in the other branch, x∧y=e would force x=y=e, contradicting x≰y. Therefore the separation equivalence follows from antisymmetry.

For meet preservation, fix x,y,z:

- If x≤y and x≤z, every output in the required equation is e.
- If x≤y and x≰z, then x≰y∧z, and both sides equal x∧z. The case x≰y and x≤z is symmetric.
- If x≰y and x≰z, then x≰y∧z, and both sides equal x∧y∧z.

For the third semibrace identity, if x≤y then x∧y=x and x·y=e; the equation reduces to x·z=e·(x·z).

Otherwise put a=x∧y, so x·y=a. If x≤z, then a≤z and both sides of the identity equal e. If x≰z, put b=x∧z. Since a≤x,

a≤b iff a≤z.

When these inequalities hold, a·z=a·b=e. When they fail,

a·z=a∧z=a∧b=a·b.

This proves (x∧y)·z=(x·y)·(x·z) in every case. Exchanging x and y, then using commutativity of meet, yields the cycloid equation. Every printed axiom is now verified.

No infinite meet, join, distributive law, well-order, cancellation, or bijectivity of an individual translation occurs in this argument. Injectivity of the assignment a↦T_a in the necessity proof is not being confused with injectivity of each map T_a.

## Infinite and nondistributive cases

The proof genuinely covers infinite meet-semilattices without joins. For a concrete example, take elements 0,a,b,e and c_n for nonnegative integers n. Let a and b be incomparable, put 0<a,b<c_n<e for every n, and let c_(n+1)<c_n. Meets exist: a∧b=0, c_m∧c_n=c_max(m,n), and the other meets follow from comparability. But a and b have no join, since their common upper bounds are e and the descending chain of all c_n, with no least member. The construction applies unchanged.

A greatest element does not imply a least element for an infinite meet-semilattice: the chain of nonpositive integers has greatest element 0, the binary meet is minimum, and there is no least element. The construction applies there as well.

Finite nondistributive cases are covered both algebraically and by the separate finite checks below. In particular the five-element diamond M3 passes all axioms. Thus no hidden distributivity condition is present.

## Problem 10 is a different operation

The printed Problem 10 on p. 546 uses the second-branch output y. The operation audited here uses x∧y. They coincide on chains, but not on arbitrary meet-semilattices.

For the four-element Boolean lattice with bottom 0, top e, and atoms a,b, the Problem 10 operation has

a·(a∧b)=a·0=0,

while

(a·a)∧(a·b)=e∧b=b.

Thus that operation fails the first semibrace equation on this lattice. This is a verified negative control, not a failure of the new construction. The candidate states this distinction correctly.

## Supplementary finite verification

The supplementary verification program independently generates all naturally labelled partial orders on up to six elements, retains exactly those having pairwise meets, and constructs the operations directly. Every finite partial order admits a natural labelling, so every isomorphism class in this size range is represented; multiple labelings are not deduplicated.

The numbers of retained semilattices for sizes 1 through 6 were 1, 1, 2, 7, 39, 320. The numbers with a greatest element were 1, 1, 1, 2, 7, 39. The program verifies the meet laws, all four semibrace equations for right projection at every choice of e, all L-algebra and semibrace equations for the proposed construction, and equality of the two orders. In total it checks 2,152 pointed projection structures and 51 instances of the new construction, plus an explicit separate M3 case.

As an independent necessity stress check, it examines every multiplication table satisfying the unit, diagonal, and absorption L-algebra identities for every e and every retained semilattice through size four. It checks 114,745 tables. Every table also satisfying the remaining joint axioms has e greatest and equal logical/meet orders. There are 18 retained joint structures across these naturally labelled test inputs. This is not a count of isomorphism classes of L-algebras.

The Boolean negative control fails meet preservation exactly as expected. Ordinary Python and Python with optimization (-O) produce identical JSON output; the script uses explicit exceptions rather than optimization-dependent assert statements. These tests supplement the universal proof and are not its basis.

## Final limitations and handling

The frozen manuscript and its input source were not altered. The mathematical result is an existence classification, not a classification of all operations and not a statement about self-similarity, nondegeneracy, or other unstated restrictions. The scope qualification concerning the printed axioms should stay visible wherever the result is summarized.
