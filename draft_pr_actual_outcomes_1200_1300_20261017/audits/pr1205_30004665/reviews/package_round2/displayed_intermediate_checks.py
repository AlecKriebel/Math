"""New literal comparison of all displayed reverse-pullback proof stages.

This check deliberately uses the distributed sparse arithmetic engine, which
was independently cross-checked against the fresh forward-X reconstruction.
It is not another independent arithmetic implementation.
"""
import importlib.util, json, pathlib
HERE=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('distributed_verifier',HERE/'extracted/verify.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
B,F=v.quiver(v.WORD);route=(2,6,1,3,4,8,5,10)
matrices=[B]
for k in route:matrices.append(v.mutate(matrices[-1],k-1,F))
stage4=[(),(8,),(8,10),(5,8,10),(4,5,8,10)]
stage3=[(),(8,),(3,8),(8,10),(5,8,10),(3,8,10),(3,5,8,10),(3,4,5,8,10)]
stage1=stage3+[(1,3,4,5,8,10)]
stage6=[(),(6,),(6,8),(3,6,8),(6,8,10),(5,6,8,10),(3,6,8,10),(3,5,6,8,10),(3,4,5,6,8,10),(3,4,5,6,6,8,10),(1,3,4,5,6,6,8,10)]
expected={4:v.add(*(v.monomial(7,*p) for p in stage4)),3:v.add(*(v.monomial(7,*p) for p in stage3)),1:v.add(*(v.monomial(7,*p) for p in stage1)),6:v.add(*(v.monomial(7,*p) for p in stage6))}
d=json.loads((HERE/'extracted/certificate.json').read_text())
expected[2]={tuple(r['a']):1 for r in d['certificate_rows'] if r['a'][6]}
p=v.monomial(7);report=[]
for j in reversed(range(len(route))):
    k=route[j];p=v.pullback(p,matrices[j],k-1)
    if k in expected:
        if p!=expected[k]:raise ValueError('displayed stage mismatch '+str(k))
        report.append({'final_reverse_step':k,'terms':len(p),'displayed_identity_exact':True})
(HERE/'displayed_intermediate_checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
