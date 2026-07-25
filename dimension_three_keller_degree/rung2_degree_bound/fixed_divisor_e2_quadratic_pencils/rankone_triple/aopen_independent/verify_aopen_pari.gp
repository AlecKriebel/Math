\\ Independent PARI/GP certificate for the A != 0 branch of the
\\ rank-one fixed-divisor e=2 triple-companion obstruction.

die(msg) = { print(Str("FAIL: ", msg)); quit(1); };
check(flag,msg) = { if(!flag,die(msg)); };
checkeq(got,want,msg) =
{
  if(got!=want,die(Str(msg, ": got ",got,", want ",want)));
};

xyz=[x,y,z];

homexps(n) =
{
  my(out=List());
  forstep(i=n,0,-1,
    forstep(j=n-i,0,-1,listput(out,[i,j,n-i-j]))
  );
  Vec(out);
};

monoms(n) =
{
  my(E=homexps(n));
  vector(#E,i,x^E[i][1]*y^E[i][2]*z^E[i][3]);
};

coeffxyz(f,e) =
{
  polcoeff(polcoeff(polcoeff(f,e[1],x),e[2],y),e[3],z);
};

hcoeffs(f,n) =
{
  my(E=homexps(n));
  vector(#E,i,coeffxyz(f,E[i]));
};

jacvec(hh) = matrix(3,3,i,j,deriv(hh[i],xyz[j]));

zero_vars(f,vv) =
{
  my(g=f);
  for(i=1,#vv,g=subst(g,vv[i],0));
  g;
};

subst_many(f,vv,ww) =
{
  my(g=f);
  check(#vv==#ww,"subst_many length mismatch");
  for(i=1,#vv,g=subst(g,vv[i],ww[i]));
  g;
};

linear_system(f,n,vv) =
{
  my(cc=hcoeffs(f,n));
  my(M=matrix(#cc,#vv,i,j,deriv(cc[i],vv[j])));
  my(rhs=vector(#cc,i,-zero_vars(cc[i],vv))~);
  [M,rhs];
};

vector_complement(n,indices) =
{
  my(L=List(),S=Set(indices));
  for(i=1,n,if(!setsearch(S,i),listput(L,i)));
  Vec(L);
};

pivot_solution(M,rhs,unknowns,rows,pivots) =
{
  my(free=vector_complement(#unknowns,pivots));
  my(square=vecextract(M,rows,pivots));
  my(freepart=if(#free,
    vecextract(M,rows,free)*vector(#free,i,unknowns[free[i]])~,
    vector(#rows)~));
  my(pivotvalues=matsolve(square,vecextract(rhs,rows)-freepart));
  my(sol=unknowns~);
  for(i=1,#pivots,sol[pivots[i]]=pivotvalues[i]);
  [sol,pivots,free,M*sol-rhs];
};

cleared_left_data(M,rhs) =
{
  my(N=matker(M~),pairs=List(),vectors=List());
  for(j=1,matsize(N)[2],
    my(den=1,v,pair);
    for(i=1,matsize(N)[1],den*=denominator(N[i,j]));
    v=den*N[,j];
    checkeq(M~*v,vector(matsize(M)[2])~,
      Str("cleared left vector ",j," is not a syzygy"));
    pair=v~*rhs;
    listput(vectors,v);
    listput(pairs,pair);
  );
  [Vec(vectors),Vec(pairs)];
};

lookup_solution(vv,ww,target) =
{
  for(i=1,#vv,if(vv[i]==target,return(ww[i])));
  die(Str("solution lookup failed for ",target));
};

is_rational_constant(v) =
{
  type(v)=="t_INT" || type(v)=="t_FRAC";
};

associate(a,b) =
{
  if(a==0 || b==0,return(a==0 && b==0));
  my(ratio=simplify(a/b));
  is_rational_constant(ratio) && a==ratio*b;
};

find_associate(vv,target) =
{
  for(i=1,#vv,if(associate(vv[i],target),return(1)));
  0;
};

m2=monoms(2);
aall=[a0,a1,a2,a3,a4,a5];
ball=[b0,b1,b2,b3,b4,b5];
ell=[l0,l1,l2,l3,l4,l5,l6,l7,l8];
alllower=concat(concat(aall,ball),ell);
Lmat=matrix(3,3,i,j,ell[3*(i-1)+j]);

P=x^4;
q=y^2+x*z;
Q=x^2*q;
R=x^3;

weighted_determinant(U,V,W) =
{
  my(H2=[sum(i=1,6,aall[i]*m2[i]),
         sum(i=1,6,ball[i]*m2[i]),W]);
  matdet(Lmat+t*jacvec(H2)+t^2*jacvec([U,V,R])
              +t^3*jacvec([P,Q,0]));
};

solve_E6(weighted,label) =
{
  my(sys=linear_system(polcoeff(weighted,6,t),6,alllower));
  my(M=sys[1],rhs=sys[2],idx=matindexrank(M));
  checkeq(matrank(M),4,Str(label,": E6 rank"));
  my(sol=pivot_solution(M,rhs,alllower,idx[1],idx[2]));
  checkeq(sol[4],vector(matsize(M)[1])~,Str(label,": E6 residual"));
  sol;
};

E5_data(weighted,label) =
{
  my(sol6=solve_E6(weighted,label));
  my(value=subst_many(polcoeff(weighted,5,t),alllower,sol6[1]));
  my(free=vector(#sol6[3],i,alllower[sol6[3][i]]));
  my(sys=linear_system(value,5,free));
  my(left=cleared_left_data(sys[1],sys[2]));
  [sol6,free,sys[1],sys[2],left[2]];
};

solve_E65(weighted,label) =
{
  my(data=E5_data(weighted,label));
  my(sol6=data[1],free=data[2],M=data[3],rhs=data[4]);
  my(idx=matindexrank(M));
  my(sol5=pivot_solution(M,rhs,free,idx[1],idx[2]));
  checkeq(sol5[4],vector(matsize(M)[1])~,
    Str(label,": E5 residual"));
  my(full=vector(#alllower,i,
    subst_many(sol6[1][i],free,sol5[1])));
  checkeq(subst_many(polcoeff(weighted,6,t),alllower,full),0,
    Str(label,": composed E6"));
  checkeq(subst_many(polcoeff(weighted,5,t),alllower,full),0,
    Str(label,": composed E5"));
  [full,sol6,sol5];
};

normal_W=w1*x*y+w2*x*z+w3*y^2;
normal_U=x*q+4/3*x*normal_W;
normal_V=C0*x^2*z+C1*x*y^2+C2*x*y*z+C3*x*z^2 \
  +w1*(3-4*w3)/9*y^3 \
  +(w2-w3)*(3-4*w3)/9*y^2*z;
normal_weighted=weighted_determinant(normal_U,normal_V,normal_W);

print("PARI audit A-open: scalar normalization and four-factor cover");

\\ If the original coefficient is A != 0, precompose by X -> A X and
\\ postcompose by diag(A^-4,A^-4,A^-3).  The quartic pair and x^3 are
\\ fixed, while every cubic coefficient in U,V and every quadratic
\\ coefficient in W is divided by A.
checkeq(A^-4*subst(x^4,x,A*x),x^4,"normalization fixes P");
checkeq(A^-4*subst(subst(subst(x^2*(y^2+x*z),x,A*x),y,A*y),z,A*z), \
  Q,"normalization fixes Q");
checkeq(A^-3*subst(x^3,x,A*x),x^3,"normalization fixes R");
checkeq(A^-4*subst(subst(subst(A*x*q,x,A*x),y,A*y),z,A*z), \
  x*q,"normalization sends A xq to xq");

for(k=7,9,checkeq(polcoeff(normal_weighted,k,t),0, \
  Str("normal E",k)));
normal6=solve_E6(normal_weighted,"normal");
normal5=subst_many(polcoeff(normal_weighted,5,t),alllower,normal6[1]);
checkeq(coeffxyz(normal5,[0,5,0]), \
  2*w3*(w2-w3)*(4*w3-3)*(4*w3+3)/27, \
  "four-factor y^5 coefficient");

print("PASS normalization and exact four-factor branch cover");

print("PARI audit A-open: w3=0 branch, including every W=0 rank drop");

zero_W=w1*x*y+w2*x*z;
zero_U=x*q+4/3*x*zero_W;
zero_V=C0*x^2*z+C1*x*y^2+C2*x*y*z+C3*x*z^2 \
  +w1/3*y^3+w2/3*y^2*z;
zero_weighted=weighted_determinant(zero_U,zero_V,zero_W);
zero5=E5_data(zero_weighted,"w3=0");
check(find_associate(zero5[5],w2^2), \
  "w3=0 compatibility missing w2^2");

zeroaxis_weighted=subst(zero_weighted,w2,0);
zeroaxis5=E5_data(zeroaxis_weighted,"w3=w2=0");
check(find_associate(zeroaxis5[5],w1*C3), \
  "w3=w2=0 compatibility missing w1*C3");

\\ On W=0, use a constant-pivot E6 solution and inspect the raw E5
\\ coefficients before any C_i localization.
W0_weighted=subst(zeroaxis_weighted,w1,0);
W0sol6=solve_E6(W0_weighted,"W=0");
W0E5=subst_many(polcoeff(W0_weighted,5,t),alllower,W0sol6[1]);
checkeq(coeffxyz(W0E5,[2,3,0]),-2*l8, \
  "W=0 literal l8 equation");
W0X=3*C1*C2-3*C2*a3-3*b4;
checkeq(coeffxyz(W0E5,[4,0,1]),W0X+l7, \
  "W=0 first l7 equation");
checkeq(coeffxyz(W0E5,[3,2,0]),-2*W0X+l7, \
  "W=0 second l7 equation");

\\ These equations give l7=l8=0.  The third coordinate is then
\\ x^3+l6*x+constant, so the whole determinant has a nonunit factor.
F1=P+zero_vars(normal_U,[w1,w2,w3]) \
  +sum(i=1,6,aall[i]*m2[i])+l0*x+l1*y+l2*z;
F2=Q+(C0*x^2*z+C1*x*y^2+C2*x*y*z+C3*x*z^2) \
  +sum(i=1,6,ball[i]*m2[i])+l3*x+l4*y+l5*z;
F3=R+l6*x;
W0det=matdet(jacvec([F1,F2,F3]));
W0minor=deriv(F1,y)*deriv(F2,z)-deriv(F1,z)*deriv(F2,y);
checkeq(W0det,(3*x^2+l6)*W0minor, \
  "W=0 determinant factorization");

\\ The remaining chart has w1 != 0 and C3=0.  Recompute there; no
\\ equation obtained by dividing by C3 is used.
zeroopen_weighted=subst(subst(zeroaxis_weighted,C3,0),w1,ww);
zeroopen65=solve_E65(zeroopen_weighted,"w3=w2=C3=0, w1-open");
zeroopenE4=subst_many(polcoeff(zeroopen_weighted,4,t), \
  alllower,zeroopen65[1]);
checkeq(coeffxyz(zeroopenE4,[0,4,0]),ww^2*(-6*C2+ww)/3, \
  "w1-open E4 y4");
checkeq(coeffxyz(zeroopenE4,[2,0,2]), \
  -ww*(-3*C2+2*ww)*(-C2+ww)/3, \
  "w1-open E4 x2z2");
checkeq(subst(coeffxyz(zeroopenE4,[2,0,2]),C2,ww/6), \
  -5*ww^3/12,"w1-open residual after C2=w1/6");

print("PASS w3=0: W=0 factors the determinant; W!=0 has a literal E4 contradiction");

print("PARI audit A-open: equal-factor branch away from the two resonances");

diag_W=ww*x*y+ss*q;
diag_U=x*q+4/3*x*diag_W;
diag_V=C0*x^2*z+C1*x*y^2+C2*x*y*z+C3*x*z^2 \
  +ww*(3-4*ss)/9*y^3;
diag_weighted=weighted_determinant(diag_U,diag_V,diag_W);
diag5=E5_data(diag_weighted,"w2=w3");
check(find_associate(diag5[5],C3*ss*(4*ss-3)), \
  "equal branch missing C3 condition");
check(find_associate(diag5[5], \
  ss*(4*ss-3)*(6*C2+4*ss*ww-ww)), \
  "equal branch missing C2 condition");
diag_reduced_pairs=vector(#diag5[5],i, \
  subst(subst(diag5[5][i],C3,0),C2,ww*(1-4*ss)/6));
check(find_associate(diag_reduced_pairs, \
  ss*ww*(4*ss-3)*(4*ss+3)), \
  "equal branch missing final resonance factor");

\\ The nonresonant remaining leaf has ww=0, C2=C3=0.
diag0_weighted=subst_many(diag_weighted,[ww,C2,C3],[0,0,0]);

\\ D=C0-C1 != 0.
diagD_weighted=subst_many(diag0_weighted,[C0,C1],[CC+DD,CC]);
diagD65=solve_E65(diagD_weighted,"equal nonresonant D-open");
checkeq(lookup_solution(alllower,diagD65[1],l7),0, \
  "equal D-open l7");
checkeq(lookup_solution(alllower,diagD65[1],l8),ss*DD, \
  "equal D-open l8");
diagDE4=subst_many(polcoeff(diagD_weighted,4,t), \
  alllower,diagD65[1]);
checkeq(coeffxyz(diagDE4,[3,0,1]),l1*ss*(4*ss-3)/3, \
  "equal D-open forces l1");
diagDE4_l1=subst(diagDE4,l1,0);
checkeq(coeffxyz(diagDE4_l1,[4,0,0]),-3*l4, \
  "equal D-open then forces l4");
checkeq(subst_many(matdet(Lmat),[l1,l4,l7],[0,0,0]),0, \
  "equal D-open singular L");

\\ D=0 is a fresh E5 rank drop.
diagEq_weighted=subst_many(diag0_weighted,[C0,C1],[CC,CC]);
diagEq65=solve_E65(diagEq_weighted,"equal nonresonant D=0");
checkeq(lookup_solution(alllower,diagEq65[1],l7),0, \
  "equal D=0 l7");
checkeq(lookup_solution(alllower,diagEq65[1],l8),0, \
  "equal D=0 l8");
diagEqE4=subst_many(polcoeff(diagEq_weighted,4,t), \
  alllower,diagEq65[1]);
checkeq(coeffxyz(diagEqE4,[3,0,1]),l1*ss*(4*ss-3)/3, \
  "equal D=0 forces l1");
checkeq(coeffxyz(diagEqE4,[2,1,1]),-2*l2*ss*(4*ss-3)/3, \
  "equal D=0 forces l2");
checkeq(subst_many(matdet(Lmat),[l1,l2,l7,l8],[0,0,0,0]),0, \
  "equal D=0 singular L");

print("PASS equal branch: only plus/minus resonances survive; every other leaf has det L=0");

print("PARI audit A-open: plus resonance, including aligned rank drops");

plus_W=w1*x*y+w2*x*z+3/4*y^2;
plus_U=x*q+4/3*x*plus_W;
plus_V=C0*x^2*z+C1*x*y^2+C2*x*y*z+C3*x*z^2;
plus_weighted=weighted_determinant(plus_U,plus_V,plus_W);
plus5=E5_data(plus_weighted,"plus");
check(find_associate(plus5[5],(4*w2-3)^2), \
  "plus branch missing w2=3/4 square");

plusdiag_weighted=subst(plus_weighted,w2,3/4);
plusdiag5=E5_data(plusdiag_weighted,"plus diagonal");
check(find_associate(plusdiag5[5],w1*C3), \
  "plus diagonal missing w1*C3");
check(find_associate(plusdiag5[5],w1*(3*C2+w1)), \
  "plus diagonal missing w1*(3C2+w1)");

\\ w1 != 0.
plusopen_weighted=subst_many(plusdiag_weighted, \
  [w1,C2,C3],[ww,-ww/3,0]);
plusopen65=solve_E65(plusopen_weighted,"plus w1-open");
plusopenE4=subst_many(polcoeff(plusopen_weighted,4,t), \
  alllower,plusopen65[1]);
checkeq(coeffxyz(plusopenE4,[0,3,1]),-ww^2/2, \
  "plus w1-open literal E4 contradiction");

\\ w1=0.  First C3 != 0, then the fresh C3=0,C2 != 0 rank drop.
plus0_weighted=subst(plusdiag_weighted,w1,0);
plusC3_weighted=subst(plus0_weighted,C3,GG);
plusC365=solve_E65(plusC3_weighted,"plus C3-open");
plusC3E4=subst_many(polcoeff(plusC3_weighted,4,t), \
  alllower,plusC365[1]);
checkeq(coeffxyz(plusC3E4,[0,1,3]),3*GG^2, \
  "plus C3-open literal E4 contradiction");

plusC2_weighted=subst_many(plus0_weighted,[C3,C2],[0,HH]);
plusC265=solve_E65(plusC2_weighted,"plus C3=0,C2-open");
plusC2E4=subst_many(polcoeff(plusC2_weighted,4,t), \
  alllower,plusC265[1]);
checkeq(coeffxyz(plusC2E4,[0,3,1]),3*HH^2/2, \
  "plus C2-open literal E4 contradiction");

\\ The aligned D != 0 chart: V=(CC+DD)x^2z+CC*xy^2.
plusAlignD_weighted=subst_many(plus0_weighted, \
  [C0,C1,C2,C3],[CC+DD,CC,0,0]);
plusAlignDvars=[a1,a2,a3,a4,a5,b1,b2,b4,b5,l7,l8];
plusAlignDvals=[4*TT/3,CC+DD-KK/DD+4*RR/3,CC-KK/DD,0,0, \
  l1,b3+l2+KK,0,0,TT,RR];
for(k=5,6,checkeq(subst_many(polcoeff(plusAlignD_weighted,k,t), \
  plusAlignDvars,plusAlignDvals),0,Str("plus aligned D-open E",k)));
plusAlignDE4=subst_many(polcoeff(plusAlignD_weighted,4,t), \
  plusAlignDvars,plusAlignDvals);
plusF=-3*CC*DD-3*DD^2+4*DD*RR+6*KK;
plusG=-3*CC*DD+6*DD^2-8*DD*RR+6*KK;
plusH=-CC*DD+2*KK;
checkeq(coeffxyz(plusAlignDE4,[3,0,1]),-TT*plusF/(3*DD), \
  "plus aligned D-open tF");
checkeq(coeffxyz(plusAlignDE4,[2,2,0]),-TT*plusG/(3*DD), \
  "plus aligned D-open tG");
checkeq(coeffxyz(plusAlignDE4,[2,1,1]), \
  -(3*DD-4*RR)*plusF/(6*DD), \
  "plus aligned D-open resonance F");
checkeq(coeffxyz(plusAlignDE4,[1,3,0]), \
  -(3*DD-4*RR)*plusH/(2*DD), \
  "plus aligned D-open resonance H");
checkeq(plusF-plusG,3*DD*(4*RR-3*DD), \
  "plus aligned F-G identity");

\\ The displayed four equations force RR=3DD/4.  Solve the remaining
\\ two E4 coefficients without any further localization.
plusL4=TT*(-6*a0+4*l6)/9+KK*l1/DD;
plusL5=DD*b3-CC*KK+KK^2/DD+KK*l2/DD+2*TT^2/9;
plusAfterE4vars=concat(plusAlignDvars,[l4,l5]);
plusAfterE4vals=concat(plusAlignDvals, \
  [plusL4,plusL5]);
plusAfterE4vals=subst_many(plusAfterE4vals,[RR],[3*DD/4]);
plusAfterE4=subst_many(polcoeff(plusAlignD_weighted,4,t), \
  plusAfterE4vars,plusAfterE4vals);
checkeq(coeffxyz(plusAfterE4,[3,0,1]),-TT*plusH/DD, \
  "plus aligned remaining tH");
checkeq(coeffxyz(plusAfterE4,[2,2,0]),-TT*plusH/DD, \
  "plus aligned duplicate tH");

\\ TT != 0 forces KK=CC*DD/2, and E3 is immediately inconsistent.
plusTopenE3=subst_many(polcoeff(plusAlignD_weighted,3,t), \
  plusAfterE4vars, \
  subst_many(plusAfterE4vals,[KK],[CC*DD/2]));
checkeq(coeffxyz(plusTopenE3,[1,1,1]),-2*TT^2/3, \
  "plus aligned TT-open E3 contradiction");

\\ TT=0: det L already has the factor l1.  If l1 != 0, E3 forces
\\ KK=CC*DD/2; the next identities force l2=KK and then -3*l1^2/4.
plusT0vals=subst_many(plusAfterE4vals,[TT],[0]);
plusT0det=subst_many(matdet(Lmat),plusAfterE4vars,plusT0vals);
checkeq(subst(plusT0det,l1,0),0, \
  "plus aligned TT=0,l1=0 singular L");
plusT0E3=subst_many(polcoeff(plusAlignD_weighted,3,t), \
  plusAfterE4vars,plusT0vals);
checkeq(coeffxyz(plusT0E3,[2,0,1]),3*l1*plusH/(4*DD), \
  "plus aligned TT=0 E3 forces H");
plusA0=CC^2/2-2*b3+2*l6/3;
plusT0lowerVars=concat(plusAfterE4vars,[KK,a0,l2]);
plusT0lowerVals=concat(plusT0vals,[CC*DD/2,plusA0,CC*DD/2]);
plusT0E2=subst_many(polcoeff(plusAlignD_weighted,2,t), \
  plusT0lowerVars,plusT0lowerVals);
checkeq(coeffxyz(plusT0E2,[1,1,0]),-3*l1^2/4, \
  "plus aligned TT=0,l1-open E2 contradiction");

\\ The aligned D=0 chart is recomputed from scratch.
plusAlignEq_weighted=subst_many(plus0_weighted, \
  [C0,C1,C2,C3],[CC,CC,0,0]);
plusEqVars=[a1,a2,a3,a4,a5,b1,b2,b4,b5,l7,l8];
plusEqVals=[4*TT/3,a3+4*RR/3,a3,0,0,l1,b3+l2,0,0,TT,RR];
for(k=5,6,checkeq(subst_many(polcoeff(plusAlignEq_weighted,k,t), \
  plusEqVars,plusEqVals),0,Str("plus aligned D=0 E",k)));
plusEqE4=subst_many(polcoeff(plusAlignEq_weighted,4,t), \
  plusEqVars,plusEqVals);
plusAlpha=CC-2*a3;
checkeq(coeffxyz(plusEqE4,[3,0,1]),-TT*(3*plusAlpha+4*RR)/3, \
  "plus aligned D=0 first t equation");
checkeq(coeffxyz(plusEqE4,[2,2,0]),-TT*(3*plusAlpha-8*RR)/3, \
  "plus aligned D=0 second t equation");
checkeq(coeffxyz(plusEqE4,[2,1,1]),2*RR*(3*plusAlpha+4*RR)/3, \
  "plus aligned D=0 r equation");
checkeq(coeffxyz(plusEqE4,[1,3,0]),2*RR*plusAlpha, \
  "plus aligned D=0 r-alpha equation");

\\ Hence RR=0.  TT=0 makes the last two columns proportional;
\\ TT!=0 forces a3=CC/2 and then E3 contains -2*TT^2/3.
plusEqL4=(CC-a3)*l1+TT*(-6*a0+4*l6)/9;
plusEqL5=(CC-a3)*l2+2*TT^2/9;
plusEqAfterVars=concat(plusEqVars,[l4,l5]);
plusEqAfterVals=concat(plusEqVals,[plusEqL4,plusEqL5]);
plusEqAfterVals=subst_many(plusEqAfterVals,[RR],[0]);
checkeq(subst_many(matdet(Lmat), \
  concat(plusEqAfterVars,[TT]),concat(plusEqAfterVals,[0])),0, \
  "plus aligned D=0,TT=0 singular L");
plusEqTopenE3=subst_many(polcoeff(plusAlignEq_weighted,3,t), \
  concat(plusEqAfterVars,[a3]), \
  concat(plusEqAfterVals,[CC/2]));
checkeq(coeffxyz(plusEqTopenE3,[1,1,1]),-2*TT^2/3, \
  "plus aligned D=0,TT-open E3 contradiction");

print("PASS plus resonance: all open and aligned rank-drop charts close");

print("PARI audit A-open: minus resonance and its equal-factor intersection");

minus_W=w1*x*y+w2*x*z-3/4*y^2;
minus_U=x*q+4/3*x*minus_W;
minus_V=C0*x^2*z+C1*x*y^2+C2*x*y*z+C3*x*z^2 \
  +2*w1/3*y^3+(2*w2/3+1/2)*y^2*z;
minus_weighted=weighted_determinant(minus_U,minus_V,minus_W);
minus5=E5_data(minus_weighted,"minus");
minusC2eq=-9*C2+4*w1*w2+9*w1;
minusC3eq=-72*C3+16*w2^2+72*w2+45;
check(find_associate(minus5[5],minusC2eq), \
  "minus branch missing C2 equation");
check(find_associate(minus5[5],minusC3eq), \
  "minus branch missing C3 equation");
minus_reduced_pairs=vector(#minus5[5],i, \
  subst_many(minus5[5][i],[C2,C3], \
    [w1*(4*w2+9)/9,(16*w2^2+72*w2+45)/72]));
check(find_associate(minus_reduced_pairs,(4*w2+3)^3), \
  "minus branch missing cubic equal-factor equation");

\\ Thus w2=-3/4, C2=2w1/3, C3=0.
minusdiag_weighted=subst_many(minus_weighted, \
  [w2,C2,C3],[-3/4,2*w1/3,0]);

\\ w1 != 0, first D != 0 and then the fresh D=0 chart.
minusOpenD_weighted=subst_many(minusdiag_weighted, \
  [w1,C0,C1],[ww,CC+DD,CC]);
minusOpenD65=solve_E65(minusOpenD_weighted,"minus w1-open,D-open");
minusOpenDE4=subst_many(polcoeff(minusOpenD_weighted,4,t), \
  alllower,minusOpenD65[1]);
checkeq(coeffxyz(minusOpenDE4,[2,1,1]) \
  -coeffxyz(minusOpenDE4,[1,3,0]),10*ww^4/81, \
  "minus w1-open,D-open E4 contradiction");

minusOpenEq_weighted=subst_many(minusdiag_weighted, \
  [w1,C0,C1],[ww,CC,CC]);
minusOpenEq65=solve_E65(minusOpenEq_weighted,"minus w1-open,D=0");
minusOpenEqE4=subst_many(polcoeff(minusOpenEq_weighted,4,t), \
  alllower,minusOpenEq65[1]);
checkeq(coeffxyz(minusOpenEqE4,[2,1,1]) \
  -coeffxyz(minusOpenEqE4,[1,3,0]),10*ww^4/81, \
  "minus w1-open,D=0 E4 contradiction");

\\ w1=0, D != 0.
minus0_weighted=subst(minusdiag_weighted,w1,0);
minus0D_weighted=subst_many(minus0_weighted,[C0,C1],[CC+DD,CC]);
minus0D65=solve_E65(minus0D_weighted,"minus w1=0,D-open");
checkeq(lookup_solution(alllower,minus0D65[1],l7),0, \
  "minus w1=0,D-open l7");
checkeq(lookup_solution(alllower,minus0D65[1],l8),-3*DD/4, \
  "minus w1=0,D-open l8");
minus0DE4=subst_many(polcoeff(minus0D_weighted,4,t), \
  alllower,minus0D65[1]);
checkeq(coeffxyz(minus0DE4,[3,0,1]),3*l1/2, \
  "minus w1=0,D-open forces l1");
checkeq(coeffxyz(subst(minus0DE4,l1,0),[4,0,0]),-3*l4, \
  "minus w1=0,D-open then forces l4");
checkeq(subst_many(matdet(Lmat),[l1,l4,l7],[0,0,0]),0, \
  "minus w1=0,D-open singular L");

\\ w1=0, D=0, recomputed without a D pivot.
minus0Eq_weighted=subst_many(minus0_weighted,[C0,C1],[CC,CC]);
minus0Eq65=solve_E65(minus0Eq_weighted,"minus w1=0,D=0");
checkeq(lookup_solution(alllower,minus0Eq65[1],l7),0, \
  "minus w1=0,D=0 l7");
checkeq(lookup_solution(alllower,minus0Eq65[1],l8),0, \
  "minus w1=0,D=0 l8");
minus0EqE4=subst_many(polcoeff(minus0Eq_weighted,4,t), \
  alllower,minus0Eq65[1]);
checkeq(coeffxyz(minus0EqE4,[3,0,1]),3*l1/2, \
  "minus w1=0,D=0 forces l1");
checkeq(coeffxyz(minus0EqE4,[2,1,1]),-3*l2, \
  "minus w1=0,D=0 forces l2");
checkeq(subst_many(matdet(Lmat),[l1,l2,l7,l8],[0,0,0,0]),0, \
  "minus w1=0,D=0 singular L");

print("PASS minus resonance: cubic compatibility reaches the equal factor, and every rank drop closes");
print("PASS all A!=0 branches excluded exactly in PARI/GP");
