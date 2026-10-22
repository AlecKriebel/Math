# PR #1205: independent exact polyhedral audit

Checkpoint: 2026-10-17 09:30 America/Los_Angeles (16:30 UTC).
Audit completion estimate: 100% of this assigned mathematical/polyhedral review;
publication and priority review are outside this checkpoint.

Decision: **No mathematical defect found in the claimed counterexample to the
original canonical-W converse.** This finding is confined to the explicit D4
example and the original W-coordinate assertion. It is not a priority verdict,
and it does not settle the later string-coordinate converse.

## Exact claim and independence

The testable claim is that the specified reduced-word canonical potential for
Spin_8(C) has 22 combined monomials, all coefficient 1, with two X_6 exponents
equal to -2, while its complete monomial inequality presentation is irredundant.
The source conventions, canonical normalization and chamber map must identify
the actual potential: merely choosing any polynomial for the same cone would
not suffice.

I read the submitted PROOF.md, AUDIT.md and ACCEPTANCE.md. I wrote verify.py from
scratch using only Python's standard library. No candidate program, historical
verifier, machine certificate JSON, LP solver or floating arithmetic was
imported. The proof and audit tables were parsed only as inert comparison data.
I did see the candidate before implementing the review; this review does not
claim pre-candidate discovery or a sealed independent reconstruction. The
independence here is a separate implementation of the defining algebra and
checks, not independence of knowing the proposed example or its fixed routes.

## Checkable results

1. The root system was enumerated independently by closure under all four
   simple reflections. It has 24 roots and 12 positive roots. The word's 12
   inversion roots equal that positive-root set without repetition; the Weyl
   matrix is -I_4. Thus this is genuinely a reduced word for w_0.
2. The quiver was generated from occurrences and D4 adjacency, rather than
   loaded from a candidate adjacency matrix. Its complete 16-arrow set and
   frozen positions 7,9,11,12 agree with the prose.
3. All four fixed-label mutation routes mutate only mutable positions and end
   with the relevant frozen row nonpositive at every mutable column. Exact
   reverse pullback of the optimized frozen monomial gives the stated four
   summands with 14,5,2,1 terms. The pullback engine expands Laurent polynomial
   numerators over Z and performs exact division by powers of 1+y_k. A
   nonzero remainder raises an exception. It agrees identically with the
   independently assembled factored formula, not just at sample points.
4. Both prose supports equal this reconstructed polynomial after combining
   equal exponents. There are precisely 22 distinct terms, every coefficient
   is 1, and precisely PROOF rows 21 and 22 have exponent 2 at y_6. No omitted
   coefficient or cross-summand merger explains the squared variable.
5. All 484 products for the PROOF separator table pass. Separately, all 484
   products for the different AUDIT indexing/sign convention pass. Each
   selected inequality evaluates to -1 and every other inequality evaluates
   nonnegatively. These are exact integer certificates over the reals, not
   numerical feasibility claims.
6. The support has exact rational rank 12. With

       u = (0,0,0,0,0,0,1,0,1,0,1,1),

   every exponent row a has a.u=1. Hence the cone in z=-x coordinates is
   full-dimensional. Its lineality is ker(A), of dimension 0. It is pointed.
7. There is an additional concise facet certificate not stated in the
   submission. For each submitted PROOF separator z_j, put p_j=z_j+u. Then
   a_j.p_j=0 and every other a_r.p_j is at least 1. Thus p_j is in the
   relative interior of the indicated facet. The verifier also constructs
   11 rationally independent tangent directions in a_j-perp for every row.
   By continuity, a neighborhood of p_j in that hyperplane satisfies all
   other inequalities strictly. Consequently all 22 distinct facets have
   dimension 11. This strengthens, rather than assumes, the irredundancy
   argument. All p_j are recorded in results.json.
8. The chamber exponent matrix K is upper triangular with diagonal 1 and
   determinant 1. Multiplication a -> aK gives 22 rows whose entries are all
   -1,0,1. In particular the two squared terms pull back to
   x_2*x_4*x_6/x_7 and x_1. This is an integral monomial isomorphism; it
   preserves the cone presentation and its nonredundancy, but demonstrably
   changes the exponent bound in this example.

The interior point u is allowed to have zero mutable coordinates: the
tropical X-cocharacter space is R^12, with no extra coordinate positivity
constraints. Introducing such constraints without transporting them would
change the problem. All four canonical summands are included; no argument
about only a proper subsystem is used.

## Adversarial controls and reproduction

Run from this directory or anywhere in the checkout:

    python3 /Users/alec/Documents/Math/draft_pr_actual_outcomes_1200_1300_20261017/audits/pr1205_30004665/reviews/polyhedral_family/verify.py

The verifier rejected all 30 negative controls: a changed combined coefficient,
a missing squared term, clamping exponent 2 to 1, reversing exponent-row signs,
22 separately zeroed separators, reversing horizontal arrow 1->7, omitting the
last frozen-7 optimizing mutation, changing the last word letter, and accepting
a non-Laurent quotient 1/(1+y_6). The corrupted quiver and truncated route are
actually replayed and rejected; they are not just compared as unequal inputs.
The division implementation has a positive exact cancellation fixture too.

As supplementary implementation controls, each mutable matrix mutation is
checked to be involutive. Its rational coordinate formula is tested twice on
three exact positive rational vectors. Twelve exact forward-route evaluations
also agree with the full symbolic reverse pullbacks. These sampled checks are
only controls; the symbolic identities and complete finite certificates above
are what establish this candidate's conclusions.

Normal, -O and -OO executions all pass, using explicit exceptions rather than
assertions. receipt.json records Python version, verifier hash and all three
runs. All runs generated byte-identical results.json, SHA-256
04a8e276fed130d648eb3b3f7be19e2e1c38196c615c57247c1541652de0ab47.
The result file includes both complete dot-product matrices, root data,
canonical support and coefficients, optimizing endpoint rows, full K matrix,
transformed support, facet points and rejected controls.

## Primary-source scope checks

The [OWR report](https://ems.press/content/serial-article-files/46898), printed
pp.1124–1125, defines redundancy by deletion and explicitly places its exponent
test on the canonical potential restricted to the dual cluster torus. It also
identifies the resulting cone with the string cone by a unimodular map. Thus
the candidate's original-coordinate counterexample addresses that assertion.

The [published Koshevoy–Schumann article](https://link.springer.com/article/10.1007/s10801-022-01144-z)
was inspected as publisher HTML, particularly equation (3), Definitions 7–10,
Proposition 5 and the proof of Theorem 2. The optimized monomial normalization,
mutation convention and chamber map agree. The proof does assert equivalence
of the two exponent bounds; this case disproves that assertion. No use of that
equivalence or Theorem 2 is needed in the present direct certificate proof.
Its sufficient theorem's conclusion is not refuted here. Publisher Definition
8 omits adjacency, so applying that text literally would give the wrong seed;
the candidate explicitly uses the established canonical adjacency rule.

[Genz–Koshevoy–Schumann, Section 4.2.2](https://arxiv.org/html/1711.07176v1)
supplies the adjacency condition on inclined edges and the arrow orientation.
That source has additional negative frozen indices for the graded setting;
the current potential uses the reduced ungraded torus, as in the later paper.
The stated specialization in Proposition 5 supplies that boundary. None of
the current certificate calculations assumes that an arbitrary torus
isomorphism preserves coordinatewise exponent bounds.

## Strongest conclusion and exact remaining gap

The explicit candidate is a complete exact counterexample to the original
canonical-W exponent-bound converse. Within the stated source conventions,
there is no remaining mathematical gap identified by this family. A concise
note can carry this result with its complete polynomial, seed/routes and
integer certificate table. The new standalone verifier can accompany it so
that historical verification narratives are not required for reproducibility.

This family did not perform a priority survey, establish present-day novelty,
review the historical corrected comparison example, or authenticate any
unprovided historical machine inventory. It does not settle the later
varsigma-coordinate converse, refute the coefficient conjecture, or prove or
disprove the general sufficient theorem. Those boundaries must remain explicit
in any publication and in the repository outcome.
