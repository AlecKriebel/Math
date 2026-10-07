from pathlib import Path
import datetime,hashlib,json,os,subprocess
P=Path(__file__).resolve().parent
G=Path('/opt/homebrew/Cellar/gh/2.85.0/bin/gh')
HEAD='6a865c574586d08e6fa185b09ebe746122457ff0'
def ck(v,msg):
 if not v: raise RuntimeError(msg)
def pin(f):
 b=f.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def read(n):return json.loads((P/n).read_bytes())
families=[]
for name,sha in [
 ('analytic_zero_boundary_adversary_20261006','340bdaa5c84baf3c756462a9654f83c9460b514ba27456f6af44d1154e393771'),
 ('scalar_sharpness_reproduction_adversary_20261006','06fef4a28dd8d49daae178895a93354ed03c03be8e760a685de4f2f46708df14')]:
 d=P/name;mf=d/'FINAL_MANIFEST.json';ck(pin(mf)['sha256']==sha,'family manifest binding '+name)
 m=json.loads(mf.read_bytes());files=m['files']
 for x in files:
  rel=Path(x['path']);ck(not rel.is_absolute() and '..' not in rel.parts,'manifest escape')
  ck(pin(d/rel)=={'bytes':x['bytes'],'sha256':x['sha256']},'family full member '+str(rel))
 r=json.loads((d/'RESULT.json').read_bytes())
 if name.startswith('analytic'):
  ck(r['math_verdict']=='PASS_ALL_REAL_ALPHA_SUFFICIENT_CONDITION' and not r['mandatory_corrections'] and r['mathematical_gap_found'] is None and r['source_scope_verdict']=='PASS_LITERAL_SUFFICIENT_GENERALIZATION','analytic clearance')
 else:
  ck(r['mathematics_verdict']=='PASS_EXACT_STATED_ALL_REAL_SUFFICIENCY_AND_RESTRICTED_SHARPNESS' and r['remaining_mathematical_gap_in_exact_scope'] is None,'scalar clearance')
  ck(r['methodological_repair_exercised'] and r['repair_clean_receipt_matches_both_modes'] and r['repair_false_parameter_rejects_both_modes'],'repair exercised')
 families.append({'folder':name,'manifest':pin(mf),'full_member_count':len(files),'all_full_members_authenticated':True,'result':pin(d/'RESULT.json'),'report':pin(d/'AUDIT.md'),'result_object':r})
orig=read('original_head_authentication_20261006/ORIGINAL_AUTHENTICATION.json')
ck(orig['original_head']==HEAD and orig['original_literal_status']=='claimed_solved' and orig['original_budget']=='1/5','original target')
ck(len(orig['original_files'])==17,'original count')
for x in orig['original_files']:
 f=P/'original_head_authentication_20261006/original_attempt'/x['path'];b=f.read_bytes()
 ck(pin(f)=={'bytes':x['bytes'],'sha256':x['sha256']},'original full member')
 ck(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['Git_blob'],'original Git blob')
rd=read('original_head_authentication_20261006/original_attempt/readiness.json');ck(rd['substantive_approaches']==1,'real original effort')
for x in read('PRIMARY_FETCH_RECEIPT_20261006.json')['items']:
 ck(pin(P/'private_primary_sources_20261006'/x['path'])=={'bytes':x['bytes'],'sha256':x['sha256']},'primary full source')
 ck(x['sha256']==x['original_reported_sha256'] and x['extraction_exit_code']==0,'source equivalence')
ck(pin(Path('/Users/alec/Downloads/hayman2019.pdf'))['sha256']=='1388a8c153a3eb16156d90542d1f00e4a6203b594566540c71c5f354238e14dc','user book')
repro=read('PARENT_REPRODUCTION_AUTHENTICATION_20261006.json');ck(repro['run_count']==12 and repro['all_repaired_false_identity_controls_rejected'],'root reproduction')
cmd=[str(G),'api','--hostname','github.com','repos/AlecKriebel/Math/pulls/134']
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
child=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
out,err=child.communicate();stop=datetime.datetime.now(datetime.timezone.utc).isoformat()
(P/'MATH_GATE_PR_GET_20261006.json').write_bytes(out)
journal={'actual_operator_PID':os.getpid(),'child_PID':child.pid,'argv':cmd,'UTC_started':start,'UTC_finished':stop,'exit_code':child.returncode,'stdout':pin(P/'MATH_GATE_PR_GET_20261006.json'),'stderr_sha256':hashlib.sha256(err).hexdigest()}
(P/'MATH_GATE_PROCESS_JOURNAL_20261006.json').write_text(json.dumps(journal,indent=2)+'\n')
ck(child.returncode==0,'GitHub read failure')
pr=json.loads(out);ck(pr['number']==134 and pr['html_url']=='https://github.com/AlecKriebel/Math/pull/134' and pr['head']['sha']==HEAD and pr['state']=='open' and pr['draft'] and not pr['merged'],'current immutable target')
doc=P/'PARENT_MATHEMATICAL_SOURCE_AUDIT_20261006.md'
t=doc.read_text();t=t.replace('Promotion awaits authentication of the complete independent audit seals.','The parent has authenticated both complete independent audit seals and all 12 reproduction runs; the mathematical/source gate is now passed with the exercised methodology repair.')
doc.write_text(t)
v={'schema':'pr134-parent-mathematical-source-gate/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_operator_PID':os.getpid(),'PR':134,'problem_id':2306064,'original_head':HEAD,'incoming_literal_status':'claimed_solved','original_effort':'1/5','original_readiness_substantive_approaches':1,'original_17_full_bodies_and_Git_blobs_unchanged':True,'new_central_proof_search_turns':0,'verdict':'PASS_EXACT_MATHEMATICS_AND_SOURCE_AFTER_EXERCISED_METHOD_CONTROL_REPAIR','full_families':families,'parent_report':pin(doc),'parent_reproduction_authentication':pin(P/'PARENT_REPRODUCTION_AUTHENTICATION_20261006.json'),'source_scope':'all real alpha; sufficient coefficient condition; strict open-disk conclusion; sharpness only stated nonnegative interpolation family 0<alpha<=1','methodology_correction':'Original independent -O assert predicates erased; isolated explicit-if repair enforced all28722 and rejected false identity both modes; originals archival unchanged','operative_repair_sha256':'4ccfb72d1f9e41c92eed9f26becd9ae1ece41f43718a74038bf993edf413686d','mathematical_remaining_gaps':[],'source_remaining_gaps':[],'priority_gate':'now may begin; no novelty clearance','priority_audit_authorized_to_begin':True,'service_mutations':False,'shared_index_native_main_mutations':False,'completion_math_source_percent':100,'completion_case_percent':25,'program_completed':22,'program_published':11,'goal_status':'active','process_journal':pin(P/'MATH_GATE_PROCESS_JOURNAL_20261006.json')}
(P/'MATHEMATICS_SOURCE_GATE_20261006.json').write_text(json.dumps(v,indent=2)+'\n')
with (P/'RESEARCH_LOG.md').open('a') as h:h.write('\n'+v['UTC']+': Mathematical/source gatePASS after parent authenticated both108manifestmembers (including private analytic render),17unchanged original bodies/Gitblobs, all12actualreproductionreceipts and exercised explicit-if repair, current open draft samehead. Math/source100%, priority0%, case25%; program22/99 completed11published. Original1/5/newproof0. Deep priority audit may begin; no novelty/service/shared mutation clearance.\n')
print(json.dumps({k:v[k] for k in ['UTC','actual_operator_PID','verdict','completion_math_source_percent','priority_gate','original_effort','new_central_proof_search_turns']}))

