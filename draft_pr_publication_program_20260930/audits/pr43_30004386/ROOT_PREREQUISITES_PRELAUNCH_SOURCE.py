"""ROOT's completed scientific reading and exact current administrative inputs.

ROOT already read proofs and sources personally; these mechanical checks bind
that genuine judgment to the unchanged closures. No scientific helper is run.
"""
from pathlib import Path
import datetime as dt
import hashlib
import json
import math
import os
import stat
import subprocess
import sys

A = Path(__file__).resolve().parent
R = A.parents[2]
PREP = 'bbf269401514530da541500ee2f43e03cfd4514fab65c2a34193283e11b6fcc7'
ADV = '8ffa04e6410864c7095d8c7d20bd3f635c6a0c58daf64fc4b0715b55c9afb859'
SCOPE = '95a4d9b76267c33ea68aba9582d6493dd4c89baa77c3e820806b5e9482f0cf36'
HEAD = 'c61dc0cb572de281b871264819c8b80d647d0373'
records, git_records = [], []


def utc():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def load(raw):
    def pairs(items):
        out = {}
        for key, value in items:
            assert key not in out
            out[key] = value
        return out
    def bad(value):
        raise ValueError('Nonfinite JSON: ' + value)
    value = json.loads(raw, object_pairs_hook=pairs, parse_constant=bad)
    def visit(x):
        if type(x) is float: assert math.isfinite(x)
        elif type(x) is dict:
            for y in x.values(): visit(y)
        elif type(x) is list:
            for y in x: visit(y)
    visit(value)
    return value


def read(path, row=None):
    assert path.is_file() and not path.is_symlink()
    assert all(not p.is_symlink() for p in path.parents)
    raw = path.read_bytes()
    rec = {'path': path.relative_to(R).as_posix(), 'bytes': len(raw), 'sha256': sha(raw),
           'full_stat_S_IMODE': format(stat.S_IMODE(path.stat().st_mode), '05o')}
    if row:
        assert type(row['bytes']) is int and rec['bytes'] == row['bytes'] and rec['sha256'] == row['sha256'], str(path)
        if 'full_stat_S_IMODE' in row: assert rec['full_stat_S_IMODE'] == row['full_stat_S_IMODE']
    if path.name.endswith('.json'): load(raw)
    if path.name.endswith('.jsonl'):
        for line in raw.splitlines(): load(line)
    records.append(rec)
    return raw


def write(name, value):
    raw = (json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n').encode()
    with (A / name).open('xb') as f:
        f.write(raw); f.flush(); os.fsync(f.fileno())
    return sha(raw)


def git(*args):
    assert args in [('branch','--show-current'), ('rev-parse','HEAD')]
    rec = {'argv': ['git', *args], 'cwd': str(R), 'started_utc': utc()}
    p = subprocess.Popen(rec['argv'], cwd=R, stdin=subprocess.DEVNULL,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         env=dict(os.environ, GIT_OPTIONAL_LOCKS='0'))
    out, err = p.communicate()
    rec.update(pid=p.pid, actual_execution=True, completed=True, exit_code=p.returncode,
               stdout=out.decode(), stderr=err.decode(), finished_utc=utc())
    git_records.append(rec)
    assert p.returncode == 0 and not err
    return out.decode().strip()


def main():
    assert __debug__ and os.environ.get('PYTHONOPTIMIZE','') in ('','0')
    source = Path(__file__).read_bytes()
    with (A / 'ROOT_PREREQUISITES_PRELAUNCH_SOURCE.py').open('xb') as f: f.write(source)
    started = utc()
    assert git('branch','--show-current') == 'main' and git('rev-parse','HEAD') == HEAD
    assert not (A / 'reviewed_candidate').exists()
    assert sha(read(A / 'ROOT_CURRENT_PARTIAL_SCOPE_CERTIFICATE.md')) == SCOPE
    assert sha(read(A / 'current_preparation_family/PREPARATION_MANIFEST.json')) == PREP
    adv_root = A / 'current_source_adversary_family'
    raw = read(adv_root / 'SELF_MANIFEST.json'); assert sha(raw) == ADV
    mf = load(raw)
    assert mf['files_count'] == len(mf['files']) == 20 and mf['self_excluded'] == ['SELF_MANIFEST.json']
    paths = {p.relative_to(adv_root).as_posix() for p in adv_root.rglob('*') if p.is_file()}
    assert paths == {row['path'] for row in mf['files']} | {'SELF_MANIFEST.json'}
    dirs = {p.relative_to(adv_root).as_posix() for p in adv_root.rglob('*') if p.is_dir()}
    assert dirs == {row['path'] for row in mf['directories']}
    for row in mf['files']: read(adv_root / row['path'], row)
    assert stat.S_IMODE((adv_root / 'SELF_MANIFEST.json').stat().st_mode) == 0o444
    inputs = load(read(adv_root / 'STATIC_INPUT_MANIFEST.json'))
    assert len(inputs['static_input_files']) == 280 and len(inputs['exact_closed_trees']) == 13
    for row in inputs['static_input_files']: read(R / row['path'], row)
    for tree in inputs['exact_closed_trees']:
        root = R / tree['root']
        assert root.is_dir() and not root.is_symlink()
        assert format(stat.S_IMODE(root.stat().st_mode),'05o') == tree['root_full_stat_S_IMODE']
        files, directories = {}, {}
        for p in root.rglob('*'):
            assert not p.is_symlink()
            rel = p.relative_to(root).as_posix()
            mode = format(stat.S_IMODE(p.stat().st_mode),'05o')
            if p.is_file(): files[rel] = mode
            else:
                assert p.is_dir()
                directories[rel] = mode
        assert files == {row['path']:row['full_stat_S_IMODE'] for row in tree['files']}
        assert directories == {row['path']:row['full_stat_S_IMODE'] for row in tree['directories']}
    pins = load(read(A / 'current_preparation_family/INPUT_PINS.json'))
    created = utc()
    fresh = {'schema':'PR43_ROOT_FRESH13_INPUT_PREIMAGES_v1', 'approved_by_root':True,
        'reason':'ROOT read and pins all whole current native inputs after verified PR41 acceptance and the c61 published checkpoint; the source adversary dated observations are checked but supply no approval.',
        'created_utc':created, 'current_head':HEAD, 'files':[]}
    native = inputs['native13_observation']['files']
    assert len(native) == 13
    for row in native:
        read(R / row['path'], row)
        fresh['files'].append({k:row[k] for k in ['path','bytes','sha256']})
    fresh_hash = write('ROOT_CURRENT_INPUT_PREIMAGES.json', fresh)
    draft = load(read(A / 'current_preparation_family/DRAFT_ROOT_READ_LEDGER.json'))
    common = {k:v for k,v in draft.items() if k not in ['schema','instruction']}
    common.update(created_utc=created, reading_completed=True,
        root_flags={k:True for k in draft['root_flags']}, scope_certificate_sha256=SCOPE,
        preparation_manifest_sha256=PREP,
        reading_notes='ROOT personally read full original16 and full957-line diff, full JKP v2 and operative OWR target, both independently closed proof families, genuine current527/historical527/old-independent664 source and full typed receipts, whole raw/allSQL provenance, and all source preparation contracts and new source adversary. The separately authored certificate supplies precise scientific and historical limits.')
    reading = dict(common, schema='PR43_ROOT_PRIMARY_READ_LEDGER_v1',
        independent_source_adversary_manifest_sha256=ADV,
        source_preparation_safety_review_completed=True, future_whole_current_approval=False)
    ledger_hash = write('ROOT_PRIMARY_READ_LEDGER.json',reading)
    science = dict(common, schema='PR43_ROOT_SCIENCE_CARD_v1', status='already_solved',
        partial_valid=True, full_target_resolved_in_prior_published_literature=True,
        full_problem_solved_by_project=False, novelty_claimed=False, turn_limit=5,
        prior_publication_doi='10.4064/sm210413-16-9', read_ledger_sha256=ledger_hash,
        current_input_manifest_sha256=fresh_hash, new_whole_current_gate='PENDING',
        current_model=None, current_reasoning_effort=None,current_deadline_utc=None,
        current_verdict=None,paper_created=False,new_DOI_created=False,tracker_row_created=False)
    science_hash = write('ROOT_SCIENCE_CARD.json',science)
    assert git('rev-parse','HEAD') == HEAD
    for row in fresh['files']: read(R / row['path'],row)
    result = {'status':'PASS_ROOT_GENUINE_CURRENT_PREREQUISITES', 'pid':os.getpid(),
        'parent_pid':os.getppid(), 'started_utc':started, 'finished_utc':utc(),
        'source_sha256':sha(source), 'scope_sha256':SCOPE,'preparation_manifest_sha256':PREP,
        'source_adversary_manifest_sha256':ADV,'read_ledger_sha256':ledger_hash,
        'science_card_sha256':science_hash,'current_input_manifest_sha256':fresh_hash,
        'complete_input_read_rows':records,'actual_readonly_git_queries':git_records,
        'new_whole_current_gate':'PENDING','scientific_helpers_executed':False,
        'native_mutations':False,'original_substantive_attempts':0,'new_substantive_attempts':0,'audit_turns':0}
    write('ROOT_CURRENT_PREREQUISITES_INSPECTION.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ['complete_input_read_rows','actual_readonly_git_queries']},indent=2))


if __name__ == '__main__':
    main()
