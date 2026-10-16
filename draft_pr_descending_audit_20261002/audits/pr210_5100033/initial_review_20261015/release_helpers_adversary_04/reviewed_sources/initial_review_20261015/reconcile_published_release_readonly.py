"""Revalidate the SAME published pair/tracker row against repaired workflow pins.

No deposit stage/publish, sheet append/update, Git write, PR update or merge.
Preserve all initial receipts; only replace local accepted receipt bindings after
actual read-only verification of the same record, same files and same four cells.
"""
import sys
if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Read-only reconciliation refuses optimized Python')
from pathlib import Path
from datetime import datetime,timezone
import base64,hashlib,json,os,subprocess,urllib.request
D=Path(__file__).resolve().parent;C=D.parent;R=C/'preprint';PUB=C/'publication'
sys.path.insert(0,str(PUB))
from release_binding import context,binding,unchanged,publication,tracker,acquire,exclusive_json,pr_identity,require,digest,durable_mkdir,sync_directory,verify_doi
H=D/'history/release_helpers_review03_frozen'
GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
GWS='/Users/alec/.nvm/versions/node/v22.16.0/bin/gws'
PY='/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
KIT=Path('/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py')
SHEET='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
OLD='2180d64b648b81ac660a792f7823d0b715f9cf12'

def load(p):return json.loads(p.read_text())
def encoded(x):return (json.dumps(x,indent=2,ensure_ascii=False)+'\n').encode()
def replace_local(path,raw):
    temp=path.with_name(path.name+'.reconciliation-tmp')
    with temp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    os.replace(temp,path);sync_directory(path.parent)

def main():
    require(not (PUB/'RELEASE_BINDING_RECONCILIATION_ATTEMPT.json').exists(),
        'Prior local reconciliation intent exists; inspect retained local state read-only before any retry')
    lock=acquire(PUB)
    ctx=context(R);clear=ctx['clear']
    require(clear.get('prior_published_clearance_sha256')==digest(H/'FINAL_CLEARANCE.json'),
        'New clearance does not authorize this exact historical published clearance')
    pin=clear.get('supplemental_readonly_reconciliation',{})
    me=Path(__file__).resolve()
    require(pin==dict(path=me.name,bytes=me.stat().st_size,sha256=digest(me)),
        'Reconciliation source differs from fresh supplemental approval')
    archive=load(H/'ARCHIVE_MANIFEST.json')
    for row in archive['files']:
        p=H/row['path'];require(p.stat().st_size==row['bytes'] and digest(p)==row['sha256'],
            'Historical release evidence changed: '+row['path'])
    oldclear=load(H/'FINAL_CLEARANCE.json')
    for key in ['package_manifest_sha256','deposit_manifest_sha256','publication_metadata_sha256',
                'submission_files','source_manifest','manuscript_source','publication_metadata','original_native_head']:
        require(clear.get(key)==oldclear.get(key),'Scientific/publication inputs changed: '+key)
    oldbinding=dict(clearance_sha256=digest(H/'FINAL_CLEARANCE.json'),
        package_manifest_sha256=clear['package_manifest_sha256'],
        deposit_manifest_sha256=clear['deposit_manifest_sha256'],metadata_sha256=clear['publication_metadata_sha256'])
    oz=load(H/'ZENODO_VERIFIED_PUBLICATION.json');ot=load(H/'TRACKER_VERIFIED_APPEND.json')
    require((PUB/'ZENODO_VERIFIED_PUBLICATION.json').read_bytes()==(H/'ZENODO_VERIFIED_PUBLICATION.json').read_bytes()
        and (PUB/'TRACKER_VERIFIED_APPEND.json').read_bytes()==(H/'TRACKER_VERIFIED_APPEND.json').read_bytes(),
        'Initial current local receipts changed; reconcile manually')
    require(oz.get('submitted') is True and oz.get('metadata_and_files_verified') is True
        and oz.get('exact_reviewed_frozen_files_published') is True,'Historical publication not verified')
    require(oz.get('release_binding')==oldbinding and oz.get('metadata')==ctx['metadata']
        and oz.get('files')==ctx['expected_files'],'Historical public pair/binding mismatch')
    verify_doi(oz)
    require(oz.get('doi')=='10.5281/zenodo.'+str(oz.get('id'))
        and oz.get('doi_url')=='https://doi.org/'+oz['doi']
        and oz.get('record_url')=='https://zenodo.org/records/'+str(oz['id']),'Wrong old record identity')
    require(ot.get('verified') is True and ot.get('exact_all_four_cells_readback') is True
        and ot.get('release_binding')==oldbinding
        and ot.get('publication_receipt_sha256')==digest(H/'ZENODO_VERIFIED_PUBLICATION.json')
        and ot.get('spreadsheet_id')==SHEET and ot.get('sheet_id')==1254632077
        and ot.get('doi_url')==oz['doi_url'],'Historical tracker chain mismatch')
    require(ot.get('append_count')==1 and len(ot.get('values',[]))==4
        and ot['values'][0]=='https://arxiv.org/abs/2004.12497v11' and ot['values'][1]==''
        and ot['values'][2]==oz['doi_url'] and '5100033' in ot['values'][3]
        and ctx['metadata']['title'] in ot['values'][3],'Historical tracker payload mismatch')
    require(not (PUB/'NATIVE_PREPARE_ATTEMPT.json').exists() and not (PUB/'PR_PREPARED.json').exists()
        and not (PUB/'native_current_source').exists(),'Native preparation already occurred; reconcile manually')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    T=PUB/'private_transport'/('readonly_binding_reconciliation_'+stamp);durable_mkdir(T,exist_ok=False)
    def call(label,args):
        run=subprocess.run(args,capture_output=True,text=True,timeout=180)
        (T/(label+'-stdout.json')).write_text(run.stdout)
        (T/(label+'-stderr.txt')).write_text(run.stderr)
        require(run.returncode==0,label+' read-only verification failed; no mutation authorized')
        return json.loads(run.stdout)
    pr=call('PR',[GH,'api','repos/AlecKriebel/Math/pulls/210']);pr_identity(pr,OLD,True)
    require(not pr.get('merged'),'PR already merged')
    q=call('original-QUEUE',[GH,'api','repos/AlecKriebel/Math/contents/unsolved_math_prioritization/QUEUE.md?ref='+OLD])
    intake=load(D/'INTAKE.json');require(q.get('sha')==intake['Queue_blob'],'Original Queue identity changed')
    rows=[x for x in base64.b64decode(q['content']).decode().splitlines() if '5100033 / AMR-050-0033' in x]
    require(len(rows)==1 and rows[0].split('|')[8].strip()=='claimed_solved','Exact PR head is ineligible')
    v=call('published-record',[PY,'-B',str(KIT),'inspect',str(R/'deposit.json'),'--check-doi'])
    require(v.get('environment')=='production' and v.get('state')=='published'
        and v.get('id')==oz['id'] and v.get('files')==ctx['expected_files'],'Same published pair not confirmed')
    require(all(v.get(k)==oz[k] for k in ['doi','doi_url','record_url']),'Published DOI/version changed')
    verify_doi(v)
    downloads=[]
    for row in ctx['expected_files']:
        req=urllib.request.Request(v['record_url']+'/files/'+row['name']+'?download=1',
            headers={'User-Agent':'Math-Research-Publication-Verification/1.0'})
        with urllib.request.urlopen(req,timeout=60) as response:raw=response.read()
        require(len(raw)==row['size'] and hashlib.sha256(raw).hexdigest()==row['sha256'],
            'Actual unchanged public bytes mismatch')
        downloads.append(dict(file=row['name'],bytes=len(raw),sha256=row['sha256'],actual_public_download_byte_hash_match=True))
    props=call('tracker-properties',[GWS,'sheets','spreadsheets','get','--params',json.dumps(dict(spreadsheetId=SHEET))])
    tabs=[x['properties'] for x in props['sheets'] if x['properties']['sheetId']==1254632077]
    require(len(tabs)==1 and tabs[0]['title']=='Math Puzzles','Wrong tracker destination')
    cells=call('tracker-four-cells',[GWS,'sheets','spreadsheets','values','get','--params',
        json.dumps(dict(spreadsheetId=SHEET,range=ot['updated_range']))])
    require(cells.get('values')==[ot['values']],'Actual existing four tracker cells differ')
    unchanged(R,ctx)
    require(digest(me)==pin['sha256'],'Supplemental source changed during read-only verification')
    utc=datetime.now(timezone.utc).isoformat()
    z=dict(oz,utc=utc,release_binding=binding(ctx),doi_resolution=v['doi_resolution'],
        tool_postpublication_readback=v,additional_actual_public_file_downloads=downloads,
        read_only_workflow_reconciliation=True,initial_publication_receipt_sha256=digest(H/'ZENODO_VERIFIED_PUBLICATION.json'),
        initial_clearance_sha256=digest(H/'FINAL_CLEARANCE.json'),additional_stage_or_publish_calls=0)
    zr=encoded(z)
    t=dict(ot,utc=utc,release_binding=binding(ctx),publication_receipt_sha256=hashlib.sha256(zr).hexdigest(),
        read_only_workflow_reconciliation=True,initial_tracker_receipt_sha256=digest(H/'TRACKER_VERIFIED_APPEND.json'),
        additional_append_or_update_calls=0,existing_four_cells_freshly_reverified=True)
    tr=encoded(t)
    exclusive_json(PUB/'RELEASE_BINDING_RECONCILIATION_ATTEMPT.json',dict(utc=utc,
        kind='Local receipt rebinding after read-only provider revalidation; no external mutations',
        prior_release_binding=oldbinding,new_release_binding=binding(ctx),record_id=oz['id'],
        tracker_range=ot['updated_range'],new_publication_receipt_sha256=hashlib.sha256(zr).hexdigest(),
        new_tracker_receipt_sha256=hashlib.sha256(tr).hexdigest(),supplemental_source_pin=pin))
    replace_local(PUB/'ZENODO_VERIFIED_PUBLICATION.json',zr)
    replace_local(PUB/'TRACKER_VERIFIED_APPEND.json',tr)
    publication(R,PUB,ctx);tracker(R,PUB,ctx,z)
    result=dict(utc=utc,verified=True,prior_release_binding=oldbinding,new_release_binding=binding(ctx),
        unchanged_submission_pair=ctx['expected_files'],record_id=oz['id'],doi_url=oz['doi_url'],
        tracker_range=ot['updated_range'],actual_public_SHA256_downloads=downloads,exact_four_cell_readback=True,
        additional_stage_publish_append_update_or_native_mutations=0,prior_evidence_preserved=True,
        supplemental_source_pin=pin,case_completion_percent=95,actual_native_merge_pending=True)
    exclusive_json(PUB/'RELEASE_BINDING_RECONCILIATION.json',result)
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
