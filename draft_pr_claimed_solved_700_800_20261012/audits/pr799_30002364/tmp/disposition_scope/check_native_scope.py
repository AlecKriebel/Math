"""Independent read-only immutable-commit audit of PR799's 8-path closure mirror.

Uses only GitHub GETs and writes its own report. No imports of mutating project
helpers, local Git writes, skipped mathematics, or production services.
"""
from pathlib import Path
import csv,datetime,hashlib,io,json,subprocess,sys,urllib.request
W=Path(__file__).resolve().parent;T=W.parent;A=T.parent
P='30002364';N='unsolved_math_prioritization';HEAD='cc45ec9dc93515593c3b2a228def86c3a562e13f'
FILES=['QUEUE.md','state.json','history.jsonl','catalog.json','ranking.csv','assessments.json','assessment_history.jsonl','attempts/30002364/PR799_PRIOR_RESULT.json']
ALLOWED={N+'/'+f for f in FILES}
def need(v,m):
 if not v:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def oid(kind,b):return hashlib.sha1(kind.encode()+b' '+str(len(b)).encode()+b'\0'+b).hexdigest()
def get(path):
 p=subprocess.run(['gh','api','repos/AlecKriebel/Math/'+path,'--method','GET'],capture_output=True,text=True,check=True)
 return json.loads(p.stdout)
def tree_oid(rows):
 ordered=sorted(rows.items(),key=lambda x:x[0].encode()+(b'/' if x[1]['type']=='tree' else b''))
 return oid('tree',b''.join(r['mode'].lstrip('0').encode()+b' '+n.encode()+b'\0'+bytes.fromhex(r['sha']) for n,r in ordered))
class Commit:
 def __init__(self,commit):
  self.commit=commit;self.meta=get('git/commits/'+commit);need(self.meta['sha']==commit,'Commit identity');self.root=self.meta['tree']['sha'];self.cache={}
 def tree(self,ident):
  if ident is None:return {}
  if ident not in self.cache:
   j=get('git/trees/'+ident);need(j['sha']==ident and not j.get('truncated'),'Nonrecursive tree identity')
   rows={r['path']:{k:r[k] for k in ['mode','type','sha']} for r in j['tree']}
   need(len(rows)==len(j['tree']) and tree_oid(rows)==ident,'Complete authenticated Git tree')
   self.cache[ident]=rows
  return dict(self.cache[ident])
 def entry(self,path):
  ident=self.root
  for i,n in enumerate(path.split('/')):
   row=self.tree(ident).get(n)
   if row is None:return None
   if i==len(path.split('/'))-1:return row
   need(row['type']=='tree','Path ancestor type');ident=row['sha']
 def text(self,path):
  row=self.entry(path);need(row and row['type']=='blob' and row['mode']=='100644','Expected regular text')
  req=urllib.request.Request('https://raw.githubusercontent.com/AlecKriebel/Math/'+self.commit+'/'+path,headers={'User-Agent':'PR799-independent-scope-audit'})
  with urllib.request.urlopen(req,timeout=60) as response:b=response.read()
  need(oid('blob',b)==row['sha'],'Immutable content Git blob hash');return b.decode()
 def rebuilt(self,replacements):
  trie={}
  for path,row in replacements.items():
   node=trie
   for n in path.split('/')[:-1]:node=node.setdefault(n,{})
   node[path.split('/')[-1]]=('replace',row)
  def rec(ident,changes):
   rows=self.tree(ident)
   for n,c in changes.items():
    if isinstance(c,tuple):rows[n]=c[1]
    else:
     old=rows.get(n);need(old is None or old['type']=='tree','Tree rebuild ancestor');rows[n]={'mode':'040000','type':'tree','sha':rec(old['sha'] if old else None,c)}
   return tree_oid(rows)
  return rec(self.root,trie)
def skip(s,p):
 while p<len(s) and s[p].isspace():p+=1
 return p
def object_members(raw):
 d=json.JSONDecoder();p=skip(raw,0);need(raw[p]=='{','Root object');p=skip(raw,p+1);out=[]
 while raw[p]!='}':
  start=p;k,q=d.raw_decode(raw,p);need(isinstance(k,str) and k not in [r[0] for r in out],'Unique root key');p=skip(raw,q);need(raw[p]==':','Colon');vstart=skip(raw,p+1);v,end=d.raw_decode(raw,vstart);out.append((k,raw[start:end],v));p=skip(raw,end)
  if raw[p]==',':p=skip(raw,p+1)
  else:need(raw[p]=='}','Object delimiter')
 need(not raw[p+1:].strip(),'Root trailing bytes');return out
def array_members(raw):
 d=json.JSONDecoder();p=skip(raw,0);need(raw[p]=='[','Root array');p=skip(raw,p+1);out=[]
 while raw[p]!=']':
  start=p;v,end=d.raw_decode(raw,p);need(isinstance(v,dict) and 'id' in v,'Catalog record');out.append((v['id'],raw[start:end],v));p=skip(raw,end)
  if raw[p]==',':p=skip(raw,p+1)
  else:need(raw[p]==']','Array delimiter')
 need(not raw[p+1:].strip(),'Array trailing bytes');return out

def main():
 receipt=json.loads((T/'root-receipts/NATIVE_PRIORITY_MIRROR_RECEIPT.json').read_text());disposition=json.loads((A/'DISPOSITION.json').read_text())
 need(receipt['result']=='PASS' and receipt['pr']==799 and receipt['problem']==P and receipt['status']=='already_solved','Receipt target/status')
 need(set(receipt['paths'])==ALLOWED and len(receipt['paths'])==8,'Exactly eight declared paths')
 before=Commit(receipt['parent']);after=Commit(receipt['commit'])
 need([r['sha'] for r in after.meta['parents']]==[receipt['parent']],'Ordinary single-parent native commit')
 changed={}
 def walk(left,right,prefix=''):
  aa=before.tree(left);bb=after.tree(right)
  for n in sorted(set(aa)|set(bb)):
   a,b=aa.get(n),bb.get(n)
   if a==b:continue
   path=prefix+n
   if (a is None or a['type']=='tree') and b is not None and b['type']=='tree':walk(a['sha'] if a else None,b['sha'],path+'/')
   else:
    need(a is None or a['type']=='blob','No removed/retyped tree');need(b and b['type']=='blob' and b['mode']=='100644','No removal or nonregular change');changed[path]=b
 walk(before.root,after.root)
 need(set(changed)==ALLOWED,'Full Merkle diff is exactly eight allowed paths')
 expected=before.rebuilt(changed);need(expected==after.root,'Independently rebuilt entire resulting root tree')
 old={f:before.text(N+'/'+f) for f in FILES[:-1]};new={f:after.text(N+'/'+f) for f in FILES}
 need(before.entry(N+'/'+FILES[-1]) is None,'New sidecar does not overwrite prior file')
 for f in FILES:need(sha(new[f].encode())==receipt['file_hashes'][N+'/'+f],'Published bytes match receipt')
 # Exact queue non-target physical rows; only target status/turn/findings may change.
 def qrow(s):
  rows=[x for x in s.splitlines(keepends=True) if x.startswith('| ') and (' '+P+' / ') in x];need(len(rows)==1,'Unique queue target');return rows[0]
 oq,nq=qrow(old['QUEUE.md']),qrow(new['QUEUE.md']);oc,nc=oq.split('|'),nq.split('|')
 need(old['QUEUE.md'].replace(oq,'<OWN ROW>')==new['QUEUE.md'].replace(nq,'<OWN ROW>'),'All other queue bytes')
 need(len(oc)==len(nc)==14 and nc[8].strip()=='already_solved' and nc[9].strip()=='5/5' and not nc[12].strip(),'Own native status/budget/blank DOI')
 need(all(oc[i]==nc[i] for i in range(14) if i not in (8,9,11)),'Only allowed own queue cells')
 need('mathematical PASS' in nc[11] and 'prior' in nc[11] and 'PR#799' in nc[11],'Own findings carry disposition')
 # Exact other JSON members/records and ordering.
 preserved_counts={}
 for f,parser in [('state.json',object_members),('assessments.json',object_members),('catalog.json',array_members)]:
  a,b=parser(old[f]),parser(new[f]);need([(k,v) for k,v,_ in a if k!=P]==[(k,v) for k,v,_ in b if k!=P],'Unrelated JSON member bytes/order: '+f)
  target=[r[2] for r in b if r[0]==P];need(len(target)==1,'Unique own JSON member: '+f);v=target[0];preserved_counts[f]=len([r for r in a if r[0]!=P])
  need(v['statement_hash']==disposition['statement_hash'] and v['review_hash']==disposition['review_hash'],'Own source hash preservation: '+f)
  if f=='state.json':need(v['status']=='already_solved' and v['turns_used']==5 and v['turn_limit']==5,'Own state outcome/budget')
  elif f=='assessments.json':need(v['resolution']=='already_solved' and v['decision']=='exclude','Own assessment exclusion')
  else:need(v['local_status']=='already_solved' and v['eligible'] is False and v['turns_used']==5 and v['rank'] is None,'Own catalog outcome/budget')
 # Histories preserve exact raw prefixes, append exactly one own event each.
 for f in ['history.jsonl','assessment_history.jsonl']:
  need(new[f].startswith(old[f]),'History byte prefix: '+f);suffix=new[f][len(old[f]):];lines=[s for s in suffix.splitlines() if s.strip()];need(len(lines)==1,'Exactly one appended event: '+f);e=json.loads(lines[0]);need(e['id']==P and e['statement_hash']==disposition['statement_hash'] and e['review_hash']==disposition['review_hash'],'Own appended event provenance')
  if f=='history.jsonl':need(e['status']=='already_solved' and e['turns_used']==5 and e['turn_limit']==5 and e['pr']==799,'Own history outcome/budget')
  else:need(e['resolution']=='already_solved' and e['decision']=='exclude','Own assessment-history outcome')
 # CSV is physical-row scoped, avoiding a global reserialization.
 aa=old['ranking.csv'].splitlines(keepends=True);bb=new['ranking.csv'].splitlines(keepends=True);need(aa[0]==bb[0],'Ranking header');header=next(csv.reader([aa[0]]));ix=header.index('id')
 def split_target(rows):
  targets=[(i,next(csv.reader([r]))) for i,r in enumerate(rows[1:],1) if next(csv.reader([r]))[ix]==P];need(len(targets)==1,'Unique CSV target');i,row=targets[0];return i,row,rows[:i]+rows[i+1:]
 oi,orow,oa=split_target(aa);ni,nrow,na=split_target(bb);need(oi==ni and oa==na,'All other CSV physical rows and position')
 need(nrow[header.index('local_status')]=='already_solved' and nrow[header.index('turns_used')]=='5' and nrow[header.index('eligible')]=='False','Own ranking outcome/budget')
 # Sidecar exactly binds executed disposition, changing only mirror timestamp.
 side=json.loads(new[FILES[-1]]);need({k:v for k,v in side.items() if k!='native_mirror_at'}==disposition,'Exact disposition sidecar');need(side['original_explicit_budget']=='5/5' and side['new_Zenodo_deposit'] is False and side['tracker_row_added'] is False,'No new publication claim')
 need(side['original_candidate_files']==54 and side['original_candidate_source_identity_sha256']=='a875b05b2fd00b21dde0328993d8ae6492588c9b02f03f2655ee6cdb0d51b9fe','Preserved candidate binding')
 # All original files remain authenticated at the reviewed branch head; none is among native changes.
 src=json.loads((T/'intake/ROOT_SOURCE_IDENTITY.json').read_text());orig=Commit(HEAD);original_main_present=0
 for r in src['original_files']:
  need(orig.entry(r['path'])=={'mode':'100644','type':'blob','sha':r['git_blob']},'Immutable original branch Git entry')
  need(r['path'] not in changed,'No native candidate rewrite')
  bef,aft=before.entry(r['path']),after.entry(r['path']);need(bef==aft,'Original main entry/absence preserved')
  original_main_present+=int(bef is not None)
 # Fresh independent metadata closure still agrees.
 pr=get('pulls/799');comment=get('issues/comments/6223000406')
 need(pr['state']=='closed' and pr['merged'] is False and pr['draft'] is True and pr['head']['sha']==HEAD,'Fresh exact-head closure')
 need(comment['body'].encode()==(T/'root-receipts/CLOSE_COMMENT.md').read_bytes(),'Fresh exact comment')
 result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS','scope':'Administrative immutable native/closure scope only; no new mathematics or whole-preprint review','pr':799,'problem':P,'commit':receipt['commit'],'parent':receipt['parent'],'before_root_tree':before.root,'after_root_tree':after.root,'independently_rebuilt_root_tree':expected,'complete_changed_paths':sorted(changed),'all_unrelated_Git_paths_modes_preserved':True,'other_JSON_raw_members_and_order_preserved':preserved_counts,'other_queue_bytes_preserved':True,'other_CSV_physical_rows_and_position_preserved':True,'histories_exact_prefix_and_one_own_append_each':True,'native_status':'already_solved','own_original_budget':'5/5','own_DOI_blank':True,'originals_confirmed_at_reviewed_head':54,'original_main_entries_present_unchanged':original_main_present,'original_main_entries_absent_unchanged':54-original_main_present,'new_Zenodo_deposit_or_tracker_row_claimed':False,'fresh_exact_head_closed_unmerged':True,'fresh_posted_comment_exact':True,'receipt_sha256':sha((T/'root-receipts/NATIVE_PRIORITY_MIRROR_RECEIPT.json').read_bytes())}
 (W/'NATIVE_SCOPE_READBACK.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
