# Corrections and release notes

The frozen candidate is preserved unchanged. No mathematical estimate or proof mechanism needs repair.

## C1: Source convention wording

At PROOF.md line 16, replace the sentence beginning “The source's word” and the next sentence with:

> The printed source does not explicitly require distinct or increasing samples. We interpret its classical claim as a theorem about distinct positive integers, equivalently an increasing sequence; this is consistent with the separated-sampling hypothesis in the cited literature. If arbitrary repetitions are permitted, the literal statement is false: Section 6 gives a counterexample even when the repeated sequence tends to infinity.

This is a source-precision correction. It does not change the already stated theorem or the counterexample. In SOURCE_STATUS.md's scope caveat, similarly prefer “The intended distinct/increasing interpretation is corroborated by the separated-sampling theorem cited below” to any suggestion that the bare word “sequence” formally enforces distinctness.

## C2: Audit status after acceptance

A release copy may replace “independent audit pending” / “subject to independent audit” with a dated link to this audit, while preserving the historical checkpoint log. Record the reviewed original proof hash and any new proof hash after editorial changes. Do not silently alter the frozen checkpoint or claim that its original bytes already contain the later audit result.

## C3: Manifest inventory

Any parent/status report that says the full manifest has 31 entries should say 32. The public allowlist still has exactly six entries. This counting correction does not change a hash or permit redistribution of private sources.

## Classification

Keep the proposed historical disposition already_solved and the single substantive reconstruction turn (1/5), with the explicit distinct/increasing interpretation and the negative result for unrestricted repetitions. Do not label this verified_solved as a novel contribution. There is no remaining mathematical gap in either scope after this audit.
