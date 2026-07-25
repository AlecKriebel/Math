\\ Independent exact checks for WORKING_FIXED_CUBIC_LINE_ROW.md.

jacmap(V) = matrix(3,3,i,j,deriv(V[i],[p,q,r][j]));
checkzero(value,message) = if(value != 0,print(Str("FAIL: ",message));quit(1));

h = c0*p^3+c1*p^2*q+c2*p*q^2+c3*q^3+c4*p^2*r+c5*p*q*r+c6*q^2*r+c7*p*r^2+c8*q*r^2+c9*r^3;
hr = deriv(h,r);
A = [p,q,0]~;
H4 = h*A;
C = jacmap(H4);
kvec = [p*hr,q*hr,r*hr-4*h]~;
e3 = [0,0,1]~;

checkzero(C*kvec-[0,0,0]~,"right-kernel identity mismatch");
checkzero(matadjoint(C)+h*kvec*e3~,"adjugate identity mismatch");

Dkh = deriv(h,p)*kvec[1]+deriv(h,q)*kvec[2]+deriv(h,r)*kvec[3];
checkzero(Dkh+h*hr,"Euler derivation mismatch");

cubmons = [p^3,p^2*q,p*q^2,q^3,p^2*r,p*q*r,q^2*r,p*r^2,q*r^2,r^3];
quadmons = [p^2,p*q,q^2,p*r,q*r,r^2];
g3coeffs = [g30,g31,g32,g33,g34,g35,g36,g37,g38,g39];
g2coeffs = [g20,g21,g22,g23,g24,g25];
G3 = sum(i=1,10,g3coeffs[i]*cubmons[i]);
G2 = sum(i=1,6,g2coeffs[i]*quadmons[i]);
DkG3 = deriv(G3,p)*kvec[1]+deriv(G3,q)*kvec[2]+deriv(G3,r)*kvec[3];
DkG2 = deriv(G2,p)*kvec[1]+deriv(G2,q)*kvec[2]+deriv(G2,r)*kvec[3];

u1coeffs = [u10,u11,u12,u13,u14,u15,u16,u17,u18,u19];
u2coeffs = [u20,u21,u22,u23,u24,u25,u26,u27,u28,u29];
H3 = [sum(i=1,10,u1coeffs[i]*cubmons[i]),sum(i=1,10,u2coeffs[i]*cubmons[i]),0]~;
B = jacmap(H3);
v1coeffs = [v10,v11,v12,v13,v14,v15];
v2coeffs = [v20,v21,v22,v23,v24,v25];
v3coeffs = [v30,v31,v32,v33,v34,v35];
H2 = [sum(i=1,6,v1coeffs[i]*quadmons[i]),sum(i=1,6,v2coeffs[i]*quadmons[i]),sum(i=1,6,v3coeffs[i]*quadmons[i])]~;
JH2 = jacmap(H2);
DkH2third = deriv(H2[3],p)*kvec[1]+deriv(H2[3],q)*kvec[2]+deriv(H2[3],r)*kvec[3];

G3map = [0,0,G3]~;
checkzero(trace(matadjoint(C)*jacmap(G3map))+h*DkG3,"degree-eight identity mismatch");
checkzero(trace(matadjoint(B)*C),"mixed degree-seven term mismatch");
checkzero(trace(matadjoint(C)*JH2)+trace(matadjoint(B)*C)+h*DkH2third,"degree-seven identity mismatch");

hex = p*r^2;
hrex = deriv(hex,r);
kex = [p*hrex,q*hrex,r*hrex-4*hex]~;
G2ex = p*r;
DkG2ex = deriv(G2ex,p)*kex[1]+deriv(G2ex,q)*kex[2]+deriv(G2ex,r)*kex[3];
checkzero(DkG2ex,"double-factor sharpness example mismatch");

H4ex = hex*A;
JH4ex = jacmap(H4ex);

\\ The q*r orbit after the complete degree-six/degree-five solve.
H3q = [2*cq*p*q*r,r*(aq*p^2+bq*p*q+cq*q^2),0]~;
H2q = [(2*xq-2*aq*cq)*p^2+(2*yq-2*bq*cq)*p*q+cq^2*q^2+dq*p*r+eq*q*r,xq*p*q+yq*q^2+fq*p*r+gq*q*r,q*r]~;
L0q = [ql0,ql1,ql2;ql3,ql4,ql5;aq,bq,0];
weightedq = matdet(L0q+zz*jacmap(H2q)+zz^2*jacmap(H3q)+zz^3*JH4ex);
checkzero(polcoef(weightedq,6,zz),"q*r orbit degree-six mismatch");
checkzero(polcoef(weightedq,5,zz),"q*r orbit degree-five mismatch");
E4q = polcoef(weightedq,4,zz);
q_r3 = polcoef(polcoef(polcoef(E4q,3,r),1,q),0,p);
p_r3 = polcoef(polcoef(polcoef(E4q,3,r),0,q),1,p);
checkzero(q_r3-ql2,"q*r orbit first degree-four exit mismatch");
checkzero(p_r3+2*ql5,"q*r orbit second degree-four exit mismatch");
checkzero(subst(subst(matdet(L0q),ql2,0),ql5,0),"q*r orbit singular-linear-part mismatch");

\\ The p*r orbit before its K split.
upcoeffs = [up0,up1,up2,up3,up4,up5,up6,up7,up8,up9];
wpcoeffs = [wp0,wp1,wp2,wp3,wp4,wp5];
Up = sum(i=1,10,upcoeffs[i]*cubmons[i]);
Vp = sum(i=1,6,wpcoeffs[i]*quadmons[i]);
H3praw = [2*tt*p*q*r,Up,0]~;
H2praw = [tt^2*q^2+dd0*p*r+kk*q*r,Vp,p*r]~;
L0praw = [pl0,pl1,pl2;pl3,pl4,pl5;0,tt,0];
weightedpraw = matdet(L0praw+zz*jacmap(H2praw)+zz^2*jacmap(H3praw)+zz^3*JH4ex);
for (degree=5,8,checkzero(polcoef(weightedpraw,degree,zz),"p*r orbit unexpected upper coefficient"));
E4praw = polcoef(weightedpraw,4,zz);
expectedE4praw = 3*kk*up9*r^4+kk*up8*q*r^3+(kk*up7-pl2)*p*r^3+kk*(tt-up6)*q^2*r^2+(-dd0*tt-kk*up5+pl1)*p*q*r^2+(-kk*up4+pl0)*p^2*r^2-3*kk*up3*q^3*r-3*kk*up2*p*q^2*r-3*kk*up1*p^2*q*r-3*kk*up0*p^3*r;
checkzero(E4praw-expectedE4praw,"p*r orbit degree-four table mismatch");

L0pzero = [0,tt*dd0,0;pl3,pl4,pl5;0,tt,0];
checkzero(matdet(L0pzero),"p*r K=0 singular-linear-part mismatch");

\\ The K!=0 branch after degrees four and three.
H3pfinal = [2*tt*p*q*r,r*(aa*p^2+bb*p*q+tt*q^2+cc*p*r),0]~;
H2pfinal = [tt^2*q^2+dd0*p*r+kk*q*r,aa*tt*p*q+bb*tt*q^2+ee*p*r+gg*q*r,p*r]~;
L0pfinal = [kk*aa,tt*dd0+kk*bb,kk*cc;mm,nn,om;0,tt,0];
weightedpfinal = matdet(L0pfinal+zz*jacmap(H2pfinal)+zz^2*jacmap(H3pfinal)+zz^3*JH4ex);
for (degree=3,8,checkzero(polcoef(weightedpfinal,degree,zz),"p*r final unexpected upper coefficient"));
E2pfinal = polcoef(weightedpfinal,2,zz);
expectedE2pfinal = -kk*(aa*cc*tt-aa*gg+mm)*p*r-kk*(bb*cc*tt-bb*gg-ee*tt+nn)*q*r+kk*(cc^2*tt-cc*gg+om)*r^2;
checkzero(E2pfinal-expectedE2pfinal,"p*r degree-two table mismatch");

msol = aa*(gg-cc*tt);
nsol = ee*tt+bb*(gg-cc*tt);
omsol = cc*(gg-cc*tt);
E2sol = subst(subst(subst(E2pfinal,mm,msol),nn,nsol),om,omsol);
E1sol = subst(subst(subst(polcoef(weightedpfinal,1,zz),mm,msol),nn,nsol),om,omsol);
detLsol = subst(subst(subst(matdet(L0pfinal),mm,msol),nn,nsol),om,omsol);
checkzero(E2sol,"p*r degree-two solution mismatch");
checkzero(E1sol,"p*r degree-one solution mismatch");
checkzero(detLsol,"p*r singular-linear-part mismatch");

print("fixed-cubic line-row PARI/GP checks passed");
quit;
