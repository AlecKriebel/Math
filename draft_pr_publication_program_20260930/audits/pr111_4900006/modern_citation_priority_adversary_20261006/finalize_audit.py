"""Authenticate inputs and private source evidence; emit bounded portable audit metadata.

Does not edit source bytes, Git, services, or files outside this audit folder.
"""
import datetime
import hashlib
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent
AUDIT = ROOT.parent
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()
EXPECTED = '0e2e4e1484193c304cb2394142e24460c89a50f6ab3bb58ad838624cabb9035f'

def digest(path):
    body = path.read_bytes()
    return {'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()}

def save(name, value):
    (ROOT/name).write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True)+'\n')

diagnostic = AUDIT/'repaired_diagnostics_v2'/'COUNTEREXAMPLE.md'
diagnostic_record = {'path': 'repaired_diagnostics_v2/COUNTEREXAMPLE.md', **digest(diagnostic)}
if diagnostic_record['bytes'] != 10969 or diagnostic_record['sha256'] != EXPECTED:
    raise RuntimeError('Wrong diagnostic version')
gate_path = AUDIT/'ROOT_MATHEMATICAL_GATE_20261006.json'
gate = json.loads(gate_path.read_text())
if gate.get('all_mathematical_findings_resolved') is not True:
    raise RuntimeError('Supplied mathematical gate does not pass')
if gate.get('corrected_v2',{}).get('sha256') != EXPECTED:
    raise RuntimeError('Supplied mathematical gate has different input')

receipt_files = [
 'RETRIEVAL_RECEIPTS.json','ADDITIONAL_RETRIEVAL_RECEIPTS.json',
 'RELATED_RETRIEVAL_RECEIPTS.json','NORMALIZED_PUBLISHER_RECEIPTS.json',
 'REVIEW_RETRIEVAL_RECEIPTS.json','METADATA_RETRIEVAL_RECEIPTS.json',
]
receipts = [entry for name in receipt_files for entry in json.loads((ROOT/name).read_text())]
index = {entry['name']:entry for entry in receipts}

reading = {
 'pg_v1': ('Parker–Goluskin', 'Computation of attractor dimension and maximal sums of Lyapunov exponents using polynomial optimization', 'arXiv2510.14870v1; submitted16October2025', ['printedpp2,5–8; relevant reference chain', 'relevant definition and attainment paragraph compared withv2'], False),
 'pg_v2': ('Parker–Goluskin', 'Computation of attractor dimension and maximal sums of Lyapunov exponents using polynomial optimization', 'arXiv2510.14870v2; revised21January2026; latest version verified6October2026', ['printedpp2,5–8,27–29,43–45; relevant scope/definitions/numerical context/references'], False),
 'km2018': ('Kuznetsov–Mokaev', 'A note on finite-time Lyapunov dimension of the Rossler attractor', 'arXiv1807.00235v1; submitted30June2018; PDFdated3July2018', ['SectionII, printedpp1–2; numerical conclusions and referencesp3; nonnegative boundary inEq5'], False),
 'kuznetsov2016': ('Nikolay Kuznetsov', 'The Lyapunov dimension and its estimation via the Leonov method', 'arXiv1602.05410v3 banner26November2016; PDFfooter3July2018; PhysicsLettersA380:2142–2149(2016), DOI10.1016/j.physleta.2016.04.036', ['definitionspp1–4; concludingpp11–12; critical-point and scope footnotes'], False),
 'leonov_kuznetsov2015_v2': ('Nikolay Kuznetsov–Gennady Leonov', 'A short survey on Lyapunov dimension for finite dimensional dynamical systems in Euclidean space', 'arXiv1510.03835v2 banner19February2016; PDFfooter2July2018', ['printedpp3–4 and11, Eq46–51; relevant later critical-point/Lorenz exposition and references'], False),
 'anikushin_romanov2025': ('Mikhail Anikushin–Andrey Romanov', 'Robust upper estimates for topological entropy via nonlinear constrained optimization over adapted metrics', 'arXiv2503.11150v1; submitted14March2025; only version verified6October2026', ['introductionp3; Section4 pp11–12; Section8 pp34–37; relevant bibliography'], False),
 'anikushin_v10': ('Mikhail Anikushin', 'Variational description of uniform Lyapunov exponents via adapted metrics on exterior products', 'arXiv2304.05713v10 revised14October2025; NoDEA33:26(2026), online20November2025, DOI10.1007/s00030-025-01163-2', ['Remark3.9 printedp21; AppendixA TheoremA.2, CorollaryA.1, EqA.25 pp53–55; relevant definitions/reference chain'], False),
 'ecc2024': ('Rui Kato–Hideaki Ishii', 'A Unified Framework on Global Stability and Lyapunov Dimension of Lur’e Systems', 'EuropeanControlConference25–28June2024; officialproceedingsPDF0464', ['printedpp2793–2797; definitions and conditional corollary'], False),
 'rabinovich2018_author': ('Kuznetsov–Leonov–Mokaev–Prasad–Shrimali', 'Finite-time Lyapunov dimension and hidden attractor of the Rabinovich system', '2018 author/repository version; DOI10.1007/s11071-018-4054-z', ['Section5.1 and5.3; exact term-selected scope passages'], False),
 'bochi2018': ('Jairo Bochi', 'Ergodic optimization of Birkhoff averages and Lyapunov exponents', 'ICM2018 author version; arXiv1712.01612v3 revised23April2018', ['printedpp4–9; periodic/generic Birkhoff context, Sturmian context and Section3 matrix-cocycle nonperiodic maximizers'], False),
 'zelik_cascade_author': ('Sergey Zelik', 'A remark on a uniform Lyapunov dimension of cascade systems', 'Author version associated with CPAA7(4):971–985(2008), official journal title On the Lyapunov dimension of cascade systems; DOI10.3934/cpaa.2008.7.971', ['introductorypp1–3; Examples3.1–3.3 printedpp10–12; full relevant displayed formulas visually read'], False),
 'zelik_review_current': ('Sergey Zelik', 'Attractors. Then and now', 'arXiv2208.12101v1,25August2022; journalRMS78(4):635–777(2023), DOI10.4213/rm10095e', ['Section6.5 printedpp64–68; relevant introduction and references; currentarxivversion verified'], False),
 'wias_preprint777': ('Dmitry Turaev–Sergey Zelik', 'Homoclinic bifurcations and dimension of attractors for damped nonlinear hyperbolic equations', 'WIASPreprint777, Berlin2002; related journalNonlinearity16:2163–2198(2003), DOI10.1088/0951-7715/16/6/317', ['introductionprintedpp1–3; Corollary3.2 contextprintedp27; Remark4.3 printedp34'], False),
}

sources = []
checks = []
for name,(authors,title,version,ranges,full_read) in reading.items():
    receipt=index[name]
    if not receipt.get('success'):
        raise RuntimeError('Required source fetch failed: '+name)
    pdf=ROOT/'private_sources'/(name+'.pdf')
    txt=ROOT/'private_sources'/(name+'.txt')
    actual_pdf=digest(pdf)
    actual_txt=digest(txt)
    if actual_pdf['sha256']!=receipt['sha256'] or actual_pdf['bytes']!=receipt['bytes']:
        raise RuntimeError('PDF receipt differs: '+name)
    if actual_txt['sha256']!=receipt['extracted_text_sha256']:
        raise RuntimeError('Text receipt differs: '+name)
    sources.append({
       'id':name,'authors':authors,'title':title,'version_or_publication':version,
       'requested_url':receipt['url'],'final_url':receipt['final_url'],
       'retrieved_UTC':receipt['completed_UTC'],'private_pdf':{'path':'private_sources/'+name+'.pdf',**actual_pdf},
       'private_extracted_text':{'path':'private_sources/'+name+'.txt',**actual_txt},
       'full_body_retrieved':True,'whole_body_completely_read':full_read,
       'actual_relevant_reading':ranges,
       'text_term_scan':True,'portable_body_included':False,
    })
    checks.append({'source':name,'actual_pdf_and_text_match_receipt':True})

metadata=[]
for entry in receipts:
    if entry['name'] in reading or not entry.get('success'):
        continue
    path=ROOT/'private_sources'/(entry['name']+'.html')
    if not path.exists():
        continue
    actual=digest(path)
    if actual['sha256']!=entry['sha256']:
        raise RuntimeError('HTML receipt differs: '+entry['name'])
    metadata.append({**entry,'private_html':{'path':'private_sources/'+path.name,**actual},'body_read_scope':'public metadata, abstract, relevant notes/bibliography or source-link inventory only','portable_body_included':False})

visual=[]
for name in ['pg_v2_p2.png','pg_v2_p7.png','leonov_kuznetsov2015_v2_p11.png','zelik_cascade_author_p10.png','zelik_cascade_author_p11.png','zelik_cascade_author_p12.png','anikushin_v10_p21.png']:
    path=ROOT/'private_sources'/name
    visual.append({'path':'private_sources/'+name,**digest(path),'render_command':'pdftoppm -scale-to1800 -singlefile -png; actual PDF page matches name','visually_inspected':True,'portable_body_included':False})

def text(name):
    return (ROOT/'private_sources'/(name+'.txt')).read_text()

flags={
 'pg_v2_embedded_manifold_permitted':'lower-dimensional manifold embedded' in text('pg_v2'),
 'pg_v1_embedded_manifold_permitted':'lower-dimensional manifold embedded' in text('pg_v1'),
 'pg_v1_attainment_paragraph_present':'attained on an equilibrium or periodic orbit' in text('pg_v1'),
 'pg_v2_attainment_paragraph_present':'attained on an equilibrium or periodic orbit' in text('pg_v2'),
 'lk_eq50_source_present': '(50)' in text('leonov_kuznetsov2015_v2') and 'Eden conjecture' in text('leonov_kuznetsov2015_v2'),
 'zelik_author_direct_product_example_present':'Example 3.1.' in text('zelik_cascade_author'),
 'zelik_author_quasiperiodic_example_present':'Example 3.2.' in text('zelik_cascade_author'),
 'zelik_author_global_attractor_definition_present':'global attra' in text('zelik_cascade_author'),
 'anikushin_generic_or_particular_scope_present':'generically' in text('anikushin_v10') and 'particular systems' in text('anikushin_v10'),
 'wias_torus_context_present':'Remark 4.3' in text('wias_preprint777') and 'torus' in text('wias_preprint777'),
}
if not all(flags.values()):
    raise RuntimeError('A declared source presence control failed: '+json.dumps(flags))

gaps=[
 {'source':'Eden1989 thesis','full_body_read':False,'impact':'Historical full quantifiers and attribution cannot be certified; no historical resolution asserted.'},
 {'source':'Kuznetsov–Reitmann chapter6, DOI10.1007/978-3-030-50987-3_6','full_body_read':False,'public_read':'Official abstract, metadata, notes and bibliography','impact':'Modern book may contain additional hypotheses, discussion or prior examples; no negative-content claim made.'},
 {'source':'Zelik2008 version of record','full_body_read':False,'author_body_read':True,'impact':'Exact journal-page/numbering correspondence not certified. Author version and official publication metadata separately pinned.'},
 {'source':'Anikushin NoDEA2026 version of record','full_body_read':False,'author_v10_relevant_body_read':True,'impact':'Version differences possible; conclusions explicitly attached to authorv10; journal metadata separately authenticated.'},
 {'source':'Fedorov2018 master thesis','full_body_read':False,'impact':'Only Anikushin–Romanov2025 description read; no thesis-level proof authentication or eq-or-periodic refutation claimed.'},
 {'source':'Bousch–Mairesse and subsequent finiteness-conjecture originals','full_body_read':False,'impact':'Bochi author survey supplies relevant background only; no ODE/global-attractor realization or priority conclusion inferred.'},
]
save('SOURCE_MANIFEST.json',{
 'schema':'pr111-modern-priority-sources/v1','UTC':NOW,
 'sources':sources,'public_metadata_receipts':metadata,
 'failed_or_non_pdf_retrievals':[r for r in receipts if not r.get('success')],
 'private_visual_authentication':visual,'access_and_reading_gaps':gaps,
 'copyright_policy':'PDF/HTML/text/render bodies remain ignored under private_sources and excluded from every portable file/member manifest. Only bibliographic metadata, hashes, bounded summaries and original audit deductions are portable.',
 'no_outside_human_communication':True,
})
save('INPUT_AND_SOURCE_CONTROLS.json',{
 'schema':'pr111-modern-priority-controls/v1','UTC':NOW,
 'corrected_v2':diagnostic_record,
 'root_math_gate':{'path':gate_path.name,**digest(gate_path)},
 'root_math_gate_pass':True,'checks':checks,'source_presence_flags':flags,
 'visual_reading_count':len(visual),'other_new_priority_reports_read':False,
 'claimed_solved_publication_cleared':False,
 'limits':'Text-presence controls do not prove source meanings or novelty. Semantic and mathematical adjudications are in the reports. No new central proof-search turn.',
})

queries=[
 '"Eden conjecture" counterexample', '"Eden’s conjecture" "torus"',
 '"Lyapunov dimension" "Eden" "counterexample"',
 '"Lyapunov dimension" "Eden" "conjecture"',
 '"Lyapunov dimension" "counterexample" "periodic"',
 '"Lyapunov dimension" "quasiperiodic" "maximum"',
 '"Eden" "Lyapunov" "false"','"Eden" "Lyapunov" "quasiperiodic"',
 '"Eden" "Lyapunov" "counterexamples"','"Eden" "Lyapunov" "disproved"',
 '"Lyapunov dimension" "torus" "Eden"',
 '"Lyapunov dimension" "periodic orbits" "irrational"',
 '"Eden conjecture" "generic"',
 '"Lyapunov dimension" "Eden" "torus"',
 '"Eden conjecture" counterexample -growth -Dhar -hypercubic -Garden',
 '"Lyapunov dimension" "quasiperiodic" "maximal"',
 '"Lyapunov dimension" "periodic orbits" "counterexample"',
 'Sergey Zelik "Attractors. Then and now" arxiv',
 '"Lyapunov dimension" "Eden" "counterexample" -"Eden model"',
 '"Eden conjecture" "quasiperiodic"',
 '"maximum" "Lyapunov dimension" "torus"',
 '"Homoclinic bifurcations and dimension of attractors" Turaev Zelik 2003',
 '"A note on finite-time Lyapunov dimension" 1807.00235 DOI',
 '"Parker" "Goluskin" "Eden" conjecture counterexample correction',
 '"Eden conjecture" "false" "Lyapunov"',
]
save('QUERY_LOG.json',{
 'schema':'pr111-modern-priority-query-log/v1','UTC':NOW,
 'executed_UTC_date':'2026-10-06','exact_individual_web_query_timestamps_retained':False,
 'queries':queries,
 'additional_search_scope':'Exact source title/ID/version searches; publisher/author/repository copy searches for the book, scoped primary-source searches and review citation followups.',
 'direct_primary_pages':[r['url'] for r in receipts],
 'outcome':'No named prior exact full-Euclidean/nonvacuous disproof or PG correction located in inspected hits. A mathematically sufficient prior torus-product obstruction exists for the literal manifold-inclusive scope. Negative hits do not prove novelty.',
 'excluded_false_hits':['Dhar/Eden lattice-growth and first-passage percolation','Garden-of-Eden cellular automata','Eden–Staudacher physics','Matrix-cocycle finiteness conjecture without checked ODE realization','Rabinovich equilibrium-only negative example'],
 'exhaustive_search_claim':False,'no_external_outreach':True,
})
save('RESULT.json',{
 'schema':'pr111-modern-priority-adversary/v1','UTC':NOW,'PR':111,'problem_id':4900006,
 'original_head':'8a7270989d7064a4b97badecaa4b311db5e6d49f',
 'audited_diagnostic':diagnostic_record,'math_gate_accepted_as_input':True,
 'bounded_audit_complete':True,'bounded_audit_completion_percent':100,
 'novelty_cleared':False,'historical_conjecture_resolution_cleared':False,
 'claimed_solved_publication_cleared':False,
 'priority_status':'Prior elementary obstruction for exact unrestricted manifold-inclusive assertion; strengthened entire-R5 nonvacuous theorem novelty unresolved.',
 'explicit_published_named_Eden_refutation_located':False,
 'mathematically_sufficient_prior_theory_obstruction_adjudicated':True,
 'prior_obstruction_scope':{'phase_space':'R×T2, embedded inR5','global_attractor_relative_to_phase':'{0}×T2','equilibria':0,'periodic_orbits':0,'intrinsic_spectrum':['0','0','-1'],'intrinsic_KY':'2','ambient_extension_spectrum':['0','0','0','0','-1'],'PG_fixed_global_index':4,'PG_ambient_dimension':'4','entire_R5_compact_global_attractor':False},
 'candidate_strengthening':{'entire_R5_complete_real_analytic_flow':True,'compact_global_attractor_for_entire_phase':True,'actual_equilibria':1,'actual_periodic_circles':4,'strict_aperiodic_maximum':'203/50','strict_ambient_volume_contraction':True,'two_conventions_separately_computed':True,'finite_time_equality_claim':False,'identical_prior_full_theorem_located':False,'novelty_inferred_from_negative_search':False},
 'excluded_scopes':['original unread thesis quantifiers','Lorenz-specific','chaotic/strange-attractor-only','typical/generic/self-excited','transitive global attractors'],
 'findings':[
  {'id':'MP1','severity':'publication-blocking priority/scope','finding':'The literal unrestricted modern assertion includes phase spaces admitting the classical product-torus counterexample; it cannot be promoted as a novel longstanding solution.'},
  {'id':'MP2','severity':'mandatory framing','finding':'The candidate is stronger than the elementary prior specialization, but familiarity of the mechanism and failure to locate identical prior results neither prove duplication nor prove novelty.'},
  {'id':'MP3','severity':'material access limits for comprehensive history','finding':'Book chapter body and original thesis unread; author/journal version distinctions retained. No unread-content claim.'},
 ],
 'recommended_disposition':'Preserve mathematics as a verified stronger example/partial source-scope result. Do not issue a claimed-solved preprint framed as novel decisive Eden resolution. Parent decides already-resolved/partial classification and any separately authorized bounded research note.',
 'human_peer_review_performed':False,
 'new_central_proof_search_turns':0,'subdelegation':False,
 'other_new_priority_reports_read':False,'no_git_index_ref_PR_service_publication_mutation':True,
 'no_outside_human_communication':True,'portable_copyright_bodies_included':False,
 'absolute_novelty_assurance':'Not established, not a percent-certifiable outcome',
})

portable=[]
for path in sorted(ROOT.iterdir()):
    if not path.is_file() or path.name=='OUTPUT_MANIFEST.json':
        continue
    if path.suffix.lower() in {'.pdf','.png','.jpg','.jpeg','.html','.txt'}:
        raise RuntimeError('Unexpected potentially private body at portable root: '+path.name)
    portable.append({'path':path.name,**digest(path)})
save('OUTPUT_MANIFEST.json',{
 'schema':'pr111-modern-priority-portable-output/v1','UTC':NOW,
 'members':portable,'excluded_tree':'private_sources/',
 'no_copyright_bodies_or_renders_included':True,
 'self_hash_omitted':True,'scope':'This folder only; parent diagnosis/gate recorded as inputs but not copied.',
})
print(json.dumps({'success':True,'UTC':NOW,'input_sha256':EXPECTED,'pdf_source_count':len(sources),'source_controls_all_pass':all(flags.values()),'portable_file_count':len(portable),'output_manifest':digest(ROOT/'OUTPUT_MANIFEST.json'),'result':digest(ROOT/'RESULT.json'),'report':digest(ROOT/'REPORT.md')},sort_keys=True))
