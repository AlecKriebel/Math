#!/usr/bin/env python3
"""Local review runner. All mutations and outputs remain under this review dir."""
from pathlib import Path
import subprocess,hashlib,json,datetime,shutil,sys,os,zipfile,stat,re,warnings
R=Path(__file__).resolve().parent;A=R.parents[1];P=A/'preprint_v1_0';K=P/'kit'
LOG=[]
def h(b):return hashlib.sha256(b).hexdigest()
def require(v,m):
 if not v:raise RuntimeError(m)
def run(name,cmd,cwd=R,want=0):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 proc=subprocess.run(cmd,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=90,env={'PATH':os.environ['PATH'],'PYTHONDONTWRITEBYTECODE':'1','LANG':'C.UTF-8'})
 for kind,data in [('stdout',proc.stdout),('stderr',proc.stderr)]: (R/'receipts'/f'{name}.{kind}').write_bytes(data)
 row={'name':name,'argv':list(map(str,cmd)),'cwd':str(cwd),'started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'returncode':proc.returncode,'expected':want,'stdout_bytes':len(proc.stdout),'stdout_sha256':h(proc.stdout),'stderr_bytes':len(proc.stderr),'stderr_sha256':h(proc.stderr)}
 row['expectation_met']=(proc.returncode==0 if want==0 else proc.returncode!=0)
 LOG.append(row)
 (R/'COMMAND_RUNS.json').write_text(json.dumps(LOG,indent=2)+'\n')
 require(row['expectation_met'],f'{name} return {proc.returncode} expected {want}')
 return proc

def copycase(name):
 d=R/'scratch'/name
 if d.exists():raise RuntimeError('refuse overwrite case '+name)
 shutil.copytree(K,d);return d

def repin(d):
 p=d/'MANIFEST.json';v=json.loads(p.read_text())
 for row in v['files']:
  b=(d/row['path']).read_bytes();row.update(bytes=len(b),sha256=h(b))
 p.write_text(json.dumps(v,indent=2)+'\n')

modes={'normal':[],'O':['-O'],'OO':['-OO']}
# Canonical source is only read, never imported into a cache-writing interpreter.
for mode,opts in modes.items():run('canonical_'+mode,[sys.executable,'-I','-B',*opts,str(K/'scripts/verify_kit.py'),'--archive',str(P/'pr1032_supportkit_v1.0.zip')])
C=R/'scratch'/'cold_extract';C.mkdir()
with zipfile.ZipFile(P/'pr1032_supportkit_v1.0.zip') as z:z.extractall(C)
for mode,opts in modes.items():run('cold_'+mode,[sys.executable,'-I','-B',*opts,str(C/'scripts/verify_kit.py')])
# Rebuild outside package and refuse existing target.
archive=R/'scratch'/'rebuilt.zip'
run('archive_outside',[sys.executable,'-I','-B',str(K/'scripts/build_archive.py'),str(archive)])
require(archive.read_bytes()==(P/'pr1032_supportkit_v1.0.zip').read_bytes(),'deterministic rebuild mismatch')
run('archive_existing_refusal',[sys.executable,'-I','-B',str(K/'scripts/build_archive.py'),str(archive)],want=1)
# Hostile genuine input changes, both integrity and re-pinned semantic probes.
cases=[]
d=copycase('byte_tamper');(d/'README.md').write_text((d/'README.md').read_text()+'\nAltered byte control.\n');cases.append(('byte_tamper',d))
d=copycase('unlisted');(d/'extra.txt').write_text('unlisted control');cases.append(('unlisted',d))
d=copycase('missing');(d/'CITATION.bib').unlink();cases.append(('missing',d))
d=copycase('symlink');(d/'unlisted-link').symlink_to('README.md');cases.append(('symlink',d))
d=copycase('repinned_readiness');p=d/'STATUS.json';v=json.loads(p.read_text());v['publication_ready']=True;p.write_text(json.dumps(v));repin(d);cases.append(('repinned_readiness',d))
d=copycase('repinned_priority');p=d/'STATUS.json';v=json.loads(p.read_text());v['priority_overlap_Luo_Zha']='CLEARED';p.write_text(json.dumps(v));repin(d);cases.append(('repinned_priority',d))
d=copycase('repinned_endpoint');p=d/'scripts/check_analytic_independent.py';t=p.read_text();require("'C': (3, 3)" in t,'endpoint control trigger');p.write_text(t.replace("'C': (3, 3)","'C': (3, 4)",1));repin(d);cases.append(('repinned_endpoint',d))
d=copycase('repinned_table');p=d/'paper.tex';t=p.read_text();trigger='$(A,B)$ & $(A,B),(A,D)$';require(trigger in t,'table control trigger');p.write_text(t.replace(trigger,'$(A,B)$ & $(A,B)$',1));repin(d);cases.append(('repinned_table',d))
d=copycase('repinned_expected');p=d/'EXPECTED_RESULTS.json';v=json.loads(p.read_text());v['check_analytic_independent.py']['sha256']='0'*64;p.write_text(json.dumps(v));repin(d);cases.append(('repinned_expected',d))
for name,d in cases:
 for mode,opts in modes.items():run(name+'_'+mode,[sys.executable,'-I','-B',*opts,str(d/'scripts/verify_kit.py')],want=1)
# Archive structure probes against canonical kit. No unsafe archive is extracted.
base=P/'pr1032_supportkit_v1.0.zip'
for kind in ['traversal','duplicate','symlink','bad_timestamp','unexpected']:
 target=R/'scratch'/('hostile_'+kind+'.zip')
 with zipfile.ZipFile(base) as src,zipfile.ZipFile(target,'x') as dst:
  for entry in src.infolist():dst.writestr(entry,src.read(entry))
  if kind=='traversal':dst.writestr('../escape.txt','control')
  elif kind=='duplicate':
   with warnings.catch_warnings():warnings.simplefilter('ignore');dst.writestr('README.md','duplicate control')
  elif kind=='symlink':
   info=zipfile.ZipInfo('fake-link',(2026,10,16,0,0,0));info.create_system=3;info.external_attr=(stat.S_IFLNK|0o777)<<16;dst.writestr(info,'README.md')
  elif kind=='bad_timestamp':
   info=zipfile.ZipInfo('bad-time',(2025,1,1,0,0,0));dst.writestr(info,'control')
  elif kind=='unexpected':
   info=zipfile.ZipInfo('extra.txt',(2026,10,16,0,0,0));info.create_system=3;info.external_attr=(stat.S_IFREG|0o644)<<16;dst.writestr(info,'control')
 for mode,opts in modes.items():run('archive_'+kind+'_'+mode,[sys.executable,'-I','-B',*opts,str(K/'scripts/verify_kit.py'),'--archive',str(target)],want=1)
# Independently reproduce the documented natural TARGET failure, on disposable kit.
d=copycase('builder_inside')
run('inside_before',[sys.executable,'-I','-B',str(d/'scripts/verify_kit.py')])
run('builder_inside_succeeds',[sys.executable,'-I','-B',str(d/'scripts/build_archive.py'),'inside.zip'],cwd=d)
require((d/'inside.zip').is_file(),'no output from inside builder')
for mode,opts in modes.items():run('inside_after_'+mode,[sys.executable,'-I','-B',*opts,str(d/'scripts/verify_kit.py')],want=1)
# Native local check only. No token lookup, network client, remote API, or state write.
N=Path('/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py')
for name,manifest in [('preprint',P/'zenodo-deposit.json'),('repository',A/'publication/zenodo-deposit.json')]:
 proc=run('native_'+name,[sys.executable,'-I','-B',str(N),'check',str(manifest)])
 v=json.loads(proc.stdout);require(v['title']==json.loads((P/'.zenodo.json').read_text())['title'],'native title mismatch')
 require([(f['name'],f['size'],f['sha256']) for f in v['files']]==[('paper.pdf',106270,'83fa69dab776cc423218281959b2600a7dbc87decf97ad8ea9b21eb2dd6f7300'),('pr1032_supportkit_v1.0.zip',357557,'c2fc98f158cfad4e8b9b11def0da06e9e5f4acd74ea27f877401e6968741bcdd')],'native objects differ')
# Independently inspect every archive member, manifest row, copy, bibliography object.
with zipfile.ZipFile(base) as z:
 infos=z.infolist();require(len(infos)==34,'archive count');names=z.namelist()
 require(names==sorted(names),'archive order');require(len(names)==len(set(names)),'duplicate')
 require(all(z.read(n)==(K/n).read_bytes() for n in names),'archive member bytes')
 require(all(not n.startswith('/') and '..' not in Path(n).parts and not n.endswith('.zip') for n in names),'member scope')
 require(all(not ('/sources/raw' in n or '/receipts/' in n or 'fixture' in n or n.endswith('.png')) for n in names),'private member class')
for row in json.loads((K/'COPY_MAP.json').read_text()):
 source=A/row['original_relative_to_audit'];dest=K/row['copy_relative_to_kit'];require(source.read_bytes()==dest.read_bytes(),'copy mismatch '+str(source))
 require(len(dest.read_bytes())==row['bytes'] and h(dest.read_bytes())==row['sha256'],'copy identity')
meta=json.loads((P/'.zenodo.json').read_text());deposit=json.loads((P/'zenodo-deposit.json').read_text());repo=json.loads((A/'publication/zenodo-deposit.json').read_text())
require(meta==deposit['metadata']==repo['metadata']==json.loads((K/'.zenodo.json').read_text()),'metadata semantic equality')
for name in ['paper.tex','paper.pdf','CITATION.bib','STATUS.json']:
 require((P/name).read_bytes()==(K/name).read_bytes(),'top/kit mismatch '+name)
tex=(P/'paper.tex').read_text();bib=json.loads((K/'BIBLIOGRAPHIC_OBJECTS.json').read_text())
parsed=dict(re.findall(r'\\bibitem\{(.*?)\}\s*(.*?)(?=\n\\bibitem|\n\\end\{thebibliography\})',tex,re.S))
require(len(parsed)==14,'bib count')
require(all(parsed[x['key']].strip()==x['tex_bibliographic_object'].strip() for x in bib['items']),'bib mismatch')
require('doi' not in meta and 'prereserve_doi' not in meta,'invented DOI key')
summary={'status':'COMPLETED_WITH_ONE_ACTIONABLE_P3_BUILDER_FINDING','commands':len(LOG),'all_expectations_met':all(x['expectation_met'] for x in LOG),'diagnostics_per_verifier_success':15,'canonical_verifications':3,'cold_verifications':3,'negative_cases':len(cases),'archive_structure_controls':5,'builder_inside_reproduced':True,'native_local_checks':2,'network_calls':0,'credentials_read':False,'native_uploader_sha256':h(N.read_bytes()),'archive_bytes':base.stat().st_size,'archive_sha256':h(base.read_bytes()),'members':34,'copies_verified':16,'bibliography_objects':14,'publication_ready':False}
(R/'PACKAGE_RESULTS.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
