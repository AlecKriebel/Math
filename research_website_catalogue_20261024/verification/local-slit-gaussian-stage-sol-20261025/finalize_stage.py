"""Seal a complete private-stage package; never change original inputs."""
from pathlib import Path
import ast,datetime,hashlib,json,re
O=Path(__file__).resolve().parent;R=O.parents[1]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,obj):
 p=O/name;assert not p.exists(),p;p.write_text(obj if isinstance(obj,str) else json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
before=json.loads((O/'inputs-before.json').read_text())['bindings']
after={path:{'bytes':Path(path).stat().st_size,'sha256':sha(Path(path))} for path in before}
assert before==after
save('integrity-after.json',{'utc':now(),'status':'PASS','original_bindings':len(before),'unchanged':True,'bindings':after})
source={}
for rid in ['23383961','23430906']:
 p=R/'papers'/rid;c=json.loads((p/'publication.json').read_text());g=json.loads((p/'promotion.json').read_text())
 source[rid]={'publication':{'path':str(p/'publication.json'),'sha256':sha(p/'publication.json')},'promotion':{'path':str(p/'promotion.json'),'sha256':sha(p/'promotion.json')},'original_source_binding':c['source_binding'],'original_custom_reviews':g['reviews'],'later_root_authority':{'path':g['root_clearance_file'],'sha256':g['root_clearance_sha256'],'scope_gate_resolution':g['scope_gate_resolution']},'root_editorial_authority':{'path':f'verification/root-editorial-{rid}-20261025.json','sha256':sha(R/f'verification/root-editorial-{rid}-20261025.json')},'full_actual_public_copy':{'path':f'public-copy-{rid}.txt','sha256':sha(O/f'public-copy-{rid}.txt')},'full_actual_sections':{'path':f'public-sections-{rid}.json','sha256':sha(O/f'public-sections-{rid}.json')}}
save('source-bindings.json',{'utc':now(),'records':source,'original_objects_preserved':True,'no_source_alias_or_receipt_normalization_write':True})
ledger=[]
for rid in ['23383961','23430906']:
 for rel in ['publication.json','promotion.json','reviews/editorial/REPORT.md','reviews/editorial/PUBLIC_COPY.md','reviews/editorial/SCHEMA_ADAPTER.json']:
  p=R/'papers'/rid/rel;ledger.append({'path':str(p),'sha256':sha(p),'reading_scope':'Full current contents; configs include complete original custom objects and separate later root authority.'})
 p=R/'papers'/rid/'reviews/editorial/public-sections.json'
 if p.exists():ledger.append({'path':str(p),'sha256':sha(p),'reading_scope':'Full ordered section specification.'})
 for kind in ['clearance','editorial']:
  p=R/f'verification/root-{kind}-{rid}-20261025.json';ledger.append({'path':str(p),'sha256':sha(p),'reading_scope':'Entire current root authority.'})
 for name in [f'public-copy-{rid}.txt',f'public-sections-{rid}.json']:
  ledger.append({'path':str(O/name),'sha256':sha(O/name),'reading_scope':'Entire actual staged copy / complete actual section arrays, checked against all public source paragraphs.'})
save('READ_LEDGER.json',{'utc':now(),'model':'GPT-6.1 Sol Ultra','children':0,'entries':ledger,'limits':'Static source-bound editorial/stage verification. No new independent scientific adjudication, production-site render, HTTP/browser/native publication or priority clearance.'})
# Removing exactly the additions recovers the complete installed checker; this
# proves every untouched quadratic/bosonic/amplifier and other branch survived.
original=(O/'inputs/final-content-check.py').read_text();proposed=(O/'final-content-check.proposed.py').read_text()
restored=proposed.replace(" '23383961':'published-source/verification_package/support_slit_verification/support_slit.tex',\n '23430906':'support/paper.tex',\n",'',1)
start=restored.index("SLIT_GAUSSIAN_IDS=");end=restored.index('def normalized_quadratic_abstract',start);restored=restored[:start]+restored[end:]
restored=restored.replace(' if record_id in SLIT_GAUSSIAN_IDS:return wt(normalized_slit_gaussian_abstract(record_id,tex))\n','',1)
restored=restored.replace(" if c.get('related_resources') and rid not in SLIT_GAUSSIAN_IDS:"," if c.get('related_resources'):",1)
restored=restored.replace((O/'new-record-checks.block.txt').read_text(),'',1)
assert restored==original
save('full-existing-checker-preservation.json',{'utc':now(),'status':'PASS','exact_addition_reversal_recovers_entire_installed_checker':True,'installed_checker_sha256':sha(O/'inputs/final-content-check.py'),'proposal_sha256':sha(O/'final-content-check.proposed.py'),'quadratic_bosonic_amplifier_and_all_other_existing_branches_unchanged':True})
validation=json.loads((O/'stage-validation.json').read_text());validation['completion_percent']=100;validation['scope']='Bounded private staging only; all203-paper goal remains ongoing.'
save('completion.json',validation)
with (O/'RESEARCH_LOG.md').open('a') as f:f.write(now()+' — 100% of bounded private staging: Final complete copies reviewed, 131/131 content checks and 72 falsification controls pass. All 1,057 original bindings unchanged, including all444 actual site files. Production authorization and actual publication gates remain with root.\n')
report='''# Private slit and Gaussian staging

Status: **PRIVATE_STAGE_CHECKS_PASS_PENDING_ROOT_ACCEPTANCE_AND_PUBLICATION_GATES**.
Completion: **100% of this bounded private staging assignment**. The overall203-paper program remains ongoing. Model: GPT-6.1 Sol Ultra; no descendants.

All work is confined to `verification/local-slit-gaussian-stage-sol-20261025/`. The actual site and shared scripts, original source/config/review/verdict/seal objects, Git, deployment, browser, native Sheet and release state were not changed. No person was contacted, messaged or emailed, and no outreach was prepared. Original paper programs were not executed; no new download, environment, installer, build, compiler or source repair was used.

## Reviewable outputs

- `public/research/nonmonotone-argument-radial-angle-support-slit/index.html` and `public/research/localized-gaussian-witness-fractional-iterated-area/index.html`: complete private staged pages and unchanged deposited PDF/ZIP files.
- `public-copy-23383961.txt` and `public-copy-23430906.txt`: the complete actual visible bodies, read in full. `public-sections-*.json` contain every actual ordered section heading, paragraph and link.
- `render_page.proposed.py`, `final-content-check.proposed.py` and `proposed-shared-{renderer,checker}.diff`: full final production proposals and exact unified patches against the current installed scripts. No helper or asset-resolver change is proposed.
- `render_page.stage.py`, `final-content-check.stage.py` and the two `*-staging-overrides.diff` files: owned execution copies with explicit original read-only ROOT/import paths and private SITE/output selection. Production proposals contain no private-stage path or fallback. The production renderer keeps its existing actual SITE default.
- `target-stage-check-final.{json,md,stdout.json,stderr.txt}`, `negative-controls.json`, `authority-negative-controls.json`, `legacy-dispatch-comparison.json`, `versioned-render-comparison.json`, `full-existing-checker-preservation.json`, `index-sitemap-checks.json` and `stage-validation.json`: verification evidence.
- `source-bindings.json`, `READ_LEDGER.json`, `inputs-before.json`, `integrity-after.json` and `stage-readiness-manifest.json`: source authorities, exact original custom objects, reading extents, unchanged original inputs, and all owned artifact bindings. The final manifest excludes only itself to avoid circularity; its SHA-256 is the package seal.

## Bounded proposal

The renderer uses each new record's existing `abstract_heading` only for these two records, producing **Original abstract** without changing the full original field. It adds two explicit local PDF download anchors per new page, preserves direct opening and the single unchanged PDF iframe, adds each approved short reader introduction, and renders the complete local-download/original-Zenodo ZIP link set for the two new records. The slit config's original empty `related_resources` array is preserved. The Gaussian supporting-resource URLs remain exact; the dedicated section uses the approved public-copy labels and download attribute. Existing50 page behavior remains unchanged.

The checker adds only the exact two TeX mappings, their narrow mathematical-typography abstract normalizer and the bounded two-record branch. Its new checks bind exact publication/promotion bytes, full original abstract/source/candidate equality, exact current TeX bytes, complete custom verdict/report objects and paths, separate later root scientific and editorial authorities, original receipt shapes, original metadata and API asset comparisons, MD5/SHA-256/size, edition chronology, source-custody receipts, download/open/iframe/local-original asset links, all archive members, citation/metadata/index/sitemap and exact scientific scope phrases. No source aliases, copied substitute authority, rewritten receipt, fabricated conventional verdict status or source/config normalization is created.

The original slit scope verdict still has its pending/null/false fields. Its analytic and adversarial original custom verdicts remain complete. The original Gaussian scope hold/nulls/promotion prohibition, analytic COMPLETE/PASS and explicit excluded-H=1 review self-correction, and adversarial custom no-defect verdict remain complete. Later root dispositions remain separate. Promotion/metadata state stays rendering/live/browser/native pending; this private stage does not rewrite it.

## Complete public content

The slit page retains the complete original one-paragraph abstract and the exact fixed coefficient functional, epsilon10^-24, every-maximizer quantifier, actual omitted analytic slit, both monotonic directions, signed outward and unsigned conventions, eta10^-12, actual-tip radius3/10 versus constructed radius25/81, actual-slit continuation, infinity limit and separate interior-zero argument. It keeps classical-method credits, bounded history/novelty language, extensive AI/unrefereed/no-human-review/no-formal-certification wording, passive substantive collaboration and null follow-up.

The Gaussian page retains the complete original one-paragraph abstract, including its final prior-method/novelty/openness and canonical-area/arXiv-v1 qualifications. It retains fixed H in(1/4,1), independent centered standard equal-H coordinates, both complete deterministic uniform grids including terminalT, n observations in each component, everyT>0/everyintegern>=1/everyL2 estimator including nonlinear, the canonical iterated-integral convention, exact H-only positive constant and periodization formula. It retains dependence between cells, all sampling/endpoint/constant/unequal-H/correlation exclusions, halved versus unhalved antisymmetric factors, established canonical input, Brownian and smooth-rate/Fourier/Gaussian antecedent credits and unresolved broader priority/implication limits. No source repair, new firstness claim or mathematical rescope was introduced.

Every configured public abstract/plain/result/proof/limits/status/background/collaboration paragraph appears unchanged. All11 specified headings are present. The established site shell contributes its normal navigation, byline, citation author order, contact links and one stock authorship paragraph. Canonical/Search-description/header-link lines in editorial PUBLIC_COPY remain metadata specifications, as both exact root editorial receipts explain. No private control correction, hash, count, review date or authority narrative appears on either public page.

## Verification

The final combined checker passed **131/131** checks with empty stderr: slit23383961 **65/65**, Gaussian23430906 **66/66**. Their deposited readers remain searchable PDFs of5 and7 pages respectively. All255 slit ZIP members, including12 hidden members, and all225 Gaussian ZIP members match their original extracted bytes. The slit archive has no reader PDF or nested archive; the Gaussian archive's sole paper.pdf is byte-identical to its standalone reader and has no nested archive. Both complete ZIP assets remain unchanged.

The private index contains **52** unique entries. Every old50 visible list item is byte-identical, every old50 structured entry is exact and in order, and only the two new final URLs were appended in slit-then-Gaussian order. The sitemap contains **53** unique URLs including its root: all old51 are exact and in order, followed by only these two URLs. CSS and robots remain byte-identical.

All **49** old TEX_PATHS and abstract dispatches were compared on their actual published source and are unchanged. The pilot old50th page remains unmapped, exactly as before. Removing exactly the declared additions recovers the entire installed checker byte-for-byte, preserving every existing quadratic, bosonic, amplifier and other branch. Four executable original-versus-proposed private renderer cases—23539283 default version,23306332 custom quadratic,22089807 amplifier tar.gz,23203100 absent/null version—produced identical HTML, citations, assets, index, sitemap, CSS and robots. These were isolated private renders; no actual-site render was performed.

**36 altered private stages were rejected** by the complete target checker, including first/middle/final abstract truncation for each paper, citation/version/canonical/date/heading/download/original-ZIP/index/sitemap defects, PDF/ZIP corruption, slit some-versus-every/arbitrary-epsilon/tangent-direction alterations and Gaussian H endpoints/all-L2/terminal-grid/sharp-constant/antisymmetric-factor alterations.

**36 copied-byte authority controls were rejected** by complete checker executions with narrowly intercepted read-only source paths: actual TeX, receipt, metadata, root science/editorial bytes, each original report and verdict, rewritten embedded root/scope objects, root disposition, config scope quantifiers and original source assets, plus Gaussian raw-record and receipt-schema changes. Each control retains its exact altered bytes, run output and rejection report or fail-closed exception. No original input was mutated. Initial v1 outputs are preserved under `iterations/validation-v1/`; one named epsilon check was tightened after the general result equality already rejected that control, so the named test also detects that precise loss.

## Custody and remaining gates

All **1,057** captured original bindings remain unchanged, including all **444** actual site files, the complete new2 source trees, exact publication/promotion and scientific/editorial/root authorities, current installed renderer/checker/bosonic helper/asset resolver, and the current50 production integration's relevant manifest/report core. No unrelated environment or125k-file runtime inventory was copied. Primary staged content includes only the two new paper folders and the few shared/navigation files needed for local link checks. The package is about287MiB, chiefly repeated deliberate negative controls and retained initial-stage evidence; no multi-gigabyte program or environment copy was made.

Root must read the complete final production proposals, actual public copies and this evidence before any production authorization. Production remains frozen while current50 browser/native gates are pending. Root retains actual production integration/rendered-copy acceptance, local/live HTTP and asset-byte checks, desktop/mobile browser checks, deployment/index freshness and native Sheet AA publication gates. Native AA remains blank until verified live. **No actual-site render, live HTTP, browser, mobile-layout, deployment, native-publication, Git push or release PASS is claimed.**
'''
save('REPORT.md',report)
outputs={str(p.relative_to(O)):{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(O.rglob('*')) if p.is_file() and p.name!='stage-readiness-manifest.json'}
save('stage-readiness-manifest.json',{'utc':now(),'status':'PRIVATE_STAGE_COMPLETE_PENDING_ROOT_AND_PUBLICATION_GATES','completion_percent':100,'scope':'Bounded private two-paper staging only; overall203-paper research-site goal ongoing.','original_input_bindings':before,'original_inputs_unchanged':True,'owned_output_bindings':outputs,'excluded_self':'stage-readiness-manifest.json','final_proposal_hashes':{name:sha(O/name) for name in ['render_page.proposed.py','final-content-check.proposed.py']},'actual_site_render_live_browser_native_pass':False})
print(json.dumps({'status':'PRIVATE_STAGE_COMPLETE','completion_percent':100,'original_inputs_unchanged':len(before),'owned_outputs':len(outputs),'manifest_sha256':sha(O/'stage-readiness-manifest.json')}))
