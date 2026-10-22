#!/usr/bin/env python3
"""Explicit own-file checkpoint without fetching a pack into a full filesystem.

GitHub createCommitOnBranch uses an exact expected parent and changes only the
supplied files. No deletions, force push, checkout, index or local Git writes.
API contract: https://docs.github.com/en/graphql/reference/commits and /git.
This checkpoints research drafts; it does not accept or publish a preprint.
"""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('Use Python -I -S -B')
import argparse
import base64
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import uuid

P = Path(__file__).resolve().parent
ROOT = P.parent
PREFIX = P.name + '/'
REPO = 'AlecKriebel/Math'

def need(ok, text):
    if not ok:
        raise ValueError(text)

def now():
    return datetime.now(timezone.utc).isoformat()

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def graphql(query, variables):
    payload = json.dumps({'query': query, 'variables': variables}).encode()
    result = subprocess.run(['gh', 'api', 'graphql', '--input', '-'], input=payload,
                            cwd=ROOT, capture_output=True, timeout=60)
    try:
        reply = json.loads(result.stdout)
    except Exception as error:
        raise RuntimeError('No JSON response; inspect exact intent before retrying') from error
    return result.returncode, reply

def main_head():
    code, reply = graphql('query{repository(owner:"AlecKriebel",name:"Math"){ref(qualifiedName:"refs/heads/main"){target{oid}}}}', {})
    need(code == 0 and not reply.get('errors'), 'main metadata read failed')
    value = reply['data']['repository']['ref']['target']['oid']
    need(re.fullmatch('[0-9a-f]{40}', value) is not None, 'main SHA')
    return value

def own_file(name):
    need(type(name) is str and name.startswith(PREFIX)
         and PurePosixPath(name).as_posix() == name and '\\' not in name
         and all(x not in ('', '.', '..') for x in name.split('/')), 'own canonical path required')
    parts = name.split('/')
    need(not any(x.startswith('private') or x in ('tmp', 'venv', '.venv', 'runtime', '.git', '__pycache__') for x in parts), 'private/cache/runtime path excluded')
    need(parts[-1] != 'source_record_private.txt', 'raw source excluded')
    path = ROOT / name
    need(not any(x.is_symlink() for x in (path, *path.parents)), 'symlink path excluded')
    st = path.lstat()
    need(stat.S_ISREG(st.st_mode) and st.st_nlink == 1 and st.st_size <= 8*1024**2, 'bounded regular single-link file required')
    raw = path.read_bytes()
    need(len(raw) == st.st_size and path.read_bytes() == raw, 'input changed while capturing')
    return raw

def blob_metadata(commit, names):
    result = {}
    for start in range(0, len(names), 80):
        batch = names[start:start+80]
        fields = ' '.join('f'+str(i)+':object(expression:'+json.dumps(commit+':'+name)+'){__typename ...on Blob{oid byteSize}}' for i,name in enumerate(batch))
        code, reply = graphql('query{repository(owner:"AlecKriebel",name:"Math"){'+fields+'}}', {})
        need(code == 0 and not reply.get('errors'), 'immutable own-file metadata read failed')
        values = reply['data']['repository']
        need(set(values) == {'f'+str(i) for i in range(len(batch))}, 'incomplete metadata')
        result.update({name:values['f'+str(i)] for i,name in enumerate(batch)})
    return result

def exclusive_json(path, value):
    raw = (json.dumps(value, indent=2)+'\n').encode()
    with path.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--allowlist', required=True)
    parser.add_argument('--message', required=True)
    parser.add_argument('--receipt', required=True)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    need(re.fullmatch('[A-Za-z0-9_.-]+[.]json', args.receipt), 'simple receipt name')
    branch = subprocess.run(['git','symbolic-ref','--short','HEAD'],cwd=ROOT,
                            capture_output=True,check=True,text=True).stdout.strip()
    need(branch == 'main', 'local checkout must stay main')
    listing = json.loads(own_file(args.allowlist))
    names = listing['paths'] if type(listing) is dict else listing
    need(type(names) is list and names and len(names) == len(set(names)) and len(names) <= 512, 'explicit unique own-file allowlist')
    captured = {name:own_file(name) for name in names}
    need(sum(map(len,captured.values())) <= 8*1024**2, 'total checkpoint cap')
    pins = {name:{'bytes':len(raw),'sha256':sha(raw),'git_blob':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()} for name,raw in captured.items()}
    parent = main_head()
    old = blob_metadata(parent, names)
    changed = [name for name in names if old[name] is None or old[name].get('__typename') != 'Blob' or old[name].get('oid') != pins[name]['git_blob']]
    need(changed, 'no changed own files')
    marker = 'research-checkpoint-'+str(uuid.uuid4())
    intent = {'utc':now(),'expected_parent':parent,'marker':marker,'method':'GitHub GraphQL createCommitOnBranch exact-parent; own additions only','files':{n:pins[n] for n in changed},'no_deletions':True,'local_checkout_index_HEAD_untouched':True,'uncertain_outcome_rule':'Do not repeat mutation. Locate marker in current main commit history and verify its exact parent and own blob pins; otherwise reconcile first.'}
    print(json.dumps({'dry_run':args.dry_run,'parent':parent,'changed_paths':len(changed),'bytes':sum(len(captured[n]) for n in changed)}),flush=True)
    if args.dry_run:
        return
    folder = P/'checkpoints'
    folder.mkdir(exist_ok=True)
    receipt = folder/args.receipt
    need(not receipt.exists(), 'receipt exists')
    exclusive_json(folder/(args.receipt+'.intent.json'),intent)
    for name in changed:
        need(own_file(name) == captured[name], 'input changed before mutation')
    query = 'mutation($input:CreateCommitOnBranchInput!){createCommitOnBranch(input:$input){commit{oid url parents(first:2){nodes{oid}}}clientMutationId}}'
    variables = {'input':{'branch':{'repositoryNameWithOwner':REPO,'branchName':'main'},'expectedHeadOid':parent,'message':{'headline':args.message,'body':marker},'clientMutationId':marker,'fileChanges':{'additions':[{'path':n,'contents':base64.b64encode(captured[n]).decode()} for n in changed]}}}
    code, reply = graphql(query,variables)
    if code != 0 or reply.get('errors'):
        print(json.dumps({'mutation_reply':reply,'intent_marker':marker,'no_automatic_retry':True}),flush=True)
        raise RuntimeError('Mutation rejected or uncertain; inspect exact intent before any retry')
    action = reply['data']['createCommitOnBranch']
    commit = action['commit']['oid']
    need(action['clientMutationId'] == marker and action['commit']['parents']['nodes'] == [{'oid':parent}], 'exact single-parent checkpoint readback')
    new = blob_metadata(commit,changed)
    need(all(new[n] is not None and new[n].get('__typename')=='Blob' and new[n].get('oid')==pins[n]['git_blob'] and new[n].get('byteSize')==pins[n]['bytes'] for n in changed), 'immutable committed byte identity')
    out = {**intent,'completed_utc':now(),'commit':commit,'url':action['commit']['url'],'push_confirmed':True,'committed_files_independently_read_back':True,'observed_main_after':main_head()}
    print(json.dumps({'commit':commit,'push_confirmed':True,'paths':len(changed),'all_own_blob_pins_verified':True}),flush=True)
    try:
        exclusive_json(receipt,out)
    except OSError as error:
        print(json.dumps({'confirmed_checkpoint':out,'receipt_saved':False,'error':str(error)}),flush=True)
        raise

if __name__ == '__main__':
    main()
