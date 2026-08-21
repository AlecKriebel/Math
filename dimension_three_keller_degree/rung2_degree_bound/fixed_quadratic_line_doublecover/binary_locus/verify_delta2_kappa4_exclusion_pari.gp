\\ Independent PARI/GP replay of the full doubled-root kappa=4 solve.

p='p; q='q; r='r; z='z;
vars=[p,q,r];
jacmat(H)=matrix(3,3,i,j,deriv(H[i],vars[j]));
check_zero(value,message)={if(value!=0,error(Str("FAIL: ",message,"; residual = ",value)))};
hc(f,degree,index)=polcoeff(subst(f,q,1),degree-index,p);

aa='aa; bb='bb; kk='kk; mm='mm; nn='nn; la='la;
u0='u0; u1='u1; u2='u2; u3='u3;
v0='v0; v1='v1; v2='v2; v3='v3;
tt0='tt0; tt1='tt1; tt2='tt2;
x0='x0; x1='x1; x2='x2; x3='x3; x4='x4; x5='x5;
y0='y0; y1='y1; y2='y2; y3='y3; y4='y4; y5='y5;
l0='l0; l1='l1; l2='l2; l3='l3; l4='l4;
l5='l5; l6='l6; l7='l7; l8='l8;

h=(p+q)^2;
dd=(5*bb-6*aa)/3;
R=aa*p^3+bb*p^2*q+3*dd*p*q^2/2+dd*q^3;
Nu=6*p+4*q;
Nv=-2*q;
Nt=6*aa-bb;
W=mm*p+nn*q;
S=kk*r^2/2+W*r;
U0=u0*p^3+u1*p^2*q+u2*p*q^2+u3*q^3;
V0=v0*p^3+v1*p^2*q+v2*p*q^2+v3*q^3;
T0=tt0*p^2+tt1*p*q+tt2*q^2;
A0=x0*p^2+x1*p*q+x2*q^2;
B0=y0*p^2+y1*p*q+y2*q^2;
H4=[h*p^2,h*q^2,0]~;
H3=[U0+Nu*S,V0+Nv*S,R]~;
H2=[A0+r*(x3*p+x4*q)+x5*r^2,B0+r*(y3*p+y4*q)+y5*r^2,T0+Nt*S]~;
L0=[l0,l1,l2;l3,l4,l5;l6,l7,l8];
D=matdet(L0+z*jacmat(H2)+z^2*jacmat(H3)+z^3*jacmat(H4));
E8=polcoeff(D,8,z);
E7=polcoeff(D,7,z);
E6=polcoeff(D,6,z);
E5=polcoeff(D,5,z);
E4=polcoeff(D,4,z);
check_zero(E8,"E8");
check_zero(E7,"E7");
expected=-kk^2*(6*aa*p^3-18*aa*p*q^2-12*aa*q^3-4*bb*p^3-18*bb*p^2*q-33*bb*p*q^2-22*bb*q^3);
check_zero(polcoeff(E6,3,r)-expected,"E6 r^3");
print("PASS PARI full E8/E7 and E6 r^3");

E6r=polcoeff(subst(E6,kk,0),1,r);
check_zero(hc(E6r,5,0)-4*(3*aa-2*bb)*(-mm^2+y5),"E6 r p^5");
check_zero(hc(E6r,5,5)-4*nn^2*(6*aa+11*bb),"E6 r q^5");
special=substvec(E6r,[aa,y5],[-11*bb/6,mm^2]);
check_zero(hc(special,5,4)-16*bb*(-4*mm^2+x5),"special E6 coefficient");
check_zero(hc(special,5,3)-4*bb*(-56*mm^2+9*nn^2+14*x5),"special E6 second coefficient");
print("PASS PARI E6 r endpoint mutations");

E6high=substvec(E6,[kk,mm,nn,x5,y5],[0,0,0,0,0]);
E6done=substvec(E6high,[x3,x4,y3,y4,l8],[6*la,4*la,0,-2*la,(6*aa-bb)*la]);
check_zero(E6done,"complete E6 kernel");
E5high=substvec(E5,[kk,mm,nn,x5,y5,x3,x4,y3,y4,l8],[0,0,0,0,0,6*la,4*la,0,-2*la,(6*aa-bb)*la]);
E5zero=subst(E5high,la,0);
Mzero=matrix(6,2,i,j,if(j==1,polcoeff(hc(E5zero,5,i-1),1,l2),polcoeff(hc(E5zero,5,i-1),1,l5)));
check_zero(matdet(vecextract(Mzero,[1,2],[1,2]))-12*aa*(3*aa-2*bb),"lambda zero first rank minor");
check_zero(matdet(vecextract(Mzero,[1,3],[1,2]))-4*(3*aa-2*bb)*(9*aa+bb),"lambda zero second rank minor");
print("PASS PARI complete E6 kernel and lambda-zero guards");

L2sol=-12*la*u0+14*la*u1-15*la*u2+27*la*u3/2;
L5sol=6*la*u0-5*la*u1+6*la*u2-6*la*u3+4*la*v1-3*la*v3;
V0sol=u0-5*u1/6+u2-u3+5*v1/6-v3/2;
V2sol=-u2/2+3*u3/4+3*v3/2;
commonvars=[aa,l2,l5,tt0,tt1,v0,v2];
commonvals=[bb/6,L2sol,L5sol,tt2/4,tt2,V0sol,V2sol];
E5done=substvec(E5high,commonvars,commonvals);
check_zero(E5done,"residual complete E5 solve");
E4high=substvec(E4,[kk,mm,nn,x5,y5,x3,x4,y3,y4,l8],[0,0,0,0,0,6*la,4*la,0,-2*la,(6*aa-bb)*la]);
E4done=substvec(E4high,commonvars,commonvals);
check_zero(polcoeff(E4done,1,r)-6*bb*la^2*(p+2*q)^3,"decisive E4 r coefficient");
print("PASS PARI residual E5 solve and E4 contradiction");

print("ALL PARI KAPPA=4 DELTA=2 EXCLUSION CHECKS PASSED");
