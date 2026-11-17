#!/usr/bin/env python3
"""One independent read-only raw-index/TREE/commit remainder audit."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, re, stat, struct, subprocess, sys, traceback

P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024');M=P.parent
W=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
A=P/'verification/radial-tree-TREE-commit-remainder-sol-20261117'
S=P/'verification/radial-tree-stage-sol-20261117';PREP=P/'verification/radial-tree-production-preparation-sol-20261117'
R=P/'verification/radial-tree-runtime-sol-20261117/publish/f03e6c345529683595dba38fe6ded458852fcbc506e74d082f8441f4b7922be0'
PACKETS=[P/'verification'/n for n in ['radial-tree-post-publication-audit-sol-20261117','radial-tree-metadata-diagnosis-sol-20261117','radial-tree-native-semantics-sol-20261117']]
COMMIT='7d5ac8ea5dc8d6cddee457da7a5b40042d36d344';PARENT='96f04aa5544df69daba07a9ed4d6212172e9984a'
ROOT='c59d0d0a542f20bceb3556b1e936e86b22626434';OLDROOT='7260c2f004d311ab06dd8556de6e17a2196d1d28'
ZERO_STAT=(0,0,0,0,0,0,0o100644,0,0,0)
checks=[];active='startup';before=None;failure=None;batch_count=0;summary={}
def now():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def save(name,x):(A/name).write_text(json.dumps(x,indent=2,ensure_ascii=True)+'\n')
def need(ok,label,detail=None):
    global active
    active=label
    if not ok:raise AssertionError(json.dumps({'criterion':label,'detail':detail},ensure_ascii=True))
    checks.append({'criterion':label,'pass':True,'detail':detail})
def meta(p):
    s=p.lstat()
    if not stat.S_ISREG(s.st_mode):raise ValueError('Not regular '+str(p))
    b=p.read_bytes();return {'bytes':len(b),'SHA256':sha(b),'mode':oct(stat.S_IMODE(s.st_mode))}
def snapshot(root):
    s=root.lstat();f={};d={};o={}
    if not stat.S_ISDIR(s.st_mode):raise ValueError('Not directory '+str(root))
    for p in sorted(root.rglob('*')):
        q=p.lstat();n=str(p.relative_to(root))
        if stat.S_ISREG(q.st_mode):f[n]=meta(p)
        elif stat.S_ISDIR(q.st_mode):d[n]=oct(stat.S_IMODE(q.st_mode))
        else:o[n]={'mode':oct(stat.S_IMODE(q.st_mode)),'target':os.readlink(p) if p.is_symlink() else None}
    return {'root':str(root),'root_mode':oct(stat.S_IMODE(s.st_mode)),'files':f,'directories':d,'other':o}
def native(repo):
    gd=repo/'.git';p=gd/'packed-refs';lines=[x for x in p.read_text().splitlines() if re.match(r'^[0-9a-f]{40} refs/heads/',x)]
    head=(gd/'HEAD').read_text().strip();ref=head.removeprefix('ref: ');loose=gd/ref
    resolved=loose.read_text().strip() if loose.is_file() else next(x.split()[0] for x in lines if x.split()[1]==ref)
    return {'files':{n:meta(gd/n) for n in ['HEAD','index','config']},'HEAD':head,'resolved_local_HEAD':resolved,
            'local_heads':snapshot(gd/'refs/heads'),'packed_local_head_lines':lines,'packed_refs_mode':oct(stat.S_IMODE(p.stat().st_mode))}
def guard():
    return {'UTC':now(),'M_native':native(M),'W_native':native(W),'actual_public':snapshot(W/'public'),
            'candidate':snapshot(S/'candidate/public'),'stage':snapshot(S),'preparation':snapshot(PREP),'runtime_publish':snapshot(R),
            'frozen_predecessors':{str(p):snapshot(p) for p in PACKETS},
            'exclusions':['remote-tracking refs','FETCH_HEAD','nonlocal packed-ref lines','Firebase metadata outside public']}
def comparable(x):return {k:v for k,v in x.items() if k!='root'}

def git_read(label,args,input_bytes=None):
    env={k:v for k,v in os.environ.items() if not k.startswith('GIT_')};env.update(GIT_OPTIONAL_LOCKS='0',GIT_NO_REPLACE_OBJECTS='1')
    argv=['/usr/bin/git','--no-optional-locks','-C',str(W),*args]
    r=subprocess.run(argv,input=input_bytes,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env)
    (A/(label+'.stdout.bin')).write_bytes(r.stdout);(A/(label+'.stderr.bin')).write_bytes(r.stderr)
    if input_bytes is not None:(A/(label+'.stdin.bin')).write_bytes(input_bytes)
    save(label+'.receipt.json',{'argv':argv,'exit':r.returncode,'stdout_bytes':len(r.stdout),'stdout_SHA256':sha(r.stdout),'stderr_bytes':len(r.stderr),'stderr_SHA256':sha(r.stderr)})
    if r.returncode:raise RuntimeError('Readonly Git failure '+label+': '+r.stderr.decode(errors='replace'))
    return r.stdout

def index(path,label):
    b=path.read_bytes();need(b[:4]==b'DIRC' and len(b)>32,label+'_header')
    version,count=struct.unpack('>II',b[4:12]);need(version==2,label+'_v2')
    need(hashlib.sha1(b[:-20]).digest()==b[-20:],label+'_trailing_SHA1')
    entries={};names=[];pos=12
    for number in range(count):
        start=pos;fields=struct.unpack('>10I',b[pos:pos+40]);oid=b[pos+40:pos+60];flags=struct.unpack('>H',b[pos+60:pos+62])[0];pos+=62;extended=b''
        if flags&0x4000:extended=b[pos:pos+2];pos+=2
        end=b.index(b'\0',pos);name=b[pos:end];pos=start+((end+1-start+7)//8)*8
        if not name or name in entries or any(b[end+1:pos]) or (flags&0xfff)!=min(len(name),0xfff) or (flags>>12)&3:raise AssertionError(label+' malformed/staged record '+str(number))
        entries[name]={'stat':fields,'oid':oid,'flags':flags,'extended':extended,'raw':b[start:pos],'padding':b[end+1:pos]};names.append(name)
    need(names==sorted(names),label+'_raw_name_order')
    exts=[]
    while pos<len(b)-20:
        signature=b[pos:pos+4];length=struct.unpack('>I',b[pos+4:pos+8])[0];raw=b[pos:pos+8+length]
        if len(raw)!=length+8:raise AssertionError('Truncated extension')
        exts.append((signature,raw,raw[8:]));pos+=length+8
    need(pos==len(b)-20 and [e[0] for e in exts]==[b'TREE'],label+'_only_complete_TREE_extension')
    return b,entries,exts[0]

def build_trees(entries):
    root={}
    for path,e in entries.items():
        parts=path.split(b'/');node=root
        if any(x in (b'',b'.',b'..') for x in parts):raise AssertionError('Unsafe raw path')
        for x in parts[:-1]:
            if x not in node:node[x]={}
            if not isinstance(node[x],dict):raise AssertionError('Tree path collision')
            node=node[x]
        if parts[-1] in node:raise AssertionError('Tree leaf collision')
        node[parts[-1]]=(e['stat'][6],e['oid'])
    trees={}
    def visit(node,path):
        chunks=[];count=0;children=0
        for name,value in sorted(node.items(),key=lambda q:q[0]+(b'/' if isinstance(q[1],dict) else b'\0')):
            if isinstance(value,dict):
                t=visit(value,path+b'/'+name if path else name);mode=b'40000';oid=t['oid'];count+=t['count'];children+=1
            else:
                m,oid=value
                if m not in (0o100644,0o100755,0o120000,0o160000):raise AssertionError('Unexpected raw mode '+oct(m))
                mode=format(m,'o').encode();count+=1
            chunks.append(mode+b' '+name+b'\0'+oid)
        raw=b''.join(chunks);oid=hashlib.sha1(b'tree '+str(len(raw)).encode()+b'\0'+raw).digest()
        row={'oid':oid,'raw':raw,'count':count,'children':children};trees[path]=row;return row
    visit(root,b'');return trees

def parse_cache(payload):
    pos=0;nodes=[]
    def visit(parent,top=False):
        nonlocal pos
        start=pos;end=payload.index(b'\0',pos);component=payload[pos:end];pos=end+1
        end=payload.index(b'\n',pos);count,children=map(int,payload[pos:end].split(b' '));pos=end+1
        if (top and component) or (not top and (not component or b'/' in component)) or children<0 or count< -1:raise AssertionError('Invalid cache header')
        path=b'' if top else parent+b'/'+component if parent else component;oid=None
        if count>=0:oid=payload[pos:pos+20];pos+=20
        row={'path':path,'count':count,'children':children,'oid':oid,'header_raw':payload[start:pos]};nodes.append(row)
        for _ in range(children):visit(path)
    visit(b'',True);need(pos==len(payload),'all_TREE_payload_consumed')
    need(len({n['path'] for n in nodes})==len(nodes),'all_TREE_paths_unique')
    return nodes

def object_batch(label,expected):
    global batch_count
    batch_count+=1;need(batch_count<=2,'at_most_two_bounded_cat_file_batches')
    ids=sorted(expected);request=b''.join(i.hex().encode()+b'\n' for i in ids)
    data=git_read(label,['cat-file','--batch'],request);pos=0;result={}
    for oid in ids:
        end=data.index(b'\n',pos);header=data[pos:end].split();pos=end+1
        if len(header)!=3 or header[0].decode()!=oid.hex() or header[1].decode()!=expected[oid]:raise AssertionError('Missing/wrong object '+oid.hex())
        size=int(header[2]);raw=data[pos:pos+size];pos+=size
        if len(raw)!=size or data[pos:pos+1]!=b'\n':raise AssertionError('Batch object framing')
        pos+=1
        if hashlib.sha1(header[1]+b' '+str(size).encode()+b'\0'+raw).digest()!=oid:raise AssertionError('Object SHA1 mismatch '+oid.hex())
        result[oid]=raw
    need(pos==len(data),label+'_all_output_consumed');return result

def commit_leaves(commit,label):
    data=git_read(label,['ls-tree','-r','-z','--full-tree',commit]);result={}
    for unit in data.split(b'\0'):
        if not unit:continue
        head,name=unit.split(b'\t',1);mode,kind,oid=head.split()
        if name in result:raise AssertionError('Duplicate object leaf')
        result[name]=(int(mode,8),bytes.fromhex(oid.decode()))
    return result
def identity(raw):
    head,message=raw.split(b'\n\n',1);headers={};parents=[]
    for line in head.splitlines():
        k,v=line.split(b' ',1)
        if k==b'parent':parents.append(v.decode())
        elif k in headers:raise AssertionError('Duplicate commit header')
        else:headers[k]=v.decode()
    return {'headers':{k.decode():v for k,v in headers.items()},'parents':parents,'message':message.decode()}

try:
    targets=json.loads((S/'TARGETS.json').read_text());plan=json.loads((PREP/'PLAN.json').read_text());auth=json.loads((R/'authorization.json').read_text())
    baseline=json.loads((S/'GUARDS_BEFORE_V2.json').read_text())
    before=guard();save('GUARDS_BEFORE.json',before)
    need([len(before['frozen_predecessors'][str(p)]['files']) for p in PACKETS[:2]]==[14,23],'old_14_and_diagnosis_23_namespaces')
    for key in ['target_plan','build_guards_before']:
        c=plan['controls'][key];m=meta(Path(c['path']));need(m['SHA256']==c['SHA256'] and m['bytes']==c['bytes'],'frozen_control_'+key)
    public=before['actual_public'];candidate=before['candidate']
    need(comparable(public)==comparable(candidate),'actual_complete_public_equals_candidate')
    need(len(public['files'])==781 and len(public['directories'])==377 and public['root_mode']=='0o750' and not public['other'],'actual_public_781_377_0750')
    add=set(targets['A']);modify=set(targets['M']);scope=add|modify;rawscope={('public/'+n).encode() for n in scope};rawadd={('public/'+n).encode() for n in add}
    need(len(add)==9 and len(modify)==2 and not targets['D'] and len(scope)==11 and len(targets['new_directories'])==4,'TARGETS_exact_11_9A2M_four_dirs')
    need(set(plan['scope_paths'])=={'public/'+n for n in scope} and all(not n.startswith('public/') for n in scope),'public_prefix_exactly_once')
    need(set(public['directories'])-set(baseline['public']['directories'])==set(targets['new_directories']),'actual_four_added_directories')
    oldbytes,old,oldext=index(R/'native-backups/index.before','actual_backup');newbytes,new,newext=index(W/'.git/index','actual_native');selbytes,selected,selext=index(R/'native-successor.index','actual_selected_successor')
    need(len(oldbytes)==9057886 and sha(oldbytes)=='e6285d49b7249ae2c88a1f624ca98c1dcf480424db272c4fe111ca91dbdafb5e','baseline_exact_file_pin')
    need(len(newbytes)==9059206 and sha(newbytes)=='592a25281b63a357fbe4fe2580e2c9764ba2b4836650d8751ac573ff8117c365','successor_exact_file_pin')
    need(newbytes==selbytes and meta(W/'.git/index')['mode']==meta(R/'native-successor.index')['mode']=='0o644','actual_selected_and_native_exact_bytes_mode')
    need(len(old)==58712 and len(new)==58721 and set(new)==set(old)|rawadd and set(old)&rawscope=={('public/'+n).encode() for n in modify},'exact_raw_record_sets_58712_to_58721')
    protected=sorted(set(old)-rawscope)
    need(len(protected)==58710 and all(old[p]['raw']==new[p]['raw'] for p in protected),'all_58710_whole_raw_records_exact')
    save('PROTECTED_RAW_RECORDS.json',{'records':[{'path_hex':p.hex(),'raw_SHA256':sha(old[p]['raw']),'raw_bytes':len(old[p]['raw']),'stat_fields':old[p]['stat'],'mode':oct(old[p]['stat'][6]),'OID':old[p]['oid'].hex(),'flags':old[p]['flags'],'extended_hex':old[p]['extended'].hex(),'padding_hex':old[p]['padding'].hex()} for p in protected]})
    selected_evidence=[];blob_expected={};payloads={}
    for p in sorted(rawscope):
        entry=new[p];data=(W/os.fsdecode(p)).read_bytes();oid=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).digest()
        base=struct.pack('>10I',*ZERO_STAT)+oid+struct.pack('>H',len(p))+p+b'\0';expected=base+b'\0'*((-len(base))%8)
        need(entry['stat']==ZERO_STAT and entry['flags']==len(p) and not entry['extended'] and entry['oid']==oid and entry['raw']==expected,'selected_explicit_zero_stat_record_'+p.decode())
        selected_evidence.append({'path_hex':p.hex(),'stat_fields':entry['stat'],'flags':entry['flags'],'raw_name_bytes':len(p),'OID':oid.hex(),'padding_hex':entry['padding'].hex(),'raw_record_SHA256':sha(entry['raw']),'payload_bytes':len(data),'payload_SHA256':sha(data)})
        blob_expected[oid]='blob';payloads[p]=(oid,data)
    save('SELECTED_RECORD_SCHEMA.json',{'fresh_lstat_cache_equality_required':False,'template':ZERO_STAT,'records':selected_evidence})
    oldtrees=build_trees(old);newtrees=build_trees(new)
    need(oldtrees[b'']['oid'].hex()==OLDROOT and newtrees[b'']['oid'].hex()==ROOT,'complete_in_memory_tree_hashes')
    need(oldext[1]==newext[1]==selext[1] and len(newext[1])==35878 and sha(newext[1])=='f12d2a0b795034ce5cab45ad6fa5da31b4d7ad6f4b22a5999ce27841b41350b3','TREE_whole_35878_exact_preserved')
    need(len(newext[2])==35870 and sha(newext[2])=='6078bbaef4d39e7b0418bc6ed44ad8f37d2733ec6de4a4e4ba165fe7e665bfcb','TREE_payload_35870_distinct_pin')
    nodes=parse_cache(newext[2]);valid=[n for n in nodes if n['count']>=0];invalid=[n for n in nodes if n['count']==-1]
    invalid_paths=[b'',b'public',b'public/research',b'public/research/binary-relation-liveness',b'public/research/rational-point-undecidability',b'public/research/focal-distance-period-criterion']
    need(len(nodes)==983 and len(valid)==977 and [n['path'] for n in invalid]==invalid_paths and all(n['oid'] is None for n in invalid),'983_TREE_nodes_977_valid_6_preexisting_invalid_without_OID')
    expected={n['oid']:'tree' for n in valid};expected.update({bytes.fromhex(OLDROOT):'tree',bytes.fromhex(ROOT):'tree',bytes.fromhex(PARENT):'commit',bytes.fromhex(COMMIT):'commit'})
    bodies=object_batch('objects_batch_1_trees_commits',expected);cache=[]
    for n in valid:
        oldtree=oldtrees.get(n['path']);newtree=newtrees.get(n['path'])
        if oldtree is None or newtree is None or n['count']!=newtree['count'] or n['children']!=newtree['children'] or n['oid']!=newtree['oid'] or n['oid']!=oldtree['oid'] or bodies[n['oid']]!=newtree['raw']:
            raise AssertionError('Valid TREE path/count/children/OID/object mismatch '+n['path'].hex())
        cache.append({'path_hex':n['path'].hex(),'count':n['count'],'children':n['children'],'OID':n['oid'].hex(),'object_payload_SHA256':sha(bodies[n['oid']])})
    need(len(cache)==977 and bodies[bytes.fromhex(ROOT)]==newtrees[b'']['raw'] and bodies[bytes.fromhex(OLDROOT)]==oldtrees[b'']['raw'],'all_valid_TREE_nodes_and_both_root_objects_exact')
    save('TREE_EVIDENCE.json',{'whole_extension':{'bytes':len(newext[1]),'SHA256':sha(newext[1])},'payload':{'bytes':len(newext[2]),'SHA256':sha(newext[2])},'valid_nodes':cache,'invalid_nodes':[{'path_hex':n['path'].hex(),'count':n['count'],'children':n['children'],'OID':None,'header_raw_hex':n['header_raw'].hex()} for n in invalid]})
    parent_id=identity(bodies[bytes.fromhex(PARENT)]);new_id=identity(bodies[bytes.fromhex(COMMIT)])
    need(parent_id['headers']['tree']==OLDROOT and new_id['headers']['tree']==ROOT and new_id['parents']==[PARENT],'actual_commit_parent_and_root_headers')
    names=[]
    for k in ['author','committer']:
        match=re.fullmatch(r'(.*) <([^>]+)> (\d+) ([+-]\d{4})',new_id['headers'][k]);need(match is not None,'actual_'+k+'_header_structure')
        need(match[1]==auth['author_name'] and match[2]==auth['author_email'],'actual_'+k+'_identity_from_authority')
        names.append({'role':k,'name':match[1],'email':match[2],'timestamp':int(match[3]),'timezone':match[4]})
    need(new_id['message'].strip()==plan['commit_message'],'actual_message_matches_frozen_PLAN')
    need(all(datetime.fromtimestamp(n['timestamp'],timezone.utc)==datetime.fromisoformat(auth['commit_date']) for n in names),'actual_commit_timestamp_matches_authority')
    save('ACTUAL_COMMIT_IDENTITY.json',{'parent':parent_id,'published':new_id,'parsed_identities':names,'authorization_date':auth['commit_date']})
    actualold=commit_leaves(PARENT,'parent_all_leaves');actualnew=commit_leaves(COMMIT,'published_all_leaves')
    rawold={p:(e['stat'][6],e['oid']) for p,e in old.items()};rawnew={p:(e['stat'][6],e['oid']) for p,e in new.items()}
    need(rawold==actualold and rawnew==actualnew,'complete_raw_and_actual_commit_semantic_maps_foreign_staging_0_to_0')
    need(set(actualnew)==set(actualold)|rawadd and all(actualold[p]==actualnew[p] for p in protected),'all_untargeted_commit_leaves_exact')
    save('FULL_SEMANTIC_MAPS.json',{'old_root':OLDROOT,'new_root':ROOT,'old':[{'path_hex':p.hex(),'mode':oct(m),'OID':o.hex()} for p,(m,o) in sorted(rawold.items())],'new':[{'path_hex':p.hex(),'mode':oct(m),'OID':o.hex()} for p,(m,o) in sorted(rawnew.items())],'both_maps_exact_actual_Git_commit_leaves':True,'foreign_staging_before':0,'foreign_staging_after':0})
    delta=git_read('actual_commit_delta',['diff-tree','--no-commit-id','--no-renames','--raw','-r','-z',PARENT,COMMIT]);parts=delta.split(b'\0');rows=[]
    if parts[-1]!=b'' or (len(parts)-1)%2:raise AssertionError('Delta framing')
    for i in range(0,len(parts)-1,2):rows.append({'path':parts[i+1],'fields':parts[i].split()})
    expected_delta={**{p:'A' for p in rawadd},**{('public/'+n).encode():'M' for n in modify}}
    need(len(rows)==11 and {r['path']:r['fields'][-1].decode() for r in rows}==expected_delta,'actual_exact_11_path_9A2M_commit_delta')
    blob_objects=object_batch('objects_batch_2_selected_blobs',blob_expected)
    need(all(blob_objects[oid]==data and actualnew[p]==(0o100644,oid) for p,(oid,data) in payloads.items()),'all_11_actual_payloads_equal_Git_blob_objects')
    save('EXACT_DELTA.json',{'rows':[{'path_hex':r['path'].hex(),'raw_fields':[x.decode() for x in r['fields']]} for r in rows],'new_directories':targets['new_directories']})
    for label,repo in [('M',M),('W',W)]:
        cur=before[label+'_native'];oldc=baseline['native_controls'][label]
        need(cur['HEAD']==oldc['HEAD'] and cur['files']['HEAD']==oldc['files']['HEAD'] and cur['files']['config']==oldc['files']['config'] and cur['packed_local_head_lines']==oldc['packed_local_head_lines'] and cur['packed_refs_mode']==oldc['packed_refs_mode'],'preserved_HEAD_config_local_packed_heads_'+label)
        heads={**oldc['local_heads'],'other':{}}
        if label=='W':heads={**heads,'files':{**heads['files'],'master':{**heads['files']['master'],'SHA256':sha((COMMIT+'\n').encode())}}}
        need(comparable(cur['local_heads'])==comparable(heads),'only_authorized_loose_local_head_delta_'+label)
        if label=='M':need(cur['files']['index']==oldc['files']['index'] and cur['resolved_local_HEAD']==oldc['resolved_local_HEAD'],'Math_native_index_and_main_unchanged')
        else:need(cur['resolved_local_HEAD']==COMMIT,'W_native_master_at_actual_commit')
    summary={'old_records':len(old),'new_records':len(new),'protected_whole_raw_records':len(protected),'selected_zero_stat_records':len(selected_evidence),'old_root':OLDROOT,'new_root':ROOT,'TREE_nodes':len(nodes),'valid_TREE_nodes':len(cache),'invalid_TREE_nodes':len(invalid),'actual_delta_paths':len(rows),'cat_file_batches':batch_count,'foreign_staging_before':0,'foreign_staging_after':0}
except BaseException as ex:
    failure={'UTC':now(),'criterion':active,'exception':repr(ex),'traceback':traceback.format_exc()};save('FIRST_FAILURE.json',failure);sys.stderr.write(failure['traceback'])
finally:
    after=guard();save('GUARDS_AFTER.json',after)
    unchanged=before is not None and {k:v for k,v in before.items() if k!='UTC'}=={k:v for k,v in after.items() if k!='UTC'}
    if not unchanged and failure is None:
        failure={'UTC':now(),'criterion':'complete_protected_guards','exception':'Protected scope changed','traceback':''};save('FIRST_FAILURE.json',failure);sys.stderr.write(failure['exception']+'\n')
    result={'schema':'independent_radial_TREE_commit_remainder_v1','UTC':now(),'status':'FIRST_FAILURE_STOP' if failure else 'PASS_BOUNDED_REMAINDER','checks':checks,'summary':summary,'failure':failure,'protected_guards_unchanged':unchanged,'reader_attempts':1,'cat_file_batches':batch_count,'producer_helper_import_AST_compile_test_mode_executions':0,'network_or_protected_writes':False,'scope_exclusions':['remote-tracking refs','FETCH_HEAD','nonlocal packed-ref lines','Firebase metadata outside public'],'completion_percent':100 if failure is None else None,'no_science_or_live_UI_certificate':True}
    save('DATA_RESULT.json',result);print(json.dumps({'status':result['status'],'checks_passed':len(checks),'guards_unchanged':unchanged,'failure':failure['criterion'] if failure else None,'summary':summary}))
sys.exit(1 if failure else 0)
