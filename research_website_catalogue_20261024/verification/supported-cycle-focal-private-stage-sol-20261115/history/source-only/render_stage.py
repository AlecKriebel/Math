"""New source-only private leaf adapter; no aggregate/live/Git or upstream programme execution.
The full-stage aggregate adapter must be completed only from the later actual623 baseline.
"""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import hashlib
import json
import verify_stage as V

O = Path(__file__).resolve().parent


def source_leaves():
    inputs = V.source_fences()
    rows = {r['path']: r for r in inputs['files']}
    def cached(path):
        row = rows[str(path)]
        return V.pin(O / row['blob'], row)
    output = {}
    for item in inputs['records']:
        rid = item['record_id']
        editorial = V.P / 'papers' / rid / 'reviews/editorial'
        publication = json.loads(cached(editorial / 'publication.json'))
        prefix = 'research/' + publication['slug'] + '/'
        main = cached(editorial / 'PUBLIC_MAIN.html')
        candidate = cached(editorial / 'candidate/index.html')
        V.need(candidate.count(main) == 1 and b'noindex,nofollow,noarchive' in candidate
               and b'<link rel="canonical"' not in candidate, 'source preview stays private with entire exact approved MAIN')
        output[prefix + 'index.html'] = candidate
        output[prefix + 'citation.bib'] = cached(editorial / 'citation.bib')
        for asset in publication['native_assets_in_original_order']:
            name = asset['original_api_file_object']['key']
            V.need('/' not in name and '\\' not in name, 'native article-root filename')
            output[prefix + name] = cached(Path(asset['path']))
    V.need(len(output) == 8, 'exact source-only eight private article-root leaves')
    return output


def main():
    V.need(sys.argv[1:] in [['source', 'normal'], ['source', 'optimized']],
           'only explicit source-only private mode until actual baseline GO')
    mode = sys.argv[2]
    destination = O / ('source-only-a' if mode == 'normal' else 'source-only-b') / 'public'
    output = source_leaves()
    V.need(not destination.parent.exists(), 'fresh owned preview namespace only')
    for name, body in output.items():
        path = destination / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(body)
    print(json.dumps({'status': 'PARTIAL_PRIVATE_SOURCE_LEAVES_ONLY', 'mode': mode,
                      'optimization_level': sys.flags.optimize, 'files':
                      [{'path': n, 'bytes': len(b), 'SHA256': hashlib.sha256(b).hexdigest()} for n, b in sorted(output.items())],
                      'aggregate_baseline_observed_or_changed': False, 'ready_to_publish': False,
                      'production_authority': False, 'canonical_url': None, 'AA': None}, indent=2))

if __name__ == '__main__':
    main()
