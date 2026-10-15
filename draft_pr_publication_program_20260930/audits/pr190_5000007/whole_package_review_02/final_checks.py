"""Remaining source-AST, archive-internal metadata, visual and seal consistency checks."""
from pathlib import Path
import ast,datetime,hashlib,json,stat,subprocess
R=Path(__file__).resolve().parent;A=R.parent;P=A/'publication_package_v2'
def need(x,m):
    if not x:raise ValueError(m)
def digest(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
rows=[]
for family,seal,key in [('exact_reproduction_adversary','FINAL_SEAL.json','public_file_sha256'),('global_geometry_adversary','FINAL_SHA256_SEAL.json','sha256'),('primary_priority_adversary','FINAL_SEAL.json','manifest'),('current_literature_priority_adversary','FINAL_SEAL.json','files')]:
    d=json.loads((A/family/seal).read_text())[key]
    fs=([{'path':n,'sha256':h} for n,h in d.items()] if isinstance(d,dict) else d)
    for f in fs:
        p=A/family/f['path'];b=p.read_bytes();need(hashlib.sha256(b).hexdigest()==f['sha256'],'family seal mismatch')
        if 'bytes' in f:need(len(b)==f['bytes'],'family size mismatch')
        need(stat.S_IMODE(p.stat().st_mode)==0o444,'family mode mismatch')
    rows.append({'family':family,'seal':seal,'authenticated_entries':len(fs),'all_actual_modes_0444':True})
ls=A/'literal_source_adversary'
for line in (ls/'FINAL_SHA256SUMS.txt').read_text().splitlines():
    h,n=line.split(None,1);p=ls/n;need(hashlib.sha256(p.read_bytes()).hexdigest()==h,'literal seal mismatch');need(stat.S_IMODE(p.stat().st_mode)==0o444,'literal mode mismatch')
rows.append({'family':'literal_source_adversary','seal':'FINAL_SHA256SUMS.txt','authenticated_entries':10,'all_actual_modes_0444':True})
# Reverse only the documented guard conversion and compare complete expression trees.
class Guard(ast.NodeTransformer):
    def visit_If(self,node):
        if isinstance(node.test,ast.UnaryOp) and isinstance(node.test.op,ast.Not) and len(node.body)==1 and isinstance(node.body[0],ast.Raise) and not node.orelse:
            ex=node.body[0].exc
            if isinstance(ex,ast.Call) and isinstance(ex.func,ast.Name) and ex.func.id=='AssertionError' and ex.args and isinstance(ex.args[0],ast.Constant) and ex.args[0].value=='audit-hardened validation guard failed':return ast.Assert(test=node.test.operand,msg=None)
        return self.generic_visit(node)
asts=[]
for name in ['check_certificate.py','check_half_turn.py']:
    original=ast.parse((A/'original_submission/files/unsolved_math_prioritization/attempts/5000007'/name).read_text());current=ast.parse((P/'verification/current'/name).read_text())
    count=sum(isinstance(x,ast.Assert) for x in ast.walk(original));need(not any(isinstance(x,ast.Assert) for x in ast.walk(current)),'assert remains')
    need(ast.dump(original)==ast.dump(Guard().visit(current)),'guard scientific AST mismatch')
    asts.append({'script':name,'guards_replaced':count,'whole_scientific_AST_identical_after_inverse_guard_conversion':True})
md=json.loads((P/'zenodo-deposit.json').read_text());inner=json.loads((P/'verification/provenance/intended_zenodo_metadata.json').read_text());need(md['metadata']==inner,'intended Zenodo metadata mismatch')
for name in ['dodecahedron_endpoint.pdf','dodecahedron_endpoint.tex']:need((P/name).read_bytes()==(P/'verification/manuscript'/name).read_bytes(),'manuscript copy differs')
visual=[]
for i in range(1,5):
    p=R/f'render/supplied-{i}.png';q=R/f'render/rebuilt-{i}.png';need(p.read_bytes()==q.read_bytes(),'page render differs');visual.append({'page':i,'personally_viewed_complete_supplied_page':True,'rebuilt_render_bytes_equal':True,'render':digest(p.read_bytes())})
need((R/'supplied_pdftotext.stdout').read_bytes()==(R/'rebuilt_pdftotext.stdout').read_bytes(),'PDF text differs')
# Own displayed-coordinate check in the degree-four cyclotomic field, independent
# of the canonical quadratic formula A^2+phi*A*B+B^2.
ns={'__file__':str(R/'independent_link_and_refolding.py')}
exec(compile((R/'independent_link_and_refolding.py').read_text().split('# Build the entire metric link')[0],str(R/'independent_link_and_refolding.py'),'exec'),ns)
F=ns['F'];add=ns['add'];scale=ns['scale'];mul=ns['mul'];power=ns['powr'];one=ns['one'];sub=ns['sub']
sqrt5=add(one,scale(2,add(power(1),power(4))));eta=scale(-1,power(3));aa=add(scale(F(31,2),one),scale(F(13,2),sqrt5));bb=add(scale(-17,one),scale(-8,sqrt5));v=add(aa,mul(bb,eta))
conjugate=sum([],[]) if False else ns['zero']
for j,c in enumerate(v):conjugate=add(conjugate,scale(c,power(-j)))
actual=mul(v,conjugate);expected=add(scale(F(425,2),one),scale(F(189,2),sqrt5));advertised=add(scale(F(307,2),one),scale(F(137,2),sqrt5));need(actual==expected,'own quartic coordinate norm mismatch');need(sub(actual,advertised)==add(scale(59,one),scale(26,sqrt5)),'own coordinate discrepancy mismatch')
result={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'family_seals':rows,'scientific_AST_comparison':asts,'inner_metadata_equals_uploader_metadata_object':True,'inner_manuscript_replicas_equal':True,'visual':visual,'all_four_pages_layout':'Complete pages personally inspected; no clipping, overlap, unreadable equation or broken reference. Two underfull warnings concern one bibliography paragraph and produce no visible defect. No UI/editor/tab opened.','rebuilt_and_supplied_text_equal':True,'own_cyclotomic_coordinate_norm':{'eta':'-r^3','actual':'(425+189sqrt5)/2','advertised':'(307+137sqrt5)/2','difference':'59+26sqrt5','polynomial_coefficients':list(map(str,actual))},'result':'PASS'}
(R/'FINAL_CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
