"""Build paraphrased public ledgers and private receipt index from existing bytes.

No network, Git or outside-namespace writes. Reading declarations are agent
observations; native receipts prove retrieval/rendering/execution only.
"""
from pathlib import Path
from datetime import datetime,timezone
import json,re,hashlib
S=Path(__file__).resolve().parent;P=S/'private_evidence'
sha=lambda b:hashlib.sha256(b).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
scopes={
 'fisher2001':('All33physical pages read; visual physical4,5,26,27 (printed172,173,194,195).','Tate Lemma1.1/discriminant and full-level Lemma3.4; direct old modular input.'),
 'fisher2003':('Physical1–7,19,46 read; whole extract keyword-scanned. Other pages not claimed read.','Author preprint11Oct2001; later JNT98(2003). Universal Tate/descent/normal quintic comparison, not publisher-PDF identity.'),
 'fisher2008':('Physical1–2,9 (Theorem4.4) read; whole extract keyword-scanned.','2006arXiv version of later2008journal paper; general invariants/Jacobian framework for normal models.'),
 'fisher2013':('Physical1–4 read; whole extract keyword-scanned.','2011arXiv version of later2013journal paper; normal quintic/Pfaffian/full-level framework.'),
 'consani2001':('Physical1–2,4–5,8–9 read; whole extract keyword-scanned; not all50pages read.','2000arXiv manuscript of later quintic-threefold paper; old pentagonal line geometry, different fibers including genus6.'),
 'morton2016_v1':('All10text pages read; original pixels physical3,4,5 inspected.','Direct earliest inspected Morton table/radical/product formulas; displayed v1 date19Dec2016.'),
 'morton2018_v4':('All19text pages read; original pixels physical5,6,7,18 inspected.','Expanded universal coordinate formulas and generic field recovery; displayed v4 date11Jun2018 distinct from2022PDF build.'),
 'morton2019_repository':('Whole extracted text compared after whitespace normalization with fully read v4; PDF not separately visually read.','Computed text equality, different bytes; journal version-of-record identity not established.'),
 'verdure2006':('All18original pages visually read. Text extraction is nearly empty and was not treated as a full reading.','Published IJPAM33(1)(2006)75–92; Theorem5/p84, Proposition3/Corollary1/p80–81 and specialization proof/p84–88.'),
 'explicit_descent1':('Physical1–2 read; whole extract keyword-scanned.','General explicit n-descent introduction only; not a whole37-page exclusion.'),
 'cullinan2022':('Physical1–2,28–33 read (operative printed67–72); whole extract keyword-scanned.','51PDFpages=cover+50article pages; Lemma4.3.3 old universal5-isogenous Kummer field overQ, distinguish candidate base/twist.'),
 'mccallum1988_pdf':('Original pixels physical2–5,31 read (printed637–640,666). Not all30article pages read.','31PDFpages=metadata/terms cover+30article pages; original title curve, correcting index curvature.'),
 'bhakta2023':('Physical1–5,38 read; whole extract keyword-scanned. Not all39pages read.','Published author-deposited Wiley article; p5 cites AIM Questions23,33, different target.'),
 'aim_html':('Question17 and all four remarks read in operative HTML; surrounding source-version context inspected.','Current display matches original question mathematically; no current-openness certificate.'),
 'fisher_page':('Current bibliography titles/publication fields read, including final update26June2026.','Author bibliography/version leads, not full reading of every listed paper.'),
 'morton_metadata':('Submission history/journal-reference metadata read.','v1 19Dec2016; v2 31Dec2016; v3 31May2018; v4 11Jun2018; journal2019 distinct.'),
 'fisher2008_metadata':('Submission history/journal-reference metadata read.','10Oct2006arXiv submission, later2008journal.'),
 'fisher2013_metadata':('Submission history/journal-reference metadata read.','16Oct2011arXiv submission, later2013journal.'),
 'consani_metadata':('Submission history metadata read.','13Sep2000arXiv submission, not later journal/publication-PDF identity.'),
 'mccallum1988_eudml':('Bibliographic metadata and original-source link read.','Index title typo corrected using original pixels; index not a theorem source.'),
 'mccallum1988_gdz':('Full short HTML inspected to ground IIIF manifest link.','Library source navigation; not article reading.'),
 'mccallum1988_manifest':('Article-specific sequence/rendering URL extracted from complete JSON.','Thirty article canvases identified; structural machine inspection rather than manual full870KBreading.'),
 'upstream_research_results':('Selected target report object parsed and fully read; whole80MBdataset not manually read.','Pinned upstream report semantically equal to current imported record and reconstructs legacy26340byte/hash under stated serialization.'),
 'upstream_problems':('Selected id20000450 object parsed/read; whole68MBdataset not manually read.','Pinned target semantics equal current source payload; separate historic6071-byte wrapper not reconstructed.'),
 'github_pr329':('PR metadata state/times/head/base read.','Historical author/committer/PR fields distinct from first-publication proof.'),
 'github_pr329_commits':('Both returned commit metadata objects read.','Two exact public candidate commits; no first-push timestamp established.'),
 'github_commits329':('Returned empty default-branch path-history list inspected.','No claim target absent from PR or all refs.'),
 'github_releases':('All28returned names, bodies and asset names machine-scanned; names/date fields read.','No target-pattern metadata match; archive contents not searched.'),
 'github_releases_page2':('Returned empty list inspected.','Page1 complete for this returned endpoint at retrieval, not all possible archives.'),
 'zenodo_repo_search2':('Both returned records metadata inspected.','Known repo concept/latest version plus unrelated preprint; not universal author archive census.'),
 'zenodo_repo_versions':('All19returned version metadata inspected.','Known concept versions latest7Sep2026; deposited file contents not inspected.'),
 'zenodo_exact_target':('Returned record title/metadata inspected.','One unrelated record has numeric Zenodo id20000450; not a zero-hit result and not mathematical target.'),
 'zenodo_pentagonal_torsion':('All25returned metadata titles inspected, plus metadata machine scan.','Total32; page2 separately retrieved. No exact pencil answer identified in inspected metadata; deposited papers not read.'),
 'zenodo_pentagonal_torsion_page2':('All7returned metadata titles inspected.','Completes32metadata titles for this query; not full deposited-source reading.'),
 'gh329_first_tree_noslash':('All12returned top-level entries inspected.','First commit file inventory; all4scientific bodies separately retrieved.'),
 'gh329_head_tree_noslash':('All16returned top-level entries inspected including review directory.','Second commit adds ancillary material; snapshot21attempt files includes review descendants.'),
}
sources=[];private=[]
for rp in sorted(P.glob('*/retrieval.receipt.json')):
 d=rp.parent;r=json.loads(rp.read_text());su=json.loads((d/'SUMMARY.json').read_text())
 b=(d/'source.bytes').read_bytes() if (d/'source.bytes').exists() else None
 pg=None
 if (d/'pdfinfo.stdout').exists():
  m=re.search(r'^Pages:\s+(\d+)',(d/'pdfinfo.stdout').read_text(),re.M);pg=int(m.group(1)) if m else None
 scope,role=scopes.get(d.name,('',''))
 if d.name.startswith('gh329_') and not scope:
  if r['actual_exit_code']==0:
   scope='Entire raw scientific body retrieved and byte-compared against released snapshot; mathematical reading was from frozen snapshot.'
   role='Exact public first/head candidate version comparison.'
  else:scope='Native failed access preserved; no body read.';role='Trailing-slash redirect lost ref on initial attempts; corrected no-slash first/head access succeeded. Exact base-path404 remains bounded API evidence.'
 if d.name=='zenodo_repo_search':scope='Native failed request400/curl22 preserved; no records read.';role='Corrected query/size subsequently succeeded; no zero-hit inference.'
 assert scope,(d.name,'missing scope declaration')
 row={'id':d.name,'canonical_url':su['url'],'retrieval_started_utc':r['started_utc'],'retrieval_finished_utc':r['finished_utc'],'actual_native_exit_code':r['actual_exit_code'],'actual_http_status_from_curl':su['http_status'],'retrieved_source_bytes':len(b) if b is not None else None,'source_sha256':sha(b) if b is not None else None,'actual_pdf_page_count':pg,'read_scope':scope,'operative_role_or_limit':role,'evidence_type':'native retrieval receipt; read scope separately declared','raw_source_publicly_exported':False}
 sources.append(row)
 private.append(row|{'receipt_path':str(rp.relative_to(S)),'receipt_sha256':sha(rp.read_bytes()),'raw_source_path':str((d/'source.bytes').relative_to(S)) if b is not None else None,'source_mode_decimal':(d/'source.bytes').stat().st_mode&0o777 if b is not None else None,'actual_effective_url_kept_private':su.get('url_effective')})
orig={'id':'original_aim_pdf_source_stage','canonical_url':'https://www.aimath.org/WWN/qptsurface2/qptsurface2.pdf','source_sha256':'8b64d2f6b91f791c35afae10b2ef79c15a927a94c2142a56386f80c8b8a596e6','retrieved_source_bytes':502057,'actual_pdf_page_count':59,'read_scope':'Original operativeQuestion17/all4remarks physical51 in pixels; sourcecover1 and contextual45 pixels; text1,2,44,45,50,51,52. Not all59pages read. Frozen source-only ledger supplies exact primary retrieval receipt.','operative_role_or_limit':'Workshop11–20Dec2002, PDFversion22Nov2004; old known∞subgroup distinct fullkernel.','raw_source_publicly_exported':False}
original_receipt=json.loads((S.parent/'private_source_evidence/official_current.retrieval_receipt.json').read_text())
orig.update({'retrieval_started_utc':original_receipt['started_utc'],'retrieval_finished_utc':original_receipt['finished_utc'],'actual_native_exit_code':original_receipt['exit_code'],'actual_http_status_from_curl':200,'evidence_type':'Independent native original-source retrieval in unchanged source-only freeze; read scope separately declared'})
dump(S/'SOURCE_INVENTORY.json',{'schema':'pr329-public-source-inventory-v1','scope':'Canonical primary source metadata and brief paraphrased read scopes only. No private raw sources or complete transcription exported. Failed attempts remain explicit.','source_count':len(sources)+1,'sources':[orig]+sources})
dump(P/'NATIVE_SOURCE_RECEIPT_INDEX.json',{'kind':'computed_index_of_genuine_native_receipts_not_itself_exit_receipt','sources':private})
reading=[{k:x.get(k) for k in ['id','source_sha256','actual_pdf_page_count','read_scope','operative_role_or_limit']} for x in [orig]+sources]
dump(S/'READING_LEDGER.json',{'schema':'pr329-paraphrased-reading-ledger-v1','reading_is_not_rendering':'Actual native retrieval/render receipts do not by themselves establish reading. Agent text/pixel inspection declared separately; no whole-read claim from a scan or keyword search.','frozen_source_baseline':'Unchanged source-only freeze completed09:21:24.927608UTC before candidate exposure; first-candidate freeze09:42:25.906544UTC before ancillary/imported/literature.','identity':'Existing PR344 child identity reused because new-agent creation failed thread limit; no PR344 scientific verdict transferred and no PR329 candidate was read before explicit release.','entries':reading,'candidate_scopes':{'original_scientific_files':'Four released files fully read before first-candidate freeze; all21attempt files subsequently fully read.','imported_report':'Selected report fully read with bounded rereads following combined-output truncation.','root_sibling_verdicts':'Mathematical gate reported by parent; not treated as independent priority source or transplanted acceptance.'},'visual_scopes':{'verdure2006':'All18original pages','morton2016_v1':'3,4,5','morton2018_v4':'5,6,7,18','fisher2001':'physical4,5,26,27','mccallum1988_pdf':'physical2,3,4,5,31','original_aim':'physical1,45,51'},'publication_authorization':False})
queries=[
 ['"pentagon" "5-torsion" McCallum','"P" "circle" "quintic" McCallum elliptic','"regular pentagon" "elliptic curve"','"Some examples of 5 and 7 descent" Fisher2001'],
 ['"pentagonal" "torsion" elliptic McCallum','"pentagon" "quintic" "McCallum"','"regular pentagon" "torsion"','"Cassels-Tate pairing and the Platonic solids" Fisherpdf'],
 ['"pentagonal pencil" elliptic torsion','"pentagonal quintic" torsion','"McCallum" "pentagon" elliptic','"Tate normal form" "5-torsion" radical division field'],
 ['"Lagrange resolvents and torsion of elliptic curves" Verdurepdf','"McCallum" "pentagon" "quintic"','"regular pentagon" "P +" "torsion"','"pentagonal quintic" "5" elliptic'],
 ['"McCallum" "pentagon" "elliptic"','"circumcircle" "quintic" "torsion"','"pentagonal" "quintic" "torsion"','"qptsurface2" "Question 17" torsion'],
 ['"McCallum" "pentagon" "5"','"pentagon" "circle" "X_1(5)"','"McCallum" "quintic" "torsion"','"pentagonal" "quintic" "elliptic curve"'],
 ['"McCallum" "pentagon" mathematics -Martha -Kristy -military -Navy -Army -podcast','"quintic" "circumcircle" elliptic','"pentagon" "genus one" torsion','"pentagonal" "division field"'],
 ['"quintic" "5phi" torsion','"pentagon" "lambda" "Tate"','"McCallum" "qptsurface2" solution','"20000450" "torsion"'],
 ['"The elliptic sieve and Brauer groups" arxiv','"pentagonal" "elliptic" McCallum Fisher circle','"regular pentagon" torsion']]
findings=['OriginalAIM/Fisher leads; snippets not verdicts.','Originalquestion and generaldescent leads.','MaterialMorton andCullinan primary leads, subsequently retrieved/read in scope.','Verdure original concrete lead, subsequently fully visually read.','No inspected exactcompletepencil answer; searchresult absence not firstness.','No inspected exactcompletepencil answer; generic matches not target.','Broad noisefiltered model/field query, bounded indexed coverage.','Concrete newerAIMciting Bhakta lead; subsequently primaryp5 shows Questions23,33, not17.','Bhakta official primary retrieved; domains on query2 arxiv.org/aimath.org/cam.ac.uk, query3 arxiv.org/cam.ac.uk/math.arizona.edu.']
web=[]
for i,(qs,f) in enumerate(zip(queries,findings),1):
 p=P/f'web_search{i:03d}.json';b=p.read_bytes();x=json.loads(b)
 web.append({'id':f'web_search{i:03d}','query_text_from_retrospective_working_record':qs,'request_limit':'Original request JSON was not stored with these tool results; retrospective transcription is not a byte-certified request receipt.','tool_evidence_sha256':sha(b),'tool_evidence_bytes':len(b),'stored_json_type':type(x).__name__,'query_execution_utc':'Exact invocation time not recorded in stored web-tool result; not reconstructed as a native receipt.','capture_file_mtime_utc':datetime.fromtimestamp(p.stat().st_mtime,timezone.utc).isoformat(),'mtime_limit':'Filesystem metadata for stored evidence, not tool execution/start timestamp.','evidence_kind':'tool-level web results, not genuine native process receipt','inspection_and_result_limit':f,'full_result_display':'Several combined outputs truncated; complete tool-return serialization retained privately. Only actual primary reading supports scientific verdicts.'})
dump(S/'SEARCH_INVENTORY.json',{'schema':'pr329-bounded-search-inventory-v1','coverage_date_utc':'2026-10-04','query_count':sum(map(len,queries)),'methods':['Exact problem phrases and variants','Model/torsion/field words','Cited-source and stronger-universal-theory chase','Primary original reading and version comparison','CurrentofficialAIM/currentauthorbibliography','Readonly repository andZenodo metadata inspection'],'web_searches':web,'native_repository_and_archive_queries':[{'source_id':x['id'],'url':x['canonical_url'],'actual_started_utc':x['retrieval_started_utc'],'actual_finished_utc':x['retrieval_finished_utc'],'exit_code':x['actual_native_exit_code'],'http_status':x['actual_http_status_from_curl'],'scope':x['read_scope'],'limit':x['operative_role_or_limit']} for x in sources if x['id'].startswith(('github_','gh329_','zenodo_'))],'verdict_boundary':'No earlier complete exact-pencil answer found in actually inspected sources. No first-discovery/application, archive-absence or continuing-open certificate. Unread snippets and inaccessible/unretrieved sources remain leads.'})
print(json.dumps({'native_source_rows':len(sources),'public_sources_including_original':len(sources)+1,'public_web_query_count':sum(map(len,queries)),'failures':[(x['id'],x['actual_http_status_from_curl'],x['actual_native_exit_code']) for x in sources if x['actual_native_exit_code']!=0],'pdf_pages':{x['id']:x['actual_pdf_page_count'] for x in sources if x['actual_pdf_page_count'] is not None}},indent=2))
