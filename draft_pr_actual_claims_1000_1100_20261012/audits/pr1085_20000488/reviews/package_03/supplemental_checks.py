from pathlib import Path
import subprocess,json,hashlib,sys,os,shutil,datetime
P=Path(__file__).resolve().parent;S=P/'scratch';K=S/'KitRoot';rows=[];base={str(p.relative_to(K)):p.read_bytes() for p in K.rglob('*') if p.is_file()};py=sys.executable
def need(b,m):
 if not b:raise ValueError(m)
def h(b):return hashlib.sha256(b).hexdigest()
def restore():
 for p in K.rglob('*'):
  if p.is_file() or p.is_symlink():p.unlink()
 for n,b in base.items():p=K/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
def change(n,k,v):
 p=K/n;o=json.loads(p.read_text());o[k]=v;p.write_text(json.dumps(o,indent=2)+'\n')
def repin():
 p=K/'SUPPORT_MANIFEST.json';o=json.loads(p.read_text())
 for r in o['files']:
  b=(K/r['path']).read_bytes();r.update(bytes=len(b),sha256=h(b))
 p.write_text(json.dumps(o,indent=2)+'\n')
def maprepin(n,copied):
 p=K/n;o=json.loads(p.read_text())
 for r in o['files']:
  if r['copy']==copied:
   b=(K/copied).read_bytes();r.update(bytes=len(b),sha256=h(b))
 p.write_text(json.dumps(o,indent=2)+'\n')
def run(label,args,good=False,message=None):
 r=subprocess.run([py,*args],capture_output=True,text=True);rows.append({'label':label,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'argv':[py,*args],'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'expected_success':good,'expected_message':message});(P/'SUPPLEMENTAL_RECEIPTS.json').write_text(json.dumps(rows,indent=2)+'\n');need((r.returncode==0)==good,'status '+label)
 if message:need(message in r.stderr,'intended semantic gate '+label)
 return r
for mode in [[],['-O']]:
 restore();n='evidence/case_alias01/ROOT_TERMINAL_ADMIN_REVIEW_20261016.json';change(n,'services_held_after_pr',0);maprepin('CASE_ALIAS_REPAIR_COPY_MAP.json',n);repin();run('coherent-case-copy-and-manifest-semantic-hold'+str(mode),[*mode,'-B',str(K/'verify_package.py')],message='case repair root hold evidence')
 restore();n='evidence/terminal/ROOT_WHOLE_PACKAGE_REVIEW_02.json';change(n,'publication_ready',True);maprepin('TERMINAL_COPY_MAP.json',n);repin();run('historical-source-pin-cannot-rewrite-via-current-copymap'+str(mode),[*mode,'-B',str(K/'verify_package.py')],message='terminal source/copy identity')
 for k,v,msg in [('published',True,'case repair forbidden promotion'),('root_repair_adoption_required',False,'case repair required review/adoption/history'),('services_hold','none','case repair ordered hold'),('priority','FIRST','case repair historical scope'),('schema',True,'case repair schema')]:
  restore();change('CASE_ALIAS_REPAIR_ACCOUNTING.json',k,v);repin();run('coherent-current-'+k+str(mode),[*mode,'-B',str(K/'verify_package.py')],message=msg)
 restore();p=K/'CASE_ALIAS_REPAIR_ACCOUNTING.json';p.write_text(p.read_text().replace('"schema": 1,','"schema": 1, "schema": 1,',1));repin();run('duplicate-json'+str(mode),[*mode,'-B',str(K/'verify_package.py')],message='duplicate JSON key')
 for typ in ['dangling','ordinary','corrupt','wrong-location']:
  restore();desc=S/('descriptor-'+typ+'.json');desc.unlink(missing_ok=True)
  if typ=='dangling':desc.symlink_to(S/'no-such-descriptor')
  elif typ=='ordinary':desc.symlink_to(K/'zenodo-deposit.json')
  elif typ=='corrupt':desc.write_text('{')
  else:desc.write_bytes((K/'zenodo-deposit.json').read_bytes())
  run('supplied-'+typ+str(mode),[*mode,'-B',str(K/'verify_package.py'),'--deposit',str(desc)]);desc.unlink()
 restore();(K/'zenodo-deposit.json').unlink();(K/'zenodo-deposit.json').symlink_to(S/'no-deposit');run('dangling-default-optional'+str(mode),[*mode,'-B',str(K/'verify_package.py')],message='symlink input')
 restore();ev=K/'evidence/case_alias01';holding=S/'holding-evidence';ev.rename(holding);ev.symlink_to(holding,target_is_directory=True);(K/'SUPPORT_MANIFEST.json').write_text('{');run('input-ancestor-preparse'+str(mode),[*mode,'-B',str(K/'verify_package.py')],message='symlink input or ancestor');ev.unlink();holding.rename(ev)
 restore();old=S/'submitted/README.md';old.parent.mkdir(exist_ok=True);old.write_bytes((K/'evidence/submitted/README.md').read_bytes());before=old.read_bytes()
 for e,arg in [('verify_package.py','--output'),('check_math.py','--output'),('build_archive.py','--output')]:run('frozen-external-original-'+e+str(mode),[*mode,'-B',str(K/e),arg,str(old)],message='aliases protected input');need(old.read_bytes()==before,'original conservation')
 out=S/'external-old-pdf';out.mkdir(exist_ok=True);os.link(old,out/'paper.tex');run('frozen-external-original-build_pdf'+str(mode),[*mode,'-B',str(K/'build_pdf.py'),'--out-dir',str(out)],message='hardlinks protected input');(out/'paper.tex').unlink();out.rmdir();old.unlink()
restore()
(P/'SUPPLEMENTAL_SUMMARY.json').write_text(json.dumps({'passed':True,'commands':len(rows),'coherent_current_case_hold_reached':True,'historical_pins_immutable':True,'all_requests_disposable':True,'initial_generation_failure':'Earlier shell heredoc could not be created during transient no-space state; no test ran in that attempt.'},indent=2)+'\n');print(len(rows))
