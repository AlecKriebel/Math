#!/usr/bin/env python3
"""Replay a separately anchored author payload and exercise rejection boundaries."""
import argparse,hashlib,json,pathlib,shutil,stat,subprocess,sys,tempfile,zipfile
ZIP_SHA='6bc7b4cc916c38afbc1f7a6289e0dd9643f577d17778ecc79524c1f4646a538b'
MANIFEST_SHA='9516d60833e6f198eea54faf502f70d151aafe39ed26504ae9be3af05b22bab4'
NAMES={'APPROACH_LOG.md','PROOF.md','README.md','RESULTS.json','SOURCE_METADATA.json','certificate.py','verify_bundle.py'}
def need(x,msg):
 if not x:raise RuntimeError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def main(root,manifest,archive):
 need(sha(manifest.read_bytes())==MANIFEST_SHA,'untrusted input manifest')
 need(sha(archive.read_bytes())==ZIP_SHA,'untrusted input archive')
 m=json.loads(manifest.read_text())
 need({x.name for x in root.iterdir()}==NAMES,'input inventory')
 with zipfile.ZipFile(archive) as z:
  need(len(z.infolist())==len(NAMES) and set(z.namelist())==NAMES,'archive inventory')
  for rec in m['files']:
   name=rec['path'];b=(root/name).read_bytes();zi=z.getinfo(name)
   need(stat.S_ISREG((root/name).lstat().st_mode),'input nonregular')
   need(len(b)==rec['bytes'] and sha(b)==rec['sha256'],'input identity')
   need(z.read(name)==b and stat.S_ISREG(zi.external_attr>>16),'archive byte or mode mismatch')
 trusted=root/'verify_bundle.py';results=[]
 def run(case,r,mp,opt,want):
  cmd=[sys.executable,'-I','-B']+(['-O'] if opt else [])+[str(trusted),'--root',str(r),'--manifest',str(mp)]
  p=subprocess.run(cmd,cwd='/tmp',capture_output=True,text=True,timeout=120)
  need((p.returncode==0)==want,'unexpected outcome: '+case+' '+p.stderr[-400:])
  diagnostic=p.stderr.strip().splitlines()[-1] if p.stderr else 'verified'
  results.append({'case':case,'optimized':opt,'accepted':p.returncode==0,'returncode':p.returncode,'diagnostic':diagnostic})
 def refresh(r,mp):
  mm=json.loads(manifest.read_text())
  for rec in mm['files']:
   b=(r/rec['path']).read_bytes();rec.update(bytes=len(b),sha256=sha(b))
  mp.write_text(json.dumps(mm))
 for opt in (False,True):run('original',root,manifest,opt,True)
 with tempfile.TemporaryDirectory(prefix='independent-torus-controls-') as td:
  t=pathlib.Path(td);moved=t/'relocated payload with spaces';shutil.copytree(root,moved)
  for opt in (False,True):run('relocated foreign cwd',moved,manifest,opt,True)
  cases=['missing proof','unexpected file','nested directory','bytecode directory','symlink payload','symlink root',
   'symlink manifest','manifest inside root','proof byte mutation','result byte mutation','verifier byte mutation',
   'certificate byte mutation','manifest missing file','manifest duplicate record','manifest traversal path',
   'manifest absolute path','manifest wrong schema','manifest wrong problem','manifest bool problem',
   'manifest bool byte count','manifest float byte count','manifest negative byte count','manifest wrong length',
   'manifest uppercase digest','manifest extra key','manifest record extra key','manifest duplicate key',
   'manifest nested duplicate key','manifest invalid JSON','manifest invalid UTF8',
   'rehashed wrong result','rehashed nonregular quotient','rehashed incorrect product','rehashed overclaim',
   'rehashed false status','rehashed certificate stderr']
  for i,case in enumerate(cases):
   r=t/('case '+str(i));shutil.copytree(root,r);mp=t/('manifest '+str(i)+'.json');shutil.copyfile(manifest,mp)
   mm=json.loads(mp.read_text())
   if case=='missing proof':(r/'PROOF.md').unlink()
   elif case=='unexpected file':(r/'EXTRA').write_text('extra')
   elif case in ('nested directory','bytecode directory'):(r/('extra' if case=='nested directory' else '__pycache__')).mkdir()
   elif case=='symlink payload':(r/'PROOF.md').unlink();(r/'PROOF.md').symlink_to(root/'PROOF.md')
   elif case=='symlink root':link=t/'root-link';link.symlink_to(r);r=link
   elif case=='symlink manifest':mp.unlink();mp.symlink_to(manifest)
   elif case=='manifest inside root':mp=r/'external.json';shutil.copyfile(manifest,mp)
   elif case.endswith('byte mutation'):
    name={'proof':'PROOF.md','result':'RESULTS.json','verifier':'verify_bundle.py','certificate':'certificate.py'}[case.split()[0]]
    p=r/name;p.write_bytes(p.read_bytes()+b'\n')
   elif case=='manifest missing file':mm['files'].pop()
   elif case=='manifest duplicate record':mm['files'][-1]=mm['files'][0]
   elif case=='manifest traversal path':mm['files'][0]['path']='../PROOF.md'
   elif case=='manifest absolute path':mm['files'][0]['path']='/tmp/PROOF.md'
   elif case=='manifest wrong schema':mm['schema']='unknown'
   elif case=='manifest wrong problem':mm['problem_id']=30001703
   elif case=='manifest bool problem':mm['problem_id']=True
   elif case=='manifest bool byte count':mm['files'][0]['bytes']=True
   elif case=='manifest float byte count':mm['files'][0]['bytes']=float(mm['files'][0]['bytes'])
   elif case=='manifest negative byte count':mm['files'][0]['bytes']=-1
   elif case=='manifest wrong length':mm['files'][0]['bytes']+=1
   elif case=='manifest uppercase digest':mm['files'][0]['sha256']=mm['files'][0]['sha256'].upper()
   elif case=='manifest extra key':mm['extra']=1
   elif case=='manifest record extra key':mm['files'][0]['extra']=1
   elif case=='manifest duplicate key':mp.write_text(mp.read_text().replace('"problem_id":','"problem_id": 1, "problem_id":'))
   elif case=='manifest nested duplicate key':mp.write_text(mp.read_text().replace('"bytes":','"bytes": 1, "bytes":',1))
   elif case=='manifest invalid JSON':mp.write_text('{')
   elif case=='manifest invalid UTF8':mp.write_bytes(b'\xff')
   elif case=='rehashed wrong result':
    p=r/'RESULTS.json';p.write_text(p.read_text().replace('5250','5251'));refresh(r,mp)
   else:
    p=r/'certificate.py';s=p.read_text()
    if case=='rehashed nonregular quotient':s=s.replace('quotient(d,d+1) for d','quotient(d,d) for d')
    elif case=='rehashed incorrect product':s=s.replace('math.factorial(p+q)*p*q','math.factorial(p+q)*(p*q+1)')
    elif case=='rehashed overclaim':s=s.replace("'universal_factorial_bound_proved':False","'universal_factorial_bound_proved':True")
    elif case=='rehashed false status':s=s.replace("'PARTIAL_UNRESOLVED'","'SOLVED'")
    elif case=='rehashed certificate stderr':s+='\nimport sys\nprint("deliberate stderr",file=sys.stderr)\n'
    else:raise RuntimeError('unknown case')
    p.write_text(s)
    if case in ('rehashed overclaim','rehashed false status'):
     out=subprocess.run([sys.executable,'-I','-B',str(p)],capture_output=True,text=True,timeout=120)
     need(out.returncode==0,'mutation generation failed');(r/'RESULTS.json').write_text(out.stdout)
    refresh(r,mp)
   if case.startswith('manifest ') and case not in ('manifest inside root','manifest duplicate key','manifest nested duplicate key','manifest invalid JSON','manifest invalid UTF8'):
    mp.write_text(json.dumps(mm))
   for opt in (False,True):run(case,r,mp,opt,False)
  # This is a declared trust boundary, not a negative check or authenticity claim.
  r=t/'untrusted rehashed prose';shutil.copytree(root,r);mp=t/'untrusted.json'
  p=r/'PROOF.md';p.write_text(p.read_text()+'\nDeliberate prose mutation used only to demonstrate the manifest trust boundary.\n');refresh(r,mp)
  for opt in (False,True):run('untrusted replacement manifest permits changed prose',r,mp,opt,True)
 return {'status':'PASS_WITH_DOCUMENTED_TRUST_BOUNDARY','author_zip_sha256':ZIP_SHA,'author_manifest_sha256':MANIFEST_SHA,
  'payload_files':len(NAMES),'executions':len(results),'expected_positive':sum(x['accepted'] for x in results),
  'expected_negative':sum(not x['accepted'] for x in results),'cases':results,
  'boundary':'The replay verifier is not a proof checker and cannot authenticate a caller-replaced manifest. Independently pin the supplied original ZIP/manifest hashes.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--author-root',type=pathlib.Path,required=True);p.add_argument('--manifest',type=pathlib.Path,required=True);p.add_argument('--archive',type=pathlib.Path,required=True);a=p.parse_args()
 print(json.dumps(main(a.author_root.resolve(),a.manifest.resolve(),a.archive.resolve()),indent=2,sort_keys=True))
