"""PR196 math45 adapter over frozen scoped checkpoint primitives; ref moves separate."""
from pathlib import Path
import datetime,hashlib,importlib.util,json,sys
D=Path(__file__).resolve().parent;A=D.parent
p=A/'intake_checkpoint_01/checkpoint196.py'
assert hashlib.sha256(p.read_bytes()).hexdigest()=='c7e9ee0e90aad851bf8e5111bd0dd8b42b339e39dfea6ba712ba9c730c5fb9d3'
s=importlib.util.spec_from_file_location('frozen196intakeprimitives',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
m.D=D;m.MUTABLE|={m.CASE+'CURRENT_CASE_STATUS.json',m.CASE+'RESEARCH_LOG.md'}
PRIOR=A/'intake_checkpoint_01/intake15_01'
def baseline(c):
 r=m.read(PRIOR/'PREPARATION.json');a=m.read(PRIOR/'ACCEPTANCE.json');assert a['accepted'] is True and a['every_selected_identity_checked_at_actual_observed_MAIN'] is True
 assert a['checkpoint_commit']==r['commit']=='cd4b939e139480b4436bd6d78a69a7e5f865edcb' and a['selected_files']==len(r['selected_files'])==1517
 assert a['selected_map_sha256']==r['selected_map_sha256']==c.selected_digest(r['selected_files'])=='17f173a13e175f6c9d86d284b02d518180997587b19dee34d1d94902b02a28ca'
 return r
m.baseline=baseline

def overlay(h,parent,stamp):
 gatepath=A/'ROOT_MATHEMATICAL_GATE_01.json';gate=m.read(gatepath);assert m.pin(gatepath.read_bytes())=={'bytes':9283,'sha256':'60bde30c01962338935287aaf3c49001e850b7ae05d5b3e4c370faedc8ebdfff'};assert gate['mathematical_clearance'] is True and gate['source_contract_clearance'] is True and gate['priority_clearance'] is False
 out={m.CASE+'ROOT_MATHEMATICAL_GATE_01.json':gatepath.read_bytes()}
 def add(rel,x=None):
  p=A/rel;assert p.is_file() and not p.is_symlink() and p.stat().st_mode&0o777==0o444,rel;b=p.read_bytes()
  if x is not None:assert m.pin(b)==x,rel
  out[m.CASE+rel]=b
 for dirname,row in gate['three_NEW_independent_audit_families'].items():
  for name,x in row['safe_files'].items():add(dirname+'/'+name,x)
 for name,x in gate['normalization_addendum_safe_files'].items():add('original_source_audit_01/'+name,x)
 add('ROOT_THREE_FAMILY_AUTHENTICATION_01.json',gate['Root_authentication'])
 for name in ['PREPARATION.json','ROOT_PRE_MOVE_VERIFICATION.json','ACCEPTANCE.json']:add('intake_checkpoint_01/intake15_01/'+name)
 add('science_checkpoint_01/checkpoint_math196.py')
 case=json.loads(h.body_at(m.CASE+'CURRENT_CASE_STATUS.json',parent));assert case['PR']==196 and case['case_percent']==15 and case['original_head']==m.HEAD
 status='MATHEMATICS_AND_SOURCE_CONTRACTS_CLEARED_DEEP_PRIORITY_ACTIVE'
 remain='Deep bounded priority audit, especially original2021 announced interior construction,2017 survey and modern regularity results; determine precise credited contribution/disposition before any paper or publication. No197 intake.'
 case.update(UTC=stamp,status=status,case_percent=45,mathematical_clearance=True,mathematical_result_valid=True,source_contract_clearance=True,independent_mathematical_families_active=False,independent_mathematical_families_complete=3,mathematical_gate='ROOT_MATHEMATICAL_GATE_01.json',priority_audit_active=True,priority_audit_complete=False,priority_clearance=False,historical_novelty_or_firstness_established=False,publication_ready=False,source_provenance_correction_required=True,source_provenance_warning='OWR announces/sketches an interior construction with tentative smoothness. The current strict-positive proof is mathematically verified; historical novelty and precise prior contribution remain under priority review.',normalization_convention='dc=i/(4pi)(barpartial-partial); ddc=i/(2pi)partialbarpartial; log-squared unit pole and FSarea1. Printed source inconsistency not an author-confirmed erratum.',remaining_required_steps=remain)
 out[m.CASE+'CURRENT_CASE_STATUS.json']=m.enc(case)
 p=json.loads(h.body_at(m.PREFIX+'CURRENT_PROGRESS.json',parent));assert (p['current_PR'],p['fully_completed_count'],p['published_count'],p['last_completed_PR'],p['current_PR_workflow_percent'])==(196,42,26,195,15)
 p.setdefault('historical_current_case_snapshots',[]).append({'UTC':stamp,'PR':196,'prior_phase':15,'values':{k:v for k,v in p.items() if k.startswith('current_')}})
 p.update(UTC=stamp,updated_UTC=stamp,current_status=status,current_PR_workflow_percent=45,current_workflow_estimate_percent=45,current_mathematical_clearance=True,current_mathematics_cleared=True,current_mathematical_result_valid=True,current_source_contract_clearance=True,current_source_provenance_warning=case['source_provenance_warning'],current_independent_mathematical_audit_active=False,current_independent_mathematical_audit_families_complete=3,current_mathematical_gate='audits/pr196_30004690/ROOT_MATHEMATICAL_GATE_01.json',current_priority_audit_active=True,current_priority_clearance=False,current_priority_audit_complete=False,current_historical_novelty_or_firstness_established=False,current_publication_ready=False,current_remaining_required_steps=remain,remaining_current_step=remain,next_step=remain,program_snapshot_semantics='PR196 mathematics and literal source contracts PASS after3NEW independent families and Root source/proof/exact replay checks. OriginalOWR announces/sketches interior route; provenance correction and coherent unit normalization mandatory. Deep priority audit active,novelty/firstness unresolved;42completed/26published,last195,cursor196/advancefalse.',program_snapshot_authority_condition='Math45 postimage effective only after actual true-parent/fullscope/all-current-selected-identities acceptance. No priority,publication,merge or next-intake authority.')
 assert p['current_completed'] is False and p['advance_to_next_PR_authorized_now'] is False
 out[m.PREFIX+'CURRENT_PROGRESS.json']=m.enc(p)
 note='\n'+stamp+' — PR196 math45%: three NEW independent geometry/potential,Legendre/PDE and literal-source familiesPASS; Root complete reports/derivations/code read, all27safe seals and2normalization-addendum files authenticated, original19unchanged, new scalar and original81/486exact replays match. Positive-length finiteT contact and finiteL<0 prove actual interior second-order Taylor failure with smooth strictlyKahler boundary. Exact PDE/coordinate contracts checked. Required corrections: credit OWR own announced/sketched interior construction; avoid imported world-open claim, and state coherent unit-log-squared/FSarea1 normalization rather than inconsistent printed prefactor. Deep priority audit active; no novelty/publication clearance.42completed/26published,last195;cursor196/advancefalse; broader goal active.\n'
 for path in [m.CASE+'RESEARCH_LOG.md',m.PREFIX+'CURRENT_PROGRESS.md',m.PREFIX+'RESEARCH_LOG.md']:out[path]=h.body_at(path,parent)+note.encode()
 return out
m.overlay=overlay
m.message=lambda d:'Record PR196 mathematical and source-contract45 clearance; deep priority active\n\nCredited finite-time contact-arc interior non-C2 proof verified; source provenance and normalization corrections explicit.42completed/26published,last195.\nPR196 mathematical selected-map SHA256: '+d

def accept(c,h,gen):
 base=baseline(c);r=m.read(D/gen/'PREPARATION.json');out=overlay(h,r['expected_main'],r['UTC']);ex=m.selected(c,base['selected_files'],out);m.verify(c,h,r,ex);main=h.api('git/ref/heads/main')['object']['sha'];assert h.api('compare/'+r['commit']+'...'+main)['status'] in ['identical','ahead'];tree=c.selected_current(h,main,ex,r['tree']);m.original(h)
 for path,b in out.items():assert c.byte_pin(b)==ex[path] and h.lookup(tree,path)==('100644','blob',ex[path]['git_blob'])
 a={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PR':196,'accepted':True,'checkpoint_commit':r['commit'],'sole_parent':r['expected_main'],'main_observed':main,'actual_tree':tree,'selected_files':len(ex),'selected_map_sha256':c.selected_digest(ex),'every_selected_identity_checked_at_actual_observed_MAIN':True,'all_overlay_body_identities_verified':True,'full_foreign_tree_scope_preserved':True,'QUEUE_native_original_PR_unchanged':True,'mathematical_clearance':True,'source_contract_clearance':True,'priority_clearance':False,'priority_audit_active':True,'publication_ready':False,'case_percent':45,'fully_completed_count':42,'published_count':26,'last_completed_PR':195,'next_numeric_intake_cursor':196,'advance_to_next_PR_authorized_now':False,'goal_complete':False};m.save(D/gen/'ACCEPTANCE.json',m.enc(a));print(json.dumps(a))
if __name__=='__main__':
 assert sys.dont_write_bytecode
 c,h=m.load();h.m.TREE_CACHE_PATH=A/'MATH_PRIVATE_TREE_CACHE.json';{'prepare':m.prepare,'accept':accept}[sys.argv[1]](c,h,sys.argv[2])
