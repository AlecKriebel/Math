\\ Independent exact checks for the nonbinary fixed-quadratic line-cover row.

jacmap(V) = matrix(3,3,i,j,deriv(V[i],[p,q,r][j]));
checkzero(value,message) = if(value != 0,print(Str("FAIL: ",message));quit(1));
coeff3(P,ep,eq,er) = polcoef(polcoef(polcoef(P,er,r),eq,q),ep,p);
solvevar(expression,variable) = -subst(expression,variable,0)/deriv(expression,variable);

\\ General adjugate and derivation.
h = h0*p^2+h1*p*q+h2*q^2+h3*p*r+h4*q*r+h5*r^2;
hr = deriv(h,r);
H4general = [h*p^2,h*q^2,0]~;
Cgeneral = jacmap(H4general);
kvec = [p*hr,q*hr,r*hr-4*h]~;
e3 = [0,0,1]~;
checkzero(Cgeneral*kvec-[0,0,0]~,"general right kernel");
checkzero(matadjoint(Cgeneral)+2*h*p*q*kvec*e3~,"general adjugate");

G3 = g30*p^3+g31*p^2*q+g32*p*q^2+g33*q^3+g34*p^2*r+g35*p*q*r+g36*q^2*r+g37*p*r^2+g38*q*r^2+g39*r^3;
G2 = g20*p^2+g21*p*q+g22*q^2+g23*p*r+g24*q*r+g25*r^2;
DkG3 = deriv(G3,p)*kvec[1]+deriv(G3,q)*kvec[2]+deriv(G3,r)*kvec[3];
DkG2 = deriv(G2,p)*kvec[1]+deriv(G2,q)*kvec[2]+deriv(G2,r)*kvec[3];
Hts = subst(subst(h,q,p*t),r,p*s)/p^2;
g3ts = subst(subst(G3,q,p*t),r,p*s)/p^3;
g2ts = subst(subst(G2,q,p*t),r,p*s)/p^2;
checkzero(subst(subst(DkG3,q,p*t),r,p*s)-p^4*(3*deriv(Hts,s)*g3ts-4*Hts*deriv(g3ts,s)),"degree-three derivation");
checkzero(subst(subst(DkG2,q,p*t),r,p*s)-p^3*(2*deriv(Hts,s)*g2ts-4*Hts*deriv(g2ts,s)),"degree-two derivation");

\\ Exceptional square.
H4 = [p^2*r^2,q^2*r^2,0]~;
J4 = jacmap(H4);
ksquare = [2*p*r,2*q*r,-2*r^2]~;
checkzero(deriv(p*r,p)*ksquare[1]+deriv(p*r,q)*ksquare[2]+deriv(p*r,r)*ksquare[3],"p*r invariant");
checkzero(deriv(q*r,p)*ksquare[1]+deriv(q*r,q)*ksquare[2]+deriv(q*r,r)*ksquare[3],"q*r invariant");

\\ The p*r orbit after E4 in the K-nonzero branch.
H3pr = [2*p*r*(aa*p+bb*q+cc*r),q*r*(AA*p+BB*q+CC*r),0]~;
H2pr = [(aa*p+bb*q)^2+dd*p*r+(2*bb*cc-kk)*q*r+cc^2*r^2,(AA*p+BB*q)^2/4+gg*p*r+jj*q*r+CC^2*r^2/4,p*r]~;
Lpr = [-AA*kk/2-2*aa^2*cc+aa*dd,-BB*kk/2-2*aa*bb*cc+bb*dd,-CC*kk/2-2*aa*cc^2+cc*dd;mm,nn,om0;aa,bb,cc];
wpr = matdet(Lpr+zz*jacmap(H2pr)+zz^2*jacmap(H3pr)+zz^3*J4);
for (degree=3,8,checkzero(polcoef(wpr,degree,zz),"p*r unexpected upper identity"));
mmsol = (-AA*BB*CC-2*AA*CC*aa+2*AA*jj+4*aa*gg)/4;
nnsol = (-2*AA*CC*bb-BB^2*CC+2*BB*jj+4*bb*gg)/4;
om0sol = (-2*AA*CC*cc-BB*CC^2+2*CC*jj+4*cc*gg)/4;
wprsol = subst(subst(subst(wpr,mm,mmsol),nn,nnsol),om0,om0sol);
Lprsol = subst(subst(subst(Lpr,mm,mmsol),nn,nnsol),om0,om0sol);
checkzero(polcoef(wprsol,2,zz),"p*r degree two");
checkzero(polcoef(wprsol,1,zz),"p*r degree one");
checkzero(matdet(Lprsol),"p*r determinant");

\\ K=0 forces proportional first and third rows.
Lprzero = [aa*(dd-2*aa*cc),bb*(dd-2*aa*cc),cc*(dd-2*aa*cc);mm,nn,om0;aa,bb,cc];
checkzero(matdet(Lprzero),"p*r resonant determinant");

\\ Standard branch of the (p+q)r orbit, after X=Y=0.
d0 = 2*aa+al;
e0 = 2*bb+be;
t0 = 2*cc+ga;
H3sum = [-p*r*(d0*p+e0*q+t0*r)+2*p*r*(aa*p+bb*q+cc*r),q*r*(d0*p+e0*q+t0*r),0]~;
H2sum = [al^2*p^2/4+al*be*p*q/2+be^2*q^2/4+pp*p*r+qq*q*r+ga^2*r^2/4,d0^2*p^2/4+d0*e0*p*q/2+e0^2*q^2/4+rr1*p*r+ss1*q*r+t0^2*r^2/4,(p+q)*r]~;
Lsum = [l00,l01,l02;l10,l11,l12;aa,bb,cc];
wsum = matdet(Lsum+zz*jacmap(H2sum)+zz^2*jacmap(H3sum)+zz^3*J4);
for (degree=5,8,checkzero(polcoef(wsum,degree,zz),"sum standard unexpected upper identity"));

\\ Solve the five linear E4 entries independently, leaving l11.
e4 = polcoef(wsum,4,zz);
l10sol = solvevar(coeff3(e4,2,0,2),l10);
wsum1 = subst(wsum,l10,l10sol);
Lsum1 = subst(Lsum,l10,l10sol);
e4 = polcoef(wsum1,4,zz);
l00sol = solvevar(coeff3(e4,1,1,2),l00);
wsum2 = subst(wsum1,l00,l00sol);
Lsum2 = subst(Lsum1,l00,l00sol);
e4 = polcoef(wsum2,4,zz);
l12sol = solvevar(coeff3(e4,1,0,3),l12);
wsum3 = subst(wsum2,l12,l12sol);
Lsum3 = subst(Lsum2,l12,l12sol);
e4 = polcoef(wsum3,4,zz);
l01sol = solvevar(coeff3(e4,0,2,2),l01);
wsum4 = subst(wsum3,l01,l01sol);
Lsum4 = subst(Lsum3,l01,l01sol);
e4 = polcoef(wsum4,4,zz);
l02sol = solvevar(coeff3(e4,0,1,3),l02);
wsum5 = subst(wsum4,l02,l02sol);
Lsum5 = subst(Lsum4,l02,l02sol);
checkzero(polcoef(wsum5,4,zz),"sum standard E4 solve");

mfac = -4*l11+4*aa*be*cc+2*aa*be*ga+2*al*be*cc+al*be*ga-8*bb^2*cc-4*bb^2*ga-8*bb*be*cc-4*bb*be*ga+4*bb*ss1-2*be^2*cc-be^2*ga-2*be*rr1+2*be*ss1;
e3 = polcoef(wsum5,3,zz);
checkzero(coeff3(e3,2,0,1)-d0*mfac/2,"sum standard p2r factor");
checkzero(coeff3(e3,1,1,1)-(al+e0)*mfac/2,"sum standard pqr factor");
checkzero(coeff3(e3,0,2,1)-be*mfac/2,"sum standard q2r factor");
l11sol = solvevar(mfac,l11);
checkzero(subst(matdet(Lsum5),l11,l11sol),"sum standard determinant");

\\ Deep exceptional branch d0=0, e0=2a=2b.
H3ex = [2*aa*p^2*r-ga*p*r^2,2*aa*q^2*r+(2*cc+ga)*q*r^2,0]~;
H2ex = [(aa^2+XX)*p^2+YY*p*q+pp*p*r+qq*q*r+ga^2*r^2/4,-XX*p*q+(aa^2-YY)*q^2+rr1*p*r+ss1*q*r+(2*cc+ga)^2*r^2/4,(p+q)*r]~;
Lex = [l00,l01,l02;l10,l11,l12;aa,aa,cc];
wex = matdet(Lex+zz*jacmap(H2ex)+zz^2*jacmap(H3ex)+zz^3*J4);
for (degree=5,8,checkzero(polcoef(wex,degree,zz),"sum exceptional unexpected upper identity"));

e4 = polcoef(wex,4,zz);
l10ex = solvevar(coeff3(e4,2,0,2),l10);
wex1 = subst(wex,l10,l10ex);
Lex1 = subst(Lex,l10,l10ex);
e4 = polcoef(wex1,4,zz);
l00ex = solvevar(coeff3(e4,1,1,2),l00);
wex2 = subst(wex1,l00,l00ex);
Lex2 = subst(Lex1,l00,l00ex);
e4 = polcoef(wex2,4,zz);
l12ex = solvevar(coeff3(e4,1,0,3),l12);
wex3 = subst(wex2,l12,l12ex);
Lex3 = subst(Lex2,l12,l12ex);
e4 = polcoef(wex3,4,zz);
l01ex = solvevar(coeff3(e4,0,2,2),l01);
wex4 = subst(wex3,l01,l01ex);
Lex4 = subst(Lex3,l01,l01ex);
e4 = polcoef(wex4,4,zz);
l02ex = solvevar(coeff3(e4,0,1,3),l02);
wex5 = subst(wex4,l02,l02ex);
Lex5 = subst(Lex4,l02,l02ex);
checkzero(polcoef(wex5,4,zz),"sum exceptional E4 solve");
e3 = polcoef(wex5,3,zz);
checkzero(coeff3(e3,3,0,0)+2*XX^2,"sum exceptional X square");
checkzero(coeff3(e3,0,3,0)+2*YY^2,"sum exceptional Y square");

wdeep = subst(subst(wex5,XX,0),YY,0);
Ldeep = subst(subst(Lex5,XX,0),YY,0);
mstar = l11+2*aa^2*cc+aa^2*ga-aa*ss1;
astar = 4*aa*cc+2*aa*ga+rr1-ss1;
checkzero(coeff3(polcoef(wdeep,2,zz),1,0,1)-mstar*astar,"sum exceptional E2");
checkzero(coeff3(polcoef(wdeep,1,zz),1,0,0)-mstar*(aa*astar-mstar),"sum exceptional E1");
l11star = -2*aa^2*cc-aa^2*ga+aa*ss1;
checkzero(subst(matdet(Ldeep),l11,l11star),"sum exceptional determinant");

print("nonbinary fixed-quadratic line-cover PARI/GP checks passed");
quit;
