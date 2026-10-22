import sys,os,json,hashlib,subprocess,datetime,zipfile,io,stat,tempfile,shutil,collections
from pathlib import Path
sys.dont_write_bytecode=True
A=Path(__file__).resolve().parents[1];R=A/'finalization/terminal_admin_20261016';P=A/'preprint_v1_0';O=A/'root_reproduction/terminal_20261016';O.mkdir(exist_ok=True)
def need(c,s):
 if not c:raise RuntimeError(s)
def load(p):return json.loads(p.read_text())
def identity(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def expected(r):return {k:r[k] for k in ['bytes','sha256']}
def same(p,r):return identity(p)==expected(r)
def save(p,v):p.write_text(json.dumps(v,indent=2,allow_nan=False)+'\n')
seal=load(R/'OUTPUT_SEAL.json');need(identity(R/'OUTPUT_PINS.json')==seal['output_pins'],'seal pin binding')
for row in load(R/'OUTPUT_PINS.json')['entries']:need(same(A/row['path'],row),'terminal output '+row['path'])
base=load(R/'INPUT_FREEZE.json')['entries'];resolution=load(R/'BASELINE_RESOLUTION.json')['entries'];need(len(base)==len(resolution)==358,'baseline count')
counts=collections.Counter()
for old,row in zip(base,resolution):
 need(all(old[k]==row[k] for k in old),'baseline row original identity');counts[row['disposition']]+=1
 p=A/(row['before_path'] if 'before_path' in row else row['path']);need(same(p,old),'baseline original bytes')
 need(identity(A/row['path'])==row['current_identity'],'baseline current identity')
 if row['disposition']=='UNCHANGED_CURRENT_EXACT':need(stat.S_IMODE(p.stat().st_mode)==old['mode'] and p.stat().st_mtime_ns==old['mtime_ns'] and p.stat().st_nlink==old['nlink'],'protected metadata')
need(counts=={'UNCHANGED_CURRENT_EXACT':353,'CHANGED_CURRENT_EXACT_EXTANT_BEFORE':5},'bounded counts')
for row in load(R/'CURRENT_PINS.json')['entries']:need(same(A/row['path'],row),'current pin')
copies=load(R/'COPY_LEDGER.json')['entries'];need(len(copies)==18,'18 copies')
for row in copies:need(same(A/row['source'],row) and same(P/row['destination'],row) and (A/row['source']).read_bytes()==(P/row['destination']).read_bytes(),'copy')
custody=load(P/'CUSTODY_SELECTION.json')['entries'];prep=load(P/'INPUT_FREEZE.json')['entries'];need(len(custody)==len(prep)==168,'168 prep')
for row in prep:need(same(A/row['path'],row),'prep source')
for row in custody:
 need(same(A/row['path'],row),'custody source')
 if row['disposition']=='EXACT_AUTHORED_COPY':need(same(P/row['destination'],row),'80 original copies')
 else:need(row['disposition']=='OMITTED' and bool(row['reason']),'individual omission')
need(collections.Counter(r['disposition'] for r in custody)=={'EXACT_AUTHORED_COPY':80,'OMITTED':88},'80/88')
prep_res=load(P/'terminal/PREPARATION_PIN_RESOLUTION.json')['entries'];need([{k:r[k] for k in ['path','bytes','sha256']} for r in prep_res]==load(P/'OUTPUT_PINS.json')['entries'],'123 exact ordered prep identities')
for r in prep_res:
 p=R/'before/preprint_v1_0/pr1098_support_v1_0.zip' if r['disposition']=='KNOWN_OLD_ZIP_OMITTED' else P/(r['resolved_path'] if 'resolved_path' in r else r['path']);need(same(p,r),'prep resolution '+r['path'])
decisions=load(P/'terminal/REVIEW_STAGE_SELECTION.json')['entries'];need(len(decisions)==55,'55 decisions')
for number in [1,2]:
 rr=A/('reviews/package_'+str(number).zfill(2));rows=load(rr/'OUTPUT_PINS.json')['entries'];need(identity(rr/'OUTPUT_PINS.json')==load(rr/'OUTPUT_SEAL.json')['output_pins'],'review pinseal')
 for row in rows:
  need(same(rr/row['path'],row),'review output');ds=[r for r in decisions if r['review']=='package_'+str(number).zfill(2) and r['path']==row['path']];need(len(ds)==1 and expected(ds[0])==expected(row),'individual review decision')
oldgit=load(A/'reviews/package_01/CUSTODY_REVIEW.json')['actual_git'];newgit=load(P/'validation/ORIGINAL_INPUT_RECHECK.json')['actual_git'];need(len(oldgit)==len(newgit)==9,'nine Git records')
for row in oldgit:
 name=Path(row['path']).name;r=next(r for r in newgit if r['path']==name);need(same(A/'submitted'/name,row) and expected(row)==expected(r) and r['actual_git_equal'],'nine original retained Git receipts')
def closed(root):
 rows=load(root/'MANIFEST.json')['entries'];payload={r['path']:(root/r['path']).read_bytes() for r in rows}
 for r in rows:need(same(root/r['path'],r),'manifest member')
 payload['MANIFEST.json']=(root/'MANIFEST.json').read_bytes();buf=io.BytesIO()
 with zipfile.ZipFile(buf,'w',compression=zipfile.ZIP_STORED) as z:
  for n in sorted(payload):
   i=zipfile.ZipInfo(n,(2026,10,16,0,0,0));i.create_system=3;i.external_attr=0o100644<<16;z.writestr(i,payload[n])
 return buf.getvalue()
raw=(P/'pr1098_support_v1_0.zip').read_bytes();need(closed(P)==raw and len(load(P/'MANIFEST.json')['entries'])==123,'independent closed124')
with zipfile.ZipFile(io.BytesIO(raw)) as z:need(len(z.infolist())==124 and z.testzip() is None and not z.comment,'archive CRC/count')
receipts=[]
def run(argv,ok=True):
 e=os.environ.copy();e['PYTHONDONTWRITEBYTECODE']='1';p=subprocess.run(argv,cwd=O,env=e,capture_output=True,text=True);receipts.append({'argv':argv,'cwd':str(O),'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'expected_success':ok});save(O/'ACTUAL_COMMANDS.json',receipts);need((p.returncode==0)==ok,'actual command '+str(argv));return p
py='/opt/homebrew/bin/python3.14';tmp=Path(tempfile.mkdtemp(prefix='root1098-terminal-',dir='/private/tmp'));C=tmp/'clean';C.mkdir();cleanup=[]
try:
 with zipfile.ZipFile(io.BytesIO(raw)) as z:z.extractall(C)
 shutil.copyfile(P/'paper.pdf',C/'paper.pdf');shutil.copyfile(P/'pr1098_support_v1_0.zip',C/'pr1098_support_v1_0.zip')
 sentinel=tmp/'sentinel';sentinel.write_text('root1098 terminal sentinel\n');sentinel_id=identity(sentinel)
 for flags in [[],['-O']]:
  for root in [P,C]:run([py,'-B',*flags,str(root/'code/verify_kit.py')])
  p=run([py,'-B',*flags,str(C/'code/run_checks.py')]);need(json.loads(p.stdout)==load(R/'MATH_normal.json'),'full math JSON')
  run([py,'-B',*flags,str(C/'code/run_checks.py'),'--invalid'],False)
  target=tmp/('optimized.zip' if flags else 'normal.zip');run([py,'-B',*flags,str(C/'code/rebuild_archive.py'),'--output',str(target)]);need(target.read_bytes()==raw,'actual rebuild')
  for script,arg in [('rebuild_archive.py','--output'),('build_pdf.py','--out-dir')]:
   run([py,'-B',*flags,str(C/'code'/script),arg,str(sentinel)],False)
   alias=A.with_name(A.name.swapcase());need(alias.samefile(A),'physical case alias');run([py,'-B',*flags,str(C/'code'/script),arg,str(alias/'root1098-never-output')],False)
 # Coherently rehash and fully repack the changed current count: semantic verifier must reject.
 status=C/'TERMINAL_STATUS.json';man=C/'MANIFEST.json';arc=C/'pr1098_support_v1_0.zip';sb=status.read_bytes();mb=man.read_bytes();ab=arc.read_bytes()
 d=load(status);d['new_complete_whole_reviews_completed']=1;status.write_text(json.dumps(d));m=load(man)
 for r in m['entries']:
  if r['path']=='TERMINAL_STATUS.json':r.update(identity(status))
 man.write_text(json.dumps(m));arc.write_bytes(closed(C))
 for flags in [[],['-O']]:run([py,'-B',*flags,str(C/'code/verify_kit.py')],False)
 status.write_bytes(sb);man.write_bytes(mb);arc.write_bytes(ab)
 # Bootstrap manifest symlink rejection, before parsing.
 man.unlink();man.symlink_to(sentinel)
 for flags in [[],['-O']]:run([py,'-B',*flags,str(C/'code/verify_kit.py')],False)
 man.unlink();man.write_bytes(mb)
 run([py,'-B',str(C/'code/verify_kit.py')]);need(identity(sentinel)==sentinel_id,'sentinel unchanged')
 run([py,'-B','/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py','check',str(P/'publication/zenodo-deposit.json')])
finally:
 for p in sorted(tmp.rglob('*')):
  if p.is_symlink():cleanup.append({'path':str(p),'symlink_target':str(p.readlink())})
  elif p.is_file():cleanup.append({'path':str(p),**identity(p)})
 save(O/'OWN_EXTERNAL_CLEANUP.json',{'scope':'Only newly created unsealed ROOT terminal reproduction fixtures; exact identities before removal. No old or pinned source/candidate retired.','entries':cleanup});shutil.rmtree(tmp)
for row in load(R/'OUTPUT_PINS.json')['entries']:need(same(A/row['path'],row),'postrun terminal pin')
adoption={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ROOT_ADOPT_TERMINAL_ADMIN_ZERO_ACTIONABLE_LOCALLY_READY_ORDERED_SERVICES_HELD','ROOT_full_REPORT_operative_prose_code_diff_current_verifier_and_seal_generator_read':True,'counts':{'baseline':358,'authorized_changes':5,'protected':353,'terminal_outputs':158,'current_canonical_pins':127,'authored_interface_copies':18,'preparation_rows':168,'original_copies':80,'original_individual_omissions':88,'preparation_output_resolutions':123,'review_output_decisions':55,'closed_archive_members':124},'baseline_and_before_and_all_original_ordered_rows_and_sources_rehashed':True,'actual_root_commands':receipts,'independent_closed_archive':identity(P/'pr1098_support_v1_0.zip'),'unchanged_paper':identity(P/'paper.pdf'),'whole_reviews_completed':2,'minimum_whole_reviews':2,'latest_complete_whole02_root_adopted_zero_actionable':True,'further_whole_review_currently_required':False,'historical_record_scope':'Dated internal pending ROOT flags remain exact; this external ROOT adoption/current final seal governs local readiness. Earlier first admin clean-extraction failure and corrected individual18 local-preparation omissions preserved, no false success.','no_new_math_code_pathguard_PDF_TeX_native_metadata_change':True,'publication_ready':True,'issues_resolved':True,'published':False,'services_held_after_pr':1032,'remaining_full_result_method_priority_and_worldwide_openness':'UNKNOWN','no_external_service_or_Git_called':True}
save(A/'ROOT_TERMINAL_ADMIN_REVIEW_20261016.json',adoption)
files=[A/'ROOT_TERMINAL_ADMIN_REVIEW_20261016.json',R/'OUTPUT_SEAL.json',R/'OUTPUT_PINS.json',R/'OPERATIVE_DIFF.patch',P/'paper.pdf',P/'paper.tex',P/'pr1098_support_v1_0.zip',P/'DEPOSIT_BINDING.json',P/'publication/zenodo-deposit.json']
integrity={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'current_authority':'External ROOT current final seal; immutable earlier internal pending records remain dated history.','entries':[{'path':str(p.relative_to(A)),**identity(p)} for p in files],'all_158_terminal_outputs_checked':True,'all_358_baseline_resolutions_checked':True,'publication_ready':True,'issues_resolved':True,'published':False,'services_held_after_pr':1032};save(A/'CURRENT_FINAL_INTEGRITY_20261016.json',integrity)
save(A/'CURRENT_FINAL_SEAL_20261016.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'CURRENT_ROOT_FINAL_READY_ORDERED_SERVICES_HELD_AFTER_PR1032','integrity':identity(A/'CURRENT_FINAL_INTEGRITY_20261016.json'),'root_adoption':identity(A/'ROOT_TERMINAL_ADMIN_REVIEW_20261016.json'),'publication_ready':True,'issues_resolved':True,'published':False,'services_held_after_pr':1032,'whole_reviews_completed':2,'minimum_whole_reviews':2,'all_actionable_findings_resolved':True,'paper':identity(P/'paper.pdf'),'support_archive':identity(P/'pr1098_support_v1_0.zip')})
print(json.dumps({'status':'PASS_ROOT_CURRENT_FINAL_SEALED_READY_UNPUBLISHED_HOLD1032','commands':len(receipts),'archive':identity(P/'pr1098_support_v1_0.zip')}))
