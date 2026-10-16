from pathlib import Path
import os,json,hashlib,shutil,subprocess,sys,tempfile,socket,datetime
W=Path(__file__).resolve().parent;A=W.parents[1];B=W/'tmp/extracted';pin='4bf17667e368b032dce0f34de931de2860a79f73774015be556db11525b963b5'
def req(c,m):
 if not c:raise RuntimeError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rehash(root,name):
 mp=root/'PACKAGE_MANIFEST.json';m=json.loads(mp.read_text());p=root/name;m['files'][name]={'bytes':p.stat().st_size,'sha256':sha(p)};mp.write_text(json.dumps(m));return sha(mp)
results=[]
with tempfile.TemporaryDirectory(dir=W/'tmp',prefix='attacks-') as td:
 for opt in ([],['-O']):
  cases=['socket_special_entry','nested_fifo','listed_file_to_directory','float_bytecount','same_size_wrong_pdf','manifest_path_traversal','changed_note_rehashed_trusted_pin','nonanchor_original_script_changed']
  for case in cases:
   root=Path(td)/(case+str(bool(opt)));shutil.copytree(B,root);anchor=pin;pdf=A/'publication/output/pdf/note.pdf';sock=None
   if case=='socket_special_entry':
    previous=Path.cwd();os.chdir(root);sock=socket.socket(socket.AF_UNIX);sock.bind('bad.sock');os.chdir(previous)
   if case=='nested_fifo':(root/'nested').mkdir();os.mkfifo(root/'nested/x')
   if case=='listed_file_to_directory':(root/'note.tex').unlink();(root/'note.tex').mkdir()
   if case=='same_size_wrong_pdf':
    q=Path(td)/('badpdf'+str(bool(opt)));raw=bytearray(pdf.read_bytes());raw[100]^=1;q.write_bytes(raw);pdf=q
   if case=='float_bytecount':
    p=root/'PACKAGE_MANIFEST.json';m=json.loads(p.read_text());m['files']['note.tex']['bytes']=float(m['files']['note.tex']['bytes']);p.write_text(json.dumps(m));anchor=sha(p)
   if case=='manifest_path_traversal':
    p=root/'PACKAGE_MANIFEST.json';m=json.loads(p.read_text());m['files']['../escape']=m['files']['note.tex'];p.write_text(json.dumps(m));anchor=sha(p)
   if case=='changed_note_rehashed_trusted_pin':
    q=root/'note.tex';q.write_bytes(q.read_bytes()+b'\n% Universal claim deleted by test attacker\n');rehash(root,'note.tex')
   if case=='nonanchor_original_script_changed':
    q=root/'original_packet/author/verify.py';q.write_bytes(q.read_bytes()+b'\n# test alteration\n')
   p=subprocess.run([sys.executable,*opt,str(root/'verify_package.py'),'--integrity-only','--expected-manifest',anchor,'--pdf',str(pdf)],capture_output=True,text=True,timeout=30)
   if sock:sock.close()
   req(p.returncode!=0,'False supported PASS: '+case);results.append({'case':case,'optimized':bool(opt),'rejected':True,'stderr':p.stderr.strip()})
 # New substantive false positive attack on fresh checker: change central cubic coefficient.
 for name in ['reviews/proof_family/check_exact.py','reviews/computation_family/checks/exact_controls.py']:
  for opt in ([],['-O']):
   root=Path(td)/('mathmutation-'+name.split('/')[1]+str(bool(opt)));shutil.copytree(B,root);p=root/name;text=p.read_text()
   if name.endswith('check_exact.py'):
    old='scale(mul(mul(power(x, 2), power(y, 2)), power(z, 2)), 3)';new=old[:-2]+'4)'
   else:
    old='scale(mul(mul(power(X[0],2),power(X[1],2)),power(X[2],2)),3)';new=old[:-2]+'4)'
   if old not in text:
    # Find precisely from independently inspected checker code; do not invent a mutation.
    results.append({'case':'checker_mutation','script':name,'optimized':bool(opt),'status':'NOT_RUN_PATTERN_UNAVAILABLE'});continue
   req(text.count(old)==1,'ambiguous checker mutation');p.write_text(text.replace(old,new))
   q=subprocess.run([sys.executable,*opt,str(p)],capture_output=True,text=True,timeout=60);req(q.returncode!=0,'Fresh checker false PASS');results.append({'case':'central_coefficient_checker_mutation','script':name,'optimized':bool(opt),'rejected':True,'stderr':q.stderr[-1200:]})
 # Trust boundary positive control: a self-rehashed manuscript can pass without trusted pin.
 root=Path(td)/'self-rehashed';shutil.copytree(B,root);p=root/'note.tex';p.write_bytes(p.read_bytes()+b'\n% attacker changed prose\n');rehash(root,'note.tex');q=subprocess.run([sys.executable,str(root/'verify_package.py'),'--integrity-only'],capture_output=True,text=True);req(q.returncode==0,'Documented unauthenticated integrity boundary changed');results.append({'case':'self_rehashed_without_external_pin','passes_consistency':True,'scope':'documented trust boundary; no authenticity claim'})
 # Utilities and supplemental attack runner in writable disposable copies only.
 for script,args in [('reviews/proof_family/verify_review.py',[]),('reviews/proof_family/seal_manifest.py',[]),('reviews/computation_family/checks/replay_and_attack.py',['--result-name','full_package_01_rerun.json'])]:
  root=Path(td)/('utility-'+Path(script).stem);shutil.copytree(B,root);q=subprocess.run([sys.executable,str(root/script),*args],capture_output=True,text=True,timeout=300);req(q.returncode==0,'utility failed '+script+q.stderr)
  (W/'evidence'/('utility_'+Path(script).stem+'.stdout')).write_text(q.stdout);(W/'evidence'/('utility_'+Path(script).stem+'.stderr')).write_text(q.stderr)
  if 'replay_and_attack' in script:shutil.copy2(root/'reviews/computation_family/results/full_package_01_rerun.json',W/'evidence/supplemental_replay.json')
  results.append({'case':'shipped_utility','script':script,'returncode':q.returncode})
(W/'evidence/tool_attacks.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_WITH_DOCUMENTED_TRUST_BOUNDARY','tests':results},indent=2)+'\n');print(json.dumps({'status':'PASS','tests':len(results)},indent=2))
