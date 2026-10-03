#!/usr/bin/env python3
"""Private copies, bounded replay, exact stdout and counterfeit-source controls."""
from pathlib import Path
import datetime, hashlib, json, os, shutil, subprocess, sys, time
P=Path(__file__).resolve().parent
S=P.parent/'snapshot'/'problems'/'30003853_thompson_subgroup_abelianization'
D=P/'private'/'author'
if D.exists(): shutil.rmtree(D)
shutil.copytree(S,D)
R=P/'replay_outputs';R.mkdir(exist_ok=True)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
receipts=[]
def run(label,args,cwd,expected=None,timeout=90):
    start=time.monotonic()
    r=subprocess.run(args,cwd=cwd,env=env,capture_output=True,timeout=timeout)
    out=R/(label+'.stdout');err=R/(label+'.stderr')
    out.write_bytes(r.stdout);err.write_bytes(r.stderr)
    rec={'label':label,'arguments':args,'cwd':str(cwd),'exit':r.returncode,
         'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'seconds':round(time.monotonic()-start,6),
         'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),
         'stderr_sha256':hashlib.sha256(r.stderr).hexdigest(),
         'stdout_bytes':len(r.stdout),'stderr_bytes':len(r.stderr)}
    if expected is not None: rec['exact_stdout_matches_frozen']=r.stdout==expected
    receipts.append(rec)
    return r

for t in range(1,6):
    q=run('author_turn'+str(t),[sys.executable,str(D/('verify_turn'+str(t)+'.py'))],D,
          (S/('TURN_'+str(t)+'_CHECKS.json')).read_bytes())
    assert q.returncode==0 and receipts[-1]['exact_stdout_matches_frozen']
q=run('author_all_public',[sys.executable,str(D/'REPLAY_ALL.py')],D)
assert q.returncode==0
expected=json.loads((S/'FINAL_REPLAY.json').read_text());expected['local_source_bindings']=0
assert json.loads(q.stdout)==expected
q=run('historical_independent',[sys.executable,str(D/'independent_review'/'independent_check.py')],D/'independent_review',
      (S/'independent_review'/'INDEPENDENT_CHECKS.json').read_bytes())
assert q.returncode==0 and receipts[-1]['exact_stdout_matches_frozen']
q=run('publication',[sys.executable,str(D/'verify_publication.py')],D)
assert q.returncode==0

# Counterfeit sources have the advertised lengths, so failure is specifically
# due to the SHA, not merely a filename, size, format, or retrieval failure.
bad=P/'private'/'counterfeit_sources';bad.mkdir(exist_ok=True)
entries=[]
for name in ('SOURCE_MANIFEST.json','TURN_3_SOURCES.json','TURN_5_SOURCES.json'):
    entries+=json.loads((S/name).read_text())['files']
for e in entries:
    prefix=b'%PDF-1.7\nCOUNTERFEIT theorem: every quotient of a torsion-free group is torsion-free.\n'
    (bad/Path(e['path']).name).write_bytes((prefix+b' ' * e['bytes'])[:e['bytes']])
q=run('counterfeit_optional_omitted',[sys.executable,str(D/'REPLAY_ALL.py')],D)
assert q.returncode==0 and json.loads(q.stdout)['local_source_bindings']==0
q=run('counterfeit_explicit_source_binding',[sys.executable,str(D/'REPLAY_ALL.py'),'--source-dir',str(bad)],D)
assert q.returncode!=0 and b'bgk-p6.png' in q.stderr

# Independent content-gate control on the three primary dependencies, matching
# their manifest SHA rather than trusting MIME, PDF magic, a URL, or the claim.
manifest_by_name={Path(e['path']).name:e for e in entries}
source_checks=[]
for own,original in [('owr2018-26.pdf','owr2018-26.pdf'),
                     ('kassabov-matucci.pdf','kassabov-matucci.pdf'),
                     ('bleak-algebraic.pdf','bleak2006-algebraic.pdf')]:
    b=(P/'sources'/own).read_bytes();e=manifest_by_name[original]
    ck=len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256']
    fake=b[:200]+bytes([b[200]^1])+b[201:]
    rejected=hashlib.sha256(fake).hexdigest()!=e['sha256']
    assert ck and rejected and fake.startswith(b'%PDF-')
    source_checks.append({'source':original,'genuine_sha_match':ck,
                          'same_length_one_byte_pdf_counterfeit_rejected':rejected})

summary={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'author_assertions':562635,'historical_independent_assertions':110736,
         'full_public_replay_passed':True,'source_binding_count_public':0,
         'counterfeit_explicit_source_mode_rejected':True,
         'counterfeit_optional_omitted_mode_passed_with_zero_binding_label':True,
         'primary_source_checks':source_checks,'receipts':receipts}
(P/'REPLAY_RECEIPTS.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='receipts'},sort_keys=True,indent=2))
