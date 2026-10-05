"""Noncircular reviewer-only custody closure and actual after-freeze readback."""
from pathlib import Path
from datetime import datetime,timezone
import gzip,hashlib,json,os,stat,sys
HERE=Path(__file__).resolve().parent;F=HERE.parent/'preprint_package_v02'
def now():return datetime.now(timezone.utc).isoformat()
def digest(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=str(p.absolute()),bytes=len(b),sha256=digest(b),mode=stat.S_IMODE(p.stat().st_mode))
def write(p,d):Path(p).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def main():
 need(sys.flags.optimize==0,'Optimization must be disabled')
 need(not (HERE/'OUTPUT_MANIFEST.json').exists()and not(HERE/'CLOSURE_SEAL.json').exists(),'Already closed')
 verdict=json.loads((HERE/'VERDICT.json').read_text());need(not verdict['mandatory_unresolved_issues']and not verdict['new_nonmandatory_suggestions']and not verdict['publication_clearance'],'Verdict scope')
 final=json.loads((HERE/'process_evidence/final_evidence_authentication/execution.json').read_text());need(final['actual_child_PID']==67816 and final['exit_code']==0,'Final actual check not passed')
 for name in ['stdout','stderr']:
  row=final[name];b=gzip.decompress(Path(row['stored']['path']).read_bytes());need(len(b)==row['logical_bytes']and digest(b)==row['logical_sha256'],'Final native stream')
  if name=='stderr':need(not b,'Final check stderr')
 for row in final['sources_before']:
  b=gzip.decompress(Path(row['stored']['path']).read_bytes());need(b==Path(row['original']['path']).read_bytes()and len(b)==row['logical_bytes']and digest(b)==row['logical_sha256'],'Final check prelaunch source')
 source=pin(__file__);archive=HERE/'closure_executed_source.bin.gz';body=Path(__file__).read_bytes();archive.write_bytes(gzip.compress(body,mtime=0));need(gzip.decompress(archive.read_bytes())==body,'Closure full source copy')
 write(HERE/'CLOSURE_REQUEST.json',dict(actual_executing_PID=os.getpid(),requested_UTC=now(),argv=sys.argv,cwd=str(Path.cwd()),executed_source_before_freeze=source,retained_full_source=pin(archive),interpreter=pin(sys.executable),optimization=sys.flags.optimize,scope='Only this reviewer-owned namespace file/directory modes and custody files. No original/candidate/Git/PR/service mutation.',limits='Actual executing-process self-report; no future Popen completion or independently authenticated upstream/OS clock claimed. Final completed tool outcome and literal frozen readback are external to this sealed namespace.'))
 with (HERE/'RESEARCH_LOG.md').open('a')as out:
  out.write('\n'+now()+' — Independent whole-package review completed:100%. No unresolved or new optional issue; native final full evidence checker actual67816exit0 authenticated301source copies and complete earlier tapes without repeating scientific suites. Noncircular manifest and0444/0555 final-custody declarations now follow; actual after-freeze tool readback will be external to this log. Actual closing-process PID '+str(os.getpid())+'.\n')
 exclusions={'OUTPUT_MANIFEST.json','CLOSURE_SEAL.json'};rows=[];directories=[HERE]
 for p in sorted(HERE.rglob('*')):
  need(not p.is_symlink(),'Symlink in review namespace')
  if p.is_dir():directories.append(p)
  elif p.is_file():
   need(p.relative_to(HERE).as_posix()not in exclusions,'Unexpected old excluded file')
   row=pin(p);row.update(relative_path=p.relative_to(HERE).as_posix(),mode=0o444);rows.append(row)
  else:raise RuntimeError('Nonregular member '+str(p))
 directory_rows=[dict(path=str(p),relative_path='.'if p==HERE else p.relative_to(HERE).as_posix(),mode=0o555)for p in sorted(directories)]
 manifest=HERE/'OUTPUT_MANIFEST.json';write(manifest,dict(schema='full-literal-review-namespace-noncircular-v1',prepared_UTC=now(),actual_preparing_PID=os.getpid(),namespace=str(HERE),files=rows,directories=directory_rows,excluded_local_custody_files=sorted(exclusions),exclusion_reason='Manifest cannot noncircularly pin itself; seal pins the manifest and is excluded from its payload. External readback pins both.',final_file_mode=0o444,final_directory_mode=0o555,historical_mode_qualification='All older native receipts retain their actual prefreeze modes. The literal manifest declares and after-freeze readback verifies the later final custody epoch. This does not rewrite old source/stream pins.'))
 public=json.loads((F/'SECOND_CANDIDATE_MANIFEST.json').read_text());anchors=[pin(F/'SECOND_CANDIDATE_MANIFEST.json'),pin(HERE.parent/'snapshot_manifest.json'),*[pin(r['path'])for r in public['files']]]
 need(anchors[0]['sha256']=='b38a09c6768e11c2954892cdaa345a485557082c464d950f573a945f48b5ec71','Candidate changed')
 for r in public['files']:need(all(pin(r['path'])[k]==r[k]for k in ['bytes','sha256','mode']),'Public anchor differs')
 mp=pin(manifest);mp['mode']=0o444
 docpins=[]
 for n in ['REPORT.md','DERIVATION.md','READ_LEDGER.md','VERDICT.json','RESEARCH_LOG.md','PRESEAL_CHECK.json','SOURCE_ARCHIVE_INDEX.json']:
  r=pin(HERE/n);r['mode']=0o444;docpins.append(r)
 seal=HERE/'CLOSURE_SEAL.json';write(seal,dict(schema='review-custody-seal-v1',prepared_UTC=now(),actual_closing_PID=os.getpid(),status='FINAL_CUSTODY_DECLARATION_WITH_LITERAL_AFTER_FREEZE_READBACK_REQUIRED',review_complete_percent=100,mathematical_disposition=verdict['status'],mandatory_unresolved_issues=[],new_optional_issues=[],publication_clearance=False,merge_authority=False,manifest=mp,decisive_documents=docpins,manifest_payload_files=len(rows),literal_namespace_files=len(rows)+2,literal_namespace_directories=len(directory_rows),full_source_body_copies=301,actual_final_native_checker_PID=67816,actual_final_native_checker_exit=0,external_anchors=anchors,local_exclusions=sorted(exclusions),limits='This seal describes final declarations checked by the actual closing process after freezing. It does not record a future native completion. Final completed tool output and independent literal post-close readback are external anchors. File0444/directory0555 custody is read-only permissions, not an OS immutable flag, clock attestation, formal proof, exhaustive priority certificate, human referee report, or publication authority.'))
 for p in HERE.rglob('*'):
  if p.is_file():os.chmod(p,0o444)
 for p in sorted(directories,key=lambda p:len(p.parts),reverse=True):os.chmod(p,0o555)
 actual={p.relative_to(HERE).as_posix()for p in HERE.rglob('*')if p.is_file()};need(actual=={r['relative_path']for r in rows}|exclusions,'Frozen literal file set')
 for r in rows:need(pin(r['path'])==dict(path=r['path'],bytes=r['bytes'],sha256=r['sha256'],mode=r['mode']),'Frozen body differs')
 for r in directory_rows:need(stat.S_IMODE(Path(r['path']).stat().st_mode)==r['mode'],'Frozen directory differs')
 need(pin(manifest)==mp,'Frozen manifest differs');need(all(stat.S_IMODE(p.stat().st_mode)==0o444 for p in HERE.rglob('*')if p.is_file()),'Final modes')
 stored=sum(p.stat().st_size for p in HERE.rglob('*')if p.is_file());physical=sum(p.stat().st_blocks*512 for p in HERE.rglob('*'))+HERE.stat().st_blocks*512
 need(stored<20_000_000 and physical<20_000_000,'Own namespace exceeds20MB')
 for r in anchors:need(pin(r['path'])==r,'External input changed')
 print(json.dumps(dict(status='PASS_ACTUAL_CLOSED_LITERAL_READBACK',completed_readback_UTC=now(),actual_closing_PID=os.getpid(),manifest=pin(manifest),seal=pin(seal),decisive_documents=docpins,files=len(actual),directories=len(directory_rows),stored_bytes=stored,physical_bytes=physical,all_files_mode='0444',all_directories_mode='0555',candidate_23_public_files_unchanged=True,source_body_copies=301,publication_clearance=False)))
if __name__=='__main__':main()
