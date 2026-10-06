# Nonconvexity of fixed odd-power sum-of-squares cones

Alec Kriebel · Independent researcher · ORCID 0009-0001-9320-500X

The research note answers the original general-dimensional fixed odd-power convexity question negatively. It gives an explicit sextic cube counterexample in 3·10^62 variables and proves that every fixed odd q≥3 has a counterexample in some finite dimension depending on q. See CLAIM_SCOPE.md for the precise limits and PRIORITY_NOTE.md for classical credits and the dated audit's coverage gaps.

The companion PDF is the manuscript. This archive supplies its standalone editable paper.tex and an exact finite certificate with a portable checker. It contains no third-party paper PDFs, downloaded dependencies, credentials or network requirement.

With Python 3.9 or later, from the extracted archive folder run:

```sh
python3 -E -B verify_package.py
```

The verifier checks every manifest-listed full file, executes the standard-library-only certificate checker in an isolated child process, and compares its complete output with verification/expected_output.json. A successful run prints PASS. To inspect just the mathematics computation, run:

```sh
python3 -E -B verification/check_certificate.py
```

The local matrix has 220 monomials and eight parity blocks of at most 35 rows. The checks use integers and exact rational fractions. The immense finite tensor product is handled by the written algebraic argument; no matrix with 10^62 blocks is constructed. The computation verifies the local certificate and explicit cubic obstruction. It does not replace the written product/separation/general-odd-power proof or establish historical novelty. The manifest detects accidental changes and is not an independent digital signature.

AI tools were used extensively in derivation, source comparison, reproduction, writing and adversarial verification. This is an unrefereed preprint without human peer review or a formal proof-assistant certificate. The original research and subsequent audit are preserved in the [immutable original repository snapshot](https://github.com/AlecKriebel/Math/tree/c0c88b18db237e97a0bddbf28a6d4fdd52af5522/unsolved_math_prioritization/attempts/30005460). License: Creative Commons Attribution 4.0 International (CC BY 4.0).
