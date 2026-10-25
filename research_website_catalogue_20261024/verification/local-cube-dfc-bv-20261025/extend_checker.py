"""Apply three record-specific content checks without modifying existing checks."""
from pathlib import Path
import ast, hashlib, json
R = Path(__file__).resolve().parents[2]
target = R/'verification/final-content-check.py'
before = target.read_text()
assert hashlib.sha256(target.read_bytes()).hexdigest() == '903f26f14a1d1a69c710af94e91757b95423c6d0bd998fda59a94f08eddfb1a2'
edits = [json.loads((R/f'papers/{rid}/reviews/publication/checker-additions.json').read_text()) for rid in ['23328912','23524971']]
paths = ''.join(' '+repr(k)+':'+repr(v)+',\n' for e in edits for k,v in e['tex_paths_entry'].items())
paths += " '23572690':'published-source/bv-generators-source-and-verification/main.tex',\n"
after = before.replace('TEX_PATHS={\n','TEX_PATHS={\n'+paths,1)
helpers = ''.join(e['module_level_helper'] for e in edits)
helpers += r'''def normalized_bv_abstract(body):
 body=' '.join(body.split())
 replacements={r'\(0\ne h\in k[x]\)':'0≠h∈k[x]',r'\(A_h=k\langle x,Y\rangle/(Yx-xY-h(x))\)':'A_h=k⟨x,Y⟩/(Yx−xY−h(x))',r'\(k\)':'k',r'\(h\)':'h','Batalin--Vilkovisky':'Batalin–Vilkovisky','~':' '}
 for old,new in replacements.items():body=body.replace(old,new)
 return body
'''
after = after.replace('def abstract_tokens(tex,record_id=None):\n',helpers+'def abstract_tokens(tex,record_id=None):\n'+''.join(' '+e['abstract_tokens_dispatch_before_generic_commands']+'\n' for e in edits)+" if record_id=='23572690':return wt(normalized_bv_abstract(tex))\n",1)
checks = ''.join('\n'.join(' '+line if line else '' for line in e['per_paper_checks_before_result_papers_assignment'].splitlines())+'\n' for e in edits)
checks += r''' if rid=='23572690':
  test('abstract_full_source_text',normalized_bv_abstract(a)==c['abstract'])
  test('abstract_full_source_word_count',len(c['abstract'].split())==114)
  test('abstract_source_paragraphs',len(re.split(r'\n\s*\n',a.strip()))==len(c['abstract'].split('\n\n'))==1)
  test('abstract_source_binding',c['source_binding']['abstract_source']=='sources/'+TEX_PATHS[rid] and c['source_binding']['abstract_source_sha256']==sha(textpath) and c['source_binding']['abstract_word_count']==114)
  test('promotion_source_receipt_binding',gate['source_receipt_sha256']==sha(p/'sources/receipt.json'))
  test('promotion_review_bindings',set(gate['reviews'])=={'analytic','adversarial','scope'} and all(v['sha256']==sha(p/v['report']) and v['verdict_sha256']==sha(p/v['verdict_file']) and v['verdict']==json.loads((p/v['verdict_file']).read_text()) for v in gate['reviews'].values()))
  test('all_published_source_assets_bound',gate['source_files']==receipt['files']==c['source_binding']['files'] and all(sha(p/'sources'/asset_name(x))==x['sha256'] for x in receipt['files']))
  clearance_path=R/gate['root_clearance_file'];clearance=json.loads(clearance_path.read_text())
  test('root_clearance_binding',clearance['record_id']==rid and clearance['status']=='PASS' and clearance['disposition_by']==gate['disposition_by']=='root' and gate['root_clearance_sha256']==sha(clearance_path) and gate['root_clearance_record']==clearance and gate['approved_scope']==clearance['approved_scope'] and gate['source_repair'] is False and gate['human_peer_review'] is False and gate['formal_machine_verification'] is False)
  test('root_clearance_source_review_identity',clearance['pdf_sha256']==gate['pdf_sha256'] and clearance['source_receipt_sha256']==gate['source_receipt_sha256'] and all(clearance['reviews'][k]['report_sha256']==v['sha256'] and clearance['reviews'][k]['verdict_sha256']==v['verdict_sha256'] for k,v in gate['reviews'].items()))
  test('frozen_scope_candidate_binding',c['source_binding']['frozen_scope_content_path']=='reviews/scope/content.json' and c['source_binding']['frozen_scope_content_sha256']==sha(p/'reviews/scope/content.json'))
  test('frozen_scope_chronology_preserved',gate['reviews']['scope']['root_disposition']=='SCOPE_COMPLETE' and bool(gate['scope_gate_resolution']))
  test('no_unjustified_follow_up',c['follow_up'] is None and gate['follow_up'] is None)
  test('printed_edition_date',r'\date{22 October 2026\\\small Preprint, version 1.0.0}' in source and record['version']==c['version']==c['source_binding']['manuscript_version']=='1.0.0' and record['publication_date']==c['publication_date']=='2026-10-22')
  test('record_creation_exact',json.loads((p/'sources/record.json').read_text())['created']==c['source_binding']['record_created_utc']=='2026-10-22T17:40:39.241356+00:00')
  test('date_qualification_visible',c['publication_date_label']=='Manuscript dated' and c['edition_note'] in unescape(h) and 'do not establish first priority' in unescape(h))
  test('exact_nonzero_characteristic_zero_domain',all(x in unescape(h) for x in ['For any characteristic-zero field k and nonzero h∈k[x]','ordinary HH•(A_h,A_h)','canonical Gerstenhaber bracket','Nonzero constant polynomials','original field','does not require the polynomial to split']))
  test('all_generator_obstruction_and_zero_positive_case',all(x in unescape(h) for x in ['no bracket generator exists','zero operator is a BV generator','every degree-minus-one bracket generator','even if its square is not required to vanish','central degree-one class annihilates every other degree-one class']))
  test('embedded_zero_boundary',all(x in unescape(h) for x in ['literal embedded h=0 case instead gives k[x]','Δ(f∂x)=−f′','abstract two-generator presentation gives a different algebra, k[x,Y]']))
  test('scope_limits_and_predecessors',all(x in unescape(h) for x in ['does not classify arbitrary Weyl subalgebras, positive-characteristic cases, twisted-coefficient variants, or Poisson analogues','It makes no first-discovery claim','Lopes and Solotar','Benkart, Lopes and Ondrus','Herscovich and Li','Proposition 4.15','Theorem 1.7 assumes a semisimple modular automorphism']))
  test('two_original_assets_one_reader',len(receipt['files'])==2 and len(texts)==6 and c.get('additional_assets',[])==[] and c['source_binding'].get('embedded_assets',[])==[] and {asset_name(x) for x in receipt['files']}=={c['pdf_filename'],c['supplement_filename']})
  test('primary_source_verification_zip',c['supplement_filename']=='bv-generators-source-and-verification.zip' and gate['supplement_sha256']==c['source_binding']['supplement_sha256']==sha(p/'sources'/c['supplement_filename']) and c['supplement_filename'] in [x.get('href') for t,x in d.a if t=='a'])
'''
anchor = " result['papers'][rid]={'checks':checks"
assert after.count(anchor)==1
after = after.replace(anchor,checks+anchor,1)
ast.parse(after)
# Exact reversal proves the old check bodies were not rewritten or weakened.
reversed_text = after.replace(checks,'',1).replace(helpers,'',1)
reversed_text = reversed_text.replace(''.join(' '+e['abstract_tokens_dispatch_before_generic_commands']+'\n' for e in edits)+" if record_id=='23572690':return wt(normalized_bv_abstract(tex))\n",'',1)
reversed_text = reversed_text.replace(paths,'',1)
assert reversed_text == before
target.write_text(after)
print(json.dumps({'old_sha256':hashlib.sha256(before.encode()).hexdigest(),'new_sha256':hashlib.sha256(after.encode()).hexdigest(),'old_checks_unchanged':True,'record_specific_additions':['23328912','23524971','23572690']}))
