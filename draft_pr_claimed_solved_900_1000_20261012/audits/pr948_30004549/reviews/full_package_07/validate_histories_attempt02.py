from pathlib import Path
import json,os,datetime
R=Path(__file__).parent;A=R.parents[1];D=A/'preprint';P=A.parents[1]
n={'__name__':'review07_history_inert','__file__':str(P/'accept_pr948.py')};exec(compile((P/'accept_pr948.py').read_bytes(),str(P/'accept_pr948.py'),'exec',dont_inherit=True,optimize=0),n)
context=n['capture_inventory']('500866df6a5c92a38f133dbe7088da956bc52b54ade02b3fa258a07c3af4e002');current=n['freeze_check']((D/'FREEZE.json').read_bytes(),'1bbfc6c554984f8f8a4a6c467c92ff6e5e87f22b2b79d2d9d91766bf0822e68c',context,base=D);original=n['original_check']();rows=[];previous=None;streak=0
for i in range(1,7):
 base=A/f'reviews/full_package_{i:02d}';result=json.loads((base/'RESULT.json').read_bytes());complete=n['result_schema'](result);pins=result['candidate_pins'];candidate=D if i!=1 else D/'reviewed_candidates/candidate01';freeze=current if i!=1 else n['freeze_check']((candidate/'FREEZE.json').read_bytes(),pins['freeze'],context,base=candidate,historical=True)
 start,end=n['utc'](result['started_utc']),n['utc'](result['completed_utc']);assert start<end and (previous is None or previous<start);previous=end
 a,ta=n['review_authentication'](json.loads((base/'AUTHENTICATION_START.json').read_bytes()),pins,freeze,original);b,tb=n['review_authentication'](json.loads((base/'AUTHENTICATION_END.json').read_bytes()),pins,freeze,original);c,tc=n['review_cold'](json.loads((base/'COLD_REPLAY.json').read_bytes()),pins,freeze,candidate);assert start<=ta<=tc<=tb<=end
 clean=bool(complete and a and b and c and result['clean_for_preprint'] and i!=1);streak=streak+1 if clean else 0
 rows.append({'round':i,'candidate':str(candidate),'completed_flags':complete,'authentication_start_pass':a,'authentication_end_pass':b,'cold_pass':c,'clean_current':clean,'nonclean_history':result.get('nonclean_history'),'chronology_pass':True,'clean_streak':streak})
# Independently check root's 44-survivor claim: no lost artifacts are inferred.
b5=A/'reviews/full_package_05';sur=b5/'history/surviving_partial_before_recovery';survival=json.loads((sur/'PRESERVATION.json').read_bytes());assert len(survival['files'])==44;survivors=[sur/n for n in survival['files']];assert len(survivors)==44
for p in survivors: assert n['fingerprint'](p.read_bytes())==survival['files'][p.relative_to(sur).as_posix()]
preserved={str(p.relative_to(sur)):{'bytes':len(p.read_bytes()),'sha256':n['sha'](p.read_bytes()),'identical_current_original':(b5/p.relative_to(sur)).is_file() and (b5/p.relative_to(sur)).read_bytes()==p.read_bytes()} for p in survivors}
# Root intentionally wraps SOME top-level records; those exact originals remain archived, never overwritten in preservation.
report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_ALL_SIX_HISTORICAL_SCHEMAS_AND_CHRONOLOGY','rounds':rows,'latest_clean_streak_through06':streak,'acceptance':False,'surviving05':preserved,'missing_lost_data_certified':False,'review06_scope_assessment':'Exact metadata exposure and initial NONCLEAN interpretation are preserved. Incomplete05 administrative status and empty defect list certify no candidate theorem/priority result. Root clarification did not replace a missing source authentication or proof check. Under the disclosed substantive-independence standard,06 is clean; this is not a blindness certificate or an erasure of the original interpretation.'}
raw=(json.dumps(report,indent=2)+'\n').encode()
with (R/'PRIOR_HISTORY_VALIDATION.json').open('wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
assert (R/'PRIOR_HISTORY_VALIDATION.json').read_bytes()==raw;print(json.dumps({'status':report['status'],'streak':streak,'rounds':[(r['round'],r['clean_current']) for r in rows],'survived05':44}))
