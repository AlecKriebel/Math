#!/usr/bin/env python3
"""Reproduce artifact, full-input pins and executable diagnostics. No geometry prover."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile

ARCHIVE = ('CONNECTED_SUM_ROPELENGTH_2733_AUTHOR_SAFE_FREEZE.zip',16395,'f05d1acd29f9366fa08facff81b97e561bcadd60072584dce6037a001e273953')
EXTERNAL = ('CONNECTED_SUM_ROPELENGTH_2733_AUTHOR_EXTERNAL_MANIFEST.json',3750,'c715974ed45a383eb56086518b506887b340671025d532f3a33cf36f62cdeb44')
CORPUS = {
 'catalog.json': (21735099,'891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566'),
 'problems.json':(68931837,'04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf'),
 'research_results.json':(80334822,'8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b')}
STATEMENT='0697193ff65093da9abc34c354a747974b2dfedc0f9db20372d79336626545b7'
PAIR='3728d6f7692daadc11b003a16e89a90a49832dd78bdeb4fe0719072b0d1e81e0'
MEMBERS={'APPROACH_LOG.md','ARITHMETIC_CERTIFICATE.json','MANIFEST.json','PROOF.md','README.md','REPORT.md','SOURCE_AUDIT.json','STATUS.json','verify.py'}
PDF_NAMES=['k3.pdf','cks02.pdf','cks02_arxiv.pdf','clr12.pdf','milnor50.pdf']

def require(ok,msg):
 if not ok: raise RuntimeError(msg)
def sha(b): return hashlib.sha256(b).hexdigest()
def unique(pairs):
 d={}
 for k,v in pairs:
  require(k not in d,'Duplicate key: '+k);d[k]=v
 return d
def parse(b):
 def bad(v): raise ValueError('Nonfinite JSON: '+v)
 return json.loads(b,object_pairs_hook=unique,parse_constant=bad)
def write(p,obj): p.write_text(json.dumps(obj,sort_keys=True,indent=2)+'\n',encoding='utf-8')
def pin(path,size,digest):
 b=path.read_bytes();require(len(b)==size and sha(b)==digest,'Pin mismatch: '+path.name)
 return {'name':path.name,'bytes':len(b),'sha256':sha(b),'match':True}
def rehash(root,name):
 p=root/'MANIFEST.json';m=json.loads(p.read_text());b=(root/name).read_bytes()
 for e in m['members']:
  if e['name']==name: e.update(bytes=len(b),sha256=sha(b))
 write(p,m)
def edit(root,name,fn):
 p=root/name;d=json.loads(p.read_text());fn(d);write(p,d);rehash(root,name)
def mutate(root,which):
 if which=='tampered_proof': (root/'PROOF.md').write_bytes((root/'PROOF.md').read_bytes()+b'\nchanged\n')
 elif which=='missing_file': (root/'PROOF.md').unlink()
 elif which=='unexpected_file': (root/'extra.txt').write_text('unexpected\n')
 elif which=='malformed_manifest': (root/'MANIFEST.json').write_text('{bad')
 elif which=='duplicate_manifest_key':
  p=root/'MANIFEST.json';p.write_text(p.read_text().replace('{','{"schema_version":1,',1))
 elif which=='symlink_payload':
  p=root/'PROOF.md';p.unlink();p.symlink_to('README.md')
 elif which=='rehashed_false_resolution': edit(root,'STATUS.json',lambda d:d.update(intended_nontrivial_part_a='proved'))
 elif which=='rehashed_wrong_splice': edit(root,'ARITHMETIC_CERTIFICATE.json',lambda d:d['splice_numerator_polynomial'].update({'delta*S':1}))
 elif which=='rehashed_wrong_problem_id': edit(root,'STATUS.json',lambda d:d.update(problem_id=2734))
 elif which=='rehashed_nonfinite_json':
  p=root/'ARITHMETIC_CERTIFICATE.json';p.write_text(p.read_text().replace('"pi_strict_lower_bound": 3','"pi_strict_lower_bound": NaN'));rehash(root,p.name)
 elif which=='rehashed_boolean_coefficient': edit(root,'ARITHMETIC_CERTIFICATE.json',lambda d:d['unknot_ropelength'].update(pi=True))
 elif which=='rehashed_duplicate_status_key':
  p=root/'STATUS.json';p.write_text(p.read_text().replace('{','{"problem_id":2733,',1));rehash(root,p.name)
 elif which=='duplicate_manifest_member':
  p=root/'MANIFEST.json';m=json.loads(p.read_text());m['members'][1]=m['members'][0].copy();write(p,m)
 elif which=='invalid_hash_syntax':
  p=root/'MANIFEST.json';m=json.loads(p.read_text());m['members'][0]['sha256']='g'*64;write(p,m)
 else: raise RuntimeError('Unknown mutation')

MUTATIONS=['tampered_proof','missing_file','unexpected_file','malformed_manifest','duplicate_manifest_key','symlink_payload','rehashed_false_resolution','rehashed_wrong_splice','rehashed_wrong_problem_id','rehashed_nonfinite_json','rehashed_boolean_coefficient','rehashed_duplicate_status_key','duplicate_manifest_member','invalid_hash_syntax']

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--archive',required=True,type=Path);ap.add_argument('--external-manifest',required=True,type=Path);ap.add_argument('--output',required=True,type=Path)
 for n in ['catalog','problems','research-results','source-dir']: ap.add_argument('--'+n,type=Path)
 a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=True)
 artifact={'archive':pin(a.archive,*ARCHIVE[1:]),'external_manifest':pin(a.external_manifest,*EXTERNAL[1:]),'members':[]}
 ext=parse(a.external_manifest.read_bytes());require(ext['archive']=={'name':ARCHIVE[0],'bytes':ARCHIVE[1],'sha256':ARCHIVE[2]},'External archive record mismatch')
 with zipfile.ZipFile(a.archive) as z:
  infos=z.infolist();require(len(infos)==9 and {x.filename for x in infos}==MEMBERS,'Archive member set mismatch')
  for i in infos:
   require(not i.is_dir() and '/' not in i.filename and '\\' not in i.filename,'Unsafe archive name')
   kind=stat.S_IFMT(i.external_attr>>16);require(kind in (0,stat.S_IFREG),'Nonregular archive entry')
  contents={i.filename:z.read(i.filename) for i in infos}
 entries=ext['members'];require(len(entries)==9 and {e['name'] for e in entries}==MEMBERS,'External coverage mismatch')
 for e in entries:
  b=contents[e['name']];require(len(b)==e['bytes'] and sha(b)==e['sha256'],'External member mismatch')
  artifact['members'].append(dict(e,match=True))
 im=parse(contents['MANIFEST.json']);require({e['name'] for e in im['members']}==MEMBERS-{'MANIFEST.json'} and len(im['members'])==8,'Internal coverage mismatch')
 for e in im['members']:
  b=contents[e['name']];require(len(b)==e['bytes'] and sha(b)==e['sha256'],'Internal member mismatch')
 artifact.update(archive_names_safe=True,regular_members=True,duplicate_names=False,internal_manifest_matches=True)
 write(a.output/'ARTIFACT_VERIFICATION.json',artifact)
 source=parse(contents['SOURCE_AUDIT.json'])
 if any([a.catalog,a.problems,a.research_results]):
  require(all([a.catalog,a.problems,a.research_results]),'All three full corpus inputs required')
  data={};checks=[]
  for name,p in [('catalog.json',a.catalog),('problems.json',a.problems),('research_results.json',a.research_results)]:
   checks.append(pin(p,*CORPUS[name]));data[name]=parse(p.read_bytes())
  cats=[r for r in data['catalog.json'] if str(r['id'])=='2733'];probs=[r for r in data['problems.json'] if r['id']==2733]
  require(len(cats)==len(probs)==1,'Exact ID not unique');c,p=cats[0],probs[0];reports=data['research_results.json'];r=reports.get(p['problem_number'],{})
  hstatement=sha(p['statement'].encode());hp=sha(json.dumps([p,r],sort_keys=True).encode())
  require(p['problem_number']==c['problem_number']=='KP-1.74' and c['rank']==907,'ID/number/rank mismatch')
  require(hstatement==STATEMENT==c['statement_hash'] and hp==PAIR==c['review_hash'],'Selected record pin mismatch')
  require(source['selected_record_verification']['statement_sha256']==hstatement and source['selected_record_verification']['pair_sha256']==hp,'Authored selected metadata mismatch')
  require(r=={},'Unexpected substantive inherited report')
  require('LITERATURE-TRIAGE:BEGIN' in p['background'] and 'OPEN-TRIAGE' in p['background'],'Triage background marker missing')
  write(a.output/'CORPUS_VERIFICATION.json',{'result':'PASS','inputs':checks,'catalog_records':len(data['catalog.json']),'problem_records':len(data['problems.json']),'report_records':len(reports),'selected_id':2733,'problem_number':'KP-1.74','rank':907,'id_unique_in_catalog_and_problems':True,'statement_sha256':hstatement,'complete_problem_report_pair_sha256':hp,'pair_serialization':'json.dumps([complete_problem_record,reports.get(problem_number,{})],sort_keys=True) with Python defaults; UTF-8 bytes','report_key_present':'KP-1.74' in reports,'report_empty':r=={},'background_has_literature_triage':True,'no_dataset_text_emitted':True})
 if a.source_dir:
  pdfs=[]
  for name,meta in zip(PDF_NAMES,source['pdf_retrievals']):
   p=a.source_dir/name;entry=pin(p,meta['bytes'],meta['sha256']);info=subprocess.run(['pdfinfo',str(p)],capture_output=True,text=True,check=True).stdout
   pages=int(next(line.split(':')[1] for line in info.splitlines() if line.startswith('Pages:')))
   require(pages==meta['pages'],'PDF page-count mismatch')
   entry.update(title=meta['title'],url=meta['url'],pages=pages,redistributed=False);pdfs.append(entry)
  write(a.output/'PDF_VERIFICATION.json',{'result':'PASS','pdfs':pdfs,'scope':'Local PDF bytes and page counts independently recomputed; semantic inspection documented separately.'})
 modes=[[],['-O'],['-OO']];baselines=[];neg=[]
 with tempfile.TemporaryDirectory(prefix='ropelength-independent-') as td:
  work=Path(td);pkg=work/'relocated package with spaces';pkg.mkdir()
  for n,b in contents.items(): (pkg/n).write_bytes(b)
  elsewhere=work/'unrelated cwd';elsewhere.mkdir()
  env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
  for flags in modes:
   for invocation in ['implicit_root','explicit_root']:
    cmd=[sys.executable,*flags,str(pkg/'verify.py')]+([str(pkg)] if invocation=='explicit_root' else [])
    r=subprocess.run(cmd,cwd=elsewhere,env=env,capture_output=True,text=True,timeout=30)
    require(r.returncode==0,'Baseline failed');o=parse(r.stdout);require(o['result']=='PASS' and o['intended_part_a']=='unresolved' and o['part_b']=='unresolved','Unexpected baseline output')
    baselines.append({'flags':flags,'invocation':invocation,'relocated':True,'unrelated_cwd':True,'exit_code':r.returncode,'stdout':o,'stderr':r.stderr.strip()})
  for which in MUTATIONS:
   target=work/which;shutil.copytree(pkg,target);mutate(target,which)
   for flags in modes:
    r=subprocess.run([sys.executable,*flags,str(target/'verify.py')],cwd=elsewhere,env=env,capture_output=True,text=True,timeout=30)
    require(r.returncode!=0 and r.stderr.startswith('FAIL:'),'Mutation not fail-closed: '+which)
    neg.append({'mutation':which,'flags':flags,'exit_code':r.returncode,'stderr':r.stderr.strip(),'failed_closed':True})
  unchanged={p.name:p.read_bytes() for p in pkg.iterdir()};require(unchanged==contents,'Clean replay package changed')
 write(a.output/'REPLAY_RESULTS.json',{'result':'PASS','baseline_runs':baselines,'mutation_case_count':len(MUTATIONS),'mutation_runs':neg,'mutation_run_count':len(neg),'all_negative_tests_failed_closed':True,'clean_extracted_package_unchanged':True,'scope':'Integrity and exact polynomial arithmetic only; geometry/topology audited in separate written report. Freshly rehashed arbitrary prose is not semantically certified by author verifier; exact artifact pins remain the trust boundary.'})
 # Recheck both originals after all tests.
 pin(a.archive,*ARCHIVE[1:]);pin(a.external_manifest,*EXTERNAL[1:])
 print(json.dumps({'result':'PASS','archive_sha256':ARCHIVE[2],'external_manifest_sha256':EXTERNAL[2],'baseline_runs':len(baselines),'mutation_cases':len(MUTATIONS),'mutation_runs':len(neg),'original_pins_unchanged':True},sort_keys=True))

if __name__=='__main__':
 try: main()
 except Exception as e:
  print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
