"""Build source-free metadata catalogue; never include body text or signed redirects."""
import pathlib,json,hashlib,datetime,re
from html.parser import HTMLParser
BASE=pathlib.Path(__file__).resolve().parent
PRIVATE=BASE/'private'
class Citation(HTMLParser):
    def __init__(self): super().__init__(); self.meta={}
    def handle_starttag(self,tag,attrs):
        d=dict(attrs); name=d.get('name','')
        if tag=='meta' and name in ('citation_title','citation_author','citation_doi','citation_date','citation_online_date','citation_arxiv_id'):
            self.meta.setdefault(name,[]).append(d.get('content'))

SCOPES={
 'marugame_arxiv_v1':('Marugame, The Bonnet theorem for statistical manifolds','arXiv2103.10102v1, 2021-03-18','PRIMARY_BODY_READ','All 10 pages; especially p4 Definition2.1/Theorem2.2, p5 proof, pp9-10 Bonnet proof; positive Riemannian, local only, prescribed codimension conditional tensors.'),
 'marugame_uec':('Marugame, The Bonnet theorem for statistical manifolds','Institutional author accepted manuscript, journal2021','PRIMARY_BODY_READ_AM_NOT_VOR','Same local Theorem2.2 pp4-6 and Bonnet proof pp9-10; repository rights field explicitly distinguishes accepted manuscript from version of record.'),
 'marugame_publisher':('Marugame journal publication metadata','Information Geometry4,363-376; online2021-09-29; DOI10.1007/s41884-021-00056-4','PRIMARY_PREVIEW_ONLY','Journal publication dates and local abstract checked; final theorem body not accessible.'),
 'marugame_official_pdf':('Marugame official PDF access attempt','DOI10.1007/s41884-021-00056-4','ACCESS_GAP_HTML_INSTEAD_OF_PDF','HTTP200 returned HTML subscription preview; not a PDF or final proof access.'),
 'marugame_uec_record':('UEC repository record for Marugame','Record10333; deposited2023; publication2021-12','PRIMARY_VERSION_METADATA','Rights statement says accepted version, not version of record; post-acceptance corrections may differ.'),
 'le_arxiv_v6':('Le, Monotone invariants and embeddings of statistical manifolds','arXivmath/0506163v6, 2016-03-10; volume publication2007','PRIMARY_BODY_READ','Introduction pp1-2; definitions§2; relevant §5 pp14-23 complete; Theorem5.1 p15 compact; explicit uniform scaling step p15; Theorem5.6 pp22-23 compact finite simplex.'),
 'le_history':('Le arXiv version history','v6, 2016-03-10 15:52:27 UTC','PRIMARY_VERSION_METADATA','Comments explicitly add compactness in Main Theorem and Theorem5.6; not a separate publisher erratum.'),
 'le_talk2016_curl':('Le, Embeddings of statistical manifolds','Author slides, Liblice, June2016','PRIMARY_BODY_READ','Entire 27-page talk; PDFp8 compact finite sample/noncompact countable sample; pp17-21 proof outline; p22 bounded-comass remark. Retrieved with system curl and normal TLS verification.'),
 'le2022':('Le, Natural differentiable structures on statistical models and the Fisher metric','arXiv2208.06539v4, 2022-12-09','PRIMARY_BODY_READ','PDFp4 paragraph citing AJLS2017 Theorem4.10 p222: countable sample for all smooth statistical manifolds; finite if compact. Not a finite ambient-dimension claim.'),
 'le2022_v4':('Le exact v4 body equality check','arXiv2208.06539v4, 2022-12-09','PRIMARY_BODY_READ','Exact versioned URL matches the previously fetched unversioned PDF bytes; p4 pin retained.'),
 'ajls_book_publisher':('Ay–Jost–Le–Schwachhofer, Information Geometry','Springer2017; DOI10.1007/978-3-319-56478-4','PRIMARY_PREVIEW_ONLY','Book and metadata; no full book-body access.'),
 'ajls_chapter':('AJLS chapter4, The Intrinsic Geometry of Statistical Models','DOI10.1007/978-3-319-56478-4_4; online2017-08-26; pp185-239','MATERIAL_PRIMARY_BODY_ACCESS_GAP','Publisher abstract asserts a broad finite-sample result for noncompact manifolds. Actual Theorem4.10 p222 not retrieved (locator authenticated by author2022); §4.5.5 Theorem4.11 pp238-239 is a discovery pointer only, not primary-body authenticated. Author2022 states countable/noncompact and finite/compact. Preserve conflict; do not infer erratum or falsity.'),
 'ajls_chapter_pdf':('AJLS official chapter-PDF access attempt','DOI10.1007/978-3-319-56478-4_4','MATERIAL_ACCESS_GAP_HTML_INSTEAD_OF_PDF','Official /content/pdf/ request returned HTTP200 HTML subscription preview, not chapter PDF.'),
 'ajls2017':('Jost, Information Geometry, lecture slides','PDFmetadata2019-10-15; 168pages with overlays','SCREENED_NOT_THE_2017_BOOK','Search title ambiguity resolved by actual body and PDFmetadata. This is a talk, not AJLS book theorem access.'),
 'loi_matta_v1':('Loi–Matta, Robustness of statistical models','arXiv2110.06145v1, 2021-10-12','PRIMARY_BODY_READ','Theorem1 p2; §2 linearization pp3-5; Definition2/Props6-7 pp5-7 and proofTheorem1 p7. Requires already N-induced; generic robustness and nearby realizations, not all prescribed data.'),
 'loi_matta_accepted':('Loi–Matta, Robustness of statistical manifolds','Author accepted manuscript; Topology and its Applications327(2023),108438; DOI10.1016/j.topol.2023.108438','PRIMARY_BODY_READ_AM_NOT_VOR','Cover explicitly author accepted manuscript. Printedp2/PDFp3 Theorem1 N>=n(n²+9n+20)/6; same already-induced scope and Props6-7. Entire relevant proof read.'),
 'loi_matta_publisher':('Loi–Matta publisher access attempt','Journal issue2023-03-15; DOI10.1016/j.topol.2023.108438','ORIGIN_HTTP403','Search-service primary publisher preview read separately; final publisher body unavailable, accepted manuscript available.'),
 'uohashi2012':('Uohashi, A Hessian Domain Constructed with a Foliation by 1-Conformally Flat Statistical Manifolds','International Mathematical Forum7(48)(2012),2363-2371; receivedApril2012','PRIMARY_BODY_READ','Entire 9-page body. Theorem2.2 p2365 local restricted class; Theorem4.1 pp2368-2370 conditional local common-domain result, assumed affine immersion family and compatibility.'),
 'canonical2026':('Gnandi–Boyom–Puechmorel, Canonical foliations of statistical manifolds with statistical models','Information Geometry9(2026),319-349; online2026-02-27; DOI10.1007/s41884-026-00193-8','PRIMARY_FULL_HTML_BODY_READ','§5 Theorem5.2 explicitlycompact; §5.3 Theorems5.6/5.8 and §7 Theorem7.1: conditional compact Hessian leaves and probability models, not all-manifold ambient embedding.'),
 'canonical_pdf':('Canonical foliations2026 publisher PDF','Published2026 version of record','PRIMARY_BODY_READ','Printedp334/PDFp16 Theorem5.2 compact; printedp334-337 definitions and leaf results; §7 Theorem7.1. Independent fresh origin fetch.'),
 'fox2023':('Fox, Conelike radiant structures','Information Geometry6(2023),463-595; online2023-10-04; DOI10.1007/s41884-023-00115-y','PRIMARY_FULL_HTML_BODY_READ_RELEVANT_SECTIONS','§1 citation[107] is general historical context; relevant§§8-10, especially Theorem10.5. Radiant/Thomas connections and conditional special statistical structures; a covariant Hessian for a curved connection does not establish a positive dually flat ambient.'),
 'curved_bregman_v5':('Nielsen, Curved representational Bregman divergences and their applications','arXiv2504.05654v5, 2026-03-27; initialv1 2025-04-08','PRIMARY_BODY_READ_RELEVANT_SECTIONS','§2 Definitions1-2 pp3ff and propositions for supplied generators and embeddings; §4 monotone representations. No universal realization theorem for arbitrary prescribed metric and cubic tensor.'),
 'relative_entropy_web_observation':('Gauvin, Relative-Entropy Geometry of Translations and Boosts: Minimal Realisation and Affine Rigidity','Preprints.org202609.1460v1; posted2026-09-17','PRIMARY_SERVICE_BODY_OBSERVATION_ORIGIN_GAP','§4 Theorems2-3 and proof: a specific two-dimensional contrast family has a 3-dimensional positive Hessian realization; not arbitrary statistical manifolds. Origin urllib403; service-rendered body only, fingerprint explicitly not origin-byte hash.'),
 'twopoint2026':('Ciaglia–Marmo–Pacelli–Schiavone–Zampini, A two-point approach to the inverse problem in information geometry','arXiv2608.16714v1, 2026-08-17','PRIMARY_BODY_READ_RELEVANT_SECTIONS','Introduction pp2-4; §2.1 Proposition2.2 pp13-14 and complete partition-of-unity proof; §§2.2.1-2.2.2. Output is contrast bi-form/function on M×M or a diagonal neighborhood; no finite-dimensional positive flat ambient asserted.'),
 'osipov2021':('Osipov, Statistical Lie algebras of a constant curvature and locally conformally Kahler Lie algebras','arXiv2112.06686v2, 2022-05-20; initial2021-12-13','PRIMARY_BODY_READ_RELEVANT_SECTIONS','§2.2 pp6-9, Theorem2.12 and proof, Corollary2.13: genuine global Hessian cone realization for constant statistical curvature (direct theorem c<=1; corollary nonzero c). Exact remaining gap is arbitrary variable-curvature statistical structures.'),
 'osipov2021_v2':('Osipov2021 exact v2 body check','arXiv2112.06686v2','PRIMARY_BODY_EQUALITY_CHECK','Versioned URL equality with prior unversioned retrieval.'),
 'osipov2022':('Osipov, Locally conformally Hessian and statistical manifolds','arXiv2209.02357v3, 2023-09-06; initial2022-09-06; DOI10.1016/j.geomphys.2023.104989','PRIMARY_BODY_READ_RELEVANT_SECTIONS','§3.3 Theorems3.14/3.16 pp12-14 and proof; §1 global structure statements. Same constant-curvature cone class; compact radiant conformal Hessian structure theorem, not arbitrary statistical embedding.'),
 'osipov2022_v3':('Osipov2022 exact v3 body check','arXiv2209.02357v3','PRIMARY_BODY_EQUALITY_CHECK','Versioned URL equality with prior unversioned retrieval.'),
 'totally_umbilical2026':('Ueno, Doubly Totally-Umbilical Statistical Submanifolds in the Probability Simplex','arXiv2606.06395v2, 2026-06-05','PRIMARY_BODY_SCOPE_READ','Introduction and main Theorems4.5/4.6; classification of existing doubly umbilical submanifolds, not arbitrary realization. Current preprint, not assumed journal publication.'),
 'ueno2026_v2':('Ueno exact v2 body check','arXiv2606.06395v2','PRIMARY_BODY_EQUALITY_CHECK','Versioned URL equality with unversioned retrieval.'),
 'le2025review':('Le–Minh–Protin–Tuschmann, Categorical and geometric methods in statistical, manifold, and machine learning','arXiv2505.03862v1, 2025-05-06','PRIMARY_BODY_SCREEN_ONLY','Introduction and search for Hessian/Lauritzen/embedding followed. Statistical learning/kernel and Riemannian embedding topics; no exact generic statistical realization theorem located. Not treated as a theorem-level predecessor.'),
 'kurose2007_2023':('Gezer–Aktas–Durmaz, Notes concerning Kahler and anti-Kahler structures on quasi-statistical manifolds','arXiv2307.15065v1; body dated2023-05-31, not authenticated submission date','FALSE_CITATION_LEAD_REJECTED','A secondary search result associated this arXiv ID with Kurose2007; actual fetched title/body is a different work. Filename preserves retrieval history. Never used as Kurose evidence.'),
 'marugame_openalex':('OpenAlex Marugame record','Index observation2026-10-15','DISCOVERY_ONLY_NOT_THEOREM_EVIDENCE','One indexed forward citation, Fox2023.'),
 'openalex_marugame_citers':('OpenAlex forward-citation query for Marugame','Index observation2026-10-15','DISCOVERY_ONLY_NOT_THEOREM_EVIDENCE','One result; supplemented by exact-title/year web queries. Index incompleteness explicit.')
}

def main():
    events=[json.loads(x) for x in (PRIVATE/'network_events.jsonl').read_text().splitlines()]
    out=[]
    for r in events:
        e={k:v for k,v in r.items() if k not in ('final_url','etag')}
        if r['key'] in SCOPES:
            a,b,c,d=SCOPES[r['key']];e.update(title=a,version_or_publication=b,access_class=c,read_locators_and_scope=d)
        if e.get('path'):
            p=BASE/e['path'];assert p.stat().st_size==e['bytes'];assert hashlib.sha256(p.read_bytes()).hexdigest()==e['sha256']
        out.append(e)
    p=PRIVATE/'relative_entropy_web_observation.json'
    a,b,c,d=SCOPES['relative_entropy_web_observation']
    out.append(dict(key='relative_entropy_web_observation',title=a,version_or_publication=b,access_class=c,read_locators_and_scope=d,
        request_url='https://www.preprints.org/manuscript/202609.1460',observation_utc_window=json.loads(p.read_text())['observation_utc_window'],path=str(p.relative_to(BASE)),bytes=p.stat().st_size,
        sha256=hashlib.sha256(p.read_bytes()).hexdigest(),hash_kind='web-service observation serialization, NOT origin bytes'))
    metadata={}
    for p in PRIVATE.glob('*metadata.html'):
        x=Citation();x.feed(p.read_text());s=p.read_text();m=re.search(r'<h2>Submission history</h2>(.*?)</div>',s,re.S)
        metadata[p.stem]={'citation_metadata':x.meta,'history_plain':re.sub(r'<[^>]*>',' ',m[1]).strip() if m else None}
    catalogue={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sources':out,'version_metadata':metadata,
      'policy':'All bodies, extracted text, renders and raw network events private. Metadata does not certify historical firstness. Request URLs are public locators; signed redirect URLs never curated.',
      'private_body_count':len([x for x in out if x.get('path')]),
      'version_equalities':{a:hashlib.sha256((PRIVATE/(a+'.pdf')).read_bytes()).hexdigest()==hashlib.sha256((PRIVATE/(b+'.pdf')).read_bytes()).hexdigest() for a,b in [('le2022','le2022_v4'),('osipov2021','osipov2021_v2'),('osipov2022','osipov2022_v3'),('totally_umbilical2026','ueno2026_v2')]}}
    assert all(catalogue['version_equalities'].values())
    (BASE/'SOURCE_CATALOG.json').write_text(json.dumps(catalogue,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'source_events':len(out),'version_equalities':catalogue['version_equalities']}))
if __name__=='__main__':main()
