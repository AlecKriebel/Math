\\ Independent PARI/GP replay of the D4-DN-3 transverse-plane E5 obstruction.
\\
\\ This file reconstructs the weighted determinant directly in PARI.  It
\\ solves the specialization-safe seven-pivot E6 system while retaining all
\\ eleven free lower variables, then checks two E5 coefficients which are
\\ independent of those variables and cannot vanish simultaneously.

p='p; q='q; r='r; ww='ww;
vars=[p,q,r];
jacmat(H)=matrix(3,3,i,j,deriv(H[i],vars[j]));
check_zero(value,message)={if(value!=0,print(Str("FAIL: ",message,"; residual = ",value));quit(1))};
check_true(value,message)={if(!value,print(Str("FAIL: ",message));quit(1))};
coef3(f,ip,iq,ir)=polcoeff(polcoeff(polcoeff(f,ir,r),iq,q),ip,p);

h=(p+q)^2;
P=h*p^2;
Q=h*q^2;
R=(p+q)^3;
H4=[P,Q,0]~;

\\ Work over Q(sqrt(2)).
rr='rr;
rt=Mod(rr,rr^2-2);
ss='ss; kk='kk;
cplus=(-4+2*rt)/3;
U1=(4*kk-3*(ss+cplus*kk))*p^2/3+(4*kk-3*ss)*p*q/3;
V1=(ss+cplus*kk)*p*q+ss*q^2;
T1=kk*(p+q);

\\ All lower coefficients are retained.
u0='u0;u1='u1;u2='u2;u3='u3;
v0='v0;v1='v1;v2='v2;v3='v3;
t0='t0;t1='t1;t2='t2;
a0='a0;a1='a1;a2='a2;a3='a3;a4='a4;a5='a5;
b0='b0;b1='b1;b2='b2;b3='b3;b4='b4;b5='b5;
l0='l0;l1='l1;l2='l2;l3='l3;l4='l4;l5='l5;l6='l6;l7='l7;l8='l8;
U0=u0*p^3+u1*p^2*q+u2*p*q^2+u3*q^3;
V0=v0*p^3+v1*p^2*q+v2*p*q^2+v3*q^3;
T0=t0*p^2+t1*p*q+t2*q^2;
A=a0*p^2+a1*p*q+a2*p*r+a3*q^2+a4*q*r+a5*r^2;
B=b0*p^2+b1*p*q+b2*p*r+b3*q^2+b4*q*r+b5*r^2;
L0=[l0,l1,l2;l3,l4,l5;l6,l7,l8];
H3=[U0+r*U1,V0+r*V1,R]~;
H2=[A,B,T0+r*T1]~;
D=matdet(L0+ww*jacmat(H2)+ww^2*jacmat(H3)+ww^3*jacmat(H4));
check_zero(polcoeff(D,7,ww),"E7 on the plus plane");

E6=polcoeff(D,6,ww);
E5=polcoeff(D,5,ww);
low=[a2,a4,a5,b2,b4,b5,l8,u0,u1,u2,u3,v0,v1,v2,v3,t0,t1,t2];
zeros=vector(18);
exps=[[6,0,0],[5,1,0],[5,0,1],[4,2,0],[4,1,1],[3,3,0],[3,2,1],[2,4,0],[2,3,1],[1,5,0],[1,4,1],[0,6,0],[0,5,1]];
eq=vector(13,i,lift(coef3(E6,exps[i][1],exps[i][2],exps[i][3])));
M=matrix(13,18,i,j,Mod(polcoeff(eq[i],1,low[j]),rr^2-2));
rhs=matrix(13,1,i,j,Mod(-substvec(eq[i],low,zeros),rr^2-2));

\\ This is the certified k-nonzero pivot, independent of s.
rows=[1,2,3,4,5,6,8];
pivcols=[1,2,3,4,6,8,9];
freecols=[5,7,10,11,12,13,14,15,16,17,18];
Mp=vecextract(M,rows,pivcols);
Mf=vecextract(M,rows,freecols);
bp=vector(#rows,i,rhs[rows[i],1])~;
check_zero(matdet(Mp)-373248*(7-5*rt)*kk^2,"safe E6 pivot");

freevec=vector(#freecols,i,low[freecols[i]])~;
pivsol=matsolve(Mp,bp-Mf*freevec);
sol=vector(18,i,low[i]);
for(i=1,#pivcols,sol[pivcols[i]]=pivsol[i]);

\\ The substitution must solve every E6 equation, not only the pivot rows.
check_zero(substvec(E6,low,sol),"complete E6 system after pivot solve");

E5sub=substvec(E5,low,sol);
cp=coef3(E5sub,3,0,2);
cq=coef3(E5sub,0,3,2);
expectedp=3*(rt-2)*kk*(ss+cplus*kk)^2;
expectedq=3*(rt-2)*kk*(ss-4*kk/3)^2;
check_zero(cp-expectedp,"[p^3 r^2] E5");
check_zero(cq-expectedq,"[q^3 r^2] E5");

\\ With k nonzero, the two squares would require incompatible values of s.
check_true(3*(rt-2)!=0,"nonzero common scalar");
check_true(cplus!=-4/3,"incompatible zero loci");

\\ The conjugate plane follows under sqrt(2) -> -sqrt(2).
cpminus=Mod(subst(lift(cp),rr,-rr),rr^2-2);
cqminus=Mod(subst(lift(cq),rr,-rr),rr^2-2);
cminus=(-4-2*rt)/3;
check_zero(cpminus-3*(-rt-2)*kk*(ss+cminus*kk)^2,"minus-plane p coefficient");
check_zero(cqminus-3*(-rt-2)*kk*(ss-4*kk/3)^2,"minus-plane q coefficient");
check_true(cminus!=-4/3,"minus-plane incompatible zero loci");

print("D4_DN3_TRANSVERSE_E5_PARI_PASS");
quit(0);
