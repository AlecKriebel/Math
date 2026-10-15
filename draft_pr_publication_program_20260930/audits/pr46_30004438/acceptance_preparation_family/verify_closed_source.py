"""ROOT-only future read-only post-exit inspection; never imports proposed helpers."""
from pathlib import Path, PurePosixPath
import argparse, datetime as dt, hashlib, json, math, os, re, stat
H = Path(__file__).resolve().parent
NAME = 'PREPARATION_MANIFEST.json'
KEYS = {'schema','status','utc','self_excluded','files_count','files','source_only',
 'proposed_helpers_imported_compiled_executed','future_acceptance_or_ROOT_approval_claimed'}

def need(ok, message):
    if not ok: raise ValueError(message)
def sha(raw): return hashlib.sha256(raw).hexdigest()
def parse(raw):
    def pairs(items):
        out = {}
        for key, value in items:
            need(key not in out, 'Duplicate JSON key'); out[key] = value
        return out
    def floating(value):
        value = float(value); need(math.isfinite(value), 'Nonfinite'); return value
    return json.loads(raw, object_pairs_hook=pairs, parse_float=floating,
      parse_constant=lambda value: (_ for _ in ()).throw(ValueError('Nonfinite')))
def relative(name):
    need(type(name) is str and name and name != '.' and '\\' not in name
      and '\0' not in name, 'Invalid path')
    path = PurePosixPath(name)
    need(not path.is_absolute() and path.as_posix() == name and not
      {'.','..','.git','__pycache__'}.intersection(path.parts), 'Noncanonical path')
    return path
def read(path):
    need(not path.is_symlink() and stat.S_ISREG(path.lstat().st_mode)
      and all(not p.is_symlink() for p in path.parents)
      and stat.S_IMODE(path.stat().st_mode) == 0o444, 'Full0444 regular file required')
    return path.read_bytes()
def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--manifest-sha256', required=True)
    args = parser.parse_args()
    need(__debug__ and os.environ.get('PYTHONOPTIMIZE','') in ('','0'), 'Optimization prohibited')
    need(re.fullmatch('[0-9a-f]{64}', args.manifest_sha256), 'Explicit manifest SHA256 required')
    body = read(H / NAME); need(sha(body) == args.manifest_sha256, 'Closed manifest differs')
    obj = parse(body)
    need(type(obj) is dict and set(obj) == KEYS and obj['schema'] == 'pr46-acceptance-source-closure/v1'
      and obj['status'] == 'CLOSED_SOURCE_ONLY' and obj['source_only'] is True
      and obj['proposed_helpers_imported_compiled_executed'] is False
      and obj['future_acceptance_or_ROOT_approval_claimed'] is False
      and obj['self_excluded'] == [NAME], 'Exact source-only closure schema differs')
    rows = obj['files']
    need(type(rows) is list and type(obj['files_count']) is int and len(rows) == obj['files_count']
      and len({z['path'] for z in rows}) == len(rows), 'Closure rows differ')
    names, directories, folded = {NAME}, set(), set()
    for row in rows:
        need(type(row) is dict and set(row) == {'path','bytes','sha256'}, 'Exact member schema differs')
        relative(row['path']); need(row['path'] != NAME, 'Self listed as payload')
        raw = read(H / row['path'])
        need(type(row['bytes']) is int and row['bytes'] >= 0 and row['bytes'] == len(raw)
          and sha(raw) == row['sha256'], 'Entire member body differs')
        if row['path'].endswith('.json'): parse(raw)
        names.add(row['path'])
        directories.update(p.as_posix() for p in PurePosixPath(row['path']).parents if p.as_posix() != '.')
    actual_names, actual_dirs = set(), set()
    for path in H.rglob('*'):
        name = path.relative_to(H).as_posix(); relative(name)
        need(name.casefold() not in folded and not path.is_symlink(), 'Alias/symlink')
        folded.add(name.casefold()); mode = path.lstat().st_mode
        if stat.S_ISDIR(mode): actual_dirs.add(name)
        else:
            need(stat.S_ISREG(mode), 'FIFO/special member'); read(path); actual_names.add(name)
    need(actual_names == names and actual_dirs == directories, 'Exact self-only topology differs')
    need(read(H / NAME) == body, 'Manifest changed during post-exit read')
    print(json.dumps({'status':'PASS_READONLY_CLOSED_SOURCE_ONLY','actual_inspecting_pid':os.getpid(),
      'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'manifest_sha256':args.manifest_sha256,
      'payload_files':len(rows),'relative_directories':len(directories),
      'proposed_helpers_imported_compiled_executed':False,
      'future_acceptance_or_ROOT_approval_claimed':False}, sort_keys=True))
if __name__ == '__main__': main()
