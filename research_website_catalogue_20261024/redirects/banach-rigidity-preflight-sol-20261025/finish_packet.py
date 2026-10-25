"""Finalize only this new preflight packet, refusing an existing final seal.
No source/Git mutation, paper execution, legacy builder, or remote fetch.
"""
from pathlib import Path
import json,hashlib,datetime,subprocess,os
E=Path(__file__).resolve().parent;P=E.parents[1];G=P.parent
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def save(n,x):(E/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def binding(p):b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':sha(b)}
def git(*args):return subprocess.run(['git',*args],cwd=G,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0','GIT_TERMINAL_PROMPT':'0'},check=True,capture_output=True,timeout=30).stdout
assert not (E/'FINAL_SEAL.json').exists()
before=json.loads((E/'PRESERVATION_BEFORE.json').read_text());changed=[]
for r in before['files']:
 p=Path(r['path'])
 if not p.is_file() or p.stat().st_size!=r['bytes'] or sha(p.read_bytes())!=r['sha256']:changed.append(r['path'])
docs=sorted(str(p) for p in (G/'docs').rglob('*') if p.is_file())
refs={k:git('rev-parse',v).decode().strip() for k,v in [('HEAD','HEAD'),('main','refs/heads/main'),('origin_main_local_ref','refs/remotes/origin/main')]}
refs['symbolic_HEAD']=git('symbolic-ref','HEAD').decode().strip()
authorized_ref=str(G/'.git/refs/remotes/origin/main')
after={'utc':utc(),'original_bindings':len(before['files']),'changed_files':changed,'authorized_concurrent_changed_files':[authorized_ref] if authorized_ref in changed else [],'unauthorized_or_unexplained_changed_files':[p for p in changed if p!=authorized_ref],'added_or_removed_working_docs':sorted(set(docs)^set(before['docs_paths'])),'refs':refs,'refs_unchanged':all(refs[k]==before[k] for k in refs),'local_HEAD_main_symbolic_HEAD_unchanged':all(refs[k]==before[k] for k in ['HEAD','main','symbolic_HEAD']),'working_docs_status_unchanged':git('status','--porcelain=v1','--','docs').decode()==before['working_docs_status'],'actual_working_docs_files':len(docs),'authorized_root_tracking_ref_final_binding':binding(G/'.git/refs/remotes/origin/main'),'authority':'ROOT_CONCURRENT_CHECKPOINT_AUTHORITY.json'}
save('PRESERVATION_AFTER.json',after)
assert not after['unauthorized_or_unexplained_changed_files'] and not after['added_or_removed_working_docs'] and after['local_HEAD_main_symbolic_HEAD_unchanged'] and after['working_docs_status_unchanged'],after
reused=json.loads((E/'REUSED_EXTRACT_BINDINGS.json').read_text())
for r in reused:assert binding(Path(r['path']))==r
start=utc();raw=git('ls-remote','origin','refs/heads/main');ended=utc();(E/'remote-main-closing.raw.txt').write_bytes(raw)
pin=json.loads((E/'REMOTE_PIN.json').read_text());closing=raw.decode().split('\t')[0]
assert raw==f'{closing}\trefs/heads/main\n'.encode()
assert git('rev-parse',closing+':docs').decode().strip()==pin['docs_tree']
assert git('ls-tree','-r','-l','--full-tree',closing,'--','docs')==(E/'docs-tree.raw.txt').read_bytes()
git('merge-base','--is-ancestor',pin['commit'],closing)
objects=[]
for kind,oid in [('commit',closing),('tree',git('rev-parse',closing+'^{tree}').decode().strip())]:
 b=git('cat-file',kind,oid);assert hashlib.sha1(kind.encode()+b' '+str(len(b)).encode()+b'\0'+b).hexdigest()==oid
 p=E/('closing-git-object-'+oid+'.raw');p.write_bytes(b);objects.append({'kind':kind,'oid':oid,**binding(p)})
save('REMOTE_CLOSING_RECEIPT.json',{'started_utc':start,'ended_utc':ended,'operation':['git','ls-remote','origin','refs/heads/main'],'raw':binding(E/'remote-main-closing.raw.txt'),'same_commit_as_initial':closing==pin['commit'],'commit':closing,'initial_commit':pin['commit'],'docs_tree':pin['docs_tree'],'same_complete_recursive_docs_listing':True,'root_authorized_checkpoint':'ROOT_CONCURRENT_CHECKPOINT_AUTHORITY.json','new_commit_and_root_tree_objects':objects,'changed_paths_initial_to_closing':git('diff-tree','--no-commit-id','--name-only','-r',pin['commit'],closing).decode().splitlines(),'no_fetch_or_ref_update_by_this_task':True})
search=json.loads((E/'COMPLETE_SEARCH.json').read_text());assert len(search['rows'])==260
assert all(not v for r in search['rows'] for k,v in r['hits'].items() if k!='broad_context')
tree=json.loads((E/'DOCS_OBJECT_BINDINGS.json').read_text());target=json.loads((E/'TARGET_IDENTITY.json').read_text());controls=json.loads((E/'QUERY_CONTROLS.json').read_text());assert controls['status']=='PASS'
save('MATCH_MAP.json',{'utc':utc(),'record':23217863,'genuine_article_counterparts':[],'matching_title_DOI_or_distinctive_queries':[],'matching_current_reader_SHA256':[r['path'] for r in tree if r['sha256']==target['reader']['sha256']],'matching_foreign_OpenAI_reader_SHA256':[r['path'] for r in tree if r['sha256']==target['foreign_OpenAI_28pp_SHA256']],'redirect_candidates':[],'authority':'No route mutation authorized by this packet'})
save('EXCLUSIONS.json',{'utc':utc(),'all_broad_hit_paths':sorted({r['path'] for r in search['nonempty']}),'exclusions':[
 {'path':'docs/papers/cyclic-bell-exact-values-and-randomness/paper.pdf','extent':'Actual PDF1,5,6; all precise-query search results;28-page full reading not claimed','mechanism':'Generated von Neumann algebra for polar-functional-calculus Bell bound; no ordinary Banach–Mazur comparison'},
 {'path':'docs/papers/cyclic-bell-exact-values-and-randomness/two-page-summary.pdf','extent':'Complete2-page extract','mechanism':'Bell values, maximizer support and permutation randomness; no target theorem'},
 {'path':'docs/papers/cyclic-bell-tsirelson-bound/paper.pdf','extent':'Actual PDF1–2','mechanism':'Earlier cyclic Bell operator upper bound, no near-isometric algebra classification'},
 {'path':'docs/papers/gamma-supercyclicity/index.html','extent':'Actual title/headings and matching decoded visible contexts','mechanism':'Banach coefficient spaces in supercyclicity'},
 {'path':'docs/papers/gamma-supercyclicity/paper.pdf','extent':'Complete5-page extract','mechanism':'Weighted shift/composition Gamma-orbit equivalence, no Banach–Mazur rigidity'},
 {'path':'docs/papers/kourovka-16-45/paper.pdf','extent':'Actual PDF1,9','mechanism':'Finite group bases; Mazur is a substring of Mazurov'},
 {'path':'docs/papers/kourovka-16-63/paper.pdf','extent':'Actual PDF1,12,13','mechanism':'Finite Lie-lattice cohomology and group automorphisms; Mazurov substring'}]})
save('READ_LEDGER.json',{'utc':utc(),'prior_method_full_reads':['redirects/odd-ear-blocking-preflight-sol-20261025/REPORT.md','redirects/odd-ear-blocking-preflight-sol-20261025/PIN_AUTHORITY.json','redirects/odd-ear-blocking-preflight-sol-20261025/CORPUS_RECEIPT.json','redirects/odd-ear-blocking-preflight-sol-20261025/VERDICT.json','redirects/odd-ear-blocking-preflight-sol-20261025/inspect_pinned.py','redirects/odd-ear-blocking-preflight-sol-20261025/complete_search.py','redirects/odd-ear-blocking-preflight-sol-20261025/verify_readonly.py','redirects/ambient-block-modulus-preflight-sol-20261025/REPORT.md','redirects/ambient-block-modulus-preflight-sol-20261025/CUSTODY.json'],
 'target_current_reads':['SOURCE_READY complete','normalized-metadata complete','controlling main.tex lines1–150: exact title, abstract, whole main theorem, external input and attribution, actual-image convention and start of deformation proof'],'earlier_target_full_read':'Entire7-page reader and449-line controlling TeX were read in this agent’s earlier scientific/editorial work; no fresh full reread is claimed in this bounded preflight',
 'corpus_identity_reads':'All47 HTML titles and h1/h2 lists; all76 PDF first-title-line entries; full visible old index and full34-entry sitemap; every actual broad-hit context; selected/full reader extents in EXCLUSIONS.json',
 'automatic_not_human_full_read':'All76 complete extracts (854pages),137 decodable text objects and47 visible HTML representations searched; not a human semantic full reading of all unrelated pages',
 'display_truncation_correction':'Initial combined Bell/Gamma/model display omitted part of Bell main PDF5; separately read full PDF5 before finalization',
 'foreign_primaries_or_bundled_paper_code_executed':False,'support_archives_expanded':False,'new_PDF_cache_or_whole_workingtree_copy':False})
verdict={'utc':utc(),'status':'NO_GENUINE_LEGACY_CORRESPONDENCE_IDENTIFIED','exact_record_id':23217863,'target_title':target['title'],'initial_remote_main_commit':pin['commit'],'closing_remote_main_commit':closing,'docs_tree':pin['docs_tree'],'genuine_matches':0,'redirect_candidates':[],'scope':'Exactly the complete254-file pinned GitHub Pages docs tree;137 tracked textual blobs,47 decoded HTML texts and76 preexisting complete PDF extracts','precise_queries_all_empty':True,'positive_controls':6,'publication_or_redirect_authority':False,'source_or_scientific_status_reinterpreted':False,'foreign_OpenAI28pp_not_target':True,'completion_percent_this_preflight':100,'all203_programme_complete':False,'limitations':['No worldwide absence claim','No all-history or other-branch search','No recursive interpretation of unrelated support archives','No fresh live website HTTP verification','No human complete reading of854 unrelated PDF pages']}
save('VERDICT.json',verdict)
save('VALIDATION.json',{'utc':utc(),'status':'PASS_WITH_AUTHORIZED_CONCURRENT_ROOT_CHECKPOINT','original_bindings_unchanged':len(before['files'])-len(changed),'authorized_concurrent_changed_files':after['authorized_concurrent_changed_files'],'working_docs_files_unchanged':len(docs),'preserved_local_HEAD_main_index':True,'all76_reused_extract_bindings_unchanged':True,'all254_immutable_blobs_authenticated':True,'precise_query_families':7,'precise_hits':0,'positive_controls':6,'closing_remote_docs_tree_unchanged':True,'no_legacy_route_or_site_mutation':True,'scope':'Concrete successful checks plus explicit concurrent root ref advance, not a scientific PASS or publication authority'})
log=(E/'RESEARCH_LOG.md').read_text();log=log.replace('* Post-search checkpoint —',f"* {search['utc']} —")
log+=f"* {utc()} — Complete report, exact exclusions/read ledger and negative custom verdict written. {len(before['files'])-len(changed)}/{len(before['files'])} protected bindings unchanged; the only difference is root's explicitly authorized origin/main tracking-ref advance. All{len(docs)} actual working-docs files, local HEAD/main/index/status and76 reused extracts unchanged. Closing fresh remote pin {closing} has the same complete docs tree. No route proposed or public mutation by this task. Completion estimate100%; all203 ongoing. Final sealed read-only verifier follows.\n"
(E/'RESEARCH_LOG.md').write_text(log)
payload=[]
for p in sorted(E.iterdir()):
 if p.is_file():b=p.read_bytes();payload.append({'path':p.name,'bytes':len(b),'sha256':sha(b)})
save('FINAL_MANIFEST.json',{'utc':utc(),'namespace':str(E),'files':payload,'original_bindings_receipt':'PRESERVATION_BEFORE.json','reused_extract_bindings':'REUSED_EXTRACT_BINDINGS.json','preserve_immutable':True})
save('FINAL_SEAL.json',{'utc':utc(),'status':verdict['status'],'manifest_sha256':sha((E/'FINAL_MANIFEST.json').read_bytes()),'report_sha256':sha((E/'REPORT.md').read_bytes()),'verdict_sha256':sha((E/'VERDICT.json').read_bytes()),'owned_payload_files':len(payload),'original_bindings':len(before['files']),'redirect_candidates':[],'publication_or_redirect_authority':False,'preserve_immutable':True})
print(json.dumps({'files':len(payload),'protected_originals':len(before['files']),'docs_files':len(docs),'report':binding(E/'REPORT.md'),'verdict':binding(E/'VERDICT.json'),'manifest':binding(E/'FINAL_MANIFEST.json'),'seal':binding(E/'FINAL_SEAL.json')},indent=2))
