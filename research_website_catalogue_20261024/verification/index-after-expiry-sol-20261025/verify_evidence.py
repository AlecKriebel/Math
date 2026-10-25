#!/usr/bin/env python3
"""Read-only audit of retained browser evidence and frozen prior bindings."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import struct

HERE = Path(__file__).resolve().parent
PROGRAMME = HERE.parents[1]
INDEX = 'https://aleckriebel.com/research/'
EXPECTED = {
    '23393596': INDEX + 'deep-derived-pure-braids-not-one-solvable/',
    '23358014': INDEX + 'critical-wave-sparse-control-quadratic-growth/',
    '23356964': INDEX + 'generic-cantor-actions-wreath-product-hyperfinite/',
}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def jpeg_dimensions(path):
    raw = path.read_bytes()
    assert raw[:2] == b'\xff\xd8'
    at = 2
    while at < len(raw):
        assert raw[at] == 255
        while raw[at] == 255:
            at += 1
        marker = raw[at]
        at += 1
        length = struct.unpack('>H', raw[at:at + 2])[0]
        if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                      0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            height, width = struct.unpack('>HH', raw[at + 3:at + 7])
            return {'width': width, 'height': height}
        at += length
    raise AssertionError('No JPEG dimensions found')

def audit():
    events = json.loads((HERE / 'navigation-events-after-reset.json').read_text())
    captures = json.loads((HERE / 'capture-events.json').read_text())
    labels = [e['label'] for e in events]
    assert len(labels) == len(set(labels)) == 22
    for e in events:
        assert json.loads((HERE / (e['label'] + '.json')).read_text()) == e
        assert (HERE / (e['label'] + '.dom.txt')).is_file()
        assert (HERE / (e['label'] + '.ax.txt')).is_file()
    first = next(e for e in events if e['label'].startswith('03-'))
    assert first['action']['initiatedUTC'] >= '2026-10-25T04:57:25'
    assert first['data']['observedUTC'] >= '2026-10-25T04:57:25'
    baseline_urls = [li['links'][0]['href'] for li in first['data']['mainListItems']]
    assert len(baseline_urls) == len(set(baseline_urls)) == 47
    index_rows = []
    for e in events:
        d = e['data']
        if d['url'] != INDEX:
            continue
        urls = [li['links'][0]['href'] for li in d['mainListItems']]
        present = {record: url in urls for record, url in EXPECTED.items()}
        assert len(d['mainListItems']) == len(d['allListItems']) == 47
        assert urls == baseline_urls
        assert all(present.values())
        assert d['canonical'] == INDEX
        assert d['documentWidth'] <= d['viewport']['width']
        index_rows.append({
            'label': e['label'], 'utc': d['observedUTC'],
            'url': d['url'], 'canonical': d['canonical'],
            'viewport': d['viewport'], 'count': 47,
            'unique_article_title_urls': len(set(urls)),
            'all_three_expected_title_links_present': present,
            'same_ordered_47_article_urls': True,
            'method': e['action']['method'],
        })
    routes = []
    for width, height, article_prefixes, return_prefixes in [
        (2056, 1146, ['05-', '07-', '09-'], ['06-', '08-', '10-']),
        (390, 844, ['19-', '21-', '23-'], ['20-', '22-', '24-']),
    ]:
        for record, ap, rp in zip(EXPECTED, article_prefixes, return_prefixes):
            a = next(e for e in events if e['label'].startswith(ap))
            r = next(e for e in events if e['label'].startswith(rp))
            assert a['data']['url'] == a['data']['canonical'] == EXPECTED[record]
            assert r['data']['url'] == r['data']['canonical'] == INDEX
            assert a['action']['from'] == INDEX
            assert r['action']['from'] == EXPECTED[record]
            for e in (a, r):
                assert e['data']['viewport']['width'] == width
                assert e['data']['viewport']['height'] == height
                assert e['data']['documentWidth'] <= width
            assert a['data']['observedUTC'] < r['data']['observedUTC']
            routes.append({'record': record, 'width': width, 'height': height,
                           'article_state': a['label'], 'article_utc': a['data']['observedUTC'],
                           'return_state': r['label'], 'return_utc': r['data']['observedUTC'],
                           'article_url': EXPECTED[record], 'return_index_count': 47,
                           'article_activation': a['action']['method'],
                           'return_activation': r['action']['method'],
                           'PASS': True})
    screenshot_rows = []
    assert len(captures) == len({c['label'] for c in captures}) == 20
    for c in captures:
        p = HERE / (c['label'] + '.jpg')
        dims = jpeg_dimensions(p)
        assert p.stat().st_size == c['bytes']
        assert dims['width'] == c['viewport']['width']
        assert dims['height'] == c['viewport']['height']
        screenshot_rows.append({**c, 'path': str(p), 'sha256': sha(p),
                                'JPEG_dimensions': dims, 'retained': True})
    assert len(list(HERE.glob('*.jpg'))) == 20
    cleanup = json.loads((HERE / 'cleanup.json').read_text())
    assert cleanup['allInitialUserTabIdsRemain']
    assert cleanup['protectedSheet963520539Present']
    assert not cleanup['protectedSheetClaimed']
    assert cleanup['remainingOwnTabs'] == []
    assert cleanup['viewportOverrideReset']
    before = json.loads((HERE / 'preservation-before.json').read_text())
    frozen = []
    for m in before['manifests']:
        p = Path(m['path'])
        d = json.loads(p.read_text())
        checks = []
        assert sha(p) == m['sha256']
        for f in d['files']:
            fp = Path(f['path'])
            match = sha(fp) == f['sha256'] and fp.stat().st_size == f['bytes']
            assert match, str(fp)
            checks.append({'path': str(fp), 'bytes': fp.stat().st_size,
                           'sha256': sha(fp), 'match': match})
        assert len(checks) == m['files_checked']
        frozen.append({'path': str(p), 'sha256': sha(p), 'files_checked': len(checks),
                       'all_match': True, 'checks': checks})
    return {
        'utc': datetime.now(timezone.utc).isoformat(),
        'status': 'BOUNDED_POST_EXPIRY_ORDINARY_INDEX_NAVIGATION_PASS',
        'index_task_completion_estimate_percent': 100,
        'full_browser_PASS': False,
        'publication_tracker_acceptance': False,
        'navigation_state_records': len(events),
        'actual_index_observations': len(index_rows),
        'index_counts_observed': sorted({r['count'] for r in index_rows}),
        'completed_article_title_and_header_return_routes': len(routes),
        'first_post_expiry_index_observation_utc': first['data']['observedUTC'],
        'first_post_expiry_header_click_utc': first['action']['initiatedUTC'],
        'index_rows': index_rows, 'routes': routes,
        'ordered_47_article_title_urls': baseline_urls,
        'screenshot_count': len(screenshot_rows),
        'screenshots': screenshot_rows, 'preserved_frozen_manifests': frozen,
        'cleanup_utc': cleanup['utc'],
        'pointer_activation_exception': {
            'attempt': '12-mobile-23393596-actual-title-link',
            'current_state_check': '18-mobile-state-after-navigation-race',
            'actual_result': 'Index remained at canonical URL with 47 items after click; no article navigation verified.',
            'successful_alternative': '19-mobile-23393596-title-enter-success',
            'cause': 'Not established; label navigation-race is an attempted descriptive label, not a causal finding.',
        },
    }

if __name__ == '__main__':
    result = audit()
    # Optional report destinations must be new files; the default run is read-only.
    import sys
    if len(sys.argv) == 2:
        with Path(sys.argv[1]).open('x') as handle:
            json.dump(result, handle, indent=2)
            handle.write('\n')
    print(json.dumps({k: v for k, v in result.items() if k not in
                     ('index_rows', 'routes', 'ordered_47_article_title_urls',
                      'screenshots', 'preserved_frozen_manifests')}, indent=2))
