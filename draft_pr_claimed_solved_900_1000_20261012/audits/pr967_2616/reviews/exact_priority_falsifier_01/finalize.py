from pathlib import Path
import json,hashlib,datetime,base64
O=Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012/audits/pr967_2616/reviews/exact_priority_falsifier_01')
def sha(b):return hashlib.sha256(b).hexdigest()
def write(n,s):(O/n).write_text(s.strip()+'\n')
def jwrite(n,x):write(n,json.dumps(x,indent=2))
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
current=(O/'private/primary_current.pdf').read_bytes();archive=(O/'private/archive_20261002.body').read_bytes()
cdx=json.loads((O/'private/ia_cdx.body').read_bytes());entry=dict(zip(cdx[0],cdx[1]))
assert archive==current
assert sha(archive)=='eb095248a64ebe4a52ea2cd32b40012cefc03b18475c5432c58747febc4e5de7'
assert base64.b32encode(hashlib.sha1(archive).digest()).decode().strip('=')==entry['digest']
assert (O/'private/primary_p60.txt').read_bytes()==(O/'private/archive_p60.txt').read_bytes()
capture=datetime.datetime.strptime(entry['timestamp'],'%Y%m%d%H%M%S').replace(tzinfo=datetime.timezone.utc)
commit=datetime.datetime.fromisoformat('2026-10-07T21:42:54-07:00')
assert capture<commit
jwrite('ARCHIVE_CONTENT_VALIDATION.json',{'actual_utc':now,'capture_utc':capture.isoformat(),'submitted_commit_author_and_committer_utc':commit.astimezone(datetime.timezone.utc).isoformat(),'capture_precedes_submitted_timestamp':True,'elapsed_seconds':(commit-capture).total_seconds(),'current_archive_exact_byte_equality':True,'both_pdf_bytes':len(archive),'both_pdf_sha256':sha(archive),'computed_sha1_base32':entry['digest'],'cdx_digest_matches':True,'current_and_archive_p60_extract_equal':True,'scope':'content identity and recorded provider chronology; mathematical validity separately assessed in INDEPENDENT_ASSESSMENT.md','limitation':'October 2 archive; no September content-fixed archive obtained; no independently notarized conception date or ultimate priority claim'})
privatefiles={str(p.relative_to(O)):{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted((O/'private').rglob('*')) if p.is_file()}
jwrite('SOURCE_COVERAGE.json',{'actual_utc':now,'scope':'PR967/2616/21.107 only','submitted_head':'b356dec5cb01e5f536b9cfeece56ad08844c03cb','original_26_identity_checks':'INTAKE_AUTHENTICATION.json and FINAL_AUTHENTICATION.json; no full review claim for all26','mathematics_read':[{'source':'submitted author/public/REPORT.md','coverage':'complete report, all sections','sha256':'ddde58f03f320c881b78e59b60a40f315e1811c7c88aaa25ce620c427afbb6ca'},{'source':'official and archive Results on problems from the Kourovka Notebook','coverage':'complete Section3.44, printed/PDFp60; both extracted and rendered, both images personally inspected; title and PDFmetadata checked','sha256':sha(current)},{'source':'official arxiv1401.0300v47','coverage':'target21.107 and exact cited mathematics-PDF URL on p193; submissionhistory forv47; other problem proofs not assessed','sha256':'a93b2d27c3f6dcba3103450a2e56ca083377a7431bec04fbc75bff025f145e76'}],'chronology_sources':['FETCH_PRIMARY_RECEIPT.json','CHRONOLOGY_REQUEST_RECEIPTS.json','ARCHIVE_FETCH_RECEIPT.json','ARCHIVE_CONTENT_VALIDATION.json'],'external_searches':[{'queries':['"Kourovka" "21.107-proof.md"','"Results on problems from the Kourovka Notebook" "September"'],'outcome':'No additional primary fixed-source lead used; tertiary results and unrelated problem snippets excluded as mathematical evidence.'}],'fresh_family_reports_read':[],'root_conclusions_read':[],'private_source_artifacts':privatefiles,'source_artifacts_public_seal_status':'All source PDF/HTML/rawresponse/extract/image contents remain private; this coverage file and public receipts seal their bytes/hash metadata.'})
write('CHRONOLOGY.md',r'''
# Chronology adjudication

This chronology is independently obtained. Detailed actual request/completion UTC, HTTP status, response headers, sizes, and hashes are in the three receipt files. The decisive equality and timestamp comparison are in ARCHIVE_CONTENT_VALIDATION.json.

- September19 manuscript date and PDFCreationDate: ordinary mutable bibliography, not a historical body pin.
- September24 official current Last-Modified: a mutable server assertion, not by itself a proof of which bytes existed then.
- September30 12:35:42Z arxiv1401.0300v47: official fixed version cites the exact linked PDF URL. It does not fix the linked body or endorse21.107.
- October2 01:45:49Z InternetArchive capture: direct raw replay is the complete 598093-byte currentPDF, SHA256eb095248a64ebe4a52ea2cd32b40012cefc03b18475c5432c58747febc4e5de7. The replay's computedSHA1 matches theCDX digestD23DOIESSOEFBPQ4OTLTGP2BK44U6R6G. Page60 was independently rendered and visually read. This supplies a fixed historical copy of the exact proof before the submitted commit's stated time.
- October8 04:42:54Z: submittedGitcommit author/committer timestamp (October7 21:42:54−07:00). These timestamps do not themselves notarize when a proof was conceived.

Archive raw URL: https://web.archive.org/web/20261002014549id_/https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/09/kourovka-mathematics.pdf

Independent attempts and negative evidence: official repository200 (generic link present); officialarxivabs200 andPDF200; WaybackavailabilityAPI200 but empty archived_snapshots at requestedtimestamp20261007; WaybackCDX200 withOctober2capture; rawarchive200 with matchingbody; WordPresswp-jsonmediaroute404. The emptyavailability result is retained, not interpreted as absence after a successful directcapture. NoSeptemberbodycapture obtained. No circumvention, installs, contact or preparedcontact occurred.

No ultimatefirstness, author-knowledge, dependence or misconduct inference is made. This record establishes a bounded earlierpublic-equivalent-result finding with ordinary archival trust, not cryptographic notarization of all possible historical events.
''')
write('ADVERSE_FINDINGS.md',r'''
# Adverse findings and limitations

The adverse-priority lead survives direct falsification attempts: the exact countably infinite Hausdorff ZFC target is settled by the complete earlier source. Its core mechanism is the same as the submission. The source's AI association and proposed-answer label provide no reason to ignore a complete proof.

The original chronological weakness was real: a September label, mutable Last-Modified, and immutable citation of aURL alone do not pin itsbody. This review separately obtained an October2 raw archivedPDF with exactbyte identity andCDX digest agreement, sufficient to put the completebody before the submission's statedOctober7/8 timestamp. NoSeptembercontent archive is asserted.

One misleading negative record is preserved: the Waybackavailability query returned no nearestsnapshot althoughCDX and directreplay succeeded. ThatAPI response is not an absence proof. This audit does not claim the repository's generic link was target-indexed, editor-accepted, or refereed. It does not establish ultimate firstdiscovery, what the candidate author knew, or copying.

There is no identified repair of the current submission that turns this exact existing result into a new solution of the original unsolvedproblem. Attribution/rediscovery relabeling can correct presentation, but cannot supply the requested novelty. No unrelated newresearch program was invented as a salvageclaim.

All26 submitted files were authenticated, twice. Mathematical review here covers only the complete candidateREPORT and complete primarySection3.44, with chronology records. It gives no wholepackageclean credit.
''')
write('RESEARCH_LOG.md',f'''
# Research log

All work stayed in this dedicated directory. NoGit/index/ref/config mutation, publication, outreach, preparedoutreach, install, or action on anyPR occurred. No other fresh family report or root conclusion was read. The parent task supplies this restricted scope, overriding general checkpointpublication instructions for this subtask.

| ActualUTC | Checkpoint | Bestguess completion |
|---|---|---|
| 2026-10-16T20:49:31.560502Z | RecordsfileSHA and all26 Git/diskbytes and modes authenticated before candidateintake | 20% |
| 2026-10-16T20:49:46.680276Z | CurrentprimaryPDF fetched and pinned; p60 extracted/rendered for completeSection3.44 inspection | 45% |
| 2026-10-16T20:50:22.265181Z | OwnCDX request completed with anOctober2capture; other independentchronology requests recorded, including negativeavailability | 70% |
| 2026-10-16T20:50:52.331549Z | RawOctober2archive retrieved; contentSHA andCDXdigest match; archivedp60 subsequently personally visuallyinspected | 85% |
| 2026-10-16T20:52:23.527508Z | Independentassessment written andSHAsealed before any otherfamily/rootintake; all listed mathematicaledgecases checked | 95% |
| 2026-10-16T20:52:40.651964Z | Original26 reauthenticated after review; nochange | 99% |
| {now} | Finalsourcecoverage, chronologyvalidation, adversefindings and publicsealing prepared | 100% |

Percentages measure this audit's taskcompletion; they are not probabilities of truth or completion of the broader researchgoal. Earlier entries are retrospective log entries grounded in timestamped receipts. Fullproof reasoning is in INDEPENDENT_ASSESSMENT.md, preserved unchanged at the independentphaseboundary. The finalmanifest excludes itself and all private sourcecontents, and binds an explicit exact publicallowlist.
''')
write('REPORT.md',r'''
# Exact-priority falsification review

Independent finding: the earlier primarysource contains a complete ZFC counterexample to the exactcountableHausdorff21.107 target. A directlyretrieved InternetArchive capture dated2026-10-02T01:45:49Z is byteidentical to the inspected current598093-bytePDF, SHA256eb095248a64ebe4a52ea2cd32b40012cefc03b18475c5432c58747febc4e5de7. ItsSHA1 matches theCDX digest. This fixes the completeproof before the submittedcommit's stated2026-10-08T04:42:54Z timestamp.

The submittedcandidate uses the samegroup, topology, densepartition and maxima/thinning/parity argument. No mathematicalfalsifier or noveltypreserving repair of this current result was found. Attribution/rediscovery relabeling does not supply a novel solution of the original unsolvedproblem. No ultimatefirstness, dependence or misconductclaim is made.

Read INDEPENDENT_ASSESSMENT.md for the full quantifiedclaim, alltopology/density/empty/identity/maxfiber/thinning/parity/fixedopen checks, and limitations. INDEPENDENCE_PHASE_BOUNDARY.json seals that assessment before otherfreshfamily/rootintake; none was later read. SOURCE_COVERAGE.json distinguishes exact26-file identityauthentication from the deliberatelynarrow substantiveproofcoverage. All26 were reauthenticated at end.

CHRONOLOGY.md, ARCHIVE_CONTENT_VALIDATION.json and rawfetchreceipts preserve the newarchive evidence and negativeattempts. ADVERSE_FINDINGS.md preserves gaps and adverseevidence. RESEARCH_LOG.md provides actualUTC and checkpointpercentages. SourcePDF/extract/imagecontents stayprivate. MANIFEST.json binds the exactpublicallowlist, excluding itself.
''')
print('prepared',now,'private artifacts',len(privatefiles))
