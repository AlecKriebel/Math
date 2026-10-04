"""ROOT-only closure of an adverse SOURCE review. This file has not been run by the reviewer."""
import argparse
import datetime as dt
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import stat

F = Path(__file__).absolute().parent
R = F.parents[3]
NAME = 'SELF_MANIFEST.json'
PIN = '48ddcccb22eb898c42598278fa4914d84fa0da640e098973a1e70d7c60577662'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def parse(raw):
    def pairs(items):
        out = {}
        for k, v in items:
            need(k not in out, 'Duplicate JSON key')
            out[k] = v
        return out
    def finite(s):
        x = float(s)
        need(math.isfinite(x), 'Nonfinite JSON number')
        return x
    return json.loads(raw, object_pairs_hook=pairs, parse_float=finite,
                      parse_constant=lambda v: (_ for _ in ()).throw(ValueError(v)))


def relative(n):
    need(type(n) is str and n and '\\' not in n and '\x00' not in n, 'Literal path')
    p = PurePosixPath(n)
    need(not p.is_absolute() and p.as_posix() == n and n != '.'
         and not {'.', '..', '.git', '__pycache__'}.intersection(p.parts), 'Canonical path')
    return n


def raw(p):
    need(not p.is_symlink() and stat.S_ISREG(p.stat().st_mode)
         and all(not x.is_symlink() for x in p.parents), 'Regular nonsymlink member')
    return p.read_bytes()


def check_external():
    inputs = parse(raw(F / 'INPUT_BINDINGS.json'))
    need(set(inputs) == {'schema', 'unique_count', 'rows', 'groups', 'dated_native4_pinned_live',
                         'actual_PR47_post_certified', 'future_acceptance_approved'}, 'Exact input schema')
    need(inputs['schema'] == 'pr48-v2-fresh-source-adversary-fixed-inputs/v1'
         and type(inputs['unique_count']) is int and inputs['unique_count'] == 4371
         and type(inputs['rows']) is list and len(inputs['rows']) == 4371
         and inputs['dated_native4_pinned_live'] is False
         and inputs['actual_PR47_post_certified'] is False
         and inputs['future_acceptance_approved'] is False, 'Fixed inputs only')
    names = []
    for z in inputs['rows']:
        need(type(z) is dict and set(z) == {'path', 'bytes', 'sha256', 'full_mode'}, 'Four-key external binding')
        n = relative(z['path'])
        need(type(z['bytes']) is int and z['bytes'] >= 0 and type(z['full_mode']) is int
             and 0 <= z['full_mode'] <= 0o7777 and type(z['sha256']) is str
             and re.fullmatch('[0-9a-f]{64}', z['sha256']), 'Typed full external reference')
        b = raw(R / n)
        need(len(b) == z['bytes'] and sha(b) == z['sha256']
             and stat.S_IMODE((R / n).stat().st_mode) == z['full_mode'], 'Entire fixed external body/mode ' + n)
        names.append(n)
    need(names == sorted(set(names)), 'Sorted unique inputs')
    need(type(inputs['groups']) is dict and set().union(*(set(v) for v in inputs['groups'].values())) == set(names),
         'Exact complete group memberships')
    return inputs


def topology():
    files, dirs = {}, set()
    need(F.is_dir() and not F.is_symlink(), 'Owned review root')
    for p in F.rglob('*'):
        n = relative(p.relative_to(F).as_posix())
        need(not p.is_symlink() and (p.is_file() or p.is_dir()), 'No symlink or special topology')
        if p.is_file():
            files[n] = p
        else:
            dirs.add(n)
    expected = {x.as_posix() for n in files for x in PurePosixPath(n).parents if x.as_posix() != '.'}
    need(dirs == expected, 'Exact directories, no empty unbound directories')
    return files, dirs


def captures():
    expected = [('private_controls_actual_capture', 55631, 0), ('fixed_custody_actual_capture', 63872, 1),
                ('fixed_custody_v2_actual_capture', 64951, 1), ('fixed_custody_v3_actual_capture', 66194, 0)]
    for name, pid, exit_code in expected:
        folder = F / name
        need({p.name for p in folder.iterdir()} == {'CAPTURE.json', 'PRELAUNCH.json', 'PRELAUNCH_SOURCE.py',
                                                   'PRELAUNCH_OPERATOR.py', 'stdout.bin', 'stderr.bin'}, 'Whole CAP6')
        c = parse(raw(folder / 'CAPTURE.json'))
        pre = parse(raw(folder / 'PRELAUNCH.json'))
        need(c['schema'] == 'pr48-v2-fresh-source-adversary-private-capture/v1'
             and c['actual_execution'] is True and c['completed'] is True
             and type(c['pid']) is int and c['pid'] == pid and type(c['exit_code']) is int
             and c['exit_code'] == exit_code and c['stdin_supplied'] is False
             and c['source_unchanged'] is True and c['operator_unchanged'] is True
             and c['production_imported_compiled_executed'] is False, 'Genuine typed completed private capture')
        need(c['argv'] == pre['argv'] and c['cwd'] == pre['cwd'] == str(F)
             and c['argv'][:2] == ['/usr/bin/python3', '-B']
             and len(c['argv']) == 3 and Path(c['argv'][2]).parent == F, 'Literal own private argv')
        need(sha(raw(folder / 'PRELAUNCH_SOURCE.py')) == c['source_sha256'] == pre['source_sha256']
             and sha(raw(folder / 'PRELAUNCH_OPERATOR.py')) == c['operator_sha256'] == pre['operator_sha256'], 'Entire actual prelaunch sources')
        for ch in ['stdout', 'stderr']:
            z = c[ch]
            b = raw(folder / (ch + '.bin'))
            need(set(z) == {'path', 'bytes', 'sha256'} and z['path'] == ch + '.bin'
                 and type(z['bytes']) is int and len(b) == z['bytes'] and sha(b) == z['sha256'], 'Full captured stream')
        start, end = [dt.datetime.fromisoformat(c[k]) for k in ['started_utc', 'finished_utc']]
        need(start.tzinfo is not None and end.tzinfo is not None
             and start.utcoffset() == end.utcoffset() == dt.timedelta(0)
             and start <= end <= dt.datetime.now(dt.timezone.utc), 'Real aware UTC interval')
        need(c['status'] == ('PASS' if exit_code == 0 else 'FAIL'), 'Failures preserved honestly')
        need(raw(folder / 'stderr.bin') == b'' if exit_code == 0 else bool(raw(folder / 'stderr.bin')),
             'Whole stderr disposition')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--expected-report-sha256', required=True)
    a = p.parse_args()
    need(not (F / NAME).exists() and not (F / NAME).is_symlink(), 'Absent ROOT-only self')
    rb = raw(F / 'REPORT.md')
    need(sha(rb) == a.expected_report_sha256, 'ROOT supplied entire report pin')
    v = parse(raw(F / 'VERDICT.json'))
    need(v['schema'] == 'pr48-acceptance-source-adversary-verdict/v1'
         and v['verdict'] == 'NEEDS_SOURCE_CORRECTION_SCOPED'
         and v['preparation_manifest_sha256'] == PIN and v['report_sha256'] == sha(rb)
         and [x['id'] for x in v['mandatory_corrections']] == ['M2']
         and v['production_imported_compiled_executed'] is False
         and v['future_acceptance_approved'] is False, 'Entire adverse SOURCE disposition')
    check_external()
    captures()
    files, dirs = topology()
    need(NAME not in files, 'Literal self excluded')
    rr = [{'path': n, 'bytes': len(raw(q)), 'sha256': sha(raw(q))} for n, q in sorted(files.items())]
    for q in files.values():
        q.chmod(0o444)
    for z in rr:
        b = raw(F / z['path'])
        need(len(b) == z['bytes'] and sha(b) == z['sha256']
             and stat.S_IMODE((F / z['path']).stat().st_mode) == 0o444, 'Exact first-party full444')
    check_external()
    current_files, current_dirs = topology()
    need(set(current_files) == set(files) and current_dirs == dirs, 'Topology stable before publication')
    m = {'schema': 'pr48-v2-fresh-source-adversary-closure/v1', 'status': 'CLOSED_ADVERSE_SOURCE_REVIEW',
         'utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'actual_closing_pid': os.getpid(),
         'self_excluded': [NAME], 'files_count': len(rr), 'files': rr, 'directories': sorted(dirs),
         'production_imported_compiled_executed': False, 'future_acceptance_approved': False,
         'ROOT_approval_authored': False, 'mandatory_corrections': ['M2']}
    body = (json.dumps(m, sort_keys=True, indent=2) + '\n').encode()
    stage = F / '.SELF_MANIFEST.staging'
    with stage.open('xb') as stream:
        stream.write(body)
        stream.flush()
        os.fsync(stream.fileno())
    stage.chmod(0o444)
    os.link(stage, F / NAME, follow_symlinks=False)
    stage.unlink()
    fd = os.open(F, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)
    after, after_dirs = topology()
    need(set(after) == set(files) | {NAME} and after_dirs == dirs
         and stat.S_IMODE((F / NAME).stat().st_mode) == 0o444, 'Exact published self closure')
    print(json.dumps({'status': 'CLOSED_ADVERSE_SOURCE_REVIEW', 'actual_closing_pid': os.getpid(),
                      'payload_files': len(rr), 'directories': len(dirs), 'manifest_sha256': sha(raw(F / NAME)),
                      'production_imported_compiled_executed': False, 'future_acceptance_approved': False}, sort_keys=True))


if __name__ == '__main__':
    main()
