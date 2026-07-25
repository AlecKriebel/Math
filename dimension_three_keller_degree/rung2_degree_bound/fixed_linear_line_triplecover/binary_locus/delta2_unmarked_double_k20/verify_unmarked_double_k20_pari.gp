\\ Independent PARI/GP replay of the full unmarked-double {2,0} component.

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
jacmap(V) = matrix(3,3,i,j,deriv(V[i],[p,q,r][j]));
cf(f,ep,eq) = polcoef(polcoef(f,eq,q),ep,p);
cfr(f,ep,eq,er) = polcoef(polcoef(polcoef(f,er,r),eq,q),ep,p);
subslist(f,variables,values) =
{
  my(g=f);
  for(i=1,#variables,g=subst(g,variables[i],values[i]));
  g
};

{
P=p*q^3;
Q=p*(p^3+b*p^2*q+3*b^2*p*q^2/8);
R=c0*(p^3+3*b*p^2*q/4+3*b^2*p*q^2/16)+c3*q^3;
alpha=jac2(Q,R); beta=-jac2(P,R); gam=jac2(P,Q);
N=[(deriv(P,q)-b*deriv(P,p)/4)/q^2,
   (deriv(Q,q)-b*deriv(Q,p)/4)/q^2,
   (deriv(R,q)-b*deriv(R,p)/4)/q^2]~;
checkzero(N[1]-(3*p-b*q/4),"first exceptional tangent");
checkzero(N[2]+3*b^3*p/16,"second exceptional tangent");
checkzero(N[3]+3*(b^3*c0-64*c3)/64,
          "third exceptional tangent");
checkzero(alpha*N[1]+beta*N[2]+gam*N[3],
          "exceptional syzygy");
checkzero(deriv(P,p)-deriv(P,p),"PARI derivative sanity");
for(i=1,3,
  ff=[P,Q,R][i];
  checkzero(deriv(ff,q)-q^2*N[i]-b*deriv(ff,p)/4,
            "determinant-q2 gradient reconstruction")
);

C=(N[3]*jac2(P,N[2])+N[3]*jac2(N[1],Q)
  -N[2]*jac2(N[1],R)+N[1]*jac2(N[2],R))/2;
Cexpected=-3*b*(3*b^5*c0*p*q^2+12*b^4*c0*p^2*q
  +16*b^3*c0*p^3-48*b^3*c3*q^3-768*b^2*c3*p*q^2
  -3072*b*c3*p^2*q-4096*c3*p^3)/2048;
checkzero(C-Cexpected,"exceptional curvature");
checkzero(subst(polcoef(Cexpected,3,q),c3,b^3*c0/256)
          -9*b^7*c0/32768,
          "curvature cannot vanish on nonzero R");

f=mm*p+nn*q;
S=f*N;
K=polcoef(jac3(P,r*S[2],r*S[3])
         +jac3(r*S[1],Q,r*S[3])
         +jac3(r*S[1],r*S[2],R),1,r);
res=K-lm*alpha-mu*beta;
E=vector(6,i,cf(res,5-(i-1),i-1));
TT=b^3*c0-256*c3;
checkzero(E[1]+3*b*mm^2*TT/64,"first contact coefficient");
checkzero(E[2]+3*b*mm*(3*b*mm+8*nn)*TT/256,
          "second contact coefficient");
for(i=1,6,
  vv=subst(subst(subst(E[i],mm,0),lm,b*nn^2),
           mu,-3*b^4*nn^2/64);
  checkzero(vv,"universal nq contact")
);
\\ On TT=0 the same lambda,mu make the remaining equations literal
\\ nonzero multiples of m^2 and mn.
e4=subst(subst(subst(subst(E[4],c3,b^3*c0/256),
    lm,b*nn^2),mu,-3*b^4*nn^2/64),mm,mm);
e5=subst(subst(subst(subst(E[5],c3,b^3*c0/256),
    lm,b*nn^2),mu,-3*b^4*nn^2/64),mm,mm);
checkzero(e4-9*b^7*c0*mm^2/16384,
          "TT=0 forces m^2");
checkzero(e5-9*b^7*c0*mm*nn/8192,
          "TT=0 forces mn");

\\ Top-only E5 obstruction for the nq contact.
Snq=subst(S,mm,0);
H4=[P,Q,0];
H3=[r*Snq[1],r*Snq[2],R];
H2=[-b*nn^2*r^2/2,3*b^4*nn^2*r^2/128,r*Snq[3]];
weighted=matdet(zz*jacmap(H2)+zz^2*jacmap(H3)+zz^3*jacmap(H4));
E5=polcoef(polcoef(weighted,5,zz),2,r);
checkzero(cf(E5,3,0)-3*b*nn^3*TT/64,
          "E5 p3 obstruction");
checkzero(cf(E5,2,1)-9*b^2*nn^3*TT/256,
          "E5 p2q obstruction");
checkzero(cf(E5,1,2)-9*b^3*nn^3*TT/1024,
          "E5 pq2 obstruction");
checkzero(cf(E5,0,3)+9*b^4*c3*nn^3/64,
          "E5 q3 obstruction");

\\ Zero-contact endpoint N3=0.  Normalize b=c0=1,c3=1/64,
\\ solve E5 explicitly with seven free parameters, and reconstruct E4.
P0=p*q^3;
Q0=p*(p^3+p^2*q+3*p*q^2/8);
R0=p^3+3*p^2*q/4+3*p*q^2/16+q^3/64;
N01=3*p-q/4; N02=-3*p/16;
u0=64*u3-40*v0/3+32*v1/3+1024*v3/3
   -64*l13/(3*et)-1024*l23/(9*et);
u1=48*u3+2*v0-8*v1+256*v3
   -16*l13/et-256*l23/(3*et);
u2=12*u3+8*v1/3-128*v3
   -4*l13/et+128*l23/(3*et);
v2=12*v3-4*l23/et;
w0=16*w2; w1=8*w2;
U=u0*p^3+u1*p^2*q+u2*p*q^2+u3*q^3;
V=v0*p^3+v1*p^2*q+v2*p*q^2+v3*q^3;
T0=w0*p^2+w1*p*q+w2*q^2;
A0=aa0*p^2+aa1*p*q+aa2*q^2;
B0=bb0*p^2+bb1*p*q+bb2*q^2;
H40=[P0,Q0,0];
H30=[U,V,R0];
H20=[A0+et*r*N01,B0+et*r*N02,T0];
L=[l11,l12,l13;l21,l22,l23;l31,l32,0];
W0=matdet(L+zz*jacmap(H20)+zz^2*jacmap(H30)+zz^3*jacmap(H40));
checkzero(polcoef(W0,5,zz),"solved zero-contact E5");
E4r=polcoef(polcoef(W0,4,zz),1,r);
checkzero(E4r-9*et^2*R0/64,
          "zero-contact E4 obstruction");

\\ Boundary b1=0.  Exact gcd q^2 forces the q^3 coefficient of R
\\ nonzero; normalize it to one.
Pb=p*q^3;
Qb=p^4;
Rb=dd*p^3+q^3;
alphab=jac2(Qb,Rb);
betab=-jac2(Pb,Rb);
gammab=jac2(Pb,Qb);
checkzero(alphab-12*p^3*q^2,"b1=0 alpha");
checkzero(betab-3*q^2*(3*dd*p^3-q^3),"b1=0 beta");
checkzero(gammab+12*p^4*q^2,"b1=0 gamma");

\\ Complete E7 parameterization: V_r=0 and U_r=p*T_r.
bf=bm*p+bn*q;
BU0=bu0*p^3+bu1*p^2*q+bu2*p*q^2+bu3*q^3;
BV0=bv0*p^3+bv1*p^2*q+bv2*p*q^2+bv3*q^3;
BT0=bw0*p^2+bw1*p*q+bw2*q^2;
BA0=baa0*p^2+baa1*p*q+baa2*q^2;
BB0=bbb0*p^2+bbb1*p*q+bbb2*q^2;
BU=BU0+3*p*bf*r+3*br*p*r^2/2;
BV=BV0;
BT=BT0+3*bf*r+3*br*r^2/2;
BA=BA0+r*(bxp*p+bxq*q)+bxrr*r^2;
BB=BB0+r*(byp*p+byq*q)+byrr*r^2;
checkzero(alphab*deriv(BU,r)+betab*deriv(BV,r)
          +gammab*deriv(BT,r),
          "b1=0 complete-E7 parameter family");

BH4=[Pb,Qb,0];
BH3=[BU,BV,Rb];
BH2=[BA,BB,BT];
BL=[be0,be1,be2;be3,be4,be5;be6,be7,be8];
BW=matdet(BL+zz*jacmap(BH2)+zz^2*jacmap(BH3)+zz^3*jacmap(BH4));
BE8=polcoef(BW,8,zz);
BE7=polcoef(BW,7,zz);
BE6=polcoef(BW,6,zz);
BE5=polcoef(BW,5,zz);
BE4=polcoef(BW,4,zz);
checkzero(BE8,"b1=0 E8");
checkzero(BE7,"b1=0 E7");

BC=-3*dd*be5+3*dd*be8*bv3-4*be2+4*be8*bu3;
BD=-be5+be8*bv3;
BArel=-3*dd*be4+3*dd*be7*bv3-4*be1+4*be7*bu3;
BBrel=-be4+be7*bv3;

\\ br != 0 chart.
rv=[bv1,bv2,bu1,bu2,byp,byq,byrr,bxp,bxq,bxrr];
rw=[0,0,bw1,bw2,3*bm*bv3,3*bn*bv3,3*br*bv3/2,
    be8+3*bm*bu3,3*bn*bu3,3*br*bu3/2];
checkzero(subslist(BE6,rv,rw),"b1=0 rho chart E6");
rlv=[bbb1,bbb2,baa1,baa2];
rlw=[bv3*bw1,bv3*bw2,be7+bu3*bw1,bu3*bw2];
Br5=subslist(subslist(BE5,rv,rw),rlv,rlw);
checkzero(Br5-(-3*BC*p^3*q^2+3*BD*q^5),
          "b1=0 rho chart E5 columns");
Br4=subslist(subslist(subslist(BE4,rv,rw),rlv,rlw),
             [be5,be2],[be8*bv3,be8*bu3]);
checkzero(polcoef(Br4,1,r)
          -(3*br*BArel*p^3-3*br*BBrel*q^3),
          "b1=0 rho chart E4 columns");

\\ br=0,bm!=0 chart; scale bm=1 and write bn=bt.
mv=[br,bm,bn,bv2,bu1,bu2,byp,byq,bxp,bxq,bxrr,byrr];
mw=[0,1,bt,-bt*bv1/2,bw1-3*dd*bv1/4,
    bw2+3*dd*bt*bv1/8,3*bv3-bt^2*bv1,3*bt*bv3,
    be8+3*bu3+3*dd*bt^2*bv1/4,3*bt*bu3-bv1/4,0,0];
checkzero(subslist(BE6,mv,mw),"b1=0 m chart E6");
Bm5=subslist(BE5,mv,mw);
checkzero(cfr(Bm5,4,0,1)-12*bv1,
          "b1=0 m chart forces v1");
mlv=[bv1,baa1,baa2,bbb1,bbb2];
mlw=[0,be7+bu3*bw1,bu3*bw2,bv3*bw1,bv3*bw2];
Bm5r=subslist(Bm5,mlv,mlw);
checkzero(Bm5r-(-3*BC*p^3*q^2+3*BD*q^5),
          "b1=0 m chart E5 columns");
Bm4=subslist(subslist(subslist(BE4,mv,mw),mlv,mlw),
             [be5,be2],[be8*bv3,be8*bu3]);
checkzero(Bm4-(3*BArel*p^4+3*bt*BArel*p^3*q
                   -3*BBrel*p*q^3-3*bt*BBrel*q^4),
          "b1=0 m chart E4 columns");

\\ br=bm=0,bn!=0 chart; scale bn=1.
nv=[br,bm,bn,bv1,bu1,byp,byq,bxp,bxq,bxrr,byrr];
nw=[0,0,1,0,bw1,2*bv2,3*bv3,
    be8+2*bu2-2*bw2,3*bu3,0,0];
checkzero(subslist(BE6,nv,nw),"b1=0 n chart E6");
Bn5=subslist(BE5,nv,nw);
checkzero(cfr(Bn5,1,3,1)+6*bv2,
          "b1=0 n chart forces v2");
nlv=[bv2,bu2,baa1,baa2,bbb1,bbb2];
nlw=[0,bw2,be7+bu3*bw1,
     (be2-be8*bu3+2*bu3*bw2)/2,
     bv3*bw1,(be5-be8*bv3+2*bv3*bw2)/2];
checkzero(subslist(Bn5,nlv,nlw),"b1=0 n chart E5 solve");
Bn4=subslist(subslist(BE4,nv,nw),nlv,nlw);
checkzero(polcoef(Bn4,1,r)-(-3*BC*p^3+3*BD*q^3),
          "b1=0 n chart E4 column three");
Bn4c=subslist(Bn4,[be5,be2],[be8*bv3,be8*bu3]);
checkzero(Bn4c-(3*BArel*p^3*q-3*BBrel*q^4),
          "b1=0 n chart E4 column two");

\\ In every nonzero chart, the forced column relations make det L zero.
BLsing=subslist(matdet(BL),[be5,be2,be4,be1],
                 [be8*bv3,be8*bu3,be7*bv3,be7*bu3]);
checkzero(BLsing,"b1=0 forced singular linear part");

\\ Zero E7 contact.  E6 leaves only
\\ (A_r,B_r,ell_33)=be8*(p,0,1), a scalar multiple of N/3.
Bz6=subslist(BE6,[br,bm,bn],[0,0,0]);
Bz6s=subslist(Bz6,[bxp,bxq,bxrr,byp,byq,byrr],
                    [be8,0,0,0,0,0]);
checkzero(Bz6s,"b1=0 zero-contact E6 plane-field form");

print("PASS independent PARI unmarked-double {2,0} reconstruction");
}
quit;
