\\ Independent exact checks for the nonbinary fixed-conic tangent reduction.

default(parisizemax, 512000000);
allocatemem(128000000);

cross3(x,y) = [x[2]*y[3]-x[3]*y[2],x[3]*y[1]-x[1]*y[3],x[1]*y[2]-x[2]*y[1]]~;
jacmap(H) = matrix(3,3,i,j,deriv(H[i],[p,q,r][j]));

A = [p^2,p*q,q^2]~;
Ap = vector(3,i,deriv(A[i],p))~;
Aq = vector(3,i,deriv(A[i],q))~;
Delta = cross3(Ap,Aq);

h = c0*p^2+c1*p*q+c2*q^2+c3*p*r+c4*q*r+c5*r^2;
hr = deriv(h,r);
k = [p*hr,q*hr,r*hr-4*h]~;
C = jacmap(h*A);
if (matadjoint(C)+h*k*Delta~/2 != matrix(3,3),error("general adjugate identity mismatch"));
if (C*k != [0,0,0]~,error("general kernel identity mismatch"));

DkDelta = jacmap(Delta)*k;
if (DkDelta-2*hr*Delta != [0,0,0]~,error("normal derivative mismatch"));

f0 = aa0*p^2+aa1*p*q+aa2*q^2;
f1 = aa3*p+aa4*q;
g0 = bb0*p^2+bb1*p*q+bb2*q^2;
g1 = bb3*p+bb4*q;
fgeneral = f0+r*f1+aa5*r^2;
ggeneral = g0+r*g1+bb5*r^2;
H3general = fgeneral*Ap+ggeneral*Aq;
H4square = r^2*A;
Csquare = jacmap(H4square);
normalterm = trace(matadjoint(jacmap(H3general))*Csquare);
R = q*f0-p*g0;
S = q*f1-p*g1;
normalmod = polcoef(normalterm,0,r)+r*polcoef(normalterm,1,r)+r^2*polcoef(normalterm,2,r);
if (normalmod-12*r*R^2-16*r^2*R*S != 0,error("degree-seven normal certificate mismatch"));

L = aa0*p+aa1*q;
f = p*L+r*(aa3*p+aa4*q+aa5*r);
g = q*L+r*(bb3*p+bb4*q+bb5*r);
H3 = f*Ap+g*Aq;
H2 = [(aa3-bb4)^2*p^2-2*aa4*bb3*p^2+2*aa4*(aa3-bb4)*p*q+aa4^2*q^2+aa5^2*r^2,bb3*(aa3-bb4)*p^2+aa5*bb5*r^2,bb3^2*p^2+bb5^2*r^2]~;
E7 = trace(matadjoint(Csquare)*jacmap(H2))+trace(matadjoint(jacmap(H3))*Csquare);
if (E7 != 0,error("full degree-seven solution mismatch"));

translationCubic = xxi*deriv(H4square,p)+eeta*deriv(H4square,q);
if (translationCubic-r^2*(xxi*Ap+eeta*Aq) != [0,0,0]~,error("affine translation cubic mismatch"));

H3normalized = subst(subst(H3,aa5,0),bb5,0);
H2base = subst(subst(H2,aa5,0),bb5,0);
ell = ellp*p+ellq*q;
mform = mp*p+mq*q;
H2full = H2base+ell*Ap+mform*Aq+r*[ku0*p+ku1*q,ku2*p+ku3*q,ku4*p+ku5*q]~;
E7full = trace(matadjoint(Csquare)*jacmap(H2full))+trace(matadjoint(jacmap(H3normalized))*Csquare);
if (E7full != 0,error("full degree-seven affine kernel mismatch"));

L0 = [l0,l1,l2;l3,l4,l5;l6,l7,l8];
weighted = matdet(L0+s*jacmap(H2full)+s^2*jacmap(H3normalized)+s^3*Csquare);
E6 = polcoef(weighted,6,s);
if (polcoef(polcoef(polcoef(E6,4,r),2,p),0,q)-2*l8 != 0,error("p^2 r^4 exit mismatch"));
if (polcoef(polcoef(polcoef(E6,4,r),1,p),1,q)+4*l5 != 0,error("p q r^4 exit mismatch"));
if (polcoef(polcoef(polcoef(E6,4,r),0,p),2,q)-2*l2 != 0,error("q^2 r^4 exit mismatch"));

H4plus = (r^2+p^2)*A;
H3plus = 2*(xp*p+yq*q)*A;
H2plus = [(-pu4+2*pu0)*p^2+2*pu1*p*q+2*pu2*p*r,pu3*p^2/2+pu0*p*q+pu1*q^2+pu5*p*r/2+pu2*q*r,pu3*p*q+pu4*q^2+pu5*q*r]~;
weightedPlus = matdet(L0+s*jacmap(H2plus)+s^2*jacmap(H3plus)+s^3*jacmap(H4plus));
if (polcoef(weightedPlus,7,s) != 0,error("r^2+p^2 degree-seven family mismatch"));
E6plus = polcoef(weightedPlus,6,s);
expectedE6plus = 4*l8*p^6-8*l5*p^5*q-2*l6*p^5*r+4*l2*p^4*q^2+2*(2*l3-l7)*p^4*q*r+6*l8*p^4*r^2-2*(l0-2*l4)*p^3*q^2*r-12*l5*p^3*q*r^2-2*l6*p^3*r^3-2*l1*p^2*q^3*r+6*l2*p^2*q^2*r^2+2*(2*l3-l7)*p^2*q*r^3+2*l8*p^2*r^4-2*(l0-2*l4)*p*q^2*r^3-4*l5*p*q*r^4-2*l1*q^3*r^3+2*l2*q^2*r^4;
if (E6plus-expectedE6plus != 0,error("r^2+p^2 degree-six exit mismatch"));

H4pr = p*r*A;
H3pr = 2*(xp*p+yq*q+zr*r)*A;
weightedPr = matdet(L0+s*jacmap(H2plus)+s^2*jacmap(H3pr)+s^3*jacmap(H4pr));
if (polcoef(weightedPr,7,s) != 0,error("pr degree-seven family mismatch"));
E6pr = polcoef(weightedPr,6,s);
expectedE6pr = -l6*p^5*r+(2*l3-l7)*p^4*q*r+3*l8*p^4*r^2+(-l0+2*l4)*p^3*q^2*r-6*l5*p^3*q*r^2-l1*p^2*q^3*r+3*l2*p^2*q^2*r^2;
if (E6pr-expectedE6pr != 0,error("pr degree-six exit mismatch"));

H4rp = (r^2+p*q)*A;
H3rp = 2*(xp*p+yq*q+zr*r)*A;
weightedRp = matdet(L0+s*jacmap(H2plus)+s^2*jacmap(H3rp)+s^3*jacmap(H4rp));
if (polcoef(weightedRp,7,s) != 0,error("r^2+pq degree-seven family mismatch"));
E6rp = polcoef(weightedRp,6,s);
expectedE6rp = 4*l8*p^4*q^2-2*l6*p^4*q*r-8*l5*p^3*q^3+2*(2*l3-l7)*p^3*q^2*r+6*l8*p^3*q*r^2-2*l6*p^3*r^3+4*l2*p^2*q^4-2*(l0-2*l4)*p^2*q^3*r-12*l5*p^2*q^2*r^2+2*(2*l3-l7)*p^2*q*r^3+2*l8*p^2*r^4-2*l1*p*q^4*r+6*l2*p*q^3*r^2-2*(l0-2*l4)*p*q^2*r^3-4*l5*p*q*r^4-2*l1*q^3*r^3+2*l2*q^2*r^4;
if (E6rp-expectedE6rp != 0,error("r^2+pq degree-six exit mismatch"));

H4pq = (p*r+q^2)*A;
H3pq = 2*(xp*p+yq*q+zr*r)*A;
weightedPq = matdet(L0+s*jacmap(H2plus)+s^2*jacmap(H3pq)+s^3*jacmap(H4pq));
if (polcoef(weightedPq,7,s) != 0,error("pr+q^2 degree-seven family mismatch"));
E6pq = polcoef(weightedPq,6,s);
expectedE6pq = -l6*p^5*r-l6*p^4*q^2+(2*l3-l7)*p^4*q*r+3*l8*p^4*r^2+(2*l3-l7)*p^3*q^3+(-l0+2*l4+7*l8)*p^3*q^2*r-6*l5*p^3*q*r^2+(-l0+2*l4+4*l8)*p^2*q^4+(-l1-14*l5)*p^2*q^3*r+3*l2*p^2*q^2*r^2+(-l1-8*l5)*p*q^5+7*l2*p*q^4*r+4*l2*q^6;
if (E6pq-expectedE6pq != 0,error("pr+q^2 degree-six exit mismatch"));

print("nonbinary fixed-conic PARI/GP checks passed");
quit;
