"""Fresh static package checks. Run in a disposable review copy; writes owned receipts/tmp."""
from pathlib import Path
import datetime, hashlib, importlib.util, io, json, os, shutil, stat, struct, subprocess, sys, zipfile, zlib
HERE=Path(__file__).resolve().parent
PRE=HERE.parent/'preprint'; TMP=HERE/'tmp'; SRC=TMP/'source'; PDF=PRE/'output/pdf/paper.pdf'
PY312='/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
DESTS=('paper.tex','output/pdf/paper.pdf','source-and-verification.zip','zenodo-deposit.json','zenodo-metadata.json','zenodo-upload-kit.zip','PACKAGE_INVENTORY.json')
def need(v,m):
 if not v:raise RuntimeError(m)
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(n,v):(HERE/n).write_text(json.dumps(v,indent=2)+'\n')
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def tree(root):
 if not os.path.lexists(root):return {}
 paths=[root]+list(root.rglob('*')) if root.is_dir() and not root.is_symlink() else [root]
 ans={}
 for p in paths:
  s=p.lstat();kind=stat.S_IFMT(s.st_mode)
  ans[p.relative_to(root).as_posix()]={'kind':kind,'content':os.readlink(p) if stat.S_ISLNK(s.st_mode) else ident(p.read_bytes()) if stat.S_ISREG(s.st_mode) else None,'inode':s.st_ino,'links':s.st_nlink}
 return ans
def call(args,opt=None):
 e=os.environ.copy();e.pop('PYTHONOPTIMIZE',None);e['PYTHONDONTWRITEBYTECODE']='1'
 if opt is not None:e['PYTHONOPTIMIZE']=str(opt)
 return subprocess.run(args,cwd='/',env=e,text=True,capture_output=True,timeout=240)
def closed_copy(dst):
 if dst.exists():shutil.rmtree(dst)
 with zipfile.ZipFile(PRE/'source-and-verification.zip') as z:
  ns=z.namelist();need(ns==sorted(set(ns)),'zip order/duplicates')
  for i in z.infolist():
   need(not i.is_dir() and stat.S_ISREG(i.external_attr>>16),'member nonregular')
   need(not i.filename.startswith('/') and all(p not in ('','.','..') for p in i.filename.split('/')) and '\\' not in i.filename,'unsafe member')
  z.extractall(dst)
def editj(p,fn):
 x=json.loads(p.read_bytes());fn(x);p.write_text(json.dumps(x,indent=2)+'\n')
def rehash(s):
 def upd(m):
  for r in m['files']:
   p=s/r['path']
   if p.is_file():r.update(ident(p.read_bytes()))
 editj(s/'MANIFEST.json',upd)
def main():
 TMP.mkdir(exist_ok=True);closed_copy(SRC);before=tree(SRC)
 checks=json.loads((HERE/'CHECKED_INPUTS.json').read_bytes())['before']
 for r in checks:need(ident(Path(r['path']).read_bytes())=={k:r[k] for k in ('bytes','sha256')},'frozen start')
 replay=[]
 for label,py,flags,opt in [('normal',sys.executable,[],None),('outer_O',sys.executable,['-O'],None),('env_OPT2',sys.executable,[],2),('bundled312',PY312,[],None)]:
  r=call([py,*flags,'-B',str(SRC/'verify_bundle.py'),'--pdf',str(PDF)],opt)
  need(r.returncode==0,label+':'+r.stderr);j=json.loads(r.stdout)
  h=j['historical_replay'];need([h[k] for k in ('author_assertions','first_portable_assertions','first_with_author_archive_assertions','second_exact_tail_checks')]==[4187,2911,2923,2304],'counts')
  need(tree(SRC)==before,'replay mutation');replay.append({'mode':label,'version':call([py,'--version']).stdout.strip(),'exit':r.returncode,'source_unchanged':True,'result':j})
 save('REPLAY_RECEIPT.json',{'utc':now(),'unrelated_cwd':'/','child_assertion_mode':'-I -B, no optimization; __debug__ actively checked by entrypoint','modes':replay})
 comparisons=[]
 snap=json.loads((SRC/'audit/SNAPSHOT.json').read_bytes())
 for r in snap['files']:
  name=r['path'].split('attempts/30005613/',1)[1];raw=(SRC/'historical_candidate'/name).read_bytes()
  need(raw==(HERE.parent/'original'/r['path']).read_bytes(),'actual frozen original '+name)
  need(ident(raw)=={k:r[k] for k in ('bytes','sha256')},'snapshot '+name);comparisons.append({'path':name,**ident(raw)})
 need(len(comparisons)==39,'39originals')
 arcs=[]
 for p in sorted((SRC/'historical_candidate/archives').glob('*.zip')):
  with zipfile.ZipFile(p) as z:
   ns=z.namelist();need(len(ns)==len(set(ns)),'nested duplicate');members=[]
   for i in z.infolist():
    need(not i.filename.startswith('/') and '..' not in i.filename.split('/'),'nested unsafe')
    if i.is_dir():continue
    raw=z.read(i);matches=[q.relative_to(SRC/'historical_candidate').as_posix() for q in (SRC/'historical_candidate').rglob('*') if q.is_file() and q.suffix!='.zip' and q.read_bytes()==raw]
    need(matches,'unmatched extraction');members.append({'member':i.filename,'matches':matches,**ident(raw)})
   arcs.append({'archive':p.name,'members':members,'CRC_valid':z.testzip() is None})
 need(len(arcs)==3,'3archives');save('PRESERVATION_RECEIPT.json',{'utc':now(),'original_count':39,'files':comparisons,'archives':arcs,'named_archive_identity_rechecked_by_historical_entrypoint':True})
 # Rebuild ordinary changed single-link outputs; retain descriptors to disallow accidental inode recycling.
 builds=[]
 for label,py,flags in [('normal',sys.executable,[]),('outer_O',sys.executable,['-O']),('bundled312',PY312,[])]:
  out=TMP/'rebuild';out.mkdir();fds={};old={}
  for n in DESTS:
   p=out/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b'OLD OUTPUT '+n.encode());fds[n]=p.open('rb');old[n]=p.stat().st_ino
  r=call([py,*flags,'-B',str(SRC/'build_package.py'),'--output-dir',str(out),'--pdf',str(PDF)])
  need(r.returncode==0,r.stderr);rows=[]
  for n in DESTS:
   p=out/n;need(p.stat().st_ino!=old[n] and p.stat().st_nlink==1,'fresh inode '+n)
   need(fds[n].read()==b'OLD OUTPUT '+n.encode(),'old inode truncated '+n);fds[n].close()
   if n!='PACKAGE_INVENTORY.json':need(p.read_bytes()==(PRE/n).read_bytes(),'byte rebuild '+n)
   rows.append({'path':n,'fresh_regular_inode':True,'old_open_inode_unchanged':True,'byte_identical':True if n!='PACKAGE_INVENTORY.json' else 'timestamped receipt'})
  with zipfile.ZipFile(out/'zenodo-upload-kit.zip') as z:
   need(set(z.namelist())=={'paper.pdf','source-and-verification.zip','zenodo-deposit.json','zenodo-metadata.json','README.md'},'kit')
   d=json.loads(z.read('zenodo-deposit.json'));m=json.loads(z.read('zenodo-metadata.json'))
   need(d['files']==[{'path':'paper.pdf'},{'path':'source-and-verification.zip'}],'deposit count')
   need(d['metadata']==m['metadata']==json.loads((out/'zenodo-deposit.json').read_bytes())['metadata']==json.loads((out/'zenodo-metadata.json').read_bytes())['metadata'],'metadata copies')
   need(z.read('paper.pdf')==PDF.read_bytes() and z.read('source-and-verification.zip')==(out/'source-and-verification.zip').read_bytes(),'kit content')
  need({q.relative_to(out).as_posix() for q in out.rglob('*') if q.is_file()}==set(DESTS),'unexpected output files or temporary leftovers')
  need(tree(SRC)==before,'build source mutation');builds.append({'mode':label,'outputs':rows,'kit_metadata_two_payloads':True,'source_unchanged':True});shutil.rmtree(out)
 save('REBUILD_RECEIPT.json',{'utc':now(),'runs':builds,'source_closed_files':sum(1 for x in before.values() if x['kind']==stat.S_IFREG)})
 # Every stream independently recompressed rather than trusting builder settings.
 compress=[]
 for name in ('source-and-verification.zip','zenodo-upload-kit.zip'):
  raw=(PRE/name).read_bytes();streams=[]
  def deflate(b,l):
   c=zlib.compressobj(l,zlib.DEFLATED,-15);return c.compress(b)+c.flush()
  with zipfile.ZipFile(io.BytesIO(raw)) as z:
   need(z.testzip() is None,'CRC');need(z.namelist()==sorted(set(z.namelist())),'zip inventory')
   for i in z.infolist():
    h=struct.unpack_from('<4s5H3I2H',raw,i.header_offset);start=i.header_offset+30+h[-2]+h[-1];stream=raw[start:start+i.compress_size];b=z.read(i)
    need(h[0]==b'PK\x03\x04' and i.compress_type==8 and i.date_time==(2026,10,15,0,0,0) and i.external_attr>>16==0o100644,'zip attributes')
    need(stream==deflate(b,9),'level9 '+name+'/'+i.filename)
    streams.append({'path':i.filename,'compressed_bytes':len(stream),'matches_level9':True,'differs_from_default':stream!=deflate(b,-1)})
  compress.append({'archive':name,'members':len(streams),'distinguishing_streams':sum(x['differs_from_default'] for x in streams),'streams':streams})
 need(sum(x['members'] for x in compress)==125,'125streams');save('COMPRESSION_RECEIPT.json',{'utc':now(),'zlib':zlib.ZLIB_RUNTIME_VERSION,'archives':compress})
 # Import bytecode-free, compare exact structure and tolerance boundaries.
 sys.dont_write_bytecode=True;sys.path.insert(0,str(SRC));import verify_bundle as vb
 comps=[]
 for label,a,b,want in [('same',1.,1.,True),('within',1.,1.+5e-13,True),('outside',1.,1.+2e-12,False),('zero_near',0.,1e-300,False),('signedzero',-0.,0.,True),('nan',float('nan'),float('nan'),False),('inf',float('inf'),float('inf'),False),('neg_inf',float('-inf'),float('-inf'),False),('int_float',1,1.,False),('bool_int',True,1,False),('keys',{'a':1},{'b':1},False),('list_len',[1],[1,2],False),('count',4187,4188,False),('negative',-1.,-1.-5e-13,True),('nested_type',{'a':[1]},{'a':[True]},False),('small_relative',1e-200,1e-200*(1+2e-12),False)]:
  ok=True
  try:vb.compare_diagnostics(a,b)
  except ValueError:ok=False
  need(ok==want,label);comps.append({'case':label,'accepted':ok,'expected':want})
 save('COMPARATOR_RECEIPT.json',{'relative':1e-12,'absolute':0,'cases':comps})
 # Physical negative fixtures. Snapshot AFTER fixture setup, BEFORE invocation.
 attacks=[];case=TMP/'case'
 def one(label,mut=None,kind='verify',setup=None,opt=2):
  if case.exists():shutil.rmtree(case)
  case.mkdir();s=case/'input';closed_copy(s);o=case/'out';p=case/'supplied.pdf';p.write_bytes(PDF.read_bytes())
  if mut:mut(s)
  argsout=o
  if setup:
   changed=setup(s,o,p)
   if changed:argsout,p=changed
  b=tree(case)
  args=[sys.executable,'-O','-B',str(s/('build_package.py' if kind=='build' else 'verify_bundle.py'))]
  if kind=='build':args+=['--output-dir',str(argsout),'--pdf',str(p)]
  else:args+=['--integrity-only','--pdf',str(p)]
  r=call(args,opt);after=tree(case)
  need(r.returncode!=0,'accepted attack '+label);need(after==b,'pre-write preservation failed '+label)
  attacks.append({'case':label,'exit':r.returncode,'rejected_before_change':True,'stderr_tail':r.stderr.splitlines()[-1] if r.stderr.splitlines() else ''})
  shutil.rmtree(case)
 def modfile(name):
  def f(s):(s/name).write_bytes((s/name).read_bytes()+b'\nCHANGED\n')
  return f
 for n in ['paper.tex','zenodo-metadata.json','historical_candidate/author/PROOF.md','historical_candidate/archives/QUASICONICAL_30005613_AUTHOR_SAFE_FREEZE.zip','audit/review_geometry_family/REPORT.md']:
  one('changed_'+n,modfile(n))
 for n in ['paper.tex','audit/review_spectral_family/REPORT.md']:
  one('missing_'+n,lambda s,n=n:(s/n).unlink())
 for n in ['extra','.hidden','historical_candidate/.hidden','audit/review_geometry_family/.extra']:
  one('extra_'+n,lambda s,n=n:(s/n).write_text('extra'))
 one('emptydir',lambda s:(s/'empty').mkdir())
 one('source_symlink',lambda s:(s/'link').symlink_to(s/'paper.tex'))
 one('source_fifo',lambda s:os.mkfifo(s/'fifo'))
 for bad in ['/abs','../paper.tex','a/../b','a//b','./paper.tex','a/./b','a\\b','']:
  one('unsafe_manifest_'+repr(bad),lambda s,bad=bad:editj(s/'MANIFEST.json',lambda m:m['files'][0].update(path=bad)))
 one('manifest_duplicate',lambda s:editj(s/'MANIFEST.json',lambda m:m['files'].append(m['files'][0])))
 one('manifest_self',lambda s:editj(s/'MANIFEST.json',lambda m:m['files'].append({'path':'MANIFEST.json','bytes':0,'sha256':'0'*64})))
 for family in ['historical_candidate','audit/review_geometry_family','audit/review_spectral_family','audit/review_spectral_family_addendum','audit/priority_audit','audit/priority_adversary01']:
  mf='PUBLICATION_MANIFEST.json' if family=='historical_candidate' else 'MANIFEST.json'
  def mut(s,f=family,mf=mf):
   q=s/f/mf;q.write_bytes(q.read_bytes()+b' ');rehash(s)
  one('repinned_'+family,mut)
 def addreview(s):
  q=s/'audit/review_geometry_family/.extra';q.write_text('x');editj(s/'MANIFEST.json',lambda m:m['files'].append({'path':q.relative_to(s).as_posix(),**ident(q.read_bytes())}))
 one('rehash_extra_review',addreview)
 def repinproof(s):modfile('historical_candidate/author/PROOF.md')(s);rehash(s)
 one('repinned_original_proof',repinproof)
 for n in DESTS:
  for typ in ['direct_symlink','dangling_symlink','directory','fifo','source_hardlink','foreign_hardlink','PDF_overlap']:
   def setup(s,o,p,n=n,t=typ):
    o.mkdir();d=o/n;d.parent.mkdir(parents=True,exist_ok=True)
    if t=='direct_symlink':d.symlink_to(s/'paper.tex')
    elif t=='dangling_symlink':d.symlink_to(case/'no-such-target')
    elif t=='directory':d.mkdir()
    elif t=='fifo':os.mkfifo(d)
    elif t=='source_hardlink':os.link(s/'paper.tex',d)
    elif t=='foreign_hardlink':
     (case/'foreign').write_bytes(b'foreign');os.link(case/'foreign',d)
    else:d.write_bytes(PDF.read_bytes());return o,d
   one(typ+'_'+n,kind='build',setup=setup)
 for ancestor in ['output','output/pdf']:
  for typ in ['source_link','foreign_link','dangling_link','file','fifo']:
   def setup(s,o,p,a=ancestor,t=typ):
    o.mkdir();d=o/a;d.parent.mkdir(parents=True,exist_ok=True)
    if t=='source_link':d.symlink_to(s,target_is_directory=True)
    elif t=='foreign_link':d.symlink_to(case,target_is_directory=True)
    elif t=='dangling_link':d.symlink_to(case/'absent',target_is_directory=True)
    elif t=='file':d.write_bytes(b'parent sentinel')
    else:os.mkfifo(d)
   one('ancestor_'+ancestor+'_'+typ,kind='build',setup=setup)
 def top_link(s,o,p):o.symlink_to(case,target_is_directory=True)
 one('output_root_symlink',kind='build',setup=top_link)
 def intermediate_link(s,o,p):
  (case/'ancestor').symlink_to(case,target_is_directory=True);return case/'ancestor'/'out',p
 one('root_parent_symlink',kind='build',setup=intermediate_link)
 one('closed_output',kind='build',setup=lambda s,o,p:(s/'inside',p))
 def wrongpdf(s,o,p):p.write_bytes(b'%PDF-WRONG')
 one('wrong_external_PDF',kind='build',setup=wrongpdf)
 save('PHYSICAL_ATTACKS.json',{'utc':now(),'count':len(attacks),'cases':attacks,'static_fixtures_only':True,'all_source_and_output_path_types_bytes_inodes_unchanged_on_rejection':True})
 need(tree(SRC)==before,'final source mutation')
 print(json.dumps({'status':'PASS','replay_modes':len(replay),'exact_rebuilds':len(builds),'physical_rejections':len(attacks),'compression_members':125,'originals':39,'archive_identities':3,'comparator_cases':len(comps)}))
if __name__=='__main__':main()
