#!/usr/bin/env python3
"""One-shot, same-ID unpublished verification-ZIP repair; never publishes.

Only after actual current full release authentication and an explicit immutable
baseline. Unknown outcomes reconcile by GET; an existing attempt never repeats
DELETE or PUT. The shared client is unchanged, including its 204 JSON error.
"""
from pathlib import Path
import argparse,datetime,hashlib,importlib.util,json,re,sys,uuid
PROGRAM=Path(__file__).resolve().parents[1]
A=PROGRAM/'audits/pr1262_30001248';P=A/'publication'
KNOWN=23443230
PDF='Triangle_Modular_Threshold_Note_v1.0.pdf'
ZIP='Triangle_Modular_Threshold_Verification_v1.0.zip'
FIELDS={'title','upload_type','publication_type','description','creators','access_right','license','version','publication_date','keywords','related_identifiers'}
def need(v,m):
 if not v:raise RuntimeError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def binding(p):return {'bytes':p.stat().st_size,'sha256':sha(p)}
def read(p):return json.loads(p.read_text())
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def exclusive(p,x):
 try:
  with p.open('x') as f:f.write(json.dumps(x,indent=2)+'\n')
 except FileExistsError:raise RuntimeError('Prior attempt exists; inspect known draft read-only')
def coordinator():
 path=PROGRAM/'publication_coordinators/pr1262.py';spec=importlib.util.spec_from_file_location('pr1262_repair_strict_coordinator',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def canonical_uuid(raw):
 need(isinstance(raw,str),'Missing canonical file UUID')
 try:value=str(uuid.UUID(raw))
 except (ValueError,AttributeError):raise RuntimeError('Invalid file UUID')
 need(value==raw,'Noncanonical file UUID');return raw
def baseline():
 b=read(A/'DRAFT_REPAIR_BASELINE.json')
 need(b.get('schema')=='math-pr1262-draft-repair-baseline-v1' and b.get('pr')==1262 and b.get('problem_id')==30001248 and type(b.get('id')) is int and b['id']==KNOWN and b.get('environment')=='production' and b.get('submitted') is False,'Pinned unpublished production baseline required')
 need(b.get('protected_name')==PDF and b.get('replacement_name')==ZIP,'Baseline protected/replacement names differ')
 bucket=b.get('bucket','');need(re.fullmatch(r'https://zenodo\.org/api/files/[0-9a-f-]{36}',bucket) is not None,'Canonical production bucket required');canonical_uuid(bucket.rsplit('/',1)[1])
 files=b.get('files');need(isinstance(files,list) and len(files)==2 and {e.get('name') for e in files}=={PDF,ZIP},'Exactly old PDF and ZIP baseline entries required')
 for e in files:
  need(type(e.get('size')) is int and e['size']>0 and re.fullmatch('[0-9a-f]{32}',e.get('md5','')) is not None and re.fullmatch('[0-9a-f]{64}',e.get('sha256','')) is not None,'Exact baseline size/MD5/SHA256 required');canonical_uuid(e.get('id'))
 need(len({e['id'] for e in files})==2,'Duplicate baseline file UUID')
 need(sha(P/'STAGE_INTENT.json')==b.get('stage_intent_sha256'),'Original stage intent differs')
 need(sha(P/'zenodo-deposit.json')==b.get('new_metadata_sha256'),'Explicit current escaped metadata baseline differs')
 return b

def authenticate(c,kit):
 gate=c.authenticate_release();b=baseline();need(gate.get('latest_review',{}).get('status')=='CLEAN','Current final clean actual review required')
 f=(P/gate['latest_review']['input_freeze']).resolve();need(sha(f)==gate['latest_review']['input_freeze_sha256'],'Latest freeze differs');obj=read(f);entries=obj.get('files',[])+obj.get('external_readonly_inputs',[])
 # These two additional inputs must explicitly supplement the existing full
 # release gate. External paths here are selected only by exact target identity.
 for wanted in [Path(__file__).resolve(),(A/'DRAFT_REPAIR_BASELINE.json').resolve()]:
  matches=[]
  for e in entries:
   raw=e.get('path');need(isinstance(raw,str) and '..' not in Path(raw).parts,'Malformed frozen input path');p=Path(raw);p=p if p.is_absolute() else A/p
   if p.resolve()==wanted:matches.append(e)
  need(len(matches)==1 and {k:matches[0].get(k) for k in ['bytes','sha256']}==binding(wanted),'Latest review omits/differs from actual repair helper or baseline')
 need(not (P/'PUBLISH_INTENT.json').exists() and not (P/'PUBLICATION_RECEIPT.json').exists(),'Publication attempt/receipt exists; repair prohibited')
 _,state=kit.local_state((P/'zenodo-deposit.json').resolve(),'production');need(state and type(state.get('id')) is int and state['id']==KNOWN and not state.get('publication'),'Known same-ID unpublished kit state required')
 meta,new=kit.load_manifest(P/'zenodo-deposit.json');need(set(meta)==FIELDS and len(new)==2 and {e['name'] for e in new}=={PDF,ZIP},'Exact eleven metadata fields and two current files required')
 old={e['name']:e for e in b['files']};current={e['name']:e for e in new};need(all(current[PDF][k]==old[PDF][k] for k in ['size','md5','sha256']),'Protected local PDF drift');need(current[ZIP]['sha256']!=old[ZIP]['sha256'],'A genuinely amended reviewed ZIP is required')
 return gate,b,meta,new

def common(d,b,meta,kit):
 kit.validate_record(d,KNOWN);need(d['submitted'] is False,'Published/non-false draft cannot be repaired');need(d.get('links',{}).get('bucket')==b['bucket'],'Bucket drift')
 remote=d.get('metadata');need(isinstance(remote,dict) and all(remote.get(k)==meta[k] for k in FIELDS),'Exact all-eleven current metadata required')
 files=kit.server_files(d);need(PDF in files,'Protected PDF absent');old=next(e for e in b['files'] if e['name']==PDF);need(kit.matching_file(files[PDF],old) and files[PDF].get('id')==old['id'],'Protected remote PDF drift')
 return files

def strict(d,meta,files,kit):
 changes=kit.verify(d,meta,files);need(changes==[],'Metadata normalization refused')
def old_state(d,b,meta,kit):
 files=common(d,b,meta,kit);strict(d,meta,b['files'],kit)
 for e in b['files']:need(files[e['name']].get('id')==e['id'],'Old staged file UUID differs')
 return files

def pdf_only(d,b,meta,kit):
 common(d,b,meta,kit);strict(d,meta,[next(e for e in b['files'] if e['name']==PDF)],kit)

def new_state(d,b,meta,new,kit):
 files=common(d,b,meta,kit);strict(d,meta,new,kit);canonical_uuid(files[ZIP].get('id'))

def intent_identity(g,b,new):
 return {'schema':'math-pr1262-known-draft-repair-intent-v1','id':KNOWN,'baseline_sha256':sha(A/'DRAFT_REPAIR_BASELINE.json'),'repair_helper_sha256':sha(Path(__file__).resolve()),'final_gate_sha256':sha(P/'FINAL_REVIEW_GATE.json'),'current_metadata_sha256':sha(P/'zenodo-deposit.json'),'old_zip':next(e for e in b['files'] if e['name']==ZIP),'new_zip':{k:next(e for e in new if e['name']==ZIP)[k] for k in ['name','size','md5','sha256']},'protected_pdf':next(e for e in b['files'] if e['name']==PDF),'bucket':b['bucket'],'policy':'One DELETE and at most one PUT in this invocation only; existing or uncertain attempts reconcile by GET, never retry mutations.'}

def record_stage(c,kit,d,b,meta,new):
 new_state(d,b,meta,new,kit)
 summary={'environment':'production','title':meta['title'],'files':[{'name':e['name'],'size':e['size'],'sha256':e['sha256']} for e in new],'metadata_normalizations':[],'id':KNOWN,'state':'ready_to_publish','verified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'repair_recovery':'Same known unpublished ID, unchanged PDF and exact reviewed new ZIP/all supplied metadata verified by actual strict kit.'}
 c.validate_summary(summary,kit,KNOWN,'ready_to_publish')
 if (P/'STAGE_RECEIPT.json').exists():c.validate_summary(read(P/'STAGE_RECEIPT.json'),kit,KNOWN,'ready_to_publish')
 else:save(P/'STAGE_RECEIPT.json',summary)
 return {'id':KNOWN,'status':'ready_to_publish','stage_receipt_written_or_verified':True,'no_publish_attempted':True}

def inspect_known(c,kit,client,g,b,meta,new):
 # No mutation, even if a prior DELETE/PUT did not reach the server.
 d=client.get(KNOWN);common(d,b,meta,kit)
 try:new_state(d,b,meta,new,kit)
 except (RuntimeError,kit.DepositError):
  result={'id':KNOWN,'status':'recovery_required','stage_receipt_written_or_verified':False,'read_only':True,'reason':'Known draft does not yet contain the exact new two-file package; no repair mutation retried.'}
 else:
  need(authenticate(c,kit)[0]==g,'Release changed during inspection');result=record_stage(c,kit,d,b,meta,new);result['read_only']=True
 save(P/'DRAFT_REPAIR_INSPECT.json',result);return result

def execute(action,kit=None,client=None):
 need(action in {'replace','inspect'},'Expected replace or inspect');c=coordinator();kit=c.load_exact_kit() if kit is None else c.install_exact_verifier(kit);g,b,meta,new=authenticate(c,kit)
 client=kit.ZenodoClient('production',kit.token_for('production')) if client is None else client
 identity=intent_identity(g,b,new);intent=P/'DRAFT_REPAIR_INTENT.json';upload=P/'DRAFT_REPAIR_UPLOAD_INTENT.json'
 if intent.exists():need(read(intent)==identity,'Prior repair intent differs; read-only manual reconciliation required')
 if upload.exists():need(intent.exists() and read(upload)==identity,'Upload intent differs or lacks repair intent')
 if action=='inspect' or intent.exists():return inspect_known(c,kit,client,g,b,meta,new)
 need(not upload.exists(),'Unexpected earlier upload attempt');d=client.get(KNOWN);common(d,b,meta,kit)
 try:new_state(d,b,meta,new,kit)
 except (RuntimeError,kit.DepositError):old_state(d,b,meta,kit)
 else:
  need(authenticate(c,kit)[0]==g,'Release changed during same-ID inspection');return record_stage(c,kit,d,b,meta,new)
 def guarded():
  need(authenticate(c,kit)[0]==g,'Current reviewed release drift');c.live_preflight();need(authenticate(c,kit)[0]==g,'Current release changed during live original PR/tracker preflight')
 guarded();d=client.get(KNOWN);old_state(d,b,meta,kit);need(authenticate(c,kit)[0]==g,'Reviewed release drift before DELETE');exclusive(intent,identity)
 oldzip=next(e for e in b['files'] if e['name']==ZIP);url='https://zenodo.org/api/deposit/depositions/'+str(KNOWN)+'/files/'+oldzip['id']
 try:client.request('DELETE',url)
 except kit.DepositError:
  # Documented 204-empty success is rejected by shared request's JSON contract.
  # Do not echo its text or assume success: a fresh exact GET is authoritative.
  pass
 # Any failed/unavailable read ends this invocation with its durable intent.
 # A later invocation is GET-only and cannot repeat DELETE or start another PUT.
 d=client.get(KNOWN);pdf_only(d,b,meta,kit);guarded();d=client.get(KNOWN);pdf_only(d,b,meta,kit);need(authenticate(c,kit)[0]==g,'Reviewed release drift before PUT');exclusive(upload,identity)
 try:client.upload(b['bucket'],next(e for e in new if e['name']==ZIP))
 except kit.DepositError:pass
 # Both a successful response and an uncertain PUT require same-ID fresh GET.
 # GET failure propagates without a stage receipt; inspect is the only recovery.
 return inspect_known(c,kit,client,g,b,meta,new)

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('action',choices=['replace','inspect']);args=parser.parse_args();print(json.dumps(execute(args.action),indent=2))
if __name__=='__main__':main()
