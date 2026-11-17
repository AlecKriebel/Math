"""Data-only custody/finite seal; no Git/network/native math or search execution."""
from pathlib import Path
import hashlib,json,stat,datetime
R=Path(__file__).resolve().parent;P=R.parents[1]
def pin(p,root=None):
    st=p.lstat()
    if not stat.S_ISREG(st.st_mode):raise RuntimeError('not regular: '+str(p))
    b=p.read_bytes()
    return dict(path=p.relative_to(root).as_posix() if root else str(p),bytes=len(b),SHA256=hashlib.sha256(b).hexdigest(),mode=oct(stat.S_IMODE(st.st_mode)))
def create(n,x):
    with (R/n).open('x') as f:f.write(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def connector(n):
    x=json.loads((R/n).read_text())
    if x['isError'] is not False:raise RuntimeError('connector error')
    return json.loads(x['structuredContent']['content'])
for n in ('CLOSING_GUARDS.json','EXECUTION.json','MANIFEST.json','FINAL.json'):
    if (R/n).exists():raise RuntimeError('already sealed: '+n)
initial=json.loads((R/'INITIAL.json').read_text());base=initial['baseline']
if pin(R/'INITIAL.json',R)['SHA256']!='05c0fa7eb9440b2dad344729e9f87692189ec860dd88b15f093865c601773a25':raise RuntimeError('INITIAL drift')
if (R/'INITIAL.sha256').read_text()!='05c0fa7eb9440b2dad344729e9f87692189ec860dd88b15f093865c601773a25  INITIAL.json\n':raise RuntimeError('INITIAL hash receipt drift')
openref=connector('OPEN_REMOTE_REF.connector.json');closeref=connector('CLOSE_REMOTE_REF.connector.json')
if openref['object']['sha']!=closeref['object']['sha']!=initial['opening_remote']['main']:raise RuntimeError('remote branch mismatch')
if openref['object']['sha']!=initial['opening_remote']['main'] or closeref['object']['sha']!=initial['opening_remote']['main']:raise RuntimeError('remote changed')
expected_heads=base['Math_HEAD']+'\n'+base['W_HEAD']+'\n'
if (R/'CLOSE_GIT_READ.txt').read_text()!=expected_heads or (R/'CLOSE_GIT_READ.stderr.txt').read_bytes()!=b'':raise RuntimeError('closing HEAD read mismatch')
guards=[]
for label,repo in [('Math',Path('/Users/alec/Documents/Math')),('W',Path('/Users/alec/Desktop/alec-dev/aleckriebel.com'))]:
    index=pin(repo/'.git/index');want=base[label+'_index']
    if (index['bytes'],index['SHA256'],index['mode'])!=(want['bytes'],want['SHA256'],want['mode']):raise RuntimeError('index drift '+label)
    config=pin(repo/'.git/config');head=pin(repo/'.git/HEAD')
    if config['SHA256']!=base[label+'_config_SHA256'] or config['mode']!='0o644' or config['bytes']!=({'Math':2061,'W':365}[label]):raise RuntimeError('config drift '+label)
    if head['SHA256']!=base[label+'_HEAD_file_SHA256']:raise RuntimeError('HEAD bytes drift '+label)
    guards.append(dict(repository=label,HEAD=base[label+'_HEAD'],index=index,config_opaque_pin=config,HEAD_file=head,
        index_config_bytes_and_modes_unchanged=True,HEAD_bytes_unchanged=True,HEAD_file_mode_before_not_observed=True))
search=json.loads((R/'SEARCH.stdout.json').read_text())
if search['status']!='PASS_CURRENT_DOCS_AUTHENTICATED_AND_BOUNDED_SEARCH_COMPLETE' or (R/'SEARCH.stderr.txt').read_bytes()!=b'':raise RuntimeError('search failed')
if (search['metadata_entries'],search['blob_metadata'],search['tree_metadata'],search['complete_HTML_buffers'],search['complete_HTML_bytes'])!=(304,254,50,47,612221):raise RuntimeError('search extent mismatch')
if len(search['reconstructed_tree_objects'])!=51 or search['candidate_paths'] or search['metadata_path_hits'] or any(x['hits'] for x in search['rows']):raise RuntimeError('unexpected hits/result')
references=[]
for record in ('23331709','23174156'):
    c=P/('verification/root-clearance-'+record+'-20261116.json');clear=json.loads(c.read_text())
    review=P/clear['review']['path'];rp=pin(review,P)
    if rp!=clear['review']:raise RuntimeError('root report binding mismatch '+record)
    native=P/('papers/'+record+'/sources/record.response.body')
    title=json.loads(native.read_text())['metadata']['title']
    if title!=next(t['title'] for t in initial['targets'] if t['record']==record):raise RuntimeError('published title mismatch '+record)
    references.extend([pin(c,P),rp,pin(native,P)])
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
create('CLOSING_GUARDS.json',dict(UTC=now,status='PASS_OPENING_AND_CLOSING_LOCAL_AND_REMOTE_GUARDS',repositories=guards,
    remote_main_open=initial['opening_remote']['main'],remote_main_close=closeref['object']['sha'],docs_tree=search['docs_tree'],
    target_authority_and_native_title_pins=references,no_credentials_or_config_contents_exposed=True))
create('EXECUTION.json',dict(UTC=now,program=pin(R/'search_current.py',R),whole_current_body_read_before_sole_use=True,
    command='python3 search_current.py > SEARCH.stdout.json 2> SEARCH.stderr.txt',actual_exit=0,elapsed_seconds=0.381458083,
    stdout=pin(R/'SEARCH.stdout.json',R),stderr=pin(R/'SEARCH.stderr.txt',R),purposeful_search_iterations=1,
    old_helper_native_math_HTTP_or_mutating_execution=False,closing_sealer_is_data_only=True,
    literal_limits=['Combined report display truncated; whole second root report reread',
        'Full search display truncated; complete47title/h1/hit projection reread untruncated',
        'INITIAL count shorthand corrected in separate artifact without modifying INITIAL']))
files=[];dirs=[]
for p in sorted(R.rglob('*')):
    st=p.lstat()
    if stat.S_ISREG(st.st_mode):files.append(pin(p,R))
    elif stat.S_ISDIR(st.st_mode):dirs.append(dict(path=p.relative_to(R).as_posix(),mode=oct(stat.S_IMODE(st.st_mode))))
    else:raise RuntimeError('unexpected owned object')
if dirs:raise RuntimeError('expected bounded flat packet')
create('MANIFEST.json',dict(UTC=now,files=files,directories=dirs,root_mode=oct(stat.S_IMODE(R.lstat().st_mode)),
    exact_excluded_terminal_controls=['MANIFEST.json','FINAL.json'],all_ignored_empty_files_and_modes_included=True))
create('FINAL.json',dict(UTC=now,status='FROZEN_BOUNDED_CURRENT_DOCS_NO_MATCH_BOTH_RECORDS',records=['23331709','23174156'],
    report=pin(R/'REPORT.md',R),manifest=pin(R/'MANIFEST.json',R),correspondence=pin(R/'CORRESPONDENCE.json',R),
    initial=pin(R/'INITIAL.json',R),current_remote_main=closeref['object']['sha'],docs_tree=search['docs_tree'],
    all47HTML_bytes_modes_and304metadata51tree_objects_authenticated=True,
    complete_HTML_bytes=612221,candidate_articles=0,old_to_future_proposal_mappings=[],
    no_history_absence_or_priority_or_live_HTTP_claim=True,source_and_website_native_HEAD_index_config_guards_unchanged=True,
    execution=pin(R/'EXECUTION.json',R),closing_guards=pin(R/'CLOSING_GUARDS.json',R),
    extent=dict(regular_files=len(files)+2,child_directories=0,all_paths=sorted([x['path'] for x in files]+['MANIFEST.json','FINAL.json'])),
    completion_percent=100,follow_up=None,publication_canonical_AA_or_redirect_authority=False,
    all_writes_owned_folder_only=True,quiescent_after_seal=True,self_hash_excluded=True))
for p in files:
    if pin(R/p['path'],R)!=p:raise RuntimeError('owned payload drift during seal')
print(json.dumps(dict(FINAL=pin(R/'FINAL.json',R),MANIFEST=pin(R/'MANIFEST.json',R),regular_files=len(files)+2,child_directories=0),indent=2))
