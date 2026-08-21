\\ Independent PARI/GP replay of the fixed-p plus contact leaf.

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

TT='TT; CC='CC; ss='ss; tt='tt; x5='x5; y5='y5;
ell=p+q;
P=p^3*ell; Q=p*ell*q^2;
R=p*(4*TT*p^2+3*TT*p*q+CC*q^2);
H4=[P,Q,0]~;
alpha=jac2(Q,R); beta=-jac2(P,R); gam=jac2(P,Q);
check_zero(gcd(gcd(alpha,beta),gam)-p*q,"generic gcd");
gC0=gcd(gcd(substvec(alpha,[CC,TT],[0,1]),substvec(beta,[CC,TT],[0,1])),gam);
gCT=gcd(gcd(substvec(alpha,[CC,TT],[-1,1]),substvec(beta,[CC,TT],[-1,1])),gam);
check_zero(gC0^2-(p^2*q)^2,"C=0 deeper gcd");
check_zero(gCT^2-(p*q*ell)^2,"C=-T deeper gcd");

u0='u0; u1='u1; u2='u2; v0='v0; v1='v1; v2='v2; t0='t0; t1='t1;
unknown7=[u0,u1,u2,v0,v1,v2,t0,t1];
uform=u0*p^2+u1*p*q+u2*q^2;
vform=v0*p^2+v1*p*q+v2*q^2;
tform=t0*p+t1*q;
E7=alpha*uform+beta*vform+gam*tform;
M7=matrix(8,8,i,j,polcoeff(hc(E7,7,i-1),1,unknown7[j]));
check_zero(matrank(substvec(M7,[CC,TT],[0,1]))-5,"C=0 fresh E7 rank");
check_zero(matrank(substvec(M7,[CC,TT],[-1,1]))-5,"C=-T fresh E7 rank");
check_zero(matdet(vecextract(M7,[2,3,4,5,6,7],[1,2,3,4,5,6]))+72*CC^3*(CC+TT)^2*(16*CC-9*TT),"generic E7 rank minor");
print("PASS PARI fresh C=0 and C=-T delta-three reruns");

N1=[-5*CC*p^2,CC*(16*p^2+22*p*q+q^2),CC*p*(16*CC-9*TT)];
N2=[p^2*(8*CC+3*TT),16*CC*p*q+24*CC*q^2-24*TT*p^2-42*TT*p*q-15*TT*q^2,CC*q*(16*CC-9*TT)];
for(index=1,2,{
  Ncheck=if(index==1,N1,N2);
  check_zero(alpha*Ncheck[1]+beta*Ncheck[2]+gam*Ncheck[3],Str("generic E7 tangent ",index))
});
Mg=contact_matrix(R,N1,N2);
check_zero(matdet(vecextract(Mg,[1,2,3,4,5],[1,2,3,4,5]))-27648*CC^5*(CC+TT)^2*(12*CC+7*TT)*(16*CC-9*TT)^3,"generic contact determinant");
print("PASS PARI generic lifted contact determinant");

Rp=substvec(R,[CC,TT],[9,16]);
ap=substvec(alpha,[CC,TT],[9,16]);
bp=substvec(beta,[CC,TT],[9,16]);
M7p=substvec(M7,[CC,TT],[9,16]);
check_zero(matdet(vecextract(M7p,[2,3,4,5,6,7],[1,2,3,4,5,7]))-32805000,"pivot E7 rank minor");
Np1=[-5*p^2,16*p^2+22*p*q+q^2,0];
Np2=[8*p^2/9,-8*p*(3*p+4*q)/9,(8*p+3*q)/3];
for(index=1,2,{
  Ncheck=if(index==1,Np1,Np2);
  check_zero(ap*Ncheck[1]+bp*Ncheck[2]+gam*Ncheck[3],Str("pivot E7 tangent ",index))
});
Mp=contact_matrix(Rp,Np1,Np2);
check_zero(matdet(vecextract(Mp,[1,2,3,4,5],[1,2,3,4,5]))-422400000,"pivot contact determinant");
print("PASS PARI fresh 16C=9T pivot chart");

Rs=substvec(R,[CC,TT],[7,-12]);
as=substvec(alpha,[CC,TT],[7,-12]);
bs=substvec(beta,[CC,TT],[7,-12]);
M7s=substvec(M7,[CC,TT],[7,-12]);
check_zero(matdet(vecextract(M7s,[2,3,4,5,6,7],[1,2,3,4,5,6]))+135828000,"special E7 rank minor");
Ns1=[-p^2/44,(16*p^2+22*p*q+q^2)/220,p];
Ns2=[p^2/77,(72*p^2+154*p*q+87*q^2)/385,q];
for(index=1,2,{
  Ncheck=if(index==1,Ns1,Ns2);
  check_zero(as*Ncheck[1]+bs*Ncheck[2]+gam*Ncheck[3],Str("special E7 tangent ",index))
});
Ms=contact_matrix(Rs,Ns1,Ns2);
Ks=[-2354/3,3773/24,-539/48,0,1]~;
check_zero(Ms*Ks,"special contact kernel");
check_zero(matdet(vecextract(Ms,[2,3,4,5],[1,2,3,4]))+864/9317,"special rank-four minor");
check_zero(Ks[2]^2-Ks[1]*Ks[3]-3053435/192,"special Veronese obstruction");
print("PASS PARI fresh 12C=-7T kernel misses Veronese");

a0='a0; a1='a1; b0='b0; b1='b1; l33='l33;
E6c=alpha*(a0*p+a1*q)+beta*(b0*p+b1*q)+gam*l33;
unknown=[a0,a1,b0,b1,l33];
Mc=matrix(7,5,i,j,polcoeff(hc(E6c,6,i-1),1,unknown[j]));
check_zero(matdet(vecextract(Mc,[2,3,4,5,6],[1,2,3,4,5]))-72*CC^2*(CC+TT)^2,"constant E6 determinant");
print("PASS PARI constant E6 full rank and all-binary exit");
print("ALL PARI PELL FIXED-P CONTACT {1,1} CHECKS PASSED");
