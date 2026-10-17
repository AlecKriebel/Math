"""Root read-only parent/preimage capture. No local Git, lock or existing-view writes."""
import base64,datetime,hashlib,json,os,re,sys,types
from pathlib import Path
HERE=Path(__file__).absolute().parent
CASE=HERE.parent
PROGRAM=CASE.parents[1]
CHECKOUT=PROGRAM.parent
GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
ANCHOR='ad3af31e26c29115d222142ae6b033115e195808'
QUEUE='unsolved_math_prioritization/QUEUE.md'
VIEWS=('draft_pr_publication_program_20260930/audits/pr212_30005310/CURRENT_CASE_STATUS.json',
'draft_pr_publication_program_20260930/audits/pr212_30005310/RESEARCH_LOG.md',
'draft_pr_publication_program_20260930/CURRENT_PROGRESS.json',
'draft_pr_publication_program_20260930/CURRENT_PROGRESS.md',
'draft_pr_publication_program_20260930/RESEARCH_LOG.md')
OUT=HERE/'_private_parent_capture_01'
def need(x,m):
    if type(x) is not bool or not x:raise RuntimeError(m)
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(x):return (json.dumps(x,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def save(name,b):
    need(type(b) is bytes and Path(name).name==name and len(b)<=12000000,'Bounded owned new output')
    fd=os.open(OUT/name,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o444)
    with os.fdopen(fd,'wb') as f:
        need(f.write(b)==len(b),'Short write');f.flush();os.fsync(f.fileno())
    need((OUT/name).read_bytes()==b,'Output readback')
def module(name,filename,n,sha):
    p=CASE/'native_custody_01'/filename;b=p.read_bytes()
    need(pin(b)=={'bytes':n,'sha256':sha} and p.resolve()==p,'Pinned inert source')
    d=types.ModuleType(name);d.__file__=str(p);exec(compile(b,str(p),'exec'),d.__dict__);return d
def main():
    need(sys.flags.ignore_environment and sys.flags.no_site and sys.flags.safe_path and sys.dont_write_bytecode and not sys.flags.optimize,'Python -E -S -B -P')
    h=module('readonly_get','get_primitives.py',3794,'808149b347a61809e37a0b71fc4dc602ec17e63e38e985d99123827268286e09')
    core=module('readonly_trees','native_trees_readonly.py',4719,'c71575a580c43fea8d302c978e0b6c340a16474779ffeb4671e77b967cf6e2ce')
    selection_path=CASE/'root_native_source_assessment_01/ROOT_PRELIMINARY_ARCHIVE_SELECTION_01.json'
    raw=h.regular(selection_path);need(pin(raw)=={'bytes':130418,'sha256':'b90c7034a30b36b640e34a7478c41da8bfab3698c3c5e746dcf978e07bd883cf'},'Pinned positive selection')
    selection=h.decode(raw);paths={r['path'] for r in selection['files']}
    paths.remove('draft_pr_publication_program_20260930/audits/pr212_30005310/ROOT_ARCHIVE_README_01.md')
    paths.add('draft_pr_publication_program_20260930/audits/pr212_30005310/ROOT_ARCHIVE_README_02.md')
    need(len(paths)==220,'Explicit220 preliminary paths')
    OUT.mkdir(mode=0o700,exist_ok=False)
    calls=[]
    def get(route):
        need(route in ('git/ref/heads/main','pulls/212') or re.fullmatch(r'git/(?:commits|trees|blobs)/[0-9a-f]{40}',route) is not None or re.fullmatch(r'compare/[0-9a-f]{40}\.\.\.[0-9a-f]{40}',route) is not None,'Only actual GET routes')
        need(len(calls)<200,'Bounded200 calls')
        name=str(len(calls)+1).zfill(4)
        intent={'method':'GET','hostname':'github.com','repository':'AlecKriebel/Math','path':route}
        save(name+'.intent.json',enc(intent))
        result=h.bounded_get([GH,'api','--hostname','github.com','--method','GET','repos/AlecKriebel/Math/'+route])
        save(name+'.stdout.json',result.stdout);save(name+'.stderr.txt',result.stderr)
        receipt={**intent,'exit':result.returncode,'raw_stdout':{'path':str(OUT/(name+'.stdout.json')),**pin(result.stdout)},'raw_stderr':{'path':str(OUT/(name+'.stderr.txt')),**pin(result.stderr)}}
        save(name+'.receipt.json',enc(receipt));calls.append(receipt)
        need(result.returncode==0,'Actual GET failure; no retry')
        value=h.decode(result.stdout);need(type(value) is dict,'Native object')
        return value
    def observer(method,route,body=None):
        need(method=='GET' and body is None,'GET-only observer');return get(route)
    def blob(oid):
        j=get('git/blobs/'+oid)
        need(j.get('sha')==oid and j.get('encoding')=='base64' and type(j.get('size')) is int and 0<=j['size']<=4000000 and type(j.get('content')) is str,'Bounded full blob')
        b=base64.b64decode(''.join(j['content'].split()),validate=True)
        need(len(b)==j['size'] and h.native('blob',b)==oid,'Full blob canonical SHA1/size')
        return b
    first=get('git/ref/heads/main');parent=first['object']['sha'];need(h.hexid(parent),'Actual parent')
    commit=get('git/commits/'+parent);need(commit.get('sha')==parent and h.hexid(commit['tree']['sha']),'Actual parent/root')
    root=commit['tree']['sha']
    if parent!=ANCHOR:
        comparison=get('compare/'+ANCHOR+'...'+parent)
        need(comparison.get('status')=='ahead' and comparison['merge_base_commit']['sha']==ANCHOR,'Actual211 retained ancestry')
    pr=get('pulls/212')
    for k,v in {'number':212,'state':'open','draft':True,'merged':False,'commits':3,'merged_at':None,'title':'30005310: Credited prior counterexamples to literal numerical scenarios'}.items():
        need(h.exact(pr.get(k),v),'Current PR metadata '+k)
    need(pr['head']['sha']=='99af7a27a711271bcd0b9e7ce90e374e4100ea6d' and pr['head']['ref']=='math/30005310-colored-threshold-wip' and pr['base']['ref']=='main','Exact current untouched draft')
    trees=core.NativeTrees(observer)
    preimages={s:trees.lookup(root,s) for s in sorted(paths|set(VIEWS))}
    protected={s:trees.lookup(root,s) for s in ('unsolved_math_prioritization/attempts/30005310','draft_pr_descending_audit_20261002/audits/pr212_30005310')}
    qt=trees.lookup(root,QUEUE);need(qt is not None and qt[:2]==('100644','blob'),'Whole parent QUEUE tuple')
    qb=blob(qt[2]);save('PARENT_QUEUE_BODY.txt',qb)
    native_views=[];local_views=[]
    for i,s in enumerate(VIEWS):
        item=preimages[s];body=None
        if item is not None:
            need(item[:2]==('100644','blob'),'Regular native current view')
            body=blob(item[2]);save('NATIVE_VIEW_'+str(i)+'.txt',body)
        native_views.append({'path':s,'tuple':item,'body_pin':pin(body) if body is not None else None,'source':str(OUT/('NATIVE_VIEW_'+str(i)+'.txt')) if body is not None else None})
        local=CHECKOUT/s
        if not local.exists() and not local.is_symlink():lb=None
        else:lb=h.regular(local,immutable=False);save('LOCAL_VIEW_'+str(i)+'.txt',lb)
        local_views.append({'path':s,'preimage':pin(lb) if lb is not None else None,'source':str(OUT/('LOCAL_VIEW_'+str(i)+'.txt')) if lb is not None else None})
    progress=h.decode((OUT/'NATIVE_VIEW_2.txt').read_bytes())
    for k,v in {'fully_completed_count':53,'published_count':37,'last_completed_PR':211,'next_numeric_intake_cursor':212,'goal_complete':False,'dated_eligible_total':99}.items():
        need(h.exact(progress.get(k),v),'Intervening numeric progress '+k)
    baseline_raw=h.regular(CASE/'native_administrative_preparation_01/BASELINE_MEMBERSHIP.json',immutable=False)
    need(pin(baseline_raw)=={'bytes':853,'sha256':'b4fe8858faebc0f14ab956d8849af28072837807f3fc87e85a2abe356bfb2f1e'},'Exact source membership baseline')
    baseline=h.decode(baseline_raw)
    need(all(h.exact(progress.get(k),v) for k,v in baseline.items()),'Exact53/37 membership lists')
    final_pr=get('pulls/212')
    selected=lambda x:{k:x.get(k) for k in ('number','title','state','draft','merged','commits','merged_at','body')}|{'head':x['head']['sha'],'branch':x['head']['ref'],'base':x['base']['ref']}
    need(h.exact(selected(pr),selected(final_pr)),'PR changed during capture')
    last=get('git/ref/heads/main')['object']['sha']
    result={'schema':'pr212-root-readonly-immutable-parent-preimage-capture-v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'parent':parent,'parent_tree':root,'ref_at_end':last,'coherent_ref_before_after':last==parent,'preimages':preimages,'protected_queue':qt,'protected_queue_body_pin':pin(qb),'protected_nodes':protected,'current_PR_opaque_body_pin':pin(json.dumps(pr.get('body'),sort_keys=True,separators=(',',':'),allow_nan=False).encode()),'native_views':native_views,'local_views':local_views,'captured_tree_count':len(trees.cache),'inspected_tree_entries':trees.inspected,'actual_GET_count':len(calls),'actual_GET_receipts':calls,'no_native_POST_or_ref_PR_global_five_or_lock_effect':True,'Root_logical_packet_native_or_numeric_authority':False,'scope':'Immutable dated parent/preimages only, no lease or completed checkpoint.'}
    save('FACTUAL_PARENT_CAPTURE.json',enc(result));save('CAPTURED_NATIVE_TREES.json',enc(trees.cache))
    print(json.dumps({k:result[k] for k in ('parent','parent_tree','ref_at_end','coherent_ref_before_after','captured_tree_count','inspected_tree_entries','actual_GET_count','no_native_POST_or_ref_PR_global_five_or_lock_effect')},sort_keys=True))
if __name__=='__main__':main()
