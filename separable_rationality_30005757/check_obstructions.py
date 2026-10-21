"""Exact positive-system identities; these are not permutation classes."""
import sympy as s
import json
T=s.symbols('T');x=T/(1+T)**2
S=1/(1-T)
D=3*T+4*T*T*S+4*T*T*S*S
A=(1-T)/(1-3*T+T*T);B=T/(1-3*T+T*T)
checks=[1+T+D-1/(1-4*x),A-1-2*T*A-T*B,B-T*A-T*B,B-x/(1-5*x),1+T+(4*T+10*T*T*A+5*T*T*B+5*T*B)-1/(1-5*x)]
for i,c in enumerate(checks):
 if s.factor(c)!=0:raise RuntimeError('Positive grammar identity '+str(i)+' failed')
print(json.dumps({'positive_grammar_exact_identities':len(checks),'all_zero':True,'permutation_class_counterexample':False},indent=2))
