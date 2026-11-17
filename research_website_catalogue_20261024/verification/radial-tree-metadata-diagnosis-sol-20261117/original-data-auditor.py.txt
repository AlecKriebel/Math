#!/usr/bin/env python3
"""One finite read-only audit. No project imports, writers, network, or retries."""
from pathlib import Path
import hashlib, json, os, re, stat, struct, subprocess, sys, traceback
from datetime import datetime, timezone
from html.parser import HTMLParser
import xml.etree.ElementTree as ET

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
M = P.parent
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
A = P / 'verification/radial-tree-post-publication-audit-sol-20261117'
S = P / 'verification/radial-tree-stage-sol-20261117'
R = P / 'verification/radial-tree-runtime-sol-20261117/publish/f03e6c345529683595dba38fe6ded458852fcbc506e74d082f8441f4b7922be0'
PREP = P / 'verification/radial-tree-production-preparation-sol-20261117'
COMMIT = '7d5ac8ea5dc8d6cddee457da7a5b40042d36d344'
PARENT = '96f04aa5544df69daba07a9ed4d6212172e9984a'
TREE = 'c59d0d0a542f20bceb3556b1e936e86b22626434'
checks, evidence = [], {}
active = 'startup'

def now(): return datetime.now(timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def save(name, value):
    (A/name).write_text(json.dumps(value, indent=2, ensure_ascii=True)+'\n')
def need(ok, label, detail=None):
    global active
    active = label
    if not ok: raise AssertionError(json.dumps({'criterion':label,'detail':detail}, ensure_ascii=True))
    checks.append({'criterion':label,'pass':True,'detail':detail})
def meta(p):
    st=p.lstat()
    if not stat.S_ISREG(st.st_mode): raise ValueError('Not regular: '+str(p))
    b=p.read_bytes()
    return {'bytes':len(b),'SHA256':sha(b),'mode':oct(stat.S_IMODE(st.st_mode))}
def snapshot(root):
    st=root.lstat()
    if not stat.S_ISDIR(st.st_mode): raise ValueError('Not directory: '+str(root))
    files,dirs,other={}, {}, {}
    for p in sorted(root.rglob('*')):
        t=p.lstat(); name=str(p.relative_to(root))
        if stat.S_ISREG(t.st_mode): files[name]=meta(p)
        elif stat.S_ISDIR(t.st_mode): dirs[name]=oct(stat.S_IMODE(t.st_mode))
        else: other[name]={'mode':oct(stat.S_IMODE(t.st_mode)), 'symlink':os.readlink(p) if p.is_symlink() else None}
    return {'root':str(root),'root_mode':oct(stat.S_IMODE(st.st_mode)), 'files':files,'directories':dirs,'other':other}
def git(repo,*args):
    cmd=['/usr/bin/git','--no-optional-locks','-C',str(repo),*args]
    r=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'})
    if r.returncode: raise RuntimeError(json.dumps({'argv':cmd,'exit':r.returncode,'stderr':r.stderr.decode(errors='replace')}))
    return r.stdout
def native(repo):
    gd=repo/'.git'; packed=gd/'packed-refs'
    return {'files':{n:meta(gd/n) for n in ['HEAD','index','config']},
            'HEAD':(gd/'HEAD').read_text().strip(),
            'resolved_local_HEAD':git(repo,'rev-parse','HEAD').decode().strip(),
            'local_heads':snapshot(gd/'refs/heads'),
            'packed_local_head_lines':[x for x in packed.read_text().splitlines() if re.match(r'^[0-9a-f]{40} refs/heads/',x)],
            'packed_refs_mode':oct(stat.S_IMODE(packed.stat().st_mode))}
def comparable_snapshot(x): return {k:v for k,v in x.items() if k!='root'}
def guard():
    return {'UTC':now(), 'M':native(M), 'W':native(W), 'public':snapshot(W/'public'),
            'candidate':snapshot(S/'candidate/public'),
            'source_namespaces':{str(P/'papers'/n/'sources'):snapshot(P/'papers'/n/'sources') for n in ['22983519','23527793']},
            'frozen_stage_namespace':snapshot(S), 'frozen_preparation_namespace':snapshot(PREP),
            'runtime_publish_namespace':snapshot(R),
            'inputs':{str(p):meta(p) for p in guarded_files},
            'scope_exclusions':['remote-tracking refs','FETCH_HEAD','nonlocal packed-ref lines','Firebase metadata outside public'],
            'no_global_native_repository_identity_inferred':True}

def read_index(path):
    b=path.read_bytes()
    need(b[:4]==b'DIRC' and len(b)>=32,'index_header_'+path.name)
    version,n=struct.unpack('>II',b[4:12]); need(version==2,'index_version_'+path.name,version)
    need(hashlib.sha1(b[:-20]).digest()==b[-20:],'index_checksum_'+path.name)
    pos=12; entries={}; order=[]
    for i in range(n):
        start=pos; fields=struct.unpack('>10I',b[pos:pos+40]); oid=b[pos+40:pos+60]; flags=struct.unpack('>H',b[pos+60:pos+62])[0]
        pos+=62; ext=b''
        if flags&0x4000: ext=b[pos:pos+2];pos+=2
        end=b.index(b'\0',pos); name=b[pos:end]; pos=start+((end+1-start+7)//8)*8
        padding=b[end+1:pos]
        if not name or any(padding) or ((flags&0xfff)!=min(len(name),0xfff)) or ((flags>>12)&3):
            raise AssertionError('Malformed/unmerged record '+str(i)+' in '+str(path))
        if name in entries: raise AssertionError('Duplicate index name '+name.hex())
        entries[name]={'raw':b[start:pos], 'mode':fields[6], 'oid':oid,'flags':flags,'extended':ext,'stat':fields,'padding':padding}
        order.append(name)
    need(order==sorted(order),'index_order_'+path.name)
    extensions=[]
    while pos<len(b)-20:
        sig=b[pos:pos+4]; size=struct.unpack('>I',b[pos+4:pos+8])[0]; whole=b[pos:pos+8+size]
        if len(whole)!=8+size: raise AssertionError('Truncated extension')
        extensions.append((sig,whole,whole[8:]));pos+=8+size
    need(pos==len(b)-20 and [x[0] for x in extensions]==[b'TREE'],'index_extensions_'+path.name)
    return {'bytes':b,'entries':entries,'extension':extensions[0]}

def trees(entries):
    root={}
    for path,e in entries.items():
        parts=path.split(b'/'); node=root
        if any(p in (b'',b'.',b'..') for p in parts): raise AssertionError('Unsafe raw name')
        for part in parts[:-1]:
            if part not in node: node[part]={}
            if not isinstance(node[part],dict): raise AssertionError('Tree collision')
            node=node[part]
        if parts[-1] in node: raise AssertionError('Tree collision')
        node[parts[-1]]=(e['mode'],e['oid'])
    result={}
    def build(node,path):
        raw=b''; count=0; sub=0
        for name,v in sorted(node.items(),key=lambda t:t[0]+(b'/' if isinstance(t[1],dict) else b'\0')):
            if isinstance(v,dict):
                child=build(v,path+b'/'+name if path else name);mode=b'40000';oid=child['oid'];count+=child['count'];sub+=1
            else:
                m,oid=v
                if m not in (0o100644,0o100755,0o120000,0o160000): raise AssertionError('Unexpected index mode '+oct(m))
                mode=format(m,'o').encode();count+=1
            raw+=mode+b' '+name+b'\0'+oid
        oid=hashlib.sha1(b'tree '+str(len(raw)).encode()+b'\0'+raw).digest()
        row={'oid':oid,'raw':raw,'count':count,'subtrees':sub};result[path]=row;return row
    build(root,b'');return result

def cache_nodes(payload):
    pos=0; out=[]
    def parse(parent,root=False):
        nonlocal pos
        end=payload.index(b'\0',pos);name=payload[pos:end];pos=end+1
        end=payload.index(b'\n',pos); count,sub=map(int,payload[pos:end].split(b' '));pos=end+1
        if root and name!=b'':raise AssertionError('Cache root name')
        if not root and (not name or b'/' in name):raise AssertionError('Cache component')
        path=b'' if root else parent+b'/'+name if parent else name
        oid=None
        if count>=0:oid=payload[pos:pos+20];pos+=20
        row={'path':path,'count':count,'subtrees':sub,'oid':oid};out.append(row)
        for _ in range(sub):parse(path)
    parse(b'',True)
    need(pos==len(payload),'TREE_payload_consumed')
    return out

def leaves(commit):
    raw=git(W,'ls-tree','-r','-z','--full-tree',commit);out={}
    for row in raw.split(b'\0'):
        if not row:continue
        head,name=row.split(b'\t',1);mode,kind,oid=head.split(b' ')
        if name in out:raise AssertionError('Duplicate Git leaf')
        out[name]=(int(mode,8),bytes.fromhex(oid.decode()))
    return out

def objects(oids):
    sequence=sorted(set(oids));request=b''.join(x.hex().encode()+b'\n' for x in sequence)
    if not sequence:return {}
    cmd=['/usr/bin/git','--no-optional-locks','-C',str(W),'cat-file','--batch']
    q=subprocess.run(cmd,input=request,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'})
    if q.returncode:raise RuntimeError(q.stderr.decode(errors='replace'))
    b=q.stdout;pos=0;out={}
    for wanted in sequence:
        end=b.index(b'\n',pos);head=b[pos:end].split();pos=end+1
        if len(head)!=3 or head[1]!=b'tree':raise AssertionError('Missing/non-tree cache object '+wanted.hex())
        size=int(head[2]);body=b[pos:pos+size];pos+=size
        if b[pos:pos+1]!=b'\n':raise AssertionError('Batch framing')
        pos+=1
        if bytes.fromhex(head[0].decode())!=wanted or hashlib.sha1(b'tree '+str(size).encode()+b'\0'+body).digest()!=wanted:raise AssertionError('Git object hash mismatch')
        out[wanted]=body
    if pos!=len(b):raise AssertionError('Trailing batch output')
    return out

class ItemHTML(HTMLParser):
    def __init__(self):super().__init__();self.parts=[];self.stack=[];self.units=[];self.links=[]
    def handle_starttag(self,tag,attrs):
        if tag=='li':self.parts=[];self.links=[];self.stack.append('li')
        if self.stack and tag=='a':self.links.append(dict(attrs).get('href'))
    def handle_data(self,data):
        if self.stack:self.parts.append(data)
    def handle_endtag(self,tag):
        if tag=='li' and self.stack:
            self.units.append({'text':' '.join(' '.join(self.parts).split()),'hrefs':self.links[:]});self.stack.pop()
def aggregate(text):
    scripts=re.findall(r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',text,re.S|re.I)
    data=[json.loads(s) for s in scripts]
    lists=[]
    def visit(x):
        if isinstance(x,dict):
            if x.get('@type')=='ItemList':lists.append(x)
            for v in x.values():visit(v)
        elif isinstance(x,list):
            for v in x:visit(v)
    for x in data:visit(x)
    if len(lists)!=1:raise AssertionError('Expected exactly one ItemList')
    h=ItemHTML();h.feed(text)
    raw_html=re.findall(r'<li\b[^>]*>.*?</li>',text,re.S|re.I)
    raw_json=[];decoder=json.JSONDecoder()
    script=next(s for s in scripts if '"ItemList"' in s)
    pos=script.index('[',script.index('"itemListElement"'))+1
    while True:
        while script[pos].isspace() or script[pos]==',':pos+=1
        if script[pos]==']':break
        _,end=decoder.raw_decode(script,pos);raw_json.append(script[pos:end]);pos=end
    return lists[0],h.units,raw_html,raw_json
def xmltree(x):return {'tag':x.tag,'attributes':x.attrib,'text':x.text,'tail':x.tail,'children':[xmltree(c) for c in x]}

baseline=json.loads((S/'GUARDS_BEFORE_V2.json').read_text())
plan=json.loads((PREP/'PLAN.json').read_text())
targets=json.loads((S/'TARGETS.json').read_text())
guarded_files=[PREP/'PLAN.json',PREP/'release_two.py',S/'TARGETS.json',S/'GUARDS_BEFORE_V2.json',S/'AGGREGATE_PRESERVATION.json',S/'CANDIDATE_MANIFEST.json',S/'originals/research-index.html',S/'originals/research-sitemap.xml']
guarded_files += [p for p in R.rglob('*') if p.is_file()]
asset_map=[]
for record,slug in [('22983519','radial-orthogonality-dual-conformal-flatness'),('23527793','designed-tree-congestion-fragmentation')]:
    source=P/'papers'/record/'sources/assets'
    names=['SHA256SUMS.txt','paper.pdf','source-and-verification.zip'] if record=='22983519' else ['congestion-fragmentation.pdf','congestion-fragmentation-verification.zip']
    for name in names:asset_map.append((source/name,'research/'+slug+'/assets/'+name))
for packet,slug in [('radial-statistical-editorial-sol-20261117','radial-orthogonality-dual-conformal-flatness'),('designed-tree-editorial-sol-20261117','designed-tree-congestion-fragmentation')]:
    asset_map.append((P/'verification'/packet/'citation.bib','research/'+slug+'/citation.bib'))
guarded_files += [p for p,_ in asset_map]
before=None; failure=None
try:
    before=guard();save('GUARDS_BEFORE.json',before)
    need(meta(PREP/'release_two.py')['SHA256']=='c253cf4b3a20bd2499b752e9cb2fece9019a6a0ba10be16b63ff85b7adf7c56d','producer_helper_identity_only_no_execution')
    for key in ['target_plan','candidate_manifest','build_guards_before','aggregate_preservation']:
        ctl=plan['controls'][key];actual=meta(Path(ctl['path']))
        need(actual['bytes']==ctl['bytes'] and actual['SHA256']==ctl['SHA256'] and int(actual['mode'],8)==int(ctl['mode'],8),'frozen_input_control_pin_'+key)
    need(before['public']['root_mode']=='0o750','public_root_mode')
    pub=before['public'];cand=before['candidate']
    need(comparable_snapshot(pub)==comparable_snapshot(cand),'complete_public_equals_candidate')
    need(len(pub['files'])==781 and len(pub['directories'])==377 and not pub['other'],'complete_public_counts',{'files':len(pub['files']),'dirs':len(pub['directories'])})
    need(sum(Path(x).name=='.DS_Store' for x in pub['files'])==17,'all_17_DSStore')
    cm=json.loads((S/'CANDIDATE_MANIFEST.json').read_text())
    need(all(pub[k]==cm[k] for k in ['root_mode','files','directories']),'candidate_manifest_actual')
    old=baseline['public']; add=set(targets['A']);mod=set(targets['M']);scope=add|mod
    need(len(add)==9 and len(mod)==2 and not targets['D'] and len(scope)==11,'target_schema_9A2M')
    need(set(plan['scope_paths'])=={'public/'+x for x in scope} and all(not x.startswith('public/') for x in scope),'public_prefix_exactly_once')
    need(set(pub['files'])==set(old['files'])|add and not add&set(old['files']),'exact_file_additions')
    need(len(old['files'])==772 and len(old['directories'])==373,'baseline_scope_counts')
    preserved={k:v for k,v in old['files'].items() if k not in mod}
    need(len(preserved)==770 and all(pub['files'][k]==v for k,v in preserved.items()),'all_770_untargeted_buffers_modes')
    need(set(pub['directories'])==set(old['directories'])|set(targets['new_directories']),'four_new_directories')
    need(all(pub['directories'][k]==v for k,v in old['directories'].items()),'all_373_old_directory_modes')
    need(all(pub['directories'][k]=='0o755' for k in targets['new_directories']) and all(pub['files'][k]['mode']=='0o644' for k in scope),'new_and_selected_modes')
    for source,rel in asset_map:need(source.read_bytes()==(W/'public'/rel).read_bytes(),'exact_source_asset_or_Bib_'+rel,meta(source))
    oldhtml=(S/'originals/research-index.html').read_text();newhtml=(W/'public/research/index.html').read_text()
    oldxml=(S/'originals/research-sitemap.xml').read_text();newxml=(W/'public/research/sitemap.xml').read_text()
    need(meta(S/'originals/research-index.html')==old['files']['research/index.html'] and meta(S/'originals/research-sitemap.xml')==old['files']['research/sitemap.xml'],'original_replacement_buffers_bound_to_baseline')
    ag=json.loads((S/'AGGREGATE_PRESERVATION.json').read_text()); oi,ov,oh,oj=aggregate(oldhtml);ni,nv,nh,nj=aggregate(newhtml)
    need(len(ov)==126 and len(nv)==128 and oi['numberOfItems']==126 and ni['numberOfItems']==128,'aggregate_126_to_128_counts')
    need(nv[:126]==ov and nh[:126]==oh and nj[:126]==oj and ni['itemListElement'][:126]==oi['itemListElement'],'all_126_visible_typed_raw_units')
    need(ov==ag['index']['old_visible'] and oh==ag['index']['old_raw_HTML_units'] and oj==ag['index']['old_raw_JSON_units'] and oi['itemListElement']==ag['index']['old_typed'],'preservation_data_independently_extracted')
    need(ni['itemListElement'][126:]==ag['index']['new_items'] and len({x['url'] for x in ni['itemListElement']})==128,'new_two_unique_items')
    restore=newhtml.replace(ag['index']['appended_HTML'],'',1).replace(ag['index']['appended_JSON'],'',1).replace('"numberOfItems": 128','"numberOfItems": 126',1)
    need(newhtml.count(ag['index']['appended_HTML'])==1 and newhtml.count(ag['index']['appended_JSON'])==1 and restore==oldhtml,'whole_HTML_buffer_reversible')
    ox=ET.fromstring(oldxml);nx=ET.fromstring(newxml);orn=re.findall(r'<url>.*?</url>',oldxml,re.S);nrn=re.findall(r'<url>.*?</url>',newxml,re.S)
    need(len(ox)==127 and len(nx)==129 and nrn[:127]==orn and [xmltree(x) for x in nx[:127]]==[xmltree(x) for x in ox],'all_127_XML_nodes_preserved')
    need(newxml.count(ag['sitemap']['appended_XML'])==1 and newxml.replace(ag['sitemap']['appended_XML'],'',1)==oldxml,'whole_XML_buffer_reversible')
    evidence['aggregate']={'old_articles':126,'new_articles':128,'old_XML':127,'new_XML':129,'all_prior_units_and_buffers_exact':True}
    idx=read_index(W/'.git/index');backup=read_index(R/'native-backups/index.before');selected=read_index(R/'native-successor.index')
    need(len(idx['bytes'])==9059206 and sha(idx['bytes'])=='592a25281b63a357fbe4fe2580e2c9764ba2b4836650d8751ac573ff8117c365','actual_native_successor_pin')
    need(before['W']['files']['index']['mode']=='0o644' and meta(R/'native-successor.index')['mode']=='0o644','native_and_selected_index_modes')
    need(len(backup['bytes'])==9057886 and sha(backup['bytes'])=='e6285d49b7249ae2c88a1f624ca98c1dcf480424db272c4fe111ca91dbdafb5e','actual_native_baseline_pin')
    need(idx['bytes']==selected['bytes'],'selected_successor_equals_actual_native')
    ie,be=idx['entries'],backup['entries']; paths={('public/'+x).encode() for x in scope}; adds={('public/'+x).encode() for x in add}
    need(len(ie)==58721 and len(be)==58712 and set(ie)==set(be)|adds,'raw_index_counts_paths')
    untouched=set(be)-paths
    need(len(untouched)==58710 and all(be[n]['raw']==ie[n]['raw'] for n in untouched),'all_58710_whole_raw_records_preserved')
    save('RAW_RECORD_EVIDENCE.json',{'protected_count':len(untouched),'records':[{'path_hex':n.hex(),'raw_SHA256':sha(be[n]['raw']),'raw_bytes':len(be[n]['raw']),'stat_fields':be[n]['stat'],'mode':oct(be[n]['mode']),'OID':be[n]['oid'].hex(),'flags':be[n]['flags'],'extended_hex':be[n]['extended'].hex(),'padding_hex':be[n]['padding'].hex()} for n in sorted(untouched)]})
    bt=trees(be);it=trees(ie);need(it[b'']['oid'].hex()==TREE,'in_memory_full_native_tree')
    bcommit=leaves(PARENT);icommit=leaves(COMMIT)
    raw_before={p:(v['mode'],v['oid']) for p,v in be.items()};raw_after={p:(v['mode'],v['oid']) for p,v in ie.items()}
    need(raw_before==bcommit and raw_after==icommit,'all_commit_leaves_modes_OIDs_and_foreign_staging_0_to_0')
    need(set(icommit)==set(bcommit)|adds and all(icommit[n]==bcommit[n] for n in untouched),'all_untargeted_commit_leaves_preserved')
    need(bt[b'']['oid'].hex()==git(W,'rev-parse',PARENT+'^{tree}').decode().strip(),'baseline_in_memory_tree_matches_parent')
    commitbody=git(W,'cat-file','commit',COMMIT).decode();headers,message=commitbody.split('\n\n',1)
    need(headers.splitlines()[:2]==['tree '+TREE,'parent '+PARENT] and all(re.fullmatch(k+r' Alec Kriebel <me@aleckriebel.com> \d+ [+-]\d{4}',next(x for x in headers.splitlines() if x.startswith(k+' '))) for k in ['author','committer']) and message.strip()==plan['commit_message'],'commit_parent_tree_identity_message')
    delta=git(W,'diff-tree','--no-commit-id','--no-renames','--raw','-r','-z',PARENT,COMMIT).split(b'\0'); changes=[]
    for i in range(0,len(delta)-1,2):
        fields=delta[i].split();name=delta[i+1];changes.append((name,fields[-1].decode()))
    need(dict(changes)=={**{x:'A' for x in adds},**{('public/'+x).encode():'M' for x in mod}},'exact_actual_commit_11_path_9A2M_delta')
    for rel in scope:
        name=('public/'+rel).encode();data=(W/'public'/rel).read_bytes();expected=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).digest()
        need(raw_after[name]==(0o100644,expected),'selected_Git_blob_actual_bytes_'+rel)
    ext=idx['extension'];bext=backup['extension']
    need(ext[1]==bext[1] and len(ext[1])==35878 and sha(ext[1])=='f12d2a0b795034ce5cab45ad6fa5da31b4d7ad6f4b22a5999ce27841b41350b3','TREE_whole_extension_distinct_pin')
    need(len(ext[2])==35870 and sha(ext[2])=='6078bbaef4d39e7b0418bc6ed44ad8f37d2733ec6de4a4e4ba165fe7e665bfcb','TREE_payload_distinct_pin')
    nodes=cache_nodes(ext[2]);valid=[n for n in nodes if n['count']>=0];invalid=[n for n in nodes if n['count']<0]
    expected_invalid=[b'',b'public',b'public/research',b'public/research/binary-relation-liveness',b'public/research/rational-point-undecidability',b'public/research/focal-distance-period-criterion']
    need(len(nodes)==983 and len(valid)==977 and [n['path'] for n in invalid]==expected_invalid and all(n['oid'] is None and n['count']==-1 for n in invalid),'TREE_983_nodes_977_valid_6_preexisting_invalid_no_OID')
    need(len({n['path'] for n in nodes})==983,'TREE_unique_paths')
    bodies=objects([n['oid'] for n in valid]);cache=[]
    for n in valid:
        t=it.get(n['path']);oldtree=bt.get(n['path'])
        if t is None or oldtree is None or n['count']!=t['count'] or n['subtrees']!=t['subtrees'] or n['oid']!=t['oid'] or bodies[n['oid']]!=t['raw'] or oldtree['oid']!=n['oid']:
            raise AssertionError('TREE valid node mismatch '+n['path'].hex())
        cache.append({'path_hex':n['path'].hex(),'entries':n['count'],'subtrees':n['subtrees'],'OID':n['oid'].hex(),'tree_raw_SHA256':sha(t['raw'])})
    need(len(cache)==977,'every_valid_TREE_node_matches_raw_entries_and_existing_Git_object')
    save('TREE_NODE_EVIDENCE.json',{'whole_extension':{'bytes':len(ext[1]),'SHA256':sha(ext[1])},'payload':{'bytes':len(ext[2]),'SHA256':sha(ext[2])},'valid_nodes':cache,'invalidated_paths':[n['path'].hex() for n in invalid],'raw_native_root_tree':it[b'']['oid'].hex(),'old_parent_cache_not_assumed_valid_at_invalid_nodes':True})
    for repo,key in [(M,'M'),(W,'W')]:
        cur=before[key];oldn=baseline['native_controls'][key]
        need(cur['HEAD']==oldn['HEAD'] and cur['files']['HEAD']==oldn['files']['HEAD'] and cur['files']['config']==oldn['files']['config'] and cur['packed_local_head_lines']==oldn['packed_local_head_lines'] and cur['packed_refs_mode']==oldn['packed_refs_mode'],'native_HEAD_config_packed_local_heads_'+key)
        expected_heads=oldn['local_heads'].copy();expected_heads={**expected_heads,'other':{}}
        if key=='W':expected_heads={**expected_heads,'files':{**expected_heads['files'],'master':{**expected_heads['files']['master'],'SHA256':sha((COMMIT+'\n').encode())}}}
        need(comparable_snapshot(cur['local_heads'])==comparable_snapshot(expected_heads),'native_loose_local_head_scope_'+key)
        if key=='M':need(cur['files']['index']==oldn['files']['index'] and cur['resolved_local_HEAD']==oldn['resolved_local_HEAD'],'Math_native_index_and_main_preserved')
        else:need(cur['resolved_local_HEAD']==COMMIT and (repo/'.git/refs/heads/master').read_text()==COMMIT+'\n','authorized_W_master_only')
    evidence['commit']={'commit':COMMIT,'parent':PARENT,'tree':TREE,'paths':[{'path_hex':p.hex(),'status':s} for p,s in changes],'foreign_staging_before':0,'foreign_staging_after':0}
    evidence['index']={'before_records':len(be),'after_records':len(ie),'protected_whole_raw_records':len(untouched),'TREE_valid_nodes':len(cache),'TREE_invalid_nodes':len(invalid)}
except BaseException as ex:
    failure={'UTC':now(),'active_criterion':active,'exception':repr(ex),'traceback':traceback.format_exc()}
    save('FIRST_FAILURE.json',failure);sys.stderr.write(failure['traceback'])
finally:
    after=guard();save('GUARDS_AFTER.json',after)
    if before:
        left={k:v for k,v in before.items() if k!='UTC'};right={k:v for k,v in after.items() if k!='UTC'}
        unchanged=left==right
        if not unchanged and failure is None:
            failure={'UTC':now(),'active_criterion':'complete_before_after_guards','exception':'Protected guard changed during one audit','traceback':''};save('FIRST_FAILURE.json',failure);sys.stderr.write(failure['exception']+'\n')
    else:unchanged=False
    result={'schema':'independent-radial-tree-local-postpublication-audit-v1','UTC':now(),'status':'FIRST_FAILURE_STOP' if failure else 'PASS_FINITE_LOCAL_DATA_AUDIT','checks':checks,'evidence':evidence,'before_after_protected_guards_unchanged':unchanged,'first_failure':failure,'audit_runs':1,'helper_or_producer_execution_import_AST_compile_test':0,'network_or_mutation_of_protected_scope':False,'completion_percent':100 if failure is None else round(100*len(checks)/80),'scope_limit':'Local observed data and existing Git objects only; no live/UI/deployment/scientific certificate.'}
    save('DATA_AUDIT.json',result)
    print(json.dumps({'status':result['status'],'checks_passed':len(checks),'guards_unchanged':unchanged,'first_failure':failure['active_criterion'] if failure else None}))
sys.exit(1 if failure else 0)
