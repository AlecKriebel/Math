"""Six new compatibility-boundary faults, in memory only; stdout only."""
from pathlib import Path
import copy
import json
import re
import sys
import presentation_supplement as supplement


def run(root, candidate):
    first = supplement.first; contract = first.load_contract(root)
    records = contract['records']; baseline = json.loads((root / 'INDEPENDENT_BASELINE.json').read_bytes())
    site = Path(baseline['public_root']); paths = {Path(r['path']).relative_to(site).as_posix() for r in baseline['public_files']}
    for r in records:
        p = r['whole_original_publication']; pre = 'research/' + p['slug'] + '/'
        paths |= {pre + 'index.html', pre + 'assets/' + p['pdf_filename'], pre + 'assets/' + p['supplement_filename'], pre + 'assets/citation.bib'}
    result = []
    def reject(label, action):
        try: action()
        except ValueError as exc: result.append({'fault': label, 'literal_rejection': str(exc)})
        else: raise ValueError('accepted compatibility fault: ' + label)
    for i, change, label in [(0, 'abstract', 'ScholarlyArticle_full_abstract_shortened'),
                              (1, 'encoding', 'native_ZIP_PDF_encoding_order_reversed'),
                              (0, 'datePublished', 'WebPage_build_date_substituted_for_article_date')]:
        r = records[i]; p = r['whole_original_publication']; raw = (candidate / 'research' / p['slug'] / 'index.html').read_text()
        match = re.search(r'<script type="application/ld\+json">([\s\S]*?)</script>', raw); value = json.loads(match.group(1)); old = copy.deepcopy(value)
        if change == 'abstract': value['@graph'][1]['abstract'] = value['@graph'][1]['abstract'][:60]
        elif change == 'encoding': value['@graph'][1]['encoding'].reverse()
        else: value['@graph'][1]['datePublished'] = supplement.BUILD_DATE
        first.need(value != old, 'nonvacuous graph fault')
        bad = (raw[:match.start(1)] + json.dumps(value, ensure_ascii=False) + raw[match.end(1):]).encode()
        reject(label, lambda r=r,bad=bad: supplement.page(root, r, bad, paths, baseline))
    r = records[1]; p = r['whole_original_publication']; raw = (candidate / 'research' / p['slug'] / 'index.html').read_bytes()
    old = b'href="/research/research.css"'; first.need(raw.count(old) == 1, 'CSS unique fault anchor')
    bad = raw.replace(old, b'href="/research/unapproved.css"', 1)
    reject('unapproved_external_stylesheet', lambda: supplement.page(root, r, bad, paths, baseline))
    raw = (candidate / 'research/index.html').read_text(); match = re.search(r'<script type="application/ld\+json">([\s\S]*?)</script>', raw)
    obj = json.loads(match.group(1)); obj['mainEntity']['itemListElement'][0]['position'] = False
    bad = (raw[:match.start(1)] + json.dumps(obj, ensure_ascii=False) + raw[match.end(1):]).encode()
    reject('old_typed_ItemList_position_normalized_to_boolean', lambda: supplement.index(root, bad, records, baseline))
    raw = (candidate / 'research/sitemap.xml').read_bytes(); oldxml = first.ET.fromstring(first.read_blob(root, baseline['baseline_sitemap']))
    url = oldxml[0].find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text.encode(); first.need(url in raw, 'old sitemap fault nonvacuous')
    bad = raw.replace(url, url + b'wrong-old-entry/', 1)
    reject('old_sitemap_location_altered', lambda: supplement.sitemap(root, bad, records, baseline))
    return {'literal_custom_status': 'SIX_DISTINCT_EXACT_PRESENTATION_SUPPLEMENT_FAULTS_REJECTED',
            'cases': result, 'science_or_writer_controls_replayed': False, 'positive_files_or_originals_modified': False}


if __name__ == '__main__':
    if len(sys.argv) != 2: raise ValueError('supply sealed private candidate')
    print(json.dumps(run(Path(__file__).resolve().parent, Path(sys.argv[1])), indent=2))
