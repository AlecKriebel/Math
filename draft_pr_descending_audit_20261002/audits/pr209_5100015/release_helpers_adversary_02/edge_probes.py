"""Independent adapter/actual-package edge checks; no live provider access."""
import probes as H
import compact_fixtures
from pathlib import Path
import json,types,subprocess,sys,zipfile,io,copy,traceback
D,C,B,I,M,P,A,V=H.D,H.C,H.B,H.I,H.M,H.P,H.A,H.V
ROWS=[]
def check(name,fn,fixture):
 start=H.utc()
 try:result=fn();row=dict(name=name,start_utc=start,end_utc=H.utc(),PASS=True,result=result)
 except Exception as e:row=dict(name=name,start_utc=start,end_utc=H.utc(),PASS=False,error=repr(e),traceback=traceback.format_exc())
 ROWS.append(row);H.js(D/'EDGE_RESULTS.json',ROWS);print(json.dumps(row),flush=True)
 if (D/'fixtures'/fixture).exists():compact_fixtures.main([fixture])

def text_readers():
 r,pub,p=H.make_case('all_text_readers');ctx=B.context(r)
 def child(cmd,**kw):return H.REAL_RUN([H.PY,'-B','-c',"import os;os.write(1,b'prefix\\x00\\xffsuffix');os.write(2,b'error-stream')"],**kw)
 out={}
 V.subprocess=types.SimpleNamespace(run=child)
 folder=pub/'synthetic_inspect_failure';folder.mkdir()
 out['inspect_exception']=H.rejects(lambda:V.inspect_existing(r,ctx,p.id,folder))
 assert (folder/'inspect-stdout.json').read_bytes()==(folder/'inspect-stderr.txt').read_bytes()==b''
 P.subprocess=types.SimpleNamespace(run=child)
 out['publish_preflight_exception']=H.rejects(lambda:P.publish_once(r,pub,ROOT=pub.parent.parent))
 run=list((pub/'private_transport/zenodo_stage').iterdir())[0]
 assert (run/'PR-head-preflight-stdout.json').read_bytes()==(run/'PR-head-preflight-stderr.txt').read_bytes()==b''
 assert not (pub/'STAGE_ATTEMPT.json').exists()
 out.update(both_streams_lost_in_both_callers=True,real_local_child_stdout_hex=b'prefix\x00\xffsuffix'.hex(),real_local_child_stderr_hex=b'error-stream'.hex())
 H.js(pub.parent/'TEXT_READER_RESULT.json',out);return out

def log_dynamic_and_zip():
 r,pub,p=H.make_case('log_dynamic_zip');ctx=B.context(r);cpath=r/'FINAL_CLEARANCE.json';craw=cpath.read_bytes();mp=pub/'PUBLIC_EXPORT_MANIFEST.json';mraw=mp.read_bytes();manifest=json.loads(mraw)
 assert B.public_exports(r,pub,ctx)['preprint/manuscript.log']==(r/'manuscript.log').read_bytes()
 manifest['files']=[x for x in manifest['files'] if x['path']!='preprint/manuscript.log'];H.js(mp,manifest);c=json.loads(craw);c['public_export_manifest']=H.pin(mp,pub.parent);H.js(cpath,c)
 out=dict(unpinned_compiler_log=H.rejects(lambda:B.context(r),'Unexpected top-level release file'))
 H.put(mp,mraw);H.put(cpath,craw)
 dynamic=copy.deepcopy(ctx);dynamic['metadata'].update(version='1.1',publication_date='2026-10-17');row=B.expected_tracker_row(dynamic,dict(doi_url='https://doi.org/SYNTHETIC'))
 assert 'v1.1,2026-10-17' in row[3] and row[0]=='https://arxiv.org/abs/2004.12497v11';out['version_date_derived']=True
 source=I.frozen_source(r);assert len(source)==211
 zp=r/'k303b-source-verification.zip';original=zp.read_bytes()
 with zipfile.ZipFile(io.BytesIO(original)) as old:
  names=old.namelist();bodies={n:old.read(n) for n in names}
 with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as new:
  for name in names[:-1]:new.writestr(name,bodies[name])
 H.put(pub.parent/'MISSING_MEMBER_SOURCE_ZIP.zip',zp.read_bytes())
 out['zip_missing_member']=H.rejects(lambda:I.frozen_source(r),'Exact frozen ZIP set differs');H.put(zp,original)
 assert len(I.frozen_source(r))==211;out['actual_zip_exact_members']=211
 H.js(pub.parent/'LOG_DYNAMIC_ZIP_RESULTS.json',out);return out

def metadata_drift():
 r,pub,p=H.make_case('metadata_during_inspect')
 def mutate():
  q=json.loads((r/'metadata.json').read_bytes());q['version']='CHANGED-DURING-INSPECT';H.js(r/'metadata.json',q)
 p.mutate_on_live=mutate
 result=H.rejects(lambda:P.publish_once(r,pub,ROOT=pub.parent.parent),'metadata bytes changed')
 assert (pub/'STAGE_ATTEMPT.json').exists() and not (pub/'PUBLISH_ATTEMPT.json').exists()
 before=len([x for x in p.calls if x.get('provider')=='zenodo' and x.get('operation')in ['stage','publish']])
 H.rejects(lambda:P.publish_once(r,pub,ROOT=pub.parent.parent))
 after=len([x for x in p.calls if x.get('provider')=='zenodo' and x.get('operation')in ['stage','publish']]);assert before==after==1
 p.save('metadata_drift');return dict(drift_rejected=result,stage_writes=1,publish_writes=0)

if __name__=='__main__':
 check('real_binary_decode_loss_all_other_text_callers',text_readers,'all_text_readers')
 check('compiler_log_pin_dynamic_tracker_metadata_actual211zip',log_dynamic_and_zip,'log_dynamic_zip')
 check('metadata_drift_during_inspect_no_publication_or_second_stage',metadata_drift,'metadata_during_inspect')
 H.js(D/'EDGE_SUMMARY.json',dict(utc=H.utc(),groups=len(ROWS),passed=sum(x['PASS'] for x in ROWS),all_expected_outcomes=all(x['PASS'] for x in ROWS),synthetic_only=True,no_release_authority=True))
 sys.exit(0 if all(x['PASS'] for x in ROWS) else 1)
