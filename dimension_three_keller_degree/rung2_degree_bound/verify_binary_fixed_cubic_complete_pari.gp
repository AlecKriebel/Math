\\ Independent PARI/GP reconstruction for the binary fixed-cubic row.

fail(message) = { print(Str("FAIL: ", message)); quit(1); };
check(condition,message) = if(!condition,fail(message));
checkzero(value,message) = check(value == 0,message);

jacmap(V) = matrix(3,3,i,j,deriv(V[i],[p,q,r][j]));
jac2(f,g) = deriv(f,p)*deriv(g,q)-deriv(f,q)*deriv(g,p);

\\ Coefficients of every degree-d monomial in p,q,r, including zeros.
homcoeff(f,d) = {
  my(out=List());
  for(i=0,d,
    for(j=0,d-i,
      my(k=d-i-j);
      listput(out,polcoef(polcoef(polcoef(f,i,p),j,q),k,r))
    )
  );
  Vec(out)
};

substmany(f,V,S) = {
  my(out=f);
  for(i=1,#V,out=subst(out,V[i],S[i]));
  out
};

linear_system(E,U) = {
  my(m=#E,n=#U,A=matrix(#E,#U),b=vector(#E),zero=vector(#U));
  for(i=1,m,
    for(j=1,n,A[i,j]=deriv(E[i],U[j]));
    b[i]=-substmany(E[i],U,zero)
  );
  [A,b~]
};

\\ Exact RREF.  Returns a simultaneous substitution vector; pivot formulas
\\ contain only the original free variables.
rrefsolve(A,b,U) = {
  my(m=matsize(A)[1],n=matsize(A)[2],M=matconcat([A,b]));
  my(row=1,pivots=List());
  for(col=1,n,
    my(pivot=0);
    for(i=row,m,if(M[i,col]!=0,pivot=i;break));
    if(pivot,
      if(pivot!=row,
        for(j=1,n+1,
          my(tmp=M[row,j]); M[row,j]=M[pivot,j]; M[pivot,j]=tmp
        )
      );
      my(scale=M[row,col]);
      for(j=1,n+1,M[row,j]=M[row,j]/scale);
      for(i=1,m,
        if(i!=row && M[i,col]!=0,
          my(mult=M[i,col]);
          for(j=1,n+1,M[i,j]=M[i,j]-mult*M[row,j])
        )
      );
      listput(pivots,col);
      row++;
      if(row>m,break)
    )
  );
  for(i=row,m,
    for(j=1,n,checkzero(M[i,j],"RREF missed a coefficient"));
    checkzero(M[i,n+1],"inconsistent purportedly compatible system")
  );
  my(S=vector(n,j,U[j]));
  for(k=1,#pivots,
    my(col=pivots[k],value=M[k,n+1]);
    for(j=1,n,if(j!=col,value-=M[k,j]*U[j]));
    S[col]=value
  );
  [S,Vec(pivots),M]
};

contains_exact(V,target) = {
  for(i=1,#V,if(V[i]==target,return(1)));
  0
};

cub=[p^3,p^2*q,p*q^2,q^3];
quad=[p^2,p*q,q^2];
allquad=[p^2,p*q,q^2,p*r,q*r,r^2];

\\ Core two-by-two identities.
h=h0*p^3+h1*p^2*q+h2*p*q^2+h3*q^3;
W=w0*p^3+w1*p^2*q+w2*p*q^2+w3*q^3;
D=matrix(2,2,i,j,deriv([p*h,q*h][i],[p,q][j]));
checkzero(matdet(D)-4*h^2,"det D != 4h^2");
expectedadj=4*h*matid(2)-[p,q]~*[deriv(h,p),deriv(h,q)];
checkzero(matadjoint(D)-expectedadj,"adj D identity");
row=[deriv(W,p),deriv(W,q)]*matadjoint(D);
checkzero(row[1]+jac2(q*h,W),"first E7 syzygy coefficient");
checkzero(row[2]-jac2(p*h,W),"second E7 syzygy coefficient");

\\ All local monomial root-order instances.
check_roots() = {
  for(m=1,3,
    for(n=0,3,
      my(hm=p^m*q^(3-m),wm=p^n*q^(3-n));
      my(a=jac2(q*hm,wm),b=jac2(p*hm,wm),c=jac2(p*hm,q*hm));
      my(gcdabc=gcd(gcd(a,b),c),observed=valuation(gcdabc,p));
      check(observed==min(2*m,m+n-1),"local root-order formula")
    )
  )
};
check_roots();

\\ Build and solve a fixed nonzero E7 tangent through E6, then inspect E5.
fixed_e7(name,hc,Wc,N,expected) = {
  my(U=[u0,u1,u2,u3,u4,u5,u6,u7]);
  my(A=[a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14]);
  my(Lv=[l0,l1,l2,l3,l4,l5,l6,l7,l8]);
  my(H3=[
    sum(i=1,4,U[i]*cub[i])+r*N[1],
    sum(i=1,4,U[i+4]*cub[i])+r*N[2],
    Wc
  ]~);
  my(H2=[
    sum(i=1,6,A[i]*allquad[i]),
    sum(i=1,6,A[i+6]*allquad[i]),
    sum(i=1,3,A[i+12]*quad[i])+r*N[3]
  ]~);
  my(L=matrix(3,3,i,j,Lv[3*(i-1)+j]));
  my(H4=[p*hc,q*hc,0]~);
  my(weighted=matdet(L+zz*jacmap(H2)+zz^2*jacmap(H3)+zz^3*jacmap(H4)));
  checkzero(polcoef(weighted,8,zz),Str(name," E8"));
  checkzero(polcoef(weighted,7,zz),Str(name," E7"));
  my(unknowns=concat(concat(U,A),[l8]));
  my(sys=linear_system(homcoeff(polcoef(weighted,6,zz),6),unknowns));
  my(sol=rrefsolve(sys[1],sys[2],unknowns)[1]);
  my(E5=homcoeff(substmany(polcoef(weighted,5,zz),unknowns,sol),5));
  check(contains_exact(E5,expected),Str(name," missing E5 constant ",expected));
  print(Str(name,": E5 constant ",expected))
};

fixed_e7("t3d-E7",p^3,p*q^2,[8*p^2/5,p*q,0]~,24/25);
fixed_e7("d4a-E7",p^2*q,p*q^2,[5*p^2/2,p*q,0]~,15);
fixed_e7("d4b-E7",p^2*q,p^2*q,[-p^2/2,p*q,0]~,3/2);
fixed_e7("t4-E7",p^3,p^2*(p+q),[4*p^2,-p*(3*p-q),0]~,-12);

\\ Build and solve a zero-normal lower syzygy through E5, then inspect E4.
fixed_lower(name,hc,Wc,N,expected) = {
  my(U=[u0,u1,u2,u3,u4,u5,u6,u7]);
  my(A=[a0,a1,a2,a3,a4,a5,a6,a7,a8]);
  my(Lv=[l0,l1,l2,l3,l4,l5,l6,l7]);
  my(H3=[
    sum(i=1,4,U[i]*cub[i]),
    sum(i=1,4,U[i+4]*cub[i]),
    Wc
  ]~);
  my(H2=[
    sum(i=1,3,A[i]*quad[i])+r*N[1],
    sum(i=1,3,A[i+3]*quad[i])+r*N[2],
    sum(i=1,3,A[i+6]*quad[i])
  ]~);
  my(L=[Lv[1],Lv[2],Lv[3];Lv[4],Lv[5],Lv[6];Lv[7],Lv[8],0]);
  my(H4=[p*hc,q*hc,0]~);
  my(weighted=matdet(L+zz*jacmap(H2)+zz^2*jacmap(H3)+zz^3*jacmap(H4)));
  for(degree=6,8,checkzero(polcoef(weighted,degree,zz),Str(name," E",degree)));
  my(unknowns=concat(concat(U,A),[l2,l5]));
  my(sys=linear_system(homcoeff(polcoef(weighted,5,zz),5),unknowns));
  my(sol=rrefsolve(sys[1],sys[2],unknowns)[1]);
  my(E4=homcoeff(substmany(polcoef(weighted,4,zz),unknowns,sol),4));
  check(contains_exact(E4,expected),Str(name," missing E4 constant ",expected));
  print(Str(name,": E4 constant ",expected))
};

fixed_lower("t3d-lower",p^3,p*q^2,[8*p/5,q]~,-24/5);
fixed_lower("d4a-lower",p^2*q,p*q^2,[5*p/2,q]~,-15/2);
fixed_lower("d4b-lower",p^2*q,p^2*q,[-p/2,q]~,3/2);
fixed_lower("t4-lower",p^3,p^2*(p+q),[4*p,-3*p+q]~,-12);

\\ The d4b nonzero-r branch.  Reduction modulo 3*g^2-8*g+8 is
\\ performed by lifting to the exact quadratic quotient.
grel=3*g^2-8*g+8;
redg(x)=lift(Mod(x,grel));
check_d4b_gamma() = {
print("d4b gamma: reconstructing");
ga=Aalpha; gb=Bbeta;
kappa=1-3*g/8;
R1=[-p/2,q,0]~; R2=[2*p,0,1]~;
Ur=vector(3,j,r*(g*R1[j]+R2[j])+(ga*p+gb*q)*(R1[j]+kappa*R2[j]));
GU=[gu0,gu1,gu2,gu3,gu4,gu5,gu6,gu7];
GA=[ga0,ga1,ga2,ga3,ga4,ga5,ga6,ga7,ga8,ga9,ga10,ga11,ga12,ga13,ga14];
GL=[gl0,gl1,gl2,gl3,gl4,gl5,gl6,gl7,gl8];
GH3=[
  sum(i=1,4,GU[i]*cub[i])+intformal(Ur[1],r),
  sum(i=1,4,GU[i+4]*cub[i])+intformal(Ur[2],r),
  p^2*q
]~;
GH2=[
  sum(i=1,6,GA[i]*allquad[i]),
  sum(i=1,6,GA[i+6]*allquad[i]),
  sum(i=1,3,GA[i+12]*quad[i])+intformal(Ur[3],r)
]~;
GLM=matrix(3,3,i,j,GL[3*(i-1)+j]);
GH4=[p^3*q,p^2*q^2,0]~;
GD=matrix(2,2,i,j,deriv(GH4[i],[p,q][j]));
GB=matrix(2,2,i,j,deriv(GH3[i],[p,q][j]));
GAA=matrix(2,2,i,j,deriv(GH2[i],[p,q][j]));
Gw=[deriv(GH3[3],p),deriv(GH3[3],q)];
Gur=[deriv(GH3[1],r),deriv(GH3[2],r)]~;
Gar=[deriv(GH2[1],r),deriv(GH2[2],r)]~;
Gt=[deriv(GH2[3],p),deriv(GH2[3],q)];
Gtau=deriv(GH2[3],r);
GE6raw=matdet(GD)*gl8+trace(matadjoint(GB)*GD)*Gtau-Gw*matadjoint(GD)*Gar-Gw*matadjoint(GB)*Gur-Gt*matadjoint(GD)*Gur;
GE5raw=trace(matadjoint(GB)*GD)*gl8+(trace(matadjoint(GAA)*GD)+matdet(GB))*Gtau-Gw*matadjoint(GD)*[gl2,gl5]~-Gw*matadjoint(GB)*Gar-Gw*matadjoint(GAA)*Gur-Gt*matadjoint(GD)*Gar-Gt*matadjoint(GB)*Gur-[gl6,gl7]*matadjoint(GD)*Gur;
Gvars=[gu0,gu1,gu2,gu3,gu4,ga3,ga4,ga9];
Gvals=[
  (6*ga11*g-4*ga11+16*ga12-3*gu5*g+2*gu5)/12,
  (4*ga13*g+8*ga5-3*gu6*g+2*gu6)/4,
  (8*ga14-3*gu7)*(g+2)/12,
  0,
  0,
  -(6*ga*ga5*g-16*ga*ga5+3*gb*ga11*g-8*gb*ga11+4*ga10-16*gl8)/8,
  -gb*ga5*(3*g-8)/4,
  -ga*ga11*(3*g-8)/4
];
GE6=homcoeff(substmany(GE6raw,Gvars,Gvals),6);
for(i=1,#GE6,checkzero(redg(GE6[i]),"d4b gamma E6 parameterization"));
GE5=homcoeff(substmany(GE5raw,Gvars,Gvals),5);
GE5=vector(#GE5,i,redg(GE5[i]));
check(contains_exact(GE5,redg((g+2)/6)),"d4b gamma missing E5 constant");
check(redg(g+2)!=0,"d4b gamma constant accidentally zero");
print("d4b gamma: E5 constant (g+2)/6");
};
check_d4b_gamma();

\\ The t4 nonzero-r branch.  These substitutions are a simultaneous exact
\\ row reduction of E6, E5, and the three displayed E4 pivots.
check_t4_gamma() = {
ta=Talpha; tb=Tbeta;
TR=[0,p,1]~;
TN1=[4*p^2,-p*(3*p-q),0]~;
TN3=[0,p^2,p]~;
TN4=[-4*p^2,3*p^2,q]~;
TUr=vector(3,j,r*TR[j]+ta*TN1[j]+tb*TN3[j]+ta*TN4[j]);
TU=[tu0,tu1,tu2,tu3,tu4,tu5,tu6,tu7];
TA=[ta0,ta1,ta2,ta3,ta4,ta5,ta6,ta7,ta8,ta9,ta10,ta11,ta12,ta13,ta14];
TL=[tl0,tl1,tl2,tl3,tl4,tl5,tl6,tl7,tl8];
TH3=[
  sum(i=1,4,TU[i]*cub[i])+intformal(TUr[1],r),
  sum(i=1,4,TU[i+4]*cub[i])+intformal(TUr[2],r),
  p^2*(p+q)
]~;
TH2=[
  sum(i=1,6,TA[i]*allquad[i]),
  sum(i=1,6,TA[i+6]*allquad[i]),
  sum(i=1,3,TA[i+12]*quad[i])+intformal(TUr[3],r)
]~;
TLM=matrix(3,3,i,j,TL[3*(i-1)+j]);
TH4=[p^4,p^3*q,0]~;
Tweighted=matdet(TLM+zz*jacmap(TH2)+zz^2*jacmap(TH3)+zz^3*jacmap(TH4));
T6vars=[tu1,tu2,tu3,tu5,ta3,ta4,ta9];
T6vals=[
  2*(-4*ta14+ta5+4*tu6+18*tu7),
  6*tu7,
  0,
  2*ta11+ta13+6*ta14-6*tu6-27*tu7,
  -2*(4*ta*ta11-tb*ta5-2*ta10),
  2*ta*ta5,
  6*ta*ta11+2*tb*ta11-3*ta10+tl8
];
TE6=homcoeff(substmany(polcoef(Tweighted,6,zz),T6vars,T6vals),6);
for(i=1,#TE6,checkzero(TE6[i],"t4 gamma E6 parameterization"));
T5vars=[tu7,ta14,ta10,ta2,tl5,tl2,ta1,ta7];
T5vals=[
  0,
  tu6,
  2*ta*ta11,
  2*ta5*tu6,
  2*ta11*tl8,
  2*ta5*tl8,
  -16*ta11*tu6+2*ta13*ta5+8*ta8,
  tl7-3*(-16*ta11*tu6+2*ta13*ta5+8*ta8)/4+2*ta11*ta13+3*ta13*ta5/2
];
TE5=homcoeff(substmany(substmany(polcoef(Tweighted,5,zz),T6vars,T6vals),T5vars,T5vals),5);
for(i=1,#TE5,checkzero(TE5[i],"t4 gamma E5 parameterization"));
T4vars=concat(concat(T6vars,T5vars),[ta8,tl1,tl4]);
T4vals=concat(concat(T6vals,T5vals),[2*ta11*tu6,2*ta5*tl7,2*ta11*tl7]);
TE4=homcoeff(substmany(polcoef(Tweighted,4,zz),T4vars,T4vals),4);
for(i=1,#TE4,checkzero(TE4[i],"t4 gamma E4 parameterization"));
checkzero(substmany(matdet(TLM),T4vars,T4vals),"t4 gamma det L");
print("t4 gamma: E4 forces proportional columns and det L=0");
};
check_t4_gamma();

print("ALL BINARY FIXED-CUBIC PARI/GP CERTIFICATES PASSED");
quit;
