import sys
if not(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):raise RuntimeError('trusted isolation flags required')
import pathlib,hashlib,json,datetime
W=pathlib.Path('/Users/alec/Documents/Math');P=W/'draft_pr_claimed_solved_900_1000_20261012';A=P/'audits/pr967_2616';R=A/'reviews/closure_package_adversary_02'
def sha(b):return hashlib.sha256(b).hexdigest()
cp='4a9a273e37d43b7d987dea29319aaa4ca70f14432e6bafb568ee5f6af9130c88';wp='59f46a1f29140fc2018f9bb10ea3f2989dbaf0313ab33acf32f02ba05b787533';ip='1aec2d70a27a8ef251c8478932d1cd578c0a259e075fec591edc345c19d8745a';dp='1c783ed45d2b15500ec4ebf83f071373ea1e49cd342ec1f8a3cbfbf102c86160'
for path,h in [(P/'close_pr967.py',cp),(P/'finalize_pr967_and_gate_next.py',wp),(A/'CLOSURE_OPERATIONS_INVENTORY.json',ip)]:
 if sha(path.read_bytes())!=h:raise RuntimeError('external complete initial input pin')
raw=(P/'close_pr967.py').read_bytes();n={'__name__':'_own_actual_readonly','__file__':str(P/'close_pr967.py')};exec(compile(raw,str(P/'close_pr967.py'),'exec',dont_inherit=True,optimize=0),n)
originalgit=n['git'];originalapi=n['api'];calls=[]
def git(*a,**kw):
 allowed=(a==('fetch','--no-auto-maintenance','--no-write-fetch-head','--no-tags','--no-recurse-submodules','--no-prune','origin','95931fd570cc2d6c0eb85f6cb9776d08d8a8a603')or a[:2]in [('remote','get-url'),('ls-tree','-r'),('cat-file','blob'),('cat-file','-e'),('symbolic-ref','--short')]or a[0]in ['ls-remote','show'])
 if not allowed:raise RuntimeError('read-only reviewer prohibits Git command '+repr(a))
 calls.append({'kind':'Git','argv':list(a)});return originalgit(*a,**kw)
def api(method,endpoint,payload=None):
 if not(method=='GET' or(method=='POST'and endpoint=='graphql')):raise RuntimeError('reviewer prohibits actual service mutation')
 calls.append({'kind':'API','method':method,'endpoint':endpoint});return originalapi(method,endpoint,payload)
n.update(git=git,api=api);start=datetime.datetime.now(datetime.timezone.utc).isoformat();context=n['inventory'](ip);check,d,body,auth=n['preflight'](dp,context);who,stamp=n['actor']()
if who!=auth['actor']:raise RuntimeError('actual actor differs from authorization')
out={'started_utc':start,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_ACTUAL_CURRENT_PREREQUISITES','current_main':check['gate']['pr']['currentBaseRefOid'],'target_head':check['gate']['pr']['headRefOid'],'target_status':check['gate']['status'],'target_state':check['gate']['pr']['state'],'target_draft':check['gate']['pr']['isDraft'],'changed_paths':check['gate']['changed_paths'],'queue_blob':check['gate']['queue_blob'],'queue_row_sha256':check['gate']['queue_row_sha256'],'source':check['source'],'native':check['native'],'original_files':len(check['originals']),'families':{k:{x:v[x]for x in ['members','bytes','manifest_sha256']}for k,v in check['families'].items()},'actual_actor':who,'actor_server_utc':stamp,'calls':calls,'actual_service_mutations':0,'actual_Git_reference_index_checkout_config_mutations':0,'actual_Git_exact_object_fetches':sum(c.get('kind')=='Git'and c.get('argv',[None])[0]=='fetch'for c in calls),'private_source_body_output':False,'actual_operations_called':False,'operations_inventory_sha256':ip,'decision_sha256':dp}
(R/'ACTUAL_READONLY_GATES02.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k not in ['calls','source','native','families','changed_paths']},indent=2))
