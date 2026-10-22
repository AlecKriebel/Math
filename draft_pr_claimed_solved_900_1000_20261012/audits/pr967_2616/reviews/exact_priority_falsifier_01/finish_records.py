from pathlib import Path
import json,datetime,hashlib,subprocess
O=Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012/audits/pr967_2616/reviews/exact_priority_falsifier_01')
def sha(b):return hashlib.sha256(b).hexdigest()
def write(n,s):(O/n).write_text(s.strip()+'\n')
def jw(n,x):write(n,json.dumps(x,indent=2))
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
jw('POST_BOUNDARY_NOTICE.json',{'actual_utc_recorded':now,'notice':'Parent sent a primary-source archive lead, expressly not a verdict: its own GET at 20:53:02Z found the October 2 archive identical to the current PDF. It requested independent verification.','independence_check':'Our own archive fetch completed 20:50:52.331549Z; our unchanged independent assessment was sealed 20:52:23.527508Z. Both precede that parent GET and notification. No other family report or root disposition was read.','new_fact_from_notice_used_in_assessment':False,'qualification':'Parent availability query reportedly succeeded; ours returned empty. Own negative response remains preserved. Source body/time/section already independently authenticated before notice.'})
coverage=json.loads((O/'SOURCE_COVERAGE.json').read_text());coverage['post_boundary_parent_primary_notice']='POST_BOUNDARY_NOTICE.json; independently replicated earlier, no change to independent assessment';jw('SOURCE_COVERAGE.json',coverage)
write('REPORT.md',r'''
# Exact-priority falsification review

The earlier primary source contains a complete ZFC counterexample to the exact countable Hausdorff 21.107 target. A directly retrieved Internet Archive capture dated 2026-10-02T01:45:49Z is byte-identical to the inspected current 598093-byte PDF, SHA-256 eb095248a64ebe4a52ea2cd32b40012cefc03b18475c5432c58747febc4e5de7. Its SHA-1 matches the CDX digest. This fixes the complete proof before the submitted commit's stated 2026-10-08T04:42:54Z timestamp.

The submitted candidate uses the same group, topology, dense partition, and maxima/thinning/parity argument. No mathematical falsifier or novelty-preserving repair of this current result was found. Attribution or rediscovery relabeling does not supply a novel solution of the original unsolved problem. No ultimate-firstness, dependence, or misconduct claim is made.

Read INDEPENDENT_ASSESSMENT.md for the full quantified claim, topology/density/empty/identity/finite-fiber/thinning/parity/fixed-open checks, and limitations. INDEPENDENCE_PHASE_BOUNDARY.json seals that unchanged assessment before any fresh family report or root observation intake. A later primary-source notification from the parent is recorded in POST_BOUNDARY_NOTICE.json; this review's own archive retrieval and sealed assessment preceded it. No other family report or root disposition was read.

SOURCE_COVERAGE.json distinguishes 26-file identity authentication from the deliberately narrow substantive proof coverage. The original 26 files were reauthenticated after review. CHRONOLOGY.md, ARCHIVE_CONTENT_VALIDATION.json, and fetch receipts preserve the archive evidence and negative attempts. ADVERSE_FINDINGS.md preserves limitations. RESEARCH_LOG.md provides actual UTC and checkpoint percentages. Source PDFs, extracts, and images remain private. MANIFEST.json binds an exact public allowlist and excludes itself.
''')
write('CHRONOLOGY.md',r'''
# Chronology adjudication

This chronology was independently obtained. Detailed actual request/completion UTC, HTTP status, response headers, sizes, and hashes are in the three fetch receipt files. The decisive equality and timestamp comparison are in ARCHIVE_CONTENT_VALIDATION.json.

- September 19 manuscript date and PDF CreationDate: ordinary mutable bibliographic evidence.
- September 24 official current Last-Modified: a mutable server assertion; alone it does not fix a historical body.
- September 30, 12:35:42Z, arXiv:1401.0300v47: an official fixed version cites the exact PDF URL. This fixes the citation, not the linked body or an endorsement of 21.107.
- October 2, 01:45:49Z, Internet Archive capture: the direct raw replay is the complete 598093-byte current PDF, SHA-256 eb095248a64ebe4a52ea2cd32b40012cefc03b18475c5432c58747febc4e5de7. Its computed SHA-1 matches the CDX digest D23DOIESSOEFBPQ4OTLTGP2BK44U6R6G. Page 60 was independently rendered and visually read. This provides a fixed historical copy of the exact proof before the submitted commit's stated time.
- October 8, 04:42:54Z: submitted Git commit author/committer timestamp (October 7, 21:42:54-07:00). These timestamps do not notarize when a proof was conceived.

Raw archive URL: https://web.archive.org/web/20261002014549id_/https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/09/kourovka-mathematics.pdf

Own attempts: official repository HTTP 200, with generic link; official arXiv abstract and PDF HTTP 200; Wayback availability API HTTP 200 but empty archived_snapshots at timestamp=20261007; Wayback CDX HTTP 200 with October 2 capture; direct raw archive HTTP 200 with matching body; WordPress wp-json media route HTTP 404. The negative availability response remains preserved and is not interpreted as absence after a successful direct capture. No September body capture was obtained. No circumvention, installation, contact, or prepared contact occurred.

A parent primary-source notification arrived after the independent assessment was sealed; see POST_BOUNDARY_NOTICE.json. It does not supply the basis for this independent archive finding.

No ultimate-firstness, author-knowledge, dependence, or misconduct inference is made. This record establishes a bounded earlier-public-equivalent-result finding with ordinary archival trust, not cryptographic notarization of every possible historical event.
''')
write('ADVERSE_FINDINGS.md',r'''
# Adverse findings and limitations

The adverse-priority lead survives direct falsification attempts: the exact countably infinite Hausdorff ZFC target is settled by the complete earlier source. Its core mechanism is the same as the submission. The source's AI association and proposed-answer label provide no reason to ignore a complete proof.

The original chronological weakness was real: a September label, mutable Last-Modified, and immutable citation of a URL alone do not fix its body. This review separately obtained an October 2 raw archived PDF with exact byte identity and CDX digest agreement, placing the complete body before the submission's stated October 7/8 timestamp. No September content archive is asserted.

One potentially misleading negative record is preserved: the Wayback availability query returned no nearest snapshot although CDX and direct replay succeeded. That API response is not an absence proof. This audit does not claim that the repository's generic link was target-indexed, editor-accepted, or refereed. It does not establish ultimate first discovery, what the candidate author knew, or copying.

No repair of the current submission was identified that turns this exact existing result into a new solution of the original unsolved problem. Attribution or rediscovery relabeling can correct presentation but cannot supply the requested novelty. No unrelated research program was invented as a salvage claim.

All 26 submitted files were authenticated before intake and reauthenticated after review. Mathematical review here covers only the complete candidate REPORT and complete primary Section 3.44, with chronology records. It gives no whole-package clean credit.
''')
subprocess.run(['python3',str(O/'authenticate.py'),'POST_NOTICE_AUTHENTICATION.json'],check=True)
last=json.loads((O/'POST_NOTICE_AUTHENTICATION.json').read_text())['actual_utc']
write('RESEARCH_LOG.md',f'''
# Research log

All work stayed in this dedicated directory. No Git/index/ref/config mutation, publication, outreach, prepared outreach, installation, or action on any PR occurred. No other fresh family report or root disposition was read. The parent's restricted subtask scope overrides general checkpoint publication instructions here.

| Actual UTC | Checkpoint | Best-guess completion |
|---|---|---|
| 2026-10-16T20:49:31.560502Z | Records SHA and all 26 Git/disk contents and modes authenticated before candidate intake | 20% |
| 2026-10-16T20:49:46.680276Z | Current primary PDF fetched and pinned; page 60 extracted/rendered for complete Section 3.44 inspection | 45% |
| 2026-10-16T20:50:22.265181Z | Own CDX request completed with an October 2 capture; independent chronology requests preserved, including negative availability | 70% |
| 2026-10-16T20:50:52.331549Z | Raw October 2 archive retrieved; PDF hash and CDX digest match; archived page 60 subsequently visually inspected | 85% |
| 2026-10-16T20:52:23.527508Z | Independent assessment written and SHA-sealed before fresh family/root intake; all listed mathematical edge cases checked | 95% |
| 2026-10-16T20:52:40.651964Z | Original 26 reauthenticated after review; unchanged | 99% |
| {now} | Later parent primary-source notice recorded; own archive finding and unchanged assessment predate it | 99% |
| {last} | Original 26 reauthenticated again after that notice; unchanged; final records and public seal complete | 100% |

Percentages measure this audit's completion, not probabilities of truth or completion of the broader research goal. Earlier entries are retrospective log entries grounded in timestamped receipts. Full reasoning is in INDEPENDENT_ASSESSMENT.md, preserved unchanged at the independent phase boundary. The later parent notice supplies no new fact used by that assessment. Source contents remain private. The final manifest excludes itself and binds an explicit exact public allowlist.
''')
allowlist=[
'ADVERSE_FINDINGS.md','ARCHIVE_CONTENT_VALIDATION.json','ARCHIVE_FETCH_RECEIPT.json','CHRONOLOGY.md','CHRONOLOGY_REQUEST_RECEIPTS.json','FETCH_PRIMARY_RECEIPT.json','FINAL_AUTHENTICATION.json','INDEPENDENCE_PHASE_BOUNDARY.json','INDEPENDENT_ASSESSMENT.md','INTAKE_AUTHENTICATION.json','POST_BOUNDARY_NOTICE.json','POST_NOTICE_AUTHENTICATION.json','RESEARCH_LOG.md','REPORT.md','SOURCE_COVERAGE.json','authenticate.py','chronology_requests.py','fetch_archive.py','fetch_primary.py','finalize.py','finish_records.py','write_assessment.py']
assert len(allowlist)==len(set(allowlist)) and 'MANIFEST.json' not in allowlist
actual={p.name for p in O.iterdir() if p.is_file() and p.name!='MANIFEST.json'}
assert actual==set(allowlist),(actual-set(allowlist),set(allowlist)-actual)
phase=json.loads((O/'INDEPENDENCE_PHASE_BOUNDARY.json').read_text())
assert sha((O/phase['assessment_file']).read_bytes())==phase['sha256']
files={n:{'bytes':(O/n).stat().st_size,'sha256':sha((O/n).read_bytes())} for n in sorted(allowlist)}
m={'actual_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Independent exact-priority falsification, PR967/2616 only','files':files,'explicit_allowlist':sorted(allowlist),'file_count':len(files),'total_bytes':sum(v['bytes'] for v in files.values()),'allowlist_unique':True,'dictionary_keys_equal_allowlist':True,'manifest_self_excluded':True,'private_directory_excluded':True,'private_contents_covered_by_hash_metadata_in':'SOURCE_COVERAGE.json','independent_phase_assessment_sha256':phase['sha256'],'completion_percent':100}
jw('MANIFEST.json',m)
check=json.loads((O/'MANIFEST.json').read_text())
assert set(check['files'])==set(check['explicit_allowlist'])==actual
for n,v in check['files'].items():assert (O/n).stat().st_size==v['bytes'] and sha((O/n).read_bytes())==v['sha256']
print(json.dumps({'manifest_path':str(O/'MANIFEST.json'),'sha256':sha((O/'MANIFEST.json').read_bytes()),'file_count':len(files),'independent_phase_sha256':phase['sha256'],'completed_utc':m['actual_utc'],'completion_percent':100},indent=2))
