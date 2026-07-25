\\ Independent exact PARI/GP checks for the marked-critical infinity orbit.

jacmap(V) = matrix(3,3,i,j,deriv(V[i],[x,y,z][j]));
jac3(f,g,h) = matdet(jacmap([f,g,h]~));
delta(f) = z*deriv(f,z)-y*deriv(f,y);
coeff3(P,ex,ey,ez) = polcoef(polcoef(polcoef(P,ez,z),ey,y),ex,x);
checkzero(value,message) = if(value != 0,print(Str("FAIL: ",message));quit(1));

p = x^2;
q = y*z;
H4 = [p^2,q^2,0]~;
L = [l0,l1,l2;l3,l4,l5;l6,l7,l8];
quadmons = [x^2,x*y,x*z,y^2,y*z,z^2];
cubmons = [x^3,x^2*y,x^2*z,x*y^2,x*y*z,x*z^2,y^3,y^2*z,y*z^2,z^3];
B2 = d0*x^2+d1*x*y+d2*x*z+d3*y^2+d4*y*z+d5*z^2;
Vgen = r1*x^2*y+r2*x^2*z+r3*x*y^2+r4*x*y*z+r5*x*z^2+r6*y^3+r9*z^3;

\\ Raw E7 polarization.
ucoeffs = [uu0,uu1,uu2,uu3,uu4,uu5,uu6,uu7,uu8,uu9];
vcoeffs = [vv0,vv1,vv2,vv3,vv4,vv5,vv6,vv7,vv8,vv9];
wcoeffs = [ww0,ww1,ww2,ww3,ww4,ww5];
Uraw = sum(i=1,10,ucoeffs[i]*cubmons[i]);
Vraw = sum(i=1,10,vcoeffs[i]*cubmons[i]);
Wraw = sum(i=1,6,wcoeffs[i]*quadmons[i]);
E7raw = jac3(p^2,q^2,Wraw)+jac3(p^2,Vraw,x^3)+jac3(Uraw,q^2,x^3);
checkzero(E7raw+2*x^2*q*delta(3*Uraw-4*x*Wraw),"raw E7");

\\ Case A != 0, C != 0.
W1 = w0*p+w4*q;
U21 = u0*p+4*l7*x*y/3+4*l8*x*z/3+u4*q;
H31 = [CC*x*q,BB*x*q,x^3]~;
H21 = [U21,B2,W1]~;
wd1 = matdet(L+zz*jacmap(H21)+zz^2*jacmap(H31)+zz^3*jacmap(H4));
checkzero(polcoef(wd1,6,zz),"case 1 E6");
E51 = polcoef(wd1,5,zz);
checkzero(coeff3(E51,0,3,2)+2*CC*l7,"case 1 l32");
checkzero(coeff3(E51,0,2,3)-2*CC*l8,"case 1 l33");
checkzero(subst(subst(coeff3(E51,2,2,1),l7,0),l8,0)-6*l1,"case 1 l12");
checkzero(subst(subst(coeff3(E51,2,1,2),l7,0),l8,0)+6*l2,"case 1 l13");
checkzero(matdet([l0,0,0;l3,l4,l5;l6,0,0]),"case 1 determinant");

\\ Case A != 0, C = 0.
W2c = w0*p+w1*x*y+w2*x*z-3*AA*q/4;
U32 = 4*x*W2c/3+AA*x*q;
U22 = u0*p+(4*l7/3+4*w0*w1/9)*x*y+(4*l8/3+4*w0*w2/9)*x*z+2*w1^2*y^2/9+u4*q+2*w2^2*z^2/9;
H32 = [U32,BB*x*q,x^3]~;
H22 = [U22,B2,W2c]~;
wd2 = matdet(L+zz*jacmap(H22)+zz^2*jacmap(H32)+zz^3*jacmap(H4));
checkzero(polcoef(wd2,6,zz),"case 2 E6");
E52 = polcoef(wd2,5,zz);
checkzero(coeff3(E52,0,4,1)-8*w1^3/9,"case 2 w1 cube");
checkzero(coeff3(E52,0,1,4)+8*w2^3/9,"case 2 w2 cube");
E42 = polcoef(wd2,4,zz);
E42s = subst(subst(subst(subst(subst(subst(subst(subst(E42,w1,0),w2,0),d1,0),d2,0),d3,0),d5,0),l1,4*w0*l7/9),l2,4*w0*l8/9);
checkzero(coeff3(E42s,0,3,1)+8*l7^2/3,"case 2 l32 square");
checkzero(coeff3(E42s,0,1,3)-8*l8^2/3,"case 2 l33 square");

\\ Case A = 0, C != 0.
W3c = w0*p+3*CC*q/4;
H33 = [CC*x*q,Vgen,x^3]~;
H23 = [U21,B2,W3c]~;
wd3 = matdet(L+zz*jacmap(H23)+zz^2*jacmap(H33)+zz^3*jacmap(H4));
checkzero(polcoef(wd3,6,zz),"case 3 E6");
E53 = polcoef(wd3,5,zz);
checkzero(coeff3(E53,1,3,1)-3*CC^2*r3/2,"case 3 r3");
checkzero(coeff3(E53,1,1,3)+3*CC^2*r5/2,"case 3 r5");
checkzero(coeff3(E53,0,4,1)-9*CC^2*r6/4,"case 3 r6");
checkzero(coeff3(E53,0,1,4)+9*CC^2*r9/4,"case 3 r9");
checkzero(coeff3(E53,0,3,2)+2*CC*l7,"case 3 l32");
checkzero(coeff3(E53,0,2,3)-2*CC*l8,"case 3 l33");

\\ Resonant K=0 subbranch, built directly after the E5/E4 solves.
L3r = [l0,-CC^2*r1/8,-CC^2*r2/8;l3,l4,l5;l6,0,0];
U23r = u0*p-2*CC*w0*q/3;
B23r = d0*p+2*r1*w0*x*y/3+2*r2*w0*x*z/3+d4*q;
H23r = [U23r,B23r,W3c]~;
wd3r = matdet(L3r+zz*jacmap(H23r)+zz^2*jacmap(H33)+zz^3*jacmap(H4));
E23r = polcoef(wd3r,2,zz);
expected23 = -3*CC^2*(r1*l5-r2*l4)/8;
checkzero(coeff3(E23r,2,0,0)-expected23,"case 3 resonant E2");
checkzero(matdet(L3r)-l6*expected23/3,"case 3 determinant factor");

\\ Case A = C = 0 before the target shear.
W4raw = w0*p+w1*x*y+w2*x*z;
U34raw = 4*x*W4raw/3;
U24raw = u0*p+(4*l7/3+4*w0*w1/9)*x*y+(4*l8/3+4*w0*w2/9)*x*z+2*w1^2*y^2/9+u4*q+2*w2^2*z^2/9;
wd4raw = matdet(L+zz*jacmap([U24raw,B2,W4raw]~)+zz^2*jacmap([U34raw,Vgen,x^3]~)+zz^3*jacmap(H4));
checkzero(polcoef(wd4raw,6,zz),"case 4 raw E6");
E54raw = polcoef(wd4raw,5,zz);
checkzero(coeff3(E54raw,0,4,1)-8*w1^3/9,"case 4 w1 cube");
checkzero(coeff3(E54raw,0,1,4)+8*w2^3/9,"case 4 w2 cube");

\\ Post-shear canonical form.
W4 = w0*p;
H34 = [0,Vgen,x^3]~;
H24 = [U21,B2,W4]~;
wd4 = matdet(L+zz*jacmap(H24)+zz^2*jacmap(H34)+zz^3*jacmap(H4));
checkzero(polcoef(wd4,6,zz),"case 4 E6");
E54 = polcoef(wd4,5,zz);
checkzero(subst(coeff3(E54,2,2,1),l1,-8*w0*l7/9),"case 4 l12");
checkzero(subst(coeff3(E54,2,1,2),l2,-8*w0*l8/9),"case 4 l13");
E44 = polcoef(wd4,4,zz);
E44s = subst(subst(E44,l1,-8*w0*l7/9),l2,-8*w0*l8/9);
checkzero(coeff3(E44s,0,3,1)+8*l7^2/3,"case 4 l32 square");
checkzero(coeff3(E44s,0,1,3)-8*l8^2/3,"case 4 l33 square");

print("line-(2,2) marked-critical infinity PARI/GP checks passed");
quit;
