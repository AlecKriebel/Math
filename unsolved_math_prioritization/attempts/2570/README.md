# KOU-21.61: effective coherence remains unresolved

UnsolvedMath record **2570**, rank **691**. Disposition: **unsolved, 5/5**.

For a fixed finite-rank free-by-infinite-cyclic group, the problem asks for an algorithm that converts any finite subgroup generating tuple into a finite presentation. This package does not give that algorithm in general.

## What was established

- Exact height-kernel saturation, terminating when that kernel is finitely generated.
- A complete restricted algorithm for periodic outer monodromy, including direct products.
- Eventual correctness of finite HNN windows without an effective stopping certificate.
- Arbitrarily long false plateaus in one fixed direct product, refuting fixed-length plateau tests.
- A fibre that is not a virtual retract, refuting that universal certificate strategy.

The obstructions are not counterexamples to effective coherence and do not prove undecidability. Five substantive approach families leave the full target unresolved. No novelty or priority is claimed.

## Evidence

- [Full authored proofs](author/PROOFS.md), [five-approach research log](author/RESEARCH_LOG.md), and [limitations](author/LIMITATIONS.md)
- [Complete independent scoped audit](audit/PARTIALS_AUDIT.md)
- [Public source verification](author/SOURCE_VERIFICATION.json)
- [Publication binding](BINDING.json) and [publication log](RESEARCH_LOG.md)

All nine author files and all four independent-audit files are preserved byte-for-byte. Historical statements that the audit/publication is pending, that the author made no remote writes, and that the reviewer did not execute author helpers describe those frozen stages. The publication verifier subsequently inspects/replays those helpers separately; it does not rewrite the audit history. No mathematical correction was required.

## Boundaries that remain

The current dataset row was inspected but is not immutably bound to the pinned corpus. The separate prior AI report was not inspected. Duplicate record 20001495 is contextual only and receives no row change. Whole-corpus hashes are public manifest declarations, not fresh independent download verifications.

Gray–Linton's general rewriting-system algorithm requires a finite presentation of the group to be processed already as input. Its existence theorem therefore does not supply the missing presentation from subgroup generators. The generator-input theorem has additional locally quasiconvex hyperbolic virtually special hypotheses.

The audit is computational-assistant review, not human review, peer acceptance or formal verification. Foundational results and broader geometric-combination literature have the inspection limits stated in the full audit.

## Portable verification

Only Python 3's standard library is needed. From this directory run:

    python3 -B verify_publication.py --replay --selftest
    python3 -O -B verify_publication.py --replay --selftest

The strict wrapper remains active under optimization. It runs the frozen assertion-based helpers in isolated, unoptimized child processes and temporary copies, compares all recorded output values, and checks every payload byte before and after replay. Eighteen negative controls check strict inventory, binding and scope. Finite tests supplement the written proofs; they do not establish the full algorithm.

The published material consists of authored mathematics/code, the complete authored audit and public verification metadata. Source PDFs, extracted source text, dataset contents and private coordination material are excluded. The existing queue changes only this target's Status and Turns cells; all remaining bytes, including the pre-existing header and links, are preserved.
