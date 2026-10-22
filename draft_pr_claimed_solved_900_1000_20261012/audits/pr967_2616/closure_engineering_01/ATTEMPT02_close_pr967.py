#!/usr/bin/env python3
"""PROPOSED PR967 priority closure; default is read-only, never acceptance.

Use a trusted interpreter with -I -S -B and independently authenticated operations
and disposition SHA256 pins. No external operation occurs on import. The external
pins, interpreter and standard library are trust roots, not an OS sandbox.
"""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise RuntimeError('Use Python -I -S -B')
import argparse,base64,copy,fcntl,hashlib,json,os,re,sqlite3,stat,subprocess
from contextlib import contextmanager
from datetime import datetime,timezone
from email.utils import parsedate_to_datetime
from pathlib import Path,PurePosixPath
P=Path(__file__).resolve().parent
ROOT=P.parent
A=P/'audits/pr967_2616'
W=A/'closure_runtime'
PR=967
KEY='2616'
HEAD='b356dec5cb01e5f536b9cfeece56ad08844c03cb'
REPO='AlecKriebel/Math'
QUEUE='unsolved_math_prioritization/QUEUE.md'
STATE='unsolved_math_prioritization/state.json'
HISTORY='unsolved_math_prioritization/history.jsonl'
CATALOG='unsolved_math_prioritization/catalog.json'
RELATED='unsolved_math_prioritization/review_v2/related_target_groups.json'
PREFIX='unsolved_math_prioritization/attempts/'+KEY+'/'
HELPERS=['close_pr967.py','finalize_pr967_and_gate_next.py']
FAMILIES=frozenset(['structural_selection_01','topology_falsifier_01','computational_adversary_01','priority_classical_01','priority_recent_01','exact_priority_falsifier_01'])
RECORDS_SHA='610351fbb778f78ce53cda03ea715f38615abb5710690987c214f8093bda13ae'
REPORT_SHA='ddde58f03f320c881b78e59b60a40f315e1811c7c88aaa25ce620c427afbb6ca'
STATEMENT='4535dfaab53da411c31aefaf58681b91c9cec815d0b47c6605f85646e08d0cf4'
REVIEW='84c273ec6e60695b39018662d237af6d5aa5717b6bcdff0bcabb5ab378c98a4c'
PRIVATE='07e53ea5a9d2a89d4c9d4803d25385ed81784d86b826230b6bdf39e7441e47e8'
PRIOR='44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a'
FINDING_COUNTS={'structural_selection_01':4,'topology_falsifier_01':8,'computational_adversary_01':7,'priority_classical_01':6,'priority_recent_01':5,'exact_priority_falsifier_01':5}
RECENT_SEAL='268863c9f2055cebbb9b46c2cd72a7dd4b722105913ce9852c8edad4f8718558'
MARKER='<!-- PR967-PRIORITY-CLOSURE-v1:'+HEAD+' -->'
OUTCOME='closed_without_merge_established_priority'
MAX=32*1024*1024
MAX_JSON=8*1024*1024


def need(ok,message):
    if not ok:raise RuntimeError('PR967 closure guard: '+message)

def sha(raw):return hashlib.sha256(raw).hexdigest()
def pin(raw):return {'bytes':len(raw),'sha256':sha(raw)}
def enc(value):return (json.dumps(value,sort_keys=True,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
def now():return datetime.now(timezone.utc).isoformat()
def utc(value):
    need(type(value) is str,'timestamp string')
    result=datetime.fromisoformat(value.replace('Z','+00:00'))
    need(result.tzinfo is not None and result.utcoffset().total_seconds()==0,'explicit UTC timestamp')
    return result

def exact(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return set(a)==set(b) and all(exact(a[k],b[k]) for k in a)
    if type(a) is list:return len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b))
    return a==b

def strict(raw):
    def pairs(items):
        out={}
        for k,v in items:need(k not in out,'duplicate JSON key');out[k]=v
        return out
    def bad(x):raise RuntimeError('Nonfinite JSON: '+x)
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=bad)

def safe(name):
    return (type(name) is str and bool(name) and '\\' not in name and '\0' not in name
        and not PurePosixPath(name).is_absolute() and PurePosixPath(name).as_posix()==name
        and all(x not in ('','.','..') for x in name.split('/')))

def fingerprint(value):
    need(type(value) is dict and set(value)=={'bytes','sha256'} and type(value['bytes']) is int
        and 0<=value['bytes']<=MAX and type(value['sha256']) is str
        and re.fullmatch('[0-9a-f]{64}',value['sha256']),'exact bounded fingerprint')

def digest(value):need(type(value) is str and re.fullmatch('[0-9a-f]{64}',value),'SHA256 string')
def oid(value):need(type(value) is str and re.fullmatch('[0-9a-f]{40}',value),'Git object identity')
def fields(value,types,label):
    need(type(value) is dict and set(types)<=set(value),label+' mandatory fields')
    for k,t in types.items():need(type(value[k]) is t,label+' type '+k)

def directory(path):
    name=Path(path).relative_to(ROOT).as_posix();need(safe(name),'directory scope')
    fd=os.open(ROOT,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW|os.O_NONBLOCK)
    try:
        for part in name.split('/'):
            child=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=fd)
            os.close(fd);fd=child
        return os.dup(fd)
    finally:os.close(fd)

def read(path,expected=None,cap=MAX):
    path=Path(path);name=path.relative_to(ROOT).as_posix();need(safe(name),'read path scope')
    if expected is not None:fingerprint(expected);cap=expected['bytes']
    fd=directory(path.parent)
    try:
        handle=os.open(path.name,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=fd)
        try:
            info=os.fstat(handle);need(stat.S_ISREG(info.st_mode) and info.st_size<=cap,'regular bounded input: '+name)
            blocks=[];total=0
            while total<=cap:
                block=os.read(handle,min(1024*1024,cap+1-total))
                if not block:break
                blocks.append(block);total+=len(block)
            raw=b''.join(blocks);need(len(raw)<=cap,'input grew: '+name)
            if expected is not None:need(pin(raw)==expected,'input fingerprint changed: '+name)
            return raw
        finally:os.close(handle)
    finally:os.close(fd)

def exists(path):
    try:read(path,cap=MAX_JSON);return True
    except FileNotFoundError:return False

def save(path,value):
    """Exclusive durable receipt; no silent overwrite or following ancestors."""
    raw=enc(value);need(len(raw)<=MAX_JSON,'receipt size cap');fd=directory(Path(path).parent)
    try:
        handle=os.open(Path(path).name,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW|os.O_NONBLOCK,0o600,dir_fd=fd)
        with os.fdopen(handle,'wb') as stream:
            need(stream.write(raw)==len(raw),'receipt short write');stream.flush();os.fsync(stream.fileno())
        os.fsync(fd)
    finally:os.close(fd)

def load(path):return strict(read(path,cap=MAX_JSON))

def runtime():
    fd=directory(A)
    try:
        try:os.mkdir(W.name,0o700,dir_fd=fd);os.fsync(fd)
        except FileExistsError:pass
    finally:os.close(fd)
    fd=directory(W)
    try:
        info=os.fstat(fd);need(info.st_uid==os.getuid() and stat.S_IMODE(info.st_mode)==0o700,'private operation directory owner/mode')
    finally:os.close(fd)

def run(args,raw=False,input=None):
    result=subprocess.run(args,cwd=ROOT,input=input,capture_output=True,check=True,text=not raw,timeout=90)
    out=result.stdout;need(len(out)<=MAX,'bounded command output');return out

def git(*args,raw=False,input=None):
    return run(['git','-c','maintenance.auto=false','-c','gc.auto=0',*args],raw=raw,input=input)

def api(method,endpoint,payload=None):
    """No retries. Server Date is retained for provable recovery chronology."""
    need(method in ('GET','POST','PATCH'),'bounded API method')
    args=['gh','api','--include','--method',method,endpoint]
    if payload is not None:args+=['--input','-']
    raw=run(args,raw=True,input=enc(payload) if payload is not None else None)
    split=re.split(b'\r?\n\r?\n',raw,maxsplit=1);need(len(split)==2,'API included response headers')
    header,body=split;lines=header.decode().splitlines();need(lines and re.fullmatch(r'HTTP/\S+ 2[0-9][0-9](?: .*)?',lines[0]),'API successful explicit HTTP status')
    dates=[x.split(':',1)[1].strip() for x in lines[1:] if x.lower().startswith('date:')]
    need(len(dates)==1,'API unique server Date');stamp=parsedate_to_datetime(dates[0]);need(stamp.tzinfo is not None,'server timezone')
    return strict(body),stamp.astimezone(timezone.utc).isoformat()

def gql(query,variables):
    data,stamp=api('POST','graphql',{'query':query,'variables':variables})
    need(type(data) is dict and not data.get('errors') and type(data.get('data')) is dict,'GraphQL complete response')
    return data['data'],stamp

def identity_actor(value):
    fields(value,{'id':int,'login':str,'node_id':str},'actor')
    need(value['id']>0 and value['login'] and value['node_id'],'actual actor identity')
    return {k:value[k] for k in ('id','login','node_id')}

def actor():
    value,stamp=api('GET','user');return identity_actor(value),stamp

def metadata(number):
    raw,stamp=api('GET',f'repos/{REPO}/pulls/{number}')
    fields(raw,{'number':int,'state':str,'draft':bool,'head':dict,'base':dict,'html_url':str,'node_id':str},'PR metadata')
    need(raw['number']==number and raw['state'] in ('open','closed') and raw['html_url']==f'https://github.com/{REPO}/pull/{number}','PR number/state/URL')
    for part in ('head','base'):
        fields(raw[part],{'sha':str,'ref':str,'repo':dict},part+' metadata');oid(raw[part]['sha'])
        fields(raw[part]['repo'],{'full_name':str,'owner':dict},part+' repository');fields(raw[part]['repo']['owner'],{'login':str},part+' owner')
        need(raw[part]['ref'] and raw[part]['repo']['full_name'],'nonempty branch/repository')
    for name in ('merged_at','closed_at'):need(name in raw and (raw[name] is None or type(raw[name]) is str),'explicit merge/closed timestamp')
    query='query($number:Int!){repository(owner:"AlecKriebel",name:"Math"){nameWithOwner pullRequest(number:$number){number state isDraft headRefOid headRefName baseRefName url mergedAt closedAt baseRef{name target{oid}}}}}'
    data,_=gql(query,{'number':number});repo=data.get('repository');need(type(repo) is dict and repo.get('nameWithOwner')==REPO,'actual repository')
    node=repo.get('pullRequest');fields(node,{'number':int,'state':str,'isDraft':bool,'headRefOid':str,'headRefName':str,'baseRefName':str,'url':str,'baseRef':dict},'live pointer')
    ref=node['baseRef'];fields(ref,{'name':str,'target':dict},'actual baseRef');fields(ref['target'],{'oid':str},'actual base target');oid(ref['target']['oid'])
    expected={'number':number,'state':'OPEN' if raw['state']=='open' else 'CLOSED','isDraft':raw['draft'],'headRefOid':raw['head']['sha'],'headRefName':raw['head']['ref'],'baseRefName':raw['base']['ref'],'url':raw['html_url'],'mergedAt':raw['merged_at'],'closedAt':raw['closed_at']}
    if raw['merged_at'] is not None:expected['state']='MERGED'
    need(all(k in node and exact(node[k],v) for k,v in expected.items()) and ref['name']==node['baseRefName'],'REST/GraphQL identity drift')
    result={**expected,'currentBaseRefOid':ref['target']['oid'],'node_id':raw['node_id'],'head_repository':raw['head']['repo']['full_name'],'head_owner':raw['head']['repo']['owner']['login'],'base_repository':raw['base']['repo']['full_name'],'base_owner':raw['base']['repo']['owner']['login']}
    return result,stamp

def changed_paths(before):
    query='query($number:Int!,$cursor:String){repository(owner:"AlecKriebel",name:"Math"){pullRequest(number:$number){number state isDraft headRefOid headRefName baseRefName url mergedAt closedAt baseRef{name target{oid}} changedFiles files(first:100,after:$cursor){nodes{path} pageInfo{hasNextPage endCursor}}}}}'
    paths=[];pages=[];cursor=None;seen=set();count=None
    for _ in range(30):
        data,_=gql(query,{'number':before['number'],'cursor':cursor});node=data.get('repository',{}).get('pullRequest')
        fields(node,{'changedFiles':int,'files':dict,'baseRef':dict},'filename page')
        for field in ('number','state','isDraft','headRefOid','headRefName','baseRefName','url','mergedAt','closedAt'):
            need(field in node and exact(node[field],before[field]),'filename page PR identity drift')
        need(node['baseRef'].get('name')==before['baseRefName'] and node['baseRef'].get('target',{}).get('oid')==before['currentBaseRefOid'],'filename page actual live base drift')
        n=node['changedFiles'];need(1<=n<=3000 and (count is None or n==count),'bounded stable changedFiles');count=n
        con=node['files'];need(set(con)=={'nodes','pageInfo'} and type(con['nodes']) is list and 1<=len(con['nodes'])<=100,'canonical filename connection')
        for item in con['nodes']:
            need(type(item) is dict and set(item)=={'path'} and safe(item['path']),'canonical safe filename');paths.append(item['path'])
        need(len(paths)<=count and len(paths)==len(set(paths))==len({x.casefold() for x in paths}),'duplicate/aliased/excess changed paths')
        info=con['pageInfo'];fields(info,{'hasNextPage':bool},'filename pagination');pages.append({'sha256':sha(enc(node)),'count':len(con['nodes'])})
        if not info['hasNextPage']:
            need(len(paths)==count,'complete changed filename pages');return {'paths':paths,'pages':pages,'count':count}
        cursor=info.get('endCursor');need(type(cursor) is str and cursor and cursor not in seen,'distinct filename cursor');seen.add(cursor)
    raise RuntimeError('Filename page bound exceeded')

def queue_blob(head):
    oid(head)
    query='query($expr:String!){repository(owner:"AlecKriebel",name:"Math"){object(expression:$expr){... on Blob{oid byteSize isBinary text}}}}'
    data,_=gql(query,{'expr':head+':'+QUEUE});obj=data.get('repository',{}).get('object')
    fields(obj,{'oid':str,'byteSize':int,'isBinary':bool,'text':str},'immutable QUEUE blob');oid(obj['oid'])
    raw=obj['text'].encode();need(obj['isBinary'] is False and 0<len(raw)<=MAX and len(raw)==obj['byteSize'],'immutable QUEUE size/text')
    need(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==obj['oid'],'immutable QUEUE actual Git blob OID')
    return raw,{'git_blob':obj['oid'],**pin(raw)}

def row(raw,key):
    matches=[x for x in raw.splitlines(keepends=True) if ('| '+key+' /').encode() in x]
    need(len(matches)==1,'unique exact queue target row')
    literal=matches[0];cells=literal.decode().rstrip('\r\n').split('|');need(len(cells)>=13,'queue row schema')
    need(cells[2].strip().startswith(key+' /'),'queue row target identity')
    return literal,cells[8].strip(),cells[9].strip()

def repo_destination(meta):
    need(meta['head_repository']==REPO and meta['head_owner']=='AlecKriebel' and meta['base_repository']==REPO and meta['base_owner']=='AlecKriebel' and meta['baseRefName']=='main','exact head/base owner/repository/main; no fork retarget')

def status_gate(number=PR,key=KEY,expected_head=HEAD,allow_closed=False):
    """No mathematical/source/family intake until exact selected status passes."""
    before,stamp=metadata(number)
    closed=allow_closed and before['state']=='CLOSED' and before['mergedAt'] is None
    if not closed and (before['state']!='OPEN' or before['isDraft'] is not True):
        after,_=metadata(number);need(exact(before,after),'metadata-only skip identity drift')
        return {'action':'SKIP_NOT_OPEN_DRAFT','pr':after,'math_source_read':False,'server_utc':stamp}
    paths=changed_paths(before)
    if key is None:
        ids={m[1] for name in paths['paths'] if (m:=re.fullmatch(r'unsolved_math_prioritization/attempts/([0-9]+)/.+',name))}
        need(len(ids)==1,'next filename-only target identity');key=ids.pop()
    raw,blobpin=queue_blob(before['headRefOid']);literal,status,turns=row(raw,key)
    after,_=metadata(number);need(exact(before,after),'complete metadata/live-base/status bracket drift')
    out={'pr':after,'problem_id':key,'status':status,'declared_turns':turns,'queue_blob':blobpin,'queue_row':literal.decode(),'queue_row_sha256':sha(literal),'changed_paths':paths,'math_source_read':False,'server_utc':stamp}
    if status!='claimed_solved':return {**out,'action':'SKIP_STATUS_ONLY'}
    repo_destination(after)
    need(all(n==QUEUE or n.startswith('unsolved_math_prioritization/attempts/'+key+'/') for n in paths['paths']),'selected complete changed path scope')
    need(QUEUE in paths['paths'],'selected QUEUE change required')
    if expected_head is not None:
        need(number==PR and key==KEY and after['headRefOid']==expected_head and turns=='1/5','exact selected immutable HEAD/id/declared1/5')
        names=original_records()['files'];need(set(paths['paths'])==set(names)|{QUEUE},'exact original26+QUEUE complete filename scope')
    return {**out,'action':'CLOSED_RECONCILE_ONLY' if closed else 'ELIGIBLE'}

def original_records():
    raw=read(A/'ORIGINAL_FILE_RECORDS.json');need(sha(raw)==RECORDS_SHA,'external original26 inventory pin')
    doc=strict(raw);need(doc.get('head')==HEAD and type(doc.get('files')) is dict and len(doc['files'])==26,'original26 records schema')
    need(sum(x['bytes'] for x in doc['files'].values())==147731,'original total147731 bytes');return doc

def originals():
    records=original_records()['files'];listing=git('ls-tree','-r','-z',HEAD,'--',PREFIX,raw=True);entries={}
    for value in listing.split(b'\0'):
        if not value:continue
        header,name=value.split(b'\t',1);mode,kind,obj=header.decode().split();name=name.decode()
        need(name not in entries,'duplicate Git path');entries[name]=(mode,kind,obj)
    need(set(entries)==set(records),'closed immutable original Git inventory')
    checked={}
    for name,record in records.items():
        need(safe(name) and name.startswith(PREFIX),'original path scope');fingerprint({k:record[k] for k in ('bytes','sha256')})
        need(entries[name]==('100644','blob',record['git_blob']) and record['git_mode']=='100644' and record['disk_mode']=='0644','original Git/record mode')
        raw=git('cat-file','blob',record['git_blob'],raw=True);disk=read(A/'original'/name,expected={k:record[k] for k in ('bytes','sha256')})
        need(raw==disk and sha(raw)==record['sha256'] and len(raw)==record['bytes'],'original Git/disk exact bytes')
        need(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==record['git_blob'],'actual Git blob identity')
        info=(A/'original'/name).lstat();need(stat.S_IMODE(info.st_mode)==0o644,'original disk0644 mode')
        checked[name]={**pin(raw),'git_blob':record['git_blob'],'git_mode':'100644','disk_mode':'0644'}
    base=A/'original'/PREFIX
    actual={x.relative_to(A/'original').as_posix() for x in base.rglob('*') if not x.is_dir() or x.is_symlink()}
    need(actual==set(records),'closed original disk inventory')
    need(checked[PREFIX+'author/public/REPORT.md']['sha256']==REPORT_SHA,'source-specific proof report pin')
    return checked

def remote_main():
    url=git('remote','get-url','origin').strip();need(url in ('https://github.com/'+REPO+'.git','https://github.com/'+REPO,'git@github.com:'+REPO+'.git'),'origin exact GitHub owner/repository')
    values=git('ls-remote','origin','refs/heads/main').splitlines();need(len(values)==1,'unique actual remote main')
    parts=values[0].split();need(len(parts)==2 and parts[1]=='refs/heads/main','actual remote main reference');oid(parts[0]);parent=parts[0]
    try:git('cat-file','-e',parent+'^{commit}')
    except subprocess.CalledProcessError:
        git('fetch','--no-auto-maintenance','--no-write-fetch-head','--no-tags','--no-recurse-submodules','--no-prune','origin',parent)
    return parent

def blob(parent,name):return git('show',parent+':'+name,raw=True)

def sqlite_pin(path):
    fd=directory(path.parent)
    try:
        handle=os.open(path.name,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=fd)
        try:
            info=os.fstat(handle);need(stat.S_ISREG(info.st_mode) and info.st_size<=256*1024*1024,'bounded regular SQLite')
            h=hashlib.sha256();total=0
            while True:
                block=os.read(handle,1024*1024)
                if not block:break
                total+=len(block);need(total<=256*1024*1024,'SQLite grew beyond cap');h.update(block)
            need(total==info.st_size,'stable SQLite size');return {'bytes':total,'sha256':h.hexdigest()}
        finally:os.close(handle)
    finally:os.close(fd)

def source_gate(parent):
    raw=read(A/'source_record_private.txt');need(sha(raw)==PRIVATE,'private source pin')
    source=strict(raw);need(type(source) is dict and source.get('review_hash')==REVIEW and type(source.get('problem')) is dict and type(source.get('prior_research')) is dict,'private source schema')
    problem=source['problem'];prior=source['prior_research'];need(prior=={} and sha(json.dumps(prior,sort_keys=True).encode())==PRIOR,'actual empty prior object; no inherited nonempty assumption')
    need(str(problem.get('id'))==KEY and type(problem.get('statement')) is str and sha(problem['statement'].encode())==STATEMENT,'nested statement identity')
    db=ROOT/'unsolved_math_prioritization/cache/catalog.sqlite'
    db_before=sqlite_pin(db);info=db.lstat();need(stat.S_ISREG(info.st_mode) and not db.is_symlink(),'regular read-only SQLite')
    with sqlite3.connect(db.as_uri()+'?mode=ro&immutable=1',uri=True) as connection:
        rows=connection.execute('SELECT payload,report FROM records WHERE key=?',(KEY,)).fetchall()
    need(len(rows)==1,'unique actual SQLite target');payload,report=map(strict,rows[0])
    need(exact(payload,problem) and exact(report,prior) and sha(json.dumps([payload,report],sort_keys=True).encode())==REVIEW,'actual SQLite source/prior/review reconstruction')
    need(sqlite_pin(db)==db_before,'SQLite byte identity unchanged by read')
    catalogue=strict(blob(parent,CATALOG));need(type(catalogue) is list,'current catalogue list')
    selected=[x for x in catalogue if type(x) is dict and str(x.get('id'))==KEY]
    need(len(selected)==1 and selected[0].get('present') is True and selected[0].get('holds')==[] and selected[0].get('statement_hash')==STATEMENT and selected[0].get('review_hash')==REVIEW,'fresh current catalogue/holds/source identity')
    groups=strict(blob(parent,RELATED)).get('groups');need(type(groups) is list and all(type(g) is dict and type(g.get('ids')) is list for g in groups),'current related-group schema')
    need(not any(KEY in map(str,g['ids']) for g in groups),'fresh related target membership requires reconciliation')
    return {'parent':parent,'statement_sha256':STATEMENT,'review_hash':REVIEW,'private_source_sha256':PRIVATE,'prior_report_sha256':PRIOR,'prior_report_actual_empty_object':True,'SQLite':db_before,'source_reconstructed':True,'holds':[],'related_target_groups':[]}

def native_pins(parent):
    raw={name:blob(parent,name) for name in (QUEUE,STATE,HISTORY)}
    state=strict(raw[STATE]);need(type(state) is dict and KEY not in state,'native target state must remain absent/UNKNOWN')
    history=[strict(x) for x in raw[HISTORY].splitlines() if x.strip()]
    need(all(type(x) is dict for x in history) and not any(str(x.get('id'))==KEY for x in history),'native target history must remain absent/UNKNOWN')
    return {name:pin(body) for name,body in raw.items()}

def inventory(expected):
    digest(expected);raw=read(A/'CLOSURE_OPERATIONS_INVENTORY.json');need(sha(raw)==expected,'external two-helper operations inventory')
    doc=strict(raw);need(type(doc) is dict and set(doc)=={'schema','pr','problem_id','original_pr_head','files'} and doc['schema']=='pr967-closure-operations-v1' and type(doc['pr']) is int and doc['pr']==PR and doc['problem_id']==KEY and doc['original_pr_head']==HEAD,'operations target/schema')
    names={(P/n).relative_to(ROOT).as_posix() for n in HELPERS};need(type(doc['files']) is dict and set(doc['files'])==names,'entire two-helper inventory')
    captured={name:read(ROOT/name,expected=value) for name,value in doc['files'].items()}
    return {'inventory_sha256':expected,'inventory':doc,'captured':captured}

def refraw(reference,evidence):
    need(type(reference) is dict and set(reference)=={'path','sha256'} and safe(reference['path']),'evidence reference schema')
    digest(reference['sha256']);need(reference['path'] in evidence and evidence[reference['path']]['sha256']==reference['sha256'],'separately pinned evidence reference')
    return read(ROOT/reference['path'],expected=evidence[reference['path']])

def refdoc(reference,evidence):return strict(refraw(reference,evidence))

def family(name,item,evidence):
    need(type(item) is dict and set(item)=={'manifest','authentication'},'family declaration')
    manifestref=item['manifest'];need(manifestref.get('path')==(A/'reviews'/name/'MANIFEST.json').relative_to(ROOT).as_posix(),'family-specific manifest path')
    manifest=refdoc(manifestref,evidence)
    normalized=refdoc(item['authentication'],evidence)
    top={'schema','normalization_utc','pr','problem_id','original_head','normalization_is_retrospective','families'}
    need(type(normalized) is dict and set(normalized)==top and normalized['schema']=='pr967-normalized-family-authentications-v1' and type(normalized['pr']) is int and normalized['pr']==PR and normalized['problem_id']==KEY and normalized['original_head']==HEAD and normalized['normalization_is_retrospective'] is True and type(normalized['families']) is dict and set(normalized['families'])==FAMILIES,'truthful combined root normalization')
    auth=normalized['families'][name]
    required={'status','manifest_path','manifest_sha256','manifest_allowlist_field','file_count','total_bytes','root_authentication_path','root_authentication_sha256','root_authentication_utc','root_authentication_entry_path','source_manifest_pin_field','source_count_field','source_bytes_field','source_all_members_field','full_intake_path','full_intake_sha256','full_intake_utc','authenticated_before_substantive_intake','historical_root_record_schema_preserved'}
    need(type(auth) is dict and set(auth)==required and auth['status']=='PASS_BYTES_BEFORE_FULL_REPORT_INTAKE' and auth['authenticated_before_substantive_intake'] is True and auth['historical_root_record_schema_preserved'] is True,'normalized family actual measured authentication')
    need(auth['manifest_path']==manifestref['path'] and auth['manifest_sha256']==manifestref['sha256'],'normalized exact family manifest')
    field=auth['manifest_allowlist_field'];need(field in ('explicit_public_allowlist','explicit_allowlist'),'explicit declared family allowlist field')
    need(not ({'explicit_public_allowlist','explicit_allowlist'}-{field})&set(manifest),'ambiguous undeclared family allowlist alias')
    records=manifest.get('files');allowed=manifest.get(field)
    need(type(records) is dict and records and type(allowed) is list and all(type(x) is str for x in allowed) and len(allowed)==len(set(allowed)) and set(allowed)==set(records) and 'MANIFEST.json' not in records,'equal unique entire declared family allowlist')
    need(len(records)<=1000 and type(auth['file_count']) is int and auth['file_count']==len(records) and type(auth['total_bytes']) is int,'bounded actual family count')
    for part,record in records.items():
        need(safe(part) and not set(part.split('/'))&{'private','private_sources','private_tmp','__pycache__'},'unsafe/private family member')
        read(A/'reviews'/name/part,expected=record)
    need(auth['total_bytes']==sum(v['bytes'] for v in records.values()),'actual family total byte count')
    source=refdoc({'path':auth['root_authentication_path'],'sha256':auth['root_authentication_sha256']},evidence)
    selector=auth['root_authentication_entry_path'];need(selector in ([],['families',name]),'exact right-family original source selector')
    selected=source if selector==[] else source.get('families',{}).get(name)
    need(type(selected) is dict and source.get('before_substantive_intake') is True,'original measured before-intake authentication')
    for fieldname,allowed,expected in [('source_manifest_pin_field',('external_manifest_sha256','manifest_sha256'),manifestref['sha256']),('source_count_field',('files','file_count'),len(records)),('source_bytes_field',('bytes','total_bytes'),auth['total_bytes']),('source_all_members_field',('all_members_authenticated',),True)]:
        key=auth[fieldname];need(key in allowed and exact(selected.get(key),expected),'original right-family source '+fieldname)
    intake=refdoc({'path':auth['full_intake_path'],'sha256':auth['full_intake_sha256']},evidence)
    need(source.get('utc')==auth['root_authentication_utc'] and intake.get('utc')==auth['full_intake_utc'],'original measured source/intake timestamps')
    need(utc(auth['root_authentication_utc'])<utc(auth['full_intake_utc'])<=utc(normalized['normalization_utc']),'retrospective normalization does not backdate authentication')
    if name=='priority_recent_01':need(manifestref['sha256']==RECENT_SEAL,'actual original recent-family seal')
    return {'manifest_sha256':manifestref['sha256'],'members':len(records),'bytes':auth['total_bytes'],'authentication_sha256':item['authentication']['sha256'],'sealed_files':records}

def prerequisites(disposition_pin,context):
    digest(disposition_pin);raw=read(A/'PRIORITY_DISPOSITION.json');need(sha(raw)==disposition_pin,'separate external priority disposition pin')
    d=strict(raw);keys={'schema','utc','pr','problem_id','original_pr_head','disposition','operations_inventory_sha256','closure_comment_sha256','fresh_reviewer_approved_comment_sha256','families','evidence_files','readiness','operation_authorization','finding_dispositions','reason','scope','historical_evidence'}
    need(type(d) is dict and set(d)==keys and d['schema']=='pr967-priority-closure-decision-v1' and type(d['pr']) is int and d['pr']==PR and d['problem_id']==KEY and d['original_pr_head']==HEAD and d['disposition']=='CLOSE_WITHOUT_MERGE_ESTABLISHED_PRIORITY','root final closure decision required')
    utc(d['utc']);need(d['operations_inventory_sha256']==context['inventory_sha256'],'decision exact current proposed helpers')
    scope=d['scope'];need(type(scope) is dict and type(scope.get('strict_historical_linked_body_hash_available')) is bool,'explicit reviewed historical body availability')
    expected_scope={'original_declared_turns':'1/5','historical_native_turn_count':'UNKNOWN','new_author_proof_responses':0,'proof_search_turns_added_by_audit':0,'no_ultimate_discovery_or_misconduct_adjudication':True,'strict_historical_linked_body_hash_available':scope['strict_historical_linked_body_hash_available'],'strict_historical_linked_body_hash_qualification_retained':True,'credit_alone_restores_original_target_novelty':False}
    need(d['reason']=='mathematically_correct_rediscovery' and exact(scope,expected_scope),'exact bounded closure/accounting/qualification scope')
    evidence=d['evidence_files'];need(type(evidence) is dict and evidence,'root evidence inventory')
    for name,record in evidence.items():need(safe(name) and name.startswith(A.relative_to(ROOT).as_posix()+'/'),'root evidence scope');read(ROOT/name,expected=record)
    need(type(d['families']) is dict and set(d['families'])==FAMILIES,'all SIX independent family seals')
    counts={name:family(name,item,evidence) for name,item in d['families'].items()}
    history=d['historical_evidence'];need(type(history) is dict and set(history)=={'status','original_qualification','archival_addendum'},'separate historical evidence chain')
    refraw(history['original_qualification'],evidence)
    if scope['strict_historical_linked_body_hash_available']:
        need(history['status']=='PINNED_PREPR_ARCHIVE_BODY','reviewed archival status')
        refraw(history['archival_addendum'],evidence)
    else:need(history['status']=='NOT_AVAILABLE_QUALIFIED' and history['archival_addendum'] is None,'honest historical qualification')
    ready=refdoc(d['readiness'],evidence)
    need(type(ready) is dict and set(ready)=={'schema','utc','pr','problem_id','original_pr_head','checks'} and ready['schema']=='pr967-root-closure-readiness-v1' and type(ready['pr']) is int and ready['pr']==PR and ready['problem_id']==KEY and ready['original_pr_head']==HEAD,'root source/proof/reproduction readiness schema')
    checks=ready['checks'];need(type(checks) is dict and set(checks)=={'source_identity','whole_proof','actual_reproduction','classical_priority_intake','recent_priority_intake','exact_priority_falsification','historical_date_qualification','finding_dispositions'},'all required individually rooted readiness checks')
    for label,check in checks.items():
        need(type(check) is dict and set(check)=={'status','observed_utc','evidence'} and check['status']=='PASS' and type(check['evidence']) is list and check['evidence'],'actual readiness evidence required: '+label)
        need(utc(check['observed_utc'])<=utc(ready['utc'])<=utc(d['utc']),'root readiness actual chronology')
        for reference in check['evidence']:refraw(reference,evidence)
    findings=refdoc(d['finding_dispositions'],evidence)
    required={'schema','utc','pr','problem_id','original_head','families','all_ids_unique','required_mathematical_repairs_remaining','priority_outcome','external_action_authority','no_new_author_proof_responses'}
    need(type(findings) is dict and set(findings)==required and findings['schema']=='pr967-root-individual-family-findings-v1' and type(findings['pr']) is int and findings['pr']==PR and findings['problem_id']==KEY and findings['original_head']==HEAD and type(findings['families']) is dict and set(findings['families'])==FAMILIES and findings['all_ids_unique'] is True and findings['required_mathematical_repairs_remaining']==[] and findings['external_action_authority'] is False and findings['no_new_author_proof_responses'] is True,'actual individually catalogued six-family findings')
    ids=[]
    for name,entries in findings['families'].items():
        need(type(entries) is list and len(entries)==FINDING_COUNTS[name],'all current individually identified family findings')
        for entry in entries:
            need(type(entry) is dict and set(entry)=={'id','identifier_origin','source','finding','disposition','resolution'} and all(type(entry[k]) is str and entry[k].strip() for k in entry),'individual finding actual disposition and identifier origin')
            need(entry['identifier_origin'] in ('original_family_id','root_canonical_index_of_narrative_finding_not_an_original_family_id'),'do not invent original-family IDs')
            source_names=[x for x in entry['source'].split('/') if x.endswith(('.md','.json','.py'))]
            need(source_names and all(x in counts[name]['sealed_files'] for x in source_names),'finding source actual sealed family file/section')
            ids.append(entry['id'])
    need(len(ids)==len(set(ids))==sum(FINDING_COUNTS.values()),'unique complete individually resolved initial finding catalog')
    body=read(A/'CLOSURE_COMMENT_DRAFT.md',cap=65536).decode();need(body.count(MARKER)==1 and body.strip() and sha(body.encode())==d['closure_comment_sha256']==d['fresh_reviewer_approved_comment_sha256'],'exact independently reviewed comment bytes/unique marker')
    authorization=refdoc(d['operation_authorization'],evidence)
    required={'schema','utc','root_issued','pr','problem_id','original_pr_head','operations_inventory_sha256','closure_comment_sha256','operation_nonce','actor','allowed_operations'}
    need(type(authorization) is dict and set(authorization)==required and authorization['schema']=='pr967-root-operation-authorization-v1' and authorization['root_issued'] is True and type(authorization['pr']) is int and authorization['pr']==PR and authorization['problem_id']==KEY and authorization['original_pr_head']==HEAD and authorization['operations_inventory_sha256']==context['inventory_sha256'] and authorization['closure_comment_sha256']==sha(body.encode()) and authorization['allowed_operations']==['comment','close','finalize'],'separate ROOT-issued operation authorization')
    digest(authorization['operation_nonce']);identity_actor(authorization['actor']);utc(authorization['utc'])
    fresh=inventory(context['inventory_sha256']);need(exact(fresh,context),'current helper bytes changed during prerequisite authentication')
    return d,body,authorization,counts

def preflight(disposition_pin,context,closed=False):
    gate=status_gate(allow_closed=closed);need(gate['action']==('CLOSED_RECONCILE_ONLY' if closed else 'ELIGIBLE'),'selected PR remains exactly eligible')
    d,body,authorization,counts=prerequisites(disposition_pin,context)
    checked=originals();parent=remote_main();need(parent==gate['pr']['currentBaseRefOid'],'fresh live MAIN pointer matches actual remote')
    source=source_gate(parent);native=native_pins(parent)
    after=status_gate(allow_closed=closed);need(exact(after['pr'],gate['pr']) and exact(after['queue_blob'],gate['queue_blob']) and exact(after['changed_paths'],gate['changed_paths']) and after['queue_row']==gate['queue_row'],'entire original/source/family eligibility bracket')
    need(remote_main()==parent,'main advanced within authority bracket')
    return {'gate':after,'source':source,'native':native,'originals':checked,'families':counts},d,body,authorization

def package_approval(expected,disposition_pin,context,body,authorization):
    digest(expected);raw=read(A/'CLOSURE_PACKAGE_APPROVAL.json');need(sha(raw)==expected,'separate external current closure-package approval')
    doc=strict(raw);required={'schema','utc','root_issued','pr','problem_id','original_pr_head','decision_sha256','operations_inventory_sha256','closure_comment_sha256','review_manifest','root_authentication','reviewer_agent_id','status'}
    need(type(doc) is dict and set(doc)==required and doc['schema']=='pr967-root-closure-package-approval-v1' and doc['root_issued'] is True and type(doc['pr']) is int and doc['pr']==PR and doc['problem_id']==KEY and doc['original_pr_head']==HEAD and doc['decision_sha256']==disposition_pin and doc['operations_inventory_sha256']==context['inventory_sha256'] and doc['closure_comment_sha256']==sha(body.encode()) and doc['status']=='PASS_ENTIRE_CURRENT_CLOSURE_PACKAGE' and type(doc['reviewer_agent_id']) is str and doc['reviewer_agent_id'].strip(),'actual current entire-closure-package approval, not a specialized science-family review')
    refs={}
    for field in ('review_manifest','root_authentication'):
        item=doc[field];need(type(item) is dict and set(item)=={'path','bytes','sha256'} and safe(item['path']) and item['path'].startswith(A.relative_to(ROOT).as_posix()+'/'),'approval root/review reference')
        refs[field]=strict(read(ROOT/item['path'],expected={k:item[k] for k in ('bytes','sha256')}))
    manifest=refs['review_manifest'];records=manifest.get('files');allowed=manifest.get('explicit_public_allowlist')
    mandatory={'RESULT.json','AUTHENTICATION_START.json','AUTHENTICATION_END.json','FULL_AUDIT.md','RESEARCH_LOG.md'}
    need(type(records) is dict and mandatory<=set(records) and type(allowed) is list and all(type(x) is str for x in allowed) and len(allowed)==len(set(allowed)) and set(allowed)==set(records) and 'MANIFEST.json' not in records,'entire sealed closure review allowlist')
    base=(ROOT/doc['review_manifest']['path']).parent
    captured={name:read(base/name,expected=value) for name,value in records.items() if safe(name)}
    need(len(captured)==len(records),'safe entire closure review paths')
    result=strict(captured['RESULT.json']);need(type(result) is dict and result.get('pr')==PR and type(result.get('pr')) is int and result.get('problem_id')==KEY and result.get('original_pr_head')==HEAD and result.get('operations_inventory_sha256')==context['inventory_sha256'] and result.get('decision_sha256')==disposition_pin and result.get('closure_comment_sha256')==sha(body.encode()) and result.get('reviewer_agent_id')==doc['reviewer_agent_id'] and result.get('clean_context') is True and result.get('entire_closure_package_review') is True and result.get('full_reproducer_completed') is True and result.get('required_issues')==[] and result.get('optional_issues')==[] and result.get('clean_for_closure') is True,'fresh entire current closure review RESULT')
    start,end=utc(result.get('started_utc')),utc(result.get('completed_utc'));need(start<end<=utc(doc['utc']),'fresh closure reviewer actual chronology')
    expected_pins={'decision_sha256':disposition_pin,'operations_inventory_sha256':context['inventory_sha256'],'closure_comment_sha256':sha(body.encode())}
    for name in ('AUTHENTICATION_START.json','AUTHENTICATION_END.json'):
        auth=strict(captured[name]);need(type(auth) is dict and auth.get('status')=='PASS' and all(auth.get(k)==v for k,v in expected_pins.items()) and auth.get('all26_original_bytes_and_modes_authenticated') is True and auth.get('all_six_family_members_authenticated') is True and auth.get('both_entire_helpers_authenticated') is True,'actual complete closure review authentication bracket')
        need(start<=utc(auth.get('utc'))<=end,'closure review authentication time bracket')
    root=refs['root_authentication'];need(type(root) is dict and root.get('before_substantive_intake') is True and root.get('all_members_authenticated') is True and root.get('external_manifest_sha256')==doc['review_manifest']['sha256'] and utc(end)<=utc(root.get('utc'))<=utc(doc['utc']),'root before-intake authentication of the sealed closure review')
    return doc

def authority(disposition_pin,context,body,authorization,approval_pin=None):
    return {'pr':PR,'problem_id':KEY,'original_pr_head':HEAD,'decision_sha256':disposition_pin,'operations_inventory_sha256':context['inventory_sha256'],'closure_comment_sha256':sha(body.encode()),'operation_nonce':authorization['operation_nonce'],'authorization_issued_utc':authorization['utc'],'closure_package_approval_sha256':approval_pin,'actor':authorization['actor']}

@contextmanager
def operation_lock(bound):
    runtime();fd=directory(W)
    try:
        handle=os.open('OPERATION.lock',os.O_RDWR|os.O_CREAT|os.O_NOFOLLOW|os.O_NONBLOCK,0o600,dir_fd=fd)
        try:
            info=os.fstat(handle);need(stat.S_ISREG(info.st_mode) and info.st_nlink==1 and info.st_uid==os.getuid() and stat.S_IMODE(info.st_mode)==0o600,'root-authorized operation lock owner/mode')
            fcntl.flock(handle,fcntl.LOCK_EX|fcntl.LOCK_NB)
            current=os.read(handle,MAX_JSON+1);need(len(current)<=MAX_JSON,'lock size')
            if current:need(exact(strict(current),bound),'operation lock foreign authority; no adoption')
            else:
                raw=enc(bound);need(os.write(handle,raw)==len(raw),'lock short write');os.fsync(handle);os.fsync(fd)
            yield
        finally:os.close(handle)
    finally:os.close(fd)

def bound_file(name,bound):
    value=load(W/name);need(type(value) is dict and exact(value.get('authority'),bound),'foreign or malformed '+name);return value

def current_actor(bound):
    who,stamp=actor();need(exact(who,bound['actor']),'current authenticated actor differs from ROOT authorization');return stamp

def comments():
    values=[];pages=[];ids=set();last=None
    for page in range(1,101):
        data,stamp=api('GET',f'repos/{REPO}/issues/{PR}/comments?per_page=100&page={page}');need(type(data) is list and len(data)<=100,'bounded full comment page')
        for item in data:
            fields(item,{'id':int,'body':str,'user':dict,'created_at':str,'updated_at':str,'html_url':str,'issue_url':str},'actual comment')
            need(item['id']>0 and item['id'] not in ids,'unique paginated comment IDs');ids.add(item['id']);values.append(item)
        pages.append({'page':page,'count':len(data),'sha256':sha(enc(data))});last=stamp
        if len(data)<100:return values,pages,last
    raise RuntimeError('Full comment pagination bound exceeded; no action')

def comment_identity(comment,bound,intent,server_stamp):
    need(type(comment) is dict and comment.get('body')==intent['body'] and comment['body'].count(MARKER)==1,'actual exact posted comment/marker')
    need(exact(identity_actor(comment.get('user')),bound['actor']),'posted comment actual actor')
    cid=comment.get('id');need(type(cid) is int and cid>0 and cid not in intent['before_comment_ids'],'comment is new after exclusive known intent')
    need(comment.get('html_url')==f'https://github.com/{REPO}/pull/{PR}#issuecomment-{cid}' and comment.get('issue_url')==f'https://api.github.com/repos/{REPO}/issues/{PR}','posted comment target URL')
    need(utc(intent['server_not_before_utc'])<=utc(comment['created_at'])<=utc(comment['updated_at'])<=utc(server_stamp),'provable server timestamp for posted comment')
    return {'id':cid,'url':comment['html_url'],'body_sha256':sha(comment['body'].encode()),'actor':identity_actor(comment['user']),'created_utc':comment['created_at'],'updated_utc':comment['updated_at']}

def reconcile_comment(bound,body,write=False):
    intent=bound_file('COMMENT_POST_INTENT.json',bound)
    need(set(intent)=={'schema','utc','authority','body','before_comment_ids','server_not_before_utc','blind_retry_permitted'} and intent['schema']=='pr967-comment-post-intent-v1' and intent['body']==body and intent['blind_retry_permitted'] is False and type(intent['before_comment_ids']) is list and all(type(x) is int for x in intent['before_comment_ids']) and len(intent['before_comment_ids'])==len(set(intent['before_comment_ids'])),'exact exclusive comment POST intent')
    need(utc(bound['authorization_issued_utc'])<=utc(intent['utc']) and utc(bound['authorization_issued_utc'])<=utc(intent['server_not_before_utc']),'intent cannot predate reviewed ROOT authorization')
    values,pages,stamp=comments();matches=[x for x in values if x['body']==body or MARKER in x['body']]
    need(len(matches)==1,'uncertain comment: require one exact actual body/marker across all pages; never repost')
    identified=comment_identity(matches[0],bound,intent,stamp)
    readback,stamp=api('GET',f'repos/{REPO}/issues/comments/{identified["id"]}')
    need(exact(comment_identity(readback,bound,intent,stamp),identified),'posted comment exact individual readback')
    result={'schema':'pr967-comment-receipt-v1','authority':bound,'post_intent_sha256':sha(read(W/'COMMENT_POST_INTENT.json')),'comment':identified,'full_paginated_unique_match':True}
    if exists(W/'COMMENT_RECEIPT.json'):need(exact(load(W/'COMMENT_RECEIPT.json'),result),'canonical comment receipt changed or foreign')
    elif write:save(W/'COMMENT_RECEIPT.json',result)
    return result

def closure_events():
    values=[];ids=set()
    for page in range(1,101):
        data,stamp=api('GET',f'repos/{REPO}/issues/{PR}/events?per_page=100&page={page}');need(type(data) is list and len(data)<=100,'bounded complete issue event page')
        for event in data:
            fields(event,{'id':int,'event':str,'created_at':str},'issue event');need(event['id']>0 and event['id'] not in ids,'unique issue event IDs');ids.add(event['id']);values.append(event)
        if len(data)<100:return values,stamp
    raise RuntimeError('Issue event pagination bound exceeded')

def closure_receipt(bound,body,context,write=False):
    intent=bound_file('CLOSE_PATCH_INTENT.json',bound)
    need(set(intent)=={'schema','utc','authority','server_not_before_utc','comment_receipt_sha256','gate','native_before','before_event_ids','blind_retry_permitted'} and intent['schema']=='pr967-close-patch-intent-v1' and intent['blind_retry_permitted'] is False,'exact close PATCH intent')
    need(utc(bound['authorization_issued_utc'])<=utc(intent['utc']) and utc(bound['authorization_issued_utc'])<=utc(intent['server_not_before_utc']),'close intent cannot predate ROOT authorization')
    need(exists(W/'COMMENT_RECEIPT.json') and sha(read(W/'COMMENT_RECEIPT.json'))==intent['comment_receipt_sha256'],'close intent exact canonical comment authority')
    comment=reconcile_comment(bound,body)
    gate=status_gate(allow_closed=True);need(gate['action']=='CLOSED_RECONCILE_ONLY' and gate['pr']['mergedAt'] is None,'actual CLOSED unmerged immutable HEAD')
    need(intent['gate']['action']=='ELIGIBLE' and intent['gate']['pr']['headRefOid']==HEAD and intent['gate']['pr']['state']=='OPEN','saved actual still-eligible close intent')
    events,stamp=closure_events();matched=[x for x in events if x['event']=='closed' and x['id'] not in intent['before_event_ids'] and utc(x['created_at'])>=utc(intent['server_not_before_utc'])]
    need(len(matched)==1 and matched[0]['created_at']==gate['pr']['closedAt'] and utc(matched[0]['created_at'])<=utc(stamp) and exact(identity_actor(matched[0].get('actor')),bound['actor']),'unique actual closure event by authorized actor after known PATCH intent')
    parent=remote_main();need(parent==gate['pr']['currentBaseRefOid'],'actual closed gate live MAIN')
    need(exact(native_pins(parent),intent['native_before']),'native QUEUE/state/history actual complete bytes changed; reconcile foreign changes')
    original=originals();source_gate(parent)
    fresh=inventory(context['inventory_sha256']);need(exact(fresh,context),'helpers changed at closure receipt boundary')
    result={'schema':'pr967-closure-receipt-v1','authority':bound,'outcome':OUTCOME,'comment_receipt_sha256':sha(read(W/'COMMENT_RECEIPT.json')),'close_intent_sha256':sha(read(W/'CLOSE_PATCH_INTENT.json')),'comment':comment['comment'],'closed_pr':gate['pr'],'closure_event':{'id':matched[0]['id'],'created_utc':matched[0]['created_at'],'actor':bound['actor']},'native_before_and_after':intent['native_before'],'original_files':26,'original_bytes':147731,'original_records_sha256':RECORDS_SHA,'original_declared_turns':'1/5','historical_native_turn_count':'UNKNOWN','new_author_proof_responses':0,'merge_performed':False,'preprint_DOI_sheet_native_mutations':False,'API_write_protocol':'fresh bounded complete gate, one request, exact post-readback; GitHub offers no atomic head/base/draft compare-and-close','observed_race_concealed':False}
    if exists(W/'CLOSURE_RECEIPT.json'):need(exact(load(W/'CLOSURE_RECEIPT.json'),result),'foreign/conflicting canonical closure receipt')
    elif write:save(W/'CLOSURE_RECEIPT.json',result)
    return result

def close_operation(args,context):
    first=status_gate()
    recovering=first['pr']['state']=='CLOSED' and first['pr']['mergedAt'] is None and exists(W/'CLOSE_PATCH_INTENT.json')
    if first['action']!='ELIGIBLE' and not recovering:
        print(json.dumps(first,sort_keys=True));return
    check,d,body,authorization=preflight(args.disposition_sha256,context,closed=recovering)
    approval_pin=getattr(args,'approval_sha256',None)
    if args.execute:package_approval(approval_pin,args.disposition_sha256,context,body,authorization)
    bound=authority(args.disposition_sha256,context,body,authorization,approval_pin)
    if not args.execute:
        result={'read_only':True,'status':'PASS_PREREQUISITES','authority':bound,'eligibility':check['gate'],'original_files':len(check['originals']),'family_counts':check['families'],'service_mutations':0,'acceptance_authority':False}
        if recovering:result['reconciled_closure']=closure_receipt(bound,body,context)
        print(json.dumps(result,sort_keys=True));return
    with operation_lock(bound):
        current_actor(bound)
        if recovering:
            result=closure_receipt(bound,body,context,write=True);print(json.dumps(result,sort_keys=True));return
        need(not exists(W/'CLOSURE_RECEIPT.json'),'preexisting receipt without actual closed state; no authority adoption')
        if exists(W/'COMMENT_POST_INTENT.json'):reconcile_comment(bound,body,write=True)
        else:
            need(not exists(W/'COMMENT_RECEIPT.json') and not exists(W/'CLOSE_PATCH_INTENT.json'),'orphan receipt/close intent; reconcile without mutation')
            fresh,_,freshbody,auth=preflight(args.disposition_sha256,context);need(freshbody==body and exact(auth,authorization),'root authority drift before comment')
            values,_,_=comments();need(not any(x['body']==body or MARKER in x['body'] for x in values),'preexisting foreign/unowned matching comment; never adopt')
            stamp=current_actor(bound)
            boundary=status_gate();need(boundary['action']=='ELIGIBLE' and exact(boundary['pr'],fresh['gate']['pr']) and exact(boundary['queue_blob'],fresh['gate']['queue_blob']) and boundary['queue_row']==fresh['gate']['queue_row'] and exact(boundary['changed_paths'],fresh['gate']['changed_paths']),'immediate complete pre-POST eligibility')
            need(sha(read(A/'PRIORITY_DISPOSITION.json'))==args.disposition_sha256 and sha(read(A/'CLOSURE_COMMENT_DRAFT.md'))==sha(body.encode()) and exact(inventory(context['inventory_sha256']),context),'canonical decision/comment/helper pins at pre-POST boundary')
            save(W/'COMMENT_POST_INTENT.json',{'schema':'pr967-comment-post-intent-v1','utc':now(),'authority':bound,'body':body,'before_comment_ids':[x['id'] for x in values],'server_not_before_utc':stamp,'blind_retry_permitted':False})
            # An exception or lost response leaves the durable intent. Subsequent
            # invocations perform full-paginated exact-ID/body/actor GET recovery.
            api('POST',f'repos/{REPO}/issues/{PR}/comments',{'body':body})
            reconcile_comment(bound,body,write=True)
        need(not exists(W/'CLOSE_PATCH_INTENT.json'),'uncertain existing close PATCH intent while OPEN: never repeat')
        fresh,_,freshbody,auth=preflight(args.disposition_sha256,context);need(freshbody==body and exact(auth,authorization),'root authority drift before close')
        comment=reconcile_comment(bound,body);events,_=closure_events();stamp=current_actor(bound)
        # Final live identity check after all potentially slow GETs, immediately
        # before saving intent and issuing the one exact-target PATCH.
        boundary=status_gate();need(boundary['action']=='ELIGIBLE' and exact(boundary['pr'],fresh['gate']['pr']),'still eligible immutable target at close boundary')
        need(sha(read(A/'PRIORITY_DISPOSITION.json'))==args.disposition_sha256 and sha(read(A/'CLOSURE_COMMENT_DRAFT.md'))==sha(body.encode()) and exact(inventory(context['inventory_sha256']),context),'canonical decision/comment/helper pins at pre-PATCH boundary')
        save(W/'CLOSE_PATCH_INTENT.json',{'schema':'pr967-close-patch-intent-v1','utc':now(),'authority':bound,'server_not_before_utc':stamp,'comment_receipt_sha256':sha(read(W/'COMMENT_RECEIPT.json')),'gate':boundary,'native_before':fresh['native'],'before_event_ids':[x['id'] for x in events],'blind_retry_permitted':False})
        api('PATCH',f'repos/{REPO}/pulls/{PR}',{'state':'closed'})
        result=closure_receipt(bound,body,context,write=True);print(json.dumps(result,sort_keys=True))


def scan_next():
    skipped=[]
    for number in range(PR+1,1001):
        gate=status_gate(number,key=None,expected_head=None)
        if gate['action']=='ELIGIBLE':return {'schema':'pr967-ascending-status-gate-v1','range':[968,1000],'skipped':skipped,'next_eligible':gate,'end_of_range':False,'math_source_read':False,'whole_goal_complete':False,'two_complete_900_1000_resweeps_still_required':True}
        skipped.append(gate)
    return {'schema':'pr967-ascending-status-gate-v1','range':[968,1000],'skipped':skipped,'next_eligible':None,'end_of_range':True,'math_source_read':False,'whole_goal_complete':False,'two_complete_900_1000_resweeps_still_required':True}

def local_record(bound,receipt,disposition):
    return {'pr':PR,'problem_id':KEY,'outcome':OUTCOME,'original_pr_head':HEAD,'decision_sha256':bound['decision_sha256'],'operations_inventory_sha256':bound['operations_inventory_sha256'],'closed_at':receipt['closed_pr']['closedAt'],'closure_comment_url':receipt['comment']['url'],'closure_comment_id':receipt['comment']['id'],'closure_receipt_sha256':sha(read(W/'CLOSURE_RECEIPT.json')),'original_declared_turns':'1/5','historical_native_turn_count':'UNKNOWN','new_author_proof_responses':0,'original_files_unchanged':26,'original_bytes':147731,'reason':'mathematically_correct_rediscovery','strict_historical_linked_body_hash_available':disposition['scope']['strict_historical_linked_body_hash_available'],'no_ultimate_discovery_or_misconduct_adjudication':True,'merge_commit':None,'doi':None,'tracker_range':None,'native_queue_or_state_mutated':False}

def proposed_local(raws,record,scan):
    state=strict(raws['state']);items=strict(raws['inventory'])
    need(type(state) is dict and type(items) is list and all(type(x) is dict and type(x.get('number')) is int for x in items),'local state/inventory schema')
    ids=[x['number'] for x in items];need(len(ids)==len(set(ids)) and ids.count(PR)==1,'unique inventory identities/selected PR')
    index=ids.index(PR);item=items[index];need(item.get('headRefOid')==HEAD and item.get('baseRefName')=='main' and item.get('url')==f'https://github.com/{REPO}/pull/{PR}','local target inventory exact head/main/URL')
    need(type(item.get('entries')) is list and len(item['entries'])==1 and str(item['entries'][0].get('id'))==KEY,'local target inventory exact one problem')
    for name in ('eligible_prs','completed_prs','published_prs'):
        need(type(state.get(name)) is list and all(type(x) is int for x in state[name]) and len(state[name])==len(set(state[name])),'unique typed local '+name)
    rows=state.get('completed_results');need(type(rows) is list and all(type(x) is dict and type(x.get('pr')) is int and type(x.get('outcome')) is str for x in rows),'local completed result schema')
    need(len(rows)==len({x['pr'] for x in rows}) and set(state['completed_prs'])=={x['pr'] for x in rows},'consistent completed results')
    need(set(state['published_prs'])=={x['pr'] for x in rows if x['outcome']=='accepted_merged_preprint_published'},'consistent published results')
    active=state.get('active_pr');need(active is None or type(active) is int,'typed active PR')
    old=[x for x in rows if x['pr']==PR]
    if old:need(exact(old[0],record),'conflicting completed priority record')
    else:need(active in (PR,None) or active>PR,'another earlier active target; preserve foreign state')
    need(item.get('disposition') in ('pending_audit','claimed_solved',OUTCOME),'conflicting inventory disposition')
    projection={'disposition':OUTCOME,'closure_comment_url':record['closure_comment_url'],'closure_receipt_sha256':record['closure_receipt_sha256'],'decision_sha256':record['decision_sha256']}
    for k,v in projection.items():
        if k in item and k!='disposition':need(exact(item[k],v),'conflicting inventory publication/closure field')
    desired=copy.deepcopy(state);inventory_after=copy.deepcopy(items);inventory_after[index].update(projection)
    if not old:
        completed=sorted([*rows,record],key=lambda x:x['pr'])
        desired.update(completed_results=completed,completed_prs=[x['pr'] for x in completed],published_prs=[x['pr'] for x in completed if x['outcome']=='accepted_merged_preprint_published'])
        if 'closed_prs' in desired:
            need(type(desired['closed_prs']) is list and all(type(x) is int for x in desired['closed_prs']) and set(desired['closed_prs'])=={x['pr'] for x in rows if x['outcome'].startswith('closed_')},'consistent existing closed list')
            desired['closed_prs']=[x['pr'] for x in completed if x['outcome'].startswith('closed_')]
    if active in (PR,None):
        nextgate=scan['next_eligible'];nextpr=nextgate['pr']['number'] if nextgate else None
        desired.update(active_pr=nextpr,active_problem_id=nextgate['problem_id'] if nextgate else None,next_pr=nextpr,phase='post_PR967_status_only_gate',active_pr_completion_estimate_percent=0,PR967_ascending_gate_end=scan['end_of_range'],two_complete_900_1000_final_resweeps_required=True)
        for name in ('active_original_head','original_candidate_turns','review_families','priority_families','publication_disposition','priority_status','full_package_reviews','active_candidate_revision','active_freeze_sha256','active_package_manifest_sha256'):
            desired.pop(name,None)
        if nextgate:desired['active_original_head']=nextgate['pr']['headRefOid']
    # Do not set whole-goal completion or infer eligibility denominator changes.
    result={'state':enc(desired),'inventory':enc(inventory_after)}
    token=b'PR967-PRIORITY-LOCAL-COMPLETION-V1 '
    marker={'schema':'pr967-local-priority-completion-v1','scope_completion_estimate_percent':100,'record_sha256':sha(enc(record)),'whole_goal_complete':False}
    addition=token+json.dumps(marker,sort_keys=True,separators=(',',':')).encode()+b'\n'
    for role in ('project_log','audit_log'):
        raw=raws[role];hits=[line for line in raw.splitlines(keepends=True) if b'PR967-PRIORITY-LOCAL-COMPLETION' in line]
        need(len(hits)<=1 and (not hits or hits[0]==addition),'unique canonical same-outcome log marker')
        result[role]=raw if hits else raw+(b'\n' if raw and not raw.endswith(b'\n') else b'')+addition
    return result

def local_paths():return {'state':P/'CURRENT_STATE.json','inventory':P/'inventory.json','project_log':P/'RESEARCH_LOG.md','audit_log':A/'RESEARCH_LOG.md'}

def atomic(path,raw,before):
    """Cooperating-lock byte check and replacement, not noncooperating-writer CAS."""
    fingerprint(before);need(pin(read(path))==before,'local foreign bytes changed; explicit reconciliation required')
    if pin(raw)==before:return
    fd=directory(Path(path).parent);temporary='.pr967-'+os.urandom(12).hex()+'.tmp'
    try:
        info=os.stat(Path(path).name,dir_fd=fd,follow_symlinks=False);need(stat.S_ISREG(info.st_mode) and info.st_nlink==1 and stat.S_IMODE(info.st_mode) in (0o600,0o644),'local single-link regular mode')
        handle=os.open(temporary,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,stat.S_IMODE(info.st_mode),dir_fd=fd)
        with os.fdopen(handle,'wb') as stream:
            os.fchmod(stream.fileno(),stat.S_IMODE(info.st_mode));need(stream.write(raw)==len(raw),'local temporary short write');stream.flush();os.fsync(stream.fileno())
        need(pin(read(path))==before,'local input changed before atomic rename')
        os.replace(temporary,Path(path).name,src_dir_fd=fd,dst_dir_fd=fd);temporary=None;os.fsync(fd)
        need(read(path)==raw,'local exact write readback')
    finally:
        if temporary is not None:
            try:os.unlink(temporary,dir_fd=fd)
            except FileNotFoundError:pass
        os.close(fd)

def staged_raw(path,raw):
    fd=directory(path.parent)
    try:
        handle=os.open(path.name,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600,dir_fd=fd)
        with os.fdopen(handle,'wb') as stream:need(stream.write(raw)==len(raw),'staging short write');stream.flush();os.fsync(stream.fileno())
        os.fsync(fd)
    finally:os.close(fd)

def reconcile_local(bound,record,scan,execute):
    paths=local_paths();intent_path=W/'LOCAL_FINALIZATION_INTENT.json'
    if exists(intent_path):
        plan=bound_file(intent_path.name,bound)
        need(set(plan)=={'schema','utc','authority','record','scan','files'} and plan['schema']=='pr967-local-finalization-intent-v1' and exact(plan['record'],record),'exact known local finalization authority')
        need(set(plan['files'])==set(paths),'all four local paths in intent')
        before={};after={}
        for role,item in plan['files'].items():
            need(type(item) is dict and set(item)=={'before','after'},'local staged fingerprints')
            before[role]=read(W/(role+'.before'),expected=item['before']);after[role]=read(W/(role+'.after'),expected=item['after'])
        need(exact(plan['scan'],scan),'saved next-target scan differs from current fresh scan; explicit local reconciliation required')
        need(exact(proposed_local(before,record,plan['scan']),after),'staged finalization differs from independently derived narrow update')
    else:
        before={role:read(path,cap=MAX_JSON) for role,path in paths.items()};after=proposed_local(before,record,scan)
        plan={'schema':'pr967-local-finalization-intent-v1','utc':now(),'authority':bound,'record':record,'scan':scan,'files':{role:{'before':pin(before[role]),'after':pin(after[role])} for role in paths}}
        if execute:
            # Orphan staging left before an intent is uncertain, never reused.
            need(not any(exists(W/(role+suffix)) for role in paths for suffix in ('.before','.after')),'orphan local staging requires reconciliation')
            for role in paths:staged_raw(W/(role+'.before'),before[role]);staged_raw(W/(role+'.after'),after[role])
            save(intent_path,plan)
    for role,path in paths.items():
        live=read(path,cap=MAX_JSON);need(live in (before[role],after[role]),'foreign local writer conflicts with pending plan: '+role)
    if not execute:return {'read_only':True,'local_plan':plan,'local_writes':0,'whole_goal_complete':False}
    for role in ('inventory','state','project_log','audit_log'):
        live=read(paths[role]);
        if live!=after[role]:atomic(paths[role],after[role],pin(before[role]))
    need(all(read(path)==after[role] for role,path in paths.items()),'all four finalization files exact complete readback')
    receipt={'schema':'pr967-local-finalization-receipt-v1','authority':bound,'intent_sha256':sha(read(intent_path)),'record':record,'after':{role:pin(raw) for role,raw in after.items()},'confirmed':True,'both_research_logs_confirmed':True,'whole_goal_complete':False,'two_complete_900_1000_final_resweeps_required':True,'local_write_limit':'cooperating operation lock and exact old-byte checks; rename is not a noncooperating-writer compare-and-swap'}
    if exists(W/'LOCAL_FINALIZATION_RECEIPT.json'):need(exact(load(W/'LOCAL_FINALIZATION_RECEIPT.json'),receipt),'conflicting local finalization receipt')
    else:save(W/'LOCAL_FINALIZATION_RECEIPT.json',receipt)
    return receipt

def finalize_operation(args,context):
    first=status_gate(allow_closed=True)
    if first['action']!='CLOSED_RECONCILE_ONLY':print(json.dumps({'read_only':not args.execute,'action':'NO_CONFIRMED_CLOSED_TARGET','gate':first},sort_keys=True));return
    need(exists(W/'CLOSE_PATCH_INTENT.json') and exists(W/'CLOSURE_RECEIPT.json'),'finalization requires known close intent and canonical actual closure receipt')
    check,d,body,authorization=preflight(args.disposition_sha256,context,closed=True)
    approval_pin=getattr(args,'approval_sha256',None)
    if args.execute:package_approval(approval_pin,args.disposition_sha256,context,body,authorization)
    bound=authority(args.disposition_sha256,context,body,authorization,approval_pin);current_actor(bound)
    actual=closure_receipt(bound,body,context);record=local_record(bound,actual,d)
    scan=scan_next()
    if not args.execute:print(json.dumps(reconcile_local(bound,record,scan,False),sort_keys=True));return
    with operation_lock(bound):
        current_actor(bound);preflight(args.disposition_sha256,context,closed=True);closure_receipt(bound,body,context)
        result=reconcile_local(bound,record,scan,True)
        print(json.dumps(result,sort_keys=True))

def operation(action,args,context):
    need(sys.flags.optimize==0,'authenticated worker always actual optimization0')
    need(git('symbolic-ref','--short','HEAD').strip()=='main','shared checkout remains main')
    {'close':close_operation,'finalize':finalize_operation}[action](args,context)

def entry(action):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--operations-sha256',required=True);parser.add_argument('--disposition-sha256',required=True);parser.add_argument('--execute',action='store_true');parser.add_argument('--approval-sha256')
    args=parser.parse_args();context=inventory(args.operations_sha256)
    bundle={'action':action,'args':vars(args),'inventory_sha256':context['inventory_sha256'],'inventory':context['inventory'],'captured':{k:base64.b64encode(v).decode() for k,v in context['captured'].items()}}
    bootstrap=('import argparse,base64,json,sys; b=json.loads(sys.stdin.buffer.read()); '
      'c={"inventory_sha256":b["inventory_sha256"],"inventory":b["inventory"],"captured":{k:base64.b64decode(v,validate=True) for k,v in b["captured"].items()}}; '
      'n={"__name__":"_pr967_authenticated_core_","__file__":sys.argv[1]}; '
      'exec(compile(c["captured"][sys.argv[2]],sys.argv[1],"exec",dont_inherit=True,optimize=0),n); '
      'n["operation"](b["action"],argparse.Namespace(**b["args"]),c)')
    result=subprocess.run([sys.executable,'-I','-S','-B','-c',bootstrap,str(P/'close_pr967.py'),(P/'close_pr967.py').relative_to(ROOT).as_posix()],cwd=ROOT,input=json.dumps(bundle).encode())
    raise SystemExit(result.returncode)

if __name__=='__main__':entry('close')
