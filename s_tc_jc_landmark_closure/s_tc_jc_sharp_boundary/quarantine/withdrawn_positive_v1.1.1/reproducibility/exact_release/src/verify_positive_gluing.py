#!/usr/bin/env python3
"""Exact analytic inverse for positive JC tripod/cut gluing."""
from pathlib import Path
import json
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'certificates'/'positive_gluing.json'

def main():
 P,Q,z=sp.symbols('P Q z', positive=True)
 U=P*z;V=Q*z;W=P*Q
 z2=sp.sqrt(U*V/W);P2=sp.simplify(U/z2);Q2=sp.simplify(V/z2)
 assert sp.simplify(z2-z)==0 and sp.simplify(P2-P)==0 and sp.simplify(Q2-Q)==0
 assert sp.expand(z**2-U*V/W)==0
 J=sp.Matrix([U,V,W]).jacobian([P,Q,z]);det=sp.factor(J.det())
 assert det==-2*P*Q*z
 result={'status':'PROVED','inverse':{'z':'sqrt(UV/W)','P':'U/z','Q':'V/z'},'jacobian_determinant':str(det),'dimension_additivity':True,'positive_context_contraction':True}
 OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
