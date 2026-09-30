# Random projective plane transversals

**Unresolved after two substantive attempts.** This package does not prove either lower bound in Alon's Conjecture 5, and makes no novelty claim.

`BASELINE.md` gives a self-contained classical lower bound, a standard alteration upper bound, the exact minimal-blocker counting reduction, and the quantified failure of a direct application of the cited container theorem. `SOURCE_AUDIT.md` identifies the original statement and duplicate ID 30006391. `RESEARCH_LOG.md` and `turn_ledger.json` preserve the attempt budget and final gap.

Run `python check_small_planes.py` from this directory to reproduce `check_results.json`. It uses only the Python standard library and checks all 128 subsets of PG(2,2) and all 8192 subsets of PG(2,3). These exact diagnostics do not establish an asymptotic result.

Independent adversarial review is pending. The actual model was gpt-6-astra at xhigh reasoning. The pinned source records are attributed to [ulamai/UnsolvedMath](https://huggingface.co/datasets/ulamai/UnsolvedMath), CC BY 4.0.
