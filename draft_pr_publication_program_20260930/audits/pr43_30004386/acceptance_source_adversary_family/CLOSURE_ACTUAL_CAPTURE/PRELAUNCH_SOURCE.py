"""Verify complete own actual review evidence; parent closes only after child exit."""
from pathlib import Path, PurePosixPath
import datetime as dt
import hashlib
import json
import os
H=Path(__file__).resolve().parent;A=H.parent;R=A.parents[2]
sha=lambda b:hashlib.sha256(b).hexdigest()
now=lambda:dt.datetime.now(dt.timezone.utc).isoformat()
started=now();checks=0
def demand(v,msg):
    global checks
    checks+=1
    if not v:raise AssertionError(msg)
reading=json.loads((H/'FULL_INPUT_READING.json').read_bytes());controls=json.loads((H/'INDEPENDENT_CONTROL_RESULTS.json').read_bytes());verdict=json.loads((H/'VERDICT.json').read_bytes())
demand(reading['full_read_count']==1588 and reading['whole_read_bytes']==376265941,'complete actual own reading')
demand(controls['predicate_count']==4724 and len(controls['negative_controls'])==40,'complete own controls')
demand(len(verdict['mandatory_defects'])==2 and verdict['verdict']=='FAIL_REQUIRES_TWO_NARROW_SOURCE_REPAIRS','actual source disposition, no future PASS')
demand(sha((A/'acceptance_preparation_family/PREPARATION_MANIFEST.json').read_bytes())=='4161032794d175f8e0cfc3b62b3d1567f172ca93abe590f43ef81576d6cd20f9','original closed preparation unchanged')
captures=[]
for name,expected in [('INPUT_READING_ACTUAL_CAPTURE',1),('AUTHOR_READER_V2_ACTUAL_CAPTURE',0),('INPUT_READING_V2_ACTUAL_CAPTURE',0),('INDEPENDENT_CONTROLS_ACTUAL_CAPTURE',1),('AUTHOR_CONTROLS_V2_ACTUAL_CAPTURE',0),('INDEPENDENT_CONTROLS_V2_ACTUAL_CAPTURE',0)]:
    d=H/name;c=json.loads((d/'CAPTURE.json').read_bytes())
    demand(c['actual_execution']is True and c['completed']is True and type(c['pid'])is int and c['pid']>0 and c['exit_code']==expected,'actual own PID/exit')
    demand(sha((d/'PRELAUNCH_SOURCE.py').read_bytes())==c['prelaunch_source_sha256']and c['source_unchanged']is True,'genuine prelaunch own source')
    clocks=[dt.datetime.fromisoformat(c[k])for k in ['started_utc','finished_utc']];demand(all(x.utcoffset()==dt.timedelta(0)for x in clocks)and clocks[0]<=clocks[1],'actual aware UTC order')
    demand({p.name for p in d.iterdir()}=={'CAPTURE.json','PRELAUNCH_SOURCE.py','PRELAUNCH_OPERATOR.py','stdout.bin','stderr.bin'},'exact actual5capture')
    for channel in ['stdout','stderr']:
        row=c[channel];raw=(d/row['path']).read_bytes();demand(len(raw)==row['bytes']and sha(raw)==row['sha256'],'whole actual stream')
    captures.append({'path':name+'/CAPTURE.json','pid':c['pid'],'exit_code':expected,'started_utc':c['started_utc'],'finished_utc':c['finished_utc']})
# Remove only the already-recorded private Git-component probe before closure.
private=H/'PRIVATE/resolver_root/.git';demand((private/'hidden').read_bytes()==b'not public','own private probe exact body');(private/'hidden').unlink();private.rmdir()
foreign={}
for z in reading['full_reads']:
    key=(z['path'],z.get('git_head'))
    if key in foreign:demand(foreign[key]['bytes']==z['bytes']and foreign[key]['sha256']==z['sha256'],'consistent duplicate full input')
    else:foreign[key]={'path':z['path'],'bytes':z['bytes'],'sha256':z['sha256'],'role':z['role'],'individual_exclusion':True,**({'historical_git_head':z['git_head'],'present_authority':False}if 'git_head'in z else{})}
external=sorted(foreign.values(),key=lambda x:(x['path'],x.get('historical_git_head','')))
(H/'EXTERNAL_INPUTS_INDIVIDUALLY_EXCLUDED.json').write_text(json.dumps({'schema':'PR43_ACCEPTANCE_SOURCE_ADVERSARY_INDIVIDUAL_FOREIGN_INPUTS_v1','files_count':len(external),'files':external,'full_foreign_bodies_copied':False,'four_historical_native_rows_are_dated_Git_inputs_not_current_authority':True},indent=2)+'\n')
note='\n## '+now()+' — Original source review completed\n\nReview100%; new discovery0%; original0/5,new0,audit0. ExactlyM1/M2 mandatory\nsource defects, independently confirmed. Input32160 and controls35798 are real\ncomplete exit0 captures. Own failed31301/35357 and their separately corrected\nsources/captures remain. No proposed code was executed. Private symlink probes\nwere removed within their own control operation; the private .git-component\nprobe alone is removed now after its exact recorded check. All retained private\nmode observations are historical before the final full0444 own closure.\nNo PASS transfers to any repair family. Future ROOT and PR42 gates remain future.\n'
with(H/'RESEARCH_LOG.md').open('a')as f:f.write(note)
result={'schema':'PR43_ACCEPTANCE_SOURCE_ADVERSARY_OWN_CLOSURE_CONTROL_v1','started_utc':started,'finished_utc':now(),'actual_pid':os.getpid(),'status':'PASS_COMPLETE_REVIEW_EVIDENCE_WITH_TWO_MANDATORY_DEFECTS','predicates':checks,'captures':captures,'individually_excluded_foreign_inputs':len(external),'report_sha256':sha((H/'FINAL_REPORT.md').read_bytes()),'verdict_sha256':sha((H/'VERDICT.json').read_bytes()),'future_execution_approved':False,'review_completion_percent':100,'new_discovery_percent':0}
(H/'CLOSURE_CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
