\\ Independent PARI/GP replay of the doubled-nonbranch simple-fixed leaf.

p='p; q='q; r='r; z='z;
vars=[p,q,r];
jacmat(H)=matrix(3,3,i,j,deriv(H[i],vars[j]));
jac2(f,g)=deriv(f,p)*deriv(g,q)-deriv(f,q)*deriv(g,p);
check_zero(value,message)={if(value!=0,error(Str("FAIL: ",message,"; residual = ",value)))};
hc(f,degree,index)=polcoeff(subst(f,q,1),degree-index,p);
cv(f,degree)=vector(degree+1,index,hc(f,degree,index-1));

contact_column_case(Pc,Qc,Rc,Nc,xvalue,yvalue)={
  my(H4c,H3c,H2c,Dc,E6rc);
  H4c=[Pc,Qc,0]~;
  H3c=[r*Nc[1],r*Nc[2],Rc]~;
  H2c=[xvalue*r^2,yvalue*r^2,r*Nc[3]]~;
  Dc=matdet(z*jacmat(H2c)+z^2*jacmat(H3c)+z^3*jacmat(H4c));
  check_zero(polcoeff(Dc,7,z),"E7 determinant");
  E6rc=polcoeff(polcoeff(Dc,6,z),1,r);
  cv(E6rc,5)
};

contact_matrix_case(Pc,Qc,Rc,Nfirst,Nsecond)={
  my(zeroN,colX,colY,colZ,colx,coly);
  zeroN=[0,0,0];
  colX=contact_column_case(Pc,Qc,Rc,Nfirst,0,0);
  colZ=contact_column_case(Pc,Qc,Rc,Nsecond,0,0);
  colY=contact_column_case(Pc,Qc,Rc,Nfirst+Nsecond,0,0)-colX-colZ;
  colx=contact_column_case(Pc,Qc,Rc,zeroN,1,0);
  coly=contact_column_case(Pc,Qc,Rc,zeroN,0,1);
  matrix(6,5,i,j,[colX,colY,colZ,colx,coly][j][i])
};

A='A; B='B; C='C;
h=(p+q)^2;
P=h*p^2; Q=h*q^2;
R=(p+q)*(A*p^2+B*p*q+C*q^2);
alpha=jac2(Q,R); beta=-jac2(P,R); gam=jac2(P,Q);
check_zero(gcd(gcd(alpha,beta),gam)^2-4*h^2,"generic gcd");

e1=A-2*B; e2=2*B-C; e3=A-B+C;
g1=gcd(gcd(subst(alpha,A,2*B),subst(beta,A,2*B)),gam);
g2=gcd(gcd(subst(alpha,C,2*B),subst(beta,C,2*B)),gam);
g3=gcd(gcd(subst(alpha,A,B-C),subst(beta,A,B-C)),gam);
check_zero(g1^2-4*q^2*h^2,"A=2B boundary gcd");
check_zero(g2^2-4*p^2*h^2,"C=2B boundary gcd");
check_zero(g3^2-4*(p+q)^6,"A-B+C boundary gcd");
check_zero(substvec(R,[p,q,A,C],[q,p,C,A])-R,"residual stabilizer");
print("PASS PARI exact-open gcd mutations and residual stabilizer");

Delta=4*A*C-B^2;
N1=[-2*(B-8*C)*p^2+12*C*p*q,-6*B*p*q-4*(2*B-C)*q^2,3*Delta*p];
N2=[4*(A-2*B)*p^2-6*B*p*q,12*A*p*q+2*(8*A-B)*q^2,3*Delta*q];
for(index=1,2,check_zero(alpha*[N1,N2][index][1]+beta*[N1,N2][index][2]+gam*[N1,N2][index][3],Str("generic tangent ",index)));
mons=[p^2,p*q,q^2,p^2,p*q,q^2,p,q];
columns=vector(8,index,if(index<=3,alpha*mons[index],if(index<=6,beta*mons[index],gam*mons[index])));
M7=matrix(8,8,i,j,hc(columns[j],7,i-1));
check_zero(matdet(vecextract(M7,[1,2,3,4,5,6],[1,2,3,4,5,6]))+768*e1*e2*Delta*e3^2,"generic E7 rank minor");
Mc=contact_matrix_case(P,Q,R,N1,N2);
expected=26542080*e1*e2*Delta^3*e3^3;
check_zero(matdet(vecextract(Mc,[1,2,3,4,5],[1,2,3,4,5]))-expected,"generic contact determinant");
print("PASS PARI generic Delta-nonzero contact determinant");

Ad=B^2/(4*C);
Rd=subst(R,A,Ad);
alphad=subst(alpha,A,Ad); betad=subst(beta,A,Ad);
N1d=[(B-8*C)*p^2-6*C*p*q,3*B*p*q+2*(2*B-C)*q^2,0];
N2d=[10*C*p^2+8*C*p*q,-2*C*p*q,(2*B-C)*(B*p+2*C*q)];
for(index=1,2,check_zero(alphad*[N1d,N2d][index][1]+betad*[N1d,N2d][index][2]+gam*[N1d,N2d][index][3],Str("Delta=0 tangent ",index)));
M7d=subst(M7,A,Ad);
check_zero(matdet(vecextract(M7d,[1,2,3,4,5,6],[1,2,3,4,5,7]))+16*B*(B-8*C)*(B-2*C)^4*(2*B-C)^2/C^3,"Delta=0 E7 rank minor");
Mcd=contact_matrix_case(P,Q,Rd,N1d,N2d);
expectedd=-3840*B*(B-8*C)*(B-2*C)^6*(2*B-C)^4/C;
check_zero(matdet(vecextract(Mcd,[1,2,3,4,5],[1,2,3,4,5]))-expectedd,"Delta=0 contact determinant");
check_zero(subst(e1,A,Ad)-B*(B-8*C)/(4*C),"Delta=0 e1");
check_zero(subst(e3,A,Ad)-(B-2*C)^2/(4*C),"Delta=0 e3");
print("PASS PARI fresh Delta-zero contact determinant and exact-open cover");

constcols=[alpha*p,alpha*q,beta*p,beta*q,gam];
Mconstant=matrix(7,5,i,j,hc(constcols[j],6,i-1));
check_zero(matdet(vecextract(Mconstant,[1,2,3,4,5],[1,2,3,4,5]))+512*e1*e2*e3^2,"constant E6 determinant");
print("PASS PARI uniform constant E6 determinant and all-binary exit");
print("ALL PARI DOUBLED-NONBRANCH SIMPLE-FIXED {1,1} CHECKS PASSED");
