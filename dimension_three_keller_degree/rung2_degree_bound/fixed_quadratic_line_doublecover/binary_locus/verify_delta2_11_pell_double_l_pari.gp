\\ Independent PARI/GP replay of h=p(p+q), R=(p+q)^2(Ap+Bq).

p='p; q='q; r='r; z='z;
vars=[p,q,r];
jacmat(H)=matrix(3,3,i,j,deriv(H[i],vars[j]));
jac2(f,g)=deriv(f,p)*deriv(g,q)-deriv(f,q)*deriv(g,p);
check_zero(value,message)={if(value!=0,error(Str("FAIL: ",message,"; residual = ",value)))};
hc(f,degree,index)=polcoeff(subst(f,q,1),degree-index,p);
cv(f,degree)=vector(degree+1,index,hc(f,degree,index-1));

AA='AA; BB='BB; ss='ss; tt='tt; x5='x5; y5='y5;
ell=p+q; h=p*ell; P=h*p^2; Q=h*q^2; R=ell^2*(AA*p+BB*q);
alpha=jac2(Q,R); beta=-jac2(P,R); gam=jac2(P,Q);
check_zero(gcd(gcd(alpha,beta),gam)-ell^2,"generic gcd");
check_zero(gcd(gcd(subst(alpha,BB,0),subst(beta,BB,0)),gam)+p*ell^2,"B=0 gcd");
check_zero(5*gcd(gcd(subst(alpha,AA,-4*BB/5),subst(beta,AA,-4*BB/5)),gam)-q*ell^2,"5A+4B gcd");
check_zero(gcd(gcd(subst(alpha,AA,BB),subst(beta,AA,BB)),gam)-ell^2,"A=B stays exact");

N1=[-27*BB*p^2,q*(8*AA*p+10*BB*p-9*BB*q),5*p*(AA-BB)^2];
N2=[3*p^2*(5*AA+4*BB),-q*(18*AA*p-5*AA*q-4*BB*q),5*q*(AA-BB)^2];
for(index=1,2,{
  Ncheck=if(index==1,N1,N2);
  check_zero(alpha*Ncheck[1]+beta*Ncheck[2]+gam*Ncheck[3],Str("generic tangent ",index))
});
N=vector(3,index,ss*N1[index]+tt*N2[index]);
H4=[P,Q,0]~;
H3=[r*N[1],r*N[2],R]~;
H2=[x5*r^2,y5*r^2,r*N[3]]~;
Dtop=matdet(z*jacmat(H2)+z^2*jacmat(H3)+z^3*jacmat(H4));
check_zero(polcoeff(Dtop,7,z),"generic E7");
E6r=polcoeff(polcoeff(Dtop,6,z),1,r);
colX=cv(substvec(E6r,[ss,tt,x5,y5],[1,0,0,0]),5);
colZ=cv(substvec(E6r,[ss,tt,x5,y5],[0,1,0,0]),5);
colY=cv(substvec(E6r,[ss,tt,x5,y5],[1,1,0,0]),5)-colX-colZ;
colx=cv(substvec(E6r,[ss,tt,x5,y5],[0,0,1,0]),5);
coly=cv(substvec(E6r,[ss,tt,x5,y5],[0,0,0,1]),5);
M=matrix(6,5,i,j,[colX,colY,colZ,colx,coly][j][i]);
minor0=matdet(vecextract(M,[2,3,4,5,6],[1,2,3,4,5]));
minor1=matdet(vecextract(M,[1,3,4,5,6],[1,2,3,4,5]));
check_zero(minor0+466560000*BB^3*(AA-BB)^6*(5*AA^2+26*AA*BB+23*BB^2),"first contact minor");
check_zero(minor1+311040000*BB^3*(AA-BB)^6*(2*AA+7*BB)*(5*AA+4*BB),"second contact minor");
check_zero(subst(5*AA^2+26*AA*BB+23*BB^2,AA,-7*BB/2)+27*BB^2/4,"two-minor cover");

\\ Fresh A=B=1 tangent chart.
Req=ell^3;
N1eq=[3*p^2,-q*(2*p-q),0];
N2eq=[0,8*p*q/9,ell];
Neq=vector(3,index,ss*N1eq[index]+tt*N2eq[index]);
H3eq=[r*Neq[1],r*Neq[2],Req]~;
H2eq=[x5*r^2,y5*r^2,r*Neq[3]]~;
Deq=matdet(z*jacmat(H2eq)+z^2*jacmat(H3eq)+z^3*jacmat(H4));
check_zero(polcoeff(Deq,7,z),"A=B E7");
E6eq=polcoeff(polcoeff(Deq,6,z),1,r);
cX=cv(substvec(E6eq,[ss,tt,x5,y5],[1,0,0,0]),5);
cZ=cv(substvec(E6eq,[ss,tt,x5,y5],[0,1,0,0]),5);
cY=cv(substvec(E6eq,[ss,tt,x5,y5],[1,1,0,0]),5)-cX-cZ;
cx=cv(substvec(E6eq,[ss,tt,x5,y5],[0,0,1,0]),5);
cy=cv(substvec(E6eq,[ss,tt,x5,y5],[0,0,0,1]),5);
Meq=matrix(6,5,i,j,[cX,cY,cZ,cx,cy][j][i]);
check_zero(matdet(vecextract(Meq,[2,3,4,5,6],[1,2,3,4,5]))-276480,"A=B contact determinant");
print("PASS PARI two-minor contact cover and A=B pivot chart");

a0='a0; a1='a1; b0='b0; b1='b1; l33='l33;
E6c=alpha*(a0*p+a1*q)+beta*(b0*p+b1*q)+gam*l33;
unknown=[a0,a1,b0,b1,l33];
Mc=matrix(7,5,i,j,polcoeff(hc(E6c,6,i-1),1,unknown[j]));
check_zero(matdet(vecextract(Mc,[1,2,3,4,5],[1,2,3,4,5]))+648*BB^3*(5*AA+4*BB),"constant E6 determinant");
print("PASS PARI exact boundaries, constant rank, and all-binary exit");
print("ALL PARI PELL DOUBLED-L {1,1} CHECKS PASSED");
