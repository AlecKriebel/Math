"""Small, explicit, new-target-only in-memory integration faults. Never run on import."""
from pathlib import Path
import argparse
import copy
import json
import platform
from stage_model import Frozen, load_records, validate_record, require, OLD_SENTENCE, NEW_SENTENCE
from check_private import read_tree, check_outputs


def run(output_root, build_date):
    frozen = Frozen(); records = load_records(frozen); positive = read_tree(output_root)
    check_outputs(positive, records, frozen, build_date)
    results = []

    def page_fault(name, rid, old, new):
        data = dict(positive); record = next(r for r in records if r['id'] == rid)
        path = 'research/' + record['pub']['slug'] + '/index.html'
        require(data[path].count(old.encode()) == 1, 'unique fault anchor: ' + name)
        data[path] = data[path].replace(old.encode(), new.encode(), 1)
        reject(name, lambda: check_outputs(data, records, frozen, build_date))

    def reject(name, action):
        try: action()
        except (ValueError, KeyError, TypeError, IndexError, json.JSONDecodeError) as e:
            results.append({'case': name, 'rejected': True, 'reason': str(e)})
        else: raise ValueError('UNREJECTED integration fault: ' + name)

    for rid in ('23439582', '23440389'):
        page_fault('template_outer_body_' + rid, rid, '<body>', '<template><body>')
        page_fault('noscript_outer_body_' + rid, rid, '<body>', '<noscript><body>')
        page_fault('hidden_article_' + rid, rid, '<article>', '<article hidden>')
        page_fault('article_in_iframe_rawtext_' + rid, rid, '<article>', '<iframe class="paper-pdf" loading="lazy" src="assets/x.pdf" title="inert"><article>')
        page_fault('nonempty_iframe_' + rid, rid, '</iframe>', '<p>hidden replacement</p></iframe>')
    page_fault('approved_sentence_missing', '23439582', NEW_SENTENCE, OLD_SENTENCE)
    # Literal underscore notation must remain actual text in the complete original main tree.
    p121 = 'research/' + records[0]['pub']['slug'] + '/index.html'
    require(b'C_*' in positive[p121], 'literal C_* anchor')
    changed = dict(positive); changed[p121] = changed[p121].replace(b'C_*', b'C<em></em>', 1)
    reject('literal_chain_notation_reinterpreted', lambda: check_outputs(changed, records, frozen, build_date))
    page_fault('build_date_substituted_for_original_citation', '23440389', 'content="2026/10/17"', 'content="' + build_date.replace('-', '/') + '"')
    p122 = 'research/' + records[1]['pub']['slug'] + '/index.html'
    changed = dict(positive); text = changed[p122].decode(); start = text.index('<script type="application/ld+json">') + len('<script type="application/ld+json">'); end = text.index('</script>', start)
    obj = json.loads(text[start:end]); obj['@graph'][1]['encoding'].reverse(); changed[p122] = (text[:start] + json.dumps(obj, ensure_ascii=False) + text[end:]).encode()
    reject('native_encoding_order_reversed', lambda: check_outputs(changed, records, frozen, build_date))
    for rid, extension in (('23439582', '.pdf'), ('23440389', '.zip')):
        r = next(r for r in records if r['id'] == rid); prefix = 'research/' + r['pub']['slug'] + '/assets/'
        path = prefix + r['pub']['pdf_filename' if extension == '.pdf' else 'supplement_filename']
        changed = dict(positive); changed[path] = changed[path][:-1]
        reject('native_asset_truncated_' + rid, lambda: check_outputs(changed, records, frozen, build_date))
    changed = dict(positive); changed['research/index.html'] = changed['research/index.html'].replace(b'Free spanning-forest degree can decrease under squaring', b'Altered old entry', 1)
    reject('old_index_entry_changed', lambda: check_outputs(changed, records, frozen, build_date))
    changed = dict(positive); changed['research/sitemap.xml'] = changed['research/sitemap.xml'].replace(b'https://aleckriebel.com/research/free-spanning-forest-degree/', b'https://aleckriebel.com/research/wrong-old-entry/', 1)
    reject('old_sitemap_entry_changed', lambda: check_outputs(changed, records, frozen, build_date))
    changed = copy.deepcopy(records[0]); changed['ready']['completion_percent'] = 100
    changed['pub']['source_binding']['whole_original_source_ready']['completion_percent'] = 100
    changed['promotion']['whole_original_source_ready']['completion_percent'] = 100
    reject('121_historical_READY95_normalized', lambda: validate_record(changed, frozen))
    changed = copy.deepcopy(records[0]); changed['pub']['source_binding']['native_ZIP_fresh_GET_claimed'] = True
    reject('121_cached_ZIP_fresh_GET_invented', lambda: validate_record(changed, frozen))
    changed = copy.deepcopy(records[1]); changed['verdicts'][0]['whole_literal_object'] = {'verdict': 'PASS'}
    reject('whole_custom_verdict_replaced_by_generic_PASS', lambda: validate_record(changed, frozen))
    changed = copy.deepcopy(records[1]); changed['pub']['code_license'] = 'MIT'
    reject('122_code_license_invented', lambda: validate_record(changed, frozen))
    require(read_tree(output_root) == positive, 'pristine positive tree never mutated')
    return {'status': 'PASS', 'python': platform.python_version(), 'optimized': not __debug__, 'positive_records': 2, 'fault_count': len(results), 'all_rejected': True,
        'pristine_positive_tree_unchanged': True, 'scope': 'Bounded integration controls only; no scientific or archived campaigns.', 'cases': results}


def main():
    ap = argparse.ArgumentParser(description=__doc__); ap.add_argument('--output-root', required=True); ap.add_argument('--build-date', required=True)
    args = ap.parse_args(); print(json.dumps(run(args.output_root, args.build_date), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
