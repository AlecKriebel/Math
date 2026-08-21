\\ Independent PARI/GP replay of h=pq, R=pq(Ap+Bq).

p='p; q='q; r='r; z='z;
vars=[p,q,r];
jacmat(H)=matrix(3,3,i,j,deriv(H[i],vars[j]));
jac2(f,g)=deriv(f,p)*deriv(g,q)-deriv(f,q)*deriv(g,p);
check_zero(value,message)={if(value!=0,error(Str("FAIL: ",message,"; residual = ",value)))};
hc(f,degree,index)=polcoeff(subst(f,q,1),degree-index,p);
cv(f,degree)=vector(degree+1,index,hc(f,degree,index-1));

AA='AA; BB='BB; ss='ss; tt='tt; x5='x5; y5='y5;
P=p^3*q; Q=p*q^3; R=p*q*(AA*p+BB*q);
alpha=jac2(Q,R); beta=-jac2(P,R); gam=jac2(P,Q);
check_zero(gcd(gcd(alpha,beta),gam)-p*q,"generic gcd");
check_zero(gcd(gcd(subst(alpha,AA,0),subst(beta,AA,0)),gam)-p*q^2,"A=0 deeper gcd");
check_zero(gcd(gcd(subst(alpha,BB,0),subst(beta,BB,0)),gam)-p^2*q,"B=0 deeper gcd");
N1=[5*p^2,-q^2,3*AA*p];
N2=[-p^2,5*q^2,3*BB*q];
for(index=1,2,{
  Ncheck=if(index==1,N1,N2);
  check_zero(alpha*Ncheck[1]+beta*Ncheck[2]+gam*Ncheck[3],Str("E7 tangent ",index))
});
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
K=[1,7/5,1,0,0]~;
check_zero(M*K,"contact kernel");
check_zero(matdet(vecextract(M,[2,3,4,5],[1,2,4,5]))-5760*AA^2*BB^2,"contact rank minor");
check_zero(K[2]^2-K[1]*K[3]-24/25,"Veronese obstruction");
print("PASS PARI rank-four contact kernel misses Veronese");

a0='a0; a1='a1; b0='b0; b1='b1; l33='l33;
E6c=alpha*(a0*p+a1*q)+beta*(b0*p+b1*q)+gam*l33;
unknown=[a0,a1,b0,b1,l33];
Mc=matrix(7,5,i,j,polcoeff(hc(E6c,6,i-1),1,unknown[j]));
check_zero(matdet(vecextract(Mc,[2,3,4,5,6],[1,2,3,4,5]))-8*AA^2*BB^2,"constant E6 determinant");
print("PASS PARI constant E6 full rank and all-binary exit");
print("ALL PARI PQ TWO-SIMPLE {1,1} CHECKS PASSED");
