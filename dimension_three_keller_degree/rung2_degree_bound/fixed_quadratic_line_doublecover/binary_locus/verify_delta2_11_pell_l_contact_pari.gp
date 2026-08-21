\\ Independent PARI/GP replay of the fixed-(p+q) plus contact leaf.

p='p; q='q; r='r; z='z;
vars=[p,q,r];
jacmat(H)=matrix(3,3,i,j,deriv(H[i],vars[j]));
jac2(f,g)=deriv(f,p)*deriv(g,q)-deriv(f,q)*deriv(g,p);
check_zero(value,message)={if(value!=0,error(Str("FAIL: ",message,"; residual = ",value)))};
hc(f,degree,index)=polcoeff(subst(f,q,1),degree-index,p);
cv(f,degree)=vector(degree+1,index,hc(f,degree,index-1));
contact_matrix(Rc,Nfirst,Nsecond)={
  my(Nc,H3c,H2c,Dc,E6rc,colX,colY,colZ,colx,coly);
  Nc=vector(3,index,ss*Nfirst[index]+tt*Nsecond[index]);
  H3c=[r*Nc[1],r*Nc[2],Rc]~;
  H2c=[x5*r^2,y5*r^2,r*Nc[3]]~;
  Dc=matdet(z*jacmat(H2c)+z^2*jacmat(H3c)+z^3*jacmat(H4));
  check_zero(polcoeff(Dc,7,z),"fresh E7 determinant");
  E6rc=polcoeff(polcoeff(Dc,6,z),1,r);
  colX=cv(substvec(E6rc,[ss,tt,x5,y5],[1,0,0,0]),5);
  colZ=cv(substvec(E6rc,[ss,tt,x5,y5],[0,1,0,0]),5);
  colY=cv(substvec(E6rc,[ss,tt,x5,y5],[1,1,0,0]),5)-colX-colZ;
  colx=cv(substvec(E6rc,[ss,tt,x5,y5],[0,0,1,0]),5);
  coly=cv(substvec(E6rc,[ss,tt,x5,y5],[0,0,0,1]),5);
  matrix(6,5,i,j,[colX,colY,colZ,colx,coly][j][i])
};

BB='BB; CC='CC; ss='ss; tt='tt; x5='x5; y5='y5;
ell=p+q;
P=p^3*ell; Q=p*ell*q^2;
R=ell*(-4*BB*p^2+BB*p*q+CC*q^2);
H4=[P,Q,0]~;
alpha=jac2(Q,R); beta=-jac2(P,R); gam=jac2(P,Q);
check_zero(gcd(gcd(alpha,beta),gam)-q*ell,"generic gcd");
gC0=gcd(gcd(substvec(alpha,[CC,BB],[0,1]),substvec(beta,[CC,BB],[0,1])),gam);
gC5=gcd(gcd(substvec(alpha,[CC,BB],[5,1]),substvec(beta,[CC,BB],[5,1])),gam);
check_zero(gC0^2-(p*q*ell)^2,"C=0 deeper gcd");
check_zero(gC5^2-(q*ell^2)^2,"C=5B deeper gcd");

u0='u0; u1='u1; u2='u2; v0='v0; v1='v1; v2='v2; t0='t0; t1='t1;
unknown7=[u0,u1,u2,v0,v1,v2,t0,t1];
uform=u0*p^2+u1*p*q+u2*q^2;
vform=v0*p^2+v1*p*q+v2*q^2;
tform=t0*p+t1*q;
E7=alpha*uform+beta*vform+gam*tform;
M7=matrix(8,8,i,j,polcoeff(hc(E7,7,i-1),1,unknown7[j]));
check_zero(matrank(substvec(M7,[CC,BB],[0,1]))-5,"C=0 fresh E7 rank");
check_zero(matrank(substvec(M7,[CC,BB],[5,1]))-5,"C=5B fresh E7 rank");
check_zero(matdet(vecextract(M7,[2,3,4,5,6,7],[1,2,3,4,5,6]))-216*CC^3*(BB+16*CC)*(5*BB-CC)^2,"generic E7 rank minor");
print("PASS PARI fresh C=0 and C=5B delta-three reruns");

N1=[-27*CC*p^2,8*BB*p^2+8*BB*p*q-16*CC*p^2+2*CC*p*q-9*CC*q^2,p*(BB+16*CC)*(5*BB-CC)];
N2=[3*p^2*(5*BB+8*CC),72*BB*p^2+62*BB*p*q+5*BB*q^2-16*CC*p*q+8*CC*q^2,q*(BB+16*CC)*(5*BB-CC)];
for(index=1,2,{
  Ncheck=if(index==1,N1,N2);
  check_zero(alpha*Ncheck[1]+beta*Ncheck[2]+gam*Ncheck[3],Str("generic E7 tangent ",index))
});
Mg=contact_matrix(R,N1,N2);
check_zero(matdet(vecextract(Mg,[1,2,3,4,5],[1,2,3,4,5]))+746496*CC^3*(BB+16*CC)^3*(5*BB-4*CC)*(5*BB-CC)^4,"generic contact determinant");
print("PASS PARI generic lifted contact determinant");

Rp=substvec(R,[BB,CC],[-16,1]);
ap=substvec(alpha,[BB,CC],[-16,1]);
bp=substvec(beta,[BB,CC],[-16,1]);
M7p=substvec(M7,[BB,CC],[-16,1]);
check_zero(matdet(vecextract(M7p,[2,3,4,5,6,7],[1,2,3,4,5,7]))+157464,"pivot E7 rank minor");
Np1=[3*p^2,16*p^2+14*p*q+q^2,0];
Np2=[0,8*p*ell/9,-8*p+q];
for(index=1,2,{
  Ncheck=if(index==1,Np1,Np2);
  check_zero(ap*Ncheck[1]+bp*Ncheck[2]+gam*Ncheck[3],Str("pivot E7 tangent ",index))
});
Mp=contact_matrix(Rp,Np1,Np2);
check_zero(matdet(vecextract(Mp,[1,2,3,4,5],[1,2,3,4,5]))-6967296,"pivot contact determinant");
print("PASS PARI fresh B=-16C pivot chart");

Rs=substvec(R,[BB,CC],[4,5]);
as=substvec(alpha,[BB,CC],[4,5]);
bs=substvec(beta,[BB,CC],[4,5]);
M7s=substvec(M7,[BB,CC],[4,5]);
check_zero(matdet(vecextract(M7s,[2,3,4,5,6,7],[1,2,3,4,5,6]))-510300000,"special E7 rank minor");
Ns1=[-3*p^2/28,-(16*p^2-14*p*q+15*q^2)/420,p];
Ns2=[p^2/7,(24*p^2+14*p*q+5*q^2)/105,q];
for(index=1,2,{
  Ncheck=if(index==1,Ns1,Ns2);
  check_zero(as*Ncheck[1]+bs*Ncheck[2]+gam*Ncheck[3],Str("special E7 tangent ",index))
});
Ms=contact_matrix(Rs,Ns1,Ns2);
Ks=[-840,-945/2,-945/4,0,1]~;
check_zero(Ms*Ks,"special contact kernel");
check_zero(matdet(vecextract(Ms,[2,3,4,5],[1,2,3,4]))-120/343,"special rank-four minor");
check_zero(Ks[2]^2-Ks[1]*Ks[3]-99225/4,"special Veronese obstruction");
print("PASS PARI fresh 5B=4C kernel misses Veronese");

a0='a0; a1='a1; b0='b0; b1='b1; l33='l33;
E6c=alpha*(a0*p+a1*q)+beta*(b0*p+b1*q)+gam*l33;
unknown=[a0,a1,b0,b1,l33];
Mc=matrix(7,5,i,j,polcoeff(hc(E6c,6,i-1),1,unknown[j]));
check_zero(matdet(vecextract(Mc,[3,4,5,6,7],[1,2,3,4,5]))+648*CC^3*(5*BB-CC),"constant E6 determinant");
print("PASS PARI constant E6 full rank and all-binary exit");
print("ALL PARI PELL FIXED-L CONTACT {1,1} CHECKS PASSED");
