# 10400036: Polyak's iterated-linking presentation problem

**Active research, four of five author turns used. The full original target is unresolved.**

The exact problem is to give a based or appropriately corrected iterated-Seifert-surface linking expression for the integer Milnor invariants of arbitrary string links, without requiring lower invariants to vanish. The imported following virtual-knot section is not part of the question.

[Turn 1](TURN_1.md) proves the necessary ordered correction identity, gives explicit point-pushing examples that expose two naive-rule failures, and identifies an ordered cut-surface intersection count with all nonrepeating coefficients on that restricted family. These are credited classical deductions, not a resolution of the arbitrary-string-link construction.

[Turn 2](TURN_2.md) retains the canonical cut-open lift, identifies the central lattice lost on closure, and gives the full degree-two based-transport correction formula for arbitrary string links. The all-order derived-link geometry remains the gap.

- [Exact target](TARGET.md)
- [Source and prior-work gate](SOURCE_GATE.md)
- [Primary PDF hashes](source_manifest.json)
- [Research log](RESEARCH_LOG.md) and [turn ledger](turns.json)
- [Turn-1 exact checker](turn_1_check.py), [receipt](turn_1_checks.json), [frozen turn files](TURN_1_MANIFEST.json)

The checker uses only the Python standard library. Its finite exact controls do not certify the written geometric arguments. No final PR or status promotion is authorized before independent adversarial review.

Turn-2 controls: [checker](turn_2_check.py), [receipt](turn_2_checks.json), [frozen turn files](TURN_2_MANIFEST.json).

[Turn 3](TURN_3.md) gives an all-order integral relative-cochain construction, proves filling-choice independence by based gauge, and extracts every target Magnus coefficient. Its cellular identities and holonomy have not been identified with the requested embedded derived-link geometry. [Checker](turn_3_check.py), [receipt](turn_3_checks.json), [frozen turn files](TURN_3_MANIFEST.json).

[Turn 4](TURN_4.md) realizes the all-order integer by intersection with a genuine properly embedded surface in a marked nilpotent cover of the other strands' exterior, using a lower-data closing path. The comparison with the requested downstairs derived link is still missing. [Checker](turn_4_check.py), [receipt](turn_4_checks.json), [frozen turn files](TURN_4_MANIFEST.json).
