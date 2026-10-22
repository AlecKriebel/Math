from pathlib import Path
import importlib.util,contextlib,io,json,hashlib,datetime
R=Path(__file__).resolve().parent;P=R/'scratch_local/audit/publication';s=importlib.util.spec_from_file_location('ind_actual_compile',P/'compile_note.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.PROGRAM=R/'scratch_local'
out=io.StringIO()
with contextlib.redirect_stdout(out):m.main()
(R/'RECOMPILE_STDOUT.txt').write_text(out.getvalue());receipt=json.loads((P/'COMPILE_RECEIPT.json').read_text());a=Path(json.loads((R/'INPUT_FREEZE.json').read_text())['root'])/'publication';same=(P/'output/pdf/main.pdf').read_bytes()==(a/'output/pdf/main.pdf').read_bytes()
if not same:raise RuntimeError('Same compiler/source stamp PDF differs')
(R/'RECOMPILE_RESULTS.json').write_text(json.dumps({'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','receipt':receipt,'exact_pdf_bytes':same,'copied_source_unchanged':(P/'manuscript/main.tex').read_bytes()==(a/'manuscript/main.tex').read_bytes(),'scope':'Actual compile_note.main on copied source, same installed Tectonic and cache, actual SOURCE_DATE_EPOCH environment. PROGRAM cache location redirected into ignored scratch; no original receipt/PDF/source changed. This is same-environment reproduction, not a cross-platform guarantee.'},indent=2)+'\n');print('Exact PDF recompilation PASS')
