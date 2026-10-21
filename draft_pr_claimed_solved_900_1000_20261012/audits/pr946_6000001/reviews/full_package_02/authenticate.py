from pathlib import Path,PurePosixPath
import datetime,hashlib,json,os,re,sqlite3,stat,subprocess,sys,zipfile
R=Path('/Users/alec/Documents/Math'); A=R/'draft_pr_claimed_solved_900_1000_20261012/audits/pr946_6000001'; D=A/'preprint'; O=A/'reviews/full_package_02'
HEAD='7d3adb0e500b0414a49a449e7981d34ade329427'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def h(b):return hashlib.sha256(b).hexdigest()
def check(t,m):
 if not t:raise RuntimeError(m)
def fp(p):
 s=p.lstat();check(stat.S_ISREG(s.st_mode) and not p.is_symlink(),'not regular '+str(p));b=p.read_bytes();return {'bytes':len(b),'sha256':h(b)}
def cmd(a):return subprocess.check_output(a,cwd=R)
startfile=O/'START.json'
if not startfile.exists():startfile.write_text(json.dumps({'started_utc':now(),'reviewer_agent_id':'/root/pr946_full_package_02','prior_completed_utc':'2026-10-15T13:19:04.506804+00:00'},indent=2)+'\n')
check(json.loads(startfile.read_text())['started_utc']>'2026-10-15T13:19:04.506804+00:00','chronology')
pins={'FREEZE.json':'bdd016d29f8647c92081990d8fe271e577bd01abe5f132790fdec00600d3bf67','package/PACKAGE_MANIFEST.json':'52165ba2410fa32238244feef20820e5bca9971f60c90542a2360f4d44e6c4ec','package/verify_package.py':'1896614c7b163e8fd69fa15c82c4d2a77e1ca46f4e4ada407d9ea5b52c2a2d2d','research_note.pdf':'a3a1059bf762171d37dde836efb7ae0422477015d181102d0f323c369760ce90','global_hessian_verification.zip':'0b6883acc22bc986ab7250157568041a3fe90770372b30d95e369d84952497d0','ARCHIVE_MANIFEST.json':'2790863687ae7bf92c62f03d13c8102b7341d687709df8d1c74b41326126b986'}
for n,s in pins.items():check(fp(D/n)['sha256']==s,'external pin '+n)
check(fp(A/'OPERATIONS_INVENTORY.json')['sha256']=='dd4e67e75a6271f9fa115095765373acc2e8953884b975a2bc710990826df0c4','operations pin')
f=json.loads((D/'FREEZE.json').read_bytes()); check(f['revision_candidate']==2 and f['original_pr_head']==HEAD,'freeze identity')
for n,m in f['files'].items():check(fp(D/n)=={k:m[k] for k in ['bytes','sha256']},'freeze '+n)
for n,m in f['evidence_files'].items():check(fp(R/n)=={k:m[k] for k in ['bytes','sha256']},'evidence '+n)
ops=json.loads((A/'OPERATIONS_INVENTORY.json').read_bytes());
for n,m in ops['files'].items():check(fp(R/n)==m,'operational '+n)
check(len(f['future_helpers'])==6,'six helpers')
for n,m in f['future_helpers'].items():check(fp(A.parent.parent/n)==m,'future helper '+n)
live=json.loads(cmd(['gh','pr','view','946','--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,baseRefName,url,updatedAt']))
check(live['number']==946 and live['state']=='OPEN' and live['isDraft'] is True and live['baseRefName']=='main' and live['headRefOid']==HEAD,'live gate')
q=cmd(['git','show',HEAD+':unsolved_math_prioritization/QUEUE.md']).decode();rows=[x for x in q.splitlines() if re.search(r'\|\s*6000001\s*/',x)];check(len(rows)==1,'unique original row');row=rows[0];cols=[x.strip() for x in row.split('|')];check(cols[8]=='claimed_solved' and cols[9]=='4/5','exact claimed solved original4/5')
remote=cmd(['git','ls-remote','origin','refs/heads/main']).decode().split()[0]
if subprocess.run(['git','cat-file','-e',remote+'^{commit}'],cwd=R,stderr=subprocess.DEVNULL).returncode:
 cmd(['git','-c','gc.auto=0','fetch','--no-write-fetch-head','origin',remote])
cat=json.loads(cmd(['git','show',remote+':unsolved_math_prioritization/catalog.json']));t=[x for x in cat if x['id']=='6000001'];check(len(t)==1,'main source');t=t[0]
check(t['statement_hash']=='04707260f4ed2585125f1da57279c9cf1da447cd99a9010d463e5be43dc945cd' and t['review_hash']=='f8584e1f273da5d42d94704da74c51cf5aa9f0100b44e2bc9b2096c45eabf4fb' and t['holds']==[] and t['present'] is True,'current main hashes/holds')
c=sqlite3.connect('file:'+str(R/'unsolved_math_prioritization/cache/catalog.sqlite')+'?mode=ro',uri=True);p,r=c.execute('select payload,report from records where key=?',('6000001',)).fetchone();p=json.loads(p);r=json.loads(r);c.close()
check(h(p['statement'].encode())==t['statement_hash'] and h(json.dumps([p,r],sort_keys=True).encode())==t['review_hash'],'raw source identity')
groups=json.loads(cmd(['git','show',remote+':unsolved_math_prioritization/review_v2/related_target_groups.json']));related=[g for g in groups['groups'] if '6000001' in g.get('ids',[])];check(related==[],'related target membership changed')
snap=json.loads((A/'ORIGINAL_SNAPSHOT.json').read_bytes());check(snap['head']==HEAD and len(snap['files'])==33,'original inventory')
orig={};z=zipfile.ZipFile(D/'global_hessian_verification.zip');names=z.namelist();check(len(names)==len(set(names))==220,'archive exact unique220');am=json.loads((D/'ARCHIVE_MANIFEST.json').read_bytes());check(set(names)==set(am['files'])|{'ARCHIVE_MANIFEST.json'} and len(am['files'])==219,'archive exact219')
for n in names:
 i=z.getinfo(n);pp=PurePosixPath(n);check(not pp.is_absolute() and '..' not in pp.parts and stat.S_ISREG(i.external_attr>>16),'archive regular safe '+n)
 if n in am['files']:check({'bytes':len(z.read(n)),'sha256':h(z.read(n))}==am['files'][n],'archive pin '+n)
for n,s in snap['files'].items():
 entry=cmd(['git','ls-tree',HEAD,'--',n]).decode().strip().split();check(len(entry)>=3 and entry[0]=='100644' and entry[1]=='blob','original git mode '+n);oid=entry[2];b=cmd(['git','cat-file','blob',oid]);check(h(b)==s,'git original pin '+n)
 dp=A/'original'/n;db=dp.read_bytes();ds=dp.lstat();an='package/original/'+n;ai=z.getinfo(an);ab=z.read(an)
 check(b==db==ab and stat.S_IMODE(ds.st_mode)==0o644 and stat.S_ISREG(ds.st_mode) and (ai.external_attr>>16)==0o100644,'original disk/archive '+n)
 orig[n]={'bytes':len(b),'sha256':s,'git_blob':oid,'git_mode':'100644','disk_mode':'0644','archive_mode':'100644','disk_and_archive_match':True}
result={'status':'PASS','utc':now(),'original_pr_head':HEAD,'freeze_sha256':pins['FREEZE.json'],'package_manifest_sha256':pins['package/PACKAGE_MANIFEST.json'],'verifier_sha256':pins['package/verify_package.py'],'candidate_revision':2,'future_helpers':f['future_helpers'],'candidate_files':f['files'],'evidence_files':f['evidence_files'],'payloads':219,'archive_members':220,'originals':orig,'original_files':33,'live_pr':live,'remote_main':remote,'current_source':{k:t[k] for k in ['id','statement_hash','review_hash','holds','present','turn_limit']},'related_target_membership':related,'original_queue_row':row,'original_declared_turns':'4/5','certified_historical_native_events':False,'proof_search_turns_added':0,'scope_gate_completed_before_math_reads':True}
out=O/('AUTHENTICATION_END.json' if '--end' in sys.argv else 'AUTHENTICATION_START.json');out.write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps({'status':'PASS','utc':result['utc'],'file':str(out),'files':len(f['files']),'evidence':len(f['evidence_files']),'originals':len(orig),'live':live,'remote_main':remote}))
