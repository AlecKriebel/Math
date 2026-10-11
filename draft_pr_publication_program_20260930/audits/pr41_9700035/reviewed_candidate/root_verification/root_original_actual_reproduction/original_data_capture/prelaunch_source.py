#!/usr/bin/env python3
"""Independent original-data audit. Does not execute/import submitted helpers."""
import argparse, ast, collections, datetime, hashlib, json, pathlib, sqlite3, subprocess

def digest(data):
    return hashlib.sha256(data).hexdigest()

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--repo',type=pathlib.Path,required=True); parser.add_argument('--output',type=pathlib.Path,required=True); args=parser.parse_args()
    repo=args.repo.resolve(); out=args.output.resolve(); out.mkdir(exist_ok=False)
    audit=repo/'draft_pr_publication_program_20260930/audits/pr41_9700035'; snap=audit/'source_snapshot'
    commands=[]
    def git(*argv):
        cmd=['git',*argv]; started=datetime.datetime.now(datetime.timezone.utc).isoformat()
        p=subprocess.run(cmd,cwd=repo,capture_output=True,timeout=90,env=None)
        index=len(commands); outputs={}
        for channel,data in [('stdout',p.stdout),('stderr',p.stderr)]:
            path=out/(str(index)+'.'+channel);path.write_bytes(data);outputs[channel]={'path':path.name,'size':len(data),'sha256':digest(data)}
        commands.append({'argv':cmd,'started_utc':started,'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':p.returncode,**outputs})
        (out/'GIT_COMMANDS.json').write_text(json.dumps(commands,indent=2)+'\n')
        if p.returncode:raise ValueError('Readonly Git command failed; full streams retained')
        return p.stdout
    manifest_bytes=(audit/'snapshot_manifest.json').read_bytes()
    assert digest(manifest_bytes)=='feef9bf6433c165296d3cdea883ceb74440048e17ff87f03ef636a99338cb3e6'
    manifest=json.loads(manifest_bytes);assert len(manifest['files'])==16 and len(manifest['changed_paths'])==17
    head=manifest['head'];base=manifest['base'];records=[];parsed={}
    for row in manifest['files']:
        data=(snap/row['path']).read_bytes();path=manifest['prefix']+row['path']
        assert type(row['size']) is int and len(data)==row['size'] and digest(data)==row['sha256']
        assert git('show',head+':'+path)==data
        assert git('ls-tree',head,'--',path).decode().strip()==row['mode']+' blob '+row['git_blob']+'\t'+path
        if row['path'].endswith('.json'):parsed[row['path']]=json.loads(data)
        if row['path'].endswith('.py'):ast.parse(data)
        records.append(row)
    patch=(audit/'pr_input/diff.patch').read_bytes();assert patch==git('diff',base,head)
    assert git('diff','--name-only',base,head).decode().splitlines()==manifest['changed_paths']
    metadata=json.loads((audit/'pr_input/metadata.json').read_bytes());assert metadata['number']==41 and metadata['headRefOid']==head and metadata['isDraft'] is True
    attempt=parsed['attempt.json'];turns=parsed['turns.json'];assert type(attempt['substantive_attempts_used']) is int and type(attempt['substantive_attempt_limit']) is int
    assert attempt['substantive_attempts_used']==len(turns)==2 and attempt['substantive_attempt_limit']==5
    assert [x['turn'] for x in turns]==[1,2] and all(type(x['turn']) is int for x in turns)
    assert attempt['full_original_resolution_claimed'] is False and attempt['novel_result_claimed'] is False
    assert attempt['proof_sha256']==digest((snap/'PROOF.md').read_bytes())==parsed['verification.json']['proof_sha256']
    for name,count in [('verification.json',211),('review/independent_results.json',3809)]:
        record=parsed[name];assert type(record['passed']) is int and record['passed']==len(record['checks'])==count
        assert type(record['failed']) is int and record['failed']==0 and all(type(v) is str and v=='PASS' for v in record['checks'].values())
    native=repo/'unsolved_math_prioritization';corpus=(native/'cache/problems.json').read_bytes();reports_bytes=(native/'cache/research_results.json').read_bytes()
    raw=json.loads(corpus);reports=json.loads(reports_bytes);pin=json.loads((native/'manifest.json').read_bytes())
    assert pin['files']['problems.json']=={'bytes':len(corpus),'sha256':digest(corpus)} and pin['files']['research_results.json']=={'bytes':len(reports_bytes),'sha256':digest(reports_bytes)}
    assert len(raw)==pin['records']==15458;byid={str(p['id']):p for p in raw};counts=collections.Counter(p['problem_number'] for p in raw)
    source=parsed['source_record.json'];prior=parsed['prior_report.json'];assert byid['9700035']==source and counts[source['problem_number']]==1
    assert source['problem_number'] in reports and reports[source['problem_number']]==prior and prior
    db=sqlite3.connect('file:'+str(native/'cache/catalog.sqlite')+'?mode=ro&immutable=1',uri=True);db.execute('PRAGMA query_only=ON');assert db.execute('PRAGMA query_only').fetchone()==(1,)
    assert db.execute('SELECT revision FROM metadata').fetchone()==(pin['revision'],)
    rows=db.execute('SELECT key,payload,report FROM records ORDER BY key').fetchall();assert len(rows)==15458
    for key,payload,report in rows:
        p=dict(byid[key]);code=p['problem_number']
        if counts[code]>1 and code in reports:p['_ambiguous_report']=True
        expected={} if p.get('_ambiguous_report') else reports.get(code,{})
        assert json.loads(payload)==p and json.loads(report)==expected
    db.close()
    absences=[]
    for ref in [base,head,'HEAD']:
        state=json.loads(git('show',ref+':unsolved_math_prioritization/state.json'))
        history=git('show',ref+':unsolved_math_prioritization/history.jsonl');events=[json.loads(x) for x in history.splitlines() if x]
        assert '9700035' not in state and not any(str(x.get('id'))=='9700035' for x in events)
        absences.append({'ref':ref,'state_entry_absent':True,'history_event_absent':True,'history_events':len(events),'history_sha256':digest(history)})
    result={'status':'PASS_READONLY_ORIGINAL_DATA','original16':records,'full17_path_diff_bytes':len(patch),'full_diff_sha256':digest(patch),'all_original_JSON_parsed':len(parsed),'proposal_helpers_AST_parsed_not_executed':True,'actual_prior_PRESENT_nonempty':True,'source_prior_whole_raw_snapshot_equal':True,'raw_corpus_bytes':len(corpus)+len(reports_bytes),'raw_problem_count':len(raw),'raw_report_count':len(reports),'all_SQL_rows_verified':len(rows),'SQL_configuration':'mode=ro&immutable=1; PRAGMA query_only=ON verified1','native_absence':absences,'original_substantive_attempts':2,'limit':5,'new_substantive_attempts':0,'audit_attempts_added':0,'scientific_theorem_or_original_verifier_replay_certified':False}
    (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='original16' and k!='native_absence'},indent=2))

if __name__=='__main__':main()
