import itertools,json,sys
class ReviewFailure(Exception):pass
def need(b,m):
 if not b:raise ReviewFailure(m)
def laws(X,meet,op,e):
 for x in X:
  need(op(e,x)==x and op(x,e)==e and op(x,x)==e,'unit/diagonal')
  for y in X:
   need((op(x,y)==e)==(meet(x,y)==x),'order')
   need((op(x,y)==e and op(y,x)==e)==(x==y),'separation')
   for z in X:
    need(op(x,meet(y,z))==meet(op(x,y),op(x,z)),'S1')
    need(op(meet(x,y),z)==op(op(x,y),op(x,z)),'S3')
    need(op(op(x,y),op(x,z))==op(op(y,x),op(y,z)),'cycloid')
    if meet(x,y)==x:need(op(x,op(y,z))==op(x,z),'translation absorption')
 return True

def check_family(X):
 e=15;op=lambda x,y: e if x&y==x else x&y
 laws(X,lambda x,y:x&y,op,e)
 # Candidate partial multiplication criterion is verified from its original
 # existential specification, without treating an absent product as a value.
 for y in X:
  for z in X:
   rs=[]
   for r in X:
    products=[w for w in X if w&y==w and op(y,w)==r]
    need(len(products)<=1,'partial-product uniqueness')
    if products and products[0]&z==products[0]:rs.append(r)
   need(op(y,z) in rs and all(r&op(y,z)==r for r in rs),'partial-product greatest criterion')
 return len(X)**3

def main():
 if '--inject-failure' in sys.argv:need(False,'ROUND2_MATH_INJECTED_FALSE')
 distribution={};n=0;triples=0
 # All 2^15 families containing the universal four-point set. Closure by
 # intersection is checked directly, without using a published enumeration.
 for mask in range(1<<15):
  X=[i for i in range(15) if mask>>i&1]+[15];bag=set(X)
  if not all((a&b) in bag for a in X for b in X):continue
  triples+=check_family(X);n+=1;distribution[len(X)]=distribution.get(len(X),0)+1
 # A larger hIS4 family does not imply the target identities, even with
 # order agreement and meet preservation. Use original quantified H3.
 X=range(4);h=((3,3,3,3),(0,3,3,3),(0,0,3,3),(0,1,2,3));op=lambda x,y:h[x][y]
 for x,y,z in itertools.product(X,repeat=3):
  need(not x<=op(y,z) or min(x,y)<=z,'original H3')
  need(op(x,min(x,y))==op(x,y),'H4')
  need(op(x,min(y,z))==min(op(x,y),op(x,z)),'countermodel S1')
 for x,y in itertools.product(X,repeat=2):
  need(op(3,x)==x and op(x,3)==3 and op(x,x)==3,'countermodel units')
  need((op(x,y)==3)==(x<=y),'countermodel order')
 need(op(op(1,2),op(1,0))!=op(op(2,1),op(2,0)),'hIS4 cycloid must fail')
 need(op(min(2,1),0)!=op(op(2,1),op(2,0)),'hIS4 S3 must fail')
 # Exact old fallback-y operation fails S1 on the Boolean square.
 X=[0,1,2,3];old=lambda x,y:3 if x&y==x else y
 need(old(1,1&2)!=old(1,1)&old(1,2),'old fallback-y must fail')
 # Missing separation makes the necessity statement false: projection at
 # a nongreatest point satisfies S1--S4 but is outside the simultaneous class.
 for e in [0,1,2,3]:
  for x,y,z in itertools.product(X,repeat=3):
   proj=lambda a,b:b
   need(proj(x,y&z)==proj(x,y)&proj(x,z),'projection S1')
   need(proj(x&y,z)==proj(proj(x,y),proj(x,z)),'projection S3')
  need(all(proj(e,x)==x and proj(x,e)==e for x in X),'projection units')
 # Sample infinite carrier operations are checked only as implementation
 # diagnostics; missing-bottom and topless claims are proved symbolically.
 for e in [0]:
  ns=range(-20,1);topop=lambda x,y:0 if x<=y else min(x,y)
  laws(ns,min,topop,e)
 print(json.dumps({'status':'PASS','family_mechanism':'all intersection-closed families containing the universal subset of a four-point base','checked_families':n,'sizes':distribution,'checked_ordered_triples':triples,'translation_absorption_and_original_partial_product_criterion':True,'hIS4_countermodel_original_H3_H4_S1_order_units_checked':True,'hIS4_cycloid_failure':{'x':1,'y':2,'z':0},'hIS4_S3_failure':{'x':2,'y':1,'z':0},'old_fallback_y_Boolean_S1_failure':True,'projection_every_prescribed_point':4,'nonpositive_integer_sample_only':21,'limits':'Finite supplementary diagnostics. Universal proof and infinite no-bottom/topless boundaries are separate symbolic arguments.'},sort_keys=True))
if __name__=='__main__':main()
