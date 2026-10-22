"""Finite prefix/order diagnostics only; does not prove transfinite or Hahn-support claims."""
from itertools import product
from pathlib import Path
from datetime import datetime, timezone
import json

MAX_LENGTH = 12
all_sequences = [s for n in range(MAX_LENGTH + 1) for s in product((-1, 1), repeat=n)]

def key(s):
    return s + (0,) * (MAX_LENGTH + 3 - len(s))

def prefixes(s):
    return {s[:n] for n in range(len(s))}

def transform(s, alpha):
    a = (-1,) * alpha
    if s == a:
        return ()
    if s[:alpha] != a or len(s) < alpha:
        return (1,) + s
    assert s[alpha] == 1
    return (1,) + a + s[alpha + 1:]

results = []
for alpha in range(MAX_LENGTH + 1):
    a = (-1,) * alpha
    source = sorted((s for s in all_sequences if key(s) >= key(a)), key=key)
    image_by_source = {s: transform(s, alpha) for s in source}
    image = list(image_by_source.values())
    assert len(set(image)) == len(source)
    assert image == sorted(image, key=key)
    assert image_by_source[a] == ()
    assert all(not z or z[0] == 1 for z in image)
    source_by_image = {z: s for s, z in image_by_source.items()}
    right_predecessor_checks = 0
    for s, z in image_by_source.items():
        expected = {()} | {image_by_source[v] for v in prefixes(s) if v != a}
        if s == a:
            assert not prefixes(z)
        else:
            assert prefixes(z) == expected
        assert prefixes(z) <= source_by_image.keys()
        for q in prefixes(z):
            if key(q) > key(z):
                y = source_by_image[q]
                assert y in prefixes(s) and key(y) > key(s)
                assert y != a
                right_predecessor_checks += 1
    results.append({"alpha": alpha, "source_nodes": len(source), "right_predecessor_pairs_checked": right_predecessor_checks})

output = {
    "utc": datetime.now(timezone.utc).isoformat(),
    "max_length": MAX_LENGTH,
    "claim": "Finite tests of injectivity/order, exact prefix identity, target initiality and right-predecessor implication.",
    "limitation": "This checks finite sign sequences only. It is not proof of limit-length sign surgery or arbitrary set-sized Hahn supports.",
    "all_passed": True,
    "runs": results,
}
out_path = Path(__file__).with_name("diagnostic_results.json")
out_path.write_text(json.dumps(output, indent=2) + "\n")
print(json.dumps(output, indent=2))
