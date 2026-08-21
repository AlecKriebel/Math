\\ Independent PARI/GP replay of the squarefree-interior two-fixed leaf.

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
  check_zero(polcoeff(Dc,7,z),"E7 determinant");
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
P=h*p^2; Q=h*q^2; R=h*(AA*p+BB*q);
H4=[P,Q,0]~;
alpha=jac2(Q,R); beta=-jac2(P,R); gam=jac2(P,Q);
gg=gcd(gcd(alpha,beta),gam);
check_zero(gg^2-h^2,"generic gcd");
gE=gcd(gcd(substvec(alpha,[AA,BB],[-ww,1]),substvec(beta,[AA,BB],[-ww,1])),gam);
gD=gcd(gcd(substvec(alpha,[AA,BB],[1,-ww]),substvec(beta,[AA,BB],[1,-ww])),gam);
gleft=gcd(gcd(substvec(alpha,[AA,BB],[4*ww,ww^2+1]),substvec(beta,[AA,BB],[4*ww,ww^2+1])),gam);
gright=gcd(gcd(substvec(alpha,[AA,BB],[ww^2+1,4*ww]),substvec(beta,[AA,BB],[ww^2+1,4*ww])),gam);
check_zero(gE^2-(L*Mfix^2)^2,"M doubled boundary gcd");
check_zero(gD^2-(L^2*Mfix)^2,"L doubled boundary gcd");
check_zero(gleft^2-(q*h)^2,"left-contact boundary gcd");
check_zero(gright^2-(p*h)^2,"right-contact boundary gcd");
print("PASS PARI four deeper-incidence boundary gcd reruns");

evalM=AA+BB*ww; evalL=AA*ww+BB;
leftc=AA*ww^2+AA-4*BB*ww;
rightc=-4*AA*ww+BB*ww^2+BB;
u0='u0; u1='u1; u2='u2; v0='v0; v1='v1; v2='v2; t0='t0; t1='t1;
unknown7=[u0,u1,u2,v0,v1,v2,t0,t1];
uform=u0*p^2+u1*p*q+u2*q^2;
vform=v0*p^2+v1*p*q+v2*q^2;
tform=t0*p+t1*q;
E7=alpha*uform+beta*vform+gam*tform;
M7=matrix(8,8,i,j,polcoeff(hc(E7,7,i-1),1,unknown7[j]));
check_zero(matdet(vecextract(M7,[1,2,3,4,5,6],[1,2,3,4,5,6]))-24*ww^6*evalM^2*(ww-1)^2*(ww+1)^2*evalL^2*rightc*leftc,"E7 rank minor");

N1=[p*(4*AA*p*ww+5*BB*p*ww^2+5*BB*p-6*BB*q*ww),q*(4*AA*q*ww+6*BB*p*ww-BB*q*ww^2-BB*q),3*p*evalM*evalL];
N2=[-p*(AA*p*ww^2+AA*p-6*AA*q*ww-4*BB*p*ww),-q*(6*AA*p*ww-5*AA*q*ww^2-5*AA*q-4*BB*q*ww),3*q*evalM*evalL];
for(index=1,2,{
  Ncheck=if(index==1,N1,N2);
  check_zero(alpha*Ncheck[1]+beta*Ncheck[2]+gam*Ncheck[3],Str("E7 tangent ",index))
});
Mc=contact_matrix(R,N1,N2);
check_zero(matdet(vecextract(Mc,[1,2,3,4],[1,2,3,4]))+41472*ww^5*evalM^4*evalL^4*rightc*leftc,"contact rank-four minor");
K=[5*AA^2*ww^4-14*AA^2*ww^2+5*AA^2-4*AA*BB*ww^3-4*AA*BB*ww-4*BB^2*ww^2,2*AA^2*ww^3+2*AA^2*ww+7*AA*BB*ww^4-6*AA*BB*ww^2+7*AA*BB+2*BB^2*ww^3+2*BB^2*ww,-4*AA^2*ww^2-4*AA*BB*ww^3-4*AA*BB*ww+5*BB^2*ww^4-14*BB^2*ww^2+5*BB^2,-36*ww*evalM^2*evalL^2,-36*ww*evalM^2*evalL^2]~;
check_zero(Mc*K,"contact kernel");
check_zero(K[2]^2-K[1]*K[3]-24*evalM^2*(ww-1)^2*(ww+1)^2*evalL^2,"Veronese obstruction");
print("PASS PARI rank-four contact kernel misses Veronese");

a0='a0; a1='a1; b0='b0; b1='b1; l33='l33;
E6const=alpha*(a0*p+a1*q)+beta*(b0*p+b1*q)+gam*l33;
unknown=[a0,a1,b0,b1,l33];
Mconst=matrix(7,5,i,j,polcoeff(hc(E6const,6,i-1),1,unknown[j]));
check_zero(matdet(vecextract(Mconst,[1,2,3,4,5],[1,2,3,4,5]))+8*ww^5*evalM*(ww-1)^2*(ww+1)^2*evalL*rightc*leftc,"constant E6 determinant");
print("PASS PARI constant E6 full rank and all-binary exit");
print("ALL PARI INTERIOR TWO-FIXED {1,1} CHECKS PASSED");
