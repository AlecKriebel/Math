"""New OS process reads persisted intents and refuses all uncertain repeats."""
from pathlib import Path
from datetime import datetime,timezone
import json,subprocess,sys
import adversarial_wire as w
HERE=Path(__file__).resolve().parent
child='''
import sys,json
from pathlib import Path
import run_supplied as s
nt=s.nt
c=s.original.CAPTURED
client=nt.NativeOwnDraftClient("offline-review-token-only",c.metadata,c.files,allow_writes=True,journal_path=Path(sys.argv[1]))
client._wire_request=lambda *a,**k: (_ for _ in ()).throw(RuntimeError("MUTATION REACHED WIRE"))
try:
 client.operation(sys.argv[2],sys.argv[3],sys.argv[4],file=c.files[0]["path"])
except nt.zenodo.DepositError as e:
 print(json.dumps({"refused":True,"existing_intent":sys.argv[2] in client.journal["operations"]}))
else:
 raise SystemExit("Uncertain operation repeated")
'''
results=[]
for kind in ['initialize','content','commit','publish']:
    case=w.WireTests(methodName='runTest');case.setUp()
    try:
        name=case.captured.files[0]['name']
        if kind=='publish':case.stage();method,url,key='POST',w.nt.DRAFT+'/actions/publish','publish';command='publish'
        elif kind=='initialize':method,url,key='POST',w.nt.DRAFT+'/files','initialize:'+name;command='stage'
        else:method,url,key=('PUT' if kind=='content' else 'POST'),w.nt.DRAFT+'/files/'+name+('/content' if kind=='content' else '/commit'),kind+':'+name;command='stage'
        case.server.fault=(method,url,'before')
        try:case.run_kit(command)
        except w.kit.DepositError:pass
        args=[sys.executable,'-B']+(['-O'] if sys.flags.optimize else [])+['-c',child,str(case.client.journal_path),key,method,url]
        done=subprocess.run(args,cwd=HERE,capture_output=True)
        decoded=json.loads(done.stdout) if done.returncode==0 else {}
        results.append({'kind':kind,'child_returncode':done.returncode,**decoded})
    finally:case.tearDown()
result={'checked_utc':datetime.now(timezone.utc).isoformat(),'optimization':sys.flags.optimize,'controls':results,
        'all_uncertain_repeat_attempts_refused':all(r.get('refused') and r.get('existing_intent') and r['child_returncode']==0 for r in results),'real_network_calls':0}
(HERE/('RESTART_OPTIMIZED.json' if sys.flags.optimize else 'RESTART_NORMAL.json')).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
raise SystemExit(not result['all_uncertain_repeat_attempts_refused'])
