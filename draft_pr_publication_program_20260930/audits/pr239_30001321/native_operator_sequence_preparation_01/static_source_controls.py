"""Static source/argument controls only; never imports or invokes any engine module."""
import ast,hashlib,json,re,stat,sys
from pathlib import Path
BASE=Path(__file__).absolute().parent
E=BASE.parent/'operational_source_preparation_01'
def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def check(ok,name):
    if type(ok) is not bool or not ok:raise RuntimeError('Static control failed: '+name)
    checks.append(name)
checks=[]
def node_file(path):return ast.parse(path.read_bytes(),filename=str(path))
def named(tree,name):return next(x for x in tree.body if isinstance(x,(ast.FunctionDef,ast.ClassDef)) and x.name==name)
def astpin(node):return pin(ast.dump(node,include_attributes=False).encode())
def literals(tree):return {x.value for x in ast.walk(tree) if isinstance(x,ast.Constant) and type(x.value) is str}
def assignment(tree,name):
    x=next(x for x in tree.body if isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in x.targets))
    return ast.literal_eval(x.value)
def run():
    check(sys.flags.ignore_environment==1 and sys.flags.no_site==1 and sys.dont_write_bytecode is True and sys.flags.safe_path is True and sys.flags.optimize==0,'ordinary isolated nonoptimized Python flags')
    contract=json.loads((BASE/'ARGUMENT_CONTRACT.json').read_bytes())
    provenance=json.loads((BASE/'AST_PROVENANCE.json').read_bytes())
    references=json.loads((BASE/'REFERENCE_PINS.json').read_bytes())
    check(contract['source_only'] is True and contract['operational_authority'] is False and contract['no_actual_command_or_Root_gate'] is True,'documentary source-only contract')
    check(provenance['no_new_operational_wrapper'] is True and provenance['no_engine_source_modified'] is True,'no new operational wrapper')
    check(len(references['references'])==15,'finite positive references')
    for row in references['references']:
        p=Path(row['path']);s=p.lstat()
        check(p.is_absolute() and p.resolve()==p and stat.S_ISREG(s.st_mode) and stat.S_IMODE(s.st_mode)==0o444 and pin(p.read_bytes())=={k:row[k] for k in ('bytes','sha256')},'reference '+p.name+' in '+p.parent.name)
    manifest=json.loads((E/'SOURCE_MANIFEST.json').read_bytes())
    check(len(manifest['files'])==19 and manifest['source_only'] is True,'unchanged engine positive19')
    for row in manifest['files']:
        p=E/row['path']
        check(p.parent==E and pin(p.read_bytes())=={k:row[k] for k in ('bytes','sha256')} and stat.S_IMODE(p.lstat().st_mode)==0o444,'engine body '+p.name)
    trees={fn:node_file(E/fn) for fn in provenance['current_symbols']}
    for fn,rows in provenance['current_symbols'].items():
        for row in rows:
            node=named(trees[fn],row['name'])
            check(astpin(node)==row['AST_pin'] and node.lineno==row['first_line'] and node.end_lineno==row['last_line'],'current AST '+fn+':'+row['name'])
    for row in provenance['prior_218_symbol_comparisons']:
        nt=node_file(Path(row['new_source']));ot=node_file(Path(row['old_source']))
        nn=named(nt,row['symbol']);old=[x for x in ot.body if isinstance(x,(ast.FunctionDef,ast.ClassDef)) and x.name==row['symbol']]
        check(astpin(nn)==row['new_AST_pin'],'new comparison AST '+row['symbol'])
        if not old:
            check(row['old_symbol_absent'] is True and row['old_AST_pin'] is None and row['exact_AST_equal'] is False and row['only_explicit_PR_namespace_normalization_equal'] is False,'honest added symbol '+row['symbol'])
        else:
            a=ast.dump(old[0],include_attributes=False);b=ast.dump(nn,include_attributes=False)
            n=a.replace('PR218','PR239').replace('pr218','pr239').replace('COMPLETE218','COMPLETE239').replace('native218','native239')
            check(pin(a.encode())==row['old_AST_pin'] and row['old_symbol_absent'] is False and row['exact_AST_equal']==(a==b) and row['only_explicit_PR_namespace_normalization_equal']==(n==b),'honest prior comparison '+row['symbol'])
    ext=trees['concurrent_get_extension.py'];driver=trees['completion_checkpoint.py'];terminal=trees['ROOT_TERMINAL_INSPECTION.py']
    operations=assignment(ext,'OPERATIONS')
    check(operations=={'candidate','verify','hold-CAS','sync','terminal'},'exact direct extension operations')
    extmain=named(ext,'main');extstrings=literals(extmain)
    loop=next(x for x in ast.walk(extmain) if isinstance(x,ast.For) and isinstance(x.target,ast.Name) and x.target.id=='name')
    refnames=ast.literal_eval(loop.iter)
    check(refnames==('manifest','logical-gate','admission','admission-gate','extension-acceptance','actual-CAS','preCAS-acceptance'),'extension reference flag spelling')
    expected_extensions={
      'candidate':{'manifest','logical-gate','admission','admission-gate','extension-acceptance'},
      'verify':{'manifest','logical-gate','admission','admission-gate','extension-acceptance'},
      'hold-CAS':{'manifest','logical-gate','admission','admission-gate','extension-acceptance','preCAS-acceptance'},
      'sync':{'manifest','logical-gate','admission','admission-gate','extension-acceptance','actual-CAS'},
      'terminal-readout':{'manifest','logical-gate','admission','admission-gate','extension-acceptance','actual-CAS'}}
    ops=contract['operations']
    check(set(ops)==set(expected_extensions)|{'admit','external-Root-terminal'},'finite positive operation recipes')
    for op,row in ops.items():
        t=row['tokens']
        check(t[:5]==['/opt/homebrew/bin/python3.11','-E','-S','-B','-P'] and t[5]=='<E>/'+row['entry'],'direct interpreter token prefix '+op)
        check(all(type(x) is str and '\n' not in x and '\0' not in x for x in t),'finite one-argument tokens '+op)
        check('--phase' not in t and '--force' not in t and '--expected-sha' not in t,'no invented CLI/ref flag '+op)
        if op in expected_extensions:
            check(row['entry']=='concurrent_get_extension.py' and t[6]==('terminal' if op=='terminal-readout' else op) and t[6] in operations,'exact accepted direct action '+op)
            flags={x[2:] for x in t if x.startswith('--') and not x.endswith(('-bytes','-sha256'))}
            check(flags==expected_extensions[op]|(set() if op=='candidate' else {'journal'}),'exact minimal ref/journal flags '+op)
        for i,x in enumerate(t):
            if x.startswith('--') and x.endswith('-bytes'):
                stem=x[:-6];j=t.index(stem)
                check(i==j+2 and t[i+2]==stem+'-sha256' and t[j+1].endswith('.path>') and t[i+1].endswith('.bytes>') and t[i+3].endswith('.sha256>'),'exact full reference triplet '+op+':'+stem)
    check('--journal' not in ops['candidate']['tokens'],'candidate uses only admitted journal')
    check('--Root-gate' in ops['external-Root-terminal']['tokens'] and '--admission-gate' not in ops['external-Root-terminal']['tokens'],'inspector Root-gate spelling')
    check('--Root-gate' not in ops['admit']['tokens'] and set(ops['admit']['references'])=={'M','LG'},'admit before Runtime has only seed refs')
    check(ops['external-Root-terminal']['action'] is None and ops['external-Root-terminal']['phase_only']=='completion100','external inspector not lower-case terminal action')
    check('--extension-source' in ops['external-Root-terminal']['tokens'] and '--extension-acceptance' in ops['external-Root-terminal']['tokens'],'paired explicit inspector extension transport')
    check('--source-acceptance' in ops['external-Root-terminal']['tokens'] and ops['external-Root-terminal']['tokens'][-1]=='ROOT_ACTUAL_COMPLETION_VERIFICATION_01.json','separate inspector source gate and fixed receipt')
    phases=contract['phase_contracts']
    check(set(phases)=={'merge95','completion100'},'exact two phase documents')
    for phase,label in [('merge95','M95'),('completion100','C100')]:
        p=phases[phase]
        check(p['actual_pointer']==str(E/('ROOT_ACTUAL_'+phase.upper()+'_POINTER.json')),'exact distinct phase pointer '+phase)
        for key,name in p['example_journals'].items():
            check(name.startswith('ROOT_COMPLETE239_') and label in name and re.fullmatch('[A-Za-z0-9_-]+',name) is not None,'owned phase-specific journal '+phase+':'+key)
            if key=='ROOT_TERMINAL_JOURNAL':check(re.fullmatch('ROOT_COMPLETE239_READ_ROOT_TERMINAL_[A-Za-z0-9_-]{1,35}',name) is not None,'bounded exact terminal journal')
            elif key=='SYNC_JOURNAL':check(name.startswith('ROOT_COMPLETE239_SYNC_FAST_'),'accepted extension sync journal')
            elif key in ('READ_ADMIT_JOURNAL','ADMITTED_CANDIDATE_JOURNAL'):check(name.startswith('ROOT_COMPLETE239_READ_') if key=='READ_ADMIT_JOURNAL' else name.startswith('ROOT_COMPLETE239_CANDIDATE_'),'accepted admission journals '+phase+':'+key)
            else:check(name.startswith('ROOT_COMPLETE239_FAST_READ_'),'accepted read/hold journal '+phase+':'+key)
    check(phases['merge95']['held_counts']==[55,39] and phases['merge95']['last_completed_PR']==218 and phases['merge95']['current_numeric_cursor']==239 and phases['merge95']['advance_to240'] is False,'phase95 conservative facts')
    check(phases['completion100']['conditional_counts']==[56,40] and phases['completion100']['conditional_last_completed_PR']==239 and phases['completion100']['conditional_numeric_cursor']==240 and phases['completion100']['advance_to240_before_actual_external_terminal'] is False,'phase100 conditional facts only')
    check(len(phases['merge95']['ordered_parents'])==2 and len(phases['completion100']['ordered_parents'])==1,'different phase parent cardinalities')
    maincalls={ast.unparse(x.func) for x in ast.walk(extmain) if isinstance(x,ast.Call)}
    check({'source_module','q.Seed','q.Runtime','bind_runtime','q.hold_CAS','q.sync'}.issubset(maincalls),'direct accepted CLI constructs inherited exact paths')
    hold=named(driver,'hold_CAS');calls={ast.unparse(x.func) for x in ast.walk(hold) if isinstance(x,ast.Call)}
    check({'rt.e.WriterLock','wait_actual_CAS_reference','sys.stdin.fileno','actual_cas','lock.check'}.issubset(calls),'direct original stdin and stable held lock')
    check(not any(x.startswith(('subprocess.','os.exec','os.fork')) for x in maincalls|calls),'no intermediary subprocess or stdin forwarder in direct hold route')
    wait=named(driver,'wait_actual_CAS_reference');text=ast.unparse(wait)
    check('180' in text and '4096' in text and 'Queued excess after Root CAS reference refused' in text,'original180sec4096byte and queued excess guards')
    context=named(terminal,'context');contexttext=ast.unparse(context)
    check('ROOT_ACTUAL_COMPLETION100_POINTER.json' in contexttext and "rt.m['phase'] == 'completion100'" in contexttext,'external inspector exact100 pointer and phase')
    check('ROOT_COMPLETE239_FAST_READ_' in extstrings and 'ROOT_COMPLETE239_SYNC_FAST_' in extstrings,'source-reviewed direct journal prefixes')
    check(assignment(ext,'PROTOCOL_PIN')==pin((E/'completion_checkpoint.py').read_bytes()),'extension pins exact current driver')
    print(json.dumps({'schema':'pr239-native-operator-static-control-results-v1','source_only':True,'checks':len(checks),'all_passed':True,'names':checks,'engine_modules_imported_or_executed':False,'Seed_Runtime_extension_guard_GET_POST_lock_provider_tracker_PR_five_intake_or_Git_actions':False},sort_keys=True,indent=2))
if __name__=='__main__':run()
