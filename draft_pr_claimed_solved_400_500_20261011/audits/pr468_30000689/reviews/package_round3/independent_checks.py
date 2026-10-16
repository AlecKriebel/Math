#!/usr/bin/env python3
"""Read-only candidate audit; all extraction and invalid copies stay private."""
import ast
import datetime
import difflib
import hashlib
import importlib.util
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys
import zipfile

sys.dont_write_bytecode = True
OUT = Path(__file__).resolve().parent
ROOT = OUT.parent.parent
PACKAGE = ROOT / 'package'
PRIVATE = OUT / 'private_sources'


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def save(name, data):
    (OUT/name).write_text(json.dumps(data, indent=2, sort_keys=True)+'\n')


def execute(script, mode, cwd=None):
    command = [sys.executable]+(['-O'] if mode == 'optimized' else [])+[str(script)]
    run = subprocess.run(command, cwd=cwd, capture_output=True, timeout=300)
    return {'mode':mode, 'exit_code':run.returncode, 'stdout_sha256':sha(run.stdout),
            'stdout_bytes':len(run.stdout), 'stderr':run.stderr.decode(errors='replace'),
            'stdout':run.stdout.decode(errors='replace')}


def apply_unified(original, patch):
    source = original.splitlines(keepends=True)
    result = []
    position = 0
    lines = patch.splitlines(keepends=True)
    i = 0
    while i < len(lines):
        if not lines[i].startswith('@@'):
            i += 1
            continue
        match = re.match(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', lines[i])
        require(match is not None, 'Bad patch hunk')
        start = int(match[1])-1
        result.extend(source[position:start])
        position = start
        i += 1
        while i < len(lines) and not lines[i].startswith('@@'):
            line = lines[i]
            if line.startswith((' ', '-')):
                require(position < len(source) and source[position] == line[1:], 'Patch context differs')
                position += 1
            if line.startswith((' ', '+')):
                result.append(line[1:])
            i += 1
    result.extend(source[position:])
    return ''.join(result)


def package_checks():
    selected = json.loads((PACKAGE/'SHA256SUMS.json').read_text())['files']
    freeze = json.loads((ROOT/'PACKAGE_REVIEW_INPUT_3.json').read_text())['files']
    readback = {}
    for name, record in freeze.items():
        p = PACKAGE/name
        current = {'sha256':sha(p.read_bytes()), 'bytes':p.stat().st_size}
        require(current == record, 'Freeze mismatch '+name)
        readback[name] = current
    for name, record in selected.items():
        p = PACKAGE/name
        require(p.is_file() and not p.is_symlink(), 'Selected file type '+name)
        require({'sha256':sha(p.read_bytes()), 'bytes':p.stat().st_size} == record, 'Selected mismatch '+name)
    extraction = PRIVATE/'zip_extract'
    extraction.mkdir(exist_ok=True)
    members = []
    with zipfile.ZipFile(PACKAGE/'missing_faces_verification_v1.zip') as archive:
        infos = archive.infolist()
        require(len(infos)==len({x.filename for x in infos}), 'Duplicate member')
        require(set(x.filename for x in infos)==set(selected)|{'SHA256SUMS.json'}, 'Archive membership')
        require(archive.testzip() is None, 'CRC failure')
        for info in infos:
            name = info.filename
            path = PurePosixPath(name)
            require(not path.is_absolute() and '..' not in path.parts and '\\' not in name,
                    'Unsafe member '+name)
            mode = info.external_attr >> 16
            require(not info.is_dir() and not stat.S_ISLNK(mode), 'Nonregular archive member')
            require(stat.S_IFMT(mode) in (0, stat.S_IFREG), 'Unsupported member file type')
            data = archive.read(info)
            require(data == (PACKAGE/name).read_bytes(), 'Archive readback '+name)
            require(len(data)==info.file_size, 'Archive size')
            target = extraction/name
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(data)
            members.append({'name':name,'bytes':len(data),'sha256':sha(data),'crc32':info.CRC})
    historical = PACKAGE/'verification/historical'
    snapshot = ROOT/'source_snapshot/unsolved_math_prioritization/attempts/30000689'
    historical_files = sorted(p.relative_to(historical).as_posix() for p in historical.rglob('*') if p.is_file())
    require(len(historical_files)==15, 'Historical count')
    require(historical_files == sorted(p.relative_to(snapshot).as_posix() for p in snapshot.rglob('*') if p.is_file()), 'Snapshot membership')
    for name in historical_files:
        require((historical/name).read_bytes()==(snapshot/name).read_bytes(), 'Historical changed '+name)
    references = []
    for base, manifest, key, pathkey in [(historical/'release','FROZEN_AUTHOR_MANIFEST.json','files','path'),
        (historical/'audit','AUDIT_MANIFEST.json','audit_files','file'),
        (historical,'PUBLICATION_MANIFEST.json','public_payload_files','path')]:
        for record in json.loads((base/manifest).read_text())[key]:
            p = base/record[pathkey]
            require(sha(p.read_bytes())==record['sha256'] and p.stat().st_size==record['bytes'], 'Historical manifest mismatch')
            references.append(str(p.relative_to(PACKAGE)))
    require(len(references)==24,'Historical reference count')
    patches={}
    for name, original in [('check_exact.py',historical/'release/check_exact.py'),
                           ('check_independent.py',historical/'audit/check_independent.py')]:
        patch = (PACKAGE/'verification/patches'/name.replace('.py','.patch')).read_text()
        result = apply_unified(original.read_text(),patch)
        current = (PACKAGE/'verification/checks'/name).read_text()
        require(result==current,'Patch does not produce current checker')
        patches[name]={'exactly_produces_current':True,'sha256':sha(current.encode())}
    old_author=json.loads((historical/'release/exact_results.json').read_text())
    new_author=json.loads((PACKAGE/'verification/expected/author_results.json').read_text())
    old_scope=old_author.pop('scope');new_scope=new_author.pop('scope')
    require(old_author==new_author,'Numerical author output changed')
    require((historical/'audit/independent_results.json').read_bytes()==(PACKAGE/'verification/expected/audit_results.json').read_bytes(),'Audit output changed')
    explicit = {}
    for name in ['reproduce.py','checks/check_exact.py','checks/check_independent.py','checks/check_bitmask_controls.py']:
        tree=ast.parse((PACKAGE/'verification'/name).read_text())
        require(not any(isinstance(node,ast.Assert) for node in ast.walk(tree)), 'Removable assertion '+name)
        explicit[name]={'no_assert':True,'require_defined':any(isinstance(node,ast.FunctionDef) and node.name=='require' for node in ast.walk(tree))}
    meta=json.loads((PACKAGE/'metadata.json').read_text())
    deposit=json.loads((PACKAGE/'deposit.json').read_text())
    require(meta==deposit['metadata'],'Canonical metadata mismatch')
    require((extraction/'metadata.json').read_bytes()==(PACKAGE/'metadata.json').read_bytes(),'Archived metadata bytes')
    spec=importlib.util.spec_from_file_location('audit_zenodo_pure','/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    loaded,files=module.load_manifest(PACKAGE/'deposit.json')
    require(loaded==meta,'Pure kit metadata mismatch')
    receipt=json.loads((PACKAGE/'ARCHIVE_RECEIPT.json').read_text())
    require(receipt['bytes']==freeze['missing_faces_verification_v1.zip']['bytes'] and receipt['sha256']==freeze['missing_faces_verification_v1.zip']['sha256'] and receipt['file_count']==len(members),'Archive receipt')
    save('PACKAGE_CHECKS.json',{'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'freeze':readback,
        'selected_payload_count':len(selected),'zip_member_count':len(members),'members':members,'all_crc_and_payload_readbacks':True,
        'historical_files_identical_to_source_snapshot':historical_files,'historical_manifest_reference_count':len(references),
        'historical_manifest_references':references,'patches':patches,'author_scope_before':old_scope,'author_scope_after':new_scope,
        'all_numerical_author_json_unchanged':True,'audit_expected_bytes_unchanged':True,'explicit_guards':explicit,
        'canonical_deposit_archive_metadata_equal':True,'pure_kit_files':[{**f,'path':str(f['path'])} for f in files],
        'pure_kit_usage':'Only import and load_manifest; no client, token, state or network call.'})
    reproduction=execute(extraction/'verification/reproduce.py','normal',extraction/'verification')
    require(reproduction['exit_code']==0 and not reproduction['stderr'],'Extracted reproduction failed')
    save('REPRODUCTION.json',{'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'extracted_archive':True,'receipt':json.loads(reproduction['stdout']), 'driver_exit_code':reproduction['exit_code'],'driver_stderr':reproduction['stderr']})


def faults():
    fixture_root=PRIVATE/'invalid_fixtures';fixture_root.mkdir(exist_ok=True)
    mutations=[
      ('author_rank','check_exact.py','return len(basis)','return len(basis)-1',"source quotient equality",'original line 139'),
      ('author_missing_cell','check_exact.py','cells+=1','if cells == 0:\n                cells += 1\n                continue\n            cells+=1','remove one disjoint pair from formal Flores cycle','original line 107'),
      ('audit_empty_filling','check_independent.py','return {pool[j] for j in solve(cols,target)}','return set()','replace computed homological filling by zero chain','original line 106'),
      ('audit_missing_cell','check_independent.py',' bd=set()',' omega.remove(next(iter(omega)))\n bd=set()','delete one mapped witness cell','original line 106'),
      ('bitmask_rank','check_bitmask_controls.py','return pivot_row','return pivot_row+1','wrong modular relation rank','Source quotient dimensions'),
      ('bitmask_circuit','check_bitmask_controls.py','    for power in range(ambient_dimension+1):','    coefficients=(-coefficients[0],)+coefficients[1:]\n    for power in range(ambient_dimension+1):','flip one affine dependence coefficient','Circuit affine dependence fails'),
      ('bitmask_filling','check_bitmask_controls.py','    actual=set()','    if result:\n        result.remove(min(result))\n    actual=set()','delete a triangle from a solved chain filling','Returned filling has wrong boundary')]
    computations=[]
    for name,script,before,after,mechanism,guard in mutations:
        source=(PACKAGE/'verification/checks'/script).read_text()
        require(source.count(before)==1,'Mutation target is not unique '+name)
        target=fixture_root/(name+'.py');target.write_text(source.replace(before,after))
        for mode in ['normal','optimized']:
            run=execute(target,mode)
            run.update({'case':name,'mechanism':mechanism,'expected_guard_substring':guard,'fixture_sha256':sha(target.read_bytes())})
            run['intended_runtime_rejection']=run['exit_code']!=0 and 'RuntimeError:' in run['stderr'] and guard in run['stderr']
            computations.append(run)
    drivers=[]
    cases=['changed_script','changed_expected','missing_file','directory_as_file','inside_direct_script_symlink',
           'inside_direct_expected_symlink','outside_direct_symlink','escaping_path','absolute_escaping_path',
           'wrong_expected_with_updated_hash','unexpected_stderr_with_updated_hash','benign_symlink_ancestor']
    for name in cases:
        dest=fixture_root/name
        shutil.copytree(PACKAGE/'verification',dest)
        manifest=json.loads((dest/'CONTROL_MANIFEST.json').read_text());case=manifest['cases'][0]
        script=dest/case['script'];expected=dest/case['expected']
        guard='Control file checksum mismatch'
        if name=='changed_script':script.write_bytes(script.read_bytes()+b'\n')
        elif name=='changed_expected':expected.write_bytes(expected.read_bytes()+b'\n')
        elif name=='missing_file':script.unlink();guard='Missing regular control file'
        elif name=='directory_as_file':script.unlink();script.mkdir();guard='Missing regular control file'
        elif name in ('inside_direct_script_symlink','inside_direct_expected_symlink'):
            target=script if name=='inside_direct_script_symlink' else expected
            alias=target.with_name('actual_'+target.name);target.rename(alias);target.symlink_to(alias.name);guard='Missing regular control file'
        elif name=='outside_direct_symlink':
            outside=fixture_root/(name+'_outside.py');outside.write_bytes(script.read_bytes());script.unlink();script.symlink_to(outside);guard='Control path escapes package'
        elif name in ('escaping_path','absolute_escaping_path'):
            outside=fixture_root/(name+'_outside.py');outside.write_bytes(script.read_bytes())
            case['script']=str(outside) if name.startswith('absolute') else '../'+outside.name;guard='Control path escapes package'
        elif name=='wrong_expected_with_updated_hash':
            expected.write_bytes(b'{"deliberately_wrong": true}\n');case['expected_sha256']=sha(expected.read_bytes());guard='output differs from recorded bytes'
        elif name=='unexpected_stderr_with_updated_hash':
            script.write_bytes(script.read_bytes()+b'\nimport sys\nsys.stderr.write("deliberate diagnostic\\n")\n');case['script_sha256']=sha(script.read_bytes());guard='produced unexpected diagnostic output'
        elif name=='benign_symlink_ancestor':
            (dest/'checks').rename(dest/'actual_checks');(dest/'checks').symlink_to('actual_checks',target_is_directory=True);guard=None
        (dest/'CONTROL_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
        for mode in ['normal','optimized']:
            run=execute(dest/'reproduce.py',mode,dest)
            run.update({'case':name,'expected_guard_substring':guard})
            run['intended_runtime_rejection']=guard is not None and run['exit_code']!=0 and 'RuntimeError:' in run['stderr'] and guard in run['stderr']
            run['accepted_probe']=guard is None and run['exit_code']==0 and not run['stderr']
            drivers.append(run)
    save('FAULT_CONTROLS.json',{'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'scope':'Actual computation faults and disposable file integrity/type/path controls; finite evidence, not universal or general security certification.',
        'computation_fault_runs':computations,'driver_runs':drivers,
        'computation_intended_rejections':sum(r['intended_runtime_rejection'] for r in computations),
        'driver_intended_rejections':sum(r['intended_runtime_rejection'] for r in drivers),
        'accepted_ancestor_symlink_probes':sum(r['accepted_probe'] for r in drivers),
        'invalid_fixtures':'Only ignored private_sources/invalid_fixtures; not successful verifications or public output artifacts.'})
    unexpected=[r for r in computations if not r['intended_runtime_rejection']]+[r for r in drivers if not (r['intended_runtime_rejection'] or r['accepted_probe'])]
    require(not unexpected,'Unexpected adverse result: '+str([(r['case'],r['mode'],r['exit_code'],r['stderr'][-240:]) for r in unexpected]))


if __name__=='__main__':
    package_checks()
    faults()
    print('Package, extraction, historical bytes, patches, pure metadata, reproduction and actual controls completed.')
