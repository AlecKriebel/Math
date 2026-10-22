"""Specific PR195 bounded-priority checkpoint; no ref mutation here."""
from pathlib import Path
import datetime, hashlib, importlib.util, json, sys
D=Path(__file__).resolve().parent; A=D.parent
CASE='draft_pr_publication_program_20260930/audits/pr195_30004601/'
PREFIX='draft_pr_publication_program_20260930/'
PRIOR=A/'science_checkpoint_02/math45_01'
MUTABLE={CASE+x for x in ['CURRENT_CASE_STATUS.json','RESEARCH_LOG.md']}|{PREFIX+x for x in ['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md']}
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def read(p):return json.loads(p.read_bytes())
def enc(j):return (json.dumps(j,indent=2)+'\n').encode()
def save(p,b):
 with p.open('xb') as f:f.write(b)
 p.chmod(0o444)
def load():
 p=A/'science_checkpoint_02/checkpoint_math195.py'
 assert pin(p.read_bytes())=={'bytes':12361,'sha256':'998f72fdaceaa37cd5731d6cb703866bc37abc4531516ebf6b04b0f374dcccb7'}
 s=importlib.util.spec_from_file_location('approved195_science_lowlevel',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
 v,c,h=m.load();h.m.TREE_CACHE_PATH=A/'PRIORITY_PRIVATE_TREE_CACHE.json'
 return v,c,h
def baseline(c,h):
 r=read(PRIOR/'PREPARATION.json');a=read(PRIOR/'ACCEPTANCE.json')
 assert a['accepted'] is True and a['checkpoint_commit']==r['commit']=='39604ae16a4c4375213fe9939f6b10f5ec399f0b'
 assert a['selected_files']==len(r['selected_files'])==1348 and a['every_selected_identity_checked_at_actual_observed_MAIN'] is True
 assert a['selected_map_sha256']==r['selected_map_sha256']==c.selected_digest(r['selected_files'])=='bab774d0319d52ef9bdf25e5118bf24cec29083e73b2d378add0d072e6952ce7'
 return r
def original(h):
 p=h.api('pulls/195');assert p['head']['sha']=='e776a961293116775fed2cb2a3019d577b84c04a' and p['state']=='open' and p['draft'] is True and p['merged'] is False
def overlay(h,parent,stamp):
 gate=(A/'ROOT_PRIORITY_GATE_01.json').read_bytes()
 assert pin(gate)=={'bytes':6208,'sha256':'e26fce014c720e43be77f5387b181be1f1106723211004abe7f050032089fce8'}
 g=json.loads(gate);assert g['qualified_research_note_scope_accepted'] is True and g['historical_novelty_or_firstness_established'] is False
 out={CASE+'ROOT_PRIORITY_GATE_01.json':gate}
 for name,x in g['audit_safe_files'].items():
  p=A/'priority_audit_01'/name;assert p.is_file() and not p.is_symlink() and p.stat().st_mode&0o777==0o444
  b=p.read_bytes();assert pin(b)==x;out[CASE+'priority_audit_01/'+name]=b
 for name in ['PREPARATION.json','ROOT_PRE_MOVE_VERIFICATION.json','ACCEPTANCE.json']:out[CASE+'science_checkpoint_02/math45_01/'+name]=(PRIOR/name).read_bytes()
 out[CASE+'priority_checkpoint_01/checkpoint_priority195.py']=Path(__file__).read_bytes()
 case=json.loads(h.body_at(CASE+'CURRENT_CASE_STATUS.json',parent))
 assert case['PR']==195 and case['original_effort']=='prior unknown; 1 recovered' and case['case_percent']==45
 remain='Complete qualified note and verification package; compile/render/reproduce; successive NEW whole-package adversaries until clean; actual Zenodo/tracker/originalHEAD-safe merge and factual MAIN acceptance.'
 status='BOUNDED_PRIORITY_AUDIT_COMPLETE_QUALIFIED_RESEARCH_NOTE_DRAFTING'
 case.update(UTC=stamp,status=status,case_percent=60,priority_audit_active=False,priority_audit_complete=True,qualified_publication_scope_accepted=True,priority_gate='ROOT_PRIORITY_GATE_01.json',historical_novelty_or_firstness_established=False,remaining_required_steps=remain)
 out[CASE+'CURRENT_CASE_STATUS.json']=enc(case)
 p=json.loads(h.body_at(PREFIX+'CURRENT_PROGRESS.json',parent))
 assert (p['current_PR'],p['fully_completed_count'],p['published_count'],p['last_completed_PR'],p['current_PR_workflow_percent'])==(195,41,25,193,45)
 p.setdefault('historical_current_case_snapshots',[]).append({'UTC':stamp,'PR':195,'prior_phase':45,'values':{k:v for k,v in p.items() if k.startswith('current_')}})
 p.update(UTC=stamp,updated_UTC=stamp,current_status=status,current_PR_workflow_percent=60,current_workflow_estimate_percent=60,current_priority_audit_active=False,current_priority_audit_complete=True,current_priority_clearance=True,current_priority_clearance_semantics='Bounded audit complete and explicitly qualified research-note scope accepted; historical novelty/firstness/independence/current-world-openness NOT established.',current_qualified_publication_scope_accepted=True,current_priority_gate='audits/pr195_30004601/ROOT_PRIORITY_GATE_01.json',current_remaining_required_steps=remain,remaining_current_step=remain,next_step='Complete195 qualified note and fresh whole-package review loop; no196 intake.',program_snapshot_semantics='PR195 mathematics verified; bounded36-source/120-query priority audit complete with17earlier examples excluded. Qualified research-note scope accepted; historical priority unresolved.41completed/25published,last193,cursor195/advancefalse.',program_snapshot_authority_condition='Priority60 postimage effective only after actual true-parent/fullscope/all-current-identities acceptance. No publication-ready,DOI,tracker,merge,completion or next-intake authority.')
 assert p['current_historical_novelty_or_firstness_established'] is False and p['current_completed'] is False and p['advance_to_next_PR_authorized_now'] is False
 out[PREFIX+'CURRENT_PROGRESS.json']=enc(p)
 note='\n'+stamp+' — PR195 qualified-note60% checkpoint: mathematics cleared; bounded priority audit36sources/120queries complete,Root read both verifiers and reproduced17prior-example checks. No complete predecessor identified in checked corpus; historical priority/independence/worldwide openness unestablished. Classical parallel connection, applicable Migliore–Nagel J^top resolution and standard tools credited. Ilardi2018 fulltext and parameter/code-history gaps explicit. Qualified note drafting; publication/package reviews,DOI,tracker,merge and completion remain pending.41completed/25published,last193;cursor195/advancefalse; broader goal active.\n'
 for n in [CASE+'RESEARCH_LOG.md',PREFIX+'CURRENT_PROGRESS.md',PREFIX+'RESEARCH_LOG.md']:out[n]=h.body_at(n,parent)+note.encode()
 return out
def message(d):return 'Record PR195 bounded priority audit and qualified-note60 checkpoint\n\nPR195 selected-map SHA256: '+d
def prepare(v,c,h,gen):
 b=baseline(c,h);parent=h.api('git/ref/heads/main')['object']['sha'];pt=c.selected_current(h,parent,b['selected_files'],b['tree']);original(h)
 assert h.api('compare/'+b['commit']+'...'+parent)['status'] in ['identical','ahead']
 stamp=datetime.datetime.now(datetime.timezone.utc).isoformat();out=overlay(h,parent,stamp)
 assert 'unsolved_math_prioritization/QUEUE.md' not in out
 for n,raw in out.items():
  if n in b['selected_files'] and n not in MUTABLE:assert c.byte_pin(raw)==b['selected_files'][n]
 expected={**b['selected_files'],**{n:c.byte_pin(raw) for n,raw in out.items()}}
 dest=D/gen;dest.mkdir(exist_ok=False)
 tree=h.api('git/trees','POST',{'base_tree':pt,'tree':[{'path':n,'mode':'100644','type':'blob','content':raw.decode()} for n,raw in sorted(out.items())]})['sha']
 commit=h.api('git/commits','POST',{'tree':tree,'parents':[parent],'message':message(c.selected_digest(expected))})['sha']
 h.m.m.h.warm_selected_directories([pt,tree],expected)
 r={'UTC':stamp,'expected_main':parent,'parent_tree':pt,'tree':tree,'commit':commit,'selected_files':expected,'selected_map_sha256':c.selected_digest(expected),'overlay_paths':sorted(out),'changed_paths':sorted(n for n,x in expected.items() if h.lookup(pt,n)!=('100644','blob',x['git_blob'])),'MAIN_moved':False}
 save(dest/'PREPARATION.json',enc(r));v.verify_object(c,h,r,expected,message(c.selected_digest(expected)));assert h.api('git/ref/heads/main')['object']['sha']==parent
 print(json.dumps({'expected_main':parent,'commit':commit,'tree':tree,'selected':len(expected),'changed':len(r['changed_paths'])}))
def accept(v,c,h,gen):
 b=baseline(c,h);r=read(D/gen/'PREPARATION.json');out=overlay(h,r['expected_main'],r['UTC']);expected={**b['selected_files'],**{n:c.byte_pin(raw) for n,raw in out.items()}}
 v.verify_object(c,h,r,expected,message(c.selected_digest(expected)))
 main=h.api('git/ref/heads/main')['object']['sha'];assert h.api('compare/'+r['commit']+'...'+main)['status'] in ['identical','ahead']
 tree=c.selected_current(h,main,expected,r['tree'])
 for n,raw in out.items():assert h.body_at(n,main)==raw
 assert c.byte_pin(h.body_at('unsolved_math_prioritization/QUEUE.md',main))==b['selected_files']['unsolved_math_prioritization/QUEUE.md'];original(h)
 a={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PR':195,'accepted':True,'status':'ACTUAL_PR195_QUALIFIED_PRIORITY60_FULL_SCOPE_CURRENT_IDENTITIES_ACCEPTED','checkpoint_commit':r['commit'],'sole_parent':r['expected_main'],'main_observed':main,'actual_tree':tree,'selected_files':len(expected),'selected_map_sha256':c.selected_digest(expected),'every_selected_identity_checked_at_actual_observed_MAIN':True,'all_output_bodies_verified':True,'bounded_priority_audit_complete':True,'qualified_note_scope_accepted':True,'historical_priority_established':False,'publication_ready':False,'case_percent':60,'fully_completed_count':41,'published_count':25,'last_completed_PR':193,'QUEUE_native_PR_unchanged':True,'next_numeric_intake_cursor':195,'advance_to_next_PR_authorized_now':False,'goal_complete':False}
 save(D/gen/'ACCEPTANCE.json',enc(a));print(json.dumps(a))
if __name__=='__main__':
 assert sys.dont_write_bytecode
 v,c,h=load();{'prepare':prepare,'accept':accept}[sys.argv[1]](v,c,h,sys.argv[2])
