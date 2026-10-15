"""ROOT-only separate readback; no mathematical, priority or publication approval."""
from pathlib import Path
import argparse,hashlib,json,os,stat
F=Path(__file__).absolute().parent
def main():
    a=argparse.ArgumentParser();a.add_argument('--manifest-sha256',required=True);v=a.parse_args()
    assert all(not p.is_symlink() for p in [F,*F.parents])
    p=F/'SELF_MANIFEST.json';s=p.lstat();b=p.read_bytes()
    assert stat.S_ISREG(s.st_mode) and stat.S_IMODE(s.st_mode)==0o444 and hashlib.sha256(b).hexdigest()==v.manifest_sha256
    m=json.loads(b);assert m['schema']=='pr57-independent-priority-closure/v1' and m['priority_verdict']=='READY_FOR_PRIORITY_ADJUDICATION' and m['ROOT_approval_claimed'] is False
    assert {p.name for p in F.iterdir()}=={z['path'] for z in m['files']}|{'SELF_MANIFEST.json'}
    for z in m['files']:
        p=F/z['path'];s=p.lstat();b=p.read_bytes();assert stat.S_ISREG(s.st_mode) and not p.is_symlink()
        assert (len(b),hashlib.sha256(b).hexdigest(),format(stat.S_IMODE(s.st_mode),'04o'))==(z['bytes'],z['sha256'],z['full_mode'])
    for z in json.loads((F/'BINDINGS.json').read_text())['rows']:
        p=Path(z['path']);s=p.lstat();b=p.read_bytes();assert stat.S_ISREG(s.st_mode) and not p.is_symlink()
        assert (len(b),hashlib.sha256(b).hexdigest(),format(stat.S_IMODE(s.st_mode),'04o'))==(z['bytes'],z['sha256'],z['full_mode'])
    for z in json.loads((F/'PRIMARY_READING.json').read_text())['read_receipts']:
        for k in ('pdf_reference','extracted_text_reference'):
            q=z[k];p=Path(q['path']);s=p.lstat();b=p.read_bytes();assert stat.S_ISREG(s.st_mode) and not p.is_symlink()
            assert (len(b),hashlib.sha256(b).hexdigest(),format(stat.S_IMODE(s.st_mode),'04o'))==(q['bytes'],q['sha256'],q['full_mode'])
    print(json.dumps(dict(status='READBACK_PASS_SOURCE_ONLY',actual_pid=os.getpid(),payload_count=len(m['files']),manifest_sha256=v.manifest_sha256,ROOT_approval_claimed=False)))
if __name__=='__main__':main()
