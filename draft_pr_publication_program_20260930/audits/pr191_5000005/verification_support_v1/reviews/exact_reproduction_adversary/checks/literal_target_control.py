"""Exact counterexample to the bare A0 shorthand, not to repaired type law."""
import json
n=5;M=n-2
# For direct X0Xj in source clockwise order: a=n-j-1,b=n-j+1.
first={'vertex':2,'a':2,'b':4,'segments':1,'figure9_k':1}
second={'vertex':3,'a':1,'b':3,'segments':1,'figure9_k':2}
ell=-1;epsilon=1
if not all(t['b']-t['a']==2 for t in (first,second)):raise RuntimeError('bare antecedent')
if second['a']!=ell+epsilon*first['a']:raise RuntimeError('unwrapped transform')
if not all(0<=t['a']<=M for t in (first,second)):raise RuntimeError('sector')
if (epsilon*first['figure9_k']-ell)%M!=second['figure9_k']:raise RuntimeError('repaired law fails')
bare_predicted=(epsilon*0-ell)%M
if bare_predicted==0:raise RuntimeError('false control failed to reject bare target')
print(json.dumps({'status':'PASS_COUNTEREXAMPLE_TO_BARE_SHORTHAND','n':n,'angular_units':'pi/n','first':first,'second':second,'ell':ell,'epsilon':epsilon,'bare_A0_assignments':[0,0],'bare_signed_law_predicts_second_type':bare_predicted,'parity_repaired_signed_law_passes':True},indent=2))
