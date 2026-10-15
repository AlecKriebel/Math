#!/usr/bin/env python3
"""Independent private administrative predicates; production source is only read as text."""
from pathlib import Path, PurePosixPath
import copy
import ctypes
import datetime as dt
import hashlib
import json
import math
import os
import re
import stat
import sys

F = Path(__file__).absolute().parent
A = F.parent
R = A.parents[2]
V = A / 'current_preparation_family_v2'
ASSERTIONS = []
READS = {}
NATIVE = {'unsolved_math_prioritization/' + n for n in [
    'QUEUE.md', 'state.json', 'history.jsonl', 'catalog.json', 'assessments.json',
    'queue.py', 'policy.json', 'manifest.json', 'cache/problems.json',
    'cache/research_results.json', 'cache/catalog.sqlite', 'review_v2/related_target_groups.json']}
NATIVE.add('draft_pr_publication_program_20260930/inventory.json')
SHA_PREP = '5ba87a43d1e5da841c8d6f47b6c398c5de55047a447468e1576d2b0cbbd7439e'
SHA_BUILD = 'e6df8cf9b54132d0ec9aee6d4a010e4f8ae95797dbbdd4abd23eb03f86856215'
SHA_OPERATOR = '02a5a169bfc87cb83595d796e375ece467f4073e63ac91f4171af6403606ae8a'

def check(name, value):
    if not value:
        raise AssertionError(name)
    ASSERTIONS.append(name)

def req(value):
    if not value:
        raise ValueError('Independent predicate rejection')

def bad(name, fn, *args):
    try:
        fn(*args)
    except (ValueError, TypeError, KeyError, FileNotFoundError, OSError):
        check(name, True)
    else:
        raise AssertionError('Negative accepted: ' + name)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def dump(value):
    return (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + '\n').encode()

def strict(raw):
    def pairs(items):
        value = {}
        for k, v in items:
            req(k not in value)
            value[k] = v
        return value
    def finite(s):
        n = float(s)
        req(math.isfinite(n))
        return n
    def constant(s):
        raise ValueError(s)
    return json.loads(raw, object_pairs_hook=pairs, parse_float=finite, parse_constant=constant)

def equal(a, b):
    return json.dumps(a, sort_keys=True, separators=(',', ':'), allow_nan=False) == json.dumps(b, sort_keys=True, separators=(',', ':'), allow_nan=False)

def canonical(n):
    req(type(n) is str and n and '\\' not in n and '\0' not in n)
    p = PurePosixPath(n)
    req(not p.is_absolute() and str(p) == n and not set(p.parts).intersection({'.', '..', '.git', '__pycache__'}))
    return n

def rows(values):
    req(type(values) is list)
    names = set()
    for v in values:
        req(type(v) is dict and set(v) == {'path', 'bytes', 'sha256'})
        n = canonical(v['path'])
        req(n not in names and type(v['bytes']) is int and v['bytes'] >= 0)
        req(type(v['sha256']) is str and re.fullmatch('[0-9a-f]{64}', v['sha256']))
        names.add(n)
    return names

def read(path):
    req(not path.is_symlink() and not any(p.is_symlink() for p in path.parents))
    req(stat.S_ISREG(path.stat().st_mode))
    return path.read_bytes()

def tree(root):
    req(root.is_dir() and not root.is_symlink() and not any(p.is_symlink() for p in root.parents))
    files, dirs = set(), set()
    for p in root.rglob('*'):
        req(not p.is_symlink())
        n = canonical(p.relative_to(root).as_posix())
        if stat.S_ISREG(p.stat().st_mode):
            files.add(n)
        else:
            req(stat.S_ISDIR(p.stat().st_mode))
            dirs.add(n)
    expected = {str(p) for n in files for p in PurePosixPath(n).parents if str(p) != '.'}
    req(expected == dirs)
    return files

def fullmode(mode, expected=0o444):
    req(type(mode) is int and mode == expected)

def full_read(row, prefix=''):
    n = canonical(prefix + row['path'])
    raw = read(A / n)
    check('fixed full bytes/SHA ' + n, len(raw) == row['bytes'] and sha(raw) == row['sha256'])
    READS[n] = {'path': n, 'bytes': len(raw), 'sha256': sha(raw), 'full_mode': stat.S_IMODE((A/n).stat().st_mode)}
    return raw

def closed(root, manifest_name, count=None, separate=()):
    raw = read(root / manifest_name)
    m = strict(raw)
    rr = [{k: v[k] for k in ('path', 'bytes', 'sha256')} for v in m['files']]
    req(type(m['files_count']) is int and m['files_count'] == len(rr))
    if count is not None:
        req(m['files_count'] == count)
    req(m['self_excluded'] == [manifest_name] + list(separate))
    req(tree(root) == rows(rr) | {manifest_name} | set(separate))
    fullmode(stat.S_IMODE((root/manifest_name).stat().st_mode))
    for row in rr:
        body = read(root/row['path'])
        req(len(body) == row['bytes'] and sha(body) == row['sha256'])
        fullmode(stat.S_IMODE((root/row['path']).stat().st_mode))
    return m

def utc(s):
    req(type(s) is str)
    value = dt.datetime.fromisoformat(s[:-1]+'+00:00' if s.endswith('Z') else s)
    req(value.tzinfo is not None and value.utcoffset() == dt.timedelta(0))
    return value

def aware(s, low):
    req(utc(low) <= utc(s) <= dt.datetime.now(dt.timezone.utc))

def native_row(v):
    req(type(v) is dict and set(v) == {'path', 'bytes', 'sha256', 'full_mode'})
    rows([{k: v[k] for k in ('path', 'bytes', 'sha256')}])
    req(type(v['full_mode']) is int and 0 <= v['full_mode'] < 4096)

def current(obj, low):
    req(type(obj) is dict and set(obj) == {'schema','approved_by_root','created_utc','reason','current_head','files','operative_preparation_directory'})
    req(obj['schema'] == 'PR46_ROOT_FRESH13_INPUT_PREIMAGES_v1' and obj['approved_by_root'] is True)
    req(obj['operative_preparation_directory'] == 'current_preparation_family_v2')
    aware(obj['created_utc'], low)
    req(type(obj['reason']) is str and len(obj['reason'].strip()) >= 40)
    req(type(obj['current_head']) is str and re.fullmatch('[0-9a-f]{40}', obj['current_head']))
    req(type(obj['files']) is list and len(obj['files']) == 13)
    for row in obj['files']:
        native_row(row)
    req(rows([{k: row[k] for k in ('path','bytes','sha256')} for row in obj['files']]) == NATIVE)

def live(rows_, root, expected_head, actual_head, branch):
    req(branch == 'main' and actual_head == expected_head)
    for row in rows_:
        body = read(root/row['path'])
        req(len(body) == row['bytes'] and sha(body) == row['sha256'] and stat.S_IMODE((root/row['path']).stat().st_mode) == row['full_mode'])
        if row['path'].endswith('.json'):
            strict(body)
        elif row['path'].endswith('.jsonl'):
            for line in body.splitlines():
                req(line.strip())
                strict(line)

def child(cap, root, low=None):
    req(cap['actual_execution'] is True and cap['completed'] is True)
    req(type(cap['pid']) is int and cap['pid'] > 0 and type(cap['exit_code']) is int and cap['exit_code'] == 0)
    req(cap['stdin_supplied'] is False and cap['source_unchanged'] is True)
    req(cap['operator_pid'] == 62514 and cap['cwd'] == str(R))
    req(utc(cap['started_utc']) <= utc(cap['finished_utc']) <= dt.datetime.now(dt.timezone.utc))
    for k in ['source','copied_source','stdout','stderr']:
        rr = cap[k]
        rows([rr])
        req(rr['path'].startswith(A.relative_to(R).as_posix()+'/'))
        raw = read(root/rr['path'])
        req(len(raw) == rr['bytes'] and sha(raw) == rr['sha256'])

def summary(obj, author, independent, ledger):
    req(obj['schema'] == 'pr46-root-current-complete-reproduction-summary/v1')
    req(obj['status'] == 'PASS_ROOT_COMPLETED_FIRST_PARTY_REPRODUCTION')
    req(equal(obj['entire_author_result'], author) and equal(obj['entire_historical_independent_result'], independent) and equal(obj['complete_original_turns'], ledger))
    req(obj['future_acceptance_approved'] is False and obj['historical_failure_preserved'] is True and obj['foreign_primary_SQL_raw_cache_body_copy'] is False)
    req(obj['source_record_schema'] == 'plain_raw_problem_object' and obj['source_record_wrapper_claimed'] is False)
    req(obj['selected_prior_key_present'] is False and equal(obj['selected_prior_fallback'], {}))
    for k,v in [('original_substantive_attempts',0),('source_verification_responses',1),('new_substantive_attempts',0),('audit_turns',0)]:
        req(type(obj[k]) is int and obj[k] == v)
    req(type(obj['complete_helper_captures']) is list and len(obj['complete_helper_captures']) == 2)

def raw_audit(obj, source):
    req(obj['schema'] == 'pr46-root-in-place-complete-raw-sql-audit/v1' and obj['status'] == 'PASS_FULL_RAW_PRIOR_SQL_AND_ORIGINAL_PLAIN_SOURCE')
    req(type(obj['full_raw_and_prior_bytes']) is int and obj['full_raw_and_prior_bytes'] == 149266659)
    req(type(obj['all_SQL_rows']) is int and obj['all_SQL_rows'] == 15458 and len(obj['complete_row_bindings']) == 15458)
    req(obj['complete_saved_source_equals_raw_selected'] is True and obj['selected_prior_key_present'] is False and equal(obj['selected_prior_fallback'], {}))
    req(obj['raw_null_present'] is False and obj['raw_or_SQL_or_foreign_source_bodies_copied'] is False)
    req(equal(obj['original_native_selected_read']['complete_selected_problem'], source) and equal(obj['original_native_selected_read']['complete_selected_prior_report'], {}))

def main():
    req(not sys.flags.optimize)
    req(F.name == 'current_source_adversary_family_v2' and R == Path('/Users/alec/Documents/Math'))
    builder, operator = read(V/'prepare_current_packet.py').decode(), read(V/'capture_root_builder_operation.py').decode()
    check('operative builder pin', sha(builder.encode()) == SHA_BUILD)
    check('operative operator pin', sha(operator.encode()) == SHA_OPERATOR)
    prep = closed(V,'PREPARATION_MANIFEST.json',122)
    check('operative manifest pin', sha(read(V/'PREPARATION_MANIFEST.json')) == SHA_PREP)
    for rr in prep['files']:
        full_read(rr, 'current_preparation_family_v2/')
    full_read({'path':'current_preparation_family_v2/PREPARATION_MANIFEST.json','bytes':len(read(V/'PREPARATION_MANIFEST.json')),'sha256':SHA_PREP})
    # Source fragments are evidence of source placement only, never executed snippets.
    g = builder.split('    def git(*argv):',1)[1].split('    prep_raw=',1)[0]
    check('live inner finally chronology', g.index('        finally:') < g.index("(attempt/'GIT_COMMANDS.json').write_bytes(encode(commands))") < g.index('        return regular'))
    check('only complete outer postwait', operator.index("record['exit_code'] = child.wait(timeout=600)") < operator.index("(capture / 'CAPTURE.json').write_bytes(dump(record))"))
    check('operator never writes inner GIT_COMMANDS', 'GIT_COMMANDS' not in operator)
    for text in ["'final_inner_GIT_COMMANDS_written_incrementally_by_builder_before_exit':True", "'frozen_inner_command_copy_is_prepublication_prefix':True", "'outer_operator_does_not_write_inner_GIT_COMMANDS':True", "'ROOT_final_original_inner_commands_inspection_required_AFTER_child_exit':True", "'complete_outer_capture_written_only_after_child_exit':True", "'already_complete_outer_receipt_or_whole_PASS_certified':False"]:
        check('source chronology ' + text, text in builder)
    check('false V1 field removed from operative code', 'final_inner_GIT_COMMANDS_written_only_after_builder_exit' not in builder)
    for text in ["os.environ.get('PR46_ROOT_OUTER_CAPTURE','')", "outer['operator_pid']==os.getppid()", "outer['builder_sha256']==sha(regular(script))", "outer['operator_sha256']==sha(regular(script.parent/'capture_root_builder_operation.py'))", "outer['argv']==['/usr/bin/python3','-B',str(script),*sys.argv[1:]]", "outer['cwd']==str(repo)", "outer['schema']=='PR46_ROOT_BUILDER_PRELAUNCH_v2'", "PR46_ROOT_OUTER_CAPTURE=capture.relative_to(audit).as_posix()"]:
        check('parent source anchor ' + text, text in builder or text in operator)
    for text in ["'PR46_ROOT_ACTUAL_BUILDER_OPERATION_v2'", "family.name == 'current_preparation_family_v2'", "root_pr46_current_v2_outer_"]:
        check('operator V2 anchor ' + text, text in operator)
    for text in ["script.parent.name=='current_preparation_family_v2'", "root_pr46_current_v2_build_", "obj['operative_preparation_directory']=='current_preparation_family_v2'", "evidence['operative_preparation_directory']=='current_preparation_family_v2'", "current['operative_preparation_directory']=='current_preparation_family_v2'"]:
        check('builder V2 anchor ' + text, text in builder)
    for doc in ['EXECUTION_CONTRACT.md','CURRENT_OVERVIEW.md','SOURCE_PRECISION_QUALIFICATIONS.md','REPAIR_DECISION.md']:
        body = read(V/doc).decode()
        check('global chronology ' + doc, 'incrementally' in body and 'AFTER' in body and 'OUTER CAPTURE' in body)
    for n in ['DRAFT_ROOT_READ_LEDGER.json','DRAFT_ROOT_SCIENCE_CARD.json']:
        obj = strict(read(V/n))
        check('draft unapproved ' + n, obj['reading_completed'] is False and obj['created_utc'] is None and obj['preparation_manifest_sha256'] is None and all(v is False for v in obj['root_flags'].values()) and obj['operative_preparation_directory'] == 'current_preparation_family_v2')
    for n in ['DRAFT_ROOT_CURRENT_INPUT_PREIMAGES.json','DRAFT_ROOT_EVIDENCE_BINDINGS.json']:
        obj = strict(read(V/n))
        check('draft unapproved ' + n, obj['approved_by_root'] is False and obj['created_utc'] is None and obj['operative_preparation_directory'] == 'current_preparation_family_v2')
    check('no draft acceptance sentinel', 'ROOT_SCOPE_ACCEPTED_EXACT_KNOWN_RESULT_ONLY' not in read(V/'DRAFT_ROOT_CURRENT_KNOWN_RESULT_SCOPE_CERTIFICATE.md').decode())
    sc = strict(read(V/'DRAFT_ROOT_SCIENCE_CARD.json'))
    check('draft scientific/runtime fields honest', sc['exact_known_target_verified'] is False and sc['full_problem_solved'] is False and sc['full_target_prior_result_verified'] is False and all(sc[k] is False for k in ['project_solved','novelty_claimed','paper_created','new_DOI_created','tracker_row_created']) and all(sc[k] is None for k in ['current_model','current_reasoning_effort','current_deadline_utc','current_verdict']))
    for mode in range(4096):
        try:
            fullmode(mode)
            accepted = True
        except ValueError:
            accepted = False
        check('fullmode enumeration %04o' % mode, accepted == (mode == 0o444))
        row = {'path':'x','bytes':0,'sha256':'a'*64,'full_mode':mode}
        native_row(row)
        check('native fullmode range %04o' % mode, True)
    for mode in [-1,4096,8191,True,False,0.0,'0444',None]:
        bad('fullmode typed boundary '+repr(mode),fullmode,mode)
        bad('native mode typed boundary '+repr(mode),native_row,{'path':'x','bytes':0,'sha256':'a'*64,'full_mode':mode})
    work=F/('fixtures_'+dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')); work.mkdir(exist_ok=False)
    modefile=work/'mode'; modefile.write_bytes(b'private fixture\n')
    for mode in range(4096):
        modefile.chmod(mode)
        check('actual chmod full mode %04o' % mode, stat.S_IMODE(modefile.stat().st_mode) == mode)
    modefile.chmod(0o444)
    for n in ['x','a/b','a-.json','Unicode_α']:
        check('canonical positive '+n,canonical(n)==n)
    check('isolated lexical dot accepts then regular guard rejects',canonical('.')=='.')
    bad('dot directory cannot be a regular body',read,work/'.')
    for n in ['', './x', 'x/', 'a//b', '/x', '../x', 'a/../b', 'a/./b', '.git/x', '__pycache__/x', 'a\\b', 'a\0b', 7,True,None]:
        bad('canonical rejection '+repr(n),canonical,n)
    goodrow={'path':'x','bytes':0,'sha256':'a'*64}
    check('row positive',rows([goodrow])=={'x'})
    for field,values in [('path',['./x','../x','/x',True]),('bytes',[True,False,-1,0.0,'0',None]),('sha256',['A'*64,'a'*63,'g'*64,0,None])]:
        for v in values:
            row=dict(goodrow); row[field]=v
            bad('typed row '+field+' '+repr(v),rows,[row])
    bad('row duplicate',rows,[goodrow,goodrow])
    bad('row extra key',rows,[dict(goodrow,extra=False)])
    bad('rows not list',rows,tuple([goodrow]))
    for payload in [b'{"x":1,"x":2}',b'{"x":NaN}',b'{"x":Infinity}',b'{"x":1e10000}',b'{"x":{"a":1,"a":2}}',b'{',b'']:
        bad('strict JSON '+repr(payload),strict,payload)
    check('scalar token distinction',not equal({'x':0},{'x':False}) and not equal({'x':1},{'x':True}) and not equal({'x':1},{'x':1.0}) and not equal({},None))
    clean=work/'topology'; (clean/'sub').mkdir(parents=True); (clean/'sub'/'a').write_bytes(b'a')
    check('topology positive',tree(clean)=={'sub/a'})
    (clean/'empty').mkdir(); bad('empty directory rejected',tree,clean); (clean/'empty').rmdir()
    (clean/'link').symlink_to('sub/a'); bad('symlink member rejected',tree,clean); bad('regular symlink rejected',read,clean/'link'); (clean/'link').unlink()
    parent_alias=work/'parent_alias'; parent_alias.symlink_to(clean.name,target_is_directory=True)
    bad('symlink parent rejected',read,parent_alias/'sub'/'a'); parent_alias.unlink()
    os.mkfifo(clean/'fifo'); bad('special member rejected',tree,clean); (clean/'fifo').unlink()
    alias=work/'case_alias'; alias.mkdir(); (alias/'alpha').write_bytes(b'a')
    case_sensitive=not (alias/'ALPHA').exists()
    if case_sensitive:
        (alias/'ALPHA').write_bytes(b'b')
        check('case-sensitive distinct lexical files',tree(alias)=={'alpha','ALPHA'})
    else:
        try:
            with (alias/'ALPHA').open('xb') as out: out.write(b'b')
        except FileExistsError:
            check('casealias exclusive write prevents replacement',True)
        else:
            raise AssertionError('casealias replacement')
        bad('casealias fictitious exact manifest rejected',lambda: req(tree(alias)=={'alpha','ALPHA'}))
    testroot=work/'self_closure'; testroot.mkdir(); (testroot/'file').write_bytes(b'file'); (testroot/'file').chmod(0o444)
    m={'self_excluded':['MANIFEST.json'],'files_count':1,'files':[{'path':'file','bytes':4,'sha256':sha(b'file')}]}
    (testroot/'MANIFEST.json').write_bytes(dump(m)); (testroot/'MANIFEST.json').chmod(0o444)
    check('self-only closure positive',closed(testroot,'MANIFEST.json',1)['files_count']==1)
    for key,value in [('self_excluded',['MANIFEST.json','OTHER']),('files_count',True),('files_count',0),('files',[])]:
        mutated=copy.deepcopy(m); mutated[key]=value; (testroot/'MANIFEST.json').chmod(0o644); (testroot/'MANIFEST.json').write_bytes(dump(mutated)); (testroot/'MANIFEST.json').chmod(0o444)
        bad('closure mutation '+key+' '+repr(value),closed,testroot,'MANIFEST.json',1)
    (testroot/'MANIFEST.json').chmod(0o644); (testroot/'MANIFEST.json').write_bytes(dump(m)); (testroot/'MANIFEST.json').chmod(0o444)
    (testroot/'file').chmod(0o644); bad('writable member rejected',closed,testroot,'MANIFEST.json',1); (testroot/'file').chmod(0o444)
    (testroot/'MANIFEST.json').chmod(0o644); bad('writable self manifest rejected by private closure',closed,testroot,'MANIFEST.json',1); (testroot/'MANIFEST.json').chmod(0o444)
    (testroot/'extra').write_bytes(b'x'); bad('extra closure member rejected',closed,testroot,'MANIFEST.json',1); (testroot/'extra').unlink()
    # A private absent-only publication exercises the same documented OS primitive.
    req(sys.platform=='darwin'); libc=ctypes.CDLL(None,use_errno=True); rename=libc.renamex_np
    rename.argtypes=[ctypes.c_char_p,ctypes.c_char_p,ctypes.c_uint]; rename.restype=ctypes.c_int
    src=work/'exclusive_source'; dst=work/'exclusive_destination'; src.mkdir(); (src/'member').write_bytes(b'original')
    check('actual exclusive rename absent',rename(os.fsencode(src),os.fsencode(dst),4)==0 and read(dst/'member')==b'original')
    src.mkdir(); (src/'other').write_bytes(b'attempt')
    check('actual exclusive rename refuses destination',rename(os.fsencode(src),os.fsencode(dst),4)!=0 and read(dst/'member')==b'original' and read(src/'other')==b'attempt')
    nativefixture=work/'native'; nativefixture.mkdir()
    rr=[]
    for n in sorted(NATIVE):
        path=nativefixture/n; path.parent.mkdir(parents=True,exist_ok=True)
        body=b'{}\n' if n.endswith(('.json','.jsonl')) else b'private\n'
        path.write_bytes(body); rr.append({'path':n,'bytes':len(body),'sha256':sha(body),'full_mode':0o644})
    low=prep['utc']; now=dt.datetime.now(dt.timezone.utc).isoformat()
    fresh={'schema':'PR46_ROOT_FRESH13_INPUT_PREIMAGES_v1','approved_by_root':True,'created_utc':now,'reason':'Private fixture only; no real ROOT approval or future native authority.','current_head':'a'*40,'files':rr,'operative_preparation_directory':'current_preparation_family_v2'}
    current(fresh,low); check('private exact13 current fixture',True)
    live(rr,nativefixture,'a'*40,'a'*40,'main'); check('wholefile/fullmode/currentHEAD positive fixture',True)
    for key,val in [('approved_by_root',False),('approved_by_root',1),('created_utc',None),('created_utc','2000-01-01T00:00:00+00:00'),('created_utc','2999-01-01T00:00:00+00:00'),('current_head','A'*40),('operative_preparation_directory','current_preparation_family'),('files',rr[:-1]),('files',rr+[rr[0]])]:
        obj=copy.deepcopy(fresh); obj[key]=val; bad('fresh13 mutation '+key+' '+repr(val)[:80],current,obj,low)
    duplicate=copy.deepcopy(fresh); duplicate['files'][-1]=duplicate['files'][0]; bad('fresh13 duplicate substitution',current,duplicate,low)
    extra=copy.deepcopy(fresh); extra['future_merge_approved']=True; bad('fresh13 extra future approval',current,extra,low)
    for args in [('a'*40,'b'*40,'main'),('a'*40,'a'*40,'other')]:
        bad('native head/branch changed '+str(args),live,rr,nativefixture,*args)
    chosen=nativefixture/rr[0]['path']; body=read(chosen); chosen.write_bytes(body+b'x'); bad('native appended body rejected',live,rr,nativefixture,'a'*40,'a'*40,'main'); chosen.write_bytes(body)
    chosen.chmod(0o1644); bad('native special fullmode rejected',live,rr,nativefixture,'a'*40,'a'*40,'main'); chosen.chmod(0o644)
    for n in ['DRAFT_ROOT_CURRENT_INPUT_PREIMAGES.json']:
        bad('real false/null draft cannot authorize current',current,strict(read(V/n)),low)
    pins=strict(read(V/'STATIC_INPUT_BINDINGS.json'))
    for key in ['snapshot_manifest','original_metadata','original_preparation_manifest']:
        full_read(pins[key])
    for key in ['original_preparation_members','original_separate_closure_capture','genuine_closed_ROOT_evidence_fixed_rows','superseded_v1_closed_source_rows']:
        for rr_ in pins[key]: full_read(rr_)
    original_manifest=strict(read(A/'ORIGINAL_PREPARATION_MANIFEST.json'))
    check('original scoped318+self exact',original_manifest['self_excluded']==['ORIGINAL_PREPARATION_MANIFEST.json'] and original_manifest['files_count']==318 and len(original_manifest['files'])==318)
    actual=set(original_manifest['authorship_root_files'])
    for root in original_manifest['authorship_directory_roots']: actual |= {root+'/'+n for n in tree(A/root)}
    check('original authored topology excludes siblings',actual=={v['path'] for v in original_manifest['files']}=={v['path'] for v in pins['original_preparation_members']})
    for family,info in pins['families'].items():
        for rr_ in info['members']+info['separate_excluded_closure']: full_read(rr_,family+'/')
        full_read(info['manifest'],family+'/')
        closed(A/family,info['manifest']['path'],len(info['members']),info['manifest_self_excluded'][1:])
        check('family exact topology '+family,tree(A/family)=={v['path'] for v in info['members']+info['separate_excluded_closure']}|{info['manifest']['path']})
        dirs={p.relative_to(A/family).as_posix() for p in (A/family).rglob('*') if p.is_dir()}
        check('family directory topology '+family,dirs==set(info['directories'])==set(info['directory_modes']))
        check('family full directory modes '+family,all(stat.S_IMODE((A/family/n).stat().st_mode)==mode for n,mode in info['directory_modes'].items()))
    check('projective34+5 separate',len(pins['families']['projective_algebra_family']['members'])==34 and len(pins['families']['projective_algebra_family']['separate_excluded_closure'])==5)
    check('complex33 closure included',len(pins['families']['complex_dynamics_family']['members'])==33 and not pins['families']['complex_dynamics_family']['separate_excluded_closure'])
    snap=strict(read(A/'snapshot_manifest.json'))
    check('original13 exact tree',tree(A/'source_snapshot')=={v['relative_path'] for v in snap['files']} and len(snap['files'])==13)
    check('source science exact',sha(read(A/'source_snapshot/SOURCE_STATUS.md'))=='a0d374da6984537cd9902e2e790177791739bdc32ea820b74830a6b50241ea6c')
    for v in snap['files']:
        full_read({'path':'source_snapshot/'+v['relative_path'],'bytes':v['bytes'],'sha256':v['sha256']}); fullmode(stat.S_IMODE((A/'source_snapshot'/v['relative_path']).stat().st_mode))
        check('snapshot Git identity '+v['relative_path'],v['git_mode']=='100644' and v['snapshot_mode']=='0444' and bool(re.fullmatch('[a-f0-9]{40}',v['git_object'])))
    meta=strict(read(A/'original_pr_metadata.json')); dif=full_read(meta['full_diff'])
    check('complete original14 diff bound',len(dif)==89103 and sha(dif)=='944d6ac424b3e6fa6d4ccf163e6b381352072589528a3a5a29b146454e458209' and meta['changed_files']==14 and len(meta['all_changed_paths'])==14)
    author=strict(read(A/'source_snapshot/verification.json')); independent=strict(read(A/'source_snapshot/independent_review/independent_results.json')); ledger=strict(read(A/'source_snapshot/turns.json')); source=strict(read(A/'source_snapshot/source_record.json'))
    for receipt,num in [(author,51),(independent,848)]:
        check('full literal receipt '+str(num),type(receipt['passed']) is int and receipt['passed']==num and type(receipt['failed']) is int and receipt['failed']==0 and type(receipt['checks']) is dict and len(receipt['checks'])==num and all(v=='PASS' for v in receipt['checks'].values()))
    check('original object ledger0/5 plus source1',type(ledger) is dict and type(ledger['substantive_turns_used']) is int and ledger['substantive_turns_used']==0 and type(ledger['source_verification_responses']) is int and ledger['source_verification_responses']==1 and type(ledger['turn_limit']) is int and ledger['turn_limit']==5)
    repro=closed(A/'root_original_actual_reproduction_v2','MANIFEST.json',37)
    check('ROOT reproduction no future approval',repro['future_acceptance_approved'] is False and repro['foreign_primary_raw_SQL_cache_bodies_copied'] is False)
    for rr_ in repro['files']: full_read(rr_,'root_original_actual_reproduction_v2/')
    s=strict(read(A/'root_original_actual_reproduction_v2/ROOT_CURRENT_REPRODUCTION_SUMMARY.json')); summary(s,author,independent,ledger); check('entire actual ROOT result/ledger source verification',True)
    for cap in s['complete_helper_captures']: child(cap,R); check('actual bound child '+str(cap['pid']),True)
    for key,val in [('future_acceptance_approved',True),('source_record_wrapper_claimed',True),('selected_prior_key_present',True),('selected_prior_fallback',None),('source_verification_responses',True),('complete_original_turns',{'substantive_turns_used':0}),('entire_author_result',{'passed':51,'failed':0}),('entire_historical_independent_result',{'passed':848,'failed':0}),('complete_helper_captures',s['complete_helper_captures'][:1])]:
        obj=copy.deepcopy(s); obj[key]=val; bad('ROOT summary mutation '+key,summary,obj,author,independent,ledger)
    for key,val in [('pid',True),('pid',0),('exit_code',False),('completed',False),('actual_execution',False),('operator_pid',0),('cwd','/tmp'),('source_unchanged',False),('finished_utc','2000-01-01T00:00:00+00:00')]:
        obj=copy.deepcopy(s['complete_helper_captures'][0]); obj[key]=val; bad('actual capture mutation '+key+' '+repr(val),child,obj,R)
    check('actual ROOT author bytes',read(A/'root_original_actual_reproduction_v2/author/verification.json')==read(A/'source_snapshot/verification.json'))
    check('actual ROOT independent bytes',read(A/'root_original_actual_reproduction_v2/historical_independent/independent_results.json')==read(A/'source_snapshot/independent_review/independent_results.json'))
    raw=strict(read(A/'ROOT_COMPLETE_RAW_SQL_AUDIT.json')); raw_audit(raw,source); check('raw absence/not-null/plain-record entire bindings',True)
    for k,v in [('selected_prior_key_present',True),('selected_prior_fallback',None),('raw_null_present',True),('all_SQL_rows',True),('complete_row_bindings',raw['complete_row_bindings'][:-1]),('raw_or_SQL_or_foreign_source_bodies_copied',True)]:
        obj=copy.deepcopy(raw); obj[k]=v; bad('raw audit mutation '+k,raw_audit,obj,source)
    old=closed(A/'current_preparation_family','PREPARATION_MANIFEST.json',60)
    oldroot=A/'current_preparation_family'; archive=V/'superseded_v1_source_archive'
    check('literal V1 archive exact topology',tree(oldroot)==tree(archive))
    check('literal V1 archive entire bodies unchanged',all(read(oldroot/n)==read(archive/n) for n in tree(oldroot)))
    external=A/'current_preparation_v2_closure_actual_capture'
    cap=strict(read(external/'CAPTURE.json')); pre=strict(read(external/'PRELAUNCH.json'))
    check('real external V2 closure child10748',cap['pid']==10748 and cap['actual_execution'] is True and cap['completed'] is True and type(cap['exit_code']) is int and cap['exit_code']==0 and cap['stdin_supplied'] is False)
    check('real external V2 closure chronology',cap['started_utc']=='2026-10-03T04:48:28.741755+00:00' and cap['finished_utc']=='2026-10-03T04:48:28.922890+00:00' and utc(cap['started_utc'])<=utc(prep['utc'])<=utc(cap['finished_utc']))
    check('V2 manifest real closing child anchor',prep['actual_closure_pid']==cap['pid'])
    for channel in ['stdout','stderr']:
        v=cap[channel]; raw_=read(external/v['path']); check('external V2 complete stream '+channel,len(raw_)==v['bytes'] and sha(raw_)==v['sha256'])
    check('external capture honest prelaunch flags',pre['actual_execution'] is False and pre['pid'] is None and pre['completed'] is False and pre['exit_code'] is None)
    check('external operator preserved source',sha(read(external/'prelaunch_operator.py'))==cap['operator_sha256'])
    # Current native bytes are read in place; no cache, SQLite or foreign body is staged.
    fingerprints=[]
    for n in sorted(NATIVE):
        raw_=read(R/n); fingerprints.append({'path':n,'bytes':len(raw_),'sha256':sha(raw_),'full_mode':stat.S_IMODE((R/n).stat().st_mode)})
    (F/'CURRENT_NATIVE_FINGERPRINTS.json').write_bytes(dump({'phase':'SOURCE_READING_ONLY_NO_AUTHORITY','files':fingerprints,'native_body_copy':False,'future_acceptance_approved':False}))
    for n in ['CURRENT_OVERVIEW.md','SOURCE_PRECISION_QUALIFICATIONS.md']:
        text=read(V/n).decode()
        check('bounded credited known result '+n,'Kozhasov' in text and 'Kummer' in text and 'preprint' in text and '2d+1' in text and 'every' in text and 'all' in text and 'no new discovery' in text.lower() if n=='CURRENT_OVERVIEW.md' else 'Campaign novelty and new-discovery credit are zero.' in text)
    # Complete byte inspection != a fresh review of every unrelated historical semantic claim.
    result={'schema':'PR46_INDEPENDENT_V2_SOURCE_PRIVATE_CONTROLS_v1','utc':dt.datetime.now(dt.timezone.utc).isoformat(),'assertions_passed':len(ASSERTIONS),'assertion_labels':ASSERTIONS,'failed':0,'all4096_permissions_logically_and_actual_chmod_tested':True,'case_sensitive_fixture_filesystem':case_sensitive,'fixed_full_body_reads_unique':len(READS),'complete_fixed_member_reads':sorted(READS.values(),key=lambda v:v['path']),'production_import_compile_execute':False,'canonical_native_Git_index_remote_mutation':False,'ROOT_runtime_or_future_merge_certified':False,'foreign_raw_bodies_staged':False}
    (F/'PRIVATE_CONTROL_RESULTS.json').write_bytes(dump(result))
    print(json.dumps({'status':'PASS_PRIVATE_SOURCE_PREDICATES_ONLY','assertions_passed':len(ASSERTIONS),'fixed_unique_full_body_reads':len(READS),'case_sensitive_fixture_filesystem':case_sensitive,'production_executed':False,'future_acceptance_approved':False},sort_keys=True))

if __name__ == '__main__':
    main()
