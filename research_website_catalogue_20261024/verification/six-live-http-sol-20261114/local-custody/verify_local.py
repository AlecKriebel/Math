#!/usr/bin/env python3
"""Local read-only hashes/namespace only. No network or old code execution."""
from pathlib import Path
import hashlib
import json

OWN = Path(__file__).resolve().parent


def data(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(path, row):
    if not path.is_file() or path.is_symlink() or path.stat().st_size != row['bytes'] or sha(path) != row['sha256']:
        raise RuntimeError('Local custody mismatch: '+str(path))


bindings = data(OWN/'INPUT_BINDINGS.json')
for row in bindings['inputs']:
    original, copy = Path(row['original_path']), OWN/row['copy']
    check(original, row);check(copy, row)
    if original.read_bytes() != copy.read_bytes():
        raise RuntimeError('Original object copy mismatch')
expected = data(OWN/'EXPECTED_LOCAL.json')
public, stage = Path(expected['public_root']), Path(expected['approved_overlay_root'])
baseline, install, adoption = [data(OWN/('original-'+name)) for name in ['FRESH_BASELINE.json','PUBLIC_INSTALL.json','ROOT_ADOPTION.json']]
if install['installed_public_files'] != adoption['exact26_public_payloads']:
    raise RuntimeError('Root approved26/install26 list mismatch')
for row in expected['unchanged_old_public_files']:
    check(public/row['path'], row)
for row in expected['unchanged_core_files']:
    check(Path(row['path']), row)
for row in expected['approved_installed26']:
    check(public/row['path'], row)
    check(stage/row['path'], row)
for row in expected['HTTP_extra_original_bindings']:
    check(public/row['path'], row)
names = {row['path'] for row in expected['unchanged_old_public_files']} | {row['path'] for row in expected['approved_installed26']}
actual = {str(f.relative_to(public)) for f in public.rglob('*') if f.is_file()}
if actual != names or len(actual) != 556:
    raise RuntimeError('Installed full public namespace differs from530+26')
excluded = {'OWNED_MANIFEST.json','FINAL_SEAL.json','RESULT.json'}
if (OWN/'OWNED_MANIFEST.json').exists():
    manifest = data(OWN/'OWNED_MANIFEST.json')
    actual_owned = {str(f.relative_to(OWN)) for f in OWN.rglob('*') if f.is_file() and str(f.relative_to(OWN)) not in excluded}
    if actual_owned != {x['relative_path'] for x in manifest['files']}:
        raise RuntimeError('Owned custody inventory mismatch')
    for row in manifest['files']:
        check(OWN/row['relative_path'], row)
if (OWN/'FINAL_SEAL.json').exists():
    seal = data(OWN/'FINAL_SEAL.json')
    for key,name in [('owned_manifest_sha256','OWNED_MANIFEST.json'),('input_bindings_sha256','INPUT_BINDINGS.json'),('expected_local_sha256','EXPECTED_LOCAL.json'),('report_sha256','REPORT.md'),('result_sha256','RESULT.json')]:
        if seal[key] != sha(OWN/name):
            raise RuntimeError('Final local-custody seal mismatch')
print(json.dumps({'status':'PASS_LOCAL_READ_ONLY_PREDEPLOY_OR_POSTDEPLOY_CUSTODY',
                  'public_root':str(public),'approved_overlay_root':str(stage),
                  'old_nonoverlay_public_files_unchanged':len(expected['unchanged_old_public_files']),
                  'installed_core_files_unchanged':len(expected['unchanged_core_files']),
                  'installed26_match_both_approved_hashes_and_overlay':len(expected['approved_installed26']),
                  'public_namespace_files':len(actual),
                  'original_HTTP_extra_bindings':expected['HTTP_extra_original_bindings'],
                  'network_HTTP_browser_or_Git':False,'writes':False,'old_code_or_campaign_executed':False},indent=2))
