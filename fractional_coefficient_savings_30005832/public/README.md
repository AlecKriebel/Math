# 30005832: fractional coefficient savings

A conservatively scoped research packet for OWR-14298166-010.

- `PROOF.md`: a fully specified bounded-width, linear-size binary-adder cardinality family with rational Nullstellensatz mass `O(log N)` and arbitrary-real proof support / integer mass `Omega(N)`; proof-system and encoding caveats are explicit.
- `APPROACHES.md`: five substantive approaches, including a credited reconstruction and exact replication analysis of Potechin–Zhang's published finite example.
- `check_exact.py`: dependency-free exact arithmetic checks, including actual sparse polynomial expansion of generated certificates.
- `exact_results.json`: reproducible output of the checker.
- `SOURCES.md`: primary-source verification, prior attribution, and limited duplicate/literature search.

Run `python check_exact.py` from this directory. The script writes no files and prints JSON; compare its output to `exact_results.json`.

Status: quantitative partial result, original qualitative naturalness/intended-strength question not declared fully resolved. No bit-complexity or superpolynomial separation, historical priority, or human peer review claim. Independent adversarial review is pending at the author freeze.
