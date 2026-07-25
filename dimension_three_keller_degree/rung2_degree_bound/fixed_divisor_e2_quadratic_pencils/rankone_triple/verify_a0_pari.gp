\\ Independent PARI/GP certificate for the A = 0 branch of the
\\ rank-one fixed-divisor e=2 triple-companion obstruction.
\\
\\ This script rebuilds every weighted Jacobian determinant in PARI.
\\ It deliberately orders coefficient equations oppositely from the
\\ primary SymPy verifier and recomputes every rank-drop specialization.

die(msg) = { print(Str("FAIL: ",msg)); quit(1); };
check(flag,msg) = { if(!(flag),die(msg)); };
checkeq(got,want,msg) =
{
  if(got!=want,die(Str(msg,": got ",got,", want ",want)));
};

xyz=[x,y,z];

\\ Ascending order is intentionally opposite to the primary verifier.
eqexps(n) =
{
  my(out=List());
  for(i=0,n,
    for(j=0,n-i,listput(out,[i,j,n-i-j]))
  );
  Vec(out);
};

coeffxyz(f,e) =
{
  polcoeff(polcoeff(polcoeff(f,e[1],x),e[2],y),e[3],z);
};

hcoeffs(f,n) =
{
  my(E=eqexps(n));
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
  my(out=List(),S=Set(indices));
  for(i=1,n,if(!setsearch(S,i),listput(out,i)));
  Vec(out);
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

lookup_solution(vv,ww,target) =
{
  for(i=1,#vv,if(vv[i]==target,return(ww[i])));
  die(Str("solution lookup failed for ",target));
};

\\ Lower terms use the same coefficient names as the paper:
\\ H2_1=a0*x^2+a1*xy+a2*xz+a3*y^2+a4*yz+a5*z^2,
\\ and similarly for H2_2.  L is row-major l0,...,l8.
m2=[x^2,x*y,x*z,y^2,y*z,z^2];
aall=[a0,a1,a2,a3,a4,a5];
ball=[b0,b1,b2,b3,b4,b5];
ell=[l0,l1,l2,l3,l4,l5,l6,l7,l8];
alllower=concat(concat(aall,ball),ell);
lower_no_a3=[a0,a1,a2,a4,a5,b0,b1,b2,b3,b4,b5, \
  l0,l1,l2,l3,l4,l5,l6,l7,l8];
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

augmented_minor_data(M,rhs) =
{
  my(A=concat(M,rhs),idx=matindexrank(A));
  [matrank(M),matrank(A),
   matdet(vecextract(A,idx[1],idx[2])),idx];
};

compatibility_minor_data(M,rhs) =
{
  my(idx=matindexrank(M),r=#idx[1]);
  my(pivot=matdet(vecextract(M,idx[1],idx[2])));
  my(extra=vector_complement(matsize(M)[1],idx[1]));
  my(A=concat(M,rhs),cols=concat(Vec(idx[2]),[matsize(A)[2]]));
  my(minors=vector(#extra,i,
    matdet(vecextract(A,concat(Vec(idx[1]),[extra[i]]),cols))));
  [r,pivot,extra,minors];
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

solve_E654_fixed_a3(weighted,a3value,label) =
{
  my(base=subst(weighted,a3,a3value),lower=lower_no_a3);
  my(sys6=linear_system(polcoeff(base,6,t),6,lower));
  my(idx6=matindexrank(sys6[1]));
  checkeq(matrank(sys6[1]),4,Str(label,": E6 rank"));
  my(sol6=pivot_solution(sys6[1],sys6[2],lower,idx6[1],idx6[2]));
  checkeq(sol6[4],vector(matsize(sys6[1])[1])~,
    Str(label,": E6 residual"));
  my(free6=vector(#sol6[3],i,lower[sol6[3][i]]));

  my(E5=subst_many(polcoeff(base,5,t),lower,sol6[1]));
  my(sys5=linear_system(E5,5,free6),idx5=matindexrank(sys5[1]));
  checkeq(matrank(sys5[1]),4,Str(label,": E5 rank"));
  my(sol5=pivot_solution(sys5[1],sys5[2],free6,idx5[1],idx5[2]));
  checkeq(sol5[4],vector(matsize(sys5[1])[1])~,
    Str(label,": E5 residual"));
  my(full65=vector(#lower,i,subst_many(sol6[1][i],free6,sol5[1])));
  my(free5=vector(#sol5[3],i,free6[sol5[3][i]]));

  my(E4=subst_many(polcoeff(base,4,t),lower,full65));
  my(active4list=List());
  for(i=1,#free5,if(deriv(E4,free5[i])!=0,
    listput(active4list,free5[i])));
  my(active4=Vec(active4list));
  my(sys4=linear_system(E4,4,active4),idx4=matindexrank(sys4[1]));
  checkeq(matrank(sys4[1]),4,Str(label,": E4 rank"));
  my(sol4=pivot_solution(sys4[1],sys4[2],active4,idx4[1],idx4[2]));
  checkeq(sol4[4],vector(matsize(sys4[1])[1])~,
    Str(label,": E4 residual"));
  my(full654=vector(#lower,i,
    subst_many(full65[i],active4,sol4[1])));
  for(k=4,6,
    checkeq(subst_many(polcoeff(base,k,t),lower,full654),0,
      Str(label,": composed E",k)));
  [base,lower,full654,sys4[1],idx4,active4,sol4];
};

{
fullV=C0*x^2*z+C1*x*y^2+C2*x*y*z+C3*x*z^2 \
  +C4*y^3+C5*y^2*z+C6*y*z^2+C7*z^3;

print("PARI audit A=0: w3-open branch");

w3U=4/3*s*x*q;
w3W=s*q;
w3weighted=weighted_determinant(w3U,fullV,w3W);
w3data=E5_data(w3weighted,"A=0,w3-open");
w3RawAug=augmented_minor_data(w3data[3],w3data[4]);
checkeq([w3RawAug[1],w3RawAug[2]],[5,6],
  "w3-open raw augmented ranks");
check(associate(w3RawAug[3],s^4*C7^2),
  "w3-open raw augmented minor");

w3C7zero=subst(w3weighted,C7,0);
w3C7zero5=E5_data(w3C7zero,"A=0,w3-open,C7=0");
w3C7Aug=augmented_minor_data(w3C7zero5[3],w3C7zero5[4]);
checkeq([w3C7Aug[1],w3C7Aug[2]],[5,6],
  "w3-open C7=0 augmented ranks");
check(associate(w3C7Aug[3],s^4*C6^2),
  "w3-open C7=0 augmented minor");

w3C76zero=subst(w3C7zero,C6,0);
w3C76zero5=E5_data(w3C76zero,"A=0,w3-open,C7=C6=0");
w3Delta=C3-C5;
w3DeltaData=compatibility_minor_data(w3C76zero5[3],w3C76zero5[4]);
checkeq(w3DeltaData[1],5,"w3-open delta chart E5 rank");
check(associate(w3DeltaData[2],s^2*w3Delta),
  "w3-open delta chart pivot");
check(find_associate(w3DeltaData[4],s^4*C5*w3Delta),
  "w3-open delta chart C5 minor");
check(find_associate(w3DeltaData[4],s^4*C3*w3Delta),
  "w3-open delta chart C3 minor");
\\ Hence delta != 0 would force C5=C3=0, contradicting delta != 0.

w3C3eqC5=subst(w3C76zero,C3,C5);
w3C3eqC55=E5_data(w3C3eqC5,
  "A=0,w3-open,C7=C6=0,C3=C5");
w3Eta=C2-C4;
w3EtaData=compatibility_minor_data(w3C3eqC55[3],w3C3eqC55[4]);
checkeq(w3EtaData[1],5,"w3-open eta chart E5 rank");
check(associate(w3EtaData[2],s^2*w3Eta),
  "w3-open eta chart pivot");
check(find_associate(w3EtaData[4],s^4*C5*w3Eta),
  "w3-open eta chart C5 minor");
check(find_associate(w3EtaData[4],
  s^4*w3Eta*(2*C2-3*C4)),
  "w3-open eta chart first linear minor");
check(find_associate(w3EtaData[4],
  s^4*w3Eta*(C2-3*C4)),
  "w3-open eta chart second linear minor");
\\ Thus eta != 0 forces C5=0 and two incompatible linear ratios,
\\ so eta=0 is the only remaining chart.

w3DoubleEq=subst(w3C3eqC5,C2,C4);
w3DoubleEq5=E5_data(w3DoubleEq,
  "A=0,w3-open,C7=C6=0,C3=C5,C2=C4");
w3DoubleAug=augmented_minor_data(w3DoubleEq5[3],w3DoubleEq5[4]);
checkeq([w3DoubleAug[1],w3DoubleAug[2]],[4,5],
  "w3-open double-equality augmented ranks");
check(associate(w3DoubleAug[3],s^3*C5^2),
  "w3-open double-equality C5 minor");

w3TripleEq=subst(w3DoubleEq,C5,0);
w3TripleEq5=E5_data(w3TripleEq,
  "A=0,w3-open,C7=C6=0,C3=C5=0,C2=C4");
w3TripleAug=augmented_minor_data(w3TripleEq5[3],w3TripleEq5[4]);
checkeq([w3TripleAug[1],w3TripleAug[2]],[4,5],
  "w3-open triple-equality augmented ranks");
check(associate(w3TripleAug[3],s^3*C4^2),
  "w3-open triple-equality C4 minor");

\\ The rank tree has now forced C2=...=C7=0.
w3tailV=C0*x^2*z+C1*x*y^2;
w3tail=weighted_determinant(w3U,w3tailV,w3W);
checkeq(subst(w3TripleEq,C4,0),w3tail,
  "w3-open terminal tail specialization");

\\ Recompute D=0 before solving E5: no generic D pivot is retained.
w3equal=subst(w3tail,C0,C1);
w3eq65=solve_E65(w3equal,"A=0,w3-open,D=0");
checkeq(lookup_solution(alllower,w3eq65[1],l1),0,
  "w3-open D=0 l1");
checkeq(lookup_solution(alllower,w3eq65[1],l2),0,
  "w3-open D=0 l2");
checkeq(lookup_solution(alllower,w3eq65[1],l7),0,
  "w3-open D=0 l7");
checkeq(lookup_solution(alllower,w3eq65[1],l8),0,
  "w3-open D=0 l8");
checkeq(subst_many(matdet(Lmat),alllower,w3eq65[1]),0,
  "w3-open D=0 determinant");

\\ On D != 0, first work on a3=rr != 0.  The E4 pivot records
\\ exactly why this solve cannot be specialized to rr=0.
w3D=subst_many(w3tail,[C0,C1],[CC+DD,CC]);
w3Ropen=solve_E654_fixed_a3(w3D,rr,
  "A=0,w3-open,D-open,a3-open");
w3Rpivot=matdet(vecextract(w3Ropen[4],
  w3Ropen[5][1],w3Ropen[5][2]));
check(associate(w3Rpivot,s^8),
  "w3-open D-open a3-open alternate E4 pivot");
checkeq(w3Ropen[6],[b1,b2,b3,b4,b5],
  "w3-open D-open a3-open E4 variables");
checkeq(lookup_solution(w3Ropen[2],w3Ropen[3],b1),0,
  "w3-open D-open a3-open b1");
checkeq(lookup_solution(w3Ropen[2],w3Ropen[3],b2),CC*DD+b3,
  "w3-open D-open a3-open b2");
checkeq(lookup_solution(w3Ropen[2],w3Ropen[3],b4),0,
  "w3-open D-open a3-open b4");
checkeq(lookup_solution(w3Ropen[2],w3Ropen[3],b5),0,
  "w3-open D-open a3-open b5");
w3E3=subst_many(polcoeff(w3Ropen[1],3,t),
  w3Ropen[2],w3Ropen[3]);
checkeq(coeffxyz(w3E3,[2,0,1]),4/3*s^2*l4,
  "w3-open D-open a3-open [x2z]E3");
checkeq(coeffxyz(w3E3,[1,2,0]),4/3*s^2*l4,
  "w3-open D-open a3-open [xy2]E3");
checkeq(subst_many(matdet(Lmat),w3Ropen[2],w3Ropen[3]),
  DD*l4*(s*l0-rr*l6),"w3-open D-open determinant");

\\ Fresh a3=0 rank drop.  Its alternate E4 pivot is independent of DD.
w3Rzero=solve_E654_fixed_a3(w3D,0,
  "A=0,w3-open,D-open,a3=0");
w3RzeroPivot=matdet(vecextract(w3Rzero[4],
  w3Rzero[5][1],w3Rzero[5][2]));
check(associate(w3RzeroPivot,s^8),
  "w3-open D-open a3=0 alternate E4 pivot");
checkeq(w3Rzero[6],[b1,b2,b3,b4,b5],
  "w3-open D-open a3=0 E4 variables");
checkeq(lookup_solution(w3Rzero[2],w3Rzero[3],b1),0,
  "w3-open D-open a3=0 b1");
checkeq(lookup_solution(w3Rzero[2],w3Rzero[3],b2),CC*DD+b3,
  "w3-open D-open a3=0 b2");
checkeq(lookup_solution(w3Rzero[2],w3Rzero[3],b4),0,
  "w3-open D-open a3=0 b4");
checkeq(lookup_solution(w3Rzero[2],w3Rzero[3],b5),0,
  "w3-open D-open a3=0 b5");
w3E3zero=subst_many(polcoeff(w3Rzero[1],3,t),
  w3Rzero[2],w3Rzero[3]);
checkeq(coeffxyz(w3E3zero,[2,0,1]),4/3*s^2*l4,
  "w3-open D-open a3=0 [x2z]E3");
checkeq(coeffxyz(w3E3zero,[1,2,0]),4/3*s^2*l4,
  "w3-open D-open a3=0 [xy2]E3");
checkeq(subst_many(matdet(Lmat),w3Rzero[2],w3Rzero[3]),
  DD*l0*l4*s,"w3-open D-open a3=0 determinant");

print("PASS A=0,w3-open: tail collapse and all D/a3 charts");

print("PARI audit A=0: origin, including the a3 rank drop");

origin=weighted_determinant(0,fullV,0);
origin6=solve_E6(origin,"A=0,origin");
originE5=subst_many(polcoeff(origin,5,t),alllower,origin6[1]);
originExpected=3*l1*x^5 \
  +6*((C0-C1)*a3-l2)*x^4*y \
  -3*C2*a3*x^4*z \
  +3*a3*(2*C2-3*C4)*x^3*y^2 \
  +6*a3*(2*C3-C5)*x^3*y*z \
  -3*C6*a3*x^3*z^2 \
  +6*C5*a3*x^2*y^3 \
  +12*C6*a3*x^2*y^2*z \
  +18*C7*a3*x^2*y*z^2;
checkeq(originE5,originExpected,"origin complete literal E5");

originE4a0=subst_many(
  subst_many(polcoeff(origin,4,t),alllower,origin6[1]),
  [a3,l1,l2],[0,0,0]);
checkeq(coeffxyz(originE4a0,[2,1,1]),8/3*l8^2,
  "origin a3=0 l8 square");
checkeq(coeffxyz(originE4a0,[3,1,0]),
  4/3*(3*a0*l8-2*l6*l8-l7^2),
  "origin a3=0 l7 square");
originDeta0=subst_many(
  subst_many(matdet(Lmat),alllower,origin6[1]),
  [a3,l1,l2,l8,l7],[0,0,0,0,0]);
checkeq(originDeta0,0,"origin a3=0 determinant");

\\ On a3 != 0 literal E5 kills C2,...,C7.  The following fresh
\\ polynomial parametrization solves E6,E5,E4 even at DD=0.
originSpecial=weighted_determinant(
  0,(CC+DD)*x^2*z+CC*x*y^2,0);
originVars=[a1,a2,a3,a4,a5,b1,b3,b4,b5,l1,l2,l7,l8];
originVals=[0,rr,rr,0,0,0,b2-CC*DD,0,0,0,DD*rr,0,0];
for(k=4,6,
  checkeq(subst_many(polcoeff(originSpecial,k,t),
    originVars,originVals),0,Str("origin a3-open E",k)));
originE3=subst_many(polcoeff(originSpecial,3,t),
  originVars,originVals);
originx3=coeffxyz(originE3,[3,0,0]);
checkeq(originx3,-3*rr*l4,"origin a3-open [x3]E3");
checkeq(3*subst_many(matdet(Lmat),originVars,originVals),
  DD*l6*originx3,"origin a3-open determinant identity");

print("PASS A=0 origin: literal E5 and both a3 charts");

print("PARI audit A=0: legal stabilizer/gauge reduction and xz axis");

shearQ=(y+aa*x)^2+x*(z-2*aa*y-aa^2*x);
checkeq(shearQ,q,"q-preserving source shear");
shearW=x*(ww1*(y+aa*x)+ww2*(z-2*aa*y-aa^2*x));
shearExpected=x*((ww1-2*aa*ww2)*y+ww2*z \
  +(aa*ww1-aa^2*ww2)*x);
checkeq(shearW,shearExpected,"source shear action on W");
checkeq(subst(coeffxyz(shearW,[1,1,0]),aa,ww1/(2*ww2)),0,
  "source shear kills xy coefficient");
checkeq(subst(coeffxyz(shearW,[2,0,0]),aa,ww1/(2*ww2)),
  ww1^2/(4*ww2),"source shear x2 residue");

\\ The x^2 residue is a legal top-kernel gauge: one third of source
\\ x-translation, followed by a target shear in coordinate two,
\\ gives precisely (4/3*x^3,0,x^2).
tx1=deriv(P,x); tx2=deriv(Q,x); tx3=deriv(R,x);
checkeq(tx1/3,4/3*x^3,"x-translation first component");
checkeq(tx2/3-2/3*x*y^2-x^2*z,0,
  "target shear cancels x-translation second component");
checkeq(tx3/3,x^2,"x-translation third component");

xzU=4/3*s*x^2*z;
xzW=s*x*z;
xzBaseV=C0*x^2*z+C1*x*y^2+C2*x*y*z+C3*x*z^2 \
  +C4*y^3+C5*y^2*z+C6*y*z^2+C7*z^3;
xzBase=weighted_determinant(xzU,xzBaseV,xzW);
xz5=E5_data(xzBase,"A=0,xz");
xzAug=augmented_minor_data(xz5[3],xz5[4]);
checkeq([xzAug[1],xzAug[2]],[5,6],"xz raw augmented ranks");
check(associate(xzAug[3],s^6*C6),"xz raw augmented minor");

xzC6only=subst(xzBase,C6,0);
xzC6only5=E5_data(xzC6only,"A=0,xz,C6=0");
xzC6Aug=augmented_minor_data(xzC6only5[3],xzC6only5[4]);
checkeq([xzC6Aug[1],xzC6Aug[2]],[5,6],
  "xz C6=0 augmented ranks");
check(associate(xzC6Aug[3],s^6*(3*C5-2*s)),
  "xz C6=0 augmented minor");

xzC6C5=subst(xzC6only,C5,2/3*s);
xzC6C55=E5_data(xzC6C5,"A=0,xz,C6=0,C5=2s/3");
xzC6C5Aug=augmented_minor_data(xzC6C55[3],xzC6C55[4]);
checkeq([xzC6C5Aug[1],xzC6C5Aug[2]],[5,6],
  "xz C6=0,C5=2s/3 augmented ranks");
check(associate(xzC6C5Aug[3],s^6*C4),
  "xz C6=0,C5=2s/3 augmented minor");

\\ C7 != 0 chart: solve E5 over its function field and inspect E4.
xzGeneric=subst(xzC6C5,C4,0);
xzGenericData=E5_data(xzGeneric,"A=0,xz,terminal,C7-open,pivot");
xzGenericIdx=matindexrank(xzGenericData[3]);
xzGenericPivot=matdet(vecextract(xzGenericData[3],
  xzGenericIdx[1],xzGenericIdx[2]));
check(associate(xzGenericPivot,s^3*C7),
  "xz terminal C7-open pivot minor");
xzGeneric65=solve_E65(xzGeneric,"A=0,xz,C7-open");
xzE4=subst_many(polcoeff(xzGeneric,4,t),
  alllower,xzGeneric65[1]);
checkeq(coeffxyz(xzE4,[0,1,3]),-8/27*s^4,
  "xz C7-open literal [yz3]E4");

\\ C7=0 is a fresh E5 rank drop, not a specialization of that solve.
xzC7zero=subst(xzGeneric,C7,0);
xzC7zero5=E5_data(xzC7zero,"A=0,xz,C7=0");
check(find_associate(xzC7zero5[5],s^3),
  "xz C7=0 missing terminal E5 obstruction");

print("PASS A=0 xz axis: legal reduction and every rank-drop chart");

print("PARI audit A=0: xy axis and full factor tree");

xyU=4/3*s*x^2*y;
xyW=s*x*y;
xyBase=weighted_determinant(xyU,fullV,xyW);
xy5=E5_data(xyBase,"A=0,xy");
xyC7Aug=augmented_minor_data(xy5[3],xy5[4]);
checkeq([xyC7Aug[1],xyC7Aug[2]],[4,5],
  "xy C7-open augmented ranks");
check(associate(xyC7Aug[3],s^5*C7),
  "xy C7-open augmented minor");

xyC7zero=subst(xyBase,C7,0);
xyC7zero5=E5_data(xyC7zero,"A=0,xy,C7=0");
xyC6Aug=augmented_minor_data(xyC7zero5[3],xyC7zero5[4]);
checkeq([xyC6Aug[1],xyC6Aug[2]],[4,5],
  "xy C7=0,C6-open augmented ranks");
check(associate(xyC6Aug[3],s^5*C6),
  "xy C7=0,C6-open augmented minor");

xyC76zero=subst(xyC7zero,C6,0);
xyC76zero5=E5_data(xyC76zero,"A=0,xy,C7=C6=0");
xyC5Aug=augmented_minor_data(xyC76zero5[3],xyC76zero5[4]);
checkeq([xyC5Aug[1],xyC5Aug[2]],[4,5],
  "xy C7=C6=0,C5-open augmented ranks");
check(associate(xyC5Aug[3],s^5*C5),
  "xy C7=C6=0,C5-open augmented minor");

xyC765zero=subst(xyC76zero,C5,0);
xyC765zero5=E5_data(xyC765zero,"A=0,xy,C7=C6=C5=0");
xyC3Aug=augmented_minor_data(xyC765zero5[3],xyC765zero5[4]);
checkeq([xyC3Aug[1],xyC3Aug[2]],[4,5],
  "xy C7=C6=C5=0,C3-open augmented ranks");
check(associate(xyC3Aug[3],s^5*C3),
  "xy C7=C6=C5=0,C3-open augmented minor");
xyTailFresh=subst(xyC765zero,C3,0);
xyTailFresh5=E5_data(xyTailFresh,
  "A=0,xy,C7=C6=C5=C3=0");

\\ Thus C3=C5=C6=C7=0.  Recompute the h=0 rank drop.
xyTailV=C0*x^2*z+C1*x*y^2+C2*x*y*z+C4*y^3;
xyTail=weighted_determinant(xyU,xyTailV,xyW);
checkeq(xyTailFresh,xyTail,"xy complete tail specialization");
xyHzero=subst(xyTail,C4,2/3*s);
xyHzero5=E5_data(xyHzero,"A=0,xy,h=0");
check(find_associate(xyHzero5[5],s^3),
  "xy h=0 missing terminal E5 obstruction");

\\ Work on h=2s-3C4 != 0.  The substitutions solve E6 and E5.
xyH=subst(xyTail,C4,(2*s-hh)/3);
kk=4*s^3/(3*hh);
xyTopVars=[a1,a3,a2,a4,a5,l1,l2,l8];
xyTopVals=[4/3*l7,2*s^2*(3*hh-2*s)/(27*hh),
  -kk/9+4/3*l8,0,0,
  2*s*(3*a0-2*l6)/9,
  -4*s*(3*hh*l7+(C0-C1)*s^2)/(27*hh),
  -(2*s-3*C2)*s^2/(9*hh)];
for(k=5,6,
  checkeq(subst_many(polcoeff(xyH,k,t),xyTopVars,xyTopVals),0,
    Str("xy h-open E",k)));

xyE4top=subst_many(polcoeff(xyH,4,t),xyTopVars,xyTopVals);
xySelected=[l0,b3,b4,b5];
xySys4=linear_system(xyE4top,4,xySelected);
checkeq(matrank(xySys4[1]),4,"xy h-open E4 selected rank");
xyIdx4=matindexrank(xySys4[1]);
checkeq(Vec(xyIdx4[2]),[1,2,3,4],"xy h-open E4 pivot columns");
xySol4=pivot_solution(xySys4[1],xySys4[2],xySelected,
  xyIdx4[1],xyIdx4[2]);
checkeq(vecextract(xySol4[4],xyIdx4[1]),
  vector(#xyIdx4[1])~,"xy h-open E4 pivot residual");
xyE4res=subst_many(xyE4top,xySelected,xySol4[1]);
xyCompA=C1*s^2*(s-hh)+(3*hh^2+2*s^2)*l7;
xyCompB=(3*hh+2*s)*(-6*C2-3*hh+4*s);
checkeq(xyE4res,
  -2/9*s*xyCompA*x^3*z/hh \
  -4/243*s^4*xyCompB*x*y^3/hh^2,
  "xy h-open complete E4 remainder");

xyE3base=subst_many(
  subst_many(polcoeff(xyH,3,t),xyTopVars,xyTopVals),
  xySelected,xySol4[1]);
xyE2base=subst_many(
  subst_many(polcoeff(xyH,2,t),xyTopVars,xyTopVals),
  xySelected,xySol4[1]);
xyE1base=subst_many(
  subst_many(polcoeff(xyH,1,t),xyTopVars,xyTopVals),
  xySelected,xySol4[1]);
xyDetBase=subst_many(
  subst_many(matdet(Lmat),xyTopVars,xyTopVals),
  xySelected,xySol4[1]);

\\ First E4 factor: 3h+2s=0 and l7=-C1*s/2.
firstVars=[hh,l7];
firstVals=[-2/3*s,-C1*s/2];
checkeq(subst_many(xyE4res,firstVars,firstVals),0,
  "xy first factor E4");
xyE3first=subst_many(xyE3base,firstVars,firstVals);
checkeq(coeffxyz(xyE3first,[1,0,2]),
  -2/9*s^3*(s-C2)^2,
  "xy first factor C2 square");

xyE3firstC2=subst(xyE3first,C2,s);
xySelected3=[b0,b2,l4,l5];
xySys3=linear_system(xyE3firstC2,3,xySelected3);
checkeq(matrank(xySys3[1]),3,"xy first factor E3 selected rank");
xyIdx3=matindexrank(xySys3[1]);
xySol3=pivot_solution(xySys3[1],xySys3[2],xySelected3,
  xyIdx3[1],xyIdx3[2]);
checkeq(vecextract(xySol3[4],xyIdx3[1]),
  vector(#xyIdx3[1])~,"xy first factor E3 pivot residual");
xyE3res=subst_many(xyE3firstC2,xySelected3,xySol3[1]);
checkeq(xyE3res,
  2/9*C1*s^3*(2*C0-3*C1)*x*y^2,
  "xy first factor complete E3 remainder");

xyE2first=subst_many(
  subst(subst_many(xyE2base,firstVars,firstVals),C2,s),
  xySelected3,xySol3[1]);
xyE1first=subst_many(
  subst(subst_many(xyE1base,firstVars,firstVals),C2,s),
  xySelected3,xySol3[1]);
xyDetFirst=subst_many(
  subst(subst_many(xyDetBase,firstVars,firstVals),C2,s),
  xySelected3,xySol3[1]);

\\ C1=0 descendant.
xyE2zero=subst(xyE2first,C1,0);
checkeq(coeffxyz(xyE2zero,[0,1,1]),-4/27*C0^2*s^4,
  "xy C1=0 [yz]E2");
xyE2zero=subst(xyE2zero,C0,0);
checkeq(coeffxyz(xyE2zero,[1,1,0]),8/27*s^2*l6^2,
  "xy C1=C0=0 [xy]E2");
xyE2zero=subst(xyE2zero,l6,0);
checkeq(coeffxyz(xyE2zero,[2,0,0]),
  s^2*(2*s*l3-3*a0*b1)/9,
  "xy C1=C0=l6=0 [x2]E2");
xyE2zero=subst(xyE2zero,l3,3*a0*b1/(2*s));
checkeq(xyE2zero,0,"xy C1=0 complete E2");
xyE1zero=subst_many(xyE1first,
  [C1,C0,l6,l3],[0,0,0,3*a0*b1/(2*s)]);
checkeq(coeffxyz(xyE1zero,[1,0,0]),-2/9*s^3*b1^2,
  "xy C1=0 [x]E1");
xyDetZero=subst_many(xyDetFirst,
  [C1,C0,l6,l3,b1],[0,0,0,3*a0*b1/(2*s),0]);
checkeq(xyDetZero,0,"xy C1=0 determinant");

\\ 2C0=3C1 descendant, with C1 nonzero (the overlap is above).
xyE2ratio=subst(xyE2first,C0,3/2*C1);
checkeq(coeffxyz(xyE2ratio,[1,0,1]),
  -C1*s^3*(3*C1^2+4*l6)/18,
  "xy ratio [xz]E2");
xyE2ratio=subst(xyE2ratio,l6,-3/4*C1^2);
checkeq(coeffxyz(xyE2ratio,[1,1,0]),
  -2/9*b1*C1*s^3,"xy ratio [xy]E2");
xyE2ratio=subst(xyE2ratio,b1,0);
checkeq(coeffxyz(xyE2ratio,[2,0,0]),
  s^2*(2*s*l3-3*C1*l4)/9,
  "xy ratio [x2]E2");
xyE2ratio=subst(xyE2ratio,l3,3*C1*l4/(2*s));
checkeq(xyE2ratio,0,"xy ratio complete E2");
xyDetRatio=subst_many(xyDetFirst,
  [C0,l6,b1,l3],
  [3/2*C1,-3/4*C1^2,0,3*C1*l4/(2*s)]);
checkeq(xyDetRatio,0,"xy ratio determinant");

\\ Second E4 factor: C2=(4s-3h)/6.
xySecondC2=(4*s-3*hh)/6;
GG=3*hh^2+2*s^2;
xyE4second=subst(xyE4res,C2,xySecondC2);

\\ G != 0: solve the remaining compatibility and inspect E3.
xyL7open=-C1*s^2*(s-hh)/GG;
checkeq(subst(xyE4second,l7,xyL7open),0,
  "xy second factor G-open E4");
xyE3gopen=subst_many(xyE3base,
  [C2,l7],[xySecondC2,xyL7open]);
checkeq(coeffxyz(xyE3gopen,[1,0,2]),
  s^4*(3*hh+2*s)^2/(243*hh),
  "xy second factor G-open [xz2]E3");

\\ G=0: Res_h(G,s-h)=5s^2, hence E4 forces C1=0.
checkeq(polresultant(GG,s-hh,hh),5*s^2,
  "xy G=0 resultant");
xyE4gzero=subst_many(xyE4res,[C2,C1],[xySecondC2,0]);
checkeq(xyE4gzero,-2/9*s*GG*l7*x^3*z/hh,
  "xy G=0 complete E4 factorization");
xyE3gzero=subst_many(xyE3base,[C2,C1],[xySecondC2,0]);
checkeq(coeffxyz(xyE3gzero,[1,0,2]),
  s^4*(3*hh+2*s)^2/(243*hh),
  "xy G=0 [xz2]E3");
checkeq((3*hh+2*s)^2-3*GG,-2*s*(s-6*hh),
  "xy G=0 exact E3 remainder identity");
checkeq(subst(GG,s,6*hh),75*hh^2,
  "xy G=0 final contradiction");

print("PASS A=0 xy axis: every E5/E4 rank drop and both descendants");
print("all independent PARI A=0 certificates passed");
quit(0);
}
