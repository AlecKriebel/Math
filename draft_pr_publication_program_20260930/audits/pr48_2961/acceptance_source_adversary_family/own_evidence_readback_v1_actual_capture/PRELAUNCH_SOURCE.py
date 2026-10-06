"""Own independent completed-capture/read-only result check. No reviewed code execution."""
from pathlib import Path
import datetime as dt, hashlib, json, math, os
F=Path(__file__).absolute().parent; R=F.parents[3]
def need(v,m):
    if not v: raise ValueError(m)
def sha(b): return hashlib.sha256(b).hexdigest()
def parse(b):
    def pairs(v):
        d={}
        for k,x in v: need(k not in d,'Duplicate key'); d[k]=x
        return d
    def fl(s): x=float(s); need(math.isfinite(x),'Finite'); return x
    return json.loads(b,object_pairs_hook=pairs,parse_float=fl,parse_constant=lambda s:(_ for _ in ()).throw(ValueError(s)))
def clock(s):
    c=dt.datetime.fromisoformat(s); need(c.tzinfo is not None and c.utcoffset()==dt.timedelta(0),'UTC aware'); return c
def main():
    captures=[]
    for n,code in [('inspect_fixed_v1_actual_capture',0),('countermodels_v1_actual_capture',1),('countermodels_v2_actual_capture',0)]:
        d=F/n; need({p.name for p in d.iterdir()}=={'CAPTURE.json','PRELAUNCH.json','PRELAUNCH_SOURCE.py','PRELAUNCH_OPERATOR.py','stdout.bin','stderr.bin'},'Exact own CAP6')
        c=parse((d/'CAPTURE.json').read_bytes()); p=parse((d/'PRELAUNCH.json').read_bytes())
        need(c['schema']=='pr48-acceptance-source-adversary-private-actual-capture/v1' and c['production_imported_compiled_executed'] is False and c['actual_execution'] is True and c['completed'] is True and type(c['exit_code']) is int and c['exit_code']==code and type(c['pid']) is int and c['pid']>0 and type(c['operator_pid']) is int and c['operator_pid']>0 and c['stdin_supplied'] is False and c['source_unchanged'] is True and c['operator_unchanged'] is True,'Actual private completed scalar schema')
        need(c['argv']==p['argv'] and c['cwd']==p['cwd']==str(R) and c['argv'][:2]==['/usr/bin/python3','-B'] and Path(c['argv'][2]).parent==F,'Exact private argv/cwd')
        need(sha((d/'PRELAUNCH_SOURCE.py').read_bytes())==c['source_sha256']==p['source_sha256'] and sha((d/'PRELAUNCH_OPERATOR.py').read_bytes())==c['operator_sha256']==p['operator_sha256'],'Complete actual prelaunch source/operator')
        for ch in ['stdout','stderr']:
            z=c[ch]; b=(d/z['path']).read_bytes(); need(set(z)=={'path','bytes','sha256'} and z['path']==ch+'.bin' and type(z['bytes']) is int and len(b)==z['bytes'] and sha(b)==z['sha256'],'Complete own streams')
        need((d/'stderr.bin').read_bytes()==b'' if code==0 else b'Sorted distinct foreign identities' in (d/'stderr.bin').read_bytes(),'Honest actual failure/passing disposition')
        need(clock(c['started_utc'])<=clock(c['finished_utc'])<=dt.datetime.now(dt.timezone.utc),'Actual clock'); captures.append(c)
    result=parse((F/'PRIVATE_CONTROLS_RESULT.json').read_bytes()); printed=parse((F/'countermodels_v2_actual_capture/stdout.bin').read_bytes()); need(result==printed and type(result['actual_pid']) is int and result['actual_pid']==captures[2]['pid'] and result['expected_negative_controls']==92,'Entire saved/printed own controls')
    inspection=parse((F/'FIXED_INPUT_INSPECTION.json').read_bytes()); need(inspection==parse((F/'inspect_fixed_v1_actual_capture/stdout.bin').read_bytes()) and inspection['actual_pid']==captures[0]['pid'] and inspection['metadata_unique_inputs']==4354,'Entire saved/printed own fixed inspection')
    bindings=parse((F/'INPUT_READ_BINDINGS.json').read_bytes()); need(len(bindings['rows'])==4354 and len({z['path'] for z in bindings['rows']})==4354 and all(set(z)=={'path','bytes','sha256','full_mode'} and type(z['bytes']) is int and type(z['full_mode']) is int for z in bindings['rows']),'Complete individually normalized body/mode rows')
    out={'schema':'pr48-independent-acceptance-source-evidence-check/v1','status':'PASS_OWN_EVIDENCE_WITH_ONE_PRESERVED_PRIVATE_FAILURE','actual_pid':os.getpid(),'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'completed_captures':captures,'complete_saved_printed_objects_equal':True,'mandatory_mode_correction_retained':True,'production_imported_compiled_executed':False,'future_acceptance_approved':False}
    with (F/'PRIVATE_EVIDENCE_CHECK.json').open('xb') as h: h.write((json.dumps(out,sort_keys=True,indent=2)+'\n').encode()); h.flush(); os.fsync(h.fileno())
    print(json.dumps({k:v for k,v in out.items() if k!='completed_captures'},sort_keys=True))
if __name__=='__main__': main()
