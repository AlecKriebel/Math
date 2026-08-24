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
EXPECTED_MERGED_FILE_SHA256 = "d4ead86840c417454da1d860671f2b2d1883915c73a45cd8fea28acc4c69d965"
EXPECTED_MERGED_PAYLOAD_SHA256 = "608b92231877dd6199ff2bfcfc548b5a3e4ed2952de21db0c7352859bfc38cb8"
EXPECTED_SWEEP_SHA256 = "2a9a19ba3e9498df1c77582b07fcfd5ac315a4437ee634d25ce8ec4aa5cbaab0"
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
        "36c1dcf1f0148a2e025202a79b0a22881df8c050e09142f51e3973c847fcd6bb",
        "fd5e5d2f04ba8502f699ae671866e5471ae4d51dd25a21390cc812de978b9ab9",
    ),
    1: (
        "3baf1c1b6a74604fb7218de9d9f1e77be72179b00c6a7647747f69ef5f398d9e",
        "ea90e22c74cad7fd1357950099d455fa8e36a16964dde90846cadfa7bcc08923",
    ),
    2: (
        "6c88bdfddd48701e05e49df1cdad03abb910641df50b72b3ac508eb2d479cdb5",
        "2a2738fdbadbe8a1f9463d22fa9ebe2bc01a75cee2d337d19f7644982150e1d5",
    ),
    3: (
        "3da91b97e39820d1ed295df99c6983f3fb9d497685857e368e141761f96278a7",
        "7c56dec6163974f89021427d54e7008227621782b737f0f3570e4672ad697187",
    ),
    4: (
        "7f925b83fc2f17a74a562b07e69ad18dd1829efd4d3e4fa291371f6ec3d2badb",
        "9cbf729da3d1199805d2a5722635961b6f33fdc294ac015729c5aa5d15f75fba",
    ),
    5: (
        "97c7d6f46b0ae8c592bdb4c81deb85d793aaae4d869293e62c4f4c2f5f3d43bd",
        "546935f44c7d22fbcdbd5f5a4710f1891cca7f461a339ff645578dc12285d5c2",
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
    (1, 25): ("unresolved", "0f287b4eb4af8419b28934c95fc08ebe92902b34b00325980f7d909cd5aaa631", "4f0e2376ccadf988cf636c97cfcb6972c9b4f7ed2185c4cccfb096b76693aea6"),
    (1, 26): ("unresolved", "4f167ebb89e798735c502ecd5ebf59f03c0121d1758256af6c23278a18ba2856", "92448610f967fc32bb513f32a747a662e1212bfea2a4ba43d72829bde65eb411"),
    (1, 27): ("unresolved", "d1e3ad70a952b16d2630ee2b4454d4889b3383cf0f29bc853b2c32ea5be79afb", "b91b9808e585684c866bf951546df05f23dbc07050152c0411164d01f6103b98"),
    (1, 28): ("unresolved", "aec4d7a5a7f81fe75ab58f548b9f864467ec7c7aae050c09d69aa988f9fde749", "60966a8e55b87afd9967e1b9e5887f6c39c088457037e7033772effe74d8f705"),
    (1, 29): ("unresolved", "bb13d2b9c34ec4a1972bfe01aa30c8ac5fb07596be25590397480fbae0a2acba", "33ba326474432092f724f53f10b51c1de8232716274a29e72b874afd5a0d0cfe"),
    (1, 30): ("unresolved", "c0e13d68f6470798131e01a6c92215962e55eb3114992bea5d027d4fb6c7427a", "029b542636f9a8e0959f8494edaad5829b7c346118633f17ce984d9a405b0b67"),
    (1, 31): ("unresolved", "9f14fb91d812f85a569a84f889586d72dfe0c711c0b194714e3e33b2f44bf186", "619b55bf8bdeb10463bb777385474c4b8ea4ac9996d52ede27b3e6f1f54c843b"),
    (1, 32): ("unresolved", "4721cfae07d323e365aa9e60010987d213f228243246e5378374af1c15a4c412", "b02bdd273fd5a7c1330d2d508645bf495c762381128d998eab9dfd39a3c567b9"),
    (1, 33): ("unresolved", "2196121cf97abc303250e74dc5c9bd33b70bd3d8844ec582dbecf95ac00a304e", "a023c7933e9c595cc4d67d4186949af3f82dfcfc2d7b0fe5f2c38abe0ae69b54"),
    (1, 34): ("unresolved", "1339df9e66aa5811706c4cac13d36739ed4fa3e725aeb90bd98c45d809acfeb8", "d9c1bb126d55f2253184e983df05506cf44641e713e78613f171000d440a89d6"),
    (1, 35): ("unresolved", "87221a4f31f969a8945d13a422be2fb50c05d734f52de513ea18824396365d41", "397c07379d345964ea9c97ded0c746c890f892510891973f97c54679be9803de"),
    (1, 36): ("unresolved", "62beddffe9fe2fbe3b11f6926201d39c9396714f5f257ece9f36b99fe29c0853", "1a9be95417f48be8fd34a6f40f36e5bf9f8bbb9bc9257f03c8b645535ce403bb"),
    (1, 37): ("unresolved", "e69176b55d9bc10f2191c2ba6ccf57ef32333a91896c86c4f98b012e9e9500a1", "b37ab3bdc55ea4b14d4b1aa225933599fbb97835e24d512982a56b1f7cabd6ca"),
    (1, 39): ("unresolved", "2416b56031b7ed6a7852b532c5ee222208d41259a26c83c1202488f0457db324", "911294ce527f866d78dbac4204275e88c36ff7d8b976454c402e03d01ec7d04c"),
    (1, 40): ("unresolved", "76e64eb5dd820ba036972d4c629204e86bb384204cb01ba6117242f9c217b142", "81234aa2d70bf75d9639a35498243cf19b8786890ce38479eb97baaa8f6bc0c8"),
    (1, 41): ("unresolved", "b612c0cb070f0516c1262b3b90f3026fcf8b72dbf15ac2b660ea2b70560e6a6c", "83621f25a799d7888e457feed8cdd4adbcd79924d0400dab7952a67c8cdad81a"),
    (1, 42): ("unresolved", "5fd47f21d53d3b360e462baa462e0303f959277fdece40b85984962b30f39168", "55c91abd5fa20fadbfbd1e6cf8aa8d87e92c5f65ba893f07ab7eb2d245d8d999"),
    (1, 43): ("unresolved", "346203e1372726ab862f69bcea31ef19610b379371b44b05c8aebc386a86208f", "04d7635077d13eb3b4b6894115d732661d71d56f37bd6efa977fcb1ef6b3b8b7"),
    (1, 44): ("unresolved", "fbdee119f47cf32ebb6fa5af8b3f7bc7250e159ffd856ba0092c46f11f4785fb", "0773c6d40db5ea4ab199aac0efd7621cb0081f83193d64bebff950205df26a5e"),
    (1, 45): ("unresolved", "a8d9a139fcbdcf6e831e8e6d665a05143914b038491e40c66ba5626f5f32d4ed", "00ab200d222384e46efc63f737ee9c671cacd440d36a007ad989057668868c2a"),
    (1, 46): ("unresolved", "e91b8704c22efd9366871f2d401da981bce30fd2939ae8f15aa35afa9d5fc4ec", "a19e5e5abc76b6ee2993ff277a27ec61fab3ca217d8c14098a058e7a028ff29a"),
    (1, 47): ("unresolved", "354f9371e5037c011ccf27473bfe56934f138af7af69b07a5a995e56888ba55f", "acbaee4b0b6481765b0c6d3b093bd14c1925b8060e7da80b94f1d0d2159ebe71"),
    (2, 112): ("unresolved", "0e9cd3f1363bf2534bc6322b985de7ccd0bd608391ed5268c0a88146a70a60e4", "ea75e96372b675d55698e6598f17ad14b6bd7d50d53892e203c20261ee2299a8"),
    (2, 113): ("unresolved", "c2eb523cdeda57410af6499733f850a0b36d7b1a8e4ae6a30862ccabcd4eea5a", "916bc118e7499b75807dce75391fa295ab096f4cce16303d92f11f2a30d1e416"),
    (2, 114): ("unresolved", "232c1ffccf6a2e8b254408db700798cb22c6e93e5c6ecd5b876df89b86b56e56", "9138fe85c0b9fdf07983f10779c55990c304b29f2a53da9d5662debee9aaa800"),
    (2, 115): ("unresolved", "55424e4b5d2525d0ba45329edad48823e9c476429bdd805448411f992ecb55f0", "ba5643148316e9512c2b3b52104f44e72dbc79289d118fc794f31a842fbb083d"),
    (3, 112): ("unresolved", "a9606f654be8441db6ebf4c09e374e36d882686a70b1a55ed719df3b520278ef", "a4a753ed25a7e5491128d03513b0a6144ee61df7010c6e8316b5bad2b8131186"),
    (3, 113): ("unresolved", "01766bbe80b46122c99622960ad3b653c63dbfbc95830c0b5f98600115e880c3", "fee77ddc756d8f759f08d14b6bef33637f21d88e91710f530b51b46ed421673e"),
    (3, 114): ("unresolved", "a3b904bfce32ebf166f3cea669f8ecd61c2bcd1d84edddb5e168a56a49db26ec", "0c6f6c7fc5f74d4b6c1d05848f3bc1359421defc0195c62f1e20c8d48a3a3456"),
    (3, 115): ("unresolved", "97722d274171137aec7a88f9dd48b3090aed5b208ffdc934c8d520afa8f6dffb", "c4364bc97fa8a38d4208fcbf295fed5a4dc0d26ad27dda64dd53f15585eb011b"),
    (4, 8): ("unresolved", "e101f5dc107c57f6ae22f8b313fe8a50f68ba0fee864f4d93d7c1da264e7b27a", "c7e5d83b9431318f9f2b28da192000c1396254439c789ebb93a79e81169875dc"),
    (4, 9): ("unresolved", "ae54129af03cd28646f9ab06088c8ae88d8bfb13842a4cd57647401439916a01", "b91dc7f8d5aaf70b222822c25aa78cb3794e1cd23c65b8a36db0ea7f02b57caf"),
    (4, 10): ("unresolved", "0924cdba2f6e1c860d93ee10b62274ca820132bfd719ed105bae784d92ce5b3c", "6dc9c89efbc1c11ecc74623c55e1efdbb41f5aadef34785bf4df609b74456045"),
    (4, 11): ("unresolved", "961359d9d8bc55751b69f7257bc0bef47b2354951a34853655b435ae0578c8ee", "375999db17d25bada623789f616957bb161134f9da595bc77027edac4cd496ca"),
    (5, 9): ("separated", "7b3581fa86bcc5227355f29e5af05ae7cf58f935c689aaf025be76501759ec87", "1d8853bd1b165a97c7e80b0c348242e23d1a7bd28b4ccc31ba5c820bc4400a89"),
    (5, 10): ("separated", "1f539d5c46cc970362c17751db0cb896eb553a19b203693baac4f9d1be4ac2e1", "d165ded05c20a61cf64d65cf3cf7bb7b376a213d7a54ae207233e46038a24182"),
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
