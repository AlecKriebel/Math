#!/usr/bin/env python3
import sys;from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'computation'))
from asymptotics import diffusion_extrema,R_INF,C_INF,HINF,ETA_INF,CUBIC_INF
import sympy as sp
assert diffusion_extrema(3)==(sp.Rational(1,56),sp.Integer(21),sp.Integer(1176))
for m in range(4,20): assert diffusion_extrema(m)[2]==1589*m-3220
assert R_INF+C_INF/sp.Integer(224)>0 and ETA_INF>0 and CUBIC_INF>0
print('ASYMPTOTICS_PASS')
