# Current editorial qualification — 17 October 2026

This edition retains the original submitted mathematical text below and adds current attribution and evidence qualifications. The full existence classification under the four equations printed in Dietzel, *Some problems on L-algebras*, OWR9/2023, Definition2 and Problem3, is accepted after fresh root verification, a genuinely source-only reconstruction and separate independent adversarial reviews. No all-products classification, self-similarity, cancellation, or extra unstated axiom is claimed. Under the separately attested meet-monoid convention both existence questions require a greatest element; that convention predates the workshop, including arXiv:2206.04955v1 (10June2022), Definition3.1.

**Prior construction credit.** The joint operation x·y=e for x≤y, and x·y=x∧y otherwise, is already printed by José Luis Castiglioni and Hernán Javier San Martín, *On a symmetrization of hemiimplicative semilattices*, arXiv:1611.09589v1 (29November2016), p7, Example3.5, formula(4). Their p2 defines bounded as having a greatest element; this formula needs no bottom or distributivity. The final publication is titled *l-Hemi-Implicative Semilattices*, Studia Logica106(2018),675–690, DOI10.1007/s11225-017-9759-3 (online3October2017). The version-pinned body and final bibliographic metadata are distinct evidence. This is attributed verification and deduction of the full printed existence answer, not a claim of a new solution, operation, mechanism, first combined statement, independent discovery or current worldwide openness. Earlier L-algebra and closure theory is due to Rump; the question is credited to Dietzel. Historical priority for an earlier explicit combined conclusion remains unestablished after a bounded audit, with missing earlier source bodies disclosed separately.

**Historical versus current evidence.** All eight submitted Git-authenticated files are retained verbatim in original_submitted/ of the verification package. The earlier6872-byte candidate,10375-byte audit and original finite-enumeration programs referred to in the submitted receipts were unavailable in this audit. Their hashes, old acceptance declarations, old counts and first-person statements below are historical records, not fresh certification of absent inputs or rerun results. Available public-side byte ranges were checked, but that does not authenticate missing old-side bytes. Fresh reproducible programs/results and independent review records are separately identified in the package. Any historical wording such as new refers to progress relative to an earlier partial candidate and grants no literature-priority claim. The original mathematical proof below remains an object of the current verification.

AI tools were used extensively for reconstruction, mathematical checking, computation, literature auditing and preparation. This work is unrefereed, with no external human peer review or formal proof certification. The present qualification governs the historical text that follows.

---

## Original submitted text, preserved verbatim

# Meet-semilattice realization under the printed semibrace axioms

Problem 30005434 (row 1694), Carsten Dietzel, *Some problems on L-algebras*, Oberwolfach Report 9/2023, printed pp. 544–547, Definition 1 on p. 544 and Definition 2 / Problem 3 on p. 545. Public primary source: <https://ems.press/content/serial-article-files/47003>.

This AI-assisted, unrefereed manuscript gives a complete algebraic construction, separate from the previously frozen partial candidate. No human or formal certification is claimed. It makes no assertion of historical novelty or of an author's unstated intent. The theorem concerns exactly the following stated axioms.

## 1. Axioms and classification

A meet-semilattice has an associative, commutative, idempotent binary operation ∧. Write x ≤ y if x∧y=x. Given a distinguished element e, the four printed semibrace axioms are

(S1) x·(y∧z)=(x·y)∧(x·z),

(S2) e·x=x,

(S3) (x∧y)·z=(x·y)·(x·z),

(S4) x·e=e.

The printed L-algebra axioms are

(L1) e·x=x and x·x=x·e=e,

(L2) (x·y)·(x·z)=(y·x)·(y·z),

(L3) x·y=y·x=e if and only if x=y.

**Theorem.**

1. Every nonempty meet-semilattice admits a distinguished element and multiplication satisfying (S1)–(S4), and the empty semilattice does not.
2. A meet-semilattice admits a distinguished element and multiplication satisfying both (S1)–(S4) and (L1)–(L3) if and only if it has a greatest element. In every such realization e is that greatest element, and the meet order equals the L-algebra order.

If the definition of semibrace additionally requires e to be the identity for ∧, both existence questions instead have exactly the meet-semilattices with a greatest element as their answer. No finiteness, bottom element, join operation, distributivity, completeness, or self-similarity is assumed.

## 2. The first part

On any nonempty meet-semilattice choose e and set x·y=y. In (S1), both sides are y∧z; (S2) reads e·x=x; in (S3), both sides are z; and (S4) reads x·e=e. Conversely, the required element e rules out the empty set.

This projection is an L-algebra only on a singleton, because x·x=x must equal e. If e must also be the meet identity, choose the greatest element; a meet identity is equivalent to a greatest element.

## 3. Necessity in the second part

Assume (S1)–(S4) and (L1)–(L3). First, equal left translations imply equal elements. Indeed, if a·z=b·z for every z, substituting z=a and z=b gives b·a=e=a·b. Then (L3) gives a=b.

For every x,z, axioms (S3), (S4), and (S2) give

(x∧e)·z=(x·e)·(x·z)=e·(x·z)=x·z.

The left translations of x∧e and x coincide, so x∧e=x. Hence e is greatest.

If x∧y=x, use z=y in (S3):

x·y=(x·y)·(x·y)=e.

Conversely, if x·y=e, then for every z,

(x∧y)·z=(x·y)·(x·z)=e·(x·z)=x·z,

and equality of left translations gives x∧y=x. Thus

x≤y ⇔ x∧y=x ⇔ x·y=e.

## 4. A construction on every meet-semilattice with a greatest element

Let e be the greatest element of a meet-semilattice X. Define

x·y = e, if x≤y;

x·y = x∧y, if x≰y.

This operation is defined on every ordered pair and takes its values in X.

### 4.1 Unit, diagonal, absorption, and antisymmetry

For y=e, e·e=e. For y≠e, e≰y and e·y=e∧y=y. Thus e·y=y. Since x≤x and x≤e, one has x·x=x·e=e.

Moreover, x·y=e implies x≤y: in the other branch x∧y=e would imply e≤x≤e and e≤y≤e, so x=y=e, contradicting x≰y. Therefore x·y=e exactly when x≤y, and mutual equality to e is equivalent to x=y by antisymmetry of the semilattice order. This proves (S2), (S4), (L1), and (L3).

### 4.2 Preservation of meets, (S1)

Fix x,y,z. There are three exhaustive cases, treating the middle case symmetrically.

- If x≤y and x≤z, then x≤y∧z. Both sides of (S1) equal e.
- If x≤y and x≰z, then x≰y∧z. The left side is x∧y∧z=x∧z; the right side is e∧(x∧z)=x∧z. Interchanging y,z gives the other mixed case.
- If x≰y and x≰z, then x≰y∧z. The left side is x∧y∧z, and the right side is (x∧y)∧(x∧z)=x∧y∧z.

Thus (S1) holds.

### 4.3 The semibrace identity, (S3)

If x≤y, then x∧y=x and x·y=e. The right side of (S3) is e·(x·z)=x·z, which equals the left side.

Now assume x≰y and put a=x∧y. Then a<x and x·y=a.

- If x≤z, then a≤z and x·z=e. Both sides of (S3) equal e: the left side is a·z=e and the right side is a·e=e.
- If x≰z, put b=x∧z. Then x·z=b and a≤b is equivalent to a≤z, because a≤x. If a≤z, then a≤b, and a·z=a·b=e. If a≰z, then a≰b, and a·z=a∧z while a·b=a∧b=a∧x∧z=a∧z. In either subcase the left side a·z equals the right side a·b.

This proves (S3) in every case.

### 4.4 The cycloid identity, (L2)

By (S3) and commutativity of ∧,

(x·y)·(x·z)=(x∧y)·z=(y∧x)·z=(y·x)·(y·z).

All four semibrace axioms and all three L-algebra axioms have now been verified. This proves sufficiency and the theorem.

## 5. Relation to the earlier partial candidate

On a chain, x≰y means y<x and x∧y=y, so the new operation specializes to the earlier top-chain example. Products of any existing examples remain examples by componentwise evaluation of the identities and the implication (L3). The new operation on a product need not equal the componentwise product operation; equality is neither claimed nor needed.

The different formula in Problem 10 of the workshop report, namely e for x≤y and y otherwise, must not be substituted on an arbitrary meet-semilattice. For example, in the four-element Boolean lattice with incomparable atoms a,b, that formula gives a·(a∧b)=0 but (a·a)∧(a·b)=e∧b=b. The new construction uses a∧b=0 in the second branch and avoids this failure.

## 6. Source convention and limits

The full Dietzel contribution was inspected, including all four printed pages. Its semilattice footnote requires associativity, commutativity, and idempotence; Definition 2 does not separately require e to be a meet identity. Problem 3 distinguishes the additional L-algebra condition. No nontriviality requirement is stated. The workshop's comment about a missing obvious trivial example is not an additional axiom, but it cautions against attributing unstated intent.

Dietzel, Menchón, and Vendramin, *On the enumeration of finite L-algebras*, Definition 3.1, instead require (X,∧,e) to be a commutative monoid before imposing the same four equations. See <https://arxiv.org/abs/2206.04955>, or the accepted author manuscript <https://cris.vub.be/ws/portalfiles/portal/106964011/96040919.pdf>. Restricted to semilattices, this convention requires a greatest element. The construction above satisfies this stronger convention too.

The theorem classifies which semilattices admit at least one such multiplication, not all possible multiplications, nor self-similar structures, braces involving groups, or structures with additional unstated axioms. No historical novelty claim is made.
