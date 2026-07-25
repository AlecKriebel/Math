#!/usr/bin/env python3
"""Deterministic aggregate replay of both characteristic-two witnesses."""

from __future__ import annotations

import hashlib
from pathlib import Path

from verify_char2_support_witness import parse_witness, verify


ROOT = Path(__file__).resolve().parent
EXPECTED = {
    1: {
        "json_semantic": (
            "fc5b7f7bd19250731d148bdbae1200cb64b08851bd8e28d5f0047d5983273dc4"
        ),
        "text_sha256": (
            "3f77fc3d39fc6b8dfd33efbba846e61ca835581d15f9ae4c12d8f57a3249e697"
        ),
    },
    2: {
        "json_semantic": (
            "2f03cbaaf514b4a90bd4aa7ad7f533b8abd9e0b1fddb724aeb40d718db51465c"
        ),
        "text_sha256": (
            "2e5087308dceb18398daaba4b1ca5868d755cecb41ae7892f988ae8083c03c22"
        ),
    },
}


def main() -> None:
    for quotient_type in (1, 2):
        text_path = ROOT / f"TYPE{quotient_type}_SUPPORT_WITNESS.txt"
        json_path = ROOT / f"TYPE{quotient_type}_SUPPORT_WITNESS.json"
        text_type, text_words, text_digest = parse_witness(text_path)
        json_type, json_words, json_digest = parse_witness(json_path)
        assert text_type == json_type == quotient_type
        assert text_words == json_words
        assert text_digest == EXPECTED[quotient_type]["text_sha256"]
        assert json_digest == EXPECTED[quotient_type]["json_semantic"]
        assert (
            hashlib.sha256(text_path.read_bytes()).hexdigest()
            == EXPECTED[quotient_type]["text_sha256"]
        )
        verify(json_path)
    optimized_text = ROOT / "TYPE1_SUPPORT_WITNESS_CARRY672.txt"
    optimized_json = ROOT / "TYPE1_SUPPORT_WITNESS_CARRY672.json"
    text_type, text_words, text_digest = parse_witness(optimized_text)
    json_type, json_words, json_digest = parse_witness(optimized_json)
    assert text_type == json_type == 1
    assert text_words == json_words
    assert (
        text_digest
        == "bb6d7431ace29949e0af8077afdd7377b7dd3c615832e197562018fe18eee060"
    )
    assert (
        json_digest
        == "7d6e7d1827a4129fc12916c3007772511e40bd011f6b5193349029de3522aaae"
    )
    verify(optimized_json)
    print("aggregate_status PASS")
    print("witness_types 1 2")
    print("optimized_type1_mod4_carry 672/1503")
    print("scope adjacency_mod2 conference_core_mod8")


if __name__ == "__main__":
    main()
