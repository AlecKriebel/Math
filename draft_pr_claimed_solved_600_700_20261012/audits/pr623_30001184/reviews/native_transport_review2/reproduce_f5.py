"""Parent's deployed extractor shapes, rebased to own 623 in an offline server.

This reviewer makes no network calls here. Real kit/native methods and real
immutable bytes are exercised through the independent stdlib wire substitute.
"""
from pathlib import Path
from datetime import datetime,timezone
from copy import deepcopy
import hashlib,json,sys,unittest,zipfile,io
import adversarial_wire as wire
HERE=Path(__file__).resolve().parent
observed=json.loads((HERE/'tmp/primary/NATIVE_PUBLISHED_FILE_COLLECTION_CALIBRATION.json').read_bytes())
calibration={'.pdf':observed['entries'][0],'.zip':observed['entries'][1]}
results=[]
def annotated(entry,kind,which):
    out=deepcopy(entry)
    if which in ('metadata','both'):
        out['metadata']=deepcopy(calibration[kind]['metadata'])
        if kind=='.zip':
            data=wire.captured_modules.original.FILES[1]['path'].read_bytes()
            with zipfile.ZipFile(io.BytesIO(data)) as z:out['metadata']['zip_toc_position']=z.start_dir
    if which in ('links','both'):
        for name,url in calibration[kind]['links'].items():
            if name in {'self','content'}:continue
            out['links'][name]=url.replace(str(observed['record_id']),str(wire.nt.RECORD_ID)).replace(calibration[kind]['key'],entry['key'])
    return out
for kind in ['.pdf','.zip']:
    for which in ['metadata','links','both']:
        case=wire.WireTests(methodName='runTest');case.setUp()
        try:
            case.stage() # Genuine unannotated positive baseline, exact bytes.
            before=case.writes()
            def collection(r):
                r['entries']=[annotated(e,kind,which) if e['key'].endswith(kind) else e for e in r['entries']]
            case.server.list_mutator=collection
            for state,command in [('ready_draft','publish'),('published','inspect')]:
                case.server.published=state=='published'
                try:case.run_kit(command)
                except wire.kit.DepositError as exc:
                    result={'kind':kind,'annotation':which,'remote_state':state,'command':command,'rejected':True,
                            'reason':str(exc),'mutation_added':case.writes()!=before,
                            'receipt_saved':'publication' in wire.kit.read_json(case.place),
                            'reviewed_payload_sha256_matches':all(hashlib.sha256(case.server.content[n]).hexdigest()==p[1] for n,p in wire.nt.FILE_PINS.items())}
                else:result={'kind':kind,'annotation':which,'remote_state':state,'command':command,'rejected':False}
                results.append(result)
        finally:case.tearDown()
report={'checked_utc':datetime.now(timezone.utc).isoformat(),'optimization':sys.flags.optimize,
        'expected_defect_reproduced':len(results)==12 and all(r['rejected'] and not r['mutation_added'] and not r['receipt_saved'] and r['reviewed_payload_sha256_matches'] for r in results),
        'controls':results,'real_network_calls':0,'production_publication_attempted':False,
        'basis':'Parent deployed own-PR618 read-only collection receipt; ID/key rebased only inside own offline model. Actual PR623 generated annotations remain unexecuted.'}
dest=HERE/('F5_OPTIMIZED.json' if sys.flags.optimize else 'F5_NORMAL.json')
dest.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
if not report['expected_defect_reproduced']:raise SystemExit(1)
