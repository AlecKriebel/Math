# Publication and independent verification

The supplied 14 September 2026 package is preserved byte for byte. Its README,
progress file, research log, PDF, and statements about no publication or review
describe the original package preparation. The original `SHA256SUMS` remains
valid for all 39 listed files; `independent_audit/IMPORTED_FILES.json` also records
the manifest itself, covering all 40 imported files.

The subsequent independent AI audit on 17 September 2026 UTC found the main
theorem, stronger proposition, numerical controls, and supporting computations
correct. Read [the verification report](independent_audit/VERIFICATION_REPORT.md)
and [publication research log](RESEARCH_LOG.md).

- [Public result page](https://aleckriebel.github.io/Math/papers/equal-sum-product/)
- [Original mathematical note](notes/equal_sum_product_note.pdf)
- [Direct proof review](independent_audit/proof_referee.md)
- [Independent alternate derivation](independent_audit/alternate_referee.md)
- [Computational review](independent_audit/computation_referee.md)

The result resolves the equal-common-sum/product conjecture attributed to Joseph
DeVincentis, under the original globally distinct positive-integer assumptions.
The statement that equality requires two rows assumes at least two columns.
Other smallest-entry questions on the source page and historical priority are
not settled by this package. These are internal AI reviews, not external peer
review or proof-assistant formalization.

From this folder, `python3 src/reproduce.py` reproduces the original checks and
refreshes the original logs. To retain their historical hashes, run it in a copy.
The added independent checks can be run from the repository root with
`python3 equal_sum_product/independent_audit/computation/independent_checks.py`.
The supplied code and PDF required no mathematical correction. A source comment
says “100-digit” where the actual probe and published documentation correctly
say 101-digit; this harmless typo is retained for provenance.
