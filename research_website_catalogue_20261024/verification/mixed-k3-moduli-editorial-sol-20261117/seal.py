"""Passive finite closure after complete personal copy read; never imports the builder."""
import datetime, hashlib, json, os, stat, time
from pathlib import Path

P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OWN=P/'verification/mixed-k3-moduli-editorial-sol-20261117'
SRC=P/'papers/23204176/sources'
TERMINALS={'MANIFEST.json','FINAL.json'}
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
t=time.monotonic()
def pin(p):
    a=p.lstat()
    assert stat.S_ISREG(a.st_mode) and not p.is_symlink()
    raw=p.read_bytes()
    z=p.lstat()
    assert (a.st_dev,a.st_ino,a.st_size,a.st_mode,a.st_mtime_ns,a.st_ctime_ns)==(z.st_dev,z.st_ino,z.st_size,z.st_mode,z.st_mtime_ns,z.st_ctime_ns)
    return dict(bytes=len(raw),SHA256=hashlib.sha256(raw).hexdigest(),MD5=hashlib.md5(raw).hexdigest(),mode=oct(stat.S_IMODE(z.st_mode)))
def census(root):
    files,dirs={},{'.':oct(stat.S_IMODE(root.lstat().st_mode))}
    pending=[root]
    while pending:
        here=pending.pop()
        a=here.lstat()
        assert stat.S_ISDIR(a.st_mode) and not here.is_symlink()
        for p in sorted(here.iterdir()):
            rel=p.relative_to(root).as_posix()
            z=p.lstat()
            assert not p.is_symlink()
            if stat.S_ISDIR(z.st_mode):
                dirs[rel]=oct(stat.S_IMODE(z.st_mode));pending.append(p)
            else:files[rel]=pin(p)
        z=here.lstat()
        assert (a.st_dev,a.st_ino,a.st_mode,a.st_mtime_ns,a.st_ctime_ns)==(z.st_dev,z.st_ino,z.st_mode,z.st_mtime_ns,z.st_ctime_ns)
    return dict(schema='whole-original-source-guard-v1',root=str(root),files=files,directories=dirs,hidden_paths=[n for n in sorted(set(files)|set(dirs)) if n!='.' and any(x.startswith('.') for x in n.split('/'))],empty_files=[n for n,x in sorted(files.items()) if x['bytes']==0],empty_directories=[n for n in sorted(dirs) if n!='.' and not any(q.startswith(n+'/') for q in set(files)|set(dirs))])
def read(n):return json.loads((OWN/n).read_bytes())
def write(n,data):
    with (OWN/n).open('x') as f:json.dump(data,f,ensure_ascii=False,indent=2);f.write('\n')

assert not any((OWN/n).exists() for n in TERMINALS)
execution=read('EXECUTION.json')
assert execution['exit_code']==0 and execution['stdout_bytes']==execution['stderr_bytes']==0 and execution['attempt']==1
assert pin(OWN/'prepare.py')['SHA256']==execution['builder_SHA256']
result=read('PREPARATION_RESULT.json')
model=read('page-model.json')
for n,key in [('article.html','article'),('head.html','head'),('main.html','main'),('page-model.json','model'),('prepare.py','builder')]:assert pin(OWN/n)==result[key]
for n,value in result['inputs'].items():assert pin(P/n)==value
before,after=read('SOURCE_GUARDS_BEFORE.json'),read('SOURCE_GUARDS_AFTER.json')
finalsource=census(SRC)
assert before==after==finalsource and len(finalsource['files'])==43 and len(finalsource['directories'])==8
write('SOURCE_GUARDS_FINAL.json',finalsource)
css=read('COLLISION_AND_CSS.json')
assert pin(Path(css['stylesheet']))==css['stylesheet_pin'] and not os.path.lexists(css['checked_path'])
assert all(model[n] is None for n in ('canonical_url','base_url','production_url','actual_publication_date','AA','follow_up','native_version'))
assert model['publication_authority'] is False and model['robots']=='noindex, nofollow'
assert model['native_API_version_field_present'] is False
for row in model['native_asset_order']:
    actual=pin(OWN/row['local_path']);original=pin(SRC/'zenodo-files'/row['name'])
    assert actual==original
    assert all(actual[k]==row[k] for k in actual)
copy_names=['article.html','head.html','main.html','page-model.json','citation.bib','ABSTRACT.txt','ABSTRACT_SOURCE.json','main.template.html']
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
write('COPY_READ_AND_INPUT_PINS.json',dict(schema='private-editorial-complete-personal-copy-read-v1',UTC=utc,record_id='23204176',complete_saved_builder_template_invoker_read_before_only_preparation=True,complete_actual_article_head_main_model_Bib_abstract_personally_read=True,artifact_pins={n:pin(OWN/n) for n in copy_names},root_clearance_review_pins=result['inputs'],scientific_disposition_inherited_not_reperformed=True,reviewer_reservation_retained_in_root_review_not_public_audit_replay=True,source_guard_all_43_files_7_childdirs_exact=True,no_source_or_old_helper_execution=True,ordinary_AI_review_not_formal_or_human_refereeing=True))
report='''# Private K3-moduli article packet

Private editorial preparation is complete, ready for independent factual review and the root's actual copy read. It inherits the bounded scientific clearance for record 23204176; this writer did not independently re-audit the imported geometry.

The article explains the rational cycle-class conclusion for finite mixed products of actual smooth projective stable moduli in Bülles Theorem 0.1 scope. It preserves arbitrary different or repeated complex projective K3 bases, Brauer classes, fixed-data stability hypotheses, the non-fine normalized splitting, empty and point cases, and Hilbert n=0/1. Attribution to OpenAI's pinned mixed-K3 input, Bülles and earlier Arapura transfers is prominent. It presents an assembled corollary with inherited reduction.

The complete original TeX abstract is preserved with only its declared Bülles accent rendering and whitespace normalization; the longer native API Description is separately recorded. Visible abstract, DC description, single ScholarlyArticle and page model agree exactly. No API version is invented. Declared manuscript/publication date is 6 October 2026; actual website canonical/base/production/publication date and AA remain null. A collision-free proposed slug is stored separately. Robots remain noindex, nofollow. The unchanged shared research.css is linked.

Native assets remain PDF then ZIP, whole-byte identical to the controlling outer four-page, 67,264-byte PDF and 135,014-byte source archive. The page supplies PDF iframe/open/download and native original links, BibTeX, citation/SEO metadata, CC BY 4.0 rights for owned materials with third-party attribution/rights retained, extensive AI-use and unrefereed status, and passive substantive collaboration with contribution-based authorship. No follow-up is proposed. No tracker completion is inferred or written.

The 190-line fresh builder was personally read in full and executed exactly once, exit 0 with empty stdout/stderr. Literal invocation and timing are saved. Complete original source, 43 files/7 child directories including controls, bytes, modes and hidden/empty topology, matched the actual custody manifest and external pins and remained exact before/after/final. The private page has only static data checks; browser rendering, live URLs, deployment and downloads over the network were not verified. W access was limited to reading shared CSS and checking the proposed path. The preparation result's no-W-actions field denotes no mutations: no W/Git/Sheet mutation, network access, scientific-program execution, release, Zenodo or outreach action occurred. Root review keeps its actual reviewer reservation; no unanimity or human/formal certificate is claimed.

Completion 100% of this private writer task. This packet has no publication authority. The finite namespace is frozen; independent factual review, root adoption and all later production work are separate tasks.
'''
with (OWN/'REPORT.md').open('x') as f:f.write(report)
with (OWN/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+utc+' — Personally read all actual generated article/head/main/model/citation/abstract content. Passive final guards passed. Completion100% of private writer scope; frozen for independent factual/root review, no production authority; stop.\n')
write('SEAL_EXECUTION.json',dict(schema='passive-editorial-seal-v1',started_UTC=started,finished_UTC=utc,elapsed_seconds=time.monotonic()-t,full_saved_seal_personally_read_before_invocation=True,preparation_attempts=1,preparation_exit_code=0,source_guard_exact=True,substantive_failures=[],completion_percent=100))
all_before=census(OWN)
assert not (set(all_before['files'])&TERMINALS)
names=sorted(set(all_before['files'])|TERMINALS)
directories=all_before['directories']
manifest=dict(schema='finite-private-editorial-manifest-v1',UTC=utc,root=str(OWN),root_mode=directories['.'],payload_files=[dict(path=n,**v) for n,v in sorted(all_before['files'].items())],directories=[dict(path=n,mode=m) for n,m in sorted(directories.items()) if n!='.'],actual_file_count=len(names),actual_child_directory_count=len(directories)-1,terminal_control_topology=[dict(path=n,mode='0o644') for n in sorted(TERMINALS)],exact_terminal_self_hash_exclusions=sorted(TERMINALS),hidden_paths=all_before['hidden_paths'],empty_files=all_before['empty_files'],empty_directories=all_before['empty_directories'],scope='Entire own actual namespace; no hidden/empty/ignored filters; exact terminal circular/self-hash pair only')
write('MANIFEST.json',manifest)
write('FINAL.json',dict(schema='private-editorial-FINAL-v1',UTC=utc,status='READY_FOR_INDEPENDENT_FACT_AND_ROOT_COPY_REVIEW',completion_percent=100,record_id='23204176',sheet_row=191,root=str(OWN),root_mode=directories['.'],article=pin(OWN/'article.html'),head=pin(OWN/'head.html'),main=pin(OWN/'main.html'),model=pin(OWN/'page-model.json'),citation=pin(OWN/'citation.bib'),builder=pin(OWN/'prepare.py'),builder_lines=190,manifest=pin(OWN/'MANIFEST.json'),actual_files=len(names),actual_childdirs=len(directories)-1,complete_file_names=names,directories=manifest['directories'],terminal_self_hash_exclusions=sorted(TERMINALS),source_files_childdirs=[43,7],complete_source_before_after_final_exact=True,source_control_pins=result['source_control_pins'],root_clearance_review_pins=result['inputs'],native_API_version=None,declared_publication_date='2026-10-06',proposed_slug=model['deployment_proposal']['slug'],canonical_url=None,base_url=None,production_url=None,actual_publication_date=None,AA=None,follow_up=None,publication_authority=False,preparation_attempts=1,preparation_exit_code=0,failures=[],limitations=['Scientific disposition inherited; no new independent theorem review','Static private checks only; browser/live/download-over-network unverified','No website/Git/tracker/network/scientific execution or publication actions'],quiescent_stop=True))
actual=census(OWN)
assert set(actual['files'])==set(names) and actual['directories']==directories
assert all(actual['files'][n]==v for n,v in all_before['files'].items())
assert actual['files']['MANIFEST.json']==read('FINAL.json')['manifest']
assert all(actual['files'][n]['mode']=='0o644' for n in TERMINALS)
print(json.dumps(dict(status='FROZEN',files=len(names),childdirs=len(directories)-1,article=actual['files']['article.html'],MANIFEST=actual['files']['MANIFEST.json'],FINAL=actual['files']['FINAL.json'])))
