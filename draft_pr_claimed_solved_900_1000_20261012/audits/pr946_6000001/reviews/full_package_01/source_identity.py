import sys
if not sys.flags.safe_path:raise SystemExit('safe startup')
import pathlib,sqlite3,json,hashlib,subprocess,datetime
R=pathlib.Path('/Users/alec/Documents/Math');A=R/'draft_pr_claimed_solved_900_1000_20261012/audits/pr946_6000001';W=A/'reviews/full_package_01'
db=sqlite3.connect('file:'+str(R/'unsolved_math_prioritization/cache/catalog.sqlite')+'?mode=ro',uri=True)
rows=db.execute('select payload, report from records where key=?',('6000001',)).fetchall();db.close()
if len(rows)!=1:raise ValueError('source')
p,r=map(json.loads,rows[0]);rh=hashlib.sha256(json.dumps([p,r],sort_keys=True).encode()).hexdigest();sh=hashlib.sha256(p['statement'].encode()).hexdigest();record=json.loads((A/'source_record_private.txt').read_text())
if rh!='f8584e1f273da5d42d94704da74c51cf5aa9f0100b44e2bc9b2096c45eabf4fb' or sh!='04707260f4ed2585125f1da57279c9cf1da447cd99a9010d463e5be43dc945cd' or p!=record['problem'] or r!=record['prior_research']:raise ValueError('source hashes')
main=subprocess.check_output(['git','ls-remote','origin','refs/heads/main'],cwd=R,text=True).split()[0]
cat=json.loads(subprocess.check_output(['git','show',main+':unsolved_math_prioritization/catalog.json'],cwd=R));target=[x for x in cat if str(x.get('id'))=='6000001'];groups=json.loads(subprocess.check_output(['git','show',main+':unsolved_math_prioritization/review_v2/related_target_groups.json'],cwd=R))['groups'];membership={str(i):g for i,g in enumerate(groups) if '6000001' in [str(x) for x in g.get('ids',[])]}
if len(target)!=1 or target[0]['holds']!=[] or not target[0]['present'] or target[0]['review_hash']!=rh or target[0]['statement_hash']!=sh or membership!={}:raise ValueError('current gate')
q=subprocess.check_output(['gh','pr','view','946','--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,baseRefName,title,body'],cwd=R,text=True);pr=json.loads(q);f=json.loads((A/'preprint/FREEZE.json').read_text())
if pr['number']!=946 or pr['state']!='OPEN' or pr['isDraft'] is not True or pr['headRefOid']!=f['original_pr_head'] or pr['baseRefName']!='main' or hashlib.sha256(pr['body'].encode()).hexdigest()!=f['pr_description_sha256']:raise ValueError('live metadata')
j={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cached_source_read_only':True,'record_count':1,'review_hash':rh,'statement_hash':sh,'full_record_matches_saved':True,'observed_remote_main':main,'present':True,'holds':[],'related_membership':membership,'live_PR':{k:v for k,v in pr.items() if k!='body'},'live_body_sha256':f['pr_description_sha256'],'original_native_events':'unavailable; declared4/5 not independently certified','audit_proof_turns_added':0,'mutations':0}
(W/'SOURCE_LIVE_IDENTITY.json').write_text(json.dumps(j,indent=2)+'\n');print(json.dumps(j))
