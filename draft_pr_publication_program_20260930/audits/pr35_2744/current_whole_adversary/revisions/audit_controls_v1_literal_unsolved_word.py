"""Complete-current input checks and actual new negative controls; read-only external inputs."""
from pathlib import Path
import argparse,copy,datetime,hashlib,importlib.util,json,os,re,shutil,sqlite3,subprocess
P=argparse.ArgumentParser();P.add_argument('--repo',default='/Users/alec/Documents/Math');P.add_argument('--audit');P.add_argument('--output-dir');args=P.parse_args()
HERE=Path(__file__).resolve().parent;REPO=Path(args.repo).resolve();AUDIT=Path(args.audit).resolve() if args.audit else HERE.parent
OUT=Path(args.output_dir).resolve() if args.output_dir else HERE;OUT.mkdir(parents=True,exist_ok=True);WORK=OUT/'tmp/new_controls';WORK.mkdir(parents=True,exist_ok=True)
C=AUDIT/'reviewed_candidate';Q=REPO/'unsolved_math_prioritization';WANT='65e7ac9d28b8504346d68c771256c2f4642c374d07bbce06bdaecfe85b8f644a'
ENV={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'};checks={};parsed=[];runs=[]
sha=lambda b:hashlib.sha256(b).hexdigest();load=lambda p:json.loads(p.read_bytes())
def ck(k,v):
 assert bool(v),k
 checks[k]='PASS'
def parse(p):
 b=p.read_bytes()
 if p.suffix=='.json':v=json.loads(b);n=1
 elif p.suffix=='.jsonl':v=[json.loads(z) for z in b.splitlines() if z.strip()];n=len(v)
 else:return None
 parsed.append({'path':str(p),'bytes':len(b),'sha256':sha(b),'records':n});return v
def bindings():
 m=load(C/'MANIFEST.json');d=load(C/'CURRENT_PROOF_DEPENDENCIES.json');ck('candidate_manifest',sha((C/'MANIFEST.json').read_bytes())==WANT)
 ck('complete42_and115',len(m['files'])==42 and len(d['files'])==115)
 ck('explicit_anchor',d['base']=='../' and d['dependency_anchor_repository_relative']==str(AUDIT.relative_to(REPO)))
 rows=[]
 for root,entries in [(C,m['files']),(AUDIT,d['files'])]:
  ck('unique_members_'+str(root),len({e['path'] for e in entries})==len(entries))
  for e in entries:
   p=root/e['path'];b=p.read_bytes();ck('binding_'+str(p),len(b)==e['bytes'] and sha(b)==e['sha256']);parse(p)
   rows.append({'path':str(p.relative_to(REPO)),'bytes':len(b),'sha256':sha(b)})
 return rows
names=['Rank','ID / code','Problem','EV','Impact (/10)','Difficulty','Proposed','Status','Turns','Chat','Findings','DOI']
def row(text):
 lines=text.splitlines(keepends=True);h=next(x for x in lines if x.startswith('| Rank |'))
 assert [v.strip() for v in h.split('|')[1:-1]]==names
 selected=[x for x in lines if len(x.split('|'))==14 and x.split('|')[2].strip()=='2744 / KP-1.85'];assert len(selected)==1
 cells=[x.strip() for x in selected[0].split('|')[1:-1]];assert len(cells)==12
 return selected[0],dict(zip(names,cells))
def guarded_patch(text,p):
 before,n=row(text);assert before==p['row_before'] and n['Status']=='queued' and n['Turns']=='0/5' and n['Chat']==n['Findings']==n['DOI']==''
 after,an=row(next(x for x in text.splitlines() if x.startswith('| Rank |'))+'\n'+p['row_prospective'])
 assert all(n[k]==an[k] for k in names if k not in p['allowed_named_changes'])
 assert p['allowed_named_changes']==['Status','Turns','Findings'] and an['Status']=='unsolved' and an['Turns']=='1/5' and an['Chat']==an['DOI']=='' and an['Findings']
 assert text.count(before)==1
 return text.replace(before,after,1)
def run(label,code,expected_exit=0,expected_failure=None):
 r=subprocess.run(['/usr/bin/python3',str(code)],cwd=WORK,capture_output=True,env=ENV,timeout=180)
 (OUT/(label+'.stdout')).write_bytes(r.stdout);(OUT/(label+'.stderr')).write_bytes(r.stderr)
 rec={'name':label,'code_sha256':sha(code.read_bytes()),'exit':r.returncode,'stdout':r.stdout.decode(),'stderr':r.stderr.decode()};runs.append(rec)
 if expected_exit==0:ck(label+'_successful',r.returncode==0 and not r.stderr)
 else:ck(label+'_scientific_rejection',r.returncode!=0 and ('AssertionError: '+expected_failure) in r.stderr.decode())
 return rec
try:
 before=bindings();sm=load(AUDIT/'snapshot_manifest.json');ck('head_and_base',sm['head']=='ecef51f6dd0b60be6e3c37f7d89b69ef89da276d' and sm['base']=='c6975ca76f9f667f1250ba403d0e6da2aafe14d0')
 for z in sm['files']:
  b=(AUDIT/'source_snapshot'/z['path']).read_bytes();git=subprocess.check_output(['git','show',sm['head']+':unsolved_math_prioritization/attempts/2744/'+z['path']],cwd=REPO)
  ck('original15_git_archive_'+z['path'],len(b)==z['size'] and sha(b)==z['sha256'] and b==git==(C/'original_archive'/z['path']).read_bytes())
 ck('sixteen_changed_paths',subprocess.check_output(['git','diff','--name-only',sm['base']+'...'+sm['head']],cwd=REPO).decode().splitlines()==sm['changed_paths'] and len(sm['changed_paths'])==16)
 diff=subprocess.check_output(['git','diff',sm['base']+'...'+sm['head']],cwd=REPO);ck('actual_diff_bytes',len(diff)==sm['diff_bytes'] and sha(diff)==sm['diff_sha256'] and diff==(AUDIT/'pr_input/diff.patch').read_bytes())
 for family,n in [('algebraic_family',27),('cone_family',32),('primary_scope_family',24)]:
  fm=parse(AUDIT/family/'MANIFEST.json');ck('closed_count_'+family,len(fm['files'])==n)
  for e in fm['files']:
   b=(AUDIT/family/e['path']).read_bytes();ck('closed_'+family+'/'+e['path'],len(b)==e['bytes'] and sha(b)==e['sha256'])
 # Complete pinned corpora and actual importer join, not a selected string scrape.
 manifest=parse(Q/'manifest.json');ck('pinned_revision',manifest['revision']=='37e53eabe540fb458758e198be61634bd02ee008')
 for n in ['problems.json','research_results.json']:
  b=(Q/'cache'/n).read_bytes();ck('raw_corpus_'+n,len(b)==manifest['files'][n]['bytes'] and sha(b)==manifest['files'][n]['sha256'])
 ps=parse(Q/'cache/problems.json');rs=parse(Q/'cache/research_results.json');ck('full15458',len(ps)==15458)
 matches=[p for p in ps if p['id']==2744];ck('unique_numeric',len(matches)==1);p=matches[0];r=rs.get(p['problem_number'],{})
 ck('absent_separate_report',p['problem_number']=='KP-1.85' and p['problem_number'] not in rs and r=={})
 ck('unique_code',sum(v['problem_number']=='KP-1.85' for v in ps)==1)
 ck('raw_record_preserved',p==load(C/'source_record.json') and r==load(C/'prior_report.json'))
 ck('embedded_dated_triage', '2026-08-17' in p['background'])
 db=sqlite3.connect('file:'+str(Q/'cache/catalog.sqlite')+'?mode=ro',uri=True);rr=db.execute('select payload,report from records where key=?',('2744',)).fetchone();db.close()
 ck('readonly_sqlite',rr is not None and json.loads(rr[0])==p and json.loads(rr[1])==r)
 rh=sha(json.dumps([p,r],sort_keys=True).encode());sth=sha(p['statement'].encode());ck('hash_roles',rh=='f1e027d879447ba7fe2692009e5e226437de60fbc0234c2d316b7e290ffdc28e' and sth=='1ef73aeb08729350a05e422c05c3f4d5b080490819d2e52a0ce0cc373517158e')
 spec=importlib.util.spec_from_file_location('readonly_score',Q/'queue.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);score=mod.score(p,r,load(Q/'policy.json'));ck('actual_pure_score',score['review_hash']==rh and score['statement_hash']==sth)
 norm=lambda s:re.sub(r'\s+',' ',s).strip();ck('full_exact_duplicate_scan',[z['id'] for z in ps if norm(z['statement'])==norm(p['statement'])]==[2744])
 parse(Q/'review_v2/related_target_groups.json')
 # Read every shared JSON/JSONL byte into a parser. No acceptance transition reconstructed.
 shared={}
 for n in ['state.json','history.jsonl','assessment_history.jsonl','update_history.jsonl']:
  v=parse(Q/n);shared[n]={'sha256':sha((Q/n).read_bytes()),'records':len(v)}
 ck('no_selected_acceptance_state','2744' not in load(Q/'state.json'))
 turns=load(C/'turns.json');ready=load(C/'readiness.json');pro=load(C/'provenance.json');status=load(C/'current_status.json')
 ck('historical_turns',turns['substantive_turns_used']==1 and turns['turn_limit']==5 and turns['outcome']=='unsolved' and len(turns['responses'])==1 and (C/'turns.json').read_bytes()==(AUDIT/'source_snapshot/turns.json').read_bytes())
 ck('current_status',status['queue_status_proposed']=='unsolved' and status['cumulative_attempts']=='1/5' and status['new_substantive_attempts']==status['verification_attempts']==0 and status['literal_problem_resolved']==status['paper_or_new_doi_or_tracker']==status['worldwide_open_status_exhaustively_certified']==False)
 ck('ready_exact_budget',ready['budget']['used_substantive_attempts']==ready['budget']['original_substantive_attempts']==1 and ready['budget']['maximum_substantive_attempts']==5 and ready['budget']['new_substantive_attempts']==ready['budget']['verification_attempts']==0 and ready['budget']['time_cap_utc'] is None)
 ck('ready_source_hashes',ready['review_hash']==pro['review_hash']==rh and ready['statement_hash']==pro['statement_hash']==sth and ready['reviewed_artifact_sha256']==pro['original_artifact_sha256']==sha((C/'OBSTRUCTION.md').read_bytes()))
 ck('ready_certificate',ready['supporting_certificate_sha256']==sha((C/ready['supporting_universal_certificate']).read_bytes()) and pro['current_universal_certificate_sha256']==ready['supporting_certificate_sha256'])
 ck('ready_no_novelty',ready['positive_novelty_claim']==ready['paper_or_new_doi_or_tracker']==False and pro['paper_or_new_doi_or_tracker']==False)
 ck('historical_provenance',pro['historical_original_provenance']==load(C/'original_archive/provenance.json') and ready['historical_original_turn_metadata']==turns and ready['original_turns_sha256']==sha((C/'turns.json').read_bytes()))
 ck('body_equal',(C/'pr_body.md').read_bytes()==(C/'PR_DRAFT.md').read_bytes())
 for n in ['README.md','pr_body.md','RESEARCH_LOG.md','CURRENT_AUDIT_SCOPE.md','CURRENT_SOURCE_QUALIFICATION.md']:
  text=(C/n).read_text();ck('scoped_text_'+n,'NEW' in text and ('unsolved' in text or n=='CURRENT_SOURCE_QUALIFICATION.md'))
 patch=load(C/'CURRENT_QUEUE_PATCH.json');qt=(Q/'QUEUE.md').read_text();old,qr=row(qt);ck('live_selected_queued',qr['Status']=='queued' and qr['Turns']=='0/5' and qr['Chat']==qr['Findings']==qr['DOI']=='')
 prospective=guarded_patch(qt,patch);ck('guard_preserves_unrelated',prospective.replace(patch['row_prospective'],patch['row_before'],1)==qt)
 # Dated whole-queue hash is not a guard against a legitimate unrelated accepted row.
 synthetic=qt.replace('| Rank |','Unrelated acceptance remains here\n| Rank |',1);patched=guarded_patch(synthetic,patch);ck('unrelated_snapshot_drift_preserved',patched.replace(patch['row_prospective'],patch['row_before'],1)==synthetic and sha(synthetic.encode())!=patch['whole_queue_preimage_sha256'])
 queue_receipt={'live_sha256':sha(qt.encode()),'dated_preimage_sha256':patch['whole_queue_preimage_sha256'],'whole_snapshot_still_equal':sha(qt.encode())==patch['whole_queue_preimage_sha256'],'live_named_row':qr,'private_prospective_sha256':sha(prospective.encode()),'no_write':True}
 # Validator mutations: corrupted bytes, status/attempt/DOI/provenance and column swaps.
 negatives=[]
 for label,operation in [
  ('alter_artifact_binding',lambda:sha((C/'OBSTRUCTION.md').read_bytes()+b'False full solution')==pro['original_artifact_sha256']),
  ('cross_document_source_hash',lambda:rh==sha((C/'independent_review/REVIEW.md').read_bytes())),
  ('compact_serialization_hash',lambda:rh==sha(json.dumps([p,r],sort_keys=True,separators=(',',':')).encode())),
  ('invent_new_attempt',lambda:status['new_substantive_attempts']==1),('erase_original_attempt',lambda:turns['substantive_turns_used']==0),
  ('claimed_solution',lambda:status['literal_problem_resolved']==True),('invent_paper',lambda:status['paper_or_new_doi_or_tracker']==True),
  ('invent_deadline',lambda:ready['budget']['time_cap_utc']=='2026-10-02T07:00:00Z'),
  ('erase_anchor',lambda:load(C/'CURRENT_PROOF_DEPENDENCIES.json')['base']=='.')]:
  ck('reject_'+label,not operation());negatives.append({'name':label,'rejected':True,'kind':'specific bookkeeping validator mutation, not proof recognizer'})
 forged=copy.deepcopy(patch);cells=forged['row_prospective'].split('|');cells[10],cells[11]=cells[11],cells[10];forged['row_prospective']='|'.join(cells)
 try:guarded_patch(qt,forged);raise RuntimeError('forged columns wrongly accepted')
 except AssertionError:ck('reject_findings_into_chat',True);negatives.append({'name':'findings_into_chat','rejected':True})
 # Actual scientific executable corruptions of independently written diagnostics.
 code=(HERE/'scientific_controls.py').read_text();cp=WORK/'baseline/scientific_controls.py';cp.parent.mkdir(exist_ok=True);cp.write_text(code);run('new_scientific_baseline',cp)
 ck('independent33',load(cp.with_name('SCIENTIFIC_RESULTS.json'))['passed']==33)
 mutant_specs=[('wrong_acnode_sign','a=y*y+x*x*(1+x)','a=y*y-x*x*(1+x)','acnode_strict_bound'),('compact_elliptic_replacement','D=s.diag(2,s.Rational(1,2))','D=s.eye(2)','noncompact_product'),('false_order_two_lift','T=s.diag(s.I,-s.I)','T=s.diag(1,-1)','order_two_projective_element'),('wrong_fold_direction','mu=alpha+z*z','mu=alpha-z*z','imaginary_fold_decreases_angle'),('wrong_flat_homology','[[0,4,0],[4,0,0],[1,1,1]]','[[0,3,0],[3,0,0],[1,1,1]]','flat_finite_homology'),('collapsed_projective_coordinate','s.diff(s.trace(U)**2,t)','s.diff(s.Integer(4),t)','projective_character_variation')]
 mutations=[]
 for label,old,new,failure in mutant_specs:
  ck('mutation_present_'+label,old in code);mp=WORK/label/'scientific_controls.py';mp.parent.mkdir(exist_ok=True);mp.write_text(code.replace(old,new));rec=run(label,mp,1,failure);mutations.append({**rec,'exact_old':old,'exact_new':new,'expected_failed_check':failure})
 # False prose is actually executed through both unchanged original implementations.
 blind=[];science=(C/'OBSTRUCTION.md').read_text()
 for label,addition in [('false_universal','\nCLAIM: All hyperbolic S3 knots now have the required arc; the full problem is solved.\n'),('false_component_identity','\nCLAIM: Meridian sign twisting equals complex conjugation and gives a different projective component.\n')]:
  wd=WORK/label;wd.mkdir(exist_ok=True);(wd/'OBSTRUCTION.md').write_text(science+addition)
  for rel in ['check_controls.py','independent_review/independent_checks.py']:
   dest=wd/Path(rel).name;shutil.copyfile(C/rel,dest);rec=run(label+'_'+dest.stem,dest);rec['forged_prose_sha256']=sha((wd/'OBSTRUCTION.md').read_bytes());blind.append(rec)
  ck('false_prose_counts_'+label,load(wd/'check_results.json')['passed']==21 and load(wd/'independent_results.json')['passed']==121)
  ck('false_prose_bound_rejected_'+label,sha((wd/'OBSTRUCTION.md').read_bytes())!=pro['original_artifact_sha256'])
 after=bindings();ck('frozen_binding_before_after',before==after)
 result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','bookkeeping_and_control_checks':len(checks),'checks':checks,'before_bindings':before,'after_bindings':after,'full_json_jsonl_parses':parsed,'raw_prior_report':r,'source_pair_hash':rh,'statement_hash':sth,'shared_read_only_snapshots':shared,'queue_guard':queue_receipt,'validator_mutations':negatives,'new_scientific_diagnostics':33,'actual_new_scientific_mutants':mutations,'actual_false_prose_runs':blind,'runs':runs,'new_substantive_attempts':0,'proof_scope':'UNIVERSAL_PROOF supplies complete retained deductions; counts add no proof of the original universal assertion.'}
 (OUT/'AUDIT_RESULTS.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');print(json.dumps({'status':'PASS','checks':len(checks),'scientific':33,'actual_mutants':6,'false_prose_runs':4,'full_json_jsonl_parses':len(parsed)}))
except Exception as e:
 (OUT/'AUDIT_FAILURE.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'error':repr(e),'checks_completed':checks,'runs':runs,'code_sha256':sha(Path(__file__).read_bytes())},indent=2)+'\n');raise
