"""Fresh OS process uncertain-write guard; captured source, no API calls."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,sys,tempfile
import run_supplied as loaded
HERE=Path(__file__).resolve().parent
nt=loaded.nt
name='gns_generation_counterexample.pdf'
CASES={
 'initialize:'+name:('POST',nt.DRAFT+'/files'),
 'content:'+name:('PUT',nt.DRAFT+'/files/'+name+'/content'),
 'commit:'+name:('POST',nt.DRAFT+'/files/'+name+'/commit'),
 'publish':('POST',nt.DRAFT+'/actions/publish')}
if len(sys.argv)>1:
    journal=Path(sys.argv[1]);key=sys.argv[2]
    def forbidden(*a,**k):
        (journal.parent/'network-called').write_text('bad');raise RuntimeError('Network forbidden')
    nt.http.client.HTTPSConnection=forbidden
    captured=nt.capture_inputs()
    client=nt.NativeOwnDraftClient('offline-restart-only',captured.metadata,captured.files,allow_writes=True,journal_path=journal)
    try:client.operation(key,*CASES[key])
    except nt.zenodo.DepositError as exc:
        if 'already attempted'not in str(exc):raise
    else:raise RuntimeError('Uncertain write was repeated')
    raise SystemExit(0)
controls=[]
with tempfile.TemporaryDirectory(dir=HERE/'tmp')as folder:
    journal=Path(folder)/'journal.json'
    for key in CASES:
        value={'id':23356540,'manifest_sha256':nt.MANIFEST_SHA,'file_pins':{k:list(v)for k,v in nt.FILE_PINS.items()},'operations':{key:{'phase':'attempted','started_utc':'2026-10-14T00:00:00Z'}}}
        nt.durable_journal_save(journal,value);before=journal.read_bytes()
        command=[sys.executable,'-B']+(['-O']if sys.flags.optimize else[])+[str(Path(__file__).resolve()),str(journal),key]
        result=subprocess.run(command,capture_output=True)
        if result.returncode!=0 or journal.read_bytes()!=before or (journal.parent/'network-called').exists():raise RuntimeError('Fresh-process guard failure '+key)
        controls.append({'key':key,'child_exit':result.returncode,'journal_unchanged':True,'network_dispatches':0})
report={'checked_utc':datetime.now(timezone.utc).isoformat(),'optimization':sys.flags.optimize,'controls':controls,'tests':4,'failures':0,'network_calls':0,'scope':'Fresh OS processes read actual durable attempted-operation keys through current captured adapter and refuse duplicate dispatch'}
(HERE/('RESTART_OPTIMIZED.json'if sys.flags.optimize else'RESTART_NORMAL.json')).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'controls':4,'all_uncertain_repeats_refused':True,'optimization':sys.flags.optimize}))
