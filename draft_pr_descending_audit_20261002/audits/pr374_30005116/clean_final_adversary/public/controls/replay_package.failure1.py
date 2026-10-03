#!/usr/bin/env python3
"""Replay unchanged author/history/wrapper in private copies, preserving every stream."""
import argparse,datetime,hashlib,json,os,pathlib,shutil,subprocess,sys,time

def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--snapshot',required=True);parser.add_argument('--own',required=True)
    parser.add_argument('--stdlib',default=sys.executable)
    parser.add_argument('--sympy',default='/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr378_30004322/sources_effective_review/private_runtime/bin/python')
    args=parser.parse_args();own=pathlib.Path(args.own);source=pathlib.Path(args.snapshot)/'problems/30005116_induced_four_cycle_profile'
    private=own/'private'/'replay_packet';private.mkdir(parents=True,exist_ok=True)
    logs=own/'public'/'logs';logs.mkdir(parents=True,exist_ok=True)
    for path in source.rglob('*'):
        if path.is_file():
            relative=path.relative_to(source);target=private/relative;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,target)
    files={str(p.relative_to(private)):sha(p.read_bytes()) for p in private.rglob('*') if p.is_file() and '__pycache__' not in str(p)}
    assert len(files)==45
    env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1';env['TMPDIR']=str(own/'private'/'wrapper_tmp');pathlib.Path(env['TMPDIR']).mkdir(exist_ok=True)
    records=[]
    def run(label,argv,cwd,expected=None,json_expected=None):
        started=datetime.datetime.now(datetime.timezone.utc).isoformat();before=time.monotonic()
        result=subprocess.run(argv,cwd=cwd,env=env,capture_output=True)
        (logs/(label+'.stdout')).write_bytes(result.stdout);(logs/(label+'.stderr')).write_bytes(result.stderr)
        record={'label':label,'started_utc':started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':round(time.monotonic()-before,6),'returncode':result.returncode,'stdout_sha256':sha(result.stdout),'stderr_sha256':sha(result.stderr),'stdout_bytes':len(result.stdout),'stderr_bytes':len(result.stderr)}
        records.append(record)
        assert result.returncode==0,(label,result.stderr.decode())
        assert result.stderr==b'',(label,'nonempty stderr')
        if expected is not None:
            assert result.stdout==expected,(label,'whole stream bytes differ')
            record['complete_stdout_byte_match']=True
        if json_expected is not None:
            assert json.loads(result.stdout)==json_expected,(label,'whole JSON differs')
            record['whole_json_match']=True
        return result.stdout
    assertions=0
    for i in range(1,6):
        expected=(private/f'TURN_{i}_CHECKS.json').read_bytes()
        out=run(f'author_turn{i}',[args.stdlib,str(private/f'verify_turn{i}.py')],private,expected,json.loads(expected));assertions+=json.loads(out)['assertions']
    assert assertions==93505
    R=private/'independent_review'
    expected=(R/'AUTHOR_REPLAY.json').read_bytes()
    run('historical_author_replay',[args.stdlib,str(R/'replay_author.py'),str(private)],private,expected,json.loads(expected))
    expected=(R/'INDEPENDENT_CHECKS.json').read_bytes()
    run('historical_independent',[args.sympy,str(R/'independent_check.py')],R,expected,json.loads(expected))
    assert json.loads(expected)['independent_assertions']==1080
    run('portable_publication',[args.sympy,str(private/'verify_publication.py')],private,b'PASS: immutable publication hashes, exact author replay and independent SymPy-backed replay\n')
    after={str(p.relative_to(private)):sha(p.read_bytes()) for p in private.rglob('*') if p.is_file() and '__pycache__' not in str(p)}
    assert after==files,'private packet bytes modified by verification'
    receipt={'status':'PASS','author_assertions':assertions,'historical_independent_assertions':1080,'private_packet_files':45,'packet_unchanged':True,'records':records,'volatile_fields':['records[*].started_utc','records[*].finished_utc','records[*].elapsed_seconds'],'no_other_output_or_JSON_differences_allowed':True,'sympy_runtime_invoked_literal':args.sympy,'scope':'Whole stored author/history receipts and portable wrapper, no raw-source retrieval by wrapper.'}
    (own/'public'/'package_replay_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({k:v for k,v in receipt.items() if k not in ('records','sympy_runtime_invoked_literal')},sort_keys=True))

if __name__=='__main__':main()
