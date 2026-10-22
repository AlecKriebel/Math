"""Stage only the reviewed PR248 against fresh native main, preserving other work."""
from pathlib import Path
from datetime import datetime, timezone
import base64, hashlib, json, subprocess
PRE=Path(__file__).resolve().parent
ROOT=Path('/Users/alec/Documents/Math')
D=PRE.parent/'initial_review_20261013'
PUB=PRE.parent/'publication'
OUT=PUB/('native-pr-integration-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
OUT.mkdir(parents=True,exist_ok=False)
GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
B='repos/AlecKriebel/Math/'
seq=0

def api(method,path,payload=None):
    global seq
    seq+=1;args=[GH,'api','--method',method,B+path]
    if payload is not None:
        f=OUT/f'{seq:02d}-request.json';f.write_text(json.dumps(payload));args+=['--input',str(f)]
    r=subprocess.run(args,capture_output=True)
    (OUT/f'{seq:02d}-stdout.json').write_bytes(r.stdout)
    (OUT/f'{seq:02d}-stderr.txt').write_bytes(r.stderr)
    if r.returncode:raise RuntimeError(f'Native call {seq} failed; reconcile before retrying an uncertain mutation')
    return json.loads(r.stdout)

clear=json.loads((PRE/'FINAL_CLEARANCE.json').read_text())
assert clear['mathematical_verdict']=='PASS' and clear['fresh_clean_reviews']>=3
for name,pin in clear['candidate_files'].items():
    data=(PRE/name).read_bytes();assert len(data)==pin['bytes'] and hashlib.sha256(data).hexdigest()==pin['sha256']
z=json.loads((PUB/'ZENODO_VERIFIED_PUBLICATION.json').read_text())
t=json.loads((PUB/'TRACKER_VERIFIED_APPEND.json').read_text())
assert z['submitted'] and z['metadata_and_files_verified'] and t['verified'] and t['doi_url']==z['doi_url']
doi=z['doi_url']
assert not (PUB/'PR_PREPARED.json').exists(), 'Prepared head exists; reconcile before retry'
i=json.loads((D/'INTAKE.json').read_text())
pr=api('GET','pulls/248')
assert pr['state']=='open' and pr['draft'] and pr['head']['sha']==i['head']
oldhead=pr['head']['sha']
q=api('GET','contents/'+i['Queue_path']+'?ref='+oldhead)
row=next(x for x in base64.b64decode(q['content']).decode().splitlines() if '30004630 / OWR-4990378-001' in x)
assert row.split('|')[8].strip()=='claimed_solved'
base=api('GET','git/ref/heads/main')['object']['sha']
basetree=api('GET','git/commits/'+base)['tree']['sha']
q=api('GET','contents/'+i['Queue_path']+'?ref='+base)
oldqueue=base64.b64decode(q['content']).decode()
rows=[x for x in oldqueue.splitlines() if '30004630 / OWR-4990378-001' in x]
assert len(rows)==1
oldrow=rows[0];cells=[x.strip() for x in oldrow.split('|')][1:-1]
assert cells[7] in {'queued','claimed_solved'}
cells[7]='claimed_solved';cells[8]='1/5'
cells[10]=('2026-10-14: Explicit negative answer to unchanged ordinary-cone strict positivity to strong control-L2 growth at beta2=0 in actual critical quintic wave. '
           'Unique global zero optimizer, zero cone/vacuity, Linfinity-null pulses; per-fixed-finite-nu radial all-optimizer non-Lipschitz estimate; local L1 growth and weaker upper bounds. '
           'Independent math/source, bounded classical/recent priority and three sequential NEW full manuscript audits passed; final editorial payload independently checked. '
           'Classical mechanisms credited; no firstness certificate. Unrefereed extensive-AI preprint: '+doi)
newrow='| '+' | '.join(cells)+' |'
newqueue=oldqueue.replace(oldrow,newrow)
assert newqueue.count(newrow)==1 and newqueue.replace(newrow,oldrow)==oldqueue
entries=[{'path':i['Queue_path'],'mode':'100644','type':'blob','content':newqueue}]
staged=PRE/'pr_update/30004630'
assert staged.is_dir()
for p in sorted(staged.rglob('*')):
    if p.is_file():entries.append({'path':i['native_source_prefix']+p.relative_to(staged).as_posix(),'mode':'100644','type':'blob','content':p.read_text()})
paths=[p for p in PRE.iterdir() if p.is_file() and p.suffix in {'.tex','.json','.py','.md','.txt'}]
paths += [PRE/'output/pdf/critical_wave_growth.pdf',PRE/'output/critical_wave_verification.zip']
paths += [p for p in (PRE/'verification_package').rglob('*') if p.is_file() and '__pycache__' not in p.parts]
paths += [p for p in (PRE/'history').rglob('*') if p.is_file()]
for name in ['fresh_review_01','fresh_review_02','fresh_review_03','editorial_delta_review_01']:
    folder=PRE/name;fm=folder/'FINAL_AUDIT_MANIFEST.json';m=json.loads(fm.read_text());paths.append(fm)
    keys=[k for k in ['public_authored_relative_paths','public_authored_files','authored_files','files'] if k in m]
    assert len(keys)==1,(name,keys)
    pins=m[keys[0]];pins=[{'path':k,**v} for k,v in pins.items()] if isinstance(pins,dict) else pins
    for pin in pins:
        p=folder/pin.get('path',pin.get('relative_path'))
        assert p.resolve().is_relative_to(folder.resolve())
        data=p.read_bytes();assert len(data)==pin['bytes'] and hashlib.sha256(data).hexdigest()==pin['sha256']
        paths.append(p)
paths += [PUB/'ZENODO_VERIFIED_PUBLICATION.json',PUB/'TRACKER_VERIFIED_APPEND.json',D/'RESEARCH_LOG.md']
paths += [p for p in (D/'priority_classical_adversary_01/historical_recovery').rglob('*') if p.is_file() and '__pycache__' not in p.parts]
nativepins=[]
for p in sorted(set(paths)):
    assert p.resolve().is_relative_to(PRE.parent.resolve()) and not p.is_symlink()
    data=p.read_bytes();entry={'path':p.relative_to(ROOT).as_posix(),'mode':'100644','type':'blob'}
    if p.suffix in {'.pdf','.zip'}:
        entry['sha']=api('POST','git/blobs',{'content':base64.b64encode(data).decode(),'encoding':'base64'})['sha']
    else:entry['content']=data.decode()
    entries.append(entry);nativepins.append({'path':entry['path'],'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
assert len({x['path'] for x in entries})==len(entries)
newtree=api('POST','git/trees',{'base_tree':basetree,'tree':entries})['sha']
commit=api('POST','git/commits',{'message':'Finalize audited critical-wave quadratic-growth counterexample and published preprint','tree':newtree,'parents':[base,oldhead]})['sha']
assert api('GET','pulls/248')['head']['sha']==oldhead
prepared={'utc':datetime.now(timezone.utc).isoformat(),'original_head':oldhead,'prepared_head':commit,'main_parent':base,'tree':newtree,'doi_url':doi,'target_queue_row':newrow,'included_owned_pins':nativepins,'branch_mutation_status':'about to be attempted; outcome not yet known'}
(PUB/'NATIVE_PREPARATION_ATTEMPT.json').write_text(json.dumps(prepared,indent=2)+'\n')
updated=api('PATCH','git/refs/heads/'+pr['head']['ref'],{'sha':commit,'force':False})
assert updated['object']['sha']==commit
title='30004630: refute unchanged unregularized strong-L2 growth for the critical wave'
body=('The actual capped energy-critical quintic-wave problem on the 3D unit ball has a unique global zero optimizer with ordinary critical cone {0}. '
      'The source strict condition is vacuous, while feasible controls converging in Linfinity have gap o(the squared control-L2 norm), defeating both source localizations after beta2 is removed. '
      'For every fixed finite nonnegative velocity weight, every global optimizer under positive radial terminal-target perturbations fails the stated Lipschitz L2 estimate. '
      'Local L1 quadratic growth and weaker fixed-basepoint upper bounds survive. This answers the unchanged implication, without claiming a complete unregularized replacement theory or a sharp exponent.\n\n'
      'Independent mathematical/source families, extensive bounded classical/recent priority audits and three sequential NEW full manuscript reviews passed. '
      'A full new review after editorial refinements and a separate independent final-payload addendum found no mandatory remaining issue. '
      'The compatible nonlinear-state proof and compactness argument are analytic; seven portable full scientific receipts reproduce5603 exact assertions plus5 noncertified diagnostics.\n\n'
      'Classical wave estimates, group-sparse threshold calculus and concentration/noncoercivity/NDC methods are credited. No covering predecessor was authenticated in the bounded accessible corpus; worldwide firstness is not certified.\n\n'
      'Six-page preprint and113-file verification archive: '+doi+'\n\n'
      'AI tools were used extensively. This is unrefereed, without external human peer review or proof-assistant formalization. Exact Zenodo metadata/files and the requested Google Workspace tracker row were read back. '
      'All original19 source bytes and historical audits are preserved; current presentation clarifies the radial quantifier, dense tangents and mild-limit identification.')
api('PATCH','pulls/248',{'title':title,'body':body})
prepared.update(title=title,body=body,branch_mutation_status='verified nonforce fast-forward',shared_checkout_and_index_mutations=0,native_merge_pending=True)
(PUB/'PR_PREPARED.json').write_text(json.dumps(prepared,indent=2)+'\n')
print(json.dumps({k:v for k,v in prepared.items() if k not in {'body','included_owned_pins','target_queue_row'}},indent=2))
