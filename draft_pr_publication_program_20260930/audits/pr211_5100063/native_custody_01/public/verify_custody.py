"""PR211 offline read-only public/private artifact custody verifier (stdlib only)."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,io,json,re,stat,zipfile
P=Path(__file__).resolve().parent;B=P.parent

def need(v,s):
 if not v:raise ValueError(s)
def safe(s):
 p=PurePosixPath(s);need(not p.is_absolute() and str(p)==s and '..' not in p.parts,'Unsafe path');return p
def data(root,s):
 q=root/str(safe(s));need(q.is_file() and not q.is_symlink() and q.resolve()==q,'Noncanonical regular file '+s);return q.read_bytes()
def load(root,s):return json.loads(data(root,s))
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def native(k,b):return hashlib.sha1(k.encode()+b' '+str(len(b)).encode()+b'\0'+b).hexdigest()

def main(private=False):
 m=load(P,'MANIFEST.json');allowed={x['path'] for x in m['files']}|{'MANIFEST.json'};actual={str(x.relative_to(P)) for x in P.rglob('*') if x.is_file()};need(actual==allowed,'Public allowlist closure')
 for x in m['files']:need(pin(data(P,x['path']))=={k:x[k] for k in ['bytes','sha256']},'Public file pin '+x['path'])
 d=load(P,'CUSTODY_IDENTITIES.json');trees=load(P,'NATIVE_TREES.json')
 for oid,rows in trees.items():
  body=b''.join((x['mode'].lstrip('0')+' '+n).encode()+b'\0'+bytes.fromhex(x['sha']) for n,x in sorted(rows.items(),key=lambda z:(z[0]+('/' if z[1]['type']=='tree' else '')).encode()));need(native('tree',body)==oid,'Tree hash '+oid)
 for x in d['commits']:
  b=data(P,x['path']);need(pin(b)=={k:x[k] for k in ['bytes','sha256']} and native('commit',b)==x['sha'],'Raw commit '+x['sha']);head=b.split(b'\n\n',1)[0].splitlines();need(head[0]==b'tree '+x['tree'].encode(),'Commit tree');need([z[7:].decode() for z in head if z.startswith(b'parent ')]==x['parents'],'Ordered commit parents')
 def lookup(root,path):
  oid=root
  for n in safe(path).parts:
   x=trees[oid].get(n)
   if x is None:return None
   oid=x['sha']
  return x
 snap=d['snapshots']
 for label,skey in [('original','original'),('prepared','revised'),('current_MAIN','current_MAIN')]:
  root=snap[skey]['tree']
  for x in d['own_body_identities'][label]:need(lookup(root,x['path'])=={k:x[k] for k in ['mode','type','sha']},'Own identity ancestry '+label+'/'+x['path'])
 for x in d['selected_frozen_publication_identities']:need(lookup(snap['merge']['tree'],x['path'])=={k:x[k] for k in ['mode','type','sha']},'Publication identity ancestry '+x['path'])
 for x in d['original_history_exact_coverage']['records']:need(x['exact'] and x['original_git_blob']==x['archive_git_blob'],'Original archive identity')
 changed=[]
 def walk(a,b,path):
  if a==b:return
  if a and a['type']=='tree' or b and b['type']=='tree':
   aa=trees[a['sha']] if a and a['type']=='tree' else {};bb=trees[b['sha']] if b and b['type']=='tree' else {}
   if a and a['type']!='tree' or b and b['type']!='tree':changed.append({'path':path,'before':a,'after':b})
   for n in sorted(set(aa)|set(bb)):walk(aa.get(n),bb.get(n),path+'/'+n if path else n)
  else:changed.append({'path':path,'before':a,'after':b})
 walk({'mode':'040000','type':'tree','sha':snap['merge_first_parent']['tree']},{'mode':'040000','type':'tree','sha':snap['merge']['tree']},'');need(changed==d['actual_merge_changed_leaves'],'Complete merged native leaf delta')
 groups={'own_attempt':0,'old_owned_audit':0,'QUEUE':0,'foreign':0}
 for x in changed:
  p=x['path'];k='own_attempt' if p.startswith('unsolved_math_prioritization/attempts/5100063/') else 'old_owned_audit' if p.startswith('draft_pr_descending_audit_20261002/audits/pr211_5100063/') else 'QUEUE' if p=='unsolved_math_prioritization/QUEUE.md' else 'foreign';groups[k]+=1
 need(groups==d['actual_merge_scope_counts'] and groups['foreign']==0,'Foreign scope')
 for k,x in d['own_QUEUE_projection'].items():need(pin(x['own_row'].encode())==x['own_row_pin'],'Own row pin '+k)
 result={'public_allowlist_files':len(allowed),'native_trees':len(trees),'native_commits':len(d['commits']),'own_identity_counts':{k:len(v) for k,v in d['own_body_identities'].items()},'actual_merge_scope_counts':groups,'public_identity_verification':'PASS','private_body_witness_verified':False,'scientific_or_workflow_verdict':False}
 if private:
  seal=load(B,'PRIVATE_SEAL.json')
  for x in seal['files']:need(pin(data(B,x['path']))=={k:x[k] for k in ['bytes','sha256']},'Private seal '+x['path'])
  ledgers=['ORIGINAL_BODY_CUSTODY.json','REVISED_BODY_CUSTODY.json','CURRENT_MAIN_BODY_CUSTODY.json','OLD_AUDIT_BODY_CUSTODY.json'];num=0
  for name in ledgers:
   ledger=load(B,name)
   for x in ledger['records']:
    b=data(B,x['reading_copy']);need(pin(b)=={k:x[k] for k in ['bytes','sha256']} and native('blob',b)==x['sha'],'Private reading body '+x['path']);need(lookup(ledger['root'],x['path'])=={k:x[k] for k in ['mode','type','sha']},'Private body ancestry '+x['path']);num+=1
  q=load(B,'OWN_QUEUE_AND_FOREIGN_PRESERVATION.json')['snapshots'];fullq={}
  for label,x in q.items():
   b=data(B,'private_queues/'+label+'.md');need(pin(b)=={k:x[k] for k in ['bytes','sha256']} and native('blob',b)==x['git_blob'],'Private QUEUE native identity');row=x['own_row'].encode();need(b.count(row)==1,'Own row unique');need(pin(b.replace(row,b'',1))==x['foreign_bytes_pin'],'Foreign QUEUE witness');fullq[label]=b
  need(q['merge_first_parent']['foreign_bytes_pin']==q['merge']['foreign_bytes_pin'],'Foreign QUEUE preservation')
  old=load(B,'OLD_AUDIT_BODY_CUSTODY.json')['records'];om={x['path']:x for x in old};pre='draft_pr_descending_audit_20261002/audits/pr211_5100063/preprint/';get=lambda n:data(B,om[pre+n]['reading_copy']);pkg=json.loads(get('PACKAGE_MANIFEST.json'));src=json.loads(get('SOURCE_MANIFEST.json'));f=load(B,'FROZEN_PUBLICATION_AND_ZIP_IDENTITY.json');entrymap={x['logical_path']:x for x in f['ZIP_entries']};allb={}
  with zipfile.ZipFile(io.BytesIO(get('k904a-source-verification.zip'))) as z:
   need(z.testzip() is None,'ZIP CRC');need(len(z.infolist())==f['ZIP_entry_count']==pkg['source_archive_entries'],'ZIP count');names=[]
   for x in z.infolist():
    safe(x.filename);need(x.filename.startswith(f['ZIP_wrapper']),'ZIP wrapper');n=x.filename[len(f['ZIP_wrapper']):];safe(n);need(n not in names and not x.is_dir() and stat.S_IFMT(x.external_attr>>16) in (0,stat.S_IFREG),'ZIP duplicate/type');names.append(n);b=z.read(x);need(pin(b)=={k:entrymap[n][k] for k in ['bytes','sha256']},'ZIP entry pin');allb[n]=b
  need(set(allb)=={x['path'] for x in src['files']}|{'SOURCE_MANIFEST.json'},'ZIP closure');need(allb['SOURCE_MANIFEST.json']==get('SOURCE_MANIFEST.json'),'ZIP manifest body')
  for x in src['files']:need(pin(allb[x['path']])=={k:x[k] for k in ['bytes','sha256']},'Source manifest entry')
  for x in [pkg['source_manifest'],pkg['manuscript_source'],pkg['metadata']]+pkg['submission_files']:need(pin(get(x['path']))=={k:x[k] for k in ['bytes','sha256']},'Package manifest entry')
  for x in load(B,'ORIGINAL_BODY_CUSTODY.json')['records']:
   rel=x['path'].split('attempts/5100063/',1)[1];b=allb['pr_update/5100063/history/original_submission_20261015/'+rel];need(native('blob',b)==x['sha'],'ZIP exact original source')
  transport=sorted((B/'private_transport').glob('*.intent.json'))
  for p in transport:
   j=json.loads(p.read_text());need(j['method']=='GET' and j['automatic_retries']==0 and j['argv'][:6]==['/opt/homebrew/Cellar/gh/2.85.0/bin/gh','api','--hostname','github.com','--method','GET'],'Read-only transport grammar')
  result.update({'private_body_witness_verified':True,'private_reading_body_records':num,'ZIP_entries':len(allb),'private_transport_attempts':len(transport),'private_seal_files':len(seal['files']),'foreign_QUEUE_preservation':'PASS'})
 print(json.dumps(result,sort_keys=True))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--private',action='store_true');a=p.parse_args();main(a.private)
