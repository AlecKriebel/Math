#!/usr/bin/env python3
"""Independent packet controls; these checks do not prove an analytic theorem."""
from pathlib import Path
from fractions import Fraction
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    'PROOF_VERIFICATION.md': '2e34ca15ff80b3a6c435b25bd0c09833eeac0e1fdc71509bfde6ceee3766fc6d',
    'README.md': '3d17d4b4ffb33cade6709413c5af840d0ddbc8984b89a89f3b505fb6b0e09ba6',
    'RESEARCH_LOG.md': 'df9183d612b02d4d83203bdcf5dbaeed5e59ae4e8d44d2700a630223492279d5',
    'SOURCE_GATE.md': '96a139997f84b7abc898def009038425d843e420f8e553e73c9f7fc228c8c45d',
    'STATUS.json': '585a047bedd3b1718e78ee1722fa0fc769c5328a750b6d728a6228bc38d6f1e4',
    'turn_01.md': '604cc1bfc483664f50ad7ea6090bddf7ae195ab98b236a37dae599188baf6e0f',
}
ART = ROOT / 'artifacts'
sha = lambda b: hashlib.sha256(b).hexdigest()
checks = {}
checks['exact_six_file_allowlist'] = {p.name for p in ART.iterdir() if p.is_file()} == set(EXPECTED)
checks['frozen_hashes_preserved'] = all(sha((ART / name).read_bytes()) == digest for name, digest in EXPECTED.items())
status = json.loads((ART / 'STATUS.json').read_text())
def scoped_status(s):
    return (
        s['problem_id'] == 2302005
        and s['problem_code'] == 'AMR-022-2005'
        and s['queue_rank'] == 518
        and s['proposed_status'] == 'already_solved'
        and s['substantive_attempts'] == 1
        and s['specific_two_value_question_resolved'] is True
        and s['general_classification_provided'] is False
        and s['novel_result_claimed'] is False
        and s['new_paper_or_doi_warranted'] is False
    )
checks['finite_question_status_scope'] = scoped_status(status)
checks['internal_links_exist'] = all(
    (p.parent / target.split('#')[0]).is_file()
    for p in ART.glob('*.md')
    for target in re.findall(r'\]\(([^)]+)\)', p.read_text())
    if not target.startswith(('https://', 'http://', '#'))
)
checks['logarithmic_error_decays_faster'] = Fraction(5, 3) > Fraction(5, 4)
checks['other_terms_decay_faster'] = Fraction(2) > Fraction(5, 4)
checks['power_map_exponent_comparison'] = Fraction(5, 4) < 2
# At delta < 1/4, 1/(1+2/delta) < 1/9 < 1/3, as used in the proof.
checks['radial_separation_exponent_comparison'] = Fraction(1, 9) < Fraction(1, 3)
checks['keldysh_power_compatibility'] = Fraction(1, 4) < Fraction(1, 2)

negative_controls = {}
bad = dict(status, general_classification_provided=True)
negative_controls['overbroad_classification_rejected'] = not scoped_status(bad)
bad = dict(status, novel_result_claimed=True)
negative_controls['novelty_claim_rejected'] = not scoped_status(bad)
negative_controls['ocr_one_half_error_rejected'] = not (Fraction(1, 2) > Fraction(5, 4))
name = 'PROOF_VERIFICATION.md'
negative_controls['changed_frozen_bytes_rejected'] = sha((ART / name).read_bytes() + b'\n') != EXPECTED[name]

result = {
    'problem_id': 2302005,
    'scope': 'Exact frozen bytes, public file allowlist, statement metadata, relative links, and elementary exponent comparisons only. Not a proof or numerical certification of entire-function existence or approximation.',
    'checks': checks,
    'negative_controls': negative_controls,
    'passed': all(checks.values()) and all(negative_controls.values()),
}
print(json.dumps(result, indent=2, ensure_ascii=False))
raise SystemExit(0 if result['passed'] else 1)
