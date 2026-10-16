#!/usr/bin/env python3
"""Pin this authored audit without touching Git, queue records, or other shards."""
from pathlib import Path
import json,hashlib,datetime
BASE=Path(__file__).resolve().parent
AUDIT=BASE.parent
ROOTS=AUDIT/'root_source_reading'
PRIVATE=ROOTS/'private_reading'
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(name,obj):(BASE/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
original=json.loads((ROOTS/'PRIMARY_RETRIEVAL.json').read_text())
checks=[]
for obj in original['objects']:
    p=PRIVATE/obj['name'];actual=sha(p)
    checks.append({'name':obj['name'],'source_path':str(p),'url':obj['url'],'expected_sha256':obj['sha256'],'actual_sha256':actual,'bytes':p.stat().st_size,'match':actual==obj['sha256']})
assert len(checks)==6 and all(x['match'] for x in checks)
proof=AUDIT/'submitted/unsolved_math_prioritization/attempts/9700040/PROOF.md'
dump('INPUT_VERIFICATION.json',{'utc':now,'candidate_head_supplied':'0b4db59eb5515f2d90d8b8df33b6b729b78b48f1','candidate_proof':{'path':str(proof),'sha256':sha(proof)},'six_primary_pins_independently_hashed':checks,'all_match':True,'independence':'Initial mathematical reconstruction saved before inherited verdicts or other priority reports were read. Later sources and leads were read as hypotheses; other priority-family reports were not read.'})
source_records=[]
locs={
'left_Hamm.html':('Author webpage says posted February 2018; current content only, not an archival 2018 capture.','Full page','Exact source request and finite-k generator; live status is not a novelty test.'),
'patience1993.pdf':('Author webpage identifies these as unfinished unpublished 1993 notes.','§4.1 printed36–38; §4.2 printed39–40; dump47–48','Earlier stationary Gamma(B) representation, coupling, drift process. Printed transform has sign/initial-time defects; no literal reliance on them.'),
'ad1999.pdf':('Bulletin AMS36(1999),413–432; title page electronic publication21Jul1999.','§1.1–1.2; §2.1 printed418–419; §5.2 printed427','Pile tops equal insertion-tableau first row and finite RSK count; later fixed-left-pile context.'),
'okounkov-reshetikhin.pdf':('math/0107056v3,31Jan2003; v1 first6Jul2001; JAMS16(2003),581–603.','Complete relevant §§2.1–2.3; esp(7)–(14),Def1–2,Thm1','Exact ascending Schur specialization and normalizer, and full correlations. Automatic coverage follows after the explicit parameter mapping.'),
'schur-sampling.pdf':('Published MPRF24(2018),381–418; author-hosted print PDF.','§6 printed413–416; (6.2),(6.4),(6.6)–(6.8); full displayedp415 visually inspected','Exponential specialization and Poissonized RSK confirmation. Precise2015v2 source independently obtained below.'),
'ad1995.pdf':('PTRF103(1995),199–213.','Full 21 manuscript pages independently rendered and OCR-read; visual checks pp1,6,7; especially §2.2 and Lemma4','Published exact empty-Hammersley count equals LIS graphical representation, nearest-right rule, and simultaneous scaling; these premises support the elementary stationary-coordinate bridge. Ordinary spatial Poisson invariant law is distinct.')}
for x in checks:
    a,b,c=locs[x['name']]
    source_records.append({'id':x['name'],'url':x['url'],'path':x['source_path'],'sha256':x['actual_sha256'],'bytes':x['bytes'],'chronology':a,'read_locator':b,'coverage':c,'primary':True})
new=[
('borodin-olshanski-0402064.pdf','https://arxiv.org/pdf/math-ph/0402064v2','math-ph/0402064v2,29Sep2004; v1first24Feb2004; publishedAMS Translations217(2006),9–22','Full relevant §§1–3; all theorem statements and remaining scaling/results context read. Thm2.3,Remark1.5,Thm3.3 decisive.','Direct theorem identifies quadrant-PPP RSK path on C=(x,1); rates telescope exactly to candidate law; extended Bessel full barriers.'),
('betea-1407.3764v2.pdf','https://arxiv.org/pdf/1407.3764v2','1407.3764v2,14Sep2015;firstv114Jul2014','Complete §6 printed23–24;eq(6.2),(6.4),(6.6) and PoissonizedRSK','Confirms the explicit formula and full Schur construction predate 2018. Extraction warned on a repaired xref; displayed equations agree with published copy.'),
('nica-1404.4015.pdf','https://arxiv.org/pdf/1404.4015v4','Canonical v4,29Mar2017;SPA127(2),Feb2017,449–474; PDF title displays15Sep2021','§§1–3 includingfull relevant proof3.4 and §4Thm4.1/Remark4.2','Explicit full shape path. Do not use the displayed 2021 title date as a publication date; an earlier version source was authenticated.'),
('nica-1404.4015v3.pdf','https://arxiv.org/pdf/1404.4015v3','Canonical v3,29Apr2015;current PDF title displays15May2022','Theorem3.2,Remark3.3 printedp6 visually inspected; full §3.4 printedpp8–12 read','Same exact positive path formula; source right-branch exponent typo corrected by Remark3.3 and proof, explicitly recorded.'),
('thoma-1303.2794.pdf','https://arxiv.org/pdf/1303.2794v2','1303.2794v2,13Aug2013;firstv112Mar2013','§1.6 and complete §10 printed50–51; preceding relevantcontext','Confirms local-cover conjecture remains unproved there; boundary Plancherel degeneration alone is not rigorous local invariant theorem.')]
for name,url,date,loc,cov in new:
    p=BASE/'private_reading'/name
    source_records.append({'id':name,'url':url,'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size,'chronology':date,'read_locator':loc,'coverage':cov,'primary':True})
for name,url,date,loc,cov in [
('borodin_olshanski_2013.pdf','https://arxiv.org/pdf/1303.2795v1','12Mar2013,onlyv1','Full10-page note read;intro;Conj3.3;Claim4.2;Claim5.4;§6','Exact direct dynamics degeneration and one-row projection, but local stationarity is unproved; not counted as a theorem.'),
('young_bouquet.pdf','https://arxiv.org/pdf/1110.4458v1','20Oct2011;publishedMMJ13(2013),193–232','Definition3.4.2–3.4.3;relevantboundarycontext;complete§5.1–5.3','Gibbs continuous tableau / Plancherel boundary law. Does not prove the conjectured local dynamics.')]:
    p=AUDIT/'root_priority/private_reading'/name
    source_records.append({'id':name,'url':url,'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size,'chronology':date,'read_locator':loc,'coverage':cov,'primary':True,'lead_provenance':'Root-supplied source lead; independently hashed and inspected as primary material; no inherited priority verdict was relied on.'})
archive=BASE/'private_reading/nica-1404.4015v3-source'
source_records.append({'id':'nica-v3-source','url':'https://arxiv.org/src/1404.4015v3','path':str(archive),'sha256':sha(archive),'bytes':archive.stat().st_size,'read_locator':'RS_arxiv.tex lines573–600 theorem/Schur expression; title source lines229–233; all date-setting search','chronology':'Canonical 2015 v3 source; source member mtime 2015-04-29T04:28:36Z; gzip header 2015-04-30','coverage':'Authenticated earlier theorem content despite compilation-dependent later PDF title dates. Detailed member pins are in NICA_SOURCE_ARCHIVE_PIN.json.','primary':True})
searches=[
['Borodin Olshanski Poissonized Plancherel process monotone curves Hammersley 2006 partitions','Found math-ph/0402064; read the primary paper.'],
['Johansson extended Bessel kernel Poissonized Plancherel process first row Hammersley stationary drift','The 2004 paper references earlier static Bessel and PNG cases; no explicit drift-process answer was identified.'],
['Perfect sampling algorithms for Schur processes arxiv 2015','Authenticated 1407.3764v2.'],
['drift-jump Schur; leftmost piles Plancherel; left_Hamm stationary distribution; Aldous drift Plancherel stationary','No primary paper explicitly closing the named problem was located.'],
['Hammersley exponential stationary Plancherel; Hammersley drift stationary distribution; pile tops Schur; Plancherel growth first row hitting','Different ordinary Hammersley, source/sink, and TASEP models were excluded from coverage.'],
['Hammersley first k stationary; drift-jump particle process stationary distribution Aldous solution; Plancherel pile stationary Aldous','Source webpage and unrelated hits; no explicit named answer.'],
['An interacting particle process related to Young tableaux proof Plancherel; Young bouquet boundary Plancherel; Markov dynamics Thoma cone','Found the primary conjecture caveat and boundary law; recorded this route as blocked when used alone.'],
['Decorated Young tableaux poissonized Robinson-Schensted arxiv; Plancherel linear drift tableaux','Found Nica explicit full positive path law; authenticated the 2015 source.']]
dump('SOURCE_LEDGER.json',{'utc':now,'primary_sources':source_records,'search_ledger':searches,'web_primary_metadata_pages':['https://arxiv.org/abs/math/0107056','https://arxiv.org/abs/math-ph/0402064','https://arxiv.org/abs/1407.3764','https://arxiv.org/abs/1303.2795','https://arxiv.org/abs/1303.2794','https://arxiv.org/abs/1110.4458','https://arxiv.org/abs/1404.4015v3'],'bounded_search_result':'No explicit paper answering the named 2018 question was located; complete automatic mathematical coverage of the candidate law was verified.','source_redistribution':'Whole PDFs, full text and page renders are private reading copies, excluded from authored release manifest.'})
log='''# Research log — Schur / Plancherel adversary

All times UTC. Completion percentages estimate progress on this bounded priority audit, not a percentage probability that an open problem is solved.

| UTC checkpoint | Completion | Finding / decision |
| --- | ---: | --- |
| 2026-10-15 03:51:57 | 0% | Began assigned independent audit; read candidate PROOF before inherited conclusions. |
| 2026-10-15 03:52:39 | 10% | Saved INITIAL_RECONSTRUCTION.md; identified exact ascending-Schur and inverse-first-row hypothesis before reading inherited verdicts. |
| 2026-10-15 03:54:12 | 45% | OR exact symbol specialization confirmed; BO2004 primary Theorem2.3, horizontal curve and full kernel inspected; old1993 invariant rank representation read. |
| 2026-10-15 03:55:35 | 60% | Direct2013 dynamics source and Thoma caveat read; blocked that route as a stand-alone rigorous cover; identified Nica primary lead. |
| 2026-10-15 03:57:16 | 80% | Exact mapping controls passed:5914 permutations,2459 chain equalities,7377 skew determinants; candidate=Nica rescaling=BO Markov weights. |
| 2026-10-15 03:58:56 | 90% | Extended-Bessel barrier orientation checked numerically; full old stationary-law bridge reconstructed; Nica theorem typo and date caveats tracked. |
| 2026-10-15 04:01:31 | 96% | Draft report complete; authenticated2015 Nica source archive contains theorem; corrected initial manually entered03:54 header to actual filesystem creation03:52:39 without changing mathematical content. |
'''
log+=f'| {now} | 100% | Full AD1995 primary read adds published graphical/scaling premises; final authored report, six-source independent hashes, source ledger, exact and numerical controls, and authored manifest complete. No exact earlier named-problem answer located; automatic complete classical coverage supported. |\n'
log+='''
No external outreach or draft outreach was created. No Git/index/ref/provider or queue writes occurred. Other priority-family reports were not read. Primary leads supplied by the root were inspected independently and retained with their limitations. No claims from the conjectural general2013 local dynamics were promoted to theorems.

Routes: exact Schur specialization VERIFIED; quadrant-Poisson Plancherel path VERIFIED; Nica explicit weight VERIFIED; stationary Gamma(B)-to-first-row bridge VERIFIED by finite compatibility/inversion and direct coordinate check; general2013 local-cover route BLOCKED for missing invariance proof; explicit historical answer to named2018question NOT LOCATED in boundedsearch. Exact remaining uncertainty is historical attribution and source's qualitative explicitness criterion.
'''
(BASE/'RESEARCH_LOG.md').write_text(log)
authored=[p for p in BASE.iterdir() if p.is_file() and p.name!='FINAL_AUDIT_MANIFEST.json']
manifest={'utc':now,'status':'bounded_audit_complete','completion_percent':100,'strongest_supported_conclusion':'Full candidate stationary joint law is a complete elementary specialization/combination of earlier primary results; exact earlier expressly named solution not located.','scope':'Only this shard written; no queue classification or publication action.','authored_artifacts':[{'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(authored)],'private_reading_excluded_from_authored_artifacts':True,'manifest_self_hash':'Not included to avoid circular self-reference; caller may hash this manifest independently.'}
dump('FINAL_AUDIT_MANIFEST.json',manifest)
print(json.dumps({'six_source_pins_match':True,'primary_source_records':len(source_records),'authored_artifacts':len(authored),'completion_percent':100,'manifest_sha256':sha(BASE/'FINAL_AUDIT_MANIFEST.json')},indent=2))
