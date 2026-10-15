#!/usr/bin/env python3
"""TEXT ONLY until genuine ROOT prerequisites; administrative copying and read-only Git."""
import argparse, ctypes, datetime as dt, hashlib, json, math, os, re, stat, subprocess, sys, traceback
from pathlib import Path, PurePosixPath
HEAD='487327b2412c436ae69e8c52bf353a9a1fb7594e'; BASE='c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
FAMILY='current_preparation_family'; GATE='PENDING_NEW_WHOLE_CURRENT_SOURCE_FIRST_ADVERSARY'
NATIVE={'unsolved_math_prioritization/'+n for n in ['QUEUE.md','state.json','history.jsonl','catalog.json','assessments.json','queue.py','policy.json','manifest.json','cache/problems.json','cache/research_results.json','cache/catalog.sqlite','review_v2/related_target_groups.json']}|{'draft_pr_publication_program_20260930/inventory.json'}
NATIVE4=['unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl','draft_pr_publication_program_20260930/inventory.json']
IMMUTABLE=['verify.py','verification.json','source_checksums.json','source_record.json','turns.json','prior_report.json','review/independent_checks.py','review/independent_results.json','review/submitted_verify.py','review/submitted_results.json']
HEADER=['Rank','ID / code','Problem','EV','Impact (/10)','Difficulty','Proposed','Status','Turns','Chat','Findings','DOI']
def need(v,m):
    if not v: raise ValueError(m)
def sha(b): return hashlib.sha256(b).hexdigest()
def enc(o): return (json.dumps(o,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
def utc(): return dt.datetime.now(dt.timezone.utc).isoformat()
def clock(v):
    need(type(v) is str,'Explicit awareUTC time'); t=dt.datetime.fromisoformat(v.replace('Z','+00:00')); need(t.tzinfo is not None and t.utcoffset()==dt.timedelta(0),'AwareUTC required'); return t
def equal(a,b):
    if type(a) is not type(b): return False
    if type(a) is dict: return set(a)==set(b) and all(equal(a[k],b[k]) for k in a)
    if type(a) is list: return len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b))
    return a==b
def hex64(v): return type(v) is str and re.fullmatch('[0-9a-f]{64}',v) is not None
def load(b):
    def pairs(items):
        out={}
        for k,v in items: need(k not in out,'Duplicate JSON key'); out[k]=v
        return out
    def constant(v): raise ValueError('Nonfinite JSON constant '+v)
    def floating(v):
        n=float(v); need(math.isfinite(n),'Nonfinite JSON number'); return n
    return json.loads(b,object_pairs_hook=pairs,parse_constant=constant,parse_float=floating)
def relative(v):
    need(type(v) is str and v and '\\' not in v and '\0' not in v,'Canonical POSIX path'); p=PurePosixPath(v)
    need(not p.is_absolute() and str(p)==v and not {'.','..','.git','__pycache__'}.intersection(p.parts),'Unsafe relative path'); return v
def raw(p):
    need(not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode),'Regular nonsymlink file'); return p.read_bytes()
def topology(root):
    need(root.is_dir() and not root.is_symlink() and all(not q.is_symlink() for q in root.parents),'Regular directory'); fs=set(); ds=set()
    for p in root.rglob('*'):
        need(not p.is_symlink(),'No symlink members'); n=relative(p.relative_to(root).as_posix())
        if stat.S_ISREG(p.stat().st_mode): fs.add(n)
        else: need(stat.S_ISDIR(p.stat().st_mode),'No special members'); ds.add(n)
    need(ds=={q.as_posix() for n in fs for q in PurePosixPath(n).parents if str(q)!='.'},'Extra/empty directories'); return fs,ds
def rows(rs,mode=False):
    need(type(rs) is list,'Typed row list'); names=set()
    for r in rs:
        need(type(r) is dict and set(r)==({'path','bytes','sha256','full_mode'} if mode else {'path','bytes','sha256'}),'Exact typed row keys'); n=relative(r['path']); need(n not in names,'Duplicate row'); names.add(n)
        need(type(r['bytes']) is int and r['bytes']>=0 and hex64(r['sha256']),'Typed nonboolean byte count/SHA')
        if mode: need(type(r['full_mode']) is int and 0<=r['full_mode']<4096,'Full mode nonboolean0..4095')
    return names
def write(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as h: h.write(b); h.flush(); os.fsync(h.fileno())
def publish_absent(source,destination):
    need(sys.platform=='darwin','macOS RENAME_EXCL required'); lib=ctypes.CDLL(None,use_errno=True); fn=lib.renamex_np; fn.argtypes=[ctypes.c_char_p,ctypes.c_char_p,ctypes.c_uint]; fn.restype=ctypes.c_int
    if fn(os.fsencode(source),os.fsencode(destination),4)!=0:
        n=ctypes.get_errno(); raise OSError(n,os.strerror(n),str(destination))
def build(args,script,A,R,attempt):
    F=script.parent; dest=A/'reviewed_candidate'; need(not dest.exists() and not dest.is_symlink(),'Destination must be absent'); deps={}; outputs={}; commands=[]
    def bindrepo(n,expected=None):
        n=relative(n); b=raw(R/n); r={'path':n,'bytes':len(b),'sha256':sha(b),'full_mode':stat.S_IMODE((R/n).stat().st_mode)}
        need(expected is None or all(r[k]==expected[k] for k in expected),'Exact pinned dependency changed')
        need(n not in deps or equal(deps[n],r),'Repeated dependency changed'); deps[n]=r; return b
    def bind(n): return bindrepo((A/relative(n)).relative_to(R).as_posix())
    def checked(r): rows([r],mode='full_mode' in r); return bindrepo(r['path'],r)
    def git(*argv):
        need(argv and argv[0] in {'branch','rev-parse','show','ls-tree','diff'} and (argv[0]!='branch' or argv[1:]==('--show-current',)),'Read-only Git whitelist'); index=len(commands); directory=attempt/'git'; directory.mkdir(exist_ok=True)
        rec={'argv':['git',*argv],'cwd':str(R),'started_utc':utc(),'actual_execution':False,'completed':False,'pid':None,'exit_code':None,'stdin_supplied':False}; commands.append(rec)
        try:
            with (directory/(str(index)+'.stdout')).open('xb') as out,(directory/(str(index)+'.stderr')).open('xb') as err:
                child=subprocess.Popen(rec['argv'],cwd=R,stdin=subprocess.DEVNULL,stdout=out,stderr=err,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')); rec.update(actual_execution=True,pid=child.pid)
                try: rec['exit_code']=child.wait(timeout=60); rec['completed']=True
                except BaseException: child.kill(); rec['exit_code']=child.wait(); raise
        except BaseException: rec['failure']=traceback.format_exc(); raise
        finally:
            rec['finished_utc']=utc()
            for channel in ['stdout','stderr']:
                p=directory/(str(index)+'.'+channel)
                if p.exists(): b=raw(p); rec[channel]={'path':p.relative_to(attempt).as_posix(),'bytes':len(b),'sha256':sha(b)}
            # Incrementally persisted by this live builder, not by the outer operator.
            (attempt/'GIT_COMMANDS.json').write_bytes(enc(commands))
        need(rec['completed'] is True and type(rec['exit_code']) is int and rec['exit_code']==0 and not raw(directory/(str(index)+'.stderr')),'Failed read-only Git retained'); return raw(directory/(str(index)+'.stdout'))
    prepraw=bind(FAMILY+'/PREPARATION_MANIFEST.json'); prep=load(prepraw)
    need(prep['schema']=='PR47_CURRENT_SOURCE_ONLY_CLOSURE_v1' and prep['status']=='CLOSED_SOURCE_ONLY_CURRENT_PREPARATION' and prep['self_excluded']==['PREPARATION_MANIFEST.json'] and type(prep['files_count']) is int and prep['files_count']==len(prep['files']),'Genuine closed SOURCE-only prep')
    need(topology(F)[0]==rows(prep['files'])|{'PREPARATION_MANIFEST.json'},'Exact self-only SOURCE closure')
    for r in prep['files']:
        b=bind(FAMILY+'/'+r['path']); need(len(b)==r['bytes'] and sha(b)==r['sha256'] and stat.S_IMODE((F/r['path']).stat().st_mode)==0o444,'SOURCE full bytes/full0444'); outputs['build/source_preparation/'+r['path']]=b
    need(stat.S_IMODE((F/'PREPARATION_MANIFEST.json').stat().st_mode)==0o444,'SOURCE self full0444'); outputs['build/source_preparation/PREPARATION_MANIFEST.json']=prepraw
    pins=load(bind(FAMILY+'/STATIC_INPUT_BINDINGS.json')); need(pins['schema']=='PR47_FIXED_CURRENT_SOURCE_INPUTS_v1','Exact fixed contract')
    for group,info in pins['groups'].items():
        mr=info['manifest']; mb=checked(mr); m=load(mb); root=(R/mr['path']).parent
        need(stat.S_IMODE((R/mr['path']).stat().st_mode)==0o444,'Fixed closed self full0444')
        expected={str(PurePosixPath(r['path']).relative_to(root.relative_to(R))) for r in info['members']}; expected_dirs={r['path'] for r in info['directories']}
        if group=='original':
            need(m['schema']=='pr47-original-preparation-self-only-manifest/v1' and m['self_excluded']==['ORIGINAL_PREPARATION_MANIFEST.json'] and len(m['files'])==301 and len(expected_dirs)==55,'Original301+self/55dirs')
            actual=set(info['authorship_root_files']); ds=set()
            for n in info['authorship_directory_roots']:
                fs,sub=topology(A/n); actual|={n+'/'+p for p in fs}; ds|={n}|{n+'/'+p for p in sub}
            need(actual==expected and ds==expected_dirs,'Original scoped ownership; never whole audit root')
        else:
            need(group in {'cover_algebra_family','gauge_geometry_family'},'Exact math families'); fs,ds=topology(root); need(fs==expected|{'SELF_MANIFEST.json'} and ds==expected_dirs,'Exact family topology')
            need(len(m['files'])==(143 if group=='cover_algebra_family' else 71) and len(ds)==(23 if group=='cover_algebra_family' else 15),'Exact family counts')
        for d in info['directories']: need(stat.S_IMODE((root/d['path']).stat().st_mode)==d['full_mode'],'Closed directory mode changed')
        outputs['fixed_first_party_evidence/'+group+'/'+Path(mr['path']).name]=mb
        for r in info['members']:
            need(r['full_mode']==0o444,'Fixed closed member full0444'); outputs['fixed_first_party_evidence/'+group+'/'+str(PurePosixPath(r['path']).relative_to(root.relative_to(R)))]=checked(r)
    for r in pins['separate_original_and_ROOT_actual_captures']: outputs['separate_actual_capture_evidence/'+r['path']]=checked(r)
    rootfixed=load(bind(FAMILY+'/ROOT_FIXED_EVIDENCE.json')); need(rootfixed['schema']=='PR47_FIXED_COMPLETED_ROOT_EVIDENCE_v1' and rootfixed['ROOT_scope_or_current_acceptance_approved'] is False and rootfixed['ROOT_D_closed_payload_files']==219,'Real closed ROOT evidence, not acceptance')
    checked(rootfixed['manifest'])
    for r in rootfixed['members']+rootfixed['separate_actual_closure_members']: checked(r)
    original={}; snapraw=bind('snapshot_manifest.json'); snap=load(snapraw)
    need(snap['schema']=='pr47-original-source-snapshot/v1' and snap['head']==HEAD and snap['github_base']==BASE and snap['merge_base']==BASE and len(snap['files'])==16,'Original16 identities')
    for r in snap['files']:
        n=relative(r['relative_path']); need(n not in original and r['path']=='unsolved_math_prioritization/attempts/2849/'+n and r['git_mode']=='100644' and r['snapshot_mode']=='0444','Exact original native path/mode'); b=bind('source_snapshot/'+n)
        need(len(b)==r['bytes'] and sha(b)==r['sha256'] and stat.S_IMODE((A/'source_snapshot'/n).stat().st_mode)==0o444,'Exact original bytes/full mode')
        need(git('show',HEAD+':'+r['path'])==b and git('ls-tree',HEAD,'--',r['path']).decode().strip()=='100644 blob '+r['git_object']+'\t'+r['path'],'Original Git blob/mode/body'); original[n]=b
    need(topology(A/'source_snapshot')[0]==set(original),'Exact original16 snapshot topology')
    tree=git('ls-tree','-r','-z',HEAD,'--','unsolved_math_prioritization/attempts/2849/').decode().split('\0'); need({r.split('\t',1)[1] for r in tree if r}=={'unsolved_math_prioritization/attempts/2849/'+n for n in original},'Full scientific Git tree')
    metadata=load(bind('original_pr_metadata.json')); need(metadata['head']==HEAD and metadata['github_base']==BASE and metadata['merge_base']==BASE and metadata['changed_files']==17,'Full17 metadata')
    diff=bind('original_diff.patch'); need(len(diff)==59460 and sha(diff)=='17a6b488f85b54d22af865a5e0c9644b016211c3c985bd352631b46632dedc27' and git('diff','--no-ext-diff','--no-textconv','--binary',BASE,HEAD,'--')==diff and git('diff','--name-only',BASE,HEAD).decode().splitlines()==[r['path'] for r in metadata['all_changed_paths']],'Full original17-path diff')
    ledger=load(original['turns.json']); source=load(original['source_record.json']); author=load(original['verification.json']); independent=load(original['review/independent_results.json'])
    need(type(ledger) is dict and type(ledger['count']) is int and ledger['count']==1 and len(ledger['attempts'])==1 and original['prior_report.json']==b'null\n' and type(source) is dict and source['id']==2849 and 'problem' not in source,'Original object1/5/plain source/literalnull')
    future={}
    for n,option in [('ROOT_CURRENT_SCOPE_CERTIFICATE.md','root_scope_certificate_sha256'),('ROOT_PRIMARY_READ_LEDGER.json','root_read_ledger_sha256'),('ROOT_SCIENCE_CARD.json','root_science_card_sha256'),('ROOT_CURRENT_INPUT_PREIMAGES.json','root_current_input_manifest_sha256'),('ROOT_EVIDENCE_BINDINGS.json','root_evidence_bindings_sha256')]:
        b=bind(n); need(sha(b)==getattr(args,option),'Exact genuine separate ROOT prerequisite pin'); future[n]=b
    evidence=load(future['ROOT_EVIDENCE_BINDINGS.json']); need(set(evidence)=={'schema','operative_preparation_directory','approved_by_root','created_utc','notes','manifest','proof_notes','summary','raw_audit','source_adversary'} and evidence['schema']=='PR47_ROOT_EVIDENCE_BINDINGS_v1' and evidence['operative_preparation_directory']==FAMILY and evidence['approved_by_root'] is True and type(evidence['notes']) is str and len(evidence['notes'].strip())>=40 and clock(prep['utc'])<=clock(evidence['created_utc'])<=clock(utc()),'Actual post-SOURCE ROOT evidence approval')
    def auditrow(r):
        rows([r]); return checked(dict(r,path=(A/r['path']).relative_to(R).as_posix()))
    need(evidence['manifest']['path']=='root_original_actual_reproduction/MANIFEST.json' and evidence['summary']['path']=='root_original_actual_reproduction/ROOT_CURRENT_REPRODUCTION_SUMMARY.json' and evidence['proof_notes']['path']=='ROOT_MATHEMATICAL_REVIEW.md' and evidence['raw_audit']['path']=='ROOT_COMPLETE_RAW_SQL_AUDIT.json','Exact genuine ROOT evidence anchors')
    rmraw=auditrow(evidence['manifest']); rm=load(rmraw); root=A/'root_original_actual_reproduction'
    need(rm['schema']=='pr47-root-original-complete-reproduction-self-only-closure/v1' and rm['self_excluded']==['MANIFEST.json'] and type(rm['files_count']) is int and rm['files_count']==len(rm['files'])==219 and sha(rmraw)==rootfixed['manifest']['sha256'],'Genuine pinned ROOT219+self closure')
    rr=[]
    for r in rm['files']:
        need(type(r) is dict and set(r) in [{'path','bytes','sha256'},{'path','bytes','sha256','full_mode'}],'Typed ROOT closed member')
        if 'full_mode' in r: need(type(r['full_mode']) is int and r['full_mode']==0o444 or type(r['full_mode']) is str and r['full_mode']=='0444','ROOT full mode')
        rr.append({k:r[k] for k in ['path','bytes','sha256']})
    need(topology(root)[0]==rows(rr)|{'MANIFEST.json'} and stat.S_IMODE((root/'MANIFEST.json').stat().st_mode)==0o444,'Exact ROOT evidence topology/fullself')
    outputs['root_evidence/MANIFEST.json']=rmraw
    for r in rr:
        need(stat.S_IMODE((root/r['path']).stat().st_mode)==0o444,'ROOT member full0444'); outputs['root_evidence/'+r['path']]=auditrow(dict(r,path='root_original_actual_reproduction/'+r['path']))
    closedsummary=load(auditrow(evidence['summary'])); need(closedsummary['schema']=='pr47-root-current-complete-reproduction-summary/v1' and closedsummary['status']=='PASS_ROOT_COMPLETED_FIRST_PARTY_REPRODUCTION' and closedsummary['future_acceptance_approved'] is False and closedsummary['full_problem_solved'] is False and closedsummary['foreign_primary_SQL_raw_cache_body_copy'] is False and closedsummary['duplicate_closure_failure_preserved'] is True,'Completed genuine ROOT summary without future acceptance')
    summary=closedsummary['entire_reproduction_result']; need(equal(summary,load(bind('root_original_actual_reproduction/ROOT_REPRODUCTION_RESULT.json'))) and summary['schema']=='pr47-root-original-complete-reproduction/v1' and summary['status']=='PASS_ROOT_UNCHANGED_ORIGINAL_REPRODUCTION' and summary['future_acceptance_approved'] is False and summary['full_Floer_problem_solved'] is False and summary['duplicate114_counted_independent'] is False and equal(summary['entire_author_result'],author) and equal(summary['entire_identical_submitted_copy_result'],author) and equal(summary['entire_historical_independent_result'],independent) and equal(summary['complete_original_turns'],ledger) and summary['original_prior_literal'] is None,'Complete genuine ROOT result/scalar types')
    for k,n in [('original_substantive_attempts',1),('turn_limit',5),('new_substantive_attempts',0),('audit_turns',0)]: need(type(summary[k]) is int and summary[k]==n,'Typed ROOT accounting')
    for n,b in [('author/verification.json',original['verification.json']),('submitted_copy/verification.json',original['verification.json']),('historical_independent/independent_results.json',original['review/independent_results.json'])]: need(bind('root_original_actual_reproduction/'+n)==b,'Entire actual ROOT receipts byte-exact')
    caps=summary['complete_actual_helper_captures']; need(type(caps) is list and len(caps)==3,'All3 real unchanged ROOT helper captures')
    for c in caps+summary['complete_actual_Git_captures']:
        need(c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']>0 and type(c['exit_code']) is int and c['exit_code']==0 and c['stdin_supplied'] is False and clock(c['started_utc'])<=clock(c['finished_utc'])<=clock(utc()),'Actual complete child records')
        for k in ['stdout','stderr']: checked(c[k])
        if 'source' in c: checked(c['source']); need(c['source_unchanged'] is True,'Unchanged mathematical helper')
    need(len(summary['complete_actual_Git_captures'])==33,'Actual full16body/tree/full17diff captures')
    rawrecord=load(auditrow(evidence['raw_audit'])); need(rawrecord['schema']=='pr47-root-in-place-complete-raw-sql-audit/v1' and rawrecord['status']=='PASS_FULL_RAW_PRIOR_SQL_AND_ORIGINAL_PLAIN_SOURCE' and type(rawrecord['full_raw_and_prior_bytes']) is int and rawrecord['full_raw_and_prior_bytes']==149266659 and type(rawrecord['all_SQL_rows']) is int and rawrecord['all_SQL_rows']==15458 and len(rawrecord['complete_row_bindings'])==15458 and rawrecord['source_record_schema']=='plain_raw_problem_object' and rawrecord['complete_saved_source_equals_raw_selected'] is True and rawrecord['selected_prior_key_present'] is False and equal(rawrecord['selected_prior_fallback'],{}) and rawrecord['raw_null_present'] is False and rawrecord['literal_original_prior_file_value'] is None and rawrecord['literal_original_prior_differs_from_upstream_absent_fallback'] is True and rawrecord['raw_or_SQL_or_foreign_source_bodies_copied'] is False and rawrecord['future_acceptance_approved'] is False and equal(rawrecord['original_native_selected_read']['complete_selected_problem'],source),'Actual full raw/SQL/prior null versus absence{}')
    need(all(r['complete_payload_recursive_type_equal'] is True and r['complete_report_recursive_type_equal'] is True and r['ambiguous_code'] is False for r in rawrecord['complete_row_bindings']) and len({r['key'] for r in rawrecord['complete_row_bindings']})==15458,'Complete unique typed SQL comparisons')
    notes=auditrow(evidence['proof_notes']); need(notes.decode().strip() and not notes.decode().lstrip().startswith('# DRAFT'),'Genuine ROOT mathematical review'); outputs['root_evidence/ROOT_MATHEMATICAL_REVIEW.md']=notes; outputs['root_evidence/ROOT_COMPLETE_RAW_SQL_AUDIT.json']=auditrow(evidence['raw_audit'])
    arraw=auditrow(evidence['source_adversary']); ar=load(arraw)
    need(ar['schema']=='PR47_ROOT_NEW_SOURCE_ADVERSARY_RECORD_v1' and ar['approved_by_root'] is True and ar['complete_report_personally_read'] is True and ar['new_different_source_adversary'] is True and ar['closed_clean'] is True and ar['mandatory_corrections']==[] and ar['preparation_manifest_sha256']==sha(prepraw) and ar['builder_sha256']==sha(raw(script)) and ar['operator_sha256']==sha(raw(F/'capture_root_builder_operation.py')) and clock(prep['utc'])<=clock(ar['created_utc'])<=clock(utc()),'New different clean SOURCE review/ROOT read required')
    amraw=auditrow(ar['manifest']); am=load(amraw); arp=PurePosixPath(ar['manifest']['path']); arroot=A/arp.parent.as_posix(); arn=arp.name
    need(am['self_excluded']==[arn] and type(am['files_count']) is int and am['files_count']==len(am['files']),'Adversary true self-only closure'); ars=[]
    for r in am['files']:
        need(type(r) is dict and set(r) in [{'path','bytes','sha256'},{'path','bytes','sha256','full_mode'}],'Typed source adversary member'); ars.append({k:r[k] for k in ['path','bytes','sha256']})
        if 'full_mode' in r: need(type(r['full_mode']) is int and r['full_mode']==0o444 or type(r['full_mode']) is str and r['full_mode']=='0444','Source adversary declared full0444')
    need(topology(arroot)[0]==rows(ars)|{arn} and stat.S_IMODE((arroot/arn).stat().st_mode)==0o444 and equal(ar['members'],[dict(r,path=arp.parent.as_posix()+'/'+r['path']) for r in ars]),'Exact closed source adversary member list')
    need(ar['report']['path'] in {r['path'] for r in ar['members']},'Report belongs to closed reviewer'); auditrow(ar['report']); outputs['new_source_adversary/'+ar['manifest']['path']]=amraw
    for r in ar['members']: need(stat.S_IMODE((A/r['path']).stat().st_mode)==0o444,'Source adversary full0444'); outputs['new_source_adversary/'+r['path']]=auditrow(r)
    outputs['root_approval/ROOT_NEW_SOURCE_ADVERSARY_RECORD.json']=arraw
    cert=future['ROOT_CURRENT_SCOPE_CERTIFICATE.md'].decode(); need(cert.splitlines()[0]=='# ROOT PR47 corrected unresolved scope acceptance' and cert.splitlines().count('ROOT_SCOPE_ACCEPTED_CORRECTED_UNRESOLVED_ONLY')==1 and 'DRAFT' not in cert,'Real exact scoped ROOT certificate')
    for literal in [HEAD,BASE,'Status: unsolved','Original turns: 1/5; new: 0; audit: 0','Universal normal vanishing: false','Realized example instanton rank: unknown','Full problem solved: false','Novelty: false','NEW whole-current review: PENDING','Paper/new DOI/tracker: false','Sivek','Zentner','Proposition6.1']: need(literal in cert,'Required precise scope '+literal)
    read=load(future['ROOT_PRIMARY_READ_LEDGER.json']); science=load(future['ROOT_SCIENCE_CARD.json']); flags=load(bind(FAMILY+'/DRAFT_ROOT_READ_LEDGER.json'))['root_flags']; qual=bind(FAMILY+'/SOURCE_PRECISION_QUALIFICATIONS.md'); familypins={k:v['manifest']['sha256'] for k,v in pins['groups'].items() if k!='original'}
    for o,schema in [(read,'PR47_ROOT_READ_LEDGER_v1'),(science,'PR47_ROOT_SCIENCE_CARD_v1')]:
        need(o['schema']==schema and o['operative_preparation_directory']==FAMILY and o['reading_completed'] is True and equal(o['root_flags'],{k:True for k in flags}) and type(o['reading_notes']) is str and len(o['reading_notes'].strip())>=40 and clock(prep['utc'])<=clock(o['created_utc'])<=clock(utc()),'Actual complete ROOT reading')
        need(o['scope_certificate_sha256']==args.root_scope_certificate_sha256 and o['preparation_manifest_sha256']==sha(prepraw) and o['source_qualification_sha256']==sha(qual) and o['evidence_bindings_sha256']==args.root_evidence_bindings_sha256 and equal(o['family_manifest_sha256'],familypins),'Actual ROOT evidence pins')
        for k,n in [('original_substantive_attempts',1),('new_substantive_attempts',0),('audit_turns',0)]: need(type(o[k]) is int and o[k]==n,'Typed exact accounting')
    need(science['status']=='unsolved' and science['full_problem_solved'] is False and science['novelty_claimed'] is False and science['universal_normal_vanishing_false'] is True and science['realized_example_instanton_rank_computed'] is False and type(science['turn_limit']) is int and science['turn_limit']==5 and science['read_ledger_sha256']==args.root_read_ledger_sha256 and science['current_input_manifest_sha256']==args.root_current_input_manifest_sha256 and science['new_whole_current_gate']=='PENDING' and all(science[k] is None for k in ['current_model','current_reasoning_effort','current_deadline_utc','current_verdict']) and all(science[k] is False for k in ['paper_created','new_DOI_created','tracker_row_created']),'Scoped unresolved science, never full-solution or runtime approval')
    current=load(future['ROOT_CURRENT_INPUT_PREIMAGES.json']); need(set(current)=={'schema','operative_preparation_directory','approved_by_root','created_utc','reason','current_head','files'} and current['schema']=='PR47_ROOT_FRESH13_INPUT_PREIMAGES_v1' and current['operative_preparation_directory']==FAMILY and current['approved_by_root'] is True and type(current['reason']) is str and len(current['reason'].strip())>=40 and clock(prep['utc'])<=clock(current['created_utc'])<=clock(utc()) and type(current['current_head']) is str and re.fullmatch('[0-9a-f]{40}',current['current_head']) and len(current['files'])==13 and rows(current['files'],True)==NATIVE,'Actual fresh13/main authority')
    currentby={r['path']:r for r in current['files']}
    for r in rawrecord['inputs']: need(r['path'] in currentby and all(r[k]==currentby[r['path']][k] for k in ['bytes','sha256']),'Actual raw/SQL binding matches approved live inputs')
    def nativecheck():
        need(git('branch','--show-current').strip()==b'main' and git('rev-parse','HEAD').decode().strip()==current['current_head'],'Exact approved main HEAD')
        for r in current['files']:
            b=raw(R/r['path']); need(len(b)==r['bytes'] and sha(b)==r['sha256'] and stat.S_IMODE((R/r['path']).stat().st_mode)==r['full_mode'],'Live native bytes/full modes')
            if r['path'].endswith('.json'): load(b)
            if r['path'].endswith('.jsonl'):
                for line in b.splitlines(): need(bool(line.strip()),'Nonblank JSONL'); load(line)
    nativecheck()
    for n in NATIVE4: need(git('show',current['current_head']+':'+n)==raw(R/n),'Dated committed native4 equals live body'); git('ls-tree',current['current_head'],'--',n)
    outername=relative(os.environ.get('PR47_ROOT_OUTER_CAPTURE','')); need(re.fullmatch(r'tmp/root_pr47_current_outer_[0-9]{8}T[0-9]{6}\.[0-9]{6}Z',outername),'Inherited actual outer path'); opraw=bind(outername+'/OPERATION_PRELAUNCH.json'); op=load(opraw)
    need(op['schema']=='PR47_ROOT_BUILDER_PRELAUNCH_v1' and type(op['operator_pid']) is int and op['operator_pid']==os.getppid() and op['builder_sha256']==sha(raw(script)) and op['operator_sha256']==sha(raw(F/'capture_root_builder_operation.py')) and op['argv']==['/usr/bin/python3','-B',str(script),*sys.argv[1:]] and op['cwd']==str(R) and clock(op['started_utc'])<=clock(utc()),'Actual parent/source/argv/cwd')
    for n,pin in [('PRELAUNCH_BUILDER_SOURCE.py',op['builder_sha256']),('PRELAUNCH_OPERATOR.py',op['operator_sha256'])]: b=bind(outername+'/'+n); need(sha(b)==pin,'Prelaunch source'); outputs['build/root_outer_prelaunch/'+n]=b
    outputs['build/root_outer_prelaunch/OPERATION_PRELAUNCH.json']=opraw
    outputs['CURRENT_EXECUTION_REFERENCE.json']=enc({'audit_relative_outer_capture':outername,'outer_parent_pid':os.getppid(),'actual_builder_pid':os.getpid(),'audit_relative_inner_attempt':attempt.relative_to(A).as_posix(),'outer_complete_CAPTURE_written_only_after_child_exit':True,'inner_GIT_COMMANDS_written_incrementally_while_builder_alive':True,'frozen_inner_copy_is_prepublication_prefix':True,'outer_operator_does_not_write_inner_commands':True,'ROOT_personally_reads_original_final_inner_full_records_streams_AFTER_child_exit':True,'ROOT_final_actual_outer_capture_full_read_required':True,'completed_outer_or_current_verdict_claimed':False})
    queue=raw(R/NATIVE4[0]); lines=queue.splitlines(keepends=True); need(sum(line.startswith(b'|') and [x.strip() for x in line.decode().split('|')[1:-1]]==HEADER for line in lines)==1,'Unique named queue header')
    hits=[line for line in lines if line.startswith(b'|') and len(line.decode().split('|'))==14 and line.decode().split('|')[2].strip()=='2849 / KP-3.51']; need(len(hits)==1,'Unique exact target row'); before=hits[0]; fields=before.decode().split('|'); need(fields[8].strip()=='queued' and fields[9].strip()=='0/5','Exact queued0/5 preimage'); after=list(fields)
    finding='Corrected unresolved PR47: known Sivek-Zentner menagerie Prop6.1 realizes normal H1 degeneracy, so universal vanishing is false. Actual degenerate Floer contributions/differentials or bypass mechanism remain missing. Quartic unrealized; trefoil6 known instanton L-space; auxiliary2608.20551v1 clause only. Original1/5,new0,audit0; NEW whole-current review PENDING; no full solution/novelty/DOI/tracker.'
    for i,v in [(8,'unsolved'),(9,'1/5'),(11,finding)]: after[i]=' '+v+' '
    need(all(x==y for i,(x,y) in enumerate(zip(fields,after)) if i not in {8,9,11}),'All other cells/Chat/DOI exact'); afterraw='|'.join(after).encode(); prospective=b''.join(afterraw if line==before else line for line in lines)
    for n,b in original.items(): outputs['original_archive/'+n]=b
    for p in sorted((F/'operative_proposal').rglob('*')):
        if p.is_file(): outputs[p.relative_to(F/'operative_proposal').as_posix()]=bind(FAMILY+'/operative_proposal/'+p.relative_to(F/'operative_proposal').as_posix())
    need(all(outputs[n]==original[n] for n in IMMUTABLE),'Operative immutable helpers/results/plain source/object turns/null exact')
    for n in ['README.md','PR_DRAFT.md','pr_body.md','CURRENT_CONTEXT.md','CURRENT_REVIEW_CONTEXT.md']: outputs[n]=bind(FAMILY+'/presentations/'+n)
    outputs['SOURCE_PRECISION_QUALIFICATIONS.md']=qual; outputs['original_snapshot_manifest.json']=snapraw; outputs['original_diff.patch']=diff
    for n in NATIVE4:
        b=raw(R/n); label=n.replace('/','__'); outputs['native4_proposal/preimage/'+label]=b; outputs['native4_proposal/prospective/'+label]=prospective if n==NATIVE4[0] else b
    outputs['CURRENT_QUEUE_PATCH.json']=enc({'phase':'LOCAL_PROSPECTIVE_NO_NATIVE_ACCEPTANCE','selected_id':2849,'allowed_named_changes':['Status','Turns','Findings'],'row_before':before.decode(),'row_prospective':afterraw.decode(),'queue_preimage_sha256':sha(queue),'queue_prospective_sha256':sha(prospective),'all_other_rows_cells_Chat_DOI_preserved':True,'state_history_inventory_unchanged_byte_exact':True,'future_fresh13_and_ROOT_native_acceptance_required':True})
    for n,b in future.items(): outputs['root_approval/'+n]=b
    common={'schema':'PR47_CURRENT_CORRECTED_UNRESOLVED_v1','id':2849,'problem_number':'KP-3.51','status':'unsolved','original_substantive_attempts':1,'turn_limit':5,'new_substantive_attempts':0,'audit_turns':0,'full_problem_solved':False,'novelty_claimed':False,'universal_normal_vanishing_false':True,'realized_example_instanton_rank_computed':False,'current_model':None,'current_reasoning_effort':None,'current_deadline_utc':None,'current_verdict':None,'current_gate':GATE,'old_review_PASS_transferred':False,'native_mirror_disposition':'PENDING','paper_created':False,'new_DOI_created':False,'tracker_row_created':False,'exact_remaining_gap':'Actual degenerate reducible Floer contribution/differential control or another sufficient mechanism.'}
    for n in ['status.json','readiness.json','review/verdict.json','review/review_summary.json']: outputs[n]=enc(common)
    outputs['CURRENT_DEPENDENCIES.json']=enc({'anchor':'repository_root','files':sorted(deps.values(),key=lambda r:r['path']),'current_native13':current['files'],'current_main_head':current['current_head'],'fresh13_and_final_current_evidence_needed_again_before_acceptance':True,'native4_Git_stdout_dated_first_party_only':True,'foreign_bodies_copied':False})
    outputs['RESEARCH_LOG.md']=(utc()+' — Actual administrative freeze75%; target discovery0%; original1/5,new0,audit0. Corrected route/provenance scope only. NEW whole-current review, ROOT reconciliation and native acceptance PENDING.\n').encode()+qual
    def recheck():
        for r in deps.values(): b=raw(R/r['path']); need(len(b)==r['bytes'] and sha(b)==r['sha256'] and stat.S_IMODE((R/r['path']).stat().st_mode)==r['full_mode'],'Dependency byte/full mode changed')
        nativecheck(); need(raw(R/NATIVE4[0])==queue,'Queue changed')
    recheck(); retained=[]
    for prior in sorted((A/'tmp').glob('root_pr47_current_build_*')):
        need(prior.is_dir() and not prior.is_symlink(),'Regular retained actual attempt'); fs=set(); ds=set(); listed=[]
        # A genuine failed stage can contain empty directories: preserve its real tree.
        for p in prior.rglob('*'):
            need(not p.is_symlink(),'Retained attempt symlink rejected'); n=relative(p.relative_to(prior).as_posix())
            if stat.S_ISREG(p.stat().st_mode): fs.add(n)
            else: need(stat.S_ISDIR(p.stat().st_mode),'Retained special member rejected'); ds.add(n)
        for n in sorted(fs):
            b=raw(prior/n); listed.append({'path':n,'bytes':len(b),'sha256':sha(b)})
            if prior==attempt: outputs['build/actual_attempt_prepublication_prefix/'+n]=b
        retained.append({'audit_relative_directory':prior.relative_to(A).as_posix(),'files':listed,'directories':sorted(ds),'current_attempt_prepublication_prefix':prior==attempt,'all_original_attempts_preserved':True})
    outputs['build/RETAINED_ACTUAL_ATTEMPTS.json']=enc(retained)
    stage=attempt/'stage'; stage.mkdir(exist_ok=False)
    for n,b in sorted(outputs.items()): p=stage/relative(n); write(p,b); p.chmod(0o444)
    need(topology(stage/'original_archive')[0]==set(original) and all(raw(stage/'original_archive'/n)==b for n,b in original.items()),'All16 byte-exact archived originals')
    need(all(raw(stage/n)==original[n] for n in IMMUTABLE),'Immutable operative data exact')
    members=[{'path':n,'bytes':len(raw(stage/n)),'sha256':sha(raw(stage/n))} for n in sorted(topology(stage)[0])]; manifest={'schema':'PR47_STRICT_CURRENT_PACKET_v1','self_excluded':['MANIFEST.json'],'files_count':len(members),'files':members,'directories':sorted(topology(stage)[1]),'full_permission_mode':'0444','current_gate':GATE,'status':'unsolved','full_problem_solved':False,'novelty_claimed':False,'original_substantive_attempts':1,'new_substantive_attempts':0,'audit_turns':0}
    write(stage/'MANIFEST.json',enc(manifest)); (stage/'MANIFEST.json').chmod(0o444); need(topology(stage)[0]==rows(members)|{'MANIFEST.json'},'Self-only exact frozen topology')
    for r in members: p=stage/r['path']; b=raw(p); need(len(b)==r['bytes'] and sha(b)==r['sha256'] and stat.S_IMODE(p.stat().st_mode)==0o444,'Full staged bytes/full0444')
    need(stat.S_IMODE((stage/'MANIFEST.json').stat().st_mode)==0o444,'Self full0444'); recheck(); need(not dest.exists() and not dest.is_symlink(),'Destination appeared, retain stage'); publish_absent(stage,dest)
    print(json.dumps({'status':'ACTUAL_CURRENT_FREEZE_WHOLE_REVIEW_PENDING','destination':str(dest),'manifest_sha256':sha(raw(dest/'MANIFEST.json')),'original_attempts':'1/5','new_attempts':0,'audit_turns':0,'native_writes':0,'current_whole_verdict':None},indent=2))
def main():
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--execute',action='store_true')
    for n in ['root-scope-certificate','root-read-ledger','root-science-card','root-current-input-manifest','root-evidence-bindings']: parser.add_argument('--'+n+'-sha256',required=True)
    args=parser.parse_args(); need(args.execute and all(hex64(v) for k,v in vars(args).items() if k.endswith('sha256')),'Explicit execute/five genuine ROOT SHA pins'); need(not sys.flags.optimize and os.environ.get('PYTHONOPTIMIZE','') in ('','0'),'No optimized guards')
    script=Path(__file__).absolute(); raw(script); A=script.parent.parent; R=A.parents[2]; need(script.parent.name==FAMILY and A.name=='pr47_2849' and R==Path('/Users/alec/Documents/Math'),'Exact ROOT PR47 anchor')
    (A/'tmp').mkdir(exist_ok=True); need(not (A/'tmp').is_symlink(),'Regular audit-local tmp'); attempt=A/'tmp'/('root_pr47_current_build_'+dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')); attempt.mkdir(exist_ok=False)
    write(attempt/'PRELAUNCH_BUILDER_SOURCE.py',raw(script)); write(attempt/'INVOCATION.json',enc({'argv':sys.argv,'cwd':str(Path.cwd()),'pid':os.getpid(),'parent_pid':os.getppid(),'utc':utc(),'source_sha256':sha(raw(script)),'administrative_only':True}))
    try: build(args,script,A,R,attempt)
    except BaseException:
        error=traceback.format_exc(); write(attempt/'BUILD_FAILURE.json',enc({'utc':utc(),'status':'FAILED_ACTUAL_BUILD_PRESERVED','traceback':error,'current_positive_verdict':False})); print(error,file=sys.stderr); raise
if __name__=='__main__': main()
