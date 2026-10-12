from pathlib import Path
from datetime import datetime, timezone
import hashlib, json

ROOT = Path(__file__).resolve().parent

def measure(p):
    b = p.read_bytes()
    return {'path': str(p.relative_to(ROOT)), 'bytes': len(b),
            'sha256': hashlib.sha256(b).hexdigest(),
            'mode_when_measured': oct(p.stat().st_mode & 0o777)}

# Read scopes bind the report's comparisons to actual complete passages read.
specs = [
 ('S01','arxiv2004v1','v1; submitted 26 April 2020','pp.5–6 §3.6, Table5 k605','exact_prior_statement_and_partial_even_proof'),
 ('S02','arxiv2004v11','v11; submitted 29 October 2020','Table7 p.9 k606; definitions and signed Eq.1','exact_prior_statement_and_partial_even_proof'),
 ('S03','fifty_published','journal version of record; online 18 February 2021','pp.343,349; Eq.1, §3.7, Table7 k607, k604a/b','exact_prior_statement_and_partial_even_proof'),
 ('S04','self_intersected','arXiv2011.06640v3; 19 January 2021','pp.1–2,8–10,12–14; full relevant propositions/corrections','restricted_partial'),
 ('S05','inversive_triangle','arXiv2012.03020v2; 13 July 2021','§§1–4 pp.1–6; Prop.7 and Observation1','different_objects_restricted'),
 ('S06','bicentric_published','Arnold Mathematical Journal 7(2021)619–637; version of record','pp.622–627 Thms1/2; AppendixA pp.629–630; B p.631','mechanism_only'),
 ('S07','impa_book','IMPA first printing July 2021; ISBN978-65-89124-43-6','printed17–20,67–71,88,130,158–162,205–207; PDF offset+11','restricted_triangular_mechanism'),
 ('S08','pedal_like','arXiv2009.02581v3; 16 September 2020','§2 pp.3–6; AppendixB pp.12–14 full Props7/9','classical_and_smooth_mechanism'),
 ('S09','steiner_hat_preprint','arXiv2006.13166v5; 5 October 2020','§§2/3 pp.3–5 full Thm1/Cor1; Prop9 p.11; §8 p.17','different_envelope_mechanism'),
 ('S10','triangular','arXiv2001.08054v3; 12 December 2021','pp.3–4,6–12 full Thms1–4/Cor1 proofs','restricted_triangular_mechanism'),
 ('S11','circuminvariants','International Journal of Geometry10(1)(2021)31–57','intro/index; §3 p.40; §4 pp.41–42; §5 p.45; conclusion p.50','restricted_triangular_mechanism'),
 ('S12','center_power','arXiv2102.09438v4; 16 April 2021','§§3.3–3.5 pp.6–7; Prop7 pp.12–13 full proof; AppendixB p.23','restricted_triangular_mechanism'),
 ('S13','spatial','arXiv2102.10899v1; 22 February 2021','entire pp.1–9','different_averaged_invariants'),
 ('S14','stachel_grid','arXiv2105.03362v2; 19 May 2021','definitions §§2–3; pp.21–25; full Thms4.5/4.7 proofs','symmetry_and_local_foot_mechanism'),
 ('S15','querret_pedal','Annales14(1823–1824)280–285; NUMDAM primary scan','entire printed280–285','classical_signed_triangle_quadratic'),
 ('S16','sturm_pedal','Annales14(1823–1824)286–293; NUMDAM primary scan','entire printed286–293; signed discussion287; general polygon292–293','classical_signed_triangle_and_polygon_quadratic'),
 ('S17','steiner_werke1','WerkeI(1881), primary collected scan; proof explicitly dated November1825','printed15–16 PDF30–31 entire proof, both visually inspected','exact_prior_general_quadratic_mechanism'),
 ('S18','steiner_original','e-rara DOI10.3931/e-rara-3816; bound volume catalog1836–1841','§§XIV–XVI printed18–21 PDF23–26; ellipse application32–33 PDF37–38','classical_finite_and_smooth_mechanism'),
 ('S19','forum_all_mirror','Alperin Forum Geometricorum4(2004)143–151; mirror of primary journal article','entire article PDF769–777; all Prop1–4 proofs','conic_pedal_mechanism'),
 ('S20','external_pedal_antipedal','author PDF dated1 October2026 v1.0; independent deposit date unverified','entire6pages','restricted_recent_bridge'),
 ('S21','external_outer_pedal','author PDF dated1 October2026 v1.1; independent deposit date unverified','entire9pages; p.5 also separately reread','restricted_recent_bridge'),
 ('S22','harmonic','Journal for Geometry and Graphics26(2)(2022)217–236; publisher PDF','full relevant §4.1–4.3 printed227–228 PDF11–12; Props4–6 and conjectures','different_homothetic_polar_objects'),
 ('S23','pedal_extremal','primary authors webpage, declared update15 July2020; timestamp not independently archived','§§2–3 formula discussion; full relevant browser text; native HTML capture','modern_exposition_of_classical_mechanisms'),
]

receipts = []
for p in sorted((ROOT/'receipts').glob('*.json')):
    r = json.loads(p.read_text())
    receipts.append({'receipt': measure(p), 'record': r})

sources = []
for sid,stem,edition,scope,classification in specs:
    paths = sorted((ROOT/'sources_private').glob(stem+'.*'))
    source_receipts = [x for x in receipts if x['record']['name'].startswith(stem+'_')]
    urls = list(dict.fromkeys(x['record']['url'] for x in source_receipts if x['record'].get('url')))
    sources.append({'id':sid,'stem':stem,'edition':edition,'read_scope':scope,
        'classification':classification,'urls':urls,
        'files':[measure(p) for p in paths],
        'receipt_paths':[x['receipt']['path'] for x in source_receipts]})

failed = []
for stem,reason in [('inversive_published','curl exit0 returned HTML rather than PDF; extraction exit1'),
                    ('pedal_like_published','curl exit0 returned HTML rather than PDF; extraction exit1'),
                    ('steiner_hat','curl exit22; no acquired journal PDF'),
                    ('steiner_hat_alt','curl exit22; no acquired journal PDF'),
                    ('alperin_conics','curl exit6 DNS failure; primary article later read in mirror')]:
    failed.append({'stem':stem,'reason':reason,'receipt_paths':[x['receipt']['path'] for x in receipts if x['record']['name'].startswith(stem+'_')],
                   'files':[measure(p) for p in (ROOT/'sources_private').glob(stem+'.*')]})

custody = {
 'audit_root':str(ROOT),'metadata_UTC':datetime.now(timezone.utc).isoformat(),
 'criteria_freeze':json.loads((ROOT/'CRITERIA_FREEZE.json').read_text()),
 'browser_search_record':'SEARCH_TRAIL.md; exact browser tool transcript retained in conversation. Browser calls have no native argv/exit/stdout/stderr and are not fabricated as native calls.',
 'private_source_policy':'Original PDFs, scans, HTML and extracts remain private evidence; report does not redistribute their full text.',
 'mode_semantics':'Receipts retain actual modes at retrieval/extraction; FINAL_SEAL.json records final read-only file modes after closure.',
 'sources':sources,
 'all_private_evidence_files':[measure(p) for p in sorted((ROOT/'sources_private').iterdir()) if p.is_file()],
 'native_receipts':receipts,'failed_acquisitions':failed,
 'historical_receipt_resolution':[{'receipt':'receipts/classical_boundary_control.json',
    'original_recorded_path':'classical_boundary_control.py',
    'preserved_original_bytes':'classical_boundary_control_initial.py',
    'reason':'Initial control was strengthened to derive all six coefficients. The original receipt is preserved unchanged and its original script bytes are retained separately; final script has its separate final receipt.'}],
 'unavailable_versions_of_record':[
  {'source':'S05','doi':'10.1007/s40879-021-00489-2','gap':'potential restricted triangular addition, no concrete full-domain E/M theorem identified'},
  {'source':'S08','doi':'10.1007/s13366-021-00588-x','gap':'edition coverage; inspected preprint treats fixed/smooth curves'},
  {'source':'S09','doi':'10.31896/k.24.2','gap':'edition coverage; inspected preprint treats envelope and homothetic family'},
  {'source':'S10','journal':'American Mathematical Monthly128(10)(2021)898–910','gap':'potential restricted triangular addition, no concrete full-domain E/M theorem identified'},
  {'source':'S12','doi':'10.1007/s10883-021-09580-z','gap':'potential restricted triangular addition, no concrete full-domain E/M theorem identified'},
  {'source':'S13','doi':'10.1007/s10883-022-09608-y','gap':'edition coverage; inspected preprint treats spatial averages of perimeter/cosines'}],
 'mathematical_dependency':'ROOT_MATHEMATICAL_AUDIT.md; mathematical gate passed2026-10-04T23:26:52Z. Historical imported raw records used as leads only, not as current literature truth.',
}
(ROOT/'SOURCE_CUSTODY.json').write_text(json.dumps(custody,ensure_ascii=False,indent=2)+'\n')

claims = {
 'E':{'statement':'A+/A−=B+/B−, signed original/outer focal supporting-line pedal areas, domain as frozen',
      'prior_statement':{'source':'S01','locator':'Table5 p.6 k605, §3.6 pp.5–6','earliest_supported_date':'26 April2020 posting, observation dated4/20'},
      'prior_proof':'Primitive even case follows directly from published S03 §3.7 p.349 k604a/b symmetry.',
      'bounded_verdict':'No full-domain proof or fully checked equivalent was identified in audited primary theorem sets. E discovery is prior art; proof priority is unresolved.'},
 'M':{'statement':'B_j=C0 A_j at both foci with positive C0 independent of phase',
      'bounded_verdict':'Potential stronger candidate contribution; historical priority unresolved. No full equivalent theorem identified in audited sections.',
      'concrete_implication_gaps':['N3: Sturm triangle formula plus simultaneous original/excentral circle-center formulas; not independently closed.',
         'Even primitive: S20 Lemma3 focal p trace plus S21 Eq14 outer radial quadratic; scalar relation not independently closed. S20 p=KT and S21 TB theorem have disjoint primitive period classes.'],
      'blocked_route':'Steiner fixed-polygon quadraticity alone supplies no phase-independent relation between two moving polygons; central difficulty remains unsupported.'},
 'C':{'statement':'Common focal ratio in E is independent of phase','truth_dependency':'False by ROOT exact triangles and central inversion.',
      'bounded_priority_verdict':'No prior explicit correction identified in inspected statements; first correction is not certified.'},
 'source_classifications':[{'source':s['id'],'classification':s['classification'],'read_scope':s['read_scope']} for s in sources],
 'absolute_firstness_claim':False,'merge_or_publication_authorization':False,
 'remaining_general_limits':['Unavailable journal editions as classified in SOURCE_CUSTODY.json.',
   'Unindexed current literature, complete bibliography graph, theses/non-English material not exhaustively certified.',
   'Other independent priority-family reports were not read; ROOT must independently authenticate and adjudicate.']}
(ROOT/'CLAIM_COMPARISON.json').write_text(json.dumps(claims,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'sources':len(sources),'native_receipts':len(receipts),
  'private_files':len(custody['all_private_evidence_files']),
  'SOURCE_CUSTODY':measure(ROOT/'SOURCE_CUSTODY.json'),
  'CLAIM_COMPARISON':measure(ROOT/'CLAIM_COMPARISON.json')},indent=2))
