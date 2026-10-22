"""Supplementary finite exact-arithmetic checks; the Markdown proofs are primary."""
from fractions import Fraction
import json
from pathlib import Path
ROOT=Path(__file__).parent

def need(condition,message):
    if not condition:raise RuntimeError(message)

def cubic_length(j):return (j+1)**3-j**3

def logarithmic_length(j):return j*j.bit_length()**2

N=1000
cubic_partial=sum((Fraction(cubic_length(j),(2*cubic_length(j+1)+1)**2) for j in range(1,N+1)),Fraction())
cubic_tail=Fraction(1,12*N)
need(cubic_partial+cubic_tail<Fraction(1,6),'Cubic bound')
for j in range(1,10001):
    need(26*j*j >= (j+2)**3-j**3,'Cubic delay conversion')

K=10;J=2**K-1
log_partial=sum((Fraction(logarithmic_length(j),(2*logarithmic_length(j+1)+1)**2) for j in range(1,J+1)),Fraction())
log_tail=Fraction(1,4*K)
need(log_partial+log_tail<Fraction(1,2),'Log bound')
S=1
for j in range(1,10001):
    L=logarithmic_length(j);Ln=logarithmic_length(j+1);b=j.bit_length()
    need(S>=j,'Time-index comparison')
    need(Ln>=L,'Monotone lengths')
    if j>=2:
        need(20*S >= j*j*b*b,'Spatial-time lower bound')
        need(8*Ln<=27*L,'Successor-length bound')
        need(2*(L+Ln)<=9*L,'Lead bound')
        need(5*(j//2)*((j+1)//2)>=j*j,'Half-block lower count')
    else:
        need(S+L+Ln-1==9,'Initial lead')
    S+=L
need(Fraction(9,2)**2*20<21**2,'Final square-root constant')

neighborhood=lambda p:{(p[0]+dx,p[1]+dy) for dx in (-1,0,1) for dy in (-1,0,1)}
bad_centers=[]
for m in (2,3,10,30):
    B={(x,y) for x in range(3*m) for y in range(3*m) if x%3 or y%3}
    A={(x,y) for x in range(-1,3*m+1) for y in range(-1,3*m+1) if len(neighborhood((x,y))&B)>=8}
    E={(x,y) for x in range(-2,3*m+2) for y in range(-2,3*m+2) if neighborhood((x,y))<=A}
    need(len(B)==8*m*m,'Bomb cardinality')
    need(len(A)==(3*m-2)**2,'Danger-center cardinality')
    need(len(E)==(3*m-4)**2,'Losing-center cardinality')
    bad_centers.append({'m':m,'bombs':len(B),'danger_centers':len(A),'losing_centers':len(E),'ratio':str(Fraction(len(E),len(B)))})
for k in range(1,101):
    M=(2*k+1)**2;T=2*k+M+1
    need(k+M==T-k-1,'Earliest-deadline announcement budget')
    need(T-(T-k)==k,'Remaining moves')
room={(0,0),(0,1),(1,0),(1,1)}
minimum=min(len(neighborhood(p)&{(q[0]+dx,q[1]+dy) for q in room}) for p in room for dx,dy in ((0,0),(1,0),(-1,0),(0,1),(0,-1)))
need(minimum==2,'Room transport reachability')
def rounded_upper(x):
    scale=10**6
    return str(Fraction((x.numerator*scale+x.denominator-1)//x.denominator,scale))

result={'status':'PASS','scope':'Supplementary exact checks, not substitutes for proofs','cubic':{'terms':N,'certified_upper_on_partial_plus_tail':rounded_upper(cubic_partial+cubic_tail),'less_than':'1/6'},'logarithmic':{'terms':J,'certified_upper_on_partial_plus_tail':rounded_upper(log_partial+log_tail),'less_than':'1/2'},'integer_delay_checks_through_block':10000,'bad_center_cases':bad_centers,'deadline_budget_checks_through_k':100,'room_minimum_reachable_cells':minimum}
print(json.dumps(result,indent=2))
