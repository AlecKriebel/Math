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

if not __debug__:
    raise SystemExit("K2P_PORTABLE_OPTIMIZED_MODE_FORBIDDEN")

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
EXPECTED_MERGED_FILE_SHA256 = "6db7342e82c0007e9d2339bf4e235ac20633893e3272c7d8782d864634f897ea"
EXPECTED_MERGED_PAYLOAD_SHA256 = "1362ddc19c7b69b460b0d1790b8199df098df115aa73281800360b7cfa194959"
EXPECTED_SWEEP_SHA256 = "166bdb02b44a0a5068c79d2302275cd01c1ac835f59cbce6368c989a615f800c"
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
        "a5bc5f71b1891988aab1050c3096683b9b8ee22291d3bb7c2e76ac6be97fd6b8",
        "d98d89ef3c1cdbcefd8399f878ccdbc3389a99148124592f447bddd02d27c467",
    ),
    1: (
        "c779b86d5ad3ac8a57dcd9cefea453b52eaa3de0c995bf13a09af1fa51406559",
        "6c66b09943bb1f07d9c2d94ffdf3aaab26a51b6cf6fb28d587820fb27b5bf515",
    ),
    2: (
        "0533eac31babd5a7d5e08da9158da433405d8551c0568ee2ec58d3ce7fb62d6e",
        "725217217f5a0d70b90588002a183939bcc88755e86918dd28ed18e0a5afe8f7",
    ),
    3: (
        "f340bb48f42620b7aec3e282d12789b408cc16a71588c5da6ddd41b26a985c22",
        "c9321d92b4d1fc567ed2a805595911329da8a381f82514362ea4597a8af67778",
    ),
    4: (
        "cebc1c7efcd356b951a59fe6c9de562104807109053965e59bbb923410109636",
        "f8476e607e19cd578909e6d3fa027ecc980fb05570a0d3833c04004e9775fb2b",
    ),
    5: (
        "2b796fc9a4cd1f55780f77e62b81721e1e84f6cbfc515fdbf686c0cbfc083d57",
        "89c26b40eec81f327cfca8fca5afacc9868fded5f8db837965ddfacfba9bb307",
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
    (1, 25): ("unresolved", "8055a51bd742bb95b4ca13bfe5d93342d7c5d951e8a97f992df145600b71e1b7", "c43ccea29a5ddb32482dea2f70480e6b64ed09a9264e3825e2af733f301325c7"),
    (1, 26): ("unresolved", "a0e1b48d3ed38f83661e7beb6ad87314a43c50cfb8db46984cbce7d760386914", "f804907764b9aa6e14a7a676cf9865b7e7b3803a522211823a78a02cfb1974dc"),
    (1, 27): ("unresolved", "7243b77296e0f9335e7af93399cd7f15518e239b816ef1d9d6770a4f7e625a7f", "ef1045e7db5a0a69bd50ea90ba3a195f417ea12295fb5654ce7160383aa122c0"),
    (1, 28): ("unresolved", "11c48c5d856d22c5b7d6425553f63018de30a8b9c486d62781e3ae84a0d756db", "37f13f15c9a56934c8ab28db362da5afd32d6c37ab693f5b5aba5b89ec809712"),
    (1, 29): ("unresolved", "f22cfa761c0973f886eb7641d0f56af768c949c0a97417aeed4500081dde409b", "4f72757af522b4cf22dd705c18873c719db395fb7b6e6e7ca5aa3968f6ad7ed5"),
    (1, 30): ("unresolved", "8ff4e0c0e64625f5ff404e8873e1606b541f9d2d926a3bccd150ad86bb4a3313", "363071f3dfc4f3b6c3e08eb24589745697b6df020f938d718f4c1b5c228ec4de"),
    (1, 31): ("unresolved", "c45e45cdc46ce35d7a998c02a02cbb3efa3b7d72221d0b13ba01851648b5db2d", "9caa7eafaa85affc8f736c1fbb43bbb6e1092538f1ae98ab85edd1b2ee04038c"),
    (1, 32): ("unresolved", "9e3592b53639720661e50067452a3af5123597bcb75b7ac126c81e12fa1702cc", "a75025dd20c6a79593ce95f501245d27070ce8a8132e9dce5b76aa85eb2d7218"),
    (1, 33): ("unresolved", "1531c6534b4213107944e934683adf0efa72d737ea4b458990696f444385b592", "5f8dba99deea1a22954a2c77462f9c89d6af1127a06143c810be5acf4d810d9f"),
    (1, 34): ("unresolved", "eb2ee00b93c2f98f52fd093be09b0e05812f935e98cab54e4519862786405d57", "5c9d5c116abdf76a22dca032350153c0613ad95eb63bb85dd79c5bedf24558f8"),
    (1, 35): ("unresolved", "878e8773bf3e9683f47081ebc0f623dc48ee8a8820203fcf6aaef4d80eac4ccd", "b6e55ee6ed490d3895fc4d04ae7055e7bc9afda6b3cff861f3bb0400d4ec03ff"),
    (1, 36): ("unresolved", "ccbfe5d9bcde98f5de5a4ac702b87fe27df1143cfb80da12746d9d77dc644058", "0ce142ce70f8cbedd1c29a55a1d751c35a780fcdb6977cf648bf4a4b54c9ecfd"),
    (1, 37): ("unresolved", "d07329e646d1244a4ab59b51aa89409aa02596cb9279508fe2510f46c8def07f", "e123da4186d0916df5c443b6d602b8d80d6884c14e6f42a62208e529e8d15fd8"),
    (1, 39): ("unresolved", "526ad1df3b703772d8fb8f9048c8d71f0f42b0004fc895cc799b0ff9efab5bc8", "bea8c8eadd7e86ff5651c9412cc113b693d1fc406465af6d95528b2b0fd73d1c"),
    (1, 40): ("unresolved", "f17a0da132093c5acc1256960024c3fef0f36406f5f064d902d9277f6d1148f5", "6f7fd4312506f692d68f6b89c324a9f65e7342e633a8466202479d02d3c2dc41"),
    (1, 41): ("unresolved", "1eb8834b8ec2ee8238b120fdedd166bd93c9768ca88dae5427c590f8f2b52bfa", "b0383ef4aa3dade5e5e6033fded004d2757c1aa1b8438007c8b56fd9f362cff9"),
    (1, 42): ("unresolved", "b9b8d544a36831c3f669c08ae3dbb5a9cdd7a9b60eab0e9cb716f9d4d1a3b0b7", "20837a597bdd0cb82ae676e04a96e9261d06856aa0f5bb7bda1a849d46c45dcb"),
    (1, 43): ("unresolved", "b407ba27b80b3ec38353cbdcc1326e9d6324c0db6b08b9f3f7aa9f3ce125c6ea", "82aaf53e08698d56d1cf804641a2dc7504715b45cf0e56f797cc2e2251cd0981"),
    (1, 44): ("unresolved", "fd01bef1a90107daabbd8811fa50245c6870f5c4d9b627a40c3d9503c563ae4f", "58b6eb5530540f153baa5b607529893aa35a5fcaebb108df47e6212d19514461"),
    (1, 45): ("unresolved", "5141b9d116d0432162bda06c484d30e766f94288748208387a4e2153e62bd398", "46885769651f141eb9f1a0ecad5a2542166fdb4ef6c39624a8ab7a9ce443a991"),
    (1, 46): ("unresolved", "7e9f8126bd7dfd65994359b50eb9898aea4346137a91b87ec3ebca7ad28db729", "da0bf2cbf2fa2db845c67d680dccb26ae568532bd76157dd4bd776d6250d42f5"),
    (1, 47): ("unresolved", "4b9953e4168d5e287b477d040fc0e73bdd31cad729a782859b685a2c515ff723", "9af6d440320fcd64319d24fd042251a66735981cbe456ae6a671253f5351b00d"),
    (2, 112): ("unresolved", "626a723f856ae40a5e6a4a52118ea67fff2798b99ccc372ba5de3b33c8a6e4a9", "e34c92366bb6fb8c32ac556180abe5c347f92bb5859c2b2429a394b2e4b6403d"),
    (2, 113): ("unresolved", "e173e18cd626ccec13a09395db2e7fbac876237538ffb094038fa9b96ef1212f", "80638e3cc825f31f9a382c98bbc0d6bbf3229a2102fe3ea74382ba84cf5cec71"),
    (2, 114): ("unresolved", "1fc7fba2972dad8cd84ac1e0bfb795d577bff96e27c0de9989543c7dd60c3f29", "493d3612623a666e6858ffef0dac11b06252201046ee218d8038a4df2910c596"),
    (2, 115): ("unresolved", "0a86072e65803b031a6bcacad5673644dbe418ef860ea2cc3328f2326f4a6283", "1b9e8a36f16be620ac70b0da130c8c9c2b0f6f09fbcea4f70d147ad65fa28a22"),
    (3, 112): ("unresolved", "e2627c64cd3b93cf3fe8687e7a618a2548505808799ba6cdc7d0296803ac8c62", "31a1a21d0ffeb957964fe8efc3b1b2bed7e6fb6a60f87bf77383ec0a33cb421b"),
    (3, 113): ("unresolved", "3537213fffc48978abf2cd03f48e1b898e73c7130ce7b8e3167dc9f7e1db0a96", "bc512f5edfa70c1e6571b0cb94cf15a6d3a3fda9d520ebb580dcfc79bae77aaa"),
    (3, 114): ("unresolved", "4acd4913f59ca9212fbb9914d3059f0558cd92e1d770712cf1fda03accb8198a", "6075a50cd2ec30c1894cfe114994df035fb742830be54389b24d022b2b1762a2"),
    (3, 115): ("unresolved", "b5f092eed8605be965bf48e232c0b99eee45e7337a904ab4d0eff0785b9bd3bd", "eaa00bdc61b9dc5704f73e6b70ebfdc4957bcacab00e7e6d67320e4c839a5774"),
    (4, 8): ("unresolved", "d6f701dd9b5b71e6876cae2cd3709bfe6c3ad97d94ab451d9fe236146060ece5", "4e2c8a18b9f4d29c124cadd2af5830537fde4df51b680c168ce53c013d264c56"),
    (4, 9): ("unresolved", "49e32404545c2a0ea40e8a84f65e25014fb58e2ee0ef450e1b1db881512cf933", "2a75329c4c33747ceb2de526c924c27477611051238b477d88dcd3e6bc1c5c2c"),
    (4, 10): ("unresolved", "150cfaf25d69fc6ee88dd508b5819ad0c7d5df4c042bdf06b74e990d801e726c", "6ba7abe70cb8f3781aff7d586338b2b35b5204df8ac602e30ce047bda780e405"),
    (4, 11): ("unresolved", "8a75ef4775d01c663180f4d142ee5ed54222deaa9817bdbbc6fe74ec68a989d1", "2f25aee71a207ab3a7403b476d9b784c644949ded72fb3008f09b759f2bcc2e2"),
    (5, 9): ("separated", "e6380a9c893bfc62cc6df78b5f5504ed6cbf8c421b73fc42d02e71e8c9425f88", "7f4140b2f98050664b320880661540571c8f690843b2a5308a3242c9872622bf"),
    (5, 10): ("separated", "c08de2fd42ccbb78574f29ea89994b678365cb1239c96352e9e1006d8c966614", "ae46ae184a9f25d3145e33ba8b527c89f3b91dc6fa7fac5b1306704c8b4c33bf"),
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


def explicit_check(condition: bool, code: str, detail: object | None = None) -> None:
    """Fail without a traceback for mutation-qualified certificate bindings."""

    if not condition:
        raise SystemExit(code if detail is None else f"{code}: {detail}")


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
    explicit_check(
        digest(quintic) == quintic_artifact["invariant_sha256"],
        "DIRECT_QUINTIC_ARTIFACT_HASH_FAIL",
    )
    explicit_check(
        digest(quintic) == EXPECTED_QUINTIC_SHA256,
        "DIRECT_QUINTIC_EXPECTED_HASH_FAIL",
    )
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
        explicit_check(
            digest(polynomial) == EXPECTED_QUARTIC_SHA256[name],
            "DIRECT_QUARTIC_EXPECTED_HASH_FAIL",
            name,
        )
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
    explicit_check(
        normalized_artifact_cubic == CUBIC,
        "DIRECT_CUBIC_ARTIFACT_TERMS_FAIL",
    )
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
