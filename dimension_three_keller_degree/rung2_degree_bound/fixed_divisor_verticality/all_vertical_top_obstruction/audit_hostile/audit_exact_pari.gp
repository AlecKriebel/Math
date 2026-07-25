\\ Independent exact PARI/GP reconstruction of the normal forms and kernels.

x='x; y='y; z='z;
a='a; b='b; c='c; A='A; B='B;
vars=[x,y,z];

fail(label,value) = {
  print(Str("FAIL ",label,": ",value));
  quit(1)
};
checkzero(value,label) = if(value != 0,fail(label,value));
checkequal(value,expected,label) = checkzero(value-expected,label);
gradmat(F) = matrix(3,3,i,j,deriv(F[i],vars[j]));
jac3(f,g,h) = matdet(gradmat([f,g,h]));
cf(P,i,j,k) = polcoeff(polcoeff(polcoeff(P,i,x),j,y),k,z);
exponents(d) = {
  my(L=List());
  forstep(i=d,0,-1,
    forstep(j=d-i,0,-1,listput(L,[i,j,d-i-j]))
  );
  Vec(L)
};
monomial(e) = x^e[1]*y^e[2]*z^e[3];
e3=exponents(3);
e4=exponents(4);
e8=exponents(8);
mons3=vector(#e3,i,monomial(e3[i]));

mapmatrix(first,second,eout) = {
  matrix(#eout,#e3,i,j,cf(jac3(first,second,mons3[j]),eout[i][1],eout[i][2],eout[i][3]))
};

checkkernel(label,first,second,eout,expectedrank,witnesses) = {
  my(M=mapmatrix(first,second,eout));
  checkequal(matrank(M),expectedrank,Str(label," rank"));
  for(i=1,#witnesses,checkzero(jac3(first,second,witnesses[i]),Str(label," witness ",i)));
};

\\ Universal determinant factorization in the p=h shape, with generic
\\ coefficient parameters specialized only after the polynomial identity.
h=x^2+2*x*y+3*y*z+5*z^2;
q=2*x^2+x*z+y^2+7*z^2;
G=x^3+2*x^2*y+3*x*y*z+5*z^3;
checkzero(jac3(h^2,h*q,G)-2*h^2*jac3(h,q,G),"p=h determinant factorization");

\\ Explicit source/pencil normalizations.
r2=y*z+a*x*y+b*x*z+c*x^2;
Y2=y+b*x;
Z2=z+a*x;
checkzero(r2-(Y2*Z2+(c-a*b)*x^2),"rank-two restriction normalization");

r1=y^2+a*x*y+b*x*z+c*x^2;
Y1=y+a*x/2;
checkzero(r1-(Y1^2+b*x*z+(c-a^2/4)*x^2),"rank-one restriction completion");

\\ The canonical pencils have a unique double member.  For the first
\\ pencil B=0 gives x^2, while B!=0 has the displayed nonzero 2x2 minor.
Mtwo=[A,0,0;0,0,B/2;0,B/2,0];
checkequal(matdet(Mtwo),-A*B^2/4,"rank-two pencil conic determinant");
checkequal(matdet(vecextract(Mtwo,[2,3],[2,3])),-B^2/4,"rank-two pencil excludes a second double line");

Mone=[A,0,B/2;0,B,0;B/2,0,0];
checkequal(matdet(Mone),-B^3/4,"rank-one pencil excludes a second double line");

\\ Exact Q-ranks and complete displayed kernels.
checkkernel("rank-two canonical",x^2,y*z,e4,8,[x^3,x*y*z]);
checkkernel("rank-one canonical",x^2,y^2+x*z,e4,8,[x^3,x*(y^2+x*z)]);
checkkernel("binary nonminimal",x^2,y^2,e4,6,[x^3,x^2*y,x*y^2,y^3]);

\\ The original degree-eight maps for representative impossible shapes
\\ have full cubic rank, while the double-member p=h sample has rank 8.
checkkernel("square generic",z^2*(z*x),z^2*(x^2+y^2),e8,10,[]);
checkkernel("square other double",z^2*(z*x),z^2*y^2,e8,10,[]);
checkkernel("distinct split",(y*z)*(x*y),(y*z)*z^2,e8,10,[]);
checkkernel("no-double p=h",(x^2+y^2+z^2)^2,(x^2+y^2+z^2)*(x^2+2*y^2+3*z^2),e8,10,[]);
checkkernel("double-member p=h",(x^2+y^2+z^2)^2,(x^2+y^2+z^2)*z^2,e8,8,[z^3,z*(x^2+y^2)]);

print("PASS: hostile exact PARI normal-form and kernel reconstruction");
quit;
