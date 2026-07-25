\\ Independent PARI/GP reconstruction of the unmarked-double {1,1}
\\ contact exclusion.

default(parisizemax,512000000);
allocatemem(128000000);

checkzero(value,message) =
{
  if(value != 0,
    print(Str("FAIL: ",message));
    quit(1)
  );
};
jac2(f,g) = deriv(f,p)*deriv(g,q)-deriv(f,q)*deriv(g,p);
jac3(f,g,h) = matdet([deriv(f,p),deriv(f,q),deriv(f,r);deriv(g,p),deriv(g,q),deriv(g,r);deriv(h,p),deriv(h,q),deriv(h,r)]);
cf(f,ep,eq) = polcoef(polcoef(f,eq,q),ep,p);
contactvec(P,Q,R,N,M) =
{
  my(S=xx*N+yy*M,K,res);
  K=polcoef(jac3(P,r*S[2],r*S[3])
           +jac3(r*S[1],Q,r*S[3])
           +jac3(r*S[1],r*S[2],R),1,r);
  res=K-lm*jac2(Q,R)-mu*(-jac2(P,R));
  vector(6,i,cf(res,5-(i-1),i-1))
};

{
\\ General normal form and the two divided-gradient columns.
P=p*q^3;
Q=p*(p^3+b*p^2*q+c*p*q^2);
R=d*(p^3+3*b*p^2*q/4+(3*c/4-3*b^2/32)*p*q^2)+e*q^3;
K=3*b^2-8*c;
Fp=[deriv(P,p),deriv(Q,p),deriv(R,p)]~;
Fq=[deriv(P,q),deriv(Q,q),deriv(R,q)]~;
N=(Fq-b*Fp/4)/q;
M=(p*N+K*Fp/16)/q;
C=[-16*p/K,(3*b^2*q-4*b*p-8*c*q)/K;
   16*q/K,4*b*q/K];
G=matrix(3,2,i,j,[Fp,Fq][j][i]);
for(i=1,3,for(j=1,2,
  checkzero(G[i,j]-(matconcat([N,M])*C)[i,j],
            "general gradient reconstruction")
));
checkzero(matdet(C)+16*q^2/K,"general change determinant");
alpha=jac2(Q,R); beta=-jac2(P,R); gam=jac2(P,Q);
checkzero(alpha*N[1]+beta*N[2]+gam*N[3],"first HB syzygy");
checkzero(alpha*M[1]+beta*M[2]+gam*M[3],"second HB syzygy");

\\ Generic scaling chart b=d=1.
Pg=p*q^3;
Qg=p*(p^3+p^2*q+cc*p*q^2);
Rg=p^3+3*p^2*q/4+(3*cc/4-3/32)*p*q^2+ee*q^3;
Kg=3-8*cc;
Fpg=[deriv(Pg,p),deriv(Qg,p),deriv(Rg,p)]~;
Fqg=[deriv(Pg,q),deriv(Qg,q),deriv(Rg,q)]~;
Ng=(Fqg-Fpg/4)/q;
Mg=(p*Ng+Kg*Fpg/16)/q;
GC=contactvec(Pg,Qg,Rg,Ng,Mg);
Jg=192*cc^3-48*cc^2-1024*cc*ee-5*cc+1024*ee^2+320*ee;
Bg=-jac2(Pg,Rg)/q^2;
Hg=3*p^2+2*p*q+cc*q^2;
checkzero(polresultant(subst(Bg,q,1),subst(Hg,q,1),p)
          -243*Jg/1024,
          "generic exact-gcd boundary resultant");

\\ y=0,x=1 contact.
Y0=vector(6,i,subst(subst(GC[i],yy,0),xx,1));
checkzero(Y0[1],"generic y0 first zero");
checkzero(Y0[2],"generic y0 second zero");
checkzero(Y0[6]-3*ee*(cc+8*mu)/8,"generic y0 mu pivot");
muv=-cc/8;
checkzero(subst(Y0[5],mu,muv)
          +3*ee*(16*lm*cc-8*cc-3)/8,
          "generic y0 lambda pivot");
lmv=(8*cc+3)/(16*cc);
checkzero(subst(subst(Y0[3],mu,muv),lm,lmv)
          +3*(8*cc-3)*(96*cc^2-36*cc-128*ee+5)/(512*cc),
          "generic y0 first residual");
checkzero(subst(subst(Y0[4],mu,muv),lm,lmv)
          +3*(8*cc-3)*(32*cc*ee+cc-24*ee)/(128*cc),
          "generic y0 second residual");
eev=(96*cc^2-36*cc+5)/128;
checkzero(subst(32*cc*ee+cc-24*ee,ee,eev)
          -3*(4*cc-1)^2*(8*cc-5)/16,
          "generic y0 contact alternatives");
checkzero(subst(Jg,ee,eev)
          -9*(4*cc-1)^2*(8*cc-5)^2/16,
          "generic y0 alternatives have larger gcd");

\\ y=1 contact.  The first two coefficients force ee=e0 and h=0
\\ off the exceptional component.
Y1=vector(6,i,subst(GC[i],yy,1));
e0=-(25-144*cc+192*cc^2)/512;
h=64*cc^2-16*cc-1;
checkzero(Y1[1]-3*(192*cc^2-144*cc+512*ee+25)/128,
          "generic y1 e pivot");
checkzero(subst(Y1[2],ee,e0)+45*(8*cc-3)*h/2048,
          "generic y1 quadratic");
R2=-1024*lm*cc+256*lm-2048*mu+1024*cc*xx^2
   -512*cc*xx-104*cc-320*xx^2+160*xx+31;
R3=-5120*lm*cc+1280*lm-10240*mu+5120*cc*xx^2
   -3904*cc*xx-408*cc-1600*xx^2+1208*xx+121;
checkzero(divrem(subst(Y1[3],ee,e0),h,cc)[2]-9*R2/2048,
          "generic y1 first h remainder");
checkzero(divrem(subst(Y1[4],ee,e0),h,cc)[2]-3*R3/8192,
          "generic y1 second h remainder");
checkzero(R3-5*R2+2*(56*cc-17)*(12*xx-1),
          "generic y1 x compatibility");
checkzero(polresultant(h,56*cc-17,cc)-128,
          "generic y1 x pivot resultant");

E0=9216*lm*cc-2304*lm+18432*mu+1256*cc-379;
E1=4608*lm*cc-1728*lm-73728*mu*cc+9216*mu
   +12792*cc-3865;
E2=221184*mu*cc-64512*mu-824*cc+249;
checkzero(subst(divrem(subst(Y1[3],ee,e0),h,cc)[2],xx,1/12)+E0/2048,
          "generic y1 E0");
checkzero(subst(divrem(subst(Y1[5],ee,e0),h,cc)[2],xx,1/12)-E1/98304,
          "generic y1 E1");
checkzero(subst(divrem(subst(Y1[6],ee,e0),h,cc)[2],xx,1/12)-E2/393216,
          "generic y1 E2");
Aug=[deriv(E0,lm),deriv(E0,mu),subst(subst(E0,lm,0),mu,0);
     deriv(E1,lm),deriv(E1,mu),subst(subst(E1,lm,0),mu,0);
     deriv(E2,lm),deriv(E2,mu),subst(subst(E2,lm,0),mu,0)];
checkzero(divrem(matdet(Aug),h,cc)[2]+31850496*(79048*cc-23855),
          "generic y1 augmented determinant");
checkzero(polresultant(h,79048*cc-23855,cc)-278656,
          "generic y1 final resultant");

\\ Boundary b!=0,d=0; scale b=e=1.
P10=p*q^3;
Q10=p*(p^3+p^2*q+cc*p*q^2);
R10=q^3;
F10p=[deriv(P10,p),deriv(Q10,p),deriv(R10,p)]~;
F10q=[deriv(P10,q),deriv(Q10,q),deriv(R10,q)]~;
N10=(F10q-F10p/4)/q;
M10=(p*N10+(3-8*cc)*F10p/16)/q;
C10=contactvec(P10,Q10,R10,N10,M10);
checkzero(C10[1]-12*yy^2,"b nonzero d0 y pivot");
C10z=vector(6,i,subst(subst(C10[i],yy,0),xx,1));
checkzero(C10z[3]+12*(lm-1),"b nonzero d0 lambda");
checkzero(C10z[4]+3*(8*cc+12*lm-15)/4,
          "b nonzero d0 exceptional divisor");

\\ Boundary b=0,c=1,d=1.
P01=p*q^3;
Q01=p*(p^3+p*q^2);
R01=p^3+3*p*q^2/4+ee*q^3;
F01p=[deriv(P01,p),deriv(Q01,p),deriv(R01,p)]~;
F01q=[deriv(P01,q),deriv(Q01,q),deriv(R01,q)]~;
N01=F01q/q;
M01=(p*N01-F01p/2)/q;
C01=contactvec(P01,Q01,R01,N01,M01);
checkzero(C01[1]-9*yy^2/2,"b0 d nonzero y pivot");
C01z=vector(6,i,subst(subst(C01[i],yy,0),xx,1));
checkzero(C01z[6]-3*ee*mu,"b0 d nonzero mu pivot");
checkzero(C01z[5]+3*(mu+8*ee*lm)/4,
          "b0 d nonzero lambda pivot");
checkzero(C01z[4]+3*(lm+4*ee)/2,
          "b0 d nonzero contradiction");

\\ Corner b=d=0,c=e=1.
P00=p*q^3;
Q00=p*(p^3+p*q^2);
R00=q^3;
F00p=[deriv(P00,p),deriv(Q00,p),deriv(R00,p)]~;
F00q=[deriv(P00,q),deriv(Q00,q),deriv(R00,q)]~;
N00=F00q/q;
M00=(p*N00-F00p/2)/q;
C00=contactvec(P00,Q00,R00,N00,M00);
checkzero(C00[2]-30*yy^2,"b0 d0 y pivot");
checkzero(subst(subst(C00[4],yy,0),xx,1)+6,
          "b0 d0 contradiction");

print("PASS independent PARI unmarked-double {1,1} reconstruction");
}
quit;
