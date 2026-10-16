#!/usr/bin/env python3
"""Future commissioned private PR110 native candidate; no export/Git/service mutation."""
import sys,os
_env={'PATH':'/usr/bin:/bin','LC_ALL':'C','LANG':'C','TZ':'UTC'}
if sys.platform=='darwin':_env['__CF_USER_TEXT_ENCODING']='0x'+format(os.getuid(),'X')+':0x0:0x0'
if __name__=='__main__' and (not(sys.flags.ignore_environment and sys.flags.no_site and sys.flags.dont_write_bytecode and getattr(sys.flags,'safe_path',False)) or dict(os.environ)!=_env):
    raise SystemExit('Initial runner requires exact clean environment and Python -E -S -B -P before imports.')
import argparse, base64, configparser, datetime, difflib, hashlib, json, pathlib, re, selectors, shutil, signal, stat, subprocess, time, types
A=pathlib.Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr110_5100032')
D=A/'native_execution_programs_v1';C=A.parents[2];N='unsolved_math_prioritization/'
PROGRAMS={'native_runner.py','native_worker.py','native_launcher.sh','protocol.py'}
PROTOCOL_SHA='5111652d104c70aa81880426f449fd4ca1c1c15c5f4847db1acfca5924f67056'
_spawn_critical=False;_pending_signal=None
def need(ok,message):
    if not ok:raise ValueError(message)
def canonical(obj):return(json.dumps(obj,sort_keys=True,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
def sha(body):return hashlib.sha256(body).hexdigest()
def pin(body):return{'bytes':len(body),'sha256':sha(body)}
def same(a,b):return canonical(a)==canonical(b)
def loads(body):
    def pairs(items):
        out={}
        for key,value in items:need(key not in out,'Duplicate JSON key');out[key]=value
        return out
    def bad(value):raise ValueError('Nonfinite JSON '+value)
    return json.loads(body,object_pairs_hook=pairs,parse_constant=bad)
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def bootstrap_read(path,cap,spec=None):
    path=pathlib.Path(path);need(path.is_absolute() and '..' not in path.parts,'Canonical absolute startup path')
    fd=os.open('/',os.O_RDONLY|os.O_DIRECTORY)
    try:
        for part in path.parent.parts[1:]:
            nxt=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd);os.close(fd);fd=nxt
        child=os.open(path.name,os.O_RDONLY|os.O_NOFOLLOW,dir_fd=fd)
        try:
            first=os.fstat(child);need(stat.S_ISREG(first.st_mode) and first.st_nlink==1 and first.st_size<=cap,'Safe bounded startup input')
            blocks=[];count=0
            while True:
                chunk=os.read(child,65536)
                if not chunk:break
                count+=len(chunk);need(count<=cap,'Startup input grew');blocks.append(chunk)
            last=os.fstat(child);need((first.st_ino,first.st_dev,first.st_size,first.st_mtime_ns)==(last.st_ino,last.st_dev,last.st_size,last.st_mtime_ns),'Startup input changed')
            body=b''.join(blocks)
            if spec is not None:need(same(pin(body),{k:spec[k] for k in ['bytes','sha256']}),'Startup pin changed')
            return body
        finally:os.close(child)
    finally:os.close(fd)
def audit_path(spec):
    need(set(spec)=={'path','bytes','sha256'} and isinstance(spec['path'],str),'Exact audit pin')
    rel=pathlib.PurePosixPath(spec['path']);need(not rel.is_absolute() and '..' not in rel.parts and str(rel)==spec['path'],'Nonescaping audit pin')
    need(type(spec['bytes']) is int and 0<=spec['bytes']<=8*1024*1024 and isinstance(spec['sha256'],str) and re.fullmatch('[0-9a-f]{64}',spec['sha256']),'Audit pin bounds')
    return A/spec['path']
def load_bootstrap(config_path):
    config_path=pathlib.Path(config_path);need(config_path.parent.is_relative_to(D) and config_path.name.endswith('.json'),'Configuration inside new program folder')
    raw=bootstrap_read(config_path,128*1024);cfg=loads(raw)
    need(raw==canonical(cfg) and set(cfg)=={'schema','template_only','packet','adversary','commission'} and
         cfg['schema']=='pr110-concrete-native-config/v1' and cfg['template_only'] is False,'Actual canonical non-template config')
    packet_bytes=bootstrap_read(audit_path(cfg['packet']),512*1024,cfg['packet']);packet=loads(packet_bytes)
    need(packet_bytes==canonical(packet) and packet['schema']=='pr110-concrete-native-inputs/v1' and packet['template_only'] is False,'Actual immutable canonical packet')
    family={}
    need(set(packet['program_files'])==PROGRAMS,'Exact entire native program family')
    for name,spec in packet['program_files'].items():
        path=audit_path(spec);need(path==D/name,'Exact original reviewed code location');family[name]=bootstrap_read(path,128*1024,spec)
    need(family['native_runner.py']==bootstrap_read(pathlib.Path(__file__),128*1024) and sha(family['protocol.py'])==PROTOCOL_SHA,'Executing runner/sealed pure protocol bytes')
    approvals={}
    for role,key in [('adversary','adversary'),('root','commission')]:
        body=bootstrap_read(audit_path(cfg[key]),128*1024,cfg[key]);obj=loads(body)
        need(body==canonical(obj) and obj['schema']=='pr110-concrete-native-commission/v1' and obj['role']==role and
             obj['template_only'] is False and obj.get('fixture',False) is False and obj.get('simulated',False) is False and
             obj['actual_review'] is True and obj['clearance'] is True and obj['packet_sha256']==sha(packet_bytes) and
             same(obj['program_hashes'],{n:sha(b) for n,b in family.items()}),'Actual fresh source/packet-bound review')
        approvals[role]=(obj,body)
    root=approvals['root'][0];ad=approvals['adversary'][0]
    need(root['adversary_sha256']==sha(approvals['adversary'][1]) and root['actual_services_independently_authenticated'] is True and
         root['whole_package_R1_R2_clean'] is True and root['accepted_mathematical_full_resolution'] is True and
         root['bounded_novelty_and_source_credit_checked'] is True and root['native_candidate_preparation_commissioned'] is True,
         'Actual service/package/full-resolution commissioning')
    for obj,_ in approvals.values():need(obj['main_parent']==packet['main_parent'],'Review current main binding')
    # Load only source bytes authenticated before any local module import.
    worker=types.ModuleType('native_worker');worker.__file__=str(D/'native_worker.py');sys.modules['native_worker']=worker
    exec(compile(family['native_worker.py'],worker.__file__,'exec'),worker.__dict__)
    p=worker.module_from_bytes('protocol',family['protocol.py'],D/'protocol.py')
    need(p.stamp(ad['UTC'])<=p.stamp(root['UTC'])<=p.stamp(utc()) and
         p.stamp(utc())-p.stamp(root['UTC'])<=datetime.timedelta(minutes=30),'Fresh commissioning UTC')
    return cfg,packet,packet_bytes,family,approvals,worker,p

def process_policy(policy):
    need(set(policy)=={'deadline_seconds','stdout_cap','stderr_cap','retain_bytes','max_processes','term_grace_seconds','allocation_cap',
         'file_count_cap','headroom_bytes','commit_reserve_bytes','runtime_reserve_bytes'},'Exact bounded parent policy')
    need(all(type(v) is int and v>0 for v in policy.values()),'Integer parent policy')
    need(policy['deadline_seconds']<=120 and policy['stdout_cap']<=32*1024*1024 and policy['stderr_cap']<=65536 and policy['retain_bytes']<=4096 and
         policy['max_processes']<=32 and policy['term_grace_seconds']<=2 and policy['allocation_cap']<=160*1024*1024 and policy['file_count_cap']<=512 and
         policy['headroom_bytes']>=32*1024*1024 and policy['commit_reserve_bytes']>=8*1024*1024 and policy['runtime_reserve_bytes']>=8*1024*1024,'Parent process/capacity bounds')
class Processes:
    def __init__(self,workspace,policy,worker):self.root=pathlib.Path(workspace);self.policy=policy;self.w=worker;self.records=[];self.launches=[];process_policy(policy)
    def run(self,argv,cwd,env,deadline=None,watch=None,allow_failure=False,fixture=False):
        global _spawn_critical,_pending_signal
        need(len(self.records)<self.policy['max_processes'] and isinstance(argv,list) and argv and all(isinstance(x,str) for x in argv),'Bounded explicit process argv')
        need(isinstance(env,dict) and all(isinstance(k,str) and isinstance(v,str) for k,v in env.items()),'Explicit string environment')
        limit=deadline or min(30,self.policy['deadline_seconds']);need(type(limit) is int and 1<=limit<=self.policy['deadline_seconds'],'Deadline within frozen policy')
        environment_digest=sha(canonical(env));started=utc();begin=time.monotonic();proc=None;sel=None
        counts={'stdout':0,'stderr':0};hashes={k:hashlib.sha256() for k in counts};retained={k:bytearray() for k in counts};buffers={k:bytearray() for k in counts}
        reason=None;term=None;killed=False;pending_error=None;fully_drained=False;group_absent=False;cleanup_errors=[]
        def group_exists():
            if proc is None:return False
            try:os.killpg(proc.pid,0);return True
            except ProcessLookupError:return False
            except PermissionError:
                if 'PGID_probe_permission_denied' not in cleanup_errors:cleanup_errors.append('PGID_probe_permission_denied')
                return True  # Absence is unconfirmed, never claim successful cleanup.
        def group_signal(sig):
            if proc is None:return
            try:os.killpg(proc.pid,sig)
            except ProcessLookupError:pass
            except PermissionError:
                label='PGID_'+signal.Signals(sig).name+'_permission_denied'
                if label not in cleanup_errors:cleanup_errors.append(label)
        def stop(why):
            nonlocal reason,term
            if reason is None:
                reason=why;term=time.monotonic()
                group_signal(signal.SIGTERM)
        try:
            # The installed operator handler defers TERM/INT through the
            # return-to-assignment gap; children do not inherit blocked masks.
            _spawn_critical=True
            try:proc=subprocess.Popen(argv,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
            finally:_spawn_critical=False
            if _pending_signal is not None:
                sig=_pending_signal;_pending_signal=None;raise SystemExit('Deferred actual operator signal '+signal.Signals(sig).name)
            sel=selectors.DefaultSelector()
            for kind,stream in [('stdout',proc.stdout),('stderr',proc.stderr)]:os.set_blocking(stream.fileno(),False);sel.register(stream,selectors.EVENT_READ,kind)
            self.launches.append({'actual_process_record':True,'synthetic_fixture_only':fixture,'argv':argv,'cwd':str(cwd),
              'environment_sha256':environment_digest,'PID':proc.pid,'UTC_start':started,'state':'launched_not_yet_reaped'})
            journal=self.root/'PROCESS_LAUNCHES.json';previous=self.w.read_file(journal,128*1024) if journal.exists() else None
            self.w.atomic_write(self.root,journal.name,canonical({'operator_PID':os.getpid(),'launches':self.launches}),128*1024,
              replace=previous is not None,expected=pin(previous) if previous is not None else None)
            while sel.get_map() or proc.poll() is None:
                elapsed=time.monotonic()-begin
                if elapsed>=limit:stop('deadline')
                if watch is not None and reason is None:
                    try:watch()
                    except BaseException as error:stop('watchdog:'+str(error)[:180])
                if term is not None and time.monotonic()-term>=self.policy['term_grace_seconds'] and not killed:
                    group_signal(signal.SIGKILL)
                    killed=True
                if elapsed>=limit+self.policy['term_grace_seconds']+3:stop('drain_deadline');break
                for key,_ in sel.select(0.1):
                    chunk=os.read(key.fileobj.fileno(),65536);kind=key.data
                    if not chunk:sel.unregister(key.fileobj);key.fileobj.close();continue
                    counts[kind]+=len(chunk);hashes[kind].update(chunk)
                    retain=self.policy['retain_bytes']-len(retained[kind]);retained[kind].extend(chunk[:max(0,retain)])
                    cap=self.policy['stdout_cap'] if kind=='stdout' else self.policy['stderr_cap']
                    buffers[kind].extend(chunk[:max(0,cap-len(buffers[kind]))])
                    if counts[kind]>cap:stop(kind+'_cap')
        except BaseException as error:
            pending_error=error;stop('operator_exception:'+type(error).__name__)
        finally:
            if sel is not None:fully_drained=not bool(sel.get_map());sel.close()
            if group_exists():
                stop('surviving_process_group' if proc.poll() is not None else 'operator_cleanup')
                end=time.monotonic()+self.policy['term_grace_seconds']
                while group_exists() and time.monotonic()<end:time.sleep(0.02)
            if group_exists():
                group_signal(signal.SIGKILL)
                killed=True
            if proc is not None:
                try:proc.wait(timeout=3)
                except subprocess.TimeoutExpired:reason='unreaped_operator_intervention_required'
                group_absent=not group_exists()
                for stream in [proc.stdout,proc.stderr]:
                    if not stream.closed:stream.close()
        if proc is None:
            need(pending_error is None,'No child spawned: '+type(pending_error).__name__)
            raise ValueError('No child spawned; no fictitious PID receipt')
        rec={'actual_process_record':True,'synthetic_fixture_only':fixture,'argv':argv,'cwd':str(cwd),'environment_sha256':environment_digest,
          'PID':proc.pid,'UTC_start':started,'UTC_end':utc(),'exit_code':proc.returncode,'deadline_seconds':limit,
          'termination_reason':reason,'SIGKILL_attempted':killed,'reaped':proc.returncode is not None,
          'environment_captured_before_spawn':True,'bounded_stdout_capture':True,'bounded_stderr_capture':True,
          'streams_fully_drained':fully_drained,'process_group_absence_confirmed':group_absent,
          'cleanup_errors':cleanup_errors,'operator_intervention_required':bool(cleanup_errors) or proc.returncode is None or not group_absent,
          'elapsed_monotonic_seconds':time.monotonic()-begin,'streams':{}}
        i=len(self.records)
        for kind in counts:
            name=f'process_{i}_{kind}.prefix';self.w.atomic_write(self.root,name,bytes(retained[kind]),4096)
            rec['streams'][kind]={'observed_bytes':counts[kind],'observed_sha256':hashes[kind].hexdigest(),'retained_path':name,**pin(bytes(retained[kind]))}
        self.records.append(rec);path=self.root/'PROCESS_JOURNAL.json';body=canonical({'operator_PID':os.getpid(),'processes':self.records})
        self.w.atomic_write(self.root,path.name,body,128*1024,replace=path.exists(),expected=pin(self.w.read_file(path,128*1024)) if path.exists() else None)
        if pending_error is not None:raise pending_error
        need(allow_failure or (rec['exit_code']==0 and reason is None and rec['reaped'] and fully_drained and group_absent and not cleanup_errors),'Subprocess failed; actual receipt retained')
        return bytes(buffers['stdout']),rec

def resolve_invocation(spec,w):
    """Authenticate each actual symlink, then read the resolved unique regular file."""
    need(set(spec)=={'invocation_path','resolved_absolute_path','symlink_chain','bytes','sha256','version'},'Runtime invocation/resolved pin')
    original=pathlib.Path(spec['invocation_path']);need(original.is_absolute() and '..' not in original.parts,'Absolute invocation path')
    pending=list(original.parts[1:]);base=pathlib.Path('/');chain=[]
    while pending:
        part=pending.pop(0)
        if part in ['', '.']:continue
        if part=='..':base=base.parent;continue
        candidate=base/part;fd=w.directory_fd(base)
        try:
            info=os.stat(part,dir_fd=fd,follow_symlinks=False)
            if stat.S_ISLNK(info.st_mode):
                need(len(chain)<32,'Symlink loop/chain cap')
                target=os.readlink(part,dir_fd=fd);last=os.stat(part,dir_fd=fd,follow_symlinks=False)
                need((info.st_dev,info.st_ino,info.st_mtime_ns)==(last.st_dev,last.st_ino,last.st_mtime_ns) and
                     os.readlink(part,dir_fd=fd)==target,'Symlink changed while authenticating')
                chain.append({'path':str(candidate),'target':target,'target_utf8_sha256':sha(target.encode())})
                # Preserve component-by-component kernel semantics: symlink
                # directories must be resolved before a following '..'.
                pending=target.split('/')+pending
                if target.startswith('/'):base=pathlib.Path('/')
                continue
            if pending:need(stat.S_ISDIR(info.st_mode),'Non-directory invocation ancestor')
            else:need(stat.S_ISREG(info.st_mode) and info.st_nlink==1,'Resolved invocation is not unique regular file')
            base=candidate
        finally:os.close(fd)
    need(str(base)==spec['resolved_absolute_path'] and same(chain,spec['symlink_chain']),'Actual resolved path/symlink-chain drift')
    need(isinstance(spec['version'],str) and spec['version'],'Current preflight version text')
    w.read_file(base,64*1024*1024,spec,retain=False);return str(base)

def validate_gh_configuration_lines(text):
    """Strict subset covering the genuine default GH configuration, without YAML execution."""
    need(isinstance(text,str) and '\x00' not in text,'GH text configuration')
    seen=set();aliases=False
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith('#'):continue
        if line.startswith(' '):
            need(aliases and re.fullmatch(r'    co: pr checkout',line) and 'alias:co' not in seen,'Unreviewed GH alias or YAML indentation')
            seen.add('alias:co');continue
        need(':' in line and not line.startswith(('\t','-','!','&','*')),'GH plain configuration mapping required')
        key,value=line.split(':',1);value=value.strip();need(key not in seen,'Duplicate GH configuration key');seen.add(key)
        aliases=key=='aliases'
        if key=='git_protocol':need(value=='https','GH HTTPS protocol required')
        elif key in ['editor','pager','browser','http_unix_socket']:need(value in ['', 'null','~'],'GH external command/socket configuration forbidden')
        elif key in ['prompt','prefer_editor']:need(value in ['enabled','disabled'],'GH prompt/editor preference value')
        elif key=='aliases':need(value in ['', '{}'],'GH alias mapping')
        elif key=='version':need(value in ['1','"1"',"'1'"],'GH configuration version')
        else:raise ValueError('Unknown GH configuration key')

def validate_runtime(runtime,w,p):
    need(set(runtime)=={'UTC','pin_scope','historical_binary_bytes_attested','binaries','dependency_files','python_environment','gh_config_directory','private_configuration_pins'},'Exact runtime choices')
    need(runtime['pin_scope']=='fresh_current_preflight_only' and runtime['historical_binary_bytes_attested'] is False,'Current runtime pins must not imply retrospective executable custody')
    p.stamp(runtime['UTC'])
    need(set(runtime['binaries'])=={'python','git','gh','gws','node','sh','env'} and same(runtime['python_environment'],w.clean_environment()),'Pinned binary family and clean environment')
    for role,spec in runtime['binaries'].items():
        resolve_invocation(spec,w)
    need(runtime['binaries']['python']['resolved_absolute_path']==str(pathlib.Path(sys.executable)) and
         runtime['binaries']['sh']['invocation_path']=='/bin/sh' and runtime['binaries']['env']['invocation_path']=='/usr/bin/env','Exact current physical Python/shell/env')
    need(isinstance(runtime['dependency_files'],dict) and set(runtime['dependency_files'])=={'gws_package_json','gws_platform_js','gws_native_backend'},'Explicit current GWS package mapper/backend graph')
    for name,spec in runtime['dependency_files'].items():
        need(set(spec)=={'absolute_path','bytes','sha256'},'Exact dependency file pin');w.read_file(spec['absolute_path'],64*1024*1024,spec,retain=False)
    wrapper=pathlib.Path(runtime['binaries']['gws']['resolved_absolute_path']);deps=runtime['dependency_files']
    need(wrapper.name=='run.js' and deps['gws_package_json']['absolute_path']==str(wrapper.parent/'package.json') and
         deps['gws_platform_js']['absolute_path']==str(wrapper.parent/'platform.js') and
         deps['gws_native_backend']['absolute_path']==str(wrapper.parent/'bin/gws'),'Exact installed wrapper/mapper/backend paths')
    need(isinstance(runtime['private_configuration_pins'],list) and runtime['private_configuration_pins'],'Private configuration metadata required')
    pinned=set()
    # This isolated checkout is a normal repository. Do not follow a worktree
    # pointer to a different admin/configuration tree during future execution.
    fd=w.directory_fd(C/'.git');os.close(fd)
    need(not os.path.lexists(C/'.git/commondir'),'Unexpected common Git admin directory')
    ghdir=pathlib.Path(runtime['gh_config_directory']);fd=w.directory_fd(ghdir);os.close(fd)
    required={(str(C/'.git/config'),'git')}
    if os.path.lexists(C/'.git/config.worktree'):required.add((str(C/'.git/config.worktree'),'git'))
    for item in os.scandir(ghdir):
        info=item.stat(follow_symlinks=False)
        need(item.name in ['config.yml','hosts.yml','state.yml'] and stat.S_ISREG(info.st_mode) and info.st_nlink==1,'Unexpected GH configuration entry')
        required.add((str(ghdir/item.name),'gh'))
    need((str(ghdir/'hosts.yml'),'gh') in required,'Actual GH host credential configuration required privately')
    for spec in runtime['private_configuration_pins']:
        need(set(spec)=={'role','absolute_path','bytes','sha256','body_private'} and spec['body_private'] is True and spec['role'] in ['git','gh'],'Explicit private config role')
        identity=(spec['absolute_path'],spec['role']);need(identity not in pinned and identity in required,'Configuration duplicate or unrelated path');pinned.add(identity)
        body=w.read_file(spec['absolute_path'],128*1024,spec)
        if spec['role']=='git':
            config=configparser.RawConfigParser();config.read_string(body.decode())
            for section in config.sections():
                need(not section.lower().startswith(('include','alias','url ','filter ','diff ','credential')),'Unreviewed Git include/command/rewrite config')
                for key,value in config[section].items():need(key.lower() not in ['sshcommand','pager','editor','proxy','promisor','partialclonefilter'],'Unreviewed Git runtime command')
        elif pathlib.Path(spec['absolute_path']).name=='config.yml':validate_gh_configuration_lines(body.decode())
    need(pinned==required,'All actual effective local Git/GH configurations must be pinned')
    return runtime

def format_scoped_json(before,scoped,p):
    """Retain native baseline dictionary insertion order; avoid global key-order churn."""
    if 'catalog.json' in scoped:
        prior=p.loads(before['catalog.json']);updated={row['id']:row for row in p.loads(scoped['catalog.json'])}
        rows=[]
        for row in prior:
            new=updated[row['id']]
            rows.append(row if row['id']!=p.K else {**row,**new})
        scoped['catalog.json']=(json.dumps(rows,ensure_ascii=False,indent=2)+'\n').encode()
        need(same(p.loads(scoped['catalog.json']),[updated[row['id']] for row in prior]),'Scoped catalog serialization altered objects/order')
    if 'summary.json' in scoped:
        value={**p.loads(before['summary.json']),**p.loads(scoped['summary.json'])}
        scoped['summary.json']=(json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode()
    return {name:body for name,body in scoped.items() if body!=before[name]}

def full_diff(before,offers,prefix,cap=1024*1024):
    """Complete unified diff for every offered UTF-8 file; fail instead of truncate."""
    parts=[];count=0
    for name,body in offers.items():
        old=before.get(name[len(N):]) if name in {N+n for n in before} else None
        need(old is None or old!=body,'Unchanged derived output must not be offered')
        try:
            previous=[] if old is None else old.decode('utf8').splitlines(keepends=True)
            added=body.decode('utf8').splitlines(keepends=True)
        except UnicodeDecodeError:
            need(old is None,'Native derived files must be UTF-8')
            encoded=('Complete new binary addition '+name+' '+json.dumps(pin(body),sort_keys=True)+'\n'+base64.b64encode(body).decode()+'\n').encode()
            count+=len(encoded);need(count<=cap,'Complete binary DIFF exceeds reviewed cap');parts.append(encoded);continue
        for line in difflib.unified_diff(previous,added,fromfile='/dev/null' if old is None else 'a/'+name,tofile='b/'+name):
            if not line.endswith('\n'):line+='\n\\ No newline at end of file\n'
            encoded=line.encode();count+=len(encoded);need(count<=cap,'Complete DIFF exceeds reviewed cap; obtain revised program review')
            parts.append(encoded)
    return b''.join(parts)
def git_environment(w):
    return {**w.clean_environment(),'GIT_CONFIG_NOSYSTEM':'1','GIT_CONFIG_GLOBAL':'/dev/null','GIT_CONFIG_SYSTEM':'/dev/null',
      'GIT_OPTIONAL_LOCKS':'0','GIT_NO_REPLACE_OBJECTS':'1','GIT_TERMINAL_PROMPT':'0'}
def git_argv(runtime,*args):return[runtime['binaries']['git']['resolved_absolute_path'],'-c','core.fsmonitor=false','-c','core.hooksPath=/dev/null','-c','credential.helper=',*args]
def live_checks(packet,runner,w,p):
    runtime=packet['runtime'];env=git_environment(w)
    def git(*args):return runner.run(git_argv(runtime,*args),C,env)[0].decode().strip()
    need(git('rev-parse','HEAD')==packet['main_parent'] and git('symbolic-ref','--short','HEAD')=='main','Current main changed')
    remote=git('ls-remote','https://github.com/AlecKriebel/Math.git','refs/heads/main').split()
    need(len(remote)==2 and remote[0]==packet['main_parent'],'Remote main changed')
    gh_env={**w.clean_environment(),'GH_CONFIG_DIR':packet['runtime']['gh_config_directory'],'GH_HOST':'github.com','GH_PROMPT_DISABLED':'1',
      'GH_PAGER':'','GH_BROWSER':'/usr/bin/false','GH_EDITOR':'/usr/bin/false','GH_NO_UPDATE_NOTIFIER':'1'}
    body,_=runner.run([runtime['binaries']['gh']['resolved_absolute_path'],'pr','view','https://github.com/AlecKriebel/Math/pull/110',
                     '--json','number,state,isDraft,headRefOid,baseRefName,headRefName'],C,gh_env)
    live=p.loads(body)
    need(live.get('number')==110 and live.get('state')=='OPEN' and live.get('isDraft') is True and live.get('headRefOid')==p.HEAD and
         live.get('baseRefName')=='main' and live.get('headRefName')=='dot/math-5100032','Original open draft PR head/base changed')
    need(not os.path.lexists(C/(N+'attempts/'+p.K)),'Native target already present; reconcile')

def execute(config_path):
    cfg,packet,packet_bytes,family,approvals,w,p=load_bootstrap(config_path);w.startup()
    def terminated(sig,frame):
        global _pending_signal
        if _spawn_critical:_pending_signal=sig;return
        raise SystemExit('Actual operator termination signal '+signal.Signals(sig).name)
    signal.signal(signal.SIGTERM,terminated);signal.signal(signal.SIGINT,terminated)
    expected={'schema','template_only','identity','main_parent','workspace_parent','program_files','native_baseline','input_files',
      'original','package','publication_receipt','sheet_receipt','service_process_contracts','preflight_receipt','runtime','source_cache','raw_source_pins',
      'resources','parent_policy','assessment_overlay','campaign_note','import_UTC','attempt_offer_sources','checked_artifacts'}
    need(set(packet)==expected,'Every effective packet choice explicit')
    need(same(packet['identity'],{'PR':110,'id':p.K,'code':p.CODE,'original_head':p.HEAD,'review_hash':p.REVIEW,'statement_hash':p.STATEMENT,
      'dataset_revision':p.REV,'literal_status':'claimed_solved','turns_used':2,'new_central_proof_search_turns':0,'exact_claim':p.CLAIM}), 'Full literal identity/claim')
    need(packet['workspace_parent']==str(D/'workspaces') and isinstance(packet['main_parent'],str) and re.fullmatch('[0-9a-f]{40}',packet['main_parent']),'Fixed future workspace/current main')
    validate_runtime(packet['runtime'],w,p);w.limits_policy(packet['resources']);process_policy(packet['parent_policy'])
    parent_limits=w.apply_limits(packet['resources'])
    need(set(packet['native_baseline'])==set(p.NATIVE),'Full native baseline pin set')
    for name,spec in packet['native_baseline'].items():need(spec['path']==N+name and type(spec['bytes']) is int and spec['bytes']<=32*1024*1024,'Native Git path/size')
    registry=packet['input_files'];need(isinstance(registry,list) and 1<=len(registry)<=256,'Bounded input registry before reads')
    for spec in registry:audit_path(spec)
    need(len({spec['path'] for spec in registry})==len(registry) and sum(spec['bytes'] for spec in registry)<=32*1024*1024,'Unique aggregate input cap before reads')
    bodies={spec['path']:w.read_file(audit_path(spec),8*1024*1024,spec) for spec in registry}
    inputs=p.Inputs(packet['input_files'],bodies)
    original,source,prior=p.validate_original(packet['original'],inputs)
    package=packet['package'];need(set(package)=={'manifest','logical_inventory','effective_proof','transport_inventory_receipt'},'Exact package choices')
    package_bytes=inputs.read(package['manifest']);parsed_manifest=p.loads(package_bytes)
    need(isinstance(parsed_manifest,dict) and bool(parsed_manifest) and isinstance(package['logical_inventory'],dict) and
         len(package['logical_inventory'])==33 and package['manifest'] in package['logical_inventory'].values() and
         package['effective_proof'] in package['logical_inventory'].values() and bool(inputs.read(package['effective_proof'])),
         'Complete fixed33 package includes nonempty manifest/effective proof')
    transport=inputs.obj(package['transport_inventory_receipt']);p.actual(transport)
    need(transport['package_manifest_sha256']==sha(package_bytes) and same(transport['exact_logical_inventory'],package['logical_inventory']) and
         transport['no_missing_duplicate_extra_or_unsafe_archive_members'] is True,'Actual exact package transport inventory')
    publication=inputs.obj(packet['publication_receipt']);doi,_,zenodo_end=p.publication(publication,package,inputs)
    sheet=inputs.obj(packet['sheet_receipt']);selected,sheet_end=p.sheet(sheet,doi,source,zenodo_end,inputs)
    service_records={'zenodo.metadata':publication['metadata_GET'],**{'zenodo.payload.'+name:item['GET'] for name,item in publication['logical_readbacks'].items()},
                    **{'gws.'+role:record for role,record in sheet['processes'].items()}}
    need(set(packet['service_process_contracts'])==set(service_records),'All exact actual service process contracts')
    for role,record in service_records.items():
        contract=packet['service_process_contracts'][role];need(set(contract)=={'argv','cwd','environment_sha256','executable_role','program_inputs'},'Service contract fields')
        binary=contract['executable_role'];need(binary in ['python','gws'] and record['argv'][0]==packet['runtime']['binaries'][binary]['invocation_path'] and
          (not role.startswith('gws.') or binary=='gws') and all(same(record[k],contract[k]) for k in ['argv','cwd','environment_sha256']),'Actual service/runtime contract')
        for spec in contract['program_inputs']:inputs.read(spec)
    pre=inputs.obj(packet['preflight_receipt']);p.actual(pre)
    need(pre['main_parent']==packet['main_parent'] and pre['remote_main']==packet['main_parent'] and pre['original_head']==p.HEAD and
      pre['review_hash']==p.REVIEW and pre['statement_hash']==p.STATEMENT and pre['SQL_prior_equals_nonempty_original'] is True and
      pre['SQL_source_equals_original'] is True and pre['full_native_baseline_and_runtime_independently_checked'] is True and
      pre['schema']=='pr110-concrete-native-preflight/v1' and pre['branch']=='main' and pre['dataset_revision']==p.REV and
      type(pre['SQL_record_count']) is int and pre['SQL_record_count']==15458 and same(pre['source_cache'],packet['source_cache']) and
      same(pre['raw_source_pins'],packet['raw_source_pins']) and same(pre['native_baseline'],packet['native_baseline']) and
      same(pre['runtime'],packet['runtime']) and pre['native_target_absent'] is True and pre['SQL_sidecars_absent'] is True and
      same(pre['live_PR'],{'number':110,'head':p.HEAD,'base':'main','state':'OPEN','isDraft':True}) and
      pre['root_independently_authenticated_actual_preflight_processes'] is True,'Actual refreshed full main/source/cache/runtime preflight')
    need(sheet_end<=p.stamp(pre['UTC'])<=p.stamp(packet['import_UTC'])<=p.stamp(approvals['root'][0]['UTC']) and
         p.stamp(packet['runtime']['UTC'])<=p.stamp(pre['UTC']),'Service/runtime/preflight/import/commission chronology')
    for spec in packet['checked_artifacts']:inputs.read(spec)
    overlay=packet['assessment_overlay'];need(set(overlay)<=p.ASSESSMENT_METADATA and overlay['original_budget']=='2/5' and
      type(overlay['new_central_proof_search_turns']) is int and overlay['new_central_proof_search_turns']==0 and
      overlay['original_structured_ledger_present'] is False and overlay['publication_DOI']==doi and overlay['package_manifest_sha256']==sha(package_bytes), 'Exact reviewed target descriptive overlay')
    note=packet['campaign_note'];need(isinstance(note,str) and len(note.split())>=8 and not any(c in note for c in '|\r\n'),'Reviewed campaign note')
    original_cache_pins={s['path'].rsplit('/',1)[-1]:{k:s[k] for k in ['bytes','sha256']}
      for s in inputs.obj(packet['original']['sourcepair_authentication'])['input_pins'] if '/cache/' in s['path']}
    cache=packet['source_cache'];need(set(cache)=={'absolute_path','pin'} and same(cache['pin'],original_cache_pins['catalog.sqlite']) and
      same(packet['raw_source_pins'],{name:original_cache_pins[name] for name in ['problems.json','research_results.json']}),'Original immutable complete SQL/raw source pins')
    w.check_cache(cache['absolute_path'],cache['pin'],p.REV,15458,original['source_record.json'],original['prior_imported_report.json'])
    for name,spec in packet['raw_source_pins'].items():need(name in ['problems.json','research_results.json'],'Raw cache name');w.read_file('/Users/alec/Documents/Math/unsolved_math_prioritization/cache/'+name,128*1024*1024,spec,retain=False)
    need(set(packet['raw_source_pins'])=={'problems.json','research_results.json'},'Both full raw source pins')
    prefix=N+'attempts/'+p.K+'/';offers=packet['attempt_offer_sources']
    need(isinstance(offers,dict) and all(p.relative(name).startswith(prefix) for name in offers),'Exact target attempt destinations')
    required={prefix+'historical_original/'+name:spec for name,spec in packet['original']['files'].items()}
    required.update({prefix+'source_record.json':packet['original']['files']['source_record.json'],prefix+'prior_imported_report.json':packet['original']['files']['prior_imported_report.json']})
    need(all(same(offers.get(name),spec) for name,spec in required.items()),'Mandatory preserved original/nonempty sourcepair offer map')
    need(offers.get(prefix+'PROOF.md',{}).get('path')=='native_acceptance_source_v1/PROOF.md','Reviewed current native proof guide required separately from historical original')
    offer_bodies={name:inputs.read(spec) for name,spec in offers.items()};inputs.finish()
    caps=w.derive_caps(packet['native_baseline'],packet['resources']);policy=packet['parent_policy']
    capacity=sum(caps.values())+sum(caps[n] for n in p.DERIVED)+sum(len(b) for b in offer_bodies.values())+max(caps.values())+2*1024*1024
    need(capacity<=policy['allocation_cap'],'Exact private output/atomic-slot allocation exceeds reviewed cap')
    reserves=policy['headroom_bytes']+policy['commit_reserve_bytes']+policy['runtime_reserve_bytes']
    need(shutil.disk_usage(D).free>=capacity+reserves,'Insufficient free allocation plus independent reserves')
    parent=D/'workspaces'
    if not parent.exists():w.safe_mkdir(D,'workspaces')
    workspace=w.safe_mkdir(parent,'candidate_'+sha(packet_bytes)[:16]);backend=w.safe_mkdir(workspace,'private_native_backend')
    allowed={name:128*1024 for name in family}|{'EXECUTION_INPUTS.json':512*1024,'ROOT_COMMISSION.json':128*1024,
      'PREEXEC_ADVERSARY.json':128*1024,'SOURCE_RECORD.json':65536,'PRIOR_REPORT.json':65536,'WORKER_CONTROL.json':512*1024,
      'WORKER_RESULT.json':128*1024,'PROCESS_JOURNAL.json':128*1024,'PROCESS_LAUNCHES.json':128*1024,'CANDIDATE_RECEIPT.json':128*1024,'FAILURE.json':65536,'DIFF.txt':1024*1024}
    allowed.update({'private_native_backend/'+n:cap for n,cap in caps.items()})
    for i in range(policy['max_processes']):
        for stream in ['stdout','stderr']:allowed[f'process_{i}_{stream}.prefix']=4096
    generated=['IMPORT_BASELINE.json','HISTORICAL_DESK_ASSESSMENT.json','assessment.json','PUBLICATION_EVIDENCE.json','ACCEPTANCE_EVIDENCE.json','README.md','RESEARCH_LOG.md']
    for name in generated:need(prefix+name not in offers,'Generated/source offer collision')
    for name,body in offer_bodies.items():allowed['offer/'+name]=len(body)
    for name in generated:allowed['offer/'+prefix+name]=65536
    for name in p.DERIVED:allowed['offer/'+N+name]=caps[name]
    def watch():
        count=0;size=0
        def scan(root,rel=''):
            nonlocal count,size
            for entry in os.scandir(root):
                path=rel+entry.name;info=entry.stat(follow_symlinks=False)
                if stat.S_ISDIR(info.st_mode):need(any(name.startswith(path+'/') for name in allowed),'Unenumerated private directory');scan(entry.path,path+'/')
                else:
                    base=path[:-4] if path.endswith('.tmp') else path
                    need(stat.S_ISREG(info.st_mode) and info.st_nlink==1 and base in allowed and info.st_size<=allowed[base],'Unsafe/unlisted/oversized private output')
                    count+=1;size+=info.st_size
        scan(workspace);need(count<=policy['file_count_cap'] and size<=policy['allocation_cap'],'Private file/byte cap')
        need(shutil.disk_usage(D).free>=reserves,'Private run consumed required headroom/reserves')
        return {'files':count,'bytes':size,'free_bytes':shutil.disk_usage(D).free}
    runner=Processes(workspace,policy,w)
    try:
        for name,body in family.items():w.atomic_write(workspace,name,body,128*1024)
        for name,body in [('EXECUTION_INPUTS.json',packet_bytes),('ROOT_COMMISSION.json',approvals['root'][1]),('PREEXEC_ADVERSARY.json',approvals['adversary'][1]),
                          ('SOURCE_RECORD.json',original['source_record.json']),('PRIOR_REPORT.json',original['prior_imported_report.json'])]:w.atomic_write(workspace,name,body,allowed[name])
        live_checks(packet,runner,w,p)
        before={}
        for name,spec in packet['native_baseline'].items():
            body,_=runner.run(git_argv(packet['runtime'],'show',packet['main_parent']+':'+spec['path']),C,git_environment(w),watch=watch)
            need(same(pin(body),{k:spec[k] for k in ['bytes','sha256']}),'Native full Git preimage changed');before[name]=body
            local=C/spec['path']
            if os.path.lexists(local):w.read_file(local,32*1024*1024,spec,retain=False)
            w.atomic_write(backend,name,body,caps[name])
        need(sha(before['queue.py'])==p.QUEUE_SHA and p.loads(before['manifest.json'])['revision']==p.REV and
          p.loads(before['manifest.json'])['records']==15458 and same(p.loads(before['manifest.json'])['files'],packet['raw_source_pins']),'Current native runtime/revision/raw pins')
        catalog=p.loads(before['catalog.json']);state=p.loads(before['state.json']);oldass=p.loads(before['assessments.json']);target=next(r for r in catalog if r['id']==p.K)
        need(p.K not in state and target['local_status']=='queued' and type(target['turns_used']) is int and target['turns_used']==0 and
          target['review_hash']==p.REVIEW and target['statement_hash']==p.STATEMENT and target['present'] is True and target['holds']==[],'Target queued0 baseline changed')
        event=p.imported_baseline(packet['import_UTC'],p.ORIGINAL_ROW_SHA,p.ORIGINAL_LOG_SHA)
        newstate={**state,p.K:event};newhistory=before['history.jsonl']+json.dumps(event,ensure_ascii=False).encode()+b'\n'
        need(not before['history.jsonl'] or before['history.jsonl'].endswith(b'\n'),'Historical ledger terminal newline')
        w.atomic_write(backend,'state.json',(json.dumps(newstate,ensure_ascii=False,indent=2)+'\n').encode(),caps['state.json'],replace=True,expected=pin(before['state.json']))
        w.atomic_write(backend,'history.jsonl',newhistory,caps['history.jsonl'],replace=True,expected=pin(before['history.jsonl']))
        assessment={**oldass[p.K],**overlay};w.atomic_write(backend,'assessment.json',canonical(assessment),65536)
        pre_assess={name:w.read_file(backend/name,caps[name],retain=False) for name in caps}
        control={'schema':'pr110-native-worker-control/v1','fixture':False,'packet_sha256':sha(packet_bytes),'backend':str(backend),
          'resources':packet['resources'],'caps':caps,'SQL_cache':cache['absolute_path'],'SQL_pin':cache['pin'],'record_count':15458,'revision':p.REV,'pre_assess_pins':pre_assess}
        control_bytes=canonical(control);w.atomic_write(workspace,'WORKER_CONTROL.json',control_bytes,512*1024);watch()
        _,process=runner.run([packet['runtime']['binaries']['python']['resolved_absolute_path'],'-E','-S','-B','-P',str(workspace/'native_worker.py'),
                            '--control',str(workspace/'WORKER_CONTROL.json')],workspace,w.clean_environment(),deadline=policy['deadline_seconds'],watch=watch,allow_failure=True)
        result=p.loads(w.read_file(workspace/'WORKER_RESULT.json',128*1024))
        need(process['exit_code']==0 and process['termination_reason'] is None and process['reaped'] and process['process_group_absence_confirmed'] and result['outcome']=='success' and
          result['native_assess_call_attempted'] is True and result['native_assess_completed'] is True and result['actual_worker_PID']==process['PID'] and result['packet_sha256']==sha(packet_bytes) and
          result['control_sha256']==sha(control_bytes) and same(result['validated_control'],control),'Actual native worker/control/result correspondence')
        need(result['schema']=='pr110-actual-native-worker-result/v1' and same(result['startup'],{'PID':process['PID'],
          'argv':[str(workspace/'native_worker.py'),'--control',str(workspace/'WORKER_CONTROL.json')],'cwd':str(workspace),
          'environment_sha256':process['environment_sha256'],'Python_ignore_environment':True,'Python_no_site':True,'Python_no_bytecode':True,'Python_safe_path':True}) and
          p.stamp(process['UTC_start'])<=p.stamp(result['UTC_start'])<=p.stamp(result['UTC_end'])<=p.stamp(process['UTC_end']), 'Actual startup and worker/outer process chronology')
        need(w.read_file(workspace/'WORKER_CONTROL.json',512*1024)==control_bytes and
          same(result['limits']['requested'],packet['resources']) and same(result['limits']['enforced'],{
            'RLIMIT_CPU':[packet['resources']['cpu_seconds']]*2,'RLIMIT_FSIZE':[packet['resources']['file_size_bytes']]*2,
            'RLIMIT_NOFILE':[packet['resources']['open_files']]*2}) and result['limits']['memory']['hard_memory_limit_claimed'] is False,'Actual applied resource readbacks')
        after={name:w.read_file(backend/name,caps[name],result['output_pins'][name]) for name in p.NATIVE}
        scoped,drift=p.scoped_outputs(before,after,overlay,event,note,doi);scoped=format_scoped_json(before,scoped,p)
        live_checks(packet,runner,w,p);validate_runtime(packet['runtime'],w,p)
        w.check_cache(cache['absolute_path'],cache['pin'],p.REV,15458,original['source_record.json'],original['prior_imported_report.json'])
        for name,spec in packet['raw_source_pins'].items():w.read_file('/Users/alec/Documents/Math/unsolved_math_prioritization/cache/'+name,128*1024*1024,spec,retain=False)
        for spec in packet['input_files']:w.read_file(audit_path(spec),8*1024*1024,spec,retain=False)
        for name,spec in packet['native_baseline'].items():
            if os.path.lexists(C/spec['path']):w.read_file(C/spec['path'],32*1024*1024,spec,retain=False)
        generated_bodies={'IMPORT_BASELINE.json':canonical(event),'HISTORICAL_DESK_ASSESSMENT.json':canonical(oldass[p.K]),
          'assessment.json':canonical(p.loads(after['assessments.json'])[p.K]),
          'PUBLICATION_EVIDENCE.json':canonical({'schema':'pr110-published-native-candidate-evidence/v1','original_head':p.HEAD,'review_hash':p.REVIEW,
             'statement_hash':p.STATEMENT,'DOI':doi,'Sheet_range':selected,'package_manifest_sha256':sha(package_bytes),'packet_sha256':sha(packet_bytes),
             'original_budget':'2/5','new_central_proof_search_turns':0,'prior_report_pin':p.PRIOR_PIN,'literal_native_status':'claimed_solved'}),
          'ACCEPTANCE_EVIDENCE.json':canonical({'schema':'pr110-reviewed-full-resolution-native-candidate/v1','accepted_mathematical_full_resolution':True,
             'actual_Zenodo_and_GWS_independently_authenticated_by_root':True,'native_status':'claimed_solved','turns_used':2,
             'original_structured_ledger_present':False,'packet_sha256':sha(packet_bytes),'actual_worker_PID':process['PID'],
             'candidate_only':True,'live_native_acceptance_executed':False,'native_export_executed':False,'fresh_candidate_review_required':True}),
          'README.md':('# '+p.K+' focal antipedal equality\n\nLiteral original claimed_solved, two of five turns; nonempty imported prior and all original seventeen files preserved. '
             'IMPORT_BASELINE is a dated import, not a recovered historical structured ledger. No new central proof-search turn. '
             'The exact strictly nested elliptical-caustic ordinary-positive norm-sum claim and source observation credit are retained; novelty is bounded. '
             'Reviewed full-resolution/publication evidence is separate from the literal native status. Private candidate awaits actual export review. DOI: https://doi.org/'+doi+'\n').encode(),
          'RESEARCH_LOG.md':('# PR110 native import log\n\n'+utc()+': Private native candidate preparation 95% pending independent candidate DIFF/readbacks and authorized export; '
             'original claimed_solved2/5 imported, no fabricated readiness/candidate ledger, no extra proof turn.\n').encode()}
        alloffers={**offer_bodies,**{N+name:body for name,body in scoped.items()},**{prefix+name:body for name,body in generated_bodies.items()}}
        offerroot=w.safe_mkdir(workspace,'offer');affected=[]
        for name,body in alloffers.items():
            path=offerroot/name;cur=offerroot
            for part in pathlib.PurePosixPath(name).parts[:-1]:
                nxt=cur/part
                if not nxt.exists():w.safe_mkdir(cur,part)
                else:fd=w.directory_fd(nxt);os.close(fd)
                cur=nxt
            w.atomic_write(cur,path.name,body,allowed['offer/'+name]);need(w.read_file(path,allowed['offer/'+name])==body,'Every offered file readback')
            old=before.get(name[len(N):]) if name in {N+n for n in p.DERIVED} else None
            affected.append({'path':name,'before':None if old is None else pin(old),'after':pin(body)})
        diff=full_diff(before,alloffers,prefix)
        w.atomic_write(workspace,'DIFF.txt',diff,1024*1024)
        receipt={'schema':'pr110-actual-private-native-candidate/v1','UTC':utc(),'operator_PID':os.getpid(),'packet_sha256':sha(packet_bytes),
          'main_parent':packet['main_parent'],'original_head':p.HEAD,'native_assess_actual_PID':process['PID'],'native_status':'claimed_solved','turns_used':2,
          'new_central_proof_search_turns':0,'nonempty_prior_preserved':True,'unrelated_projection_drift_restored':drift,'affected_paths':affected,
          'capacity_before_final_receipt':watch(),'parent_limits':parent_limits,'DIFF_pin':pin(diff),'native_export_executed':False,'Git_mutations':0,'service_writes':0,'fresh_candidate_adversary_and_root_review_required':True}
        w.atomic_write(workspace,'CANDIDATE_RECEIPT.json',canonical(receipt),128*1024);final_capacity=watch()
        print(json.dumps({'candidate':str(workspace),'packet_sha256':sha(packet_bytes),'affected_paths':len(affected),'final_capacity':final_capacity,'native_export_executed':False}))
    except BaseException as error:
        failure={'schema':'pr110-actual-private-native-failure/v1','UTC':utc(),'operator_PID':os.getpid(),'packet_sha256':sha(packet_bytes),
          'error_type':type(error).__name__,'error':str(error)[:1200],'candidate_must_not_be_exported':True,'native_export_executed':False}
        try:w.atomic_write(workspace,'FAILURE.json',canonical(failure),65536)
        except BaseException:pass
        raise

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--config',required=True);execute(parser.parse_args().config)
