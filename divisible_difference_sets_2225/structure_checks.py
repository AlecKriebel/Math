"""Bounded cross-checks of authored formulas. Not an unrestricted proof."""
import itertools,json
from fractions import Fraction

def require(condition,message):
 if not condition:raise RuntimeError(message)
def edge(a,b,t):
 d=abs(a-b)
 return d>=t and max(a,b)%d==0
def oddpart(x):
 while x%2==0:x//=2
 return x
def power_count(n,t):
 L=n.bit_length()-1;q=max(1,(t-1).bit_length())
 return min(L,q-1)+(max(0,L-q+1)+1)//2
def transfer_edge(low,high,g):
 c=abs((1<<g)*high-low)
 return low%c==0
def maximum_cycle_mean(graph):
 means=[]
 def visit(start,node,seen,weight):
  for nxt,w in graph[node]:
   if nxt==start:means.append(Fraction(weight+w,len(seen)))
   elif nxt not in seen:visit(start,nxt,seen+(nxt,),weight+w)
 for start in graph:visit(start,start,(start,),0)
 return max(means)
def main():
 counts={'threshold':0,'oddpart':0,'power_paths':0,'transfer_edges':0}
 for n in range(1,41):
  for t in range(1,9):
   for a in range(1,n+1):
    for b in range(a+1,n+1):
     expected=any(a==k*d and b==(k+1)*d for d in range(t,b+1) for k in [a//d])
     require(edge(a,b,t)==expected,'threshold');counts['threshold']+=1
   for x in range(2,n+1,2):
    free=all(not edge(x,y,t) for y in range(1,n+1,2))
    require(free==(oddpart(x)<t),'oddpart');counts['oddpart']+=1
   if t>=2:
    powers=[1<<k for k in range(1,n.bit_length())]
    best=max(sum(bits) for bits in itertools.product([0,1],repeat=len(powers)) if all(not(bits[i] and bits[j]) or not edge(a,b,t) for i,a in enumerate(powers) for j,b in enumerate(powers) if i<j))
    require(best==power_count(n,t),'power_paths');counts['power_paths']+=1
 for t in range(2,13):
  K=(t-1).bit_length()
  for m in range(1,t,2):
   for n in range(1,t,2):
    for g in range(1,8):
     require(transfer_edge(m,n,g)==edge((1<<K)*m,(1<<(K+g))*n,t),'transfer_edges');counts['transfer_edges']+=1
 # t=2 transfer states: empty / occupied previous layer. Only the occupied-to-occupied transition is forbidden.
 graph={0:[(0,0),(1,1)],1:[(0,0)]}
 rho=maximum_cycle_mean(graph)
 require(rho==Fraction(1,2),'cycle_mean')
 print(json.dumps({'passed':True,'counts':counts,'cycle_mean_t2':str(rho),'scope':'Bounded formula checks and t=2 cycle mean only; no larger-t coefficient certified.'},sort_keys=True))
if __name__=='__main__':main()
