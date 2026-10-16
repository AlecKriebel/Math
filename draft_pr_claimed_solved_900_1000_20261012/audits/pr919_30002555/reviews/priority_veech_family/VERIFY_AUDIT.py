#!/usr/bin/env python3
"""Read-only verification of this priority audit seal, originals and source pins.

This authenticates artifacts and exact arithmetic. It is not formal proof checking,
human review, a search-completeness test, or a firstness certificate.
"""
from pathlib import Path
import hashlib
import json
from fractions import Fraction

D = Path(__file__).resolve().parent
B = D.parent.parent


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run():
    original = json.loads((B / 'ORIGINAL_SNAPSHOT.json').read_text())
    frozen = [digest(B / 'original' / p) == h for p, h in original['files'].items()]
    manifest = json.loads((D / 'MANIFEST.json').read_text())
    listed = {r['path'] for r in manifest['files']}
    actual = {str(p.relative_to(D)) for p in D.iterdir() if p.is_file() and p.name != 'MANIFEST.json'}
    public_ok = listed == actual and all(
        digest(D / r['path']) == r['sha256'] and (D / r['path']).stat().st_size == r['size']
        for r in manifest['files']
    )
    sources = json.loads((D / 'SOURCE_MANIFEST.json').read_text())
    available_private_pins = []
    for r in sources['sources']:
        if 'sha256' not in r:
            continue
        suffix = '.pdf' if r.get('content_type', '').startswith('application/pdf') else '.html'
        p = D / 'private' / (r['key'] + suffix)
        if p.exists():
            available_private_pins.append(digest(p) == r['sha256'] and p.stat().st_size == r['size'])
    q = json.loads((D / 'QUERY_LOG.json').read_text())
    a, b = Fraction(3, 5), Fraction(4, 5)
    exact_norm_and_det = a*a + b*b == 1
    out = {
        'frozen_27_match': len(frozen) == 27 and all(frozen),
        'pinned_head': original['head'],
        'proof_sha256': digest(B / 'original/unsolved_math_prioritization/attempts/30002555/public/PROOF.md'),
        'curated_public_manifest_exact': public_ok,
        'available_private_source_pins_match': all(available_private_pins),
        'available_private_bodies_checked': len(available_private_pins),
        'all_53_search_strings_recorded': sum(len(x['search_queries']) for x in q['batches']) == 53,
        'nineteen_web_batches_recorded': len(q['batches']) == 19,
        'raw_directory_ignored': (D / '.gitignore').read_text().strip() == 'private/',
        'witness_exact_orthogonality_and_det_one': exact_norm_and_det,
        'infinite_order_proof': 'all-n recurrence in PRIOR_BRIDGE.md, not finite-power testing',
        'firstness_certified': False,
        'formal_or_human_review_claimed': False,
    }
    out['pass'] = all(out[k] for k in [
        'frozen_27_match', 'curated_public_manifest_exact',
        'available_private_source_pins_match', 'all_53_search_strings_recorded',
        'nineteen_web_batches_recorded', 'raw_directory_ignored',
        'witness_exact_orthogonality_and_det_one',
    ])
    return out


if __name__ == '__main__':
    result = run()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['pass'] else 1)
