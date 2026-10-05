# Borel aperiodic versus hyper-aperiodic SFT colorings

Problem 30004996 / OWR-9790354-007. Status: **unsolved**.

This is a five-approach research and obstruction report, not a proof or counterexample to the full problem. The main remaining issue is a Borel map into one compact free subshift of the original SFT, with the original output alphabet.

The packet proves elementary reductions and scope checks. It also gives a restricted compact-subshift consequence: when every nonidentity group element has infinite centralizer, the assumed Borel aperiodic coloring implies that the target contains a nonempty compact free subshift. That deduction uses Bernshteyn and Frisch's 2025 preprint. It does **not** establish the needed Borel map into that subshift, and no novelty claim is made.

- `analysis.md`: exact scope, five approaches, rigorous partial results and failed-route counterexamples
- `source_map.md`: public references, exact locations, and inspection limits
- `research_log.md`: five substantive approaches and completion assessment
- `result.json`: classification and explicit gap
- `verify.py`, `controls.json`: reproducible finite consistency checks
- `verification_metadata.json`: hashes and retrieval metadata, without source contents

Run `python3 verify.py` and compare stdout with `controls.json`. These finite controls check identities and counterexample mechanisms; they do not settle the infinite Borel existence question.
