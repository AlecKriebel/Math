"""Full-byte source/provenance/build and revised-package reconciliation."""
from pathlib import Path
from datetime import datetime
import difflib,gzip,hashlib,json,os,stat
from capture import HERE,pin,write,digest,now
R=Path('/Users/alec/Documents/Math');A=HERE.parent;F=A/'preprint_package_v02';F1=A/'preprint_package_v01'
checked=[]
def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def check_pin(row,mode=True):
 p=Path(row['path']);need(p.is_file() and not p.is_symlink(),'Nonregular '+str(p));got=pin(p)
 need(all(got[k]==row[k] for k in (('bytes','sha256','mode') if mode else ('bytes','sha256'))),'Pin differs '+str(p));checked.append(got);return p
def stream(row):
 p=check_pin(row['stored']);b=gzip.decompress(p.read_bytes());need(len(b)==row['logical_bytes'] and digest(b)==row['logical_sha256'],'Logical stream differs');return b
def main():
 originals=json.loads((A/'snapshot_manifest.json').read_text())
 need(originals['head']=='eb6e0e999521d84a65f9857d338cad76b84d30db' and originals['original_submitted_status']=='claimed_solved' and originals['original_author_turn_count']=='2/5','Original head/status mismatch')
 need(len(originals['files'])==29,'Original29 count')
 for row in originals['files']:
  p=A/'snapshot'/row['path'];b=p.read_bytes();got=pin(p)
  need(len(b)==row['bytes'] and digest(b)==row['sha256'] and got['mode']==0o444,'Original snapshot differs')
  need(hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()==row['git_blob_sha'],'Original full Git blob differs');checked.append(got)
 need(originals['original_target_row'] in (A/'snapshot/unsolved_math_prioritization/QUEUE.md').read_text(),'Original queue literal row differs')
 prov=json.loads((F/'PAYLOAD_PROVENANCE.json').read_text());expected=json.loads((F/'EXPECTED_SCIENTIFIC_OUTPUTS.json').read_text());case_list=json.loads((F/'CONTROL_CASES.json').read_text());cases={c['source']:c for c in case_list}
 controls=0;notes=0
 for row in prov['payload_sources']:
  old=R/row['original_source'];public=F/row['package_path'];before=old.read_bytes();after=public.read_bytes();checked.extend([pin(old),pin(public)])
  if row['package_path'].startswith('controls/'):
   need(before==after and len(before)==row['bytes'] and digest(before)==row['sha256'] and row['program_body_unchanged'],'Program provenance differs')
   baseline=R/row['historical_expected_output'];body=baseline.read_bytes();need(len(body)==row['baseline_bytes'] and digest(body)==row['baseline_sha256'],'Historical expected output differs')
   historical=json.loads(body);case=cases[row['package_path']];need(row['portable_comparison_fields']==case['scientific_fields'],'Selected provenance fields differ')
   need({k:historical[k] for k in case['scientific_fields']}==expected[case['label']],'Expected fields not actual historical values');checked.append(pin(baseline));controls+=1
  else:
   need(len(before)==row['original_bytes'] and digest(before)==row['original_sha256'] and len(after)==row['public_bytes'] and digest(after)==row['public_sha256'],'Note provenance differs')
   diff=''.join(difflib.unified_diff(before.decode().splitlines(keepends=True),after.decode().splitlines(keepends=True),fromfile=row['original_source'],tofile=row['package_path']))
   need(diff==row['wording_diff'],'Complete note diff differs');notes+=1
 need(controls==8 and notes==2,'Provenance counts')
 archive=json.loads((A/'frozen_first_preprint_candidate/ARCHIVE_MANIFEST.json').read_text());check_pin(archive['actual_archived_manifest'])
 oldfirst=json.loads(Path(archive['actual_archived_manifest']['path']).read_text());need(len(archive['files'])==len(oldfirst['files'])==23,'First archive count')
 archived={}
 for row in archive['files']:
  p=check_pin(row['actual_byte_identical_archive']);need(all(row['actual_original_input'][k]==row['actual_byte_identical_archive'][k] for k in ('bytes','sha256','mode')),'First archive not literal original');archived[Path(row['actual_original_input']['path']).relative_to(F1).as_posix()]=p
 for row in oldfirst['files']:
  rel=Path(row['path']).relative_to(F1).as_posix();need(all(pin(archived[rel])[k]==row[k] for k in ('bytes','sha256','mode')),'First original-to-archive binding')
 changed=[]
 for rel,p in archived.items():
  if (F/rel).read_bytes()!=p.read_bytes():changed.append(rel)
 need(set(changed)=={'README.md','SOURCE_EDITIONS.md','classical_regularization_application.md','independent_classical_derivation.md','spectral_tensor_consistency.tex','PAYLOAD_PROVENANCE.json','MANIFEST.json','spectral_tensor_consistency.pdf','spectral_tensor_verification.zip'},'Unexpected candidate change set')
 recon=json.loads((F1/'AUTHORING_PATH_RECONCILIATION_02.json').read_text());author=check_pin(recon['current_authoring_source']);need(author.read_bytes()==(F/'spectral_tensor_consistency.tex').read_bytes(),'Same-editor authoring source differs')
 td=''.join(difflib.unified_diff(archived['spectral_tensor_consistency.tex'].read_text().splitlines(keepends=True),author.read_text().splitlines(keepends=True),fromfile='first-candidate.tex',tofile='repaired-authoring-source.tex'));need(td==recon['exact_TeX_diff'],'Authoring exact diff differs')
 repairs=json.loads((F/'GLOBAL_REPAIR_RECEIPT.json').read_text());check_pin(repairs['first_review_adjudication']);check_pin(repairs['first_candidate_full_archive']);check_pin(repairs['authoring_path_reconciliation'])
 need(repairs['unchanged_metadata'] and repairs['unchanged_all8_control_sources_and_expected_scientific_outputs'],'Repair unchanged declarations')
 text=(F/'spectral_tensor_consistency.tex').read_text();ind=(F/'independent_classical_derivation.md').read_text();cl=(F/'classical_regularization_application.md').read_text();ed=(F/'SOURCE_EDITIONS.md').read_text()
 need('Set $K_h(x,z)=0$ for $z\\in\\partial D$.' in text and '\\Prob(Y_i\\in\\partial D)=0' in text,'C3 missing')
 need('CRITERIA.md' not in ind and 'bundled classical_regularization_application.md' in ind,'C1 missing')
 need('0<eta<min{1,s-d/2-2}' in ind,'C4 missing')
 need(all('10.1017/S0266466608080304' in x and 'Uniform convergence rates for kernel estimation with dependent data' in x for x in (cl,ed)),'C2 missing')
 editor=json.loads((F/'ROOT_NATIVE_EDITOR_COMPILE_ACCEPTANCE.json').read_text());check_pin(editor['compiled_authoring_source']);check_pin(editor['unchanged_authoring_source_after_actual_tool']);need(editor['actual_tool_result_status']=='success' and not editor['actual_tool_result']['isError'],'Native editor compile status')
 build=json.loads((F/'BUILD_RECEIPT.json').read_text());need(build['page_count']==len(build['pages'])==8,'PDF pages');check_pin(build['PDF'],mode=False);check_pin(build['source'],mode=False);check_pin(build['same_editor_authoring_source']);check_pin(build['native_editor_compile_receipt'])
 native=[]
 for run in build['actual_native_processes']:
  need(run['exit_code']==0 and run['optimization']==0,'Build failure/optimization')
  need(datetime.fromisoformat(run['requested_UTC'])<=datetime.fromisoformat(run['started_UTC'])<=datetime.fromisoformat(run['completed_UTC']),'Build time order')
  for key in ('executed_recorder_source','recorder_interpreter','child_binary','manuscript','retained_full_source','retained_full_manuscript'):check_pin(run[key])
  need(Path(run['executed_recorder_source']['path']).read_bytes()==Path(run['retained_full_source']['path']).read_bytes(),'Build source archive')
  need(Path(run['manuscript']['path']).read_bytes()==Path(run['retained_full_manuscript']['path']).read_bytes(),'Build manuscript archive')
  output=stream(run['stdout']);err=stream(run['stderr']);native.append(dict(PID=run['actual_PID'],argv=run['argv'],cwd=run['cwd'],UTC_interval=[run['started_UTC'],run['completed_UTC']],stdout_bytes=len(output),stderr_bytes=len(err)))
 for row in build['pages']:check_pin(row)
 need(Path(build['actual_native_processes'][1]['argv'][1]).read_bytes()==(F/'spectral_tensor_consistency.pdf').read_bytes(),'Exported/public PDF differs')
 need((F/'private_build_01/full_pdf_text.txt').read_bytes()==(HERE/'rendered_note.txt').read_bytes(),'Fresh/public-build PDF extraction differs')
 local=json.loads((F/'private_local_deposit_check/execution.json').read_text());need(local['exit_code']==0 and local['actual_PID']==41184,'Local check actual status');check_pin(local['resolved_executable'])
 for row in local['full_prelaunch_sources']:
  historical_frozen_helper=Path(row['input']['path']).name=='close_second_candidate.py'
  check_pin(row['input'],mode=not historical_frozen_helper);check_pin(row['full_prelaunch_copy'])
  if historical_frozen_helper:need(pin(row['input']['path'])['mode']==0o444 and row['input']['mode']==0o644,'Explicit historical failed-helper freeze mode')
  need(Path(row['input']['path']).read_bytes()==Path(row['full_prelaunch_copy']['path']).read_bytes(),'Local check full prelaunch source')
 stream(local['stdout']);need(not stream(local['stderr']),'Local check stderr')
 first_verdict=json.loads((A/'preprint_adversary_01/VERDICT.json').read_text());need(not first_verdict['mandatory_unresolved_issues'] and {i['id'] for i in first_verdict['nonmandatory_suggestions']}=={'C1','C2','C3','C4'},'First review reconciliation differs')
 adjudication=json.loads((A/'ROOT_FIRST_PREPRINT_REVIEW_ADJUDICATION.json').read_text());need(adjudication['status']=='PASS_FIRST_WHOLE_PACKAGE_REVIEW_FOR_LISTED_GLOBAL_REPAIRS' and adjudication['ROOT_accepts_mathematics'] and not adjudication['publication_clearance'],'First acceptance scope')
 for row in adjudication['exact_frozen_namespace_files']:check_pin(row)
 write(HERE/'EVIDENCE_CROSSCHECK.json',dict(status='PASS_FULL_ORIGINAL_BLOBS_PROVENANCE_BUILD_ARCHIVE_AND_FOUR_GLOBAL_REPAIRS',UTC=now(),actual_recorder_PID=os.getpid(),executed_source=pin(__file__),original_blobs=29,unchanged_control_programs=controls,complete_note_diffs=notes,first_archived_public_files=23,revised_changed_public_files=sorted(changed),all_four_minor_repairs_verified=True,native_build_readbacks=native,reused_visual_pages=build['pages'],ROOT_first_review_acceptance_read_extent='Scalar decision/scope and programmatic entire literal pin inventory; not a claim to manually read all161675 bytes or all prior raw tape content.',first_review_payload_fullpins=len(adjudication['exact_frozen_namespace_files']),full_byte_checked_pins=checked,mode_qualification='Public second-candidate TeX/PDF build pins are historical0644, now exactly0444 in the frozen candidate manifest. First-candidate original author path intentionally repaired only after literal archive; old body authenticated at its actual archive. Other compared pins match current modes.',candidate_modified=False,publication_clearance=False))
 print(json.dumps(dict(status='PASS',actual_recorder_PID=os.getpid(),checked_pins=len(checked),changed_files=sorted(changed),actual_build_PIDs=[r['PID'] for r in native])))
if __name__=='__main__':main()
