#!/usr/bin/env python3
"""Read-only integrity audit of byte-frozen final package; writes only own folder."""
from pathlib import Path,PurePosixPath
from datetime import datetime,timezone
from hashlib import sha256
from zipfile import ZipFile
import json,subprocess,sys,io
ROOT=Path(__file__).resolve().parent
PUB=ROOT.parents[1]/'publication'
AUD=PUB.parent
TMP=ROOT/'tmp';TMP.mkdir(exist_ok=True)
checks=[]
def check(ok,label):
 if not ok:raise RuntimeError(label)
 checks.append(label)
def digest(b):return {'bytes':len(b),'sha256':sha256(b).hexdigest()}
def readzip(raw,name):
 z=ZipFile(io.BytesIO(raw));infos=z.infolist();names=[v.filename for v in infos]
 check(len(names)==len(set(names)),name+' no duplicate names')
 check(len(names)==len(set(n.casefold() for n in names)),name+' no case collisions')
 for inf in infos:
  n=PurePosixPath(inf.filename)
  check(not n.is_absolute() and '..' not in n.parts and '\\' not in inf.filename,name+' safe path '+inf.filename)
  check(not inf.is_dir(),name+' no extraneous directories')
  check(not inf.flag_bits&1,name+' unencrypted')
  check((inf.external_attr>>16)&0o170000!=0o120000,name+' no symbolic link')
  check(inf.file_size<1_000_000,name+' bounded authored member size')
 check(z.testzip() is None,name+' CRCs')
 return {n:z.read(n) for n in names}
receipt=json.loads((PUB/'PACKAGE_RECEIPT.json').read_bytes())
for n,info in receipt['files'].items():check(digest((PUB/n).read_bytes())==info,'receipt '+n)
pinned={'output/pdf/negative-curvature-cone.pdf':'ad9864c08642737e4459673749c1db6d2e3dafb521f323fb1071f157f8110eb0','output/negative-curvature-cone-source-and-verification.zip':'d97ba7ed1057518e3bd499d88182c64767e912d589ed8574092c0ebc7a27c06e','output/zenodo-upload-kit.zip':'0f52fdfc42cc83e4739ca5de9cabda5120565c3d48cbb4457a0da9ab7ce1bd76'}
for n,h in pinned.items():check(digest((PUB/n).read_bytes())['sha256']==h,'task pinned '+n)
source=readzip((PUB/'output/negative-curvature-cone-source-and-verification.zip').read_bytes(),'source')
manifest=json.loads(source['SOURCE_MANIFEST.json'])
check(set(manifest)==set(source)-{'SOURCE_MANIFEST.json'},'manifest exact scope')
check(manifest==receipt['source_members'],'receipt exact manifest')
for n,h in manifest.items():check(digest(source[n])==h,'source member exact hash '+n)
expected={'LICENSE.txt','PROVENANCE.json','README.md','SOURCE_MANIFEST.json','main.tex','output/pdf/negative-curvature-cone.pdf','verification/check_geometry.py','verification/curvature_reproduction.py','verification/expected_results.json','audits/ROOT_MATHEMATICAL_CHECK.md','audits/ROOT_PRIORITY_CHECK.md','audits/curvature_01/ADVERSARIAL_REPORT.md','audits/curvature_01/execution.json','audits/curvature_01/results.json','audits/geometry_01/REPORT.md','audits/geometry_01/SOURCES.json','audits/geometry_01/results.json','audits/geometry_01/results_optimized.json','audits/priority_01/PRIORITY_AUDIT.md','audits/priority_01/SEARCH_LEDGER.md','audits/priority_01/SOURCE_LEDGER.json','audits/priority_01/SOURCE_LEDGER.md','audits/priority_01/additional_retrieval_metadata.json','audits/priority_01/remainder_check.txt','audits/priority_01/retrieval_metadata.json','audits/priority_01/supplemental_retrieval_metadata.json'}
check(set(source)==expected,'source exact 26-member membership')
for n in ['LICENSE.txt','README.md','main.tex','output/pdf/negative-curvature-cone.pdf','verification/check_geometry.py','verification/curvature_reproduction.py','verification/expected_results.json']:check(source[n]==(PUB/n).read_bytes(),'archive equals distributed '+n)
for n in source:
 if n.startswith('audits/'):
  rel=n[len('audits/'):]
  path=AUD/rel if rel.startswith('ROOT_') else AUD/'reviews'/rel
  check(source[n]==path.read_bytes(),'bundled audit equals frozen input '+n)
prov=json.loads(source['PROVENANCE.json'])
check(prov['source_head_sha']=='148130ab93ab46a3459d7bc98a11a1ca79052d65','provenance source head')
check(prov['problem_id']==30003439 and prov['problem_alias']=='OWR-15219-008','provenance target')
check(prov['source_pr']=='https://github.com/AlecKriebel/Math/pull/1108','provenance source PR')
check(prov['source_proof_sha256']==sha256((AUD/'input/PROOF.md').read_bytes()).hexdigest(),'provenance original proof exact input')
original_manifest=json.loads((AUD/'input/MANIFEST.json').read_bytes())
for item in original_manifest['entries']:check(digest((AUD/'input'/item['file']).read_bytes())=={k:item[k]for k in ('bytes','sha256')},'frozen original manifest '+item['file'])
for item in json.loads((AUD/'input/RETRIEVAL_RECEIPT.json').read_bytes())['files']:check(digest((AUD/'input'/item['file']).read_bytes())=={k:item[k]for k in ('bytes','sha256')},'original retrieval receipt '+item['file'])
meta=json.loads((PUB/'zenodo-metadata.json').read_bytes());deposit=json.loads((PUB/'zenodo-deposit.json').read_bytes())
check(deposit['metadata']==meta,'metadata equals deposit metadata')
check(meta['creators']==[{'name':'Kriebel, Alec','affiliation':'Independent researcher','orcid':'0009-0001-9320-500X'}],'author and ORCID exact')
check(meta['license']=='cc-by-4.0' and meta['access_right']=='open','license open CC-BY4')
check(meta['publication_type']=='preprint' and meta['upload_type']=='publication','preprint resource type')
check(meta['publication_date']=='2026-10-17' and meta['version']=='1.0.0','version and date')
check('AI tools were used extensively' in meta['description'] and 'Unrefereed' in meta['description'] and 'no external human peer review' in meta['description'],'metadata disclosure')
check('every-regular-cone' in meta['description'] and 'first-ever priority' in meta['description'] and 'Hildebrand' in meta['description'] and 'Roy–Xiao' in meta['description'],'metadata bounded theorem and priority scope')
kit=readzip((PUB/'output/zenodo-upload-kit.zip').read_bytes(),'kit')
check(set(kit)=={'README.md','negative-curvature-cone.pdf','negative-curvature-cone-source-and-verification.zip','zenodo-metadata.json','zenodo-deposit.json'},'kit exact membership')
for n,raw in [('negative-curvature-cone.pdf',(PUB/'output/pdf/negative-curvature-cone.pdf').read_bytes()),('negative-curvature-cone-source-and-verification.zip',(PUB/'output/negative-curvature-cone-source-and-verification.zip').read_bytes()),('zenodo-metadata.json',(PUB/'zenodo-metadata.json').read_bytes()),('README.md',(PUB/'README.md').read_bytes())]:check(kit[n]==raw,'kit exact bytes '+n)
portable=json.loads(kit['zenodo-deposit.json']);check(portable['metadata']==meta,'kit portable metadata')
check(set(portable)==set(deposit),'portable deposit keys')
check(portable['files']==[{'path':'negative-curvature-cone.pdf'},{'path':'negative-curvature-cone-source-and-verification.zip'}],'kit portable upload file paths')
for k in portable:
 if k!='files':check(portable[k]==deposit[k],'portable deposit field '+k)
for n,raw in source.items():
 out=TMP/'unpacked'/n;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(raw)
# Execute the ACTUAL archived scripts, no imports from repository-local paths.
executions=[]
expected_result=json.loads(source['verification/expected_results.json'])
for script,opt,key in [('check_geometry.py',False,'geometry'),('check_geometry.py',True,'geometry'),('curvature_reproduction.py',False,'curvature'),('curvature_reproduction.py',True,None)]:
 args=[sys.executable,'-B']+(['-O']if opt else[])+[str(TMP/'unpacked/verification'/script)]
 run=subprocess.run(args,capture_output=True,text=True)
 label=script+('_optimized'if opt else '_normal')
 (TMP/(label+'.stdout')).write_text(run.stdout);(TMP/(label+'.stderr')).write_text(run.stderr)
 entry={'script':script,'optimized':opt,'returncode':run.returncode}
 if key:
  check(run.returncode==0,'archived execution '+label);result=json.loads(run.stdout)
  stable={k:v for k,v in result.items()if k not in ({'checked_at_utc','python_version','optimization_mode'}if key=='geometry'else{'python'})}
  check(stable==expected_result[key],'stable expected output '+label)
  entry['status']=result.get('status');entry['checks_run']=result.get('checks_passed');entry['mixed_log_jets']=result.get('independent_bivariate_logarithm_series_contractions');entry['rational_grid_cases']=result.get('rational_grid_cases');entry['stdout_file']=str(TMP/(label+'.stdout'))
 else:check(run.returncode!=0 and 'requires enabled assertions' in run.stderr.lower(),'optimized curvature rejects');entry['guard']='rejected at startup'
 executions.append(entry)
result={'status':'PASS','timestamp_utc':datetime.now(timezone.utc).isoformat(),'checks':len(checks),'source_member_count':len(source),'source_members':sorted(source),'kit_members':sorted(kit),'pinned_sha256':pinned,'provenance':prov,'archived_verifier_executions':executions,'metadata':meta,'notes':['No frozen package writes; source and kit members extracted only under this review tmp.','All hashes and sizes checked, not only filenames.','No prior package_round1 report consulted.']}
(ROOT/'package_integrity_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items()if k not in {'metadata','source_members'}},indent=2))
