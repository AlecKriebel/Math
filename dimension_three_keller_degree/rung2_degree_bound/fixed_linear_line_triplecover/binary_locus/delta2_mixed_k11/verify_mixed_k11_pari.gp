\\ Independent PARI/GP replay of the fixed-linear mixed {1,1} leaf.

default(parisizemax,512000000);
allocatemem(128000000);

checkzero(value,message) =
{
  if(value != 0,
    print(Str("FAIL: ",message));
    quit(1)
  );
};
checknonzero(value,message) =
{
  if(value == 0,
    print(Str("FAIL: ",message));
    quit(1)
  );
};
jac2(f,g) = deriv(f,p)*deriv(g,q)-deriv(f,q)*deriv(g,p);
jac3(f,g,h) = matdet([deriv(f,p),deriv(f,q),deriv(f,r);deriv(g,p),deriv(g,q),deriv(g,r);deriv(h,p),deriv(h,q),deriv(h,r)]);
jacmap(V) = matrix(3,3,i,j,deriv(V[i],[p,q,r][j]));
cf(f,ep,eq) = polcoef(polcoef(f,eq,q),ep,p);
liftx(f,xx,xy) = polcoef(subst(f,y,1),2,x)*xx + polcoef(subst(f,y,1),1,x)*xy + polcoef(subst(f,y,1),0,x);
liftxy(f,xx,xy,yy) = polcoef(polcoef(f,2,x),0,y)*xx + polcoef(polcoef(f,1,x),1,y)*xy + polcoef(polcoef(f,0,x),2,y)*yy + polcoef(polcoef(f,0,x),0,y);

{
\\ First endpoint chart.
P1=p^2*q^2;
Q1=p*(p^3+p^2*q+q^3);
R1=p*(c*p^2+3*c*p*q/4+q^2);
a1=jac2(Q1,R1); b1=-jac2(P1,R1); g1=jac2(P1,Q1);
Np1=[deriv(P1,q)/p,deriv(Q1,q)/p,deriv(R1,q)/p]~;
Nq1=[(deriv(P1,q)-deriv(P1,p)/4)/q,
     (deriv(Q1,q)-deriv(Q1,p)/4)/q,
     (deriv(R1,q)-deriv(R1,p)/4)/q]~;
S1=x*Np1+y*Nq1;
K1=polcoef(jac3(P1,r*S1[2],r*S1[3])
           +jac3(r*S1[1],Q1,r*S1[3])
           +jac3(r*S1[1],r*S1[2],R1),1,r);
res1=K1-lm*a1-mu*b1;
E1=vector(5,i,cf(res1,5-(i-1),i-1));
checkzero(E1[1]+3*y^2*(49*c-16)/8,
          "first-chart leading contact coefficient");

\\ If y=0, put x=1.  The last two equations give lm=-6,
\\ mu=12c; the two remaining quadratics have nonzero resultant.
f10=numerator(subst(subst(subst(subst(E1[2],y,0),x,1),lm,-6),mu,12*c));
f20=numerator(subst(subst(subst(subst(E1[3],y,0),x,1),lm,-6),mu,12*c));
checkzero(polresultant(f10,f20,c)+17215416,
          "first-chart y=0 contradiction");

\\ At c=16/49 the lifted kernel is not Veronese.
csp=16/49;
xx1=-6/419; xy1=-141/838; yy1=4/419; lm1=-35/419; mu1=1;
for(i=1,5,
  vv=liftxy(subst(E1[i],c,csp),xx1,xy1,yy1);
  vv=subst(subst(vv,lm,lm1),mu,mu1);
  checkzero(vv,"first-chart lifted kernel")
);
checkzero(xy1^2-xx1*yy1-19977/702244,
          "first-chart Veronese obstruction");

\\ Second endpoint chart.
A=q^2*(a*p+q);
B=p^3+p^2*q+b*p*q^2;
P=p*A; Q=p*B;
R=p*(c*p^2+3*c*p*q/4+q^2);
alpha=jac2(Q,R); beta=-jac2(P,R); gam=jac2(P,Q);
Np=[deriv(P,q)/p,deriv(Q,q)/p,deriv(R,q)/p]~;
Nq=[(deriv(P,q)-deriv(P,p)/4)/q,
    (deriv(Q,q)-deriv(Q,p)/4)/q,
    (deriv(R,q)-deriv(R,p)/4)/q]~;
checkzero(alpha*Np[1]+beta*Np[2]+gam*Np[3],
          "first mixed syzygy");
checkzero(alpha*Nq[1]+beta*Nq[2]+gam*Nq[3],
          "second mixed syzygy");
S=x*Np+y*Nq;
Kc=polcoef(jac3(P,r*S[2],r*S[3])
           +jac3(r*S[1],Q,r*S[3])
           +jac3(r*S[1],r*S[2],R),1,r);
res=Kc-lm*alpha-mu*beta;
E=vector(5,i,cf(res,5-(i-1),i-1));
H=a*c-16*a-48*b*c+6*c+64;
checkzero(E[1]+3*y^2*H/8,"second-chart H coefficient");

\\ Independent resultant elimination on y=0,x=1.
Y=vector(3,i,numerator(subst(subst(subst(E[i+1],y,0),x,1),mu,-6*b)));
Ra=polresultant(Y[1],Y[3],lm);
Rb=polresultant(Y[2],Y[3],lm);
Elim=polresultant(Ra,Rb,a);
Fone=6*b*c-72*b+7;
Ftwo=9*b*c^2-48*b*c-6*c+16;
checkzero(Elim-4*b*Fone*Ftwo,
          "independent y=0 component elimination");
\\ b=0 itself is impossible because the fourth contact equation is -14.
checkzero(subst(subst(subst(subst(E[4],y,0),x,1),b,0),mu,0)+14,
          "y=0 b=0 boundary");

bf=7/(6*(12-c));
af=9*(c-8)*(c-4)/(2*(c-12));
lf=-9*c*(c-4)/(c-12);
mf=7/(c-12);
for(i=1,5,
  vv=subst(subst(subst(subst(subst(subst(E[i],a,af),b,bf),
       lm,lf),mu,mf),x,1),y,0);
  checkzero(vv,"first y=0 component")
);
Lf=3*(c-8)*p-q;
checkzero(alpha-subst(alpha,a,af)+subst(alpha,a,af)-alpha,
          "PARI substitution sanity");
for(i=1,3,
  ff=[alpha,beta,gam][i];
  qq=subst(subst(ff,a,af),b,bf)/(p*q*Lf);
  checkzero(poldegree(denominator(qq),p),
            "first y=0 extra factor p denominator");
  checkzero(poldegree(denominator(qq),q),
            "first y=0 extra factor q denominator")
);

bs=2*(3*c-8)/(3*c*(3*c-16));
as=9*c*(3*c^2-128)/(8*(3*c-16)*(3*c-8));
ls=-9*c*(3*c^2-64*c+128)/(4*(3*c-16)*(3*c-8));
ms=-4*(3*c-8)/(c*(3*c-16));
for(i=1,5,
  vv=subst(subst(subst(subst(subst(subst(E[i],a,as),b,bs),
       lm,ls),mu,ms),x,1),y,0);
  checkzero(vv,"second y=0 component")
);
Gs=27*c^3*p^2+144*c^2*p*q-1152*c*p^2-864*c*p*q
   +48*c*q^2-128*q^2;
for(i=1,3,
  ff=[alpha,beta,gam][i];
  qq=subst(subst(ff,a,as),b,bs)/(p*q*Gs);
  checkzero(poldegree(denominator(qq),p),
            "second y=0 extra factor p denominator");
  checkzero(poldegree(denominator(qq),q),
            "second y=0 extra factor q denominator")
);
\\ The apparent c=8/3,b=0 denominator endpoint is inconsistent.
Eb=vector(5,i,subst(subst(subst(subst(E[i],y,0),x,1),c,8/3),b,0));
\\ Eb[5] gives mu=0, and Eb[4] is then -14.
checkzero(subst(Eb[5],mu,0),"second-component endpoint mu equation");
checkzero(subst(Eb[4],mu,0)+14,
          "second-component endpoint contradiction");

\\ y!=0: solve H=0 and reconstruct the lifted kernel.
asol=(48*b*c-6*c-64)/(c-16);
D=24*b*c-3*c-32;
G=15*b*c^3-288*b*c^2+1536*b*c-2048*b
  -8*c^2+176*c-768;
Veq=408*b^2*c^2-6528*b^2*c+27648*b^2
    -171*b*c^2+2768*b*c-12032*b
    +18*c^2-296*c+1328;
xxv=3*(4*b-1)*(c-16)/(16*D);
xyv=3*(24*b-5)*(c-8)/(4*D);
lmv=(24*b-5)*(84*b*c^2-576*b*c-33*c^2+464*c-1536)
    /(4*(c-16)*D);
muv=b*(42*b*c-288*b-9*c+64)/(4*D);
for(i=1,5,
  vv=subst(E[i],a,asol);
  vv=liftx(vv,xxv,xyv);
  vv=subst(subst(vv,lm,lmv),mu,muv);
  checkzero(vv,"generic lifted contact kernel")
);
checkzero(xyv^2-xxv-3*Veq/(4*D^2),
          "generic Veronese equation");

\\ D=0 and G=0 both leave exact delta=2.
bD=(3*c+32)/(24*c);
aD=subst(asol,b,bD);
checkzero(aD,"D divisor forces a=0");
for(i=1,3,
  ff=subst(subst([alpha,beta,gam][i],a,aD),b,bD)/(p*q^2);
  checkzero(poldegree(denominator(ff),p),"D extra q factor");
  checkzero(poldegree(denominator(ff),q),"D extra q factor")
);
KK=15*c^3-288*c^2+1536*c-2048;
NN=8*c^2-176*c+768;
checkzero(polresultant(KK,NN,c)-209715200,
          "G denominator coprimality");
bG=NN/KK; aG=subst(asol,b,bG);
LG=15*c^2*p-192*c*p+4*c*q+512*p-64*q;
for(i=1,3,
  ff=subst(subst([alpha,beta,gam][i],a,aG),b,bG)/(p*q*LG);
  checkzero(poldegree(denominator(ff),p),"G extra line factor");
  checkzero(poldegree(denominator(ff),q),"G extra line factor")
);

\\ Top-only E5 obstruction and two independent parameter resultants.
St=subst(subst(subst(subst(subst(S,a,asol),x,xyv),y,1),
         lm,lmv),mu,muv);
H4=[subst(P,a,asol),Q,0];
H3=[r*St[1],r*St[2],R];
H2=[-lmv*r^2/2,-muv*r^2/2,r*St[3]];
weighted=matdet(zz*jacmap(H2)+zz^2*jacmap(H3)+zz^3*jacmap(H4));
E5=polcoef(weighted,5,zz);
C0=numerator(cf(polcoef(E5,2,r),3,0));
C1=numerator(cf(polcoef(E5,2,r),2,1));
Res0=polresultant(Veq,C0,b);
Res1=polresultant(Veq,C1,b);
f0=57*c^2-960*c+4096;
f1=11925*c^4-398990*c^3+5022128*c^2
   -28184576*c+59506688;
base0=(c-16)^6*(c-8)^6*f0;
base1=(c-16)^8*(c-8)^6*f1;
checkzero(poldegree(Res0/base0,c),
          "first E5 resultant factorization");
checkzero(poldegree(Res1/base1,c),
          "second E5 resultant factorization");
checknonzero(Res0,"first E5 resultant nonzero");
checknonzero(Res1,"second E5 resultant nonzero");
checkzero(polresultant(f0,f1,c)-20654497726464,
          "residual E5 resultants coprime");
checkzero(subst(Veq,c,8)-16*(4*b-1)*(24*b-7),
          "c=8 contact endpoints");
checkzero(subst(subst(D,b,7/24),c,8),"c=8 D endpoint");
checkzero(subst(subst(G,b,1/4),c,8),"c=8 G endpoint");

\\ Direct c=16 endpoint.
Qaa=9*a^2-68*a+144;
x16=(9*a-32)/96;
lm16=-(19*a-64)/32;
mu16=15*a/1024-15/256;
for(i=1,5,
  vv=subst(subst(subst(subst(subst(subst(E[i],b,5/24),c,16),
       y,1),x,x16),lm,lm16),mu,mu16);
  checkzero(numerator(vv)%Qaa,
            "c=16 contact modulo quadratic")
);
for(i=1,3,
  ff=subst(subst(subst([alpha,beta,gam][i],a,0),b,5/24),c,16)
     /(p*q^2);
  checkzero(poldegree(denominator(ff),p),"c=16 a=0 extra q");
  checkzero(poldegree(denominator(ff),q),"c=16 a=0 extra q")
);
S16=subst(subst(subst(subst(subst(S,b,5/24),c,16),x,x16),y,1),a,a);
H416=[subst(subst(P,b,5/24),c,16),
      subst(subst(Q,b,5/24),c,16),0];
H316=[r*S16[1],r*S16[2],subst(subst(R,b,5/24),c,16)];
H216=[-lm16*r^2/2,-mu16*r^2/2,r*S16[3]];
W16=matdet(zz*jacmap(H216)+zz^2*jacmap(H316)+zz^3*jacmap(H416));
co16=cf(polcoef(polcoef(W16,5,zz),2,r),3,0);
checkzero((co16%Qaa)-5*(3*a-10)/16,
          "c=16 E5 obstruction");
checkzero(polresultant(Qaa,3*a-10,a)-156,
          "c=16 obstruction coprimality");

print("PASS independent PARI mixed {1,1} reconstruction");
}
quit;
