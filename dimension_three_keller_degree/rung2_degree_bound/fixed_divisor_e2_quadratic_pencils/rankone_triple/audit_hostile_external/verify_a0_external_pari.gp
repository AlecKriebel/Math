\\ Clean-room hostile PARI/GP reconstruction of the A=0 branch in the
\\ rank-one fixed-divisor e=2 triple-companion theorem.
\\
\\ Top data:
\\   P=x^4, Q=x^2(y^2+xz), R=x^3.
\\ No matrix is imported from the supplied SymPy or PARI certificates.
\\ Every localized solve below records a pivot supported only on variables
\\ declared nonzero in that chart.  Rank-drop specializations are rebuilt.

fatal(msg) = { print(Str("FAIL: ",msg)); quit(1); };
require(flag,msg) = { if(!(flag),fatal(msg)); };
same(got,want,msg) =
{
  if(got!=want,fatal(Str(msg,": got ",got,", want ",want)));
};

xyz=[x,y,z];

\\ Ascending exponent order is independent of the primary SymPy order.
hexps(n) =
{
  my(out=List());
  for(i=0,n,
    for(j=0,n-i,listput(out,[i,j,n-i-j]))
  );
  Vec(out);
};

cxyz(f,e) =
{
  polcoeff(polcoeff(polcoeff(f,e[1],x),e[2],y),e[3],z);
};

hcoeffs(f,n) =
{
  my(E=hexps(n));
  vector(#E,i,cxyz(f,E[i]));
};

jac(hh) = matrix(3,3,i,j,deriv(hh[i],xyz[j]));

zero_all(f,vv) =
{
  my(g=f);
  for(i=1,#vv,g=subst(g,vv[i],0));
  g;
};

put_many(f,vv,ww) =
{
  my(g=f);
  require(#vv==#ww,"put_many length mismatch");
  for(i=1,#vv,g=subst(g,vv[i],ww[i]));
  g;
};

lin_system(f,n,vv) =
{
  my(cc=hcoeffs(f,n));
  my(M=matrix(#cc,#vv,i,j,deriv(cc[i],vv[j])));
  my(rhs=vector(#cc,i,-zero_all(cc[i],vv))~);
  [M,rhs];
};

complement_indices(n,indices) =
{
  my(out=List(),S=Set(indices));
  for(i=1,n,if(!setsearch(S,i),listput(out,i)));
  Vec(out);
};

pivot_solve(M,rhs,unknowns,rows,pivots) =
{
  my(free=complement_indices(#unknowns,pivots));
  my(square=vecextract(M,rows,pivots));
  my(freepart=if(#free,
    vecextract(M,rows,free)*vector(#free,i,unknowns[free[i]])~,
    vector(#rows)~));
  my(values=matsolve(square,vecextract(rhs,rows)-freepart));
  my(sol=unknowns~);
  for(i=1,#pivots,sol[pivots[i]]=values[i]);
  [sol,pivots,free,M*sol-rhs];
};

cleared_left(M,rhs) =
{
  my(N=matker(M~),pairs=List(),vectors=List());
  for(j=1,matsize(N)[2],
    my(mult=1,v,pair);
    for(i=1,matsize(N)[1],mult*=denominator(N[i,j]));
    v=mult*N[,j];
    for(i=1,matsize(N)[1],
      same(denominator(v[i]),1,
        Str("left vector ",j," retains a denominator at entry ",i)));
    same(M~*v,vector(matsize(M)[2])~,
      Str("left vector ",j," is not an exact syzygy"));
    pair=v~*rhs;
    listput(vectors,v);
    listput(pairs,pair);
  );
  [Vec(vectors),Vec(pairs)];
};

is_qconstant(v) =
{
  type(v)=="t_INT" || type(v)=="t_FRAC";
};

associate(a,b) =
{
  if(a==0 || b==0,return(a==0 && b==0));
  my(ratio=simplify(a/b));
  is_qconstant(ratio) && a==ratio*b;
};

has_associate(vv,target) =
{
  for(i=1,#vv,if(associate(vv[i],target),return(1)));
  0;
};

value_of(vv,ww,target) =
{
  for(i=1,#vv,if(vv[i]==target,return(ww[i])));
  fatal(Str("solution lookup failed for ",target));
};

\\ Lower coefficients:
\\ H2_1=sum a_i*m2_i, H2_2=sum b_i*m2_i, and L is row-major.
m2=[x^2,x*y,x*z,y^2,y*z,z^2];
aall=[a0,a1,a2,a3,a4,a5];
ball=[b0,b1,b2,b3,b4,b5];
ell=[l0,l1,l2,l3,l4,l5,l6,l7,l8];
lower=concat(concat(aall,ball),ell);
L=matrix(3,3,i,j,ell[3*(i-1)+j]);

P=x^4;
q=y^2+x*z;
Q=x^2*q;
R=x^3;

wdet(U,V,W) =
{
  my(H2=[sum(i=1,6,aall[i]*m2[i]),
         sum(i=1,6,ball[i]*m2[i]),W]);
  matdet(L+t*jac(H2)+t^2*jac([U,V,R])+t^3*jac([P,Q,0]));
};

fixed_E6(weighted,label) =
{
  my(sys=lin_system(polcoeff(weighted,6,t),6,lower));
  my(M=sys[1],rhs=sys[2]);
  my(rows=[24,25,27,28],cols=[2,3,5,6]);
  same(matrank(M),4,Str(label,": E6 rank"));
  same(matdet(vecextract(M,rows,cols)),-1296,
    Str(label,": constant E6 pivot"));
  my(sol=pivot_solve(M,rhs,lower,rows,cols));
  same(sol[4],vector(matsize(M)[1])~,Str(label,": E6 residual"));
  [sol,M,rhs];
};

E5_info(weighted,label) =
{
  my(six=fixed_E6(weighted,label),sol6=six[1]);
  my(value=put_many(polcoeff(weighted,5,t),lower,sol6[1]));
  my(free=vector(#sol6[3],i,lower[sol6[3][i]]));
  my(sys=lin_system(value,5,free));
  my(left=cleared_left(sys[1],sys[2]));
  [sol6,free,sys[1],sys[2],left[2]];
};

solve_E65_guard(weighted,label,pivot_target,expected_rank) =
{
  my(data=E5_info(weighted,label));
  my(sol6=data[1],free=data[2],M=data[3],rhs=data[4]);
  same(matrank(M),expected_rank,Str(label,": E5 rank"));
  my(idx=matindexrank(M));
  my(pivot=matdet(vecextract(M,idx[1],idx[2])));
  require(associate(pivot,pivot_target),Str(label,": unsafe E5 pivot"));
  my(sol5=pivot_solve(M,rhs,free,idx[1],idx[2]));
  same(sol5[4],vector(matsize(M)[1])~,Str(label,": E5 residual"));
  my(full=vector(#lower,i,put_many(sol6[1][i],free,sol5[1])));
  same(put_many(polcoeff(weighted,6,t),lower,full),0,
    Str(label,": composed E6"));
  same(put_many(polcoeff(weighted,5,t),lower,full),0,
    Str(label,": composed E5"));
  [full,sol6,sol5,pivot];
};

augmented_guard(M,rhs,rankM,rankAug,target,label) =
{
  my(A=concat(M,rhs),idx=matindexrank(A));
  same(matrank(M),rankM,Str(label,": coefficient rank"));
  same(matrank(A),rankAug,Str(label,": augmented rank"));
  my(d=matdet(vecextract(A,idx[1],idx[2])));
  require(associate(d,target),Str(label,": augmented minor"));
};

direction_column(d) =
{
  my(E3=hexps(3),E2=hexps(2));
  concat(concat(
    vector(10,i,cxyz(d[1],E3[i])),
    vector(10,i,cxyz(d[2],E3[i]))),
    vector(6,i,cxyz(d[3],E2[i])))~;
};

{
print("External PARI audit: raw E7 and effective gauges");

E3=hexps(3);
mon3=vector(10,i,x^E3[i][1]*y^E3[i][2]*z^E3[i][3]);
E2=hexps(2);
mon2=vector(6,i,x^E2[i][1]*y^E2[i][2]*z^E2[i][3]);
uu=[u0,u1,u2,u3,u4,u5,u6,u7,u8,u9];
vv=[v0,v1,v2,v3,v4,v5,v6,v7,v8,v9];
ww=[ww0,ww1,ww2,ww3,ww4,ww5];
rawU=sum(i=1,10,uu[i]*mon3[i]);
rawV=sum(i=1,10,vv[i]*mon3[i]);
rawW=sum(i=1,6,ww[i]*mon2[i]);
rawvars=concat(concat(uu,vv),ww);
rawE7=matdet(jac([P,Q,rawW]))
  +matdet(jac([P,rawV,R]))
  +matdet(jac([rawU,Q,R]));
rawsys=lin_system(rawE7,7,rawvars);
rawM=rawsys[1];
same(matsize(rawM),[36,26],"raw E7 shape");
same(matrank(rawM),8,"raw E7 rank");
rawidx=matindexrank(rawM);
same(matdet(vecextract(rawM,rawidx[1],rawidx[2])),-7558272,
  "raw E7 maximal minor");

dirs=List();
\\ Two determinant-one target row shears.
listput(dirs,[R,0,0]);
listput(dirs,[0,R,0]);
\\ Only x and y translations add independent top directions.
listput(dirs,[deriv(P,x),deriv(Q,x),deriv(R,x)]);
listput(dirs,[deriv(P,y),deriv(Q,y),deriv(R,y)]);
\\ Fourteen normal directions.
listput(dirs,[x*q,0,0]);
listput(dirs,[4/3*x^2*y,0,x*y]);
listput(dirs,[4/3*x^2*z,0,x*z]);
listput(dirs,[4/3*x*y^2,0,y^2]);
listput(dirs,[4/3*x*y*z,0,y*z]);
listput(dirs,[4/3*x*z^2,0,z^2]);
listput(dirs,[0,x^2*z,0]);
listput(dirs,[0,x*y^2,0]);
listput(dirs,[0,x*y*z,0]);
listput(dirs,[0,x*z^2,0]);
listput(dirs,[0,y^3,0]);
listput(dirs,[0,y^2*z,0]);
listput(dirs,[0,y*z^2,0]);
listput(dirs,[0,z^3,0]);
dirs=Vec(dirs);
K=matrix(26,18,i,j,direction_column(dirs[j])[i]);
same(rawM*K,matrix(36,18),"raw kernel directions");
same(matrank(K),18,"raw kernel independence");
Kidx=matindexrank(K);
same(matdet(vecextract(K,Kidx[1],Kidx[2])),-512/27,
  "raw kernel independence minor");
same(26-matrank(rawM),18,"raw kernel completeness");
same(direction_column([deriv(P,z),deriv(Q,z),deriv(R,z)]),
  direction_column([0,R,0]),"z translation redundancy");
same(matdet(matrix(3,3,i,j,
  if(i==j,1,if(j==3,if(i==1,ts1,if(i==2,ts2,0)),0)))),1,
  "target shear determinant");

print("PASS raw E7: rank 8/nullity 18 and exactly four independent legal gauges");

print("External PARI audit: A=0 E6 branch cover");

Vall=C0*x^2*z+C1*x*y^2+C2*x*y*z+C3*x*z^2
  +C4*y^3+C5*y^2*z+C6*y*z^2+C7*z^3;
Wall=w1*x*y+w2*x*z+w3*y^2+w4*y*z+w5*z^2;
A0all=wdet(4/3*x*Wall,Vall,Wall);
A0sys=lin_system(polcoeff(A0all,6,t),6,lower);
same(matrank(A0sys[1]),4,"A=0 raw E6 lower rank");
same(matdet(vecextract(A0sys[1],[24,25,27,28],[2,3,5,6])),
  -1296,"A=0 raw E6 constant pivot");
A0pairs=cleared_left(A0sys[1],A0sys[2])[2];
require(has_associate(A0pairs,w5^2),"A=0 E6 missing w5 square");

A0w5=subst(A0all,w5,0);
A0w5sys=lin_system(polcoeff(A0w5,6,t),6,lower);
A0w5pairs=cleared_left(A0w5sys[1],A0w5sys[2])[2];
require(has_associate(A0w5pairs,w4^2),"A=0 E6 missing w4 square");

A0red=subst(A0w5,w4,0);
A0redsys=lin_system(polcoeff(A0red,6,t),6,lower);
A0redpairs=cleared_left(A0redsys[1],A0redsys[2])[2];
require(has_associate(A0redpairs,w3*w1),
  "A=0 E6 missing w3*w1");
require(has_associate(A0redpairs,w3*(w3-w2)),
  "A=0 E6 missing w3*(w3-w2)");

print("PASS A=0 E6: w4=w5=0 and w3*w1=w3*(w3-w2)=0 exhaust the cover");

print("External PARI audit: w3-open and origin");

\\ w3=s!=0 forces W=sq.  Polynomial E5 syzygies collapse the V tail.
w3top=wdet(4/3*s*x*q,Vall,s*q);
w3info=E5_info(w3top,"w3-open full tail");
w3pairs=w3info[5];
require(has_associate(w3pairs,s^2*C6),"w3-open C6");
require(has_associate(w3pairs,s^2*(2*C2-3*C4)),
  "w3-open 2C2-3C4");
require(has_associate(w3pairs,s^2*C3),"w3-open C3");
require(has_associate(w3pairs,s^2*C5),"w3-open C5");
require(has_associate(w3pairs,s^2*C7),"w3-open C7");

w3partial=put_many(w3top,[C3,C5,C6,C7],[0,0,0,0]);
w3partialinfo=E5_info(w3partial,"w3-open reduced tail");
w3partialpairs=w3partialinfo[5];
require(has_associate(w3partialpairs,s^2*C2),"w3-open C2");
require(has_associate(w3partialpairs,s^2*(2*C2-3*C4)),
  "w3-open C4");

w3tail=wdet(4/3*s*x*q,C0*x^2*z+C1*x*y^2,s*q);

\\ D=0 is rebuilt before the E5 solve.
w3D0=subst(w3tail,C0,C1);
w3D0sol=solve_E65_guard(w3D0,"w3-open D=0",s^2,4);
same(value_of(lower,w3D0sol[1],l1),0,"w3 D=0 l1");
same(value_of(lower,w3D0sol[1],l2),0,"w3 D=0 l2");
same(value_of(lower,w3D0sol[1],l7),0,"w3 D=0 l7");
same(value_of(lower,w3D0sol[1],l8),0,"w3 D=0 l8");
same(put_many(matdet(L),lower,w3D0sol[1]),0,"w3 D=0 determinant");

\\ On D!=0, E5 has a D*s^2 pivot.  E4 has a further r=a3 rank drop.
w3D=wdet(4/3*s*x*q,(CC+DD)*x^2*z+CC*x*y^2,s*q);
w3D65=solve_E65_guard(w3D,"w3-open D!=0",DD*s^2,4);
w3E65vars=[a1,a2,a3,a4,a5,l1,l2,l7,l8];
w3E65vals=[0,rr+4/3*s*DD,rr,0,0,0,DD*rr,0,s*DD];
same(put_many(polcoeff(w3D,6,t),w3E65vars,w3E65vals),0,
  "w3 D-open explicit E6");
same(put_many(polcoeff(w3D,5,t),w3E65vars,w3E65vals),0,
  "w3 D-open explicit E5");
w3E4pre=put_many(polcoeff(w3D,4,t),w3E65vars,w3E65vals);

\\ r!=0: the advertised four-variable E4 pivot is safe only here.
w3rvars=[b1,b3,b4,b5];
w3rsys=lin_system(w3E4pre,4,w3rvars);
same(matrank(w3rsys[1]),4,"w3 D-open r-open E4 rank");
w3ridx=matindexrank(w3rsys[1]);
w3rpivot=matdet(vecextract(w3rsys[1],w3ridx[1],w3ridx[2]));
require(associate(w3rpivot,s^8),
  Str("w3 D-open r-open E4 pivot: ",w3rpivot));
w3rsol=pivot_solve(w3rsys[1],w3rsys[2],w3rvars,
  w3ridx[1],w3ridx[2]);
same(w3rsol[4],vector(matsize(w3rsys[1])[1])~,
  "w3 D-open r-open E4 residual");
w3E4vals=[0,b2-CC*DD,0,0];
same(put_many(w3E4pre,w3rvars,w3E4vals),0,
  "w3 D-open r-open E4 converse");
w3rallvars=concat(w3E65vars,w3rvars);
w3rallvals=concat(w3E65vals,w3E4vals);
w3rE3=put_many(polcoeff(w3D,3,t),w3rallvars,w3rallvals);
same(cxyz(w3rE3,[2,0,1]),4/3*s^2*l4,
  "w3 D-open r-open E3 l4");
same(put_many(matdet(L),w3rallvars,w3rallvals),
  DD*l4*(s*l0-rr*l6),"w3 D-open r-open determinant");

\\ r=0: a fresh rank-four E4 matrix has an s^8 pivot and one free b3.
w3E4r0=subst(w3E4pre,rr,0);
w3r0vars=[b1,b2,b3,b4,b5];
w3r0sys=lin_system(w3E4r0,4,w3r0vars);
same(matrank(w3r0sys[1]),4,"w3 D-open r=0 E4 rank");
w3r0idx=matindexrank(w3r0sys[1]);
require(associate(matdet(vecextract(w3r0sys[1],
  w3r0idx[1],w3r0idx[2])),s^8),"w3 D-open r=0 E4 pivot");
w3r0sol=pivot_solve(w3r0sys[1],w3r0sys[2],w3r0vars,
  w3r0idx[1],w3r0idx[2]);
same(w3r0sol[4],vector(matsize(w3r0sys[1])[1])~,
  "w3 D-open r=0 E4 residual");
w3r0vals=[0,CC*DD+b3,b3,0,0];
same(put_many(w3E4r0,w3r0vars,w3r0vals),0,
  "w3 D-open r=0 E4 converse");
w3r0basevals=put_many(w3E65vals,[rr],[0]);
w3r0allvars=concat(w3E65vars,w3r0vars);
w3r0allvals=concat(w3r0basevals,w3r0vals);
w3r0E3=put_many(polcoeff(w3D,3,t),w3r0allvars,w3r0allvals);
same(cxyz(w3r0E3,[2,0,1]),4/3*s^2*l4,
  "w3 D-open r=0 E3 l4");
same(cxyz(w3r0E3,[0,3,0]),8/3*s^2*(DD*b3-l5),
  "w3 D-open r=0 E3 second coefficient");
same(put_many(matdet(L),w3r0allvars,w3r0allvals),
  DD*l0*l4*s,"w3 D-open r=0 determinant");

\\ Origin W=U=0.  Record the literal E5 identity before splitting a3.
origin=wdet(0,Vall,0);
origin6=fixed_E6(origin,"origin");
originE5=put_many(polcoeff(origin,5,t),lower,origin6[1][1]);
originExpected=3*l1*x^5
  +6*((C0-C1)*a3-l2)*x^4*y
  -3*C2*a3*x^4*z
  +3*a3*(2*C2-3*C4)*x^3*y^2
  +6*a3*(2*C3-C5)*x^3*y*z
  -3*C6*a3*x^3*z^2
  +6*C5*a3*x^2*y^3
  +12*C6*a3*x^2*y^2*z
  +18*C7*a3*x^2*y*z^2;
same(originE5,originExpected,"origin literal E5");

originE4zero=put_many(
  put_many(polcoeff(origin,4,t),lower,origin6[1][1]),
  [a3,l1,l2],[0,0,0]);
same(cxyz(originE4zero,[2,1,1]),8/3*l8^2,
  "origin a3=0 l8 square");
same(cxyz(originE4zero,[3,1,0]),
  4/3*(3*a0*l8-2*l6*l8-l7^2),
  "origin a3=0 l7 square");
originZeroDet=put_many(
  put_many(matdet(L),lower,origin6[1][1]),
  [a3,l1,l2,l8,l7],[0,0,0,0,0]);
same(originZeroDet,0,"origin a3=0 determinant");

\\ a3=r!=0: literal E5 kills C2,...,C7; E4 is rebuilt with an r^4 pivot.
originOpen=wdet(0,(OC+OD)*x^2*z+OC*x*y^2,0);
originPreVars=[a1,a2,a3,a4,a5,l1,l2,l7,l8];
originPreVals=[0,or,or,0,0,0,OD*or,0,0];
same(put_many(polcoeff(originOpen,6,t),originPreVars,originPreVals),0,
  "origin a3-open E6");
same(put_many(polcoeff(originOpen,5,t),originPreVars,originPreVals),0,
  "origin a3-open E5");
originE4pre=put_many(polcoeff(originOpen,4,t),
  originPreVars,originPreVals);
originE4vars=[b1,b3,b4,b5];
originE4sys=lin_system(originE4pre,4,originE4vars);
same(matrank(originE4sys[1]),4,"origin a3-open E4 rank");
originE4idx=matindexrank(originE4sys[1]);
require(associate(matdet(vecextract(originE4sys[1],
  originE4idx[1],originE4idx[2])),or^4),
  "origin a3-open E4 pivot");
originE4sol=pivot_solve(originE4sys[1],originE4sys[2],
  originE4vars,originE4idx[1],originE4idx[2]);
same(originE4sol[4],vector(matsize(originE4sys[1])[1])~,
  "origin a3-open E4 residual");
originE4vals=[0,b2-OC*OD,0,0];
same(put_many(originE4pre,originE4vars,originE4vals),0,
  "origin a3-open E4 converse");
originAllVars=concat(originPreVars,originE4vars);
originAllVals=concat(originPreVals,originE4vals);
originE3=put_many(polcoeff(originOpen,3,t),originAllVars,originAllVals);
originX3=cxyz(originE3,[3,0,0]);
same(originX3,-3*or*l4,"origin a3-open E3 x3");
same(3*put_many(matdet(L),originAllVars,originAllVals),
  OD*l6*originX3,"origin a3-open determinant identity");

print("PASS w3-open and origin: all D, r=a3, and square rank drops close");

print("External PARI audit: q-shear and xz axis");

\\ The unipotent source shear preserves q, hence P,Q,R.
yim=y+sh*x;
zim=z-2*sh*y-sh^2*x;
same(yim^2+x*zim,q,"q-preserving shear");
same(matdet(jac([x,yim,zim])),1,"q-preserving shear Jacobian");
shearW=x*(sw1*yim+sw2*zim);
same(shearW,
  x*((sw1-2*sh*sw2)*y+sw2*z+(sh*sw1-sh^2*sw2)*x),
  "shear action on W");
same(put_many(cxyz(shearW,[1,1,0]),[sh],[sw1/(2*sw2)]),0,
  "shear xz chart kills xy");
same(put_many(cxyz(shearW,[2,0,0]),[sh],[sw1/(2*sw2)]),
  sw1^2/(4*sw2),"shear x2 residue");

\\ The residue pair is removed by one third of an x-translation; its
\\ second component is absorbed by the free V-tail.  No target-shear
\\ fiction or division beyond sw2!=0 is used.
tx=[deriv(P,x),deriv(Q,x),deriv(R,x)];
same(tx[1]/3,4/3*x^3,"x-translation U residue");
same(tx[2]/3,2/3*x*y^2+x^2*z,"x-translation V relabel");
same(tx[3]/3,x^2,"x-translation W residue");
resk=sw1^2/(4*sw2);
same(4/3*resk*x^3-resk*tx[1]/3,0,
  "x-translation cancels shear U residue");
same(-resk*tx[2]/3,
  -resk*(2/3*x*y^2+x^2*z),
  "x-translation changes only free V-tail coefficients");
same(resk*x^2-resk*tx[3]/3,0,
  "x-translation cancels shear W residue");

xzU=4/3*s*x^2*z;
xzW=s*x*z;
xz=wdet(xzU,Vall,xzW);
xzInfo=E5_info(xz,"xz raw");
augmented_guard(xzInfo[3],xzInfo[4],5,6,s^6*C6,
  "xz C6-open");
xzC6=subst(xz,C6,0);
xzC6Info=E5_info(xzC6,"xz C6=0");
augmented_guard(xzC6Info[3],xzC6Info[4],5,6,
  s^6*(3*C5-2*s),"xz C5-open");
xzC65=subst(xzC6,C5,2/3*s);
xzC65Info=E5_info(xzC65,"xz C6=0,C5=2s/3");
augmented_guard(xzC65Info[3],xzC65Info[4],5,6,s^6*C4,
  "xz C4-open");
xzTerminal=subst(xzC65,C4,0);

\\ C7!=0 has an s^3*C7 pivot and a literal E4 contradiction.
xzOpen=solve_E65_guard(xzTerminal,"xz terminal C7!=0",
  s^3*C7,5);
xzE4=put_many(polcoeff(xzTerminal,4,t),lower,xzOpen[1]);
same(cxyz(xzE4,[0,1,3]),-8/27*s^4,
  "xz C7-open E4 yz3");

\\ C7=0 is rebuilt and is already inconsistent at E5.
xzZero=subst(xzTerminal,C7,0);
xzZeroInfo=E5_info(xzZero,"xz terminal C7=0");
require(has_associate(xzZeroInfo[5],s^3),
  "xz C7=0 E5 obstruction");

print("PASS xz axis: shear is legal and every E5 pivot drop is rebuilt");

print("External PARI audit: xy axis and complete h/G/factor tree");

xyU=4/3*s*x^2*y;
xyW=s*x*y;
xy=wdet(xyU,Vall,xyW);

\\ Rebuild every successive augmented-rank drop.  On each open chart
\\ rank([M|rhs])=rank(M)+1, and the displayed minor is supported on s
\\ and the parameter declared nonzero.
xyInfo=E5_info(xy,"xy raw");
augmented_guard(xyInfo[3],xyInfo[4],4,5,s^5*C7,
  "xy C7-open");
xyC7=subst(xy,C7,0);
xyC7Info=E5_info(xyC7,"xy C7=0");
augmented_guard(xyC7Info[3],xyC7Info[4],4,5,s^5*C6,
  "xy C6-open");
xyC76=subst(xyC7,C6,0);
xyC76Info=E5_info(xyC76,"xy C7=C6=0");
augmented_guard(xyC76Info[3],xyC76Info[4],4,5,s^5*C5,
  "xy C5-open");
xyC765=subst(xyC76,C5,0);
xyC765Info=E5_info(xyC765,"xy C7=C6=C5=0");
augmented_guard(xyC765Info[3],xyC765Info[4],4,5,s^5*C3,
  "xy C3-open");

xyTail=subst(xyC765,C3,0);
same(xyTail,wdet(xyU,
  C0*x^2*z+C1*x*y^2+C2*x*y*z+C4*y^3,xyW),
  "xy complete tail");

\\ h=2s-3C4=0 is a fresh E5 inconsistency.
xyH0=subst(xyTail,C4,2/3*s);
xyH0Info=E5_info(xyH0,"xy h=0");
require(has_associate(xyH0Info[5],s^3),"xy h=0 E5 obstruction");

\\ On h!=0, E6/E5 have a complete four-pivot solve with pivot h*s^2.
xyH=wdet(xyU,
  C0*x^2*z+C1*x*y^2+C2*x*y*z+(2*s-hh)/3*y^3,xyW);
xyHInfo=E5_info(xyH,"xy h!=0");
same(matrank(xyHInfo[3]),4,"xy h-open E5 rank");
xyHidx=matindexrank(xyHInfo[3]);
require(associate(matdet(vecextract(xyHInfo[3],
  xyHidx[1],xyHidx[2])),hh*s^2),"xy h-open E5 pivot");

kk=4*s^3/(3*hh);
xyTopVars=[a1,a3,a2,a4,a5,l1,l2,l8];
xyTopVals=[4/3*l7,2*s^2*(3*hh-2*s)/(27*hh),
  -kk/9+4/3*l8,0,0,
  2*s*(3*a0-2*l6)/9,
  -4*s*(3*hh*l7+(C0-C1)*s^2)/(27*hh),
  -(2*s-3*C2)*s^2/(9*hh)];
same(put_many(polcoeff(xyH,6,t),xyTopVars,xyTopVals),0,
  "xy h-open explicit E6");
same(put_many(polcoeff(xyH,5,t),xyTopVars,xyTopVals),0,
  "xy h-open explicit E5");

\\ Solve four selected E4 variables.  The pivot contains only s and h;
\\ the full remainder is exactly the two displayed compatibility rows.
xyE4top=put_many(polcoeff(xyH,4,t),xyTopVars,xyTopVals);
xySelected=[l0,b3,b4,b5];
xySys4=lin_system(xyE4top,4,xySelected);
same(matrank(xySys4[1]),4,"xy h-open E4 selected rank");
xyIdx4=matindexrank(xySys4[1]);
require(associate(matdet(vecextract(xySys4[1],
  xyIdx4[1],xyIdx4[2])),s^10/hh^3),
  "xy h-open E4 selected pivot");
xySol4=pivot_solve(xySys4[1],xySys4[2],xySelected,
  xyIdx4[1],xyIdx4[2]);
same(vecextract(xySol4[4],xyIdx4[1]),
  vector(#xyIdx4[1])~,"xy h-open E4 pivot residual");
xyE4res=put_many(xyE4top,xySelected,xySol4[1]);
xyCompA=C1*s^2*(s-hh)+(3*hh^2+2*s^2)*l7;
xyCompB=(3*hh+2*s)*(-6*C2-3*hh+4*s);
same(xyE4res,
  -2/9*s*xyCompA*x^3*z/hh
  -4/243*s^4*xyCompB*x*y^3/hh^2,
  "xy complete E4 remainder");

xyE3base=put_many(
  put_many(polcoeff(xyH,3,t),xyTopVars,xyTopVals),
  xySelected,xySol4[1]);
xyE2base=put_many(
  put_many(polcoeff(xyH,2,t),xyTopVars,xyTopVals),
  xySelected,xySol4[1]);
xyE1base=put_many(
  put_many(polcoeff(xyH,1,t),xyTopVars,xyTopVals),
  xySelected,xySol4[1]);
xyDetBase=put_many(
  put_many(matdet(L),xyTopVars,xyTopVals),
  xySelected,xySol4[1]);

\\ First factor F=3h+2s=0.  CompA then fixes l7 with no new divisor.
firstVars=[hh,l7];
firstVals=[-2/3*s,-C1*s/2];
same(put_many(xyE4res,firstVars,firstVals),0,
  "xy first factor E4");
xyE3first=put_many(xyE3base,firstVars,firstVals);
same(cxyz(xyE3first,[1,0,2]),
  -2/9*s^3*(s-C2)^2,"xy first factor C2 square");

\\ C2=s.  A rank-three E3 pivot supported only on s leaves precisely
\\ C1(2C0-3C1)=0; we do not falsely require the full pre-compatibility
\\ residual to vanish.
xyE3firstC2=subst(xyE3first,C2,s);
xySelected3=[b0,b2,l4,l5];
xySys3=lin_system(xyE3firstC2,3,xySelected3);
same(matrank(xySys3[1]),3,"xy first factor E3 selected rank");
xyIdx3=matindexrank(xySys3[1]);
require(associate(matdet(vecextract(xySys3[1],
  xyIdx3[1],xyIdx3[2])),s^8),
  "xy first factor E3 selected pivot");
xySol3=pivot_solve(xySys3[1],xySys3[2],xySelected3,
  xyIdx3[1],xyIdx3[2]);
same(vecextract(xySol3[4],xyIdx3[1]),
  vector(#xyIdx3[1])~,"xy first factor E3 pivot residual");
xyE3res=put_many(xyE3firstC2,xySelected3,xySol3[1]);
same(xyE3res,
  2/9*C1*s^3*(2*C0-3*C1)*x*y^2,
  "xy first factor complete E3 remainder");

xyE2first=put_many(
  subst(put_many(xyE2base,firstVars,firstVals),C2,s),
  xySelected3,xySol3[1]);
xyE1first=put_many(
  subst(put_many(xyE1base,firstVars,firstVals),C2,s),
  xySelected3,xySol3[1]);
xyDetFirst=put_many(
  subst(put_many(xyDetBase,firstVars,firstVals),C2,s),
  xySelected3,xySol3[1]);

\\ Descendant C1=0, including its intersection with 2C0=3C1.
xyE2zero=subst(xyE2first,C1,0);
same(cxyz(xyE2zero,[0,1,1]),-4/27*C0^2*s^4,
  "xy C1=0 C0 square");
xyE2zero=subst(xyE2zero,C0,0);
same(cxyz(xyE2zero,[1,1,0]),8/27*s^2*l6^2,
  "xy C1=C0=0 l6 square");
xyE2zero=subst(xyE2zero,l6,0);
same(cxyz(xyE2zero,[2,0,0]),
  s^2*(2*s*l3-3*a0*b1)/9,
  "xy C1=C0=l6=0 E2 relation");
xyE2zero=subst(xyE2zero,l3,3*a0*b1/(2*s));
same(xyE2zero,0,"xy C1=0 complete E2");
xyE1zero=put_many(xyE1first,
  [C1,C0,l6,l3],[0,0,0,3*a0*b1/(2*s)]);
same(cxyz(xyE1zero,[1,0,0]),-2/9*s^3*b1^2,
  "xy C1=0 b1 square");
xyDetZero=put_many(xyDetFirst,
  [C1,C0,l6,l3,b1],[0,0,0,3*a0*b1/(2*s),0]);
same(xyDetZero,0,"xy C1=0 determinant");

\\ Descendant 2C0=3C1 with C1!=0.  The C1=0 overlap is above.
xyE2ratio=subst(xyE2first,C0,3/2*C1);
same(cxyz(xyE2ratio,[1,0,1]),
  -C1*s^3*(3*C1^2+4*l6)/18,
  "xy ratio l6 relation");
xyE2ratio=subst(xyE2ratio,l6,-3/4*C1^2);
same(cxyz(xyE2ratio,[1,1,0]),-2/9*b1*C1*s^3,
  "xy ratio b1 relation");
xyE2ratio=subst(xyE2ratio,b1,0);
same(cxyz(xyE2ratio,[2,0,0]),
  s^2*(2*s*l3-3*C1*l4)/9,
  "xy ratio l3 relation");
xyE2ratio=subst(xyE2ratio,l3,3*C1*l4/(2*s));
same(xyE2ratio,0,"xy ratio complete E2");
xyDetRatio=put_many(xyDetFirst,
  [C0,l6,b1,l3],
  [3/2*C1,-3/4*C1^2,0,3*C1*l4/(2*s)]);
same(xyDetRatio,0,"xy ratio determinant");

\\ Second factor B=-6C2-3h+4s=0.
xySecondC2=(4*s-3*hh)/6;
GG=3*hh^2+2*s^2;
xyE4second=subst(xyE4res,C2,xySecondC2);

\\ G!=0: CompA fixes l7.  E3 forces F=0, landing exactly in the
\\ already-closed first factor, including the intersection values.
xyL7open=-C1*s^2*(s-hh)/GG;
same(subst(xyE4second,l7,xyL7open),0,
  "xy second factor G-open E4");
xyE3gopen=put_many(xyE3base,
  [C2,l7],[xySecondC2,xyL7open]);
same(cxyz(xyE3gopen,[1,0,2]),
  s^4*(3*hh+2*s)^2/(243*hh),
  "xy second factor G-open E3 square");
same(subst(xySecondC2,hh,-2/3*s),s,
  "xy F/B intersection C2");
same(subst(xyL7open,hh,-2/3*s),-C1*s/2,
  "xy F/B intersection l7");

\\ G=0: Res_h(G,s-h)=5s^2 makes s-h a unit on s!=0, so CompA
\\ forces C1=0.  The exact E4 and E3 quotients then give a contradiction.
same(polresultant(GG,s-hh,hh),5*s^2,
  "xy G=0 unit resultant");
xyE4gzero=put_many(xyE4res,[C2,C1],[xySecondC2,0]);
same(xyE4gzero,-2/9*s*GG*l7*x^3*z/hh,
  "xy G=0 complete E4 factorization");
xyE3gzero=put_many(xyE3base,[C2,C1],[xySecondC2,0]);
same(cxyz(xyE3gzero,[1,0,2]),
  s^4*(3*hh+2*s)^2/(243*hh),
  "xy G=0 E3 square");
same((3*hh+2*s)^2-3*GG,-2*s*(s-6*hh),
  "xy G=0 E3 remainder identity");
same(subst(GG,s,6*hh),75*hh^2,
  "xy G=0 terminal contradiction");

print("PASS xy axis: h=0, both E4 factors, G split, and every intersection close");
print("ALL EXTERNAL PARI A=0 HOSTILE CHECKS PASSED");
quit(0);
}
