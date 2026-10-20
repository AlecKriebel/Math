from isolated_completion import H,calculate
import json

def count(d,n,t):
 return n**d-(n-1)**d+H(d,n-1,2*t-1-d)-H(d,n-1,t-1)
def best(d,n):
 v,t=max((count(d,n,t),t) for t in range(d,d*n+1))
 return dict(d=d,n=n,size=v,t=t,isolated_best=calculate(d,n)['completed_best']['completed'])
if __name__=='__main__':
 print(json.dumps([best(d,n) for d,n in [(3,11),(3,29),(3,30),(3,50),(3,100),(4,5),(4,11),(5,9),(6,8)]],indent=2))
