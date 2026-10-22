from pathlib import Path
import json,datetime,os,hashlib
R=Path(__file__).parent;A=R.parents[1];D=A/'preprint';P=A.parents[1];W=A/'publication/workflow'
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def save(name,value):
 b=(json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode() if not isinstance(value,str) else value.encode()
 with (R/name).open('wb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 assert (R/name).read_bytes()==b
now=utc();freeze=json.loads((D/'FREEZE.json').read_bytes());families={}
for family in ['global_topology','local_geometry','source_scope','computation_family','mathematical_falsifier','classical_priority','mechanism_priority','recent_priority','priority_falsifier_01']:
 base=A/'reviews'/family;doc=json.loads((base/'MANIFEST.json').read_bytes());mapping=doc.get('payloads',doc.get('files'));records=mapping if isinstance(mapping,dict) else {x.get('path',x.get('file')):x for x in mapping};done={}
 for name,pin in records.items():
  b=(base/name).read_bytes();assert len(b)==pin['bytes'] and sha(b)==pin['sha256'];done[name]={'bytes':len(b),'sha256':sha(b)}
 families[family]={'manifest_sha256':sha((base/'MANIFEST.json').read_bytes()),'count':len(done),'files':done}
save('FAMILY_AUTHENTICATION.json',{'utc':now,'families':families,'payload_total':sum(x['count'] for x in families.values()),'status':'PASS_identity_not_truth'})
ledger={'recorded_utc':now,'timing':'Queries were actually executed after saved INITIAL_ATTACK and before this record. Exact per-query start/end clocks were not captured and are not reconstructed.','query_batches':[
 ['"anti-invariant" "h" "3" "nonintegrable" four manifolds integrability conjecture','"J-anti-invariant" "counterexample" integrability 2025 2026','"Chen" "Zhang" "Kodaira dimensions" "anti-invariant"','"Almost Complex Geometry" "33/2020" September 14 2021'],
 ['"h_J" "integrability" "counterexample" "2026"','"anti-invariant cohomology" "three" "compact" -site:researchgate.net -site:scispace.com','"anti-invariant" "integrable" "2025" "4-manifolds"','"anti-invariant" "integrable" "2026" "4-manifolds"']],
 'fresh_primary_metadata':[{'url':'https://ems.press/journals/owr/articles/2654829','finding':'Oberwolfach Rep.17(2020), published14September2021; bibliographic and actual publication years differ.'},{'url':'https://arxiv.org/abs/1507.00282v2','finding':'Withdrawn3September2015; stated sign error in Proposition14, not an applicable theorem.'},{'url':'https://arxiv.org/abs/1307.1513v2','finding':'Withdrawn13November2014; main theorem incorrect, not a constancy bridge.'},{'url':'https://arxiv.org/abs/1112.0768v3','finding':'Four authors Tan/Wang/Zhang/Zhu; v3 distinct from earlier dropped fixed-form claim.'},{'url':'https://arxiv.org/abs/1104.2511v1','finding':'Named DLZ conjecture source, primary retained body read at pp3-5.'},{'url':'https://arxiv.org/abs/1908.03016v3','finding':'Final arXiv version; retained pp12-14 actually read, not claimed journal-final body.'}],
 'search_result_use':'Primary mathematical bodies support theorem comparisons. Unrelated, secondary, same-project/AI derivative, and physical-spin nonintegrability results were not evidence for the target. No verified qualifying predecessor established by this bounded search.','weaker_predecessor_criterion':'ANY earlier compact smooth connected real-four-dimensional nonintegrable J with hminus>=3 qualifies, regardless support/closeness/topology/mechanism.','historical_gap':'No exhaustive absence, firstness, novelty or present-openness certificate; full2012survey/Geiges1996, some journal-final comparisons, full forward citations and older CZ realHminus remain incomplete.'}
save('FRESH_WEB_CHECKS.json',ledger)
# Each inherited entry receives an independently assessed evidence statement, not a copied implementation-status grade.
E={
'R948-SOURCE-01':'Personally read MFO31 and fresh official EMS dates. note.tex context/reference separates report2020 from14September2021publication; no blanket2021error claim.',
'R948-SOURCE-02':'Personally read TWZZv3p2 Theorem1.1. note.tex names all four authors and the all-smooth-J open dense C-infinity statement.',
'R948-SOURCE-03':'Fresh arXiv1507v2/1307v2 withdrawals checked. note.tex and AUDIT_LIMITS exclude these claims; inspected LU2020 scalar-curvature hypotheses supply no threshold repair.',
'R948-PROV-01':'Actual immutable-head claimed_solved4/5 row and current remote main key-absence read in START. Provenance/metadata preserve declared4/5, historicalUNKNOWN, zero audit proof responses.',
'R948-PROC-01':'Read early local/source timing disclosures and mathematical_falsifier pre-intake record; new provenance retains both. Own START precedes math and own attack precedes prior substance; no old chronology rewritten.',
'R948-COMP-01':'Current four canonical cold receipts and85events show optimize0 checker children and rejected false assertion under outer O/OO; original auditA/B assertion weakness remains disclosed.',
'R948-COMP-02':'Read scan_tree/bounded_read and actual85event negatives for FIFO/socket/link/size/closed-inventory. They reject before reads; trust limits explicitly exclude a hostile OS sandbox.',
'R948-COMP-03':'Actual85event poison positive control executed when unisolated, hardened control ignored it. Current cold children -I-B use sanitized environment and fresh empty cwd; installed dependencies remain trusted.',
'R948-COMP-04':'Actual original_check24 Git/blob/tree100644/disk0644 plus ZIP comparison pass. Current tree files regular0644 singlelink;85events reject mode/hardlink mutation.',
'R948-COMP-05':'Read strict JSON/schema exact-int handling; actual85events and own31probes reject bool/float/malformed/nested canonical receipt substitutions. Exact primitive types retained.',
'R948-COMP-06':'Actual inspect_archive validates258outer members and7historical mirrors. ZIP_METADATA and own implied-directory-alias probe establish pre-decompression namespace rejection;85events cover bounded malicious metadata.',
'R948-COMP-07':'Externally supplied freeze/manifest/verifier pins authenticated before execution. verify compares external raw envelope SHA before parsing;85events reject coherent rebound without that anchor. No signature/truth inference.',
'R948-MATHF-01':'Actual immutable4/5 row plus current-key absence and new docs preserve distinction: current absence does not authenticate historical count. Own native placeholders/history probes pass with UNKNOWN positive control.',
'R948-MATHF-02':'Full note/metadata generic credits and EMS date distinction checked against primary passages/current official metadata. Original files and old shorthand preserved.',
'R948-MATHF-03':'Own INITIAL_ATTACK, exact full-cutoff/global proof and mathematical scripts verify only claimed smooth compact family/lowerbound. Paper excludes exacth/fixedsymplectic/analytic/firstness claims.',
'R948-MATHF-04':'Sigma notation, globalclasses-versus-pointwiseplane paragraph, nonclosed normalizedB and specified-product commonmetric contradiction personally read and independently derived;2008v1Q3.27 personally checked.',
'R948-MATHF-05':'All24 original bytes/wrapper unchanged; computation family seven weaknesses read. Current profile is separate, independently reproduced85events/fourcold. Future acceptance external to closed package.',
'classical_priority:CP-R1':'Any qualifying compactNI4D hminus>=3 counts. note/limits/metadata use bounded negative language; own primary/search work supplies no firstness or current-open certificate.',
'classical_priority:CP-R2':'Read HTfinalv3pp12-14: Proposition4.2 gives2; larger retained base2forms construction is6D. Note cites finalarXivv3, distinguishes noncompact and6D; localization alone not new.',
'classical_priority:CP-R3':'Actual withdrawal records and LU2020p13 read. The latter needs curvature equality; no unsupported corrected hminus theorem or fixedformconstancy route used.',
'classical_priority:CP-R4':'Actual TWZZv3p2 scope and allfourauthor metadata personally checked; new note/reference credit allfour.',
'classical_priority:CP-O1':'Actual DLZ2008v1p20 Question3.27 personally read; note assigns numbering to v1 and explicitly distinguishes shortened2010journalversion.',
'classical_priority:CP-O2':'New context/reference credits Li-Zhang and DLZ cohomology, with earlier compacthminus2examples. Primary DLZdefs/HTproposition support this bounded context.',
'mechanism_priority:M1':'Donaldsonpp1-3 and BKpp4-5 personally read. Note credits positiveplanes/closedpairs and supplies directkernelrealization. Own nonclosedB check shows normalizedclosedpair hypothesis fails.',
'mechanism_priority:M2':'Note/limits consistently avoid firstness/currentopen/novelty. No generalexistencetheorem is inferred from positiveplanes, upperbounds, semicontinuity or searchsilence.',
'mechanism_priority:M3':'Actual HTfinalv3 compact2/noncompact/6D distinctions checked. Removing a complexsurface base removes retainedholomorphic2forms, so no compact4Dbridge is silently presumed.',
'mechanism_priority:O1':'Read original timing/storage limits and later corrections; currentprovenance retains approximateclock and failedsave distinctions. Own queries have no invented perquerytimestamps.',
'mechanism_priority:O2':'Earlier sealed ENOSPC/approximate manual markers remain unchanged; later reauthentication does not backdate reading. Own actual failedattempts/source/reruns preserved distinctly.',
'mechanism_priority:O3':'Geiges1996 remains an explicitly unread bibliographic lead in note/limits. No result or exclusion from that body is asserted by me.',
'recent_priority:RP-R1':'Personally read CZIacceptedPDF24-27 and CZIIaccepted23-24: productplurigenera versus realclosedHminus distinction explicit; note credits them and leaves old-modelHminus calculation open.',
'recent_priority:RP-R2':'Fresh TWZZmetadata and retainedv3p2 support allfourauthor/allJgenericcredit in note and descriptor.',
'recent_priority:RP-R3':'Own boundedquery ledger and11selectedprimarybodies do not exclude all literature. Note/metadata preserve same weakness; weakerqualifyingpredecessor criterion used.',
'recent_priority:RP-R4':'Read fresh1307withdrawal and1112v3 droppedclaim comments. Currenttext does not restore withdrawnfixedFconstancy through distinct curvaturepapers.',
'recent_priority:RP-O1':'Unavailable finals/fullsurvey/Geiges/completecitations/oldCZrealcohomology remain explicit in AUDIT_LIMITS. No stronger historical claim or outreach prepared.',
'recent_priority:RP-O2':'No plurigenera/index-to-realclosedcohomology bridge assumed. OldCZI/CZIImodel analysis remains separate unfinished research rather than a falsely resolved priority exclusion.',
'ROOT-PRIORITY-01':'AUDIT_LIMITS and note distinguish earlier selectedauthorupload2012survey from unavailable fullpublisherbody, and43hashes versus18readings. My ownPRIMARY_SUPPORT claims only11selectedbodies, not inherited43fullreadings.',
'ROOT-PUBDATE-01':'Fresh officialEMS publication14September2021 with bibliographic17(2020) checked. Note/limits/metadata preserve exact distinction and addendum rather than rewrite oldseal.',
'PF01-R01':'Own weakerpredecessorcriterion and boundedprimaryaudit agree with cautiousnote/README/metadata. No novelty/currentopenness/exhaustiveabsence certificate.',
'PF01-R02':'HTfinalv3 and CZI/CZIIaccepted selectedprimaryconstruction/passages personally read. Appropriatecredit and unresolvedold-modelrealHminus caveat present in finalnote.',
'PF01-R03':'Read inheritedsurveyaccess and43versus18bodylimits; note does not claim fullpublisherread. Currentown11source selectedreading and associatedidentitymetadata distinguish hashes from understanding.',
'PF01-R04':'Exactcurrent review_check requires allnumberedhistory and two latestdistinctfullycompletecleanENTIREsamefreeze reviews; all50 and every earlierrequired+optional disposition required. Own58case rerun, actual6historyschemas verify rule; this entry verifies obligation, not future production acceptance.',
'PF01-R05':'FreshEMS date supports correctedreport2020/publication2021 narrative; newnote cites allfourTWZZauthors. Earlier sealed shorthand left unchanged.',
'PF01-R06':'Read timing/ENOSPC/processlimitations and actual latercorrections; no earlierfailedsave relabeledsuccess. Own twoauth/twohistory/general-matrix failures plus initialfixtureinterpretation preserved.',
'PF01-O01':'Sigma notation, globalrank2relation, no-common-productmetric and nonclosedB explanations independently checked, alongside earlier2008v1question.',
'PF01-O02':'Fullfinalbody/citation/oldCZrealHminus gaps remain actual disclosedhistorical limits. No universalabsence inference or outreach.',
'PF01-O03':'Optionalsurvey/GW context stays limited to selectedauthorupload reading and is unnecessary to explicitproof. No newfullbodyreading or sourceversionequivalence claimed.',
'R948-PROFILE-ROOT-01':'Read validate_namespace combinedfile/directory/impliedancestor routine; actual85events/0skips and ownZIPalias-before-open probe pass. Old76event implementation archived unmodified.',
'R948-WORKFLOW-ROOT-01':'Actualhistorical freeze authenticates262oldfiles/82archivedprivateevidence/7oldoperations and353preservation. Ownmissinghistoricalsnapshot probe reads onlyoldbase/evidence, neverlivingfallback.58case historyrepair permits honestfailed/incomplete rounds without cleancredit.',
'R948-WORKFLOW-ROOT-02':'ActualSTART associatedbase7431... differs fromcurrentlive37ec...; pr_view/next_identity/gate_next source inspected. Ownmalformedlivepointer cases plus actual26/37suites verify live-onlystableadvance/everypage/finalbracket, exactcompletecounts and no inventedinitiallivepin.',
'R948-WORKFLOW-ROOT-03':'Actualnative keyabsence baseline read at freshremoteMAIN; own6presentplaceholder/string-inttargethistory negatives and trueabsenceUNKNOWN positivecontrol pass. Source uses KEY not in state, so explicitnull cannot meanabsence.'}
assert len(E)==50
finding=json.loads((D/'FINDING_DISPOSITIONS.json').read_bytes());assert set(E)=={x['id'] for x in finding['findings']}
rows={x['id']:{'verified':True,'classification':x['classification'],'evidence':E[x['id']]} for x in finding['findings']}
save('DISPOSITIONS_CHECKED.json',{'utc':now,'inherited_count':50,'required':39,'optional':11,'dispositions':rows,'separate_prior_whole_review_issue':{'R948-FULL01-R01':{'verified':True,'evidence':'Actual current result_schema/review_authentication/review_cold/review_check permit honest historical incomplete/failed/nonPASS exactsubsets and resetstreak. Actual58case rerun covers recovery and falsePASS/missingoldarchive/evidence/helpers/chronology negatives. Actual six historical schemas pass;03/05 remainnonclean. No lost05 result recreated, no51st inheritedID.'}}})
log=(R/'RESEARCH_LOG.md').read_text()+f'\n- {now} — 85% complete. All corrected fourcold and fiveinert suites pass;85eventprofile/0skips, own12+8 mathematical groups and31directinert probes complete. Selected11primarybodies read, all5PDFpages viewed. Individually assessed50inherited+separateR01. Initial workflowfixture and defaultOSscratch boundary deviation preserved with correctedactualreruns; no candidateissue found. FinalactualEND/source-scope reassessment/schema/seal remain.\n'
save('RESEARCH_LOG.md',log)
print(json.dumps({'families':len(families),'payloads':sum(x['count'] for x in families.values()),'dispositions':len(rows),'required':sum(x['classification']=='required' for x in rows.values())}))
