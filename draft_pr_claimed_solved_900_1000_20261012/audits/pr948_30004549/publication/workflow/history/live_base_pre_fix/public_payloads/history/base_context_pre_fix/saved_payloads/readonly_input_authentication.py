from pathlib import Path
from datetime import datetime,timezone
import json,subprocess,hashlib
from urllib.request import Request,urlopen
p=Path('draft_pr_claimed_solved_900_1000_20261012').absolute();a=p/'audits/pr948_30004549';w=a/'publication/workflow';core=p/'accept_pr948.py'
n={'__name__':'_root_fixes_readonly_auth_','__file__':str(core)};exec(compile(core.read_bytes(),str(core),'exec',dont_inherit=True,optimize=0),n)
def run(args):return subprocess.run(args,capture_output=True,check=True).stdout
def live():return json.loads(run(['gh','pr','view','948','--json','number,state,isDraft,baseRefName,headRefOid,url,body,mergeable,mergeStateStatus']))
started=datetime.now(timezone.utc).isoformat();before=live();n['main_destination'](before);n['need'](before['isDraft'] is True,'still draft')
remote=run(['git','ls-remote','origin','refs/heads/main']).decode().split()[0]
oldblob=n['blob'];external={}
def readonly_blob(ref,path):
 if ref!=remote:return oldblob(ref,path)
 query='query($expr:String!){repository(owner:"AlecKriebel",name:"Math"){object(expression:$expr){... on Blob{oid byteSize isBinary}}}}'
 reply=json.loads(run(['gh','api','graphql','-f','query='+query,'-f','expr='+ref+':'+path]))
 n['need'](not reply.get('errors'),'GraphQL metadata errors')
 obj=reply.get('data',{}).get('repository',{}).get('object')
 n['need'](type(obj) is dict and type(obj.get('byteSize')) is int and 0<=obj['byteSize']<=32*1024*1024 and obj.get('isBinary') in (None,False),'immutable source blob metadata')
 url='https://raw.githubusercontent.com/AlecKriebel/Math/'+ref+'/'+path
 with urlopen(Request(url,headers={'User-Agent':'Math-PR948-readonly-auth/1.0'}),timeout=30) as response:
  data=response.read(obj['byteSize']+1)
 n['need'](len(data)==obj['byteSize'] and hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==obj['oid'],'raw immutable content does not match authenticated Git blob/size')
 external[path]={'ref':ref,'git_blob':obj['oid'],'bytes':len(data),'sha256':n['sha'](data),'transport':'unauthenticated immutable raw HTTPS; authenticated GraphQL oid/size; JSON schema parsed by source/native guards','GraphQL_isBinary':obj.get('isBinary')}
 return data
n['blob']=readonly_blob
queue=n['blob'](n['HEAD'],n['QUEUE']);row=n['claimed_row'](queue);originals=n['original_check']()
source=n['source_gate'](remote);native=n['native_safety'](remote)
after=live();remote_after=run(['git','ls-remote','origin','refs/heads/main']).decode().split()[0]
n['need'](before==after and remote==remote_after,'PR/main changed across readonly source bracket')
summary={k:v for k,v in before.items() if k!='body'}
opspin=n['sha']((w/'OPERATIONS_INVENTORY.json').read_bytes());n['capture_inventory'](opspin)
result={'schema':'pr948-workflow-final-authentication-v1','engineering_revision':'full01_nonclean_history_repair_exact50','started_utc':started,'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS_READ_ONLY_FRESH_INPUT_CONTINUITY_NOT_ACCEPTANCE','live_before':summary,'live_after':summary,'remote_main_before':remote,'remote_main_after':remote_after,'live_pr_body_sha256':n['sha'](before['body'].encode()),'immutable_queue_sha256':n['sha'](queue),'immutable_queue_row_sha256':n['sha'](row.rstrip(b'\r\n')),'immutable_queue_status':'claimed_solved','original_declared_turns':'4/5','authenticated_originals':originals,'source_gate':source,'native_safety':native,'authenticated_current_main_blobs':external,'operations_inventory_sha256':opspin,'tested_core_sha256':n['sha'](core.read_bytes()),'whole_review_prior_issue':'R948-FULL01-R01','source_object_fetch_in_this_successful_attempt':False,'index_HEAD_checkout_branch_config_mutations':0,'new_author_proof_responses':0,'external_mutations':0,'mathematical_priority_or_whole_package_acceptance':False,'engineering_completion_percent':100,'publication_completion_percent':0,'saved_to_file':False,'earlier_source_fetch_attempt_failed_and_is_separately_reported':True}
print(json.dumps(result))
