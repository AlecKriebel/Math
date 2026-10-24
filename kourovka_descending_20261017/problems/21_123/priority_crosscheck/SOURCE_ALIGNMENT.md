# Independent priority/source alignment for21.123

UTC: 2026-10-24T23:04Z. Priority/source audit completion estimate: **90%**, pending the final independent core-proof report. This file was written before reading any other agent's preparation conclusions. No original research result is claimed.

## Exact target rather than the abbreviated question

The official October20,2026 21st-edition text, printedp198, asks whether the extension specified by Smoktunowicz's Definition66 produces groups; it adds that a group answer would also produce a brace. The reference is JPAA229(12),2025,108128. The cited numbering occurs in the public arXiv version2410.20440v2, dated March29,2025. The accepted Edinburgh manuscript instead numbers the corresponding construction Definition26. These are different source versions and must not be cited as if their local formulas were byte-identical.

The mathematical domain is fixed through the invoked definitions: p>3, a finite pre-Lie ring A of additive cardinality p^n, and Property3. Put m=floor((p−1)/4). Property3 requires each right-nested product of m elements to belong to pA, and each product of m left multiplication operators to send ann(p^r) into p·ann(p^r) for every r≥1. The construction uses a section d:pA→A with pd(x)=x, factorial valuations s_j=v_p(j!), and intended protected factorial terms. It uses W and its inverse Ω to set

`a∘b=a+b+W(Ω(a),b)`.

This does not ask about arbitrary infinite pre-Lie rings, p=2 or3, arbitrary weakened annihilator hypotheses, or arbitrary proposed repairs of every misprinted formula. For p=5,7 one has m=1 and the first Property3 clause forces A=pA, hence A=0 by finiteness. These are not uncovered nontrivial prime cases.

## Version-specific correspondence

| Item | Public arXiv2410.20440v2 | Accepted Edinburgh manuscript |
| --- | --- | --- |
| Property3 | Definition59 | Definition18; same two substantive conditions |
| Factorial operators on A | Definition60; uses η_(s_j) in the displayed branch | Definition19; that exponent is changed to η_j |
| Branch statement | s_j-divisibility phrase followed by p∤j⇒s_j=0 | j-divisibility branch followed by the same p∤j⇒s_j=0 inconsistency |
| Pullback movement | Remark63; shield η_r=m v_p(r!) | Remark22; longer condition i≥r(p−1)/4 and a changed displayed identity |
| Unit recursion and unit terms | Self-referential recursion and η_(s_j) display | Corresponding defects remain in §4.1 |
| W sums | Bound index i with an unbound j in E_(j,a) | Same mismatch in Definition23 |
| Final operation | Definition66 | Definition26; same final W/Ω formula |

An arithmetic control illustrates the branch issue without interpreting author intent: at p=11,j=12 one has v_11(12!)=1 although11 does not divide12. Thus a literal assertion s_j=0 in that branch cannot hold. Also η_11=2 while η_(s_11)=η_1=0. These differences matter to a total prescription, but identifying them does not create a new open mathematical problem or a new solution.

The earlier Remark63 counterexample must **not** be presented as a counterexample to the changed accepted Remark22. This audit keeps the versions separate.

## Prior claim and its precise coverage

Natanael Wildner Fraga's [preprint v1](https://doi.org/10.20944/preprints202608.2109.v1), posted August28,2026, is explicit prior work on21.123. Its Theorem1 and Corollary5 treat the entire finite p-power Property3 class, with no homocyclic, rank, or n<p restriction. They give a canonical group/brace for an explicitly corrected factorial prescription, agree with every legal corrected literal evaluation, and describe why arbitrary section iterations can fail to be total. Formula-level comparisons explicitly use arXiv2410.20440v2, rather than purporting to quote the accepted manuscript. The page labels this version not peer-reviewed.

The following are different assertions, and only the appropriate ones can be credited to that result:

1. Every arbitrary section makes the unmodified printed strings a total operation. This is not its affirmative theorem; its elementary examples refute the relevant totality assertion.
2. A specified factorial-compatible correction has a canonical total group law for every ring under the original algebraic hypotheses. This is its affirmative theorem and is exactly the ordinary corrected mathematical target.
3. Whenever a fixed section makes all those corrected literal iterates legal, its operation equals that canonical group law. This is also expressly covered.
4. Every conceivable clarification of the source, or every unmodified formula in the accepted manuscript, has the same meaning. This is not established and is expressly not claimed.

This is substantial scope verification, not an absence search. No algebraic subclass allowed by the Notebook's invoked Property3 definition has been identified outside the prior affirmative theorem. Literal partiality, source-version discrepancies, and an unstarred Notebook listing cannot support an originality claim for rediscovering either the elementary diagnosis or the same corrected group law.

## Independent checks and remaining limits

`check_literal_diagnostics.py` independently reproduces already published section-domain examples for p=11,13,17,19,23, the old Remark63 example at p=11, and the factorial-index discrepancy. Its outputs are labelled prior reproductions, not new contributions. The corrected group law is not disproved by those checks.

A separate fresh reviewer is examining the protected operator calculus and affine BCH closure, rather than accepting the preprint's title as proof. Its provisional reconstruction found no hidden homocyclicity or extra nilpotency assumption: the block contraction and denominator budget follow from Property3. The rendered document contains exponent-grouping problems in some functional-calculus displays; their prose and proofs specify decreasing division order under multiplication by p and adding orders under products. These deserve an explicit source caveat, not silent certification that every displayed string is correct.

Provisional selection recommendation: **do not select21.123 for an original solution of the standard corrected construction.** There is direct prior complete-solution literature covering that mathematical target. If a record uses `already_solved`, annotate the corrected-prescription scope and the unreviewed-preprint status. Do not claim that an ambiguous, unmodified printed expression has been affirmed as a total group operation. A source clarification could further settle naming conventions; no external communication has been prepared or initiated.
