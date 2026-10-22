#!/usr/bin/env python3
"""Authenticate a frozen author packet; replay independent and author controls.
Only metadata is emitted. All mutations occur in temporary copies.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import runpy
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile

ANCHORS={
 'archive':(24236,'533268c19efeb1e024777bfca36afbb20ee4e9ee09ab0fd01c7d3fc0bfed8564'),
 'AUTHOR_MANIFEST.json':(1787,'690e26d6f9b86e3c95ca74213a49f90c5f9fce5cd769c512bc3698904300e782'),
 'bootstrap.py':(4362,'203a1d8f5a9e49dc0eddfc4eff73c39751b07ceb029d544ac6b07d5e4a8f7f6e'),
 'packet/PROOF.md':(18562,'c04d615722f2f2498eaeaff86f21cc7b0d5dd0cd8e1e96c324b16fb7413f57e3')}
MODES=[('normal',[]),('-O',['-O']),('-OO',['-OO'])]
class Failure(Exception):pass
def need(value,message):
 if not value:raise Failure(message)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def pin(path):
 raw=path.read_bytes();return len(raw),sha(raw)
def unique(items):
 out={}
 for key,value in items:
  need(key not in out,'duplicate JSON key');out[key]=value
 return out
def nonfinite(value):raise Failure('nonfinite JSON')
def parse(raw):return json.loads(raw,object_pairs_hook=unique,parse_constant=nonfinite)
def ordinary(path):
 need(not path.is_symlink() and stat.S_ISREG(path.stat().st_mode),'nonregular input');return path.read_bytes()
def snapshot(root):
 out={}
 for p in root.rglob('*'):
  name=str(p.relative_to(root));mode=p.lstat().st_mode
  if stat.S_ISLNK(mode):out[name]=('symlink',os.readlink(p))
  elif stat.S_ISDIR(mode):out[name]=('directory',)
  elif stat.S_ISREG(mode):out[name]=('regular',*pin(p))
  else:out[name]=('other',stat.S_IFMT(mode))
 return out
def authenticate(root,archive):
 need(pin(archive)==ANCHORS['archive'],'archive external anchor')
 need({p.name for p in root.iterdir()}=={'AUTHOR_MANIFEST.json','bootstrap.py','packet'},'root inventory')
 for name,expected in ANCHORS.items():
  if name!='archive':need((len(ordinary(root/name)),sha(ordinary(root/name)))==expected,'external anchor: '+name)
 manifest=parse(ordinary(root/'AUTHOR_MANIFEST.json'))
 names={'AUTHOR_MANIFEST.json','bootstrap.py'}
 for item in manifest['files']:
  name=item['path'];need('/' not in name and '\\' not in name and name not in ('','.','..'),'manifest path')
  full='packet/'+name;need(full not in names,'duplicate inventory');names.add(full)
  raw=ordinary(root/full);need((len(raw),sha(raw))==(item['bytes'],item['sha256']),'payload pin: '+name)
 need({p.name for p in (root/'packet').iterdir()}=={n[7:] for n in names if n.startswith('packet/')},'packet inventory')
 with zipfile.ZipFile(archive) as z:
  members=z.namelist();need(len(members)==len(set(members)) and set(members)==names,'ZIP inventory')
  for item in z.infolist():
   need(not item.is_dir(),'ZIP directory');need(z.read(item.filename)==ordinary(root/item.filename),'ZIP member bytes')
 return manifest

def process(script,flags=(),args=(),env=None,cwd=None):
 return subprocess.run([sys.executable,'-I','-S','-B',*flags,str(script),*map(str,args)],
  stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=120,env=env,cwd=cwd)
def success(p,message):
 need(p.returncode==0,message+': '+p.stderr.decode('utf8','replace'));return parse(p.stdout)
def failure(p,message):
 need(p.returncode!=0 and not p.stdout,message+' did not fail closed')
 need(b'AUDIT_UNAUTHENTICATED_CODE_EXECUTED' not in p.stderr,'unauthenticated verifier execution')
def restore(root):
 for p in root.rglob('*'):
  if not p.is_symlink():os.chmod(p,0o755 if p.is_dir() else 0o644)
 os.chmod(root,0o755)
def copy_author(root,target):shutil.copytree(root,target);return target

def mutation(root,label):
 packet=root/'packet';manifest=root/'AUTHOR_MANIFEST.json'
 if label=='same_length_proof':
  p=packet/'PROOF.md';b=p.read_bytes();p.write_bytes(bytes([b[0]^1])+b[1:])
 elif label=='missing_proof':(packet/'PROOF.md').unlink()
 elif label=='extra_root':(root/'unexpected').write_text('x')
 elif label=='nested_packet_directory':(packet/'nested').mkdir()
 elif label=='proof_symlink':
  outside=root.parent/(root.name+'-proof');shutil.copyfile(packet/'PROOF.md',outside)
  (packet/'PROOF.md').unlink();(packet/'PROOF.md').symlink_to(outside)
 elif label=='proof_fifo':(packet/'PROOF.md').unlink();os.mkfifo(packet/'PROOF.md')
 elif label=='packet_symlink':
  outside=root.parent/(root.name+'-packet');packet.rename(outside);packet.symlink_to(outside,target_is_directory=True)
 elif label=='manifest_duplicate':manifest.write_bytes(b'{"files":[],"files":[]}')
 elif label=='manifest_nan':manifest.write_bytes(b'{"files":NaN}')
 elif label=='manifest_bad_utf8':manifest.write_bytes(b'\xff')
 elif label=='manifest_boolean_integer':
  value=parse(manifest.read_bytes());value['problem_id']=True;manifest.write_text(json.dumps(value))
 elif label=='manifest_traversal':
  value=parse(manifest.read_bytes());value['files'][0]['path']='../outside';manifest.write_text(json.dumps(value))
 elif label=='rehashed_forged_verifier':
  (packet/'verify.py').write_text("raise RuntimeError('AUDIT_UNAUTHENTICATED_CODE_EXECUTED')\n")
  value=parse(manifest.read_bytes())
  for item in value['files']:
   size,digest=pin(packet/item['path']);item.update(bytes=size,sha256=digest)
  manifest.write_text(json.dumps(value,sort_keys=True))
 elif label=='unreadable_proof':os.chmod(packet/'PROOF.md',0)
 elif label=='diagnostics_tamper':(packet/'DIAGNOSTICS.json').write_bytes(b'{}\n')
 else:raise Failure('unknown mutation')

MUTATIONS=['same_length_proof','missing_proof','extra_root','nested_packet_directory','proof_symlink',
 'proof_fifo','packet_symlink','manifest_duplicate','manifest_nan','manifest_bad_utf8',
 'manifest_boolean_integer','manifest_traversal','rehashed_forged_verifier','unreadable_proof','diagnostics_tamper']

def semantic_mutation(root,label):
 packet=root/'packet'
 if label.startswith('claims_'):
  path=packet/'CLAIMS.json';value=parse(path.read_bytes())
  if label=='claims_duplicate':path.write_bytes(b'{"x":0,"x":1}');return
  if label=='claims_nonfinite':path.write_bytes(b'{"x":NaN}');return
  if label=='claims_solved':value['disposition']='solved'
  if label=='claims_bool_id':value['problem_id']=True
  if label=='claims_bool_approaches':value['approaches']=True
  if label=='claims_full_solution':value['full_solution']=True
 else:
  path=packet/'APPROACH_LEDGER.json';value=parse(path.read_bytes())
  if label=='ledger_repeat_turn':value['approaches'][1]['turn']=1
  if label=='ledger_bool_count':value['count']=True
  if label=='ledger_duplicate_name':value['approaches'][1]['approach']=value['approaches'][0]['approach']
 path.write_text(json.dumps(value))
SEMANTIC=['claims_duplicate','claims_nonfinite','claims_solved','claims_bool_id','claims_bool_approaches',
 'claims_full_solution','ledger_repeat_turn','ledger_bool_count','ledger_duplicate_name']

def independent_artifact_controls(root,archive):
 results=[]
 for label,flags in MODES:
  with tempfile.TemporaryDirectory(prefix='transverse-independent-audit-') as temporary:
   base=Path(temporary);good=copy_author(root,base/'relocated packet with spaces')
   before=snapshot(good);expected=process(good/'bootstrap.py',flags,cwd=base)
   success(expected,'relocated bootstrap')
   for p in good.rglob('*'):os.chmod(p,0o555 if p.is_dir() else 0o444)
   os.chmod(good,0o555)
   try:
    readonly=process(good/'bootstrap.py',flags,cwd=base);success(readonly,'read-only bootstrap')
    need(readonly.stdout==expected.stdout,'read-only output changed')
    need(snapshot(good)==before,'read-only packet bytes/inventory changed')
   finally:restore(good)
   hostile=base/'hostile';hostile.mkdir();(hostile/'json.py').write_text("raise RuntimeError('hostile module')")
   env=dict(os.environ,PYTHONPATH=str(hostile),PYTHONSTARTUP=str(hostile/'json.py'))
   isolated=process(good/'bootstrap.py',flags,env=env,cwd=hostile)
   success(isolated,'hostile import isolation');need(isolated.stdout==expected.stdout,'isolation output')
   rejects=0
   for i,name in enumerate(MUTATIONS):
    bad=copy_author(root,base/('mutant-'+str(i)));mutation(bad,name)
    try:failure(process(bad/'bootstrap.py',flags),name);rejects+=1
    finally:restore(bad)
   failure(process(good/'bootstrap.py',flags,args=['unexpected']),'unexpected argument');rejects+=1
   linked=base/'linked author root';linked.symlink_to(good,target_is_directory=True)
   failure(process(linked/'bootstrap.py',flags),'symlink author root');rejects+=1
   for i,name in enumerate(SEMANTIC):
    bad=copy_author(root,base/('semantic-'+str(i)));semantic_mutation(bad,name)
    failure(process(bad/'packet/verify.py',flags),name);rejects+=1
   # External anchors must reject a substituted bootstrap before executing it.
   bad=copy_author(root,base/'forged-bootstrap');(bad/'bootstrap.py').write_text("raise RuntimeError('AUDIT_UNAUTHENTICATED_CODE_EXECUTED')\n")
   try:authenticate(bad,archive)
   except Failure:rejects+=1
   else:raise Failure('substituted bootstrap authenticated')
   results.append({'mode':label,'accepted':3,'rejected':rejects,'semantic_payload_rejections':len(SEMANTIC),
    'read_only_bytes_unchanged':True})
 # Reach the strict JSON parser directly, independently of the earlier raw-hash barrier.
 namespace=runpy.run_path(str(root/'packet/verify_corpus.py'),run_name='authenticated_parser_unit_test')
 parse_count=0
 for raw in (b'',b'{',b'{"x":1,"x":2}',b'{"x":NaN}',b'{"x":Infinity}',b'{"x":-Infinity}',b'\xff'):
  try:namespace['parse'](raw)
  except Exception:parse_count+=1
  else:raise Failure('strict corpus parser accepted malformed bytes')
 return {'modes':results,'direct_parser_rejections':parse_count,
  'limits':'Mutation controls concern fixed-byte integrity and declared semantics, not adversarial filesystem races.'}

def source_replay(root,source):
 metadata=parse((root/'packet/SOURCE_PINS.json').read_bytes())
 results=[]
 for stem,item in zip(['calegari_2002','calegari_triangulations','bowden_approximation'],metadata['sources']):
  entry={'title':item['title'],'public_url':item['public_url']}
  for extension,key in [('pdf','pdf'),('txt','extraction')]:
   actual=pin(source/(stem+'.'+extension));expected=item[key]
   need(actual==(expected['bytes'],expected['sha256']),'source pin '+stem)
   entry[key]={'bytes':actual[0],'sha256':actual[1],'match':True}
  if shutil.which('pdftotext'):
   p=subprocess.run(['pdftotext','-layout',str(source/(stem+'.pdf')),'-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=60)
   need(p.returncode==0,'fresh PDF extraction')
   entry['fresh_extraction']={'bytes':len(p.stdout),'sha256':sha(p.stdout),
     'matches_retained_extraction':sha(p.stdout)==item['extraction']['sha256']}
  results.append(entry)
 return {'status':'pass','sources':results,'source_contents_emitted':False,
  'lickorish':'Opening theorem text inspected through indexed primary facsimile; no local full-PDF pin.'}

def run():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--author-root',type=Path,required=True)
 parser.add_argument('--author-archive',type=Path,required=True)
 parser.add_argument('--problems',type=Path)
 parser.add_argument('--research-results',type=Path)
 parser.add_argument('--source-dir',type=Path)
 args=parser.parse_args()
 root=args.author_root.absolute();archive=args.author_archive.absolute()
 need(bool(args.problems)==bool(args.research_results),'both complete corpus inputs are required')
 manifest=authenticate(root,archive);before=snapshot(root);archive_before=pin(archive)
 own=Path(__file__).absolute().parent
 author_runs=[];exact_runs=[];corpus=[]
 exact_output=None
 for label,flags in MODES:
  author_runs.append({'mode':label,'result':success(process(root/'bootstrap.py',flags),'author bootstrap')})
  p=process(own/'exact_controls.py',flags);result=success(p,'independent exact controls')
  if exact_output is None:exact_output=p.stdout
  need(p.stdout==exact_output,'optimization exact result mismatch')
  exact_runs.append({'mode':label,'result_sha256':sha(p.stdout),'result':result})
  if args.problems:
   result=success(process(root/'packet/verify_corpus.py',flags,
    args=[args.problems.absolute(),args.research_results.absolute()]),'author full-corpus replay')
   corpus.append({'mode':label,'result':result})
 author_controls=success(process(root/'packet/test_bootstrap.py'),'author adversarial harness')
 own_controls=independent_artifact_controls(root,archive)
 sources=source_replay(root,args.source_dir.absolute()) if args.source_dir else {'status':'not_requested'}
 need(snapshot(root)==before and pin(archive)==archive_before,'original author bytes changed')
 return {'schema':'transverse-surgery-independent-replay-v1','status':'pass','problem_id':10300034,
  'author_manifest_sha256':ANCHORS['AUTHOR_MANIFEST.json'][1],'author_payload_members':len(manifest['files']),
  'author_bootstrap':author_runs,'author_adversarial_controls':author_controls,
  'independent_exact':exact_runs,'independent_artifact_controls':own_controls,
  'full_corpus_replay':corpus if corpus else {'status':'not_requested'},'source_replay':sources,
  'original_author_bytes_unchanged':True,'contents_emitted':False,
  'limits':'Acceptance is scoped to the authored partial results; these finite checks do not decide the universal surgery question.'}

if __name__=='__main__':
 try:print(json.dumps(run(),sort_keys=True,separators=(',',':')))
 except (Failure,OSError,ValueError,TypeError,KeyError,subprocess.SubprocessError,zipfile.BadZipFile) as exc:
  print('FAIL: '+str(exc),file=sys.stderr);sys.exit(1)
