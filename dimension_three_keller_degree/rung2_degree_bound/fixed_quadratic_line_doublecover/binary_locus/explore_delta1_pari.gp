\\ Exploratory PARI kernels on delta=1 determinant components.
p='p;q='q;
aa='aa;bb='bb;cc='cc;dd='dd;ee='ee;
R=aa*p^3+bb*p^2*q+cc*p*q^2+dd*q^3;
jac(f,g)=deriv(f,p)*deriv(g,q)-deriv(f,q)*deriv(g,p);
cf(f,i,j)=polcoef(polcoef(f,i,p),j,q);
m0(h,RR)={
  my(P=h*p^2,Q=h*q^2,f=jac(Q,RR),g=-jac(P,RR),k=jac(P,Q));
  my(cols=[f*p^2,f*p*q,f*q^2,g*p^2,g*p*q,g*q^2,k*p,k*q]);
  matrix(8,8,i,j,cf(cols[j],8-i,i-1))
};
show(label,h,RR)={
  my(M=m0(h,RR),N=matker(M));
  print(label);
  print(Str("rank=",matrank(M)," kernel=",matsize(N)[2]));
  print(N);
};
show("one split",p*(p+q),subst(R,bb,3*aa/4));
show("one fixed root",p*(p+q),subst(R,cc,-aa+bb+dd));
show("branch square",p^2,R);
show("interior left",p^2+ee*p*q+q^2,subst(R,bb,3*aa*ee/4));
show("interior right",p^2+ee*p*q+q^2,subst(R,cc,3*dd*ee/4));
show("interior square",p^2+2*p*q+q^2,subst(R,ee,2));
quit;
