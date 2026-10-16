#!/usr/bin/env python3
"""Fresh bounded PR880 reviewer checks. Candidate is read-only; outputs stay here."""
from pathlib import Path
import hashlib,json,subprocess,sys,datetime,stat,zipfile,io,runpy,copy,os,tempfile
R=Path(__file__).resolve().parent
A=R.parent
O=A/'replay/revision_r1'
P=A/'preprint'
V=A/'replay/portable_r1_polished'
EXPECTED={
 'outer':'11258d48f5ba2c0c0d5bd1893c1aaba8ac2fe3c2c4cd042181ba22f25f8decc2',
 'index':'7af74074708d9ee7b462be7d74546ef1f090a3262223d538082e872288e3df3d',
 'wrapper':'b8279f4945b2f05b3755bfec20ae6c78dbbb00d053abdb04f87d8068f2ff62a7',
 'verifier':'73faad1cfa4ab2e9c7e6cfa214e58fadb361ccf4de3199ed87e96883ae6a351a',
 'checker':'e78f97d36210f29e466636861767124a338c9ad0fe48e050eeec2a5355c3771f',
 'builder':'a1d76f65b2438236f2251c0f4dc850140fd1495a6e7ed418bfbf10fc86e23cca',
 'zip':'944e5d99825a3ef6689cff551f28bc9bb7aee04a1f58dbbceb6fd55bace4af2f'}
def require(ok,msg):
 if not ok:raise ValueError(msg)
def digest(raw):return hashlib.sha256(raw).hexdigest()
def auth(path,pin):
 raw=path.read_bytes();require(digest(raw)==pin,'external startup pin '+str(path));return raw
def put(name,obj):
 (R/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
def command(label,args):
 proc=subprocess.run([sys.executable,'-I','-S','-B',*args],capture_output=True,timeout=800,cwd=R/'private')
 require(proc.returncode==0 and not proc.stderr,label+' process failed '+proc.stderr.decode())
 result=json.loads(proc.stdout);require(result['status']=='PASS',label+' status')
 put(label+'.json',result)
 return result

def main():
 require(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,'isolation flags required')
 seal=json.loads((A/'PACKAGE_SEAL_R1.json').read_text())
 auth(O/'PUBLICATION_MANIFEST.json',EXPECTED['outer'])
 auth(O/'verify_current_publication.py',EXPECTED['wrapper'])
 auth(V/'package_index.json',EXPECTED['index'])
 for f,k in [('verify_package.py','verifier'),('check_originals.py','checker'),('build_verification.py','builder')]:auth(V/f,EXPECTED[k])
 # Independent closed-inventory hashing before invoking candidate code.
 inventories=[]
 for root,manifest,total in [(O,'PUBLICATION_MANIFEST.json',215),(V,'package_index.json',161)]:
  rows=json.loads((root/manifest).read_text())['files'];seen={}
  for p in root.rglob('*'):
   require(not p.is_symlink(),'alias in reviewed tree')
   if p.is_file():seen[p.relative_to(root).as_posix()]=p
  require(set(seen)=={e['path'] for e in rows}|{manifest},'independent closed file set')
  require(len(seen)==total,'independent file count')
  for e in rows:
   raw=seen[e['path']].read_bytes();require((len(raw),digest(raw))==(e['bytes'],e['sha256']),'independent inventory member')
  inventories.append({'root':root.name,'files':total,'all_member_pins_match':True})
 for e in seal['core_files']:
  raw=(P/e['path']).read_bytes();require((len(raw),digest(raw))==(e['bytes'],e['sha256']),'core pin '+e['path'])
 auth(P/'verification.zip',EXPECTED['zip'])
 with zipfile.ZipFile(P/'verification.zip') as z:
  require(sorted(z.namelist())==sorted(p.relative_to(V).as_posix() for p in V.rglob('*') if p.is_file()),'zip independent names')
  for n in z.namelist():require(z.read(n)==(V/n).read_bytes(),'zip independent payload')
 put('INDEPENDENT_INVENTORY.json',{'status':'PASS','inventories':inventories,'core_files':11,'zip_members':161,'startup_digests_authenticated_before_execution':EXPECTED})
 runroot=Path(tempfile.mkdtemp(prefix='fresh_rebuilds_',dir=R/'private'))
 for mode,flags in [('NORMAL',[]),('OPTIMIZED',['-O'])]:
  command('OUTER_FULL_'+mode,[*flags,str(O/'verify_current_publication.py'),EXPECTED['outer'],'--root',str(O),'--full'])
  result=command('FRESH_BUILD_'+mode,[*flags,str(V/'build_verification.py'),str(V),EXPECTED['index'],EXPECTED['verifier'],str(runroot/('fresh_build_'+mode.lower()))])
  require(result['sha256']==EXPECTED['zip'] and result['bytes']==568282,'same-runtime rebuild bytes')
  require((Path(result['archive']).read_bytes())==(P/'verification.zip').read_bytes(),'fresh rebuilt archive differs')
 # The optional complete-input path uses only inspected read-only hardlinks, not corpus copies.
 repo=A.parents[2]
 args=['--catalog',str(repo/'unsolved_math_prioritization/catalog.json'),'--problems',str(repo/'unsolved_math_prioritization/cache/problems.json'),'--reports',str(repo/'unsolved_math_prioritization/cache/research_results.json'),'--pdf-dir',str(A/'private_sources'),'--pdf-2012',str(A/'private_sources/1209.5120v1.pdf')]
 command('OUTER_FULL_COMPLETE_INPUTS',[str(O/'verify_current_publication.py'),EXPECTED['outer'],'--root',str(O),'--full',*args])
 put('REPRODUCTION_SUMMARY.json',{'status':'PASS','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':sys.version,'outer_modes':['normal','optimized'],'source_free_receipts_each':8,'fresh_rebuilds':['normal','optimized'],'same_bytes':True,'optional_complete_input_outer_mode':'normal','optional_complete_input_receipts':10,'historical_106_controls_reasserted':False})
if __name__=='__main__':main()
