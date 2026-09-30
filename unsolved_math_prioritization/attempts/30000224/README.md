# 30000224: set-theoretic Cohen–Macaulayness of the Macaulay quartic

**Status: partial/stalled. The original question is not solved.**

The exact target permits arbitrary nonhomogeneous ideals. The bounded attempt
proves three restrictions on a possible Cohen–Macaulay thickening:

- It cannot be binomial in characteristic zero
- It cannot contain the reduced quadric equation wz−xy
- If homogeneous, it cannot have generic multiplicity one or two

The note also gives an explicit Koszul class showing why the natural skew-line
link fails the hypotheses of a 2025 residual-intersection theorem. These are
restricted deductions from standard theory; novelty is not claimed.

## Files

- [Complete mathematical note and exact remaining gap](PARTIAL_RESULTS.md)
- [Source and current-literature audit](SOURCES.md)
- [Fresh exact verifier](verify.py) and [receipt](verification.json)
- [Research log](RESEARCH_LOG.md), [turn ledger](turns.jsonl), [status](status.json)
- [Readiness record](readiness.json) and [pinned input](input_record.json)

Run `python3 verify.py` from this directory. It uses the Python standard library
and passes 135 exact assertions. The universal geometric/algebraic arguments
are in the note; finite computation does not prove the full original target.

Independent adversarial review is pending. No shared queue, catalog, or state
file is modified. Execution model: gpt-6-astra, xhigh.
