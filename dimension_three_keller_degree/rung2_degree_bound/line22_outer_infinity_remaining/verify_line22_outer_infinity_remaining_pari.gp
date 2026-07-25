\\ Independent exact PARI/GP checks for the remaining finite-companion chart.

jacmap(V) = matrix(3,3,i,j,deriv(V[i],[x,y,z][j]));
wd(L,H2,H3,H4) = matdet(L + T*jacmap(H2) + T^2*jacmap(H3) + T^3*jacmap(H4));
coeff3(P,ex,ey,ez) = polcoef(polcoef(polcoef(P,ez,z),ey,y),ex,x);
checkzero(value,message) = if(value != 0,print(Str("FAIL: ",message));quit(1));

p=x^2;
q=y*z;

\\ Generic a != 0 chart, with (a,c)=(1,t).
H4g=[(p-q)^2,q^2,0]~;
Wg=w0*p+w1*x*y+w2*x*z+w4*q;
Ug=A*x*q+2*w1*(x^2*y-y^2*z)/t+2*w2*(x^2*z-y*z^2)/t;
Vg=B*x*q-2*w1*y^2*z/t-2*w2*y*z^2/t;
H3g=[Ug,Vg,x*(p-t*q)]~;
checkzero(polcoef(wd(matrix(3,3),[0,0,Wg]~,H3g,H4g),7,T),"generic E7");

P2g=a0*p-A*w1*x*y/t-A*w2*x*z/t+w1^2*y^2/t^2+a4*q+w2^2*z^2/t^2;
Q2g=b0*p-B*w1*x*y/t-B*w2*x*z/t+w1^2*y^2/t^2+b4*q+w2^2*z^2/t^2;
L6g=[l0,l1,l2;l3,l4,l5;l6,-w1*w4/t,-w2*w4/t];
WD6g=wd(L6g,[P2g,Q2g,Wg]~,H3g,H4g);
checkzero(polcoef(WD6g,6,T),"generic E6 solve");
L5g=[l0,-a4*w1/t+2*w1^2*w2/t^3,-a4*w2/t+2*w1*w2^2/t^3;l3,-b4*w1/t+2*w1^2*w2/t^3,-b4*w2/t+2*w1*w2^2/t^3;l6,-w1*w4/t,-w2*w4/t];
WD5g=wd(L5g,[P2g,Q2g,Wg]~,H3g,H4g);
checkzero(polcoef(WD5g,5,T),"generic E5 solve");
checkzero(matdet(L5g),"generic proportional columns");

\\ First resonance (a,c)=(1,3).
W31=w0*p+w1*x*y+w2*x*z+w4*q;
U31=A*x*q+2*w1*(x^2*y-y^2*z)/3+2*w2*(x^2*z-y*z^2)/3;
V31=B*x*q-2*w1*y^2*z/3-2*w2*y*z^2/3;
H331=[U31,V31,x*(p-3*q)]~;
checkzero(polcoef(wd(matrix(3,3),[0,0,W31]~,H331,H4g),7,T),"first resonance E7");

P231=a0*p+(-A*w1/3+4*l7/3+4*w1*w4/9)*x*y+(-A*w2/3+4*l8/3+4*w2*w4/9)*x*z+w1^2*y^2/9+a4*q+w2^2*z^2/9;
Q231=b0*p-B*w1*x*y/3-B*w2*x*z/3+w1^2*y^2/9+b4*q+w2^2*z^2/9;
L631=[l0,l1,l2;l3,l4,l5;l6,l7,l8];
checkzero(polcoef(wd(L631,[P231,Q231,W31]~,H331,H4g),6,T),"first resonance E6 solve");

P531=a0*p+(-A*w1/3+4*s1/9)*x*y+(-A*w2/3+4*s2/9)*x*z+w1^2*y^2/9+a4*q+w2^2*z^2/9;
L531=[l0,-a4*w1/3+2*w1^2*w2/27+(B-A)*s1/9,-a4*w2/3+2*w1*w2^2/27+(B-A)*s2/9;l3,-b4*w1/3+2*w1^2*w2/27,-b4*w2/3+2*w1*w2^2/27;l6,(s1-w1*w4)/3,(s2-w2*w4)/3];
WD531=wd(L531,[P531,Q231,W31]~,H331,H4g);
K31=-3*A+6*B+8*w0;
checkzero(polcoef(WD531,5,T)-2*x^2*y*z*(s1*y-s2*z)*K31/9,"first resonance E5 K reduction");
E431K0=subst(polcoef(WD531,4,T),A,2*B+8*w0/3);
checkzero(coeff3(E431K0,0,3,1)+8*s1^2/27,"first resonance s1 square");
checkzero(coeff3(E431K0,0,1,3)-8*s2^2/27,"first resonance s2 square");
checkzero(subst(subst(matdet(L531),s1,0),s2,0),"first resonance proportional columns");

\\ Second resonance (a,c)=(2,3).
H432=[(p-2*q)^2,q^2,0]~;
U32=A*x*q+4*w1*x^2*y/3-8*w1*y^2*z/3+4*w2*x^2*z/3-8*w2*y*z^2/3;
V32=B*x*q-2*w1*y^2*z/3-2*w2*y*z^2/3;
H332=[U32,V32,x*(p-3*q)]~;
checkzero(polcoef(wd(matrix(3,3),[0,0,W31]~,H332,H432),7,T),"second resonance E7");

P232=a0*p-A*w1*x*y/3-A*w2*x*z/3+4*w1^2*y^2/9+a4*q+4*w2^2*z^2/9;
Q232=b0*p+(-B*w1/3-2*l7/3-2*w1*w4/9)*x*y+(-B*w2/3-2*l8/3-2*w2*w4/9)*x*z+w1^2*y^2/9+b4*q+w2^2*z^2/9;
checkzero(polcoef(wd(L631,[P232,Q232,W31]~,H332,H432),6,T),"second resonance E6 solve");

Q532=b0*p+(-B*w1/3-2*s1/9)*x*y+(-B*w2/3-2*s2/9)*x*z+w1^2*y^2/9+b4*q+w2^2*z^2/9;
L532=[l0,A*s1/9-8*B*s1/9-32*s1*w0/27-16*s1*w4/27-a4*w1/3+8*w1^2*w2/27,A*s2/9-8*B*s2/9-32*s2*w0/27-16*s2*w4/27-a4*w2/3+8*w1*w2^2/27;l3,A*s1/18-B*s1/3-8*s1*w0/27-4*s1*w4/27-b4*w1/3+2*w1^2*w2/27,A*s2/18-B*s2/3-8*s2*w0/27-4*s2*w4/27-b4*w2/3+2*w1*w2^2/27;l6,(s1-w1*w4)/3,(s2-w2*w4)/3];
WD532=wd(L532,[P232,Q532,W31]~,H332,H432);
K32=-3*A+6*B+8*w0+4*w4;
checkzero(polcoef(WD532,5,T)+2*x^4*(s1*y-s2*z)*K32/9,"second resonance E5 K reduction");
E432K0=subst(polcoef(WD532,4,T),A,2*B+8*w0/3+4*w4/3);
checkzero(coeff3(E432K0,2,2,0)-8*s1^2/27,"second resonance s1 square");
checkzero(coeff3(E432K0,2,0,2)+8*s2^2/27,"second resonance s2 square");
checkzero(subst(subst(matdet(L532),s1,0),s2,0),"second resonance proportional columns");

\\ Noncritical triple (a,c)=(1,0).
W0=w0*p+w4*q;
U0=A*x*q-r1*x^2*y+r1*y^2*z-r2*x^2*z+r2*y*z^2;
V0=B*x*q+r1*y^2*z+r2*y*z^2;
H30=[U0,V0,x^3]~;
checkzero(polcoef(wd(matrix(3,3),[0,0,W0]~,H30,H4g),7,T),"c=0 E7");
P20=a0*p+A*r1*x*y/2+A*r2*x*z/2+r1^2*y^2/4+a4*q+r2^2*z^2/4;
Q20=b0*p+B*r1*x*y/2+B*r2*x*z/2+r1^2*y^2/4+b4*q+r2^2*z^2/4;
L60=[l0,l1,l2;l3,l4,l5;l6,r1*w4/2,r2*w4/2];
checkzero(polcoef(wd(L60,[P20,Q20,W0]~,H30,H4g),6,T),"c=0 E6 solve");
L50=[l0,a4*r1/2-r1^2*r2/4,a4*r2/2-r1*r2^2/4;l3,b4*r1/2-r1^2*r2/4,b4*r2/2-r1*r2^2/4;l6,r1*w4/2,r2*w4/2];
checkzero(polcoef(wd(L50,[P20,Q20,W0]~,H30,H4g),5,T),"c=0 E5 solve");
checkzero(matdet(L50),"c=0 proportional columns");

\\ Marked mixed (a,c)=(0,1).
H4m=[p^2,q^2,0]~;
Wm=w0*p+w1*x*y+w2*x*z+w4*q;
H3m=[A*x*q,B*x*q-2*w1*y^2*z-2*w2*y*z^2,x*(p-q)]~;
checkzero(polcoef(wd(matrix(3,3),[0,0,Wm]~,H3m,H4m),7,T),"marked mixed E7");
P2m=a0*p-A*w1*x*y-A*w2*x*z+a4*q;
Q2m=b0*p-B*w1*x*y-B*w2*x*z+w1^2*y^2+b4*q+w2^2*z^2;
L6m=[l0,l1,l2;l3,l4,l5;l6,-w1*w4,-w2*w4];
checkzero(polcoef(wd(L6m,[P2m,Q2m,Wm]~,H3m,H4m),6,T),"marked mixed E6 solve");
L5m=[l0,-a4*w1,-a4*w2;l3,-b4*w1+2*w1^2*w2,-b4*w2+2*w1*w2^2;l6,-w1*w4,-w2*w4];
checkzero(polcoef(wd(L5m,[P2m,Q2m,Wm]~,H3m,H4m),5,T),"marked mixed E5 solve");
checkzero(matdet(L5m),"marked mixed proportional columns");

print("line-(2,2) remaining finite-companion outer-infinity PARI/GP checks passed");
quit;
