#!/usr/bin/env python3
"""Proof-first exact replay of a fixed 36-relation four-port candidate overlay.

The completed sweep is used as a hash-bound census and record source.  No separator search,
atlas pickle, rank pickle, or retained polynomial map is loaded.  Instead this
script rebuilds every K2P Fourier map from the directed graph presentations and
replays three fixed proof families:

* the 22 theta0 repair-1 quintic port-orbit obstructions;
* 12 lower-theta quartic obstructions, including their proven transports; and
* one 14-term theta3 cubic obstruction, substituted directly into both targets.

Every obstruction is checked for bridge multihomogeneity, zero target
pullback, nonzero source pullback, and nonzero value at one explicit strict
positive-domain K2P point.  This does not claim closure of restoration or of a
global classification theorem.  The resulting certificate is deterministic.
"""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import importlib.util
import itertools
import json
import math
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import networkx as nx


ROOT = Path(__file__).resolve().parents[1]
GRAPH_GRAMMAR = None


SCHEMA = "k2p-four-port-direct-candidate-overlay-v2"
EXPECTED_MERGED_FILE_SHA256 = "d6b848c45d0074f9d14e94af03861297946b17ba0000905758f44c3e406032fe"
EXPECTED_MERGED_PAYLOAD_SHA256 = "d911fecedbefa5ef1c815665c2cad0069ce918545c4b3783b0a82441f1fa05b4"
EXPECTED_SWEEP_SHA256 = "f765e1c0e5ce63e1264fb93a58a90988713acbe2e9853facbeaa759e529c819f"
EXPECTED_CUBIC_PULLBACK_SHA256 = "8bb849446bec02d42cd5aea7d7555d3ad97abfdff0834fa3b223c79ff2718deb"
EXPECTED_CUBIC_STRICT_VALUE = Fraction(701, 30_720_000_000)
EXPECTED_QUINTIC_SHA256 = "02f835bbc6b00704a993426b25e074a26239cc7124059402372b136cccb5ec4f"
EXPECTED_QUARTIC_SHA256 = {
    "F112": "176c030342cee7504fc2e488f39c448ad1d5e3631489c70c9e29f43b4f025c17",
    "F113": "b8a2203572f8a268758ca549aadd9a85a88d02dcf630a1970c657a191c6c4cba",
    "F48": "314ae606c30b87b305b2a7762bdf612a2a00811dca298242ce7cb0e8eb45b14f",
}


EXPECTED_MANIFEST_UNRESOLVED = {
    0: (),
    1: (25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 39, 40, 41, 42, 43, 44, 45, 46, 47),
    2: (112, 113, 114, 115),
    3: (112, 113, 114, 115),
    4: (8, 9, 10, 11),
    5: (),
}

EXPECTED_SOURCE_CLASS_COUNTS = (536, 747, 276, 276, 64, 32)
EXPECTED_MANIFEST_BINDINGS = {
    0: (
        "144ccdc657cd15f851e868384cbeefae36a9a443089dda8db25b8e955e2d22e6",
        "9762337a7cae9376d03dea5276573c326ad2e827c70a83cf8c5e3783f59828d3",
    ),
    1: (
        "b797860b78e9b30c1a522ec5f036e61981704a18c4b025a7b1eeb78417826025",
        "679fc6eae5cb9a110357a82be208585c3034212cd5c47a9df3152c1ff6232287",
    ),
    2: (
        "accdc4b097b7d81387784506bda079d9ca6caed3bad5661c85363683dea20017",
        "22d37ca2fdce5ba7065727b0b18613715ce525604aab35528deb6b2586f73a82",
    ),
    3: (
        "6c653ef7e28b3c96cf1292becd98d5c3a774639115ac4bf2fd62cb474e6a7d04",
        "7240cea7d93d0c7964aa294fecbe8c6dc81eab2745d1f893e1876cb60cca7401",
    ),
    4: (
        "de9de374aa1d1fea9ea81b5000bb73ff2571f4d7445fd1bb2a2f99a56f7b7e85",
        "a12d909bd391f03a9e7e9ffb253d19f3f43a1a5283890e8030f5093e124d68f5",
    ),
    5: (
        "2af1e864b403520a71a28f9c11eb98e27203b20c64090456d470a1009fb75443",
        "5f672cd06b3af70924faa0339514cd9161f653372b3deed39efccc4216863aea",
    ),
}

EXPECTED_TOTAL_STATUS_COUNTS = {
    "error": 0,
    "isomorphic": 20,
    "restoration_parent": 997,
    "separated": 845,
    "triangle": 35,
    "unresolved": 34,
}


EXPECTED_RECORD_BINDINGS = {
    (1, 25): ("unresolved", "42a078ddfc0bfc40eb231c52dbfabe86b1cec51965dc168bbdc376b29065c277", "6ef07436e8d7f8ae2832f76e3c1aaa16e01c5fdaf0350f1b8d4264d965ffcb09"),
    (1, 26): ("unresolved", "527d104bc1a438fab10f96775bc77fbb351500e9b418d3e8251ed817cd5f174f", "5431b880d91fd2c1563591f736ee99e8ac360aa406769ed415e959c1d67c0314"),
    (1, 27): ("unresolved", "031a7199d407ee75c150f15969770506da8792ba2a5bd70394ece70dd574faf4", "dee58d30460988a8e34a8de166d50b8616fa9583ce2cb8c35125196608037fad"),
    (1, 28): ("unresolved", "0202a8237822ef71bc7588ed0801497e628cf30b96f8a7b4f9d4206fa09d010a", "45655193958ffd55b0ed9ad7a4ebd181abe4333e935a434ca709df81d72b8fcd"),
    (1, 29): ("unresolved", "5a4f4c3a06acde6bf2d5c70bc89535fc5d372762d7182d70ff02048d8f644996", "bf416085967905441e135c01be03ff60a9c9a9c23d5747d2f4b2a3e79270da3a"),
    (1, 30): ("unresolved", "9bb010c03990a38a1c1c57fdea5adbc83dd18afe1a4c43a4e2755e3530ef16af", "9e5615d523e2692ac810b7f6d005eb35b70108c41237a224f059682c4619e4bc"),
    (1, 31): ("unresolved", "0a8e7cbe42c17162cdeb2be8e0fd7da39f67f24069af8ce26165d4e430ea1322", "36b2a4707b12d6e74677b66a8e2ba4c566fb4f2767388c955b3e4e7ff3745de8"),
    (1, 32): ("unresolved", "e756ba89e36ab75a9cd52477f38d08e1dd10cb3252adb0487fdcfe7af768fba3", "f9e99daf17f3ef32b07677a93c6233d272e5ce719643f8f97daca3a8bc0985e6"),
    (1, 33): ("unresolved", "1ddb610bdaa0988088107607bd08e875b53ec6f04da356e67a83518e2818642f", "af58cb320a24b34d38c805e9ad36ca921ad5ab8959600e5f32cc1659b37ee0a8"),
    (1, 34): ("unresolved", "9738845c7eca9b0cb921c43a4dfbe9d71d60ecc86c68fc335497fae266027df2", "cc3866de479d5f8b38fc954936ca30bb210590b84f01e829e7e6ebf15b167de7"),
    (1, 35): ("unresolved", "1b080b15727206964195698aa1a8ad583605b2fcd22f5855742970f569d89065", "5571b0c24809fd80422e78bb7b8766bbe4f357a8393d47dea9a46147f1ff2304"),
    (1, 36): ("unresolved", "2ecc6ad7980564804dd963a6a8d74b231e912713eac8b83dbaf9d64a674c22fc", "31dd051a45aed0c138ba56ee5545f9c7a4112ea8b40ad833e4df2d4498d59a14"),
    (1, 37): ("unresolved", "ca42e02ab2f8d2355dd2b1096d318ba091f921fc3e71f6eff5642f8d5d211eac", "2e1e38701b86a839ab13812adbd55fb40c7f95bfe5f622299757081a7cc03278"),
    (1, 39): ("unresolved", "390614d65e4fe3eb755dc8df154a28e943451ef3f9895396786bbf9968bfd6bd", "13af67d0cab4010113ac0caa2b9b6abefe10084c7cb50242a34702dff8750617"),
    (1, 40): ("unresolved", "16ec6fcd9931939a2f4547b02dbdd4f84735a2feb206927bc72bb8054bca6411", "ef3ad5b67bf49e5acba20a12500fc68d32b6c90e2f95b030bad8a3a148e9dc69"),
    (1, 41): ("unresolved", "15db2e4e65448b97ba411896f282585aede051c09a2325150a35e372248aac59", "4fbb93be68b8a7a91bd1e9c78be86316d421444f63707a1c5eb9c3312e98c505"),
    (1, 42): ("unresolved", "8befd65498931176507b16347628054ee54ea5ba04f3e9cce427a1588d4c1ebe", "f2f42905b25d3d271b942dddfee6e3937933b46691ec2dfc322146decd17127c"),
    (1, 43): ("unresolved", "1ae37f417ff3b492368a249ce9407335c7383a50666de6f37e470c002f81c1a1", "d5db778d8ccd6da6aa024ee834c30d717e4b122f2b882d16ab121d7514d129ae"),
    (1, 44): ("unresolved", "e4a3e2d54fa9a8e2a808078f397aef4eddc2eec93521e8552c4d15fd8ceaff7e", "e3bcd1fb33400b5b2240eea8ae92a35683090a71e3e2ed2e1daefb3c609900d4"),
    (1, 45): ("unresolved", "ec7c4d916092fb00ced0d9775122cf36402eeb8dd2abe12f94a20330c425f8fc", "d4e9e20bbd212d0965c88487f697ed6ebac490f99f7d98bb23c73e05079cbeee"),
    (1, 46): ("unresolved", "df5026e24102fd95c1502335d57797e53a3bb3e89c3da5584a1ffff408f99fc9", "e576773a64511b50ae99b34281185308bd37aa44501cdd930b3dbdc838e2f0bd"),
    (1, 47): ("unresolved", "d7baedf51f37fc7de87521aac6cdbdd1ead83cd6e9eb2d2532f8be9f1f209788", "719cb11e1d5a43efcd28d0e986bcec7c31697124c15fb27bb54963218d54c7e3"),
    (2, 112): ("unresolved", "e080698eda1e2bf1bcabc1517af2da228b453e162ec2f2948f7bb4f4a5e5173f", "b1bb22c138031bf1908f468de76e54ea05ce882d07b0b4664cce68fc29e0b76d"),
    (2, 113): ("unresolved", "5142da7dd73ee1d60df2708f75f76d7341a6056e64ae467c043789e617fb9698", "ad78d3ae53599363db0555af0bd81e3485b3c80196a690525013eeb17b0b5b04"),
    (2, 114): ("unresolved", "08d615535801dc432a783ed3f23955e4976f9a24c880c5b9c007a61135575f3d", "2a9b536d291537fe19a5808c6d4255cfecc5e9800ba556ec51fe20f2192b9f10"),
    (2, 115): ("unresolved", "ce282dd00dbeb776b9bc31a2a7c88ba96bbbe0a2927c7acd7eb4a2f140d7c7af", "57fa170f9dcd37ad177cd41368133f4127611a77c82f14f21df5c88a85a43785"),
    (3, 112): ("unresolved", "5ea0fafd9fe2d9541d0ea3b9573841ee876a15755eba8afd51e1fe3b578c9a4a", "2a6db5e0560a2d74e6623853195fc578c7d17f98180c86c90576dcea85f604c9"),
    (3, 113): ("unresolved", "91fa24796b4bcde90398db8174201839338c89cc731b30bf7c1a0a4d0e845307", "bb6e270fb3c5b344f99e89804e2046adb82d9e358157bb67ac3cc6774e05b3d4"),
    (3, 114): ("unresolved", "0a5859e0dde0c78e0a9851f609e2058e82bf19f045ce35af6034454587c8300a", "3e64c0f2f4c9d9cf1ace516045d03b1e05239f447efc75d6994945ea785757d0"),
    (3, 115): ("unresolved", "89c1e9ca1ec3cf04114d0c05b6befa19609b359aea75b5fa13317d98f96c2b78", "26ef50817fa5e54ff2a9b187c5e5c3dec037271da4ea741f568a3f63650e96ac"),
    (4, 8): ("unresolved", "56856d3798e209c6fc90107ef3602c82c0d4a9a322c07724a91264359695c15f", "e0be82f851544ad462e4d21960fcaba95e9b1092257eed9af33ae5e42ea99d60"),
    (4, 9): ("unresolved", "65cdb6b48b634770f614a2a85126c4a075fc0458b3bb5f002c8200d366ce3705", "b3d88bc34356ef6052701b23e4952b5844ccdbec3ce16a2c7c96dd2a00cb5f5c"),
    (4, 10): ("unresolved", "f11b2306f6bb75fa234da81cb166bb3278ac49b51a0e9ccf81e94036daa774aa", "6ac236e5b3ef92cfbfb97c653803bfcede8d9610a4a3ae90fc44181ca84fc069"),
    (4, 11): ("unresolved", "60acbfb1b392e8c39eee7c4a6bae8bf1e66ad9a23d1636f389f41c037ba3fdc2", "0b7f72e5295a0f762a79b37e45a5330ac751baf119e9433cba7d2205db5ca7de"),
    (5, 9): ("separated", "464928d324e0d85892419f78317ac9d96b4de897f3ea66d44871f18c78a6fc09", "21be41b078a522312d1fa5250d15e181f42d1f948fbb54cdf89494a7ac824603"),
    (5, 10): ("separated", "9e42c93cee33a67ea3ef1f0756354c4608fe1be983a3892cd192d7b57330c617", "813ae3ae5eebd0999b9ced243d928007004b1bb270cfbccda7795d8aae3ec0a6"),
}


# The normalized, adversarially reviewed 14-term cubic.  Tuple convention is
# (coordinate monomial, integer coefficient).
CUBIC = (
    ((0, 15, 35), 1),
    ((0, 20, 30), 1),
    ((1, 14, 35), 1),
    ((2, 15, 33), 1),
    ((2, 18, 32), 1),
    ((2, 23, 33), -1),
    ((3, 11, 35), -1),
    ((4, 20, 26), -1),
    ((6, 12, 33), 1),
    ((6, 18, 28), -1),
    ((7, 12, 32), -1),
    ((7, 15, 28), -1),
    ((7, 23, 28), 1),
    ((9, 10, 30), -1),
)


E = (0, 1, 2, 3)
A = (1, 0, 2, 3)
B = (0, 1, 3, 2)
H = (1, 0, 3, 2)


def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_graph_grammar(package_root: Path):
    """Load only the current package's graph grammar module."""
    module_path = package_root / "atlas/k2p_atlas_core.py"
    spec = importlib.util.spec_from_file_location("k2p_overlay_graph_grammar", module_path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"cannot load graph grammar: {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def canonical_data(value: Any):
    """The production driver's exact object canonicalization."""
    if dataclasses.is_dataclass(value):
        return {
            field.name: canonical_data(getattr(value, field.name))
            for field in dataclasses.fields(value)
        }
    if isinstance(value, dict):
        return {
            str(key): canonical_data(item)
            for key, item in sorted(value.items(), key=lambda pair: repr(pair[0]))
        }
    if isinstance(value, (tuple, list)):
        return [canonical_data(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return repr(value)


def sha_object(value: Any) -> str:
    raw = json.dumps(
        canonical_data(value), sort_keys=True, separators=(",", ":")
    ).encode()
    return hashlib.sha256(raw).hexdigest()


def digest(value: Any) -> str:
    raw = json.dumps(
        value, sort_keys=True, separators=(",", ":"), default=str
    ).encode()
    return hashlib.sha256(raw).hexdigest()


def graph_payload(graph: nx.DiGraph) -> dict:
    nodes = []
    for node, data in sorted(graph.nodes(data=True), key=lambda pair: repr(pair[0])):
        nodes.append(
            [repr(node), {str(key): repr(value) for key, value in sorted(data.items())}]
        )
    edges = []
    for tail, head, data in sorted(
        graph.edges(data=True), key=lambda row: (repr(row[0]), repr(row[1]))
    ):
        edges.append(
            [
                repr(tail),
                repr(head),
                {str(key): repr(value) for key, value in sorted(data.items())},
            ]
        )
    return {
        "nodes": nodes,
        "edges": edges,
        "graph": {
            str(key): repr(value) for key, value in sorted(graph.graph.items())
        },
    }


def ct_orbit_rep(characters: tuple[int, ...]) -> tuple[int, ...]:
    swapped = tuple(3 if x == 1 else (1 if x == 3 else x) for x in characters)
    return min(characters, swapped)


def orbit_assignments(k: int) -> tuple[tuple[int, ...], ...]:
    assignments = set()
    for prefix in itertools.product(range(4), repeat=k - 1):
        last = 0
        for value in prefix:
            last ^= value
        assignments.add(ct_orbit_rep(prefix + (last,)))
    return tuple(sorted(assignments))


def coordinate_weights(k: int) -> tuple[tuple[int, ...], ...]:
    result = []
    for characters in orbit_assignments(k):
        row = []
        for character in characters:
            row.extend(
                (
                    1 if character in (1, 3) else 0,
                    1 if character == 2 else 0,
                )
            )
        result.append(tuple(row))
    return tuple(result)


def reticulation_nodes(graph: nx.DiGraph) -> tuple:
    return tuple(
        sorted(
            (node for node, data in graph.nodes(data=True) if data["role"] == "retic"),
            key=repr,
        )
    )


def selected_arm_edges(graph: nx.DiGraph) -> set[tuple]:
    return {
        (tail, head)
        for tail, head in graph.edges()
        if graph.nodes[head]["role"] == "leaf"
        and isinstance(graph.nodes[head].get("label"), int)
    }


def descendant_masks(graph: nx.DiGraph, kept_edges: tuple[tuple, ...]) -> dict:
    children = {node: [] for node in graph.nodes()}
    for tail, head in kept_edges:
        children[tail].append(head)
    topology = list(nx.topological_sort(nx.edge_subgraph(graph, kept_edges).copy()))
    masks = {}
    for node in reversed(topology):
        label = graph.nodes[node].get("label")
        mask = (1 << label) if isinstance(label, int) else 0
        for child in children[node]:
            mask |= masks[child]
        masks[node] = mask
    return {(tail, head): masks[head] for tail, head in kept_edges}


def sector_for_mask(mask: int, characters: tuple[int, ...]) -> int:
    total = 0
    index = 0
    while mask:
        if mask & 1:
            total ^= characters[index]
        index += 1
        mask >>= 1
    return 0 if total == 0 else (2 if total == 2 else 1)


def inheritance_polynomial(bits: tuple[int, ...]) -> tuple[tuple[int, int], ...]:
    """Expand product lambda_j (bit=1) or (1-lambda_j) (bit=0)."""
    polynomial = {0: 1}
    for index, bit in enumerate(bits):
        updated = defaultdict(int)
        for mask, coefficient in polynomial.items():
            if bit:
                updated[mask | (1 << index)] += coefficient
            else:
                updated[mask] += coefficient
                updated[mask | (1 << index)] -= coefficient
        polynomial = {mask: value for mask, value in updated.items() if value}
    return tuple(sorted(polynomial.items()))


@dataclass(frozen=True)
class GraphFourierMap:
    k: int
    retic_count: int
    edge_class_count: int
    outputs: tuple
    edge_signatures: tuple


def graph_fourier_map(graph: nx.DiGraph) -> GraphFourierMap:
    """Rebuild the canonical paired-(s,g) K2P map directly from ``graph``."""
    k = sum(
        isinstance(data.get("label"), int) for _, data in graph.nodes(data=True)
    )
    assignments = orbit_assignments(k)
    retics = reticulation_nodes(graph)
    retic_count = len(retics)
    parents = tuple(
        tuple(sorted(graph.predecessors(node), key=repr)) for node in retics
    )
    all_edges = tuple(graph.edges())
    arms = selected_arm_edges(graph)

    base_switches = []
    for bits in itertools.product((0, 1), repeat=retic_count):
        removed = set()
        for node, choices, bit in zip(retics, parents, bits):
            kept_parent = choices[bit]
            removed.update((parent, node) for parent in choices if parent != kept_parent)
        kept = tuple(edge for edge in all_edges if edge not in removed)
        masks = descendant_masks(graph, kept)
        sectors = {
            edge: tuple(sector_for_mask(masks[edge], row) for row in assignments)
            for edge in kept
            if edge not in arms
        }
        base_switches.append((bits, kept, sectors))

    if retic_count:
        actions = tuple(
            itertools.product(
                itertools.permutations(range(retic_count)),
                itertools.product((0, 1), repeat=retic_count),
            )
        )
    else:
        actions = (((), ()),)

    variants = []
    for permutation, flips in actions:
        ordered = []
        for new_bits in itertools.product((0, 1), repeat=retic_count):
            old_bits = [0] * retic_count
            for index in range(retic_count):
                old_bits[permutation[index]] = new_bits[index] ^ flips[index]
            old_index = 0
            for bit in old_bits:
                old_index = (old_index << 1) | bit
            ordered.append((new_bits, base_switches[old_index]))

        signatures = []
        internal_edges = []
        for edge in all_edges:
            if edge in arms:
                continue
            signature = []
            for _new_bits, (_old_bits, _kept, sectors) in ordered:
                signature.extend(sectors.get(edge, (0,) * len(assignments)))
            if any(signature):
                internal_edges.append(edge)
                signatures.append(tuple(signature))
        active = tuple(sorted(set(signatures)))
        class_of = {signature: index for index, signature in enumerate(active)}
        edge_class = {
            edge: class_of[signature]
            for edge, signature in zip(internal_edges, signatures)
        }

        outputs = []
        for coordinate_index in range(len(assignments)):
            grouped = defaultdict(lambda: defaultdict(int))
            for new_bits, (_old_bits, kept, sectors) in ordered:
                factors = Counter()
                for edge in kept:
                    class_index = edge_class.get(edge)
                    if class_index is None:
                        continue
                    sector = sectors.get(edge, (0,) * len(assignments))[coordinate_index]
                    if sector:
                        factors[(class_index, sector)] += 1
                monomial = tuple(
                    sorted(
                        (class_index, sector, exponent)
                        for (class_index, sector), exponent in factors.items()
                    )
                )
                for mask, coefficient in inheritance_polynomial(new_bits):
                    grouped[monomial][mask] += coefficient
            expression = []
            for monomial, polynomial in grouped.items():
                lambda_polynomial = tuple(
                    sorted((mask, coefficient) for mask, coefficient in polynomial.items() if coefficient)
                )
                if lambda_polynomial:
                    expression.append((monomial, lambda_polynomial))
            outputs.append(tuple(sorted(expression)))
        variants.append(
            GraphFourierMap(
                k,
                retic_count,
                len(active),
                tuple(outputs),
                active,
            )
        )
    return min(
        variants,
        key=lambda descriptor: (
            descriptor.retic_count,
            descriptor.edge_class_count,
            descriptor.outputs,
            descriptor.edge_signatures,
        ),
    )


def output_sparse_polynomials(descriptor: GraphFourierMap) -> tuple[dict, ...]:
    parameter_count = 2 * descriptor.edge_class_count + descriptor.retic_count
    outputs = []
    for expression in descriptor.outputs:
        polynomial = defaultdict(int)
        for monomial, lambda_polynomial in expression:
            base = [0] * parameter_count
            for class_index, sector, exponent in monomial:
                base[2 * class_index + sector - 1] += exponent
            for mask, coefficient in lambda_polynomial:
                full = list(base)
                for index in range(descriptor.retic_count):
                    if mask >> index & 1:
                        full[2 * descriptor.edge_class_count + index] += 1
                polynomial[tuple(full)] += coefficient
        outputs.append(
            {exponent: coefficient for exponent, coefficient in polynomial.items() if coefficient}
        )
    return tuple(outputs)


def sparse_multiply(left: dict, right: dict) -> dict:
    result = defaultdict(int)
    for left_exponent, left_coefficient in left.items():
        for right_exponent, right_coefficient in right.items():
            exponent = tuple(
                a + b for a, b in zip(left_exponent, right_exponent)
            )
            result[exponent] += left_coefficient * right_coefficient
    return {exponent: coefficient for exponent, coefficient in result.items() if coefficient}


def sparse_multiply_many(polynomials: list[dict]) -> dict:
    if not polynomials:
        return {(): 1}
    result = polynomials[0]
    for polynomial in polynomials[1:]:
        result = sparse_multiply(result, polynomial)
    return result


def polynomial_pullback(polynomial: tuple, outputs: tuple[dict, ...]) -> dict:
    columns = []
    coefficients = []
    product_cache = {}
    for monomial, coefficient in polynomial:
        if monomial not in product_cache:
            product_cache[monomial] = sparse_multiply_many(
                [outputs[index] for index in monomial]
            )
        columns.append(product_cache[monomial])
        coefficients.append(Fraction(coefficient))
    result = defaultdict(Fraction)
    for column, coefficient in zip(columns, coefficients):
        for exponent, value in column.items():
            result[exponent] += coefficient * value
    return {exponent: coefficient for exponent, coefficient in result.items() if coefficient}


def evaluate_map(
    descriptor: GraphFourierMap,
    edge_pairs: tuple[tuple[Fraction, Fraction], ...],
    lambdas: tuple[Fraction, ...],
) -> tuple[Fraction, ...]:
    assert len(edge_pairs) == descriptor.edge_class_count
    assert len(lambdas) == descriptor.retic_count
    result = []
    for expression in descriptor.outputs:
        value = Fraction(0)
        for monomial, lambda_polynomial in expression:
            edge_value = Fraction(1)
            for class_index, sector, exponent in monomial:
                edge_value *= edge_pairs[class_index][sector - 1] ** exponent
            inheritance_value = Fraction(0)
            for mask, coefficient in lambda_polynomial:
                term = Fraction(coefficient)
                for index, inheritance in enumerate(lambdas):
                    if mask >> index & 1:
                        term *= inheritance
                inheritance_value += term
            value += edge_value * inheritance_value
        result.append(value)
    return tuple(result)


def evaluate_polynomial(polynomial: tuple, coordinates: tuple[Fraction, ...]) -> Fraction:
    return sum(
        Fraction(coefficient)
        * math.prod(coordinates[index] for index in monomial)
        for monomial, coefficient in polynomial
    )


def inverse(permutation: tuple[int, ...]) -> tuple[int, ...]:
    result = [0] * len(permutation)
    for index, image in enumerate(permutation):
        result[image] = index
    return tuple(result)


def coordinate_map(permutation: tuple[int, ...]) -> tuple[int, ...]:
    assignments = orbit_assignments(4)
    index = {assignment: offset for offset, assignment in enumerate(assignments)}
    return tuple(
        index[
            ct_orbit_rep(
                tuple(assignment[permutation[position]] for position in range(4))
            )
        ]
        for assignment in assignments
    )


def transform(polynomial: tuple, permutation: tuple[int, ...]) -> tuple:
    mapping = coordinate_map(permutation)
    return tuple(
        (tuple(sorted(mapping[index] for index in monomial)), coefficient)
        for monomial, coefficient in polynomial
    )


def multidegree(polynomial: tuple) -> tuple[int, ...]:
    weights = coordinate_weights(4)
    degrees = {
        tuple(
            sum(weights[index][slot] for index in monomial)
            for slot in range(8)
        )
        for monomial, _coefficient in polynomial
    }
    assert len(degrees) == 1
    return next(iter(degrees))


def first_witness(sparse_polynomial: dict) -> dict:
    exponent, coefficient = next(
        iter(sorted(sparse_polynomial.items(), key=lambda row: repr(row[0])))
    )
    return {"parameter_exponent": exponent, "coefficient": str(coefficient)}


def strict_point(descriptor: GraphFourierMap):
    edge_pairs = tuple(
        (Fraction(1, 4), Fraction(index + 1, 10))
        for index in range(descriptor.edge_class_count)
    )
    lambdas = (Fraction(1, 3), Fraction(2, 3))
    assert len(lambdas) == descriptor.retic_count
    for s_value, g_value in edge_pairs:
        assert 0 < s_value < 1
        assert 0 < g_value < 1
        assert g_value > 2 * s_value - 1
    assert all(0 < inheritance < 1 for inheritance in lambdas)
    return edge_pairs, lambdas


def semantic_record_hash(record: dict) -> str:
    diagnostic_fields = {
        "runtime_seconds",
        "peak_rss_bytes",
        "runtime_platform",
        "generated_at_utc",
        "record_payload_sha256",
        "semantic_record_sha256",
    }
    body = {
        key: value for key, value in record.items() if key not in diagnostic_fields
    }
    return hashlib.sha256(
        json.dumps(body, sort_keys=True, separators=(",", ":"), default=str).encode()
    ).hexdigest()


def record_payload_hash(record: dict) -> str:
    body = {key: value for key, value in record.items() if key != "record_payload_sha256"}
    return hashlib.sha256(
        json.dumps(body, sort_keys=True, separators=(",", ":"), default=str).encode()
    ).hexdigest()


def validate_package_lock(package_root: Path) -> tuple[dict, dict]:
    lock_path = package_root / "INPUT_LOCK.json"
    lock = json.loads(lock_path.read_text())
    assert lock["schema"] == "k2p-offline-four-port-input-lock-v1"
    assert tuple(lock["expected_source_class_counts"]) == EXPECTED_SOURCE_CLASS_COUNTS
    for relative, expected_hash in lock["files"].items():
        assert sha_file(package_root / relative) == expected_hash, relative
    bindings = {
        "compiler_sha256": lock["compiler_sha256"],
        "canonicalizer_sha256": lock["canonicalizer_sha256"],
        "descriptor_pickle_sha256": lock["files"]["atlas/descriptors_4.pkl"],
        "rank_pickle_sha256": lock["files"]["atlas/rank_certs_4.pkl"],
        "output_schema_sha256": lock["files"]["schemas/four_port_record_v3.schema.json"],
        "input_lock_sha256": sha_file(lock_path),
        "hard_certificate_sha256": lock["files"]["certificates/direct_hard_cases.json"],
    }
    assert bindings["compiler_sha256"] == lock["files"]["atlas/k2p_atlas_core.py"]
    return lock, bindings


def semantic_manifest_hash(
    source_index: int,
    class_count: int,
    bindings: dict,
    summaries: list[dict],
) -> str:
    semantic_summaries = [
        {key: value for key, value in summary.items() if key != "record_sha256"}
        for summary in summaries
    ]
    return sha_object(
        {
            "source_index": source_index,
            "canonical_class_count": class_count,
            "immutable": {"schema": "k2p-four-port-record-v3", **bindings},
            "records": semantic_summaries,
        }
    )


def load_and_bind_records(
    package_root: Path,
    run_root: Path,
    sources: tuple,
    targets: list,
):
    _lock, package_bindings = validate_package_lock(package_root)
    merged_path = run_root / "FOUR_PORT_SWEEP_MERGED_STATUS.json"
    assert sha_file(merged_path) == EXPECTED_MERGED_FILE_SHA256
    merged = json.loads(merged_path.read_text())

    manifests = {}
    summaries_by_key = {}
    merge_rows = []
    totals = {status: 0 for status in (
        "separated", "isomorphic", "triangle", "restoration_parent", "unresolved", "error"
    )}
    summary_count = 0
    for source_index, class_count in enumerate(EXPECTED_SOURCE_CLASS_COUNTS):
        manifest_path = run_root / f"source_{source_index}" / "residual_manifest.json"
        expected_raw, expected_semantic = EXPECTED_MANIFEST_BINDINGS[source_index]
        assert sha_file(manifest_path) == expected_raw
        manifest = json.loads(manifest_path.read_text())
        manifests[source_index] = manifest
        assert manifest["schema"] == "k2p-four-port-residual-manifest-v2"
        assert manifest["record_schema"] == "k2p-four-port-record-v3"
        assert manifest["source_index"] == source_index
        assert manifest["canonical_class_count"] == class_count
        assert manifest["record_count"] == class_count
        assert manifest["complete"] is True
        assert {
            key: manifest[key] for key in package_bindings
        } == package_bindings

        summaries = manifest["records"]
        assert isinstance(summaries, list)
        assert [row["canonical_class_id"] for row in summaries] == list(range(class_count))
        summary_count += len(summaries)
        for summary in summaries:
            key = (source_index, summary["canonical_class_id"])
            assert key not in summaries_by_key
            summaries_by_key[key] = summary
            assert summary["status"] in totals
            totals[summary["status"]] += 1

        unresolved = sorted(
            row["canonical_class_id"] for row in summaries if row["status"] == "unresolved"
        )
        restoration = sorted(
            row["canonical_class_id"]
            for row in summaries
            if row["status"] == "restoration_parent"
        )
        assert tuple(unresolved) == EXPECTED_MANIFEST_UNRESOLVED[source_index]
        assert manifest["unresolved"] == unresolved
        assert manifest["restoration_candidates"] == restoration
        observed_semantic = semantic_manifest_hash(
            source_index, class_count, package_bindings, summaries
        )
        assert observed_semantic == expected_semantic
        assert manifest["semantic_manifest_sha256"] == observed_semantic
        merge_rows.append(
            {
                "source_index": source_index,
                "manifest_sha256": expected_raw,
                "semantic_manifest_sha256": observed_semantic,
                "complete": True,
                "canonical_class_count": class_count,
                "record_count": class_count,
                "unresolved": unresolved,
                "restoration_candidates": restoration,
            }
        )

    assert summary_count == 1_931
    assert totals == EXPECTED_TOTAL_STATUS_COUNTS
    merged_base = {
        "schema": "k2p-four-port-six-source-merge-v2",
        "bindings": package_bindings,
        "sources": merge_rows,
        "all_six_sources_present": True,
        "all_manifests_complete": True,
        "total_status_counts": totals,
        "unresolved_by_source": {
            str(row["source_index"]): row["unresolved"]
            for row in merge_rows
            if row["unresolved"]
        },
        "restoration_candidate_counts": {
            str(row["source_index"]): len(row["restoration_candidates"])
            for row in merge_rows
        },
    }
    payload_hash = hashlib.sha256(
        json.dumps(merged_base, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    assert payload_hash == EXPECTED_MERGED_PAYLOAD_SHA256
    sweep_hash = sha_object(
        {
            "schema": merged_base["schema"],
            "bindings": package_bindings,
            "sources": [
                {
                    "source_index": row["source_index"],
                    "canonical_class_count": row["canonical_class_count"],
                    "semantic_manifest_sha256": row["semantic_manifest_sha256"],
                }
                for row in merge_rows
            ],
        }
    )
    assert sweep_hash == EXPECTED_SWEEP_SHA256
    expected_merged = {
        **merged_base,
        "payload_sha256_without_hash": payload_hash,
        "semantic_sweep_sha256": sweep_hash,
    }
    assert merged == expected_merged

    records = {}
    record_bindings = []
    for source_index in range(6):
        candidate_ids = sorted(
            class_id for candidate_source, class_id in EXPECTED_RECORD_BINDINGS
            if candidate_source == source_index
        )
        for class_id in candidate_ids:
            key = (source_index, class_id)
            expected_status, expected_semantic, expected_raw = EXPECTED_RECORD_BINDINGS[key]
            path = (
                run_root
                / f"source_{source_index}"
                / "records"
                / f"class_{class_id:06d}.json"
            )
            record = json.loads(path.read_text())
            assert record["source_index"] == source_index
            assert record["canonical_class_id"] == class_id
            assert record["status"] == expected_status
            assert record["stratum"] == "direct_no_dummy"
            assert record["omitted_roles"] == []
            assert len(record["members"]) == 1
            assert record["semantic_record_sha256"] == expected_semantic
            assert semantic_record_hash(record) == expected_semantic
            assert record_payload_hash(record) == record["record_payload_sha256"]
            assert sha_file(path) == expected_raw
            summary = summaries_by_key[key]
            assert summary == {
                "canonical_class_id": class_id,
                "status": record["status"],
                "stratum": record["stratum"],
                "descriptor_sha256": record["descriptor_sha256"],
                "record_sha256": expected_raw,
                "semantic_record_sha256": expected_semantic,
                "omitted_roles": record["omitted_roles"],
                "child_requests": record["child_requests"],
            }
            assert all(record[key_name] == value for key_name, value in package_bindings.items())

            source_graph_hash = sha_object(graph_payload(sources[source_index].graph))
            assert record["source_graph_sha256"] == source_graph_hash
            member = record["members"][0]
            target = GRAPH_GRAMMAR.relabel_record(
                targets[member["target_index"]], tuple(member["port_match"])
            )
            assert not target.dummy_labels
            selected_graph_hash = sha_object(graph_payload(target.graph))
            assert member["target_selected_graph_sha256"] == selected_graph_hash
            assert record["target_graph_sha256"] == sha_object([selected_graph_hash])

            source_descriptor = graph_fourier_map(sources[source_index].graph)
            target_descriptor = graph_fourier_map(target.graph)
            assert sha_object(target_descriptor) == record["descriptor_sha256"]
            records[key] = record
            record_bindings.append(
                {
                    "source_index": source_index,
                    "canonical_class_id": class_id,
                    "production_status": record["status"],
                    "semantic_record_sha256": record["semantic_record_sha256"],
                    "record_file_sha256": expected_raw,
                    "record_payload_sha256": record["record_payload_sha256"],
                    "source_graph_sha256": source_graph_hash,
                    "target_selected_graph_sha256": selected_graph_hash,
                    "descriptor_sha256": sha_object(target_descriptor),
                }
            )
    assert set(records) == set(EXPECTED_RECORD_BINDINGS)
    assert len(records) == 36
    sweep_validation = {
        "summary_count": summary_count,
        "manifest_file_and_semantic_sha256": {
            str(source): {
                "file": EXPECTED_MANIFEST_BINDINGS[source][0],
                "semantic": EXPECTED_MANIFEST_BINDINGS[source][1],
            }
            for source in range(6)
        },
        "merged_file_sha256": EXPECTED_MERGED_FILE_SHA256,
        "merged_payload_sha256": payload_hash,
        "semantic_sweep_sha256": sweep_hash,
        "total_status_counts": totals,
    }
    return records, record_bindings, expected_merged, sweep_validation


def verify_case(
    *,
    family: str,
    source_index: int,
    class_id: int,
    polynomial_name: str,
    polynomial: tuple,
    record: dict,
    sources: tuple,
    targets: list,
    source_map_cache: dict,
) -> dict:
    source_descriptor, source_outputs, source_coordinates = source_map_cache[source_index]
    member = record["members"][0]
    target = GRAPH_GRAMMAR.relabel_record(
        targets[member["target_index"]], tuple(member["port_match"])
    )
    target_descriptor = graph_fourier_map(target.graph)
    target_outputs = output_sparse_polynomials(target_descriptor)

    target_pullback = polynomial_pullback(polynomial, target_outputs)
    source_pullback = polynomial_pullback(polynomial, source_outputs)
    assert not target_pullback, (source_index, class_id, "target")
    assert source_pullback, (source_index, class_id, "source")

    weight = multidegree(polynomial)
    strict_value = evaluate_polynomial(polynomial, source_coordinates)
    assert strict_value != 0, (source_index, class_id, "strict witness")
    pendant_pair = (Fraction(1, 4), Fraction(1, 2))
    assert 0 < pendant_pair[0] < 1
    assert 0 < pendant_pair[1] < 1
    assert pendant_pair[1] > 2 * pendant_pair[0] - 1
    pendant_factor = math.prod(
        pendant_pair[0] ** weight[2 * port]
        * pendant_pair[1] ** weight[2 * port + 1]
        for port in range(4)
    )
    physical_strict_value = strict_value * pendant_factor
    assert physical_strict_value != 0
    return {
        "family": family,
        "source_index": source_index,
        "canonical_class_id": class_id,
        "production_status": record["status"],
        "semantic_record_sha256": record["semantic_record_sha256"],
        "target_index": member["target_index"],
        "port_match": member["port_match"],
        "polynomial": polynomial_name,
        "polynomial_sha256": digest(polynomial),
        "degree": len(polynomial[0][0]),
        "bridge_multidegree": weight,
        "bridge_multihomogeneous": True,
        "target_pullback_zero": True,
        "target_pullback_term_count": 0,
        "source_pullback_term_count": len(source_pullback),
        "source_pullback_sha256": sha_object(source_pullback),
        "source_pullback_list_sha256": digest(
            sorted(source_pullback.items(), key=lambda row: repr(row[0]))
        ),
        "source_pullback_witness": first_witness(source_pullback),
        "strict_D_plus_witness": {
            "internal_edge_class_pairs": [
                [str(s_value), str(g_value)]
                for s_value, g_value in strict_point(source_descriptor)[0]
            ],
            "selected_pendant_edge_pairs": [
                [str(pendant_pair[0]), str(pendant_pair[1])] for _port in range(4)
            ],
            "inheritance_probabilities": [
                str(value) for value in strict_point(source_descriptor)[1]
            ],
            "all_internal_and_pendant_edge_inequalities_checked": True,
            "normalized_source_obstruction_value": str(strict_value),
            "pendant_multihomogeneous_factor": str(pendant_factor),
            "physical_source_obstruction_value": str(physical_strict_value),
            "nonzero": True,
        },
    }


def main() -> None:
    if not __debug__:
        raise SystemExit("optimized Python (-O) is forbidden: proof assertions must execute")
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--package-root",
        type=Path,
        required=True,
        help="current locked portable package root",
    )
    parser.add_argument(
        "--run-root",
        type=Path,
        required=True,
        help="completed six-source run root bound to that package",
    )
    parser.add_argument(
        "--certificate",
        type=Path,
        default=Path(__file__).with_name(
            "four_port_direct_residual_closure_certificate.json"
        ),
    )
    args = parser.parse_args()
    package_root = args.package_root.resolve()
    run_root = args.run_root.resolve()

    global GRAPH_GRAMMAR
    validate_package_lock(package_root)
    GRAPH_GRAMMAR = load_graph_grammar(package_root)
    sources = tuple(GRAPH_GRAMMAR.source_supports())
    targets = GRAPH_GRAMMAR.target_completions(4, True)
    assert tuple((row.core_id, row.repair_index) for row in sources) == (
        ("theta0", 0),
        ("theta0", 1),
        ("theta1", 0),
        ("theta1", 1),
        ("theta3", 0),
        ("theta3", 1),
    )
    records, record_bindings, merged, sweep_validation = load_and_bind_records(
        package_root, run_root, sources, targets
    )

    source_map_cache = {}
    for source_index in (1, 2, 3, 4, 5):
        descriptor = graph_fourier_map(sources[source_index].graph)
        assert descriptor.k == 4
        assert descriptor.retic_count == 2
        assert descriptor.edge_class_count == 8
        outputs = output_sparse_polynomials(descriptor)
        edge_pairs, lambdas = strict_point(descriptor)
        coordinates = evaluate_map(descriptor, edge_pairs, lambdas)
        source_map_cache[source_index] = (descriptor, outputs, coordinates)

    quintic_artifact_path = Path(__file__).with_name(
        "theta0_quintic_orbit_certificate.json"
    )
    quintic_artifact = json.loads(quintic_artifact_path.read_text())
    assert quintic_artifact["schema"] == "k2p-theta0-repair1-quintic-port-orbit-v1"
    quintic = tuple(
        (tuple(monomial), coefficient)
        for monomial, coefficient in quintic_artifact["invariant"]
    )
    assert digest(quintic) == quintic_artifact["invariant_sha256"]
    assert digest(quintic) == EXPECTED_QUINTIC_SHA256
    quintic_rows = {
        row["class_id"]: row for row in quintic_artifact["rows"]
    }

    coverage = []
    zero_permutations = []
    for class_id, permutation in enumerate(itertools.permutations(range(4)), 24):
        polynomial = transform(quintic, inverse(permutation))
        source_pullback = polynomial_pullback(
            polynomial, source_map_cache[1][1]
        )
        if not source_pullback:
            zero_permutations.append(permutation)
        if class_id not in EXPECTED_MANIFEST_UNRESOLVED[1]:
            continue
        record = records[(1, class_id)]
        assert tuple(record["members"][0]["port_match"]) == permutation
        row = verify_case(
            family="theta0_quintic_port_orbit",
            source_index=1,
            class_id=class_id,
            polynomial_name=f"A_{{P^-1}}^*F5[class={class_id}]",
            polynomial=polynomial,
            record=record,
            sources=sources,
            targets=targets,
            source_map_cache=source_map_cache,
        )
        artifact_row = quintic_rows[class_id]
        assert artifact_row["source_pullback_terms"] == row["source_pullback_term_count"]
        assert artifact_row["source_pullback_sha256"] == row["source_pullback_list_sha256"]
        assert tuple(artifact_row["source_pullback_witness"]["parameter_exponent"]) == tuple(
            row["source_pullback_witness"]["parameter_exponent"]
        )
        assert artifact_row["source_pullback_witness"]["coefficient"] == row[
            "source_pullback_witness"
        ]["coefficient"]
        coverage.append(row)
    assert zero_permutations == [E, (2, 1, 0, 3)]
    assert sum(row["family"] == "theta0_quintic_port_orbit" for row in coverage) == 22

    quartic_artifact_path = Path(__file__).with_name(
        "theta_quartic_obstruction_certificates.json"
    )
    quartic_artifact = json.loads(quartic_artifact_path.read_text())
    assert quartic_artifact["schema"] in {
        "k2p-theta-quartic-obstructions-v1",
        "k2p-theta-quartic-obstructions-v2",
    }
    base_rows = {
        (row["source_index"], row["canonical_class_id"]): row
        for row in quartic_artifact["certificates"]
    }
    assert set(base_rows) == {(2, 112), (2, 113), (4, 8)}
    transport_rows = {
        (row["source_index"], row["canonical_class_id"]): row
        for row in quartic_artifact.get("transports", ())
    }
    quartics = {
        "F112": tuple(
            (tuple(indices), coefficient)
            for coefficient, indices in base_rows[(2, 112)]["terms"]
        ),
        "F113": tuple(
            (tuple(indices), coefficient)
            for coefficient, indices in base_rows[(2, 113)]["terms"]
        ),
        "F48": tuple(
            (tuple(indices), coefficient)
            for coefficient, indices in base_rows[(4, 8)]["terms"]
        ),
    }
    for name, polynomial in quartics.items():
        assert digest(polynomial) == EXPECTED_QUARTIC_SHA256[name]
    F48_A = transform(quartics["F48"], A)

    quartic_cases = []
    for source_index in (2, 3):
        quartic_cases.extend(
            (
                (source_index, 112, E, "F112", quartics["F112"]),
                (source_index, 113, B, "F113", quartics["F113"]),
                (source_index, 114, A, "F113", quartics["F113"]),
                (source_index, 115, H, "F112", quartics["F112"]),
            )
        )
    quartic_cases.extend(
        (
            (4, 8, E, "F48", quartics["F48"]),
            (4, 9, B, "A_A^*F48", F48_A),
            (4, 10, A, "A_A^*F48", F48_A),
            (4, 11, H, "F48", quartics["F48"]),
        )
    )
    if quartic_artifact["schema"] == "k2p-theta-quartic-obstructions-v2":
        assert set(transport_rows) == {
            (source_index, class_id)
            for source_index, class_id, _permutation, _name, _polynomial in quartic_cases
        }
    for source_index, class_id, permutation, name, polynomial in quartic_cases:
        record = records[(source_index, class_id)]
        assert tuple(record["members"][0]["port_match"]) == permutation
        row = verify_case(
            family="lower_theta_quartic",
            source_index=source_index,
            class_id=class_id,
            polynomial_name=name,
            polynomial=polynomial,
            record=record,
            sources=sources,
            targets=targets,
            source_map_cache=source_map_cache,
        )
        base_artifact = base_rows.get((source_index, class_id))
        if base_artifact is not None:
            assert base_artifact["source_pullback_term_count"] == row["source_pullback_term_count"]
            assert base_artifact["source_pullback_sha256"] == row["source_pullback_list_sha256"]
        transport_artifact = transport_rows.get((source_index, class_id))
        if transport_artifact is not None:
            assert tuple(transport_artifact["port_match"]) == permutation
            assert transport_artifact["target_index"] == row["target_index"]
            assert tuple(transport_artifact["port_weight"]) == tuple(
                row["bridge_multidegree"]
            )
            assert transport_artifact["target_pullback_term_count"] == 0
            assert transport_artifact["source_pullback_term_count"] == row[
                "source_pullback_term_count"
            ]
            assert transport_artifact["source_pullback_sha256"] == row[
                "source_pullback_list_sha256"
            ]
        coverage.append(row)
    assert sum(row["family"] == "lower_theta_quartic" for row in coverage) == 12

    cubic_artifact_path = Path(__file__).with_name(
        "theta3_cubic_obstruction_certificate.json"
    )
    cubic_artifact = json.loads(cubic_artifact_path.read_text())
    assert cubic_artifact["schema"] == "k2p-theta3-cubic-obstruction-v1"
    normalized_artifact_cubic = tuple(
        (tuple(monomial), coefficient)
        for coefficient, monomial in cubic_artifact["normalized_terms"]
    )
    assert normalized_artifact_cubic == CUBIC
    assert digest(CUBIC) == cubic_artifact["normalized_polynomial_sha256"]
    assert math.gcd(*(abs(coefficient) for _monomial, coefficient in CUBIC)) == 1
    assert multidegree(CUBIC) == (1,) * 8
    assert tuple(cubic_artifact["bridge_multidegree"]) == (1,) * 8
    assert cubic_artifact["exact_source_pullback"] == {
        "term_count": 96,
        "sha256": EXPECTED_CUBIC_PULLBACK_SHA256,
        "strict_D_plus_normalized_value": str(EXPECTED_CUBIC_STRICT_VALUE),
    }
    cubic_production_bindings = {
        (row["source_index"], row["canonical_class_id"]): row
        for row in cubic_artifact["fresh_production_record_bindings"]
    }
    assert set(cubic_production_bindings) == {(5, 9), (5, 10)}

    # Crucially, both targets are reconstructed and substituted separately.
    for class_id, permutation in ((9, B), (10, A)):
        record = records[(5, class_id)]
        assert tuple(record["members"][0]["port_match"]) == permutation
        production_certificate = record["certificate"]
        assert production_certificate["type"] == "exact_multihomogeneous_cubic"
        normalized_production_cubic = tuple(
            (tuple(monomial), coefficient)
            for monomial, coefficient in zip(
                production_certificate["coordinate_triples"],
                production_certificate["coefficients"],
            )
            if coefficient
        )
        assert normalized_production_cubic == CUBIC
        assert production_certificate["degree"] == 3
        assert tuple(production_certificate["weight"]) == (1,) * 8
        assert production_certificate["source_nonzero_terms"] == 96
        assert production_certificate["source_pullback_sha256"] == EXPECTED_CUBIC_PULLBACK_SHA256
        assert record["certificate_payload_sha256"] == sha_object(production_certificate)
        artifact_binding = cubic_production_bindings[(5, class_id)]
        expected_status, expected_semantic, expected_raw = EXPECTED_RECORD_BINDINGS[(5, class_id)]
        assert artifact_binding == {
            "source_index": 5,
            "canonical_class_id": class_id,
            "production_status": expected_status,
            "target_index": record["members"][0]["target_index"],
            "port_match": list(permutation),
            "semantic_record_sha256": expected_semantic,
            "record_file_sha256": expected_raw,
        }
        row = verify_case(
            family="theta3_cubic",
            source_index=5,
            class_id=class_id,
            polynomial_name="C3",
            polynomial=CUBIC,
            record=record,
            sources=sources,
            targets=targets,
            source_map_cache=source_map_cache,
        )
        assert row["source_pullback_term_count"] == 96
        assert row["source_pullback_sha256"] == EXPECTED_CUBIC_PULLBACK_SHA256
        assert Fraction(
            row["strict_D_plus_witness"]["normalized_source_obstruction_value"]
        ) == EXPECTED_CUBIC_STRICT_VALUE
        coverage.append(row)
    assert sum(row["family"] == "theta3_cubic" for row in coverage) == 2

    covered_keys = {
        (row["source_index"], row["canonical_class_id"]) for row in coverage
    }
    assert len(coverage) == 36
    assert covered_keys == set(EXPECTED_RECORD_BINDINGS)

    proof_input_paths = (
        quintic_artifact_path,
        quartic_artifact_path,
        cubic_artifact_path,
    )
    payload = {
        "schema": SCHEMA,
        "claim": (
            "Each relation in the fixed 36-candidate direct_no_dummy overlay "
            "has a replayed exact bridge-multihomogeneous obstruction which "
            "vanishes on its target and is nonzero at an explicit strict D+ "
            "source point."
        ),
        "logical_conclusion": (
            "For each of these 36 candidate records only, the strict source "
            "image is not generically contained in the bound target variety."
        ),
        "scope_limitation": (
            "This certificate is a proof overlay for 36 named direct candidates. "
            "It makes no claim that restoration, gluing, genericity, or the "
            "global classification theorem is complete."
        ),
        "package_root": (
            str(package_root.relative_to(ROOT))
            if package_root.is_relative_to(ROOT)
            else str(package_root)
        ),
        "run_root": (
            str(run_root.relative_to(ROOT))
            if run_root.is_relative_to(ROOT)
            else str(run_root)
        ),
        "semantic_sweep_sha256": merged["semantic_sweep_sha256"],
        "sweep_validation": sweep_validation,
        "production_status_counts_among_36": {
            "unresolved": 34,
            "separated": 2,
        },
        "proof_family_counts": {
            "theta0_quintic_port_orbit": 22,
            "lower_theta_quartic": 12,
            "theta3_cubic": 2,
        },
        "graph_fourier_reconstruction": {
            "atlas_pickles_loaded": False,
            "separator_search_invoked": False,
            "maps_rebuilt_from_graph_switches": True,
            "paired_s_g_sectors": True,
            "inheritance_mixtures_expanded_exactly": True,
            "parameter_coefficient_field": "Q",
        },
        "strict_D_plus_witness_recipe": {
            "internal_s_i": "1/4",
            "internal_g_i": "(i+1)/10 for i=0,...,7",
            "each_selected_pendant_pair": ["1/4", "1/2"],
            "inheritance_probabilities": ["1/3", "2/3"],
            "inequalities_checked_on_every_physical_edge": [
                "0<s_i<1",
                "0<g_i<1",
                "g_i>2*s_i-1",
            ],
        },
        "record_bindings": sorted(
            record_bindings,
            key=lambda row: (row["source_index"], row["canonical_class_id"]),
        ),
        "coverage": sorted(
            coverage,
            key=lambda row: (row["source_index"], row["canonical_class_id"]),
        ),
        "covered_candidate_classes": [
            [source_index, class_id]
            for source_index, class_id in sorted(covered_keys)
        ],
        "remaining_unproved_among_36": 0,
        "binding_gaps": [],
        "proof_input_sha256": {
            str(path.relative_to(ROOT)): sha_file(path) for path in proof_input_paths
        },
        "verifier_sha256": sha_file(Path(__file__)),
    }
    payload["payload_sha256_without_hash"] = sha_object(payload)
    args.certificate.parent.mkdir(parents=True, exist_ok=True)
    args.certificate.write_text(
        json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n"
    )
    print("FOUR_PORT_DIRECT_CANDIDATE_OVERLAY_PASS")
    print(f"covered={len(coverage)} remaining_unproved_among_36=0")
    print(f"payload_sha256={payload['payload_sha256_without_hash']}")
    print(f"certificate_sha256={sha_file(args.certificate)}")


if __name__ == "__main__":
    main()
