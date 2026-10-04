# Genus-one admissible-cover Hodge integrals

A source-based answer to Pandharipande's 2023 Question 2, catalogue ID 30005558 / OWR-13750339-002.

For connected degree-d covers with 2n ordered simple branch points,

\[
\int\lambda_{n+1}\lambda_{n-1}
=\frac{|B_{2n}|}{48n}\bigl(\sigma_{2n+1}(d)-\sigma_1(d)\bigr).
\]

The result follows from Iribar López–Pandharipande–Tseng's 2025 divisor theorem after an explicit connected-cover extraction. This is an exposition and deduction from existing work, not a claim of a new solution.

- `PROOF.md`: statement, rational function, normalization, and proof
- `SOURCE_GATE.md`: exact primary sources, updates, conventions, and dependency limits
- `ATTEMPTS.md`: mathematical attempt and the rejected disconnected-cover shortcut
- `verify.py`: exact algebra checks; Python 3 and SymPy required
- `verification.json`: recorded check output
- `SHA256SUMS`: hashes of the distributable files

Run `python verify.py` and compare its JSON output to `verification.json`. Run `sha256sum -c SHA256SUMS` to check the frozen files. The verifier does not formally verify the geometric theorems. AI-assisted and unrefereed.
