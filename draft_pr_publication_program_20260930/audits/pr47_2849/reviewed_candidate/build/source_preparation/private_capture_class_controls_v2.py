"""Independent private predicates only; no production import, compile or execution."""
import copy, ctypes, datetime as dt, hashlib, json, math, os, re, stat, sys
from pathlib import Path, PurePosixPath
F=Path(__file__).absolute().parent; A=F.parent; R=A.parents[2]
HEAD='487327b2412c436ae69e8c52bf353a9a1fb7594e'; BASE='c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
assertions=[]; readrows={}
def need(v,m):
    if not v: raise ValueError(m)
def passed(v,m): need(v,m); assertions.append(m)
def sha(b): return hashlib.sha256(b).hexdigest()
def raw(p):
    need(not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode),'Regular nonsymlink file')
    b=p.read_bytes(); r={'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b),'full_mode':stat.S_IMODE(p.stat().st_mode)}; need(r['path'] not in readrows or readrows[r['path']]==r,'Repeated body changed'); readrows[r['path']]=r; return b
def relative(n):
    need(type(n) is str and n and '\\' not in n and '\0' not in n,'Explicit canonical path'); p=PurePosixPath(n); need(not p.is_absolute() and str(p)==n and not {'.','..','.git','__pycache__'}.intersection(p.parts),'Canonical path'); return n
def checked(r):
    need(type(r) is dict and set(r)=={'path','bytes','sha256'} and type(r['bytes']) is int and r['bytes']>=0 and type(r['sha256']) is str and re.fullmatch('[0-9a-f]{64}',r['sha256']) is not None,'Typed stream/source row')
    b=raw(R/relative(r['path'])); need(len(b)==r['bytes'] and sha(b)==r['sha256'],'Complete actual source/stream bytes'); return b
def clock(v):
    need(type(v) is str,'Typed time'); t=dt.datetime.fromisoformat(v.replace('Z','+00:00')); need(t.tzinfo is not None and t.utcoffset()==dt.timedelta(0),'AwareUTC'); return t
def equal(a,b):
    if type(a) is not type(b): return False
    if type(a) is dict: return set(a)==set(b) and all(equal(a[k],b[k]) for k in a)
    if type(a) is list: return len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b))
    return a==b
def validate(c,kind,argv,source,operator):
    keys={'schema','argv','cwd','started_utc','actual_operator_pid','stdin_supplied','source','actual_execution','pid','completed','exit_code','finished_utc','stdout','stderr','source_unchanged'}
    need(type(c) is dict and set(c)==keys and c['schema']=='pr47-root-literal-operation-capture/v1','Actual capture exact key/schema')
    need(kind in {'helper','git'} and type(c['argv']) is list and all(type(x) is str for x in c['argv']) and equal(c['argv'],argv) and c['cwd']==str(R),'Actual class and fixed argv/cwd')
    need(type(operator) is int and operator>0 and type(c['actual_operator_pid']) is int and c['actual_operator_pid']==operator and c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']>0 and type(c['exit_code']) is int and c['exit_code']==0 and c['stdin_supplied'] is False and clock(c['started_utc'])<=clock(c['finished_utc'])<=dt.datetime.now(dt.timezone.utc),'Actual typed successful child')
    checked(c['stdout']); need(checked(c['stderr'])==b'','Complete empty success stderr')
    if kind=='helper':
        need(type(c['source']) is dict and equal(c['source'],source) and c['source_unchanged'] is True,'Unchanged typed helper source'); checked(c['source'])
    else: need(source is None and c['source'] is None and c['source_unchanged'] is None,'Actual null Git source, no helper substitution')
def reject(fn,label):
    try: fn()
    except (ValueError,TypeError,KeyError,FileNotFoundError,OSError): assertions.append('Reject '+label); return
    raise ValueError('Failed to reject '+label)
def main():
    passed(__debug__ and not sys.flags.optimize and os.environ.get('PYTHONOPTIMIZE','') in ('','0'),'Unoptimized private predicates')
    builder=raw(F/'prepare_current_packet.py'); operatorbody=raw(F/'capture_root_builder_operation.py')
    passed(b"FAMILY='current_preparation_family_v2'" in builder and b"prep['schema']=='PR47_CURRENT_SOURCE_ONLY_CLOSURE_v2'" in builder and b"F.name=='current_preparation_family_v2'" in operatorbody,'V2 production anchors inspected as text only')
    passed(b"if 'source' in c: checked(c['source'])" not in builder and b"validate_completed_original_capture(c,'helper'" in builder and b"validate_completed_original_capture(c,'git'" in builder,'Mandatory V1 membership branch replaced by explicit capture classes')
    s=json.loads(raw(A/'root_original_actual_reproduction/ROOT_REPRODUCTION_RESULT.json')); snap=json.loads(raw(A/'snapshot_manifest.json')); root=A/'root_original_actual_reproduction'
    helper_specs=[('author/verify.py','verify.py'),('submitted_copy/submitted_verify.py','review/submitted_verify.py'),('historical_independent/independent_checks.py','review/independent_checks.py')]
    cases=[]
    for c,(actual_n,old_n) in zip(s['complete_actual_helper_captures'],helper_specs):
        b=raw(A/'source_snapshot'/old_n); source={'path':(A/'source_snapshot'/old_n).relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b)}; argv=['/usr/bin/python3','-B',str(root/actual_n)]
        validate(c,'helper',argv,source,s['actual_operator_pid']); passed(raw(root/actual_n)==b,'Actual unchanged helper body '+old_n); cases.append((c,'helper',argv,source))
        cap=json.loads(raw((R/c['stdout']['path']).parent/'CAPTURE.json')); passed(equal(cap,c),'Full helper summary equals genuine CAPTURE '+old_n)
    argvlist=[]
    for rr in snap['files']: argvlist.extend([['git','show',HEAD+':'+rr['path']],['git','ls-tree',HEAD,'--',rr['path']]])
    argvlist.append(['git','diff','--no-ext-diff','--no-textconv','--binary',BASE,HEAD,'--'])
    passed(len(argvlist)==33 and len(s['complete_actual_Git_captures'])==33,'Exact33 read-only Git receipts')
    for i,(c,argv) in enumerate(zip(s['complete_actual_Git_captures'],argvlist)):
        validate(c,'git',argv,None,s['actual_operator_pid']); passed(c['source'] is None and c['source_unchanged'] is None,'Genuine null Git accepted '+str(i)); cases.append((c,'git',argv,None))
        passed(equal(json.loads(raw((R/c['stdout']['path']).parent/'CAPTURE.json')),c),'Full Git summary equals genuine CAPTURE '+str(i))
    passed(len(cases)==36 and len({c[0]['pid'] for c in cases})==36,'All36 genuine children distinct')
    mutation_count=0
    mutations={'schema':['fake',None,True,0],'argv':[None,[],True,['git','commit']], 'cwd':[None,'/',str(A)],'actual_operator_pid':[True,0,None,s['actual_operator_pid']+1],'pid':[True,0,-1,None],'actual_execution':[False,1,None],'completed':[False,1,None],'exit_code':[True,False,1,None],'stdin_supplied':[True,0,None],'started_utc':[None,0,'2026-10-03T00:00:00','2099-01-01T00:00:00+00:00'],'finished_utc':[None,0,'1900-01-01T00:00:00+00:00'],'stdout':[None,True,{},[]],'stderr':[None,True,{},[]]}
    for i,(c,kind,argv,source) in enumerate(cases):
        for k,values in mutations.items():
            for value in values:
                bad=copy.deepcopy(c); bad[k]=value; reject(lambda bad=bad:validate(bad,kind,argv,source,s['actual_operator_pid']),'case'+str(i)+' field '+k+' '+repr(value)); mutation_count+=1
        for k in c:
            bad=copy.deepcopy(c); del bad[k]; reject(lambda bad=bad:validate(bad,kind,argv,source,s['actual_operator_pid']),'case'+str(i)+' missing '+k); mutation_count+=1
        bad=dict(c,extra_future_acceptance=True); reject(lambda:validate(bad,kind,argv,source,s['actual_operator_pid']),'case'+str(i)+' extra capture key'); mutation_count+=1
        for field in ['stdout','stderr']:
            for key,value in [('bytes',True),('bytes',-1),('bytes',None),('sha256','0'*64),('path','../outside'),('path','/absolute'),('path','.'),('path','a//b')]:
                bad=copy.deepcopy(c); bad[field][key]=value; reject(lambda bad=bad:validate(bad,kind,argv,source,s['actual_operator_pid']),'case'+str(i)+' typed '+field+' '+key+' '+repr(value)); mutation_count+=1
        for value in [None,True,False,0,{},[],cases[0][3]]:
            if kind=='git' and value is None or kind=='helper' and equal(value,source): continue
            bad=copy.deepcopy(c); bad['source']=value; reject(lambda bad=bad:validate(bad,kind,argv,source,s['actual_operator_pid']),'case'+str(i)+' invalid source '+repr(value)); mutation_count+=1
        for value in [None,True,False,0,1,'true']:
            if kind=='helper' and value is True or kind=='git' and value is None: continue
            bad=copy.deepcopy(c); bad['source_unchanged']=value; reject(lambda bad=bad:validate(bad,kind,argv,source,s['actual_operator_pid']),'case'+str(i)+' unchanged scalar '+repr(value)); mutation_count+=1
        swapped='git' if kind=='helper' else 'helper'; reject(lambda:validate(c,swapped,argv,None if swapped=='git' else cases[0][3],s['actual_operator_pid']),'case'+str(i)+' wrong capture class'); mutation_count+=1
    for i,c in enumerate(s['complete_actual_Git_captures']):
        for badargv in [['git','commit'],['git','show','HEAD:QUEUE.md'],['git','ls-tree',HEAD,'--','QUEUE.md'],['git','diff','--ext-diff',BASE,HEAD],['git','branch','--delete','main'],['git','rev-parse','HEAD'],tuple(c['argv']),c['argv']+[ '--output=changed']]:
            bad=copy.deepcopy(c); bad['argv']=badargv; reject(lambda bad=bad,i=i:validate(bad,'git',argvlist[i],None,s['actual_operator_pid']),'Git'+str(i)+' non-whitelist argv '+repr(badargv)); mutation_count+=1
    fixture=F/'private_mode_fixture'; fixture.write_bytes(b'first-party private mode fixture\n')
    for mode in range(4096):
        fixture.chmod(mode); actual=stat.S_IMODE(fixture.stat().st_mode); passed(actual==mode and (actual==0o444)==(mode==0o444),'Actual full12-bit mode '+str(mode))
    fixture.chmod(0o444)
    for n in ['DRAFT_ROOT_READ_LEDGER.json','DRAFT_ROOT_SCIENCE_CARD.json']:
        o=json.loads(raw(F/n)); passed(o['reading_completed'] is False and all(v is False for v in o['root_flags'].values()) and o['created_utc'] is None and o['preparation_manifest_sha256'] is None and o['operative_preparation_directory']==F.name,'False/null V2 ROOT reading draft '+n)
    for n in ['DRAFT_ROOT_CURRENT_INPUT_PREIMAGES.json','DRAFT_ROOT_EVIDENCE_BINDINGS.json','DRAFT_ROOT_NEW_SOURCE_ADVERSARY_RECORD.json']:
        o=json.loads(raw(F/n)); passed(o['approved_by_root'] is False and o['created_utc'] is None,'False/null ROOT approval draft '+n)
    passed('ROOT_SCOPE_ACCEPTED_CORRECTED_UNRESOLVED_ONLY' not in raw(F/'DRAFT_ROOT_CURRENT_SCOPE_CERTIFICATE.md').decode(),'No draft ROOT acceptance sentinel')
    immutable=['verify.py','verification.json','source_checksums.json','source_record.json','turns.json','prior_report.json','review/independent_checks.py','review/independent_results.json','review/submitted_verify.py','review/submitted_results.json']
    for rr in snap['files']:
        n=rr['relative_path']; passed(raw(F/'original_archive'/n)==raw(A/'source_snapshot'/n),'Entire16 original archive exact '+n)
    for n in immutable: passed(raw(F/'operative_proposal'/n)==raw(A/'source_snapshot'/n),'Immutable operative exact '+n)
    passed(raw(F/'operative_proposal/prior_report.json')==b'null\n','Saved literal null unchanged, not absence fallback')
    passed(json.loads(raw(F/'operative_proposal/turns.json'))['count']==1,'Original object ledger1/5')
    for n in ['STATIC_INPUT_BINDINGS.json','ROOT_FIXED_EVIDENCE.json']:
        passed(raw(F/n)==raw(A/'current_preparation_family'/n),'Fixed original/current ROOT bindings preserved '+n)
    repair=json.loads(raw(F/'SOURCE_V1_REPAIR_BINDINGS.json'))
    for rr in repair['complete_fixed_member_reads']+repair['external_ROOT_closure_and_readback_members']:
        b=raw(R/rr['path']); passed(len(b)==rr['bytes'] and sha(b)==rr['sha256'] and stat.S_IMODE((R/rr['path']).stat().st_mode)==rr['full_mode'],'Closed prior source/adverse full read '+rr['path'])
    passed(repair['old_SOURCE_V1_promoted'] is False and repair['ADVERSE_promoted_to_clean_PASS'] is False and repair['future_acceptance_approved'] is False,'No failed source/ADVERSE/future promotion')
    status=json.loads(raw(F/'SOURCE_STATUS.json')); passed(status['production_import_compile_or_execution'] is False and status['actual_current_freeze'] is False and status['ROOT_approval'] is None and status['current_verdict'] is None,'SOURCE only false current approval')
    passed(not (A/'reviewed_candidate').exists() and not (A/'reviewed_candidate').is_symlink(),'No actual current freeze')
    result={'schema':'PR47_SOURCE_V2_PRIVATE_CAPTURE_CLASS_CONTROL_RESULTS_v1','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_control_pid':os.getpid(),'assertions':len(assertions),'assertion_labels':assertions,'genuine_helper_positives':3,'genuine_null_source_Git_positives':33,'capture_class_malformed_rejection_cases':mutation_count,'all4096_actual_full_modes_checked':True,'full_unique_pinned_body_reads':list(readrows.values()),'full_unique_read_bytes':sum(r['bytes'] for r in readrows.values()),'production_builder_text_sha256':sha(builder),'production_operator_text_sha256':sha(operatorbody),'production_import_compile_or_execution':False,'mathematical_helpers_run':False,'target_discovery_completion_estimate_percent':0,'assigned_SOURCE_preparation_completion_percent':95,'future_acceptance_approved':False,'new_different_clean_SOURCE_adversary_required':True,'foreign_bodies_copied':False}
    with (F/'PRIVATE_CAPTURE_CLASS_CONTROL_RESULTS.json').open('xb') as h: h.write((json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()); h.flush(); os.fsync(h.fileno())
    print(json.dumps({'status':'PASS_PRIVATE_CAPTURE_CLASS_PREDICATES_ONLY','assertions':len(assertions),'malformed_rejections':mutation_count,'all33_genuine_null_Git_accepted':True,'production_executed':False}))
if __name__=='__main__': main()
