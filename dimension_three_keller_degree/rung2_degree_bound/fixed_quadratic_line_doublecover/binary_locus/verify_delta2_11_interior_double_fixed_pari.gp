\\ Independent PARI/GP replay of the squarefree-interior double-fixed leaf.

p='p; q='q; r='r; z='z;
vars=[p,q,r];
jacmat(H)=matrix(3,3,i,j,deriv(H[i],vars[j]));
jac2(f,g)=deriv(f,p)*deriv(g,q)-deriv(f,q)*deriv(g,p);
check_zero(value,message)={if(value!=0,error(Str("FAIL: ",message,"; residual = ",value)))};
hc(f,degree,index)=polcoeff(subst(f,q,1),degree-index,p);
cv(f,degree)=vector(degree+1,index,hc(f,degree,index-1));
contact_matrix(Rc,Nfirst,Nsecond)={
  my(Nc,H3c,H2c,Dc,E6rc,colX,colY,colZ,colx,coly);
  Nc=vector(3,index,c1*Nfirst[index]+c2*Nsecond[index]);
  H3c=[r*Nc[1],r*Nc[2],Rc]~;
  H2c=[x5*r^2,y5*r^2,r*Nc[3]]~;
  Dc=matdet(z*jacmat(H2c)+z^2*jacmat(H3c)+z^3*jacmat(H4));
  check_zero(polcoeff(Dc,7,z),"fresh E7 determinant");
  E6rc=polcoeff(polcoeff(Dc,6,z),1,r);
  colX=cv(substvec(E6rc,[c1,c2,x5,y5],[1,0,0,0]),5);
  colZ=cv(substvec(E6rc,[c1,c2,x5,y5],[0,1,0,0]),5);
  colY=cv(substvec(E6rc,[c1,c2,x5,y5],[1,1,0,0]),5)-colX-colZ;
  colx=cv(substvec(E6rc,[c1,c2,x5,y5],[0,0,1,0]),5);
  coly=cv(substvec(E6rc,[c1,c2,x5,y5],[0,0,0,1]),5);
  matrix(6,5,i,j,[colX,colY,colZ,colx,coly][j][i])
};

ww='ww; AA='AA; BB='BB; c1='c1; c2='c2; x5='x5; y5='y5;
L=p-ww*q; Mfix=ww*p-q; h=L*Mfix;
P=h*p^2; Q=h*q^2; R=L^2*(AA*p+BB*q);
H4=[P,Q,0]~;
alpha=jac2(Q,R); beta=-jac2(P,R); gam=jac2(P,Q);
gg=gcd(gcd(alpha,beta),gam);
check_zero(gg^2-L^4,"generic gcd");
gother=gcd(gcd(substvec(alpha,[AA,BB],[-ww,1]),substvec(beta,[AA,BB],[-ww,1])),gam);
gleft=gcd(gcd(substvec(alpha,[AA,BB],[4*ww,5*ww^2-3]),substvec(beta,[AA,BB],[4*ww,5*ww^2-3])),gam);
gright=gcd(gcd(substvec(alpha,[AA,BB],[5-3*ww^2,4*ww]),substvec(beta,[AA,BB],[5-3*ww^2,4*ww])),gam);
check_zero(gother^2-(L^2*Mfix)^2,"other fixed-root boundary gcd");
check_zero(gleft^2-(q*L^2)^2,"left-contact boundary gcd");
check_zero(gright^2-(p*L^2)^2,"right-contact boundary gcd");
print("PASS PARI three deeper-incidence boundary gcd reruns");

other=AA+BB*ww; pivot=AA*ww+BB;
leftc=5*AA*ww^2-3*AA-4*BB*ww;
rightc=4*AA*ww+3*BB*ww^2-5*BB;
u0='u0; u1='u1; u2='u2; v0='v0; v1='v1; v2='v2; t0='t0; t1='t1;
unknown7=[u0,u1,u2,v0,v1,v2,t0,t1];
uform=u0*p^2+u1*p*q+u2*q^2;
vform=v0*p^2+v1*p*q+v2*q^2;
tform=t0*p+t1*q;
E7=alpha*uform+beta*vform+gam*tform;
M7=matrix(8,8,i,j,polcoeff(hc(E7,7,i-1),1,unknown7[j]));
check_zero(matdet(vecextract(M7,[1,2,3,4,5,6],[1,2,3,4,5,6]))-360*other^2*(ww-1)^2*(ww+1)^2*pivot^2*rightc*leftc,"generic E7 rank minor");

N1=[p*(4*AA*p*ww+27*BB*p*ww^2-5*BB*p-18*BB*q*ww),-q*(8*AA*p*ww^2-12*AA*q*ww-10*BB*p*ww-9*BB*q*ww^2+15*BB*q),5*p*pivot^2];
N2=[-p*(15*AA*p*ww^2-9*AA*p-10*AA*q*ww-12*BB*p*ww+8*BB*q),-q*(18*AA*p*ww+5*AA*q*ww^2-27*AA*q-4*BB*q*ww),5*q*pivot^2];
for(index=1,2,{
  Ncheck=if(index==1,N1,N2);
  check_zero(alpha*Ncheck[1]+beta*Ncheck[2]+gam*Ncheck[3],Str("generic E7 tangent ",index))
});
Mc=contact_matrix(R,N1,N2);

Q1=108*AA^3*ww^5-266*AA^3*ww^3+216*AA^2*BB*ww^6-855*AA^2*BB*ww^4+165*AA^2*BB*ww^2+108*AA*BB^2*ww^7-972*AA*BB^2*ww^5+450*AA*BB^2*ww^3-60*AA*BB^2*ww-378*BB^3*ww^6+270*BB^3*ww^4-45*BB^3*ww^2-5*BB^3;
Q2=127*AA^3*ww^4-285*AA^3*ww^2+294*AA^2*BB*ww^5-954*AA^2*BB*ww^3+186*AA^2*BB*ww+162*AA*BB^2*ww^6-978*AA*BB^2*ww^4+357*AA*BB^2*ww^2-15*AA*BB^2-324*BB^3*ww^5+186*BB^3*ww^3-20*BB^3*ww;
Q3=20*AA^3*ww^5-186*AA^3*ww^3+324*AA^3*ww+15*AA^2*BB*ww^6-357*AA^2*BB*ww^4+978*AA^2*BB*ww^2-162*AA^2*BB-186*AA*BB^2*ww^5+954*AA*BB^2*ww^3-294*AA*BB^2*ww+285*BB^3*ww^4-127*BB^3*ww^2;
Q4=5*AA^3*ww^7+45*AA^3*ww^5-270*AA^3*ww^3+378*AA^3*ww+60*AA^2*BB*ww^6-450*AA^2*BB*ww^4+972*AA^2*BB*ww^2-108*AA^2*BB-165*AA*BB^2*ww^5+855*AA*BB^2*ww^3-216*AA*BB^2*ww+266*BB^3*ww^4-108*BB^3*ww^2;
base=1920000*(ww-1)^3*(ww+1)^3*pivot^6*rightc*leftc;
check_zero(matdet(vecextract(Mc,[1,3,4,5,6],[1,2,3,4,5]))-base*ww^2*Q1,"residual minor Q1");
check_zero(matdet(vecextract(Mc,[1,2,4,5,6],[1,2,3,4,5]))+base*ww^2*Q2,"residual minor Q2");
check_zero(matdet(vecextract(Mc,[1,2,3,5,6],[1,2,3,4,5]))+base*ww^2*Q3,"residual minor Q3");
check_zero(matdet(vecextract(Mc,[1,2,3,4,6],[1,2,3,4,5]))-base*ww*Q4,"residual minor Q4");
print("PASS PARI four residual contact-minor identities");

q1=subst(Q1,BB,1); q2=subst(Q2,BB,1);
q3=subst(Q3,BB,1); q4=subst(Q4,BB,1);
res12=polresultant(q1,q2,AA);
res13=polresultant(q1,q3,AA);
res14=polresultant(q1,q4,AA);
res23=polresultant(q2,q3,AA);
check_zero(res12-637729200*ww^6*(ww-1)^12*(ww+1)^12*(12*ww^4+28*ww^2-57),"resultant 12");
check_zero(res13+318864600*ww^3*(ww-1)^12*(ww+1)^12*(ww^2+3)^2*(18*ww^4-27*ww^2-8),"resultant 13");
check_zero(res14-1434890700*ww^3*(ww-1)^12*(ww+1)^12*(14*ww^12+28*ww^10+77*ww^8-34*ww^6+77*ww^4+28*ww^2+14),"resultant 14");
check_zero(res23+159432300*ww^4*(ww-1)^12*(ww+1)^12*(23*ww^4-114*ww^2+23),"resultant 23");
resgcd=gcd(gcd(res12,res13),gcd(res14,res23));
expectedgcd=ww^3*(ww-1)^12*(ww+1)^12;
check_zero(resgcd/pollead(resgcd)-expectedgcd,"resultant gcd");
endpointgcd=gcd(substvec(Q1,[AA,BB],[1,0]),substvec(Q2,[AA,BB],[1,0]));
check_zero(endpointgcd/pollead(endpointgcd)-ww^2,"B=0 endpoint gcd");
print("PASS PARI projective resultant cover and endpoint gcd");

Rp=substvec(R,[AA,BB],[1,-ww]);
ap=substvec(alpha,[AA,BB],[1,-ww]);
bp=substvec(beta,[AA,BB],[1,-ww]);
M7p=substvec(M7,[AA,BB],[1,-ww]);
check_zero(matdet(vecextract(M7p,[1,2,3,4,5,6],[1,2,3,4,5,7]))+5832*ww^2*(ww-1)^4*(ww+1)^4*(ww^2-3)^2*(3*ww^2-1),"pivot E7 rank minor");
Np1=[9*p*ww*(3*p*ww^2-p-2*q*ww),9*q*ww*(2*p*ww+q*ww^2-3*q),0];
Np2=[8*p*(4*p*ww-3*q),8*p*q*ww^2,-9*L*(ww^2-3)];
for(index=1,2,{
  Ncheck=if(index==1,Np1,Np2);
  check_zero(ap*Ncheck[1]+bp*Ncheck[2]+gam*Ncheck[3],Str("pivot E7 tangent ",index))
});
Mp=contact_matrix(Rp,Np1,Np2);
check_zero(matdet(vecextract(Mp,[1,2,3,4,5],[1,2,3,4,5]))-48977602560*ww^5*(ww-1)^6*(ww+1)^6*(ww^2-3)^4*(3*ww^2-1),"pivot contact determinant");
print("PASS PARI fresh triple-fixed pivot chart");

a0='a0; a1='a1; b0='b0; b1='b1; l33='l33;
E6const=alpha*(a0*p+a1*q)+beta*(b0*p+b1*q)+gam*l33;
unknown=[a0,a1,b0,b1,l33];
Mconst=matrix(7,5,i,j,polcoeff(hc(E6const,6,i-1),1,unknown[j]));
check_zero(matdet(vecextract(Mconst,[1,2,3,4,5],[1,2,3,4,5]))+216*other^2*(ww-1)^2*(ww+1)^2*rightc*leftc,"constant E6 determinant");
print("PASS PARI constant E6 full rank and all-binary exit");
print("ALL PARI INTERIOR DOUBLE-FIXED {1,1} CHECKS PASSED");
