\\ Hostile independent exact checks omitted or only implicit in the supplied
\\ regressions: raw ranks, full-kernel dimensions, specialization constancy,
\\ and literal determinant divisibility.

jacmap(V) = matrix(3,3,i,j,deriv(V[i],[p,q,r][j]));
coeff3(P,ep,eq,er) = polcoef(polcoef(polcoef(P,er,r),eq,q),ep,p);
checkzero(value,message) = if(value != 0,print(Str("FAIL: ",message));quit(1));
checktrue(value,message) = if(!value,print(Str("FAIL: ",message));quit(1));
solvevar(expression,variable) = -subst(expression,variable,0)/deriv(expression,variable);

homexponents(degree) =
{
  my(result=List());
  for (ep=0,degree,
    for (eq=0,degree-ep,
      listput(result,[ep,eq,degree-ep-eq])
    )
  );
  Vec(result);
};

nonzerocoefficients(P,degree) =
{
  my(exponents=homexponents(degree),result=List(),value);
  for (i=1,#exponents,
    value=coeff3(P,exponents[i][1],exponents[i][2],exponents[i][3]);
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

cubicslots(V) =
{
  my(result=vector(20));
  for (component=1,2,
    for (i=1,10,
      result[10*(component-1)+i] =
        coeff3(V[component],cubicexponents[i][1],
               cubicexponents[i][2],cubicexponents[i][3])
    )
  );
  result;
};

quadraticslots(V) =
{
  my(result=vector(12));
  for (component=1,2,
    for (i=1,6,
      result[6*(component-1)+i] =
        coeff3(V[component],quadraticexponents[i][1],
               quadraticexponents[i][2],quadraticexponents[i][3])
    )
  );
  result;
};

{
cubicmonomials =
  [p^3,p^2*q,p*q^2,q^3,p^2*r,p*q*r,q^2*r,p*r^2,q*r^2,r^3];
cubicexponents =
  [[3,0,0],[2,1,0],[1,2,0],[0,3,0],[2,0,1],
   [1,1,1],[0,2,1],[1,0,2],[0,1,2],[0,0,3]];
quadraticmonomials = [p^2,p*q,q^2,p*r,q*r,r^2];
quadraticexponents =
  [[2,0,0],[1,1,0],[0,2,0],[1,0,1],[0,1,1],[0,0,2]];

H4 = [p^2*r^2,q^2*r^2,0]~;
J4 = jacmap(H4);
uvars =
  [u00,u01,u02,u03,u04,u05,u06,u07,u08,u09,
   u10,u11,u12,u13,u14,u15,u16,u17,u18,u19];
H3raw =
  [sum(i=1,10,uvars[i]*cubicmonomials[i]),
   sum(i=1,10,uvars[10+i]*cubicmonomials[i]),0]~;
vvars = [v00,v01,v02,v03,v04,v05,v10,v11,v12,v13,v14,v15];
H2first =
  [sum(i=1,6,vvars[i]*quadraticmonomials[i]),
   sum(i=1,6,vvars[6+i]*quadraticmonomials[i])]~;
L0 = [l00,l01,l02;l10,l11,l12;l20,l21,l22];
topunknowns = concat(uvars,[l20,l21,l22]);
lowerunknowns = concat(vvars,[l00,l01,l02,l10,l11,l12]);

\\ Raw E6 for H2_3=pr.
H2rawpr = [H2first[1],H2first[2],p*r]~;
wrawpr = matdet(L0+zz*jacmap(H2rawpr)+zz^2*jacmap(H3raw)+zz^3*J4);
E6rawpr = polcoef(wrawpr,6,zz);
eq6pr = nonzerocoefficients(E6rawpr,6);
A6pr = linearmatrix(eq6pr,topunknowns);
checktrue(#eq6pr==10,"raw pr E6 row count");
checktrue(matrank(A6pr)==10,"raw pr E6 rank");
checktrue(matsize(matker(A6pr))[2]==13,"raw pr E6 nullity");
checkzero(constantvector(eq6pr,topunknowns),"raw pr E6 affine remainder");
checkzero(A6pr-substall(A6pr,lowerunknowns,vector(#lowerunknowns)),
          "raw pr E6 matrix specialization dependence");

Uc = [U0,U1,U2,U3,U4,U5,U6,U7,U8,U9];
U = sum(i=1,10,Uc[i]*cubicmonomials[i]);
H3pr = [2*p*r*(aa*p+bb*q+cc*r),U,0]~;
slotspr = concat(cubicslots(H3pr),[aa,bb,cc]);
paramspr = concat([aa,bb,cc],Uc);
tangentpr = matrix(23,13,i,j,deriv(slotspr[i],paramspr[j]));
checktrue(matrank(tangentpr)==13,"raw pr E6 displayed-kernel dimension");
checkzero(A6pr*tangentpr,"raw pr E6 displayed-kernel containment");

\\ Raw E6 for H2_3=(p+q)r.
H2rawsum = [H2first[1],H2first[2],(p+q)*r]~;
wrawsum = matdet(L0+zz*jacmap(H2rawsum)+zz^2*jacmap(H3raw)+zz^3*J4);
E6rawsum = polcoef(wrawsum,6,zz);
eq6sum = nonzerocoefficients(E6rawsum,6);
A6sum = linearmatrix(eq6sum,topunknowns);
checktrue(#eq6sum==14,"raw sum E6 row count");
checktrue(matrank(A6sum)==14,"raw sum E6 rank");
checktrue(matsize(matker(A6sum))[2]==9,"raw sum E6 nullity");
checkzero(constantvector(eq6sum,topunknowns),"raw sum E6 affine remainder");
checkzero(A6sum-substall(A6sum,lowerunknowns,vector(#lowerunknowns)),
          "raw sum E6 matrix specialization dependence");

wc = [w0,w1,w2,w3,w4,w5];
W = sum(i=1,6,wc[i]*quadraticmonomials[i]);
H3sumraw =
  [-p*W+2*p*r*(aa*p+bb*q+cc*r),q*W,0]~;
slotssum = concat(cubicslots(H3sumraw),[aa,bb,cc]);
paramssum = concat([aa,bb,cc],wc);
tangentsum = matrix(23,9,i,j,deriv(slotssum[i],paramssum[j]));
checktrue(matrank(tangentsum)==9,"raw sum E6 displayed-kernel dimension");
checkzero(A6sum*tangentsum,"raw sum E6 displayed-kernel containment");

\\ Raw E5 and full affine solution in the pr orbit.
Lpr = [l00,l01,l02;l10,l11,l12;aa,bb,cc];
wE5pr = matdet(Lpr+zz*jacmap(H2rawpr)+zz^2*jacmap(H3pr)+zz^3*J4);
E5pr = polcoef(wE5pr,5,zz);
eq5pr = nonzerocoefficients(E5pr,5);
A5pr = linearmatrix(eq5pr,lowerunknowns);
checktrue(#eq5pr==4,"raw pr E5 row count");
checktrue(matrank(A5pr)==4,"raw pr E5 rank");
checktrue(matsize(matker(A5pr))[2]==14,"raw pr E5 nullity");
checkzero(A5pr-substall(A5pr,concat([aa,bb,cc],Uc),vector(13)),
          "raw pr E5 matrix specialization dependence");
Vc = [V0,V1,V2,V3,V4,V5];
V = sum(i=1,6,Vc[i]*quadraticmonomials[i]);
H2pr =
  [(aa*p+bb*q)^2+dd*p*r+ee*q*r+cc^2*r^2,V,p*r]~;
checkzero(polcoef(matdet(Lpr+zz*jacmap(H2pr)+zz^2*jacmap(H3pr)+zz^3*J4),
                  5,zz),"raw pr E5 displayed solution");
slot5pr = concat(quadraticslots(H2pr),[l00,l01,l02,l10,l11,l12]);
param5pr = concat([dd,ee],concat(Vc,[l00,l01,l02,l10,l11,l12]));
tangent5pr = matrix(18,14,i,j,deriv(slot5pr[i],param5pr[j]));
checktrue(matrank(tangent5pr)==14,"raw pr E5 displayed-solution dimension");

\\ The pr orbit after E4: no specialization inside K != 0 is suppressed.
H3prK =
  [2*p*r*(aa*p+bb*q+cc*r),q*r*(AK*p+BK*q+CK*r),0]~;
VrawK = sum(i=1,6,Vc[i]*quadraticmonomials[i]);
H2prKraw =
  [(aa*p+bb*q)^2+dd*p*r+(2*bb*cc-KK)*q*r+cc^2*r^2,
   VrawK,p*r]~;
LprK =
  [-AK*KK/2-2*aa^2*cc+aa*dd,
   -BK*KK/2-2*aa*bb*cc+bb*dd,
   -CK*KK/2-2*aa*cc^2+cc*dd;
   mm,nn,omk;
   aa,bb,cc];
wprK =
  matdet(LprK+zz*jacmap(H2prKraw)+zz^2*jacmap(H3prK)+zz^3*J4);
for (degree=4,8,checkzero(polcoef(wprK,degree,zz),
                            "pr K-nonzero unexpected upper identity"));
eq3prK = nonzerocoefficients(polcoef(wprK,3,zz),3);
A3prK = linearmatrix(eq3prK,Vc);
checktrue(#eq3prK==4,"pr K-nonzero E3 row count");
checktrue(matrank(A3prK)==4,"pr K-nonzero E3 rank");
checkzero(A3prK-KK*subst(A3prK,KK,1),
          "pr E3 has specialization beyond K");
H2prK =
  [(aa*p+bb*q)^2+dd*p*r+(2*bb*cc-KK)*q*r+cc^2*r^2,
   (AK*p+BK*q)^2/4+gg*p*r+jj*q*r+CK^2*r^2/4,p*r]~;
wprKsol =
  matdet(LprK+zz*jacmap(H2prK)+zz^2*jacmap(H3prK)+zz^3*J4);
checkzero(polcoef(wprKsol,3,zz),"pr K-nonzero complete E3 solution");
eq2prK = nonzerocoefficients(polcoef(wprKsol,2,zz),2);
A2prK = linearmatrix(eq2prK,[mm,nn,omk]);
checktrue(#eq2prK==3,"pr K-nonzero E2 row count");
checktrue(matrank(A2prK)==3,"pr K-nonzero E2 rank");
checkzero(A2prK-KK*subst(A2prK,KK,1),
          "pr E2 has specialization beyond K");
mmsol=(-AK*BK*CK-2*AK*CK*aa+2*AK*jj+4*aa*gg)/4;
nnsol=(-2*AK*CK*bb-BK^2*CK+2*BK*jj+4*bb*gg)/4;
omksol=(-2*AK*CK*cc-BK*CK^2+2*CK*jj+4*cc*gg)/4;
wprKdeep=substall(wprKsol,[mm,nn,omk],[mmsol,nnsol,omksol]);
LprKdeep=substall(LprK,[mm,nn,omk],[mmsol,nnsol,omksol]);
checkzero(polcoef(wprKdeep,2,zz),"pr K-nonzero E2 solve");
checkzero(polcoef(wprKdeep,1,zz),"pr K-nonzero E1 converse");
checkzero(matdet(LprKdeep),"pr K-nonzero determinant");
LprKzero =
  [aa*(dd-2*aa*cc),bb*(dd-2*aa*cc),cc*(dd-2*aa*cc);
   mm,nn,omk;
   aa,bb,cc];
checkzero(matdet(LprKzero),"pr K-zero proportional rows");

\\ Sum-orbit square forcing and constant rank-six lower solve.
wE5sum =
  matdet(Lpr+zz*jacmap(H2rawsum)+zz^2*jacmap(H3sumraw)+zz^3*J4);
E5sum = polcoef(wE5sum,5,zz);
checkzero(coeff3(E5sum,5,0,0)+3*w0^2,"sum E5 first outer square");
checkzero(coeff3(E5sum,0,5,0)+3*w2^2,"sum E5 second outer square");
checkzero(subst(subst(coeff3(E5sum,3,2,0),w0,0),w2,0)+3*w1^2,
          "sum E5 middle square");
E5sumlinear = substall(E5sum,[w0,w1,w2],[0,0,0]);
eq5sum = nonzerocoefficients(E5sumlinear,5);
A5sum = linearmatrix(eq5sum,lowerunknowns);
checktrue(#eq5sum==6,"raw sum E5 surviving row count");
checktrue(matrank(A5sum)==6,"raw sum E5 rank");
checktrue(matsize(matker(A5sum))[2]==12,"raw sum E5 nullity");
checkzero(A5sum-substall(A5sum,[aa,bb,cc,w3,w4,w5],vector(6)),
          "raw sum E5 matrix specialization dependence");

D0=w3; E0=w4; T0=w5;
al=D0-2*aa; be=E0-2*bb; ga=T0-2*cc;
H3sum =
  [-p*r*(D0*p+E0*q+T0*r)+2*p*r*(aa*p+bb*q+cc*r),
   q*r*(D0*p+E0*q+T0*r),0]~;
H2sum =
  [(al^2/4+XX)*p^2+(al*be/2+YY)*p*q+be^2*q^2/4
    +PP*p*r+QQ*q*r+ga^2*r^2/4,
   D0^2*p^2/4+(D0*E0/2-XX)*p*q+(E0^2/4-YY)*q^2
    +RR*p*r+SS*q*r+T0^2*r^2/4,
   (p+q)*r]~;
wsum = matdet(Lpr+zz*jacmap(H2sum)+zz^2*jacmap(H3sum)+zz^3*J4);
checkzero(polcoef(wsum,5,zz),"sum E5 displayed solution");
slot5sum = concat(quadraticslots(H2sum),[l00,l01,l02,l10,l11,l12]);
param5sum = [XX,YY,PP,QQ,RR,SS,l00,l01,l02,l10,l11,l12];
tangent5sum = matrix(18,12,i,j,deriv(slot5sum[i],param5sum[j]));
checktrue(matrank(tangent5sum)==12,"sum E5 displayed-solution dimension");

\\ The four E4 recurrence coefficients and its exact resonance ideal.
E4sum = polcoef(wsum,4,zz);
checkzero(coeff3(E4sum,3,0,1)-3*D0*XX,"sum E4 recurrence 1");
checkzero(coeff3(E4sum,2,1,1)-3*((al+E0)*XX+D0*YY),
          "sum E4 recurrence 2");
checkzero(coeff3(E4sum,1,2,1)-3*(be*XX+(al+E0)*YY),
          "sum E4 recurrence 3");
checkzero(coeff3(E4sum,0,3,1)-3*be*YY,"sum E4 recurrence 4");
recurrence = [D0,0;al+E0,D0;be,al+E0;0,be];
checkzero(matdet(recurrence[1..2,])-D0^2,"recurrence D square");
checkzero(matdet(recurrence[2..3,])-((al+E0)^2-D0*be),
          "recurrence middle minor");
checkzero(matdet(recurrence[3..4,])-be^2,"recurrence beta square");

\\ Standard X=Y=0 E4 solve and literal M divisibility.
wstd = substall(wsum,[XX,YY],[0,0]);
Lstd = Lpr;
e4 = polcoef(wstd,4,zz);
l10s = solvevar(coeff3(e4,2,0,2),l10);
wstd=subst(wstd,l10,l10s); Lstd=subst(Lstd,l10,l10s);
e4=polcoef(wstd,4,zz); l00s=solvevar(coeff3(e4,1,1,2),l00);
wstd=subst(wstd,l00,l00s); Lstd=subst(Lstd,l00,l00s);
e4=polcoef(wstd,4,zz); l12s=solvevar(coeff3(e4,1,0,3),l12);
wstd=subst(wstd,l12,l12s); Lstd=subst(Lstd,l12,l12s);
e4=polcoef(wstd,4,zz); l01s=solvevar(coeff3(e4,0,2,2),l01);
wstd=subst(wstd,l01,l01s); Lstd=subst(Lstd,l01,l01s);
e4=polcoef(wstd,4,zz); l02s=solvevar(coeff3(e4,0,1,3),l02);
wstd=subst(wstd,l02,l02s); Lstd=subst(Lstd,l02,l02s);
checkzero(polcoef(wstd,4,zz),"standard E4 solve");
Mfac =
  -4*l11+4*aa*be*cc+2*aa*be*ga+2*al*be*cc+al*be*ga
  -8*bb^2*cc-4*bb^2*ga-8*bb*be*cc-4*bb*be*ga+4*bb*SS
  -2*be^2*cc-be^2*ga-2*be*RR+2*be*SS;
E3std=polcoef(wstd,3,zz);
checkzero(coeff3(E3std,2,0,1)-D0*Mfac/2,"standard E3 D factor");
checkzero(coeff3(E3std,1,1,1)-(al+E0)*Mfac/2,
          "standard E3 middle factor");
checkzero(coeff3(E3std,0,2,1)-be*Mfac/2,"standard E3 beta factor");
divstd=divrem(matdet(Lstd),Mfac,l11);
checkzero(divstd[2],"standard determinant literal M divisibility");

\\ Deep resonance D=0, E=2a=2b: squares and division-free Mstar^2.
H3ex =
  [2*aa*p^2*r-ga*p*r^2,
   2*aa*q^2*r+(2*cc+ga)*q*r^2,0]~;
H2ex =
  [(aa^2+XX)*p^2+YY*p*q+PP*p*r+QQ*q*r+ga^2*r^2/4,
   -XX*p*q+(aa^2-YY)*q^2+RR*p*r+SS*q*r
    +(2*cc+ga)^2*r^2/4,(p+q)*r]~;
Lex=[l00,l01,l02;l10,l11,l12;aa,aa,cc];
wex=matdet(Lex+zz*jacmap(H2ex)+zz^2*jacmap(H3ex)+zz^3*J4);
e4=polcoef(wex,4,zz); l10e=solvevar(coeff3(e4,2,0,2),l10);
wex=subst(wex,l10,l10e); Lex=subst(Lex,l10,l10e);
e4=polcoef(wex,4,zz); l00e=solvevar(coeff3(e4,1,1,2),l00);
wex=subst(wex,l00,l00e); Lex=subst(Lex,l00,l00e);
e4=polcoef(wex,4,zz); l12e=solvevar(coeff3(e4,1,0,3),l12);
wex=subst(wex,l12,l12e); Lex=subst(Lex,l12,l12e);
e4=polcoef(wex,4,zz); l01e=solvevar(coeff3(e4,0,2,2),l01);
wex=subst(wex,l01,l01e); Lex=subst(Lex,l01,l01e);
e4=polcoef(wex,4,zz); l02e=solvevar(coeff3(e4,0,1,3),l02);
wex=subst(wex,l02,l02e); Lex=subst(Lex,l02,l02e);
checkzero(polcoef(wex,4,zz),"exceptional E4 solve");
checkzero(coeff3(polcoef(wex,3,zz),3,0,0)+2*XX^2,
          "exceptional X square");
checkzero(coeff3(polcoef(wex,3,zz),0,3,0)+2*YY^2,
          "exceptional Y square");
wdeep=substall(wex,[XX,YY],[0,0]);
Ldeep=substall(Lex,[XX,YY],[0,0]);
Mstar=l11+2*aa^2*cc+aa^2*ga-aa*SS;
Astar=4*aa*cc+2*aa*ga+RR-SS;
coefE2=coeff3(polcoef(wdeep,2,zz),1,0,1);
coefE1=coeff3(polcoef(wdeep,1,zz),1,0,0);
checkzero(coefE2-Mstar*Astar,"exceptional E2 factor");
checkzero(coefE1-Mstar*(aa*Astar-Mstar),"exceptional E1 factor");
checkzero(aa*coefE2-coefE1-Mstar^2,
          "exceptional division-free Mstar square");
divex=divrem(matdet(Ldeep),Mstar,l11);
checkzero(divex[2],"exceptional determinant literal Mstar divisibility");

print("AUDIT_FIXED_QUADRATIC_LINE_PARI_PASS_41D8C2");
}
quit;
