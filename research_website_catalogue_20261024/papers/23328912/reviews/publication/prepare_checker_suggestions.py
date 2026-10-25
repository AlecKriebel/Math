"""Write isolated suggestions and validate their configuration checks; no shared edits."""
from pathlib import Path
import ast, datetime, hashlib, html, json, re

R=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def save(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
checker=R/'verification/final-content-check.py'
base_sha=sha(checker)
for rid in ('23328912','23524971'):
 p=R/'papers'/rid;c=load(p/'publication.json');out=p/'reviews/publication'
 texpath=c['source_binding']['source_tex_path'].removeprefix('sources/')
 func='normalized_cubulation_abstract' if rid=='23328912' else 'normalized_dfc_abstract'
 replacement="body=body.replace(r'\\CAT','CAT').replace(r'\\mapsto','→').replace('$','').replace('~',' ')" if rid=='23328912' else "body=body.replace('birth--death','birth–death')"
 helper=f"def {func}(body):\n {replacement}\n return ' '.join(body.split())\n"
 dispatch=f"if record_id=='{rid}':return wt({func}(tex))"
 scope_candidate=c['source_binding']['frozen_scope_content_path']
 block=f'''if rid=='{rid}':
 test('abstract_full_source_text',{func}(a)==c['abstract'])
 test('abstract_full_source_word_count',len(c['abstract'].split())=={len(c['abstract'].split())})
 test('abstract_source_paragraphs',len(re.split(r'\\n\\s*\\n',a.strip()))==len(c['abstract'].split('\\n\\n'))==1)
 test('abstract_source_binding',c['source_binding']['abstract_source']=='sources/'+TEX_PATHS[rid] and c['source_binding']['abstract_source_sha256']==sha(textpath) and c['source_binding']['abstract_word_count']==len(c['abstract'].split()))
 test('promotion_source_receipt_binding',gate['source_receipt_sha256']==sha(p/'sources/receipt.json'))
 test('promotion_review_bindings',set(gate['reviews'])=={{'analytic','adversarial','scope'}} and all(v['sha256']==sha(p/v['report']) and v['verdict_sha256']==sha(p/v['verdict_file']) and v['verdict']==json.loads((p/v['verdict_file']).read_text()) for v in gate['reviews'].values()))
 test('all_published_source_assets_bound',gate['source_files']==receipt['files']==c['source_binding']['files'] and all(sha(p/'sources'/asset_name(x))==x['sha256'] for x in receipt['files']))
 clearance_path=R/gate['root_clearance_file'];clearance=json.loads(clearance_path.read_text())
 test('root_clearance_binding',clearance['record_id']==rid and clearance['status']=='PASS' and clearance['disposition_by']==gate['disposition_by']=='root' and gate['root_clearance_sha256']==sha(clearance_path) and gate['root_clearance_record']==clearance and gate['approved_scope']==clearance['approved_scope'] and gate['source_repair'] is False and gate['human_peer_review'] is False and gate['formal_machine_verification'] is False)
 test('root_clearance_source_review_identity',clearance['pdf_sha256']==gate['pdf_sha256'] and clearance['source_receipt_sha256']==gate['source_receipt_sha256'] and all(clearance['reviews'][k]['report_sha256']==v['sha256'] and clearance['reviews'][k]['verdict_sha256']==v['verdict_sha256'] for k,v in gate['reviews'].items()))
 test('frozen_scope_candidate_binding',c['source_binding']['frozen_scope_content_path']=={scope_candidate!r} and c['source_binding']['frozen_scope_content_sha256']==sha(p/{scope_candidate!r}))
 test('frozen_scope_chronology_preserved',gate['reviews']['scope']['verdict'].get('mathematical_verdict') is None and gate['reviews']['scope']['root_disposition']=='SCOPE_COMPLETE' and bool(gate['scope_gate_resolution']))
 test('no_unjustified_follow_up',c['follow_up'] is None and gate['follow_up'] is None)
 test('metadata_version_not_printed_version',record['version']==c['version']==c['source_binding']['zenodo_version']=='1.0' and c['source_binding']['manuscript_version'] is None and c['edition_label']=='Zenodo version 1.0')
 test('record_creation_exact',json.loads((p/'sources/record.json').read_text())['created']==c['source_binding']['record_created_utc']=={c['source_binding']['record_created_utc']!r})
 test('date_qualification_visible',c['publication_date_label']=='Manuscript dated' and all(x in unescape(h) for x in [c['edition_note'],'Manuscript dated','not verified public availability','Neither date establishes first priority']))
'''
 if rid=='23328912':
  block+=r''' test('scope_complete',all(x in unescape(h) for x in ['φ(a)=a, φ(b)=ab and φ(c)=bcb','the final b in bcb is positive','cell counts (1,7,8,2)','full group F⋊φZ','free, proper and cocompact','general cube-complex convention','before subdivision']))
 test('limits_and_credit',all(x in unescape(h) for x in ['b↦aba','distinct from the b↦ab target','No minimum dimension, minimum cell count, virtual specialness','no historical-firstness or absolute-novelty claim','does not establish current worldwide openness','WPD, Morse and cubical-completion theorems','Leary','Minasyan and Osin','Hagen and Wise']))
 test('printed_manuscript_date',r'\date{October 12, 2026}' in source and record['publication_date']==c['publication_date']=='2026-10-12')
 test('all_three_original_assets_one_reader',len(receipt['files'])==3 and len(texts)==6 and c['source_binding'].get('embedded_assets',[])==[] and {asset_name(x) for x in receipt['files']}=={'aim_5_2_two_cube_cubulation.pdf','aim_5_2_source.zip','aim_5_2_verification.zip'})
 test('separate_source_verification_links',c['supplement_filename'] is None and len(c['additional_assets'])==2 and {x['filename'] for x in c['additional_assets']}=={'aim_5_2_source.zip','aim_5_2_verification.zip'} and all(x['kind']=='zip' for x in c['additional_assets']) and all(name in [x.get('href') for t,x in d.a if t=='a'] for name in ['aim_5_2_source.zip','aim_5_2_verification.zip']))
 test('no_single_primary_supplement',gate['supplement_sha256'] is None and c['source_binding']['supplement_sha256'] is None)
'''
 else:
  block+=r''' test('scope_complete',all(x in unescape(h) for x in ['For every fixed real λ>0','N₀⁴','nonexplosive, irreducible and positive recurrent','unique stationary probability distribution','every finite initial state','D=x+y+1','rate λ/2','a(x+1)/D and b(y+1)/D','x(y+1)/D and y(x+1)/D','decrementing a zero coordinate has rate zero','unbounded aggregate seed upload']))
 test('limits_and_credit',all(x in unescape(h) for x in ['empty waiting rooms excluded from the contact denominator','not a solution for a capped-seed','No bound uniform in λ, stationary population moment, completion-time estimate, convergence rate or geometric ergodicity','At λ=0 the zero state is absorbing','2009 preprint conjectured high-load instability','2010 Oberwolfach stability conjecture','retained 2011 author-proof model','does not certify worldwide priority or continued openness','Foster–Lyapunov method','Meyn and Tweedie']))
 test('printed_manuscript_date',r'\date{20 October 2026\\\small Unrefereed preprint draft}' in source and record['publication_date']==c['publication_date']=='2026-10-20')
 test('two_original_assets_one_reader',len(receipt['files'])==2 and len(texts)==6 and c.get('additional_assets',[])==[] and c['source_binding'].get('embedded_assets',[])==[] and {asset_name(x) for x in receipt['files']}=={'dfc_stability.pdf','dfc_stability_verification.zip'})
 test('primary_source_verification_zip',c['supplement_filename']=='dfc_stability_verification.zip' and gate['supplement_sha256']==c['source_binding']['supplement_sha256']==sha(p/'sources'/c['supplement_filename']) and c['supplement_filename'] in [x.get('href') for t,x in d.a if t=='a'])
 test('distinct_original_verdict_schema_preserved',gate['reviews']['analytic']['verdict']['verdict']=='PASS' and gate['reviews']['adversarial']['verdict']['verdict']=='PASS' and gate['reviews']['adversarial']['verdict']['status']=='complete')
'''
 # Validate syntax without importing or running the shared checker or renderer.
 ast.parse(helper);ast.parse('def abstract_tokens(tex,record_id=None):\n '+dispatch+'\n');ast.parse(block)
 suggestion={'record_id':rid,'created_utc':utc,'status':'SUGGESTION_ONLY_NOT_APPLIED','base_checker':'verification/final-content-check.py','base_checker_sha256':base_sha,'tex_paths_entry':{rid:texpath},'module_level_helper':helper,'abstract_tokens_dispatch_before_generic_commands':dispatch,'per_paper_checks_before_result_papers_assignment':block,'integration_notes':['Add the exact TEX_PATHS entry.','Add the helper before abstract_tokens, then the dispatch inside abstract_tokens before generic unknown-command validation.','Insert the checks inside the existing record loop after receipt/record/gate/texts exist, before result["papers"][rid].','Run the final content checker after root has rendered both pages, then run the existing-page regression once. No shared change is made by this file.']}
 save(out/'checker-additions.json',suggestion)
 (out/'checker-additions.py.txt').write_text('# SUGGESTION ONLY: four explicitly scoped insertion pieces; do not execute this concatenation.\n\n# 1. TEX_PATHS entry\n'+repr(rid)+': '+repr(texpath)+',\n\n# 2. Module helper\n'+helper+'\n# 3. Inside abstract_tokens before generic commands\n'+dispatch+'\n\n# 4. Inside existing record loop, after receipt/record/gate/texts\n'+block)
 # Exercise source/configuration predicates against approved content only. This
 # intentionally excludes rendered links/page count/date visibility, and cannot
 # claim a render, PDF-display, deployment or browser pass.
 source=(p/'sources'/texpath).read_text();a=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',source,re.S).group(1)
 ns={};exec(helper,ns)
 public_parts=[c['abstract'],c['edition_note']]+sum([c[k] for k in ['plain_language','result','why_it_works','limitations']],[])
 public_parts += [x['title']+' '+x['note'] for x in c['background']]
 body=' '.join(public_parts)
 checks={}
 def test(k,v):checks[k]=bool(v)
 ctx={'rid':rid,'p':p,'R':R,'c':c,'a':a,'TEX_PATHS':{rid:texpath},'textpath':p/'sources'/texpath,'source':source,'gate':load(p/'promotion.json'),'record':load(p/'sources/record.json')['metadata'],'receipt':load(p/'sources/receipt.json'),'sha':sha,'asset_name':lambda x:x.get('name',x.get('filename')),'json':json,'re':re,'test':test,'unescape':html.unescape,'h':html.escape(body),func:ns[func]}
 tree=ast.parse(block)
 omitted=[]
 for node in tree.body[0].body:
  expression=ast.get_source_segment(block,node)
  if any(x in expression for x in ('date_qualification_visible','len(texts)','d.a')):
   omitted.append(expression.split("test('",1)[1].split("'",1)[0] if "test('" in expression else 'render_only');continue
  exec(compile(ast.Module(body=[node],type_ignores=[]),'<isolated-preparation-checks>','exec'),ctx)
 assert all(checks.values()),(rid,checks)
 save(out/'checker-suggestion-check.json',{'utc':utc,'record_id':rid,'status':'PASS_SYNTAX_AND_SOURCE_CONFIGURATION_CHECKS_ONLY','checks':checks,'not_executed_render_checks':omitted,'rendered_or_browser_pass':False,'suggestion_sha256':sha(out/'checker-additions.json'),'completion_percent':100})
 (out/'READINESS.md').write_text(f'# Publication preparation readiness\n\n{utc}\n\n100% of the assigned preparation is complete. Root scientific clearance is bound, with all original review objects and hashes unchanged. The full original abstract has {len(c["abstract"].split())} whitespace-separated words. Manuscript date and Zenodo record creation date are distinguished; no first-priority inference is made.\n\nThe paper-specific publication and promotion files are ready for root inspection. Checker additions are isolated suggestions, syntax-checked and exercised for source/configuration fidelity only. Rendered HTML, local/link/PDF content checks, deployment, desktop/mobile/PDF display and spreadsheet population remain pending with root.\n\nNo source, frozen draft, review, shared checker/renderer, website, Git, Sheet or external communication was changed. The publication editor releases this paper’s final preparation files to root.\n')
 assert sha(checker)==base_sha
 files=[p/'publication.json',p/'promotion.json',out/'binding-check.json',out/'checker-additions.json',out/'checker-additions.py.txt',out/'checker-suggestion-check.json',out/'FINALIZATION_LOG.md',out/'READINESS.md']
 if rid=='23328912':files += [out/'finalize_publication.py',out/'prepare_checker_suggestions.py']
 save(out/'FINAL_PUBLICATION_HASHES.json',{'utc':utc,'record_id':rid,'status':'SEALED_PREPARATION_ONLY','completion_percent':100,'files':[{'path':str(x.relative_to(p)),'sha256':sha(x),'bytes':x.stat().st_size} for x in files],'original_preflight_manifest_sha256':sha(out/'FINAL_HASHES.json'),'rendering_deployment_visual_qa_pending':True,'released_to_root':True})
 print(rid,len(checks),'source/configuration checks; pending render checks:',omitted)
