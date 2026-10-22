"""New standard-library decoder/reconstruction; never imports supplied readers."""
from pathlib import Path
import argparse, datetime, gzip, hashlib, json, lzma, math, os, re, stat, tempfile

OWN=Path(__file__).resolve().parent
def need(v,m):
    if not v:raise RuntimeError(m)
def H(b):return hashlib.sha256(b).hexdigest()
def parse(b):
    def pairs(xs):
        d={}
        for k,v in xs:need(k not in d,'Duplicate key');d[k]=v
        return d
    return json.loads(b,object_pairs_hook=pairs)
def equal(a,b):
    if type(a)is not type(b):return False
    if type(a)is dict:return set(a)==set(b)and all(equal(a[k],b[k])for k in a)
    if type(a)is list:return len(a)==len(b)and all(equal(x,y)for x,y in zip(a,b))
    if type(a)is float:return math.isfinite(a)and math.isfinite(b)and a==b
    return a==b
def unloss(v):
    need(type(v)is list and v,'Bad numeric spy tag');kind=v[0]
    if kind=='str':
        need(len(v)==2 and type(v[1])is list and all(type(x)is int and 0<=x<=0x10ffff for x in v[1]),'Bad codepoint spy');return ''.join(chr(x)for x in v[1])
    if kind=='dict':
        result={}
        for key,value in v[1]:
            key=unloss(key);need(type(key)is str and key not in result,'Duplicate restored spy key');result[key]=unloss(value)
        return result
    if kind=='list':return [unloss(x)for x in v[1]]
    if kind=='bool':need(type(v[1])is bool,'Spy bool type');return v[1]
    if kind=='int':return int(v[1])
    if kind=='float':return float.fromhex(v[1])
    need(v==['null'],'Unrecognized spy tag');return None
def allocated():
    seen=set();total=0
    for p in [OWN,*OWN.rglob('*')]:
        st=p.lstat();key=st.st_dev,st.st_ino
        if key not in seen:seen.add(key);total+=st.st_blocks*512
    return total
def safe(root,name):
    p=Path(name)
    need(type(name)is str and name and not p.is_absolute()and'..'not in p.parts and p.as_posix()==name,'Unsafe member')
    return root/p
def check(root):
    root=Path(root).resolve();store=root/'private/chunks17_segments';chunks={};expected=set();segments=0
    raw_total=0
    for index in sorted(store.glob('*.index.json.gz')):
        need(not index.is_symlink(),'Index symlink');v=parse(gzip.decompress(index.read_bytes()))
        name=v['data_file'];need(Path(name).name==name and name.endswith('.xz'),'Bad data name')
        f=store/name;need(f.is_file()and not f.is_symlink(),'Data not regular');expected.update({index,f})
        packed=f.read_bytes();need({'bytes':len(packed),'sha256':H(packed)}==v['compressed_pin'],'Compressed segment changed')
        raw=lzma.decompress(packed,memlimit=256*1024*1024)
        need(len(raw)==v['raw_bytes']and H(raw)==v['raw_sha256']and len(raw)<=128*1024*1024,'Raw segment changed')
        pos=0
        for key,p in v['chunks'].items():
            need(re.fullmatch('[a-f0-9]{64}',key)and key not in chunks,'Chunk collision or duplicate')
            need(type(p['offset'])is int and p['offset']==pos and type(p['bytes'])is int and 0<p['bytes']<=16384,'Noncontiguous chunk')
            b=raw[pos:pos+p['bytes']];need(len(b)==p['bytes']and H(b)==key,'Chunk body mismatch')
            chunks[key]=b;pos+=p['bytes']
        need(pos==len(raw),'Unindexed raw bytes');segments+=1;raw_total+=len(raw)
    need(set(store.iterdir())==expected,'Whole segment namespace differs')
    used=set();virtual=set();out={'root':str(root),'segments':segments,'chunks':len(chunks),'segment_raw_bytes':raw_total,'cases':0,'physical_files':0,'physical_bytes':0,'directories':0,'virtual_paths':0,'semantic_original_checks':[],'partial_VFS_cases':[],'max_own_allocated_bytes':0,'minimum_free_bytes':None,'all_bytes_modes_nsmtime_namespace':True,'supplied_reader_or_verifier_imported':False,'original_case_ZIP_or_inode_topology_claim':False,'actual_effects':0}
    def sample(bound=0):
        a=allocated();free=os.statvfs(OWN).f_bavail*os.statvfs(OWN).f_frsize
        out['max_own_allocated_bytes']=max(out['max_own_allocated_bytes'],a)
        out['minimum_free_bytes']=free if out['minimum_free_bytes']is None else min(out['minimum_free_bytes'],free)
        need(a+bound<8*1024*1024,'Own cold8MiB cap');need(free>=150*1024*1024+bound,'Cold free150MiB reserve')
    def body(pin):
        need(type(pin['chunks'])is list and all(k in chunks for k in pin['chunks']),'Missing chunk')
        used.update(pin['chunks']);b=b''.join(chunks[k]for k in pin['chunks']);need(len(b)==pin['bytes'],'Length mismatch');return b
    sample()
    with tempfile.TemporaryDirectory(prefix='independent_cold_',dir=OWN/'private')as tmp:
        for recipe in sorted((root/'private/case_archives_phase17').glob('*.case.json.gz')):
            need(not recipe.is_symlink(),'Recipe symlink');v=parse(gzip.decompress(recipe.read_bytes()))
            files=v['files'];dirs=v['directories'];need('.'in dirs and not(set(files)&set(dirs)),'Bad case namespace')
            need(v['direct_custody_no_original_ZIP_created']is True,'Wrong custody mechanism')
            if not v.get('historical_virtual_scope_complete',True):out['partial_VFS_cases'].append(v['case'])
            bound=sum(((p['bytes']+4095)//4096)*4096+4096 for p in files.values())+8192*len(dirs)+65536;sample(bound)
            base=Path(tmp)/'world';base.mkdir()
            for name in sorted(set(dirs)-{'.'},key=lambda n:n.count('/')):safe(base,name).mkdir()
            for name,p in files.items():
                b=body(p);need(H(b)==p['sha256'],'Full file hash');q=safe(base,name);q.write_bytes(b);q.chmod(p['mode']);os.utime(q,ns=(p['mtime_ns'],p['mtime_ns']))
                out['physical_files']+=1;out['physical_bytes']+=len(b)
            for name,p in sorted(dirs.items(),key=lambda kv:kv[0].count('/'),reverse=True):
                q=base if name=='.'else safe(base,name);q.chmod(p['mode']);os.utime(q,ns=(p['mtime_ns'],p['mtime_ns']))
            sample();need({p.relative_to(base).as_posix()for p in base.rglob('*')}==set(files)|(set(dirs)-{'.'}),'Restored namespace')
            for name,p in files.items():
                q=base/name;s=q.lstat();need(stat.S_ISREG(s.st_mode)and stat.S_IMODE(s.st_mode)==p['mode']and s.st_mtime_ns==p['mtime_ns']and H(q.read_bytes())==p['sha256'],'Restored exact file')
            for name,p in dirs.items():
                q=base if name=='.'else base/name;s=q.lstat();need(stat.S_ISDIR(s.st_mode)and stat.S_IMODE(s.st_mode)==p['mode']and s.st_mtime_ns==p['mtime_ns'],'Restored exact directory')
            if 'ADVERSARY_ONLY_RETURNED_BODY_SPY.json'in files:
                spy=parse((base/'ADVERSARY_ONLY_RETURNED_BODY_SPY.json').read_bytes());label=v['case'];old=label.startswith('held16_unicode_')
                m=re.search(r'(?:valid_)?original_(create|upload|update|publish)_before_',label)
                kind=m.group(1)if m else label.rsplit('_',1)[-1];need(kind in {'get','create','upload','update','publish'},'Unknown semantic case '+label)
                holds=[parse((base/n).read_bytes())for n in files if n.startswith(('runtime/CONSUMED_RESPONSE17_HOLD_','runtime/CONSUMED_RESPONSE16_HOLD_'))]
                decisive={h['original_response']['path']for h in holds if h.get('original_response')and h['original_response']['kind']==kind}
                found=[]
                for name in files:
                    if not(name.startswith('private/service_original_')and name.endswith('.json')):continue
                    value=parse((base/name).read_bytes());absolute=str(root/'private'/v['cohort']/v['case']/name)
                    if value['kind']==kind and equal(value['response'],spy)and(old or (absolute in decisive if kind=='get'else any(absolute==r['path']and kind==r['kind']for h in holds for r in h['all_consumed_response_custody']))):found.append((name,value,absolute))
                need(len(found)==(0 if old else 1),'METHOD-specific complete original mismatch '+label)
                detail={'case':label,'kind':kind,'complete_original_matches':len(found),'old16_expected_missing':old}
                if not old:
                    name,value,absolute=found[0];actual=(base/name).read_bytes();pin={'bytes':len(actual),'sha256':H(actual)}
                    refs=[r for h in holds for r in h['all_consumed_response_custody']if r['path']==absolute and r['kind']==kind]
                    need(refs and all(r['durable_write_returned']is True for r in refs),'Missing durable HOLD reference')
                    need(all(type(r['expected_integrity_verified'])is bool and(r['pin']==pin)==r['expected_integrity_verified']for r in refs),'False integrity status')
                    if kind!='get':
                        f=value['known_service_fact'];need(f['kind']==kind and type(f['requested_or_known_id'])is int and f['requested_or_known_id']==777,'Missing combined known fact')
                        need(f['sources_sha256']=='623a85eca963527260367dd192bb0373f6a81972179633fa6f219c72a6237803','Wrong source fact')
                        need(f['manifest']==str(root.parent/'operations/proposed/preprint/zenodo-deposit.json'),'Changed original manifest')
                    if label.startswith(('sdk_unicode_','adversarial_sdk_')):
                        need(actual==(json.dumps(value,ensure_ascii=True,sort_keys=True,indent=2)+'\n').encode('ascii'),'Unicode physical first representation changed')
                        need(all(r['expected_integrity_verified']is True for r in refs),'Unicode expected pin not verified')
                    detail.update(physical_pin=pin,combined_fact=kind!='get',current_HOLD_reference=True)
                out['semantic_original_checks'].append(detail)
            numeric='ADVERSARY_PARSED_ORIGINAL_LOSSLESS_CODEPOINTS.json'
            if numeric in files:
                exact=unloss(parse((base/numeric).read_bytes()));wire=(base/'SDK_RESPONSE_LITERAL_SURROGATE_UTF8.bin').read_bytes()
                need(equal(exact,json.loads(wire)),'Full numeric spy disagrees with actual SDK-input parser object')
                kind=v['case'].rsplit('_',1)[-1];need(kind in {'create','publish'},'Unknown paired-codepoint METHOD')
                receipts=[]
                for name in files:
                    if name.startswith('private/service_original_')and name.endswith('.json'):
                        value=json.loads((base/name).read_bytes())
                        if value['kind']==kind:receipts.append((name,value))
                need(len(receipts)==1,'Contested METHOD receipt count');name,value=receipts[0];replayed=value['response']
                need(not equal(exact,replayed),'Expected original-content counterexample not reproduced')
                holds=[parse((base/n).read_bytes())for n in files if n.startswith('runtime/CONSUMED_RESPONSE17_HOLD_')]
                absolute=str(root/'private'/v['cohort']/v['case']/name);refs=[r for h in holds for r in h['all_consumed_response_custody']if r['path']==absolute and r['kind']==kind]
                raw=(base/name).read_bytes();actual_pin={'bytes':len(raw),'sha256':H(raw)}
                need(refs and all(r['durable_write_returned']is True and r['expected_integrity_verified']is True and r['pin']==actual_pin for r in refs),'Byte-passing contrary receipt not bound')
                need(all(h['known_id']==777 for h in holds)and value['known_service_fact']['requested_or_known_id']==777,'Known identity missing')
                detail={'case':v['case'],'kind':kind,'status':'CONFIRMED_EXPECTED_CUSTODY_COUNTEREXAMPLE','complete_typed_actual_original_preserved_in_actor_receipt':False,'full_numeric_independent_spy_equals_rawSDK_input_parse':True,'physical_actor_expected_byte_pin_passed':True,'original_readonly_VFS_complete':v.get('historical_virtual_scope_complete',True),'rawSDK_sha256':H(wire)}
                if 'title_pair_coalescence'in v['case']:
                    need([ord(x)for x in exact['title']][-2:]==[0xd83d,0xde00]and[ord(x)for x in replayed['title']][-1:]==[0x1f600],'Wrong codepoint collapse')
                    need(json.dumps(exact,ensure_ascii=True,sort_keys=True)==json.dumps(replayed,ensure_ascii=True,sort_keys=True),'Noninjective ASCII serialization not confirmed')
                    detail['difference']={'actual_title_codepoints':[ord(x)for x in exact['title']],'receipt_title_codepoints':[ord(x)for x in replayed['title']]}
                else:
                    need('distinct_key_collision'in v['case']and len(replayed)==len(exact)-1,'Wrong key collision')
                    try:parse(raw)
                    except RuntimeError as err:need(str(err)=='Duplicate key','Unexpected strict parse error')
                    else:raise RuntimeError('Collided receipt strict-parseable')
                    detail['difference']={'actual_distinct_keys':[[ord(x)for x in k]for k in exact if k.startswith('literal_pair_')],'receipt_keys':[[ord(x)for x in k]for k in replayed if k.startswith('literal_pair_')],'duplicate_JSON_key_confirmed':True}
                out['semantic_original_checks'].append(detail)
            component='COMPONENT_ONLY_PARSED_RESPONSE_ASCII.json'
            if component in files:
                parsed=parse((base/component).read_bytes());found=[]
                for name in files:
                    if name.startswith('private/service_original_')and name.endswith('.json'):
                        value=parse((base/name).read_bytes())
                        if value['kind']=='create'and equal(value['response'],parsed):found.append((name,value))
                need(len(found)==1,'Missing complete component return');name,value=found[0]
                need((base/name).read_bytes()==(json.dumps(value,sort_keys=True,ensure_ascii=True,indent=2)+'\n').encode('ascii'),'Component ASCII representation')
                need(len(parsed['strings'])==2056 and parsed['strings'][:2048]==[chr(x)for x in range(0xd800,0xe000)],'Component domain')
                out['semantic_original_checks'].append({'case':v['case'],'kind':'component','complete_original_matches':1,'all2048_surrogate_units_plus8_controls':True})
            for digest,p in v['virtual_bodies'].items():need(H(body(p))==digest,'VFS complete body hash');virtual.add(digest)
            need(set(v['virtual_paths'].values())==set(v['virtual_bodies']),'VFS lookup closure')
            for name in v['virtual_paths']:need(name.startswith(str(root/'private'/v['cohort']/v['case'])+'/'),'VFS path outside original case')
            out['virtual_paths']+=len(v['virtual_paths']);out['cases']+=1;out['directories']+=len(dirs)
            for name in sorted(dirs,key=lambda n:n.count('/'),reverse=True):(base if name=='.'else base/name).chmod(0o700)
            for name in files:(base/name).unlink()
            for name in sorted(set(dirs)-{'.'},key=lambda n:n.count('/'),reverse=True):(base/name).rmdir()
            base.rmdir();sample()
    need(used==set(chunks),'Unused or absent chunks');out['virtual_distinct_bodies']=len(virtual);out['at']=datetime.datetime.now(datetime.timezone.utc).isoformat();out['decoder_sha256']=H(Path(__file__).read_bytes());return out
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('root');p.add_argument('--output',required=True);a=p.parse_args();v=check(a.root)
    with Path(a.output).open('x')as f:f.write(json.dumps(v,ensure_ascii=True,indent=2)+'\n')
    print(json.dumps({k:v for k,v in v.items()if k!='semantic_original_checks'},sort_keys=True))
