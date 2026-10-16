#!/usr/bin/env python3
from pathlib import Path
import datetime, hashlib, json

P = Path(__file__).resolve().parents[1]
R = P / 'sources' / 'raw'
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(f):
    return {'path': str(f.relative_to(P)), 'sha256': hashlib.sha256(f.read_bytes()).hexdigest(), 'bytes': f.stat().st_size}

# Exact search text transcribed from this independent review's tool calls.
# These are discovery queries, never a numerical certificate of absence.
QUERIES = {
 'q0': ['"A Remark on Bernstein–Zelevinsky Classification for General Linear Groups"', '"Luo" "Zha" "Bernstein" classification counterexample', '"unitary periods" "counterexample" Jacquet'],
 'q1': ['"s11464-025-0256-0"', '"Caihua Luo" "Junwei Zha"', '"A Remark on Bernstein" Luo Zha'],
 'q2': ['"unitary periods" "Matringe" Lu', '"unitary" "Conjecture 6.12" counterexample', '"Jacquet" "unitary distinction" nongeneric'],
 'q3': ['"Luo" "Zha" "standard modules" Lapid Minguez', '"bernstein-zelevinsky.pdf" Luo', '"Caihua" "Bernstein" arxiv', '"A Remark on Bernstein" "2025"'],
 'q4': ['"Luo" "Zha" "Lapid" "conjecture"', '"Junwei Zha" Bernstein Zelevinsky 2025 May 13', '"unitary periods" "Lu" "Matringe"', '"unitary periods" "2026"'],
 'q5': ['Lu Matringe distinction unitary involution 2026 arxiv', 'Mínguez Offen Sécherre unitary periods 2017', 'Beuzart Plessis multiplicities nondegenerate Hermitian matrices 2022 arxiv', '"unitary" "counterexample" "Feigon"'],
 'q6': ['"s11464-025-0256-0" pdf', '"A Remark on Bernstein" site:arxiv.org', '"A Remark on Bernstein" site:journal.hep.com.cn', '"On completeness of local intertwining periods"'],
 'q7': ['"Frontiers of Mathematics" site:journal.hep.com.cn', '"Junwei Zha" mathematics', '"Mínguez" "Offen" "Sécherre" 2017', '"On representations distinguished by unitary groups" counterexample'],
 'q8': ['Minguez Offen Secherre 2017 unitary distinction', '"imprimitive" "unitary" "representations"', '"nongeneric" "unitary groups" distinction counterexample', '"unitary periods" "multisegment"'],
 'q9': ['"Mínguez" "Offen" "Sécherre" distinction', '"Minguez" "Offen" "Secherre" unitary', '"distinguished" "2017" "unitary" "Sécherre"'],
 'q10': ['"Klyachko models for ladder representations" arxiv', '"On a determinantal formula of Tadić" arxiv', '"Introduction to the relative Langlands program" Beuzart Plessis arxiv', '"unitary" "odd cycle" "distinguished"'],
 'q11': [],
 'q12': ['"Bernstein-Zelevinsky" "May 13" "2025"', '"Caihua Luo" "Zha" pdf standard', '"Junwei Zha" "2025" "Bernstein"', '"unitary periods" counterexamples'],
 'q13': ['"unitary" "Conjecture 6.12" -site:researchgate.net -site:eurekamag.com', '"unitary groups" "counterexample" "distinguished" -site:reddit.com', '"Caihua Luo" "A remark" classification pdf', '"Junwei Zha" "standard" module'],
 'q14': ['"unitary" "[0,2]" "[1,4]" "[2,5]"', '"unitary" "[4,6]" "[3,3]"', '"unitary distinction" "counterexample"', '"Jacquet" "nongeneric" "unitary" conjecture'],
 'q15': ['"On a local conjecture of Jacquet, ladder representations and standard modules" counterexample', '"unitary" "pentagon" multisegment', '"unitary" "odd cycle" Langlands', '"Jacquet" "five-segment"'],
 'q16': ['"On two questions concerning representations distinguished by the Galois involution" arxiv', '"On parabolic induction associated with a p-adic symmetric space" arxiv', '"unitary groups" "non-generic" "distinction"', '"Jacquet conjecture" "unitary" counterexample representation'],
 'q17': ['"unitary groups" "Galois invariant" "counterexample"', '"unitary group" "nongeneric" "Jacquet"', '"unitary periods" "imprimitive"', '"Conjecture 4" "unitary" "Lapid"'],
 'q18': ['"Intertwining periods and distinction for p-adic Galois symmetric pairs" arxiv', '"On local intertwining periods" 2303.03663', '"Luo" "Zha" "0256" "kernel"', '"unitary period" "five" "counterexample"'],
 'q19': ['"unitary periods" "five-segment"', '"Hermitian" "multisegment" "counterexample"', '"unitary" "non-bipartite" representation', '"Conjecture 6.12" "counterexample" "Lapid"'],
}
OPS = {
 'open1': [{'open':'https://sites.google.com/site/chluonus/research'}, {'open':'https://link.springer.com/article/10.1007/s11464-025-0256-0'}],
 'q2': [{'click': {'ref_id':'turn214view0','id':12,'target':'https://docs.google.com/viewer?a=v&pid=sites&srcid=ZGVmYXVsdGRvbWFpbnxjaGx1b251c3xneDoxMzAyZWE5OWJmNTVmY2E3'}}],
 'q4': [{'click': {'ref_id':'turn214view0','id':20,'target':'https://drive.google.com/embeddedfolderview?id=1hFulU1Vw-MtfzSd_Sn8VguPgaNV5BOkp#list'}}],
 'q8': [{'open':'https://journal.hep.com.cn/math/EN/10.1007/s11464-025-0256-0'}],
 'q9': [{'open':'https://journal.hep.com.cn/math/EN/10.1007/s11464-025-0256-0'}, {'open':'https://arxiv.org/abs/2503.11988v2'}, {'open':'https://arxiv.org/abs/2008.05036v2'}],
 'q10': [{'open':{'ref_id':'turn222view0','lineno':0}}],
 'q11': [{'open':{'ref_id':'turn223view0','lineno':70}}, {'open':'https://arxiv.org/abs/2609.21384'}],
}
rows=[]
for key in ['q0','q1','open1']+[f'q{i}' for i in range(2,20)]:
    f=R/(key+'.json')
    rows.append({'id':key, 'search_query':[{'q':q} for q in QUERIES.get(key,[])], 'other_operations':OPS.get(key,[]),
                 'response_length':'long', 'executed_time':'Not separately captured; recorded in this active review before metadata freeze',
                 'raw_result':pin(f) if f.exists() else None,
                 'retention_note':'Initial q0 raw result not separately retained; its exact query strings are preserved. No theorem conclusion rests on q0.' if key=='q0' else None})
(P/'WEB_QUERY_LEDGER.json').write_text(json.dumps({'recorded_utc':NOW,'independent':True,'search_count_is_not_absence_proof':True,'calls':rows},indent=2)+'\n')

CAT = [
 ('owr_ems','Erez Lapid, Distinguished representations and their multiplicities, OWR14/2011','EMS publisher PDF; exact relevant p734, PDFpage16','2011',[(11,'729','Conjecture1 unrestricted local unitary converse'),(13,'731','total multiplicity as a sum over Hermitian orbits'),(16,'734','§5.2 rank-one-kernel question; §5.3 imprimitive definition, earlier three-segment example, Conjecture4')], 'Target formulation and earlier mechanism, not evidence that target was unresolved worldwide.'),
 ('flo_pdf','Feigon–Lapid–Offen, On representations distinguished by unitary groups','Published PMIHES115(2012),185–323','2012',[(4,'188','unrestricted Jacquet converse and positive classes'),(5,'189','Theorem0.2'),(30,'214','§3.2 τ-Witt index'),(31,'215','Lemma3.4'),(62,'246','Conjecture6.12'),(107,'291','Corollary13.6'),(109,'293','Theorem13.11 proof (13.3),(13.4)'),(110,'294','Entire independent open restrictions; Corollary13.12'),(112,'296','Corollary13.16; Conjecture13.17'),(113,'297','§13.6 concluding scope')], 'Full body retrieved; complete relevant pages inspected. Period basis, linked label constraints, ladders/unitarizable results precede candidate. External source proofs are dependencies, not independently re-proved here.'),
 ('lm2014_pdf','Lapid–Mínguez, On a determinantal formula of Tadić','Undated author manuscript in Universidad de Sevilla repository, 29 pages; journal bibliographic identity AJM136(2014),111–142','2014 bibliographic date; retained manuscript revision date unverified',[(2,'2','Theorem1(i), ladder kernel-generation'),(27,'27','§6.4 transported rank-one kernels'),(28,'28','Conjecture2, K=L')], 'Complete relevant pages inspected; do not silently identify undated manuscript with version of record.'),
 ('lm2016_pdf','Lapid–Mínguez, On parabolic induction on inner forms of the general linear group over a non-archimedean local field','arXiv1411.6310v3, revised2015-12-14; heading2015-12-15','Selecta Math22(2016),2347–2400',[(10,'10','Theorem2.6'),(16,'16','Leclerc four-segment example'),(34,'34','Definition5.13 ladders'),(35,'35','LC setup'),(36,'36','matching relation'),(38,'38','Proposition5.20'),(52,'52','§A.5 involution')], 'Classification and ladder-side irreducibility criteria are established interfaces. Exact candidate partition calculation is an instance, not a new matching theorem.'),
 ('mos_pdf','Mitra–Offen–Sayag, Klyachko Models for Ladder Representations','Published DocumentaMath22(2017),611–657; publisher file contains cover','2017; paper states received2016-06-07',[(4,'614','imprimitive and quotient-descent strategies'),(31,'641','Example9.4 negative Sp-distinction')], 'Different subgroup; published negative symplectic example and general descent strategy precede current framing.'),
 ('bp_pdf','Beuzart-Plessis, Multiplicities and Plancherel formula for the space of nondegenerate Hermitian matrices','arXiv2008.05036v2, revised2021-01-16','JNT230(2022),5–63; paper§1.4 records announcement2017-04/05',[(3,'3','Theorem1 tempered Plancherel'),(4,'4','Theorems2,3 generic multiplicities'),(5,'5','§1.4 announcement date')], 'Resolves generic Conjecture13.17. Its generic/tempered conclusions do not apply to this nongeneric nonunitarizable quotient.'),
 ('lu_matringe_pdf','Lu–Matringe, On completeness of local intertwining periods','arXiv2503.11988v2, revised2026-04-10; v1 submitted2025-03-15','JFA291(2026),111486; issue2026-07-01',[(25,'25','§5 begins'),(26,'26','square-integrable inducing representation assumption'),(27,'27','FLO normalizations'),(28,'28','completeness from generic/tempered multiplicities'),(29,'29','Remark5.1')], 'Full relevant §5 pp25–29 inspected. Does not assert quotient descent for arbitrary reducible standard modules.'),
 ('survey_pdf','Beuzart-Plessis, Introduction to the relative Langlands program','arXiv2509.18062v1, submitted2025-09-22','2025 survey; no later version audit claimed',[(64,'64','§3.5.9 unitary pair'),(65,'65','base-change degree setup'),(66,'66','Theorem3.22 generic multiplicities'),(67,'67','Remark3.23; different SL2 counterexample')], 'Generic formulation retained. Recent survey is not proof of worldwide current openness.'),
 ('sharma_pdf','Hariom Sharma, Duality, rigidity, and peeling for multisegments: on hypotheses of Mitra, Offen, and Sayag','arXiv2609.21384v1, submitted2026-09-18','Preprint; no journal acceptance inferred',[(19,'19','Theorem8.1 exact five-segment multiset'),(20,'20','complete witness computations'),(21,'21','Remarks8.2–8.4; symplectic-period implications'),(22,'22','§9 converse distinctions')], 'Combinatorial endpoint-order counterexample on degree8 multiset, different from GL15. It is not a unitary-period vanishing theorem.'),
 ('gurevich_pdf','Maxim Gurevich, On a local conjecture of Jacquet, ladder representations and standard modules','arXiv1411.2420v2, revised2015-09-14; PDF printed date2018-07-11','MathZ281(2015),1111–1127',[(1,'1','GLn(F) distinction; broad converse already false')], 'Different Galois fixed subgroup; do not conflate two Jacquet conjectures. Printed date discrepancy explicitly preserved.'),
 ('gmm_pdf','Gurevich–Ma–Mitra, On two questions concerning representations distinguished by the Galois involution','arXiv1609.03155v1, submitted2016-09-11','ForumMath30(2018),141–157',[(2,'2','Statement1.1; Conjecture1.2 subgroup'),(3,'3','base change from unitary group, not distinction by unitary group'),(18,'18','§8 Definition8.1 five segments'),(19,'19','imprimitive claim and Lemma8.2')], 'Full §8 inspected visually and textually. Five-segment degree20 imprimitive negative Galois distinction precedes broad narrative, not exact target.'),
 ('mo2022_pdf','Matringe–Offen, Intertwining periods and distinction for p-adic Galois symmetric pairs','arXiv2102.00480v2, revised2022-07-18; v1 submitted2021-01-31','PLMS125(2022),1179–1252',[(3,'3','explicit quotient-descent limitation'),(16,'16','Theorem1 meromorphic intertwining periods'),(18,'18','Corollary2 cuspidal induction; Remark4 negative GL5(F) example')], 'Established induced-representation mechanism, not an arbitrary quotient classification.'),
 ('moy_pdf','Matringe–Offen–Yang, On local intertwining periods','arXiv2303.03663v2, revised2023-10-05','JFA286(2024),110293',[(25,'25','Theorem5.4 sufficient condition for induced representations'),(26,'26','Corollary5.5 cuspidal induction')], 'Functional-equation and meromorphic continuation framework precedes current proof; no all-quotient multiplicity assertion identified.'),
 ('lm2020_pdf','Lapid–Mínguez, Conjectures and results about parabolic induction of representations of GLn(F)','Published InventMath222(2020),695–747; VOR2020-07-06','2020',[(28,'722','Theorem1, good ladder multisegments; Corollary3')], 'Forward-citation representation-theoretic screening; no period result used.'),
 ('lz_hku_announcement','CUHK(SZ)–HKU Representation Theory WorkshopII program','Public HKU institutional PDF,4pages','Event2025-05-13',[(1,None,'event date and Junwei Zha talk'),(4,None,'Luo–Zha-title talk abstract')], 'Primary evidence of earlier public announcement of kernel-generation disproof; no exact segments or unitary consequence supplied.'),
]
receipts=json.loads((P/'SOURCE_RETRIEVAL.json').read_text())
byid={x['id']:x for x in receipts}
catalog=[]
for key,title,version,pub,locators,assessment in CAT:
    f=R/(key+'.body'); t=R/(key+'.txt')
    catalog.append({'id':key,'title':title,'url':byid.get(key,{}).get('url'),'version':version,'publication_vs_announcement':pub,
                    'body':pin(f),'full_body_is_pdf':f.read_bytes().startswith(b'%PDF'),
                    'extracted_text':pin(t) if t.exists() else None,
                    'complete_relevant_body_locators':[{'pdf_page_1_based':a,'printed_page':b,'locator':c} for a,b,c in locators],
                    'assessment':assessment})
catalog.append({'id':'luo_zha','title':'Luo–Zha, A Remark on Bernstein–Zelevinsky Classification for General Linear Groups',
                'doi':'10.1007/s11464-025-0256-0','publisher_url':'https://link.springer.com/article/10.1007/s11464-025-0256-0',
                'VOR_published_online':'2026-07-05','HEP_mirror_date':'2026-07-28','first_public_announcement_verified':'2025-05-13',
                'received':'2025-11-13','accepted':'2026-05-19','full_primary_body_retrieved':False,
                'critical_gap':'Every exact and transformed parameter comparison, internal unitary-period/conjecture consequence, and direct kernel-mechanism overlap is UNKNOWN.',
                'attempt_ids':[x['id'] for x in receipts if x['id'].startswith('lz_') or x['id'].startswith('luo_')],
                'body_locator':None,'inference_from_abstract_excluded':True})
(P/'SOURCE_CATALOG.json').write_text(json.dumps({'recorded_utc':NOW,'full_dependency_proofs_not_independently_audited':True,'sources':catalog},indent=2)+'\n')
(P/'RAW_SOURCE_PINS.json').write_text(json.dumps({'recorded_utc':NOW,'private_raw_material_not_for_public_redistribution':True,'files':[pin(f) for f in sorted(R.rglob('*')) if f.is_file()]},indent=2)+'\n')
forward=json.loads((R/'flo_forward_openalex.body').read_text())
(P/'FORWARD_CITATION_SCREEN.json').write_text(json.dumps({'recorded_utc':NOW,'discovery_only_secondary_index':True,
 'query_url':'https://api.openalex.org/works?filter=cites:W1966456487&per-page=200','indexed_count':forward['meta']['count'],
 'not_complete_worldwide_citation_coverage':True,'all_indexed_titles_screened':True,
 'selected_primary_bodies':['lm2014_pdf','mos_pdf','bp_pdf','survey_pdf','gurevich_pdf','gmm_pdf','mo2022_pdf','moy_pdf','lu_matringe_pdf'],
 'other_routes_read_only_screened':'Titles concerning global/GGP, modular supercuspidal, different subgroup or Archimedean models were not treated as exact target resolutions. Uninspected source bodies do not establish exclusion.',
 'titles':[{'title':x.get('display_name'),'year':x.get('publication_year'),'doi':x.get('doi')} for x in forward['results']]},indent=2)+'\n')
print('metadata built; catalog',len(catalog),'raw files',len(list(R.iterdir())))
