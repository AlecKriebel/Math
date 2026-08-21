\\ Independent PARI/GP replay of the unmarked c0=0 boundary.

default(parisizemax,512000000);
allocatemem(128000000);

checkzero(value,message) =
{
  if(value != 0,
    print(Str("FAIL: ",message));
    quit(1)
  );
};
checktrue(value,message) =
{
  if(!value,
    print(Str("FAIL: ",message));
    quit(1)
  );
};
jac2(f,g) = deriv(f,p)*deriv(g,q)-deriv(f,q)*deriv(g,p);
jac3(f,g,h) = matdet([deriv(f,p),deriv(f,q),deriv(f,r);deriv(g,p),deriv(g,q),deriv(g,r);deriv(h,p),deriv(h,q),deriv(h,r)]);
jacmap(V) = matrix(3,3,i,j,deriv(V[i],[p,q,r][j]));
cf(f,ep,eq) = polcoef(polcoef(f,eq,q),ep,p);

{
P0=p*(p*q^2+aa*q^3);
Q0=p*(p^3+p^2*q+bb*q^3);
R0=p*q^2+dd*q^3;
alpha0=jac2(Q0,R0);
beta0=-jac2(P0,R0);
gam0=jac2(P0,Q0);
Nu0=(deriv(P0,q)-deriv(P0,p)/4)/q;
Nv0=(deriv(Q0,q)-deriv(Q0,p)/4)/q;
Nt0=(deriv(R0,q)-deriv(R0,p)/4)/q;
curv0=jac3(P0,r*Nv0,r*Nt0)
      +jac3(r*Nu0,Q0,r*Nt0)
      +jac3(r*Nu0,r*Nv0,R0);
K0=polcoef(curv0,1,r);
res=K0-lm*alpha0-mu*beta0;
dsol=(4*aa-1)/4;
lmsol=(4*aa-1)/2;
E=vector(6,i,subst(subst(cf(res,5-(i-1),i-1),dd,dsol),lm,lmsol));
checkzero(E[1],"first contact solve");
checkzero(E[2],"second contact solve");
checkzero(E[3]+3*(32*aa^2-30*aa-16*bb+5)/8,
          "third contact solve");

bsol=(32*aa^2-30*aa+5)/16;
musol=-(192*aa^3-368*aa^2+216*aa-35)/32;
Apoly=640*aa^3-1056*aa^2+480*aa-65;
Bpoly=128*aa^3-96*aa^2+5;
checkzero(subst(subst(E[5],bb,bsol),mu,musol)
          +3*(2*aa-1)*Apoly/128,"first residual factor");
checkzero(subst(subst(E[6],bb,bsol),mu,musol)/(4*aa-1)
          +9*(2*aa-1)*Bpoly/512,"second residual factor");
checktrue(polresultant(Apoly,Bpoly,aa)==-11324620800,
          "cubic residual resultant");

\\ Endpoint c0=0 charts before b1,c2 normalization.
Pg=p*(p*q^2+aa*q^3);
Qg=p*(p^3+b1g*p^2*q+bb*q^3);
Rg=c2g*p*q^2+dd*q^3;
ag=jac2(Qg,Rg);
bg=-jac2(Pg,Rg);
gg=jac2(Pg,Qg);
Nug=(deriv(Pg,q)-b1g*deriv(Pg,p)/4)/q;
Nvg=(deriv(Qg,q)-b1g*deriv(Qg,p)/4)/q;
Ntg=(deriv(Rg,q)-b1g*deriv(Rg,p)/4)/q;
curvg=jac3(Pg,r*Nvg,r*Ntg)
     +jac3(r*Nug,Qg,r*Ntg)
     +jac3(r*Nug,r*Nvg,Rg);
resg=polcoef(curvg,1,r)-lm*ag-mu*bg;
checkzero(cf(resg,5,0)+6*(4*aa*c2g-b1g*c2g-4*dd),
          "general c0=0 endpoint coefficient");
ae=subst(subst(subst(ag,b1g,0),c2g,1),dd,aa);
be=subst(subst(subst(bg,b1g,0),c2g,1),dd,aa);
ge=subst(subst(subst(gg,b1g,0),c2g,1),dd,aa);
ae=subst(ae,bb,0);
be=subst(be,bb,0);
ge=subst(ge,bb,0);
lineg=2*p+3*aa*q;
checkzero(ae-4*p^3*q*lineg,"endpoint alpha extra line");
checkzero(be+q^3*(p+aa*q)*lineg,"endpoint beta extra line");
checkzero(ge+4*p^4*q*lineg,"endpoint gamma extra line");

P=subst(subst(P0,aa,1/2),bb,-1/8);
Q=subst(subst(Q0,aa,1/2),bb,-1/8);
R=subst(R0,dd,1/4);
alpha=jac2(Q,R);
beta=-jac2(P,R);
gam=jac2(P,Q);
checkzero(alpha/q-(8*p^2+4*p*q+q^2)*(32*p^2+16*p*q-3*q^2)/32,
          "exact alpha factor");
checkzero(beta/q+q^2*(16*p^2+8*p*q+3*q^2)/8,
          "exact beta factor");
checkzero(gam/q+p^2*(2*p+q)^2*(4*p+q)/2,
          "exact gamma factor");
checktrue(subst(16*p^2+8*p*q+3*q^2,p,-q/2)==3*q^2,
          "first gamma-line coprimality");
checktrue(subst(16*p^2+8*p*q+3*q^2,p,-q/4)==2*q^2,
          "second gamma-line coprimality");

Nu=(16*p^2+8*p*q-q^2)/8;
Nv=-(24*p^2+12*p*q-q^2)/32;
Nt=(4*p+q)/2;
u1=3*u0/4+8*ww/9;
u2=u0/8+2*ww/3;
v0=16*ww/9+8*v2;
v1=ww+6*v2;
t1=8*ww/9;
U=u0*p^3+u1*p^2*q+u2*p*q^2+r*Nu;
V=v0*p^3+v1*p^2*q+v2*p*q^2+r*Nv;
T=t1*p*q+r*Nt;

x0=-8*l13+2*u0*ww/9+16*x2;
x1=-4*l13+u0*ww/18+16*ww^2/81+8*x2;
y0=-8*l23+16*v2*ww/9+28*ww^2/81+16*y2;
y1=-4*l23+4*v2*ww/9+2*ww^2/81+8*y2;
x3=-u0/8+4*ww/9;
x4=-u0/32-ww/9;
y3=-ww/3-v2;
y4=-ww/72-v2/4;
A2=x0*p^2+x1*p*q+x2*q^2+r*(x3*p+x4*q)-r^2/4;
B2=y0*p^2+y1*p*q+y2*q^2+r*(y3*p+y4*q)+5*r^2/64;

l31=4*l32+64*ww^2/81;
l33=-4*ww/9;
L=[l11,l12,l13;l21,l22,l23;l31,l32,l33];
H2=[A2,B2,T];
H3=[U,V,R];
H4=[P,Q,0];
weighted=matdet(L+zz*jacmap(H2)+zz^2*jacmap(H3)+zz^3*jacmap(H4));
checkzero(polcoef(weighted,8,zz),"weighted E8");
checkzero(polcoef(weighted,7,zz),"weighted E7");
checkzero(polcoef(weighted,6,zz),"weighted E6");
checkzero(polcoef(weighted,5,zz),"weighted E5");

M1=9*l11-36*l12+16*ww*l13;
M2=9*l21-36*l22+16*ww*l23;
expected=2*M1*(p^4+p^3*q)/9
        +(9*M1-8*M2)*p^2*q^2/144
        +(M1-8*M2)*p*q^3/288
        -(M1+4*M2)*q^4/384;
checkzero(polcoef(weighted,4,zz)-expected,"weighted E4 covariants");

kernel=[9,-36,16*ww]~;
checkzero((L*kernel)[1]-M1,"first kernel covariant");
checkzero((L*kernel)[2]-M2,"second kernel covariant");
checkzero((L*kernel)[3],"third kernel identity");
checktrue(kernel[1]!=0,"kernel nonzero");

print("PASS independent PARI c0=0 contact/lower replay");
}
quit;
