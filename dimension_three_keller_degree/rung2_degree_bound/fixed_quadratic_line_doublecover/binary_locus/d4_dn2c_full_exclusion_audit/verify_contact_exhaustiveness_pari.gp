\\ Independent PARI/GP audit of the D4-DN-2C contact projection.
\\
\\ This does not import either SymPy certificate.  It rebuilds the weighted
\\ determinant with all lower coefficients, proves the set-theoretic E6
\\ projection directly, and checks that its two planes have only the frozen
\\ common line and origin as boundary charts.

p='p; q='q; r='r; w='w;
coords=[p,q,r];

jacmat(H)=matrix(3,3,i,j,deriv(H[i],coords[j]));
c3(f,ip,iq,ir)=polcoeff(polcoeff(polcoeff(f,ir,r),iq,q),ip,p);
check_zero(value,message)=
{
  if(value!=0,
    print(Str("FAIL: ",message,"; residual = ",value));
    quit(1)
  )
};
check_true(value,message)=
{
  if(!value,
    print(Str("FAIL: ",message));
    quit(1)
  )
};

\\ Six contact parameters, in the coordinates of full_rebuild.
dd='dd; zz='zz; xx='xx; yy='yy; aa='aa; bb='bb;
U2=(dd+4*zz/3)*p+(2*dd+4*zz/3)*q;
V2=dd*q;
T2=zz;
U1=(xx+4*aa/3)*p^2+(yy+2*xx+4*(aa+bb)/3)*p*q+(2*yy+4*bb/3)*q^2;
V1=xx*p*q+yy*q^2;
T1=aa*p+bb*q;

\\ Every lower coefficient present in the source determinant.
u0='u0; u1='u1; u2='u2; u3='u3;
v0='v0; v1='v1; v2='v2; v3='v3;
t0='t0; t1='t1; t2='t2;
a0='a0; a1='a1; a2='a2; a3='a3; a4='a4; a5='a5;
b0='b0; b1='b1; b2='b2; b3='b3; b4='b4; b5='b5;
l0='l0; l1='l1; l2='l2; l3='l3; l4='l4; l5='l5;
l6='l6; l7='l7; l8='l8;

U0=u0*p^3+u1*p^2*q+u2*p*q^2+u3*q^3;
V0=v0*p^3+v1*p^2*q+v2*p*q^2+v3*q^3;
T0=t0*p^2+t1*p*q+t2*q^2;
A=a0*p^2+a1*p*q+a2*p*r+a3*q^2+a4*q*r+a5*r^2;
B=b0*p^2+b1*p*q+b2*p*r+b3*q^2+b4*q*r+b5*r^2;
L=[l0,l1,l2;l3,l4,l5;l6,l7,l8];

h=(p+q)^2;
P=h*p^2;
Q=h*q^2;
R=h*(p-2*q);
H4=[P,Q,0]~;
H3=[U0+r*U1+r^2*U2,V0+r*V1+r^2*V2,R]~;
H2=[A,B,T0+r*T1+r^2*T2]~;
D=matdet(L+w*jacmat(H2)+w^2*jacmat(H3)+w^3*jacmat(H4));

check_zero(polcoeff(D,9,w),"generic E9");
check_zero(polcoeff(D,8,w),"generic E8");
check_zero(polcoeff(D,7,w),"generic E7 kernel parameterization");
E6=polcoeff(D,6,w);

\\ The four lower-free r^3 equations force dd=zz=0 set-theoretically.
check_zero(c3(E6,3,0,3)+6*dd^2,"E6 p3r3");
check_zero(c3(E6,2,1,3)-16*zz*(3*dd+zz)/3,"E6 p2qr3");
check_zero(c3(E6,1,2,3)-2*(3*dd+4*zz)*(9*dd+4*zz)/3,"E6 pq2r3");
check_zero(c3(E6,0,3,3)-4*(3*dd+2*zz)^2/3,"E6 q3r3");

E60=subst(subst(E6,dd,0),zz,0);
eq=vector(6,i,c3(E60,i-1,6-i,1));

\\ Independently verify that only a5,b5 occur in this block.
otherlower=[u0,u1,u2,u3,v0,v1,v2,v3,t0,t1,t2,a0,a1,a2,a3,a4,b0,b1,b2,b3,b4,l0,l1,l2,l3,l4,l5,l6,l7,l8];
for(i=1,#eq,for(j=1,#otherlower,check_zero(deriv(eq[i],otherlower[j]),Str("E6 r1 unexpected lower variable row ",i," col ",j))));

vars=[a5,b5];
M=matrix(6,2,i,j,polcoeff(eq[i],1,vars[j]));
rhs=matrix(6,1,i,j,-substvec(eq[i],vars,[0,0]));
expectedM=[0,0;-12,24;-36,84;-36,108;-12,60;0,12];
check_zero(M-expectedM,"E6 r1 coefficient matrix");
for(i=1,6,check_zero(eq[i]-(M*vars~)[i]+rhs[i,1],Str("E6 r1 affine reconstruction row ",i)));

rows=[2,3];
Mp=vecextract(M,rows,[1,2]);
check_zero(matdet(Mp)+144,"constant E6 r1 pivot");
sol=matsolve(Mp,vector(2,i,rhs[rows[i],1])~);
res=vector(6,i,substvec(eq[i],vars,Vec(sol)));

ell=2*bb+3*yy;
f0=8*aa^2+24*aa*xx+27*xx^2-18*xx*yy+9*yy^2;
check_zero(res[1]-2*ell^2/3,"contact double hyperplane");
check_zero(res[2],"selected contact row 2");
check_zero(res[3],"selected contact row 3");
resH=vector(6,i,subst(res[i],bb,-3*yy/2));
check_zero(resH[1],"contact hyperplane row 1");
check_zero(resH[2],"contact hyperplane row 2");
check_zero(resH[3],"contact hyperplane row 3");
check_zero(resH[4]+f0/3,"contact quadratic row 4");
check_zero(resH[5]+2*f0/3,"contact quadratic row 5");
check_zero(resH[6]+f0/3,"contact quadratic row 6");

\\ Split the reduced quadratic and certify all chart boundaries.
ee='ee;
et=Mod(ee,ee^2+2);
lp=9*xx+(4+2*et)*aa+(-3+3*et)*yy;
lm=9*xx+(4-2*et)*aa+(-3-3*et)*yy;
check_zero(lp*lm-3*f0,"contact quadratic two-plane factorization");

k='k; s='s;
xplus=(-(4+2*et)*k+(3-3*et)*s)/9;
xminus=(-(4-2*et)*k+(3+3*et)*s)/9;
plusvars=[aa,bb,xx,yy];
plusvals=[k,-3*s/2,xplus,s];
minusvals=[k,-3*s/2,xminus,s];
check_zero(substvec(lp,plusvars,plusvals),"plus plane equation");
check_zero(substvec(lm,plusvars,minusvals),"minus plane equation");
delta=2*k+3*s;
check_zero(substvec(lm,plusvars,plusvals)+2*et*delta,"plus plane meets conjugate only on frozen line");
check_zero(substvec(lp,plusvars,minusvals)-2*et*delta,"minus plane meets conjugate only on frozen line");
check_zero(subst(xplus,s,-2*k/3)+2*k/3,"intersection x coordinate");
check_zero(subst(-3*s/2,s,-2*k/3)-k,"intersection b coordinate");

print("D4_DN2C_CONTACT_EXHAUSTIVENESS_DIRECT_PARI_PASS");
quit(0);
