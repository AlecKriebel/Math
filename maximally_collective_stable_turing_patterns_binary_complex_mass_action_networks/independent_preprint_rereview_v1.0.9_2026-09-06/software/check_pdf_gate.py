#!/usr/bin/env python3
"""Measure all released coefficient rows and reject the historical overprint."""
import importlib.util, json, pathlib, subprocess, sys
from audit_driver import ENV, HERE, SOURCE, SCRATCH, run

# All imports in the child use the pinned release interpreter and package path.
code = '''import importlib.util,json,sys
from pathlib import Path
root=Path(sys.argv[1]); old=Path(sys.argv[2]);out=Path(sys.argv[3])
spec=importlib.util.spec_from_file_location("pdfaudit",root/"computation/audit_pdfs.py")
m=importlib.util.module_from_spec(spec);sys.modules["pdfaudit"]=m;spec.loader.exec_module(m)
result={}
for relative in ("manuscript/supplement.pdf","submission/journal/supplement.pdf"):
 n,gap=m.audit_modulus_table_spacing(root,root/relative)
 result[relative]={"rendered_rows":n,"minimum_coefficient_gap_points":gap}
try: m.audit_modulus_table_spacing(root,old)
except AssertionError as e: result["historical_pdf_with_current_source"]={"rejected":True,"reason":str(e)}
else: raise RuntimeError("Historical overlapping PDF was accepted")
out.write_text(json.dumps(result,indent=2)+"\\n")
print(json.dumps(result,indent=2))
'''
old=SOURCE.parents[1]/'independent_full_referee_2026-09-05/source_snapshot/manuscript/supplement.pdf'
if not old.is_file(): raise SystemExit('Historical PDF unavailable; retrieve immutable6f68ad3e source first')
if run('pdf_geometry_gate',['python','-c',code,str(SOURCE),str(old),str(HERE/'PDF_GATE_RESULTS.json')],SCRATCH): raise SystemExit(1)
for profile in ('full','journal'):
 if run('shipped_pdf_audit_'+profile,['python',str(SOURCE/'computation/audit_pdfs.py'),'--root',str(SOURCE),'--profile',profile,'--output-dir',str(HERE/('pdf_audit_'+profile))],SCRATCH): raise SystemExit(1)
