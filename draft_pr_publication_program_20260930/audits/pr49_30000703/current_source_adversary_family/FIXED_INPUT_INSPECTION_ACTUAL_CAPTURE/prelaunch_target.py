"""Independent current SOURCE inspection. No production/helper execution or imports."""
from pathlib import Path, PurePosixPath
import datetime as dt, hashlib, json, math, os, re, stat
R=Path('/Users/alec/Documents/Math'); A=R/'draft_pr_publication_program_20260930/audits/pr49_30000703'; S=A/'current_preparation_family'; F=Path(__file__).absolute().parent
H='036a5ed59bee5ed79f08349290481584610f1456'; B='c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
PM='4324c2a69762752b42b159b141a629b55a6dda5351817afff12e4f2d0950e4cd'
checked={}; nodes=0
def need(x,n):
    if not x:raise ValueError(n)
def digest(b):return hashlib.sha256(b).hexdigest()
def load(b):
    def pairs(p):
        d={}
        for k,v in p:need(k not in d,'duplicate key');d[k]=v
        return d
    def floatnum(s):
        v=float(s);need(math.isfinite(v),'nonfinite float');return v
    def const(s):raise ValueError('nonfinite constant')
    return json.loads(b,object_pairs_hook=pairs,parse_float=floatnum,parse_constant=const)
def canonical(v):return json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)
def walk(v):
    global nodes
    nodes+=1
    if isinstance(v,dict):
        for k,w in v.items():need(type(k) is str,'key');walk(w)
    elif isinstance(v,list):
        for w in v:walk(w)
    else:need(v is None or type(v) in (str,bool,int,float),'JSON scalar')
def relative(n):
    need(type(n) is str and n and '\\' not in n and '\0' not in n,'path text');p=PurePosixPath(n)
    need(not p.is_absolute() and str(p)==n and not set(p.parts)&{'.','..','.git','__pycache__'},'canonical relative');return n
def raw(p):
    need(not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode),'regular file');return p.read_bytes()
def row(p):
    b=raw(p);return dict(path=p.relative_to(R).as_posix(),bytes=len(b),sha256=digest(b),full_mode=stat.S_IMODE(p.stat().st_mode))
def binding(v,mode=True):
    need(type(v) is dict and set(v)=={'path','bytes','sha256','full_mode'},'four row');relative(v['path']);need(type(v['bytes']) is int and v['bytes']>=0 and type(v['full_mode']) is int and 0<=v['full_mode']<4096 and type(v['sha256']) is str and re.fullmatch('[0-9a-f]{64}',v['sha256']),'typed row')
    p=R/v['path'];b=raw(p);actual=row(p);need(all(actual[k]==v[k] for k in ('path','bytes','sha256')) and (not mode or actual['full_mode']==v['full_mode']),'body/mode binding')
    checked[v['path']]=actual;return b
def structured(n,b):
    if n.endswith('.json'):v=load(b);walk(v)
    elif n.endswith('.jsonl'):
        try:v=load(b);walk(v)
        except (json.JSONDecodeError,UnicodeDecodeError):
            need(b==b'' or b.strip(),'whitespace JSONL')
            for line in b.splitlines():need(line.strip(),'blank JSONL row');walk(load(line))
def tree(root):
    need(root.is_dir() and not root.is_symlink() and all(not p.is_symlink() for p in root.parents),'regular directory')
    files=set();dirs={'.':stat.S_IMODE(root.stat().st_mode)}
    for p in root.rglob('*'):
        need(not p.is_symlink(),'symlink');n=relative(p.relative_to(root).as_posix());m=p.stat().st_mode
        if stat.S_ISREG(m):files.add(n)
        else:need(stat.S_ISDIR(m),'special');dirs[n]=stat.S_IMODE(m)
    ancestors={'.'}|{str(p) for n in files for p in PurePosixPath(n).parents if str(p)!='.'};need(set(dirs)==ancestors,'empty/extra directories');return files,dirs
def utc(s):
    need(type(s) is str,'UTC text');v=dt.datetime.fromisoformat(s);need(v.utcoffset()==dt.timedelta(0),'aware UTC');return v
def cap4(directory,pid,argv):
    need({p.name for p in directory.iterdir()}=={'CAPTURE.json','stdout.bin','stderr.bin','prelaunch_operator.py'},'exact CAP4')
    c=load(raw(directory/'CAPTURE.json'));walk(c);need(c['schema']=='root-explicit-command-capture/v1' and c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']==pid and type(c['exit_code']) is int and c['exit_code']==0 and c['stdin_supplied'] is False and c['operator_unchanged'] is True and c['argv']==argv and c['cwd']==str(R),'actual CAP4 identity')
    need(utc(c['started_utc'])<utc(c['finished_utc'])<=dt.datetime.now(dt.timezone.utc),'chronology');need(digest(raw(directory/'prelaunch_operator.py'))==c['operator_sha256'],'genuine captured operator source')
    for k in ('stdout','stderr'):
        x=c[k];need(set(x)=={'path','bytes','sha256'} and type(x['bytes']) is int and x['bytes']>=0 and x['path']==k+'.bin','split stream');b=raw(directory/x['path']);need(len(b)==x['bytes'] and digest(b)==x['sha256'],'complete stream')
    need(c['stderr']['bytes']==0,'success stderr');out=load(raw(directory/'stdout.bin'));walk(out)
    for p in directory.iterdir():checked[p.relative_to(R).as_posix()]=row(p)
    return c,out
def main():
    need(not (A/'reviewed_candidate').exists() and not (A/'reviewed_candidate').is_symlink(),'future candidate absent')
    prerequisites=['ROOT_CURRENT_KNOWN_RESULT_SCOPE_CERTIFICATE.md','ROOT_PRIMARY_READ_LEDGER.json','ROOT_SCIENCE_CARD.json','ROOT_CURRENT_INPUT_PREIMAGES.json','ROOT_EVIDENCE_BINDINGS.json']
    need(all(not (A/n).exists() and not (A/n).is_symlink() for n in prerequisites),'ROOT genuine five still absent')
    prep=load(raw(S/'PREPARATION_MANIFEST.json'));need(digest(raw(S/'PREPARATION_MANIFEST.json'))==PM and prep['schema']=='pr49-current-source-only-closure/v1' and type(prep['files_count']) is int and prep['files_count']==119 and prep['self_excluded']==['PREPARATION_MANIFEST.json'] and prep['SOURCE_adversary_verdict'] is None and prep['future_acceptance_approved'] is False,'SOURCE exact closure')
    files,dirs=tree(S);need(files=={v['path'] for v in prep['files']}|{'PREPARATION_MANIFEST.json'} and len(prep['files'])==119 and dirs=={v['path']:v['full_mode'] for v in prep['directories']} and len(prep['directories'])==19,'SOURCE exact topology')
    for v in prep['files']:
        need(v['full_mode']==292,'full0444');b=binding(dict(v,path=S.relative_to(R).as_posix()+'/'+v['path']));structured(v['path'],b)
    need(stat.S_IMODE((S/'PREPARATION_MANIFEST.json').stat().st_mode)==292,'SOURCE self0444');checked[(S/'PREPARATION_MANIFEST.json').relative_to(R).as_posix()]=row(S/'PREPARATION_MANIFEST.json')
    pins=load(raw(S/'STATIC_INPUT_BINDINGS.json'));need(pins['schema']=='pr49-fixed-current-source-inputs/v1' and len(pins['fixed_rows'])==1184 and pins['exact_literal_structured_exceptions']==[] and pins['future_acceptance_approved'] is False,'fixed SOURCE schema')
    names=set()
    for v in pins['fixed_rows']:need(v['path'] not in names,'duplicate fixed row');names.add(v['path']);b=binding(v);structured(v['path'],b)
    closure_counts={}
    for key,info in pins['closed_inputs'].items():
        m=load(binding(info['manifest']));walk(m);root=R/info['root'];need(m['schema']==info['schema'],'distinct actual schemas')
        if key=='original':
            need(m['files_count']==350 and m['self_excluded']==[info['self_name']],'original350');payload=m['files'];owned=set(info['authorship_root_files']);mdirs={'.':m['authorship_root_full_mode'],**{d['path']:d['full_mode'] for d in m['owned_directory_bindings']}}
            for sub in info['authorship_directory_roots']:
                sf,sd=tree(root/sub);owned|={sub+'/'+n for n in sf}
            need(m['authorship_root_files']==info['authorship_root_files'] and m['authorship_directory_roots']==info['authorship_directory_roots'],'scope exact')
        elif key=='boundary':
            need(m['member_count']==473 and m['self_excluded']==[info['self_name']],'boundary473');payload=m['members'];owned=tree(root)[0]-{info['self_name']};mdirs={d['path']:d['full_mode'] for d in m['directories']}
        elif key=='hyperbolic':
            need(m['manifest_self']['path']==info['self_name'] and m['manifest_self']['mode']=='0444' and len(m['payload_files'])==107,'hyper107');payload=[dict(path=v['path'],bytes=v['bytes'],sha256=v['sha256'],full_mode=int(v['mode'],8)) for v in m['payload_files']];need(all(v['mode']=='0444' for v in m['payload_files']),'mode strings exact');owned=tree(root)[0]-{info['self_name']};mdirs={'.':stat.S_IMODE(root.stat().st_mode),**{d['path']:int(d['mode'],8) for d in m['directories']}}
        else:
            need(key=='ROOT' and m['files_count']==192 and m['self_excluded']==[info['self_name']],'ROOT192');payload=m['files'];owned=tree(root)[0]-{info['self_name']};mdirs={'.':stat.S_IMODE(root.stat().st_mode),**{d['path']:d['full_mode'] for d in m['directories']}}
        normalized=[dict(v,path=info['root']+'/'+v['path']) for v in payload];need(canonical(sorted(normalized,key=lambda v:v['path']))==canonical(sorted(info['members'],key=lambda v:v['path'])) and len(payload)==info['payload_count'],'complete normalized rows')
        need(owned=={v['path'] for v in payload} and mdirs=={v['path']:v['full_mode'] for v in info['directories']},'full scoped topology+schema mode normalization')
        for n,mode in mdirs.items():need(stat.S_IMODE((root/n).stat().st_mode)==mode,'directory mode')
        closure_counts[key]={'payload':len(payload),'directories_including_root':len(mdirs),'schema':m['schema']}
    snap=load(raw(A/'snapshot_manifest.json'));need(snap['head']==H and snap['github_base']==B and snap['merge_base']==B and snap['original_files']==16,'original metadata')
    science={v['relative_path']:raw(A/'source_snapshot'/v['relative_path']) for v in snap['files']};need(set(science)=={p.relative_to(S/'original_archive').as_posix() for p in (S/'original_archive').rglob('*') if p.is_file()},'all16 archive')
    for n,b in science.items():need(raw(S/'original_archive'/n)==b,'all archive exact')
    immutable=['SOURCE_STATUS.md','verify.py','verification.json','source_record.json','prior_report.json','turns.json','source_checksums.json','review/submitted_verify.py','review/verification.json','review/independent_checks.py','review/independent_results.json']
    for n in immutable:need(raw(S/'operative_proposal'/n)==science[n],'operative11 exact')
    need(science['prior_report.json']==b'null\n','literal marker');sr=load(science['source_record.json']);need(type(sr['id']) is int and sr['id']==30000703,'plain original integer ID');turns=load(science['turns.json']);need(type(turns) is dict and type(turns['count']) is int and turns['count']==0 and turns['substantive_attempts']==[] and 'source_verification_response' not in turns,'object turns0 no invented response')
    t=A/'root_original_actual_reproduction';repro=load(raw(t/'ROOT_REPRODUCTION_RESULT.json'));walk(repro);need(repro['actual_operator_pid']==60012 and len(repro['complete_actual_Git_captures'])==33 and len(repro['complete_actual_helper_captures'])==3,'literal ROOT33+3')
    replay_receipts={}
    for c in repro['complete_actual_Git_captures']+repro['complete_actual_helper_captures']:
        need(c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']>0 and type(c['exit_code']) is int and c['exit_code']==0 and c['stdin_supplied'] is False and c['operator_unchanged'] is True and c['operator_pid']==60012 and c['cwd']==str(R),'actual typed old capture');need(utc(c['started_utc'])<=utc(c['finished_utc'])<utc(repro['created_utc']),'old chronology')
        for channel in ('stdout','stderr'):need(c[channel]['full_mode']==420,'historical420');binding(c[channel],mode=False);need(checked[c[channel]['path']]['full_mode']==292,'separate current292')
        need(c['stderr']['bytes']==0,'old success stderr');directory=(R/c['stdout']['path']).parent;need(canonical(load(raw(directory/'CAPTURE.json')))==canonical(c),'literal capture object');pre=load(raw(directory/'PRELAUNCH.json'));need(all(c[k]==v for k,v in pre.items() if k not in ('schema','actual_execution','completed','pid','exit_code','source_unchanged')),'genuine old prelaunch fixed values');need(digest(raw(directory/'PRELAUNCH_OPERATOR.py'))==c['operator_sha256'],'old captured operator')
        if c['schema']=='pr49-root-actual-readonly-git/v1':need(c['source'] is None and c['source_unchanged'] is None and c['argv'][0]=='git' and c['argv'][1] in ('show','ls-tree','diff','merge-base'),'Git null-null')
        else:
            need(c['schema']=='pr49-root-actual-unchanged-helper/v1' and c['source_unchanged'] is True and c['source']['full_mode']==420 and c['argv']==['/usr/bin/python3','-B',str(R/c['source']['path'])],'typed helper source');b=binding(c['source'],mode=False);need(b==raw(directory/'PRELAUNCH_TARGET.py'),'literal unchanged source')
    for k,n,count in [('author','private_author/verification.json',69),('identical_submitted','private_identical_submitted/verification.json',69),('historical_independent','private_historical_independent/independent_results.json',187)]:
        p=t/n;v=load(raw(p));need(type(v['passed']) is int and v['passed']==count and type(v['failed']) is int and v['failed']==0 and v['sympy_version']=='1.14.0' and len(v['checks'])==count and set(v['checks'].values())=={'PASS'} and canonical(v)==canonical(repro['entire_replayed_results'][k]),'full saved receipt object/types');replay_receipts[k]=row(p)
    need(raw(t/'private_author/verification.json')==science['verification.json'] and raw(t/'private_identical_submitted/verification.json')==science['review/verification.json'] and raw(t/'private_historical_independent/independent_results.json')==science['review/independent_results.json'] and repro['identical_submitted_counted_independent'] is False,'saved entire bytes and duplicate qualification')
    raw_audit=load(raw(A/'ROOT_COMPLETE_RAW_SQL_AUDIT.json'));walk(raw_audit);original=load(raw(A/'ORIGINAL_COMPLETE_RAW_SQL_READ.json'));walk(original);need(raw_audit['actual_pid']==62744 and raw_audit['all_SQL_rows']==15458 and raw_audit['full_raw_and_prior_bytes']==149266659 and raw_audit['selected_prior_key_present'] is False and raw_audit['raw_null_present'] is False and raw_audit['selected_prior_fallback']=={} and raw_audit['SQLite_literal_fallback']=='{}' and raw_audit['literal_original_prior_file_value'] is None and raw_audit['raw_or_SQL_or_foreign_source_bodies_copied'] is False,'absence/fallback/null metadata')
    origrows=original['rows'];left={v['key']:v for v in origrows};right={v['key']:v for v in raw_audit['complete_row_bindings']};need(len(left)==len(origrows)==len(right)==len(raw_audit['complete_row_bindings'])==15458 and set(left)==set(right),'all unique literal row metadata')
    for k,v in right.items():
        need(v['literal_importer_payload_byte_equal'] is True and v['literal_importer_report_byte_equal'] is True and v['complete_payload_recursive_type_equal'] is True and v['complete_report_recursive_type_equal'] is True and left[k]['literal_importer_payload_equal'] is True and left[k]['literal_importer_report_equal'] is True and left[k]['recursive_scalar_types_equal'] is True and v['payload_sha256']==left[k]['payload_utf8_sha256'] and v['report_sha256']==left[k]['report_utf8_sha256'] and type(v['prior_key_present']) is bool,'each exact derived row');need(re.fullmatch('[0-9a-f]{64}',v['payload_sha256']) and re.fullmatch('[0-9a-f]{64}',v['report_sha256']),'typed SHA metadata')
    a45=R/'draft_pr_publication_program_20260930/audits/pr45_9900007';c,out=cap4(a45/'root_pr49_current_source_closure_actual_capture',1200,['/usr/bin/python3','-B',str(S/'close_source_preparation.py'),'--expected-report-sha256','40b49e6a3c5c26cc7da6afc297b36c2402e727487a42d81b6630f18e15a0411b']);d,read=cap4(a45/'root_pr49_current_source_closed_readback_actual_capture',1444,['/usr/bin/python3','-B',str(S/'verify_source_preparation_readonly.py'),'--expected-manifest-sha256',PM]);need(out['manifest_sha256']==read['manifest_sha256']==PM and out['actual_closing_pid']==read['actual_closing_pid']==prep['actual_closing_pid']==1200 and read['actual_readback_pid']==1444 and utc(c['started_utc'])<=utc(prep['created_utc'])<=utc(c['finished_utc'])<utc(d['started_utc']),'genuine separate SOURCE closure chronology')
    for name in ['DRAFT_ROOT_PRIMARY_READ_LEDGER.json','DRAFT_ROOT_SCIENCE_CARD.json','DRAFT_ROOT_EVIDENCE_BINDINGS.json','DRAFT_ROOT_NEW_SOURCE_ADVERSARY_RECORD.json','DRAFT_ROOT_CURRENT_INPUT_PREIMAGES.json']:
        x=load(raw(S/name));need(x['approved_by_root'] is False and x['created_utc'] is None,'false/null drafts')
    result=dict(schema='pr49-current-source-adversary-fixed-read/v1',status='PASS_COMPLETE_CURRENT_SOURCE_AND_FIXED_FIRST_PARTY_INSPECTION',actual_pid=os.getpid(),created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),source_files=119,fixed_files=1184,closure_counts=closure_counts,read_json_nodes=nodes,checked_body_mode_rows=sorted(checked.values(),key=lambda v:v['path']),derived_raw_metadata_rows_read=15458,full_raw_importer_rerun_this_task=False,ROOT_raw_child_attributed=62744,historical_capture_modes=420,current_closed_modes=292,ROOT_33_Git_3_helper_captures_read=True,replayed_receipts=replay_receipts,helpers_executed_this_task=False,production_imported_compiled_executed=False,source_original_response_count=None,original_substantive_attempts=0,new_substantive_attempts=0,audit_turns=0,future_acceptance_approved=False,genuine_ROOT_five_absent=prerequisites,reviewed_candidate_absent=True,SOURCE_manifest=row(S/'PREPARATION_MANIFEST.json'),source_closure_capture=row(a45/'root_pr49_current_source_closure_actual_capture/CAPTURE.json'),source_readback_capture=row(a45/'root_pr49_current_source_closed_readback_actual_capture/CAPTURE.json'))
    with (F/'FIXED_READ_RESULT.json').open('xb') as f:f.write((json.dumps(result,indent=2,allow_nan=False)+'\n').encode())
    print(json.dumps({k:v for k,v in result.items() if k not in ('checked_body_mode_rows','replayed_receipts')},sort_keys=True))
if __name__=='__main__':main()
