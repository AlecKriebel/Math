#!/usr/bin/env python3
"""One finite data-only authentication; no imports/execution of reviewed code."""
from pathlib import Path
import hashlib
import json
import stat
import datetime

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
A = P/'verification/odd-areas-boolean-city-production-audit-sol-20261116'
N = P/'verification/odd-areas-boolean-city-production-sol-20261116'
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
M = P.parent

def need(ok, message):
    if not ok:
        raise ValueError(message)

def raw(path):
    need(not path.is_symlink(), 'no symlink: '+str(path))
    need(stat.S_ISREG(path.lstat().st_mode), 'regular file: '+str(path))
    return path.read_bytes()

def pin(data):
    return {'bytes':len(data), 'SHA256':hashlib.sha256(data).hexdigest()}

def authenticate(path, row):
    data = raw(path)
    need(pin(data)=={k:row[k] for k in ('bytes','SHA256')}, 'pin: '+str(path))
    if 'mode' in row:
        bits = int(row['mode'],8) if isinstance(row['mode'],str) else row['mode']
        need(stat.S_IMODE(path.lstat().st_mode)==bits, 'mode: '+str(path))
    return data

initial = json.loads(raw(A/'INITIAL_SEAL.json'))
for row in initial['payloads']:
    authenticate(A/row['path'],row)
need(len(initial['payloads'])==7, 'frozen seven INITIAL payloads')
final = json.loads(authenticate(N/'FINAL.json', {'bytes':7535,'SHA256':'5b77e5f982f264f466b970fa849f0ef097d3dbf3e87aebb3a5de6a3484ee2c01'}))
manifest = json.loads(authenticate(N/'BOUND_MANIFEST.json',final['manifest']))
for row in manifest['files']:
    authenticate(N/row['path'],row)
all_nodes = list(N.rglob('*'))
need(all(not path.is_symlink() for path in all_nodes), 'no source symlinks')
names = {path.relative_to(N).as_posix() for path in all_nodes if path.is_file()}
need(names=={row['path'] for row in manifest['files']}|{'FINAL.json','BOUND_MANIFEST.json'}, 'exact forty-file production namespace')
need(len(names)==40 and {path.relative_to(N).as_posix() for path in all_nodes if path.is_dir()}=={'pending-preparation'}, 'exact one child directory')
need(stat.S_IMODE((N/'pending-preparation').stat().st_mode)==0o755, 'archive mode')
old = N/'pending-preparation'
old_manifest = json.loads(raw(old/'MANIFEST.json'))
for row in old_manifest['files']:
    authenticate(old/row['path'],row)
need({path.name for path in old.iterdir()}=={row['path'] for row in old_manifest['files']}|{'MANIFEST.json','PREPARATION_READY.json'}, 'exact preserved seventeen-file pending packet')
old_plan = json.loads(raw(old/'PLAN.json'))
plan = json.loads(raw(N/'PLAN.json'))
need(old_plan.pop('root_adoption') is None, 'old pending adoption')
need(old_plan.pop('root_adoption_state')=='PENDING_INDEPENDENT_STAGE_PASS_AND_ROOT_ADOPTION', 'old pending state')
new_plan = dict(plan)
adoption = new_plan.pop('root_adoption')
need(new_plan.pop('root_adoption_state')=='ROOT_PROVIDED_AND_ADOPTED', 'new adopted state')
need(old_plan==new_plan, 'only two PLAN fields changed')
authenticate(P/adoption['path'],adoption)
old_sha = hashlib.sha256(raw(old/'PLAN.json')).hexdigest()
new_sha = hashlib.sha256(raw(N/'PLAN.json')).hexdigest()
old_code, new_code = raw(old/'release_four.py'), raw(N/'release_four.py')
needle = ("PLAN_SHA = '"+old_sha+"'").encode()
need(old_code.count(needle)==1 and old_code.replace(needle,("PLAN_SHA = '"+new_sha+"'").encode(),1)==new_code, 'sole helper PLAN_SHA literal changed')
for path in old.iterdir():
    if path.name not in {'PLAN.json','release_four.py'}:
        need(raw(path)==raw(N/path.name), 'other fifteen top-level originals unchanged')
need(raw(P/plan['public_payloads']['path'])==raw(A/'EXPECTED_PAYLOADS.json'), 'same fixed eighteen source payload rows')
rows = json.loads(raw(A/'EXPECTED_PAYLOADS.json'))
need(len(rows)==18 and sorted(row['website_relative_path'] for row in rows)==plan['scope_paths'], 'exact eighteen-path source contract')
need(plan['new_leaves']==16 and plan['replacements']==2 and plan['new_directories']==4 and plan['after_counts']==[727,118,119], 'exact scope/counts')
inputs = json.loads(raw(A/'INITIAL_INPUTS.json'))
authenticate(W/'.git/index',inputs['W']['index'])
authenticate(M/'.git/index',inputs['M']['index'])
authenticate(W/'.git/config',inputs['W']['config'])
need(hashlib.sha256(raw(W/'.git/HEAD')).hexdigest()==inputs['W']['HEAD_file_SHA256'], 'W HEAD file unchanged')
need(raw(W/'.git/refs/heads/master')==(inputs['W']['HEAD']+'\n').encode(), 'W existing master unchanged')
need(hashlib.sha256(raw(M/'.git/HEAD')).hexdigest()==inputs['M']['HEAD_file_SHA256'], 'M HEAD file unchanged')
loose = M/'.git/refs/heads/main'
main_lines = raw(loose).splitlines() if loose.exists() else [line.split(b' ')[0] for line in raw(M/'.git/packed-refs').splitlines() if line.endswith(b' refs/heads/main')]
need(main_lines==[inputs['M']['HEAD'].encode()], 'M existing main unchanged')
need(not any((N/name).exists() for name in ['ACTIVE_INSTALL.lock','ACTIVE_GIT.lock','INSTALL_AUTHORIZATION.json','GIT_AUTHORIZATION.json','transactions','git-transactions']), 'no runtime/action files created')
print(json.dumps({'status':'PASS_FINITE_STATIC_PACKET_AUTHENTICATION','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'production_files':40,'production_child_directories':1,'archived_pending_files':17,'INITIAL_payloads_unchanged':7,'binding_delta':'two PLAN fields plus sole helper PLAN_SHA literal','scope':'18 paths 16A2M; 727/118/119','W_index':'8db8/0644 unchanged','M_index':'91b10/0644 unchanged','reviewed_helper_executions':0,'Git_commands':0,'network_calls':0,'writes_by_this_utility':0},sort_keys=True))
