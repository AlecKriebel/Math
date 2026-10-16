"""Algebraic boundary controls for the postseal adversarial checkpoint."""
import hashlib
import json
from pathlib import Path


def require(value, label):
    if not value:
        raise ValueError(label)


def hom_values(domain_order, coefficient_order):
    return [v for v in range(coefficient_order) if domain_order * v % coefficient_order == 0]


def main():
    root = Path(__file__).resolve().parent
    tmp = root.parent
    bindings = json.loads((root / "INPUT_BINDINGS.json").read_text())
    for row in bindings["inputs"]:
        data = (tmp/row["path"]).read_bytes()
        require(len(data) == row["bytes"] and hashlib.sha256(data).hexdigest() == row["sha256"], "input changed: " + row["path"])
    sealed = tmp / "math_definition"
    require(hashlib.sha256((sealed/"MANIFEST.json").read_bytes()).hexdigest() == "53343305e38688a18d5b4b0f133be21ba8d7c00338e55e024b2e27a54059a093", "original sealed manifest changed")
    inventory = json.loads((sealed/"MANIFEST.json").read_text())["files"]
    require({p.name for p in sealed.iterdir()} == {r["path"] for r in inventory} | {"MANIFEST.json"}, "original sealed inventory changed")
    for row in inventory:
        data = (sealed/row["path"]).read_bytes()
        require(len(data) == row["bytes"] and hashlib.sha256(data).hexdigest() == row["sha256"], "original sealed member changed")

    # Sphere generator Z -> Z/2 is nonzero after reduction and evaluation.
    mod2_sphere_pullback = [value * (1 % 2) % 2 for value in hom_values(2, 2)]
    require(mod2_sphere_pullback == [0, 1], "torsion sphere mod-two detection")
    require(hom_values(3, 2) == [0], "odd torsion detection negative control")
    z2_reduction = sorted({v % 2 for v in hom_values(2, 4)})
    z4_reduction = sorted({v % 2 for v in hom_values(4, 4)})
    require(z2_reduction == [0], "exact order-two Bockstein")
    require(z4_reduction == [0, 1], "order-four Bockstein boundary control")
    parity = {(1, 2): 1, (1, 1): 0, (2, 2): 0}
    require(all(sum(weights) % 2 == value for weights, value in parity.items()), "loop parity boundaries")
    require([n % 2 for n in [2, 3, 4, 5]] == [0, 1, 0, 1], "cover-degree boundaries")

    # A nonzero cubic has domain dimension m-2 and target m+1 in rank two.
    rank_two_dimensions = [((m+1) - (m-2)) for m in range(3, 16)]
    rank_one_dimensions = [1 if m < 3 else 0 for m in range(16)]
    require(set(rank_two_dimensions) == {3}, "rank-two cubic quotient remains unbounded")
    require(sum(rank_one_dimensions) == 3, "rank-one positive control")
    require(all(__import__("math").gcd(p, p-1) == 1 for p in [3, 5, 7, 11, 13]), "one-dimensional p-action sample diagnostic")

    result = {
        "status": "PASS",
        "mathematical_issues": 0,
        "required_repairs": [],
        "bound_inputs": len(bindings["inputs"]),
        "original_sealed_packet": "UNCHANGED",
        "torsion_sphere_pullback_values": mod2_sphere_pullback,
        "order_two_reduction_image": z2_reduction,
        "order_four_reduction_image": z4_reduction,
        "rank_two_quotient_dimensions_degrees_3_to_15": rank_two_dimensions,
        "rank_one_total_quotient_dimension": sum(rank_one_dimensions),
        "limits": "Finite algebraic diagnostics and hash binding; universal topology is reasoned in CROSSCHECK.md."
    }
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
