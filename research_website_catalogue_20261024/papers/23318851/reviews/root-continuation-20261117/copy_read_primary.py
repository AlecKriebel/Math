from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil,subprocess,time
R=Path(__file__).resolve().parent
S=R.parent/'scope-continuation-20261117/primary'
D=R/'primary'
assert not D.exists()
specs=[('seigal.pdf',1073777,'09f688310260a3a07db1c6a0aff53163209e377c201f6044c461eb601cc70163'),('hss-v2.pdf',92607,'68a6e634e0197851b5b1d6d487918597bc0da4f7964cdb84183e8793d95cde34'),('bravyi-v1.pdf',200478,'a23c86f24764a9ce930e7de3bcb23f0a6fc4b34081244b0b749352046668cd30'),('dsl-published.pdf',327613,'707814c6d7ae700bce1c61d5519cd32441cafbe8b60af63c4b21c04acc4f6589'),('sinn-v1.pdf',287133,'1b85888e22d27942bcb4d03ca22ccdf93c251988cacc8bb6e034f91e1c07c8ba'),('ferudun.pdf',147613,'a99172938f203f5a494c2191a73072299857ce8d3adfa6867831ca737c471cbb'),('owr.pdf',1019216,'13b45b3e2c9f585fab343c1d10d3e0fc9e1b4cf47880b5bcf1808fcb23280de3'),('pr170-original-proof.md',13135,'da019dd76c0ea7bdf789df23410cf85b75f5a30af11ffe7646d1654c7261c5a8')]
def check(f,size,pin):
 b=f.read_bytes();assert len(b)==size and hashlib.sha256(b).hexdigest()==pin
 return b
before={n:check(S/n,size,pin) for n,size,pin in specs}
D.mkdir()
receipts=[]
for n,size,pin in specs:
 dest=D/n;dest.write_bytes(before[n]);dest.chmod(0o444)
 check(dest,size,pin)
 if n.endswith('.pdf'):
  for label,argv in [('info',['pdfinfo',str(dest)]),('text',['pdftotext','-layout',str(dest),str(D/(n+'.txt'))])]:
   started=datetime.now(timezone.utc).isoformat();t=time.monotonic();p=subprocess.run(argv,capture_output=True,check=False)
   (D/(n+'.'+label+'.stdout.bin')).write_bytes(p.stdout);(D/(n+'.'+label+'.stderr.bin')).write_bytes(p.stderr)
   receipts.append({'argv':argv,'UTC':started,'seconds':time.monotonic()-t,'exit':p.returncode,'stdout_bytes':len(p.stdout),'stderr_bytes':len(p.stderr)})
   (R/'PRIMARY_COPY_EXECUTIONS.json').write_text(json.dumps(receipts,indent=2)+'\n')
   assert p.returncode==0
for n,size,pin in specs:assert check(S/n,size,pin)==before[n]
result={'UTC':datetime.now(timezone.utc).isoformat(),'status':'RAW_PRIMARY_BODIES_COPIED_AUTHENTICATED','source':str(S),'root_owned_destination':str(D),'files':[{'name':n,'bytes':size,'SHA256':pin} for n,size,pin in specs],'raw_primary_bytes_only_no_peer_opinions_opened':True,'source_pinned_files_before_after_exact':True,'personal_reading_not_inferred_from_copy':True,'root_scientific_program_runs':0,'rights':'Third-party private reading copies; original authors retain copyright, not part of public site or Zenodo package'}
(R/'PRIMARY_COPY.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'PDFs':7,'original_theorem_files':1,'data_child_exits':[r['exit'] for r in receipts]}))
