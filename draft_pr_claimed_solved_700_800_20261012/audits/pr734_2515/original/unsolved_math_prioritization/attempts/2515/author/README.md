# Kourovka Notebook 21.6: infinite counterexample

**Author conclusion:** negative answer for p=2, with a complete elementary proof. **Review status:** independent audit pending. This is not an editor-accepted solution and carries no novelty or priority claim.

The construction starts with a minimally transitive order-32 group on eight points that fails the cycle-support block property. A countable iterated imprimitive wreath tower preserves this local action. Any transitive subgroup of the union must induce the same bad eight-point action, ruling out the required subgroup.

Read [PROOFS.md](PROOFS.md), especially the block-obstruction transfer lemma and the checks of every infinite-domain hypothesis. The finite example alone is not being offered as the answer.

- [RESEARCH_LOG.md](RESEARCH_LOG.md): three substantive approaches, stopping at the full counterexample
- [SOURCE_VERIFICATION.json](SOURCE_VERIFICATION.json): controlling edition, literature scope, prior-attempt checks and public hashes
- [CHECK_RESULTS.json](CHECK_RESULTS.json): exact reproducible checks
- [FINITE_CERTIFICATE.json](FINITE_CERTIFICATE.json): complete finite group and subgroup masks
- [LIMITATIONS.md](LIMITATIONS.md): scope and review limits

Run `python3 verify_math.py --check` and `python3 verify_manifest.py` from this directory. No external package, network connection or private source file is needed.

The public payload contains authored mathematics, code, certificates and verification metadata only. Source PDFs, extracted source text and dataset contents are excluded.
