# Kirby 1.69: unresolved Bennequin-sharpness converse

[The obstruction note](OBSTRUCTION.md) records two unsuccessful approaches and the exact remaining gaps. The general question is explicitly unresolved. The reductions are credited to established literature; no discovery claim is made.

The key obstacle is preserving the **transverse** link while constructing a maximal-Euler-characteristic braided surface. The known topological construction may use negative stabilization, which changes self-linking. A second approach stops at the missing canonical-surface hypothesis.

Run the modest exact controls with standard-library Python 3:

    python3 verify.py

The script prints deterministic JSON; [verification.json](verification.json) is the saved receipt. These controls test accounting identities and boundary cases, not topology or a solution of the conjecture.

See [readiness.json](readiness.json), [the research log](RESEARCH_LOG.md), [source hashes](source_manifest.json), and [frozen artifact hashes](frozen_artifacts.json). [Separate adversarial AI review](review/REVIEW.md) passed with no correction. All 324 author controls and 3,848 independent controls pass. The reviewer also checked a complete preprint dated 29 September 2026, which retains the open problem. The frozen note keeps its original pending-review sentence for exact provenance. This remains an unsuccessful attempt, not a full solution.

The pinned upstream record is attributed to [ulamai/UnsolvedMath](https://huggingface.co/datasets/ulamai/UnsolvedMath), revision 37e53eabe540fb458758e198be61634bd02ee008, CC BY 4.0. Its embedded prior triage was read; the keyed research-results dataset has no separate report for KP-1.69.
