# Source reconstruction and bounded status assessment

## The actual question

The catalog item corresponds to Question 6 in Valentina Di Proietto's contribution, pp. 1790–1792 of Oberwolfach Report 32/2014. Question 4 asks universal exactness; Theorem 5 immediately records its failure. Question 6 asks which coefficients are exact and states an expectation for geometric coefficients. The report is volume-year 2014 and was published on 2015-05-15. Its exact question number is 6; `OWR-13102-007` is the catalog identifier.

This is a cohomological invariant-cycles question. There is no Tannakian fundamental-group exact sequence in the relevant contribution. Substituting a homotopy exactness theorem would address a different problem.

Source: https://ems.press/journals/owr/articles/13102.

## Hypotheses that must not disappear

The report uses a perfect field k of positive characteristic, W=W(k), and fraction field K. The special fiber is connected, has at least two components, and has k-rational nodes. The full journal article works with a proper strictly semistable curve over a complete mixed-characteristic DVR V, smooth irreducible components, and k-rational nodes; it distinguishes K0=Frac W(k) from K=Frac V. The properness assumption is essential to the cited theorem's scope and is retained in the proof.

E is defined on the underlying special-fiber scheme without a log structure. Its associated log coefficient is used for log-crystalline/Hyodo–Kato cohomology. A general log-isocrystal with singular residues is outside this argument. No rational basepoint of the generic curve is imposed. The rational-point condition concerns nodes.

Source: https://doi.org/10.1515/crelle-2013-0117, Sections 1–3.

## Existing positive and negative results

The same article proves the trivial-coefficient theorem over perfect residue fields, injectivity and inclusion in the monodromy kernel generally, and a sufficient non-exactness criterion for unipotent extensions. In its Theorem 10, a nonzero Frobenius-compatible extension class for 0 -> E -> F -> O -> 0 lying in im(N_E), with exactness already known for E, produces a one-dimensional defect for F. Its Appendix A treats a Tate curve. These are established results, not solutions first obtained here. A Frobenius-compatible extension must not be inferred from an arbitrary cohomology vector.

The source's Appendix A contains a broad sentence about every class yielding an F-extension; the surrounding text explicitly uses Frobenius fixedness. This package retains that qualification and does not rely on the broad sentence.

## Later literature checked and why it does not close this task

- Yi-Tao Wu, *On the p-adic local invariant cycle theorem*, https://arxiv.org/abs/1511.08323. The inspected Theorem 1.1 concerns slope [0,1) for the ordinary-coefficient specialization map over a finite residue field. This does not classify arbitrary E in the present problem.
- Federico Binda and Alberto Vezzani, *A motivic approach to rational p-adic cohomologies*, https://arxiv.org/abs/2508.16196. The inspected Section 4.5 distinguishes chain complexes from exact sequences. Corollary 4.43 constructs complexes; Remark 4.44 gives exactness under weight-monodromy for ordinary cohomology. Theorem 4.35 is a complex Kähler statement. None of these inspected statements directly supplies the requested coefficient classification.

These are bounded scope checks, not a claim that no relevant theorem exists elsewhere. No claim of novelty or exhaustive current open status follows from unsuccessful searches.

## Outcome and stopping point

The deliverable proves a defect reduction and a complete answer for the stated cycle/local-triviality subclass. Its general map D still encodes component Gysin data. No general purity criterion, characterization of geometric-origin coefficients, or full solution is claimed. The broad problem remains unresolved by this investigation.

At most five substantive approaches were used: source/prior-attempt reconstruction; residue-factorization defect analysis; the local Gysin rank criterion; the cycle holonomy calculation; and a bounded later-literature/weight-theory scope check. The last approach was stopped without promoting a conditional result to an unconditional theorem.

No executable mathematics checker accompanies this package. The proof is symbolic and the checks are hand-verifiable exact identities. The independent audit accepted the stated partial results after the documented terminology correction and Gysin-hypothesis clarification. The disclosed approach count is five; the package does not contain a chronological research log independently proving that no additional approach occurred.
