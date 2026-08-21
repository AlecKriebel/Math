\\ Independent PARI/GP replay of the h=p^2 q-contact {1,1} exclusion.

p='p; q='q; r='r; z='z;
vars=[p,q,r];
jacmat(H)=matrix(3,3,i,j,deriv(H[i],vars[j]));
jac2(f,g)=deriv(f,p)*deriv(g,q)-deriv(f,q)*deriv(g,p);
check_zero(value,message)={if(value!=0,error(Str("FAIL: ",message,"; residual = ",value)))};
hc(f,degree,index)=polcoeff(subst(f,q,1),degree-index,p);
cv(f,degree)=vector(degree+1,index,hc(f,degree,index-1));

AA='AA; CC='CC; DD='DD; ss='ss; ttan='ttan;
x5='x5; y5='y5;
P=p^4; Q=p^2*q^2; H4=[P,Q,0]~;

contactmat(RR,N1,N2)={
  my(N,H3c,H2c,Dc,E6rc,colX,colY,colZ,colx,coly);
  N=vector(3,index,ss*N1[index]+ttan*N2[index]);
  H3c=[r*N[1],r*N[2],RR]~;
  H2c=[x5*r^2,y5*r^2,r*N[3]]~;
  Dc=matdet(z*jacmat(H2c)+z^2*jacmat(H3c)+z^3*jacmat(H4));
  check_zero(polcoeff(Dc,7,z),"contact E7 determinant");
  E6rc=polcoeff(polcoeff(Dc,6,z),1,r);
  colX=cv(substvec(E6rc,[ss,ttan,x5,y5],[1,0,0,0]),5);
  colZ=cv(substvec(E6rc,[ss,ttan,x5,y5],[0,1,0,0]),5);
  colY=cv(substvec(E6rc,[ss,ttan,x5,y5],[1,1,0,0]),5)-colX-colZ;
  colx=cv(substvec(E6rc,[ss,ttan,x5,y5],[0,0,1,0]),5);
  coly=cv(substvec(E6rc,[ss,ttan,x5,y5],[0,0,0,1]),5);
  matrix(6,5,i,j,[colX,colY,colZ,colx,coly][j][i])
};

R=AA*p^3+CC*p*q^2+DD*q^3;
alpha=jac2(Q,R); beta=-jac2(P,R); gam=jac2(P,Q);
check_zero(gcd(gcd(alpha,beta),gam)-2*p*q,"generic gcd");
check_zero(gcd(gcd(subst(alpha,DD,0),subst(beta,DD,0)),gam)-2*p^2*q,"D=0 deeper gcd");
Lambda=27*AA*DD^2+4*CC^3;
N1=[36*DD^2*p^2,4*CC^2*p^2-6*CC*DD*p*q+18*DD^2*q^2,Lambda*p];
N2=[-24*CC*DD*p^2,18*AA*DD*p^2+4*CC^2*p*q-12*CC*DD*q^2,Lambda*q];
for(index=1,2,{
  Ncheck=if(index==1,N1,N2);
  check_zero(alpha*Ncheck[1]+beta*Ncheck[2]+gam*Ncheck[3],Str("general tangent ",index))
});
M=contactmat(R,N1,N2);
check_zero(matdet(vecextract(M,[1,2,3,4,5],[1,2,3,4,5]))+71663616*CC^2*DD^6*Lambda^3,"generic contact minor");

\\ Lambda=0, recomputed without division by Lambda.
Alambda=-4*CC^3/(27*DD^2);
Rlambda=subst(R,AA,Alambda);
N1lambda=[2*p^2,2*CC^2*p^2/(9*DD^2)-CC*p*q/(3*DD)+q^2,0];
N2lambda=[0,2*p^2/(3*DD),2*CC*p/(3*DD)+q];
Mlambda=contactmat(Rlambda,N1lambda,N2lambda);
check_zero(matdet(vecextract(Mlambda,[1,2,3,4,5],[1,2,3,4,5]))+12288*CC^2,"Lambda=0 contact minor");
print("PASS PARI generic and Lambda=0 injective contact charts");

\\ C=0, A*D != 0: rank-four kernel misses the Veronese.
Rc0=AA*p^3+DD*q^3;
N1c0=[4*p^2/(3*AA),2*q^2/(3*AA),p];
N2c0=[0,2*p^2/(3*DD),q];
Mc0=contactmat(Rc0,N1c0,N2c0);
Kc0=[0,9*AA*DD/4,0,0,1]~;
check_zero(Mc0*Kc0,"C=0 contact kernel");
check_zero(matdet(vecextract(Mc0,[1,2,3,5],[1,2,3,4]))-8192/(9*AA^2),"C=0 rank minor");
check_zero(Kc0[2]^2-Kc0[1]*Kc0[3]-81*AA^2*DD^2/16,"C=0 Veronese obstruction");

\\ A=C=0: one and only one contact line survives E6.
Rend=DD*q^3;
N1end=[2*p^2,q^2,0];
N2end=[0,2*p^2/(3*DD),q];
Mend=contactmat(Rend,N1end,N2end);
K1=[1,0,0,1,0]~;
K2=[0,3*DD/2,0,0,1]~;
check_zero(Mend*K1,"endpoint first kernel");
check_zero(Mend*K2,"endpoint second kernel");
check_zero(matdet(vecextract(Mend,[1,3,5],[1,2,3]))+512,"endpoint rank minor");
print("PASS PARI C=0 Veronese split and unique endpoint survivor");

\\ Full lower solve on R=D*q^3.
kk='kk;
u0='u0; u1='u1; u2='u2; u3='u3;
v0='v0; v1='v1; v2='v2; v3='v3;
t0='t0; t1='t1; t2='t2;
x0='x0; x1='x1; x2='x2; x3='x3; x4='x4;
y0='y0; y1='y1; y2='y2; y3='y3; y4='y4;
l0='l0; l1='l1; l2='l2; l3='l3; l4='l4;
l5='l5; l6='l6; l7='l7; l8='l8;
U0=u0*p^3+u1*p^2*q+u2*p*q^2+u3*q^3;
V0=v0*p^3+v1*p^2*q+v2*p*q^2+v3*q^3;
T0=t0*p^2+t1*p*q+t2*q^2;
A0=x0*p^2+x1*p*q+x2*q^2;
B0=y0*p^2+y1*p*q+y2*q^2;
H3=[U0+2*kk*r*p^2,V0+kk*r*q^2,DD*q^3]~;
H2=[A0+r*(x3*p+x4*q)+kk^2*r^2,B0+r*(y3*p+y4*q),T0]~;
L0=[l0,l1,l2;l3,l4,l5;l6,l7,l8];
Dfull=matdet(L0+z*jacmat(H2)+z^2*jacmat(H3)+z^3*jacmat(H4));
E8=polcoeff(Dfull,8,z); E7=polcoeff(Dfull,7,z);
E6=polcoeff(Dfull,6,z); E5=polcoeff(Dfull,5,z); E4=polcoeff(Dfull,4,z);
check_zero(E8,"full E8");
check_zero(E7,"full E7");
check_zero(polcoeff(E6,1,r),"full E6 r");
x3s=kk*(3*u0/2-v2);
x4s=kk*u1;
y3s=kk*(-t1/(3*DD)+3*v0/2);
y4s=kk*v1;
l8s=kk*t0;
vars6=[x3,x4,y3,y4,l8,u2];
vals6=[x3s,x4s,y3s,y4s,l8s,0];
check_zero(substvec(E6,vars6,vals6),"complete E6 solve");
E6c=polcoeff(E6,0,r);
unknown6=[x3,x4,y3,y4,l8,t0,t1,t2,u0,u1,u2,u3,v0,v1,v2,v3];
M6=matrix(7,16,i,j,polcoeff(hc(E6c,6,i-1),1,unknown6[j]));
check_zero(matdet(vecextract(M6,[2,3,4,5,6,7],[1,2,3,4,5,11]))+124416*DD^5*kk,"E6 rank minor");

E5done=substvec(E5,vars6,vals6);
expectedr=-3*kk^2*q^2*(-6*DD*p^2*v0+3*DD*q^2*u0-6*DD*q^2*v2+4*p^2*t1)/2;
check_zero(polcoeff(E5done,1,r)-expectedr,"E5 r coefficient");
E5high=substvec(polcoeff(E5done,0,r),[t1,u0],[3*DD*v0/2,2*v2]);
check_zero(hc(E5high,5,0)-3*DD*kk*v0^2,"E5 compatibility");
unknown5=[x1,y1,l2,l5,l6];
M5=matrix(6,5,i,j,polcoeff(hc(E5high,5,i-1),1,unknown5[j]));
check_zero(matdet(vecextract(M5,[2,3,4,5,6],[1,2,3,4,5]))-5184*DD^4*kk^3,"E5 rank minor");

vars5=[t1,u0,v0,x1,y1,l2,l5,l6];
vals5=[0,2*v2,0,u1*v2,v1*v2,kk*(x0-v2^2),kk*y0,t0*v2];
E5complete=substvec(E5done,vars5,vals5);
check_zero(E5complete,"complete E5 solve");
E4complete=substvec(substvec(E4,vars6,vals6),vars5,vals5);
M0=kk*l0-v2*kk*(x0-v2^2);
M3=kk*l3-v2*kk*y0;
expected4=DD*(6*M3*p^2*q^2-3*M0*q^4);
check_zero(E4complete-expected4,"E4 kernel form");
Ldone=substvec(substvec(L0,vars6,vals6),vars5,vals5);
check_zero(Ldone*[kk,0,-v2]~-[M0,M3,0]~,"linear-part kernel");
print("PASS PARI full endpoint E6/E5 solve and E4 kernel");
print("ALL PARI P2 BRANCH-CONTACT {1,1} CHECKS PASSED");
