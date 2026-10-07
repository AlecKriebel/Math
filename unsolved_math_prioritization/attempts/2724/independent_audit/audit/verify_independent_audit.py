#!/usr/bin/env python3
"""Independent integrity and diagnostic replay; never a proof of KP-1.65."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tempfile
import zipfile

def require(value, message):
    if not value:
        raise RuntimeError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def load(path):
    return json.loads(Path(path).read_bytes())

def package(zip_path, manifest_path):
    manifest = load(manifest_path)
    data = Path(zip_path).read_bytes()
    require(len(data) == manifest['artifact']['bytes'], 'archive size mismatch')
    require(sha(data) == manifest['artifact']['sha256'], 'archive digest mismatch')
    expected = {item['path']: item for item in manifest['files']}
    with zipfile.ZipFile(zip_path) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)), 'duplicate archive paths')
        require(set(names) == set(expected), 'archive inventory mismatch')
        require(archive.testzip() is None, 'archive CRC failure')
        files = {}
        for name in names:
            p = PurePosixPath(name)
            require(not p.is_absolute() and '..' not in p.parts, 'unsafe path')
            b = archive.read(name)
            require(len(b) == expected[name]['bytes'], 'member size mismatch')
            require(sha(b) == expected[name]['sha256'], 'member digest mismatch')
            files[p.name] = b
        require(len(files) == len(names), 'ambiguous basenames')
    internal = json.loads(files['FILE_MANIFEST.json'])
    require(internal['self_excluded'] is True, 'manifest exclusion not explicit')
    require({x['path'] for x in internal['files']} == set(files)-{'FILE_MANIFEST.json'},
            'internal inventory mismatch')
    for item in internal['files']:
        require(len(files[item['path']]) == item['bytes'], 'internal byte mismatch')
        require(sha(files[item['path']]) == item['sha256'], 'internal hash mismatch')
    status = json.loads(files['STATUS.json'])
    for key in ('full_solution', 'counterexample_to_original_problem', 'novelty_claim'):
        require(status[key] is False, 'scope widened: '+key)
    require(status['status'] == 'unsolved' and status['turns_used'] == 1
            and status['turn_limit'] == 5, 'unexpected task scope')
    return files, {'sha256':sha(data), 'bytes':len(data), 'members_verified':len(files)}

def run(command, cwd, expect_pass):
    p = subprocess.run(command, cwd=cwd, text=True, capture_output=True, timeout=30)
    if expect_pass:
        require(p.returncode == 0, 'unexpected replay failure: '+p.stderr)
        result = json.loads(p.stdout)
        require(result == {'status':'PASS','checks':135,
            'scope':'local polynomial differential identities only',
            'problem_2724_solved':False}, 'unexpected replay output')
    else:
        require(p.returncode != 0, 'negative control was not rejected')
        require('RuntimeError' in p.stderr, 'negative control failed for unrelated reason')
        result = {'rejected':True, 'failure_kind':'RuntimeError'}
    return {'optimization':command[1] if len(command)>1 and command[1] in ('-O','-OO') else 'normal',
            'returncode':p.returncode, 'result':result}

def replay(files):
    source = files['verify_local_model.py'].decode()
    mutations = {
        'wrong_local_y': ('a,b = contact_pullback(S,', 'a,b = contact_pullback(add(S,ONE),'),
        'wrong_local_z': ('a,b = contact_pullback(S, mul(add(S,ONE),U))',
                          'a,b = contact_pullback(S, mul(add(S,scale(ONE,2)),U))'),
        'wrong_omega_sign': ('return sub(add(derivative(b, 0), b), derivative(a, 1))',
                             'return add(add(derivative(b, 0), b), derivative(a, 1))'),
        'false_legendrian_claim': ("check(b!=ZERO, 'height slices", "check(b==ZERO, 'height slices"),
        'false_family_condition': ('closed==(av==bv==cv)', 'closed==(av==bv)'),
    }
    result = {'baseline':[], 'relocated':[], 'false_premise':[], 'mutations':{}}
    with tempfile.TemporaryDirectory(prefix='kp2724-independent-') as temporary:
        root = Path(temporary)
        baseline = root/'baseline'; baseline.mkdir()
        relocated = root/'unrelated'/'path with spaces'; relocated.mkdir(parents=True)
        (baseline/'verify_local_model.py').write_text(source)
        (relocated/'different_name.py').write_text(source)
        for flags in ([],['-O'],['-OO']):
            result['baseline'].append(run([sys.executable,*flags,'verify_local_model.py'],baseline,True))
            result['relocated'].append(run([sys.executable,*flags,str(relocated/'different_name.py')],root,True))
            control = "import runpy; m=runpy.run_path('verify_local_model.py'); m['require'](False,'independent false premise')"
            result['false_premise'].append(run([sys.executable,*flags,'-c',control],baseline,False))
        for label,(before,after) in mutations.items():
            require(source.count(before)==1, 'mutation is not unique: '+label)
            mutated = source.replace(before,after)
            p = root/(label+'.py'); p.write_text(mutated)
            result['mutations'][label] = [run([sys.executable,*flags,str(p)],root,False)
                                         for flags in ([],['-O'],['-OO'])]
        # An erased guard need not be caught by the program it disables. Integrity,
        # rather than self-certification, rejects that altered verifier.
        disabled = source.replace("raise RuntimeError('FAIL: ' + label)", 'pass')
        require(disabled != source, 'guard mutation absent')
        require(sha(disabled.encode()) != sha(files['verify_local_model.py']), 'guard mutation pin collision')
        result['disabled_guard_integrity_control'] = {'digest_mismatch':True,
            'semantic_rejection_claimed':False}
    return result

def corpus(args, metadata):
    found = []
    expected = {d['name']:d for d in metadata['datasets']}
    paths = {'catalog.json':args.catalog, 'problems.json':args.problems,
             'research_results.json':args.reports}
    if not any(paths.values()):
        return {'performed':False}
    require(all(paths.values()), 'all three dataset paths are required')
    parsed = {}
    for name,path in paths.items():
        b = Path(path).read_bytes(); e = expected[name]
        require(len(b)==e['bytes'] and sha(b)==e['sha256'], 'dataset pin mismatch: '+name)
        parsed[name]=json.loads(b)
        found.append({'name':name,'bytes':len(b),'sha256':sha(b),'matched':True})
    records = [p for p in parsed['problems.json'] if str(p['id'])=='2724']
    require(len(records)==1, 'record not unique')
    record = records[0]; report = parsed['research_results.json'].get(record['problem_number'],{})
    pair = json.dumps([record,report],sort_keys=True).encode()
    require(sha(pair)==metadata['record_report_sha256'], 'complete pair hash mismatch')
    require(sha(record['statement'].encode())==metadata['statement_sha256'], 'statement hash mismatch')
    require(report=={}, 'inherited report not empty')
    entries = [p for p in parsed['catalog.json'] if str(p['id'])=='2724']
    require(len(entries)==1, 'catalog entry not unique')
    entry = entries[0]
    require(entry['rank']==905 and entry['problem_number']=='KP-1.65', 'catalog identity mismatch')
    require(entry['statement_hash']==metadata['statement_sha256'] and
            entry['review_hash']==metadata['record_report_sha256'], 'catalog hashes mismatch')
    changed = dict(record); changed.pop('background')
    require(sha(json.dumps([changed,report],sort_keys=True).encode())!=sha(pair), 'partial record mutation undetected')
    require(sha(json.dumps([record,{'mutated':True}],sort_keys=True).encode())!=sha(pair), 'report mutation undetected')
    require(sha(json.dumps([record,report],sort_keys=True,separators=(',',':')).encode())!=sha(pair),
            'serialization mutation undetected')
    return {'performed':True,'datasets':found,'rank':entry['rank'],
            'statement_sha256':metadata['statement_sha256'],
            'record_report_sha256':metadata['record_report_sha256'],
            'report_empty':True,'complete_record_read':True,'complete_report_read':True,
            'serialization':'json.dumps([complete_record,reports.get(problem_number,{})],sort_keys=True), default settings, UTF-8',
            'negative_controls':['omitted record field','changed report','compact serialization']}

def source_pins(args, metadata):
    if not args.source_directory:
        return {'performed':False}
    directory = Path(args.source_directory)
    by_hash = {}
    for p in directory.glob('*.pdf'):
        b=p.read_bytes(); by_hash[sha(b)]=(len(b), b[:5])
    results=[]
    for entry in metadata['primary_sources']:
        if 'sha256' not in entry:
            continue
        require(entry['sha256'] in by_hash, 'source hash absent: '+entry['title'])
        count,magic = by_hash[entry['sha256']]
        require(count==entry['bytes'] and magic==b'%PDF-', 'source byte/type mismatch')
        results.append({'title':entry['title'],'url':entry['url'],'sha256':entry['sha256'],
                        'bytes':count,'matched':True})
    return {'performed':True,'sources':results,'source_contents_included':False}

def integrity_controls(files):
    outcomes=[]
    with tempfile.TemporaryDirectory(prefix='kp2724-integrity-') as temporary:
        root=Path(temporary)
        def fixture(label, changed, extra=False):
            archive=root/(label+'.zip'); manifest=root/(label+'.json')
            data=dict(changed)
            if extra:
                data['unexpected.txt']=b'Unexpected member.'
            with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as z:
                for name,b in sorted(data.items()):
                    z.writestr('fixture/'+name,b)
            blob=archive.read_bytes()
            entries=[{'path':'fixture/'+name,'bytes':len(b),'sha256':sha(b)}
                     for name,b in sorted(changed.items())]
            manifest.write_text(json.dumps({'artifact':{'bytes':len(blob),'sha256':sha(blob)},'files':entries}))
            return archive,manifest
        cases={}
        cases['unexpected_member']=fixture('unexpected_member',files,True)
        internal_bad=dict(files); internal=json.loads(internal_bad['FILE_MANIFEST.json'])
        internal['files'][0]['sha256']='0'*64
        internal_bad['FILE_MANIFEST.json']=json.dumps(internal).encode()
        cases['internal_pin_changed']=fixture('internal_pin_changed',internal_bad)
        scoped=dict(files); status=json.loads(scoped['STATUS.json']);status['full_solution']=True
        scoped['STATUS.json']=json.dumps(status).encode()
        internal=json.loads(scoped['FILE_MANIFEST.json'])
        for item in internal['files']:
            if item['path']=='STATUS.json':
                item['bytes']=len(scoped['STATUS.json']);item['sha256']=sha(scoped['STATUS.json'])
        scoped['FILE_MANIFEST.json']=json.dumps(internal).encode()
        cases['self_consistent_false_solution']=fixture('self_consistent_false_solution',scoped)
        archive,manifest=fixture('archive_byte_corruption',files)
        blob=bytearray(archive.read_bytes());blob[len(blob)//2]^=1;archive.write_bytes(blob)
        cases['archive_byte_corruption']=(archive,manifest)
        for label,(archive,manifest) in cases.items():
            try:
                package(archive,manifest)
            except RuntimeError as error:
                outcomes.append({'case':label,'rejected':True,'diagnostic':str(error)})
            else:
                raise RuntimeError('integrity mutation passed: '+label)
    return outcomes

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--zip',required=True)
    parser.add_argument('--manifest',required=True)
    parser.add_argument('--catalog'); parser.add_argument('--problems'); parser.add_argument('--reports')
    parser.add_argument('--source-directory'); parser.add_argument('--output')
    args=parser.parse_args()
    files,integrity = package(args.zip,args.manifest)
    metadata=json.loads(files['PUBLIC_VERIFICATION_METADATA.json'])
    result={'status':'PASS','problem_id':2724,'scope':'artifact integrity and local diagnostic checks only',
            'problem_2724_solved':False,'integrity':integrity,'replays':replay(files),
            'integrity_negative_controls':integrity_controls(files),
            'corpus':corpus(args,metadata),'source_pins':source_pins(args,metadata)}
    output=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.output:
        Path(args.output).write_text(output)
    print(output)

if __name__=='__main__':
    main()
