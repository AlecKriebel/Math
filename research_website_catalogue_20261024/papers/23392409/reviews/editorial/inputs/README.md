# Five outgoing centers in a 16-realization cube move

Alec Kriebel · ORCID0009-0001-9320-500X · 15October2026 · CC BY4.0

This research note proves an exact at-least-five counterexample to the three-center expectation in Melotti–Ramassamy–Thévenin, Remark4.8. Six fixed algebraic boundary points admit an incoming alpha16 realization and at least five distinct outgoing centers. Crossings are permitted; the boundary itself crosses, so this is not a proper embedding. The exact total center count, global maximum and alpha<1 are outside the result. The previously studied weighted-cost/p-power curve family is fully credited. A bounded literature check located no earlier pure-power four-intersection counterexample in its checked corpus; historical priority and firstness remain unestablished. AI tools were used extensively. The note is unrefereed and has not received conventional human peer review.

## Reproduce

Run `python3 verify_five_centers.py` beside `exact_certificate.json`. The standard-library-only verifier recomputes the complete exact rational certificate, compares it and writes no files. No network or external package is required. To regenerate deliberately in a writable copy, use `--write-certificate`. The final outgoing cutpoint is10^16, with an analytic concavity bound; five strict IVT sign changes establish at least five centers without a root-uniqueness assumption. The manuscript supplies the exact algebraic distance equivalence, boundary-root uniqueness, incoming IVT and all six symbolic face identities. No equality is inferred from an interval merely containing zero. Internal condition counts are bookkeeping, not independent mathematical propositions.

The PDF is the note; `five_centers.tex` is its standalone source. The ZIP contains the same source, verifier, exact certificate, this README, reference metadata, successful verification output, mathematical audit reports/certificates and bounded priority evidence. Mathematical audits used an earlier10^17 final cutpoint and independently derived the10^16 analytic endpoint; their original records remain labeled historical audit evidence. AI adversarial checks are not conventional human peer review. Primary-source PDFs and derivatives, private state, credentials and unrelated work are excluded.

## License

CC BY4.0 covers the note and its original supporting artifacts; linked third-party works retain their own rights. See LICENSE.txt.
