#!/usr/bin/env python3
import itertools,json
checks=0
def ck(x):
 global checks
 assert x;checks+=1

def path(word):
 p=[0,0];labels=[]
 for a in word:
  if abs(a)==1:p[0]+=1 if a>0 else -1
  elif a==2:labels.append((tuple(-x for x in p),1));p[1]+=1
  else:p[1]-=1;labels.append((tuple(-x for x in p),-1))
 return labels,tuple(p)

def reduce_free(word):
 out=[]
 for x in word:
  if out and out[-1][0]==x[0] and out[-1][1]==-x[1]:out.pop()
  else:out.append(x)
 return out

def action(word,h):return [(tuple(g[i]-h[i] for i in range(2)),s) for g,s in word]
def product_images(a,b):
 la,ha=a;lb,hb=b
 return reduce_free(la+action(lb,ha)),tuple(ha[i]+hb[i] for i in range(2))
words=[];no_y=has_y=0
for n in range(0,8):
 for w in itertools.product((1,-1,2,-2),repeat=n):
  if any(w[i]==-w[i-1] for i in range(1,n)):continue
  l,h=path(w);ck(l==reduce_free(l));ck(h==(sum(1 if a==1 else -1 if a==-1 else 0 for a in w),sum(1 if a==2 else -1 if a==-2 else 0 for a in w)))
  if w:ck(bool(l) or h!=(0,0))
  if any(abs(a)==2 for a in w):has_y+=1
  else:no_y+=1
  if n<=3:words.append(w)
pairs=0
for a in words:
 for b in words:
  direct=path(a+b);direct=(reduce_free(direct[0]),direct[1]);ck(product_images(path(a),path(b))==direct);pairs+=1
# Positive commutator x y x^-1 y^-1 has linear symbol t_-e1-t_0.
l,h=path((1,2,-1,-2));ck(h==(0,0));ck(l==[((-1,0),1),((0,0),-1)])
# Its finite-support total coefficient is zero, unlike a standard meridian chord.
ck(sum(s for g,s in l)==0)
print(json.dumps({'assertions':checks,'reduced_words_through_length7':no_y+has_y,'with_vertical_letters':has_y,'without_vertical_letters':no_y,'multiplicativity_pairs':pairs,'commutator_image_free_word':l,'commutator_degree_zero':h,'scope':'Exact auxiliary free-group crossed-product tests. Formal-series faithfulness uses the separately proved classical equivariant Magnus embedding.'},indent=2))
