"""Bounded independent campaign; only this audit's outputs are written."""
from pathlib import Path
import datetime, json, os, signal, subprocess, sys, time
from independent_semantics import inspect_html, P, STAGE, IDS

O=Path(__file__).resolve().parent
PY=P/'tmp/shared-math-runtime/bin/python'
cases={'pristine':None,'title_to_index':'exact_h1_selflink_destination','Research_to_self':'exact_main_Research_destination','comment_only_priority':'exact_whole_approved_body_text','borrowed_code_licence':'exact_approved_material_note_and_code_license','hidden_article':None}
receipts=[]
for optimize in (False,True):
    for rid in IDS:
        for case,guard in cases.items():
            mode='optimized' if optimize else 'normal';stem=rid+'-'+case+'-'+mode
            cmd=[str(PY),'-B']+(['-O'] if optimize else [])+[str(O/'checker_case.py'),rid,case]
            start=datetime.datetime.now(datetime.timezone.utc).isoformat();before=time.monotonic()
            proc=subprocess.Popen(cmd,cwd=P,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
            timed=False
            try:stdout,stderr=proc.communicate(timeout=30)
            except subprocess.TimeoutExpired:
                timed=True;os.killpg(proc.pid,signal.SIGKILL);stdout,stderr=proc.communicate()
            (O/'cache/checker-cases'/(stem+'.stdout')).write_bytes(stdout);(O/'cache/checker-cases'/(stem+'.stderr')).write_bytes(stderr)
            q=O/'cache/checker-cases'/(stem+'.json');d=json.loads(q.read_text()) if q.exists() else {}
            bad=[k for k,v in d.get('papers',{}).get(rid,{}).get('checks',{}).items() if not v]
            ok=not timed and not stderr and ((proc.returncode==0 and d.get('status')=='PASS') if case in ('pristine','hidden_article') else (proc.returncode==1 and guard in bad))
            receipts.append({'utc':start,'record_id':rid,'case':case,'mode':mode,'command':cmd,'exit_code':proc.returncode,'seconds':round(time.monotonic()-before,3),'timeout':timed,'failed_guards':bad,'intended_guard':guard,'observation_matches_expected':ok,'hidden_article_is_documented_parser_boundary':case=='hidden_article','stderr_bytes':len(stderr)})
            if not ok:raise ValueError('unexpected checker observation:'+str(receipts[-1]))
(O/'CHECKER_CONTROLS.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'execution_count':len(receipts),'cases':receipts,'old67_suite_or_renderer_harness_replayed':False},indent=2)+'\n')
print(json.dumps({'executions':len(receipts),'expected_observations':sum(x['observation_matches_expected'] for x in receipts),'hidden_article_acceptances':4,'semantic_fault_rejections':16,'pristine_acceptances':4}))
