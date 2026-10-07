# Independent adversarial audit of group-theory candidates

2026-10-06 America/Los_Angeles. Review completion estimate 100% of requested transfer audit; upstream theorem correctness and exhaustive publication priority not verified.

## Kaplansky positive-characteristic idempotents: ACCEPT

Independently read source family197's NEW October4 torsion-free manuscript, `A-Torsion-Free-Group-Algebra-That-Is-Not-Directly-Finite-October-4-2026/build/sections/introduction.tex`, lines13–21. It truly states a finitely presented torsion-free G, a,b,c in F_2[G], ab=1, ac=0, c≠0, and a finite two-dimensional classifying complex. Thus there is no torsion or coefficient-field mismatch with the proposed idempotent counterexample. Do not use the earlier September23 example, which has odd-order torsion and a larger finite characteristic-two field.

Check e=1−ba: (ba)^2=b(ab)a=ba, so e²=e. If e=0, then c=bac=0, contradiction. If e=1, then ba=0; multiplying a(ba)=0 gives a=0 by ab=1, contradiction. Thus e is genuinely scalar and nontrivial. The construction works unchanged after every extension of F_2 because group-basis coefficients inject; no characteristic-zero/odd-characteristic conclusion.

For right modules, R=baR⊕eR, baR=bR, and left multiplication by b identifies R with bR, inverse left multiplication by a. Therefore R≅R⊕P for nonzero cyclic projective P=eR, and [P]=0 in K_0(R). This is a valid module cancellation statement; no implicit commutativity was used.

Corpus search for idempotent plus torsion-free/characteristic-two terms found no other statement of this consequence. Family207 concerns characteristic zero and explicitly leaves positive characteristic separate. The group C*-algebra projection problem is a different question, already a separate release result, and must not be conflated. Existing zero divisors source likewise does not automatically yield idempotents. The new direct-finiteness theorem supplies exactly the missing one-sided inverse.

Remaining issue: explicit numeric finite presentation/coefficient extraction may be work because upstream uses a probabilistic existence construction. Do not call the presentation an already-extracted explicit certificate. This affects packaging, not the short existential implication. Independent mathematical originality of implication is tiny; theorem-impact can still be high.

## Thompson F/T C*-simplicity package: ACCEPT

Independently read #248 introduction and full consequences section. Main theorem says the standard Thompson F is nonamenable; already-stated consequences cover nonunitarizability and percolation, not C*-simplicity. Intro mentions only the older direction T C*-simple⇒F nonamenable.

Independently checked primary Le Boudec–Matte Bon article full text, https://arxiv.org/html/1605.01651 , Theorem4.1, Corollary4.2, Theorem4.3, Corollary4.4. Exact results:

- F nonamenable iff F is C*-simple iff T is C*-simple (Cor4.2).
- Nonamenable F implies C*-simplicity for every COUNTABLE subgroup of Homeo(S1) containing the STANDARD F (Thm4.1).
- The real-line version uses the conjugate of standard F specified immediately before Thm4.3, not an arbitrary abstract embedding whose support leaves an interval untouched.
- F nonamenable iff Aut(F) is C*-simple iff abstract Comm(F) is C*-simple (Cor4.4).

Thus all proposed named-group conclusions match without additional group hypotheses. Unique trace follows from C*-simplicity⇒trivial amenable radical plus the unique-trace characterization; the article introduction lines104–106 records both facts. Do not confuse reduced with full group C*-algebra: full C*(G) has the trivial character for every group and is not what is asserted. Do not claim new results for V/nV, already known within the same 2016 paper. C*-simplicity is not ordinary abstract-group simplicity; F has proper normal subgroups.

Remaining work is exact theorem-chain attribution and optional boundary/representation corollaries, not a new analytic proof. The central equivalence is established literature, so frame as applying the new nonamenability input.
