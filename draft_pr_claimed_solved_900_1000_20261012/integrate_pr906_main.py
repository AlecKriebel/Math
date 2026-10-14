"""Integrate accepted immutable PR906 bytes with current main, without checkout."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
A = Path(__file__).resolve().parent/'audits/pr906_30006419'
HEAD = '32eaecaa8907dbf674e65b138b000cdcc49004ae'
QUEUE = 'unsolved_math_prioritization/QUEUE.md'

def require(ok,message):
    if not ok: raise RuntimeError(message)

def run(args,**kwargs):
    return subprocess.run(args,cwd=ROOT,check=True,capture_output=True,text=True,**kwargs).stdout.strip()

def rawblob(ref,path):
    return subprocess.run(['git','show',ref+':'+path],cwd=ROOT,check=True,capture_output=True).stdout

def main():
    accepted = json.loads((A/'ACCEPTANCE.json').read_text())
    require(accepted['accepted'] and len(accepted['full_package_reviews'])>=2,
            'Whole submission must pass sequential fresh reviews before integration')
    require(accepted['original_pr_head']==HEAD,'Wrong audited source head')
    freeze = json.loads((A/'publication/PREPUBLICATION_FREEZE.json').read_text())
    for name,r in freeze['files'].items():
        data = (A/'publication'/name).read_bytes()
        require(len(data)==r['bytes'] and hashlib.sha256(data).hexdigest()==r['sha256'],
                'Frozen publication changed: '+name)
    live = json.loads(run(['gh','pr','view','906','--repo','AlecKriebel/Math',
                          '--json','state,headRefOid,headRefName,isDraft']))
    require(live['state']=='OPEN' and live['headRefOid']==HEAD,'Live source drift')
    snapshot = json.loads((A/'ORIGINAL_SNAPSHOT.json').read_text())
    require(snapshot['head']==HEAD and len(snapshot['files'])==30,'Wrong snapshot scope')
    files = run(['gh','api','repos/AlecKriebel/Math/pulls/906/files','--paginate',
                 '--jq','.[].filename']).splitlines()
    require(set(files)==set(snapshot['files'])|{QUEUE},'Unexpected PR path scope')
    proposal = rawblob(HEAD,QUEUE).decode()
    rows = [r for r in proposal.splitlines(keepends=True) if '| 30006419 /' in r]
    require(len(rows)==1 and rows[0].split('|')[8].strip()=='claimed_solved' and
            rows[0].split('|')[9].strip()=='2/5','Wrong proposal eligibility')
    source = json.loads((A/'TARGET_IDENTITY_PREFLIGHT.json').read_text())
    parent = run(['git','ls-remote','origin','refs/heads/main']).split()[0]
    run(['git','fetch','--no-write-fetch-head','origin',parent])
    catalogue = json.loads(rawblob(parent,'unsolved_math_prioritization/catalog.json'))
    target = next(r for r in catalogue if str(r['id'])=='30006419')
    require(target['review_hash']==source['review_hash'] and
            target['statement_hash']==source['statement_hash'],'Source identity changed')
    queue = rawblob(parent,QUEUE).decode()
    lines = queue.splitlines(keepends=True)
    matches = [i for i,r in enumerate(lines) if '| 30006419 /' in r]
    require(len(matches)==1,'Ambiguous main target')
    i = matches[0]; old = lines[i]
    require(old.split('|')[8].strip() in ['queued','claimed_solved'],
            'Current main target has a different disposition; do not overwrite')
    lines[i] = rows[0]
    revised = ''.join(lines)
    require(queue.replace(old,'',1)==revised.replace(rows[0],'',1),
            'Another main queue row changed')
    with tempfile.TemporaryDirectory(prefix='p906-integration-') as td:
        env = dict(os.environ,GIT_INDEX_FILE=str(Path(td)/'index'))
        run(['git','read-tree',parent],env=env)
        for path,pin in snapshot['files'].items():
            data = rawblob(HEAD,path)
            require(hashlib.sha256(data).hexdigest()==pin,'Original source changed: '+path)
            oid = run(['git','rev-parse',HEAD+':'+path])
            run(['git','update-index','--add','--cacheinfo','100644',oid,path],env=env)
        oid = run(['git','hash-object','-w','--stdin'],input=revised)
        run(['git','update-index','--add','--cacheinfo','100644',oid,QUEUE],env=env)
        changes = run(['git','diff','--cached','--name-only',parent],env=env).splitlines()
        require(set(changes)<=set(snapshot['files'])|{QUEUE},'Unexpected integration scope')
        tree = run(['git','write-tree'],env=env)
        sha = run(['git','commit-tree',tree,'-p',HEAD,'-p',parent],
                  input='Integrate byte-preserved audited PR906 proposal with current main\n')
    for path,pin in snapshot['files'].items():
        require(hashlib.sha256(rawblob(sha,path)).hexdigest()==pin,'Integration altered packet')
    live2 = json.loads(run(['gh','pr','view','906','--repo','AlecKriebel/Math',
                           '--json','state,headRefOid']))
    require(live2['state']=='OPEN' and live2['headRefOid']==HEAD,'PR drift before branch push')
    run(['git','push','origin',sha+':refs/heads/'+live['headRefName']])
    receipt = {'utc':datetime.now(timezone.utc).isoformat(),'original_audited_head':HEAD,
               'integrated_head':sha,'main_parent':parent,'tree':tree,
               'conflict_path':QUEUE,'conflict_resolution':'Only exact target30006419 proposal row; all other main queue bytes preserved',
               'math_packet_files':30,'all_original_file_sha256_unchanged':True,
               'frozen_publication_files_unchanged':True,'only_differences_from_main':changes,
               'push_confirmed':True,'shared_checkout_index_head_untouched':True,
               'next_gate':'Fresh independent integration review; no merge yet'}
    (A/'MERGE_INTEGRATION_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))

if __name__=='__main__':main()
