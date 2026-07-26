\\ Independent PARI/GP reconstruction of the decisive BB coefficient and
\\ the two structural E7-origin E6 blocks.  This shares no SymPy code.

FAULT = if(getenv("D3_AUDIT_FAULT") == "1", 1, 0);

fail(msg) =
{
  print("FAIL ", msg);
  quit(1);
};

check0(value, msg) =
{
  if(value != 0, fail(Str(msg, ": residual=", value)));
  print("PASS ", msg);
};

coeffmon(f, ez, ep, eq, er) =
{
  my(g=f);
  for(i=1,ez,g=deriv(g,z));
  for(i=1,ep,g=deriv(g,p));
  for(i=1,eq,g=deriv(g,q));
  for(i=1,er,g=deriv(g,r));
  g=subst(subst(subst(subst(g,z,0),p,0),q,0),r,0);
  g/(ez!*ep!*eq!*er!);
};

coeffz(f, ez) =
{
  my(g=f);
  for(i=1,ez,g=deriv(g,z));
  subst(g,z,0)/ez!;
};

jac2(f,g) = deriv(f,p)*deriv(g,q)-deriv(f,q)*deriv(g,p);

det3(M) =
{
  M[1,1]*(M[2,2]*M[3,3]-M[2,3]*M[3,2])
 -M[1,2]*(M[2,1]*M[3,3]-M[2,3]*M[3,1])
 +M[1,3]*(M[2,1]*M[3,2]-M[2,2]*M[3,1]);
};

weighted(h,U,V,T) =
{
  my(P=h*p^2,Q=h*q^2,H2,H3,H4,M);
  H2=[A,B,T];
  H3=[U,V,p^2*q];
  H4=[P,Q,0];
  M=matrix(3,3,i,j,
      L[i,j]
     +z*deriv(H2[i],[p,q,r][j])
     +z^2*deriv(H3[i],[p,q,r][j])
     +z^3*deriv(H4[i],[p,q,r][j]));
  det3(M);
};

t='t; p='p; q='q; r='r; z='z; k='k;
tt=Mod(t,t^2+5);

u0='u0; u1='u1; u2='u2; u3='u3;
v0='v0; v1='v1; v2='v2; v3='v3;
t0='t0; t1='t1; t2='t2;
a0='a0; a1='a1; a2='a2; a3='a3; a4='a4; a5='a5;
b0='b0; b1='b1; b2='b2; b3='b3; b4='b4; b5='b5;
l0='l0; l1='l1; l2='l2; l3='l3; l4='l4;
l5='l5; l6='l6; l7='l7; l8='l8;

U0=u0*p^3+u1*p^2*q+u2*p*q^2+u3*q^3;
V0=v0*p^3+v1*p^2*q+v2*p*q^2+v3*q^3;
T0=t0*p^2+t1*p*q+t2*q^2;
A=a0*p^2+a1*p*q+a2*p*r+a3*q^2+a4*q*r+a5*r^2;
B=b0*p^2+b1*p*q+b2*p*r+b3*q^2+b4*q*r+b5*r^2;
L=[l0,l1,l2;l3,l4,l5;l6,l7,l8];

\\ Full D3-BB-21 E7 parameterization:
\\ S=aa*p+bb*q+cc*r,
\\ U_r=p(8S-kk*p)/5, V_r=kk*q^2, T_r=S.
aa='aa; bb='bb; cc='cc; kk='kk;
S=aa*p+bb*q+cc*r;
Ufull=U0+p*r*((8*aa-kk)*p+8*bb*q+4*cc*r)/5;
Vfull=V0+kk*q^2*r;
Tfull=T0+(aa*p+bb*q)*r+cc*r^2/2;
Dfull=weighted(p*q,Ufull,Vfull,Tfull);
rru='rru; rrv='rrv;
alphaBB=-5*p^2*q^3;
betaBB=-p^4*q;
check0(coeffmon(alphaBB*rru+betaBB*rrv,0,2,3,0)+5*rru,"BB zero r2-kernel first pivot");
check0(coeffmon(alphaBB*rru+betaBB*rrv,0,4,1,0)+rrv,"BB zero r2-kernel second pivot");
check0(deriv(Ufull,r)-p*(8*S-kk*p)/5,"BB full U_r parameterization");
check0(deriv(Vfull,r)-kk*q^2,"BB full V_r parameterization");
check0(deriv(Tfull,r)-S,"BB full T_r parameterization");
check0(coeffz(Dfull,9),"BB full arbitrary-binary E9");
check0(coeffz(Dfull,8),"BB full arbitrary-binary E8");
check0(coeffz(Dfull,7),"BB full arbitrary-binary E7");

C=12*aa^2-8*aa*kk+3*kk^2;
check0(coeffmon(Dfull,6,1,2,3)-12*cc^2/5,"BB E6 c-square");
check0(subst(coeffmon(Dfull,6,1,4,1),cc,0)-24*bb^2/5,"BB E6 b-square after c=0");
e6conic=subst(subst(coeffmon(Dfull,6,3,2,1),cc,0),bb,0);
check0(e6conic-2*C/5,"BB E6 conic after b=c=0");
e6v0=subst(subst(coeffmon(Dfull,6,6,0,0),cc,0),bb,0);
e6u3=subst(subst(coeffmon(Dfull,6,1,5,0),cc,0),bb,0);
check0(e6v0-3*v0*(3*aa-kk)/5,"BB E6 v0 endpoint");
check0(e6u3-3*u3*(2*kk-aa),"BB E6 u3 endpoint");
check0(subst(subst(coeffmon(Dfull,6,4,1,1),cc,0),bb,0)+2*b5,"BB E6 b5 pivot");
check0(subst(subst(coeffmon(Dfull,6,2,3,1),cc,0),bb,0)+10*a5,"BB E6 a5 pivot");

\\ Complete ordinary E6 pivots.  Only C and the two endpoint products remain.
b2p=aa*v1;
b4p=(-(48*aa-16*kk)*t0+(45*aa-15*kk)*u0+(aa+3*kk)*v2)/5;
a4p=((16*aa-32*kk)*t2+(5*aa+15*kk)*u2)/25;
a2p=(-(16*aa+8*kk)*t1+25*aa*u1+(-3*aa+6*kk)*v3+40*l8)/25;
Dp=subst(subst(subst(subst(Dfull,cc,0),bb,0),a5,0),b5,0);
Dp=subst(subst(subst(subst(Dp,b2,b2p),b4,b4p),a4,a4p),a2,a2p);
E6p=coeffz(Dp,6);
E6expected=2*C*p^3*q^2*r/5+3*v0*(3*aa-kk)*p^6/5+3*u3*(2*kk-aa)*p*q^5;
check0(E6p-E6expected,"BB complete E6 pivot replay");

cfull=coeffmon(Dp,5,2,1,2);
expected=2*aa*kk*(8*aa-kk)/5;
if(FAULT,expected=-expected);
check0(cfull-expected,"BB full decisive E5 coefficient");
check0(polresultant(C,aa*kk*(8*aa-kk),kk)-1680*aa^6,"BB resultant in kk");
check0(polresultant(C,aa*kk*(8*aa-kk),aa)-420*kk^6,"BB resultant in aa");

\\ The earlier conjugate line is a specialization of the full calculation.
cconj=subst(subst(cfull,aa,3*k),kk,(4+2*tt)*k);
check0(cconj-24*k^3*(25+8*tt)/5,"BB conjugate specialization");
check0(norm(24/5*(25+8*tt))-108864/5,"BB decisive coefficient norm");

\\ At the E7 origin, arbitrary U0,V0,T0 disappear from E6.
Dbb0=weighted(p*q,U0,V0,T0);
E6bb=coeffz(Dbb0,6);
Pbb=p^3*q; Qbb=p*q^3; R=p^2*q;
structbb=jac2(Qbb,R)*deriv(A,r)-jac2(Pbb,R)*deriv(B,r)+jac2(Pbb,Qbb)*l8;
check0(E6bb-structbb,"BB origin structural E6 identity");
check0(coeffmon(Dbb0,6,3,3,0)-(-5*a2+8*l8),"BB origin a2/l33 pivot");
check0(coeffmon(Dbb0,6,2,4,0)+5*a4,"BB origin a4 pivot");
check0(coeffmon(Dbb0,6,5,1,0)+b2,"BB origin b2 pivot");
check0(coeffmon(Dbb0,6,4,2,0)+b4,"BB origin b4 pivot");
check0(coeffmon(Dbb0,6,2,3,1)+10*a5,"BB origin a5 pivot");
check0(coeffmon(Dbb0,6,4,1,1)+2*b5,"BB origin b5 pivot");

Dbs0=weighted(p^2,U0,V0,T0);
E6bs=coeffz(Dbs0,6);
Pbs=p^4; Qbs=p^2*q^2;
structbs=jac2(Qbs,R)*deriv(A,r)-jac2(Pbs,R)*deriv(B,r)+jac2(Pbs,Qbs)*l8;
check0(E6bs-structbs,"BS origin structural E6 identity");
check0(coeffmon(Dbs0,6,4,2,0)+2*a2,"BS origin a2 pivot");
check0(coeffmon(Dbs0,6,3,3,0)+2*a4,"BS origin a4 pivot");
check0(coeffmon(Dbs0,6,3,2,1)+4*a5,"BS origin a5 pivot");
check0(coeffmon(Dbs0,6,6,0,0)+4*b2,"BS origin b2 pivot");
check0(coeffmon(Dbs0,6,5,1,0)-(-4*b4+8*l8),"BS origin b4/l33 pivot");
check0(coeffmon(Dbs0,6,5,0,1)+8*b5,"BS origin b5 pivot");

print("D3_CONSTRUCTION_INDEPENDENT_PARI_PASS");
quit(0);
