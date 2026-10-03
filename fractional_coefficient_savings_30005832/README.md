# Verified fractional-coefficient savings in cardinality-adder CNFs

For problem 30005832 / OWR-14298166-010, this packet proves an explicit unbounded `Omega(N/log N)` fractional-coefficient advantage in the normalized Boolean Nullstellensatz mass convention. The CNFs have linear size and bounded width. Fractional mass is `O(log N)`; arbitrary-real support and integer mass are `Omega(N)`.

The complete independent adversarial AI review is **PASS, qualified**. There is no missing step in the quantitative theorem. The conservative `unsolved, 5/5` campaign label records that the original question's qualitative naturalness and historical closure are not certified. The original question does **not** require a superpolynomial gap. No novelty or human peer-review claim is made.

Read [RELEASE_SCOPE.md](RELEASE_SCOPE.md) first for the final interpretation and the audit's separately proved encoding-robustness observation.

## Files

- [Frozen full proof](public/PROOF.md)
- [Five approaches](public/APPROACHES.md)
- [Primary-source and attribution record](public/SOURCES.md)
- [Complete independent review](audit/AUDIT_REPORT.md)
- [Independent exact checks](audit/independent_checks.py) and [results](audit/independent_results.json)
- [Author exact checks](public/check_exact.py) and [results](public/exact_results.json)

The seven files in `public/`, including its manifest, and the four audit files are unchanged from the independently reviewed versions. Historical statements about review being pending in the frozen author record are superseded by the included completed review and this release note.

## Reproduction

From this directory:

```sh
python public/check_exact.py > /tmp/fractional-author-results.json
cmp /tmp/fractional-author-results.json public/exact_results.json
python audit/independent_checks.py > /tmp/fractional-independent-results.json
cmp /tmp/fractional-independent-results.json audit/independent_results.json
```

Both scripts use only Python's standard library and exact arithmetic. The author checks report 5,757 assertions. The independent checker verifies the original proof/manifest hashes before and after its work, reconstructs the circuit differently, checks the full generated polynomial identities through 2,048 inputs, and includes adversarial sign and all-degree weakening controls. These tests support the written general proof; they are not substitutes for it.

This is a draft research record for human review. It is not a merged change, journal-reviewed article, or DOI release.
