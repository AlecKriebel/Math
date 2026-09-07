# Independent coefficient-rendering equivalence check

Review timestamp: 2026-09-07 03:46 UTC. Bounded check completion: 100%.

Verdict: the prior ambiguous-fraction finding is closed. No new finding arose
from this check of the actual shipped certificate expressions.

The target is commit `953c836a12b9d9d474521feb4a96e218c1155203`, compared with
`94d5177485b9680be8b77f13448abf1f923963e8`. The exact JSON certificate objects
for all four tables are unchanged. Independently parsing all 218 TeX table rows
in each release confirms their coefficients and exponent order agree with the
corresponding JSON data. The row counts are 35, 77, 22, and 84.

Exactly 50 row expressions changed. Every change preserves the intended exact
polynomial coefficient. For example, `8281/8100A` becomes `8281A/8100`; the
new expression makes the variable's position in the numerator explicit.
No expression of the old ambiguous form remains in the current tables.
No malformed shipped expression was encountered by the restricted parser.

The independent checker uses Python's exact `Fraction` arithmetic and an
explicit restricted grammar. It imports no repository generator, verifier, or
symbolic-expression parser. Legacy notation is interpreted according to the
coefficient-times-variable meaning fixed by the unchanged JSON coefficients.
The current grammar requires the expected coefficient variable (`U` or `A`)
and accepts the new numerator-monomial form. Negative controls independently
reject restored ambiguous notation, a changed numerator, and replacement of
`A` with `U`.

All five current table copies are byte-identical: canonical, portable
repository, arXiv source, bioRxiv source, and SIADS source. `RESULTS.json`
records their hashes and all 50 before/after expressions.

This check establishes exact semantics of the shipped table source. It does
not independently rerender or visually inspect the PDFs, test arbitrary
unshipped coefficient schemas, or substitute for the main certificate identity
verification undertaken elsewhere in this round.

Reproduce with Python 3 and no third-party dependencies:

```sh
python3 check_render_equivalence.py
```

The script expects this audit's clean `source_snapshot` and the two commits
available in the parent Git repository. It writes only its local result file.
