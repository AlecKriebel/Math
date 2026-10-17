"""Independent offline PR212 custody proof; producer verifier never executed.
Only source AST, native metadata/bytes and hashes are interpreted. No submitted
script executes and no mathematical statement/claim is evaluated. No services,
Git, original lock, global views, provider or Root gate are touched.
"""
import ast,base64,copy,datetime,hashlib,json,math,os,re,stat
from pathlib import Path
HERE=Path(__file__).absolute().parent
CASE=HERE.parent
B=CASE/'native_custody_01'
PROGRAM=CASE.parents[1]
ORIGINAL='c697b4a5cc62f3b8836d8c37d82b71a1d1c53fb7'
CURRENT='99af7a27a711271bcd0b9e7ce90e374e4100ea6d'
PARENT='8431d4eb9b4fbb56cc82f5a4ac61514053c2958d'
ROOTS={ORIGINAL:'436c162cea349eb2d07041202d32fd27c00df926',CURRENT:'3dd6b7b24c6eef3306ba47d939c6d75a2d2308de'}
OWN='unsolved_math_prioritization/attempts/30005310'
OLD='draft_pr_descending_audit_20261002/audits/pr212_30005310'
QUEUE='unsolved_math_prioritization/QUEUE.md'
checks=[]
def need(v,message):
    if v is not True:raise RuntimeError(message)
def check(name,v):
    need(v,name);checks.append({'control':name,'outcome':'PASS'})
def reject(name,fn):
    try:fn()
    except (RuntimeError,ValueError,KeyError,TypeError,OSError) as error:checks.append({'control':name,'outcome':'REFUSED','reason':str(error)[:120]})
    else:raise AssertionError('Did not refuse '+name)
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def native(kind,b):return hashlib.sha1(kind.encode()+b' '+str(len(b)).encode()+b'\0'+b).hexdigest()
def enc(v):return (json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def exact(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return set(a)==set(b) and all(exact(a[k],b[k]) for k in a)
    if type(a) is list:return len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b))
    return a==b
def strict(raw):
    def pairs(rows):
        r={}
        for k,v in rows:need(k not in r,'DuplicateJSONkey');r[k]=v
        return r
    def finite(v):
        n=float(v);need(math.isfinite(n),'NonfiniteJSON');return n
    return json.loads(raw,object_pairs_hook=pairs,parse_float=finite,parse_constant=lambda _:need(False,'NonfiniteJSON'))
def safe_relative(s):
    need(type(s) is str and s and not s.startswith('/') and '\\' not in s and '\0' not in s and all(x not in ('','.','..') for x in s.split('/')),'Unsafe evidence relativepath')
    return s
def read(path,cap=16_000_000):
    need(path.is_absolute() and path.resolve()==path,'Canonical nofollow read')
    handles=[];leaf=None
    try:
        current=Path('/');parent=os.open(current,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW);handles.append((current,parent,os.fstat(parent)))
        for name in path.parent.parts[1:]:
            current=current/name;parent=os.open(name,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=parent);handles.append((current,parent,os.fstat(parent)))
        leaf=os.open(path.name,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=parent);before=os.fstat(leaf)
        need(stat.S_ISREG(before.st_mode) and stat.S_IMODE(before.st_mode)==0o444 and before.st_size<=cap,'Readonly bounded regular evidence')
        with os.fdopen(leaf,'rb',closefd=False) as f:raw=f.read(cap+1)
        attrs=lambda s:(s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
        need(attrs(before)==attrs(os.fstat(leaf))==attrs(path.lstat()) and len(raw)==before.st_size,'Evidence changed')
        for p,fd,initial in handles:
            a,b=os.fstat(fd),p.lstat();need(stat.S_ISDIR(a.st_mode) and stat.S_ISDIR(b.st_mode) and (a.st_dev,a.st_ino)==(b.st_dev,b.st_ino)==(initial.st_dev,initial.st_ino),'Evidence ancestor changed')
        return raw
    finally:
        if leaf is not None:os.close(leaf)
        for p,fd,initial in reversed(handles):os.close(fd)
def ref(row):
    need(type(row) is dict and set(row)=={'path','bytes','sha256'} and type(row['bytes']) is int and 0<=row['bytes']<=16_000_000,'Exact typed evidence ref')
    raw=read(B/safe_relative(row['path']));need(pin(raw)=={k:row[k] for k in ('bytes','sha256')},'Evidence ref pin differs');return raw
def oid(s):return type(s) is str and re.fullmatch('[a-f0-9]{40}',s) is not None
def tree(raw,expected):
    need(type(raw) is dict and raw.get('sha')==expected and raw.get('truncated') is False and type(raw.get('tree')) is list and len(raw['tree'])<=30000,'Complete bounded native tree')
    rows=[];names=set()
    for r in raw['tree']:
        name=r['path'];pair=(r['mode'],r['type'])
        need(type(name) is str and name and '/' not in name and '\0' not in name and name not in ('.','..') and name not in names and oid(r['sha']),'Immediate tree entry identity')
        name.encode();names.add(name)
        need(pair in (('040000','tree'),('100644','blob'),('100755','blob'),('120000','blob'),('160000','commit')),'Native mode/type pair')
        rows.append((name,r['mode'],r['type'],r['sha']))
    ordered=sorted(rows,key=lambda r:r[0].encode()+(b'/' if r[1]=='040000' else b''))
    need(rows==ordered,'Noncanonical tree order')
    body=b''.join((mode.lstrip('0')+' '+name).encode()+b'\0'+bytes.fromhex(sha) for name,mode,kind,sha in rows)
    need(native('tree',body)==expected,'Native tree SHA1 differs')
    return {name:(mode,kind,sha) for name,mode,kind,sha in rows}
def blob(value,expected):
    need(type(value) is dict and value.get('sha')==expected and value.get('encoding')=='base64' and type(value.get('size')) is int and 0<=value['size']<=8_000_000 and type(value.get('content')) is str,'Typed bounded native blob')
    body=base64.b64decode(''.join(value['content'].split()),validate=True)
    need(len(body)==value['size'] and native('blob',body)==expected,'Native full blob body differs');return body
def main():
    pmraw=read(B/'PUBLIC_MANIFEST.json');pm=strict(pmraw);psraw=read(B/'PUBLIC_SEAL.json');ps=strict(psraw)
    check('Assignedpublicmanifest exactpin',pin(pmraw)=={'bytes':4094,'sha256':'8e4e0f7c3178cb51504527f3c6278079c80f71baaa5cc74794234f5a82d23dd4'})
    check('Assignedpublicseal exactpin',pin(psraw)=={'bytes':391,'sha256':'cc534cc0ca1ab75f00b5e3862d98e2be3031b5d85a57c5accffc4e6219807f38'} and ps['manifest']=={'path':'PUBLIC_MANIFEST.json',**pin(pmraw)})
    public={};private={}
    for row in pm['files']:
        raw=ref(row);public[row['path']]=raw
        if row['path'].endswith('.json'):strict(raw)
    check('All23exact publicpositivepayloads253575B',len(public)==pm['file_count']==23 and sum(map(len,public.values()))==pm['total_bytes']==253575)
    privm=strict(public['PRIVATE_EVIDENCE_MANIFEST.json'])
    for row in privm['files']:
        raw=ref(row);need(row['path'] not in private,'Duplicateprivatepath');private[row['path']]=raw
        if row['path'].endswith('.json'):strict(raw)
    actual_private={str(p.relative_to(B)) for name in ('_private_native','_private_native_commits','_private_transport') for p in (B/name).rglob('*') if p.is_file()}
    check('All256privatepositivefiles2251393Bexactclosure',len(private)==privm['file_count']==256 and sum(map(len,private.values()))==privm['total_bytes']==2251393 and set(private)==actual_private)
    check('No rawprivatebody in23publicselection',all(not p.startswith('_private') for p in public) and pm['private_direct_bodies_included'] is False)
    summary=strict(public['FACTUAL_CUSTODY_SUMMARY.json']);source=strict(public['SOURCE_MANIFEST.json'])
    check('Fullcollector28821sourcepin exact',pin(public['collect_native_custody.py'])=={'bytes':28821,'sha256':'3be204467b52a2dd4e4afba6b36b97f16a00c78e84dee7536fbc233a0a1f7b52'})
    check('All3sourceclosure exact',len(source['files'])==3 and all(pin(public[r['path']])=={k:r[k] for k in ('bytes','sha256')} for r in source['files']))
    provenance=strict(public['SOURCE_PROVENANCE.json']);originraw=read(PROGRAM/provenance['primitive_origin']['path'])
    check('Pinnedprimitiveorigin exact',pin(originraw)=={k:provenance['primitive_origin'][k] for k in ('bytes','sha256')})
    newast=ast.parse(public['get_primitives.py']);oldast=ast.parse(originraw)
    for name in provenance['primitive_AST_identical_functions']:
        a=next(n for n in newast.body if isinstance(n,ast.FunctionDef) and n.name==name);b=next(n for n in oldast.body if isinstance(n,ast.FunctionDef) and n.name==name)
        check('InheritedprimitiveASTsame '+name,ast.dump(a,include_attributes=False)==ast.dump(b,include_attributes=False))
    collector_ast=ast.parse(public['collect_native_custody.py'])
    check('Collectortransport onlyboundedGET sourcecontext',"'--hostname','github.com','--method','GET','repos/AlecKriebel/Math/'+route" in public['collect_native_custody.py'].decode())
    acceptedraw=read(CASE/'ROOT_STATUS_INTAKE_ACCEPTANCE_01.json');accepted=strict(acceptedraw)
    intakeraw=read(PROGRAM/'ordered_intakes_after_PR211_20261017/PR212_PRESERVED_STATUS_INTAKE.json');intake=strict(intakeraw)
    check('ExactRootstatusacceptance pin',pin(acceptedraw)=={'bytes':1985,'sha256':'5a40df678183a6254efc47ffb2150ba05d29a040b174237a9cba9f22df5d8439'} and accepted['accepted'] is True and type(accepted['PR']) is int and accepted['PR']==212)
    check('ExactRootintake24331pin eligibleoriginal',pin(intakeraw)=={'bytes':24331,'sha256':'7372c92dea26f315f3f2718f77965fb2b757b4c163b44396634b4694d8430e7c'} and intake['eligible'] is True)
    index=strict(public['ACTUAL_TRANSPORT_INDEX.json']);responses={};PRs=[];native_routes=set();raw_total=0;transport_summary=[]
    for i,row in enumerate(index['records'],1):
        for key in ('response','receipt','stderr','intent'):ref(row[key])
        raw=private[row['response']['path']];err=private[row['stderr']['path']];value=strict(raw)
        rec=strict(private[row['receipt']['path']]);intent=strict(private[row['intent']['path']]);route=row['route']
        need(rec['method']=='GET' and rec['hostname']=='github.com' and rec['repository']=='AlecKriebel/Math' and type(rec['exit']) is int and rec['exit']==0 and rec['no_retry'] is True and rec['route']==route,'Actual transport receipt scope')
        need(all(rec[k]==row[rk] for k,rk in [('stdout','response'),('stderr','stderr'),('intent','intent')]),'Actual rawlinks differ')
        argv=['/opt/homebrew/Cellar/gh/2.85.0/bin/gh','api','--hostname','github.com','--method','GET','repos/AlecKriebel/Math/'+route]
        need(intent['argv']==argv and intent['method']=='GET' and intent['hostname']=='github.com' and intent['repository']=='AlecKriebel/Math' and intent['route']==route and type(intent['automatic_retries']) is int and intent['automatic_retries']==0,'Explicit request provenance')
        need(route in ('pulls/212','pulls/212/commits?per_page=100&page=1') or re.fullmatch(r'git/(commits|trees|blobs)/[a-f0-9]{40}',route) is not None,'Bounded native/PR route')
        if route.startswith('git/'):
            need(type(value) is dict and value.get('sha')==route.rsplit('/',1)[1],'Routednativeidentity');native_routes.add(route)
        if route in responses:need(exact(responses[route],value) or route=='pulls/212','RepeatedimmutableGETdiffers')
        else:responses[route]=value
        if route=='pulls/212':PRs.append(value)
        raw_total+=len(raw)+len(err);transport_summary.append({'number':i,'route':route,'response_pin':pin(raw),'receipt_pin':pin(private[row['receipt']['path']])})
        check('ActualGET%02d fullraw/route/host/intent/receipt'%i,True)
    check('Exactly49complete actualGET records andaggregatebytes',len(index['records'])==index['GET_attempts']==summary['GET_attempts']==49 and raw_total==index['raw_bytes'] and raw_total<=64_000_000)
    need(len(PRs)==2,'Start/end actualPR count')
    prkeys=('number','title','state','draft','merged','commits','merge_commit_sha','merged_at','created_at','updated_at','body')
    check('Actualstart/endPRselectedmetadataandopaquebody stable',all(exact(PRs[0].get(k),PRs[1].get(k)) for k in prkeys))
    for pr in PRs:
        need(type(pr['number']) is int and pr['number']==212 and pr['state']=='open' and pr['draft'] is True and pr['merged'] is False and pr['head']['sha']==CURRENT and pr['head']['ref']=='math/30005310-colored-threshold-wip' and pr['base']['ref']=='main' and type(pr['commits']) is int and pr['commits']==3,'ExactcurrentopenDraftidentity')
        need(all(exact(pr.get(k),intake['actual_PR'].get(k)) for k in prkeys if k!='body'),'Currentmetadata versusacceptedintake')
    check('FreshendPR_HEAD99acceptedopenDraft noMainleaseclaim',summary['fresh_end_PR_HEAD']==CURRENT and summary['fresh_start_end_PR_metadata_identical'] is True)
    history=responses['pulls/212/commits?per_page=100&page=1']
    check('Complete3commitPRhistory exactorderedchain',type(history) is list and [r['sha'] for r in history]==[PARENT,ORIGINAL,CURRENT] and len(history)==PRs[-1]['commits']<100)
    commits=[]
    for sha in (PARENT,ORIGINAL,CURRENT):
        raw=private['_private_native_commits/'+sha+'.raw'];j=responses['git/commits/'+sha]
        need(native('commit',raw)==sha,'Native rawcommit SHA1')
        head,message=raw.split(b'\n\n',1);lines=head.decode().splitlines()
        need(lines[0]=='tree '+j['tree']['sha'],'Native commit tree')
        parents=[line[7:] for line in lines if line.startswith('parent ')]
        need(parents==[r['sha'] for r in j['parents']],'Native ordered parents')
        expected_prefix=['tree '+j['tree']['sha']]+['parent '+x for x in parents]
        need(lines[:len(expected_prefix)]==expected_prefix and len(lines)==len(expected_prefix)+2,'Supportedcanonicalunsignedheaders')
        for label in ('author','committer'):
            line=next(x for x in lines if x.startswith(label+' '));match=re.fullmatch(label+r' (.*) <([^<>]*)> (-?[0-9]+) ([+-][0-9]{4})',line)
            need(match is not None,'Canonical identity header')
            name,email,seconds,offset=match.groups();meta=j[label]
            need(name==meta['name'] and email==meta['email'] and offset=='-0700','Exact rawheader identity/offset')
            dt=datetime.datetime.fromisoformat(meta['date'].replace('Z','+00:00'))
            need(dt.tzinfo is not None and dt.microsecond==0 and int(dt.timestamp())==int(seconds),'Rawheaderseconds versusUTCmetadata')
        need(message.decode()==j['message'],'Exact rawmessage noLFnormalizationneeded')
        if sha in ROOTS:need(j['tree']['sha']==ROOTS[sha] and parents==([PARENT] if sha==ORIGINAL else [ORIGINAL]),'Given original/current root/parent')
        commits.append({'sha':sha,'tree':j['tree']['sha'],'parents':parents,'raw_pin':pin(raw),'author_offset':'-0700','committer_offset':'-0700'})
        check('Independent canonical3commit rawproof '+sha,True)
    trees={}
    for route,value in responses.items():
        if route.startswith('git/trees/'):
            sha=route.rsplit('/',1)[1];trees[sha]=tree(value,sha);check('Canonicalrawimmediatetree '+sha,True)
    authoredtrees=strict(public['AUTHENTICATED_NATIVE_TREES.json'])
    check('Authoredtreecache identicaltoretainedrawnativetrees',exact(authoredtrees,{sha:{n:list(v) for n,v in rows.items()} for sha,rows in trees.items()}))
    def lookup(root,path):
        parts=path.split('/');need(len(parts)<=65,'Depthbound');oid_=root
        for i,name in enumerate(parts):
            row=trees[oid_].get(name)
            if row is None:return None
            if i==len(parts)-1:return row
            if row[:2]!=('040000','tree'):return None
            oid_=row[2]
    changed=[];dirsadd=set();dirsdel=set();equalfrontier=[]
    def diff(a,b,prefix='',depth=0):
        need(depth<=64,'Diffdepth')
        if a==b:
            if a:equalfrontier.append({'path':prefix.rstrip('/'),'sha':a})
            return
        left=trees[a] if a else {};right=trees[b] if b else {}
        for name in sorted(set(left)|set(right)):
            x,y=left.get(name),right.get(name);path=prefix+name
            if x==y:
                equalfrontier.append({'path':path,'tuple':list(x) if x else None});continue
            xt=x is not None and x[:2]==('040000','tree');yt=y is not None and y[:2]==('040000','tree')
            if xt and yt:diff(x[2],y[2],path+'/',depth+1)
            else:
                if xt:dirsdel.add(path);diff(x[2],None,path+'/',depth+1)
                if yt:dirsadd.add(path);diff(None,y[2],path+'/',depth+1)
                if (x is not None and not xt) or (y is not None and not yt):changed.append({'path':path,'before':list(x) if x else None,'after':list(y) if y else None})
    diff(ROOTS[ORIGINAL],ROOTS[CURRENT]);changed.sort(key=lambda r:r['path'])
    scope=strict(public['FULL_NATIVE_CHANGE_SCOPE.json'])
    for r in changed:r['classification']='own_attempt' if r['path'].startswith(OWN+'/') else 'QUEUE' if r['path']==QUEUE else 'FOREIGN'
    check('Full40leaves39ownplusQUEUEforeign0 matchesrawproof',exact(changed,scope['changed_leaves']) and len(changed)==40 and sum(r['classification']=='own_attempt' for r in changed)==39 and sum(r['classification']=='QUEUE' for r in changed)==1)
    check('Complete changeddirectorysets exact',sorted(dirsadd)==scope['added_directories'] and sorted(dirsdel)==scope['deleted_directories'])
    additions=sum(r['before'] is None for r in changed);deletions=sum(r['after'] is None for r in changed);modifications=len(changed)-additions-deletions
    check('Exact22added7deleted11modifiedleaves', (additions,deletions,modifications)==(22,7,11))
    def inventory(root,path):
        e=lookup(root,path)
        if e is None:return []
        need(e[:2]==('040000','tree'),'Inventoryroot tree');out=[]
        def walk(sha,p,depth):
            need(depth<=64,'Inventorydepth')
            for n,v in sorted(trees[sha].items()):
                if v[:2]==('040000','tree'):walk(v[2],p+'/'+n,depth+1)
                else:out.append({'path':p+'/'+n,'mode':v[0],'type':v[1],'sha':v[2]})
        walk(e[2],path,len(path.split('/')));return out
    roles={};bodymeta=[]
    for label,sha,count,size,ownsha in [('original',ORIGINAL,20,55337,'e292a543b6d6ed16105a02d565015deca75a823a'),('current',CURRENT,35,106594,'ea0c353ee68bd732457f7f44ca237439adf28ae0')]:
        role=strict(public[label.upper()+'_BODY_CUSTODY.json']);roles[label]=role
        inv=inventory(ROOTS[sha],OWN)
        need(exact(inv,role['leaves']) and lookup(ROOTS[sha],OWN)==('040000','tree',ownsha),'Complete native owninventory')
        need(len(role['files'])==role['file_count']==count and role['decoded_bytes']==size,'Role typedcount/bytes')
        need([{k:r[k] for k in ('path','mode','type','sha')} for r in role['files']]==inv,'Roleexactbodyset')
        for row in role['files']:
            body=private[row['private_copy']];rawblob=blob(responses['git/blobs/'+row['sha']],row['sha'])
            need(body==rawblob and pin(body)=={k:row[k] for k in ('bytes','sha256')} and lookup(ROOTS[sha],row['path'])==(row['mode'],row['type'],row['sha']),'Full rolebody nativepath SHA1/SHA256')
            bodymeta.append({'role':label,'path':row['path'],**pin(body),'mode':row['mode'],'type':row['type'],'oid':row['sha']})
            check('Full'+label+'body '+row['path'],True)
        check(label+'completebodyrole total',sum(r['bytes'] for r in role['files'])==size)
        oldrole=strict(public[label.upper()+'_OLD_OWNED_AUDIT_CUSTODY.json'])
        check(label+'old descendingaudit absent',lookup(ROOTS[sha],OLD) is None and oldrole['absent'] is True and oldrole['file_count']==0)
    history=strict(public['ORIGINAL_HISTORY_COPY_ASSOCIATIONS.json']);orig_by={r['path']:r for r in roles['original']['files']};cur_by={r['path']:r for r in roles['current']['files']}
    check('Exact20completehistoricalcopy associations',len(history['matches'])==history['matched_original_files']==history['original_total']==20 and history['all_original_files_have_exact_current_history_copies'] is True and not history['unmatched_original_paths'])
    for r in history['matches']:
        old,cur=orig_by[r['original_path']],cur_by[r['current_history_path']]
        need(cur['path']==OWN+'/original_submission/'+old['path'][len(OWN)+1:] and exact({k:old[k] for k in ('mode','type','sha','bytes','sha256')},{k:cur[k] for k in ('mode','type','sha','bytes','sha256')}) and private[old['private_copy']]==private[cur['private_copy']],'Exact20historicalbodycopy')
    check('All20historycopies exactpathmodeOIDandfullbytes',True)
    queues=strict(public['QUEUE_CUSTODY_COMPARISON.json']);nonown={};queueout={}
    for label,sha,status in [('original',ORIGINAL,'claimed_solved'),('current',CURRENT,'already_solved')]:
        r=queues[label];body=private[r['private_QUEUE']]
        need(lookup(ROOTS[sha],QUEUE)==(r['mode'],r['type'],r['sha']) and blob(responses['git/blobs/'+r['sha']],r['sha'])==body and pin(body)=={k:r[k] for k in ('bytes','sha256')},'WholeQUEUEnativebody')
        lines=body.splitlines(keepends=True);found=[]
        for i,line in enumerate(lines):
            fields=line.decode().split('|')
            if len(fields)==14 and fields[2].strip().split(' / ')[0]=='30005310':found.append((i,line,fields))
        need(len(found)==1,'UniqueownQUEUErow');i,line,fields=found[0]
        need(pin(line)==r['row_pin'] and fields[8].strip()==r['status']==status and fields[9].strip()==r['effort']=='1/5','Exactstatus/effort/rowpin')
        nonown[label]=b''.join(lines[:i]+lines[i+1:]);queueout[label]={'whole_pin':pin(body),'oid':r['sha'],'own_row_pin':pin(line),'status':status,'effort':'1/5','non_target_bytes_pin':pin(nonown[label])}
        if label=='original':need(r['sha']==intake['preserved_QUEUE_blob']['git_blob'] and pin(body)=={k:intake['preserved_QUEUE_blob'][k] for k in ('bytes','sha256')} and pin(line)==intake['preserved_QUEUE_row_pin'],'Original QUEUE matchesRooteligibilityintake')
    check('ForeignQUEUEall370825nontargetbytesidentical',nonown['original']==nonown['current'] and pin(nonown['original'])=={'bytes':370825,'sha256':'fa470050bcabc650cc87da2e848a36a653723416bedb54464a98d13089d8ace3'})
    check('Revisedstatusdoesnotreplaceoriginaleligibility',queues['status_eligibility_remains_original_only'] is True and intake['eligible'] is True and queueout['original']['status']=='claimed_solved' and queueout['current']['status']=='already_solved')
    reference_metadata=strict(public['ORIGINAL_SOURCE_REFERENCE_METADATA.json'])
    for name,row in reference_metadata['records'].items():
        ownrow=orig_by[OWN+'/'+name];body=private[ownrow['private_copy']];j=strict(body)
        need(row['private_native_path']==ownrow['private_copy'] and pin(body)=={k:row[k] for k in ('bytes','sha256')} and row['top_level_fields']==list(j),'InternaloriginalJSONsourceassociation')
        def atpath(field):
            tokens=re.findall(r'\.([A-Za-z_][A-Za-z0-9_]*)|\[([0-9]+)\]',field);value=j
            for key,index in tokens:value=value[key] if key else value[int(index)]
            return value
        need(all(atpath(r['field'])==r['reference'] for r in row['technical_references']),'TechnicalreferenceJSONpathassociation')
        check('Originalinternalsource pinassociation '+name,True)
    record=strict(private[orig_by[OWN+'/source_record.json']['private_copy']]);sm=strict(private[orig_by[OWN+'/source_manifest.json']['private_copy']])
    check('Internaloriginalsource_record exactid andsource_manifest threeexcludedPDFmetadata',record['id']==30005310 and type(record['id']) is int and sm['source_pdfs_excluded'] is True and len(sm['sources'])==3 and all(type(r['sha256']) is str and re.fullmatch('[a-f0-9]{64}',r['sha256']) for r in sm['sources']))
    check('No additional nativequestioncandidatebodyclaimed',strict(public['ORIGINAL_LINKED_SOURCE_CUSTODY.json'])['bodies']['file_count']==0 and reference_metadata['additional_linked_native_question_candidate_files_found']==0)
    total=55337+106594+sum(queues[label]['bytes'] for label in ('original','current'))
    check('Exact904775decodedrolebytes withQUEUEhistoryduplication',total==summary['decoded_role_bytes_including_duplicates_and_QUEUE']==904775)
    # In-memory semantic negatives are independent oracles, not on-disk gates.
    reject('DuplicateJSONkey',lambda:strict(b'{"sha":1,"sha":2}'))
    reject('NonfiniteJSON',lambda:strict(b'{"x":NaN}'))
    treeroute=next(r for r in responses if r.startswith('git/trees/'));t=responses[treeroute];sha=treeroute.rsplit('/',1)[1]
    bad=copy.deepcopy(t);bad['tree'].append(copy.deepcopy(bad['tree'][0]));reject('Duplicate native treename',lambda:tree(bad,sha))
    bad=copy.deepcopy(t);bad['tree']=list(reversed(bad['tree']));reject('Wrong native treeorder',lambda:tree(bad,sha))
    bad=copy.deepcopy(t);bad['truncated']=True;reject('Truncated tree',lambda:tree(bad,sha))
    bad=copy.deepcopy(t);bad['tree'][0]['type']='commit';reject('Wrong mode/type nativepair',lambda:tree(bad,sha))
    bad=copy.deepcopy(t);bad['tree'][0]['sha']='0'*40;reject('Repinned native tuplebody SHA1differs',lambda:tree(bad,sha))
    br=next(r for r in responses if r.startswith('git/blobs/'));v=responses[br];boid=br.rsplit('/',1)[1]
    for k,val in [('size',False),('encoding','utf8'),('sha','0'*40),('content',base64.b64encode(b'changed').decode())]:
        bad=copy.deepcopy(v);bad[k]=val;reject('Nativeblob inner '+k,lambda bad=bad:blob(bad,boid))
    reject('Unsafeprivate reference escape',lambda:safe_relative('../outside.json'))
    check('Allsealedproducerpublic/privatepins stillunchanged',all(pin(read(B/r['path']))=={k:r[k] for k in ('bytes','sha256')} for r in pm['files']+privm['files']))
    out={'schema':'pr212-independent-offline-native-custody-controls-v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','control_count':len(checks),'checks':checks,
      'public_manifest_pin':pin(pmraw),'public_seal_pin':pin(psraw),'private_manifest_pin':pin(public['PRIVATE_EVIDENCE_MANIFEST.json']),
      'public_files':23,'public_bytes':253575,'private_files':256,'private_bytes':2251393,'source_collector_pin':pin(public['collect_native_custody.py']),
      'actual_raw_GETs':49,'transport_records':transport_summary,'canonical_commits':commits,'authenticated_immediate_trees':len(trees),'inspected_native_entries':sum(len(t) for t in trees.values()),
      'full_scope':{'changed_leaves':40,'own':39,'QUEUE':1,'foreign':0,'added_leaves':additions,'deleted_leaves':deletions,'modified_leaves':modifications,'added_directories':sorted(dirsadd),'deleted_directories':sorted(dirsdel),'equal_native_frontier_count':len(equalfrontier)},
      'original_files':20,'original_bytes':55337,'current_files':35,'current_bytes':106594,'exact_original_history_copies':20,'body_identity_ledger':bodymeta,'QUEUE':queueout,
      'decoded_role_bytes':total,'Root_status_acceptance_pin':pin(acceptedraw),'actual_intake_pin':pin(intakeraw),
      'producer_verifier_executed':False,'submitted_or_review_scripts_executed':False,'mathematics_source_question_or_priority_interpretation':False,
      'network_Git_real_lock_globalfive_ref_provider_chat_or_human_contact_effects':False,'assigned_custody_audit_completion_percent':100,
      'actual_Root_custody_gate_or_casecompletion_inferred':False}
    (HERE/'CONTROL_RESULT.json').write_bytes(enc(out))
    print(json.dumps({k:v for k,v in out.items() if k not in ('checks','transport_records','body_identity_ledger')},sort_keys=True,indent=2))
if __name__=='__main__':main()
