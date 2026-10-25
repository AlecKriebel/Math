"""Emit private review notes and full proposed public prose; no page rendering."""
from pathlib import Path
import datetime
import hashlib
import json

ROOT = Path(__file__).resolve().parents[4]
PAPER = ROOT/'papers/23383961'
OUT = PAPER/'reviews/editorial'
pub=json.loads((PAPER/'publication.json').read_text())
gate=json.loads((PAPER/'promotion.json').read_text())
val=json.loads((OUT/'editorial-validation-20261025-01.json').read_text())
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(name,text):
    with (OUT/name).open('x') as f:
        f.write(text)

copy=[f"# {pub['title']}",f"By {pub['author']}, independent researcher. ORCID: {pub['orcid']}",
      'Manuscript and declared publication date: 14 October 2026 · Zenodo version 1.0 · Unrefereed preprint',
      f"Canonical URL: {pub['canonical_url']}",
      f"Search description: {pub['description']}",
      f"[Research home](https://aleckriebel.com/research/) · [Zenodo record](https://zenodo.org/records/23383961) · [DOI](https://doi.org/{pub['doi']}) · License: {pub['license']}",
      '## Original abstract',pub['abstract']]
for title,key in [('The idea in plain English','plain_language'),('The precise result','result'),('Why the result holds','why_it_works'),('Scope and limitations','limitations')]:
    copy+=['## '+title,*pub[key]]
copy+=['## Status and AI use',pub['ai_disclosure'],pub['edition_note'],
       '## Read the paper',
       f"[Open the unchanged PDF]({pub['canonical_url']}support_slit.pdf) · [Download the unchanged PDF]({pub['canonical_url']}support_slit.pdf) · [Zenodo original PDF](https://zenodo.org/records/23383961/files/support_slit.pdf)",
       'The full five-page PDF appears in the on-page reader.',
       '## Supporting materials',
       f"[Manuscript source and verification materials (ZIP)]({pub['canonical_url']}verification_package.zip) · [Zenodo original ZIP](https://zenodo.org/records/23383961/files/verification_package.zip)",
       '## Collaborate on this result',pub['collaboration'],
       '## Cite this paper',
       f"Kriebel, Alec. (2026). *{pub['title']}* (Version 1.0, 14 October 2026) [Preprint]. Zenodo. https://doi.org/{pub['doi']}",
       f"[Download BibTeX]({pub['canonical_url']}citation.bib)",
       '## Background and prior work']
copy += [f"- [{x['title']}]({x['url']}): {x['note']}" for x in pub['background']]
write('PUBLIC_COPY.md','\n\n'.join(copy)+'\n')

adapter={
 'record_id':'23383961', 'state':'EDITORIAL_BINDINGS_ONLY; RENDERING_PENDING',
 'bounded_authority':'Only the source-bound publication/promotion configs and new editorial records were authored. This is a root-facing adapter specification, not a mutation of a shared renderer, schema or site.',
 'field_mapping':{
  'title':'HTML h1, document title and citation_title; exact published title',
  'description':'Unique meta description, Open Graph description and ScholarlyArticle.description',
  'abstract':'Full unchanged original abstract in indexable HTML and ScholarlyArticle.abstract',
  'abstract_heading':'Use Original abstract as the visible heading. The current shared renderer hardcodes Abstract and ignores this field. Root must make a bounded per-page adaptation and verify actual output; do not prefix, shorten or rewrite the abstract to work around the heading.',
  'plain_language':'The idea in plain English', 'result':'The precise result',
  'why_it_works':'Why the result holds','limitations':'Scope and limitations',
  'ai_disclosure':'Status and AI use; extensive AI/unrefereed/no human or journal review/no formal certification must survive',
  'edition_note':'Display the declared manuscript/publication date separately from record-created date; do not infer priority',
  'background':'Linked credited prior work, without adopting unverified absence/example-overlap assertions from manuscript Section 5',
  'collaboration':'Actual substantive research and writing contributions plus mutual agreement; no prepared individual outreach',
  'follow_up':'null: omit the follow-up section',
  'canonical_url':'Already the final slug-derived canonical; use it in canonical tag, structured data, citation_pdf_url, Open Graph, index and sitemap when actually staged',
  'source_binding':'Private source identity/custody; not public prose',
  'review_metadata':'Private preparation state; not public prose'
 },
 'custom_verdict_requirements':{
  'root_authority':'promotion.status PASS is the later root scientific disposition, bound to the exact root-clearance hash; it is not a live/browser/native-publication pass.',
  'scope_original':'Preserve the complete reviews.scope.verdict object including status=SCOPE_COMPLETE_PENDING_INDEPENDENT_MATHEMATICAL_REVIEW, mathematical_pass=false, scientific_verdict=null, defect_found=null and ready_to_publish=false. The frozen candidate retains mathematical_pass=false, ready_to_publish=false and canonical_url=null.',
  'analytic_original':'Preserve complete original object: status=analytic_pass_no_substantive_defect_found, publication_clearance=false and remaining_analytic_gap=null. Root disposition is separately PASS.',
  'adversarial_original':'Preserve complete original object: verdict=PASS_SCIENTIFIC_SCOPE, substantive_defect_found=false and unresolved_mathematical_gap=null. Root disposition is separately PASS.',
  'bounded_mapping':'Read each complete original object and its separately copied root_disposition. Do not rewrite source verdicts or turn the scope-only pending gate into an original mathematical PASS. Later root scope_gate_resolution explains chronology.'
 },
 'asset_specification':{
  'pdf':'Copy support_slit.pdf from the bound sources without modification; iframe/embed uses the identical local asset. Provide a direct-open link and a download link with a download attribute, plus a clear original Zenodo link. Do not regenerate the PDF.',
  'supplement':'Copy the complete verification_package.zip unchanged; provide local download and Zenodo original links. Do not extract/trim/repack it as the public supplement.',
  'no_other_assets':'No additional reader or public third-party cached primary texts. The ZIP contains no embedded PDF reader or nested archive.',
  'download_adapter':'The shared renderer currently offers direct PDF opening and the original Zenodo link but no explicit local PDF download attribute. Root should include that bounded per-page link and verify it with the final assets. The separate supporting-material links in PUBLIC_COPY must be carried through even though related_resources is empty.'
 },
 'metadata_specification':{
  'author':'Alec Kriebel; ORCID 0009-0001-9320-500X', 'version':'1.0',
  'datePublished':'2026-10-14', 'record_created_utc':'2026-10-15T04:00:29.066300+00:00',
  'creativeWorkStatus':'Unrefereed preprint', 'doi':'10.5281/zenodo.23383961',
  'license':'CC BY 4.0','canonical_url':pub['canonical_url'],
  'scholarly_graph':'Use exact title, author/ORCID, version, declared date, DOI, full original abstract, PDF encoding and unrefereed status. Keep internal review dates/hashes/check counts out of the public graph and text.'
 },
 'expected_sections':['Original abstract','The idea in plain English','The precise result','Why the result holds','Scope and limitations','Status and AI use','Read the paper','Supporting materials','Collaborate on this result','Cite this paper','Background and prior work'],
 'remaining_root_gates':['actual rendered public-copy and source-asset comparison','local HTTP and link/download checks','live HTTP and byte-identical PDF/ZIP checks','desktop/mobile browser inspection','native Sheet AA URL only after verified live'],
 'native_sheet_aa_url':None,
 'website_rendered':False,'live_verified':False,'browser_verified':False,'native_tracker_modified':False
}
write('SCHEMA_ADAPTER.json',json.dumps(adapter,ensure_ascii=False,indent=2)+'\n')

report=f'''# Editorial preparation report: Zenodo 23383961

Completed {now}. Reviewer/editor: GPT-6.1 Sol, Ultra. Completion estimate: **100% of the assigned source-bound editorial preparation**. Website rendering, live/browser verification and native publication tracking remain outside this assignment.

## Disposition and exact authority

Prepared the previously absent `papers/23383961/publication.json` and `promotion.json`, plus new artifacts only under `reviews/editorial/`. The promotion binds the exact later root scientific clearance at `verification/root-clearance-23383961-20261025.json`, SHA-256 `2a9214e52b408d2a67a4aef4d6887b8cf86f8eb46f99423ad977c4a8cf847122`. It is not a rendered, live, browser or native-Sheet publication PASS. The config state is `BINDINGS_READY_RENDERING_PENDING`.

The exact cleared result concerns normalized schlicht S and the fixed functional Re[a2+i*10^-24*(a4-3a3)]. Genuine global maximizers exist, and **every** global maximizer has an **actual** omitted analytic slit with nonmonotone continuous polar argument, signed **outward** radial angle and ordinary unsigned radial angle. Both monotone directions are excluded. No explicit maximizing map or uniqueness is asserted. The proof outline preserves the essential actual-slit realization: actual tip below3/10, constructed radius above25/81, agreement near infinity, and local uniqueness/open-closed continuation. It preserves the infinity limit needed for signed beta and the interior zero needed for its absolute value. Tangent-direction waver is not substituted for the target observables.

## Complete reading and source identity

Read the active goal, `MODEL_POLICY.md` and project `AGENTS.md`; read the entire actual five-page deposited PDF by fresh extraction and visual inspection of all five rendered pages; read the complete current `support_slit.tex`; then read all three complete final reports, all three exact verdicts, the root clearance, original scope candidate, deposited API metadata and source receipt. This is editorial assimilation of the independently cleared evidence, not a new independent mathematical review.

The original full abstract is preserved exactly under the established mathematical typography normalization and explicitly labeled **Original abstract**. A fresh comparison matches every source abstract word; the PDF abstract word comparison independently matches after replacing only the mathematical expression and normalizing ligatures/whitespace. The source TeX hash is `c4e557a58999b938578eb105c03d7224f087c04f273dbbd86e09ab45b855a4b3`.

The manuscript and declared Zenodo publication date are14October2026; version1.0. The record was created15October2026 at04:00:29.066300+00:00. The config distinguishes those dates and makes no date-derived priority claim. Author, ORCID, DOI, version, published record status, asset names, sizes, hashes and receipt identity are bound.

## Scientific wording and public copy

`PUBLIC_COPY.md` supplies the full proposed public copy, including the original abstract, accessible explanation, exact theorem, proof outline, limitations, AI/unrefereed/no-human-peer-review disclosure, edition dates, citation, substantive collaboration wording with actual contributions and mutual agreement, and linked credited classical work. It contains no private review timestamps, hashes, replay counts, source implementation details or internal review narratives.

The public explanation credits Hayman–Lingham’s original Problem6.72, Pfluger/Duren support geometry and conventions, Brown’s restricted positive point-evaluation family, deBranges coefficient bounds and the manuscript’s Friedland–Schiffer credit. No exact absence-of-earlier-example or example-overlap assertion from the wider Section5 comparisons is promoted. Those historical comparisons were not comprehensively re-audited by the current mathematical pass; Duren commentary and Hibschweiler remain uninspected leads. No firstness, exhaustive novelty or current-worldwide-openness claim is made. The archived original abstract is not silently rescaled or rewritten. Follow-up remains null.

## Fresh validation and custody

`editorial-validation-20261025-01.json` records **{val['checks_passed']} successful editorial assertions**. These assertions test source/config/custody consistency, not {val['checks_passed']} independent mathematical claims. They verify exact root authority and scope, full abstract/source identity, complete preserved custom verdict objects, source receipt/metadata/dates, final canonical slug, assets, searchable five-page PDF, all255 ZIP member bytes including12hidden members, no embedded reader or nested archive, all259 frozen source files unchanged, all159 existing review-seal bindings and the root custody receipt. Source helpers, builds and mathematical programs were not executed. The fresh validator writes only a caller-specified unused editorial stem.

Deposited PDF SHA-256: `a6d227d606fda3e68adc6db4eab462ee3f12b0544a201121b5c3a21aa5099e3d`.

Deposited ZIP SHA-256: `58853fd56272184efe8232c58c356b1a669ba43032e3c4f35e4b17e317898f51`.

Publication config SHA-256: `{val['publication_sha256']}`.

Promotion config SHA-256: `{val['promotion_sha256']}`.

All original source files, scope/analytic/adversarial/root reports, verdicts, source candidates, seals and root clearance are preserved. The original scope verdict still has its exact pending/null/false fields, and the candidate still has its original null canonical URL. The later root disposition is separate; it does not retroactively rewrite the scope worker’s evidence.

## Bounded adapter and remaining gates

Proposed final canonical: {pub['canonical_url']}

`SCHEMA_ADAPTER.json` identifies the bounded mapping required for actual staging. The shared renderer currently hardcodes the heading “Abstract”; the actual page must use “Original abstract” while keeping the full field unchanged. It also needs explicit local PDF download behavior and the complete supplement/local-original link set in the proposed copy. The source receipt is already standard; no shared normalization change was made. Consumers must preserve complete custom verdict objects and consult separate root dispositions rather than manufacture conventional status values.

The page must carry title, author/ORCID, date/version/status, full scholarly/citation metadata, canonical, indexable prose, direct-open/download/embed of the unchanged PDF, the complete unchanged ZIP, Zenodo original links, research navigation/index and sitemap. These are specifications, not completed render checks. Root retains actual rendered-copy, local/live HTTP and byte checks, desktop/mobile browser checks, and native Sheet publication gates. The canonical config is final-slug-derived now; native AA stays blank until verified live.

No site, shared script, Git, spreadsheet, release, deployment, browser/UI or external-communication action was performed. The frozen live47/readiness51 state and the other publication stages were not touched. No children were spawned and no scientific repair was attempted.
'''
write('REPORT.md',report)
before=json.loads((OUT/'source-custody-before.json').read_text())
log=f'''# Editorial research log: support slit

- {before['utc']} — Checkpoint20%: scoped ownership to absent publication/promotion configs and new editorial artifacts; froze the259-file source baseline. Authority, exact claim and preservation requirements read. No publication action.
- {pub['review_metadata']['prepared_utc']} — Checkpoint80%: full reader/source/report assimilation completed and source-bound configs written. Full original abstract retained; exact fixed-functional every-actual-maximizer scope and bounded historical credit retained. Final canonical chosen; follow-up null.
- {val['utc']} — Checkpoint95%: fresh editorial validator passed711 assertions, including source custody, all archive members, all original custom verdicts and159 review-seal bindings. No submitted mathematical program executed.
- {now} — Checkpoint100% for assigned editorial preparation: full proposed public copy, bounded schema/asset adapter and complete report written. Website render/live/browser/native-publication gates remain with root. Seal to follow; no original evidence changed.
'''
write('RESEARCH_LOG.md',log)
read_ledger={
 'utc':now,'editor_model':'gpt-6.1-sol','reasoning_effort':'ultra',
 'reading':[
  {'path':str(PAPER/'sources/support_slit.pdf'),'scope':'all five pages by fresh extraction and all five fresh rendered PNGs; source unmodified'},
  {'path':str(PAPER/pub['source_binding']['source_tex_path']),'scope':'complete released current manuscript'},
  *[{'path':str(PAPER/x['report']),'scope':'complete final report'} for x in gate['reviews'].values()],
  *[{'path':str(PAPER/x['verdict_file']),'scope':'complete exact verdict object, retained unchanged in promotion'} for x in gate['reviews'].values()],
  {'path':str(ROOT/gate['root_clearance_file']),'scope':'complete exact authority'},
  {'path':str(PAPER/'reviews/scope/candidate.json'),'scope':'complete original abstract, source/scope candidate and preserved gate'},
  {'path':str(PAPER/'sources/record.json'),'scope':'complete original metadata'},
  {'path':str(PAPER/'sources/receipt.json'),'scope':'complete original receipt'},
  {'path':str(ROOT/'MODEL_POLICY.md'),'scope':'complete'},
  {'path':'/Users/alec/Documents/Math/AGENTS.md','scope':'complete'},
  {'path':'/Users/alec/.codex/attachments/97d02095-52a0-400f-a038-cbc727c7c885/goal-objective.md','scope':'complete'}
 ],
 'reference_schema_only':['papers/22089807/publication.json','papers/22089807/promotion.json','papers/23203100/publication.json keys','papers/23306332/publication.json keys','scripts/render_page.py read-only'],
 'primary_literature_boundary':'No fresh historical source inspection by this editorial worker; use the exact bounded primary interfaces and gaps in the complete cleared scientific reports/root authority. Wider comparisons are not certified.',
 'no_submitted_math_execution':True,'no_source_mutation':True,'no_publication_action':True
}
write('READ_LEDGER.json',json.dumps(read_ledger,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'artifacts':['PUBLIC_COPY.md','SCHEMA_ADAPTER.json','REPORT.md','RESEARCH_LOG.md','READ_LEDGER.json'],'completion_percent':100}))
