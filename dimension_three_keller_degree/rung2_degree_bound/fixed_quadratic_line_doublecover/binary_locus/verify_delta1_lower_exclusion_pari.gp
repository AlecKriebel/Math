\\ Independent exact replay of the two completed delta=1 families.

p='p; q='q; r='r; zz='zz;
bb='bb; dd='dd; kk='kk;
bu1='bu1; bu3='bu3; bv1='bv1; bv2='bv2; bv3='bv3;
bt0='bt0; bt2='bt2; bx0='bx0; bx2='bx2; by0='by0; by2='by2;
bl0='bl0; bl1='bl1; bl3='bl3; bl4='bl4; bl7='bl7;
aa='aa; cc='cc;
iu0='iu0; iu1='iu1; iu2='iu2;
iv0='iv0; iv2='iv2; it0='it0; it2='it2;
ix0='ix0; ix2='ix2; iy0='iy0; iy2='iy2;
il0='il0; il1='il1; il3='il3; il4='il4; il6='il6;

fail(message) = { print(Str("FAIL: ",message)); quit(1); };
check(condition,message) = if(!condition,fail(message));
checkzero(value,message) = check(value == 0,message);
checkequal(value,expected,message) = checkzero(value-expected,message);

vars=[p,q,r];
jacmat(V)=matrix(3,3,i,j,deriv(V[i],vars[j]));
weighted(H4,H3,H2,L)=matdet(L+zz*jacmat(H2)+zz^2*jacmat(H3) \
  +zz^3*jacmat(H4));

\\ Branch-square family, after the complete E6 and E5 solution.
bH4=[p^4,p^2*q^2,0]~;
bH3=[2*bv2*p^3+bu1*p^2*q+bu3*q^3+2*kk*r*p^2, \
  bv1*p^2*q+bv2*p*q^2+bv3*q^3+kk*r*q^2, \
  bb*p^2*q+dd*q^3]~;
bH2=[bx0*p^2+bu1*bv2*p*q+bx2*q^2 \
    +kk*r*(2*bv2*p+bu1*q)+kk^2*r^2, \
  by0*p^2+bv1*bv2*p*q+by2*q^2+kk*r*bv1*q, \
  bt0*p^2+bb*bv2*p*q+bt2*q^2+kk*bb*q*r]~;
bL13=kk*(bx0-bv2^2);
bL23=kk*by0;
bL31=bt0*bv2;
bL33=kk*bt0;
bL=[bl0,bl1,bL13;bl3,bl4,bL23;bL31,bl7,bL33];
bW=weighted(bH4,bH3,bH2,bL);
for(degree=5,8,checkzero(polcoef(bW,degree,zz), \
  Str("branch E",degree)));
bM0=kk*bl0-bv2*bL13;
bM3=kk*bl3-bv2*bL23;
bE4=2*bb*bM3*p^4+(bb*bM0+6*dd*bM3)*p^2*q^2 \
  -3*dd*bM0*q^4;
checkequal(polcoef(bW,4,zz),bE4,"branch E4 collapse");
checkequal(bL*[kk,0,-bv2]~,[bM0,bM3,0]~,"branch kernel vector");
checkequal((bL*[kk,0,bv2]~)[3],2*kk*bt0*bv2, \
  "branch wrong-sign kernel mutation");

\\ Interior eta=0 family, after the complete E6 and E5 solution.
iH4=[(p^2+q^2)*p^2,(p^2+q^2)*q^2,0]~;
iH3=[iu0*p^3+iu1*p^2*q+iu2*p*q^2+kk*r*p^2, \
  iv0*p^3+iu1*p^2*q+iv2*p*q^2+2*iu1*q^3 \
    +kk*r*(p^2+2*q^2), \
  aa*p^3+cc*p*q^2]~;
iH2=[ix0*p^2+iu1*iu2*p*q+ix2*q^2+kk*r*iu2*p, \
  iy0*p^2+iu1*iv2*p*q+(iu1^2+iy2)*q^2 \
    +kk*r*(iv2*p+2*iu1*q)+kk^2*r^2, \
  it0*p^2+cc*iu1*p*q+it2*q^2+kk*cc*p*r]~;
iL13=kk*ix2;
iL23=kk*iy2;
iL32=it2*iu1;
iL33=kk*it2;
iL=[il0,il1,iL13;il3,il4,iL23;il6,iL32,iL33];
iW=weighted(iH4,iH3,iH2,iL);
for(degree=5,8,checkzero(polcoef(iW,degree,zz), \
  Str("interior E",degree)));
iM1=kk*il1-iu1*iL13;
iM4=kk*il4-iu1*iL23;
iE4=(3*aa*iM1+(-3*aa+4*cc)*iM4)*p^4 \
  +((6*aa-cc)*iM1+cc*iM4)*p^2*q^2+2*cc*iM1*q^4;
checkequal(polcoef(iW,4,zz),iE4,"interior E4 collapse");
checkequal(iL*[0,kk,-iu1]~,[iM1,iM4,0]~, \
  "interior kernel vector");
checkequal((iL*[0,kk,iu1]~)[3],2*kk*it2*iu1, \
  "interior wrong-sign kernel mutation");

\\ Independent divisor-rank mutations for b,d,c,a-c.
jac(f,g)=deriv(f,p)*deriv(g,q)-deriv(f,q)*deriv(g,p);
cf(f,i,j)=polcoef(polcoef(f,i,p),j,q);
block(h,R,level)={
  my(P=h*p^2,Q=h*q^2,al=jac(Q,R),be=-jac(P,R),ga=jac(P,Q));
  my(cols,degree);
  if(level==2,
    cols=[al,be]; degree=5,
    if(level==1,
      cols=[al*p,al*q,be*p,be*q,ga]; degree=6,
      cols=[al*p^2,al*p*q,al*q^2,be*p^2,be*p*q,be*q^2,ga*p,ga*q];
      degree=7
    )
  );
  matrix(degree+1,#cols,i,j,cf(cols[j],degree-(i-1),i-1))
};
ranks(h,R)=vector(3,i,matrank(block(h,R,3-i)));
checkequal(ranks(p^2,p^2*q+q^3),[2,5,7],"branch open rank");
checkequal(ranks(p^2,q^3),[2,5,6],"branch b=0 mutation");
checkequal(ranks(p^2,p^2*q),[2,4,5],"branch d=0 mutation");
hi=p^2+q^2;
checkequal(ranks(hi,2*p^3+p*q^2),[2,5,7],"interior open rank");
checkequal(ranks(hi,p^3),[2,5,6],"interior c=0 mutation");
checkequal(ranks(hi,p^3+p*q^2),[2,4,5], \
  "interior a-c=0 mutation");

print("ALL PARI DELTA=1 LOWER EXCLUSION CHECKS PASSED");
quit;
