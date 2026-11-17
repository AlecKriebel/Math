from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, stat, subprocess, time

R=Path(__file__).resolve().parent
S=R.parent.parent/'sources'
def sha(f): return hashlib.sha256(f.read_bytes()).hexdigest()
def snapshot():
    rows=[]
    for f in [S]+sorted(S.rglob('*')):
        assert not f.is_symlink()
        row={'path':str(f.relative_to(S)),'kind':'directory' if f.is_dir() else 'file','mode':oct(stat.S_IMODE(f.stat().st_mode))}
        if f.is_file(): row.update(bytes=f.stat().st_size,SHA256=sha(f))
        else: row['empty']=not any(f.iterdir())
        rows.append(row)
    return rows
assert sha(S/'SOURCE_FINAL.json')=='b68fbb425b7d910a2508c46ff311491a1c797568dcf39d3c7deb0a0545e1afd5'
assert sha(S/'SOURCE_MANIFEST.json')=='afa64c126da0aabc4a44ec242553e5b2354540eb1b0b60e55ab7b1a9855a09be'
before=snapshot()
assert sum(r['kind']=='file' for r in before)==55
assert sum(r['kind']=='directory' for r in before)==15
m=json.loads((S/'SOURCE_MANIFEST.json').read_text())
expected={e['path']:e for e in m['entries']}
expected.update({n:{'path':n,'kind':'file','mode_octal':v} for n,v in m['terminal_modes'].items()})
assert set(expected)=={e['path'] for e in before}
for a in before:
    e=expected[a['path']]
    assert a['mode']==e['mode_octal'] and a['kind']==e['kind']
    if 'sha256' in e: assert a['SHA256']==e['sha256'] and a['bytes']==e['bytes']
    if 'empty' in e: assert a['empty']==e['empty']
assert not (R/'SOURCE_BEFORE.json').exists()
(R/'SOURCE_BEFORE.json').write_text(json.dumps(before,indent=2)+'\n')
pdf=S/'zenodo-files/paper.pdf'
assert sha(pdf)=='527ac7feb6f2c889998559122296dd8caab2def0cf7aeac00f79c1f8b0c8a978'
commands=[['pdfinfo',str(pdf)],['pdftotext','-layout',str(pdf),str(R/'original-fresh.txt')],['pdftoppm','-r','110','-png',str(pdf),str(R/'original-page')]]
receipts=[]
for n,cmd in enumerate(commands):
    start=datetime.now(timezone.utc).isoformat(); t=time.monotonic()
    result=subprocess.run(cmd,capture_output=True,check=False)
    (R/f'command-{n}.stdout.bin').write_bytes(result.stdout)
    (R/f'command-{n}.stderr.bin').write_bytes(result.stderr)
    receipts.append({'argv':cmd,'UTC':start,'seconds':time.monotonic()-t,'exit':result.returncode,'stdout_bytes':len(result.stdout),'stderr_bytes':len(result.stderr)})
    (R/'ACQUISITION_EXECUTIONS.json').write_text(json.dumps(receipts,indent=2)+'\n')
    assert result.returncode==0
after=snapshot()
(R/'SOURCE_AFTER.json').write_text(json.dumps(after,indent=2)+'\n')
assert before==after
print(json.dumps({'status':'ORIGINAL_DATA_ACQUIRED_SOURCE_EXACT','files':55,'childdirs':14,'pages':len(list(R.glob('original-page-*.png'))),'scientific_or_source_program_runs':0}))
