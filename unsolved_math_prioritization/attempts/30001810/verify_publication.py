"""Externally pinned source-free integrity, exact patch, and finite replay checks."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECTED: use python -I -S -B [ -O | -OO ] verify_publication.py PIN PACKET')
from pathlib import Path,PurePosixPath
import hashlib,json,os,stat,subprocess,tempfile,re
AUTHOR={'APPROACH_LEDGER.md','CHECKS.md','EXACT_CHECKS.json','MANIFEST.json','MATHEMATICAL_REPORT.md','README.md','SOURCES.md','SOURCE_METADATA.json','check_exact.py'}
AUDIT={'ACCEPTANCE.json','AUDIT_REPORT.md','CORRECTED_MATHEMATICAL_REPORT.md','CORRECTION.patch','INDEPENDENT_CHECKS.json','MANIFEST.json','README.md','SOURCE_METADATA.json','independent_checks.py'}
FILES={f'author/{n}' for n in AUTHOR}|{f'audit/{n}' for n in AUDIT}|{'AUTHOR_FREEZE.json','AUDIT_FREEZE.json','corrected/MATHEMATICAL_REPORT.md','README.md','ACCEPTANCE.md','RESEARCH_LOG.md','verify_publication.py','guarded_child.py','mutation_tests.py'}
DIRS={'author','audit','corrected'}
PINS={
 'author/MANIFEST.json':'8ff41ceaafa1278519013f401c12d6279840a9fbbfe87ba74103c91293af1348',
 'author/MATHEMATICAL_REPORT.md':'b796c99ef3673687fcf40c3f3912b008fa6694d4b5eca996b1c1998f0e230062',
 'audit/MANIFEST.json':'36351f6d7fb43db42da430148b50187a1322b8c82e0ed63a1cf6e2813188bd4e',
 'audit/CORRECTION.patch':'35c7928a3988516283654e0f2926b2f852d8ec4d98644828540fc2ed902bc685',
 'audit/CORRECTED_MATHEMATICAL_REPORT.md':'e8e396d4b4fb01a2319e95d4cd95fdd8c3e38ee971e155c27b398ee5be268683',
 'corrected/MATHEMATICAL_REPORT.md':'e8e396d4b4fb01a2319e95d4cd95fdd8c3e38ee971e155c27b398ee5be268683',
}
def require(ok,message):
 if not ok:raise ValueError(message)
def digest(b):return hashlib.sha256(b).hexdigest()
def unique(pairs):
 result={}
 for k,v in pairs:
  require(k not in result,'Duplicate JSON key');result[k]=v
 return result
def parse(b):return json.loads(b,object_pairs_hook=unique)
def valid_path(name):
 return isinstance(name,str) and name and '\\' not in name and not name.startswith('/') and all(p not in ('','.', '..') for p in name.split('/')) and PurePosixPath(name).as_posix()==name

def apply_patch(original,patch):
 source=original.splitlines(keepends=True);lines=patch.splitlines(keepends=True)
 require(lines[:2]==[b'--- a/MATHEMATICAL_REPORT.md\n',b'+++ b/MATHEMATICAL_REPORT.md\n'],'Unexpected patch target')
 result=[];position=0;i=2;hunks=0
 while i<len(lines):
  match=re.fullmatch(rb'@@ -(\d+),(\d+) \+(\d+),(\d+) @@\n',lines[i]);require(match is not None,'Malformed patch hunk')
  start,old_count,new_start,new_count=map(int,match.groups());i+=1;hunks+=1
  require(start-1>=position,'Overlapping patch');result.extend(source[position:start-1]);position=start-1
  require(len(result)==new_start-1,'New patch offset mismatch');old_seen=new_seen=0
  while i<len(lines) and not lines[i].startswith(b'@@ '):
   line=lines[i];i+=1;require(line[:1] in (b' ',b'-',b'+'),'Invalid patch line')
   if line[:1] in (b' ',b'-'):
    require(position<len(source) and source[position]==line[1:],'Patch context mismatch');position+=1;old_seen+=1
   if line[:1] in (b' ',b'+'):result.append(line[1:]);new_seen+=1
  require((old_seen,new_seen)==(old_count,new_count),'Patch line count mismatch')
 require(hunks==2,'Expected two corrections');result.extend(source[position:]);return b''.join(result)

def integrity(root,pin):
 require(isinstance(pin,str) and len(pin)==64 and all(c in '0123456789abcdef' for c in pin),'Malformed pin')
 require(not root.is_symlink() and root.is_dir(),'Invalid or linked root')
 files=set();dirs=set()
 def walk(directory):
  for entry in os.scandir(directory):
   p=Path(entry.path);rel=p.relative_to(root).as_posix();mode=entry.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(mode):require(rel in DIRS,'Unexpected directory: '+rel);dirs.add(rel);walk(p)
   else:require(stat.S_ISREG(mode),'Linked or special entry: '+rel);files.add(rel)
 walk(root);require(files==FILES|{'PUBLIC_MANIFEST.json'} and dirs==DIRS,'Closed inventory mismatch')
 raw=(root/'PUBLIC_MANIFEST.json').read_bytes();require(digest(raw)==pin,'Manifest pin mismatch');manifest=parse(raw)
 require(set(manifest)=={'schema','problem_id','files'} and manifest['schema']=='immersive-publication-v1' and manifest['problem_id']==30001810,'Manifest schema/target mismatch')
 rows=manifest['files'];require(isinstance(rows,list) and len(rows)==len(FILES),'Invalid manifest size');names=[];snapshot={}
 for row in rows:
  require(isinstance(row,dict) and set(row)=={'path','bytes','sha256'},'Invalid entry');name=row['path']
  require(valid_path(name) and name in FILES and name not in names,'Invalid/duplicate path');names.append(name)
  b=(root/name).read_bytes();require(type(row['bytes']) is int and len(b)==row['bytes'] and digest(b)==row['sha256'],'Payload mismatch: '+name);snapshot[name]=b
 require(set(names)==FILES,'Manifest allowlist mismatch')
 for name,value in PINS.items():require(digest(snapshot[name])==value,'Frozen pin mismatch: '+name)
 for sub,expected in [('author',AUTHOR),('audit',AUDIT)]:
  child=parse(snapshot[sub+'/MANIFEST.json']);entries=child['files']
  require(len(entries)==len(expected)-1 and {r['path'] for r in entries}==expected-{'MANIFEST.json'},'Nested inventory mismatch')
  for row in entries:
   b=snapshot[sub+'/'+row['path']];require(len(b)==row['bytes'] and digest(b)==row['sha256'],'Nested payload mismatch')
  freeze=parse(snapshot[sub.upper()+'_FREEZE.json'])
  require(freeze['manifest_sha256']==PINS[sub+'/MANIFEST.json'] and freeze['manifest_bytes']==len(snapshot[sub+'/MANIFEST.json']) and freeze['file_count_including_manifest']==len(expected),'Freeze mismatch')
 require(parse(snapshot['AUTHOR_FREEZE.json'])['report_sha256']==PINS['author/MATHEMATICAL_REPORT.md'],'Author report freeze mismatch')
 af=parse(snapshot['AUDIT_FREEZE.json'])
 require(af['corrected_report_sha256']==PINS['corrected/MATHEMATICAL_REPORT.md'] and af['audit_report_sha256']==digest(snapshot['audit/AUDIT_REPORT.md']),'Audit report freeze mismatch')
 corrected=apply_patch(snapshot['author/MATHEMATICAL_REPORT.md'],snapshot['audit/CORRECTION.patch'])
 require(corrected==snapshot['audit/CORRECTED_MATHEMATICAL_REPORT.md']==snapshot['corrected/MATHEMATICAL_REPORT.md'],'Patch replay mismatch')
 return snapshot

def replay(snapshot):
 opt=[] if sys.flags.optimize==0 else ['-O' if sys.flags.optimize==1 else '-OO']
 with tempfile.TemporaryDirectory(prefix='immersive-publication-') as td:
  root=Path(td)
  for name,b in snapshot.items():
   p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
  results={}
  cases=[('author',['author/check_exact.py'],'author/EXACT_CHECKS.json'),('audit',['audit/independent_checks.py','--input',str(root/'author')],'audit/INDEPENDENT_CHECKS.json')]
  for label,argv,expected in cases:
   argv[0]=str(root/argv[0])
   for guarded in (False,True):
    command=[sys.executable,'-I','-S','-B',*opt]+([str(root/'guarded_child.py')] if guarded else [])+argv
    process=subprocess.run(command,cwd=root,capture_output=True,timeout=180)
    require(process.returncode==0,label+' replay failed: '+process.stderr.decode(errors='replace'))
    output=process.stdout;record={'optimization':sys.flags.optimize,'assertion_preserving':guarded or sys.flags.optimize==0}
    if guarded:
     envelope=parse(output);require(envelope['optimization']==sys.flags.optimize and envelope['assertions_rewritten']>0 and envelope['negative_assertion_rejected'] is True,'Guarded-child receipt mismatch')
     output=envelope['stdout'].encode();record['assertions_rewritten']=envelope['assertions_rewritten'];record['negative_assertion_rejected']=True
    require(output==snapshot[expected],label+' full receipt byte mismatch');record.update(status='pass',receipt_sha256=digest(output));results[label+('_guarded' if guarded else '_direct')]=record
  return results

def main():
 require(len(sys.argv)==3,'Expected external manifest pin and packet path')
 pin=sys.argv[1];root=Path(os.path.abspath(sys.argv[2]));snapshot=integrity(root,pin)
 result={'schema':'immersive-publication-replay-v1','problem_id':30001810,'status':'pass','python_optimization':sys.flags.optimize,'manifest_sha256':pin,'verified_payload_files':len(snapshot),'patch_replay_matches':True,'replays':replay(snapshot),'limits':'Integrity and finite controls, not a formal proof or resolution. Direct optimized originals omit assertions; guarded AST replay preserves them. Audit nested author replay is unoptimized.'}
 require(integrity(root,pin)==snapshot,'Input changed during replay');print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':
 try:main()
 except Exception as exc:print('REJECTED: '+str(exc),file=sys.stderr);sys.exit(1)
