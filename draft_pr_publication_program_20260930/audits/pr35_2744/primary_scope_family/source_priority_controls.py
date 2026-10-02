#!/usr/bin/env python3
"""Read-only original/source audit; all generated replay writes stay in HERE/tmp.
Counts check provenance and finite diagnostics, not the universal knot conjecture.
"""
from pathlib import Path
import argparse, copy, datetime, hashlib, importlib.util, json, re, shutil, sqlite3, subprocess
HERE=Path(__file__).resolve().parent
P=argparse.ArgumentParser();P.add_argument('--repo',default='/Users/alec/Documents/Math');A=P.parse_args();ROOT=Path(A.repo).resolve();AUDIT=HERE.parent;SNAP=AUDIT/'source_snapshot';Q=ROOT/'unsolved_math_prioritization'
checks={}
def ck(k,v):
    if not v: raise AssertionError(k)
    checks[k]='PASS'
def sha(b):return hashlib.sha256(b).hexdigest()
def js(p):return json.loads(p.read_text())
def run(cmd,cwd=ROOT):
    x=subprocess.run(cmd,cwd=cwd,capture_output=True)
    return {'command':list(map(str,cmd)),'returncode':x.returncode,'stdout':x.stdout.decode(),'stderr':x.stderr.decode()}
m=js(AUDIT/'snapshot_manifest.json');ck('exact_head',m['head']=='ecef51f6dd0b60be6e3c37f7d89b69ef89da276d');ck('exact_base',m['base']=='c6975ca76f9f667f1250ba403d0e6da2aafe14d0');ck('fifteen_originals',len(m['files'])==15)
for e in m['files']:
    b=(SNAP/e['path']).read_bytes();ck('snapshot_hash_'+e['path'],sha(b)==e['sha256'] and len(b)==e['size'])
    x=run(['git','show',m['head']+':unsolved_math_prioritization/attempts/2744/'+e['path']]);ck('git_original_'+e['path'],x['returncode']==0 and x['stdout'].encode()==b)
x=run(['git','diff','--name-only',m['base']+'...'+m['head']]);ck('all_sixteen_changed_paths',x['returncode']==0 and x['stdout'].splitlines()==m['changed_paths'])
b=(AUDIT/'pr_input/diff.patch').read_bytes();ck('exact_diff',len(b)==m['diff_bytes'] and sha(b)==m['diff_sha256'])
manifest=js(Q/'manifest.json');ck('pinned_revision',manifest['revision']=='37e53eabe540fb458758e198be61634bd02ee008')
for n in ['problems.json','research_results.json']:
    b=(Q/'cache'/n).read_bytes();ck('full_raw_corpus_'+n,len(b)==manifest['files'][n]['bytes'] and sha(b)==manifest['files'][n]['sha256'])
ps=js(Q/'cache/problems.json');rs=js(Q/'cache/research_results.json');ck('full_corpus_size',len(ps)==15458)
p=next(x for x in ps if x['id']==2744);ck('unique_problem_code',sum(x['problem_number']==p['problem_number'] for x in ps)==1);r=rs.get(p['problem_number'],{});ck('separate_prior_report_absent',r=={} and p['problem_number'] not in rs)
ck('complete_raw_problem_matches_snapshot',p==js(SNAP/'source_record.json'));ck('saved_full_raw_records',p==js(HERE/'raw_problem.json') and r==js(HERE/'raw_prior_report.json'))
c=sqlite3.connect('file:'+str(Q/'cache/catalog.sqlite')+'?mode=ro',uri=True);row=c.execute('SELECT key,payload,report FROM records WHERE key=?',('2744',)).fetchone();ck('readonly_sqlite_complete_payload',row is not None and json.loads(row[1])==p and json.loads(row[2])==r);c.close()
review_hash=sha(json.dumps([p,r],sort_keys=True).encode());statement_hash=sha(p['statement'].encode());ck('source_pair_review_hash',review_hash=='f1e027d879447ba7fe2692009e5e226437de60fbc0234c2d316b7e290ffdc28e');ck('statement_hash',statement_hash=='1ef73aeb08729350a05e422c05c3f4d5b080490819d2e52a0ce0cc373517158e')
spec=importlib.util.spec_from_file_location('pure_queue_score',Q/'queue.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);score=mod.score(p,r,js(Q/'policy.json'));ck('actual_pure_score_hash_roles',score['review_hash']==review_hash and score['statement_hash']==statement_hash)
ver=js(SNAP/'independent_review/verdict.json');pro=js(SNAP/'provenance.json');b=(SNAP/'OBSTRUCTION.md').read_bytes();ck('artifact_binding',sha(b)==ver['artifact_sha256']==pro['artifact_sha256']);ck('historical_document_hash_role',sha((SNAP/'independent_review/REVIEW.md').read_bytes())==ver['review_sha256']==pro['independent_review']['review_sha256']);ck('distinct_hash_roles',ver['review_sha256']!=review_hash)
t=js(SNAP/'turns.json');ck('one_substantive_turn',t['problem_id']==2744 and t['turn_limit']==5 and t['substantive_turns_used']==1 and t['outcome']=='unsolved' and len(t['responses'])==1 and t['responses'][0]['turn']==1)
def named_row(text):
    h=next(x for x in text.splitlines() if x.startswith('| Rank |'))
    v=next(x for x in text.splitlines() if re.search(r'\| 2744 / KP-1.85 \|',x))
    hs=[x.strip() for x in h.strip('|').split('|')];vs=[x.strip() for x in v.strip('|').split('|')]
    if len(hs)!=12 or len(vs)!=12:raise ValueError('twelve logical columns required')
    return dict(zip(hs,vs))
qtext=(Q/'QUEUE.md').read_text();qr=named_row(qtext);ck('live_named_status_turns',qr['Status']=='queued' and qr['Turns']=='0/5');ck('live_chat_findings_doi_blank',qr['Chat']==qr['Findings']==qr['DOI']=='')
prq=run(['git','show',m['head']+':unsolved_math_prioritization/QUEUE.md']);ck('head_queue_read',prq['returncode']==0);prrow=named_row(prq['stdout']);ck('original_named_status_turns',prrow['Status']=='unsolved' and prrow['Turns']=='1/5');ck('original_findings_correct_column',prrow['Chat']==prrow['DOI']=='' and 'Separate review passed' in prrow['Findings'] and 'No full-resolution or novelty claim' in prrow['Findings'])
norm=lambda s:re.sub(r'\s+',' ',s).strip();duplicates=[x['id'] for x in ps if norm(x.get('statement',''))==norm(p['statement'])];ck('exact_statement_duplicate_scan',duplicates==[2744]);groups=js(Q/'review_v2/related_target_groups.json');ck('related_groups_full_parse',isinstance(groups,(dict,list)))
patterns=re.compile(r'canonical.{0,70}component.{0,100}(?:SO.?\(?3|SU.?\(?2)|(?:SO.?\(?3|SU.?\(?2).{0,100}canonical.{0,70}component',re.I|re.S)
semantic=[{'id':x['id'],'problem_number':x['problem_number'],'statement':x['statement']} for x in ps if patterns.search(x.get('statement','')) or x['problem_number']=='KP-1.85']
# Transport-qualified source receipts. Dix was independently read via public PDF
# web parser; local 403 responses do not establish its historical byte hash.
sources=js(HERE/'SOURCE_RETRIEVAL.json');fresh={x['name']:x for x in sources if x['status']=='retrieved'}
for name in ['k3','crs-v3','hp-v2','boyle-v1','long-reid']:
    e=fresh[name];pb=HERE/'tmp/sources'/f'{name}.pdf';tb=pb.with_suffix('.txt');ck('fresh_primary_pdf_'+name,pb.read_bytes().startswith(b'%PDF') and sha(pb.read_bytes())==e['sha256'] and pb.stat().st_size==e['bytes']);ck('primary_extracted_text_'+name,sha(tb.read_bytes())==e['text_sha256'])
for e in js(HERE/'ADDITIONAL_VERSION_RETRIEVAL.json'):
    ck('additional_primary_retrieved_'+e['name'],e['status']=='retrieved')
    pb=HERE/'tmp/sources'/f"{e['name']}.pdf";tb=pb.with_suffix('.txt');ck('additional_primary_byte_'+e['name'],pb.stat().st_size==e['bytes'] and sha(pb.read_bytes())==e['sha256'] and sha(tb.read_bytes())==e['text_sha256'])
for k,n in [('k3','k3'),('crs','crs-v3'),('heusener-porti','hp-v2')]:
    old=next(x for x in pro['source_checks'] if x['name']==k);ck('historical_primary_byte_identity_'+n,old['pdf_sha256']==fresh[n]['sha256'])
# Reproduce unmodified programs in a private copy and compare complete JSON bytes.
private=HERE/'tmp/replays';private.mkdir(parents=True,exist_ok=True);replays=[]
for code,out in [('check_controls.py','check_results.json'),('independent_review/submitted_check_controls.py','independent_review/check_results.json'),('independent_review/independent_checks.py','independent_review/independent_results.json')]:
    dest=private/code;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(SNAP/code,dest);x=run(['/usr/bin/python3',str(dest)]);ck('original_replay_exit_'+code,x['returncode']==0 and not x['stderr']);ob=(private/out).read_bytes();expected=SNAP/('check_results.json' if 'independent_results' not in out else 'independent_review/independent_results.json');ck('original_replay_byte_'+code,ob==expected.read_bytes());replays.append({**x,'code_sha256':sha(dest.read_bytes()),'result_sha256':sha(ob),'byte_identical':True})
# Source/status/component admission checks deliberately bind all assumptions.
# These are bookkeeping gates, not proof recognition from arbitrary prose.
cert={'problem_id':2744,'statement_hash':statement_hash,'review_hash':review_hash,'artifact_sha256':sha(b),'status':'unsolved','turns_used':1,'turn_limit':5,'ambient':'S3 hyperbolic knot','component':'fixed oriented discrete-faithful PSL2 curve','required_locus':'nonconstant SO3 character arc','dix_assumption':'Euclidean cone structure; 0 < alpha <= pi','dix_universal':False,'new_knot_counterexample':False,'novel_result':False,'new_doi':None}
def admissible(v):return v==cert
mutants=[]
changes=[('wrong_numeric_identity',{'problem_id':2745}),('wrong_ambient',{'ambient':'arbitrary one-cusped manifold'}),('wrong_component',{'component':'any SL2 character component'}),('isolated_point_for_arc',{'required_locus':'one real character'}),('erase_cone_hypothesis',{'dix_assumption':'any hyperbolic knot'}),('promote_dix_universal',{'dix_universal':True}),('false_solved_status',{'status':'claimed_solved'}),('reset_turn_budget',{'turns_used':0}),('invent_second_turn',{'turns_used':2}),('paper_from_known_partial',{'novel_result':True,'new_doi':'10.5281/zenodo.fake'}),('cross_hash_roles',{'review_hash':ver['review_sha256']}),('compact_serialization_hash',{'review_hash':sha(json.dumps([p,r],sort_keys=True,separators=(',',':')).encode())})]
for name,change in changes:
    v={**cert,**change};ck('reject_admission_'+name,not admissible(v));mutants.append({'name':name,'changes':change,'rejected':True,'mechanism':'Exact source/scope certificate comparison, not arbitrary prose proof recognition.'})
# The original executable diagnostics are intentionally blind to prose claims.
# Execute four forged scopes and show PASS counts do not certify those claims.
blind=[];text=b.decode();forgeries=[('false_universal_resolution','**Disposition: unresolved. No full proof or counterexample was obtained.**','**Disposition: fully solved. Every hyperbolic knot satisfies the conjecture.**'),('wrong_SL_component','chosen projective curve','arbitrary SL component'),('angle_hypothesis_erased','cone angle at most $\\pi$','any cone angle'),('general_manifold_as_knot','Examples for other one-cusped manifolds are not enough.','Every one-cusped manifold is an S3 knot complement.')]
for name,old,new in forgeries:
    ck('mutation_actually_changes_'+name,old in text);d=private/'prose_mutants'/name;d.mkdir(parents=True,exist_ok=True);(d/'OBSTRUCTION.md').write_text(text.replace(old,new));shutil.copy2(SNAP/'check_controls.py',d/'check_controls.py');shutil.copy2(SNAP/'independent_review/independent_checks.py',d/'independent_checks.py');runs=[run(['/usr/bin/python3',str(d/n)]) for n in ['check_controls.py','independent_checks.py']];ck('diagnostic_blindness_'+name,all(x['returncode']==0 for x in runs) and js(d/'check_results.json')['passed']==21 and js(d/'independent_results.json')['passed']==121);ck('forged_artifact_hash_rejected_'+name,sha((d/'OBSTRUCTION.md').read_bytes())!=cert['artifact_sha256']);blind.append({'name':name,'forged_artifact_sha256':sha((d/'OBSTRUCTION.md').read_bytes()),'runs':runs,'diagnostics_still_pass':True,'bound_artifact_rejected':True})
# Actual algebraic mutations must be rejected by the original diagnostic program.
code=(SNAP/'check_controls.py').read_text();badcodes=[('wrong_product_trace','s.trace(A*B)==-s.Rational(17,4)','s.trace(A*B)==-s.Rational(15,4)'),('nonunit_quaternion','qs=[(1,0,0,0)','qs=[(2,0,0,0)'),('false_adjoint_sign','(U*A*U.inv()-(-U)*A*(-U).inv())','(U*A*U.inv()+(-U)*A*(-U).inv())')];bad_runs=[]
for name,old,new in badcodes:
    ck('code_mutation_changes_'+name,old in code);d=private/'code_mutants'/name;d.mkdir(parents=True,exist_ok=True);cp=d/'check_controls.py';cp.write_text(code.replace(old,new));x=run(['/usr/bin/python3',str(cp)]);ck('algebraic_mutation_rejected_'+name,x['returncode']!=0 and 'AssertionError' in x['stderr']);bad_runs.append({'name':name,**x})
result={'passed':len(checks),'failed':0,'checks':checks,'review_hash':review_hash,'statement_hash':statement_hash,'separate_prior_report':r,'complete_original_files':15,'changed_paths':16,'exact_statement_duplicates':duplicates,'semantic_scan_candidates':semantic,'live_named_queue':qr,'original_pr_named_queue':prrow,'original_turns':t,'admission_certificate':cert,'admission_mutants':mutants,'original_replays':replays,'false_prose_actual_replays':blind,'actual_algebraic_mutations':bad_runs,'scope':'Original fixed-head source/provenance and finite algebraic diagnostics only; universal arc claim unresolved. Dix actual independent web PDF reading is in source ledger; no fresh local Dix byte identity claimed. No shared writes, no legacy queue generator.'}
(HERE/'RESULTS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'passed':len(checks),'failed':0,'original_replays':len(replays),'admission_mutants':len(mutants),'false_prose_actual_replays':len(blind)*2,'algebraic_mutations':len(bad_runs)}))
