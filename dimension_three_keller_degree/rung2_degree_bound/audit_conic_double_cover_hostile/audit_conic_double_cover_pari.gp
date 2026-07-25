\\ Independent exact PARI/GP reconstruction of the conic double-cover row.
\\ This file intentionally does not import or translate the SymPy verifier.

jacmap(V) = matrix(3,3,i,j,deriv(V[i],[xx,yy,zz][j]));
dx(V) = vector(3,i,deriv(V[i],xx))~;
dy(V) = vector(3,i,deriv(V[i],yy))~;
coeffxyz(P,ex,ey,ez) = polcoef(polcoef(polcoef(P,ez,zz),ey,yy),ex,xx);
checkzero(value,message) = if(value != 0,print(Str("FAIL: ",message));quit(1));
checktrue(value,message) = if(!value,print(Str("FAIL: ",message));quit(1));

homexponents(degree) =
{
  my(result=List());
  for (ex=0,degree,
    for (ey=0,degree-ex,
      listput(result,[ex,ey,degree-ex-ey])
    )
  );
  Vec(result);
};

nonzerocoefficients(P,degree) =
{
  my(exponents=homexponents(degree),result=List(),value);
  for (i=1,#exponents,
    value=coeffxyz(P,exponents[i][1],exponents[i][2],exponents[i][3]);
    if (value != 0,listput(result,value))
  );
  Vec(result)~;
};

linearmatrix(equations,unknowns) =
  matrix(#equations,#unknowns,i,j,deriv(equations[i],unknowns[j]));

substall(value,unknowns,replacements) =
{
  my(result=value);
  for (i=1,#unknowns,result=subst(result,unknowns[i],replacements[i]));
  result;
};

constantvector(equations,unknowns) =
  substall(equations,unknowns,vector(#unknowns));

{
cubicmonomials =
  [xx^3,xx^2*yy,xx*yy^2,yy^3,xx^2*zz,xx*yy*zz,yy^2*zz,
   xx*zz^2,yy*zz^2,zz^3];
quadraticmonomials = [xx^2,xx*yy,yy^2,xx*zz,yy*zz,zz^2];
cubicexponents =
  [[3,0,0],[2,1,0],[1,2,0],[0,3,0],[2,0,1],[1,1,1],[0,2,1],
   [1,0,2],[0,1,2],[0,0,3]];

H4 = [xx^4,xx^2*yy^2,yy^4]~;
J4 = jacmap(H4);
normal = [8*xx*yy^5,-16*xx^3*yy^3,8*xx^5*yy]~;
e3 = [0,0,1]~;
checkzero(matadjoint(J4)-e3*normal~,"leading adjugate");

\\ E8: start from all thirty cubic coefficients.
rawcubic =
  [r00,r01,r02,r03,r04,r05,r06,r07,r08,r09,
   r10,r11,r12,r13,r14,r15,r16,r17,r18,r19,
   r20,r21,r22,r23,r24,r25,r26,r27,r28,r29];
rawH3 =
  [sum(i=1,10,rawcubic[i]*cubicmonomials[i]),
   sum(i=1,10,rawcubic[10+i]*cubicmonomials[i]),
   sum(i=1,10,rawcubic[20+i]*cubicmonomials[i])]~;
weighted8 = matdet(tt^2*jacmap(rawH3)+tt^3*J4);
E8raw = polcoef(weighted8,8,tt);
equations8 = nonzerocoefficients(E8raw,8);
matrix8 = linearmatrix(equations8,rawcubic);
checktrue(matrank(matrix8)==16,"E8 rank");
checktrue(matsize(matker(matrix8))[2]==14,"E8 nullity");
checkzero(E8raw-normal~*vector(3,i,deriv(rawH3[i],zz))~,"E8 raw identity");

cvars = [c0,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11];
C3 =
  [c0*xx^3+c1*xx^2*yy+c2*xx*yy^2+c3*yy^3,
   c4*xx^3+c5*xx^2*yy+c6*xx*yy^2+c7*yy^3,
   c8*xx^3+c9*xx^2*yy+c10*xx*yy^2+c11*yy^3]~;
T2 = [2*a*xx^2,a*yy^2+b*xx^2,2*b*yy^2]~;
H3 = C3+zz*T2;
checkzero(normal~*vector(3,i,deriv(H3[i],zz))~,"E8 displayed kernel");

candidateparameters = concat(cvars,[a,b]);
candidateslots = vector(30);
for (component=1,3,
  for (i=1,10,
    candidateslots[10*(component-1)+i] =
      coeffxyz(H3[component],cubicexponents[i][1],
              cubicexponents[i][2],cubicexponents[i][3])
  )
);
candidatematrix =
  matrix(30,#candidateparameters,i,j,deriv(candidateslots[i],
                                          candidateparameters[j]));
checktrue(matrank(candidatematrix)==14,"E8 displayed-kernel independence");
checkzero(matrix8*candidatematrix,"E8 displayed-kernel containment");

\\ E7: all eighteen quadratic coefficients, with no binary restriction.
wvars =
  [w0,w1,w2,w3,w4,w5,w6,w7,w8,w9,w10,w11,w12,w13,w14,w15,w16,w17];
rawH2 =
  [sum(i=1,6,wvars[i]*quadraticmonomials[i]),
   sum(i=1,6,wvars[6+i]*quadraticmonomials[i]),
   sum(i=1,6,wvars[12+i]*quadraticmonomials[i])]~;
weighted7 = matdet(tt*jacmap(rawH2)+tt^2*jacmap(H3)+tt^3*J4);
E7raw = polcoef(weighted7,7,tt);
equations7 = nonzerocoefficients(E7raw,7);
matrix7 = linearmatrix(equations7,wvars);
checktrue(#equations7==11,"E7 row count");
checktrue(matrank(matrix7)==9,"E7 rank");
checktrue(matsize(matker(matrix7))[2]==9,"E7 nullity");
binaryindices = [1,2,3,7,8,9,13,14,15];
for (i=1,#binaryindices,
  checkzero(matrix7[,binaryindices[i]],"E7 binary-kernel column")
);
checkzero(coeffxyz(E7raw,7,0,0)+4*b*c9,"E7 x7 endpoint");
checkzero(coeffxyz(E7raw,0,7,0)+4*a*c2,"E7 y7 endpoint");

qvars = [q0,q1,q2,q3,q4,q5,q6,q7,q8];
B2 =
  [q0*xx^2+q1*xx*yy+q2*yy^2,
   q3*xx^2+q4*xx*yy+q5*yy^2,
   q6*xx^2+q7*xx*yy+q8*yy^2]~;
solvedH2 = B2 +
  [zz*((3*a*c0-2*a*c6+2*b*c2)*xx/2
       +(2*a*c1+3*b*c3)*yy/2)+a^2*zz^2,
   zz*((-a*c10+6*a*c4+4*b*c6)*xx/4
       +(4*a*c5-b*c1+6*b*c7)*yy/4)+a*b*zz^2,
   zz*((3*a*c8+2*b*c10)*xx/2
       +(2*a*c9+3*b*c11-2*b*c5)*yy/2)+b^2*zz^2]~;
E7solved = polcoef(matdet(tt*jacmap(solvedH2)+tt^2*jacmap(H3)+tt^3*J4),
                    7,tt);
checkzero(E7solved+4*b*c9*xx^7+4*a*c2*yy^7,"E7 complete solve");

\\ Common linear part and degree-six unknown ordering.
lvars = [l0,l1,l2,l3,l4,l5,l6,l7,l8];
L0 = [l0,l1,l2;l3,l4,l5;l6,l7,l8];
unknowns6 = concat(qvars,lvars);

\\ Both a and b nonzero.
H3g = substall(H3,[a,b,c2,c9],[1,1,0,0]);
H2g = substall(solvedH2,[a,b,c2,c9],[1,1,0,0]);
weightedg = matdet(L0+tt*jacmap(H2g)+tt^2*jacmap(H3g)+tt^3*J4);
E6g = polcoef(weightedg,6,tt);
equations6g = nonzerocoefficients(E6g,6);
matrix6g = linearmatrix(equations6g,unknowns6);
checktrue(#equations6g==13,"two-nonzero E6 row count");
checktrue(matrank(matrix6g)==6,"two-nonzero E6 rank");
checktrue(matsize(matker(matrix6g))[2]==12,"two-nonzero E6 nullity");
checkzero(matrix6g-substall(matrix6g,cvars,vector(12)),
          "two-nonzero E6 matrix specialization dependence");

checkzero(coeffxyz(E6g,5,0,1)-6*(-c11+2*c5),
          "two-nonzero compatibility c11");
checkzero(coeffxyz(E6g,4,1,1)+6*c8,
          "two-nonzero compatibility c8");
checkzero(coeffxyz(E6g,3,2,1)+6*(c1-2*c7),
          "two-nonzero compatibility c1");
checkzero(coeffxyz(E6g,2,3,1)-6*(-c10+2*c4),
          "two-nonzero compatibility c10");
checkzero(coeffxyz(E6g,1,4,1)+6*c3,
          "two-nonzero compatibility c3");
checkzero(coeffxyz(E6g,0,5,1)+6*(c0-2*c6),
          "two-nonzero compatibility c0");

rhs6g = -constantvector(equations6g,unknowns6);
left6g = matker(matrix6g~);
compat6g = left6g~*rhs6g;
genericrelationvars = [c0,c1,c2,c3,c8,c9,c10,c11];
genericrelationvalues = [2*c6,2*c7,0,0,0,0,2*c4,2*c5];
checkzero(substall(compat6g,genericrelationvars,genericrelationvalues),
          "two-nonzero E6 converse compatibilities");

C3g = substall(C3,genericrelationvars,genericrelationvalues);
mug = -c4;
nug = -c7;
xig = (c4-c6)/2;
etag = (c7-c5)/2;
gaugeg = xig*dx(H4)+etag*dy(H4)+(mug*xx+nug*yy)*[2*xx^2,xx^2+yy^2,2*yy^2]~;
checkzero(C3g+gaugeg,"two-nonzero affine gauge");

H3canonical = zz*[2*xx^2,xx^2+yy^2,2*yy^2]~;
H2canonical = B2+zz^2*[1,1,1]~;
weightedcanonical =
  matdet(L0+tt*jacmap(H2canonical)+tt^2*jacmap(H3canonical)+tt^3*J4);
canonicalsolutionvars = [q1,q4,q7,l2,l5,l8];
canonicalsolutionvalues = [0,0,0,q0+q2,q3+q5,q6+q8];
checkzero(substall(polcoef(weightedcanonical,6,tt),
                   canonicalsolutionvars,canonicalsolutionvalues),
          "two-nonzero canonical E6 solution");
E5canonical = substall(polcoef(weightedcanonical,5,tt),
                       canonicalsolutionvars,canonicalsolutionvalues);
expectedE5canonical =
  -4*l7*xx^5-4*l6*xx^4*yy+8*l4*xx^3*yy^2
  +8*l3*xx^2*yy^3-4*l1*xx*yy^4-4*l0*yy^5;
checkzero(E5canonical-expectedE5canonical,"two-nonzero E5 exit");

\\ Exactly one of a,b nonzero.
H3o = substall(H3,[a,b,c2],[1,0,0]);
H2o = substall(solvedH2,[a,b,c2],[1,0,0]);
weightedo = matdet(L0+tt*jacmap(H2o)+tt^2*jacmap(H3o)+tt^3*J4);
E6o = polcoef(weightedo,6,tt);
equations6o = nonzerocoefficients(E6o,6);
matrix6o = linearmatrix(equations6o,unknowns6);
checktrue(#equations6o==10,"one-nonzero E6 row count");
checktrue(matrank(matrix6o)==6,"one-nonzero E6 rank");
checktrue(matsize(matker(matrix6o))[2]==12,"one-nonzero E6 nullity");
checkzero(matrix6o-substall(matrix6o,cvars,vector(12)),
          "one-nonzero E6 matrix specialization dependence");
checkzero(coeffxyz(E6o,4,1,1)+6*c8,"one-nonzero compatibility c8");
checkzero(coeffxyz(E6o,2,3,1)-6*(-c10+2*c4),
          "one-nonzero compatibility c10");
checkzero(coeffxyz(E6o,0,5,1)+6*(c0-2*c6),
          "one-nonzero compatibility c0");
checkzero(coeffxyz(E6o,6,0,0)-c10*c9,
          "one-nonzero compatibility product");

oneinitialvars = [c0,c2,c8,c10];
oneinitialvalues = [2*c6,0,0,2*c4];
C3o = substall(C3,oneinitialvars,oneinitialvalues);
gaugeo = -c6*dx(H4)/2-c5*dy(H4)/2-c7*yy*[2*xx^2,yy^2,0]~;
normalC3 =
  [S*xx^2*yy+D*yy^3,
   P*xx^3,
   M*xx^2*yy+2*P*xx*yy^2+N*yy^3]~;
normalmodulivalues = [c1-2*c7,c3,c4,c9,c11-2*c5];
checkzero(C3o+gaugeo-substall(normalC3,[S,D,P,M,N],normalmodulivalues),
          "one-nonzero affine gauge");
checkzero(substall(c10*c9,oneinitialvars,oneinitialvalues)-2*c4*c9,
          "one-nonzero product slice");

normalH3 = normalC3+zz*[2*xx^2,yy^2,0]~;
normalH2 =
  [q0*xx^2+3*D*P*xx*yy/2+q2*yy^2+S*yy*zz+zz^2,
   q3*xx^2-P*S*xx*yy/4+q5*yy^2+P*xx*zz,
   q6*xx^2+3*N*P*xx*yy/2+q8*yy^2+M*yy*zz]~;
normalL0 = [l0,l1,q0;l3,l4,q3;l6,l7,q6-P^2];
normalweighted =
  matdet(normalL0+tt*jacmap(normalH2)+tt^2*jacmap(normalH3)+tt^3*J4);
normalE6 = polcoef(normalweighted,6,tt);
checkzero(normalE6-2*M*P*xx^6,"one-nonzero complete E6 solve");

free6 = [q0,q2,q3,q5,q6,q8,l0,l1,l3,l4,l6,l7];
solutionslots =
  [q0,3*D*P/2,q2,q3,-P*S/4,q5,q6,3*N*P/2,q8,
   l0,l1,q0,l3,l4,q3,l6,l7,q6-P^2];
solutiontangent =
  matrix(18,12,i,j,deriv(solutionslots[i],free6[j]));
checktrue(matrank(solutiontangent)==12,"one-nonzero E6 solution dimension");

normalE5 = polcoef(normalweighted,5,tt);
expectednormalE5 =
  3*N*P^2*xx^5+(-M*P*S+8*P*q8-8*l6)*xx^4*yy/2
  +6*M*P*xx^4*zz+3*P^2*S*xx^3*yy^2
  -(3*D*M*P+16*P*q5-16*l3)*xx^2*yy^3/2
  +3*D*P^2*xx*yy^4+(-P*S^2+4*P*q2-4*l0)*yy^5;
checkzero(normalE5-expectednormalE5,"one-nonzero E5 table");

nonzeroPvars = [M,N,S,D,l0,l3,l6];
nonzeroPvalues = [0,0,0,0,P*q2,P*q5,P*q8];
E4nonzeroP = substall(polcoef(normalweighted,4,tt),
                      nonzeroPvars,nonzeroPvalues);
expectedE4nonzeroP = 2*P*l7*xx^4-4*P*l4*xx^2*yy^2+2*P*l1*yy^4;
checkzero(E4nonzeroP-expectedE4nonzeroP,"one-nonzero P-nonzero E4 exit");

\\ Hostile zero-specialization check omitted from the original prose:
\\ at P=0, E5 itself kills the first linear column.
E5Pzero = subst(normalE5,P,0);
expectedE5Pzero = -4*l6*xx^4*yy+8*l3*xx^2*yy^3-4*l0*yy^5;
checkzero(E5Pzero-expectedE5Pzero,"one-nonzero P-zero E5 strengthening");

UU = ucoordinate;
Pzeromap = subst(normalL0*[xx,yy,zz]~+normalH2+normalH3+H4,P,0);
PzeroinU = subst(Pzeromap,zz,UU-xx^2);
expectedPzeromap =
  [l0,l3,l6]~*xx+[l1,l4,l7]~*yy+[q0,q3,q6]~*UU
  +[UU^2+S*yy*UU+D*yy^3+q2*yy^2,
    UU*yy^2+q5*yy^2,
    yy^4+M*yy*UU+N*yy^3+q8*yy^2]~;
checkzero(PzeroinU-expectedPzeromap,"P-zero coordinate factorization");

swapmatrix = [0,0,1;0,1,0;1,0,0];
swappedH4 = subst(subst(swapmatrix*H4,xx,swapdummy),yy,xx);
swappedH4 = subst(swappedH4,swapdummy,yy);
checkzero(swappedH4-H4,"source-target involution");

print("AUDIT_CONIC_DOUBLE_COVER_PARI_PASS_7E4A91");
}
quit;
