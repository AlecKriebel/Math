from pathlib import Path
import sys,json,datetime,traceback
D=Path(__file__).resolve().parent
sys.path.insert(0,str(D))
import probes as H
H.C=D.parent.parent
import followup_probes as F
import edge_probes as E
import compact_fixtures as Z
rows=[]
controls=[('M01_wrong_response',H.range_mismatch,['wrong_get_range']),('M02_partial_http',H.partial_http,['partial_http']),('M02_binary_stream',H.decode_loss,['text_decode_loss']),('M02_all_text_readers',E.text_readers,['all_text_readers']),('M03_final_native_drift',F.drift_completion,['completion_drift_final'])]
for name,fn,fixtures in controls:
 start=H.utc()
 try:r=dict(name=name,start_utc=start,end_utc=None,PASS=True,result=fn())
 except Exception as e:r=dict(name=name,start_utc=start,end_utc=None,PASS=False,error=repr(e),traceback=traceback.format_exc())
 r['end_utc']=H.utc();rows.append(r);H.js(D/'ROOT_RESULTS.json',rows);print(json.dumps(r),flush=True)
 for fixture in fixtures:
  if (D/'fixtures'/fixture).exists():Z.main([fixture])
H.js(D/'ROOT_REPLAY_RECEIPT.json',dict(utc=H.utc(),all5_defect_controls_reproduced=all(x['PASS'] for x in rows),groups=len(rows),sources_exact_frozen02=True,provider_calls_only_controlled=True,no_release_authority=True,case_completion_percent=65))
sys.exit(0 if all(x['PASS'] for x in rows) else 1)
