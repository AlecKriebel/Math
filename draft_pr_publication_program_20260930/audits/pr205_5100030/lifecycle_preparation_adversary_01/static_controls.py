"""Reproducible source-only operational checks. No backend or phase call."""
from pathlib import Path
import ast,datetime,hashlib,json,subprocess,sys

here=Path(__file__).resolve().parent
source=here.parent/'publication_lifecycle_preparation_01'
expected={
 'support205.py':{'bytes':26389,'sha256':'d808f016ec0181b9e150eee6fade6a6dc50eea93730f51b48383c05eb67f97be'},
 'ready205.py':{'bytes':17062,'sha256':'de6170d07cc7f1e03759a15e0ae624d75b786b16db22058357c3c41a7578b163'},
 'lifecycle205.py':{'bytes':24626,'sha256':'54bd94227cbea81fa17f20c6c90befc06674de546eaf25f559dcdd8bf7cb2c32'},
 'make_native205.py':{'bytes':12167,'sha256':'ed4420dc58574ce47dd731eb8c0a4382995dc2fce6792bd9f9d47294305d7772'},
}
rows={}
allowed={'pathlib','base64','datetime','hashlib','json','os','re','sys'}
for name,pin in expected.items():
    raw=(source/name).read_bytes();actual={'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
    if actual!=pin:raise RuntimeError('Final source pin drift '+name)
    tree=ast.parse(raw);imports=[];calls=[]
    for node in tree.body:
        if isinstance(node,(ast.Import,ast.ImportFrom)):
            imports.extend([x.name for x in node.names] if isinstance(node,ast.Import) else [node.module])
        elif isinstance(node,ast.Expr) and isinstance(node.value,ast.Call):calls.append(ast.unparse(node.value))
    if set(imports)-allowed or calls:raise RuntimeError('Unexpected source imports/top-level expression calls '+name)
    rows[name]={'pin':actual,'imports':imports,'top_level_expression_calls':calls}
command=[sys.executable,'-O','-B','-c','import runpy,sys;runpy.run_path(sys.argv[1])',str(source/'support205.py')]
result=subprocess.run(command,capture_output=True,text=True)
if result.returncode!=1 or 'Ordinary Python -B required' not in result.stderr:raise RuntimeError('Optimization guard did not fail closed')
report={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Source-only AST and Python optimization guard; no backend or actual phase execution','candidate_source_pins':expected,'source_static':rows,'optimized_support_import':{'returncode':result.returncode,'guard_message_present':True},'all_checks_passed':True}
result_file=here/'static_and_optimize_controls.json'
if result_file.exists():result_file.chmod(0o644)
result_file.write_text(json.dumps(report,indent=2)+'\n');result_file.chmod(0o444)
print(json.dumps({'all_checks_passed':True,'final_candidate_pins_match':True,'optimized_runtime_fails_closed':True}))
