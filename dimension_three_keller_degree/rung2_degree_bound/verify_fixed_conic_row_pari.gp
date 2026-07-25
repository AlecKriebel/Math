\\ Independent exact endgame checks for WORKING_FIXED_CONIC_ROW.md.

default(parisizemax, 512000000);
allocatemem(128000000);

cross3(x,y) = [x[2]*y[3]-x[3]*y[2],x[3]*y[1]-x[1]*y[3],x[1]*y[2]-x[2]*y[1]]~;
jacmap(H) = matrix(3,3,i,j,deriv(H[i],[p,q,r][j]));

A = [p^2,p*q,q^2]~;
Ap = vector(3,i,deriv(A[i],p))~;
Aq = vector(3,i,deriv(A[i],q))~;
Delta = cross3(Ap,Aq);

splitH4 = p*q*A;
doubleH4 = p^2*A;
if (cross3(vector(3,i,deriv(splitH4[i],p))~,vector(3,i,deriv(splitH4[i],q))~)-2*p^2*q^2*Delta != [0,0,0]~, error("split top normal mismatch"));
if (cross3(vector(3,i,deriv(doubleH4[i],p))~,vector(3,i,deriv(doubleH4[i],q))~)-2*p^4*Delta != [0,0,0]~, error("double top normal mismatch"));

splitW = aa*p*Ap+dd*q*Aq;
splitZ = [0,-(aa-dd)^2/2,0]~;
splitBranch = matdet(s*jacmap(r^2*splitZ)+s^2*jacmap(r*splitW)+s^3*jacmap(splitH4));
if (polcoef(polcoef(splitBranch,6,s),2,r)-12*p^2*q^2*(aa-dd)^2*(aa+dd) != 0, error("split degree-six branch polynomial mismatch"));

doubleW = aa*p*Ap+(cc*p+dd*q)*Aq;
doubleZ = [(aa-dd)^2,cc*(aa-dd),cc^2]~;
doubleBranch = matdet(s*jacmap(r^2*doubleZ)+s^2*jacmap(r*doubleW)+s^3*jacmap(doubleH4));
if (polcoef(polcoef(doubleBranch,6,s),2,r)-24*dd*p^2*(cc*p+(dd-aa)*q)^2 != 0, error("double degree-six branch polynomial mismatch"));

Crelation = BB+UU*YY+VV*XX+XX*YY;
splitScalarH3 = [(UU-XX)*p^3+(VV-YY)*p^2*q,UU*p^2*q+VV*p*q^2,(UU+XX)*p*q^2+(VV+YY)*q^3]~+2*r*A;
splitScalarH2 = [(2*XX*YY-Crelation+2*BB)*p^2+(-2*VV*YY-YY^2)*p*q-4*YY*p*r,(UU*XX-XX^2)*p^2+BB*p*q+(-VV*YY-YY^2)*q^2+2*XX*p*r-2*YY*q*r,(2*UU*XX-XX^2)*p*q+Crelation*q^2+4*XX*q*r]~;
splitScalarL = [-2*BB*YY+2*Crelation*YY-UU*YY^2-XX*YY^2+2*ell4,YY^2*(VV+YY),2*YY^2;(2*BB*XX-2*Crelation*XX+VV*XX^2+3*XX^2*YY+ell7)/2,ell4,-2*XX*YY;XX^2*(UU-XX),ell7,2*XX^2];
splitScalarDet = matdet(splitScalarL+s*jacmap(splitScalarH2)+s^2*jacmap(splitScalarH3)+s^3*jacmap(splitH4));
for(i=3,8,if(polcoef(splitScalarDet,i,s) != 0,error("split scalar high coefficient mismatch")));
splitQ = BB*YY+UU*YY^2+ell4;
splitR = -2*BB*XX-2*UU*XX*YY+VV*XX^2+XX^2*YY+ell7;
if (polcoef(splitScalarDet,2,s)-(splitR*p-2*splitQ*q)^2 != 0,error("split scalar degree-two square mismatch"));
splitLinearFactor = VV*XX^2*YY+XX^2*YY^2+2*XX*ell4+YY*ell7;
if (matdet(splitScalarL)-splitLinearFactor^2 != 0,error("split scalar linear determinant mismatch"));

doubleB0 = UU*ZZ/2;
doubleC = BB+UU*XX+VV*ZZ/2+XX^2;
doubleScalarH3 = [(UU-XX)*p^3+VV*p^2*q,ZZ*p^3/2+UU*p^2*q+VV*p*q^2,ZZ*p^2*q+(UU+XX)*p*q^2+VV*q^3]~+2*r*A;
doubleScalarH2 = [(2*BB-doubleC+XX^2)*p^2-2*VV*XX*p*q-4*XX*p*r,doubleB0*p^2+BB*p*q-VV*XX*q^2+ZZ*p*r-2*XX*q*r,ZZ^2*p^2/4+(2*doubleB0+XX*ZZ)*p*q+doubleC*q^2+2*ZZ*q*r]~;
doubleScalarL = [-2*BB*XX+2*doubleC*XX-UU*XX^2-XX^3+2*ell4,VV*XX^2,2*XX^2;(-8*doubleB0*XX+4*BB*ZZ-4*doubleC*ZZ+4*UU*XX*ZZ+VV*ZZ^2+4*ell7)/8,ell4,-XX*ZZ;ZZ*(4*doubleB0-UU*ZZ+XX*ZZ)/4,ell7,ZZ^2/2];
doubleScalarDet = matdet(doubleScalarL+s*jacmap(doubleScalarH2)+s^2*jacmap(doubleScalarH3)+s^3*jacmap(doubleH4));
for(i=3,8,if(polcoef(doubleScalarDet,i,s) != 0,error("double scalar high coefficient mismatch")));
doubleQ = BB*XX+UU*XX^2+XX^3+ell4;
doubleR = -4*BB*ZZ-4*UU*XX*ZZ+VV*ZZ^2-4*XX^2*ZZ+4*ell7;
if (polcoef(doubleScalarDet,2,s)-(doubleR*p/4-2*doubleQ*q)^2 != 0,error("double scalar degree-two square mismatch"));
doubleLinearFactor = VV*XX*ZZ^2+4*XX*ell7+4*ZZ*ell4;
if (matdet(doubleScalarL)-doubleLinearFactor^2/16 != 0,error("double scalar linear determinant mismatch"));

print("fixed-divisor conic-row PARI/GP checks passed");
quit;
