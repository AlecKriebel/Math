"""Use immutable V1 as history; write a complete effective V2 only here."""
from pathlib import Path
import json,datetime,hashlib,os,re
B=Path(__file__).resolve().parent;V1=B.parent
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def read(name):return json.loads((V1/name).read_text())
def save(name,value):(B/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def pin(p):
    d=p.read_bytes();return {'relative_path':os.path.relpath(p,B),'bytes':len(d),'sha256':hashlib.sha256(d).hexdigest()}

old=(V1/'REPORT.md').read_text()
start=old.index('**All-root communication-tree formulations.**')
end=old.index('**Shared arborescences.**',start)
replacement='''**All-root communication-tree formulations (corrected V2).** [Tilk–Irnich2016](https://download.uni-mainz.de/RePEc/pdf/Discussion_Paper_1613.pdf), §3.2, couples commodity supports through one common undirected spanning tree, but the compact objective charges flow amounts f, rather than fixed coefficients times orientation indicators y. In the independent commodity-u pricing model(5), printed7/§4.3.2, the objective is fixed activation charge γ^u_ij y^u_ij plus flow charge c_ij f^u_ij, less a column constant; γ=−π≥0 comes from dual edge-coupling prices. The model uses at most N−1 selected arcs.

The source explicitly distinguishes demand cases. It guarantees spanning-tree generation only when every nonroot demand r_ui is positive. When a commodity has zero-demand vertices, the pricing support need only reach positive-demand terminals; the paper adds nonroot-indegree inequalities and explicitly prunes zero-demand leaves. Its global assumption that each vertex has some positive incident communication does **not** make every vertex a positive-demand terminal for every commodity.

Consequently, setting every flow-charge coefficient to0 can still leave a **fixed-cost Steiner support problem**. The source's Steiner-generalization hardness statement does not make the flow-charge term essential. The historical V1 inference to minimum spanning arborescence without a mandatory-vertex condition was incorrect and is withdrawn.

There is a conditional statement for the independent pricing problem: if every nonroot vertex must be reached (for example r_ui>0 for each i≠u), M is sufficient for the total demand, and only the source's nonnegative fixed activation charges remain, a feasible support with at most N−1 arcs is a spanning arborescence rooted at u. Conversely, each rooted spanning arborescence carries the given demands with such M. Minimizing these fixed charges is then a minimum-cost rooted spanning-arborescence problem. This restricted observation says nothing about the complexity of coupling all roots through one common tree.

No exact prior-target implication follows from either demand case. The full communication-tree objective charges tree-dependent flow; its hard pricing subclass may omit optional zero-demand vertices, and an individual pricing problem is decoupled by commodity. The literal target instead requires one shared undirected spanning support, every vertex root, and costs over every arc of every induced full rooted tree. A source-to-target transfer must prove all these feasible-set and objective correspondences. [Zetina et al.2017](https://www.cirrelt.ca/documentstravail/cirrelt-2017-72.pdf), complete definitions and arc model1–7, likewise uses communication demand on pair paths; no target correspondence was authenticated.

'''
old=old[:start]+replacement+old[end:]
old=old.replace('# Classical tree mechanisms: bounded priority audit of PR108','# Classical tree mechanisms: corrected effective V2 priority audit of PR108',1)
old=old.replace('All work was confined to this directory.','V1 is immutable history; this correction writes only the corrected_v2 subfolder.',1)
old=old.replace('[MECHANISM_FREEZE.md](MECHANISM_FREEZE.md)','[immutable V1 mechanism freeze](../MECHANISM_FREEZE.md)')
old=old.replace('[compare_cost_models.py](compare_cost_models.py)','[immutable V1 compare_cost_models.py](../compare_cost_models.py)')
old=old.replace('and four fixed-core leaf supports satisfy(C) with the predicted distinct mixed differences.','and four fixed-core leaf supports satisfy(C) with the predicted distinct mixed differences. [TILK_ZERO_FLOW_RESULTS.json](TILK_ZERO_FLOW_RESULTS.json) checks the pricing-model boundary: with zero flow charges, a zero-demand leaf is omitted at fixed cost1, whereas making that leaf a positive-demand terminal forces the full support at cost6. This is a finite model check, not a new central proof-search route.')
old=old.replace('[CLI_LEDGER.jsonl](CLI_LEDGER.jsonl) records actual retrieval/extraction PIDs, argv, start/end UTC, exit status, stdout/stderr byte counts and SHA256 hashes, including the empty archive attempts and failed Hu access.','The [immutable V1 CLI ledger](../CLI_LEDGER.jsonl) records original retrieval/extraction processes, including failed access. The effective [V2 CLI ledger](CLI_LEDGER.jsonl) records the primary-model reread and finite boundary check with actual PIDs, argv, UTC, exits, byte counts and hashes. Existing source bodies are pinned in place; no PDF is copied into V2.')
old+='''

## Correction and effective-version boundary

[CORRECTION_LEDGER.json](CORRECTION_LEDGER.json) identifies the historical defect, withdrawal, exact replacement and impact. V1 remains byte-for-byte sealed history. This complete V2 report, verdict, novelty matrix and source/read-scope ledger are the effective family assertions. Primary source pins bind the existing V1 PDF and full text; the relevant model was independently re-read at printed3–7, including §3.2, §4.2 and all of §4.3.2.

The correction removes an invalid argument about why the pricing problem is hard. It does not establish a new literal-target antecedent or invalidate the fixed-core leaf separability comparison. The source-priority recommendation remains GO to fresh combined review and a narrowly attributed answer to the2018 question if that review passes; NO-GO for novelty certification or absolute priority. Mathematical gate100% is inherited, priority establishment0%, original approaches2/5, new central proof routes0. The parent and its fresh reviewer must recheck the corrected packet; this is no publication/closure authority.
'''
(B/'REPORT.md').write_text(old)

matrix=read('NOVELTY_MATRIX.json');matrix['UTC']=now;matrix['effective_version']='corrected_v2'
row=next(x for x in matrix['rows'] if x['source']=='S3')
row.update({'classical_restrictions_verified':'One common undirected tree in the full flow model. Independent pricing(5) has nonnegative fixed activation costs, flow costs, at most N-1 arcs, and may omit/prune zero-demand vertices. All-positive nonroot commodity demand is the source\'s sufficient condition for spanning support.','same_common_tree':'yes in coupled full OCSTP; independent pricing permits terminal-subset support with zero demand','all_roots_single_arc_objective':'no: full model charges commodity flow; pricing fixed charges do not restore all-root common full spanning support','entire_target_bundle_implication':'NOT ESTABLISHED','exact_gap':'Zero flow charges can retain fixed-cost Steiner support when vertices are optional. With all vertices mandatory, only the independent fixed-charge pricing problem specializes to minimum rooted spanning arborescence. Neither establishes exact shared-all-root/full-tree target hardness; feasible-set and complete-cost mapping remains unproved.'})
matrix['correction']='S3 V1 unqualified minimum-arborescence inference withdrawn; no claim that Steiner-type hardness requires nonzero flow charges.'
save('NOVELTY_MATRIX.json',matrix)

sources=read('SOURCES_AND_READ_SCOPE.json');sources['UTC']=now;sources['effective_version']='corrected_v2'
for s in sources['sources']:
    if s.get('retrieval_label') and s['id']!='S0':s['private_source_body_pin']=pin(V1/'_private'/(s['retrieval_label']+'.stdout'))
    if s.get('extract_label'):s['private_full_extract_pin']=pin(V1/'_private'/(s['extract_label']+'.stdout'))
    if s['id']=='S0':
        s['private_relevant_extract_pin']=pin(V1/'_private/kaibel_full_contribution.stdout')
        s['parent_pdf']='../../primary_sources_20261006/owr.pdf'
s=next(s for s in sources['sources'] if s['id']=='S3')
s['read_scope']='V1 full paper read; corrected V2 independently re-read full relevant §3 definition, §3.2 compact tree-flow model, §4.2 block/master context and ALL§4.3.2 model(5), demand qualifier, indegree inequalities, Steiner-generalization statement and pruning paragraph, printed3–7. The source states generalization of Steiner tree; it does not present a separate full reduction proof in this section.'
s['model']='Full OCSTP couples supports and charges flows; independent commodity pricing has fixed activation plus flow costs. Zero-demand vertices can be optional/pruned. Zero flow charges may preserve fixed-cost Steiner support. Only all-mandatory-vertex zero-flow-charge independent pricing reduces to minimum spanning arborescence.'
s['status']='full relevant model re-read; historical V1 inference corrected; no exact target transfer'
s['V2_relevant_extract_pin']=pin(B/'_private/tilk_primary_model_reread.stdout')
sources['original_receipts_ledger_pin']=pin(V1/'CLI_LEDGER.jsonl')
save('SOURCES_AND_READ_SCOPE.json',sources)

verdict=read('VERDICT.json');verdict.update({'UTC':now,'effective_version':'corrected_v2','status':'CORRECTED_BOUNDED_FAMILY_AUDIT_COMPLETE_PENDING_FRESH_ADJUDICATION','write_scope':str(B),'historical_defect_corrected':'Tilk–Irnich zero-flow-charge pricing can remain fixed-cost Steiner with optional zero-demand vertices. V1 unconditional minimum-arborescence inference withdrawn.','corrected_Tilk_assessment':'No Steiner-flow-term-necessity claim. All-mandatory positive-demand independent pricing with zero flow charges is minimum spanning arborescence; optional/pruned terminal support can remain Steiner. Neither supplies a literal-target feasible-set/full-objective transfer.','V1_history_bindings':'V1_IMMUTABLE_BINDINGS.json','fresh_review_needed':'Parent fresh adjudication reviewer must check this corrected effective packet.'})
save('VERDICT.json',verdict)
bindings=read('INPUT_BINDINGS.json')
for k in ['candidate_proof','original_source_pdf','gate']:bindings[k]['path']=os.path.relpath((V1/bindings[k]['path']).resolve(),B)
bindings['inherited_V1_seal']=pin(V1/'SEAL.json');save('INPUT_BINDINGS.json',bindings)
save('COMPARISON_RESULTS.json',read('COMPARISON_RESULTS.json'))
save('TILK_ZERO_FLOW_RESULTS.json',json.loads((B/'_private/tilk_zero_flow_boundary.stdout').read_text()))
search=read('SEARCH_LEDGER.json');search['effective_version']='corrected_v2';search['V2_correction_research']={'UTC':now,'new_web_queries':0,'mechanism':'Read pinned primary model and its exact zero-demand qualifications; finite support boundary check. No new source-priority or central hardness route.','primary_url':'https://download.uni-mainz.de/RePEc/pdf/Discussion_Paper_1613.pdf','existing_source_body_pin':pin(V1/'_private/ocst2016.stdout')}
for x in search['raw_snapshot_retention']:x['private_path']='../'+x['private_path']
save('SEARCH_LEDGER.json',search)
ledger={'UTC':now,'correction_id':'TILK2016_ZERO_DEMAND_PRICING_V2','historical_version':'sealed V1','current_version':'corrected_v2','historical_defect':'V1 REPORT claimed that §4.3.2 Steiner-type hardness retains the flow term and removing it yields minimum arborescence. V1 S3 novelty-matrix gap repeated the unqualified removal inference. This ignored optional/pruned zero-demand vertices.','withdrawal':'Both incorrect effective assertions are removed and replaced, not retained as operative claims with a caveat.','primary_basis':'Printed7: spanning-tree guarantee only for r_ui>0 at every nonroot vertex; otherwise fewer arcs may reach all positive-demand vertices. Nonroot indegree inequalities are supplied and zero-demand leaves are pruned. Fixed charges are nonnegative; Steiner generalization does not require a nonzero flow charge.','corrected_statement':'Zero flow charges may leave a fixed-cost Steiner support problem. With all nonroot vertices mandatory, adequate M and tree support, the independent fixed-charge pricing problem is minimum spanning arborescence. The latter conditional statement does not classify the shared all-root target.','impacted_current_files':['REPORT.md','NOVELTY_MATRIX.json','SOURCES_AND_READ_SCOPE.json','VERDICT.json','SEARCH_LEDGER.json'],'source_pins':[pin(V1/'_private/ocst2016.stdout'),pin(V1/'_private/ocst2016_full.stdout'),pin(B/'_private/tilk_primary_model_reread.stdout')],'unchanged_findings':['No exact earlier literal-target theorem authenticated.','Fixed-core leaf separability proof and its bounded direct-map scope.','No genuinely new residual certified; priority0%; inherited math100%; original2/5 and extra central proof routes0.'],'recommendation_impact':'Same narrow GO/absolute-priority NO-GO recommendation, now based on corrected model distinctions; pending fresh parent adjudication.','not_a_new_central_route':True}
save('CORRECTION_LEDGER.json',ledger)
(B/'RESEARCH_LOG.md').write_text(f'''# Effective corrected V2 research log

- 2026-10-06T05:20:18Z: Correction checkpoint1. Pinned full primary §4.3.2 re-read; adversarial objection confirmed independently. Historical unconditional minimum-arborescence inference withdrawn. Correction task30%; inherited mathematical gate100%; priority0%; original2/5; extra central proof routes0.
- 2026-10-06T05:21:30.205445+00:00: Correction checkpoint2. Existing sealed V1 files verified read-only, effective V2 folder created. Logged actual pdftotext reread printed3–7, including both full support/context and zero-demand qualifier/pruning. Correction task60%; priority0%.
- {now}: Correction checkpoint3. Full effective REPORT, verdict, exact restriction matrix, source/read-scope and correction ledger rebuilt. Conditions on independent minimum arborescence and remaining terminal-subset/flow/coupling gaps stated globally. Correction task90%; pending checks/seal/fresh parent adjudication; priority0%; no publication/closure authority.
''')
print(json.dumps({'UTC':now,'operator_PID':os.getpid(),'effective_version':'corrected_v2','report_bytes':(B/'REPORT.md').stat().st_size,'historical_defect_removed':True}))
