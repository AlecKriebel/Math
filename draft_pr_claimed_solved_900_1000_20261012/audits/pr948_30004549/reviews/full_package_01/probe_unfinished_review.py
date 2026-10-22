import pathlib
R=pathlib.Path("/Users/alec/Documents/Math"); W=R/"draft_pr_claimed_solved_900_1000_20261012/audits/pr948_30004549/publication/workflow"; O=W.parents[1]/"reviews/full_package_01"; s=(W/"test_root_fixes.py").read_text()
insert="""witnesses=[]
with Patch(A=A,D=D,read_regular=virtual_read,frozen_profile=profile,inherited_findings=lambda freeze:original_findings(freeze,D),original_check=lambda:originals):
 witnesses.append({'case':'complete_adverse_plus_two_clean','accepted':len(N['review_check'](specs,freeze,pin,context)[0])==3})
 first=A/'reviews/full_package_01'
 r=json.loads(fs[str(first/'RESULT.json')]);r['full_reproducer_completed']=False;r['entire_package_review']=False;r['clean_for_preprint']=False
 put(first/'RESULT.json',raw(r))
 m=json.loads(fs[str(first/'MANIFEST.json')]);m['files']['RESULT.json']=N['fingerprint'](fs[str(first/'RESULT.json')]);put(first/'MANIFEST.json',raw(m));specs[0]='01:'+N['sha'](raw(m))
 try:N['review_check'](specs,freeze,pin,context)
 except RuntimeError as error:witnesses.append({'case':'honest_unfinished_old_round_plus_two_clean','accepted':False,'error':str(error)})
 else:witnesses.append({'case':'honest_unfinished_old_round_plus_two_clean','accepted':True})
with Patch(A=A,D=D,read_regular=virtual_read,frozen_profile=profile,inherited_findings=lambda freeze:original_findings(freeze,D),original_check=lambda:originals):
 r['full_reproducer_completed']=True;r['entire_package_review']=True;put(first/'RESULT.json',raw(r))
 c=json.loads(fs[str(first/'COLD_REPLAY.json')]);c['status']='FAIL';c['modes'][0]['returncode']=1;put(first/'COLD_REPLAY.json',raw(c))
 m['files']['RESULT.json']=N['fingerprint'](fs[str(first/'RESULT.json')]);m['files']['COLD_REPLAY.json']=N['fingerprint'](fs[str(first/'COLD_REPLAY.json')]);put(first/'MANIFEST.json',raw(m));specs[0]='01:'+N['sha'](raw(m))
 try:N['review_check'](specs,freeze,pin,context)
 except RuntimeError as error:witnesses.append({'case':'failed_old_replay_plus_two_clean','accepted':False,'error':str(error)})
 else:witnesses.append({'case':'failed_old_replay_plus_two_clean','accepted':True})
out={'utc':datetime.now(timezone.utc).isoformat(),'finding_id':'R948-FULL01-R01','candidate_source_sha256':N['sha'](p.read_bytes()),'actual_functions':['result_schema','review_check'],'fixture':'Sealed root-fix tiny in-memory old-candidate adverse plus two-current-clean chain. Only old round completion flags changed to false; RESULT and review manifest pins coherently updated. All other auth/cold data left intact to isolate unconditional completion check.','witnesses':witnesses}
(Path("""+repr(str(O/"UNFINISHED_REVIEW_WITNESS.json"))+""")).write_text(json.dumps(out,indent=2)+'\\n')
print(json.dumps(out))
"""
s=s.replace("receipt={'schema':'pr948-workflow-root-fixes-tests-v1'",insert+"receipt={'schema':'pr948-workflow-root-fixes-tests-v1'"); s=s.replace("(W/'ROOT_FIXES_RESULT.json').write_text", "(Path("+repr(str(O/"ROOT_FIXES_PROBE_REPLAY.json"))+")).write_text")
n={"__name__":"_independent_witness_","__file__":str(W/"test_root_fixes.py")};exec(compile(s,str(O/"inert-witness"),"exec",optimize=0),n)
