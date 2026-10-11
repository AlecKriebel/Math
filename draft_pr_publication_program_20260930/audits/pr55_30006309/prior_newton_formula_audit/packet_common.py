#!/usr/bin/python3
"""Own packet integrity only; never executes the mathematical/source controls."""
from pathlib import Path
from datetime import datetime
import hashlib, json, stat
ROOT = Path(__file__).resolve().parent
checks = 0
def need(value, message):
    global checks
    checks += 1
    if not value: raise AssertionError(message)
def load(path): return json.loads(Path(path).read_text())
def row(path):
    path = Path(path)
    need(not path.is_symlink() and stat.S_ISREG(path.stat().st_mode), 'Regular nonsymlink file')
    body = path.read_bytes()
    return {'path': str(path), 'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest(),
            'mode': format(path.stat().st_mode & 0o7777, '04o')}
def contained(path):
    path = Path(path)
    need(path.is_absolute() and (path == ROOT or ROOT in path.parents), 'Own absolute family path')
    for ancestor in [path] + [p for p in path.parents if p == ROOT or ROOT in p.parents]:
        need(not ancestor.is_symlink(), 'Nonsymlink owned ancestor')
    return path
def all_files(exclude=()):
    paths = []
    for path in ROOT.rglob('*'):
        need(not path.is_symlink(), 'No packet symlink')
        if path.is_file() and path.name not in exclude: paths.append(path)
    return sorted(paths)
def all_dirs(): return [ROOT] + sorted(p for p in ROOT.rglob('*') if p.is_dir())
def check_external():
    refs = load(ROOT/'EXTERNAL_REFERENCES.json')
    need(len(refs) == 6 and len({r['path'] for r in refs}) == 6, 'Six distinct actual external references')
    for ref in refs: need(row(ref['path']) == ref, 'Exact external whole body/mode')
    return refs
def check_capture(name, expected_child, expected_exit, successful_checks=None, current=False):
    folder = ROOT/'captures'/name
    cap = load(folder/'CAPTURE.json')
    need(cap['schema'] == 'actual-independent-subprocess-v1', 'Actual capture schema')
    need(cap['child_pid'] == expected_child and cap['child_pid'] != cap['operator_pid'], 'Actual operator/child')
    need(cap['exit_code'] == expected_exit and cap['source_after_unchanged'] is True, 'Literal actual exit and epoch stability')
    need(cap['acceptance_authority'] is False, 'Capture cannot accept science')
    need(cap['argv'] == ['/usr/bin/python3','-B',str(ROOT/'priority_controls.py')] and cap['cwd'] == str(ROOT), 'Actual argv/cwd')
    need(datetime.fromisoformat(cap['started_at_utc']) <= datetime.fromisoformat(cap['ended_at_utc']), 'Actual UTC chronology')
    op = (folder/'operator_prelaunch.py').read_bytes()
    need(hashlib.sha256(op).hexdigest() == cap['operator_sha256'], 'Prelaunch operator body')
    need(op == (ROOT/'capture_command.py').read_bytes(), 'Operator preserved')
    need(len(cap['source_prelaunch']) == 2, 'Separate code and input captures')
    for captured, filename in zip(cap['source_prelaunch'], ['priority_controls.py','priority_input.json']):
        need(captured['path'] == str(ROOT/filename), 'Literal original source path')
        body = contained(captured['prelaunch_copy']).read_bytes()
        need(len(body) == captured['size'] and hashlib.sha256(body).hexdigest() == captured['sha256'], 'Whole historical source copy')
        need(captured['mode'] == '0644', 'Actual historical source mode')
        if current: need(body == (ROOT/filename).read_bytes(), 'Final source matches current source body')
    for key in ['stdout','stderr']:
        stream = folder/(key+'.bin'); body = stream.read_bytes(); ref = cap[key]
        need(ref['path'] == str(stream) and ref['size'] == len(body)
             and ref['sha256'] == hashlib.sha256(body).hexdigest(), 'Whole actual stdout/stderr')
    if expected_exit == 0:
        need(cap['stderr']['size'] == 0, 'Successful stderr empty')
        output = load(folder/'stdout.bin')
        need(output['all_checks_passed'] and output['check_count'] == successful_checks, 'Literal success count')
        need(output['univariate_labels'] == 62 and output['cube_generic_projection_equal']
             and output['cube_nongeneric_discriminant'] == '0', 'Literal finite boundary controls')
    else:
        need(cap['stdout']['size'] == 0 and b'AssertionError:' in (folder/'stderr.bin').read_bytes(), 'Failed guard retained in full')
    return cap
def check_science():
    verdict = load(ROOT/'VERDICT.json')
    need(verdict['recommended_user_status'] == 'already_solved' and verdict['paper_recommended'] is False, 'Priority recommendation')
    need(verdict['root_read_claim'] is False and verdict['closure_claim'] is False
         and verdict['ROOT_acceptance_authority'] is False, 'No ROOT or acceptance claim')
    result = load(ROOT/'CONTROL_RESULTS.json')
    need(len(result['checks']) == 139 and all(r['pass'] for r in result['checks']), '139 bounded controls pass')
    need(result['universal_proof'] is False and result['ROOT_acceptance_authority'] is False, 'Finite evidence limits')
    need(result['sources'][0]['sha256'] == '95f028d12b52dedeab8ab43f2b58e814a48287b8c6d627c70b1e25a65bfb0442'
         and result['sources'][0]['bytes'] == 713083 and result['sources'][0]['physical_pages'] == 59, 'Actual primary body pin')
    check_capture('source_and_column_controls',35739,1)
    check_capture('source_and_column_controls_corrected',35989,0,134)
    check_capture('source_identification_completed',42293,1)
    cap = check_capture('source_identification_final',43779,0,139,current=True)
    need(datetime.fromisoformat(cap['started_at_utc']) < datetime.fromisoformat(result['completed_at_utc'])
         < datetime.fromisoformat(cap['ended_at_utc']), 'Final result actual epoch')
    return check_external()
def check_prepared():
    index = load(ROOT/'INDEX.json'); ready = load(ROOT/'READY.json')
    need(ready['ROOT_closure_executed'] is False and ready['ROOT_personal_read_claimed'] is False, 'Only prepared')
    need(ready['index_sha256'] == hashlib.sha256((ROOT/'INDEX.json').read_bytes()).hexdigest(), 'Whole index pin')
    paths = []
    for ref in index['files']:
        path = contained(ref['path']); need(row(path) == ref, 'Prepared whole owned body/mode'); paths.append(path)
    need(set(paths) == set(all_files(('INDEX.json','READY.json','SELF_MANIFEST.json'))), 'Exact prepared topology')
    need(len(paths) <= 58 and sum(ref['bytes'] for ref in index['files']) < 1000000, 'Compact bounds')
    dirs = [{'path':str(p),'mode':format(p.stat().st_mode&0o7777,'04o')} for p in all_dirs()]
    need(dirs == index['directories'] and all(r['mode'] == '0755' for r in dirs), 'Directory topology/modes')
    need(index['external_references'] == check_science(), 'Pinned external dependencies')
    return index, ready
def check_closed():
    manifest = load(ROOT/'SELF_MANIFEST.json')
    need(manifest['acceptance_authority'] is False and manifest['ROOT_personal_read_not_inferred_from_integrity'] is True, 'Qualified closure')
    paths = []
    for ref in manifest['files']:
        path = contained(ref['path']); need(row(path) == ref and ref['mode'] == '0444', 'Closed owned body/mode'); paths.append(path)
    need(set(paths) == set(all_files(('SELF_MANIFEST.json',))), 'Exact closed topology')
    need(format((ROOT/'SELF_MANIFEST.json').stat().st_mode&0o7777,'04o') == '0444', 'Manifest mode')
    dirs = [{'path':str(p),'mode':format(p.stat().st_mode&0o7777,'04o')} for p in all_dirs()]
    need(dirs == manifest['directories'], 'Closed directory topology')
    need(manifest['external_references'] == check_science(), 'Closed external dependencies')
    return manifest
