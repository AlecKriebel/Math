#!/usr/bin/env python3
"""Independent first-column checks of primary ordinary ctbllib source data.

This limited reader never evaluates GAP code or imports the author's verifier.
It handles the literal rows and GALOIS row references in the selected tables.
"""
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import re

HERE = Path(__file__).resolve().parent
SOURCES = HERE.parent / "sources"
TARGETS = {
    "A5": ("ctoalter.tbl", 3),
    "A6": ("ctoalter.tbl", 5),
    "A7": ("ctoalter.tbl", 6),
    "L3(2)": ("ctoline4.tbl", 3),
    "U4(2)": ("ctounit3.tbl", 5),
    "U3(3)": ("ctounit2.tbl", 7),
    "U4(3)": ("ctounit1.tbl", 189),
    "J2": ("ctoconja.tbl", 63),
    "L3(4)": ("ctoline3.tbl", 20),
}


def split_outer(text):
    """Split commas outside strings, brackets, and parentheses."""
    parts = []
    start = 0
    brackets = 0
    parentheses = 0
    quoted = False
    escaped = False
    for index, char in enumerate(text):
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            continue
        if char == '"':
            quoted = True
        elif char == '[':
            brackets += 1
        elif char == ']':
            brackets -= 1
        elif char == '(':
            parentheses += 1
        elif char == ')':
            parentheses -= 1
        elif char == ',' and brackets == 0 and parentheses == 0:
            parts.append(text[start:index].strip())
            start = index + 1
        assert brackets >= 0 and parentheses >= 0
    assert not quoted and brackets == 0 and parentheses == 0
    parts.append(text[start:].strip())
    return parts


def call(source, prefix):
    index = source.index(prefix)
    start = source.index('(', index) + 1
    depth = 1
    quoted = False
    escaped = False
    for end in range(start, len(source)):
        char = source[end]
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            continue
        if char == '"':
            quoted = True
        elif char == '(':
            depth += 1
        elif char == ')':
            depth -= 1
            if depth == 0:
                return split_outer(source[start:end]), source[:index].count('\n') + 1
    raise AssertionError("unclosed call")


def list_entries(text):
    assert text.startswith('[') and text.endswith(']')
    return [item for item in split_outer(text[1:-1]) if item]


def row_degrees(text):
    answer = []
    for row in list_entries(text):
        columns = list_entries(row)
        if re.fullmatch(r'\d+', columns[0]):
            degree = int(columns[0])
        else:
            assert columns[0] == "GALOIS", columns[0]
            reference = list_entries(columns[1])
            degree = answer[int(reference[0])-1]
        assert degree > 0
        answer.append(degree)
    return answer


def valuations(number):
    out = {}
    for prime in (2, 3, 5, 7):
        exponent = 0
        while number % prime == 0:
            exponent += 1
            number //= prime
        out[prime] = exponent
    assert number == 1
    return out


def main():
    sources = {}
    tables = {}
    outputs = {}
    for name, (filename, witness) in TARGETS.items():
        source = sources.setdefault(filename, (SOURCES / filename).read_text())
        arguments, line = call(source, f'MOT("{name}",')
        assert arguments[0] == json.dumps(name)
        centralizers = [int(item) for item in list_entries(arguments[2])]
        degrees = row_degrees(arguments[4])
        assert len(degrees) == len(centralizers)
        assert sum(d*d for d in degrees) == centralizers[0]
        assert witness in degrees
        tables[name] = degrees
        outputs[name] = {
            "file": filename,
            "MOT_line": line,
            "source_sha256": sha256((SOURCES / filename).read_bytes()).hexdigest(),
            "group_order": centralizers[0],
            "degrees": degrees,
            "witness": witness,
            "witness_occurrences": degrees.count(witness),
            "square_mass_and_class_count_match": True,
        }

    assert Counter(tables["A7"]) == Counter((1, 6, 10, 10, 14, 14, 15, 21, 35))
    projective_args, line = call(sources["ctoalter.tbl"], 'ARC("A7","projectives",')
    sections = list_entries(projective_args[2])
    assert len(sections) == 6
    projectives = {}
    for index in range(0, len(sections), 2):
        name = json.loads(sections[index])
        degrees = row_degrees(sections[index+1])
        assert sum(d*d for d in degrees) == 2520
        projectives[name] = degrees
    assert 4 in projectives["2.A7"]
    assert 24 in projectives["3.A7"]
    assert 24 in projectives["6.A7"]
    # The ConstructProj ordinary-table constructors assemble sectors by the
    # order of the cyclic central character. Galois conjugate sectors have
    # the same degrees; phi(2)=1, phi(3)=phi(6)=2.
    full_covers = {
        "2.A7": tables["A7"] + projectives["2.A7"],
        "3.A7": tables["A7"] + projectives["3.A7"] * 2,
        "6.A7": tables["A7"] + projectives["2.A7"]
                + projectives["3.A7"] * 2 + projectives["6.A7"] * 2,
    }
    covers = {}
    for name, degrees in full_covers.items():
        multiplier = int(name.split('.')[0])
        assert sum(d*d for d in degrees) == multiplier * 2520
        witness = 4 if name in ("2.A7", "6.A7") else 24
        assert witness in degrees
        constructor, constructor_line = call(sources["ctoalter.tbl"], f'MOT("{name}",')
        assert constructor[4] == "0"
        assert '"ConstructProj"' in constructor[6]
        assert len(degrees) == len(list_entries(constructor[2]))
        covers[name] = {
            "ordinary_constructor_MOT_line": constructor_line,
            "projective_sectors_ARC_line": line,
            "ordinary_degrees": degrees,
            "witness": witness,
            "witness_occurrences": degrees.count(witness),
            "group_order": multiplier * 2520,
            "square_mass_and_class_count_match": True,
            "interpretation": "Ordinary central-cover characters, not modular Brauer characters",
        }

    exclusions = {}
    for degree in (2, 3, 4, 5, 7, 20, 24, 63, 189):
        data = valuations(degree)
        omega = sum(data.values())
        balance = all(exp <= omega-exp for exp in data.values())
        assert omega % 2 or not balance
        exclusions[str(degree)] = {
            "valuations_at_2_3_5_7": data,
            "total_prime_factor_multiplicity": omega,
            "even_total": omega % 2 == 0,
            "balanced_at_every_prime": balance,
            "excluded_from_A7_degree_monoid": True,
        }
    report = {
        "checked_utc": datetime.now(timezone.utc).isoformat(),
        "checker_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "method": "Independent lexical reader of selected ordinary GAP library source rows",
        "ordinary_simple_table_checks": outputs,
        "central_cover_checks": covers,
        "monoid_exclusions": exclusions,
        "verdict": "All selected ordinary-degree witnesses and exact monoid exclusions pass",
        "limitations": "Library data are checked as external primary data; this is not a character-table construction from group matrices",
    }
    (HERE / "independent_degree_witness_results.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps({"ordinary_tables_checked": len(outputs),
                      "central_covers_checked": len(covers),
                      "monoid_exclusions_checked": len(exclusions)}, sort_keys=True))


if __name__ == "__main__":
    main()
