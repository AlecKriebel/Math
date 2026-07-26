\\ Independent PARI/GP replay of the D4-DN-1CC contact calculation.

p='p; q='q; r='r; ww='ww;
vars=[p,q,r];
jacmat(H)=matrix(3,3,i,j,deriv(H[i],vars[j]));
jac2(f,g)=deriv(f,p)*deriv(g,q)-deriv(f,q)*deriv(g,p);
check_zero(value,message)={if(value!=0,error(Str("FAIL: ",message,"; residual = ",value)))};

h=(p+q)^2;
P=h*p^2;
Q=h*q^2;
R=(p+q)*(2*p^2+p*q+2*q^2);
H4=[P,Q,0]~;
alpha=jac2(Q,R);
beta=-jac2(P,R);
gam=jac2(P,Q);
check_zero(alpha+6*p*q*(p+q)^2*(2*p+3*q),"alpha");
check_zero(beta+6*p*q*(p+q)^2*(3*p+2*q),"beta");
check_zero(gam-8*p*q*(p+q)^4,"gamma");

\\ Complete E7 parameterization.
dd='dd; zet='zet; xx='xx; yy='yy; aaa='aaa; bbb='bbb;
U2=(8*zet/15-dd)*p+(4*zet/9-2*dd/3)*q;
V2=(4*zet/45+2*dd/3)*p+dd*q;
T2=zet;
U1=(24*aaa+4*bbb-45*xx+30*yy)*p^2/45+(12*aaa+16*bbb-18*xx-15*yy)*p*q/27+2*(2*bbb-3*yy)*q^2/9;
V1=2*(6*aaa-4*bbb+45*xx-30*yy)*p^2/135+xx*p*q+yy*q^2;
T1=aaa*p+bbb*q;
check_zero(alpha*U2+beta*V2+gam*T2,"E7 r-linear block");
check_zero(alpha*U1+beta*V1+gam*T1,"E7 constant block");

\\ E6 at r^3 forces dd=zet=0.
H3c=[r*U1+r^2*U2,r*V1+r^2*V2,R]~;
H2c=[0,0,r*T1+r^2*T2]~;
Dc=matdet(ww*jacmat(H2c)+ww^2*jacmat(H3c)+ww^3*jacmat(H4));
check_zero(polcoeff(Dc,7,ww),"contact E7 determinant");
E6c=polcoeff(Dc,6,ww);
E6r3=polcoeff(E6c,3,r);
expectedr3=20*(3*dd-2*zet)^2*q^3/27+2*(15*dd^2-16*dd*zet+8*zet^2)*p*q^2/3+2*(225*dd^2+56*zet^2)*p^2*q/45+4*(15*dd+2*zet)^2*p^3/135;
check_zero(E6r3-expectedr3,"complete E6 r^3 contact block");

\\ With dd=zet=0, eliminate the two r^2 coefficients of A,B.
arr='arr; brr='brr;
H3l=[r*U1,r*V1,R]~;
H2l=[arr*r^2,brr*r^2,r*T1]~;
Dl=matdet(ww*jacmat(H2l)+ww^2*jacmat(H3l)+ww^3*jacmat(H4));
E6l=polcoeff(polcoeff(Dl,6,ww),1,r);
check_zero(polcoeff(subst(E6l,p,0),5,q)-10*(-2*bbb+3*yy)^2/27,"E6 q^5 r extreme");
check_zero(polcoeff(subst(E6l,q,0),5,p)-2*(6*aaa-4*bbb+45*xx-30*yy)^2/1215,"E6 p^5 r extreme");

E6le=substvec(E6l,[bbb,aaa],[3*yy/2,(12*yy-15*xx)/2]);
middle=vector(4,i,polcoeff(subst(E6le,q,1),i,p));
expectedmiddle=[3*(-12*arr-8*brr+yy^2),3*(-32*arr-28*brr+40*xx^2-70*xx*yy+33*yy^2),3*(-28*arr-32*brr+65*xx^2-110*xx*yy+48*yy^2),3*(-8*arr-12*brr+25*xx^2-40*xx*yy+16*yy^2)];
for(i=1,4,check_zero(middle[i]-expectedmiddle[i],Str("middle E6 row ",i)));
Aug=matrix(3,3,i,j,if(j==1,polcoeff(middle[i],1,arr),if(j==2,polcoeff(middle[i],1,brr),-substvec(middle[i],[arr,brr],[0,0]))));
check_zero(matdet(Aug)-32400*(xx-yy)^2,"E6 augmented compatibility minor");

\\ Unique affine contact line.
kk='kk;
Uline=-2*kk*p*(p+q)/3;
Vline=2*kk*q*(p+q)/3;
Tline=kk*(-p+q);
check_zero(substvec(U1,[aaa,bbb,xx,yy],[-kk,kk,2*kk/3,2*kk/3])-Uline,"unique U contact line");
check_zero(substvec(V1,[aaa,bbb,xx,yy],[-kk,kk,2*kk/3,2*kk/3])-Vline,"unique V contact line");
check_zero(substvec(T1,[aaa,bbb,xx,yy],[-kk,kk,2*kk/3,2*kk/3])-Tline,"unique T contact line");

\\ Restore arbitrary binary lower pieces and a general linear part.
u0='u0;u1='u1;u2='u2;u3='u3;
v0='v0;v1='v1;v2='v2;v3='v3;
t0='t0;t1='t1;t2='t2;
a0='a0;a1='a1;a2='a2;a3='a3;a4='a4;a5='a5;
b0='b0;b1='b1;b2='b2;b3='b3;b4='b4;b5='b5;
l0='l0;l1='l1;l2='l2;l3='l3;l4='l4;l5='l5;l6='l6;l7='l7;l8='l8;
U0=u0*p^3+u1*p^2*q+u2*p*q^2+u3*q^3;
V0=v0*p^3+v1*p^2*q+v2*p*q^2+v3*q^3;
T0=t0*p^2+t1*p*q+t2*q^2;
A0=a0*p^2+a1*p*q+a3*q^2;
B0=b0*p^2+b1*p*q+b3*q^2;
L0=[l0,l1,l2;l3,l4,l5;l6,l7,l8];

H3=[U0+r*Uline,V0+r*Vline,R]~;
H2=[A0+a2*p*r+a4*q*r+a5*r^2,B0+b2*p*r+b4*q*r+b5*r^2,T0+r*Tline]~;
Dfull=matdet(L0+ww*jacmat(H2)+ww^2*jacmat(H3)+ww^3*jacmat(H4));
E6=polcoeff(Dfull,6,ww);
E4=polcoeff(Dfull,4,ww);
vars6=[a2,a4,a5,b2,b5,u0];
vals6=[(-45*b4+8*kk*t0-8*kk*t2-30*kk*u1+45*kk*u2-45*kk*u3+90*kk*v0-90*kk*v1+75*kk*v2-45*kk*v3+24*l8)/45,(-18*b4+4*kk*t1-8*kk*t2-9*kk*u2+27*kk*u3-6*kk*v2+18*kk*v3+12*l8)/27,kk^2/45,(90*b4+24*kk*t0-20*kk*t1+16*kk*t2-405*kk*v0+315*kk*v1-240*kk*v2+180*kk*v3+12*l8)/135,kk^2/45,u1-u2+u3+v0-v1+v2-v3];
check_zero(substvec(E6,vars6,vals6),"full arbitrary-binary E6 solve");
E4done=substvec(E4,vars6,vals6);
check_zero(polcoeff(E4done,3,r)-16*kk^4*(p+q)/135,"nonzero contact E4 obstruction");

\\ Recompute the kk=0 pivot boundary independently.
H30=[U0,V0,R]~;
H20=[A0+a2*p*r+a4*q*r+a5*r^2,B0+b2*p*r+b4*q*r+b5*r^2,T0]~;
Dzero=matdet(L0+ww*jacmat(H20)+ww^2*jacmat(H30)+ww^3*jacmat(H4));
E6zero=polcoeff(Dzero,6,ww);
E4zero=polcoeff(Dzero,4,ww);
vars0=[a2,a4,a5,b2,b5];
vals0=[-(15*b4-8*l8)/15,-2*(3*b4-2*l8)/9,0,2*(15*b4+2*l8)/45,0];
check_zero(substvec(E6zero,vars0,vals0),"zero-contact full E6 solve");
E4zeroDone=substvec(E4zero,vars0,vals0);
check_zero(polcoeff(polcoeff(E4zeroDone,1,r),3,p)-2*(15*b4+2*l8)^2/135,"zero-contact p^3 r square");
check_zero(polcoeff(subst(polcoeff(E4zeroDone,1,r),p,0),3,q)-10*(3*b4-2*l8)^2/27,"zero-contact q^3 r square");

print("D4_DN1CC_PARI_INDEPENDENT_PASS_ONE_LINE");
quit(0);
