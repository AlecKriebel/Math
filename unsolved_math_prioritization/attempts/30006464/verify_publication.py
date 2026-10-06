#!/usr/bin/env python3
"""Strict publication integrity and immutable-packet replay before acceptance."""
import argparse,hashlib,json,os,stat,subprocess,sys,zipfile
from pathlib import Path,PurePosixPath
PINS={
 'author':('SHORT_CUSP_30006464_AUTHOR_SAFE_FREEZE.zip',16713,'29e8aa1e0ffe71c40132a437da8ce8d442032aaf330a73d144048899fc78b675',12,'8c9aa06e0920943b23c258c8b426408f8d18435f0dec32d454f5f47473650184'),
 'audit':('SHORT_CUSP_30006464_INDEPENDENT_AUDIT_SAFE.zip',40185,'c06c5fee1cab394b20cf092cba90ac5c34c98e8230430ac6c5f8f415fab12e27',24,'ea2d30ea3797e59844467738de3f24f75fda1014efc61d73dbbee3f5a94b474b')}
DIRS={'archives','author','audit','audit/AUTHOR'}
ROOT_FILES={'README.md','RESEARCH_LOG.md','SOURCE_CORPUS_CHECKS.json','QUEUE_DELTA.json','PUBLICATION_METADATA.json','PUBLICATION_MANIFEST.json','PUBLICATION_TEST_RESULTS.json','PATCH_TEST_RESULTS.json','verify_publication.py','test_publication.py','test_patch.py'}
def need(ok,msg):
 if not ok:raise ValueError(msg)
def digest(b):return hashlib.sha256(b).hexdigest()
def unique(pairs):
 out={}
 for k,v in pairs:need(k not in out,'duplicate JSON key: '+k);out[k]=v
 return out
def js(b):return json.loads(b,object_pairs_hook=unique)
def inventory(root):
 for p in [root,*root.parents]:need(stat.S_ISDIR(p.lstat().st_mode),'nonregular invocation ancestry')
 files={};dirs=set()
 for current,ds,fs in os.walk(root,followlinks=False):
  for n in ds+fs:
   p=Path(current)/n;name=p.relative_to(root).as_posix();mode=p.lstat().st_mode
   if stat.S_ISDIR(mode):dirs.add(name)
   else:need(stat.S_ISREG(mode),'nonregular entry: '+name);files[name]=p
 need(dirs==DIRS,'directory inventory mismatch')
 need({n for n in files if '/' not in n}==ROOT_FILES,'root inventory mismatch')
 return files
def execute(root,path,optimized=False):
 r=subprocess.run([sys.executable,'-I','-B']+(['-O'] if optimized else [])+[str(root/path)],cwd=root.parent,text=True,capture_output=True,timeout=600)
 need(r.returncode==0,'replay failure: '+path+' '+r.stderr);result=js(r.stdout);need(result.get('status') in ('PASS','pass'),'nonpass replay: '+path);return result

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--expected-manifest',required=True);ap.add_argument('--integrity-only',action='store_true');a=ap.parse_args()
 root=Path(__file__).absolute().parent;files=inventory(root)
 raw=files['PUBLICATION_MANIFEST.json'].read_bytes();need(digest(raw)==a.expected_manifest,'external manifest pin mismatch');m=js(raw)
 need(set(m)=={'schema','files'} and m['schema']=='short-cusp-publication-v1','manifest schema')
 need(set(m['files'])==set(files)-{'PUBLICATION_MANIFEST.json'},'manifest inventory mismatch')
 for name,meta in m['files'].items():
  need(set(meta)=={'bytes','sha256'} and type(meta['bytes']) is int and meta['bytes']>=0,'manifest entry schema');b=files[name].read_bytes();need((len(b),digest(b))==(meta['bytes'],meta['sha256']),'manifest bytes: '+name)
 for folder,(name,size,sha,count,msha) in PINS.items():
  b=files['archives/'+name].read_bytes();need((len(b),digest(b))==(size,sha),'immutable archive pin')
  need(digest(files[folder+'/MANIFEST.json'].read_bytes())==msha,'immutable manifest pin')
  with zipfile.ZipFile(files['archives/'+name]) as z:
   infos=z.infolist();names=[i.filename for i in infos];need(len(names)==len(set(names))==count,'archive count')
   need({folder+'/'+n for n in names}=={n for n in files if n.startswith(folder+'/')},'archive inventory mismatch')
   for info in infos:
    p=PurePosixPath(info.filename);need(not p.is_absolute() and '..' not in p.parts and str(p)==info.filename and not info.is_dir() and stat.S_IFMT(info.external_attr>>16) in (0,stat.S_IFREG),'unsafe archive entry')
    need(z.read(info)==files[folder+'/'+info.filename].read_bytes(),'frozen member mismatch: '+folder+'/'+info.filename)
 for n in [n[7:] for n in files if n.startswith('author/')]:need(files['author/'+n].read_bytes()==files['audit/AUTHOR/'+n].read_bytes(),'nested author copy mismatch')
 meta=js(files['PUBLICATION_METADATA.json'].read_bytes())
 need(meta['problem_id']==30006464 and meta['problem_number']=='OWR-14299577-017' and meta['rank']==831 and meta['status']=='unsolved' and meta['approaches_used']==5 and meta['full_resolution'] is False,'publication resolution scope')
 need(meta['verdict']=='accepted_scoped_partial_with_operative_zero_dimension_correction' and meta['operative_correction']=='audit/GRAM_ZERO_DIMENSION.patch' and meta['correction_binding']=='audit/CORRECTION.json' and meta['precision_addendum']=='audit/PRECISION_ADDENDUM.md','operative correction binding')
 need(meta['original_archives_and_members_unchanged'] is True and meta['corrected_derivative_published'] is False and meta['no_novelty_or_priority_claim'] is True and meta['no_human_peer_review_claim'] is True,'publication nonclaims')
 need(meta['archives']==[{'folder':f,'filename':n,'bytes':s,'sha256':h,'members':c} for f,(n,s,h,c,mh) in PINS.items()],'publication archive metadata')
 q=js(files['QUEUE_DELTA.json'].read_bytes());need(q['changed_cells']==['Status','Turns'] and q['all_other_bytes_unchanged'] is True and q['path']=='unsolved_math_prioritization/QUEUE.md','queue delta scope')
 old=q['old_row'].split('|');new=q['new_row'].split('|');need(len(old)==len(new)==14 and old[1].strip()=='831' and old[2].strip()=='30006464 / OWR-14299577-017','queue row identity');need([i for i,(x,y) in enumerate(zip(old,new)) if x!=y]==[8,9] and old[8]==' queued ' and old[9]==' 0/5 ' and new[8]==' unsolved ' and new[9]==' 5/5 ','queue cells')
 source=js(files['SOURCE_CORPUS_CHECKS.json'].read_bytes());ident=js(files['author/DATA_IDENTITY.json'].read_bytes());pdfs=js(files['audit/SOURCE_CHECKS.json'].read_bytes())['pinned_pdfs']
 need(source['status']=='PASS' and source['corpora']==[{**v,'full_file_rehashed':True} for v in ident['corpora']] and source['source_pdfs']==[{k:v[k] for k in ['title','url','bytes','sha256']} for v in pdfs],'source/corpus identity metadata')
 need(source['full_source_pdf_bytes_rehashed'] is True and source['unique_record'] is True and source['full_record_pair_matches_author'] is True and source['report_present'] is False and source['absent_report']=={} and source['review_bytes']==4313 and source['review_sha256']==ident['review_sha256'] and source['statement_sha256']==ident['statement_sha256'],'source/corpus match scope')
 out={'status':'PASS','regular_files':len(files),'immutable_archives':2,'immutable_archive_members':36,'strict_inventory_before_execution':True,'integrity_only':a.integrity_only,'original_problem_status':'unsolved','approaches_used':5}
 if not a.integrity_only:
  results={}
  for path in ['author/verify.py','audit/verify_audit.py','author/test_packet.py','audit/test_audit.py']:
   normal=execute(root,path);optimized=execute(root,path,True);need(normal==optimized,'normal/-O mismatch: '+path);results[path]=normal
  need(results['author/verify.py']['total_exact_controls']==790 and results['audit/verify_audit.py']['total_independent_finite_controls']==7769,'control counts')
  need(results['author/test_packet.py']['mutation_cases_rejected']==18 and results['audit/test_audit.py']['audit_mutation_cases_rejected']==26,'mutation counts')
  patch=execute(root,'test_patch.py',bool(sys.flags.optimize));need(patch==js(files['PATCH_TEST_RESULTS.json'].read_bytes()),'saved patch result mismatch')
  out.update({'author_exact_controls':790,'independent_exact_controls':7769,'author_mutation_cases':18,'independent_mutation_cases':26,'normal_optimized_gates_and_suites_agree':True,'actual_patch_command_replay':'PASS'})
 print(json.dumps(out,sort_keys=True,indent=2))
if __name__=='__main__':
 try:main()
 except Exception as e:print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
