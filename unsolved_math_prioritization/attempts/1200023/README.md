# AMR-011-0023: audited unresolved boundary-distance checkpoint

**Status: unsolved; five of five substantive approach families completed.**

[Research report](submission/REPORT.md) · [Full independent audit](independent-audit/AUDIT_REPORT.md) · [Optional clarifications](independent-audit/CORRECTIONS.md)

The source credits the unimodular case. This packet reconstructs that known proof, proves a spanning-regular-tree sufficient condition covering grandfather graphs, and gives an exact finite-support min-cut criterion. The general connected nonunimodular vertex-transitive problem remains unresolved. A disconnected literal-wording control is not presented as resolution.

All twelve authored files and all six audit files retain their original bytes. Freeze-time statements that an audit was pending are historical; the later audit passed with no required corrections. The audit's optional coordinate-model clarification applies: the verification oracles use the connected components reached from their declared roots.

## Reproduce the final layout

From this directory, using Python 3 and its standard library:

```
python3 -B verify_publication.py
python3 -B verify_publication.py --self-test
python3 -B submission/verify.py > original-replay.json
cmp original-replay.json submission/CONTROL_RESULTS.json
python3 -B independent-audit/audit_verify.py . > independent-replay.json
cmp independent-replay.json independent-audit/AUDIT_RESULTS.json
```

Write optional replay outputs outside this directory if rerunning its strict inventory checker. `verify_publication.py` checks the exact publication inventory, file sizes/hashes, both frozen trees, original and independent replays. Its self-test requires rejection of missing, altered and unexpected files and an unsafe manifest path.

Original checks include 31 finite-support networks, 872 subset comparisons and 30,595 geodesic interval cases. The independent audit rebuilds the graph models and networks, then checks 2,538 small-graph networks, 1,296 weighted networks, 20 off-center networks and 1,117 tree-boundary subsets. These support the stated partial claims, not a universal theorem or novelty assertion.

The small authored ZIP is included because the audit binds and checks its exact members. No scholarly PDFs, extracted full text, source screenshots or dataset contents are included. The packet is AI-assisted and unreviewed; this independent computational/mathematical audit is not expert peer review. No paper, release or DOI is proposed.
