"""Assemble this review's ledgers; reads originals and writes only HERE."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import hashlib, json, re, zipfile

HERE = Path(__file__).resolve().parent
P = HERE.parents[3]
SOURCE = HERE.parent.parent / 'sources'
utc = lambda: datetime.now(timezone.utc).isoformat()
def bind(path):
    b = path.read_bytes()
    return dict(bytes=len(b), sha256=hashlib.sha256(b).hexdigest())
def dump(name, obj):
    path = HERE / name
    if path.exists():
        raise RuntimeError('Refusing to replace ledger: ' + str(path))
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n')

before = json.loads((HERE / 'SOURCE_BINDINGS_BEFORE.json').read_text())['files']
for name, spec in before.items():
    if bind(Path(name)) != spec:
        raise RuntimeError('Original source changed: ' + name)
ready = json.loads((SOURCE / 'SOURCE_READY.json').read_text())
initial = json.loads((HERE / 'INITIAL_SEAL.json').read_text())
if bind(HERE / 'INITIAL_RECONSTRUCTION.md')['sha256'] != initial['reconstruction_sha256']:
    raise RuntimeError('Early reconstruction changed')
if bind(HERE / 'INITIAL_READ_LEDGER.json')['sha256'] != initial['read_ledger_sha256']:
    raise RuntimeError('Early ledger changed')
objects = {}
for name in ['SOURCE_READY.json', 'SOURCE_READY_MANIFEST.json', 'SOURCE_READY_SEAL.json',
             'SOURCE_MANIFEST.json', 'SOURCE_SEAL.json', 'record.raw.json', 'latest.raw.json',
             'versions.raw.json', 'normalized-metadata.json', 'api-and-file-receipts.json',
             'assets-acquired.json', 'archive-members.json']:
    objects[name] = json.loads((SOURCE / name).read_text())
dump('ORIGINAL_SOURCE_OBJECTS.json', dict(originals=objects, note='Whole objects copied verbatim in meaning; no source schema aliases or fabricated facts. Sources remain authoritative.'))

members = []
with zipfile.ZipFile(SOURCE / 'mtp2-edge-closure-verification.zip') as z:
    names = set()
    for info in z.infolist():
        name = PurePosixPath(info.filename)
        if name.is_absolute() or '..' in name.parts or info.filename in names or info.is_dir():
            raise RuntimeError('Unexpected archive member')
        names.add(info.filename)
        data = z.read(info)
        extracted = SOURCE / 'published-source' / info.filename
        if data != extracted.read_bytes():
            raise RuntimeError('Archive/extraction mismatch: ' + info.filename)
        members.append(dict(member=info.filename, bytes=len(data), crc32=f'{info.CRC:08x}',
                            sha256=hashlib.sha256(data).hexdigest(), exact_extracted_path=str(extracted), equal=True))
if len(members) != 13 or sum(x['bytes'] for x in members) != 203829:
    raise RuntimeError('Unexpected member count or expansion')
if (SOURCE / 'published-source/output/pdf/mtp2_edge_closure.pdf').read_bytes() != (SOURCE / 'mtp2-edge-closure-note.pdf').read_bytes():
    raise RuntimeError('Embedded reader mismatch')

prim = json.loads((HERE / 'RAW_PRIMARY_BINDINGS.json').read_text())
details = {
 'lauritzen-2022': ('Physical5–7 / printed3125–3127; entire contribution', 'Literal M_I edge-only definition, global Markov/MTP₂ and Conjectures1–3; no inference of current openness.'),
 'kahle-sullivant-v1': ('Whole15-page actual PDF text; physical7 image', 'Natural-lattice requirement, clique-design Prop4.1/Lem5.4/Th5.5 and complete proofs; Th6.1 and Example6.5; methods already prior work.'),
 'geiger-meek-sturmfels-published': ('Physical6–8 / printed1468–1470; Appendix physical25–29 /1487–1491', 'Definitions and proofs of Th3.1–3.2, A-feasibility, toric closure, faciality LemA.2; finite factors require extra support feasibility.'),
 'gandolfi-lenarda-published': ('Physical10–12 / printed415–417, including full Lem5.1/5.2 proofs; next examples context', 'Exact earlier weighted equality-support counterexample, credited; publication-date metadata read separately.'),
 'luz-published': ('Physical10–14 / printed1445–1449, section4.4 opening/Lem4.9 proof', 'All-pair lattice support reconstruction and extended-family compactness; not directly original-edge finite-factor closure; target handles n≤1 independently.'),
 'fallat-published': ('Physical21–23 / printed1172–1174, full Th7.5 proof', 'Strictly positive edge potentials for converse cancellation; zero-containing potential converse is not imported.'),
 'kz-published': ('Physical4–5 / printed150–151, full relevant F₂ statement/construction', 'Quadratic submodular cut construction on n+2 vertices, no auxiliary vertices; label convention differs consistently.'),
 'pq-report': ('Physical8–10 / printed3–5, full TheoremI and proof; physical9 image', 'Residual reachability/flow conservation and cut saturation; actual1979 report body rather than publisher1980 byte claim.'),
 'kr-published': ('Physical5–8 / manuscript5–8, definitions2.1 and full relevant sections2.1–2.2', 'Classical reparameterization, nonnegative normal form and residual maximum-flow constant updates; author manuscript layout, not publisher-byte authentication.'),
}
ledger = []
for x in prim['files']:
    spec = bind(Path(x['path']))
    if spec['sha256'] != x['sha256'] or spec['bytes'] != x['bytes']:
        raise RuntimeError('Raw primary changed')
    y = dict(x)
    y.update(read_extent=details[x['name']][0], exact_interface=details[x['name']][1],
             full_body_read=x['name']=='kahle-sullivant-v1', read_after_own_early_seal=True,
             no_prior_audit_conclusion_used=True)
    ledger.append(y)
dump('PRIMARY_LEDGER.json', dict(utc=utc(), entries=ledger,
     scope='Critical proof bodies read, not metadata/snippets substituted. Extents are explicit; full paper read claimed only for KS.',
     third_party_fulltexts_private_ignored=True, duplicate_primary_PDFs_created=0,
     retained_KR_layout='author manuscript, despite short custody label kr-published'))

tex = (SOURCE / 'published-source/mtp2_edge_closure.tex').read_text()
abstract = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', tex, re.S).group(1)
old = json.loads((HERE / 'INITIAL_READ_LEDGER.json').read_text())
if abstract != old['original_abstract']:
    raise RuntimeError('Original abstract drift')
dump('READ_LEDGER.json', dict(utc=utc(), actual_pdf=old['actual_PDF'], controlling_TeX=old['controlling_TeX'],
     original_abstract=abstract, all_five_actual_pdf_pages_subsequently_viewed=True,
     full_source_support_read=['README.md', 'SUPPLEMENT.md', 'verify_boundary.py', 'verify_priority_examples.py', 'REPRODUCE.py', 'BUILD_RECEIPT.json', 'MANIFEST.json', 'LICENSE.txt', 'zenodo-deposit.json'],
     generated_expected_JSON='Complete objects parsed/replayed and exact output equality checked; not a historical approval authority.',
     original_source_interface_full_read=True, initial_seal=str(HERE/'INITIAL_SEAL.json'),
     primary_ledger='PRIMARY_LEDGER.json', source_programs_read_before_execution=True,
     historical_audit_reports_read=False, sibling_or_root_current_final_reports_or_verdicts_read=False,
     later_raw_coordination='Raw primary paths/hashes after early seal; scope shortcut observations after all early seals, not adopted as authority.',
     model='GPT-6.1 Sol Ultra', children_spawned=0))

dump('ACCESS_LEDGER.json', dict(utc=utc(), primary_transport='Reuse scope fresh200 bodies and retained originals in place; this adversarial family did not refetch those PDFs.',
 fresh_primary_receipt=str(HERE.parent/'scope/primary-fetch-receipts.json'),
 publisher_date_receipt=str(HERE.parent/'scope/publisher-date-receipt.json'),
 current_primary_metadata_checks=[
 {'url':'https://arxiv.org/abs/2411.03139','finding':'Only v1 submitted5Nov2024 displayed; no additional revision claimed.'},
 {'url':'https://www.thomas-kahle.de/publications/','finding':'KS item to appear ProcAMS2025; general author policy prefers maintained arXiv text; no uninspected publisher-byte identity claimed.'},
 {'url':'https://sethsullivant.wordpress.ncsu.edu/publications/','finding':'KS listed to appear ProceedingsAMS; primary metadata only.'}],
 bounded_searches=['Exact target title and closedness/attractive/MTP2 edge terms', 'KS title, arXiv version history, both author publication pages'],
 inference_limits='No failed search establishes novelty, priority, or present openness. No external communication or preparation of outreach.'))

protected = {}
for rel in ['papers/23333353/reviews/editorial/SEAL.json', 'papers/23416806/reviews/editorial/SEAL.json',
 'papers/23441617/reviews/editorial/SEAL.json', 'papers/23217863/reviews/scope/FINAL_SEAL.json',
 'verification/ambient-block-modulus-navigation-correction-sol-20261025/SEAL.json',
 'verification/checkpoint-subtree-diagnostic-sol-20261025/SEAL.json',
 'verification/cylinder-discotope-code-audit-sol-20261025/FINAL_SEAL.json',
 'redirects/cubic-hessian-preflight-sol-20261025/SEAL.json']:
    path = P / rel
    protected[str(path)] = bind(path)
source_after = {str(x):bind(x) for x in sorted(SOURCE.rglob('*')) if x.is_file()}
original_bindings = dict(source_after)
original_bindings.update({x['path']:dict(bytes=x['bytes'],sha256=x['sha256']) for x in prim['files']})
for rel in ['primary-fetch-receipts.json','publisher-date-receipt.json','Retained-primary-bindings.json']:
    path=HERE.parent/'scope'/rel
    original_bindings[str(path)]=bind(path)
original_bindings.update(protected)
dump('CUSTODY.json', dict(utc=utc(), original_bindings=original_bindings,
     all_before_source_bindings_preserved=True, before_source_count=len(before), after_source_count=len(source_after),
     source_owner_additions=[x for x in source_after if x not in before],
     additions_note='SOURCE_MANIFEST/SOURCE_SEAL added by source owner, not this family; all initial25 source files unchanged.',
     archive_member_comparisons=members, selected_embedded_reader_equal=True, nested_archives=0,
     preserved_early_seal=bind(HERE/'INITIAL_SEAL.json'), protected_prior_seals_only=protected,
     do_not_follow_stale_mutable_site_core_baselines=True,
     writes_confined_to_own_namespace=True, public_or_shared_mutations=False))

dump('VERDICT.json', dict(schema='independent_adversarial_mathematical_review', record_id='23146753', row=105,
 status='COMPLETE', mathematical_disposition='PASS_FULL_LITERAL_THEOREM_WITH_EXPLICIT_SCOPE_AND_PRIORITY_LIMITS',
 full_claim='For every finite simple G, binary MTP2 laws with finite nonnegative unary/original-edge factors equal closure of strictly positive attractive Ising laws on unchanged G; exact source edge-only closedness corollary, including zeros/pins/ties/isolates/empty cases.',
 strongest_verified_result='Complete deposited theorem, both inclusions and literal-source corollary; no narrowing or repair.',
 central_mathematical_gap=None, substantive_defects=[], unresolved_central_imports=[],
 priority_status='UNKNOWN beyond bounded inspected primary comparison; no firstness or current worldwide-open claim.',
 prior_credit=['GMS finite factors/toric closure/facial support','LUZ binary lattice support and extended MTP2 family','Fallat positive potential criterion','KS natural-lattice factorization and framework','classical KZ/PQ/KR cuts/residual reparameterization','Gandolfi–Lenarda earlier exact counterexample'],
 ancillary_limits=['Finite controls do not prove arbitrary graph theorem.','KR retained body is author manuscript, not publisher-final bytes.','KS numerical example sentence overlaps bottom assignment; support obstruction and GL table independently checked, as deposited supplement acknowledges.','No proof-assistant or human peer-review certification.'],
 independent_early_seal=bind(HERE/'INITIAL_SEAL.json'), own_controls='CONTROL_RESULTS.json', proof_derivations='DERIVATIONS.md',
 source_program_replay='EXECUTION_LEDGER.json', report='REPORT.md', final_followup=None,
 publication_authority=False, public=False, rendered=False, browser_verified=False, native_verified=False,
 canonical=None, AA=None, root_adoption=None, no_outreach=True))

with (HERE/'RESEARCH_LOG.md').open('a') as f:
    f.write(f'\n{utc()} — checkpoint:85%; independent all-size proof/primary checks and distinct exact controls complete; finishing read-only custody verification. Initial seals remain immutable.\n')
print(json.dumps(dict(assembled=True, source_files=len(source_after), original_bindings=len(original_bindings), members=len(members)),indent=2))
