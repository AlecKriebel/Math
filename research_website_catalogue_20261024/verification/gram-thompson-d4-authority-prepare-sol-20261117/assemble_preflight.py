#!/usr/bin/env python3
"""SOURCE ONLY. Run once only after root reads these exact bytes and gives GO.
Usage: python3.14 assemble_preflight.py --assemble-preflight PRIVATE_EMPTY_DIR
The actor supplies a canonical empty0700 TEMP outside Math/W. No release helper
is imported or invoked. This only prepares preflight data, never later phases.
"""
import sys

def main():
    if sys.flags.optimize or sys.version_info[:2] != (3, 14) or sys.implementation.name != 'cpython':
        raise RuntimeError('unoptimized CPython3.14 required')
    if len(sys.argv) != 3 or sys.argv[1] != '--assemble-preflight':
        raise RuntimeError('explicit root GO and exact two arguments required')
    import datetime, hashlib, json, os, re, secrets, stat, subprocess, traceback
    from pathlib import Path
    P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024'); M = P.parent
    W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
    N = P/'verification/gram-thompson-d4-production-prepare-v3-sol-20261117'
    A = P/'verification/root-gram-thompson-d4-v3-source-adoption-20261117.json'
    OUT = P/'verification/root-gram-thompson-d4-preflight-authorization-20261117.json'
    E = Path(sys.argv[2])
    ignore_path = P/'verification/root-gram-thompson-d4-runtime-ignore-prerequisite-20261117.json'
    IGNORE_SHA = 'c7a59e62ab16817677cbefe4315b7015b8393ee72ccb72b4af066be285fe8d9a'
    REMOTE = '164a569600dd415f65d7d377541d1485fc43a904'
    ADOPT_SHA = '007b15062fa1f5d32a4277764956a897de17ae413b55c80ada75c99550d5892c'
    M_INDEX = {'bytes':25854746,'SHA256':'91b10d938f7d737226662bbff3b07016dcc0e501376a045811ab4e930c6fbb11','mode':'0644'}
    seq = 0

    def need(value, reason):
        if not value: raise ValueError(reason)
    def sha(raw): return hashlib.sha256(raw).hexdigest()
    def packed(value): return (json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':'))+'\n').encode()
    def pairs(rows):
        result = {}
        for key,value in rows:
            need(key not in result,'duplicate JSON key'); result[key] = value
        return result
    def parsed(raw):
        return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))
    def mode(path): return format(stat.S_IMODE(path.lstat().st_mode),'04o')
    def safe(path):
        need(path.is_absolute() and '..' not in path.parts,'absolute canonical path')
        need(all(not q.is_symlink() for q in (path,*path.parents)),'no symbolic path')
    def held(fd):
        before = os.fstat(fd); need(stat.S_ISREG(before.st_mode),'ordinary held file')
        os.lseek(fd,0,os.SEEK_SET); blocks = []
        while block := os.read(fd,1048576): blocks.append(block)
        after = os.fstat(fd)
        need((before.st_dev,before.st_ino,before.st_size,before.st_mode,before.st_mtime_ns,before.st_ctime_ns)==(after.st_dev,after.st_ino,after.st_size,after.st_mode,after.st_mtime_ns,after.st_ctime_ns),'stable whole read')
        raw = b''.join(blocks); need(len(raw)==before.st_size,'whole held bytes'); return raw
    def read(path):
        safe(path); before = path.lstat(); fd = os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
        try:
            need((before.st_dev,before.st_ino)==(os.fstat(fd).st_dev,os.fstat(fd).st_ino),'opened identity')
            raw = held(fd); after = path.lstat()
            need((after.st_dev,after.st_ino)==(before.st_dev,before.st_ino),'live held identity'); return raw
        finally: os.close(fd)
    def pin(path):
        raw = read(path); return {'bytes':len(raw),'SHA256':sha(raw),'mode':mode(path)}
    def external(path): return {'path':str(path),**pin(path)}
    def bound(row):
        need(set(row)=={'path','bytes','SHA256','mode'},'external pin shape')
        path = Path(row['path']); raw = read(path)
        need({'path':str(path),'bytes':len(raw),'SHA256':sha(raw),'mode':mode(path)}==row,'whole externally pinned file'); return raw
    def sync_dir(path):
        fd = os.open(path,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
        try: os.fsync(fd)
        finally: os.close(fd)
    def new(path,raw,permissions=0o600):
        safe(path); fd = os.open(path,os.O_RDWR|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,permissions)
        try:
            view = memoryview(raw)
            while view:
                count = os.write(fd,view); need(count>0,'complete write'); view = view[count:]
            os.fchmod(fd,permissions); os.fsync(fd); need(held(fd)==raw,'whole durable output')
        finally: os.close(fd)
        sync_dir(path.parent)
    def snapshot(root):
        files,dirs = [],[]
        def visit(directory):
            safe(directory); before = directory.stat()
            for q in sorted(directory.iterdir()):
                s = q.lstat(); name = q.relative_to(root).as_posix()
                if stat.S_ISDIR(s.st_mode): dirs.append({'path':name,'mode':mode(q)}); visit(q)
                else:
                    need(stat.S_ISREG(s.st_mode),'ordinary namespace object'); files.append({'path':name,**pin(q)})
            after = directory.stat()
            need((before.st_dev,before.st_ino,before.st_mode,before.st_mtime_ns,before.st_ctime_ns)==(after.st_dev,after.st_ino,after.st_mode,after.st_mtime_ns,after.st_ctime_ns),'stable finite namespace')
        visit(root)
        return {'root':str(root),'root_mode':mode(root),'files':sorted(files,key=lambda r:r['path']),'directories':sorted(dirs,key=lambda r:r['path']),'regular_files':len(files),'child_directories':len(dirs)}
    def git(root,*args,absent=False):
        nonlocal seq
        seq += 1; stem = E/format(seq,'04d')
        out,err = Path(str(stem)+'.stdout.bin'),Path(str(stem)+'.stderr.bin')
        fds = [os.open(q,os.O_RDWR|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600) for q in (out,err)]
        for fd in fds: os.fchmod(fd,0o600)
        sync_dir(E)
        argv = ['/usr/bin/git','--no-optional-locks','-c','core.hooksPath=/dev/null','-c','core.fsmonitor=false','-c','gc.auto=0','-c','maintenance.auto=false','-c','protocol.allow=never','-c','protocol.https.allow=always',*args]
        env = {k:v for k,v in os.environ.items() if not k.startswith('GIT_')}
        env.update(GIT_OPTIONAL_LOCKS='0',GIT_TERMINAL_PROMPT='0',GIT_NO_LAZY_FETCH='1',GIT_NO_REPLACE_OBJECTS='1')
        result,exception,captured,errors = None,None,{},[]
        new(Path(str(stem)+'.intent.json'),packed({'argv':argv,'cwd':str(root),'stdout':str(out),'stderr':str(err)}))
        try: result = subprocess.run(argv,cwd=root,env=env,stdout=fds[0],stderr=fds[1])
        except BaseException as error:
            exception = {'type':type(error).__name__,'repr':repr(error),'traceback':traceback.format_exc()}; raise
        finally:
            try:
                for label,fd,q in zip(('stdout','stderr'),fds,(out,err)):
                    try: os.fsync(fd); captured[label] = held(fd)
                    except BaseException as error: errors.append({'stream':label,'type':type(error).__name__,'repr':repr(error),'traceback':traceback.format_exc()})
                new(Path(str(stem)+'.return.json'),packed({'argv':argv,'exit':None if result is None else result.returncode,'exception':exception,'capture_errors':errors,'streams':{k:{'bytes':len(v),'SHA256':sha(v)} for k,v in captured.items()}}))
                need(not errors,'private capture failure; preserve and stop')
            finally:
                for fd in fds: os.close(fd)
        allowed = absent and args==('config','--null','--get-all','remote.origin.vcs') and result.returncode==1 and captured['stdout']==captured['stderr']==b''
        need(result.returncode==0 or allowed,'read-only Git failed; no retry'); return captured['stdout']
    def optional(path): return external(path) if os.path.lexists(path) else None
    def adopted_packet(packet):
        root = P/packet['path']; snap = snapshot(root); actual = {r['path']:{k:r[k] for k in ('bytes','SHA256','mode')} for r in snap['files']}
        need((snap['regular_files'],snap['child_directories'])==(packet['files'],packet['child_directories']),'exact adopted finite packet extent')
        for name,expected in packet['external_controls'].items():
            need(actual[name]['SHA256']==expected if isinstance(expected,str) else actual[name]==expected,'actual adopted external control')
        manifest = parsed(read(root/'MANIFEST.json')); schema = manifest['schema']
        entry_schemas = {'finite-owned-private-overlay-namespace-v1','finite-source-only-packet-manifest-v1'}
        payload_schemas = {'finite-original-failed-overlay-audit-manifest-v1','finite-corrected-private-overlay-audit-manifest-v1','finite-v3-production-static-audit-manifest-v1'}
        if schema in entry_schemas:
            rows = [r for r in manifest['entries'] if r['kind']=='file']; directories = [r for r in manifest['entries'] if r['kind']=='directory']
            if schema=='finite-source-only-packet-manifest-v1': directories = [{'path':'.','mode':manifest['root_mode']},*directories]
            terminal = manifest['terminal_content_hash_exclusions_exact']; need(terminal==['MANIFEST.json','SEAL.json'],'exact declared source/overlay terminal pair')
        else:
            need(schema in payload_schemas,'actual supported audit manifest schema')
            rows = manifest['payload_files']; directories = manifest['directories']; terminal = manifest['exact_already_created_terminal_recursive_hash_exclusions']
            need(terminal==['MANIFEST.json','FINAL.json'] and manifest['other_exclusions']==[],'exact declared audit terminal pair')
        expected_files = {}
        for row in rows:
            name = row['path']; q = root/name
            need(name not in expected_files,'unique declared packet file')
            if 'SHA256' in row:
                need(isinstance(row['SHA256'],str) and re.fullmatch('[0-9a-f]{64}',row['SHA256']),'actual payload SHA256')
                expected_files[name] = {'bytes':row['bytes'],'SHA256':row['SHA256'],'mode':format(int(row['mode'],8),'04o')}
            else:
                need(name in terminal and isinstance(row.get('content_hash_exclusion'),str),'only exact declared terminal marker')
                need(name in packet['external_controls'] and mode(q)==format(int(row['mode'],8),'04o'),'externally authenticated terminal/mode')
                expected_files[name] = actual[name]
            if 'mtime_ns' in row: need(q.lstat().st_mtime_ns==row['mtime_ns'],'declared packet mtime')
            if 'bytes' in row: need(actual[name]['bytes']==row['bytes'],'declared whole byte length')
            if 'empty' in row: need(row['empty']==(actual[name]['bytes']==0),'declared empty file')
            if 'hidden' in row: need(row['hidden']==any(part.startswith('.') for part in Path(name).parts),'declared hidden file')
        for name in terminal:
            need(name in packet['external_controls'],'every terminal externally pinned')
            if name not in expected_files:
                need(mode(root/name)==manifest['terminal_modes'][name],'exact terminal mode'); expected_files[name] = actual[name]
        expected_dirs = {r['path']:format(int(r['mode'],8),'04o') for r in directories}
        need(expected_files==actual and expected_dirs=={'.':snap['root_mode'],**{r['path']:r['mode'] for r in snap['directories']}},'whole sealed packet hashes/modes/finite topology')
        for row in directories:
            q = root if row['path']=='.' else root/row['path']
            if 'mtime_ns' in row: need(q.lstat().st_mtime_ns==row['mtime_ns'],'declared directory mtime')
            if 'empty' in row: need(row['empty']==(not any(q.iterdir())),'declared empty directory')
            if 'hidden' in row: need(row['hidden']==any(part.startswith('.') for part in Path(row['path']).parts if part!='.'),'declared hidden directory')
        return snap
    def routing(root,origin,regex):
        before = git(root,'config','--null','--show-origin','--show-scope','--get-regexp',regex)
        need(git(root,'config','--null','--get-all','remote.origin.vcs',absent=True)==b'','no external VCS helper')
        need(git(root,'remote','get-url','--all','origin')==git(root,'remote','get-url','--push','--all','origin')==(origin+'\n').encode(),'exact singleton intended origin')
        need(git(root,'config','--null','--show-origin','--show-scope','--get-regexp',regex)==before,'stable effective routing')
    def native(root,branch,expected):
        head = read(root/'.git/HEAD').decode('ascii'); need(head=='ref: '+branch+'\n','exact native symbolic branch')
        raw = read(root/'.git/packed-refs').decode('ascii'); heads = {}
        for line in raw.splitlines():
            if not line or line.startswith(('#','^')): continue
            oid,name = line.split(' ',1)
            if name.startswith('refs/heads/'): heads[name] = {'OID':oid,'raw_line':line}
        leaf = root/'.git'/branch
        oid = read(leaf).decode('ascii').strip() if os.path.lexists(leaf) else heads[branch]['OID']
        need(oid==expected,'actual native parent')
        return {'root':str(root),'HEAD':{**pin(root/'.git/HEAD'),'raw':head},'config':pin(root/'.git/config'),'index':pin(root/'.git/index'),'optional_worktree_config':None if not os.path.lexists(root/'.git/config.worktree') else pin(root/'.git/config.worktree'),'loose_local_heads':snapshot(root/'.git/refs/heads'),'packed_local_heads':heads,'packed_refs_mode':mode(root/'.git/packed-refs'),'local_branch':branch,'local_branch_OID':oid,'all_nonlocal_refs_and_FETCH_HEAD_bound_by_separate_fences':True}
    def tree_map(raw):
        rows = raw.split(b'\0'); need(rows.pop()==b'','complete NUL tree map'); result = {}
        for row in rows:
            header,name = row.split(b'\t',1); name = name.decode(); need(name not in result,'unique tree path'); result[name] = header.decode()
        return result
    def review(final_pin,manifest_pin,adoption_path,resolution):
        final = parsed(bound(final_pin)); bound(manifest_pin)
        need(resolution['classification']=='ALL_ACTUAL_FINDINGS_RESOLVED_FOR_EXACT_ARTIFACT' and resolution['all_actual_criteria_accepted'] is True and resolution['root_personally_read_complete_artifact_and_audit'] is True,'actual root resolution')
        need(resolution['audit_FINAL']==final_pin and resolution['audit_manifest']==manifest_pin,'same audit controls')
        return {'audit_FINAL':final_pin,'audit_manifest':manifest_pin,'audit_snapshot':snapshot(Path(final_pin['path']).parent),'actual_schema_present':'schema' in final,'actual_schema':final.get('schema'),'actual_status_present':'status' in final,'actual_status':final.get('status'),'root_adoption':external(adoption_path),'root_adoption_semantics':parsed(read(adoption_path)),'root_resolution':resolution}

    safe(E); safe(ignore_path)
    need(not E.is_relative_to(M) and not E.is_relative_to(W) and E.is_dir() and mode(E)=='0700' and not any(E.iterdir()),'empty canonical private0700 TEMP outside Math/W')
    need(not os.path.lexists(OUT),'preflight authority must be absent; no overwrite/retry')
    try:
        p = parsed(read(N/'PLAN.json')); RUN = Path(p['runtime_root'])
        need(sha(read(N/'PLAN.json'))=='f01b666bfd446e7ea10c1a8694bacd2d2046af1800c77ead0ecb25b620492137','exact V3 PLAN')
        need(sha(read(A))==ADOPT_SHA and mode(A)=='0644','exact actual V3 root adoption')
        adopted = parsed(read(A)); need(adopted['status']=='ACCEPTED_V3_STATIC_SOURCE_ONLY' and adopted['authenticated_files']==24,'actual source-only adoption')
        need(external(N/'release_overlay.py')==adopted['helper'] and external(N/'PLAN.json')==adopted['PLAN'],'actual adopted helper/PLAN')
        need(not os.path.lexists(RUN),'designated runtime stays absent throughout assembly')
        need(sha(read(ignore_path))==IGNORE_SHA and mode(ignore_path)=='0644','actual root-pinned ignore prerequisite')
        prerequisite = parsed(read(ignore_path))
        need(prerequisite['status']=='EXACT_RUNTIME_IGNORE_APPLIED_AND_EFFECTIVE_RUN_ABSENT' and prerequisite['root_applied_exact_line'] is True and prerequisite['root_verified_effective_ignore'] is True and prerequisite['runtime_root']==str(RUN) and prerequisite['runtime_absent'] is True,'actual completed root ignore prerequisite')
        ignore = external(P/'.gitignore'); lines = read(P/'.gitignore').decode().splitlines()
        need(ignore==prerequisite['P_ignore'],'exact root-pinned current Pignore')
        meaningful = [x for x in lines if x.strip() and not x.lstrip().startswith('#')]
        need(meaningful[-1]==p['runtime_ignore_line'],'exact final anchored ignore line')
        bindings = {'helper':adopted['helper'],'PLAN':adopted['PLAN'],'controls':p['controls'],'scope_paths':p['scope_paths'],'record_ids':p['record_ids'],'runtime_root':str(RUN),'website_parent':p['website_HEAD'],'website_index':p['website_index'],'overlay_is_not_a_full_public_mirror':True}
        overlay_path = Path(p['controls']['overlay_root_adoption']['path']); overlay = parsed(bound(p['controls']['overlay_root_adoption']))
        need(overlay['status']=='ACCEPTED_PRIVATE_OVERLAY_ONLY' and overlay['future_action_authority'] is False,'accepted overlay only')
        overlay_resolution = {'classification':'ALL_ACTUAL_FINDINGS_RESOLVED_FOR_EXACT_ARTIFACT','all_actual_criteria_accepted':True,'root_personally_read_complete_artifact_and_audit':overlay['root_all539producer_source_lines_all3actual_articles_TARGETS_spans_and_new_aggregate_units_personally_read'] and overlay['full_corrected_REPORT_FINAL_RESULTS_SCHEMA_DISPOSITION_and_adversarial_review_personally_read'],'rationale':'Existing root adoption accepts the complete corrected independent overlay audit and preserves the original failed audit.','actual_criteria_summary':'Private15path13A2M overlay, complete page/aggregate preservation and source/native guards; no action authority.','audit_FINAL':p['controls']['overlay_audit_FINAL'],'audit_manifest':p['controls']['overlay_audit_manifest'],**{key:p['controls'][control] for key,control in [('overlay_FINAL','stage_FINAL'),('overlay_manifest','stage_manifest'),('overlay_seal','stage_seal'),('overlay_builder','stage_builder')]}}
        helper_review = review(adopted['root_resolution']['audit_FINAL'],adopted['root_resolution']['audit_manifest'],A,adopted['root_resolution'])
        stage_review = review(p['controls']['overlay_audit_FINAL'],p['controls']['overlay_audit_manifest'],overlay_path,overlay_resolution)
        need(adopted['root_resolution']['helper']==bindings['helper'] and adopted['root_resolution']['PLAN']==bindings['PLAN'],'root exact source resolution')
        packets = {}
        for packet in overlay['packets']:
            packets[str(P/packet['path'])] = adopted_packet(packet)
        for key in ('source_packet','audit_packet'):
            adopted_packet(adopted[key])
        native_guards = [native(M,'refs/heads/main','a4ce3c37dad209339e490d18dcced6c48cf912d2'),native(W,'refs/heads/master',p['website_HEAD'])]
        need(native_guards[0]['index']==M_INDEX and native_guards[1]['index']=={k:p['website_index'][k] for k in ('bytes','SHA256','mode')},'unchanged complete native indices')
        Mrefs,Wrefs = snapshot(M/'.git/refs'),snapshot(W/'.git/refs')
        Maux = {key:optional(M/'.git'/leaf) for key,leaf in [('packed_refs','packed-refs'),('FETCH_HEAD','FETCH_HEAD'),('ORIG_HEAD','ORIG_HEAD')]}
        Waux = {key:optional(W/'.git'/key) for key in ('packed-refs','FETCH_HEAD','ORIG_HEAD')}
        initial = {'native':native_guards,'Mrefs':Mrefs,'Wrefs':Wrefs,'Maux':Maux,'Waux':Waux}
        new(E/'STARTED.json',packed({'assembler':external(Path(__file__).absolute()),'inputs':{'adoption':external(A),'ignore_receipt':external(ignore_path)},'designated_RUN_absent':True}))
        routing(M,p['Math_origin'],p['routing_config_key_regex']); routing(W,p['origin'],p['routing_config_key_regex'])
        ignored = git(M,'check-ignore','--no-index','-v','--',str(RUN)+'/').decode().rstrip('\n')
        source_line,ignored_path = ignored.split('\t'); source,number,pattern = source_line.rsplit(':',2)
        need(source==str((P/'.gitignore').relative_to(M)) and number.isdecimal() and pattern==p['runtime_ignore_line'] and ignored_path==str(RUN)+'/','actual effective exact ignore while RUN absent')
        need(git(M,'ls-remote','--exit-code','origin','refs/heads/main')==(REMOTE+'\trefs/heads/main\n').encode(),'fresh current Math remote')
        need(git(W,'ls-remote','--exit-code','origin',p['branch'])==(p['website_HEAD']+'\t'+p['branch']+'\n').encode(),'fresh current W remote')
        root_map = tree_map(git(M,'ls-tree','-z','--full-tree',REMOTE)); base_map = tree_map(git(M,'ls-tree','-z','--full-tree',p['Math_remote_checkpoint_base']))
        git(M,'merge-base','--is-ancestor',p['Math_remote_checkpoint_base'],REMOTE)
        need({k:v for k,v in root_map.items() if k!=P.name}=={k:v for k,v in base_map.items() if k!=P.name},'all non-P Math root entries preserved')
        siblings = {k:v for k,v in root_map.items() if k!=P.name and v.startswith('040000 tree ')}; need(len(siblings)==159,'exact159 directory siblings')
        docs = git(M,'ls-tree','-r','-z','--full-tree',REMOTE,'--','docs')
        Math_proof = {'origin':p['Math_origin'],'branch':'refs/heads/main','commit':REMOTE,'all_loose_refs':Mrefs,**Maux,'root_entries':root_map,'protected_159_directory_siblings':siblings,'docs_tree':root_map['docs'].split()[2],'docs_recursive_SHA256':sha(docs)}
        website_tree = git(W,'rev-parse',p['website_HEAD']+'^{tree}').strip().decode(); need(re.fullmatch('[0-9a-f]{40}',website_tree),'actual W parent tree')
        baseline = parsed(bound(p['controls']['website_before']))['public']; current = snapshot(W/'public')
        expected_files = sorted([{'path':r['path'],'bytes':r['bytes'],'SHA256':r['SHA256'],'mode':format(int(r['mode'],8),'04o')} for r in baseline['entries'] if r['kind']=='file'],key=lambda r:r['path'])
        expected_dirs = sorted([{'path':r['path'],'mode':format(int(r['mode'],8),'04o')} for r in baseline['entries'] if r['kind']=='directory' and r['path']!='.'],key=lambda r:r['path'])
        need(current['files']==expected_files and current['directories']==expected_dirs and current['root_mode']=='0750' and (current['regular_files'],current['child_directories'])==(803,387),'whole baseline public hashes/modes/topology; no public copy')
        for row in p['configuration_guards']: bound(row)
        need([native(M,'refs/heads/main','a4ce3c37dad209339e490d18dcced6c48cf912d2'),native(W,'refs/heads/master',p['website_HEAD'])]==native_guards and snapshot(M/'.git/refs')==Mrefs and snapshot(W/'.git/refs')==Wrefs,'native/ref snapshots stable through all reads')
        need({key:optional(M/'.git'/leaf) for key,leaf in [('packed_refs','packed-refs'),('FETCH_HEAD','FETCH_HEAD'),('ORIG_HEAD','ORIG_HEAD')]}==Maux and {key:optional(W/'.git'/key) for key in Waux}==Waux,'whole auxiliary native refs stable')
        need(external(A)==helper_review['root_adoption'] and external(P/'.gitignore')==ignore and sha(read(ignore_path))==IGNORE_SHA and not os.path.lexists(RUN),'same adoption/ignore prerequisite; runtime still absent')
        now = datetime.datetime.now(datetime.timezone.utc)
        authority = {'schema':p['authority_schema'],'mode':'preflight','bindings':bindings,'concurrency':p['concurrency'],'root_asserts_no_other_M_or_W_writer':True,'root_asserts_nonce_fresh':True,'network_read_authorized':True,'filesystem_stage_authorized':False,'commit_and_push_authorized':False,'hosting_deploy_authorized':False,'Sheet_authorized':False,'AA':None,'follow_up':None,'issued_UTC':now.isoformat(),'expires_UTC':(now+datetime.timedelta(seconds=3600)).isoformat(),'nonce':secrets.token_hex(32),'website_tree':website_tree,'Math_native_main':native_guards[0]['local_branch_OID'],'helper_review':helper_review,'stage_review':stage_review,'native_guards':native_guards,'Math_remote_proof':Math_proof,'W_all_loose_refs':Wrefs,'W_aux_controls':Waux,'adopted_overlay_packets':packets,'runtime_ignore_prerequisite':{'root_record':external(ignore_path),'actual_semantics':parsed(read(ignore_path)),'root_applied_exact_line':True,'root_verified_effective_ignore':True,'P_ignore':ignore}}
        raw = packed(authority)
        new(E/'PREPARED.json',packed({'authority_path':str(OUT),'authority':{'bytes':len(raw),'SHA256':sha(raw),'mode':'0644'},'snapshots':initial,'public_snapshot_SHA256':sha(packed(current)),'opaque_commands':seq,'release_helper_invocations':0,'future_stage_commit_deploy_authority':False}))
        new(OUT,raw,0o644)
        print(json.dumps({'status':'PREFLIGHT_AUTHORITY_PREPARED_ONLY','path':str(OUT),'bytes':len(raw),'SHA256':sha(raw),'private_evidence':str(E),'release_helper_invocations':0}))
    except BaseException:
        try: new(E/'FAILURE.txt',traceback.format_exc().encode())
        except BaseException: pass
        print(json.dumps({'status':'STOPPED_NO_RETRY','private_evidence':str(E)}),file=sys.stderr)
        raise SystemExit(1)

if __name__ == '__main__':
    main()
