from pathlib import Path
import os,sys,json,hashlib,zipfile,io,subprocess,shutil,datetime,stat,math
HERE=Path(__file__).resolve().parent; AUDIT=HERE.parent.parent; KIT=AUDIT/'preprint_v1_0'; S=HERE/'scratch'; S.mkdir(exist_ok=True)
receipts=[]
def h(b):return hashlib.sha256(b).hexdigest()
def need(ok,msg):
 if not ok:raise ValueError(msg)
def cmd(label,args,ok=True,env=None):
 p=subprocess.run(args,capture_output=True,text=True,env=env)
 r={'label':label,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':[str(a) for a in args],'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'expect_success':ok}
 receipts.append(r); (HERE/'COMMAND_RECEIPTS.json').write_text(json.dumps(receipts,indent=2)+'\n')
 need((p.returncode==0)==ok,label+' unexpected exit '+str(p.returncode)); return p
py=sys.executable
for entry in ['verify_package.py','check_math.py']:
 results=[]
 for mode in [[],['-O']]:
  r=cmd('canonical-'+entry+str(mode),[py,*mode,'-B',str(KIT/entry),'--output',str(S/(entry+('O' if mode else '')+'.json'))]); results.append(json.loads(r.stdout))
 need(results[0]==results[1],'normal optimized full JSON mismatch')
for mode in [[],['-O']]:
 cmd('canonical-required-binding'+str(mode),[py,*mode,'-B',str(KIT/'verify_package.py'),'--require-deposit'])
 for mutation in ['normal_sign','lost_jacobian','preprint_theta','fourier_boundary_sign']:
  cmd('current-math-fault-'+mutation+str(mode),[py,*mode,'-B',str(KIT/'check_math.py'),'--mutation',mutation],False)
cmd('native-local-check',[py,'-B','/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py','check',str(KIT/'zenodo-deposit.json')])
# Independently build the closed archive from file bytes, rather than invoking its builder.
names=(KIT/'PAYLOAD_MEMBERS.txt').read_text().splitlines(); closed=sorted(names+['SUPPORT_MANIFEST.json']); blob=(KIT/'pr1085_support_v1_0.zip').read_bytes(); st=io.BytesIO()
with zipfile.ZipFile(st,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for n in closed:
  i=zipfile.ZipInfo(n,(2026,10,14,0,0,0));i.create_system=3;i.external_attr=0o100644<<16;i.compress_type=zipfile.ZIP_DEFLATED;z.writestr(i,(KIT/n).read_bytes(),compresslevel=9)
need(st.getvalue()==blob,'independent closed archive byte equality')
with zipfile.ZipFile(io.BytesIO(blob)) as z:
 need(z.namelist()==closed and len(closed)==155 and z.testzip() is None,'155 sorted exact CRC')
 for i in z.infolist():need(i.extra==b'' and i.comment==b'' and i.flag_bits==0 and z.read(i.filename)==(KIT/i.filename).read_bytes(),'zip payload/header')
 K=S/'KitRoot';K.mkdir(exist_ok=True);z.extractall(K)
(K/'zenodo-deposit.json').write_bytes((KIT/'zenodo-deposit.json').read_bytes());(K/'UPLOAD_BINDINGS.json').write_bytes((KIT/'UPLOAD_BINDINGS.json').read_bytes());(K/'pr1085_support_v1_0.zip').write_bytes(blob)
original={str(p.relative_to(K)):p.read_bytes() for p in K.rglob('*') if p.is_file()}
def restore():
 for p in list(K.rglob('*')):
  if p.is_file() or p.is_symlink():p.unlink()
 for n,b in original.items():p=K/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
def repin():
 m=json.loads((K/'SUPPORT_MANIFEST.json').read_text())
 for row in m['files']:
  b=(K/row['path']).read_bytes();row['bytes']=len(b);row['sha256']=h(b)
 (K/'SUPPORT_MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')
def fault(label,edit):
 restore();edit();repin()
 for mode in [[],['-O']]:cmd('semantic-'+label+str(mode),[py,*mode,'-B',str(K/'verify_package.py')],False)
def change(n,k,v):
 p=K/n;o=json.loads(p.read_text());o[k]=v;p.write_text(json.dumps(o))
for n,k,v in [('STATUS.json','publication_ready',True),('STATUS.json','novelty','ESTABLISHED'),('TERMINAL_ACCOUNTING.json','whole_reviews_completed',3),('TERMINAL_ACCOUNTING.json','services_hold','none'),('CASE_ALIAS_REPAIR_ACCOUNTING.json','new_complete_whole03_completed',True),('CASE_ALIAS_REPAIR_ACCOUNTING.json','all_actionable_issues_resolved',True),('CASE_ALIAS_REPAIR_ACCOUNTING.json','human_peer_review',True),('SOURCE_METADATA.json','third_party_bodies_distributed',True)]:fault(n+':'+k,lambda n=n,k=k,v=v:change(n,k,v))
fault('metadata-all-wrappers-coherent',lambda:[change(n,'metadata',{'title':'unestablished first proof'}) if n=='metadata.json' else change(n,'title','unestablished first proof') for n in ['.zenodo.json','metadata.json']])
fault('case-copy-map-repin',lambda:change('CASE_ALIAS_REPAIR_COPY_MAP.json','files',[]))
fault('root-adoption-repin',lambda:change('evidence/terminal/ROOT_WHOLE_PACKAGE_REVIEW_02.json','publication_ready',True))
restore()
# Optional descriptors: absent means false; no fallback to default for explicit missing.
for mode in [[],['-O']]:
 r=cmd('explicit-missing-no-default-fallback'+str(mode),[py,*mode,'-B',str(K/'verify_package.py'),'--deposit',str(S/'ABSENT.json')]);need(json.loads(r.stdout)['external_deposit_binding_verified'] is False,'explicit absent must not default')
 cmd('explicit-missing-required'+str(mode),[py,*mode,'-B',str(K/'verify_package.py'),'--deposit',str(S/'ABSENT.json'),'--require-deposit'],False)
(K/'zenodo-deposit.json').unlink();(K/'UPLOAD_BINDINGS.json').unlink();(K/'pr1085_support_v1_0.zip').unlink()
for mode in [[],['-O']]:
 r=cmd('portable-absent-optional'+str(mode),[py,*mode,'-B',str(K/'verify_package.py')]);need(json.loads(r.stdout)['external_deposit_binding_verified'] is False,'absent not verified')
 cmd('portable-required-absent'+str(mode),[py,*mode,'-B',str(K/'verify_package.py'),'--require-deposit'],False)
restore()
(K/'UPLOAD_BINDINGS.json').write_text('{"metadata":{}}')
for mode in [[],['-O']]:cmd('corrupt-binding'+str(mode),[py,*mode,'-B',str(K/'verify_package.py')],False)
# Pre-JSON symlink preflight for bootstrap, manifest, regular member; corrupt JSON must not be parsed first.
for leaf in ['PAYLOAD_MEMBERS.txt','SUPPORT_MANIFEST.json','paper.pdf']:
 restore(); external=S/('preflight-'+leaf); external.write_bytes((K/leaf).read_bytes());(K/leaf).unlink();(K/leaf).symlink_to(external)
 if leaf!='SUPPORT_MANIFEST.json':(K/'SUPPORT_MANIFEST.json').write_text('{')
 for mode in [[],['-O']]:
  r=cmd('preparse-'+leaf+str(mode),[py,*mode,'-B',str(K/'verify_package.py')],False);need('symlink' in r.stderr,'must preflight before JSON')
restore()
# Actual writers on disposable kit only, no requests inside canonical audit inputs.
BIN=S/'bin';BIN.mkdir(exist_ok=True);sentinel=S/'COMPILER_SENTINEL';stub=BIN/'tectonic';stub.write_text('#!/bin/sh\nprintf invoked > "'+str(sentinel)+'"\nexit 37\n');stub.chmod(0o755);env=dict(os.environ,PATH=str(BIN)+os.pathsep+os.environ['PATH'])
writers={'verify_package.py':('--output',False),'check_math.py':('--output',False),'build_archive.py':('--output',False),'build_pdf.py':('--out-dir',True)}
def writer(label,e,target,mode=[],scriptroot=None,extra=[]):
 root=scriptroot or K;arg,isdir=writers[e];before={str(p):h(p.read_bytes()) for p in K.rglob('*') if p.is_file() and not p.is_symlink()};sentinel.unlink(missing_ok=True)
 r=cmd(label,[py,*mode,'-B',str(root/e),arg,str(target),*extra],False,env)
 need(not sentinel.exists(),'guard before compiler '+label)
 after={str(p):h(p.read_bytes()) for p in K.rglob('*') if p.is_file() and not p.is_symlink()};need(before==after,'guard changed kit '+label)
 return r
alias=S/'kITrOoT';need(os.path.samefile(K,alias),'physical case alias premise')
for e in writers:
 for mode in [[],['-O']]:
  for sr,ou,d in [(K,alias,'canonical-root-alias-output'),(alias,K,'alias-root-canonical-output')]:
   for tail in ['NEW_OUTPUT','ABSENT/PARENT/NEW_OUTPUT']:
    target=ou/tail;writer('physical-case-'+e+str(mode)+d+tail,e,target,mode,sr);need(not target.exists(),'no directory creation')
  writer('canonical-internal-'+e+str(mode),e,K/'other-output',mode)
  target=S/('hard-'+e);target.unlink(missing_ok=True)
  if e=='build_pdf.py':
   target.mkdir(exist_ok=True);os.link(K/'paper.pdf',target/'paper.pdf')
  else:os.link(K/'paper.pdf',target)
  writer('protected-hardlink-'+e+str(mode),e,target,mode)
  if target.is_dir():shutil.rmtree(target)
  else:target.unlink()
  target=S/('sym-'+e)
  target.symlink_to(K/'paper.pdf');writer('output-symlink-'+e+str(mode),e,target,mode);target.unlink()
  par=S/('parent-'+e);par.symlink_to(S);writer('symlink-parent-'+e+str(mode),e,par/'new',mode);par.unlink()
  if e!='build_pdf.py':writer('existing-protected-leaf-'+e+str(mode),e,K/'paper.pdf',mode)
  else:
   for leaf in ['paper.tex','paper.pdf','paper.log','COMPILE_RECEIPT.json']:
    target=S/('child-'+leaf);target.mkdir(exist_ok=True);(target/leaf).symlink_to(K/'paper.pdf');writer('pdf-child-'+leaf+str(mode),e,target,mode);shutil.rmtree(target)
# Unicode physical aliases: directory copied through rename, restore canonical name afterward.
U=S/'café';K.rename(U);UA=S/'cafe\u0301';need(os.path.samefile(U,UA),'Unicode normalization samefile premise')
K_saved=K;K=U
for e in writers:
 for mode in [[],['-O']]:
  for sr,ou,d in [(U,UA,'composed-root'),(UA,U,'decomposed-root')]:
   writer('physical-unicode-'+e+str(mode)+d,e,ou/'ABSENT/PARENT/new',mode,sr)
U.rename(K_saved);K=K_saved
# Supplied descriptor output alias protected before parsing, including hardlinks.
extra=S/'supplied.json';extra.write_bytes(b'{}')
for mode in [[],['-O']]:
 writer('supplied-descriptor-same'+str(mode),'verify_package.py',extra,mode,extra=['--deposit',str(extra)])
 hard=S/'supplied-hard.json';os.link(extra,hard);writer('supplied-descriptor-hard'+str(mode),'verify_package.py',hard,mode,extra=['--deposit',str(extra)]);hard.unlink()
# External outputs through case variants remain supported; actual positive writer executions.
restore();ext=S/'External';ext.mkdir(exist_ok=True);extalias=S/'eXTERNAL';need(os.path.samefile(ext,extalias),'external case identity')
for e in writers:
 for mode in [[],['-O']]:
  target=extalias/(e+('O' if mode else 'N'));arg,isdir=writers[e]
  cmd('external-case-positive-'+e+str(mode),[py,*mode,'-B',str(alias/e),arg,str(target)])
# Original guard identities remain conserved, plus package version metadata is exact.
summary={'passed':True,'commands':len(receipts),'zip_members':len(closed),'zip_bytes':len(blob),'zip_sha256':h(blob),'clean_normal_optimized_full_JSON_equal':True,'actual_case_samefile':True,'actual_unicode_samefile':True,'compiler_sentinel_all_guard_cases_uninvoked':True,'all_destructive_probes_disposable_only':True}
(HERE/'EXECUTION_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))
