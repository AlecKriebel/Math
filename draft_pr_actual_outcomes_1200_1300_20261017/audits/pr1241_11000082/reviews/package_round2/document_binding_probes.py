"""Actual PDF/source byte fixtures; all corruptions on a private copy."""
from pathlib import Path
import copy,datetime,importlib.util,json,shutil
HERE=Path(__file__).resolve().parent;A=HERE.parents[1];P=A/'publication';W=HERE/'scratch_local/document_binding'
def need(c,m):
    if not c:raise RuntimeError(m)
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
if W.exists():shutil.rmtree(W)
p=W/'publication';(p/'manuscript').mkdir(parents=True);(p/'output/pdf').mkdir(parents=True)
files=['manuscript/main.tex','output/pdf/main.pdf','COMPILE_RECEIPT.json','LAYOUT_VERIFICATION.json']
for n in files:shutil.copyfile(P/n,p/n)
for n in ['CURRENT_PR1241_CONTEXT.json','PRIORITY_ADJUDICATION.json']:shutil.copyfile(A/n,W/n)
spec=importlib.util.spec_from_file_location('r2_build',P/'build_package.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b);b.ROOT=p
source=(p/'manuscript/main.tex').read_bytes();pdf=(p/'output/pdf/main.pdf').read_bytes();compile=json.loads((p/'COMPILE_RECEIPT.json').read_text());layout=json.loads((p/'LAYOUT_VERIFICATION.json').read_text());context=json.loads((W/'CURRENT_PR1241_CONTEXT.json').read_text());results=[]
for case in ['positive','source_byte_drift','pdf_byte_drift','missing_compile','missing_layout','bad_epoch','failed_compilation','compile_source','compile_pdf','layout_source','layout_pdf','missing_last_page_index','duplicate_page_index','wrong_page_count','all_pages_false','context_wrong_pages','context_bool_pages']:
    (p/'manuscript/main.tex').write_bytes(source);(p/'output/pdf/main.pdf').write_bytes(pdf);save(p/'COMPILE_RECEIPT.json',compile);save(p/'LAYOUT_VERIFICATION.json',layout);save(W/'CURRENT_PR1241_CONTEXT.json',context)
    if case=='source_byte_drift':(p/'manuscript/main.tex').write_bytes(source+b'\n% altered source\n')
    elif case=='pdf_byte_drift':(p/'output/pdf/main.pdf').write_bytes(pdf+b'\n% altered PDF trailer\n')
    elif case=='missing_compile':(p/'COMPILE_RECEIPT.json').unlink()
    elif case=='missing_layout':(p/'LAYOUT_VERIFICATION.json').unlink()
    elif case=='bad_epoch':save(p/'COMPILE_RECEIPT.json',{**compile,'source_date_epoch':'1792267201'})
    elif case=='failed_compilation':save(p/'COMPILE_RECEIPT.json',{**compile,'returncode':1})
    elif case.startswith('compile_'):save(p/'COMPILE_RECEIPT.json',{**compile,('source' if case.endswith('source') else 'pdf')+'_sha256':'0'*64})
    elif case.startswith('layout_'):save(p/'LAYOUT_VERIFICATION.json',{**layout,('source' if case.endswith('source') else 'pdf')+'_sha256':'0'*64})
    elif case=='missing_last_page_index':save(p/'LAYOUT_VERIFICATION.json',{**layout,'page_indices_inspected':[1,2,3,4,5]})
    elif case=='duplicate_page_index':save(p/'LAYOUT_VERIFICATION.json',{**layout,'page_indices_inspected':[1,2,3,4,5,5]})
    elif case=='wrong_page_count':save(p/'LAYOUT_VERIFICATION.json',{**layout,'pages':5,'page_indices_inspected':[1,2,3,4,5]})
    elif case=='all_pages_false':save(p/'LAYOUT_VERIFICATION.json',{**layout,'all_pages_visually_inspected':False})
    elif case.startswith('context_'):save(W/'CURRENT_PR1241_CONTEXT.json',{**context,'expected_pdf_pages':True if case=='context_bool_pages' else 7})
    try:b.document_bindings()
    except Exception as e:done=False;error=type(e).__name__+': '+str(e)
    else:done=True;error=None
    need(done==(case=='positive'),'document binding incorrectly handled '+case);results.append({'case':case,'completed':done,'error':error})
save(HERE/'DOCUMENT_BINDING_RESULTS.json',{'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cases':results,'real_pdfinfo_used':True,'scope':'Unmodified actual document_bindings() with ROOT redirected to copies, real six-page PDF, real pdfinfo. Hash/status/page coverage controls, not a forged-receipt authenticity proof. Actual page visual inspection separately retained.'})
print('17 actual-document binding cases passed')
