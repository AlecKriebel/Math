"""Independent revised-package authentication, safe fresh ZIP replay and PDF extraction."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import gzip, hashlib, json, os, shutil, stat, sys, zipfile
from capture import capture, pin, write, now, digest, HERE
F=HERE.parent/'preprint_package_v02'
EXPECTED='b38a09c6768e11c2954892cdaa345a485557082c464d950f573a945f48b5ec71'
def need(ok,why):
 if not ok: raise RuntimeError(why)
def main():
 need(sys.flags.optimize==0,'Optimization must be disabled')
 manifest=F/'SECOND_CANDIDATE_MANIFEST.json'; need(pin(manifest)['sha256']==EXPECTED,'Candidate manifest differs')
 doc=json.loads(manifest.read_text()); rows=doc['files'];need(len(rows)==23,'Wrong public file count')
 for row in rows:
  p=Path(row['path']);need(p.is_file() and not p.is_symlink(),'Nonregular public file')
  actual=pin(p);need(all(actual[k]==row[k] for k in ('bytes','sha256','mode')),'Frozen public file differs '+str(p))
  need(actual['mode']==0o444,'Public body not frozen')
 outer=pin(F/'spectral_tensor_verification.zip'); inner=json.loads((F/'MANIFEST.json').read_text()); payload=inner['payload']
 need(len(payload)==19 and len({r['path'] for r in payload})==19,'Invalid payload declaration')
 unpack=HERE/'fresh_unpacked';unpack.mkdir(exist_ok=False)
 members=[]
 with zipfile.ZipFile(F/'spectral_tensor_verification.zip') as archive:
  infos=archive.infolist();need(len(infos)==20 and len({i.filename for i in infos})==20,'ZIP count/uniqueness')
  expected={r['path'] for r in payload}|{'MANIFEST.json'}
  actual_names=set()
  for info in infos:
   rel=PurePosixPath(info.filename);need(not rel.is_absolute() and '..' not in rel.parts and rel.parts[0]=='spectral-tensor-consistency','Unsafe ZIP path')
   need(not info.is_dir() and (info.external_attr>>16)==0o100644,'ZIP nonregular/mode mismatch')
   local=PurePosixPath(*rel.parts[1:]);actual_names.add(str(local))
   b=archive.read(info);p=unpack/Path(*rel.parts);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b);os.chmod(p,0o644)
   need(b==(F/Path(*local.parts)).read_bytes(),'Outer/package ZIP bytes differ '+str(local))
   members.append(dict(member=info.filename,bytes=len(b),sha256=digest(b),archive_mode=info.external_attr>>16,unpacked=pin(p)))
  need(actual_names==expected,'Undeclared or missing ZIP member')
 bundle=unpack/'spectral-tensor-consistency'
 for row in payload:
  actual=pin(bundle/row['path']);need(all(actual[k]==row[k] for k in ('bytes','sha256')),'ZIP payload differs')
 metadata=json.loads((F/'record_metadata.json').read_text());wrapper=json.loads((F/'zenodo-deposit.json').read_text())
 need(wrapper['metadata']==metadata and json.loads((bundle/'record_metadata.json').read_text())==metadata,'Metadata mismatch')
 sources=[Path(__file__),F/'SECOND_CANDIDATE_MANIFEST.json',F/'spectral_tensor_verification.zip',*[bundle/i['path'] for i in payload],bundle/'MANIFEST.json']
 python=Path('/Users/alec/Documents/Math/.venv/bin/python')
 result,out,err=capture('fresh_portable_replay',[str(python),'-E','-B',str(bundle/'verify_package.py'),'--output',str(HERE/'fresh_replay')],bundle,sources)
 need(result['exit_code']==0 and not err,'Actual portable runner failed')
 receipt=json.loads((HERE/'fresh_replay/REPLAY_RECEIPT.json').read_text());need(receipt['actual_launcher_PID']==result['actual_child_PID'],'Runner actual PID mismatch')
 exact=0;float_count=0;expected_values=json.loads((bundle/'EXPECTED_SCIENTIFIC_OUTPUTS.json').read_text())
 def independent_compare(a,b):
  nonlocal exact,float_count
  if isinstance(b,dict):
   need(type(a) is dict and a.keys()==b.keys(),'Scientific dict mismatch')
   for k in b: independent_compare(a[k],b[k])
  elif isinstance(b,list):
   need(type(a) is list and len(a)==len(b),'Scientific list mismatch')
   for x,y in zip(a,b): independent_compare(x,y)
  elif type(b) is float:
   import math
   need(type(a) in (float,int) and math.isfinite(a) and math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-14),'Scientific float mismatch');float_count+=1
  else: need(type(a) is type(b) and a==b,'Scientific exact mismatch');exact+=1
 for entry in receipt['native_executions']:
  run=entry['native_execution'];need(run['exit_code']==0,'Control exit')
  need(run['actual_launcher_PID']==result['actual_child_PID'],'Control parent PID')
  for name in ('stdout','stderr'):
   s=run[name];p=Path(s['stored']['path']);need(all(pin(p)[k]==s['stored'][k] for k in ('bytes','sha256','mode')),'Child stored stream differs')
   body=gzip.decompress(p.read_bytes());need(len(body)==s['logical_bytes'] and digest(body)==s['logical_sha256'],'Child logical stream differs')
   if name=='stderr':need(not body,'Child stderr nonempty')
  for key in ('source','original_source','runner_source'):
   need(all(pin(run[key]['path'])[k]==run[key][k] for k in ('bytes','sha256','mode')),'Child source differs')
  independent_compare(json.loads(Path(entry['scientific_output']['path']).read_text()),expected_values[entry['label']])
  need(datetime.fromisoformat(run['started_UTC'])<=datetime.fromisoformat(run['completed_UTC']),'Child time order')
 need(len(receipt['native_executions'])==8,'Not eight actual child suites')
 for row in members:need(pin(row['unpacked']['path'])==row['unpacked'],'Runner changed an unpacked member')
 extractor=shutil.which('pdftotext');need(extractor is not None,'No PDF extractor')
 p_result,p_out,p_err=capture('pdf_text',[extractor,'-layout',str(F/'spectral_tensor_consistency.pdf'),str(HERE/'rendered_note.txt')],HERE,[Path(__file__),F/'spectral_tensor_consistency.pdf',Path(extractor)])
 need(p_result['exit_code']==0 and not p_err,'Actual PDF extraction failed')
 for row in rows:need(all(pin(row['path'])[k]==row[k] for k in ('bytes','sha256','mode')),'Public candidate changed during readback')
 write(HERE/'AUTHENTICATION_AND_REPLAY.json',dict(status='PASS_SECOND_CANDIDATE_23_PUBLIC_FILES_SAFE_20_MEMBER_ZIP_EIGHT_ACTUAL_SUITES',UTC=now(),actual_recorder_PID=os.getpid(),executed_source=pin(__file__),manifest=pin(manifest),public_files=rows,members=members,metadata_identical=True,actual_runner_execution=result,actual_runner_receipt=pin(HERE/'fresh_replay/REPLAY_RECEIPT.json'),independently_compared_exact_leaves=exact,floating_diagnostic_leaves=float_count,PDF_extraction=p_result,extracted_PDF_text=pin(HERE/'rendered_note.txt'),limits='Finite controls and byte/custody authentication do not prove the infinite theorem, certify literature absence or confer publication authority.'))
 (HERE/'RESEARCH_LOG.md').write_text('# PR302 revised whole-package adversarial review\n\n'+now()+' — Initial literal authentication and actual freshly unpacked portable replay PASS. Mathematical/source review continues independently of earlier verdicts. Estimated review completion 25%. Actual recorder PID '+str(os.getpid())+'.\n\nThe preliminary file-locator tool returned exit2 solely for a guessed nonexistent priority_auxiliary_adversary_01 directory; extant target/mechanism sources were returned. No guessed native PID or candidate/scientific failure is attributed to that locator.\n')
 print(json.dumps(dict(status='PASS',actual_recorder_PID=os.getpid(),runner_PID=result['actual_child_PID'],child_PIDs=[e['native_execution']['actual_child_PID'] for e in receipt['native_executions']],exact_leaves=exact,floating_leaves=float_count,PDF_extractor_PID=p_result['actual_child_PID'])))
if __name__=='__main__': main()
