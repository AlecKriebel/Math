\\ Independent exact checks for WORKING_SCALAR_ALIGNED_CUSPIDAL_CUBIC_EXIT.md.

default(parisizemax, 512000000);
allocatemem(128000000);

cross3(x,y) = [x[2]*y[3]-x[3]*y[2],x[3]*y[1]-x[1]*y[3],x[1]*y[2]-x[2]*y[1]]~;
jacmap(H) = matrix(3,3,i,j,deriv(H[i],[p,q,r][j]));
coef3(P,ip,iq,ir) = polcoef(polcoef(polcoef(P,ir,r),iq,q),ip,p);
detpoly(H4,H3,H2) = matdet(L0+s*jacmap(H2)+s^2*jacmap(H3)+s^3*jacmap(H4));
upperseven(H4,H3,H2) = polcoef(matdet(s*jacmap(H2)+s^2*jacmap(H3)+s^3*jacmap(H4)),7,s);

A = [p^2*q,p^3,q^3]~;
Ap = vector(3,i,deriv(A[i],p))~;
Aq = vector(3,i,deriv(A[i],q))~;
S = [2*q,3*p,0]~;
T = [p^2,0,3*q^2]~;
N = [3*p*q^2,-2*q^3,-p^3]~;

if (cross3(S,T) != 3*N,error("reduced-normal syzygies mismatch"));
if (cross3(deriv(p*A,p),deriv(p*A,q)) != 4*p^3*N,error("cusp-marked normal mismatch"));
if (cross3(deriv(q*A,p),deriv(q*A,q)) != 4*p*q^2*N,error("flex-marked normal mismatch"));
if (cross3(deriv((p+q)*A,p),deriv((p+q)*A,q)) != 4*p*(p+q)^2*N,error("general-marked normal mismatch"));

L0 = [l0,l1,l2;l3,l4,l5;l6,l7,l8];
B2 = [z0*p^2+z1*p*q+z2*q^2,z3*p^2+z4*p*q+z5*q^2,z6*p^2+z7*p*q+z8*q^2]~;
V0 = [x0*p^3+x1*p^2*q+x2*p*q^2+x3*q^3,x4*p^3+x5*p^2*q+x6*p*q^2+x7*q^3,x8*p^3+x9*p^2*q+x10*p*q^2+x11*q^3]~;

\\ Binary-cubic leaves with kappa=0.
D0p = detpoly(p*A,V0,B2);
E60p = polcoef(D0p,6,s);
if (coef3(E60p,6,0,0) != -4*l8,error("cusp zero-tangent l33 mismatch"));
if (coef3(E60p,4,2,0) != 12*l2,error("cusp zero-tangent l13 mismatch"));
if (coef3(E60p,3,3,0) != -8*l5,error("cusp zero-tangent l23 mismatch"));

D0q = detpoly(q*A,V0,B2);
E60q = polcoef(D0q,6,s);
if (coef3(E60q,4,2,0) != -4*l8,error("flex zero-tangent l33 mismatch"));
if (coef3(E60q,2,4,0) != 12*l2,error("flex zero-tangent l13 mismatch"));
if (coef3(E60q,1,5,0) != -8*l5,error("flex zero-tangent l23 mismatch"));

D0g = detpoly((p+q)*A,V0,B2);
E60g = polcoef(D0g,6,s);
if (coef3(E60g,6,0,0) != -4*l8,error("general zero-tangent l33 mismatch"));
if (coef3(E60g,4,2,0) != 12*l2-4*l8,error("general zero-tangent l13 mismatch"));
if (coef3(E60g,3,3,0) != 24*l2-8*l5,error("general zero-tangent l23 mismatch"));

\\ Binary-cubic leaves with kappa=1.  These are the complete E6
\\ substitutions, retaining every free parameter.
Vbp = [(12*l2+pv10)*p^3/27+(-8*l5-3*pv11+18*pv4)*p^2*q/15+10*pv5*p*q^2/3-2*pv6*q^3/9,pv4*p^3+pv5*p^2*q+pv6*p*q^2,4*l8*p^3/9+pv10*p*q^2+pv11*q^3]~;
Dbp = detpoly(p*A,Vbp,B2+r*S);
if (polcoef(Dbp,6,s) != 0,error("cusp kappa-one E6 solution mismatch"));
if (coef3(polcoef(Dbp,5,s),1,3,1) != 24,error("cusp kappa-one E5 certificate mismatch"));

Vbq = [qv10*p^3/9+(l2+2*qv4)*p^2*q/2+2*(-l5+2*qv5)*p*q^2/3+qv3*q^3,qv4*p^3+qv5*p^2*q+qv7*q^3,l8*p^2*q/2+qv10*p*q^2+qv11*q^3]~;
Dbq = detpoly(q*A,Vbq,B2+r*S);
if (polcoef(Dbq,6,s) != 0,error("flex kappa-one E6 solution mismatch"));
if (coef3(polcoef(Dbq,5,s),0,4,1) != 24,error("flex kappa-one E5 certificate mismatch"));

gv0 = (180*l2+4*l8+15*gv10)/405;
gv1 = (360*l2-360*l5-16*l8+120*gv10-135*gv11+810*gv4)/675;
gv2 = -2*(90*l2+360*l5-64*l8+480*gv10-540*gv11+540*gv4-1125*gv5)/675;
gv3 = -(1440*l2+2160*l5-1024*l8+7680*gv10-8640*gv11+8640*gv4-10800*gv5+675*gv7)/4050;
Vbg = [gv0*p^3+gv1*p^2*q+gv2*p*q^2+gv3*q^3,gv4*p^3+gv5*p^2*q+3*gv7*p*q^2/4+gv7*q^3,4*l8*p^3/9+8*l8*p^2*q/15+gv10*p*q^2+gv11*q^3]~;
Dbg = detpoly((p+q)*A,Vbg,B2+r*S);
if (polcoef(Dbg,6,s) != 0,error("general kappa-one E6 solution mismatch"));
if (coef3(polcoef(Dbg,5,s),1,3,1) != 24,error("general first E5 certificate mismatch"));
if (coef3(polcoef(Dbg,5,s),0,4,1) != 24,error("general second E5 certificate mismatch"));

\\ Nonzero tangent leaf h=p, H3=V+r*A_p.
Vtp = [t0*p^3+t1*p^2*q+t2*p*q^2+t3*q^3,t4*p^3+t5*p^2*q-9*t3*p*q^2/2,t8*p^3+t9*p^2*q+t10*p*q^2+t11*q^3]~;
H3tp = Vtp+r*Ap;
tw2 = (27*t0-t10)/12;
tw4 = (15*t1+3*t11-18*t4+8*tw8)/12;
tw10 = -(3*t2-10*t5)/8;
H2tp = [tw0*p^2+tw1*p*q+tw2*p*r+tw3*q^2+tw4*q*r,tw6*p^2+tw7*p*q+tw8*p*r+tw9*q^2+tw10*q*r+3*r^2/2,tw12*p^2+tw13*p*q+9*t8*p*r/4+tw15*q^2+5*t9*q*r/4]~;
if (upperseven(p*A,H3tp,H2tp) != 0,error("cusp tangent complete E7 family mismatch"));
Dtp = detpoly(p*A,H3tp,H2tp);
if (coef3(polcoef(Dtp,6,s),1,3,2) != -12,error("cusp tangent E6 certificate mismatch"));

\\ Nonzero tangent leaf h=q, H3=V+r*A_p.
Vtpa = [u0*p^3+u1*p^2*q+u2*p*q^2+u3*q^3,u4*p^3+u5*p^2*q+u6*p*q^2+u7*q^3,u9*p^2*q+u10*p*q^2+u11*q^3]~;
H3tpa = Vtpa+r*Ap;
uw2 = 2*(u1-u4);
uw4 = (3*u2-4*u5+2*uw8)/3;
H2tpa = [uw0*p^2+uw1*p*q+uw2*p*r+uw3*q^2+uw4*q*r-r^2,uw6*p^2+uw7*p*q+uw8*p*r+uw9*q^2+u6*q*r,uw12*p^2+uw13*p*q+2*u9*p*r+uw15*q^2+(-9*u0+u10)*q*r]~;
if (upperseven(q*A,H3tpa,H2tpa) != 0,error("flex A_p complete E7 family mismatch"));
Dtpa = detpoly(q*A,H3tpa,H2tpa);
if (coef3(polcoef(Dtpa,6,s),1,3,2) != -48,error("flex A_p E6 certificate mismatch"));

\\ Nonzero tangent leaf h=q, H3=V+r*A_q.
Vtqa = [y0*p^3+y1*p^2*q+y2*p*q^2+y3*q^3,y4*p^3+y5*p^2*q+y6*p*q^2+y7*q^3,y10*p*q^2+y11*q^3]~;
H3tqa = Vtqa+r*Aq;
yw2 = (15*y2-2*y5)/12;
yw4 = (27*y3-10*y6+8*yw8)/12;
yw10 = 9*y7/4;
yw14 = (9*y0+5*y10)/4;
yw16 = -3*(y1-3*y11+2*y4)/4;
H2tqa = [yw0*p^2+yw1*p*q+yw2*p*r+yw3*q^2+yw4*q*r,yw6*p^2+yw7*p*q+yw8*p*r+yw9*q^2+yw10*q*r,yw12*p^2+yw13*p*q+yw14*p*r+yw15*q^2+yw16*q*r+3*r^2]~;
if (upperseven(q*A,H3tqa,H2tqa) != 0,error("flex A_q complete E7 family mismatch"));
Dtqa = detpoly(q*A,H3tqa,H2tqa);
if (coef3(polcoef(Dtqa,6,s),4,0,2) != 12,error("flex A_q E6 certificate mismatch"));

print("scalar-aligned cuspidal-cubic PARI/GP checks passed");
quit;
