"""Externally caller-pinned, strictly read-only closed-plan/input verifier.

No service, Git, replay, write or action authorization. Invoke with -B.
"""
from pathlib import Path
import argparse
import hashlib
import json
import stat

ROOTS = [
    'publication_preparation_03',
    'ROOT_PREPARATION03_COMPLETE_REPAIR_ACCEPTED_FOR_NEW_WHOLE_REVIEWS.json',
    'ROOT_PREPARATION03_FIRST_NEW_WHOLE_REVIEW_ADOPTION.json',
    'ROOT_FULL_QUALIFIED_MATHEMATICS_ADOPTION.json',
    'ROOT_INPUT_BINDING.json', 'ROOT_SCOPE.md',
    'ROOT_SECOND_NEW_PREPARATION03_WHOLE_REVIEW_AND_FINAL_SCIENTIFIC_PACKAGE_ADOPTION.json',
]


def require(ok, label):
    if not ok:
        raise RuntimeError(label)


def record(p):
    s = p.lstat()
    require(not stat.S_ISLNK(s.st_mode), 'symlink forbidden')
    d = stat.S_ISDIR(s.st_mode)
    require(d or stat.S_ISREG(s.st_mode), 'nonregular entry forbidden')
    row = {'kind':'directory' if d else 'file', 'mode':stat.S_IMODE(s.st_mode),
           'mtime_ns':s.st_mtime_ns, 'nlink':s.st_nlink}
    if not d:
        b = p.read_bytes()
        row.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
    return row


def input_snapshot(root):
    out = {}
    for name in ROOTS:
        q = root/name
        for p in ([q,*sorted(q.rglob('*'))] if q.is_dir() else [q]):
            out[p.relative_to(root).as_posix()] = record(p)
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--manifest-sha256',required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    b = (root/'CLOSED_DIRECTORY_SEAL.json').read_bytes()
    require(hashlib.sha256(b).hexdigest()==args.manifest_sha256,'caller-pinned seal changed')
    seal = json.loads(b)
    require(set(seal)=={'schema','excluded_exact_paths','entries'},'seal keys')
    require(seal['schema']=='pr1332-readonly-integration-plan-closed-v1','seal schema')
    require(seal['excluded_exact_paths']==['CLOSED_DIRECTORY_SEAL.json'],'exact self-exclusion')
    actual = {}
    for p in [root,*sorted(root.rglob('*'))]:
        name = p.relative_to(root).as_posix()
        if name!='CLOSED_DIRECTORY_SEAL.json':actual[name]=record(p)
    require(actual==seal['entries'],'closed namespace/bytes/modes/nsmtime/nlinks changed')
    baseline = json.loads((root/'INPUT_BASELINE.json').read_text())
    require(baseline['frozen_roots']==ROOTS and set(baseline)=={'frozen_roots','entries'},'frozen input roots')
    require(input_snapshot(root.parent)==baseline['entries'],'frozen scientific/root inputs changed')
    print(json.dumps({'status':'PASS','seal_sha256':args.manifest_sha256,
                      'payload_files':sum(v['kind']=='file'for v in actual.values()),
                      'directories':sum(v['kind']=='directory'for v in actual.values()),
                      'all_output_namespace_bytes_mode_nsmtime_nlink_exact':True,
                      'all7_frozen_input_roots_exact_unchanged':True,
                      'service_or_Git_mutations':0,'writes':0,'action_authority':False},sort_keys=True))


if __name__=='__main__':
    main()
