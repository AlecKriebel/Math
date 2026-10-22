# Independent adversarial review: Hopf finite ideals and image ideals

PR: #1102. Problem: 30006658.
Review checkpoint: 2026-10-17T16:30:58Z (09:30:58 America/Los_Angeles).
Assigned audit completion estimate: **100%**. Overall PR review/publication
completion is outside this review's scope.

**Verdict within assigned scope: PASS. No required mathematical correction
found in Lemma 1 or Proposition 3's algebraic image-ideal argument.**
This is an AI-assisted, unrefereed adversarial check, not human peer review
or formal proof certification. It does not certify the topological inputs
or priority of the resulting theorem.

## Independence and inspected input

The sole mathematical input read initially was the pinned
`input/MATHEMATICAL_REPORT.md`. The independent proof reconstruction was
saved in `INDEPENDENT_DERIVATION.md` before reading the earlier
`input/MATHEMATICAL_AUDIT.md`. The latter was read only after that record
and the separate exact convention check existed. Its conclusions agree
with the independently derived algebra conclusions. `ACCEPTANCE.json`
was not needed or read. No other current reviewer was consulted.

Pinned report: 15,361 bytes; SHA-256
`c985406f6b9b456a220baecc70f836dd98bb0ba950a153b08e35e5677ff8b23b`.

## Exact claim and strongest verified result

For an arbitrary field k, an infinite-dimensional integer-graded Hopf
algebra H in the Koszul-sign symmetric category has no nonzero
finite-dimensional graded left ideal and no such right ideal. Neither
bijectivity of the antipode, connected grading, finite-dimensional graded
pieces, commutativity, nor cocommutativity is required.

Consequently, if a map of left A-modules P->A has finite-dimensional total
homology and H_*(A) admits such a Hopf structure, its homology map is zero.
If each homology class of M is represented through such a P, every
A-linear map M->A is zero on homology. This is exactly the algebraic
mechanism of Proposition 3, conditional on the finite-approximation
input in Lemma 2.

The checkable symbolic derivation is in `INDEPENDENT_DERIVATION.md`.
It includes a shorter independent proof of the ordinary finite-ideal
step: the finite right ideal's coefficient envelope J is a finite
right ideal/right coideal; a nonzero such J has epsilon(J) nonzero;
the antipode identity then puts 1 in J, forcing J=B. Thus no hidden
inverse-antipode requirement can enter through an imported theorem.

## Mechanisms, evidence, and gaps

| Mechanism | Adversarial concern | Evidence and status | Exact remaining gap |
|---|---|---|---|
| Finite coefficient envelope | Could the dual slices produce an infinite space or lose the coideal condition? | Finitely many first-leg spans cover a basis of I; coassociativity proves Delta(J) subset J tensor B. Verified. | None. |
| Right ideal closure | Could the antipode be used in the wrong order? | Expanded identity is sum i_1 b_1 f(i_2 b_2 S(b_3)) = sum i_1 b f(i_2). Verified without S inverse. | None. |
| Left/right transfer | Could opposite algebra require bijective S? | BOTH product and coproduct are reversed. B^(op,cop) is Hopf with the original S. Verified. | None. |
| Graded-to-ordinary reduction | Could odd-characteristic signs invalidate the ordinary theorem? | Parity bosonization product/coproduct signs and both antipode identities derived explicitly. Characteristic 2 ungrading is valid separately. Verified. | None. |
| Ideal embedding | Could I#kC2 fail on one side? | Multiplication on both sides preserves I because I is a graded one-sided ideal. Verified separately for each side. | None. |
| Proposition 3 | Is the image really an ideal and finite TOTAL dimension? | H_*(A)-linearity of the homology map gives ideal closure; finite total homology of P bounds the entire image. Verified. | Lemma 2's categorical factorization must hold; its topology/application is not certified by this algebra review. |

## Reproducible exact check

Run:

    python3 check_bosonization.py

The standard-library-only script implements the **infinite, noncommutative
free tensor Hopf superalgebra** on odd x,y and even t. Words are never
truncated during any operation. Only the lengths of tested inputs are
bounded. It checks the candidate's bosonization formulas over F2, F3,
and F5. For EACH field all checks passed:

* 512 associativity triples;
* 676 coproduct multiplicativity pairs;
* 80 coassociativity inputs with both counit equations;
* 80 inputs with both antipode equations;
* 208 left-ideal and 208 right-ideal sample products;
* one negative control detecting that ordinary ungrading fails in odd
  characteristic for two odd primitives and succeeds in characteristic 2.

The exact output is `bosonization_results.json`. These computations test
conventions and are not evidence by themselves for the infinite universal
assertion; that assertion is proved symbolically above.

## Primary-source cross-check

[Lomp, *Integrals in Hopf algebras over rings*, arXiv:math/0307046](https://arxiv.org/pdf/math/0307046),
Section 2.4, printed pp. 4–5, explicitly proves the finite one-sided ideal
criterion for free Hopf algebras over a commutative ring. Specializing the
coefficient ring to a field gives the ordinary theorem used here. Its
proof also uses the coefficient-envelope/Hopf-module mechanism. It credits
the field result to Sweedler. The candidate properly treats this as prior
mathematics. Inspected on 17 October 2026.

[Shibata–Wakao, *On classification of Hopf superalgebras of low dimension*, arXiv:2306.04122v2](https://arxiv.org/html/2306.04122v2),
Section 2.1, formulas (2.1)–(2.2), supplies the right Hopf-module
isomorphism without an antipode-bijectivity assumption. Theorem 2.2 gives
the bosonization formulas; its bijectivity assumption is on the BASE Hopf
algebra, which here is kC2 and has invertible antipode. It imposes no
bijectivity condition on the braided algebra's antipode. Inspected on
17 October 2026.

Source-convention warning: that source's displayed expanded antipode in
Section 4.1 has an apparent sign typo, giving (-1)^(i+|h|); at h=1,i=1
this sends a grouplike involution to its negative. The general Theorem
2.2 formula is correct. The candidate uses the correct unexpanded formula,
equivalent to (-1)^((i+|h|)|h|) S_H(h)#g^(i+|h|), and independently
satisfies both antipode identities. This warning requires no correction
to the candidate and no outreach was prepared or made.

No exhaustive priority audit was attempted. The finite-ideal result and
bosonization are established tools, not novelty candidates in this paper.

## Boundary and falsification checks

The antipode, field, and infinite-total-dimension hypotheses are real.
Removing the antipode allows the span of an absorbing monoid element to
be a one-dimensional ideal in an infinite-dimensional bialgebra. Finite
Hopf algebras themselves violate the conclusion. Ring coefficients can
also violate it, as Lomp's examples demonstrate. All those cases are
excluded by the candidate. An infinite-dimensional source M is permitted
because the factorization is class by class. Infinite dimension in each
degree is not required. No claim of nullity in the derived category is
made or justified; the conclusion is only the induced homology map.

**Unresolved objections within assigned scope: none.** The remaining
overall proof obligations are independent verification of compact-proxy
factorization, its applicability to completed loop chains, infinite
homology under non-p-nilpotence, original-question correspondence, and
priority. Those are explicitly outside this assigned algebra verdict.
