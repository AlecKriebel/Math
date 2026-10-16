"""Actual post-whole03 terminal/physical-alias/custody controls; no compiler or service."""
from pathlib import Path
import datetime,hashlib,io,json,os,shutil,subprocess,sys,tempfile,zipfile
from contextlib import contextmanager
F=Path(__file__).resolve().parent;A=F.parents[1];K=A/'preprint_v1_0';REPO=A.parents[2]
ARCHIVE='pr1085_support_v1_0.zip';records=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def need(ok,msg):
 if not ok:raise ValueError(msg)
def dump(p,o):p.write_text(json.dumps(o,indent=2)+'\n')
def identities(root):
 return {str(p.relative_to(root)):(len(p.read_bytes()),sha(p.read_bytes())) for p in root.rglob('*') if p.is_file()}
def run(cwd,argv,label,good=True,message=None,env=None):
 p=subprocess.run(argv,cwd=cwd,capture_output=True,text=True,env=env)
 records.append({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'label':label,'cwd':str(cwd),'argv':argv,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
 dump(F/'CONTROL_RECEIPTS.json',{'scope':'Actual final-byte post-whole03 commands and complete process outputs. Disposable copies only; no actual compile/render/service.','commands':records})
 need((p.returncode==0)==good,label+' wrong exit: '+p.stdout+p.stderr)
 if message:need(message in p.stderr,label+' wrong guard: '+p.stderr)
 return p
cleanup=[]
def scratch_pins(root):
 rows=[]
 for p in sorted(root.rglob('*')):
  if p.is_symlink():rows.append({'path':str(p.relative_to(F/'scratch')),'symlink_target':os.readlink(p)})
  elif p.is_file():
   b=p.read_bytes();rows.append({'path':str(p.relative_to(F/'scratch')),'bytes':len(b),'sha256':sha(b)})
 return rows
def freeze_cleanup(root,label):
 rows=scratch_pins(root)
 for row in rows:
  p=F/'scratch'/row['path']
  if 'symlink_target' in row:need(p.is_symlink() and os.readlink(p)==row['symlink_target'],'scratch link changed')
  else:
   b=p.read_bytes();need(len(b)==row['bytes'] and sha(b)==row['sha256'],'scratch changed before cleanup')
 cleanup.append({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'root':str(root.relative_to(F)),'label':label,'rechecked_before_deletion':True,'files':rows})
 dump(F/'OWN_SCRATCH_CLEANUP_LEDGER.json',{'scope':'Only this effort owned scratch; each listed tree is individually hashed/rechecked immediately before its controlled cleanup. Canonical/other-worker inputs never removed.','events':cleanup})
@contextmanager
def owned_temp():
 base=F/'scratch';base.mkdir(exist_ok=True)
 temp=Path(tempfile.mkdtemp(prefix='terminal-controls-',dir=base))
 try:yield str(temp)
 finally:
  freeze_cleanup(temp,'final owned scratch cleanup');shutil.rmtree(temp)
def remove_tree(path):
 freeze_cleanup(path,'owned derivative subtree cleanup');shutil.rmtree(path)
def main():
 body=(K/ARCHIVE).read_bytes();baseline=identities(K)
 with zipfile.ZipFile(io.BytesIO(body)) as z:
  names=z.namelist();need(names==sorted(set(names)) and z.testzip() is None,'closed order/CRC')
  payload={i.filename:z.read(i) for i in z.infolist()}
  for i in z.infolist():
   need(i.date_time==(2026,10,14,0,0,0) and i.create_system==3 and i.external_attr==0o100644<<16 and i.compress_type==zipfile.ZIP_DEFLATED and i.flag_bits==0 and i.extra==i.comment==b'','ZIP header')
   need(payload[i.filename]==(K/i.filename).read_bytes(),'ZIP payload')
 independent=io.BytesIO()
 with zipfile.ZipFile(independent,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for n in names:
   i=zipfile.ZipInfo(n,(2026,10,14,0,0,0));i.create_system=3;i.external_attr=0o100644<<16;i.compress_type=zipfile.ZIP_DEFLATED;z.writestr(i,payload[n],compresslevel=9)
 need(independent.getvalue()==body,'independent CLOSED deflate9 mismatch')
 physical=[];aliases=[];semantic=[];mode_results=[]
 with owned_temp() as td:
  temp=Path(td);root=temp/'kit';root.mkdir()
  def fresh(full=False):
   freeze_cleanup(root,'controlled disposable-kit reset')
   for p in sorted(root.rglob('*'),key=lambda p:len(p.parts),reverse=True):
    if p.is_symlink() or p.is_file():p.unlink()
    elif p.is_dir():p.rmdir()
   for n,b in payload.items():
    p=root/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
   if full:
    (root/ARCHIVE).write_bytes(body)
    for n in ['zenodo-deposit.json','UPLOAD_BINDINGS.json']:(root/n).write_bytes((K/n).read_bytes())
  def repin():
   p=root/'SUPPORT_MANIFEST.json';o=json.loads(p.read_text())
   for row in o['files']:
    b=(root/row['path']).read_bytes();row['bytes']=len(b);row['sha256']=sha(b)
   dump(p,o)
  def change(n,key,value):
   p=root/n;o=json.loads(p.read_text());o[key]=value;dump(p,o);repin()
  writers=[('verify_package.py','--output'),('check_math.py','--output'),('build_archive.py','--output'),('build_pdf.py','--out-dir')]
  for mode in [[],['-O']]:
   label='optimized' if mode else 'normal';prefix=[sys.executable,'-B',*mode]
   fresh();start=identities(root)
   default=json.loads(run(root,prefix+['verify_package.py'],label+' clean verifier').stdout)
   math=json.loads(run(root,prefix+['check_math.py'],label+' full JSON math').stdout)
   out=temp/('rebuilt_'+label+'.zip');run(root,prefix+['build_archive.py','--output',str(out)],label+' actual archive')
   need(out.read_bytes()==body,'actual archive mismatch');out.unlink()
   run(root,prefix+['verify_package.py'],label+' post-build verifier')
   need(start==identities(root),'clean entrypoints changed kit')
   need(not default['external_deposit_binding_verified'] and not default['new_complete_whole03_required'] and default['new_complete_whole03_completed'] and default['new_whole_reviews']==3 and default['root_terminal_integrity_adoption_required'] and not default['root_terminal_integrity_adopted'],'current default semantics')
   run(root,prefix+['verify_package.py','--require-deposit'],label+' required missing descriptor',False,'regular input required')
   fresh(True);strict=json.loads(run(root,prefix+['verify_package.py','--require-deposit'],label+' strict native binding').stdout)
   need(strict['archive_verified'] and strict['external_deposit_binding_verified'],'strict binding incomplete')
   (root/'UPLOAD_BINDINGS.json').unlink();run(root,prefix+['verify_package.py','--require-deposit'],label+' required missing binding',False,'regular input required')
   fresh(True);o=json.loads((root/'UPLOAD_BINDINGS.json').read_text());o['files'][1]['sha256']='0'*64;dump(root/'UPLOAD_BINDINGS.json',o)
   run(root,prefix+['verify_package.py','--require-deposit'],label+' corrupt archive binding',False,'exact attachment binding')
   fresh(True);descriptor=root/'zenodo-deposit.json';saved=descriptor.read_bytes();descriptor.unlink();descriptor.symlink_to(temp/'absent_descriptor')
   run(root,prefix+['verify_package.py'],label+' dangling optional descriptor',False,'symlink input or ancestor')
   fresh(True);descriptor=root/'zenodo-deposit.json';saved=descriptor.read_bytes();other=temp/(label+'_descriptor_body');other.write_bytes(saved);descriptor.unlink();descriptor.symlink_to(other)
   run(root,prefix+['verify_package.py'],label+' identical symlink descriptor',False,'symlink input or ancestor');other.unlink()
   faults=[('schema',True,'case repair schema'),('pr',1086,'case repair identity'),('problem_id',True,'case repair identity'),('status','CLEARED','case repair pending stage'),('finding','NONE','case repair pending stage'),('historical_whole_reviews_completed',1,'case repair two historical reviews'),('minimum_whole_reviews',0,'case repair two historical reviews'),('new_complete_whole03_required',False,'case repair required review/adoption/history'),('root_repair_adoption_required',False,'case repair required review/adoption/history'),('historical_STATUS_and_TERMINAL_ACCOUNTING_preserved',False,'case repair required review/adoption/history'),('new_complete_whole03_completed',True,'case repair forbidden promotion'),('publication_ready',True,'case repair forbidden promotion'),('all_actionable_issues_resolved',True,'case repair forbidden promotion'),('published',True,'case repair forbidden promotion'),('human_peer_review',True,'case repair forbidden promotion'),('formal_proof_certificate',True,'case repair forbidden promotion'),('services_hold','none','case repair ordered hold'),('priority','CLEARED','case repair historical scope'),('novelty','NEW','case repair historical scope'),('worldwide_open_status','OPEN','case repair historical scope'),('independent_discovery','YES','case repair historical scope'),('paper_pdf_sha256','0'*64,'case repair unchanged paper')]
   for key,value,message in faults:
    fresh();change('CASE_ALIAS_REPAIR_ACCOUNTING.json',key,value)
    p=run(root,prefix+['verify_package.py'],label+' coherent repair fault '+key,False,message)
    semantic.append({'mode':label,'case':key,'reached_guard':message,'returncode':p.returncode,'outer_manifest_refreshed':True})
   for kind in ['membership','bytes']:
    fresh();p=root/'CASE_ALIAS_REPAIR_COPY_MAP.json';o=json.loads(p.read_text())
    if kind=='membership':o['files'].pop();message='case repair exact evidence membership'
    else:o['files'][0]['sha256']='0'*64;message='case repair copied bytes'
    dump(p,o);repin();run(root,prefix+['verify_package.py'],label+' corrupt repair map '+kind,False,message)
   fresh();name='evidence/case_alias01/ROOT_TERMINAL_ADMIN_REVIEW_20261016.json';p=root/name;o=json.loads(p.read_text());o['new_complete_whole03_required']=False;dump(p,o)
   m=root/'CASE_ALIAS_REPAIR_COPY_MAP.json';o=json.loads(m.read_text());r=next(r for r in o['files'] if r['copy']==name);b=p.read_bytes();r['bytes']=len(b);r['sha256']=sha(b);dump(m,o);repin()
   run(root,prefix+['verify_package.py'],label+' coherent copied root hold fault',False,'case repair root hold evidence')
   current_name='CURRENT_TERMINAL_ACCOUNTING_20261016.json'
   current_faults=[('schema',True,'current terminal schema'),('pr',1086,'current terminal identity'),('problem_id',True,'current terminal identity'),('status','READY','current terminal stage'),('whole_reviews_completed',2,'current terminal review count'),('minimum_whole_reviews',3,'current terminal review count'),('latest_complete_whole_review',2,'current terminal review count'),('latest_actionable_P0_P1_P2_P3',1,'current terminal review count'),('case_alias_repair_root_adopted',False,'current terminal required adoption/history'),('latest_complete_whole_review_root_adopted',False,'current terminal required adoption/history'),('new_complete_whole03_completed',False,'current terminal required adoption/history'),('root_terminal_integrity_adoption_required',False,'current terminal required adoption/history'),('historical_STATUS_TERMINAL_ACCOUNTING_CASE_REPAIR_preserved',False,'current terminal required adoption/history'),('new_complete_whole03_required',True,'current terminal forbidden promotion/stale hold'),('further_complete_whole_review_currently_required',True,'current terminal forbidden promotion/stale hold'),('root_terminal_integrity_adopted',True,'current terminal forbidden promotion/stale hold'),('publication_ready',True,'current terminal forbidden promotion/stale hold'),('all_actionable_issues_resolved',True,'current terminal forbidden promotion/stale hold'),('issues_resolved',True,'current terminal forbidden promotion/stale hold'),('published',True,'current terminal forbidden promotion/stale hold'),('human_peer_review',True,'current terminal forbidden promotion/stale hold'),('formal_proof_certificate',True,'current terminal forbidden promotion/stale hold'),('services_hold','none','current terminal ordered hold'),('priority','CLEARED','current terminal historical scope'),('novelty','NEW','current terminal historical scope'),('worldwide_open_status','OPEN','current terminal historical scope'),('independent_discovery','YES','current terminal historical scope'),('paper_pdf_sha256','0'*64,'current terminal unchanged paper'),('latest_review_prefix','elsewhere/','current terminal exact evidence interfaces')]
   for key,value,message in current_faults:
    fresh();change(current_name,key,value)
    p=run(root,prefix+['verify_package.py'],label+' coherent current fault '+key,False,message)
    semantic.append({'mode':label,'case':'current '+key,'reached_guard':message,'returncode':p.returncode,'outer_manifest_refreshed':True})
   current_prefix='evidence/terminal_after_whole03/';review_prefix=current_prefix+'reviews/package_03/'
   cmap='CURRENT_TERMINAL_COPY_MAP_20261016.json'
   def coherent_evidence(name,key,value,kind):
    p=root/name;o=json.loads(p.read_text());o[key]=value;dump(p,o)
    if kind=='review_output':
     op=root/(review_prefix+'OUTPUT_PINS.json');oo=json.loads(op.read_text());r=next(r for r in oo['files'] if r['path']==Path(name).name);b=p.read_bytes();r['bytes']=len(b);r['sha256']=sha(b);dump(op,oo)
     sp=root/(review_prefix+'SEAL.json');so=json.loads(sp.read_text());so['output_pins_bytes']=op.stat().st_size;so['output_pins_sha256']=sha(op.read_bytes())
     if Path(name).name=='VERDICT.json':so['verdict_sha256']=sha(p.read_bytes())
     if Path(name).name=='INDEPENDENT_DERIVATION.md':raise ValueError('use JSON only')
     dump(sp,so)
     ap=root/(current_prefix+'ROOT_WHOLE_PACKAGE_REVIEW_03.json');ao=json.loads(ap.read_text());ao['output_pins_sha256']=so['output_pins_sha256'];dump(ap,ao)
    mp=root/cmap;mo=json.loads(mp.read_text())
    for r in mo['files']:
     b=(root/r['copy']).read_bytes();r['bytes']=len(b);r['sha256']=sha(b)
    dump(mp,mo);repin()
   evidence_faults=[(current_prefix+'ROOT_WHOLE_PACKAGE_REVIEW_03.json','whole_reviews_completed',2,'root','whole03 root adoption semantics'),(current_prefix+'ROOT_WHOLE_PACKAGE_REVIEW_03.json','actionable_P0_P1_P2_P3',1,'root','whole03 root adoption semantics'),(current_prefix+'ROOT_WHOLE_PACKAGE_REVIEW_03.json','terminal_administrative_reconciliation_and_root_final_integrity_required',False,'root','whole03 root adoption semantics'),(current_prefix+'ROOT_WHOLE_PACKAGE_REVIEW_03.json','published',True,'root','whole03 evidence no readiness/service promotion'),(current_prefix+'ROOT_WHOLE_PACKAGE_REVIEW_03.json','services_held_after_pr',1033,'root','whole03 evidence no readiness/service promotion'),(current_prefix+'ROOT_CASE_ALIAS_REPAIR_REVIEW_01.json','status','CLEARED','root','captured root case repair adoption'),(review_prefix+'VERDICT.json','severity_counts',{'P0':0,'P1':0,'P2':0,'P3':1},'review_output','whole03 zero finding verdict semantics'),(review_prefix+'VERDICT.json','human_peer_review',True,'review_output','whole03 evidence no refereeing promotion'),(review_prefix+'VERDICT.json','novelty','NEW','review_output','whole03 evidence historical scope'),(review_prefix+'VERDICT.json','publication_ready',True,'review_output','whole03 evidence no readiness/service promotion'),(review_prefix+'DERIVATION_FREEZE.json','before_prior_review_reasoning',False,'review_output','whole03 frozen independent derivation')]
   for name,key,value,kind,message in evidence_faults:
    fresh();coherent_evidence(name,key,value,kind)
    p=run(root,prefix+['verify_package.py'],label+' coherent current evidence '+Path(name).name+' '+key,False,message)
    semantic.append({'mode':label,'case':name+' '+key,'reached_guard':message,'returncode':p.returncode,'outer_manifest_and_copy_map_refreshed':True,'review_output_manifest_seal_and_root_binding_refreshed':kind=='review_output'})
   for kind in ['membership','bytes','before_locator']:
    fresh();p=root/cmap;o=json.loads(p.read_text())
    if kind=='membership':o['files'].pop();message='current terminal exact copy membership'
    elif kind=='bytes':o['files'][0]['sha256']='0'*64;message='current terminal exact copied bytes'
    else:o['files'][-1]['source_snapshot_relative_audit']='successor/UPLOAD_BINDINGS.json';message='current terminal exact before locator'
    dump(p,o);repin();run(root,prefix+['verify_package.py'],label+' current map fault '+kind,False,message)
   fresh();(root/current_name).write_text('{"schema":1,"schema":1}\n');repin();run(root,prefix+['verify_package.py'],label+' duplicate current JSON',False,'duplicate JSON key')
   for n in ['PAYLOAD_MEMBERS.txt','SUPPORT_MANIFEST.json']:
    fresh();target=temp/(label+'_'+n);target.write_bytes((root/n).read_bytes());(root/n).unlink();(root/n).symlink_to(target)
    run(root,prefix+['verify_package.py'],label+' bootstrap symlink '+n,False,'symlink input or ancestor');target.unlink()
   fresh();(root/'CASE_ALIAS_REPAIR_ACCOUNTING.json').write_text('{"schema":1,"schema":1}\n');repin()
   run(root,prefix+['verify_package.py'],label+' duplicate repair JSON',False,'duplicate JSON key')
   fresh();compiler=temp/('compiler_'+label);compiler.mkdir();sentinel=temp/('compiler_called_'+label)
   stub=compiler/'tectonic';stub.write_text('#!/bin/sh\nprintf called > "'+str(sentinel)+'"\nexit 99\n');stub.chmod(0o755);env=dict(os.environ,PATH=str(compiler))
   # An independently observed physical premise precedes every alias run.
   alias=root.with_name('KIT');need(alias.exists() and alias.samefile(root),'no case-alias premise')
   pairs=[('case',root,alias)]
   unicode_parent=temp/'Caf\u00e9';unicode_parent.mkdir();unicode_alias=temp/'Cafe\u0301'
   normalization_supported=unicode_alias.exists() and unicode_alias.samefile(unicode_parent)
   if normalization_supported:
    unicode_root=unicode_parent/'kit';unicode_root.mkdir()
    for n,b in payload.items():
     p=unicode_root/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
    pairs.append(('normalization',unicode_root,unicode_alias/'kit'))
   for kind,canonical,alternate in pairs:
    st=canonical.stat();alt=alternate.stat();need((st.st_dev,st.st_ino)==(alt.st_dev,alt.st_ino) and canonical.samefile(alternate),'alias device/inode mismatch')
    for direction,sroot,troot in [('canonical_script_alias_output',canonical,alternate),('alias_script_canonical_output',alternate,canonical)]:
     for depth,tail in [('fresh_leaf','case_fresh'),('missing_intermediates','case_missing/child/case_fresh')]:
      for script,option in writers:
       out=troot/(tail+'_'+script);need(not os.path.lexists(out),'alias target exists');before=identities(canonical)
       p=run(root,prefix+[str(sroot/script),option,str(out)],label+' '+kind+' '+direction+' '+depth+' '+script,False,'output must be outside',env)
       need(not os.path.lexists(out) and not (troot/'case_missing').exists() and not sentinel.exists(),'alias wrote/compiled')
       need(identities(canonical)==before,'alias changed kit')
       physical.append({'mode':label,'kind':kind,'direction':direction,'depth':depth,'script':script,'script_root':str(sroot),'output':str(out),'canonical_identity':[st.st_dev,st.st_ino],'alias_identity':[alt.st_dev,alt.st_ino],'samefile':canonical.samefile(alternate),'canonical_resolve':str(canonical.resolve()),'alias_resolve':str(alternate.resolve()),'returncode':p.returncode,'no_output_directory_or_compiler_sentinel':True,'kit_unchanged':True})
   for script,option in writers:
    out=root/'canonical_missing/child/output';run(root,prefix+[script,option,str(out)],label+' canonical location '+script,False,'output must be outside',env)
    need(not (root/'canonical_missing').exists() and not sentinel.exists(),'canonical guard wrote/compiled')
   for script,option in writers:
    for kind in ['direct','hardlink','symlink','symlink_parent']:
     target=root/'paper.tex';before=target.read_bytes();out=temp/(label+'_'+script+'_'+kind)
     if kind=='direct':out=target
     elif kind=='hardlink':os.link(target,out)
     elif kind=='symlink':out.symlink_to(target)
     else:out.symlink_to(root,target_is_directory=True);out=out/'fresh_missing/child/output'
     p=run(root,prefix+[script,option,str(out)],label+' old '+kind+' '+script,False,'output ',env)
     need(target.read_bytes()==before and not sentinel.exists(),'old alias altered target/compiler')
     if kind in ['hardlink','symlink']:out.unlink()
     if kind=='symlink_parent':(temp/(label+'_'+script+'_'+kind)).unlink()
     aliases.append({'mode':label,'script':script,'kind':kind,'target_unchanged':True,'compiler_sentinel_absent':True,'returncode':p.returncode})
   external=temp/('external_descriptor_'+label);external.write_text('{}\n')
   for kind in ['direct','hardlink','symlink','symlink_parent']:
    out=temp/(label+'_descriptor_'+kind)
    if kind=='direct':out=external
    elif kind=='hardlink':os.link(external,out)
    elif kind=='symlink':out.symlink_to(external)
    else:out.symlink_to(temp,target_is_directory=True);out=out/external.name
    run(root,prefix+['verify_package.py','--deposit',str(external),'--output',str(out)],label+' protected descriptor '+kind,False,'output ')
    need(external.read_text()=='{}\n','descriptor changed')
    if kind in ['hardlink','symlink']:out.unlink()
    if kind=='symlink_parent':(temp/(label+'_descriptor_'+kind)).unlink()
   external.unlink()
   for child in ['paper.tex','paper.pdf','paper.log','COMPILE_RECEIPT.json']:
    outdir=temp/(label+'_pdf_'+child);outdir.mkdir();os.link(root/'paper.tex',outdir/child);before=(root/'paper.tex').read_bytes()
    run(root,prefix+['build_pdf.py','--out-dir',str(outdir)],label+' PDF child hardlink '+child,False,'output hardlinks protected input',env)
    need((root/'paper.tex').read_bytes()==before and sorted(p.name for p in outdir.iterdir())==[child] and not sentinel.exists(),'PDF child wrote/compiled');remove_tree(outdir)
   for script in ['verify_package.py','check_math.py','build_archive.py']:
    out=temp/(label+'_external_'+script)/'missing/child/output';run(root,prefix+[script,'--output',str(out)],label+' external missing descendant '+script)
    need(out.is_file(),'outside positive missing')
    if script=='build_archive.py':need(out.read_bytes()==body,'outside archive mismatch')
   need(not sentinel.exists(),'compiler invoked');remove_tree(compiler);remove_tree(unicode_parent)
   for mutation in ['normal_sign','lost_jacobian','preprint_theta','fourier_boundary_sign']:
    run(root,prefix+['check_math.py','--mutation',mutation],label+' original math fault '+mutation,False)
   run(root,prefix+['verify_package.py'],label+' final restored verification');need(start==identities(root),'final clean kit changed')
   mode_results.append({'mode':label,'default':default,'math':math,'strict':strict,'clean_payload_unchanged':True})
 need(mode_results[0]['default']==mode_results[1]['default'] and mode_results[0]['math']==mode_results[1]['math'] and mode_results[0]['strict']==mode_results[1]['strict'],'normal/optimized full JSON differs')
 p=run(REPO,[sys.executable,'-B',str(REPO/'zenodo_deposit_tool/zenodo.py'),'check',str(K/'zenodo-deposit.json')],'actual repository LOCAL native check')
 native=json.loads(p.stdout);need(native['files'][0]['sha256']==sha((K/'paper.pdf').read_bytes()) and native['files'][1]['sha256']==sha(body),'repository tool identities')
 need(baseline==identities(K),'canonical candidate changed by controls')
 dump(F/'PHYSICAL_ANCESTOR_CONTROLS.json',{'passed':True,'normalization_supported':normalization_supported,'cases':physical,'all_actual_samefile_premises':True,'all_four_writers':True,'no_compiler_invoked':True})
 dump(F/'OLD_ALIAS_CONTROLS.json',{'passed':True,'cases':aliases,'additional_per_mode':'Four supplied-descriptor alias cases and all four PDF child hardlinks; compiler sentinel absent.'})
 dump(F/'CURRENT_SEMANTIC_CONTROLS.json',{'passed':True,'coherent_outer_manifest_refresh':True,'cases':semantic,'additional_per_mode':'copy-map membership/hash and coherent copied root hold faults, duplicate JSON, bootstrap preflights.'})
 dump(F/'REPOSITORY_TOOL_LOCAL_CHECK.json',{'passed':True,'argv':records[-1]['argv'],'result':native,'services':'None; local check only.'})
 dump(F/'CONTROL_SUMMARY.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'passed':True,'commands':len(records),'successes':sum(r['returncode']==0 for r in records),'expected_rejections':sum(r['returncode']!=0 for r in records),'physical_alias_cases':len(physical),'mode_results':mode_results,'normal_optimized_full_JSON_equal':True,'independent_closed_deflate9_ZIP_equal':True,'headers_order_CRC_payload_verified':True,'canonical_candidate_unchanged':True,'scratch_removed':True,'no_actual_compile_render_or_marker':True})
 print(json.dumps({'passed':True,'commands':len(records),'physical_alias_cases':len(physical)}))
if __name__=='__main__':main()
