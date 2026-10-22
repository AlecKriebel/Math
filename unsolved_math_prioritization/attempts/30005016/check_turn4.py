#!/usr/bin/env python3
from itertools import permutations
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import csv,json,argparse
p=argparse.ArgumentParser();p.add_argument('--certificate',default=str(Path(__file__).with_name('TURN_4_CERTIFICATE.csv')));args=p.parse_args()
def determinant3(m):
 return m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])-m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])+m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0])
rows=[];freq=Counter();n=0
for a,b,c,d,e,f in permutations([0,1,2,4,8,16]):
 v=-(d-a)*(e-c)*(f-b)+(d-b)*(e-a)*(f-c)
 m=[[-(d-a),d-b,0],[-(e-a),0,e-c],[0,-(f-b),f-c]]
 assert v==determinant3(m) and v!=0;n+=1
 rows.append((a,b,c,d,e,f,v));freq[abs(v)]+=1
assert len(rows)==720 and set(freq.values())=={48};n+=1
assert sorted(freq)==[24,48,104,112,136,152,168,192,272,296,304,320,344,408,456];n+=1
# Independently test the five-direction construction on all assignments of five small slopes.
for a,b,c,d,e in permutations(range(6),5):
 # A=(0,0), B=(1,a). C has slope b from A and slope c from B.
 cx=F(a-c,b-c);cy=b*cx;dx=F(a-e,d-e);dy=d*dx
 A=(F(0),F(0));B=(F(1),F(a));C=(cx,cy);D=(dx,dy)
 assert len({A,B,C,D})==4;n+=1
 for X,Y,s in [(A,B,a),(A,C,b),(B,C,c),(A,D,d),(B,D,e)]:
  assert Y[1]-X[1]==s*(Y[0]-X[0]);n+=1
with open(args.certificate,'w',newline='') as f:
 w=csv.writer(f);w.writerow(['s12','s13','s14','s23','s24','s34','determinant']);w.writerows(rows)
print(json.dumps({'assertions':n,'exhaustive_six_slope_assignments':720,'five_direction_controls':720,'absolute_determinant_frequencies':dict(sorted(freq.items())),'scope':'The 720 slope assignments are a complete certificate after the proved reduction. The 720 five-direction controls merely supplement that separate symbolic proof.'},indent=2,sort_keys=True))
