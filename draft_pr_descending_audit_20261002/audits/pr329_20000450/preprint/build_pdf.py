"""Export the current standalone source with exact native input/output binding."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,sys
A=Path(__file__).resolve().parent.parent; R=A.parents[2]
O=R/'problems/20000450_pentagonal_torsion/preprint'
assert len(sys.argv)==2 and sys.argv[1].isdigit()
D=A/'root_preprint_private'/('pdf_export_v'+sys.argv[1]);assert not D.exists();D.mkdir(parents=True)
T=O/'pentagonal-torsion-note.tex';P=O/'pentagonal-torsion-note.pdf'
sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(p):
    b=p.read_bytes();return dict(bytes=len(b),sha256=sha(b))
source_before=pin(T);(D/'source.tex').write_bytes(T.read_bytes())
if P.exists():(D/'previous.pdf').write_bytes(P.read_bytes())
argv=['/opt/homebrew/bin/tectonic','--outdir',str(O),str(T)]
start=datetime.now(timezone.utc).isoformat();result=subprocess.run(argv,cwd=O,capture_output=True)
end=datetime.now(timezone.utc).isoformat()
(D/'stdout.bin').write_bytes(result.stdout);(D/'stderr.bin').write_bytes(result.stderr)
j=dict(start_utc=start,end_utc=end,argv=argv,actual_exit=result.returncode,
    source_before=source_before,source_after=pin(T),stdout_bytes=len(result.stdout),stdout_sha256=sha(result.stdout),
    stderr_bytes=len(result.stderr),stderr_sha256=sha(result.stderr))
(D/'execution.json').write_text(json.dumps(j,indent=2)+'\n')
assert result.returncode==0 and result.stderr==b'' and source_before==pin(T)
j['pdf']=pin(P);(D/'artifact.pdf').write_bytes(P.read_bytes())
(D/'source_pdf_binding.json').write_text(json.dumps(j,indent=2)+'\n')
print(json.dumps(j,indent=2));print(result.stdout.decode())
