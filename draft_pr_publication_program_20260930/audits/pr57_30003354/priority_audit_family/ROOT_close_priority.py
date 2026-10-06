"""ROOT-only absent closure of the bounded priority family; no approval."""
from pathlib import Path
import argparse,datetime as dt,hashlib,json,os,stat

F=Path(__file__).absolute().parent
def digest(b):return hashlib.sha256(b).hexdigest()
def row(p):
    s=p.lstat();assert stat.S_ISREG(s.st_mode) and not p.is_symlink(),p
    b=p.read_bytes();return dict(path=p.name,bytes=len(b),sha256=digest(b),full_mode=format(stat.S_IMODE(s.st_mode),'04o'))
def fixed_inputs():
    for z in json.loads((F/'BINDINGS.json').read_text())['rows']:
        p=Path(z['path']);s=p.lstat();assert stat.S_ISREG(s.st_mode) and not p.is_symlink(),p
        b=p.read_bytes();assert (len(b),digest(b),format(stat.S_IMODE(s.st_mode),'04o'))==(z['bytes'],z['sha256'],z['full_mode']),p
    # Primary bodies stay in our ignored cache; receipts, not copies, are public.
    for z in json.loads((F/'PRIMARY_READING.json').read_text())['read_receipts']:
        for k in ('pdf_reference','extracted_text_reference'):
            q=z[k];p=Path(q['path']);s=p.lstat();assert stat.S_ISREG(s.st_mode) and not p.is_symlink(),p
            b=p.read_bytes();assert (len(b),digest(b),format(stat.S_IMODE(s.st_mode),'04o'))==(q['bytes'],q['sha256'],q['full_mode']),p
def main():
    a=argparse.ArgumentParser();a.add_argument('--ready-sha256',required=True);v=a.parse_args()
    assert all(not p.is_symlink() for p in [F,*F.parents])
    assert not (F/'SELF_MANIFEST.json').exists()
    raw=(F/'READY.json').read_bytes();assert digest(raw)==v.ready_sha256
    ready=json.loads(raw);assert ready['status']=='READY_FOR_PRIORITY_ADJUDICATION' and ready['ROOT_approval_claimed'] is False
    actual=list(F.iterdir());assert all(p.is_file() and not p.is_symlink() for p in actual)
    assert {p.name for p in actual}=={z['path'] for z in ready['payload_without_READY']}|{'READY.json'}
    for z in ready['payload_without_READY']:assert row(F/z['path'])==z,z['path']
    assert row(F/'READY.json')['full_mode']=='0444'
    fixed_inputs()
    out=dict(schema='pr57-independent-priority-closure/v1',status='CLOSED_SOURCE_ONLY_PRIORITY_AUDIT',utc=dt.datetime.now(dt.timezone.utc).isoformat(),actual_pid=os.getpid(),ready_sha256=v.ready_sha256,self_excluded=True,files=[row(p) for p in sorted(actual)],relative_directories=[],priority_verdict='READY_FOR_PRIORITY_ADJUDICATION',ROOT_approval_claimed=False,math_reviewer_credit_transferred=False,paper_or_native_mutation=False)
    with (F/'SELF_MANIFEST.json').open('x') as f:json.dump(out,f,indent=2,sort_keys=True);f.write('\n');f.flush();os.fsync(f.fileno())
    os.chmod(F/'SELF_MANIFEST.json',0o444)
    print(json.dumps(dict(status=out['status'],actual_pid=os.getpid(),payload_count=len(actual),manifest_sha256=digest((F/'SELF_MANIFEST.json').read_bytes()))))
if __name__=='__main__':main()
