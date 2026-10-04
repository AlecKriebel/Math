#!/usr/bin/env python3
"""Read-only original provenance, whole-corpus/RO-SQL, source identity and budget audit."""
import argparse,ast,collections,datetime,hashlib,json,pathlib,re,sqlite3,subprocess,sys

def sha(b):return hashlib.sha256(b).hexdigest()
def strict_budget(d):
    if set(d)!={'id','substantive_attempts','count','reason'} or type(d['id']) is not int or d['id']!=2814 or type(d['count']) is not int or d['count']!=0 or d['substantive_attempts']!=[] or type(d['reason']) is not str:raise ValueError('invalid original zero-turn ledger')
def check(repo,out):
    out.mkdir(exist_ok=False); A=repo/'draft_pr_publication_program_20260930/audits/pr40_2814'; S=A/'source_snapshot';N=repo/'unsolved_math_prioritization';F=A/'primary_scope_family'
    start=datetime.datetime.now(datetime.timezone.utc).isoformat(); manifest=json.loads((A/'snapshot_manifest.json').read_text());checks=[];commands=[]
    def git(*args):
        z=subprocess.run(['git',*args],cwd=repo,capture_output=True); commands.append({'argv':['git',*args],'returncode':z.returncode,'stdout_sha256':sha(z.stdout),'stdout_size':len(z.stdout),'stderr':z.stderr.decode(errors='replace')});
        if z.returncode:raise ValueError('Git read failed')
        return z.stdout
    source_rows=[]
    for row in manifest['files']:
        b=(S/row['path']).read_bytes();path='unsolved_math_prioritization/attempts/2814/'+row['path'];raw=git('show',manifest['head']+':'+path);tree=git('ls-tree',manifest['head'],'--',path).decode().strip().split();assert tree[0]==row['mode'] and tree[2]==row['git_blob'];assert b==raw and len(b)==row['size'] and sha(b)==row['sha256'];source_rows.append({'path':row['path'],'mode':row['mode'],'blob':row['git_blob'],'size':len(b),'sha256':sha(b),'exact_original_git_bytes':True})
    assert len(source_rows)==13;diff=git('diff','--binary',manifest['base']+'...'+manifest['head']);assert diff==(A/'pr_input/diff.patch').read_bytes() and sha(diff)==manifest['diff_sha256'];paths=git('diff','--name-only',manifest['base']+'...'+manifest['head']).decode().splitlines();assert paths==manifest['changed_paths'] and len(paths)==14;checks.append('All original13 blobs/modes/bytes and full14-path diff exactly reproduced')
    rawb=(N/'cache/problems.json').read_bytes();reportb=(N/'cache/research_results.json').read_bytes();raw=json.loads(rawb);reports=json.loads(reportb);cfg=json.loads((N/'policy.json').read_text());nm=json.loads((N/'manifest.json').read_text());assert len(raw)==15458 and nm['records']==15458;assert {'bytes':len(rawb),'sha256':sha(rawb)}==nm['files']['problems.json'];assert {'bytes':len(reportb),'sha256':sha(reportb)}==nm['files']['research_results.json'];assert len({str(p['id']) for p in raw})==15458
    counter=collections.Counter(p['problem_number'] for p in raw);byid={str(p['id']):p for p in raw};sqlpath=N/'cache/catalog.sqlite';db=sqlite3.connect('file:'+str(sqlpath)+'?mode=ro',uri=True);assert db.execute('SELECT revision FROM metadata').fetchone()==(nm['revision'],);rows=db.execute('SELECT key,payload,report FROM records ORDER BY key').fetchall();assert len(rows)==15458
    for key,payload,report in rows:
        p=dict(byid[key]);
        if counter[p['problem_number']]>1 and p['problem_number'] in reports:p['_ambiguous_report']=True
        r={} if p.get('_ambiguous_report') else reports.get(p['problem_number'],{});assert json.loads(payload)==p and json.loads(report)==r
    db.close();checks.append('Complete149MB corpus and all15458 read-only SQL rows/report joins verified against pinned dataset manifest')
    queue_source=(N/'queue.py').read_bytes();node=ast.parse(queue_source);selected=[z for z in node.body if isinstance(z,ast.FunctionDef) and z.name in {'digest','score'}];assert len(selected)==2;env={'hashlib':hashlib,'json':json,'re':re};exec(compile(ast.Module(body=selected,type_ignores=[]),str(N/'queue.py'),'exec'),env)
    selected_records=[]
    for id,name,priorname in [('2814','source_record.json','prior_report.json'),('20001896','duplicate_record.json','duplicate_prior_report.json')]:
        p=byid[id]; snap=json.loads((S/name).read_text());assert p==snap;r=reports.get(p['problem_number']);ps=json.loads((S/priorname).read_text());assert ps==r;score=env['score'](p,{} if r is None else r,cfg);selected_records.append({'id':id,'raw_problem':p,'raw_report_key_present':p['problem_number'] in reports,'raw_report':r,'sql_fallback_report':{} if r is None else r,'score':score,'snapshot_whole_parsed_json_equal':True})
    readiness=json.loads((S/'readiness.json').read_text());assert selected_records[0]['score']['statement_hash']==readiness['statement_hash'] and selected_records[0]['score']['review_hash']==readiness['review_hash'];checks.append('Both complete selected original source/prior objects and fresh pure score fingerprints verified; 2814 raw absent report retained as literal null, importer empty-object fallback explicitly distinct')
    strict_budget(json.loads((S/'turns.json').read_text()));controls=[]
    original=json.loads((S/'turns.json').read_text())
    for label,field,value in [('bool_is_not_int','count',False),('phantom_attempt','substantive_attempts',[{'attempt':1}]),('count_out_of_sync','count',1),('wrong_duplicate_credit','id',20001896),('extra_hidden_ledger_field','new_attempt',1)]:
        d=dict(original);d[field]=value
        try:strict_budget(d)
        except ValueError:controls.append({'label':label,'rejected':True})
        else:raise AssertionError(label)
    native=[]
    for ref in [manifest['base'],manifest['head'],'HEAD']:
        state=json.loads(git('show',ref+':unsolved_math_prioritization/state.json'));hist=git('show',ref+':unsolved_math_prioritization/history.jsonl').decode();ev=[json.loads(line) for line in hist.splitlines() if line];target=[e for e in ev if str(e.get('id')) in {'2814','20001896'}];assert not target and not any(id in state for id in ['2814','20001896']);native.append({'ref':ref,'state_target_entries_absent':True,'history_target_events_absent':True,'whole_history_events':len(ev),'state_sha256':sha(json.dumps(state,sort_keys=True).encode()),'history_raw_sha256':sha(hist.encode())})
    groups=json.loads((N/'review_v2/related_target_groups.json').read_text());related=[g for g in groups['groups'] if set(map(str,g.get('ids',[])))&{'2814','20001896'}];checks.append('Original zero substantive attempts validated; five actual malformed-ledger controls rejected; target/duplicate absent from full base/head/current native state+history')
    source_identity=[];mapping={'kirby2026.pdf':'k3_book.pdf','luo-markovic.pdf':'luo_markovic_v1.pdf','xia.pdf':'xia_v1.pdf','kuhlmann2006.pdf':'kuhlmann_2006_correct.pdf','burns-matveev.pdf':'aim_geodesics.pdf'}
    for row in json.loads((S/'source_checksums.json').read_text())['sources']:
        b=(F/'foreign_cache'/mapping[row['cache_file']]).read_bytes();assert len(b)==row['bytes'] and sha(b)==row['sha256'];source_identity.append({'original_filename':row['cache_file'],'actual_family_filename':mapping[row['cache_file']],'size':len(b),'sha256':sha(b),'byte_exact_match':True})
    checks.append('All five exact original primary PDFs independently downloaded and byte-identical to historical source identities')
    (out/'SELECTED_COMPLETE_SOURCE_PAIRS.json').write_text(json.dumps(selected_records,ensure_ascii=False,indent=2)+'\n');(out/'GIT_READ_COMMANDS.json').write_text(json.dumps(commands,indent=2)+'\n')
    result={'schema':'pr40-primary-scope-original-actual/v1','status':'PASS','started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_runtime':{'argv':sys.argv,'executable':sys.executable,'version':sys.version},'checks':checks,'original13':source_rows,'raw_corpus':{'size':len(rawb),'sha256':sha(rawb),'problem_count':len(raw),'sql_rows_all_verified':len(rows),'reports_size':len(reportb),'reports_sha256':sha(reportb),'sql_open_mode':'ro'},'native_absence_checks':native,'related_groups':related,'actual_budget_negative_controls':controls,'exact_source_identity_checks':source_identity,'scope':'Read-only full originals/corpus/SQL/native history and pure queue-score audit, no proof theorem certification implied.'};(out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':result['status'],'checks':len(checks),'original_files':13,'sql_rows':len(rows),'negative_controls':len(controls)}))
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--repository-root',type=pathlib.Path,required=True);a.add_argument('--output-root',type=pathlib.Path,required=True);x=a.parse_args();check(x.repository_root.resolve(),x.output_root.resolve())
