# Research log

All times UTC, 2026-10-04. No remote writes were made.

## 17:09-17:11: readiness and source audit

The live queue names rank 659, ID 30000700 / OWR-1460-004, queued with 0/5 turns. Matching branch, pull request, and attempt-directory searches returned no actual prior attempt. The related-target-groups file contains no matching ID. The fallback research-results corpus contains no OWR-keyed entry, so no prior report was silently assumed.

The live catalogue page was inaccessible (web error and HTTP 403). The fallback record was inspected, then the authoritative publisher's complete OWR PDF was downloaded. Fang's entire contribution, printed pp. 501-503, was read; the relevant p. 503 was rendered and visually inspected. The conclusion has additive term ((c-1)/c)a. Theorem H places no nonzero restriction on a, whereas neighboring Theorem 3 explicitly does.

Completion estimate: source identification 100%; mathematical question at this checkpoint not yet independently audited.

## 17:11: first substantive approach, polynomial boundary construction

Mechanism: exploit the exact allowed zero shared value, preserving equality of zero sets while dropping equality of multiplicities. The example f=z^2/2, a=0, b=1, k=2 passes both hypotheses and has a zero, excluding every permitted exponential conclusion.

Outcome: complete candidate negative answer to the universal statement in the primary report and to the catalogue statement. It is not a counterexample manufactured from the catalogue's transcription error. The five-approach requirement stops at this complete counterexample; no artificial unsuccessful approaches are counted.

Completion estimate: 100% of the printed universal yes/no implication has a self-contained candidate refutation; independent verification and novelty assessment are not complete.

## 17:12-17:14: robustness and exhaustive polynomial analysis

Validation extension A: all polynomial examples are classified. For a != 0, every f-a root is simple and root counting contradicts the degree of f'-a. For a=0, matching zero sets force f=A(z-z0)^n; the b-condition and roots of unity force n=k and A=b/k!.

Validation extension B: a transcendental family rules out repairing the zero-value failure merely by requiring transcendence. For k>=3, choose lambda^(k-1)=-1/(2^(k-1)-2) and f=(exp(lambda z)-1)^2. Its nonempty b-fiber for b=-lambda/2 consists of exp(lambda z)=1/2, at which f^(k)=b. All such f have infinitely many zeros, excluding the conclusion.

These are robustness checks of the complete negative answer, not an assertion of resolving the distinct problem with a != 0.

## 17:14-17:18: literature, controls, and limitations

The complete Feng Lu 2010 nine-page article was read. It concerns two antecedents at the same nonzero value and is not substituted for the distinct-b hypothesis. Chang-Fang 2007 was checked through its authoritative publisher abstract; its full text was not obtained. Fang-Zalcman 2003's title/DOI and publisher abstract were found; direct article/PDF access returned HTTP 403. The catalogue's CiteSeer link failed (timeout/HTTP 502) and its other ScienceDirect link returned HTTP 403. These failures are preserved as limitations, not disguised as full-text reviews.

Exact controls passed for the smallest example, 1,703 polynomial degree/order/coefficient cases, and 22 transcendental derivative-order identities. Wrong orders/coefficients, the wrong lambda relation, and replacing the b-value implication with a multiplicity demand were checked as negative controls.

No published exact resolution or prior use of these particular formulas was verified. The mathematical refutation is self-contained, but bibliographic novelty is unestablished and no novelty is claimed. The genuinely strengthened a != 0 formulation remains unresolved here.

## Frozen result

One substantive proof-attempt response, complete counterexample found before five approaches were needed. Candidate status only, pending fresh independent audit. The packet contains authored mathematics, executable exact checks, and verification metadata. Scholarly material and corpus bytes remain outside the packet. No PR, branch, commit, push, email, or external contact was created.
