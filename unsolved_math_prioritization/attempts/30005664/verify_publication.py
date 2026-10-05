#!/usr/bin/env python3
"""Portable exact safe-inventory, frozen-ZIP, replay and optional-input verifier."""
import argparse
import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def fingerprint(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

def inventory(base):
    files, dirs = set(), set()
    for path in base.rglob('*'):
        require(not path.is_symlink(), 'Symlink forbidden: ' + str(path))
        rel = path.relative_to(base).as_posix()
        if path.is_file():
            files.add(rel)
        elif path.is_dir():
            dirs.add(rel)
        else:
            raise RuntimeError('Special entry forbidden: ' + str(path))
    return files, dirs

def run(script, *args):
    # -I ignores PYTHONOPTIMIZE and other inherited Python settings; no -O flag.
    code = "import sys,runpy; sys.flags.optimize == 0 or sys.exit('Assertions disabled'); sys.argv=sys.argv[1:]; runpy.run_path(sys.argv[0],run_name='__main__')"
    result = subprocess.run([sys.executable, '-I', '-B', '-c', code, str(script), *map(str,args)], cwd=ROOT, capture_output=True)
    require(result.returncode == 0, script.name + ' failed: ' + result.stderr.decode(errors='replace'))
    return result.stdout

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--queue', type=Path)
    optional = ('author-zip','catalog','problems','research-results','dataset-manifest','source-directory')
    for name in optional:
        parser.add_argument('--'+name, type=Path)
    args = parser.parse_args()
    manifest = json.loads((ROOT/'PUBLICATION_MANIFEST.json').read_bytes())
    rows = manifest['files']
    listed = [row['path'] for row in rows]
    require(len(listed) == len(set(listed)), 'Duplicate manifest entry')
    expected = set(listed) | {'PUBLICATION_MANIFEST.json'}
    actual, dirs = inventory(ROOT)
    require(actual == expected, 'Recursive file inventory mismatch: ' + repr((sorted(actual-expected),sorted(expected-actual))))
    expected_dirs = {str(parent) for n in expected for parent in Path(n).parents if str(parent) != '.'}
    require(dirs == expected_dirs, 'Recursive directory inventory mismatch')
    for row in rows:
        require(fingerprint((ROOT/row['path']).read_bytes()) == {'bytes':row['bytes'],'sha256':row['sha256']}, 'Fingerprint mismatch: '+row['path'])
    verdict = json.loads((ROOT/'VERDICT.json').read_bytes())
    require(verdict['original_problem_solved'] is False and verdict['status']=='unsolved' and verdict['turns']=='5/5', 'Disposition drift')
    frozen_count = 0
    for entry in verdict['archives']:
        archive = ROOT/entry['path']
        require(fingerprint(archive.read_bytes()) == {'bytes':entry['bytes'],'sha256':entry['sha256']}, 'Archive fingerprint mismatch')
        base = ROOT/entry['extracted_directory']
        frozen, frozen_dirs = inventory(base)
        require(not frozen_dirs, 'Unexpected nested freeze directory')
        with zipfile.ZipFile(archive) as z:
            require(z.testzip() is None, 'ZIP CRC failure')
            names = z.namelist()
            require(len(names)==len(set(names))==entry['members'] and set(names)==frozen, 'ZIP exact inventory mismatch')
            for name in names:
                require(z.read(name)==(base/name).read_bytes(), 'Archive/extracted byte mismatch: '+name)
                frozen_count += 1
        fm = json.loads((base/'MANIFEST.json').read_bytes())
        fr = fm['files']; fn = [e['path'] for e in fr]
        require(len(fn)==len(set(fn)) and set(fn)==frozen-{'MANIFEST.json'}, 'Frozen manifest inventory mismatch')
        for row in fr:
            require(fingerprint((base/row['path']).read_bytes()) == {'bytes':row['bytes'],'sha256':row['sha256']}, 'Frozen fingerprint mismatch')
    require(json.loads(run(ROOT/'author/verify_manifest.py'))['status']=='PASS','Author manifest verifier')
    require(json.loads(run(ROOT/'audit/verify_audit.py'))['status']=='PASS','Audit manifest verifier')
    author_bytes = run(ROOT/'author/check.py')
    require(author_bytes==(ROOT/'author/RESULTS.json').read_bytes(), 'Author replay bytes differ')
    audit_bytes = run(ROOT/'audit/independent_check.py')
    require(audit_bytes==(ROOT/'audit/INDEPENDENT_RESULTS.json').read_bytes(), 'Independent replay bytes differ')
    author = json.loads(author_bytes); audit = json.loads(audit_bytes)
    require(author['status']==audit['status']=='PASS', 'Replay status')
    require(author['total_assertions']==audit['reconstructed_author_controls']==957 and audit['supplemental_controls']==35, 'Control totals')
    require(author['groups']==audit['coverage_groups'], 'Coverage groups differ')
    queue_result = {'status':'NOT_RUN','reason':'No --queue supplied'}
    if args.queue:
        q = args.queue.resolve().read_bytes(); spec = verdict['queue']
        require(fingerprint(q)=={'bytes':spec['after_bytes'],'sha256':spec['after_sha256']},'Queue final hash/size mismatch')
        old,new = spec['old_row'].encode(),spec['new_row'].encode()
        require(q.count(new)==1,'Queue target row count')
        reconstructed = q.replace(new,old,1)
        require(fingerprint(reconstructed)=={'bytes':spec['before_bytes'],'sha256':spec['before_sha256']},'Other queue bytes changed')
        ac,bc = old.split(b'|'),new.split(b'|')
        require(len(ac)==len(bc) and [i for i in range(len(ac)) if ac[i]!=bc[i]]==[8,9],'Queue changed unexpected cells')
        require(bc[8].strip()==b'unsolved' and bc[9].strip()==b'5/5','Queue target status/turns')
        queue_result={'status':'PASS','only_status_and_turns_changed':True,'every_other_byte_preserved':True}
    values = [getattr(args,name.replace('-','_')) for name in optional]
    inputs={'status':'NOT_RUN','reason':'Optional external source and dataset inputs not supplied; frozen records are historical evidence'}
    if any(v is not None for v in values):
        require(all(v is not None for v in values),'Supply all six optional-input arguments together')
        missing = [name for name,value in zip(optional,values) if not value.exists()]
        if values[-1].is_dir():
            missing.extend('source-directory/'+name for name in ('owr.pdf','keller.pdf','keller_published.pdf','nice2026.pdf','ckn.pdf') if not (values[-1]/name).is_file())
        if missing:
            inputs={'status':'NOT_RUN','reason':'Optional external inputs unavailable','missing_arguments':missing}
        else:
            flags = [part for name,value in zip(optional,values) for part in ('--'+name,str(value.resolve()))]
            result=json.loads(run(ROOT/'audit/verify_inputs.py',*flags))
            require(result['status']=='PASS','Optional input verification failed')
            require(result==json.loads((ROOT/'audit/INPUT_VERIFICATION.json').read_bytes()),'Optional input output differs from frozen record')
            inputs={'status':'PASS','matches_frozen_complete_input_verification':True}
    print(json.dumps({'status':'PASS','original_problem_solved':False,'turns':'5/5','recursive_files':len(actual),'publication_hashes_verified':len(rows),'archives':len(verdict['archives']),'frozen_files_matched':frozen_count,'author_controls':957,'independent_controls':992,'replay_bytes_identical':True,'child_assertions_enabled':True,'queue':queue_result,'optional_input_verification':inputs},indent=2,sort_keys=True))

if __name__ == '__main__':
    main()
