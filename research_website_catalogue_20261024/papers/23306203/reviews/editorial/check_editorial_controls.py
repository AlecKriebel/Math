#!/usr/bin/env python3
"""One bounded new editorial fault check. Pure in-memory mutations, not science.
Stdlib only; no project imports, native programme, network, subprocess or writes.
"""
from pathlib import Path
import copy
import hashlib
import html
import json
E=Path(__file__).resolve().parent
CC='https://creativecommons.org/licenses/by/4.0/'
def issues(main,sg,p,native):
 text=html.unescape(main);bad=[]
 fragments={'least_period':'let n be its primitive least period','even_foci_not_constancy':'This includes n≡0 (mod 4), when the equal products still vary with phase.','circle_separate':'the noncircular pole argument is not continued through c=0.','physical_triangle':'90ac=180√30>0','final_credit':'final 2021 Arnold Mathematical Journal article, Fifty New Invariants','coverage_gap':'The full billiard body of the related Dragović–Gajić article remained unavailable'}
 for k,v in fragments.items():
  if v not in text:bad.append(k)
 fragment=(E/'ORIGINAL_PRINTED_ABSTRACT.tex').read_text()
 abstract=' '.join(fragment.split()).replace('\\(2\\)','2').replace('\\(4\\)','4').replace('\\(k_{114}\\)','k₁₁₄').replace('Reznik--Garcia--Koiller','Reznik–Garcia–Koiller')
 if sg.get('abstract')!=abstract or '<h2>Original printed abstract</h2><p>'+html.escape(abstract)+'</p>' not in main:bad.append('whole_printed_abstract')
 expected=['focal_product_support.zip','focal_product_period_criterion.pdf']
 if [x.get('contentUrl','').rsplit('/',2)[-2] for x in sg.get('encoding',[])]!=expected:bad.append('native_order')
 hashes=['23f032f0522b22f293e74eb4df9a97706f6414a385bd1d39b173c979df36ee3a','280e7e703c50615def59d2c45d22386fde015d8bfce6705a7cc878d19aef0e1e']
 if [hashlib.sha256(native[n]).hexdigest() for n in expected]!=hashes:bad.append('native_whole_bytes')
 if p.get('printed_version_field_present') is not False or p.get('printed_version') is not None:bad.append('printed_version_absent')
 if p.get('code_license')!='CC BY 4.0' or any(x.get('license')!=CC for x in sg.get('encoding',[])):bad.append('actual_CC_BY_code_and_assets')
 if any(p.get(k) is not None for k in ['canonical_url','AA','follow_up']):bad.append('private_null_gates')
 if 'Private custody checks:' in text or 'Run the editorial replay:' in text:bad.append('private_audit_narrative')
 return bad
def main():
 original_main=(E/'PUBLIC_MAIN.html').read_text();original_sg=json.loads((E/'SCHOLARLY_METADATA.json').read_text());original_p=json.loads((E/'publication.json').read_text());original_native={n:(E/'candidate'/n).read_bytes() for n in ['focal_product_support.zip','focal_product_period_criterion.pdf']}
 if issues(original_main,original_sg,original_p,original_native):raise ValueError('actual baseline violates editorial oracle')
 cases=[('least period replaced','least_period'),('even-foci distinction removed','even_foci_not_constancy'),('circle limit blurred','circle_separate'),('triangle exact difference changed','physical_triangle'),('final source credit lost','final_credit'),('coverage limit omitted','coverage_gap'),('printed abstract swapped with deposit description','whole_printed_abstract'),('native encodings reversed','native_order'),('native PDF byte changed','native_whole_bytes'),('printed version invented','printed_version_absent'),('MIT license invented','actual_CC_BY_code_and_assets'),('site canonical prematurely assigned','private_null_gates'),('public private-audit narrative added','private_audit_narrative')]
 receipts=[]
 for label,want in cases:
  text=original_main;sg=copy.deepcopy(original_sg);p=copy.deepcopy(original_p);native=dict(original_native)
  if want=='least_period':text=text.replace('let n be its primitive least period','let n be an arbitrary listed return length')
  elif want=='even_foci_not_constancy':text=text.replace('This includes n≡0 (mod 4), when the equal products still vary with phase.','Equal focal products are phase-constant for all even n.')
  elif want=='circle_separate':text=text.replace('the noncircular pole argument is not continued through c=0.','the pole argument continues through c=0.')
  elif want=='physical_triangle':text=text.replace('90ac=180√30&gt;0','90ac=0')
  elif want=='final_credit':text=text.replace('final 2021 Arnold Mathematical Journal article, Fifty New Invariants','unspecified article')
  elif want=='coverage_gap':text=text.replace('The full billiard body of the related Dragović–Gajić article remained unavailable','all cited bodies were fully cleared')
  elif want=='whole_printed_abstract':sg['abstract']=p['native_deposit_description_html']
  elif want=='native_order':sg['encoding'].reverse()
  elif want=='native_whole_bytes':native['focal_product_period_criterion.pdf']+=b'changed'
  elif want=='printed_version_absent':p['printed_version_field_present']=True;p['printed_version']='1.0.0'
  elif want=='actual_CC_BY_code_and_assets':p['code_license']='MIT'
  elif want=='private_null_gates':p['canonical_url']=p['proposed_canonical_url']
  elif want=='private_audit_narrative':text+='<p>Private custody checks: 1483</p>'
  found=issues(text,sg,p,native)
  if want not in found:raise ValueError('fault was not rejected: '+label)
  receipts.append({'fault':label,'required_detection':want,'actual_detected_issues':found,'rejected':True})
 print(json.dumps({'status':'PASS_BOUNDED_NEW_EDITORIAL_FAULT_CONTROLS','actual_baseline_accepted':True,'new_memory_faults_rejected':len(receipts),'whole_receipts':receipts,'native_or_source_scientific_execution':False,'production_authority':False},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
