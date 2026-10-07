#!/usr/bin/env python3
"""Exact input/arithmetic diagnostics. Not a formal mathematical proof verifier."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,zipfile

ROOT=Path(__file__).resolve().parent

def require(ok, message):
    if not ok:
        raise ValueError(message)

def check_blob(data,record,label):
    require(len(data)==record['bytes'],label+': size')
    require(hashlib.sha256(data).hexdigest()==record['sha256'],label+': sha256')


def main():
    b=json.loads((ROOT/'TARGET_BINDINGS.json').read_text())
    require(b['problem_id']==9700036 and b['rank']==936,'identity')
    exact={
      'SIRSN_TREE_9700036_AUTHOR_SAFE_FREEZE.zip':(10688,'3008e91a1b89b12efe3b3e300e9957585b84d81db715cad3ba340cf38db6be4e'),
      'SIRSN_TREE_9700036_AUTHOR_EXTERNAL_MANIFEST.json':(1124,'8d3de572463b79fb308117515b3710fca0fb1075fdcda4f30ebb57666f066a7a'),
      'SIRSN_TREE_9700036_CLARIFIED_SAFE.zip':(12085,'6b2264154ecdd680c2fd888d1d8c63d0b6bd0a3ba174dcece23b4fed677fe0a1'),
      'SIRSN_TREE_9700036_CLARIFIED_EXTERNAL_MANIFEST.json':(1437,'8ca08cc5e379eacfe306569d0bb27d2e1117cd8e3d8a20d8251e009793030210'),
      'SOURCE_PROOF_REPAIR_V1.md':(12374,'5d6598108c9fc3aacc7d127eb16da1af1f2ca3a4654222864036963df6ceddeb'),
    }
    for name,(size,sha) in exact.items():
        rec={'bytes':size,'sha256':sha}
        require(b['bindings'][name]==rec,'binding metadata '+name)
        path=ROOT/name if name.endswith('.md') else ROOT/'inputs'/name
        check_blob(path.read_bytes(),rec,name)
    cm=json.loads((ROOT/'inputs'/'SIRSN_TREE_9700036_CLARIFIED_EXTERNAL_MANIFEST.json').read_text())
    with zipfile.ZipFile(ROOT/'inputs'/'SIRSN_TREE_9700036_CLARIFIED_SAFE.zip') as z:
        prefix='sirsn_tree_9700036/'
        require(set(z.namelist())=={prefix+n for n in cm['package_members']},'exact clarified members')
        for name,rec in cm['package_members'].items():
            check_blob(z.read(prefix+name),rec,'clarified '+name)
        check_blob(z.read(b['clarified_result']['member']),b['clarified_result'],'clarified RESULT')
    checks=[]
    def check(ok,label):require(ok,label);checks.append(label)
    q=F(1,2**1000);p=2*q-q*q
    check(p<=F(1,2**999),'bad-pair bound')
    check(6**20*p<F(1,2**940),'long-contour exponential base')
    check(4*F(9,256)**4/(1-F(9,256))<F(1,20),'zero-cost circuit bound')
    check(F(125000,2**1020)<q,'fixed m supports q0')
    check((1+F(1,2**1020))*q<F(1,2000**2),'bad-terminal mean bound')
    check((F(24,100)-F(8,10)*F(5,1000)-F(1,1000))/F(93,100)==F(47,186),'blue fraction exact')
    check((F(20,100)-F(8,10)*F(5,1000)-F(1,1000))/F(89,100)==F(39,178),'red fraction exact')
    check(F(39,178)>F(21,100) and F(39,178)<F(1,4),'red margin and original gap')
    check(F(47,186)>F(21,100),'blue margin')
    check(F(21,100)-F(1,640000)>F(20,100),'recolor margin')
    check(F(20,100)-F(1,100)-F(1,100)==F(18,100),'short-circuit area margin')
    check(F(88,1000)/8000==F(11,1000000),'beta0')
    check(F(5,1000)-F(1,640000)>F(4,1000),'many-mixed-square margin')
    check(F(8,100)*F(4,1000)>F(11,1000000),'many-mixed-square pair constant')
    for k in range(8000,25001):
        s=(k+999)//1000
        require(F(s)<=F(k,800),'rounded side bound')
        require(F(k,200)-4*s>=F(k,2000),'excluded-square edge bound')
        require(F(k,5000)+2<=s,'centroid-neighborhood covering bound')
    checks.append('17001 rounded-side/perimeter/covering spot checks')
    for ell in range(28,10001):
        require(F(ell//7)-F(ell,20)>=F(ell,20),'selected bad-pair threshold')
    checks.append('9973 selected-pair threshold spot checks')
    for r in [F(1,7),F(1),F(10,3),F(100)]:
        check((r**3/F(3))/(r*r/F(2))==2*r/3,'radial mean '+str(r))
    out={'status':'PASS','problem_id':9700036,'input_pins_verified':len(exact),'clarified_members_verified':5,'arithmetic_checks':checks,'scope':'Input integrity and exact arithmetic diagnostics only; mathematical acceptance is the independent analytic review.'}
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':main()
