#!/usr/bin/env python3
"""Future PR110 bounded native-assess worker. Never run on genuine inputs during preparation."""
import sys, os
def clean_environment():
    env={'PATH':'/usr/bin:/bin','LC_ALL':'C','LANG':'C','TZ':'UTC'}
    if sys.platform=='darwin':env['__CF_USER_TEXT_ENCODING']='0x'+format(os.getuid(),'X')+':0x0:0x0'
    return env
def need(ok,message):
    if not ok:raise ValueError(message)
def startup():
    need(sys.flags.ignore_environment and sys.flags.no_site and sys.flags.dont_write_bytecode and getattr(sys.flags,'safe_path',False),'Python -E -S -B -P required before imports')
    need(dict(os.environ)==clean_environment(),'Exact clean startup environment required')
if __name__=='__main__':startup()
import argparse, datetime, hashlib, io, json, pathlib, resource, signal, sqlite3, stat, types
A_ROOT=pathlib.Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr110_5100032')
D_CODE=A_ROOT/'native_execution_programs_v1'
C_ROOT=A_ROOT.parents[2]

def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def canonical(obj):return (json.dumps(obj,sort_keys=True,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
def loads(body):
    def pairs(items):
        out={}
        for key,value in items:need(key not in out,'Duplicate JSON key');out[key]=value
        return out
    def bad(value):raise ValueError('Nonfinite JSON '+value)
    return json.loads(body,object_pairs_hook=pairs,parse_constant=bad)
def sha(body):return hashlib.sha256(body).hexdigest()
def pin(body):return {'bytes':len(body),'sha256':sha(body)}
def same(a,b):return canonical(a)==canonical(b)
def directory_fd(path):
    path=pathlib.Path(path)
    need(path.is_absolute() and '..' not in path.parts,'Absolute canonical filesystem path')
    fd=os.open('/',os.O_RDONLY|os.O_DIRECTORY)
    try:
        for part in path.parts[1:]:
            nxt=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd);os.close(fd);fd=nxt
        return fd
    except BaseException:os.close(fd);raise
def read_file(path,cap,expected=None,retain=True):
    path=pathlib.Path(path);fd=directory_fd(path.parent)
    try:
        filefd=os.open(path.name,os.O_RDONLY|os.O_NOFOLLOW,dir_fd=fd)
        try:
            first=os.fstat(filefd);need(stat.S_ISREG(first.st_mode) and first.st_nlink==1 and first.st_size<=cap,'Regular unique-link bounded input required')
            h=hashlib.sha256();blocks=[];count=0
            while True:
                block=os.read(filefd,1024*1024)
                if not block:break
                count+=len(block);need(count<=cap,'Input grew beyond cap');h.update(block)
                if retain:blocks.append(block)
            last=os.fstat(filefd)
            need((first.st_dev,first.st_ino,first.st_size,first.st_mtime_ns)==(last.st_dev,last.st_ino,last.st_size,last.st_mtime_ns) and
                 count==last.st_size,'Input changed while reading')
            result={'bytes':count,'sha256':h.hexdigest()}
            if expected is not None:need(same(result,{k:expected[k] for k in ['bytes','sha256']}),'Input byte pin changed')
            return b''.join(blocks) if retain else result
        finally:os.close(filefd)
    finally:os.close(fd)
def safe_mkdir(parent,name):
    need(isinstance(name,str) and name and len(name.encode())<=255 and not any(c in name for c in '/\\\0') and name not in ['.','..'],'Single new directory name')
    fd=directory_fd(parent)
    try:os.mkdir(name,mode=0o700,dir_fd=fd)
    finally:os.close(fd)
    return pathlib.Path(parent)/name
def atomic_write(root,name,body,cap,replace=False,expected=None):
    need(isinstance(body,bytes) and len(body)<=cap and isinstance(name,str) and name and len(name.encode())<=255 and
         not any(c in name for c in '/\\\0') and name not in ['.','..'] and (not replace or expected is not None),'Exact bounded output name/body/preimage')
    fd=directory_fd(root);temp=name+'.tmp';created=False
    try:
        try:existing=os.stat(name,dir_fd=fd,follow_symlinks=False)
        except FileNotFoundError:existing=None
        if existing is not None:
            need(replace and stat.S_ISREG(existing.st_mode) and existing.st_nlink==1,'Output collision or unsafe existing file')
            if expected is not None:read_file(pathlib.Path(root)/name,cap,expected)
        else:need(not replace or expected is None,'Missing expected output preimage')
        tmpfd=os.open(temp,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600,dir_fd=fd);created=True
        try:
            offset=0
            while offset<len(body):offset+=os.write(tmpfd,body[offset:])
            os.fsync(tmpfd)
        finally:os.close(tmpfd)
        # Recheck the named preimage immediately before the atomic rename.
        if expected is not None:read_file(pathlib.Path(root)/name,cap,expected)
        if not replace:
            # link is exclusive, preventing an absent-name race from overwriting.
            os.link(temp,name,src_dir_fd=fd,dst_dir_fd=fd,follow_symlinks=False);os.unlink(temp,dir_fd=fd)
        else:os.replace(temp,name,src_dir_fd=fd,dst_dir_fd=fd)
        created=False;os.fsync(fd)
    finally:
        if created:
            try:os.unlink(temp,dir_fd=fd)
            except FileNotFoundError:pass
        os.close(fd)
def limits_policy(value):
    need(set(value)=={'cpu_seconds','file_size_bytes','open_files','memory_advisory_bytes','hard_memory_claimed'},'Exact resource policy')
    need(all(type(value[k]) is int for k in value if k!='hard_memory_claimed') and value['hard_memory_claimed'] is False,'Typed resources/no hard memory claim')
    need(1<=value['cpu_seconds']<=90 and 1<=value['file_size_bytes']<=32*1024*1024 and 16<=value['open_files']<=64 and
         128*1024*1024<=value['memory_advisory_bytes']<=1024*1024*1024,'Resource bounds')
def apply_limits(value):
    limits_policy(value);actual={}
    for name,key in [('RLIMIT_CPU','cpu_seconds'),('RLIMIT_FSIZE','file_size_bytes'),('RLIMIT_NOFILE','open_files')]:
        limit=value[key];resource.setrlimit(getattr(resource,name),(limit,limit));actual[name]=list(resource.getrlimit(getattr(resource,name)))
        need(actual[name]==[limit,limit],'Resource readback differs')
    return {'requested':value,'enforced':actual,'memory':{'platform':sys.platform,
      'requested_advisory_bytes':value['memory_advisory_bytes'],'hard_memory_limit_claimed':False,
      'RLIMIT_AS_used':False,'RLIMIT_RSS_used':False}}
def module_from_bytes(name,body,path):
    module=types.ModuleType(name);module.__file__=str(path);sys.modules[name]=module
    exec(compile(body,str(path),'exec'),module.__dict__);return module
def check_cache(path,expected,revision,count,source_bytes,prior_bytes):
    path=pathlib.Path(path)
    need(str(path)=='/Users/alec/Documents/Math/unsolved_math_prioritization/cache/catalog.sqlite','Exact shared read-only SQL path')
    for suffix in ['-wal','-shm','-journal']:
        try:os.lstat(str(path)+suffix)
        except FileNotFoundError:pass
        else:raise ValueError('SQL writer sidecar present')
    read_file(path,256*1024*1024,expected,retain=False)
    db=sqlite3.connect('file:'+str(path)+'?mode=ro&immutable=1',uri=True)
    try:
        need(db.execute('SELECT revision FROM metadata').fetchone()==(revision,) and db.execute('SELECT count(*) FROM records').fetchone()[0]==count,'SQL revision/count')
        row=db.execute('SELECT payload,report FROM records WHERE key=?',('5100032',)).fetchone()
        need(row is not None and same(loads(row[0]),loads(source_bytes)) and same(loads(row[1]),loads(prior_bytes)) and bool(loads(row[1])),'SQL exact nonempty sourcepair')
    finally:db.close()

def guarded_native_paths(backend,caps):
    base=type(pathlib.Path())
    class TextSlot(io.StringIO):
        def __init__(self,path,mode,newline):
            self.path=path;self.name=path.name;self.cap=caps[self.name]
            prior=read_file(path,self.cap);self.preimage=pin(prior)
            initial=prior.decode('utf8') if mode=='a' else ''
            super().__init__(initial,newline=newline)
            if mode=='a':self.seek(0,io.SEEK_END)
        def write(self,text):
            need(isinstance(text,str),'Native text writes only')
            position=self.tell();need(position+len(text)<=self.cap,'Native text character cap')
            result=super().write(text);need(len(self.getvalue().encode())<=self.cap,'Native text byte cap');return result
        def close(self):
            if not self.closed:atomic_write(backend,self.name,self.getvalue().encode(),self.cap,replace=True,expected=self.preimage)
            super().close()
    class SafePath(base):
        def check(self):need(self.parent==pathlib.Path(backend) and self.name in caps,'Native path outside exact private backend');return self
        def read_text(self,encoding=None,errors=None):return read_file(self.check(),caps[self.name]).decode(encoding or 'utf8',errors or 'strict')
        def write_text(self,data,encoding=None,errors=None,newline=None):
            self.check();body=data.encode(encoding or 'utf8',errors or 'strict');old=read_file(self,caps[self.name])
            atomic_write(backend,self.name,body,caps[self.name],replace=True,expected=pin(old));return len(data)
        def open(self,mode='r',buffering=-1,encoding=None,errors=None,newline=None):
            self.check();need(mode in ['r','w','a'] and encoding in [None,'utf8','utf-8'] and errors in [None,'strict'],'Native allowed text open modes')
            if mode=='r':return io.StringIO(read_file(self,caps[self.name]).decode(),newline=newline)
            return TextSlot(self,mode,newline)
        def exists(self):
            self.check()
            try:read_file(self,caps[self.name],retain=False);return True
            except FileNotFoundError:return False
    return SafePath

def derive_caps(baseline,resources):
    return {name:min(resources['file_size_bytes'],baseline[name]['bytes']+256*1024) for name in baseline}|{'assessment.json':65536}
def execute(control_path):
    startup();control_path=pathlib.Path(control_path);root=control_path.parent
    control_bytes=read_file(control_path,512*1024);control=loads(control_bytes)
    need(control_path.name=='WORKER_CONTROL.json' and control['schema']=='pr110-native-worker-control/v1' and control['fixture'] is False,'Actual worker control only')
    packet_bytes=read_file(root/'EXECUTION_INPUTS.json',512*1024);packet=loads(packet_bytes)
    need(packet['template_only'] is False and packet['schema']=='pr110-concrete-native-inputs/v1' and sha(packet_bytes)==control['packet_sha256'],'Immutable worker packet')
    need(root.name=='candidate_'+sha(packet_bytes)[:16] and root.parent==D_CODE/'workspaces' and
         str(root.parent)==packet['workspace_parent'],'Exact unique private workspace')
    family={}
    for name,spec in packet['program_files'].items():
        body=read_file(root/name,128*1024,spec);family[name]=body
    need(set(family)=={'native_worker.py','native_runner.py','native_launcher.sh','protocol.py'},'Entire staged program family')
    need(read_file(pathlib.Path(__file__),128*1024)==family['native_worker.py'],'Executing worker bytes differ')
    approval=loads(read_file(root/'ROOT_COMMISSION.json',128*1024));adversary=loads(read_file(root/'PREEXEC_ADVERSARY.json',128*1024))
    for obj,role in [(approval,'root'),(adversary,'adversary')]:
        need(obj['schema']=='pr110-concrete-native-commission/v1' and obj['role']==role and obj['actual_review'] is True and obj['clearance'] is True and
             obj['packet_sha256']==sha(packet_bytes) and same(obj['program_hashes'],{n:sha(b) for n,b in family.items()}) and
             obj['template_only'] is False and obj.get('fixture',False) is False,'Worker lacks exact actual commissioning')
    p=module_from_bytes('protocol',family['protocol.py'],root/'protocol.py')
    backend=root/'private_native_backend';resources=packet['resources'];limits_policy(resources)
    need(same(control['resources'],resources) and control['backend']==str(backend) and
         same(control['caps'],derive_caps(packet['native_baseline'],resources)) and control['SQL_cache']==packet['source_cache']['absolute_path'] and
         same(control['SQL_pin'],packet['source_cache']['pin']) and control['record_count']==15458 and control['revision']==p.REV,'Exact derived worker control')
    need(set(control)=={'schema','fixture','packet_sha256','backend','resources','caps','SQL_cache','SQL_pin','record_count','revision','pre_assess_pins'},'Worker control fields')
    need(set(control['pre_assess_pins'])==set(p.NATIVE)|{'assessment.json'},'Complete exact pre-assess file pins')
    for name,spec in control['pre_assess_pins'].items():read_file(backend/name,control['caps'][name],spec)
    source=read_file(root/'SOURCE_RECORD.json',65536,p.SOURCE_PIN);prior=read_file(root/'PRIOR_REPORT.json',65536,p.PRIOR_PIN);p.sourcepair(source,prior)
    state=loads(read_file(backend/'state.json',control['caps']['state.json']))
    need(same(state[p.K],p.imported_baseline(packet['import_UTC'],p.ORIGINAL_ROW_SHA,p.ORIGINAL_LOG_SHA)),'Exact original two-turn imported state')
    result={'schema':'pr110-actual-native-worker-result/v1','actual_worker_PID':os.getpid(),'UTC_start':now(),'packet_sha256':sha(packet_bytes),
      'control_sha256':sha(control_bytes),'validated_control':control,'native_assess_call_attempted':False,'native_assess_completed':False,'outcome':'failure','limits':None,
      'startup':{'PID':os.getpid(),'argv':sys.argv,'cwd':os.getcwd(),'environment_sha256':sha(canonical(dict(os.environ))),
        'Python_ignore_environment':bool(sys.flags.ignore_environment),'Python_no_site':bool(sys.flags.no_site),'Python_no_bytecode':bool(sys.flags.dont_write_bytecode),
        'Python_safe_path':bool(sys.flags.safe_path)}}
    try:
        def terminated(sig,frame):raise SystemExit('Actual worker termination signal '+signal.Signals(sig).name)
        signal.signal(signal.SIGTERM,terminated);signal.signal(signal.SIGINT,terminated)
        result['limits']=apply_limits(resources)
        check_cache(control['SQL_cache'],control['SQL_pin'],p.REV,15458,source,prior)
        queue=read_file(backend/'queue.py',65536);need(sha(queue)==p.QUEUE_SHA,'Native runtime source changed')
        native=module_from_bytes('pr110_pinned_native_queue',queue,backend/'queue.py')
        SafePath=guarded_native_paths(backend,control['caps']);native.ROOT=SafePath(backend);native.pathlib=types.SimpleNamespace(Path=SafePath)
        def ro():return sqlite3.connect('file:'+control['SQL_cache']+'?mode=ro&immutable=1',uri=True)
        def cache_check():
            db=ro()
            try:need(db.execute('SELECT revision FROM metadata').fetchone()==(p.REV,) and db.execute('SELECT count(*) FROM records').fetchone()[0]==15458,'Native read-only cache metadata')
            finally:db.close()
        def native_json_write(path,obj):
            need(path.parent==backend and path.name in control['caps'],'Native JSON output scope')
            body=(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode();old=read_file(path,control['caps'][path.name])
            atomic_write(backend,path.name,body,control['caps'][path.name],replace=True,expected=pin(old))
        native.connect=ro;native.require_cache=cache_check;native.write=native_json_write
        result['native_assess_call_attempted']=True
        native.assess(types.SimpleNamespace(id=p.K,file=str(backend/'assessment.json')))
        result['native_assess_completed']=True
        check_cache(control['SQL_cache'],control['SQL_pin'],p.REV,15458,source,prior)
        result['output_pins']={name:read_file(backend/name,control['caps'][name],retain=False) for name in p.NATIVE}
        result['outcome']='success'
    except BaseException as error:result.update(error_type=type(error).__name__,error=str(error)[:1000])
    usage=resource.getrusage(resource.RUSAGE_SELF)
    result['resource_usage']={'user_CPU_seconds':usage.ru_utime,'system_CPU_seconds':usage.ru_stime,'maximum_RSS':usage.ru_maxrss,
      'maximum_RSS_units':'bytes' if sys.platform=='darwin' else 'KiB','hard_memory_limit_claimed':False}
    result['UTC_end']=now();atomic_write(root,'WORKER_RESULT.json',canonical(result),128*1024)
    need(result['outcome']=='success','Actual native worker failed; receipt preserved')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--control',required=True);execute(parser.parse_args().control)
