\\ Small exact derivation aid for the delta>=3 incidence classification.
\\ Only binary factor arithmetic is used; there is no large Groebner job.

jac(f,g)=deriv(f,p)*deriv(g,q)-deriv(f,q)*deriv(g,p);

R=a*p^3+b*p^2*q+c*p*q^2+d*q^3;

showchart(label,h)={
  my(P=h*p^2,Q=h*q^2);
  my(alpha=jac(Q,R),beta=-jac(P,R),gamma=jac(P,Q));
  print("=== ",label," ===");
  print("alpha = ",alpha);
  print("beta  = ",beta);
  print("gamma = ",gamma);
};

showchart("branch_square",p^2);
showchart("two_branch",p*q);
showchart("one_branch",p*(p+q));
showchart("doubled_nonbranch",(p+q)^2);
showchart("interior_eta",p^2+ee*p*q+q^2);

quit(0);
