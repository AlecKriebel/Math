"""Private independent contract checks; never import/compile/run production or helpers."""
import copy, ctypes, datetime as dt, hashlib, json, math, os, re, stat, sys
from pathlib import Path, PurePosixPath
F=Path(__file__).absolute().parent;A=F.parent;S=A/'current_preparation_family';R=A.parents[2]
HEAD='e2e5c8c3e5ad218f867fa753c465bb96b3687bda';BASE='c6975ca76f9f667f1250ba403d0e6da2aafe14d0';MERGE='60292bed09f59236aa192cb17aa138f7b4750e1a'
labels=[];fullreads={};nodes={};optional=[]
def need(v,m):
    if not v:raise ValueError(m)
def check(v,m):need(v,m);labels.append(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def equal(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return set(a)==set(b) and all(equal(a[k],b[k]) for k in a)
    if type(a) is list:return len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b))
    return a==b
def regular(p):
    need(not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode),'Regular nonsymlink');b=p.read_bytes();rr={'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b),'full_mode':stat.S_IMODE(p.stat().st_mode)}
    need(rr['path'] not in fullreads or fullreads[rr['path']]==rr,'Repeated fixed body unchanged');fullreads[rr['path']]=rr;return b
def relative(s):
    need(type(s) is str and s and '\\' not in s and '\0' not in s,'Canonical text');p=PurePosixPath(s);need(not p.is_absolute() and str(p)==s and not {'.','..','.git','__pycache__'}.intersection(p.parts),'Canonical safe path');return s
def row(r,mode=False):
    need(type(r) is dict and set(r)==({'path','bytes','sha256','full_mode'} if mode else {'path','bytes','sha256'}),'Exact typed row');relative(r['path']);need(type(r['bytes']) is int and r['bytes']>=0 and type(r['sha256']) is str and re.fullmatch('[0-9a-f]{64}',r['sha256']),'Typed bytes/SHA')
    if mode:need(type(r['full_mode']) is int and 0<=r['full_mode']<4096,'Typed full mode')
def readrow(r):
    row(r,'full_mode' in r);p=R/r['path'];b=regular(p);need(len(b)==r['bytes'] and sha(b)==r['sha256'] and ('full_mode' not in r or stat.S_IMODE(p.stat().st_mode)==r['full_mode']),'Exact complete row body/full mode');return b
def inventory(root):
    need(root.is_dir() and not root.is_symlink() and all(not p.is_symlink() for p in root.parents),'Regular directory');fs=set();ds=set()
    for p in root.rglob('*'):
        need(not p.is_symlink(),'No symlink member');n=relative(p.relative_to(root).as_posix())
        if stat.S_ISREG(p.stat().st_mode):fs.add(n)
        else:need(stat.S_ISDIR(p.stat().st_mode),'No special member');ds.add(n)
    need(ds=={q.as_posix() for n in fs for q in PurePosixPath(n).parents if str(q)!='.'},'No extra/empty directories');return fs,ds
def load(b):
    def pairs(items):
        out={}
        for k,v in items:need(k not in out,'Duplicate JSON key');out[k]=v
        return out
    def constant(s):raise ValueError('Nonfinite constant '+s)
    def floating(s):
        n=float(s);need(math.isfinite(n),'Nonfinite float');return n
    return json.loads(b,object_pairs_hook=pairs,parse_constant=constant,parse_float=floating)
def inspectnodes(o):
    n=type(o).__name__;nodes[n]=nodes.get(n,0)+1
    if type(o) is dict:
        need(all(type(k) is str for k in o),'JSON text keys')
        for v in o.values():inspectnodes(v)
    elif type(o) is list:
        for v in o:inspectnodes(v)
    else:need(o is None or type(o) in [bool,int,str,float],'JSON scalar type')
def structured(n,b):
    if n.endswith('.json'):inspectnodes(load(b))
    elif n.endswith('.jsonl'):
        try:inspectnodes(load(b))
        except (json.JSONDecodeError,UnicodeDecodeError):
            need(bool(b.strip()),'Nonempty JSONL')
            for line in b.splitlines():need(bool(line.strip()),'No blank JSONL');inspectnodes(load(line))
def clock(t):
    need(type(t) is str,'Typed time');x=dt.datetime.fromisoformat(t.replace('Z','+00:00'));need(x.tzinfo is not None and x.utcoffset()==dt.timedelta(0),'AwareUTC');return x
def reject(fn,name):
    try:fn()
    except (ValueError,KeyError,TypeError,OSError,UnicodeDecodeError):labels.append('Reject '+name);return
    raise ValueError('Not rejected: '+name)
def capture(c,kind):
    need(type(c) is dict and c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']>0 and type(c['exit_code']) is int and c['exit_code']==0 and c['stdin_supplied'] is False and type(c['actual_operator_pid']) is int and c['actual_operator_pid']==11716 and c['cwd']==str(R) and c['operator_unchanged'] is True and clock(c['started_utc'])<=clock(c['finished_utc'])<=dt.datetime.now(dt.timezone.utc),'Actual successful typed ROOT capture')
    if c['schema']=='pr48-root-unchanged-helper-actual-capture/v1':
        need(type(c['source']) is dict and c['source_unchanged'] is True and c['argv']==['/usr/bin/python3','-B',str(R/c['source']['path'])],'Typed unchanged exact helper argv');readrow(c['source'])
    else:need(c['schema']=='pr48-root-readonly-git-actual-capture/v1' and c['source'] is None and c['source_unchanged'] is None and type(c['argv']) is list and len(c['argv'])>=2 and c['argv'][0]=='git' and c['argv'][1] in {'show','ls-tree','diff','merge-base'},'Genuine readonly null source convention')
    for k in ['stdout','stderr']:readrow(c[k])
    need(c['stderr']['bytes']==0,'Full successful empty stderr')
def rename_absent(src,dst):
    need(sys.platform=='darwin','macOS exclusive rename');lib=ctypes.CDLL(None,use_errno=True);fn=lib.renamex_np;fn.argtypes=[ctypes.c_char_p,ctypes.c_char_p,ctypes.c_uint];fn.restype=ctypes.c_int
    if fn(os.fsencode(src),os.fsencode(dst),4)!=0:n=ctypes.get_errno();raise OSError(n,os.strerror(n),str(dst))
def main():
    check(__debug__ and not sys.flags.optimize and os.environ.get('PYTHONOPTIMIZE','') in ('','0'),'No optimization')
    sb=regular(S/'prepare_current_packet.py');op=regular(S/'capture_root_builder_operation.py');check(sha(sb)=='f815ea1867d0c38ce101e45d7eff48ee2979c6b113a7a5f76d8b3e44daa152f2' and len(sb.splitlines())==244 and sha(op)=='a1e7b1e4d0cb3a5bdd0ed8967352b0861650b5a5f9ba25b175421b14d411e9ef','Complete exact production text pins')
    mb=regular(S/'PREPARATION_MANIFEST.json');m=load(mb);check(sha(mb)=='ee165341f8980110f1362a19c27f697db6df2e68eac01cc110a31c8d08ee9640' and m['schema']=='pr48-current-source-only-closure/v1' and m['files_count']==55 and m['self_excluded']==['PREPARATION_MANIFEST.json'],'Actual closed55+self SOURCE')
    fs,ds=inventory(S);check(fs=={r['path'] for r in m['files']}|{'PREPARATION_MANIFEST.json'} and ds==set(m['directories']),'Complete closed SOURCE topology')
    for rr in m['files']:
        b=regular(S/rr['path']);check(len(b)==rr['bytes'] and sha(b)==rr['sha256'] and stat.S_IMODE((S/rr['path']).stat().st_mode)==0o444,'Entire SOURCE body/full mode '+rr['path']);structured(rr['path'],b)
    check(stat.S_IMODE((S/'PREPARATION_MANIFEST.json').stat().st_mode)==0o444,'SOURCE self full0444')
    pins=load(regular(S/'STATIC_INPUT_BINDINGS.json'));check(len(pins['fixed_rows'])==1633 and not pins['exact_literal_structured_exceptions'],'Complete1633 fixed first-party rows, no structured exception')
    for rr in pins['fixed_rows']:readrow(rr);structured(rr['path'],regular(R/rr['path']))
    closed={}
    for key,info in pins['closed_inputs'].items():
        mm=load(readrow(info['manifest']));root=R/info['root'];check(mm['schema']==info['schema'] and equal(mm['self_excluded'],True if key=='smooth' else [info['self_name']]) and type(mm['files_count']) is int and mm['files_count']==len(mm['files']),'Distinct actual schema '+key)
        names={rr['path'] for rr in mm['files']};check(names=={PurePosixPath(rr['path']).relative_to(info['root']).as_posix() for rr in info['members']},'Exact normalized members '+key)
        if key=='original':
            own=set(info['authorship_root_files'])
            for sub in info['authorship_directory_roots']:own|={sub+'/'+n for n in inventory(root/sub)[0]}
        else:own=inventory(root)[0]-{info['self_name']}
        check(own==names,'Exact scoped owned topology '+key);actualdirs={'.'}|{p.as_posix() for n in names for p in PurePosixPath(n).parents if str(p)!='.'};check(actualdirs=={rr['path'] for rr in info['directories']},'Complete including-root directories '+key)
        for rr in info['directories']:check(type(rr['full_mode']) is int and stat.S_IMODE((root/rr['path']).stat().st_mode)==rr['full_mode'],'Actual directory mode '+key+' '+rr['path'])
        for rr in info['members']:check(rr['full_mode']==0o444,'Full closed member mode '+rr['path']);readrow(rr)
        closed[key]={'manifest':info['manifest'],'schema':mm['schema'],'self_excluded':mm['self_excluded'],'payload_files':len(names),'inclusive_directories':len(actualdirs)}
    snap=load(regular(A/'snapshot_manifest.json'));original={}
    for rr in snap['files']:
        n=rr['relative_path'];b=regular(A/'source_snapshot'/n);check(len(b)==rr['bytes'] and sha(b)==rr['sha256'] and rr['git_mode']=='100644' and rr['snapshot_full_mode']==0o444 and rr['path']=='unsolved_math_prioritization/attempts/2961/'+n,'Original17 exact '+n);original[n]=b
    check(len(original)==17 and inventory(S/'original_archive')[0]==set(original),'Literal original17 archive')
    for n,b in original.items():check(regular(S/'original_archive'/n)==b,'Complete immutable archive '+n)
    diff=regular(A/'original_diff.patch');check(len(diff)==80679 and sha(diff)=='994b4bbd4993227d1100cbd9d7493de776c6619c9daa379dca7f4ef3b3a26698' and diff.count(b'diff --git ')==18,'Complete18path80679 diff read')
    result=load(regular(A/'root_original_actual_reproduction_v2/ROOT_REPRODUCTION_RESULT.json'));summary=load(regular(A/'root_original_actual_reproduction_v2/ROOT_CURRENT_REPRODUCTION_SUMMARY.json'));check(equal(summary['entire_reproduction_result'],result) and summary['future_acceptance_approved'] is False and summary['duplicate_shared_budget'] is True,'Complete typed ROOT result summary')
    helper=result['complete_actual_helper_captures'];git=result['complete_actual_Git_captures'];check(len(helper)==4 and len(git)==38,'Exactly4 helper/38 Git capture classes')
    for i,c in enumerate(helper+git):capture(c,'helper' if i<4 else 'git');check(equal(load(regular((R/c['stdout']['path']).parent/'CAPTURE.json')),c),'Entire genuine capture equals result '+str(i))
    check(len({c['pid'] for c in helper+git})==42,'All42 real child identities distinct')
    expected=[]
    for rr in snap['files']:expected.extend([['git','show',HEAD+':'+rr['path']],['git','ls-tree',HEAD,'--',rr['path']]])
    expected.extend([['git','merge-base',HEAD,BASE],['git','diff','--no-ext-diff','--no-textconv','--binary',MERGE,HEAD,'--'],['git','ls-tree','-r','-z',HEAD,'--','unsolved_math_prioritization/attempts/2961/'],['git','show','2c32c34e6ddfa52ce067805afd3e2157dc32a130:unsolved_math_prioritization/attempts/2961/PARTIAL.md']]);check([c['argv'] for c in git]==expected,'Every genuine38 readonly argv matches original identity')
    author=load(original['check_results.json']);ind=load(original['review/independent_results.json']);replays=result['entire_historical_and_final_replayed_results'];check(equal(replays['author_historical'],author) and equal(replays['identical_submitted_historical'],author) and equal(replays['author_final'],dict(author,partial_sha256='196568d2029fd378dfa43919efbf49dcbd11244a2de8c525483f84484f00e5fa')) and equal(result['entire_historical_independent_result'],ind),'Complete historical/final6570 independent228 byte/scalar coverage')
    old=regular(A/'root_original_actual_reproduction_v2/author_historical/PARTIAL.md');final=original['PARTIAL.md'];oldsentence=b'Separate adversarial review is pending.';newsentence=b'Separate adversarial AI review passed; see [the report](review/REVIEW.md). This has not undergone human peer review.';check(old.count(oldsentence)==1 and old.replace(oldsentence,newsentence)==final and sha(old)=='0036b78ba3164a52c15a7a24ea73fe4438a3db3c9a206f2882070c23e91cd3b2','Exact only review sentence plus human qualifier change')
    check(regular(R/git[-1]['stdout']['path'])==old,'Genuine historical Git stream equals old note');check(author['assertions']==6570 and type(author['assertions']) is int and ind['assertions']==228 and type(ind['assertions']) is int and sum(ind['checks'].values())==228 and result['identical_submitted_counted_independent'] is False,'Exact assertion and independence accounting')
    for c in helper[:3]:check(regular(R/c['source']['path'])==original['check_algebra.py'],'Literal author helper source all3 private copies')
    check(regular(R/helper[3]['source']['path'])==original['review/independent_checks.py'],'Literal historical independent helper source')
    raw=load(regular(A/'ROOT_COMPLETE_RAW_SQL_AUDIT.json'));check(raw['full_raw_and_prior_bytes']==149266659 and raw['all_SQL_rows']==len(raw['complete_row_bindings'])==15458 and raw['future_acceptance_approved'] is False and raw['raw_or_SQL_or_foreign_source_bodies_copied'] is False,'Full fixed first-party raw/SQL audit record')
    check(len({rr['key'] for rr in raw['complete_row_bindings']})==15458,'All15458 unique SQL row witnesses')
    for rr in raw['complete_row_bindings']:check(rr['complete_payload_recursive_type_equal'] is True and rr['complete_report_recursive_type_equal'] is True,'Full type-equal SQL row '+rr['key'])
    for rr in raw['complete_selected_source_bindings']:check(rr['raw_key_presence']=='ABSENT' and rr['raw_present_null'] is False and rr['sqlite_literal_fallback']=='{}' and equal(rr['SQLite_typed_fallback'],{}) and rr['original_prior_report_file_exists'] is False and rr['complete_saved_source_equals_raw_selected'] is True,'Selected ABSENT/fallback/no prior file '+rr['key'])
    ledger=[load(line) for line in original['turns.jsonl'].splitlines()];check(len(ledger)==2 and [rr['turn'] for rr in ledger]==[1,2] and all(type(rr['turn']) is int for rr in ledger),'Exact shared two-entry JSONL2/5')
    for n,ident in [('source_record.json',2961),('related_source_record.json',30004403)]:check(type(load(original[n])['id']) is int and load(original[n])['id']==ident and 'problem' not in load(original[n]),'Plain integer ID source '+n)
    for c in helper+git:
        for k,values in {'pid':[True,0,-1,None],'exit_code':[True,False,1,None],'actual_operator_pid':[True,None,0,11717],'actual_execution':[False,1,None],'completed':[False,1,None],'operator_unchanged':[False,1,None],'source_unchanged':[False,1,'true'],'cwd':['/',None],'started_utc':['2026-01-01T00:00:00',None,'2099-01-01T00:00:00+00:00']}.items():
            for v in values:
                if k=='source_unchanged' and c['source_unchanged'] is None and v is None:continue
                bad=copy.deepcopy(c);bad[k]=v;reject(lambda bad=bad:capture(bad,'private'),'capture mutant '+str(c['pid'])+' '+k+' '+repr(v))
        if c in git:
            for argv in [['git','commit'],['git','branch','--delete','main'],[],True,None]:
                bad=copy.deepcopy(c);bad['argv']=argv;reject(lambda bad=bad:capture(bad,'git'),'destructive/malformed Git argv '+str(c['pid']))
    check(equal(True,1) is False and equal(1,1.0) is False and equal(None,{}) is False and equal([],{} ) is False,'Recursive scalar equality distinguishes representations')
    for bad in [b'{"x":1,"x":2}',b'{"x":NaN}',b'{"x":Infinity}',b'{"x":1e999}']:reject(lambda bad=bad:load(bad),'Duplicate/nonfinite JSON '+repr(bad))
    for bad in ['',True,0,None,'/abs','../escape','a/../b','a//b','a/./b','a\\b','a\0b','.git/body','__pycache__/x']:reject(lambda bad=bad:relative(bad),'Unsafe typed path '+repr(bad))
    check(relative('.')=='.','Bounded lexical dot accepted; directory use rejected separately')
    test=F/'private';test.mkdir(exist_ok=False);fixture=test/'mode';fixture.write_bytes(b'private first-party fixture\n')
    for mode in range(4096):fixture.chmod(mode);check(stat.S_IMODE(fixture.stat().st_mode)==mode and (stat.S_IMODE(fixture.stat().st_mode)==0o444)==(mode==0o444),'Actual full4096 mode '+str(mode))
    fixture.chmod(0o444)
    src=test/'src';dst=test/'dst';src.mkdir();(src/'body').write_bytes(b'private source\n');rename_absent(src,dst);check((dst/'body').read_bytes()==b'private source\n' and not src.exists(),'Actual absent-only rename success')
    src.mkdir();(src/'body').write_bytes(b'private retained source\n');reject(lambda:rename_absent(src,dst),'Existing rename destination');reject(lambda:rename_absent(src,test/'DST'),'Case-insensitive destination alias');check((src/'body').read_bytes()==b'private retained source\n' and (dst/'body').read_bytes()==b'private source\n','All exclusive rename sentinel bodies preserved')
    extra=test/'extra';extra.mkdir();(extra/'empty').mkdir();reject(lambda:inventory(extra),'Actual extra empty directory');(extra/'empty').rmdir();extra.rmdir()
    target=test/'target';target.write_bytes(b'first-party nonsymlink target\n');link=test/'symlink';link.symlink_to(target);reject(lambda:regular(link),'Symlink file');link.unlink();fifo=test/'fifo';os.mkfifo(fifo);reject(lambda:regular(fifo),'Actual FIFO');fifo.unlink()
    for p in [S/'DRAFT_ROOT_PRIMARY_READ_LEDGER.json',S/'DRAFT_ROOT_SCIENCE_CARD.json',S/'DRAFT_ROOT_EVIDENCE_BINDINGS.json',S/'DRAFT_ROOT_CURRENT_INPUT_PREIMAGES.json']:
        o=load(regular(p));check(o['approved_by_root'] is False and o['created_utc'] is None and o['current_verdict'] is None and o['future_acceptance_approved'] is False,'False/null ROOT draft '+p.name)
    check(not (A/'reviewed_candidate').exists(),'No current freeze')
    # Isolated permissive guards are not operative mutations: fixed pinned inputs block them.
    c=copy.deepcopy(git[0]);c['argv']=['git','show','--output=untrusted','HEAD'];capture(c,'git');optional.append('Isolated captured-Git guard permits additional show options; actual38 receipt bytes/argv are fixed by1633 pins and verified exact here, so no operative changed child is approved.')
    optional.append('Retained failed-stage inventory rejects extra empty directories; no existing production attempt exists. A later failed partial stage may need a distinct source repair before retry, while preserving all original failures.')
    optional.append('Read/science/evidence dictionaries enforce consumed fields without a general exact-key allowlist; extra metadata alone does not grant an actual future whole verdict. ROOT must author truthful records.')
    o={'schema':'pr48-source-adversary-private-control-results/v1','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_control_pid':os.getpid(),'assertions':len(labels),'assertion_labels':labels,'whole_fixed_body_rows':list(fullreads.values()),'unique_full_fixed_body_reads':len(fullreads),'full_fixed_read_bytes':sum(rr['bytes'] for rr in fullreads.values()),'all_structured_nodes_by_type':nodes,'four_distinct_closed_inputs':closed,'source_manifest_sha256':sha(mb),'builder_sha256':sha(sb),'operator_sha256':sha(op),'genuine_helper_receipts':4,'genuine_null_Git_receipts':38,'full_mode_controls':4096,'complete_reproduction_and_raw_records_read':True,'raw_SQL_independently_rerun':False,'exact_optional_guard_limits':optional,'inherited_context_disclosed':True,'prepared_this_PR48_source':False,'production_or_historical_helpers_imported_compiled_or_executed':False,'future_freeze_or_merge_approved':False,'foreign_bodies_copied':False,'assigned_SOURCE_audit_completion_estimate_percent':85,'target_discovery_completion_estimate_percent':0}
    with (F/'CONTROL_RESULTS.json').open('x') as h:json.dump(o,h,indent=2,ensure_ascii=False,allow_nan=False);h.write('\n');h.flush();os.fsync(h.fileno())
    print(json.dumps({'status':'PASS_INDEPENDENT_SOURCE_PRIVATE_CHECKS','assertions':len(labels),'full_body_count':len(fullreads),'full_body_bytes':o['full_fixed_read_bytes'],'production_execution':False}))
if __name__=='__main__':main()
