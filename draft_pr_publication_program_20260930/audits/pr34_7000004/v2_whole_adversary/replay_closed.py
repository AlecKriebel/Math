"""Reproduce this closed audit in a new private directory; never rewrite its source."""
from pathlib import Path
import argparse, datetime, hashlib, json, shutil, subprocess, sys

SOURCE=Path(__file__).resolve().parent
P=Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr34_7000004')
C=P/'reviewed_candidate_v2'
FROZEN='8afc9a17669c12559aea4287117069a20fbb39eea2af4ffe9bba81d7586a702a'
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_bytes())

def members(root, entries):
    out=[]
    for z in entries:
        rel=Path(z['path'])
        assert not rel.is_absolute() and '..' not in rel.parts
        p=root/rel
        assert not p.is_symlink()
        b=p.read_bytes()
        assert len(b)==z['bytes'] and sha(b)==z['sha256'],str(p)
        if '.jsonl' in p.name:
            for line in b.splitlines():json.loads(line)
        elif '.json' in p.name:json.loads(b)
        out.append((z['path'],len(b),sha(b)))
    return out

def source_closure():
    m=load(SOURCE/'MANIFEST.json')
    actual=sorted(str(p.relative_to(SOURCE)) for p in SOURCE.rglob('*')
                  if p.is_file() and p!=SOURCE/'MANIFEST.json'
                  and 'tmp' not in p.relative_to(SOURCE).parts
                  and '__pycache__' not in p.relative_to(SOURCE).parts)
    assert actual==sorted(z['path'] for z in m['files'])
    return members(SOURCE,m['files'])

def candidate_closure():
    assert sha((C/'MANIFEST.json').read_bytes())==FROZEN
    m=load(C/'MANIFEST.json');d=load(C/'CURRENT_PROOF_DEPENDENCIES.json')
    assert d['base']=='../' and len(m['files'])==38 and len(d['files'])==235
    return members(C,m['files'])+members(P,d['files'])

def equivalent(obj, clock=False, traceback_paths=False):
    if isinstance(obj,dict):
        return {k:equivalent(v,clock,traceback_paths) for k,v in obj.items()
                if not (clock and k=='utc') and not (traceback_paths and k=='stderr_sha256')}
    if isinstance(obj,list):return [equivalent(v,clock,traceback_paths) for v in obj]
    return obj

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',type=Path,required=True,help='New empty directory under the audit parent tmp or this audit tmp')
    args=ap.parse_args();dest=args.output.expanduser().resolve()
    assert dest.is_relative_to((P/'tmp').resolve()) or dest.is_relative_to((SOURCE/'tmp').resolve()),'private output only'
    assert not dest.exists(),'use a new output directory'
    before=source_closure();candidate_before=candidate_closure()
    dest.mkdir(parents=True);copy=dest/'audit';copy.mkdir()
    for rel,_,_ in before:
        q=copy/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(SOURCE/rel,q)
    shutil.copyfile(SOURCE/'MANIFEST.json',copy/'MANIFEST.json')
    runs=[]
    for name in ['reproduce_historical_exact.py','verify_v2.py','reproduce_first_whole_controls.py']:
        proc=subprocess.run(['/usr/bin/python3',str(copy/name)],capture_output=True)
        run=dest/'runs'/name;run.mkdir(parents=True)
        (run/'stdout.txt').write_bytes(proc.stdout);(run/'stderr.txt').write_bytes(proc.stderr)
        rec={'program':name,'implementation_sha256':sha((copy/name).read_bytes()),
             'returncode':proc.returncode,'stdout_sha256':sha(proc.stdout),'stderr_sha256':sha(proc.stderr)}
        (run/'receipt.json').write_text(json.dumps(rec,indent=2)+'\n');runs.append(rec)
        assert proc.returncode==0 and not proc.stderr,rec
    comparisons={}
    for name,clock,tracebacks in [('REPRODUCTION_RESULTS.json',True,False),
                                  ('V2_VERIFICATION_RESULTS.json',True,True),
                                  ('FIRST_WHOLE_CONTROLS_REPLAY.json',False,False),
                                  ('HISTORICAL_ACTUAL_CONTROLS.json',False,True),
                                  ('READING_BINDING_LEDGER.json',False,False)]:
        assert equivalent(load(copy/name),clock,tracebacks)==equivalent(load(SOURCE/name),clock,tracebacks),name
        comparisons[name]=True
    assert load(copy/'HISTORICAL_ACTUAL_CONTROLS.json')['mandatory_administrative_failure']['mandatory'] is True
    assert source_closure()==before and candidate_closure()==candidate_before
    out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'closed_audit_manifest_sha256':sha((SOURCE/'MANIFEST.json').read_bytes()),
         'frozen_current_v2_manifest_sha256':FROZEN,'source_bindings_before_after':len(before),
         'current_bindings_before_after':len(candidate_before),'actual_private_runs':runs,
         'comparisons':comparisons,'historical_metadata_failure_still_recorded_as_failure':True,
         'scope':'Reproduction only; does not cure the disclosed source-first order failure or create an acceptance gate.'}
    (dest/'ROOT_REPLAY_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
