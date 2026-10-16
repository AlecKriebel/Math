"""Independently count CI minor evaluations and their transpose equivalence classes."""
from pathlib import Path
from datetime import datetime, timezone
from itertools import product, combinations
from collections import Counter
import json

D = Path(__file__).resolve().parent
out = D / 'ROOT_CI_MINOR_COUNT_SCOPE_03.json'
assert not out.exists()
results = {}
for n in (4, 6):
    E = [(i, (i + 1) % n) for i in range(n)]
    signatures = Counter()
    ordered_separations = evaluations = 0
    for assignment in product(range(4), repeat=n):
        A, B, C = [tuple(i for i, label in enumerate(assignment) if label == k) for k in (0, 1, 2)]
        if not A or not B:
            continue
        permitted = set(range(n)) - set(C)
        reach = {i: {i} for i in permitted}
        for i, j in E:
            if i in permitted and j in permitted:
                reach[i].add(j)
                reach[j].add(i)
        for k in permitted:
            for i in permitted:
                if k in reach[i]:
                    reach[i].update(reach[k])
        if any(j in reach[i] for i in A for j in B):
            continue
        ordered_separations += 1
        for c in product((0, 1), repeat=len(C)):
            for a1, a2 in combinations(product((0, 1), repeat=len(A)), 2):
                for b1, b2 in combinations(product((0, 1), repeat=len(B)), 2):
                    evaluations += 1
                    direct = (A, B, C, c, a1, a2, b1, b2)
                    transpose = (B, A, C, c, b1, b2, a1, a2)
                    signatures[min(direct, transpose)] += 1
    assert set(signatures.values()) == {2}
    assert evaluations == 2 * len(signatures)
    results['C' + str(n)] = dict(ordered_nontrivial_separations=ordered_separations,
        ordered_separation_conditioning_minor_evaluations=evaluations,
        distinct_structural_minor_labels_up_to_A_B_transpose=len(signatures),
        multiplicity_of_every_canonical_label=2)
result = dict(recorded_utc=datetime.now(timezone.utc).isoformat(), status='PASS_LABEL_DUPLICATION_CONFIRMED',
    mechanism='Independent graph transitive closure and structural labels; no imported law checker. Canonicalizes A/B transpose only, not polynomial equivalence between different marginalizations or equality on a particular law.',
    results=results, mathematical_theorem_affected=False, current_package_label_requires_correction=True)
out.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
