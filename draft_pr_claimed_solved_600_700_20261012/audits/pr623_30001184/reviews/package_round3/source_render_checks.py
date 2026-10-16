from pathlib import Path
import json,hashlib,subprocess,datetime
R=Path(__file__).resolve().parent;A=R.parent.parent;D=R/'tmp/private_sources'
report={}
queries={'OWR2009':['More precisely, a dilation','On the Universality of the Module Approach','GNS-representation of A on E'], 'BFH_v2':['Definition 4.1.','Theorem 4.4.','H12 (t)','(11)'], 'Shalit_Skeide_v3':['2.3 Definition.','(i)    Dilations','Road Map','(2.3)'], 'DMB_v3':['Method','Appendix A: Completing','Appendix B: Divergence'], 'vom_Ende_v3':['Theorem 1.'], 'Skeide_Sumesh_v2':['Does every dilation']}
for label,terms in queries.items():
 pdf=A/'sources.private/OWR2009.pdf' if label=='OWR2009' else D/(label+'.pdf')
 txt=(D/(label+'.txt')).read_text();pages=txt.split('\f')
 report[label]={'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'pdf_bytes':pdf.stat().st_size,'locators':{term:[i+1 for i,page in enumerate(pages)if term in page]for term in terms}}
# Preserve a concise source receipt, not the copyrighted full text.
report['verified_locators']={'OWR':'Printed 497-498 general definition; 542-543 first module-approach problem. General commutative diagram requires p theta_t i=T_t, not all-algebra intertwining.', 'BFH':'arXiv v2 Section 2 eq (1)-(3), PDF 3-4, flip-flop with symmetric coupling; Definition 4.1 on PDF 9; Theorem 4.4 Steps 1-2 and eq (11) on PDF 10-12.', 'DMB':'arXiv v3 Method PDF 2; Appendices A-B PDF 7; finite-unitary construction and initial divergence/derivative discussion verified.', 'Shalit_Skeide':'arXiv v3 Definition 2.3 printed/PDF 16; strong diagram (2.3) printed/PDF 20; Appendix R (Road Map), R(i) printed/PDF 211-212. Journal appendix numbering not verified and not inferred.', 'vom_Ende':'arXiv v3 Theorem 1 printed/PDF 4-5, bounded total-Hamiltonian derivative is a commutator.', 'Skeide_Sumesh':'arXiv v2 Section 5 printed/PDF 34 fixed-left-action question verified.'}
report['independent_bounded_search']={'date_utc':datetime.datetime.now(datetime.UTC).isoformat(),'queries':['site:arxiv.org Skeide GNS generation counterexample dilation','site:arxiv.org/ems.press Skeide not too big dilation GNS','site:arxiv.org forward generation GNS'],'result':'No result returned; does not certify absence or firstness.'}
(R/'SOURCE_RECEIPTS.json').write_text(json.dumps(report,indent=2)+'\n')
# Render independent source compile; compare complete text and every pixel.
source=A/'publication/gns_generation_counterexample.pdf';compiled=R/'tmp/build/gns_generation_counterexample.pdf'
subprocess.run(['pdftoppm','-r','100','-png',str(compiled),str(R/'tmp/render/compiled')],check=True)
texts=[]
for p in [source,compiled]:texts.append(subprocess.check_output(['pdftotext','-layout',str(p),'-']))
render={'all_five_delivered_pages_visually_inspected':True,'page_images_identical':{},'text_identical':texts[0]==texts[1],'compiled_pdf_sha256':hashlib.sha256(compiled.read_bytes()).hexdigest(),'delivered_pdf_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'compile':'Tectonic successful outside exact extracted inventory; only underfull warnings, no overfull warnings observed.','visual_result':'PASS: equations, theorem continuations, page numbers, disclosures and bibliography readable; no clipping/overlap/missing glyphs.'}
for i in range(1,6):render['page_images_identical'][str(i)]=(R/f'tmp/render/paper-{i}.png').read_bytes()==(R/f'tmp/render/compiled-{i}.png').read_bytes()
if not render['text_identical']or not all(render['page_images_identical'].values()):raise ValueError('compiled paper differs')
(R/'PDF_RENDER_RESULTS.json').write_text(json.dumps(render,indent=2)+'\n');print(json.dumps(render))
