"""Complete finite Thue-Morse languages via substituted adjacent pairs."""
def substitute(w):return ''.join('01' if x=='0' else '10' for x in w)
def language(n):
 k=0
 while 2**k<n-1:k+=1
 words=set()
 for ab in ['00','01','10','11']:
  w=ab
  for _ in range(k):w=substitute(w)
  words.update(tuple(map(int,w[i:i+n])) for i in range(len(w)-n+1))
 return words
