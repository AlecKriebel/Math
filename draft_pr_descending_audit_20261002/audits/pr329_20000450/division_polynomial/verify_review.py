#!/usr/bin/env python3
"""Read-only historical review integrity and mathematical replay.

public: candidate copies, public audit bodies, five current computations/streams.
full: additionally all owned private primary/render/native/historical evidence.
No sources are downloaded, files written, old failures rerun, or live inputs bound.
The manifest needs an external trusted pin; this script cannot supply a seal.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
DEFAULT_PYTHON = str(ROOT.parent/'geometry/.runtime/bin/python')


def pin(path, record):
    if path.is_symlink() or not path.is_file():
        raise ValueError('Expected regular file: '+str(path))
    data = path.read_bytes()
    if len(data) != record['bytes'] or hashlib.sha256(data).hexdigest() != record['sha256']:
        raise ValueError('File bytes/hash mismatch: '+str(path))
    if 'mode' in record and f'{stat.S_IMODE(path.stat().st_mode):04o}' != record['mode']:
        raise ValueError('Mode mismatch: '+str(path))
    return data


def owned(relative):
    p = ROOT/relative
    if '..' in Path(relative).parts or Path(relative).is_absolute():
        raise ValueError('Unsafe relative manifest path: '+relative)
    return p


def candidate_integrity():
    manifest = json.loads((ROOT/'CANDIDATE_INPUT_MANIFEST.json').read_text())
    expected = set()
    for record in manifest['files']:
        path = ROOT/'candidate'/record['relative_path']
        data = pin(path, record)
        blob = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        if blob != record['git_blob_sha']:
            raise ValueError('Candidate Git-blob hash mismatch: '+str(path))
        expected.add(record['relative_path'])
    actual = {str(p.relative_to(ROOT/'candidate')) for p in (ROOT/'candidate').rglob('*') if p.is_file()}
    if expected != actual or len(expected) != 21:
        raise ValueError('Candidate copy inventory mismatch')
    counts = {}
    for name, field in [('AUTHOR_MANIFEST.json','public_files'),('PUBLICATION_MANIFEST.json','files')]:
        obj = json.loads((ROOT/'candidate'/name).read_text())
        for relative, record in obj[field].items():
            data = pin(ROOT/'candidate'/relative, record)
            blob = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
            if blob != record['git_blob_sha1']:
                raise ValueError('Inner candidate blob hash mismatch: '+relative)
        counts[name] = len(obj[field])
    review = json.loads((ROOT/'candidate/review/REVIEW_MANIFEST.json').read_text())
    for record in review['files']:
        pin(ROOT/'candidate/review'/record['path'], record)
    counts['review/REVIEW_MANIFEST.json'] = len(review['files'])
    if list(counts.values()) != [11,20,5]:
        raise ValueError('Inner candidate manifest count mismatch')
    for relative in ['TURN_1_CHECKS.json','REPLAY_CHECKS.json','review/author_replay.json']:
        if (ROOT/'candidate'/relative).read_bytes() != (ROOT/'native/candidate_verifier_owned.stdout').read_bytes():
            raise ValueError('Historical candidate output discrepancy: '+relative)
    return counts


def native_receipts(scope):
    aliases = json.loads((ROOT/'HISTORICAL_CODE_ALIASES.json').read_text())['aliases']
    alias_map = {(a['receipt'],a['original_code_path'],a['sha256']):a['preserved_relative_path'] for a in aliases}
    historical = {'independent_generic_chord':-15,'independent_generic_chord_optimized':1,'independent_model_identities':1}
    public_stems = {'independent_generic_chord_final','independent_finite_controls','independent_model_identities_final','independent_quintic_factor_final','candidate_verifier_owned'}
    count = 0
    for receipt in sorted((ROOT/'native').glob('*.receipt.json')):
        stem = receipt.name[:-len('.receipt.json')]
        if scope == 'public' and stem not in public_stems:
            continue
        obj = json.loads(receipt.read_text())
        start = datetime.datetime.fromisoformat(obj['start_utc'])
        end = datetime.datetime.fromisoformat(obj['end_utc'])
        if start.tzinfo is None or end.tzinfo is None or end < start:
            raise ValueError('Invalid native UTC order: '+receipt.name)
        if not isinstance(obj['exit_code'],int) or not obj['argv']:
            raise ValueError('Missing actual native execution metadata: '+receipt.name)
        if obj['exit_code'] != historical.get(stem,0):
            raise ValueError('Unexpected retained native exit: '+receipt.name)
        for stream in ('stdout','stderr'):
            pin(ROOT/'native'/f'{stem}.{stream}',{'bytes':obj[stream+'_bytes'],'sha256':obj[stream+'_sha256']})
        for original, record in obj.get('code_pins',{}).items():
            relative_receipt = str(receipt.relative_to(ROOT))
            alias = alias_map.get((relative_receipt,original,record['sha256']))
            path = owned(alias) if alias else Path(original)
            # Code/evidence pins must refer to this historical owned namespace.
            if ROOT not in path.parents:
                raise ValueError('Unexpected outside owned code pin: '+str(path))
            pin(path, record)
        count += 1
    if scope == 'public' and count != 5:
        raise ValueError('Missing current native evidence')
    return count


def replay(python):
    jobs = [('independent_chord.py','independent_generic_chord_final'),
            ('independent_finite.py','independent_finite_controls'),
            ('independent_model.py','independent_model_identities_final'),
            ('independent_quintic_factors.py','independent_quintic_factor_final'),
            ('candidate/verify_turn1.py','candidate_verifier_owned')]
    results = []
    for relative, stem in jobs:
        argv = [python,'-B',str(ROOT/relative)]
        begin = datetime.datetime.now(datetime.timezone.utc).isoformat()
        process = subprocess.run(argv,cwd=ROOT,capture_output=True,
            env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0'),timeout=120)
        end = datetime.datetime.now(datetime.timezone.utc).isoformat()
        if process.returncode != 0 or process.stderr:
            raise ValueError('Replay failed '+relative+'; actual exit='+str(process.returncode)+'; stderr='+process.stderr.decode(errors='replace'))
        observed = json.loads(process.stdout)
        expected = json.loads((ROOT/'native'/f'{stem}.stdout').read_text())
        # Only declared interpreter provenance may vary; all mathematical fields,
        # SymPy version and field/count/negative-control content must be exact.
        interpreter = observed.pop('interpreter',None)
        expected.pop('interpreter',None)
        if observed != expected or observed.get('status') != 'PASS':
            raise ValueError('Mathematical JSON discrepancy: '+relative)
        if 'sympy_version' in observed and observed['sympy_version'] != '1.14.0':
            raise ValueError('Unexpected symbolic runtime version: '+relative)
        results.append(dict(program=relative,start_utc=begin,end_utc=end,argv=argv,
            actual_exit=process.returncode,stdout_bytes=len(process.stdout),
            stdout_sha256=hashlib.sha256(process.stdout).hexdigest(),stderr_bytes=len(process.stderr),
            complete_mathematical_JSON_matches=True,declared_interpreter=interpreter))
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scope',choices=['public','full'],default='full')
    parser.add_argument('--python',default=DEFAULT_PYTHON,help='Existing Python with SymPy1.14.0; no install')
    args = parser.parse_args()
    obj = json.loads((ROOT/'OWNED_NAMESPACE_MANIFEST.json').read_text())
    records = obj['files']
    selected = {relative:record for relative,record in records.items() if args.scope == 'full' or record['public_replay']}
    for relative, record in selected.items():
        pin(owned(relative),record)
    if args.scope == 'full':
        actual = {str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() or p.is_symlink()}
        expected = set(records)|{'OWNED_NAMESPACE_MANIFEST.json'}
        if actual != expected:
            raise ValueError('Full namespace inventory mismatch; extra='+str(sorted(actual-expected))+' missing='+str(sorted(expected-actual)))
        actual_dirs = {str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_dir() and not p.is_symlink()}
        if actual_dirs != set(obj['directory_modes']):
            raise ValueError('Full directory inventory mismatch')
        for relative, mode in obj['directory_modes'].items():
            if f'{stat.S_IMODE(owned(relative).stat().st_mode):04o}' != mode:
                raise ValueError('Directory mode mismatch: '+relative)
        if f'{stat.S_IMODE(ROOT.stat().st_mode):04o}' != obj['root_mode']:
            raise ValueError('Root directory mode mismatch')
        source = json.loads((ROOT/'SOURCE_INPUT.json').read_text())
        pin(Path(source['source']),source)
        image = source['provided_operative_image']
        pin(Path(image['path']),image)
        for source in json.loads((ROOT/'PRIMARY_INPUTS.json').read_text())['sources']:
            pin(Path(source['path']),source)
    inner_counts = candidate_integrity()
    receipt_count = native_receipts(args.scope)
    result = json.loads((ROOT/'REVIEW_RESULT.json').read_text())
    if result['family_verdict'] != 'PASS' or result['publication_clearance'] or result['self_sealed']:
        raise ValueError('Historical scoped verdict changed')
    runs = replay(args.python)
    print(json.dumps(dict(status='PASS',scope=args.scope,owned_files_checked=len(selected),
        candidate_files_checked=21,inner_manifest_payload_counts=inner_counts,
        native_receipts_checked=receipt_count,read_only=True,
        mathematical_replays=runs,historical_manifest_self_excluded=True,
        external_manifest_pin_required=True,publication_clearance=False,
        scope_limit='Checks recorded historical bytes, executions and mathematical identities; source/scientific reading and external closure remain separate.'),indent=2))


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print('FAIL: '+str(error),file=sys.stderr)
        raise SystemExit(1)
