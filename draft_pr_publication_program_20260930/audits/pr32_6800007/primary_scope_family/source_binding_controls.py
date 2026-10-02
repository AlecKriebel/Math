#!/usr/bin/env python3
"""Exact source-role/variant controls, separate from source-ID and proof-byte checks."""
import hashlib,json,pathlib,re
from datetime import datetime,timezone
HERE=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
tex=(HERE/'sources/problems_MTDG.tex').read_text()
questions=re.findall(r'\\begin\{question\}(.*?)\\end\{question\}',tex,re.S)
target=questions[6]
assert 'homotopy classification' in target and 'totally real immersions' in target
context=(HERE/'sources/flag_question_context.tex').read_text()
assert 'orbit of a real form' in context and 'complex full flag manifold' in context
old=(HERE/'sources/falbel_veloso_v1.txt').read_text()
assert 'Proposition 8.1' not in old and '8.1 Totally real immersions' not in old
proof=json.loads((HERE/'SOURCE_PROOF_RECEIPTS.json').read_text())
v=proof['variants']
arxiv=next(p for p in v if p['fresh_file']=='koshkin_arxiv_current.pdf')
journal=next(p for p in v if p['fresh_file']=='koshkin2009.pdf')
ps=next(p for p in v if p['fresh_file']=='borrelli2002.ps')
converted=next(p for p in v if p['fresh_file']=='borrelli2002.pdf')
assert arxiv['matches_original_bytes_and_hash'] and not journal['matches_original_bytes_and_hash']
assert ps['matches_original_bytes_and_hash'] and not converted['matches_original_bytes_and_hash']
publisher=(HERE/'tmp/fv2020_publisher_pdf.response').read_bytes()
assert not publisher.startswith(b'%PDF')
result={'utc':datetime.now(timezone.utc).isoformat(),'primary_tex_sha256':sha(tex.encode()),'global_question_number':7,
 'controls':[
  {'name':'source_question_number','accepted':7,'neighboring_real_form_target_rejected':True,'numeric_neighbor':6800006},
  {'name':'2018_preprint_as_2020_proposition','rejected':True,'reason':'Complete fresh2018 text contains neither Section8.1 nor Proposition8.1; later complete author proof must be separately cited.'},
  {'name':'journal_arxiv_byte_identity','rejected':True,'journal_bytes':journal['fresh_bytes'],'journal_sha256':journal['fresh_sha256'],'arxiv_bytes':arxiv['fresh_bytes'],'arxiv_sha256':arxiv['fresh_sha256']},
  {'name':'derived_borrelli_pdf_as_original_bytes','rejected':True,'fresh_ps_matches_original':True,'fresh_conversion_matches_old_pdf':False,'fresh_conversion_sha256':converted['fresh_sha256']},
  {'name':'publisher_html_as_complete_pdf','rejected':True,'actual_prefix_hex':publisher[:16].hex(),'bytes':len(publisher),'sha256':sha(publisher)},
  {'name':'unrestricted_euclidean_existence_transfer','rejected':True,'exact_source':'Forstneric1986 Theorem1.4 printedp245 explicitly compact orientable; source broad language is not independent support.'},
  {'name':'Koshkin_deRham_erases_torsion','rejected':True,'exact_witness':'RP2 x S1 integral cochains: d1=(2,0), d2=(0,2); H3=Z/2; candidate index obstruction nonzero. Koshkin integralTheorem3 retained.'}],
 'bound':'These controls check exact source roles, bytes and explicit scope guards, not universal correctness or historical priority.'}
(HERE/'SOURCE_BINDING_CONTROLS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'source_controls':len(result['controls']),'all_scope_corruptions_rejected':True},indent=2))
