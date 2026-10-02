"""Exact finite-word definitions; indices are zero-based and words are tuples."""
def theta_word(w,theta):
 return tuple(theta[a] for a in w)
def negative_periods(w,theta):
 t=theta_word(w,theta);n=len(w)
 return [p for p in range(1,n+1) if w[p:]==t[:n-p]]
def theta_borders(w,theta):
 t=theta_word(w,theta);n=len(w)
 return [k for k in range(1,n) if w[n-k:]==t[:k]]
def tau_theta(w,theta):
 n=len(w);t=theta_word(w,theta)
 for m in range(n,0,-1):
  for i in range(n-m+1):
   if not any(w[i+m-k:i+m]==t[i:i+k] for k in range(1,m)):return m
 raise ValueError('nonempty words only')
def parameters(w,theta):return tau_theta(w,theta),negative_periods(w,theta)[0]
def orbit_projection(w,theta):return tuple(min(a,theta[a]) for a in w)
