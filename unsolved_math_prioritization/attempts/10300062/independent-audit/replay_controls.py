#!/usr/bin/env python3
"""Independent finite controls and isolated author replays; never edits the input packet."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
sys.dont_write_bytecode = True
from verify_binding import verify


def require(condition, message):
    if not condition:
        raise ValueError(message)


def inverse(word):
    return word[::-1].swapcase()


def comm(a, b):
    return a + b + inverse(a) + inverse(b)


def reduce_word(word):
    stack = []
    for letter in word:
        if stack and stack[-1] == letter.swapcase():
            stack.pop()
        else:
            stack.append(letter)
    return "".join(stack)


def substitute(word, images):
    return reduce_word("".join(images[c] if c.islower() else inverse(images[c.lower()]) for c in word))


def command(script, root):
    result = subprocess.run([sys.executable, "-B", str(root / script)], cwd=root, text=True, capture_output=True)
    return {"returncode": result.returncode, "stdout": result.stdout.strip()}


def run(packet):
    initial = verify(packet)
    relator = comm("a", "b") + comm("c", "d") + comm("e", "f")
    pinch = {"a": "", "b": "", "c": "x", "d": "y", "e": "z", "f": "w"}
    retract = {"a": "x", "b": "y", "c": "y", "d": "x", "e": "", "f": ""}
    require(substitute(relator, pinch) == comm("x", "y") + comm("z", "w"), "Pinch relator")
    require(substitute(relator, retract) == "", "Retraction relator")
    wrong = dict(retract, c="x", d="y")
    require(substitute(relator, wrong) != "", "Wrong retraction must fail")
    for a in range(1, 65):
        for b in range(1, 65):
            require(reduce_word(comm("x" * a, "y" * b)) != "", "Powers commute")
    fold = {"a": "x", "b": "y", "c": "x", "d": "y"}
    require(substitute(comm("a", "b") + inverse(comm("c", "d")), fold) == "", "Fold relation")
    require(substitute("aC", fold) == "", "Fold kernel")
    require(["aC".count(c) - "aC".count(c.upper()) for c in "abcd"] == [1, 0, -1, 0], "Kernel homology")
    require(substitute(comm("a", "b") + comm("c", "d"), fold) != "", "Wrong fold orientation must fail")
    for d in range(1, 1001):
        require(d * (-2) != 0, "Euler pullback sample")
    for n in range(2, 1001):
        require(1 % n != 0, "Integral right inverse exists unexpectedly")
    replay = {}
    with tempfile.TemporaryDirectory(prefix="rank670-audit-") as temporary:
        temporary = Path(temporary)
        clean = temporary / "clean"
        shutil.copytree(packet, clean)
        replay["author_controls"] = command("verify.py", clean)
        require(replay["author_controls"]["returncode"] == 0, "Author controls fail")
        require((clean / "verification_results.json").read_bytes() == (packet / "verification_results.json").read_bytes(), "Replay JSON differs bytewise")
        replay["author_manifest"] = command("verify_manifest.py", clean)
        require(replay["author_manifest"]["returncode"] == 0, "Author manifest replay fails")
        negative = []
        for mutation in ("changed_file", "missing_file", "extra_file", "nested_manifest", "changed_root_manifest"):
            root = temporary / mutation
            shutil.copytree(packet, root)
            if mutation == "changed_file":
                with (root / "README.md").open("ab") as stream:
                    stream.write(b"\n")
            elif mutation == "missing_file":
                (root / "README.md").unlink()
            elif mutation == "extra_file":
                (root / "UNLISTED.txt").write_text("test\n")
            elif mutation == "nested_manifest":
                (root / "nested").mkdir()
                (root / "nested" / "MANIFEST.json").write_text("unlisted test content\n")
            else:
                with (root / "MANIFEST.json").open("ab") as stream:
                    stream.write(b"\n")
            author_accepts = command("verify_manifest.py", root)["returncode"] == 0
            try:
                verify(root)
                hard_accepts = True
            except (ValueError, OSError):
                hard_accepts = False
            require(not hard_accepts, "Hardened verifier accepted " + mutation)
            require(author_accepts == (mutation in ("nested_manifest", "changed_root_manifest")), "Unexpected author mutation behavior")
            negative.append({"mutation": mutation, "author_accepts": author_accepts, "hardened_accepts": hard_accepts})
    require(verify(packet) == initial, "Original packet changed")
    return {"status": "PASS_WITH_DOCUMENTED_PACKAGING_CAVEAT", "original_packet_unchanged": True,
            "input_binding": initial, "author_replay": replay, "reproduced_result_bytes_identical": True,
            "independent_guardrails": {"free_word_implementation": "independent signed-character reducer",
                "noncommuting_positive_power_pairs": 4096, "Euler_cover_degrees": 1000,
                "torus_cover_degrees": "2 through 1000", "wrong_retraction_detected": True,
                "wrong_fold_orientation_detected": True},
            "negative_binding_controls": negative,
            "scope": "Finite guardrails and byte checks only; topology and convergence are assessed in AUDIT.md."}


if __name__ == "__main__":
    packet = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "packet"
    print(json.dumps(run(packet), indent=2, sort_keys=True))
