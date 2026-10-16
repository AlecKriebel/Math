"""History/content checks and additional ordinary-mode/topology fixtures; owned writes only."""
from pathlib import Path
import datetime, hashlib, io, json, os, re, shutil, stat, subprocess, zipfile
from reproduce import HERE, PRE, TMP, PDF, DESTS, need, ident, tree, closed_copy, call, save

def main():
 rows=[]
 for n in ['review_preprint01','review_preprint02']:
  r=HERE.parent/n;raw=(r/'MANIFEST.json').read_bytes();m=json.loads(raw);expected={x['path']:x for x in m['authored_files']};actual={p.relative_to(r).as_posix():p for p in r.rglob('*') if not p.is_dir()}
  need(set(actual)==set(expected)|{'MANIFEST.json'},'prior inventory '+n)
  for name,p in actual.items():
   need(not p.is_symlink() and stat.S_ISREG(p.lstat().st_mode),'prior type')
   if name!='MANIFEST.json':need(ident(p.read_bytes())=={k:expected[name][k] for k in ('bytes','sha256')},'prior byte '+name)
  need(len(expected)==26,'priorcount');rows.append({'review':n,'manifest':ident(raw),'authored_files':len(expected),'all_authored_bytes_and_exact_inventory_match':True,'bound_prior_input_sha256_record':ident((r/'CHECKED_INPUTS.json').read_bytes()),'current_adjacent_input_expected_changed':True,'historical_verdict_not_used_as_proof_premise':True})
 save('INHERITED_CLOSURE_RECEIPT.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviews':rows,'scope':'Review-only closure remains valid across publication input revisions. Old current-input-binding helpers were not misrun against newer inputs.'})
 # Inspect every file as UTF8/ZIP, inventory all archives recursively, narrow credential scan.
 patterns={'private_key':rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----','github_token':rb'gh[pousr]_[A-Za-z0-9]{30,}','google_api':rb'AIza[0-9A-Za-z_-]{30,}','openai_key':rb'sk-(?:proj-)?[A-Za-z0-9_-]{40,}'}
 screen=[];ziprows=[];hits=[]
 def inspectzip(raw,label):
  with zipfile.ZipFile(io.BytesIO(raw)) as z:
   names=z.namelist();need(len(names)==len(set(names)),'zip duplicates '+label)
   for i in z.infolist():
    need(not i.filename.startswith('/') and '\\' not in i.filename and all(k not in ('','.','..') for k in i.filename.rstrip('/').split('/')),'unsafe '+label)
    if i.is_dir():continue
    need(not stat.S_ISLNK(i.external_attr>>16),'archive symlink '+label)
   need(z.testzip() is None,'CRC '+label);ziprows.append({'archive':label,'members':len(names),'safe_names_unique_CRC_valid':True})
 for p in sorted((TMP/'source').rglob('*')):
  if not p.is_file():continue
  name=p.relative_to(TMP/'source').as_posix();b=p.read_bytes()
  for k,pat in patterns.items():
   if re.search(pat,b):hits.append({'path':name,'pattern':k})
  if p.suffix=='.zip':inspectzip(b,name);typ='authored_historical_ZIP'
  else:
   b.decode('utf8');need(p.suffix.lower() in {'.json','.md','.py','.tex',''} or p.name=='.gitignore','unexpected type '+name);typ='UTF8_authored_text'
  screen.append({'path':name,'kind':typ,**ident(b)})
 inspectzip((PRE/'source-and-verification.zip').read_bytes(),'source-and-verification.zip');inspectzip((PRE/'zenodo-upload-kit.zip').read_bytes(),'zenodo-upload-kit.zip')
 need(len(screen)==120 and not hits,'content screen');save('CONTENT_SCREEN_RECEIPT.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':screen,'file_count':120,'zip_structures':ziprows,'credential_pattern_hits':hits,'limits':'Narrow signature and file-type/content screen, not universal secret detection; no retained third-party full bodies or outreach artifacts found.'})
 attacks=[];case=TMP/'supplement'
 for n in DESTS:
  for t in ['ordinary_PDF_overlap','portable_PDF_hardlink']:
   if case.exists():shutil.rmtree(case)
   case.mkdir();s=case/'source';closed_copy(s);o=case/'out';o.mkdir();d=o/n;d.parent.mkdir(parents=True,exist_ok=True);p=case/'input.pdf';p.write_bytes(PDF.read_bytes())
   if t=='ordinary_PDF_overlap':(s/'MANIFEST.json').unlink();d.write_bytes(PDF.read_bytes());p=d
   else:os.link(p,d)
   before=tree(case);r=call([os.sys.executable,'-O','-B',str(s/'build_package.py'),'--output-dir',str(o),'--pdf',str(p)],2)
   need(r.returncode!=0 and tree(case)==before,'supp '+t+n);attacks.append({'case':t+'_'+n,'exit':r.returncode,'prewrite_preservation':True,'reason':r.stderr.splitlines()[-1]});shutil.rmtree(case)
 # The input tree can itself sit below an apparently external output root.
 case.mkdir();s=case/'out/output/pdf';closed_copy(s);p=case/'paper.pdf';p.write_bytes(PDF.read_bytes());before=tree(case)
 r=call([os.sys.executable,'-O','-B',str(s/'build_package.py'),'--output-dir',str(case/'out'),'--pdf',str(p)],2)
 need(r.returncode!=0 and tree(case)==before,'nested closed input');attacks.append({'case':'closed_input_nested_under_external_output','exit':r.returncode,'prewrite_preservation':True,'reason':r.stderr.splitlines()[-1]});shutil.rmtree(case)
 save('SUPPLEMENTARY_ATTACKS.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'count':len(attacks),'cases':attacks,'scope':'Static ordinary/portable PDF aliases and nested source topology. No hostile concurrent-filesystem claim.'})
 print(json.dumps({'status':'PASS','prior_authored_files':52,'screened_files':120,'supplementary_rejections':len(attacks),'zip_structures':len(ziprows)}))
if __name__=='__main__':main()
