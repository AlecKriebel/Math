#!/usr/bin/env python3
"""Fresh read-only source/runtime/main probe. Does not assess or export."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,platform,selectors,shutil,signal,sqlite3,stat,subprocess,sys,time
A=Path(__file__).resolve().parents[1];C=A.parents[2]
def need(v,m):
    if not v:raise RuntimeError(m)
def now():return datetime.now(timezone.utc).isoformat()
def canonical(v):return (json.dumps(v,sort_keys=True,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
def hp(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def read(p):return json.loads(p.read_text())
def filepin(p):
    h=hashlib.sha256();n=0
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):n+=len(b);h.update(b)
    return {'bytes':n,'sha256':h.hexdigest()}
def clean():
    v={'PATH':'/usr/bin:/bin','LANG':'C','LC_ALL':'C','TZ':'UTC'}
    if sys.platform=='darwin':v['__CF_USER_TEXT_ENCODING']='0x'+format(os.getuid(),'X')+':0x0:0x0'
    return v
def invocation(path,version):
    original=Path(path);pending=list(original.parts[1:]);base=Path('/');chain=[]
    while pending:
        part=pending.pop(0);p=base/part;s=p.lstat()
        if stat.S_ISLNK(s.st_mode):
            target=os.readlink(p);need(len(chain)<32 and str(p) not in {r['path'] for r in chain},'Runtime symlink loop')
            chain.append({'path':str(p),'target':target,'target_utf8_sha256':hashlib.sha256(target.encode()).hexdigest()})
            resolved=os.path.normpath(target if os.path.isabs(target) else str(base/target));pending=list(Path(resolved).parts[1:])+pending;base=Path('/')
        else:base=p
    need(base.is_file() and base.stat().st_nlink==1,'Resolved runtime regular unique file')
    return {'invocation_path':str(original),'resolved_absolute_path':str(base),'symlink_chain':chain,**filepin(base),'version':version}
def main():
    expected=sys.argv[1];label=sys.argv[2];D=A/'native_actual_input_preparation_20261006'/label;D.mkdir(parents=True,exist_ok=False);ops=[]
    def run(argv,env=None):
        start=now();p=subprocess.Popen(argv,cwd=C,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
        termination=None;begin=time.monotonic();sel=selectors.DefaultSelector()
        is_git_body=len(argv)>=3 and 'show' in argv and argv[-1].startswith(expected+':')
        caps={'stdout':32*1024*1024 if is_git_body else 65536,'stderr':65536};buffers={k:bytearray() for k in caps};counts={k:0 for k in caps};hashes={k:hashlib.sha256() for k in caps}
        for name,stream in [('stdout',p.stdout),('stderr',p.stderr)]:os.set_blocking(stream.fileno(),False);sel.register(stream,selectors.EVENT_READ,name)
        def kill(reason):
            nonlocal termination
            if termination is None:
                termination=reason
                try:os.killpg(p.pid,signal.SIGKILL)
                except ProcessLookupError:pass
        while sel.get_map() or p.poll() is None:
            if time.monotonic()-begin>45:kill('deadline_KILL_and_reap')
            if time.monotonic()-begin>48:break
            for key,_ in sel.select(.1):
                b=os.read(key.fileobj.fileno(),65536);name=key.data
                if not b:sel.unregister(key.fileobj);key.fileobj.close();continue
                counts[name]+=len(b);hashes[name].update(b);buffers[name].extend(b[:max(0,caps[name]-len(buffers[name]))])
                if counts[name]>caps[name]:kill(name+'_cap_KILL_and_reap')
        drained=not bool(sel.get_map());sel.close()
        if p.poll() is None:kill('final_KILL_and_reap')
        try:p.wait(timeout=3)
        except subprocess.TimeoutExpired:termination='unreaped_operator_intervention_required'
        for stream in (p.stdout,p.stderr):
            if not stream.closed:stream.close()
        out,err=bytes(buffers['stdout']),bytes(buffers['stderr']);i=len(ops);streams={}
        for kind,body in [('stdout',out),('stderr',err)]:
            observed={'observed_bytes':counts[kind],'observed_sha256':hashes[kind].hexdigest(),'streams_fully_drained':drained}
            if kind=='stdout' and is_git_body and termination is None and drained:
                streams[kind]={**hp(body),**observed,'body_custody':'immutable_Git_blob_full_body','git_commit_path':argv[-1]}
            else:
                f=D/(str(i)+'.'+kind+'.bin');f.write_bytes(body)
                streams[kind]={'path':str(f.relative_to(A)),**hp(body),**observed,'body_custody':'full_actual_raw_CLI_stream' if drained and len(body)==counts[kind] else 'explicitly_truncated_actual_CLI_prefix'}
        ops.append({'argv':argv,'cwd':str(C),'actual_PID':p.pid,'UTC_start':start,'UTC_end':now(),'exit_code':p.returncode,'reaped':p.returncode is not None,'termination_reason':termination,'environment_sha256':hashlib.sha256(json.dumps(dict(os.environ) if env is None else env,sort_keys=True,separators=(',',':')).encode()).hexdigest(),**streams})
        (D/'PROCESS_JOURNAL.json').write_bytes(canonical({'actual_operator_PID':os.getpid(),'operations':ops}));need(p.returncode==0 and termination is None and drained,'Readonly process failed; real failure envelope retained')
        return out
    paths={'python':'/opt/homebrew/bin/python3','git':'/opt/homebrew/bin/git','gh':'/opt/homebrew/bin/gh','gws':'/Users/alec/.nvm/versions/node/v22.16.0/bin/gws','node':'/opt/homebrew/bin/node','sh':'/bin/sh','env':'/usr/bin/env'}
    need(shutil.which('node')==paths['node'],'Actual ambient Node PATH selection differs from declared current snapshot')
    pkg=Path(paths['gws']).resolve().parent
    dependencies={name:{'absolute_path':str(pkg/rel),**filepin(pkg/rel)} for name,rel in [('gws_package_json','package.json'),('gws_platform_js','platform.js'),('gws_native_backend','bin/gws')]}
    pkgdata=read(pkg/'package.json');key=('aarch64' if platform.machine()=='arm64' else 'x86_64')+'-apple-darwin'
    need(sys.platform=='darwin' and pkgdata['supportedPlatforms'][key]['binary']=='gws' and (pkg/'bin/gws').is_file(),'Current GWS native backend exists; installer branch is ineligible')
    bins={}
    for role,path in paths.items():
        command=str(pkg/'bin/gws') if role=='gws' else str(Path(path).resolve())
        version=run([command,'--version']).decode().strip() if role not in ('sh','env') else 'macOS system executable; exact bytes pinned'
        bins[role]=invocation(path,version)
    need(str(Path(sys.executable))==bins['python']['resolved_absolute_path'],'Probe must execute resolved physical Python')
    ghdir=Path('/Users/alec/.config/gh');private=[{'role':'git','absolute_path':str(C/'.git/config'),**filepin(C/'.git/config'),'body_private':True}]
    if (C/'.git/config.worktree').exists():private.append({'role':'git','absolute_path':str(C/'.git/config.worktree'),**filepin(C/'.git/config.worktree'),'body_private':True})
    for f in sorted(ghdir.iterdir()):need(f.name in ('config.yml','hosts.yml','state.yml') and not f.is_symlink(),'Unexpected GH config');private.append({'role':'gh','absolute_path':str(f),**filepin(f),'body_private':True})
    for dependency in dependencies.values():need(filepin(dependency['absolute_path'])=={k:dependency[k] for k in ('bytes','sha256')},'GWS dependency changed during current version inspection')
    runtime={'UTC':now(),'pin_scope':'fresh_current_preflight_only','historical_binary_bytes_attested':False,'binaries':bins,'dependency_files':dependencies,'python_environment':clean(),'gh_config_directory':str(ghdir),'private_configuration_pins':private}
    git=[bins['git']['resolved_absolute_path'],'-c','core.fsmonitor=false','-c','core.hooksPath=/dev/null','-c','credential.helper='];env={**clean(),'GIT_CONFIG_NOSYSTEM':'1','GIT_CONFIG_GLOBAL':'/dev/null','GIT_CONFIG_SYSTEM':'/dev/null','GIT_OPTIONAL_LOCKS':'0','GIT_NO_REPLACE_OBJECTS':'1','GIT_TERMINAL_PROMPT':'0'}
    need(run(git+['rev-parse','HEAD'],env).decode().strip()==expected and run(git+['symbolic-ref','--short','HEAD'],env).strip()==b'main','Current main/branch')
    need(run(git+['ls-remote','https://github.com/AlecKriebel/Math.git','refs/heads/main'],env).decode().split()[0]==expected,'Remote main')
    need(not run(git+['diff','--cached','--name-only','-z'],env),'Foreign staged changes')
    ghenv={**clean(),'GH_CONFIG_DIR':str(ghdir),'GH_HOST':'github.com','GH_PROMPT_DISABLED':'1','GH_PAGER':'','GH_BROWSER':'/usr/bin/false','GH_EDITOR':'/usr/bin/false','GH_NO_UPDATE_NOTIFIER':'1'}
    pr=json.loads(run([bins['gh']['resolved_absolute_path'],'pr','view','https://github.com/AlecKriebel/Math/pull/110','--json','number,state,isDraft,headRefOid,baseRefName,headRefName'],ghenv))
    need(pr=={'number':110,'state':'OPEN','isDraft':True,'headRefOid':'3d159f0a00d0bd7ff8d558d6fbc75af5094f7a35','baseRefName':'main','headRefName':'dot/math-5100032'},'Exact original open draft')
    names=['queue.py','manifest.json','policy.json','catalog.json','assessments.json','state.json','history.jsonl','assessment_history.jsonl','ranking.csv','summary.json','SHORTLIST.md','QUEUE.md'];baseline={};target=None
    for name in names:
        rel='unsolved_math_prioritization/'+name;body=run(git+['show',expected+':'+rel],env);baseline[name]={'path':rel,**hp(body)}
        if (C/rel).exists():need(filepin(C/rel)==hp(body),'Materialized baseline drift')
        if name=='catalog.json':target=next(r for r in json.loads(body) if r['id']=='5100032');need(target['local_status']=='queued' and target['turns_used']==0,'Target native baseline')
        if name=='state.json':need('5100032' not in json.loads(body),'Unexpected target native state')
        if name=='manifest.json':manifest=json.loads(body)
    sourceauth=read(A/'original_head_authentication_20261006/SOURCEPAIR_AUTHENTICATION.json');wanted={Path(e['path']).name:e for e in sourceauth['input_pins'] if '/cache/' in e['path']};raw={}
    for name in ('problems.json','research_results.json','catalog.sqlite'):
        f=Path(wanted[name]['path']);need(filepin(f)=={k:wanted[name][k] for k in ('bytes','sha256')},'Full immutable source/cache drift')
        if name!='catalog.sqlite':raw[name]=filepin(f)
    cache=Path(wanted['catalog.sqlite']['path'])
    need(not any(os.path.lexists(str(cache)+s) for s in ('-wal','-shm','-journal')),'SQL writer sidecars present')
    db=sqlite3.connect('file:'+str(cache)+'?mode=ro&immutable=1',uri=True)
    try:
        need(db.execute('SELECT revision FROM metadata').fetchone()==(sourceauth['dataset_revision'],) and db.execute('SELECT count(*) FROM records').fetchone()[0]==15458,'SQL revision/count')
        row=db.execute('SELECT payload,report FROM records WHERE key=?',('5100032',)).fetchone()
        for i,name in enumerate(('source_record.json','prior_imported_report.json')):need(canonical(json.loads(row[i]))==canonical(read(A/'original_head_authentication_20261006/original_attempt'/name)),'Actual nonempty sourcepair SQL mismatch')
    finally:db.close()
    need(bool(json.loads(row[1])) and manifest['files']==raw and manifest['revision']==sourceauth['dataset_revision'] and manifest['records']==15458,'Native/raw source identity')
    need(not os.path.lexists(C/'unsolved_math_prioritization/attempts/5100032'),'Target native attempt appeared')
    result={'schema':'pr110-concrete-native-preflight/v1','actual_receipt':True,'template_only':False,'actual_reader_PID':os.getpid(),'UTC':now(),'main_parent':expected,'remote_main':expected,'branch':'main','original_head':pr['headRefOid'],'review_hash':target['review_hash'],'statement_hash':target['statement_hash'],'dataset_revision':sourceauth['dataset_revision'],'SQL_record_count':15458,'SQL_prior_equals_nonempty_original':True,'SQL_source_equals_original':True,'native_target_absent':True,'SQL_sidecars_absent':True,'live_PR':{'number':110,'head':pr['headRefOid'],'base':'main','state':'OPEN','isDraft':True},'full_native_baseline_and_runtime_independently_checked':True,'root_independently_authenticated_actual_preflight_processes':False,'native_baseline':baseline,'runtime':runtime,'source_cache':{'absolute_path':str(cache),'pin':filepin(cache)},'raw_source_pins':raw,'target_catalog_record':target,'fresh_current_runtime_not_retrospective_binary_proof':True,'process_journal':{'path':str((D/'PROCESS_JOURNAL.json').relative_to(A)),**filepin(D/'PROCESS_JOURNAL.json')},'native_assess_executed':False,'live_native_export_executed':False}
    (D/'PREFLIGHT.json').write_bytes(canonical(result));print(json.dumps({'preflight_path':str(D/'PREFLIGHT.json'),'actual_reader_PID':os.getpid(),'UTC':result['UTC'],'processes':len(ops),'main_parent':expected}))
if __name__=='__main__':main()
