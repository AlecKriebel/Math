"""PR195 qualified-note publication-ready checkpoint. Ref moves occur separately."""
from pathlib import Path
import base64,datetime,hashlib,importlib.util,json,sys
D=Path(__file__).resolve().parent;A=D.parent
PREFIX='draft_pr_publication_program_20260930/';CASE=PREFIX+'audits/pr195_30004601/'
PRIOR=A/'priority_checkpoint_01/priority60_01'
MUTABLE={CASE+x for x in ['CURRENT_CASE_STATUS.json','RESEARCH_LOG.md']}|{PREFIX+x for x in ['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md']}
def read(p):return json.loads(p.read_bytes())
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(j):return (json.dumps(j,indent=2)+'\n').encode()
def save(p,b):
 with p.open('xb') as f:f.write(b)
 p.chmod(0o444)
def load():
 p=A/'priority_checkpoint_01/checkpoint_priority195.py';assert pin(p.read_bytes())=={'bytes':9503,'sha256':'119182ae25b75138c880facf9206f097884c78e3d922c5c10574e56f31713a8b'}
 s=importlib.util.spec_from_file_location('approved195_priority_lowlevel',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
 v,c,h=m.load();h.m.TREE_CACHE_PATH=A/'READY_PRIVATE_TREE_CACHE.json';return v,c,h

def baseline(c):
 r=read(PRIOR/'PREPARATION.json');a=read(PRIOR/'ACCEPTANCE.json')
 assert a['accepted'] is True and a['checkpoint_commit']==r['commit']=='7297de30b67d9bdeb8ad408dc2cc8922c31221cc'
 assert a['every_selected_identity_checked_at_actual_observed_MAIN'] is True
 assert a['selected_files']==len(r['selected_files'])==1370
 assert a['selected_map_sha256']==r['selected_map_sha256']==c.selected_digest(r['selected_files'])=='92e986a79585077902b5fb634fbd244aeb80066b1624166df7d7fb82c635fb03'
 return r

def original(h):
 p=h.api('pulls/195');assert p['head']['sha']=='e776a961293116775fed2cb2a3019d577b84c04a' and p['state']=='open' and p['draft'] is True and p['merged'] is False

def overlay(h,parent,stamp):
 out={}
 def add(rel,expected=None):
  p=A/rel;assert p.is_file() and not p.is_symlink() and p.stat().st_mode&0o777==0o444,rel
  b=p.read_bytes()
  if expected is not None:assert pin(b)==expected,rel
  out[CASE+rel]=b
 gatepath=A/'ROOT_PUBLICATION_GATE_01.json';gate=read(gatepath)
 add('ROOT_PUBLICATION_GATE_01.json',{'bytes':8842,'sha256':'25207e84b05f7f947830208759179ca3eea120ebd94d1dc1869bf683afecd12a'})
 assert gate['publication_ready_gate_accepted'] is True and gate['historical_priority_established'] is False
 for i in [1,2]:
  rel='ROOT_WHOLE_PACKAGE_REVIEW_0'+str(i)+'_ACCEPTANCE.json';add(rel,gate['whole_package_review_events'][i-1]['Root_acceptance']);review=read(A/rel)
  assert review['verdict']=='CLEANPASS' and review['required_repairs']==[]
  for n,p in review['review_safe_files'].items():add('whole_package_adversary_0'+str(i)+'/'+n,p)
 for dirname in ['extra_priority_controls_01','publication_package_v1','publication_package_v2']:
  allow=read(A/dirname/'SAFE_ALLOWLIST.json')['files']
  for n in allow:add(dirname+'/'+n,gate['package_safe_files'][n] if dirname=='publication_package_v2' else None)
 for n in ['PREPARATION.json','ROOT_PRE_MOVE_VERIFICATION.json','ACCEPTANCE.json']:add('priority_checkpoint_01/priority60_01/'+n)
 for n in ['make_native.py','RESEARCH_LOG.md']:add('native_publication_preparation_01/'+n)
 add('publication_checkpoint_01/checkpoint_ready195.py')
 case=json.loads(h.body_at(CASE+'CURRENT_CASE_STATUS.json',parent));assert case['PR']==195 and case['case_percent']==60 and case['original_effort']=='prior unknown; 1 recovered'
 remain='Actual exact-kit Zenodo publication, DOI/tracker readback, originalHEAD-safe MAIN merge, and actual factual completion acceptance. No196 intake yet.'
 status='QUALIFIED_RESEARCH_NOTE_READY_TWO_FRESH_WHOLE_PACKAGE_REVIEWS_CLEAN'
 case.update(UTC=stamp,status=status,case_percent=90,publication_ready=True,publication_ready_gate='ROOT_PUBLICATION_GATE_01.json',whole_package_review_loop_complete=True,whole_publication_package_reviews_complete=True,whole_package_review_events=gate['whole_package_review_events'],package='publication_package_v2',historical_priority_established=False,actual_publication_verified=False,actual_tracker_row_verified=False,actual_merge_accepted=False,remaining_required_steps=remain)
 out[CASE+'CURRENT_CASE_STATUS.json']=enc(case)
 p=json.loads(h.body_at(PREFIX+'CURRENT_PROGRESS.json',parent));assert (p['current_PR'],p['fully_completed_count'],p['published_count'],p['last_completed_PR'],p['current_PR_workflow_percent'])==(195,41,25,193,60)
 p.setdefault('historical_current_case_snapshots',[]).append({'UTC':stamp,'PR':195,'prior_phase':60,'values':{k:v for k,v in p.items() if k.startswith('current_')}})
 p.update(UTC=stamp,updated_UTC=stamp,current_status=status,current_PR_workflow_percent=90,current_workflow_estimate_percent=90,current_publication_ready=True,current_publication_ready_gate='audits/pr195_30004601/ROOT_PUBLICATION_GATE_01.json',current_package='publication_package_v2',current_publication_package='audits/pr195_30004601/publication_package_v2',current_publication_package_reviews_complete=True,current_NEW_whole_publication_package_reviews_completed=2,current_NEW_whole_publication_package_review_active=False,current_whole_package_review_loop_complete=True,current_whole_package_review_events=gate['whole_package_review_events'],current_historical_novelty_or_firstness_established=False,current_actual_publication_verified=False,current_actual_tracker_row_verified=False,current_actual_merge_accepted=False,current_remaining_required_steps=remain,remaining_current_step=remain,next_step=remain,program_snapshot_semantics='PR195 verified seven-plane counterexample and qualified note ready; first fresh whole reviewer clean on v1, terminal new reviewer clean on entire final v2. Historical priority unresolved.41completed/25published,last193,cursor195/advancefalse.',program_snapshot_authority_condition='Ready90 postimage effective only after actual true-parent/fullscope/all-current-identities acceptance. Actual publication/tracker/merge/completion pending.')
 assert p['current_completed'] is False and p['advance_to_next_PR_authorized_now'] is False
 out[PREFIX+'CURRENT_PROGRESS.json']=enc(p)
 note='\n'+stamp+' — PR195 qualified-note90% checkpoint: six-page note compiled and all pages visually inspected; sealed final v2 package exact certificates reproduced. Three mathematical families, bounded36-source/120-query priority audit plus19 exact comparison examples, and two successive NEW whole-package reviewers accepted. First whole review v1; final independent review covers entire v2. Classical construction/tools and Migliore–Nagel J-top family credited; Ilardi2018 full-text gap and unresolved historical priority explicit. All scientific/publication concerns cleared for qualified note. Actual DOI, tracker, originalHEAD-safe merge and factual completion acceptance remain.41completed/25published,last193,cursor195/advancefalse; broader goal active.\n'
 for n in [CASE+'RESEARCH_LOG.md',PREFIX+'CURRENT_PROGRESS.md',PREFIX+'RESEARCH_LOG.md']:out[n]=h.body_at(n,parent)+note.encode()
 return out

def expected(c,base,out):
 assert 'unsolved_math_prioritization/QUEUE.md' not in out
 for n,b in out.items():
  assert n.startswith(CASE) or n in MUTABLE
  if n in base and n not in MUTABLE:assert c.byte_pin(b)==base[n],n
 return {**base,**{n:c.byte_pin(b) for n,b in out.items()}}
def message(d):return 'Record PR195 qualified note ready after two fresh whole-package reviews\n\nPR195 ready selected-map SHA256: '+d

def prepare(v,c,h,gen):
 base=baseline(c);parent=h.api('git/ref/heads/main')['object']['sha'];pt=c.selected_current(h,parent,base['selected_files'],base['tree']);original(h)
 assert h.api('compare/'+base['commit']+'...'+parent)['status'] in ['identical','ahead']
 stamp=datetime.datetime.now(datetime.timezone.utc).isoformat();out=overlay(h,parent,stamp);ex=expected(c,base['selected_files'],out);dest=D/gen;dest.mkdir(exist_ok=False);entries=[]
 for n,b in sorted(out.items()):
  entry={'path':n,'mode':'100644','type':'blob'}
  if n.endswith(('.pdf','.zip')):
   entry['sha']=h.api('git/blobs','POST',{'content':base64.b64encode(b).decode(),'encoding':'base64'})['sha'];assert entry['sha']==c.byte_pin(b)['git_blob']
  else:entry['content']=b.decode('utf-8')
  entries.append(entry)
 tree=h.api('git/trees','POST',{'base_tree':pt,'tree':entries})['sha']
 co=h.api('git/commits','POST',{'tree':tree,'parents':[parent],'message':message(c.selected_digest(ex))})['sha'];h.m.m.h.warm_selected_directories([pt,tree],ex)
 r={'UTC':stamp,'expected_main':parent,'parent_tree':pt,'tree':tree,'commit':co,'selected_files':ex,'selected_map_sha256':c.selected_digest(ex),'overlay_paths':sorted(out),'changed_paths':sorted(n for n,x in ex.items() if h.lookup(pt,n)!=('100644','blob',x['git_blob'])),'MAIN_moved':False}
 save(dest/'PREPARATION.json',enc(r));v.verify_object(c,h,r,ex,message(c.selected_digest(ex)));assert h.api('git/ref/heads/main')['object']['sha']==parent
 print(json.dumps({'expected_main':parent,'commit':co,'tree':tree,'selected':len(ex),'changed':len(r['changed_paths'])}))

def accept(v,c,h,gen):
 base=baseline(c);r=read(D/gen/'PREPARATION.json');out=overlay(h,r['expected_main'],r['UTC']);ex=expected(c,base['selected_files'],out);v.verify_object(c,h,r,ex,message(c.selected_digest(ex)))
 main=h.api('git/ref/heads/main')['object']['sha'];assert h.api('compare/'+r['commit']+'...'+main)['status'] in ['identical','ahead'];tree=c.selected_current(h,main,ex,r['tree'])
 for n,b in out.items():assert h.body_at(n,main)==b,n
 original(h)
 a={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PR':195,'accepted':True,'checkpoint_commit':r['commit'],'sole_parent':r['expected_main'],'main_observed':main,'actual_tree':tree,'selected_files':len(ex),'selected_map_sha256':c.selected_digest(ex),'every_selected_identity_checked_at_actual_observed_MAIN':True,'all_output_bodies_verified':True,'publication_ready_gate_accepted':True,'historical_priority_established':False,'actual_publication_verified':False,'actual_tracker_row_verified':False,'actual_merge_accepted':False,'case_percent':90,'fully_completed_count':41,'published_count':25,'last_completed_PR':193,'QUEUE_native_PR_unchanged':True,'next_numeric_intake_cursor':195,'advance_to_next_PR_authorized_now':False,'goal_complete':False}
 save(D/gen/'ACCEPTANCE.json',enc(a));print(json.dumps(a))
if __name__=='__main__':
 assert sys.dont_write_bytecode
 v,c,h=load();{'prepare':prepare,'accept':accept}[sys.argv[1]](v,c,h,sys.argv[2])
