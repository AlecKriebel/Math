#!/usr/bin/env python3
"""Authenticate exact reciprocal-rectangle artifacts before isolated replay."""
import argparse,hashlib,io,json,os,shutil,stat,subprocess,sys,tempfile,zipfile
from pathlib import Path,PurePosixPath
MANIFEST_SHA256='873d076f155ef649f5e1039ddbabf2369fecfd966553360b81c472ac21f30cc9'
PINS={'RECIPROCAL_RECTANGLE_3900015_AUTHOR_SAFE_FREEZE.zip': (16824, 'abaee91d08a6173ca929bde0aa28578486e5d4412bca3a8ce23230a970502612'), 'RECIPROCAL_RECTANGLE_3900015_AUTHOR_EXTERNAL_MANIFEST.json': (2015, 'ae9be91cf28ef9d77dc2560068f1ce9089b1776bfd330e14fd9bf9fcd91226f7'), 'RECIPROCAL_RECTANGLE_3900015_INDEPENDENT_AUDIT_SAFE.zip': (40619, '9ee19f929512178ad3da1a565a164570a94b014e73e80ffb877184c0fac1212b'), 'RECIPROCAL_RECTANGLE_3900015_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json': (2865, '299ab86e0bbcf4774615895f6a60d43f5e5f1ba6216341117eb3501927ebe97a'), 'RECIPROCAL_RECTANGLE_3900015_INDEPENDENT_AUDIT_RECEIPT.json': (11421, '1e50c97bd7cd49c4a75af03d7397beb374005e25cfdf4df1ce451f320bbb19e3'), 'RECIPROCAL_RECTANGLE_3900015_INDEPENDENT_AUDIT_BOOTSTRAP.py': (2787, '259c27d5bace9116d86e0f63df5a63abeaf1a3071e0b953e308eea36408e8ca7')}
PREFIX='RECIPROCAL_RECTANGLE_3900015_'
AZ=PREFIX+'AUTHOR_SAFE_FREEZE.zip';AM=PREFIX+'AUTHOR_EXTERNAL_MANIFEST.json'
IZ=PREFIX+'INDEPENDENT_AUDIT_SAFE.zip';IM=PREFIX+'INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json'
def need(ok,message):
 if not ok:raise ValueError(message)
def sha(b):return hashlib.sha256(b).hexdigest()
def dig(b):return {'bytes':len(b),'sha256':sha(b)}
def unique(pairs):
 out={}
 for k,v in pairs:need(k not in out,'duplicate JSON key');out[k]=v
 return out
def parse(b):return json.loads(b,object_pairs_hook=unique)
def read(p):need(stat.S_ISREG(p.lstat().st_mode),'nonregular file');return p.read_bytes()
def authenticate(root):
 need(stat.S_ISDIR(root.lstat().st_mode),'nonordinary root');raw=read(root/'PUBLICATION_MANIFEST.json');need(sha(raw)==MANIFEST_SHA256,'publication manifest pin mismatch');m=parse(raw)
 need((m['schema'],m['problem_id'],m['problem_number'],m['rank'],m['status'],m['turns'],m['full_problem_resolved'],m['correction_required'])==('reciprocal-publication-manifest-v1','3900015','AMR-038-0015',928,'unsolved','3/5',False,False),'publication scope')
 expected=set(m['files'])|{'PUBLICATION_MANIFEST.json','verify_publication.py'};dirs=set()
 for name in expected:
  p=PurePosixPath(name);need(not p.is_absolute() and '..' not in p.parts and '\\' not in name and str(p)==name,'unsafe path');dirs.update(str(x) for x in p.parents if str(x)!='.')
 found=set()
 for base,subdirs,names in os.walk(root,followlinks=False):
  for name in subdirs:
   p=Path(base)/name;need(stat.S_ISDIR(p.lstat().st_mode) and p.relative_to(root).as_posix() in dirs,'unexpected/nonordinary directory')
  for name in names:
   p=Path(base)/name;need(stat.S_ISREG(p.lstat().st_mode),'nonregular member');found.add(p.relative_to(root).as_posix())
 need(found==expected,'exact file allowlist mismatch');buffers={'PUBLICATION_MANIFEST.json':raw,'verify_publication.py':read(root/'verify_publication.py')};need(buffers['verify_publication.py']==read(Path(__file__)),'wrapper copy mismatch')
 for name,pin in m['files'].items():
  b=read(root/name);need(dig(b)==pin,'file pin mismatch: '+name);buffers[name]=b
 for name,pin in PINS.items():
  b=buffers['releases/'+name];need((len(b),sha(b))==pin,'frozen release pin mismatch')
 return buffers
def archives(buffers):
 out=[]
 for label,az,am,count in [('original',AZ,AM,10),('audit',IZ,IM,14)]:
  raw=buffers['releases/'+az];m=parse(buffers['releases/'+am]);need(m['archive']==dict(filename=az,**dig(raw)),'archive metadata');members=m['files'];need(len(members)==count,'external inventory')
  with zipfile.ZipFile(io.BytesIO(raw)) as z:
   need(len(z.infolist())==len(set(z.namelist()))==count and set(z.namelist())==set(members),'archive inventory')
   for i in z.infolist():
    name=i.filename;need(name not in ('','.','..') and name==Path(name).name and '\\' not in name and stat.S_ISREG(i.external_attr>>16) and not i.flag_bits&1,'unsafe ZIP member');b=z.read(i);need(dig(b)==members[name] and b==buffers[label+'/'+name],'archive or expanded member mismatch')
   inner=parse(z.read('MANIFEST.json'))['files'];need(set(inner)|{'MANIFEST.json'}==set(members) and len(inner)==count-1,'internal inventory')
   for name,pin in inner.items():need(dig(z.read(name))==pin,'inner member pin')
  out.append({'label':label,'members':count,'all_members_exact_match':True})
 need(buffers['audit/AUTHOR_SAFE_FREEZE.zip']==buffers['releases/'+AZ] and buffers['audit/AUTHOR_EXTERNAL_MANIFEST.json']==buffers['releases/'+AM],'nested author identity')
 a=parse(buffers['audit/ACCEPTANCE.json']);need((a['problem_id'],a['problem_number'],a['rank'],a['proposed_queue_status'],a['proposed_turns'],a['verdict'])==('3900015','AMR-038-0015',928,'unsolved','3/5','accepted-unchanged-unresolved-bounded-partial'),'acceptance scope')
 need(a['full_problem_resolved'] is False and a['correction_required'] is False and a['corrected_derivative'] is None,'acceptance overclaim')
 need(a['accepted_author_archive']==dict(filename=AZ,**dig(buffers['releases/'+AZ])) and a['accepted_author_external_manifest']==dig(buffers['releases/'+AM]),'acceptance pins')
 need(a['accepted_author_members']==parse(buffers['releases/'+AM])['files'],'accepted member identity')
 need((a['author_m4_replay'],a['independent_prefix_grid_packings'],a['independent_m4_grid_packings'],a['independent_m4_separator_systems_tested'])==({'candidate_trials':10204,'feasible':False,'states':75},3064,0,32768),'accepted counters')
 return out
def run(script,args,opt,cwd):
 p=subprocess.run([sys.executable,'-I','-B']+(['-O'] if opt else [])+[str(script),*map(str,args)],cwd=cwd,capture_output=True,text=True,timeout=180,env={'PATH':os.environ.get('PATH','/usr/bin:/bin'),'HOME':str(cwd/'unrelated home'),'PYTHONPATH':str(cwd/'poison')});need(p.returncode==0,'replay failed: '+p.stderr);return parse(p.stdout),sha(p.stdout.encode())
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path(__file__).absolute().parent);p.add_argument('--integrity-only',action='store_true');p.add_argument('--corpus-dir',type=Path);p.add_argument('--source-dir',type=Path);a=p.parse_args();need(bool(a.corpus_dir)==bool(a.source_dir),'supply both full-input directories');need(not(a.integrity_only and a.corpus_dir),'integrity-only cannot claim input replay')
 b=authenticate(a.root.absolute());ar=archives(b);out={'status':'PASS','problem_id':'3900015','mathematical_status':'unsolved','turns':'3/5','full_problem_resolved':False,'correction_required':False,'formal_proof_check':False,'files_authenticated':len(b),'archives':ar,'full_input_replay':bool(a.corpus_dir),'mode':'integrity-only' if a.integrity_only else 'replay','replays':[]}
 with tempfile.TemporaryDirectory(prefix='reciprocal publication relocated α ') as td:
  work=Path(td);packet=work/'authenticated packet'
  for name,body in b.items():
   dest=packet/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(body)
  args=[]
  if a.corpus_dir:
   cd=work/'private corpus inputs';sd=work/'private source inputs';cd.mkdir();sd.mkdir()
   for name in ('catalog.json','problems.json','research_results.json'):shutil.copyfile(a.corpus_dir/name,cd/name)
   for name in ('junkyard.html','jiang.pdf','zhu_joos.pdf','slack_pack.pdf','martin.pdf'):shutil.copyfile(a.source_dir/name,sd/name)
   args=['--corpus-dir',cd,'--source-dir',sd]
  if not a.integrity_only:
   hashes=[]
   for opt in (False,True):
    audit,ah=run(packet/'audit/verify_audit.py',[],opt,work);need(audit['verified'] is True and audit['full_problem_resolved'] is False and audit['correction_required'] is False,'audit semantics');need(audit['author_subprocess_tests']==22 and audit['external_coordinated_tamper_checks']==1,'artifact case counts');need(audit['independent_checks']==parse(b['audit/EXPECTED_INDEPENDENT_CHECKS.json']),'independent checks')
    boot,bh=run(packet/('releases/'+PREFIX+'INDEPENDENT_AUDIT_BOOTSTRAP.py'),[],opt,work);need(boot['bootstrap_verified'] is True and boot['full_problem_resolved'] is False,'bootstrap semantics')
    row={'optimized':opt,'isolated':True,'relocated':True,'audit_stdout_sha256':ah,'bootstrap_stdout_sha256':bh,'author_subprocess_tests':22,'external_coordinated_tamper_checks':1}
    if args:
     source,sh=run(packet/'audit/verify_source_corpus.py',args,opt,work);need(source==parse(b['audit/SOURCE_CORPUS_AUDIT.json']),'complete source/corpus replay mismatch');row.update(source_corpus_stdout_sha256=sh,complete_corpora=3,complete_public_sources=5,full_record_pair_sha256=source['record_pair_sha256'])
    out['replays'].append(row);hashes.append((ah,bh,row.get('source_corpus_stdout_sha256')))
   need(hashes[0]==hashes[1],'normal/optimized mismatch')
 print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':
 try:main()
 except Exception as e:print('FAIL: '+str(e),file=sys.stderr);raise SystemExit(1)
