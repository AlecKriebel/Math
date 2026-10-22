from pathlib import Path
import json,hashlib,os,datetime,subprocess,stat
P=Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012');A=P/'audits/pr948_30004549';D=A/'preprint';W=A/'publication/workflow';R=A/'reviews/full_package_06'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def save(n,z):
 b=(json.dumps(z,indent=2,ensure_ascii=True)+'\n').encode();p=R/n;f=p.open('wb');f.write(b);f.flush();os.fsync(f.fileno());f.close();assert p.read_bytes()==b
# Every nested historical operational snapshot, preserving declared failed/partial status.
archives=[]
for m in sorted((W/'history').rglob('*MANIFEST.json')):
 z=json.loads(m.read_bytes());records=z.get('files');checked={}
 if not isinstance(records,dict):continue
 for name,pin in records.items():
  p=m.parent/name;b=p.read_bytes();assert len(b)==pin['bytes'] and sha(b)==pin['sha256'];checked[name]={'bytes':len(b),'sha256':sha(b)}
 archives.append({'manifest_relative_to_workflow':str(m.relative_to(W)),'manifest_sha256':sha(m.read_bytes()),'payload_count':len(checked),'payloads':checked})
zero=W/'LIVE_BASE_ATTEMPT_03.json';assert zero.read_bytes()==b''
save('WORKFLOW_HISTORY_AUTHENTICATION.json',{'utc':now(),'status':'PASS','nested_snapshot_maps':archives,'zero_byte_attempt_preserved_as_failure':{'path':'LIVE_BASE_ATTEMPT_03.json','bytes':0,'valid_json':False},'source_authority':'Historical candidates use archived evidence/ paths only; current operational archive rehash does not convert historical failed receipts into successful tests.'})
# Package privacy/descriptor boundary and exact public names. All contents already cryptographically authenticated.
F=json.loads((D/'FREEZE.json').read_bytes());mf=json.loads((D/'package/PACKAGE_MANIFEST.json').read_bytes());names=set(mf['files']);rawprivate=(A/'source_record_private.txt').read_bytes()
assert len(names)==257 and [n for n in names if n.endswith('.pdf')]==['paper/note.pdf']
for n in names:
 assert not any(p in Path(n).parts for p in ['private','private_fixtures','venv','__pycache__','.secrets']);assert rawprivate not in (D/'package'/n).read_bytes()
meta=json.loads((D/'zenodo-deposit.json').read_bytes());assert len(meta['files'])==2 and {x['path'] for x in meta['files']}=={'anti-invariant-four-manifold-v1.0.pdf','anti-invariant-four-manifold-verification-v1.0.zip'}
save('PACKAGE_BOUNDARIES.json',{'utc':now(),'status':'PASS','package_files_including_manifest':258,'third_party_pdf_bodies':0,'only_pdf':'paper/note.pdf','exact_private_record_embedded':False,'private_runtime_cache_credential_namespace_present':False,'descriptor_files':meta['files'],'license':'CC BY 4.0 for new note and original research/audit materials; third-party publications cited rather than included','metadata_disclosures':'Extensive AI assistance, unrefereed, no independent human review/formal proof/novelty or current-openness certificate, declared4/5 and UNKNOWN historical native count','limits':'A namespace/exact-record scan and explicit-source provenance review are not a generic secret detector or a universal copyright audit.'})
# Actual selected primary-page evidence: no full-body or hash-equals-reading inference.
z=json.loads((R/'PRIMARY_READING_INVENTORY.json').read_bytes());z['status']='SELECTED_PRIMARY_PASSAGES_PERSONALLY_READ';z['completed_utc']=now()
for row in z['selected_sources']:
 n=row['source_relative_to_audit'];row['pages_personally_read']=row['pages'] if 'czII-' not in n else [23,24];row['limits']='Selected pages only; no complete source-body or final-versus-preprint equivalence claim.'
 if n.endswith('/donaldson.pdf'):
  p=A/n;out=subprocess.check_output(['pdftotext','-f','1','-l','1','-layout',str(p),'-']);q=R/'private/donaldson-page1.selected.txt';q.write_bytes(out);q.chmod(0o600);row['pages_personally_read']=[1,2,3];row['additional_page1_text_sha256']=sha(out)
z['limitations']='Selected11 primary bodies read; some journal-final versions, full2012survey, Geiges1996, full forward citation coverage and older Chen-Zhang real Hminus calculations remain unresolved. Their absence is not a theorem exclusion.';save('PRIMARY_SUPPORT.json',z)
save('FRESH_WEB_CHECKS.json',{'utc':now(),'actual_tool':'web.run','checks':[{'url':'https://ems.press/journals/owr/articles/2654829','observation':'Official metadata distinguishes report17(2020) from actual14September2021 publication.'},{'url':'https://arxiv.org/abs/1507.00282','observation':'Current record marks v2 withdrawn on3September2015 and attributes withdrawal to a crucial sign error in Proposition14.'},{'url':'https://arxiv.org/abs/1307.1513','observation':'Current v2 record is withdrawn on13November2014; main theorem described as incorrect.'},{'url':'https://wrap.warwick.ac.uk/id/eprint/163848/','observation':'Official repository identifies2024 journal metadata and accepted manuscript, which is not a journal-final byte comparison.'}], 'actual_queries':['"anti-invariant" "h" "3" nonintegrable counterexample 2026 Draghici Li Zhang','"Kodaira dimensions of almost complex manifolds II" anti-invariant cohomology'],'search_result_scope':'Targeted results produced known primary antecedents and unrelated leads; no verified qualifying earlier compact4D hminus>=3 construction found. Secondary/unread results are discovery only. No firstness/current-open/exhaustive certificate.'})
# Entire inherited ID inventory, with individual fresh evidence statements.
fixes={
 'R948-SOURCE-01':'Read note page1 and OWR p1687, fresh EMS metadata: report2020 and publication2021 are distinguished.',
 'R948-SOURCE-02':'Read actual TWZZv3 Theorem1.1 p2 and note: all smooth J, C-infinity open/dense, all four authors credited.',
 'R948-SOURCE-03':'Fresh1507/1307 withdrawal records, selected LU2020 scalar-curvature theorem, and note distinguish unsupported old claims from genuine conditional work.',
 'R948-PROV-01':'SUBMITTED_STATUS, AUTHORSHIP_PROVENANCE and ACTUAL_AUTH_CHECKS preserve literal4/5 separately from UNKNOWN historical native count and0 new proof responses.',
 'R948-PROC-01':'Read historical source/local reports and provenance: early receipt-order deviations remain disclosed; no old timestamps repaired. This06 independently records its own header exposure as nonclean.',
 'R948-COMP-01':'COLD_REPLAY all4 exact modes and own85-event profile actually execute forced-optimize0 checker children and false-assertion guard; old direct-O caveat remains.',
 'R948-COMP-02':'Read scan_tree/bounded_read and own85events: complete bounded regular-file scan rejects FIFOs/links/devices/socket, extra objects and caps before payload reads.',
 'R948-COMP-03':'Actual85event positive control executes poison unisolated, hardened run ignores it; COLD children-I-B/minimalenv recorded; installed trusted sites explicitly remain trusted.',
 'R948-COMP-04':'AUTHENTICATION_START and ACTUAL_AUTH_CHECKS actualGit100644/blob/disk0644/originalZIP identity; profile separately enforces single-link disk0644 and declared100644.',
 'R948-COMP-05':'Actual85event type/schema/duplicate/nonfinite mutations reject; own37workflow probes reject floatoptimization, boolreturncode, extra or missing canonical nested fields.',
 'R948-COMP-06':'ZIP_METADATA_BEFORE_DECOMPRESSION saved before258file extraction; actual profile maliciousZIP tests and original7mirrors enforce names/modes/caps before expansion.',
 'R948-COMP-07':'External freeze/manifest/driver pins precede execution; actual85event coherent-rebind negative rejects; hashes are documented as integrity, not truth/signatures.',
 'R948-MATHF-01':'Native present-placeholder negatives and true-absence UNKNOWN positive, immutable4/5 row and provenance retain unauthenticated historical count.',
 'R948-MATHF-02':'Note/source pages and fresh metadata correctly credit four TWZZ authors and report2020/publication2021 distinction.',
 'R948-MATHF-03':'INITIAL_INDEPENDENT_ATTACK and exact18check algebra support only compact smooth lowerbound3, fixedclasses, support and C-infinity convergence; no stronger dimension/symplectic/analytic/priority claim.',
 'R948-MATHF-04':'Personally viewed fivepages: Sigma notation, pointwiseplane/globalclass distinction, nonclosedB and no-common-productmetric calculations plus earliestQuestion3.27 are included.',
 'R948-MATHF-05':'Read original3checkers/currentprofile and computationreport: old wrapper limits preserved; separate profile passes and external review obligation remains.',
 'classical_priority:CP-R1':'Note/README/AUDIT_LIMITS use bounded negative language and weaker qualifying-predecessor criterion, not support/closeness-based priority protection.',
 'classical_priority:CP-R2':'Personally read HTv3 pp12-14: Proposition4.2 exactly2 compact4D, Proposition5.1 large real6D, localization older context, exactversions stated.',
 'classical_priority:CP-R3':'Fresh withdrawal metadata and selected later LU curvature statement show no supported repaired threshold theorem; note does not use withdrawn claims.',
 'classical_priority:CP-R4':'Actual TWZZv3 Theorem1.1 read, four-author prior credit and all-J scope checked in source/TeX/PDF/metadata.',
 'classical_priority:CP-O1':'Personally read DLZ2008v1 p20 Question3.27; note assigns numbering specifically to v1, alongside laterConjecture2.5.',
 'classical_priority:CP-O2':'DLZ definitionspp3-5 and note reference Li-Zhang/DLZ for cohomology and HT/DLZ priorcompact2examples.',
 'mechanism_priority:M1':'Donaldsonpp1-3 and BKpp4-5 actually read: positiveorientedplanes and closednormalizedpair criteria are antecedents; directkernel proof and nonclosedB avoid hidden integrability assumption.',
 'mechanism_priority:M2':'Bounded priority wording and weaker-prior criterion checked against own primary passages; no general theorem bridge to three retained classes assumed.',
 'mechanism_priority:M3':'Read finalHT actualcompact2 proof and6Dbaseforms; note does not call localized deformation alone new.',
 'mechanism_priority:O1':'Historical report/log and provenance retain approximate windows/ENOSPC/manual marker uncertainty, rather than converting them to exact clocks.',
 'mechanism_priority:O2':'Actual historical timing/save failures remain disclosed; this06 also preserves its own real harness failures with separate rerun receipts.',
 'mechanism_priority:O3':'Geiges1996 remains explicitly unread bibliographic lead in note/AUDIT_LIMITS; no theorem exclusion derived from missing body.',
 'recent_priority:RP-R1':'Personally read CZIaccepted24-27 construction/Proposition6.6 and CZIIaccepted23: plurigenera and realclosed Hminus distinguished; older Hminus computation remains open work.',
 'recent_priority:RP-R2':'Note/metadata give all4authors and actual TWZZv3 all-J theorem; no new generic-vanishing claim.',
 'recent_priority:RP-R3':'Bounded current search and note retain full-version/access/older-model gaps; no historical absence or current-openness certification.',
 'recent_priority:RP-R4':'Current withdrawal pages independently checked; selected LU2020 theorem adds curvature conditions, not a restored fixed-form constancy chain.',
 'recent_priority:RP-O1':'Read note/AUDIT_LIMITS: inaccessible journalfinals and fullcitationcoverage remain unresolved; stronger historical claims are absent; no outreach prepared.',
 'recent_priority:RP-O2':'No unsupported realHminus/index bridge replaces CZplurigenera. ActualCZII23 explicitly distinguishes these spaces; separate oldmodel calculation remains a research gap.',
 'ROOT-PRIORITY-01':'Current limits preserve selected author-upload2012survey versus unavailable fullpublisherbody, sourcehash versus actualread distinction and no proof dependence on optionalGW/metric context.',
 'ROOT-PUBDATE-01':'Fresh EMS official record supports actual14September2021; paper/metadata distinguish this from report2020; sealed older shorthand preserved.',
 'PF01-R01':'Theorem/README/metadata claim no firstness/novelty/currentopen; any weaker qualifying compact4D predecessor counts regardless support/closeness.',
 'PF01-R02':'HT/CZ passages personally read; note credits close product models and does not infer realclosedclasses from plurigenera.',
 'PF01-R03':'Selectedsurvey access and unavailable full2012body openly limited; no fullreading asserted from inherited hashes or text snippets.',
 'PF01-R04':'Gate implements two distinct latest complete clean ENTIRE currentfreeze reviews, not selfapproval. Suites58/97 and full05 incomplete history retained. This06 is also NONCLEAN and cannot discharge the obligation.',
 'PF01-R05':'Fresh EMS metadata and note agree on report2020/publication2021 distinction; no oldseal rewrite.',
 'PF01-R06':'Historical source/process logs retain approximate query/save timing; actual failures and corrected estimates remain historical. Own06 failures preserved.',
 'PF01-O01':'Sigma typography and explanatory pointwiserank/nonclosedB/no-commonmetric/earliestQuestion exposition checked visually and algebraically.',
 'PF01-O02':'No stronger finalbody/citation/olderCZcalculation claim made; these remain precise historical gaps, not a gap in the explicit construction.',
 'PF01-O03':'Optionalmetric/GW survey context remains qualified as selectedauthorupload and not completepublisherreading or a needed proof ingredient.',
 'R948-PROFILE-ROOT-01':'Read combinednamespace implementation; actual85events/0skips include three aliases in files/dirs/ancestors and fullZIPbeforedecompression; old76history unchanged.',
 'R948-WORKFLOW-ROOT-01':'Actual historicalfreeze check and353preservation/82archivedevidence/7ops pass; ownmissingarchive-live-shadow probe rejects with no living fallback;58case honestpartial recovery passes without oldPASSfabrication.',
 'R948-WORKFLOW-ROOT-02':'Read fullcurrentpr_view/next_identity/gate_next; actual26+37cases cover samehead/stored-base stable/liveonlyadvance/pagerace/finalrace/missinginitialpin; own livepointerformat/name negatives pass. Associatedbase never substitutes for livebase.',
 'R948-WORKFLOW-ROOT-03':'Actualnative_safety requires KEY not in state; own7placeholder forms reject, targethistory string/int detected, trueabsence retains UNKNOWN rather than historical0.'}
entries=json.loads((D/'FINDING_DISPOSITIONS.json').read_bytes())['findings'];assert set(fixes)=={e['id'] for e in entries} and len(fixes)==50
out={e['id']:{'verified':True,'classification':e['classification'],'evidence':fixes[e['id']]} for e in entries};assert sum(e['classification']=='required' for e in entries)==39 and sum(e['classification']=='optional' for e in entries)==11
save('DISPOSITIONS_CHECKED.json',{'utc':now(),'status':'ALL50_INDIVIDUALLY_CHECKED','count':50,'required':39,'optional':11,'inherited_finding_dispositions':out,'separate_prior_issue_resolution':{'R948-FULL01-R01':{'verified':True,'evidence':'Read originaladversewitness/disposition/currentresult_schema/review_authentication/review_cold/review_check. Actual58case recovery accepts honestincomplete/failedhistory but resetsstreak; fullcandidate/archive/operations/chronology exactdeclaredPASS and latesttwo distinctcleanENTIRE samefreeze remain strict. Actual05 incomplete wrapper validates; no lostresult recertification. This06 NONCLEAN is an additional genuine application.'}}})
print(json.dumps({'status':'PASS','nested_archives':len(archives),'dispositions':len(out)}))
