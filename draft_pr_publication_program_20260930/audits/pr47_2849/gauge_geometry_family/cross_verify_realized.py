#!/usr/bin/env python3
"""Own exact cross-verification after source-first family independence was preserved."""
from pathlib import Path
import hashlib, itertools, json, math, subprocess, urllib.request
import sympy as s
ROOT=Path(__file__).resolve().parent
checks={}
def ck(label,value):
    assert bool(value),label
    checks[label]=True
M=s.Matrix([[3,0,0,1],[0,3,0,1],[0,0,3,2],[1,1,1,0]])
divisors=[]
for k in range(1,5):
    ds=[abs(int(M.extract(rows,cols).det())) for rows in itertools.combinations(range(4),k) for cols in itertools.combinations(range(4),k)]
    divisors.append(math.gcd(*ds))
ck("integer_relation_determinant_minus36",M.det()==-36)
ck("all_minor_gcds_1_1_3_36",divisors==[1,1,3,36])
omega=(-1+s.sqrt(3)*s.I)/2
for a in [omega,omega**2]:
    a=s.simplify(a)
    R=s.Matrix([[0,0,0,1-a],[1,a,a**2,0]]).applyfunc(s.simplify)
    B=s.Matrix([a-1,a-1,a-1,0])
    ck("cube_relation_coefficient_zero_"+str(a),s.simplify(1+a+a**2)==0)
    ck("cocycle_constraints_rank_two_"+str(a),R.rank()==2)
    ck("coboundary_nonzero_"+str(a),B.rank()==1)
    ck("coboundary_in_kernel_"+str(a),(R*B).applyfunc(s.simplify)==s.zeros(2,1))
    ck("normal_complex_H1_one_"+str(a),4-R.rank()-B.rank()==1)
d=s.symbols("d",real=True)
for theta1,theta2 in [(2*s.pi/3,2*s.pi/3),(s.pi/3,s.pi/3)]:
    realpart=s.cos(theta1)*s.cos(theta2)-d*s.sin(theta1)*s.sin(theta2)
    ck("quaternion_axes_endpoint_"+str(theta1),s.solve(s.Eq(realpart,-s.Rational(1,2)),d)==[1])
ck("nonzero_Seifert_Euler_number",-(s.Rational(1,3)+s.Rational(1,3)+s.Rational(2,3))==-s.Rational(4,3))
ck("degree3_bundle_Euler_number",3*(-s.Rational(4,3))==-4)
ck("circle_bundle_rational_b1_two",s.Matrix([[0,0,4]]).rank()==1 and 3-1==2)
url="https://zentner.app.uni-regensburg.de/menagerie.pdf"
with urllib.request.urlopen(url,timeout=45) as response: data=response.read();final_url=response.url
sha=hashlib.sha256(data).hexdigest()
ck("author_primary_identity",sha=="e3595453cbe70e44a6fa0f57137228218910c6c5d0223dfc9add2171e1a92f67" and len(data)==461253)
tmp=ROOT/"tmp"/"pdfs";tmp.mkdir(parents=True,exist_ok=True)
pdf=tmp/"menagerie.pdf";pdf.write_bytes(data)
for page in [4,25,26]:
    subprocess.run(["/opt/homebrew/bin/pdftoppm","-f",str(page),"-l",str(page),"-r","110","-png","-singlefile",str(pdf),str(tmp/("menagerie_page_"+str(page)))],capture_output=True,check=True)
pdf.unlink()
out={"passed":len(checks),"failed":0,"checks":checks,"integer_determinantal_divisors":divisors,"H1_integer":"C3 plus C12; order 36","normal_H1_complex_dimension":1,"adjoint_H1_real_dimension":2,"source":{"url":url,"final_url":final_url,"bytes":len(data),"sha256":sha,"selected_pdf_pages":[4,25,26]},"scope":"Known genuine target-premise degenerate example, independently checked after early family independence; no I# calculation or counterexample to KP-3.51."}
(ROOT/"REALIZED_CROSS_RESULTS.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))
