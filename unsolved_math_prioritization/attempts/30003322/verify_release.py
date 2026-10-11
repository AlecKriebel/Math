#!/usr/bin/env python3
"""Portable exact-byte and control replay gate for problem 30003322.
Uses Python 3.10+ standard library. Makes no network or repository changes.
"""
from pathlib import Path, PurePosixPath
import hashlib, json, re, subprocess, sys

AUTHOR_MANIFEST = '4a0a5cece35d143c2ebdf3683f0a7a115588f2a42b5730af77ac21aee7a84a54'
AUDIT_MANIFEST = '0d32cc832178f02c733816134d0d5f1b04dbc89c44ba049bd11cce5d11094992'
ADDENDUM = '9b8145a117a70834c57ed09f0ae2753e70bf9b5ad7164a9275a5a3a2be1e2b2c'
CORRECTIONS = '71e40d236f727d5975c6f3c65dfc9bfca9a098e00597bb5d5cea5e5c9a165333'
AUTHOR_FILES = {'APPROACH_LOG.json','CONTROL_RESULTS.json','LIMITATIONS.md','MANIFEST.json','QUEUE_UPDATE_PROPOSAL.json','README.md','REPOSITORY_GATE.json','RESULTS.md','SOURCE_VERIFICATION.json','check_controls.py'}
AUDIT_FILES = {'ADVERSARIAL_RESULTS.json','AUDIT.md','AUTHOR_CONTROL_REPLAY.json','BINDING.json','CORRECTIONS.md','MANIFEST.json','README.md','SOURCE_CHECK.json','verify_audit.py'}
ROOT_PAYLOADS = {'README.md','RELEASE_ADDENDUM.md','PUBLICATION_PROVENANCE.json','verify_release.py'}
EXPECTED = ROOT_PAYLOADS | {'author/'+p for p in AUTHOR_FILES} | {'audit/'+p for p in AUDIT_FILES}

def require(condition, message):
    if not condition: raise ValueError(message)

def sha(data): return hashlib.sha256(data).hexdigest()

def checked_inventory(root, entries, expected):
    require(isinstance(entries,list) and entries, 'empty or invalid manifest inventory')
    names=[]
    for ent in entries:
        require(isinstance(ent,dict) and set(ent)=={'path','bytes','sha256'}, 'invalid inventory entry')
        name=ent['path']
        require(isinstance(name,str) and name and '\\' not in name, 'invalid path')
        p=PurePosixPath(name)
        require(not p.is_absolute() and all(x not in ('','..','.') for x in name.split('/')) and p.as_posix()==name, 'escaping or noncanonical path')
        require(name not in names, 'duplicate inventory entry')
        names.append(name)
        require(name in expected, 'unexpected inventory entry')
        require(type(ent['bytes']) is int and ent['bytes']>=0, 'invalid byte count')
        require(isinstance(ent['sha256'],str) and re.fullmatch('[0-9a-f]{64}',ent['sha256']) is not None,'invalid hash')
        path=root/name
        require(path.is_file() and not path.is_symlink(),'missing or symlinked file: '+name)
        data=path.read_bytes()
        require(len(data)==ent['bytes'],'byte count mismatch: '+name)
        require(sha(data)==ent['sha256'],'hash mismatch: '+name)
    require(set(names)==expected,'incomplete inventory')


def run(root):
    root=root.resolve()
    for p in root.rglob('*'): require(not p.is_symlink(),'symlink in release')
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    require(actual==EXPECTED|{'MANIFEST.json'},'missing or extra release file')
    manifest=json.loads((root/'MANIFEST.json').read_text())
    require(manifest.get('schema')=='initial-surreal-release-v1' and manifest.get('problem_id')==30003322,'wrong release identity')
    require(manifest.get('disposition')=='unsolved' and manifest.get('turns')=='5/5','wrong disposition')
    require(manifest.get('author_manifest_sha256')==AUTHOR_MANIFEST,'wrong author binding')
    require(manifest.get('audit_manifest_sha256')==AUDIT_MANIFEST,'wrong audit binding')
    require(manifest.get('controlling_addendum_sha256')==ADDENDUM,'wrong addendum binding')
    checked_inventory(root,manifest.get('files'),EXPECTED)
    for folder,expected,digest in [('author',AUTHOR_FILES,AUTHOR_MANIFEST),('audit',AUDIT_FILES,AUDIT_MANIFEST)]:
        data=(root/folder/'MANIFEST.json').read_bytes()
        require(sha(data)==digest,'frozen manifest changed: '+folder)
        checked_inventory(root/folder,json.loads(data)['files'],expected-{'MANIFEST.json'})
    require(sha((root/'RELEASE_ADDENDUM.md').read_bytes())==ADDENDUM,'controlling correction changed')
    require(sha((root/'audit/CORRECTIONS.md').read_bytes())==CORRECTIONS,'audit corrections changed')
    binding=json.loads((root/'audit/BINDING.json').read_text())
    require(binding['original_manifest']['sha256']==AUTHOR_MANIFEST,'audit-to-author binding mismatch')
    require(binding['full_target_resolved'] is False and binding['budget_used']=='5/5','audit scope changed')
    prov=json.loads((root/'PUBLICATION_PROVENANCE.json').read_text())
    require(prov['current_disposition']=='unsolved' and prov['turns']=='5/5' and prov['full_target_resolved'] is False,'provenance disposition changed')
    require(prov['frozen_binding']=={'author_manifest_sha256':AUTHOR_MANIFEST,'audit_manifest_sha256':AUDIT_MANIFEST,'release_addendum_sha256':ADDENDUM},'provenance binding changed')
    require(prov['queue']['changed_fields']=={'Status':['queued','unsolved'],'Turns':['0/5','5/5']},'queue scope changed')
    author=subprocess.run([sys.executable,'-B',str(root/'author/check_controls.py')],capture_output=True,check=True)
    require(author.stdout==(root/'author/CONTROL_RESULTS.json').read_bytes(),'author replay differs')
    audit=subprocess.run([sys.executable,'-B',str(root/'audit/verify_audit.py'),str(root/'author')],capture_output=True,check=True)
    require(audit.stdout==(root/'audit/ADVERSARIAL_RESULTS.json').read_bytes(),'audit replay differs')
    standalone=subprocess.run([sys.executable,'-B',str(root/'audit/verify_audit.py')],capture_output=True,check=True)
    want=json.loads((root/'audit/ADVERSARIAL_RESULTS.json').read_text())
    for key in ['original_manifest_and_nine_payloads','original_replay_json_equal','original_replay_byte_equal']: want.pop(key)
    require(json.loads(standalone.stdout)==want,'standalone audit replay differs')
    return {'status':'PASS','problem_id':30003322,'disposition':'unsolved','turns':'5/5','manifested_payloads':len(EXPECTED),'release_files':len(actual),'frozen_author_files':len(AUTHOR_FILES),'frozen_audit_files':len(AUDIT_FILES),'corrections_C1_C2_C3_C4_and_nonsaturation_limit':'BOUND','author_replay':'PASS_BYTE_IDENTICAL','audit_bound_replay':'PASS_BYTE_IDENTICAL','standalone_audit_replay':'PASS_JSON_IDENTICAL','manifest_sha256':sha((root/'MANIFEST.json').read_bytes())}

if __name__=='__main__':
    try:
        print(json.dumps(run(Path(__file__).parent),indent=2))
    except (ValueError,KeyError,TypeError,OSError,subprocess.CalledProcessError) as exc:
        print('FAIL: '+str(exc),file=sys.stderr)
        sys.exit(1)
