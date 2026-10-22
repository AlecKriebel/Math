#!/usr/bin/env python3
"""Build authored inspection metadata without redistributing primary-source bodies."""
from pathlib import Path
import datetime
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parent
SCOPES = {
    'owr': ('Original publisher report; contribution and exact question', ['Problem 5.', 'total number'], 'Physical pages 25–27 inspected; printed 1137–1139. The relevant Problem 5 is physical 27, not the unrelated Problem 5 elsewhere in the report.'),
    'gs_v5': ('Latest arXiv version as listed on current abstract page: v5, 2021-09-28', ['Problem 5.6.', 'Proposition 5.7.', 'Theorem 1.', 'Theorem 5'], 'Sections 1, 4, 5.2–5.3; theorem/model bodies and the entire Proposition 5.7 proof inspected. Not every regularity lemma proof independently re-audited here.'),
    'gs_eccc_r2': ('Latest listed ECCC revision: revision 2, 2021-09-28', ['Problem 5.6.', 'Proposition 5.7.'], 'Exact comparison question and partial-transfer statement checked; archive history checked.'),
    'gs_tau_author': ('Undated current TAU author copy; 28 PDF pages; not identified as journal VoR', ['Problem 5.6.', 'Proposition 5.7.'], 'Section 5.3 checked. The question persists. Different bytes and pagination from arXiv; no assertion of complete textual identity.'),
    'goldreich_r3': ('Author revision dated 2021-10-04; latest revision listed by author page', ['October 4, 2021', 'Theorem 2.3', 'Corollary 2.4', 'Proposition 2.11', 'Theorem 2.12', 'Theorem 2.13'], 'Model, one-sided conversion proof, explicit separation examples, partition and subgraph upper-bound mechanisms, bounded-degree/minor-free upper bounds and concluding discussion inspected.'),
    'goldreich_r2': ('Older author revision dated 2019-07-14', ['July 14, 2019', 'Theorem 2.3', 'Proposition 2.11'], 'Date, relevant theorem statements and comparison to current R3; not all older proofs re-read.'),
    'fei_v2': ('Latest arXiv version as listed on current abstract page: v2, 2026-08-12', ['Definition 1.2.', 'Definition 1.3', 'Theorem 1.5', 'Definition 7.1.', 'Lemma 7.4.', 'Corollary 7.5.', 'The power of'], 'Definitions 1.2–1.3, Remark 1, Theorem 1.5, Sections 1.3–1.4 and 2.1–2.2, entire Section 7.1 including Lemma 7.4 proof, and Section 8 inspected. Main square-freeness upper-bound technical body not independently audited.'),
    'cfp_v1': ('Current arXiv lists only v1, 2024-04-17; STOC 2024 predecessor', ['Theorem 1.1.', 'Theorem 1.2.', 'Lemma 2.2.'], 'Model, main theorem statements, Section 2.1 birthday lemma and its Section 6.2 proof, and lower-bound framework inspected. No VDF graph comparison theorem found in these inspected portions.'),
    'container_v1': ('Current arXiv lists only v1, 2026-08-02', ['Theorem 1.4', 'Theorem 1.14', 'Theorem 1.15'], 'Uniform dense model, main characterization theorem and its proof, partition/large-substructure statements and mechanisms checked. Whole extracted text searched for distribution, weight, VDF, blowup; no VDF transfer theorem found.'),
    'polynomial_survey': ('Current arXiv lists only v1, 2025-08-23', ['Theorem 2.7', 'Theorem 3.1'], 'Sections 1–2, triangle-lower-bound discussion and Section 3 relevant statements inspected; whole extracted text searched for distribution/vertex-distribution with no hits. Survey, not a primary proof for the older theorems it discusses.'),
    'triangle_akkr_journal_author': ('Full author manuscript of journal work, not publisher VoR', ['Theorem 3 Let', '6.1', 'Independence Observation'], 'Theorem 3 and its Condition 1 proof, physical pages 24–27: two-fold parallel/cross parity construction and adaptive query simulation inspected. Condition 2 construction inspected only for context. Journal publication metadata separately verified at SIAM DOI 10.1137/07067917X.'),
    'triangle_akkr_author': ('Short conference-style author copy; superseded for body inspection by full author manuscript', ['Theorem 4.', 'From 1-sided error'], 'Section 6 statement and parity construction inspected before full author copy was recovered.'),
    'as_directed': ('Author manuscript for STOC 2003 / JCSS 2004, not publisher VoR', ['Theorem 4 Let', '7    Two-Sided', 'Proof of Theorem 4, part (ii)'], 'Theorems 2–4 and Section 7 entire two-sided lower-bound proof inspected. Physical pages 26–27 give older deletion worlds, random permutations and a three-vertex exposure bound.'),
    'triangle_alon2002': ('Author-paper copy hosted in Princeton course archive', ['Theorem 1', 'Behrend'], 'Definitions, main bipartite/nonbipartite classification and lower-bound construction inspected. Original journal metadata verified at DOI 10.1002/rsa.10056.'),
    'color_ak2002': ('Author manuscript hosted in Princeton course archive', ['Theorem 3', '4 '], 'Definitions, Theorem 3 and Section 4 colorability sampling proof inspected. Already a cited prior ingredient in the pinned proof.'),
    'ggr1998': ('Copy of original JACM article, faculty course mirror, 98 PDF pages', ['10.1.3.', '10.1.4.'], 'Physical pages 85–86 / printed 737–738, product-distribution extension and arbitrary-edge-distribution impossibility inspected directly.'),
    'lovasz_szegedy_v2': ('Current arXiv lists v2, 2008-03-11; later Israel J. Math. 178 (2010)', ['2.4    W', 'Definition 3.2', 'Proposition 3.9'], 'W-random graph definition and function-property/testability and hereditary-closure statements inspected. Not a complete audit of the graphon theory.'),
    'rs_volume': ('Publisher-volume bibliographic record only', ['Ruzsa', '939'], 'Volume bibliography inspected; original seven-page Ruzsa–Szemerédi article not recovered.'),
    'shapira_icm2022': ('Publisher VoR, ICM2022 chapter DOI10.4171/ICM2022/36', ['Theorem 4.10', 'Theorem 4.7', 'Removal for weighted'], 'Section 4.4 weighted-removal definition, Theorem 4.10 and discussion inspected; Section 4.3 classical prescribed-growth theorem checked. No quantitative classical/VDF comparison asserted.'),
}

receipts = json.loads((ROOT / 'FETCH_RECEIPTS.json').read_text())
rows = []
for item in receipts:
    row = dict(item)
    if item['id'] in SCOPES:
        version, terms, coverage = SCOPES[item['id']]
        row.update(version_or_role=version, inspection_coverage=coverage)
        if item.get('is_pdf'):
            pdf = ROOT / item['local_cache']
            txt = pdf.with_suffix('.txt')
            if not txt.exists():
                subprocess.run(['pdftotext', '-layout', str(pdf), str(txt)], check=True)
            body = txt.read_text()
            row['pdf_pages'] = body.count('\f')
            row['phrase_page_index'] = {
                term: sorted({body.count('\f', 0, match.start()) + 1
                              for match in re.finditer(re.escape(term), body)})
                for term in terms
            }
    if item['id'] == 'gs_journal':
        row.update(version_or_role='Journal VoR retrieval attempt', inspection_coverage='No PDF obtained: redirected to subscription/cookie HTML; must not be treated as inspected journal theorem body.')
    if item['id'] == 'gs_journal_page':
        row.update(version_or_role='Official journal metadata/preview', inspection_coverage='Israel Journal of Mathematics 245 (2021), 787–837; VoR 2021-10-30; full article body unavailable.')
    if item['id'] == 'behrend_archive':
        row.update(version_or_role='Original Behrend archive retrieval attempt', inspection_coverage='Returned reCAPTCHA HTML, not article content; no independent full-text inspection claimed.')
    if item['id'] == 'polynomial_survey_vor_xml':
        row.update(version_or_role='Elsevier VoR API metadata only', inspection_coverage='1950-byte XML contains core metadata, no theorem/full text. DOI10.1016/j.cosrev.2025.100806, November2025. No VoR-body equivalence assumed.')
    if item['id'] == 'sublinear99':
        row.update(version_or_role='Open problem page, oldid1300', inspection_coverage='Full visible page inspected; last edited2019-08-26; broad VDF/EDF questions, no current update on exact GS5.6.')
    rows.append(row)

payload = {
    'schema': 'primary-source-priority-inspection-ledger-v1',
    'generated_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'query_date': '2026-10-17',
    'technical_sources_are_primary_papers': True,
    'discovery_metadata_is_not_technical_validation': True,
    'source_bodies_only_in_ignored_tmp': True,
    'journal_vor_body_unavailable': True,
    'sources': rows,
}
(ROOT / 'SOURCE_VERSION_LEDGER.json').write_text(json.dumps(payload, indent=2) + '\n')

metadata = []
for name in ['crossref_gs.json', 'crossref_survey.json', 'openalex_target.json', 'openalex_citers.json']:
    file = ROOT / 'tmp' / name
    if file.exists():
        data = file.read_bytes()
        metadata.append({'cache': 'tmp/' + name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
(ROOT / 'CITATION_DISCOVERY_RECEIPT.json').write_text(json.dumps({
    'date': '2026-10-17',
    'crossref': 'Exact-title metadata queries located journal and conference records; no technical claims based on metadata.',
    'openalex': 'DOI10.1007/s11856-021-2228-8 resolved W2950686339. cites-filter returned only one 2020 mathematical-probability article. This is demonstrably incomplete: Fei2026 cites the target but was absent. Not an exhaustive citation audit.',
    'semantic_scholar': 'ARXIV1905.09903 graph API request returned HTTP429; no usable citing-paper list retrieved.',
    'metadata_receipts': metadata,
}, indent=2) + '\n')
print(json.dumps({'source_receipts': len(rows), 'pdf_responses': sum(bool(x.get('is_pdf')) for x in rows)}))
