"""Finite integrity controls only; these tests do not verify a PDE theorem.
Place this script beside the six named author/corrected release inputs.
Usage: python -I -S replay_adversarial_controls.py [input-directory]
"""
import copy
import hashlib
import io
import json
import os
import pathlib
import shutil
import stat
import subprocess
import sys
import tempfile
import warnings
import zipfile

ROOT = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent
PINS = {
    'GRAPH_NLS_30003521_AUTHOR_BOOTSTRAP.py': 'c18de7407e4e097a48b1c2369cd16df5ad93bc2378342eace2d54e5b30da7dcb',
    'GRAPH_NLS_30003521_AUTHOR_EXTERNAL_MANIFEST.json': '7761f7a28c02e251d926f37ddfc5d51e3bfb326a3d1eb89e4544eee507b10f66',
    'GRAPH_NLS_30003521_AUTHOR_SAFE_FREEZE.zip': '439c6e19b62f6e75843b3c84955600842488aa8e49b8f4c5b91eed52ee64542a',
    'GRAPH_NLS_30003521_CORRECTED_BOOTSTRAP.py': '3ec6ce36e3e69d6aefb9221cea0f801c57520ccd8f8bbfe810f1b304cf880706',
    'GRAPH_NLS_30003521_CORRECTED_EXTERNAL_MANIFEST.json': '05386fd90e97e008c580fe90fc1fbffe7cf037a20bde7541085eedadbc6fabfc',
    'GRAPH_NLS_30003521_CORRECTED_SAFE.zip': 'dbf1da376f6f7cb0a0df9dee55c43986b6a6911905b65fe30518c8cfa6d51a67',
}

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

sha = lambda b: hashlib.sha256(b).hexdigest()
inputs = {}
for name, pin in PINS.items():
    data = (ROOT/name).read_bytes()
    require(sha(data) == pin, 'trusted input mismatch: ' + name)
    inputs[name] = data
results = []
SENTINEL = b'import json\nprint(json.dumps({"passed": True, "probe": "UNVERIFIED_PAYLOAD_EXECUTED"}))\n'

def pack(members):
    out = io.BytesIO()
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', UserWarning)
        with zipfile.ZipFile(out, 'w', compression=zipfile.ZIP_DEFLATED) as z:
            for name, data, mode in members:
                info = zipfile.ZipInfo(name, (2026,10,6,0,0,0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = mode << 16
                z.writestr(info, data)
    return out.getvalue()

for corrected in (False, True):
    prefix = 'GRAPH_NLS_30003521_' + ('CORRECTED' if corrected else 'AUTHOR')
    bname = prefix + '_BOOTSTRAP.py'
    mname = prefix + '_EXTERNAL_MANIFEST.json'
    zname = prefix + ('_SAFE.zip' if corrected else '_SAFE_FREEZE.zip')
    base_manifest = json.loads(inputs[mname])
    with zipfile.ZipFile(io.BytesIO(inputs[zname])) as z:
        base_members = [(n,z.read(n),0o100644) for n in z.namelist()]
    scenarios = ['intact_relocated_poisoned_environment', 'stale_manifest_modified_checker', 'mutated_manifest', 'mutated_archive_tail', 'mutated_archive_same_size']
    if corrected:
        scenarios += ['layer_duplicate_member', 'layer_missing_member', 'layer_extra_member', 'layer_wrong_member_bytes', 'layer_wrong_member_sha256', 'layer_symlink_member', 'layer_bad_archive_name', 'layer_manifest_member_duplicate', 'layer_bad_expected_names', 'layer_checker_reports_false', 'layer_checker_bad_count', 'layer_checker_false_detail']
    for scenario in scenarios:
        for optimized in (False,True):
            with tempfile.TemporaryDirectory(prefix='graph-nls-controls-') as temp:
                temp = pathlib.Path(temp)
                payload = temp/'relocated inputs with spaces';payload.mkdir()
                cwd = temp/'unrelated hostile cwd';cwd.mkdir()
                poison = b'raise RuntimeError("POISON_IMPORT_EXECUTED")\n'
                for directory in (payload,cwd):
                    for name in ('json.py','hashlib.py','fractions.py','sitecustomize.py','tempfile.py'):
                        (directory/name).write_bytes(poison)
                manifest = copy.deepcopy(base_manifest)
                members = list(base_members)
                bootstrap = inputs[bname]
                archive = inputs[zname]
                mb = inputs[mname]
                if scenario == 'stale_manifest_modified_checker':
                    members = [(n,SENTINEL if n=='check_identities.py' else b,m) for n,b,m in members]
                    archive = pack(members)
                elif scenario == 'mutated_manifest':
                    mb += b' '
                elif scenario == 'mutated_archive_tail':
                    archive += b'harmless appended audit probe'
                elif scenario == 'mutated_archive_same_size':
                    archive = archive[:10] + bytes([archive[10] ^ 1]) + archive[11:]
                elif scenario.startswith('layer_'):
                    # These diagnostic copies deliberately repin higher layers to
                    # reach lower validation branches. They are never releases.
                    if scenario == 'layer_duplicate_member': members.append(members[0])
                    elif scenario == 'layer_missing_member': members=members[:-1]
                    elif scenario == 'layer_extra_member': members.append(('extra.txt',b'x',0o100644))
                    elif scenario == 'layer_wrong_member_bytes': manifest['files'][0]['bytes']+=1
                    elif scenario == 'layer_wrong_member_sha256': manifest['files'][0]['sha256']='0'*64
                    elif scenario == 'layer_symlink_member': members=[(n,b,0o120777 if i==0 else m) for i,(n,b,m) in enumerate(members)]
                    elif scenario == 'layer_bad_archive_name': manifest['archive']['name']='other.zip'
                    elif scenario == 'layer_manifest_member_duplicate': manifest['files'].append(manifest['files'][0])
                    elif scenario == 'layer_bad_expected_names': manifest['files'][0]['name']='../traversal.txt'
                    elif scenario.startswith('layer_checker_'):
                        fake={'passed':True,'count':11,'checks':{str(i):True for i in range(11)}}
                        if scenario == 'layer_checker_reports_false':fake['passed']=False
                        elif scenario == 'layer_checker_bad_count':fake['count']=10
                        else:fake['checks']['0']=False
                        replacement=('import json\nprint('+repr(json.dumps(fake))+')\n').encode()
                        members=[(n,replacement if n=='check_identities.py' else b,m) for n,b,m in members]
                        for row in manifest['files']:
                            if row['name']=='check_identities.py':row.update(bytes=len(replacement),sha256=sha(replacement))
                    archive=pack(members)
                    manifest['archive'].update(bytes=len(archive),sha256=sha(archive))
                    mb=(json.dumps(manifest,indent=2)+'\n').encode()
                    bootstrap=bootstrap.replace(PINS[mname].encode(),sha(mb).encode())
                (payload/bname).write_bytes(bootstrap)
                (payload/mname).write_bytes(mb)
                (payload/zname).write_bytes(archive)
                env=dict(os.environ, PYTHONPATH=str(cwd), PYTHONHOME=str(cwd), PYTHONOPTIMIZE='2')
                command=[sys.executable,'-I','-S']+(['-O'] if optimized else [])+[str(payload/bname)]
                proc=subprocess.run(command,cwd=cwd,env=env,capture_output=True,text=True,timeout=30)
                should_succeed=(scenario=='intact_relocated_poisoned_environment' or (not corrected and optimized))
                require((proc.returncode==0)==should_succeed, 'unexpected result: '+prefix+' '+scenario+' '+str(optimized))
                if scenario=='stale_manifest_modified_checker':
                    require(('UNVERIFIED_PAYLOAD_EXECUTED' in proc.stdout)==(not corrected and optimized),'sentinel execution mismatch')
                require('POISON_IMPORT_EXECUTED' not in proc.stdout+proc.stderr,'module isolation failed')
                marker='validation failed: '
                rejection = proc.stderr.split(marker)[-1].splitlines()[0] if marker in proc.stderr else ('AssertionError' if 'AssertionError' in proc.stderr else None)
                results.append({'target':'corrected' if corrected else 'original','case':scenario,'optimized':optimized,'exit_code':proc.returncode,'expected_behavior_observed':True,'unverified_sentinel_executed':'UNVERIFIED_PAYLOAD_EXECUTED' in proc.stdout,'rejection':rejection,'upper_layers_reanchored_for_diagnostic_only':scenario.startswith('layer_')})
    if corrected:
        check_source = dict((n,b) for n,b,m in base_members)['check_identities.py']
        broken = check_source.replace(b'c = F(1, 3)',b'c = F(1, 2)')
        require(broken != check_source,'checker fault injection target missing')
        for optimized in (False,True):
            with tempfile.TemporaryDirectory(prefix='graph-nls-checker-control-') as td:
                f=pathlib.Path(td)/'checker.py';f.write_bytes(broken)
                p=subprocess.run([sys.executable,'-I','-S']+(['-O'] if optimized else [])+[str(f)],capture_output=True,text=True,timeout=30)
                require(p.returncode!=0 and 'finite identity checks failed' in p.stderr,'checker accepted false identity')
                results.append({'target':'corrected_checker','case':'direct_false_identity_injection','optimized':optimized,'exit_code':p.returncode,'expected_behavior_observed':True,'unverified_sentinel_executed':False,'rejection':'finite identity checks failed','upper_layers_reanchored_for_diagnostic_only':False})
print(json.dumps({'schema':'graph-nls-adversarial-controls-v1','all_expected_results':True,'count':len(results),'original_failure_confirmed':True,'corrected_release_accepted':True,'release_inputs_pinned_before_execution':PINS,'scope':'Finite integrity and diagnostic controls, not a PDE proof or exhaustive security audit. A separately trusted bootstrap is the root of trust.','results':results},indent=2,sort_keys=True))
