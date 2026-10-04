from pathlib import Path
import json, stat
from closure_common import F, R, body_row, check_external, digest

original = R / 'draft_pr_publication_program_20260930/audits/pr53_30000671/original_preparation_family'
pin = 'd10783bb3d60becaa765d36a5cd5ff303c978049b9527266a2be4b2dc92f49b7'
assert digest((original / 'MANIFEST.json').read_bytes()) == pin
m = json.loads((original / 'MANIFEST.json').read_bytes())
assert len(m['files']) == 174 and m['root_approval'] is False
rows = [body_row(original / row['path'], R) for row in m['files']]
dirs = []
for d in m['directories']:
    p = original if d == '.' else original / d
    assert p.resolve() == p and p.is_dir()
    dirs.append({'path': p.relative_to(R).as_posix(),
                 'mode': format(stat.S_IMODE(p.lstat().st_mode), '04o')})
capture_paths = []
for name in ('root_pr53_original_preparation_closure_actual_capture',
             'root_pr53_original_preparation_closed_readback_actual_capture'):
    d = R / 'draft_pr_publication_program_20260930/audits/pr45_9900007' / name
    capture_paths.append((d / 'CAPTURE.json').relative_to(R).as_posix())
    for p in sorted(d.iterdir()):
        assert p.is_file() and not p.is_symlink()
        rows.append(body_row(p, R))
assert len({r['path'] for r in rows}) == len(rows) == 182
out = {'schema': 'pr53-independent-external-inputs/v1',
       'original_family_path': original.relative_to(R).as_posix(),
       'original_manifest_sha256': pin, 'rows': rows,
       'closed_original_directories': dirs,
       'root_complete_capture_paths': capture_paths,
       'original_semantic_files_personally_read': 11,
       'external_whole_body_reads_are_custody_not_all_semantic_proof_audit': True,
       'private_primary_pixels_referenced_in_place_not_copied': True,
       'large_raw_cache_personally_reaudited': False,
       'root_math_approval': False}
assert not (F / 'EXTERNAL_REFERENCES.json').exists()
(F / 'EXTERNAL_REFERENCES.json').write_text(json.dumps(out, indent=2) + '\n')
assert check_external() == 182
print(json.dumps({'status': 'INPUT_BINDINGS_AUTHORED', 'external_whole_body_rows': len(rows),
                  'original_manifest_sha256': pin, 'root_approval': False}, indent=2))
