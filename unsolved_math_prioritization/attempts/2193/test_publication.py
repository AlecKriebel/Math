#!/usr/bin/env python3
"""Corruption and relocation controls for the publication verifier."""
from pathlib import Path
from types import SimpleNamespace
import hashlib,io,json,runpy,shutil,subprocess,sys,tempfile,warnings,zipfile
D=Path(__file__).resolve().parent
M=runpy.run_path(str(D/'verify_publication.py'));H=M['H'];need=M['need'];inspect=M['inspect'];pins=M['PINS'];negative=[]
def reject(label,fn):
 try:fn()
 except (ValueError,KeyError,zipfile.BadZipFile,UnicodeError,FileNotFoundError):negative.append(label);return
 raise RuntimeError('Invalid control accepted: '+label)
p=pins['packs'][0];ab=(D/'archives'/p['archive']['name']).read_bytes();mb=(D/'archives'/p['manifest']['name']).read_bytes();original=inspect(ab,mb,p['archive'],p['manifest'],5)
reject('outer ZIP corruption',lambda:inspect(ab+b'x',mb,p['archive'],p['manifest'],5));reject('external manifest corruption',lambda:inspect(ab,mb+b' ',p['archive'],p['manifest'],5))
def mutant(label,change,rebind=False):
 es=[dict(path=n,data=b,mode=0o100644) for n,b in original.items()];change(es);buf=io.BytesIO()
 with warnings.catch_warnings():
  warnings.simplefilter('ignore',UserWarning)
  with zipfile.ZipFile(buf,'w') as z:
   for e in es:i=zipfile.ZipInfo(e['path']);i.external_attr=e['mode']<<16;z.writestr(i,e['data'])
 b=buf.getvalue();m=json.loads(mb);m['archive'].update(bytes=len(b),sha256=H(b))
 if rebind:m['members']=[dict(path=e['path'],bytes=len(e['data']),sha256=H(e['data'])) for e in es]
 mm=json.dumps(m).encode();mp=dict(p['manifest'],bytes=len(mm),sha256=H(mm));reject(label,lambda:inspect(b,mm,m['archive'],mp,5))
mutant('changed member',lambda e:e[0].update(data=e[0]['data']+b'x'))
mutant('missing member',lambda e:e.pop())
mutant('extra member',lambda e:e.append(dict(path='extra.md',data=b'x',mode=0o100644)))
mutant('duplicate member',lambda e:e.append(e[0].copy()))
for label,path in [('absolute path','/bad.md'),('traversal','../bad.md'),('backslash','bad\\path.md'),('colon','C:bad.md'),('unexpected nested member','nested/bad.md'),('unexpected extension','bad.pdf')]:mutant(label,lambda e,path=path:e[0].update(path=path),True)
mutant('symlink member',lambda e:e[0].update(mode=0o120644),True);mutant('executable member',lambda e:e[0].update(mode=0o100755),True);mutant('invalid UTF-8',lambda e:e[0].update(data=b'\xff'),True);mutant('invalid JSON',lambda e:e[0].update(path='bad.json',data=b'{'),True)
accepted={f.name:f.read_bytes() for f in (D/'accepted_author').iterdir()};patch=(D/'independent_audit/CLARIFICATIONS.patch').read_bytes()
reject('patch produces incorrect accepted bytes',lambda:M['replay'](original,dict(accepted,**{'README.md':accepted['README.md']+b'x'}),patch))
reject('patch hunk altered',lambda:M['replay'](original,accepted,patch.replace(b'+The supplied',b'+Different supplied',1)))
args=SimpleNamespace(catalog=None,problems=None,reports=None,sources_directory=None)
with tempfile.TemporaryDirectory() as tmp:
 temp=Path(tmp)/'relocated'/'nested';shutil.copytree(D,temp)
 r=M['verify'](temp,args);need(r['status']=='PASS','relocation');need(not r['corpus_checks']['performed'] and not r['source_checks']['performed'],'honest skips')
 f=temp/'accepted_author/README.md';b=f.read_bytes();f.write_bytes(b+b'x');reject('changed loose accepted file',lambda:M['verify'](temp,args));f.write_bytes(b)
 f=temp/'INDEPENDENT_AUDIT_RECEIPT.json';b=f.read_bytes();f.write_bytes(b+b' ');reject('changed independent receipt',lambda:M['verify'](temp,args));f.write_bytes(b)
 f=temp/'PUBLICATION_METADATA.json';b=f.read_bytes();o=json.loads(b);o['queue_status']='already_solved';f.write_text(json.dumps(o));reject('overbroad queue scope',lambda:M['verify'](temp,args));f.write_bytes(b)
 f=temp/'independent_audit/EXACT_ACCEPTANCE.json';b=f.read_bytes();o=json.loads(b);o['decision']='ACCEPT_FULL_SOLUTION';f.write_text(json.dumps(o));reject('overbroad acceptance',lambda:M['verify'](temp,args));f.write_bytes(b)
 fake=Path(tmp)/'bad.json';fake.write_text('{}');meta=json.loads((D/'independent_audit/INPUT_VERIFICATION.json').read_bytes());sources=json.loads((D/'independent_audit/SOURCE_AUDIT.json').read_bytes())
 reject('incomplete corpus arguments',lambda:M['inputs'](SimpleNamespace(catalog=str(fake),problems=None,reports=None,sources_directory=None),meta,sources))
 reject('corrupt complete corpus',lambda:M['inputs'](SimpleNamespace(catalog=str(fake),problems=str(fake),reports=str(fake),sources_directory=None),meta,sources))
 reject('missing source PDFs',lambda:M['inputs'](SimpleNamespace(catalog=None,problems=None,reports=None,sources_directory=tmp),meta,sources))
print(json.dumps(dict(status='PASS',optimization_level=sys.flags.optimize,relocated_package_verified=True,omitted_input_checks_explicitly_skipped=True,negative_controls_rejected=negative,negative_control_count=len(negative),historical_audit_executed=False),indent=2))
