"""Repair independently demonstrated lifecycle guard and live-alias defects."""
from pathlib import Path
import ast,datetime,hashlib,json,shutil
A=Path(__file__).resolve().parent
def require(x,msg):
 if not x:raise RuntimeError(msg)
def unique(s,a,b):
 require(s.count(a)==1,'Unique guard adaptation failed '+a[:80]);return s.replace(a,b)
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
require((A/'disposition_script_audit/FINAL_SEAL.json').is_file(),'Independent disposition report not yet sealed')
D=A/'lifecycle_pre_repair_20261015';D.mkdir(exist_ok=False)
names=['prepare_final_scoped_merge.py','prepare_factual_completion.py']
before={n:pin(A/n) for n in names}
for n in names:shutil.copyfile(A/n,D/n);(D/n).chmod(0o444)
s=(A/names[0]).read_text()
anchor="def now():return datetime.datetime.now(datetime.UTC).isoformat()"
extra="""
alias_spec=importlib.util.spec_from_file_location('campaign190',A/'campaign_aliases.py');alias_module=importlib.util.module_from_spec(alias_spec);alias_spec.loader.exec_module(alias_module)
def require_selected_at_main(main,selected,reference_tree=None):
 actual_tree=api('git/commits/'+main)['tree']['sha']
 m.m.h.warm_selected_directories([reference_tree or actual_tree,actual_tree],selected)
 for name,x in selected.items():require(lookup(actual_tree,name)==('100644','blob',x['git_blob']),'Selected current MAIN identity drift '+name)
 return actual_tree
"""
s=unique(s,anchor,anchor+'\n'+extra)
s=unique(s,"save(out/'CURRENT_PROGRESS.json',j)","alias_module.normalize(j,95);save(out/'CURRENT_PROGRESS.json',j)")
anchor="g,_,_=gates()"
s=unique(s,anchor,"require_selected_at_main(actual,r['selected_files'],r['tree'])\n "+anchor)
s=unique(s,"CASE+'TRACKER_ACCEPTANCE.json']:","CASE+'TRACKER_ACCEPTANCE.json',CASE+g['package_name']+'/dodecahedron_endpoint.pdf',CASE+g['package_name']+'/verification-package.zip']:")
s=unique(s,"'actual_native_scientific_and_metadata_bytes_accepted':True,","'actual_native_scientific_and_metadata_bytes_accepted':True,'every_selected_identity_checked_at_actual_observed_MAIN':True,")
ast.parse(s);(A/names[0]).write_text(s)
s=(A/names[1]).read_text()
anchor="e=api('git/ref/heads/main')['object']['sha'];j=json.loads(body_at(m.PREFIX+'CURRENT_PROGRESS.json',e));"
s=unique(s,anchor,"e=api('git/ref/heads/main')['object']['sha'];merged_scope=json.loads((A/'SCOPED_MERGE_PREPARATION.json').read_text());m.require_selected_at_main(e,merged_scope['selected_files'],merged_scope['tree']);j=json.loads(body_at(m.PREFIX+'CURRENT_PROGRESS.json',e));")
s=unique(s,'whole_package_review02_complete=True,publication_ready=True','whole_package_review02_complete=True,whole_package_reviews_complete=True,whole_package_review02_disposition=\'PASS\',publication_ready=True')
s=unique(s,"save(out/'CURRENT_PROGRESS.json',j)","m.alias_module.normalize(j,100);save(out/'CURRENT_PROGRESS.json',j)")
anchor="for n,x in r['selected_files'].items():\n  b=body_at(n,actual);"
s=unique(s,anchor,"merged_scope=json.loads((A/'SCOPED_MERGE_PREPARATION.json').read_text());combined=dict(merged_scope['selected_files']);combined.update(r['selected_files']);m.require_selected_at_main(actual,combined,r['tree'])\n "+anchor)
s=unique(s,"'selected_files':len(r['selected_files']),'fully_completed_count':39","'selected_files':len(r['selected_files']),'combined_expected_current_identities_checked':len(combined),'every_selected_identity_checked_at_actual_observed_MAIN':True,'fully_completed_count':39")
ast.parse(s);(A/names[1]).write_text(s)
out={'UTC':datetime.datetime.now(datetime.UTC).isoformat(),'status':'DISPOSITION_GUARD_AND_LIVE_ALIAS_REPAIR_IMPLEMENTED_TARGETED_INDEPENDENT_RECHECK_PENDING','independent_findings':'disposition_script_audit/FINAL_REPORT.md','before':before,'after':{n:pin(A/n) for n in names},'normalization_helper':pin(A/'campaign_aliases.py'),'controls_required':['Reject unexpected native/PDF/ZIP changes at descendant MAIN','Permit unrelated foreign descendant changes','Require merge identity map before factual preparation','Accept factual selected overrides while rejecting all other selected changes','Normalize95/100 aliases and case complete flag'],'scientific_packet_unchanged':True,'remote_mutations':0}
(A/'ROOT_DISPOSITION_REPAIR_01.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
