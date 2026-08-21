\\ Exact determinantal certificate for the binary fixed-quadratic E7 split.

p='p; q='q;
aa='aa; bb='bb; cc='cc; dd='dd; ee='ee;
R=aa*p^3+bb*p^2*q+cc*p*q^2+dd*q^3;

fail(message) = { print(Str("FAIL: ",message)); quit(1); };
check(condition,message) = if(!condition,fail(message));
checkzero(value,message) = check(value == 0,message);
checkequal(value,expected,message) = checkzero(value-expected,message);

jac(f,g)=deriv(f,p)*deriv(g,q)-deriv(f,q)*deriv(g,p);
cf(f,i,j)=polcoef(polcoef(f,i,p),j,q);

blocks(h,level)={
  my(P=h*p^2,Q=h*q^2,f=jac(Q,R),g=-jac(P,R),k=jac(P,Q));
  my(cols,degree);
  if(level==2,
    cols=[f,g]; degree=5,
    if(level==1,
      cols=[f*p,f*q,g*p,g*q,k]; degree=6,
      cols=[f*p^2,f*p*q,f*q^2,g*p^2,g*p*q,g*q^2,k*p,k*q];
      degree=7
    )
  );
  matrix(degree+1,#cols,i,j,cf(cols[j],degree-(i-1),i-1))
};

hbranch=p^2;
htwo=p*q;
hone=p*(p+q);
hinterior=p^2+ee*p*q+q^2;

checkzero(matdet(blocks(hbranch,0)),"branch-square determinant");
checkequal(matdet(blocks(htwo,0)),373248*aa^3*dd^3, \
  "two-branch determinant");
checkequal(matdet(blocks(hone,0)), \
  124416*dd^3*(3*aa-4*bb)*(aa-bb+cc-dd)^2, \
  "one-branch determinant");

Phi=aa^2-aa*bb*ee+aa*cc*ee^2-2*aa*cc-aa*dd*ee^3 \
  +3*aa*dd*ee+bb^2-bb*cc*ee+bb*dd*ee^2-2*bb*dd \
  +cc^2-cc*dd*ee+dd^2;
checkequal(polresultant(p^2+ee*p+1,aa*p^3+bb*p^2+cc*p+dd,p), \
  Phi,"interior resultant");
checkequal(matdet(blocks(hinterior,0)), \
  -41472*(4*cc-3*dd*ee)*(ee-2)*(ee+2) \
    *(3*aa*ee-4*bb)*Phi^2, \
  "interior determinant");

\\ Generic and specialized Hilbert--Burch rank tuples.
ranktuple(h)=vector(3,i,matrank(blocks(h,3-i)));
suball(value,vars,vals)={
  my(out=value);
  for(i=1,#vars,out=subst(out,vars[i],vals[i]));
  out
};
specialranks(h,vars,vals)=vector(3,i, \
  matrank(suball(blocks(h,3-i),vars,vals)));

checkequal(ranktuple(hbranch),[2,5,7],"branch-square generic ranks");
checkequal(ranktuple(htwo),[2,5,8],"two-branch generic ranks");
checkequal(ranktuple(hone),[2,5,8],"one-branch generic ranks");
checkequal(ranktuple(hinterior),[2,5,8],"interior generic ranks");
checkequal(specialranks(hbranch,[dd],[0]),[2,5,6], \
  "branch-square first deeper rank");
checkequal(specialranks(hbranch,[dd,cc],[0,0]),[2,4,5], \
  "branch-square second deeper rank");
checkequal(specialranks(hbranch,[bb,cc,dd],[0,0,0]),[1,2,3], \
  "power-fibre exceptional ranks");
checkequal(specialranks(htwo,[aa],[0]),[2,5,7], \
  "two-branch first divisor rank");
checkequal(specialranks(htwo,[aa,dd],[0,0]),[2,5,6], \
  "two-branch transverse intersection rank");
checkequal(specialranks(hone,[bb],[3*aa/4]),[2,5,7], \
  "one-branch splitting divisor rank");
checkequal(specialranks(hinterior,[bb],[3*aa*ee/4]),[2,5,7], \
  "interior left splitting divisor rank");
checkequal(specialranks(hinterior,[bb,cc], \
  [3*aa*ee/4,3*dd*ee/4]),[2,5,6], \
  "interior two splitting divisors rank");
checkequal(specialranks(hinterior,[ee],[2]),[2,5,7], \
  "interior doubled-root rank");

print("ALL BINARY FIXED-QUADRATIC E7 DETERMINANTS PASSED");
quit;
