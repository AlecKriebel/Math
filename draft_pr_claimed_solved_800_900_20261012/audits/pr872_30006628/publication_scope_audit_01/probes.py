#!/usr/bin/env python3
"""Offline helper audit. Every helper subprocess is replaced; no live Git/gh calls.
Run with python3 -I -B probes.py, and separately with -I -B -O.
"""
import argparse, ast, contextlib, copy, datetime, hashlib, importlib.util, io, json
from pathlib import Path
import subprocess, sys, tempfile, types

HERE = Path(__file__).resolve().parent
PROGRAM = HERE.parents[2]
QUEUE = 'unsolved_math_prioritization/QUEUE.md'
LEGACY = 'random_property_t_30006628/'
DEFAULT = 'unsolved_math_prioritization/attempts/30006628/'
DOI = 'https://doi.org/10.5281/zenodo.99999999'
CHECKS = []

def check(ok, message):
    if not ok:
        raise RuntimeError('PROBE FAILURE: ' + message)
    CHECKS.append(message)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def qrow(pid, status='claimed_solved', doi='', ending='\n'):
    return '| ' + ' | '.join(['rank', str(pid)+' / AMR-fixture', 'title', 'x', 'x', 'x', 'x', status, '3/5', 'x', 'old findings', doi]) + ' |' + ending

def queue(pid, status='claimed_solved', doi='', ending='\n'):
    return 'untouched header\n' + qrow(pid,status,doi,ending) + qrow(777777,'unsolved','', '\r\n') + 'untouched footer\n'

class MockCLI:
    """In-memory Git object/tree model and GitHub snapshot, with deny-by-default CLI."""
    def __init__(self,pid,kind,config=None):
        self.config=config or {}; self.pid=pid; self.kind=kind
        self.calls=[]; self.objects={}; self.trees={}; self.commits={}
        self.head='1'*40; self.base='2'*40; self.merged='3'*40
        self.snap_head=self.config.get('head',self.head)
        self.old_queue=queue(pid,self.config.get('head_status','claimed_solved'))
        self.main_queue=queue(pid,self.config.get('main_status','claimed_solved'),self.config.get('main_doi',''),self.config.get('ending','\n'))
        if self.config.get('duplicate_row'):
            self.main_queue += qrow(pid)
        if self.config.get('missing_row'):
            self.main_queue=queue(12345)
        oldentries={QUEUE:('100644','blob',self.blob(self.old_queue.encode()))}
        entries={QUEUE:('100644','blob',self.blob(self.main_queue.encode())),
           'foreign/executable':('100755','blob',self.blob(b'executable')),
           'foreign/link':('120000','blob',self.blob(b'elsewhere')),
           'foreign/nonutf_\udcff':('100644','blob',self.blob(b'foreign bytes')),
           'foreign/submodule':('160000','commit','4'*40),
           'foreign/nested tab\tname':('100644','blob',self.blob(b'foreign tab')),
           LEGACY+'core.txt':('100644','blob',self.blob(b'accepted core')),
           DEFAULT+'core.txt':('100644','blob',self.blob(b'accepted core'))}
        self.initial_flat=copy.deepcopy(entries)
        self.commits[self.head]=self.build(oldentries)
        self.commits[self.base]=self.build(entries)
        self.initial_root=self.commits[self.base]
        self.last_commit=None; self.last_updates=None
        self.sentinels={'HEAD':'ref: refs/heads/main','index':b'unchanged index','working':b'foreign dirty bytes'}
        self.original_sentinels=copy.deepcopy(self.sentinels)
    def object(self,kind,raw):
        oid=hashlib.sha1(kind.encode()+b' '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        self.objects[oid]=(kind,raw);return oid
    def blob(self,raw):return self.object('blob',raw)
    def tree(self,entries):
        sorted_entries=sorted(entries.items(), key=lambda item:item[0]+(b'/' if item[1][1]=='tree' else b''))
        raw=b''.join((b'40000' if mode=='040000' else mode.encode())+b' '+name+b'\0'+bytes.fromhex(oid) for name,(mode,kind,oid) in sorted_entries)
        oid=self.object('tree',raw);self.trees[oid]=dict(entries);return oid
    def build(self,flat):
        root={}
        for path,entry in flat.items():
            node=root;parts=path.split('/')
            for part in parts[:-1]:node=node.setdefault(part,{})
            node[parts[-1]]=entry
        def rec(node):
            return self.tree({name.encode('utf-8','surrogateescape'):('040000','tree',rec(value)) if isinstance(value,dict) else value for name,value in node.items()})
        return rec(root)
    def flatten(self,oid,prefix=''):
        oid=self.commits.get(oid,oid);flat={}
        for rawname,(mode,kind,obj) in self.trees[oid].items():
            name=rawname.decode('utf-8','surrogateescape');path=prefix+name
            if kind=='tree':flat.update(self.flatten(obj,path+'/'))
            else:flat[path]=(mode,kind,obj)
        return flat
    def check_output(self,argv,cwd=None,env=None,input=None,text=False,**kwargs):
        self.calls.append(list(argv))
        if argv[0]=='gh':
            if argv[:3]!=['gh','pr','view']:raise RuntimeError('Forbidden gh operation')
            requested=argv[-1]
            if requested=='headRefOid': result={'headRefOid':self.last_commit or self.snap_head}
            elif requested=='state,mergeCommit':result={'state':self.config.get('merged_state','MERGED'),'mergeCommit':{'oid':self.merged}}
            elif requested=='headRefOid,headRefName,state,isDraft': result={'headRefOid':self.snap_head,'headRefName':'draft/fixture','state':self.config.get('pr_state','OPEN'),'isDraft':self.config.get('draft',True)}
            else:raise RuntimeError('Unknown gh read')
            raw=json.dumps(result).encode()
        elif argv[0]=='git':
            a=argv[1:]; op=a[0]
            if op=='fetch':
                if a!=['fetch','--no-tags','origin','main']:raise RuntimeError('Unexpected fetch')
                raw=b''
            elif op=='rev-parse':
                if a[1]=='origin/main':raw=self.base.encode()+b'\n'
                elif a[1].endswith('^{tree}'):
                    raw=self.commits.get(a[1][:-7],a[1][:-7]).encode()+b'\n'
                else:raise RuntimeError('Unknown revision')
            elif op=='show':
                rev,path=a[1].split(':',1); entry=self.flatten(rev).get(path)
                if entry is None:raise RuntimeError('Fixture path absent: '+path)
                raw=self.objects[entry[2]][1]
            elif op=='cat-file':
                raw=self.objects[a[2]][0].encode()+b'\n'
            elif op=='ls-tree':
                oid=a[-1]
                raw=b''.join(mode.encode()+b' '+kind.encode()+b' '+obj.encode()+b'\t'+name+b'\0' for name,(mode,kind,obj) in self.trees[oid].items())
            elif op=='mktree':
                entries={}
                for row in input.split(b'\0'):
                    if not row:continue
                    header,name=row.split(b'\t',1);mode,kind,obj=header.decode().split(' ')
                    entries[name]=(mode,kind,obj)
                raw=self.tree(entries).encode()+b'\n'
            elif op=='hash-object':
                if '--stdin' in a:
                    data=input.encode() if isinstance(input,str) else input
                    raw=self.blob(data).encode()+b'\n'
                else:
                    names=a[a.index('--')+1:]
                    raw=b''.join(self.blob(Path(name).read_bytes()).encode()+b'\n' for name in names)
            elif op=='diff-tree':
                before,after=self.flatten(a[-2]),self.flatten(a[-1])
                changed=sorted(path for path in before.keys()|after.keys() if before.get(path)!=after.get(path))
                raw=('\n'.join(changed)+ ('\n' if changed else '')).encode()
            elif op=='commit-tree':
                tree=a[1]; parents=[a[i+1] for i,x in enumerate(a) if x=='-p']
                payload=(tree+' '+','.join(parents)+' '+str(input)).encode()
                commit=self.object('commit',payload);self.commits[commit]=tree
                self.last_commit=commit;self.last_parents=parents;raw=commit.encode()+b'\n'
            else:raise RuntimeError('Denied unimplemented git operation: '+repr(a))
        else:raise RuntimeError('Denied external executable: '+repr(argv))
        return raw.decode() if text else raw
    def run(self,argv,cwd=None,check=False,capture_output=False,text=False,**kwargs):
        self.calls.append(list(argv))
        if argv[:3]==['git','merge-base','--is-ancestor']:
            return types.SimpleNamespace(returncode=1 if self.config.get('not_ancestor') else 0,stdout='',stderr='')
        if argv[:3]==['git','push','origin']:
            if self.config.get('push_failure'):
                if check:raise subprocess.CalledProcessError(1,argv)
                return types.SimpleNamespace(returncode=1,stdout='',stderr='unknown failure; do not retry')
            return types.SimpleNamespace(returncode=0,stdout='',stderr='')
        raise RuntimeError('Denied subprocess.run operation: '+repr(argv))

def load(kind,variant,fake,workspace):
    name=kind+'.py'; path=PROGRAM/name
    source=path.read_text() if variant=='current' else (HERE/(name+'.baseline.txt')).read_text()
    module=types.ModuleType('audit_'+kind+'_'+variant)
    module.__file__=str(path)
    exec(compile(source,str(path),'exec'),module.__dict__)
    module.subprocess=types.SimpleNamespace(check_output=fake.check_output,run=fake.run,CalledProcessError=subprocess.CalledProcessError)
    module._tree_module.subprocess=module.subprocess
    module.ROOT=workspace/PROGRAM.name;module.ROOT.mkdir(exist_ok=True)
    module.REPO=workspace
    return module

RESULTS=[]
def run_case(label,kind,change=None,config=None,expect='accept',variant='current',push=False,post=None):
    with tempfile.TemporaryDirectory(prefix='fixture ',dir=HERE/'private_fixtures') as temp:
        work=Path(temp);local=work/'reviewed local file.txt';local.write_bytes(b'new accepted receipt')
        pid=30006628;pr=872
        mapping={'pr':pr,'problem_id':pid,'expected_head':'1'*40,'original_turns':'3/5','final_review_status':'CLEAR','findings':'accepted fixture result','commit_message':'offline fixture','receipt_path':str(work/'receipt.json'),'files':[{'repo_path':LEGACY+'receipt.txt','local_path':str(local),'sha256':sha(local.read_bytes())}], 'protected_files':[{'repo_path':LEGACY+'core.txt','sha256':sha(b'accepted core')}], 'published_record':{'environment':'production','state':'published','doi_url':DOI}}
        if change:change(mapping,work)
        fake=MockCLI(mapping['problem_id'],kind,config)
        module=load(kind,variant,fake,work)
        file=work/'mapping.json';file.write_text(json.dumps(mapping))
        oldargv=sys.argv;sys.argv=[kind,str(file)]+(['--push'] if push else [])
        error=None;receipt=None
        try:
            with contextlib.redirect_stdout(io.StringIO()):module.main()
            receipt=json.loads(Path(mapping['receipt_path']).read_text())
        except Exception as exc:error=type(exc).__name__+': '+str(exc)
        finally:sys.argv=oldargv
        accepted=error is None
        check(accepted==(expect=='accept'),label+' expected '+expect+' got '+('accept' if accepted else error))
        check(fake.sentinels==fake.original_sentinels,label+' branch/index/worktree sentinels untouched')
        check(all(call[0] in ('git','gh') for call in fake.calls),label+' external calls fully mocked')
        if accepted:
            current=fake.flatten(fake.last_commit or fake.base)
            for name,entry in fake.initial_flat.items():
                if name.startswith('foreign/'):
                    check(current[name]==entry,label+' preserves foreign mode/OID '+repr(name))
            target=str(mapping['problem_id'])
            newqueue=fake.objects[current[QUEUE][2]][1].decode()
            check(qrow(777777,'unsolved','', '\r\n') in newqueue,label+' foreign queue row byte-identical')
            check(newqueue.startswith('untouched header\n') and newqueue.endswith('untouched footer\n'),label+' foreign queue framing untouched')
            if fake.last_commit:
                expected_parents=[fake.head,fake.base] if kind=='prepare_pr_revision' else [fake.base]
                check(fake.last_parents==expected_parents,label+' correct fresh-main parent(s)')
            if post:post(mapping,fake,receipt,current)
        elif not (config or {}).get('push_failure'):
            check(not any(c[:2]==['git','push'] for c in fake.calls),label+' rejection before any mocked push')
        if (config or {}).get('no_external_expected'):
            check(not fake.calls,label+' rejection before external calls')
        RESULTS.append({'label':label,'helper':kind,'variant':variant,'push_flag':push,'expected':expect,'accepted':accepted,'error':error,'calls':fake.calls,'receipt':receipt})


def setfile(name):
    return lambda m,w:m['files'][0].update(repo_path=name)
def setting(**values):
    return lambda m,w:m.update(values)
def exact_guard(m,f,r,flat):
    check(r['pushed'] is True,'mocked push returns confirmed receipt')
    calls=[c for c in f.calls if c[:2]==['git','push']]
    check(len(calls)==1,'single non-force mocked push')
    check(all('--force' not in c and '-f' not in c for c in calls),'no force push option')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
    (HERE/'private_fixtures').mkdir(exist_ok=True)
    comparison=json.loads((HERE/'INPUT_COMPARISON.json').read_text())
    for row in comparison['files']:
        check(sha((PROGRAM/row['name']).read_bytes())==row['current_sha256'],'input pin '+row['name'])
        if row['name']=='scoped_git_tree.py':check(row['identical'],'tree helper unchanged')
        else:
            current=ast.parse((PROGRAM/row['name']).read_text());old=ast.parse((HERE/(row['name']+'.baseline.txt')).read_text())
            def assignments(tree):return [n for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='prefix' for t in n.targets)]
            current_assign=assignments(current);old_assign=assignments(old)
            guards=[n for n in ast.walk(current) if isinstance(n,ast.If) and any(isinstance(x,ast.Constant) and x.value=='PR and problem ID must be positive integer keys' for x in ast.walk(n))]
            check(len(guards)==1,'single strict key guard '+row['name'])
            guard=guards[0]
            fn=next(n for n in current.body if isinstance(n,ast.FunctionDef) and n.name=='main')
            check(guard in fn.body,'strict key guard directly in main '+row['name'])
            fn.body.remove(guard)
            check(len(current_assign)==len(old_assign)==1,'single scope assignment '+row['name'])
            keyname='number' if row['name']=='prepare_pr_revision.py' else 'pr'
            for number in range(800,901):
                for pid in (30006628,30006629,9700026):
                    expression=ast.Expression(body=current_assign[0].value)
                    value=eval(compile(expression,'<pinned-prefix>','eval'),{keyname:number,'pid':pid})
                    expected=LEGACY if (number,pid)==(872,30006628) else 'unsolved_math_prioritization/attempts/'+str(pid)+'/'
                    check(value==expected,'prefix matrix '+row['name']+' '+str(number)+' '+str(pid))
            current_assign[0].value=old_assign[0].value
            check(ast.dump(current,include_attributes=False)==ast.dump(old,include_attributes=False),'entire executable AST unchanged except prefix and strict key guard '+row['name'])
    for kind in ('prepare_pr_revision','record_publication_main'):
        run_case(kind+' legacy accepted',kind)
        run_case(kind+' legacy accepted push path (mock only)',kind,push=True,post=exact_guard)
        run_case(kind+' baseline rejects legacy',kind,variant='baseline',expect='reject')
        run_case(kind+' current rejects old default for exact pair',kind,setfile(DEFAULT+'receipt.txt'),expect='reject')
        for variant in ('current','baseline'):
            def other(m,w):m.update(pr=880,problem_id=9700026);m['files'][0]['repo_path']='unsolved_math_prioritization/attempts/9700026/receipt.txt';m['protected_files']=[{'repo_path':'unsolved_math_prioritization/attempts/9700026/core.txt','sha256':sha(b'accepted core')}]
            # No protected files for default fixture: its role here is scope differential.
            def other_no_core(m,w):other(m,w);m['protected_files']=[]
            run_case(kind+' nonexception default '+variant,kind,other_no_core,variant=variant)
        for label,change in [('different PR',setting(pr=873)),('different PID',setting(problem_id=30006629)),('string PID',setting(problem_id='30006628')),('both different',setting(pr=880,problem_id=9700026))]:
            run_case(kind+' cross tuple '+label,kind,change,expect='reject')
        def injected_prefix(m,w):
            m['repo_prefix']='foreign/';m['prefix']='foreign/';m['files'][0]['repo_path']='foreign/receipt.txt'
        run_case(kind+' caller selected prefix ignored',kind,injected_prefix,expect='reject')
        for name in ['random_property_t_30006628_evil/x','random_property_t_30006629/x','random_property_t_30006628/../foreign/x','/random_property_t_30006628/x',LEGACY+'x//y',LEGACY+'./x',LEGACY+'x\\y',LEGACY+'x\x00y']:
            run_case(kind+' unsafe '+repr(name),kind,setfile(name),expect='reject')
        def dup(m,w):m['files'].append(dict(m['files'][0]))
        run_case(kind+' duplicate mapped paths',kind,dup,expect='reject')
        def symlink(m,w):
            link=w/'local symlink';link.symlink_to(m['files'][0]['local_path']);m['files'][0]['local_path']=str(link)
        run_case(kind+' local leaf symlink',kind,symlink,expect='reject')
        def tamper(m,w):Path(m['files'][0]['local_path']).write_bytes(b'changed after review')
        run_case(kind+' local SHA mismatch',kind,tamper,expect='reject')
        run_case(kind+' duplicate QUEUE row',kind,config={'duplicate_row':True},expect='reject')
        run_case(kind+' missing QUEUE row',kind,config={'missing_row':True},expect='reject')
        run_case(kind+' current main unsolved rejected',kind,config={'main_status':'unsolved'},expect='reject')
        run_case(kind+' current main already_solved rejected',kind,config={'main_status':'already_solved'},expect='reject')
        run_case(kind+' current main nonexact status rejected',kind,config={'main_status':'Claimed_solved'},expect='reject')
        run_case(kind+' conflicting DOI rejected',kind,config={'main_doi':'https://doi.org/10.5281/zenodo.123'},expect='reject')
        run_case(kind+' CRLF target preserved',kind,config={'ending':'\r\n'},post=lambda m,f,r,flat:check(b' |\r\n' in f.objects[flat[QUEUE][2]][1],'CRLF target row retained'))
        run_case(kind+' final not clear push rejected',kind,setting(final_review_status='PENDING'),expect='reject',push=True)
        run_case(kind+' below shard rejected',kind,setting(pr=799),expect='reject')
        run_case(kind+' above shard rejected',kind,setting(pr=901),expect='reject')
    for kind in ('prepare_pr_revision','record_publication_main'):
        run_case(kind+' unknown push failure not retried',kind,config={'push_failure':True},expect='reject',push=True)
        check(sum(c[:2]==['git','push'] for c in RESULTS[-1]['calls'])==1,kind+' one unknown push attempt only')
    kind='prepare_pr_revision'
    for config in ({'pr_state':'CLOSED'},{'head':'9'*40},{'head_status':'unsolved'},{'head_status':'already_solved'},{'head_status':'Claimed_solved'}):run_case(kind+' '+repr(config),kind,config=config,expect='reject')
    run_case(kind+' queued main allowed',kind,config={'main_status':'queued'})
    kind='record_publication_main'
    for field,value in [('environment','sandbox'),('state','ready_to_publish'),('doi_url','https://doi.org/10.1234/notzenodo')]:
        run_case(kind+' bad publication '+field,kind,lambda m,w,f=field,v=value:m['published_record'].update({f:v}),expect='reject')
    for state in ('OPEN','CLOSED'):run_case(kind+' not merged '+state,kind,config={'merged_state':state},expect='reject')
    run_case(kind+' merged not ancestor',kind,config={'not_ancestor':True},expect='reject')
    run_case(kind+' queued main forbidden',kind,config={'main_status':'queued'},expect='reject')
    run_case(kind+' already same DOI accepted',kind,config={'main_doi':DOI})
    run_case(kind+' protected hash mismatch',kind,lambda m,w:m['protected_files'][0].update(sha256='0'*64),expect='reject')
    run_case(kind+' protected foreign path',kind,lambda m,w:m['protected_files'][0].update(repo_path=DEFAULT+'core.txt'),expect='reject')
    run_case(kind+' protected file modification',kind,setfile(LEGACY+'core.txt'),expect='reject')
    run_case(kind+' program own effort allowed',kind,setfile(PROGRAM.name+'/audit_receipt.txt'))
    run_case(kind+' foreign program denied',kind,setfile('other_program/audit_receipt.txt'),expect='reject')
    # Expose existing caller/type assumptions without treating them as new guards.
    run_case('existing prepare permits non-draft snapshot', 'prepare_pr_revision',config={'draft':False})
    run_case('existing record trusts caller DOI suffix','record_publication_main',lambda m,w:m['published_record'].update(doi_url='https://doi.org/10.5281/zenodo.NOT_REAL'))
    for kind in ('prepare_pr_revision','record_publication_main'):
        for field,values in [('pr',[872.0,'872',True,None]),('problem_id',[30006628.0,'30006628',True,None,0,-1])]:
            for value in values:
                run_case(kind+' strict integer key '+field+' '+repr(value),kind,setting(**{field:value}),config={'no_external_expected':True},expect='reject')
    for row in comparison['files']:check(sha((PROGRAM/row['name']).read_bytes())==row['current_sha256'],'input remains unchanged '+row['name'])
    result={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'optimized':bool(sys.flags.optimize),'python':sys.version,'all_subprocesses_mocked':True,'no_real_git_or_network_writes':True,'cases':len(RESULTS),'rejected_cases':sum(not r['accepted'] for r in RESULTS),'accepted_cases':sum(r['accepted'] for r in RESULTS),'explicit_check_count':len(CHECKS),'checks':CHECKS,'results':RESULTS,'status':'PASS'}
    Path(args.output).write_text(json.dumps(result,indent=2,ensure_ascii=True)+'\n')
    print(json.dumps({k:result[k] for k in ['status','optimized','cases','rejected_cases','accepted_cases','explicit_check_count']}))

if __name__=='__main__':main()
