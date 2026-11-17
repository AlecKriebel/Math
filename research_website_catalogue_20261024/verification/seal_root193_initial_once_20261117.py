"""Seal only original-source reader evidence, without scientific execution."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import stat

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
R = P / 'papers/23204810/reviews/root-initial-20261117'
S = P / 'papers/23204810/sources'
now = datetime.now(timezone.utc).isoformat()

def info(path):
    raw = path.read_bytes()
    s = path.lstat()
    assert stat.S_ISREG(s.st_mode)
    return {'bytes': len(raw), 'SHA256': hashlib.sha256(raw).hexdigest(),
            'mode': format(stat.S_IMODE(s.st_mode), '04o'),
            'mtime_ns': s.st_mtime_ns, 'ctime_ns': s.st_ctime_ns}

def snapshot(root):
    files, dirs = {}, {}
    for folder, children, names in os.walk(root, followlinks=False):
        path = Path(folder)
        q = path.lstat()
        assert stat.S_ISDIR(q.st_mode)
        dirs[str(path.relative_to(root))] = {'mode': format(stat.S_IMODE(q.st_mode), '04o'),
            'mtime_ns': q.st_mtime_ns, 'ctime_ns': q.st_ctime_ns, 'empty': not children and not names}
        for name in names:
            file = path / name
            files[str(file.relative_to(root))] = info(file)
    return {'root': str(root), 'files': files, 'directories_including_root': dirs,
            'file_count': len(files), 'child_directory_count': len(dirs)-1}

def write_new(path, obj):
    with path.open('x') as stream:
        json.dump(obj, stream, indent=2)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())

assert {p.name for p in R.iterdir()} == {'INITIAL.json', 'RESEARCH_LOG.md'}
initial = json.loads((R / 'INITIAL.json').read_text())
assert initial['foreign_primary_and_peer_findings_body_reads'] == initial['scientific_executions'] == 0
assert initial['actual_original_pdf_page_images_personally_viewed'] == 5
assert len(initial['original_only_deductions']) == 11
source_before = snapshot(S)
assert (source_before['file_count'], source_before['child_directory_count']) == (61,13)
assert info(S/'SOURCE_FINAL.json')['SHA256'] == '4d62403dbe129bb77393b73492dc92ae8504d5081e84d311cb7905c7323638df'
assert info(S/'SOURCE_MANIFEST.json')['SHA256'] == '045d57f33015c343ca7441d602d37425a746d93954e88e812782abfda2612820'
paper = S / 'zenodo-files/paper.pdf'
assert info(paper)['SHA256'] == 'ae0526dfe7442b63e9c3f4754c324970b0d4e8ccd15d85b6f9585ed3ee45a119'
tex = S / 'archives/03-source.zip.extracted/manuscript/main.tex'
assert info(tex)['bytes'] == 15258 and len(tex.read_text().splitlines()) == 323
assert info(S/'native-metadata/record-api.json')['bytes'] == 6263
mechanical = [P / initial['mechanically_derived_source_artifacts_only']['text']]
mechanical += [P/name for name in initial['mechanically_derived_source_artifacts_only']['rasters']]
mechanical_pins = {str(path.relative_to(P)): info(path) for path in mechanical}
assert all('/adversarial-sol/' in str(path) for path in mechanical)
write_new(R / 'INPUTS.json', {'UTC': now, 'native_source': source_before,
    'original_PDF_mechanical_reader_inputs_only': mechanical_pins,
    'peer_reviews_findings_or_scientific_programs_not_opened': True,
    'root_new_PDF_render_or_scientific_execution': 0})
assert snapshot(S) == source_before
assert {str(path.relative_to(P)): info(path) for path in mechanical} == mechanical_pins
payload = {name: info(R/name) for name in ('INITIAL.json','RESEARCH_LOG.md','INPUTS.json')}
write_new(R / 'INITIAL_SEAL.json', {'UTC': now,
    'status': 'ORIGINAL_ONLY_ROOT_INITIAL_SEALED_LOGICALLY_IMMUTABLE',
    'record_id': 23204810, 'files': 4, 'child_directories': 0,
    'payload': payload, 'exact_terminal_recursive_hash_exclusion': 'INITIAL_SEAL.json',
    'native_source_files_childdirs': [61,13], 'all_source_bytes_modes_times_topology_unchanged': True,
    'original_PDF_mechanical_text_images_reused_no_review_findings_read': True,
    'source_first_INITIAL_percent': 100, 'full_review_percent': 35,
    'scientific_verdict': None, 'scientific_executions': 0,
    'foreign_support_primary_peer_bodies_read': 0,
    'future_scientific_work_requires_distinct_continuation_folder': True,
    'publication_authority': False, 'programme_complete': False})
assert len(list(R.iterdir())) == 4
print(json.dumps({'status': 'SOURCE_FIRST_ROOT_INITIAL_SEALED', 'files':4,
                  'seal':info(R/'INITIAL_SEAL.json'), 'full_review_percent':35,
                  'scientific_verdict':None, 'scientific_executions':0}))
