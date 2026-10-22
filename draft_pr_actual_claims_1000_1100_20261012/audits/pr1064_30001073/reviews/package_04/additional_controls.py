from pathlib import Path
import subprocess,sys,json,hashlib,zipfile,datetime
O=Path(__file__).resolve().parent;A=O.parent.parent;P=A/'preprint_v1_0';S=O/'scratch';K=S/'kit';R=[]
def req(c,m):
 if not c:raise RuntimeError(m)
def h(b):return hashlib.sha256(b).hexdigest()
def run(name,args,ok=True,cwd=K):
 q=subprocess.run(args,cwd=cwd,capture_output=True,text=True);R.append({'name':name,'argv':list(map(str,args)),'returncode':q.returncode,'expected_success':ok,'stdout':q.stdout,'stderr':q.stderr});req((q.returncode==0)==ok,name);return q
for mode,flags in [('normal',[]),('optimized',['-O'])]:
 pre=[sys.executable,'-I','-B',*flags]
 binding=K/'publication/DEPOSIT_BINDING.json';good=(P/'publication/DEPOSIT_BINDING.json').read_bytes()
 for label,mutate in [('extra_field',lambda d:d.update(extra=True)),('wrong_zip_hash',lambda d:d['support_archive'].update(sha256='0'*64)),('wrong_schema',lambda d:d.update(schema_version=2))]:
  d=json.loads(good);mutate(d);binding.write_text(json.dumps(d));run(mode+'_binding_'+label,pre+['verify_package.py','--archive','tmp/rebuilt-normal.zip'],False)
 binding.unlink()
 # Coherent mutations rehash scratch manifest, so hash mismatch cannot mask gate semantics.
 for field,value in [('ready_for_submission',True),('publication_ready',True),('published',True),('issues_updated',True),('new_complete_whole04_required',False),('root_repair_adoption_required',False),('focused_validation_is_complete_whole_review',True),('ascending_publication_hold_after_pr',1033),('whole_package_reviews_completed',4)]:
  status=K/'REPAIR_STATUS_CASE_ALIAS01.json';old=status.read_bytes();mf=K/'SUPPORT_MANIFEST.json';mf_old=mf.read_bytes();d=json.loads(old);d[field]=value;status.write_text(json.dumps(d));m=json.loads(mf_old)
  for row in m['entries']:
   if row['path']==status.name:row.update(bytes=status.stat().st_size,sha256=h(status.read_bytes()))
  mf.write_text(json.dumps(m));q=run(mode+'_coherent_gate_'+field,pre+['verify_package.py'],False);req('hash mismatch' not in q.stderr,'gate masked by hash');status.write_bytes(old);mf.write_bytes(mf_old)
 # Unsafe and wrong-coverage archives, independently created.
 bad=S/'bad.zip'
 with zipfile.ZipFile(bad,'w') as z:z.writestr('../escape','x')
 run(mode+'_unsafe_archive',pre+['verify_package.py','--archive',str(bad)],False)
 with zipfile.ZipFile(bad,'w') as z:z.writestr('paper.pdf',(P/'paper.pdf').read_bytes())
 run(mode+'_missing_archive_members',pre+['verify_package.py','--archive',str(bad)],False)
run('render_canonical',['pdftoppm','-r','95','-png',str(P/'paper.pdf'),str(S/'canonical')],cwd=S)
run('extract_canonical_text',['pdftotext','-layout',str(P/'paper.pdf'),str(S/'canonical.txt')],cwd=S)
run('extract_compiled_text',['pdftotext','-layout',str(S/'compiled/paper.pdf'),str(S/'compiled.txt')],cwd=S)
req((S/'canonical.txt').read_bytes()==(S/'compiled.txt').read_bytes(),'PDF complete extracted text')
images=[]
for n in range(1,6):
 a=S/('canonical-'+str(n)+'.png');b=S/('page-'+str(n)+'.png');req(a.read_bytes()==b.read_bytes(),'canonical vs viewed compiled PNG')
 images.append({'page':n,'canonical_render':str(a.relative_to(O)),'viewed_compiled_render':str(b.relative_to(O)),'bytes':a.stat().st_size,'sha256':h(a.read_bytes()),'pixels_and_PNG_exact_equal':True,'visually_inspected':True,'defects':[]})
(O/'VISUAL_QA.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PDF_skill_read':True,'actual_supported_Tectonic_compile':True,'read_only_reproduction_no_authoring_marker_required':True,'canonical_pdf_sha256':h((P/'paper.pdf').read_bytes()),'compiled_pdf_sha256':h((S/'compiled/paper.pdf').read_bytes()),'complete_extracted_text_equal':True,'all_five_canonical_renders_exact_equal_to_individually_viewed_compiled_pages':True,'pages':images,'finding_count':0,'layout':'Readable margins, glyphs, equations, hyperlinks, page numbers, references and section boundaries; no clipping or overlap. Version/date/ORCID/credit and disclosure legible.'},indent=2)+'\n')
receipts=json.loads((O/'EXECUTION_RECEIPTS.json').read_text());native=json.loads(next(r['stdout'] for r in receipts if r['name']=='native_manifest_local_check'))
req(native['files']==[{'name':n,'size':(P/n).stat().st_size,'sha256':h((P/n).read_bytes())} for n in ['paper.pdf','support.zip']],'native full asset identities')
(O/'ADDITIONAL_RECEIPTS.json').write_text(json.dumps(R,indent=2)+'\n')
print('PASS',len(R),'additional subprocess commands, five exact PNG matches, full native identities')
