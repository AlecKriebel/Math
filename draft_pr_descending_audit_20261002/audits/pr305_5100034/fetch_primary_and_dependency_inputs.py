"""Read-only direct primary-source and exact dependency-input custody."""
from pathlib import Path
from datetime import datetime,timezone
import subprocess,json,hashlib,stat
A=Path(__file__).resolve().parent;D=A/'root_sources_private';D.mkdir(exist_ok=False)
utc=lambda:datetime.now(timezone.utc).isoformat();sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha(b),mode=f'{stat.S_IMODE(p.stat().st_mode):04o}')
def fetch(name,url):
 argv=['/usr/bin/curl','-q','--fail','--silent','--show-error','--location','--proto','=https','--proto-redir','=https','--no-netrc','--header','Authorization:','--header','Cookie:','--max-time','55',url];start=utc();r=subprocess.run(argv,cwd=A,capture_output=True)
 for k,b in [('stdout',r.stdout),('stderr',r.stderr)]:(D/(name+'.'+k)).write_bytes(b)
 rec=dict(argv=argv,cwd=str(A),started_utc=start,ended_utc=utc(),exit_code=r.returncode,stdout=pin(D/(name+'.stdout')),stderr=pin(D/(name+'.stderr')),readonly_public_input=True,no_automatic_retry=True)
 (D/(name+'.execution.json')).write_text(json.dumps(rec,indent=2)+'\n');assert r.returncode==0,(name,r.stderr)
 out=D/name;out.write_bytes(r.stdout);out.chmod(0o444);return out
sources=[('arxiv-v11.pdf','https://arxiv.org/pdf/2004.12497v11'),('published.pdf','https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf'),('stachel2022.pdf','https://repositum.tuwien.at/bitstream/20.500.12708/136087/1/Stachel-2022-European%20Journal%20of%20Applied%20Mathematics-vor.pdf')]
for name,url in sources:fetch(name,url)
base=A/'snapshot/problems/5100034_focal_pedal_equality'
deps=json.loads((base/'DEPENDENCY_REVIEW_INPUTS.json').read_bytes())
deps += [dict(file='PR210_PROOF.md',commit='2180d64b648b81ac660a792f7823d0b715f9cf12',path='unsolved_math_prioritization/attempts/5100033/PROOF.md',sha256='5a78b9d2fb1f7a0a80e556f2e2b759875bdbba055a454c148524eb44879add7e'),dict(file='PR261_PROOF.md',commit='7b7fcd63d5ea83df3a4c29853c4ba34b93d16f07',path='unsolved_math_prioritization/attempts/5100021/PROOF.md',sha256='f7aada9e28e92c6fab920f1330366acd6eaba8006b4cd0ce52e2dbd58e7ef5b9')]
for e in deps:
 out=fetch(e['file'],'https://raw.githubusercontent.com/AlecKriebel/Math/'+e['commit']+'/'+e['path']);assert pin(out)['sha256']==e['sha256']
original={Path(e['path']).name:e for e in json.loads((base/'SOURCE_HASHES.json').read_bytes())['reference_inputs_local_only']}
records={}
for name,url in sources+[(e['file'],'https://raw.githubusercontent.com/AlecKriebel/Math/'+e['commit']+'/'+e['path']) for e in deps]:
 actual=pin(D/name);expected=original[name];records[name]=dict(url=url,actual=actual,original_declared={k:expected[k] for k in ['bytes','sha256']},original_declared_exact_bytes_match=all(actual[k]==expected[k] for k in ['bytes','sha256']))
result=dict(utc=utc(),status='PASS_PRIMARY_AND_EXACT_DEPENDENCY_INPUTS_FETCHED',inputs=records,dependency_six_exact_hashes_verified=True,PDF_edition_and_content_require_full_read=True,source_record_and_upstream_raw_files_not_in_original_public_packet=True,shared_tracked_index_refs_unmodified=True)
(A/'ROOT_PRIMARY_DEPENDENCY_INPUT_CUSTODY.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
