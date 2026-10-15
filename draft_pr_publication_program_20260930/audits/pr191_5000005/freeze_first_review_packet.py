"""Freeze the first credited PR191 whole-review packet, without publication."""
from pathlib import Path
import datetime,hashlib,importlib.util,json,shutil,stat,zipfile
A=Path(__file__).resolve().parent
S=A/'verification_support_v1';D=A/'publication_package_v1'
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(p,obj):p.write_text(json.dumps(obj,indent=2,ensure_ascii=True)+'\n')
def now():return datetime.datetime.now(datetime.UTC).isoformat()
require(not (A/'ROOT_WHOLE_REVIEW_INPUT_01.json').exists(),'Review packet already frozen')
require(pin(D/'parallel_short_trajectories.tex')['sha256']=='33017fb1dd9d282556b1034675525520072cb2418ef6d93096e63887285bb95d','Source drift')
require(pin(D/'parallel_short_trajectories.pdf')['sha256']=='f5a5324b3b3bd3675805d4cd3ea08859889be749978bc9cb35cc9ba79c847e61','PDF drift')
compile_receipt=json.loads((A/'ROOT_PACKAGE_COMPILE_READBACK_01.json').read_text())
require(compile_receipt['exit']==0 and compile_receipt['desktop_compiler_actual_current_source_result']=='success','Compiler failure')
visual={'UTC':now(),'status':'ROOT_CURRENT_SIX_PAGE_COMPLETE_VISUAL_INSPECTION_ACCEPTED','source':pin(D/'parallel_short_trajectories.tex'),'PDF':pin(D/'parallel_short_trajectories.pdf'),'all6_complete_pages_actually_viewed_before_compaction':True,'no_clipping_overlap_missing_glyph_or_unresolved_reference_observed':True,'renders':[{'page':i,**pin(A/f'manuscript_visual_package_v1-{i}.png')} for i in range(1,7)],'publication_ready':False}
save(A/'ROOT_PACKAGE_VISUAL_ACCEPTANCE_01.json',visual)
pv=A/'root_priority_sources_private/root_visual'
readgroups=[('Ferudun current DOI body',[2,3,5,10,11,12,13,14,15,16,17],'ferudun_{}'),('Boissy-Lanneau earlier author draft',[1,8],'boissy_lanneau_{}'),('Boissy-Lanneau arXiv v2',[8],'boissy_lanneau_arxivv2_{}'),('Veech1989 actual PDF pages12-16, printed563-567',[12,13,14,15,16],'veech1989_{}'),('Davis-Lelievre arXiv v1',[7],'davis_lelievre2018v1_{}')]
save(A/'ROOT_PRIORITY_COMPLETE_PAGE_INSPECTION_01.json',{'UTC':now(),'scope':'Twenty complete relevant primary-source pages actually visually inspected by Root before compaction; selective reading, not whole-body reading or exhaustive history. Veech printed568 was not among Root visual pages.','sources':[{'source':name,'actual_complete_pages_viewed':pages,'render_hashes':[pin(pv/(fmt.format(i)+'.png')) for i in pages]} for name,pages,fmt in readgroups],'external_bodies_or_derivatives_redistributed':False})
native=A/'integration_preparation/native_template_pending_01'
nm=json.loads((A/'integration_preparation/NATIVE_TEMPLATE_PENDING_01_MANIFEST.json').read_text())
require(len(nm['files'])==50,'Native count drift')
for n,x in nm['files'].items():require(pin(native/n)=={'bytes':x['bytes'],'sha256':x['sha256']},'Native identity drift '+n)
require(not (S/'planned_native_integration').exists(),'Native copies already present')
shutil.copytree(native,S/'planned_native_integration')
shutil.copyfile(A/'integration_preparation/NATIVE_TEMPLATE_PENDING_01_MANIFEST.json',S/'NATIVE_TEMPLATE_PENDING_01_MANIFEST.json')
(S/'paper').mkdir()
for n in ['parallel_short_trajectories.pdf','parallel_short_trajectories.tex','zenodo-deposit.json','PACKAGE_README.md']:shutil.copyfile(D/n,S/'paper'/n)
for n in ['ROOT_PACKAGE_COMPILE_READBACK_01.json','ROOT_PACKAGE_VISUAL_ACCEPTANCE_01.json','ROOT_PRIORITY_COMPLETE_PAGE_INSPECTION_01.json','ROOT_PORTABLE_VERIFICATION_RUN_01.json','PORTABLE_VERIFICATION_RUN_01.stdout.json']:shutil.copyfile(A/n,S/'audit'/n)
readme=S/'README.md';readme.write_text(readme.read_text().replace('Python3.10 or later','Python3.11 or later')+'\nThe paper/ folder contains the exact first-review manuscript and metadata. planned_native_integration/ is the frozen50-file review template with pending publication facts, not an assertion that merging or publication has happened. The archived portable run under audit/ tested the earlier96-input scientific bootstrap; the final manifest also binds later documentary copies. Python3.11 or later is required for the -P interpreter option. Final whole-package reviewers must rerun the verifier against this complete inventory.\n')
rows=[]
for q in sorted(S.rglob('*')):
 require(not q.is_symlink(),'Symlink in support')
 if q.is_file() and q.name!='MANIFEST.json':rows.append({'path':str(q.relative_to(S)),**pin(q)})
require(all(not any(x in Path(row['path']).parts for x in ['private','private_inputs','private_sources','root_priority_sources_private','root_primary_sources_private','__pycache__','.zenodo-state']) for row in rows),'Private path selected')
save(S/'MANIFEST.json',{'status':'FROZEN_FIRST_WHOLE_REVIEW_FULL_PAYLOAD_MANIFEST','UTC':now(),'files':rows,'scope':'All exact public-safe payloads except this manifest; scientific bootstrap receipt is dated history. No actual publication or merge claimed.'})
spec=importlib.util.spec_from_file_location('verify_packet',S/'verify_all.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
require(v.integrity()==len(rows),'Final inventory integrity failed')
for q in S.rglob('*'):
 if q.is_file():q.chmod(0o444)
zpath=D/'verification-package.zip'
require(not zpath.exists(),'ZIP already exists')
with zipfile.ZipFile(zpath,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for q in sorted(S.rglob('*')):
  if q.is_file():
   info=zipfile.ZipInfo('verification-package/'+str(q.relative_to(S)),date_time=(2026,10,15,0,0,0));info.create_system=3;info.external_attr=(stat.S_IFREG|0o444)<<16;info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,q.read_bytes(),compresslevel=9)
with zipfile.ZipFile(zpath) as z:
 require(z.testzip() is None,'ZIP CRC failure');require(len(z.namelist())==len(rows)+1,'ZIP inventory count drift')
 for q in sorted(S.rglob('*')):
  if q.is_file():require(z.read('verification-package/'+str(q.relative_to(S)))==q.read_bytes(),'ZIP payload drift')
outer={n:pin(D/n) for n in ['parallel_short_trajectories.pdf','parallel_short_trajectories.tex','verification-package.zip','zenodo-deposit.json','PACKAGE_README.md']}
for n in outer:(D/n).chmod(0o444)
receipt={'UTC':now(),'status':'FIRST_CREDITED_WHOLE_PACKAGE_REVIEW_INPUT_FROZEN_NOT_PUBLICATION_READY','PR':191,'original_head':'a2791bdd3f7ecd5694aeeeb5dffb21964a5639fe','original_QUEUE_status':'claimed_solved','package_version':1,'package_folder':str(D),'package_files':outer,'support_folder':str(S),'support_payload_files_excluding_manifest':len(rows),'support_manifest':pin(S/'MANIFEST.json'),'current_proof':{'path':'CURRENT_PROOF_V4.md',**pin(A/'CURRENT_PROOF_V4.md')},'native_pending_template':str(native),'native_pending_manifest':pin(A/'integration_preparation/NATIVE_TEMPLATE_PENDING_01_MANIFEST.json'),'native_files':50,'credited_qualification':'Exact prior theorem and repair credited to Ferudun, classical mechanisms credited; no novelty, firstness, present openness, authenticated author erratum or independent discovery certification.','prior_bootstrap_scientific_run':pin(A/'PORTABLE_VERIFICATION_RUN_01.stdout.json'),'final_inventory_integrity_only_passed':True,'new_fresh_whole_package_reviews_required':True,'publication_ready':False,'actual_Zenodo_published':False,'actual_DOI':None,'actual_tracker_append':False,'actual_PR_merged':False,'goal_complete':False}
save(A/'ROOT_WHOLE_REVIEW_INPUT_01.json',receipt)
for n in ['ROOT_PACKAGE_VISUAL_ACCEPTANCE_01.json','ROOT_PRIORITY_COMPLETE_PAGE_INSPECTION_01.json','ROOT_WHOLE_REVIEW_INPUT_01.json']:(A/n).chmod(0o444)
print(json.dumps({'status':receipt['status'],'support_payloads':len(rows),'ZIP':outer['verification-package.zip'],'paper':outer['parallel_short_trajectories.pdf'],'native_files':50}))
