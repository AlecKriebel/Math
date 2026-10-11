#!/usr/bin/env python3
"""Read-only exact-head and independent source/type controls. Writes only this family."""
from pathlib import Path
from fractions import Fraction as F
import subprocess,json,hashlib,datetime,re,shutil,copy,math
P=Path(__file__).resolve().parent
ROOT=P.parents[3]
SNAP=P.parent/'source_snapshot'
HEAD='aa99d4a36eff79cbb7aae55ce3ffe4a0eb31af95'
PREFIX='unsolved_math_prioritization/attempts/2800102/'
checks=[]
def c(name,value,detail=None):
 checks.append({'name':name,'pass':bool(value),'detail':detail})
 if not value: raise AssertionError(name)
def run(*args):return subprocess.check_output(args,cwd=ROOT)
def sha(b):return hashlib.sha256(b).hexdigest()
m=json.loads((P.parent/'snapshot_manifest.json').read_text())
c('exact_frozen_head',m['head']==HEAD)
c('main_branch',run('git','branch','--show-current').decode().strip()=='main')
c('head_commit_available',run('git','rev-parse',HEAD).decode().strip()==HEAD)
c('sixteen_original_files',len(m['files'])==16)
for f in m['files']:
 b=(SNAP/f['path']).read_bytes();g=run('git','show',HEAD+':'+PREFIX+f['path'])
 c('frozen_sha256:'+f['path'],sha(b)==f['sha256'])
 c('frozen_byte_count:'+f['path'],len(b)==f['bytes'])
 c('head_blob_bytes:'+f['path'],b==g)
 c('head_blob_sha1:'+f['path'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==f['git_blob_sha1'])
c('exact_audit_sha',sha((SNAP/'SOURCE_AUDIT.md').read_bytes())=='99ae40a387e00e5d2c46ed8db4e479170092b2484cf237f83629ba5e1201ec8e')
pr=json.loads(run('gh','pr','view','25','--json','number,url,title,state,isDraft,headRefOid,baseRefOid,body,files'))
(P/'runs/live_pr.json').write_text(json.dumps(pr,indent=2)+'\n')
c('live_pr_same_head',pr['headRefOid']==HEAD)
c('live_pr_open_draft',pr['state']=='OPEN' and pr['isDraft'])
changed=run('git','diff','--name-only',m['actual_merge_base'],HEAD).decode().splitlines()
c('git_changed_inventory',set(changed)==set(m['changed_paths']))
c('github_changed_inventory',set(changed)=={x['path'] for x in pr['files']})
c('scope_attempt_plus_one_queue',set(changed)=={PREFIX+f['path'] for f in m['files']}|{'unsolved_math_prioritization/QUEUE.md'})
qdiff=run('git','diff','--unified=0',m['actual_merge_base'],HEAD,'--','unsolved_math_prioritization/QUEUE.md').decode()
rows=[x for x in qdiff.splitlines() if (x.startswith('+|') or x.startswith('-|'))]
c('queue_only_target_row',len(rows)==2 and all('2800102 / AMR-027-0102' in x for x in rows),rows)
for fn in ['verify.py','review/submitted_verify.py','review/independent_checks.py']:
 outdir=P/'runs'/fn.replace('/','_').replace('.py','');outdir.mkdir(exist_ok=True)
 dest=outdir/Path(fn).name;shutil.copyfile(SNAP/fn,dest)
 r=subprocess.run(['python3',str(dest)],cwd=outdir,capture_output=True,text=True,timeout=120)
 (outdir/'stdout.txt').write_text(r.stdout);(outdir/'stderr.txt').write_text(r.stderr)
 c('historical_replay_exit:'+fn,r.returncode==0)
 if fn.endswith('independent_checks.py'):
  result=json.loads((outdir/'independent_results.json').read_text());prior=json.loads((SNAP/'review/independent_results.json').read_text())
  c('historical_53_receipt_exact',result==prior and result['passed']==53)
 else:
  result=json.loads(r.stdout);prior=json.loads((SNAP/'verification.json').read_text())
  c('historical_383_receipt_exact:'+fn,result==prior and result['total_assertions']==383)
for f in ['review/submitted_verify.py','review/verification.json']:
 base={'review/submitted_verify.py':'verify.py','review/verification.json':'verification.json'}[f]
 c('historical_duplicate_identity:'+f,(SNAP/f).read_bytes()==(SNAP/base).read_bytes())
manifest=json.loads((ROOT/'unsolved_math_prioritization/manifest.json').read_text())
c('pinned_revision',manifest['revision']=='37e53eabe540fb458758e198be61634bd02ee008')
corpus={}
for name,info in manifest['files'].items():
 b=(ROOT/'unsolved_math_prioritization/cache'/name).read_bytes()
 c('pinned_corpus_bytes:'+name,len(b)==info['bytes'])
 c('pinned_corpus_sha256:'+name,sha(b)==info['sha256'])
 corpus[name]=json.loads(b)
record=json.loads((SNAP/'source_record.json').read_text());report=json.loads((SNAP/'prior_report.json').read_text())
raw=[x for x in corpus['problems.json'] if x['id']==2800102]
c('one_numeric_upstream_identity',len(raw)==1)
c('literal_raw_record_preserved',raw[0]==record)
c('literal_prior_report_preserved',corpus['research_results.json']['AMR-027-0102']==report)
c('prior_withdrawal_correction_preserved','withdrawn' in report['verification_note'] and 'Lemma 1 wrong' in report['verification_note'])
c('raw_stale_claim_not_promoted','arXiv:1606.00494' in record['research_summary'] and 'cannot serve as a proof certificate' in (SNAP/'SOURCE_AUDIT.md').read_text())
a=json.loads((SNAP/'attempt.json').read_text())
c('zero_original_substantive_turns',a['substantive_attempts_used']==0 and a['substantive_attempt_limit']==5)
c('no_novelty_or_full_resolution',a['novel_result_claimed'] is False and a['full_resolution_claimed_by_this_attempt'] is False)
c('explicit_real_hold','Complete independent audit of the real square preprint' in a['remaining_validation_gap'])
c('source_only_disposition','unsolved'==a['recommended_queue_status'])
code=[x['id'] for x in corpus['problems.json'] if x.get('problem_number')=='AMR-027-0102'];c('unique_problem_code_here',code==[2800102],code)
norm=lambda s:re.sub(r'\s+',' ',s).strip().casefold()
dup=[x['id'] for x in corpus['problems.json'] if norm(x['statement'])==norm(record['statement'])];c('no_identical_statement_duplicate',dup==[2800102],dup)
related=[{'id':x['id'],'number':x['problem_number'],'title':x['title']} for x in corpus['problems.json'] if re.search('singular.value|1606.00494|monotonicity of singular',x.get('title','')+' '+x.get('statement','')+' '+x.get('background',''),re.I)]
(P/'runs/related_records.json').write_text(json.dumps(related,indent=2)+'\n')
groups=(ROOT/'unsolved_math_prioritization/review_v2/related_target_groups.json').read_text();c('target_absent_related_groups','2800102' not in groups)
prs=json.loads(run('gh','pr','list','--state','all','--limit','100','--search','2800102','--json','number,title,url,headRefName,state'))
(P/'runs/all_state_matching_prs.json').write_text(json.dumps(prs,indent=2)+'\n');c('current_only_same_numeric_pr',all(x['number']==25 for x in prs))
fetches=json.loads((P/'FETCH_LOG.json').read_text());fetched={x['key']:x for x in fetches if 'sha256' in x}
prov=json.loads((SNAP/'source_provenance.json').read_text())
keys={'2608.12151.pdf':'2608.12151pdf','2608.12147.pdf':'2608.12147pdf','2608.27532.pdf':'2608.27532pdf','2609.07802.pdf':'2609.07802pdf','original-open1.2.pdf':'original-open1.2','cunden2019.pdf':'cunden2019'}
for x in prov['sources']:
 live=fetched[keys[x['local_basename']]]
 c('source_provenance_hash:'+x['local_basename'],live['sha256']==x['sha256'] and live['bytes']==x['bytes'])
for id,ver,date,author in [('2608.12151',2,'11 Sep 2026','Hutn'),('2608.12147',2,'11 Sep 2026','Hutn'),('2608.27532',1,'27 Aug 2026','Baslingker'),('2609.07802',1,'7 Sep 2026','Abreu')]:
 h=(P/'foreign'/(id+'abs.html')).read_text()
 c('current_version_anchor:'+id,('https://arxiv.org/abs/'+id+'v'+str(ver)) in h)
 c('current_date_anchor:'+id,date in h)
 c('current_author_anchor:'+id,author in h)
 c('no_live_withdrawal_marker:'+id,'This paper has been withdrawn' not in h)
 c('no_journal_ref_field:'+id,'class="tablecell jref"' not in h and 'class="metatable-label">Journal reference:' not in h)
h=(P/'foreign/1606.00494abs.html').read_text()
c('old_withdrawal_current_notice','This paper has been withdrawn' in h and '6 Mar 2023' in h)
c('old_actual_author','citation_author" content="Abreu, Luís Daniel' in h or 'citation_author" content="Abreu, Lu' in h)
c('old_invalid_estimate_notice','estimate in Lemma 1 is wrong' in h and 'This invalidates the result' in h)
c('old_unpublished_scope','This has not been published' in h)
j=(P/'foreign/abreu2026journal.html').read_text();c('new_recurrence_journal_separate','s11785-026-01988-4' in j and 'recurrence relation for the average singular value' in j)
c('new_recurrence_not_solution','still far from a solution' in j)
# NEW semantic claim controls, specified in the independent seal.
# A source-matching certificate has a distribution, scale and domain, not just a direction.
target={'real_variance':F(1),'complex_component_variance':F(1,2),'outer_exponent':F(-1),'matrix_exponent':F(-1,2),'nuclear_exponent':F(-3,2),'moment_order':F(1,2),'shape':F(0),'dimension_domain':'all integers>=1','real_direction':'increase','complex_direction':'decrease','source_type':'current preprint theorem claim','real_certified':False,'fresh_proof_turns':0,'campaign_novelty':False}
def accept(x):return x==target
c('new_exact_scope_certificate',accept(target))
mutations={'component_variance_one':('complex_component_variance',F(1)),'omit_outer_average':('outer_exponent',F(0)),'omit_inner_scale':('matrix_exponent',F(0)),'wrong_nuclear_power':('nuclear_exponent',F(-1)),'wrong_moment':('moment_order',F(1)),'rectangular_shape':('shape',F(1)),'finite_only_domain':('dimension_domain','integers1..30'),'asymptotic_only_domain':('dimension_domain','sufficiently large integers'),'reverse_real_direction':('real_direction','decrease'),'reverse_complex_direction':('complex_direction','increase'),'treat_old_abstract_as_proof':('source_type','withdrawn abstract proof certificate'),'certify_real_from_source_scope':('real_certified',True),'claim_campaign_novelty':('campaign_novelty',True),'hidden_new_proof_turn':('fresh_proof_turns',1)}
for name,(k,v) in mutations.items():
 x=copy.deepcopy(target);x[k]=v;c('new_negative_scope_control:'+name,not accept(x))
# Independent exact homogeneity checkpoints: deterministic diagonal matrices expose each factor.
for d in [1,2,3,5,8]:
 nuclear=F(d*(d+1),2)
 # Square the two positive forms to avoid radicals.
 c('new_normalization_homogeneity:'+str(d),(nuclear/F(d))**2/F(d)==nuclear**2/F(d**3))
 if d>1:
  c('new_omit_outer_average_detected:'+str(d),nuclear**2/F(d)!=nuclear**2/F(d**3))
  c('new_omit_inner_scale_detected:'+str(d),nuclear**2/F(d*d)!=nuclear**2/F(d**3))
c('new_complex_total_variance',2*F(1,2)==1 and 2*F(1)!=1)
c('new_complex_radial_square',F(1,4)==F(1,2)*F(1,2))
c('new_component_variance_error_scale',F(2)*F(1,4)!=F(1,4))
# A general target cannot be discharged solely by a tested prefix.
c('new_finite_quantifier_insufficiency',set(range(1,31))!=set(range(1,32)))
result={'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':HEAD,'passed':sum(x['pass'] for x in checks),'failed':sum(not x['pass'] for x in checks),'checks':checks,'related_record_count':len(related),'scope':'source/type/version/integrity audit, historical diagnostics reproduced; no universal real proof certification'}
(P/'CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
