"""Independent dated canonical main/QUEUE native transport and 24-withdrawal replay.
Read-only. No service calls, Git writes, publication actions or final authority.
"""
from pathlib import Path
import sys,json,hashlib,base64,datetime,re,copy
R=Path('/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7')
W=R/'audits/final_reconciliation_new_independent_adversary01'
IPIN='63f9f0d1cd4d8e8d87b3c087ce8db2535ef526db3f359e2df7f4c13ce550aa8a'
p=W/'independent_checks.py';b=p.read_bytes()
assert hashlib.sha256(b).hexdigest()==IPIN
n={'__name__':'_independent_queue_shared','__file__':str(p)}
exec(compile(b,str(p),'exec'),n)
need=n['need'];strict=n['strict'];typed=n['typed'];objpin=n['objpin'];H=n['H'];C=n['C']
API='https://api.github.com/repos/AlecKriebel/Math'
GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
MAP={'path':str(W/'HISTORICAL24_CANONICAL_WITHDRAWAL_MAP.json'),'bytes':46917,'sha256':'48e812369b09b27a69a85855cf1036dcb2b7dbb50cc1fee9b61e0595fca98a33'}
def utc(v):
 need(type(v)is str,'UTC original timestamp')
 d=datetime.datetime.fromisoformat(v.replace('Z','+00:00'))
 need(d.tzinfo is not None and d.utcoffset()==datetime.timedelta(0),'UTC-aware timestamp')
 return d
def http(e,url):
 need(type(e.get('returncode'))is int and e['returncode']==0,'Successful original CLI return')
 need(e.get('argv')==[GH,'api','--method','GET','--include',url],'Exact original full GET argv')
 raw=base64.b64decode(e['stdout_base64'],validate=True)
 base64.b64decode(e['stderr_base64'],validate=True)
 sep=b'\r\n\r\n'if b'\r\n\r\n'in raw else b'\n\n'
 need(sep in raw,'Original included HTTP envelope')
 head,body=raw.split(sep,1)
 hs=head.decode('utf-8').splitlines()
 need(bool(hs)and re.fullmatch(r'HTTP/[0-9.]+ 200(?: OK)?',hs[0])is not None,'Original HTTP200')
 need(sum(x.lower().startswith('content-type:')for x in hs)==1 and any(x.lower().startswith('content-type: application/json')for x in hs),'Original JSON HTTP content type')
 return strict(body)
def tree(t,sha):
 need(t.get('sha')==sha and t.get('url')==API+'/git/trees/'+sha and t.get('truncated')is False and type(t.get('tree'))is list,'Complete immutable tree')
 entries=t['tree'];names=[x['path']for x in entries]
 need(len(names)==len(set(names)),'Unique tree paths')
 need(all(type(x)is str and x and '/'not in x and '\x00'not in x for x in names),'Single component tree paths')
 need(all(x.get('mode')in('040000','100644','100755','120000','160000')and x.get('type')==('tree'if x['mode']=='040000'else 'commit'if x['mode']=='160000'else 'blob')and re.fullmatch('[0-9a-f]{40}',x.get('sha',''))for x in entries),'Typed complete Git tree entries')
 order=lambda x:x['path'].encode()+ (b'/'if x['type']=='tree'else b'')
 need(entries==sorted(entries,key=order),'Canonical Git tree ordering')
 raw=b''.join(x['mode'].lstrip('0').encode()+b' '+x['path'].encode()+b'\0'+bytes.fromhex(x['sha'])for x in entries)
 need(hashlib.sha1(b'tree '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==sha,'Full Git tree content-address reconstruction')
 return entries
def check_data(r,es,body,hist):
 need(r.get('kind')=='ROOT_FRESH_COMPLETE_CANONICAL_QUEUE_AND24_WITHDRAWALS','Exact dated receipt kind')
 need(len(es)==6,'All six originals')
 urls=[API+'/git/ref/heads/main',API+'/git/commits/'+r['remote_main'],API+'/git/trees/'+r['remote_tree'],API+'/git/trees/'+r['queue_folder_tree'],API+'/git/blobs/'+r['queue_blob'],API+'/git/ref/heads/main']
 chron=[];prior=None;ds=[]
 for e,u in zip(es,urls):
  a,z=utc(e.get('before')),utc(e.get('after'))
  need(z>=a and(prior is None or a>=prior),'Ordered original chronology')
  prior=z;chron.append({'before':e['before'],'after':e['after']})
  ds.append(http(e,u))
 need(utc(r['at'])>=prior and utc(r['at'])<=datetime.datetime.now(datetime.timezone.utc),'Dated receipt after native reads')
 for ref in(ds[0],ds[5]):
  need(ref.get('ref')=='refs/heads/main'and ref.get('url')==API+'/git/refs/heads/main'and ref.get('object')=={'sha':r['remote_main'],'type':'commit','url':API+'/git/commits/'+r['remote_main']},'Same remote main brackets')
 co=ds[1];need(co.get('sha')==r['remote_main']and co.get('url')==urls[1]and co.get('tree')=={'sha':r['remote_tree'],'url':API+'/git/trees/'+r['remote_tree']},'Immutable commit to complete top tree chain')
 ts=tree(ds[2],r['remote_tree'])
 sel=[x for x in ts if x['path']=='unsolved_math_prioritization']
 need(len(sel)==1 and sel[0]['type']=='tree'and sel[0]['sha']==r['queue_folder_tree'],'Exact QUEUE folder chain')
 qs=tree(ds[3],r['queue_folder_tree'])
 sel=[x for x in qs if x['path']=='QUEUE.md']
 need(len(sel)==1 and sel[0]['type']=='blob'and sel[0]['mode']=='100644'and sel[0]['sha']==r['queue_blob'],'Exact QUEUE blob tree chain')
 blob=ds[4]
 need(blob.get('sha')==r['queue_blob']and blob.get('url')==urls[4]and blob.get('encoding')=='base64'and type(blob.get('size'))is int and blob['size']==sel[0]['size'],'Exact complete blob body metadata')
 qb=base64.b64decode(''.join(blob['content'].split()),validate=True)
 need(len(qb)==blob['size']and hashlib.sha1(b'blob '+str(len(qb)).encode()+b'\0'+qb).hexdigest()==r['queue_blob'],'Decoded full Git blob SHA1 and bytes')
 need(H(qb)==r['queue_body_sha256']==body['decoded_sha256']and typed(body['blob'],blob)and base64.b64decode(body['decoded_bytes_base64'],validate=True)==qb,'Full decoded carrier binds original body')
 need(r.get('historical24_map_sha256')==MAP['sha256']and H(C(hist['items']))==hist['canonical_items_sha256'],'Historical map external and canonical pin')
 rows=[]
 for line in qb.decode('utf-8').splitlines():
  if not re.match(r'^\|\s*\d+\s*\|',line):continue
  cs=[x.strip()for x in line.strip().strip('|').split('|')]
  need(len(cs)>=12,'Complete numeric QUEUE row fields')
  rows.append({'rank':int(cs[0]),'problem_id':cs[1].split(' / ')[0],'problem_alias':cs[1],'problem_title':cs[2],'status':cs[7],'turns':cs[8],'source_line':line})
 need(len(rows)==r['complete_queue_rows']==1951 and len({x['rank']for x in rows})==len(rows),'All 1951 complete ranked rows')
 out=[];given={x['pr']:x for x in r['checks']}
 need(len(given)==len(r['checks'])==len(hist['items'])==24,'Exact 24 receipt/map identities')
 for item in hist['items']:
  candidates=[x for x in rows if x['problem_id']in item['problem_ids']and x['problem_alias']==item['historical_canonical_alias']]
  need(len(candidates)==1,'Unique exact problem ID and full alias')
  row=candidates[0]
  need(typed(row,item['historical_complete_canonical_row']),'Complete fresh row equals historical row')
  need(row['status']and 'claimed_solved'not in row['status']and row['status']in('already_solved','partial'),'Explicit withdrawal persists')
  g=given[item['pr']]
  need(typed(g['fresh_full_row'],row)and g['historical_full_row_unchanged']is True and g['withdrawal_reason']==item['adopted_withdrawal_reason'],'Exact receipt row and withdrawal semantics')
  out.append({'pr':item['pr'],'problem_id':row['problem_id'],'status':row['status'],'full_row_sha256':H(row['source_line'].encode())})
 need(r.get('all24_explicit_current_nonclaimed')is True and r.get('unresolved')==[]and type(r.get('actual_service_effects'))is int and r['actual_service_effects']==0,'No unresolved/effects in dated receipt')
 return {'status':'PASS_DATED_CANONICAL_MAIN_QUEUE_FULL_NATIVE_CHAIN_AND24_WITHDRAWALS','observed_before':chron[0]['before'],'observed_after':chron[-1]['after'],'receipt_at':r['at'],'remote_main':r['remote_main'],'queue_blob':r['queue_blob'],'queue_body_sha256':H(qb),'queue_bytes':len(qb),'complete_ranked_rows':len(rows),'withdrawals':out,'scope':'Dated canonical check only. Final checkpoint parent/main QUEUE identity must still be checked. No final PR/ledger coverage.','final_clearance':False}
def check(pin):
 r=objpin(pin);es=[objpin(p)for p in r['original_native_transports']]
 need(len({p['path']for p in r['original_native_transports']})==6,'Distinct six physical original paths')
 body=objpin(r['queue_body_and_blob_pin']);hist=objpin(MAP)
 out=check_data(r,es,body,hist)
 out['inputs']={'receipt':pin,'original_native_transports':r['original_native_transports'],'full_body':r['queue_body_and_blob_pin'],'historical_map':MAP}
 out['current_gh_binary_sha256']=H(Path(GH).read_bytes())
 out['binary_limitation']='Original transport records bind exact argv and stdout/stderr, but do not themselves contain a contemporaneous binary digest. Current digest is reported separately, not backdated.'
 return out
if __name__=='__main__':
 pin={'path':sys.argv[1],'bytes':Path(sys.argv[1]).stat().st_size,'sha256':sys.argv[2]}
 print(json.dumps(check(pin),ensure_ascii=False,sort_keys=True,indent=2))
