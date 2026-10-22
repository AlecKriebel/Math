"""Exact isolated-completed coordinate-sum slice lower bounds, no floats."""
from math import comb
import json

def H(d,n,s):
 if n<=0:return 0
 return sum((-1)**j*comb(d,j)*(comb(s-j*n,d) if s-j*n>=d else 0) for j in range(d+1))
def calculate(d,n):
 I=n**d-2*(n-1)**d+(n-2)**d
 def HI(s):return H(d,n,s)-H(d,n-1,s)-H(d,n-1,s-d)+H(d,n-2,s-d)
 rows=[]
 for t in range(1,d*n+1):
  base=H(d,n,2*t-1)-H(d,n,t-1)
  extra=I-HI(2*t-1)+HI(t-1)
  rows.append({'t':t,'slice':base,'missing_isolated':extra,'completed':base+extra})
 return {'d':d,'n':n,'plain_best':max(rows,key=lambda r:r['slice']),'completed_best':max(rows,key=lambda r:r['completed'])}
if __name__=='__main__':
 pairs=[(3,11),(4,5),(5,4),(6,3),(3,15),(3,20),(3,30),(3,50),(3,100)]
 print(json.dumps([calculate(d,n) for d,n in pairs],indent=2))
