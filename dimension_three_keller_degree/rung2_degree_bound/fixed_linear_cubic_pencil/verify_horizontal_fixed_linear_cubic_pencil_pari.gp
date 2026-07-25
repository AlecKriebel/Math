\\ Independent exact checks for the horizontal fixed-linear cubic-pencil theorem.

grad(f) = [deriv(f,x),deriv(f,y),deriv(f,z)]~;
jac3(f,g,k) = matdet(matrix(3,3,i,j,deriv([f,g,k][i],[x,y,z][j])));
jacmap(V) = matrix(3,3,i,j,deriv(V[i],[x,y,z][j]));
cross3(first,second) = [first[2]*second[3]-first[3]*second[2],first[3]*second[1]-first[1]*second[3],first[1]*second[2]-first[2]*second[1]]~;
checkzero(value,message) = if(value != 0,print(Str("FAIL: ",message));quit(1));

homexps(degree) =
{
  my(result=List());
  for(i=0,degree,
    for(j=0,degree-i,
      listput(result,[i,j,degree-i-j])
    )
  );
  Vec(result)
};

coeff3(form,exponents) =
  polcoef(polcoef(polcoef(form,exponents[1],x),exponents[2],y),exponents[3],z);

kernelmatrix(first,second,inputmons,inputdegree) =
{
  my(outputexps=homexps(inputdegree+5));
  matrix(#outputexps,#inputmons,i,j,
    coeff3(jac3(first,second,inputmons[j]),outputexps[i])
  )
};

quadmons = [z^2,y*z,y^2,x*z,x*y,x^2];
cubmons = [z^3,y*z^2,y^2*z,y^3,x*z^2,x*y*z,x*y^2,x^2*z,x^2*y,x^3];

\\ A concrete primitive horizontal Hesse pencil.
h = x+2*y+3*z;
p = x^3+y^3+z^3;
q = x*y*z;
P = h*p;
Q = h*q;

smallJ = jac3(p,q,h);
Dvec = cross3(grad(P),grad(Q));
checkzero(Dvec~*grad(h)-h^2*smallJ,"D(h) identity");
checkzero(Dvec~*grad(p)+h*p*smallJ,"D(p) identity");
checkzero(Dvec~*grad(q)+h*q*smallJ,"D(q) identity");
checkzero(Dvec~*grad(P),"D(P) identity");
checkzero(Dvec~*grad(Q),"D(Q) identity");

\\ Restriction to h=0 has rank two.
prestrict = subst(p,z,-(x+2*y)/3);
qrestrict = subst(q,z,-(x+2*y)/3);
binaryexps = [[0,3],[1,2],[2,1],[3,0]];
restrictionmatrix = matrix(2,4,i,j,polcoef(polcoef(if(i==1,prestrict,qrestrict),binaryexps[j][1],x),binaryexps[j][2],y));
if(matrank(restrictionmatrix)!=2,print("FAIL: horizontal restriction rank");quit(1));

\\ The degree-two and degree-three invariant kernels are zero.
K2 = kernelmatrix(P,Q,quadmons,2);
K3 = kernelmatrix(P,Q,cubmons,3);
if(matrank(K2)!=#quadmons,print("FAIL: horizontal quadratic kernel");quit(1));
if(matrank(K3)!=#cubmons,print("FAIL: horizontal cubic kernel");quit(1));

\\ Exact weighted determinant bookkeeping with an arbitrary-looking invertible L0.
L0 = [1,2,-1;0,1,3;2,-2,1];
H2 = [x^2+2*x*y-y*z, y^2+x*z+3*z^2, x*y+2*y*z-z^2]~;
H3 = [x^3+x*y*z+2*z^3, y^3+2*x^2*z-y*z^2, x^2*y-y^2*z+x*z^2]~;
C = jacmap([P,Q,0]~);
weighted = matdet(L0+w*jacmap(H2)+w^2*jacmap(H3)+w^3*C);
checkzero(polcoef(weighted,8,w)-jac3(P,Q,H3[3]),"E8 coefficient");

H3zero = [H3[1],H3[2],0]~;
weightedzero = matdet(L0+w*jacmap(H2)+w^2*jacmap(H3zero)+w^3*C);
checkzero(polcoef(weightedzero,8,w),"zero-normal E8 coefficient");
checkzero(polcoef(weightedzero,7,w)-jac3(P,Q,H2[3]),"E7 coefficient");

\\ A simple vertical member with a nonzero quadratic first integral.
hs = z;
ps = z*x^2;
qs = x^3+y^3;
Ps = hs*ps;
Qs = hs*qs;
G2s = x*z;
checkzero(Ps-G2s^2,"simple vertical square");
checkzero(jac3(Ps,Qs,G2s),"simple vertical quadratic invariant");

\\ A triple vertical member with cubic and quadratic first integrals.
pt = z^3;
qt = x^3+y^3;
Pt = z^4;
Qt = z*qt;
checkzero(jac3(Pt,Qt,z^3),"triple vertical cubic invariant");
checkzero(jac3(Pt,Qt,z^2),"triple vertical quadratic invariant");

print("horizontal fixed-linear cubic-pencil PARI/GP checks passed");
quit;
