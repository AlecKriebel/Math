"""Input-ledger collection only. No builder, source program, W or network access."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import stat
from urllib.parse import urlsplit

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OWN = P / 'verification/wreath-dyadic-stress-stage-sol-20261116'
CONFIG = [
    dict(record=23203143, row=164, stem='wreath-planar', slug='wreath-products-planar-triangle-bounds',
         writer_manifest='MANIFEST.json', fact_manifest='OWNED_MANIFEST.json', writer_extent=(23, 2), fact_extent=(20, 0),
         article='article.html', head='head.html', main='public-main.html', model='page-model.json',
         native=[('assets/preprint.pdf', 'preprint.pdf'), ('assets/wreath-planar-verification-v1.0.0-revised.zip', 'wreath-planar-verification-v1.0.0-revised.zip')],
         native_objects='writer', fact_final=None,
         writer_final='cdb1d0e19286e1ca5b8d9e54ae027238bf022018019e43588867c1a054814451'),
    dict(record=23205181, row=177, stem='dyadic-random-cone', slug='sharp-dyadic-threshold-random-cone',
         writer_manifest='OWNED_MANIFEST.json', fact_manifest='MANIFEST.json', writer_extent=(23, 3), fact_extent=(32, 1),
         article='candidate/research/sharp-dyadic-threshold-random-cone/index.html', head='HEAD.html', main='MAIN.html', model='MODEL.json',
         native=[('candidate/research/sharp-dyadic-threshold-random-cone/paper.pdf', 'paper.pdf'), ('candidate/research/sharp-dyadic-threshold-random-cone/source-and-audit.zip', 'source-and-audit.zip')],
         native_objects='fact', fact_final='8777b38698749745638ff49f47ec38a6698c25463dbadfc7ab3e0d908f2db529',
         writer_final='bd15c4b344ac07c909b3d7172477e930c359a52b08d45856bad88e86e5c8561c'),
    dict(record=23331540, row=183, stem='full-stress-labelled-graph', slug='full-stress-stratifications-labelled-graph',
         writer_manifest='MANIFEST.json', fact_manifest='OWNED_MANIFEST.json', writer_extent=(22, 2), fact_extent=(17, 0),
         article='article.html', head='head.html', main='public-main.html', model='page-model.json',
         native=[('assets/full_stress_stratifications_determine_a_labelled_graph.pdf', 'full_stress_stratifications_determine_a_labelled_graph.pdf'), ('assets/full_stress_stratifications_source_verification_v1.zip', 'full_stress_stratifications_source_verification_v1.zip')],
         native_objects='writer', fact_final='b4b6214861e5b1bbb1f37a6c287ad4a9e5d7771776a9388478a5130521e6e64b',
         writer_final='f588e3eeeb3767df2b456eea3bd5857e78ff0c8dda553beb165352e2ce77b554'),
]

def require(test, message):
    if not test:
        raise ValueError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def pin(path):
    info = path.lstat()
    require(stat.S_ISREG(info.st_mode), 'not regular: ' + str(path))
    data = path.read_bytes()
    return dict(bytes=len(data), mode=format(stat.S_IMODE(info.st_mode), '04o'), SHA256=digest(data))

def snapshot(root):
    require(root.is_dir() and not root.is_symlink(), 'bad root: ' + str(root))
    files, dirs = [], []
    for path in sorted(root.rglob('*')):
        info = path.lstat()
        rel = path.relative_to(root).as_posix()
        if stat.S_ISDIR(info.st_mode):
            dirs.append(dict(path=rel, mode=format(stat.S_IMODE(info.st_mode), '04o')))
        else:
            files.append(dict(path=rel, **pin(path)))
    return dict(root=str(root), root_mode=format(stat.S_IMODE(root.stat().st_mode), '04o'), files=files, directories=dirs,
                regular_files=len(files), child_directories=len(dirs), ignored_empty_and_terminal_controls_included=True)

def parsed_mode(mode):
    return mode if type(mode) is int else int(mode, 8)

def check_manifest(root, filename, snap, producer_kind):
    obj = json.loads((root / filename).read_text())
    rows = obj['payload_files'] if producer_kind == 'writer-manifest-v1' else obj['files']
    actual = {row['path']: row for row in snap['files']}
    controls = {'FINAL.json', filename}
    seen = set()
    for row in rows:
        rel = row['path']
        require(rel not in seen, 'duplicate manifest row: ' + rel)
        seen.add(rel)
        require(rel in actual, 'manifest path absent: ' + rel)
        require(int(actual[rel]['mode'], 8) == parsed_mode(row['mode']), 'file mode: ' + rel)
        if row.get('terminal_control') is True:
            require(rel in controls and 'SHA256' not in row and 'bytes' not in row, 'unexpected terminal row')
        else:
            require(actual[rel]['SHA256'] == row['SHA256'] and actual[rel]['bytes'] == row['bytes'], 'file pin: ' + rel)
    require(set(actual) == seen | controls, 'manifest finite file extent mismatch: ' + str(root))
    expected_dirs = {row['path']: parsed_mode(row['mode']) for row in obj['directories'] if row['path'] != '.'}
    require(expected_dirs == {row['path']: int(row['mode'], 8) for row in snap['directories']}, 'directory topology mismatch')
    require(parsed_mode(obj['root_mode']) == int(snap['root_mode'], 8), 'root mode mismatch')
    return dict(path=str(root / filename), **pin(root / filename), validated_payload_rows=len(rows), exact_terminal_controls=sorted(controls))

def collect():
    records = []
    for cfg in CONFIG:
        writer = P / ('verification/' + cfg['stem'] + '-editorial-sol-20261116')
        fact = P / ('verification/' + cfg['stem'] + '-fact-sol-20261116')
        ws, fs = snapshot(writer), snapshot(fact)
        require((ws['regular_files'], ws['child_directories']) == cfg['writer_extent'], 'writer extent')
        require((fs['regular_files'], fs['child_directories']) == cfg['fact_extent'], 'fact extent')
        require(pin(writer / 'FINAL.json')['SHA256'] == cfg['writer_final'], 'writer FINAL handoff pin')
        if cfg['fact_final'] is not None:
            require(pin(fact / 'FINAL.json')['SHA256'] == cfg['fact_final'], 'fact FINAL handoff pin')
        wkind = 'writer-manifest-v1' if cfg['record'] != 23205181 else 'files'
        wm = check_manifest(writer, cfg['writer_manifest'], ws, wkind)
        fm = check_manifest(fact, cfg['fact_manifest'], fs, 'files')
        fact_final = json.loads((fact / 'FINAL.json').read_text())
        if cfg['record'] == 23203143:
            receipt = json.loads((fact / 'CHECK_RECEIPT.json').read_text())
            bindings = [row for row in receipt['producer_files'] if row['path'] == 'FINAL.json']
            require(len(bindings) == 1 and bindings[0]['SHA256'] == cfg['writer_final'], 'wreath fact receipt binding')
        elif cfg['record'] == 23205181:
            require(fact_final['writer_FINAL']['SHA256'] == cfg['writer_final'], 'dyadic fact FINAL binding')
        else:
            require(fact_final['reviewed_writer']['root'] == str(writer) and fact_final['reviewed_writer']['FINAL']['SHA256'] == cfg['writer_final'], 'stress fact FINAL binding')
        article = (writer / cfg['article']).read_bytes()
        head = (writer / cfg['head']).read_bytes()
        main = (writer / cfg['main']).read_bytes()
        require(article.count(head.rstrip(b'\n')) == 1, 'HEAD not unique exact article span')
        require(article.count(main.rstrip(b'\n')) == 1, 'MAIN not unique exact article span')
        require(len(re.findall(br'<main\b', article)) == 1 and len(re.findall(br'</main>', article)) == 1, 'MAIN count')
        urls = re.findall(r'(?:href|src)="([^"]+)"', main.decode())
        local_urls = [u for u in urls if not urlsplit(u).scheme and not u.startswith(('/', '#'))]
        local_paths = sorted({urlsplit(u).path for u in local_urls})
        objects = writer if cfg['native_objects'] == 'writer' else fact
        native_file_obj = json.loads((objects / 'original-objects/files.json').read_text())
        require([entry['key'] for entry in native_file_obj['entries']] == [name for _, name in cfg['native']], 'native ordered keys')
        native_pins, targets = [], []
        article_target = 'public/research/' + cfg['slug'] + '/index.html'
        targets.append(dict(target=article_target, input=str(writer / cfg['article']), treatment='HEAD-only production wrapper activation; entire body and MAIN immutable'))
        for (rel, name), entry in zip(cfg['native'], native_file_obj['entries']):
            src = P / 'papers' / str(cfg['record']) / 'sources/assets' / name
            data, original = (writer / rel).read_bytes(), src.read_bytes()
            require(data == original, 'native whole-byte mismatch: ' + name)
            require(len(data) == entry['size'] and 'md5:' + hashlib.md5(data).hexdigest() == entry['checksum'], 'native size/MD5 mismatch')
            href = ('assets/' if rel.startswith('assets/') else '') + name
            require(href in local_paths, 'actual MAIN does not link native file: ' + href)
            target = 'public/research/' + cfg['slug'] + '/' + href
            native_pins.append(dict(writer_path=str(writer / rel), source_path=str(src), source_pin=pin(src), writer_pin=pin(writer / rel), MD5=hashlib.md5(data).hexdigest(), original_key=name, actual_MAIN_relative_path=href, target=target))
            targets.append(dict(target=target, input=str(writer / rel), treatment='unchanged entire native bytes'))
        require('citation.bib' in local_paths, 'MAIN Bib link absent')
        targets.append(dict(target='public/research/' + cfg['slug'] + '/citation.bib', input=str(writer / 'citation.bib'), treatment='unchanged entire Bib bytes'))
        require(local_paths == sorted([n['actual_MAIN_relative_path'] for n in native_pins] + ['citation.bib']), 'unexpected body-local payload')
        if cfg['record'] == 23205181:
            require((writer / 'citation.bib').read_bytes() == (writer / 'candidate/research/sharp-dyadic-threshold-random-cone/citation.bib').read_bytes(), 'dyadic Bib duplicate mismatch')
        selected = {key: dict(path=str(writer / cfg[key]), **pin(writer / cfg[key])) for key in ('article', 'head', 'main', 'model')}
        selected['Bib'] = dict(path=str(writer / 'citation.bib'), **pin(writer / 'citation.bib'))
        records.append(dict(record=cfg['record'], row=cfg['row'], proposed_slug=cfg['slug'], writer_snapshot=ws, fact_snapshot=fs,
                            writer_manifest=wm, fact_manifest=fm, selected_inputs=selected, native_assets_ordered=native_pins,
                            actual_body_local_urls=local_urls, candidate_target_map=targets, exact_head_and_main_unique_article_spans=True,
                            model_and_native_metadata_not_rewritten=True))
    target_map = [t for record in records for t in record['candidate_target_map']]
    require(len(target_map) == 12 and len({t['target'] for t in target_map}) == 12, 'addition target cardinality')
    target_dirs = sorted({str(Path(t['target']).parent) for t in target_map})
    require(len(target_dirs) == 5, 'actual nested directory cardinality')
    return dict(schema='private-stage-input-custody-v1', UTC=datetime.now(timezone.utc).isoformat(), status='PREP_INPUT_READY_BUILD_GATE_CLOSED',
                records=records, expected_additions=target_map, expected_new_article_directories=target_dirs,
                aggregate_modifications=['public/research/index.html', 'public/research/sitemap.xml'], expected_target_leaves=14,
                root_reported_W_baseline=dict(commit_prefix='b767', index_prefix='6e57', public_files=760, index_items=123, sitemap_nodes=124, DS_Store_files=17, independently_read_here=False),
                expected_successor_counts_if_baseline_confirmed=dict(public_files=772, index_items=126, sitemap_nodes=127),
                gates=dict(all_three_actual_adoptions_received_and_read=False, independent_stage_INITIAL_confirmation_received=False, builder_authoring_allowed=False, builder_execution_allowed=False, production_authority=False),
                execution_scope='One own input-custody collector; no producer/native/scientific/render/old helper, W, Git, Sheet or network action. All input namespaces are read-only.',
                opaque_scope='Whole native PDF/ZIP and unselected helper bytes were hashed for custody only. No archive extraction or source/helper execution; no new scientific certification.')

if __name__ == '__main__':
    result = collect()
    out = OWN / 'PREP_INPUT_LEDGER.json'
    with out.open('x') as handle:
        json.dump(result, handle, indent=2, ensure_ascii=False)
        handle.write('\n')
    print('PREP_INPUT_READY: 3 writers, 3 facts, 6 native assets; 12 additions/5 directories + 2 aggregate modifications. Build gate remains CLOSED.')
