# PR 124 / numeric10400231: independent literal-source and normalization audit

**Verdict: PASS_LITERAL_PRIMARY_SOURCE_SCOPE_AND_NORMALIZATION.** No mandatory source-scope or normalization correction was found in the authenticated `COUNTEREXAMPLE.md` (SHA-256 `483bc7e3dccd4d6d262d36341becdf05bfa22f7d52e721eae4f51ecdc0fb95e5`). This verdict does not certify its central topological proof, algebraic obstruction, complete refutation, novelty, or priority. It is an adversarial AI audit, not human peer review.

## Independence and evidence

The entire authenticated original `source_record.json` and `prior_imported_report.json` were read as input metadata. The original publisher PDF and both named supporting PDFs were then downloaded afresh, their full text extracted, and decisive full pages rendered and visually inspected. The literal claim and conventions were reconstructed before any candidate or old independent-review read. The preserved `PRIMARY_RECONSTRUCTION.json` checkpoint has SHA-256 `86772c90173c02fb7ca9b4940a8ae7329c424e548923c122643b29577b191ca7`.

The candidate was first read after this checkpoint. Only subsequently were `independent_review/REVIEW.md`, `source_verification.json`, and `review_summary.json` read for comparison. Their verdict is not a premise of this audit. The three freshly retrieved source PDF hashes match that old source receipt; this establishes byte agreement, not correctness by reviewer consensus. `PROVENANCE.json` records URLs, PDF hashes and sizes, actual executed download/extraction/render commands, observed warnings, inspected pages, and input hashes. Sources and derivatives are confined to ignored `private_sources/` and are not public manifest members.

## Literal target

The official [Ohtsuki collection](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf), Conjecture 12.26, printed page 542 / PDF page 170 / zero-based page 169, was checked with the complete surrounding PDF pages 168-171 (printed 540-543). The entire following remark is on the same decisive page; page 171 starts the bibliography, so there is no continuation qualifying the target.

The data are a rank-one finitely generated abelian group H and an integral polynomial in Z[H/Tors H]. The realization must have H1 isomorphic to H and be closed, connected, and oriented. The criterion is even-exponent reciprocity and augmentation plus or minus |Tors H|. The remark identifies trivial or cyclic torsion as known cases; it does not restrict the question to them or impose geometric restrictions.

The authenticated imported statement agrees with this scope. Its short title metadata is truncated, but the full statement's mathematical content is not weakened to a cardinality-only question.

## Normalization reconstruction

The target page names the Alexander polynomial and specifies its ring; it does **not** print a self-contained module-order definition. Accordingly, the identification with the conventional integral maximal-free-abelian Alexander order is independently corroborated, not falsely attributed to an explicit definition on that page.

[Massuyeau's Edinburgh author preprint](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/massu.pdf), *An introduction to the abelian Reidemeister torsion of three-dimensional manifolds*, is arXiv:1003.2517v1 (2010). Definition 3.1 on page 12 defines orders through elementary ideals. Definition 3.5 on page 13 and equation (3.2) on page 14 give the integral Z[G]-order of H1 of the maximal free abelian cover, G=H1/Tors H1. Units are plus or minus G. Theorem 4.4 and Definition 4.6 on page 19 distinguish Milnor torsion Delta/(t-1)^2 and maximal abelian torsion in the fractions of Z[H1]. Page 20 distinguishes its integral part in Z[H1].

[Alcaraz 1406.2042v1](https://arxiv.org/pdf/1406.2042v1), Section 2 on pages 3-4, independently uses integral absolute H1 of the universal free abelian cover and its zeroth order over the integral free group ring. This agrees with the candidate's convention. Rational coefficients appear later for a different proof purpose; page 16 explicitly relates the rational determinant to the integral polynomial by a scalar involving torsion factors. That scalar is harmless for degree/symmetry but is not an allowed integral unit in general.

A concrete normalization control is the integral constant polynomial 8 versus its primitive part 1: they represent the same rational unit class but different integral unit classes, and their augmentations differ. The submitted candidate has content one, so removing its primitive content alone would not change that particular polynomial; the convention is still essential for the determinant-to-polynomial bridge in its proof.

## Supporting source scope and candidate comparison

| Candidate feature | Assessment |
| --- | --- |
| H=Z direct-sum (Z/2)^3 | Within the independently reconstructed group scope. Equal cardinality with Z/8 does not imply isomorphism. |
| Delta=t+6+t^(-1) | Symmetric with exponent zero, augmentation 8, content one. The displayed conjectural conditions hold. |
| Integral finite cut torsion retained | Consistent with the source; no integral freeness assumption is borrowed. |
| No reliance on polynomial-only realization for the full H | Correct scope distinction. |
| Direct proof of square presentation and exact specialization | An independent proof burden, outside this family's certification. |

No exact statement mismatch was found. In particular, the candidate's stronger square-presentation and exact-specialization claims are presented as its own proof burden, rather than as the conclusion of Alcaraz Section 4.2. This audit leaves that burden to the independent mathematical proof families. It does not certify potentially problematic intermediate arguments elsewhere in Alcaraz; only the cited definitions, stated scope, and cut-surface context are used here.

## Checkable controls and limits

`verify_scope.py` uses explicit exceptions, with no correctness-critical Python assertions. Normal and optimized executions produce byte-identical receipts. It rejects twelve scope/borrowed-strength mutations, checks fifty sign/Laurent-unit variants, distinguishes equal-order nonisomorphic finite torsion groups, checks eleven prime-indexed family polynomials against the literal two source conditions, and verifies all three source hashes. Fifteen deliberately false claims were separately executed in both modes: all thirty runs fail with the intended explicit error, including cardinality substitution, refined torsion, rational coefficients, content removal, relaxed manifold assumptions, odd symmetry exponent, a polynomial-only theorem promoted to full-group realization, cut rank promoted to integral freeness, and a false PDF hash.

These controls are guards on the manually reconstructed source semantics and elementary normalization calculations. They are not machine proofs of the source reading, of the topological lemma, or of nonrealizability. The strongest verified conclusion of this family is that the candidate addresses the literal prescribed-pair conjecture using the matching integral polynomial convention and does not borrow a stronger prescribed-torsion claim from the cited polynomial-only theorem. No primary-source mismatch blocks the mathematical audit. The exact remaining promotion gap is independent validation of the candidate's proof and any subsequent, separately authorized priority assessment.

All work was confined to this audit family. No repository index/main/native candidate changes, commits, pushes, releases, PR operations, or external communications were performed.
