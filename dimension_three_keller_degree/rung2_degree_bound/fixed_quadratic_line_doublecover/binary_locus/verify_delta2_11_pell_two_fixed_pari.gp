\\ Independent PARI/GP replay of h=p(p+q), R=p(p+q)(Ap+Bq).

p='p; q='q; r='r; z='z;
vars=[p,q,r];
jacmat(H)=matrix(3,3,i,j,deriv(H[i],vars[j]));
jac2(f,g)=deriv(f,p)*deriv(g,q)-deriv(f,q)*deriv(g,p);
check_zero(value,message)={if(value!=0,error(Str("FAIL: ",message,"; residual = ",value)))};
hc(f,degree,index)=polcoeff(subst(f,q,1),degree-index,p);
cv(f,degree)=vector(degree+1,index,hc(f,degree,index-1));

AA='AA; BB='BB; ss='ss; tt='tt; x5='x5; y5='y5;
ell=p+q;
P=p^3*ell; Q=p*ell*q^2; R=p*ell*(AA*p+BB*q);
alpha=jac2(Q,R); beta=-jac2(P,R); gam=jac2(P,Q);
check_zero(gcd(gcd(alpha,beta),gam)-p*ell,"generic gcd");
gB0=gcd(gcd(substvec(alpha,[AA,BB],[1,0]),substvec(beta,[AA,BB],[1,0])),gam);
gAB=gcd(gcd(substvec(alpha,[AA,BB],[1,1]),substvec(beta,[AA,BB],[1,1])),gam);
gA4=gcd(gcd(substvec(alpha,[AA,BB],[-4,1]),substvec(beta,[AA,BB],[-4,1])),gam);
check_zero(gB0^2-(p^2*ell)^2,"B=0 deeper gcd");
check_zero(gAB^2-(p*ell^2)^2,"A=B deeper gcd");
check_zero(gA4^2-(p*q*ell)^2,"A=-4B deeper gcd");

u0='u0; u1='u1; u2='u2; v0='v0; v1='v1; v2='v2; t0='t0; t1='t1;
unknown7=[u0,u1,u2,v0,v1,v2,t0,t1];
uform=u0*p^2+u1*p*q+u2*q^2;
vform=v0*p^2+v1*p*q+v2*q^2;
tform=t0*p+t1*q;
E7=alpha*uform+beta*vform+gam*tform;
M7=matrix(8,8,i,j,polcoeff(hc(E7,7,i-1),1,unknown7[j]));
check_zero(matdet(vecextract(M7,[1,2,3,4,5,6],[1,2,3,4,5,6]))-24*BB^3*(AA-BB)^2*(AA+4*BB),"E7 rank minor");
check_zero(matrank(substvec(M7,[AA,BB],[1,0]))-5,"B=0 fresh E7 rank");
check_zero(matrank(substvec(M7,[AA,BB],[1,1]))-5,"A=B fresh E7 rank");
check_zero(matrank(substvec(M7,[AA,BB],[-4,1]))-5,"A=-4B fresh E7 rank");

N1=[5*BB*p^2,-BB*q*(6*p+q),3*BB*p*(AA-BB)];
N2=[-(AA+4*BB)*p^2,q*(6*AA*p+5*AA*q-4*BB*q),3*BB*q*(AA-BB)];
for(index=1,2,{
  Ncheck=if(index==1,N1,N2);
  check_zero(alpha*Ncheck[1]+beta*Ncheck[2]+gam*Ncheck[3],Str("E7 tangent ",index))
});
print("PASS PARI exact boundaries and complete E7 basis");

N=vector(3,index,ss*N1[index]+tt*N2[index]);
H4=[P,Q,0]~;
H3=[r*N[1],r*N[2],R]~;
H2=[x5*r^2,y5*r^2,r*N[3]]~;
D=matdet(z*jacmat(H2)+z^2*jacmat(H3)+z^3*jacmat(H4));
check_zero(polcoeff(D,7,z),"E7 determinant");
E6r=polcoeff(polcoeff(D,6,z),1,r);
colX=cv(substvec(E6r,[ss,tt,x5,y5],[1,0,0,0]),5);
colZ=cv(substvec(E6r,[ss,tt,x5,y5],[0,1,0,0]),5);
colY=cv(substvec(E6r,[ss,tt,x5,y5],[1,1,0,0]),5)-colX-colZ;
colx=cv(substvec(E6r,[ss,tt,x5,y5],[0,0,1,0]),5);
coly=cv(substvec(E6r,[ss,tt,x5,y5],[0,0,0,1]),5);
M=matrix(6,5,i,j,[colX,colY,colZ,colx,coly][j][i]);
K=[-(5*AA^2+4*AA*BB-4*BB^2),-BB*(7*AA-2*BB),-5*BB^2,0,36*BB^2*(AA-BB)^2]~;
check_zero(M*K,"contact kernel");
check_zero(matdet(vecextract(M,[1,2,3,4],[1,2,3,4]))+41472*BB^5*(AA-BB)^4*(AA+4*BB),"contact rank minor");
check_zero(K[2]^2-K[1]*K[3]-24*BB^2*(AA-BB)^2,"Veronese obstruction");
print("PASS PARI rank-four contact kernel misses Veronese");

a0='a0; a1='a1; b0='b0; b1='b1; l33='l33;
E6c=alpha*(a0*p+a1*q)+beta*(b0*p+b1*q)+gam*l33;
unknown=[a0,a1,b0,b1,l33];
Mc=matrix(7,5,i,j,polcoeff(hc(E6c,6,i-1),1,unknown[j]));
check_zero(matdet(vecextract(Mc,[2,3,4,5,6],[1,2,3,4,5]))-8*BB^2*(AA-BB)*(AA+4*BB),"constant E6 determinant");
print("PASS PARI constant E6 full rank and all-binary exit");
print("ALL PARI PELL TWO-FIXED {1,1} CHECKS PASSED");
