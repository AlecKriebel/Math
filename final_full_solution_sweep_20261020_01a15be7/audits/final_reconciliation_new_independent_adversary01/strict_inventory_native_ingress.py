"""Strict independent final inventory ingress. Pure read-only; no final authority.
Original full CLI request/stdout are bound to each retained REST page envelope.
"""
from pathlib import Path
import sys,json,hashlib,base64,datetime,re
R=Path('/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7')
W=R/'audits/final_reconciliation_new_independent_adversary01'
PINS={'independent_checks.py':'63f9f0d1cd4d8e8d87b3c087ce8db2535ef526db3f359e2df7f4c13ce550aa8a','check_dated_canonical_queue.py':'03dc2f119a33a34a83ec2c7918f6b2e853677116c3fd3975c407c46066278339'}
ns={}
for name,sha in PINS.items():
 p=W/name;b=p.read_bytes();assert hashlib.sha256(b).hexdigest()==sha
 n={'__file__':str(p),'__name__':'_readonly_inventory_'+name[:-3]}
 exec(compile(b,str(p),'exec'),n);ns[name]=n
s=ns['independent_checks.py'];q=ns['check_dated_canonical_queue.py']
need=s['need'];typed=s['typed'];objpin=s['objpin'];H=s['H'];C=s['C'];utc=q['utc']
API='https://api.github.com/repos/AlecKriebel/Math'
ASC=API+'/pulls?state=all&sort=created&direction=asc&per_page=100&page='
NEW=API+'/pulls?state=all&sort=created&direction=desc&per_page=1'
def native(e,url):
 need(type(e)is dict and e.get('method')=='GET'and e.get('url')==url and type(e.get('status'))is int and e['status']==200,'Exact full original labeled request/status')
 a,z=utc(e.get('at')),utc(e.get('completed_at'))
 need(a<=z<=datetime.datetime.now(datetime.timezone.utc),'Actual original UTC capture interval')
 cli=e.get('original_cli')
 need(type(cli)is dict,'Retained original full CLI request/stdout')
 out=q['http'](cli,url)
 if 'before'in cli or 'after'in cli:
  need('before'in cli and 'after'in cli and a<=utc(cli['before'])<=utc(cli['after'])<=z,'Inner actual native timestamps bound by original envelope')
 raw=base64.b64decode(e['raw_body_base64'],validate=True)
 full=base64.b64decode(cli['stdout_base64'],validate=True)
 need(full.endswith(raw)and len(full)>len(raw),'Full original native stdout binds exact body')
 prefix=full[:-len(raw)]if raw else full
 need(prefix==base64.b64decode(e['raw_headers_base64'],validate=True),'Full original included HTTP headers bind envelope headers')
 hs=[e[k]for k in('raw_sha256','raw_body_sha256')if k in e]
 need(bool(hs)and all(x==H(raw)for x in hs),'Exact original full body SHA256')
 need(typed(out,s['strict'](raw)),'Derived body equals original strict JSON')
 return out,a,z
def node(x):
 need(type(x)is dict,'Full PR object')
 keys={'url','id','node_id','html_url','diff_url','patch_url','issue_url','number','state','locked','title','user','body','created_at','updated_at','closed_at','merged_at','merge_commit_sha','head','base','_links','draft'}
 need(set(x)>=keys,'Full unprojected native PR object fields')
 number=x['number']
 need(type(number)is int and number>0 and type(x['id'])is int and x['id']>0 and type(x['node_id'])is str and x['node_id'],'Typed positive PR identity')
 need(x['url']==API+'/pulls/'+str(number)and x['html_url']=='https://github.com/AlecKriebel/Math/pull/'+str(number)and x['issue_url']==API+'/issues/'+str(number),'Exact PR/repository native identity')
 need(x['state']in('open','closed')and type(x['draft'])is bool and type(x['locked'])is bool and type(x['title'])is str and (x['body']is None or type(x['body'])is str),'Exact PR status/title/body types')
 for k in('head','base'):
  need(type(x[k])is dict and re.fullmatch('[0-9a-f]{40}',x[k].get('sha',''))and type(x[k].get('ref'))is str,'Full branch SHA/ref')
 need(type(x['base'].get('repo'))is dict and x['base']['repo'].get('full_name')=='AlecKriebel/Math','Exact base repository')
 need(type(x['_links'])is dict and x['_links'].get('self')=={'href':x['url']}and x['_links'].get('html')=={'href':x['html_url']},'Complete native links')
 for k in('created_at','updated_at'):
  utc(x[k])
 for k in('closed_at','merged_at'):
  if x[k]is not None:utc(x[k])
 if x['merged_at']is not None:
  need(x['state']=='closed'and type(x['merge_commit_sha'])is str and re.fullmatch('[0-9a-f]{40}',x['merge_commit_sha']),'Merged native commit/status')
 return number
def highest(pin):
 e=objpin(pin);a,start,end=native(e,NEW)
 need(type(a)is list and len(a)==1,'Single newest native PR')
 h=node(a[0])
 return {'status':'PASS_DATED_NEWEST_FULL_NATIVE_REQUEST_BODY_BINDING','highest':h,'head':a[0]['head']['sha'],'before':start.isoformat(),'after':end.isoformat(),'input':pin,'final_clearance':False}
def final(pin):
 o=objpin(pin);need(o.get('schema')=='root-adopted-final-join-overlay-v1','Actual final overlay schema')
 p=o['payload'];ad=objpin(o['root_adoption'])
 need(ad.get('kind')=='ROOT_ADOPTED_FINAL_JOIN_OVERLAY'and ad.get('all_native_receipts_reviewed')is True and ad.get('payload_sha256')==H(C(p)),'Authentic actual final overlay adoption')
 inv=p['final_inventory'];pages=inv['pages']
 need(type(pages)is list and len(pages)>=2,'Full pages plus terminal empty')
 need(len({x['path']for x in pages+[inv['newest']]})==len(pages)+1,'Distinct inventory original paths')
 nodes={};chron=[];prior=None;last_created=None;last_num=0
 for i,pin in enumerate(pages):
  es=objpin(pin);a,before,after=native(es,ASC+str(i+1))
  need(prior is None or before>=prior,'Ordered full inventory native intervals');prior=after
  need(type(a)is list and len(a)<=100,'Original page list bounded by100')
  need((bool(a)if i<len(pages)-1 else a==[]),'Only last terminal empty')
  if i<len(pages)-2:need(len(a)==100,'Every intermediate page is complete100')
  for x in a:
   num=node(x);created=utc(x['created_at'])
   need(num not in nodes and num>last_num and(last_created is None or created>=last_created),'Unique complete ascending creation/number sequence')
   nodes[num]=x;last_num=num;last_created=created
  chron.append({'page':i+1,'count':len(a),'before':before.isoformat(),'after':after.isoformat(),'input':pin})
 e=objpin(inv['newest']);a,before,after=native(e,NEW)
 need(before>=prior and type(a)is list and len(a)==1,'Final newest original after terminal page')
 h=node(a[0])
 need(bool(nodes)and h==max(nodes)and h>=1446,'Actual newest/max without fixed upper bound')
 identity=s['frozen_join']()['identity']
 need(typed(identity(a[0]),identity(nodes[h])),'Newest/full-page complete claim identity consistency')
 observed=utc(inv['observed_at']);need(after<=observed<=datetime.datetime.now(datetime.timezone.utc),'Final inventory observed at after native reads')
 return {'status':'PASS_STRICT_AUTHENTIC_FINAL_INVENTORY_NATIVE_REQUEST_BODY_BINDING','first_original_before':chron[0]['before'],'newest_original_after':after.isoformat(),'observed_at':inv['observed_at'],'highest':h,'native_objects':len(nodes),'numeric_slots_from9':h-8,'gaps_from9':[n for n in range(9,h+1)if n not in nodes],'pages':chron,'newest':inv['newest'],'current_gh_binary_sha256':H(Path(q['GH']).read_bytes()),'binary_limitation':'Current binary digest is not a contemporaneous original digest.','scope':'Ingress only. Every new/changed claim, gap disposition and outcome still requires complete independent mapping reconciliation.','final_clearance':False}
if __name__=='__main__':
 mode=sys.argv[1];path=Path(sys.argv[2]);pin={'path':str(path),'bytes':path.stat().st_size,'sha256':sys.argv[3]}
 print(json.dumps((highest if mode=='dated-highest'else final if mode=='final-overlay'else lambda p:(_ for _ in()).throw(RuntimeError('Unknown mode')))(pin),sort_keys=True,indent=2))
