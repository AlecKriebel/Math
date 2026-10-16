#!/usr/bin/env python3
import argparse, datetime, hashlib, json, os, pathlib, stat, subprocess, zipfile
R=pathlib.Path(__file__).resolve().parent
P=R.parents[3]
ROOT=P.parent
A=R.parents[1]
def sha(b): return hashlib.sha256(b).hexdigest()
def run(*a): return subprocess.check_output(a,cwd=ROOT)
def pin(p):
 b=p.read_bytes(); return {'bytes':len(b),'sha256':sha(b)}
def perform(candidate,live=False):
 original='704685791ec0053dc0a52590fdef49ed4aae61d9'
 base='unsolved_math_prioritization/attempts/30002555/'
 expected=json.loads((A/'ORIGINAL_SNAPSHOT.json').read_text())['files']
 tree=run('git','ls-tree','-r','--name-only',original,'--',base).decode().splitlines()
 if set(tree)!=set(expected) or len(tree)!=27: raise RuntimeError('original tree inventory')
 seen={str(p.relative_to(A/'original')) for p in (A/'original'/base).rglob('*') if p.is_file()}
 if seen!=set(expected): raise RuntimeError('disk original inventory')
 orig={}
 for name,h in expected.items():
  blob=run('git','show',original+':'+name); disk=(A/'original'/name).read_bytes()
  if sha(blob)!=h or blob!=disk: raise RuntimeError('original byte mismatch '+name)
  orig[name]={'bytes':len(blob),'sha256':h,'git_blob':run('git','rev-parse',original+':'+name).decode().strip(),'git_equals_disk':True}
 freeze=candidate/'PREPUBLICATION_FREEZE.json'; f=json.loads(freeze.read_text())
 if sha(freeze.read_bytes())!='c2c04a478b9f865655fb71b2b87945f01a2f4e41b4a78140e2eea42157f422cd': raise RuntimeError('freeze pin')
 if len(f['files'])!=14: raise RuntimeError('freeze14')
 candidatefiles={}
 for name,v in f['files'].items():
  p=candidate/name
  if not stat.S_ISREG(p.lstat().st_mode) or pin(p)!=v: raise RuntimeError('frozen file mismatch '+name)
  canonical=A/'publication'/name
  rel=str(canonical.relative_to(ROOT))
  blob=run('git','show','19c1c3a32d560bba70488efb929126b15a0a88ef:'+rel)
  if blob!=p.read_bytes(): raise RuntimeError('current Git/frozen mismatch '+name)
  candidatefiles[name]={**v,'checkpoint48_git_equals_candidate':True}
 zpath=candidate/'rotational-veech-source-verification-v1.0.zip'
 with zipfile.ZipFile(zpath) as z:
  infos=z.infolist(); names=[x.filename for x in infos]
  if len(set(names))!=len(names) or len(names)!=134 or any(x.is_dir() for x in infos): raise RuntimeError('archive inventory')
  members={n:z.read(n) for n in names}
  if sha(members['PACKAGE_MANIFEST.json'])!=f['package_manifest_sha256']: raise RuntimeError('package manifest pin')
  manifest=json.loads(members['PACKAGE_MANIFEST.json'])
  if len(manifest['files'])!=133 or set(names)!=set(manifest['files'])|{'PACKAGE_MANIFEST.json'}: raise RuntimeError('closed archive payload map')
  for info in infos:
   n=info.filename
   if not stat.S_ISREG(info.external_attr>>16): raise RuntimeError('nonregular archive entry '+n)
   if pathlib.PurePosixPath(n).as_posix()!=n or n.startswith('/') or any(x in ('','.','..') for x in n.split('/')) or '\\' in n: raise RuntimeError('unsafe archive entry '+n)
   if n!='PACKAGE_MANIFEST.json' and manifest['files'][n]!={'bytes':len(members[n]),'sha256':sha(members[n])}: raise RuntimeError('archive payload changed '+n)
  # The archived verifier supplies closed schema validation; independently check every authenticated original blob.
  for name,v in orig.items():
   matches=[n for n in names if n=='original_packet/'+name.removeprefix(base)]
   if len(matches)!=1 or sha(members[matches[0]])!=v['sha256']: raise RuntimeError('archive original mismatch '+name)
  archive={'regular_members':len(names),'payload_members':len(names)-1,'every_payload_fingerprint_checked':True,'sha256':sha(zpath.read_bytes()),'manifest_sha256':sha(members['PACKAGE_MANIFEST.json'])}
 head=run('git','rev-parse','HEAD').decode().strip()
 index=pathlib.Path(run('git','rev-parse','--git-path','index').decode().strip()); index=ROOT/index if not index.is_absolute() else index
 rawhead=pathlib.Path(run('git','rev-parse','--git-path','HEAD').decode().strip()); rawhead=ROOT/rawhead if not rawhead.is_absolute() else rawhead
 branch=run('git','symbolic-ref','HEAD').decode().strip()
 if branch!='refs/heads/main': raise RuntimeError('not main')
 row=[s for s in run('git','show',original+':unsolved_math_prioritization/QUEUE.md').decode().splitlines() if '30002555 /' in s]
 if len(row)!=1 or '| claimed_solved | 1/5 |' not in row[0]: raise RuntimeError('exact original queue gate')
 livepr=None
 if live:
  livepr=json.loads(run('gh','pr','view','919','--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,headRefName,baseRefName,title,body'))
  if livepr['number']!=919 or livepr['headRefOid']!=original or livepr['state']!='OPEN' or not livepr['isDraft']: raise RuntimeError('live gate')
 return {'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'original_head':original,'original_files':orig,'candidate_files':candidatefiles,'freeze':pin(freeze),'archive':archive,'pdf':pin(candidate/'output/pdf/note.pdf'),'shared_state':{'head_commit':head,'branch':branch,'raw_HEAD':pin(rawhead),'raw_index':pin(index)},'exact_original_queue_row':row[0],'live_pr':livepr,'original_author_turns':'1/5','audit_proof_search_turns':0}
if __name__=='__main__':
 p=argparse.ArgumentParser(); p.add_argument('--candidate',type=pathlib.Path,default=A/'publication'); p.add_argument('--output',type=pathlib.Path,required=True); p.add_argument('--live',action='store_true'); a=p.parse_args()
 a.output.write_text(json.dumps(perform(a.candidate,a.live),indent=2)+'\n')
