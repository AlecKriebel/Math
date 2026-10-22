"""One-time local correction of the sealed first release-helper review. No actions."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil
D=Path(__file__).resolve().parent;PUB=D.parent/'publication';H=D/'history/release_helpers_review01_frozen'
assert not H.exists(),'One-time repair already started; reconcile instead of reapplying'
H.mkdir(parents=True)
review=D/'release_helpers_adversary_01';m=json.loads((review/'AUTHORED_MANIFEST.json').read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for r in m['files']:
    p=review/r['path'];assert p.stat().st_size==r['bytes'] and sha(p)==r['sha256']
probe=json.loads((review/'PROBE_RESULTS.json').read_text())
for r in probe['helper_pins']:
    p=Path(r['path']);assert p.stat().st_size==r['bytes'] and sha(p)==r['sha256'];shutil.copyfile(p,H/p.name)
# Shared pure bindings, process serialization and exclusive durable intents.
s=(D/'release_binding_candidate.py').read_text().replace('import sys\n','import sys\nimport os\nimport fcntl\nfrom urllib.parse import urlsplit\n')
s=s.replace("    rows=c.get('submission_files')", """    helper_names=['append_verified_tracker.py','integrate_reviewed_pr.py','publish_preprint.py','release_binding.py','verify_and_merge.py','verify_published_readonly.py']
    helpers=c.get('release_helpers')
    require(type(helpers) is list and [x.get('path') for x in helpers]==helper_names,'Exact reviewed release-helper set required')
    for row in helpers:file_pin(root.parent/'publication',row)
    rows=c.get('submission_files')""")
s=s.replace("    return z\n\n\ndef tracker", """    verify_doi(z)
    return z


def verify_doi(z):
    d=z.get('doi_resolution',{})
    u=urlsplit(d.get('resolved_url',''))
    require(d.get('status')=='resolved' and type(d.get('http_status')) is int and 200<=d['http_status']<300,'DOI resolution is still pending')
    require(d.get('url')==z.get('doi_url') and u.scheme=='https' and u.hostname=='zenodo.org' and u.path.rstrip('/')=='/records/'+str(z.get('id')),'DOI did not resolve to the verified version record')


def tracker""")
s+='''

def acquire(pub):
    """Caller retains this handle for the whole workflow; all stages share the lock."""
    path=Path(pub)/'private_transport/release.lock';path.parent.mkdir(parents=True,exist_ok=True)
    handle=path.open('a+')
    try:fcntl.flock(handle.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
    except BlockingIOError:
        handle.close();raise RuntimeError('Another release stage is active; no parallel action allowed')
    return handle


def exclusive_json(path,data):
    """Atomic first-writer intent, flushed before the associated provider mutation."""
    with Path(path).open('x') as f:
        f.write(json.dumps(data,indent=2)+'\\n');f.flush();os.fsync(f.fileno())


def pr_identity(pr,head,draft=None,state='open'):
    require(pr.get('number')==210 and pr.get('state')==state,'Wrong PR/state')
    require(pr.get('head',{}).get('sha')==head and pr['head'].get('ref')=='dot/math-5100033','Wrong expected native head/branch')
    require(pr['head'].get('repo',{}).get('full_name')=='AlecKriebel/Math','Wrong head repository')
    require(pr.get('base',{}).get('ref')=='main' and pr['base'].get('repo',{}).get('full_name')=='AlecKriebel/Math','Wrong base repository/branch')
    if draft is not None:require(pr.get('draft') is draft,'Wrong draft state')
'''
compile(s,'release_binding.py','exec');(PUB/'release_binding.py').write_text(s)
header="import sys\nif not __debug__ or sys.flags.optimize:\n    raise RuntimeError('Release helpers refuse optimized Python before any action')\n"
imports="from release_binding import context,binding,unchanged,publication,tracker,acquire,exclusive_json,pr_identity,require,digest\n"
for name in ['publish_preprint.py','append_verified_tracker.py','integrate_reviewed_pr.py','verify_and_merge.py']:
    p=PUB/name;s=p.read_text();start=s.index('from pathlib import Path');s=s[:start]+header+imports+s[start:]
    # Context is checked before any provider calls. Assertions remain behind explicit optimization refusal.
    needle="clear = json.loads((R / 'FINAL_CLEARANCE.json').read_text())"
    s=s.replace(needle,"_RELEASE_LOCK=acquire(PUB)\nCTX=context(R)\nclear=CTX['clear']")
    if name=='publish_preprint.py':
        s=s.replace("assert pr['state'] == 'open' and pr['draft'] and pr['head']['sha'] == '2180d64b648b81ac660a792f7823d0b715f9cf12'","pr_identity(pr,'2180d64b648b81ac660a792f7823d0b715f9cf12',True)")
        s=s.replace("assert local['environment'] == 'production' and len(local['files']) == 2","assert local['environment'] == 'production' and local['files']==CTX['expected_files']\nunchanged(R,CTX)")
        a=s.index("(PUB / 'STAGE_ATTEMPT.json').write_text(");b=s.index("stage = call('02-stage'",a)
        s=s[:a]+"exclusive_json(PUB/'STAGE_ATTEMPT.json',{'utc':datetime.now(timezone.utc).isoformat(),'operation':'single stage about to be attempted','release_binding':binding(CTX),'files':CTX['expected_files']})\n"+s[b:]
        s=s.replace("assert stage['state'] == 'ready_to_publish' and stage['files'] == local['files']","assert stage['state'] == 'ready_to_publish' and stage['files'] == CTX['expected_files']")
        a=s.index("(PUB / 'PUBLISH_ATTEMPT.json').write_text(");b=s.index("published = call('04-publish'",a)
        s=s[:a]+"unchanged(R,CTX)\nexclusive_json(PUB/'PUBLISH_ATTEMPT.json',{'utc':datetime.now(timezone.utc).isoformat(),'id':stage['id'],'operation':'single publish about to be attempted','release_binding':binding(CTX)})\n"+s[b:]
        a=s.index("verified = call('05-inspect-published'")
        s=s[:a]+"from verify_published_readonly import verify_existing\nreceipt=verify_existing(R,PUB,CTX)\nprint(json.dumps({k:v for k,v in receipt.items() if k not in ['metadata','tool_postpublication_readback']},indent=2))\n"
    elif name=='append_verified_tracker.py':
        s=s.replace("z = json.loads((PUB / 'ZENODO_VERIFIED_PUBLICATION.json').read_text())","z=publication(R,PUB,CTX)")
        s=s.replace("existing = [(i, r) for i, r in enumerate(values, 1) if any(z['doi'] in str(c) for c in r)]", """import re
problem=re.compile(r'(?<![0-9])5100033(?![0-9])|AMR-050-0033',re.I)
problem_rows=[(i,r) for i,r in enumerate(values,1) if any(problem.search(str(c)) for c in r)]
existing = [(i, r) for i, r in enumerate(values, 1) if any(z['doi'] in str(c) for c in r)]
require(not problem_rows or (len(problem_rows)==1 and problem_rows==existing and problem_rows[0][1]==row),'Conflicting problem row already exists; reconcile read-only')""")
        s=s.replace("assert len(existing) == 1 and existing[0][1] == row and attempt.exists(), 'Existing DOI requires reconciliation'","assert len(existing) == 1 and existing[0][1] == row and attempt.exists(), 'Existing DOI requires reconciliation'\n    old_attempt=json.loads(attempt.read_text())\n    require(old_attempt.get('release_binding')==binding(CTX) and old_attempt.get('payload',{}).get('values')==[row],'Prior attempt belongs to different release/payload')")
        a=s.index("    attempt.write_text(");b=s.index("    result = call('03-append'",a)
        s=s[:a]+"    unchanged(R,CTX);publication(R,PUB,CTX)\n    exclusive_json(attempt,{'utc':datetime.now(timezone.utc).isoformat(),'spreadsheet_id':SHEET,'sheet_id':1254632077,'doi_url':doi,'payload':payload,'release_binding':binding(CTX),'status':'single append about to be attempted'})\n"+s[b:]
        s=s.replace("'exact_all_four_cells_readback': True}","'exact_all_four_cells_readback': True,'release_binding':binding(CTX),'publication_receipt_sha256':digest(PUB/'ZENODO_VERIFIED_PUBLICATION.json')}")
    elif name=='integrate_reviewed_pr.py':
        s=s.replace("z = json.loads((PUB / 'ZENODO_VERIFIED_PUBLICATION.json').read_text())","z=publication(R,PUB,CTX)").replace("t = json.loads((PUB / 'TRACKER_VERIFIED_APPEND.json').read_text())","t=tracker(R,PUB,CTX,z)")
        s=s.replace("assert pr['state'] == 'open' and pr['draft'] and pr['head']['sha'] == OLD","pr_identity(pr,OLD,True)")
        s=s.replace("'whole_manuscript_adversary_02']:","'whole_manuscript_adversary_02','whole_manuscript_adversary_03','release_helpers_adversary_01','release_helpers_adversary_02']:")
        s=s.replace("assert fresh_pr['state']=='open' and fresh_pr['draft'] and fresh_pr['head']['sha']==OLD","pr_identity(fresh_pr,OLD,True)\nunchanged(R,CTX);publication(R,PUB,CTX);tracker(R,PUB,CTX,z)")
        a=s.index("(PUB/'NATIVE_PREPARE_ATTEMPT.json').write_text(");b=s.index("api('PATCH', 'git/refs",a)
        s=s[:a]+"exclusive_json(PUB/'NATIVE_PREPARE_ATTEMPT.json',dict(utc=datetime.now(timezone.utc).isoformat(),old=OLD,head=head,main=main,branch='dot/math-5100033',nonforce=True,release_binding=binding(CTX)))\n"+s[b:]
        s=s.replace("'foreign_main_tree_preserved': True}","'foreign_main_tree_preserved': True,'release_binding':binding(CTX),'publication_receipt_sha256':digest(PUB/'ZENODO_VERIFIED_PUBLICATION.json'),'tracker_receipt_sha256':digest(PUB/'TRACKER_VERIFIED_APPEND.json')}")
    else:
        s=s.replace("assert not (PUB / 'PR_MERGED.json').exists(), 'Already merged; read-only reconciliation only'","assert not (PUB / 'PR_MERGED.json').exists(), 'Already merged; read-only reconciliation only'\nrequire(not (PUB/'NATIVE_MERGE_REQUEST.json').exists(),'Prior merge intent exists: read-only reconciliation only')")
        s=s.replace("z = json.loads((PUB / 'ZENODO_VERIFIED_PUBLICATION.json').read_text())","z=publication(R,PUB,CTX)").replace("t = json.loads((PUB / 'TRACKER_VERIFIED_APPEND.json').read_text())","t=tracker(R,PUB,CTX,z)\nrequire(p.get('release_binding')==binding(CTX),'Prepared PR belongs to another release')\nrequire(p.get('publication_receipt_sha256')==digest(PUB/'ZENODO_VERIFIED_PUBLICATION.json') and p.get('tracker_receipt_sha256')==digest(PUB/'TRACKER_VERIFIED_APPEND.json'),'Prepared native receipts changed')")
        s=s.replace("assert pr['state'] == 'open' and not pr['merged'] and pr['head']['sha'] == head","pr_identity(pr,head)\nassert not pr['merged']\nactual_commit=api('GET','git/commits/'+head)\nrequire(actual_commit['tree']['sha']==p['tree'] and [x['sha'] for x in actual_commit['parents']]==[clear['original_native_head'],p['main_parent']],'Actual commit tree/parents disagree with prepared receipt')",1)
        s=s.replace("    sha = p['tree']","    sha = actual_commit['tree']['sha']")
        s=s.replace("if pr['draft']:\n    result", "if pr['draft']:\n    exclusive_json(PUB/'NATIVE_READY_ATTEMPT.json',dict(utc=datetime.now(timezone.utc).isoformat(),head=head,release_binding=binding(CTX)))\n    result")
        s=s.replace("    assert pr['state'] == 'open' and not pr['merged'] and not pr['draft'] and pr['head']['sha'] == head","    pr_identity(pr,head,False)\n    assert not pr['merged']")
        s=s.replace("(PUB / 'NATIVE_MERGE_REQUEST.json').write_text(json.dumps(request, indent=2) + '\\n')","unchanged(R,CTX);publication(R,PUB,CTX);tracker(R,PUB,CTX,z)\nexclusive_json(PUB/'NATIVE_MERGE_REQUEST.json',dict(request,release_binding=binding(CTX)))")
        s=s.replace("assert pr['head']['sha'] == head","pr_identity(pr,head,False,state='closed')")
        s=s.replace("'full_goal_active_incomplete': True}","'full_goal_active_incomplete': True,'release_binding':binding(CTX)}")
    compile(s,str(p),'exec');p.write_text(s)
# Read-only postpublication reconciliation is reusable after a lost response/readback.
s='''"""Verify an existing published deposit; never stage or publish."""
import sys
if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Release verification refuses optimized Python')
from pathlib import Path
from datetime import datetime,timezone
import json,subprocess,urllib.request
from release_binding import context,binding,unchanged,publication,verify_doi,acquire,exclusive_json,require


def verify_existing(R,PUB,CTX):
    if (PUB/'ZENODO_VERIFIED_PUBLICATION.json').exists():return publication(R,PUB,CTX)
    attempt=json.loads((PUB/'PUBLISH_ATTEMPT.json').read_text())
    require(attempt.get('release_binding')==binding(CTX),'Publication attempt belongs to another cleared release')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    T=PUB/'private_transport/zenodo';T.mkdir(parents=True,exist_ok=True)
    tool=Path('/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py')
    py='/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
    run=subprocess.run([py,'-B',str(tool),'inspect',str(R/'deposit.json'),'--check-doi'],capture_output=True,text=True,timeout=180)
    (T/(stamp+'-readonly-inspect-stdout.json')).write_text(run.stdout)
    (T/(stamp+'-readonly-inspect-stderr.txt')).write_text(run.stderr)
    require(run.returncode==0,'Read-only published inspection failed; no new publication request allowed')
    v=json.loads(run.stdout);unchanged(R,CTX)
    require(v.get('state')=='published' and v.get('id')==attempt['id'],'Existing deposit publication not confirmed')
    require(v.get('files')==CTX['expected_files'],'Provider file set differs from clearance')
    provider={'utc':datetime.now(timezone.utc).isoformat(),'submitted':True,'id':v['id'],'provider_metadata_MD5_and_size_verified':True,'actual_public_SHA256_pending':True,'release_binding':binding(CTX),'tool_readback':v}
    (PUB/'ZENODO_PROVIDER_CONFIRMED_PUBLICATION.json').write_text(json.dumps(provider,indent=2)+'\\n')
    downloads=[]
    try:
        require(v.get('doi')=='10.5281/zenodo.'+str(v['id']) and v.get('doi_url')=='https://doi.org/'+v['doi'] and v.get('record_url')=='https://zenodo.org/records/'+str(v['id']),'Invalid DOI/record identity')
        verify_doi(v)
        import hashlib
        for row in CTX['expected_files']:
            url=v['record_url']+'/files/'+row['name']+'?download=1'
            request=urllib.request.Request(url,headers={'User-Agent':'Math-Research-Publication-Verification/1.0'})
            with urllib.request.urlopen(request,timeout=60) as response:raw=response.read()
            require(len(raw)==row['size'] and hashlib.sha256(raw).hexdigest()==row['sha256'],'Actual public download SHA256/size mismatch')
            downloads.append({'file':row['name'],'bytes':len(raw),'sha256':row['sha256'],'actual_public_download_byte_hash_match':True})
    except Exception as e:
        (PUB/'PUBLICATION_VERIFICATION_PENDING.json').write_text(json.dumps(dict(utc=datetime.now(timezone.utc).isoformat(),submitted=True,id=v['id'],release_binding=binding(CTX),actual_public_downloads=downloads,error=str(e),recovery='Run this read-only verifier only; never restage or republish'),indent=2)+'\\n')
        raise RuntimeError('Deposit is published; DOI/public SHA verification pending. Read-only recovery only.') from e
    unchanged(R,CTX)
    receipt={'utc':datetime.now(timezone.utc).isoformat(),'submitted':True,'metadata_and_files_verified':True,'id':v['id'],'doi':v['doi'],'doi_url':v['doi_url'],'record_url':v['record_url'],'metadata':CTX['metadata'],'files':CTX['expected_files'],'metadata_normalizations':v.get('metadata_normalizations',[]),'doi_resolution':v['doi_resolution'],'tool_postpublication_readback':v,'additional_actual_public_file_downloads':downloads,'additional_public_readback_error':None,'exact_reviewed_frozen_files_published':True,'single_publish_attempt':True,'release_binding':binding(CTX)}
    exclusive_json(PUB/'ZENODO_VERIFIED_PUBLICATION.json',receipt)
    return publication(R,PUB,CTX)


if __name__=='__main__':
    PUB=Path(__file__).resolve().parent;R=PUB.parent/'preprint'
    _RELEASE_LOCK=acquire(PUB);CTX=context(R)
    r=verify_existing(R,PUB,CTX)
    print(json.dumps({k:v for k,v in r.items() if k not in ['metadata','tool_postpublication_readback']},indent=2))
'''
compile(s,'verify_published_readonly.py','exec');(PUB/'verify_published_readonly.py').write_text(s)
result=dict(utc=datetime.now(timezone.utc).isoformat(),first_review_manifest_sha256=sha(review/'AUTHORED_MANIFEST.json'),all9findings_implemented_validation_pending=True,original_helpers_preserved=str(H.relative_to(D)),manuscript_or_ZIP_changed_by_this_repair=False,new_supporting_source_review_required=True,publication_cleared=False,helpers=[dict(path=p.name,bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(PUB.glob('*.py'))])
(D/'RELEASE_HELPER_REVIEW01_RESOLUTION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
