\\ Independent exact regression for the scalar-aligned nodal-cubic exit.

default(parisizemax, 512000000);
allocatemem(128000000);

cross3(x,y) = [x[2]*y[3]-x[3]*y[2],x[3]*y[1]-x[1]*y[3],x[1]*y[2]-x[2]*y[1]]~;
jacmap(H) = matrix(3,3,i,j,deriv(H[i],[p,q,r][j]));
coeff3(P,i,j,l) = polcoef(polcoef(polcoef(P,l,r),j,q),i,p);

A = [p^2*q,p*q^2,p^3+q^3]~;
Ap = vector(3,i,deriv(A[i],p))~;
Aq = vector(3,i,deriv(A[i],q))~;
Delta = cross3(Ap,Aq);
h = p+k*q;
H4 = h*A;

topNormal = cross3(vector(3,i,deriv(H4[i],p))~,vector(3,i,deriv(H4[i],q))~);
if (topNormal-4*h^2*Delta/3 != [0,0,0]~, error("top-normal identity mismatch"));

V = [v1*p^3+v2*p^2*q+v3*p*q^2+v4*q^3,v5*p^3+v6*p^2*q+v7*p*q^2+v8*q^3,v9*p^3+v10*p^2*q+v11*p*q^2+v12*q^3]~;
H2 = [w1*p^2+w2*p*q+w3*q^2+w4*p*r+w5*q*r+w6*r^2,w7*p^2+w8*p*q+w9*q^2+w10*p*r+w11*q*r+w12*r^2,w13*p^2+w14*p*q+w15*q^2+w16*p*r+w17*q*r+w18*r^2]~;
H3 = V+r*(alpha*Ap+beta*Aq);

weighted = s*jacmap(H2)+s^2*jacmap(H3)+s^3*jacmap(H4);
E7 = polcoef(matdet(weighted),7,s);

mons = [[7,0,0],[6,1,0],[6,0,1],[5,2,0],[5,1,1],[4,3,0],[4,2,1],[3,4,0],[3,3,1],[2,5,0],[2,4,1],[1,6,0],[1,5,1],[0,7,0],[0,6,1]];
ee = vector(15,j,coeff3(E7,mons[j][1],mons[j][2],mons[j][3]));

L0 = -2*(2*k^3-1)*ee[3]+3*k^2*ee[5]-2*k*ee[7]+ee[9];
L1 = -3*k*(k-1)*(k^2+k+1)*ee[3]+(4*k^3+1)*ee[5]/2-k^2*ee[7]+ee[11];
L2 = k*ee[5]+ee[13];
L3 = -k^3*ee[3]+k^2*ee[5]/2+ee[15];

C0 = k*alpha^2+2*k^2*alpha*beta+(k^3-3)*beta^2;
C1 = 2*k^2*alpha^2+(4*k^3+6)*alpha*beta+(2*k^4-9*k)*beta^2;
C2 = alpha^2-4*k*alpha*beta+k^2*beta^2;
C3 = k*(-2*alpha^2+2*k*alpha*beta+k^2*beta^2);

if (L0-8*C0 != 0, error("first left-null certificate mismatch"));
if (L1-4*C1 != 0, error("second left-null certificate mismatch"));
if (L2+8*C2 != 0, error("third left-null certificate mismatch"));
if (L3-4*C3 != 0, error("fourth left-null certificate mismatch"));

binaryWeighted = s*jacmap(H2)+s^2*jacmap(V)+s^3*jacmap(H4);
binaryE7 = polcoef(matdet(binaryWeighted),7,s);
expectedBinaryE7 = 4*h^2*(Delta[1]*deriv(H2[1],r)+Delta[2]*deriv(H2[2],r)+Delta[3]*deriv(H2[3],r))/3;
if (binaryE7-expectedBinaryE7 != 0, error("binary-collapse identity mismatch"));

print("scalar-aligned nodal PARI/GP checks passed");
quit;
