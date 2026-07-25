\\ Independent PARI/GP replay of the squarefree-interior two-contact leaf.

p='p; q='q; r='r; z='z;
vars=[p,q,r];
jacmat(H)=matrix(3,3,i,j,deriv(H[i],vars[j]));
jac2(f,g)=deriv(f,p)*deriv(g,q)-deriv(f,q)*deriv(g,p);
check_zero(value,message)={if(value!=0,error(Str("FAIL: ",message,"; residual = ",value)))};
hc(f,degree,index)=polcoeff(subst(f,q,1),degree-index,p);
cv(f,degree)=vector(degree+1,index,hc(f,degree,index-1));

contact_column_case(Pc,Qc,Rc,Nc,xvalue,yvalue)={
  my(H4c,H3c,H2c,Dc,E6rc);
  H4c=[Pc,Qc,0]~;
  H3c=[r*Nc[1],r*Nc[2],Rc]~;
  H2c=[xvalue*r^2,yvalue*r^2,r*Nc[3]]~;
  Dc=matdet(z*jacmat(H2c)+z^2*jacmat(H3c)+z^3*jacmat(H4c));
  check_zero(polcoeff(Dc,7,z),"E7 determinant");
  E6rc=polcoeff(polcoeff(Dc,6,z),1,r);
  cv(E6rc,5)
};

contact_matrix_case(Pc,Qc,Rc,Nfirst,Nsecond)={
  my(zeroN,colX,colY,colZ,colx,coly);
  zeroN=[0,0,0];
  colX=contact_column_case(Pc,Qc,Rc,Nfirst,0,0);
  colZ=contact_column_case(Pc,Qc,Rc,Nsecond,0,0);
  colY=contact_column_case(Pc,Qc,Rc,Nfirst+Nsecond,0,0)-colX-colZ;
  colx=contact_column_case(Pc,Qc,Rc,zeroN,1,0);
  coly=contact_column_case(Pc,Qc,Rc,zeroN,0,1);
  matrix(6,5,i,j,[colX,colY,colZ,colx,coly][j][i])
};

tangent_from_vector(v)={
  [
    v[1]*p^2+v[2]*p*q+v[3]*q^2,
    v[4]*p^2+v[5]*p*q+v[6]*q^2,
    v[7]*p+v[8]*q
  ]
};

ww='ww; aa='aa; c1='c1; c2='c2; x5='x5; y5='y5;
u=ww^2;
L=p-ww*q; Mfix=ww*p-q; h=L*Mfix;
P=h*p^2; Q=h*q^2;
R=4*ww*aa*p^3-3*(1+u)*aa*p^2*q-3*(1+u)*p*q^2+4*ww*q^3;
alpha=jac2(Q,R); beta=-jac2(P,R); gam=jac2(P,Q);
check_zero(gcd(gcd(alpha,beta),gam)^2-(p*q)^2,"generic gcd");

EL=aa*ww^3-3*aa*ww-3*u+1;
EM=-3*aa*u+aa+ww^3-3*ww;
km=u-4*ww+1; kp=u+4*ww+1;
Bpivot=16*aa^2*ww^7+48*aa^2*ww^5+48*aa^2*ww^3+16*aa^2*ww+3*aa*ww^8+108*aa*ww^6-46*aa*ww^4+108*aa*ww^2+3*aa+16*ww^7+48*ww^5+48*ww^3+16*ww;
b=-36*ww^5-8*ww^3-36*ww;
c=7*ww^6-27*ww^4-27*ww^2+7;
K1=aa*b+c; K2=aa*c+b;
Sminus=c+b; Splus=c-b;
check_zero(polresultant(K1,K2,aa)+Sminus*Splus,"K1,K2 resultant");
check_zero(content(Sminus)-1,"Sminus primitive");
check_zero(content(Splus)-1,"Splus primitive");
check_zero(polisirreducible(Sminus)-1,"Sminus irreducible");
check_zero(polisirreducible(Splus)-1,"Splus irreducible");

mons=[p^2,p*q,q^2,p^2,p*q,q^2,p,q];
columns7=vector(8,index,if(index<=3,alpha*mons[index],if(index<=6,beta*mons[index],gam*mons[index])));
M7=matrix(8,8,i,j,hc(columns7[j],7,i-1));
generic_rows=[2,3,4,5,6,7];
generic_pivots=[1,2,3,4,5,6];
Mp=vecextract(M7,generic_rows,generic_pivots);
check_zero(matdet(Mp)-5832*(ww-1)^2*(ww+1)^2*EL^2*EM^2*Bpivot,"generic E7 pivot");
generic_basis=vector(2,index,{
  my(freecol,solution,v,scale);
  freecol=6+index;
  solution=matsolve(Mp,-vecextract(M7,generic_rows,[freecol]));
  scale=3*Bpivot;
  v=vector(8,j,if(j<=6,scale*solution[j,1],if(j==freecol,scale,0)));
  v
});
N1=tangent_from_vector(generic_basis[1]);
N2=tangent_from_vector(generic_basis[2]);
for(index=1,2,check_zero(alpha*[N1,N2][index][1]+beta*[N1,N2][index][2]+gam*[N1,N2][index][3],Str("generic tangent ",index)));
Mc=contact_matrix_case(P,Q,R,N1,N2);
minors=vector(6,omit,matdet(vecextract(Mc,vector(5,j,if(j<omit,j,j+1)),[1,2,3,4,5])));
base=248832*ww^2*(u+1)*km*kp*Bpivot^3;
Qres=vector(6);
Qres[1]=minors[1]/(base*K1);
for(index=2,5,Qres[index]=minors[index]/(-base*ww^2*K1*K2));
Qres[6]=minors[6]/(base*K2);
for(index=1,6,if(denominator(Qres[index])!=1,error(Str("FAIL: nonpolynomial Q",index))));
Qpair=vector(5,index,polresultant(Qres[1],Qres[index+1],aa));
Qgcd=Qpair[1];
for(index=2,5,Qgcd=gcd(Qgcd,Qpair[index]));
W4=5*ww^4-6*ww^2+5;
expectedQgcd=ww^6*(ww-1)^8*(ww+1)^8*(u+1)^5*km^4*kp^4*W4^2;
check_zero(Qgcd-expectedQgcd,"common Q resultant gcd");
print("PASS PARI generic contact-resultant stratification");

alternate_pivots=[1,2,3,6,7,8];
alternate_free=[4,5];
Mpa=vecextract(M7,generic_rows,alternate_pivots);
check_zero(matdet(Mpa)-10368*ww^3*(ww-1)^2*(ww+1)^2*(u+1)*EL^2*EM^2,"alternate E7 pivot");
alternate_basis=vector(2,index,{
  my(freecol,solution,v);
  freecol=alternate_free[index];
  solution=matsolve(Mpa,-vecextract(M7,generic_rows,[freecol]));
  v=vector(8,j,0);
  for(j=1,6,v[alternate_pivots[j]]=solution[j,1]);
  v[freecol]=1;
  v
});
Na1=tangent_from_vector(alternate_basis[1]);
Na2=tangent_from_vector(alternate_basis[2]);
Mca=contact_matrix_case(P,Q,R,Na1,Na2);
minorsa=vector(6,omit,matdet(vecextract(Mca,vector(5,j,if(j<omit,j,j+1)),[1,2,3,4,5])));
remainders=vector(6,index,numerator(divrem(numerator(minorsa[index],ww),Bpivot,aa)[2],ww));
Bresultants=vector(6,index,polresultant(Bpivot,remainders[index],aa));
Bgcd=Bresultants[1];
for(index=2,6,Bgcd=gcd(Bgcd,Bresultants[index]));
P16=385*ww^16+9992*ww^14-23012*ww^12+53560*ww^10-24250*ww^8+53560*ww^6-23012*ww^4+9992*ww^2+385;
expectedBgcd=59049*8192*ww*(u+1)^11*km^2*kp^2*W4^2*P16;
check_zero(Bgcd-expectedBgcd,"B=0 resultant gcd");
check_zero(content(P16)-1,"P16 primitive");
check_zero(polisirreducible(P16)-1,"P16 irreducible");
print("PASS PARI alternate contact-resultant stratification");

G8=7*ww^8-156*ww^6+66*ww^4-12*ww^2+15;
H8=15*ww^8-12*ww^6+66*ww^4-156*ww^2+7;
den8=4*(3*u-4*ww+3)*(3*u+4*ww+3);
check_zero(subst(EL,aa,-c/b)-G8/den8,"K1 octic EL boundary");
check_zero(subst(EM,aa,-c/b)-H8/(ww*den8),"K1 octic EM boundary");

tt='tt;
wc=Mod(tt,tt^2+1);
gminus=1;
for(index=1,6,gminus=gcd(gminus*subst(Qres[index],ww,wc),subst(Qres[index],ww,wc)));
\\ Restart without the harmless initial unit.
gminus=subst(Qres[1],ww,wc);
for(index=2,6,gminus=gcd(gminus,subst(Qres[index],ww,wc)));
gminus=gminus/pollead(gminus,aa);
check_zero(gminus-(aa^2+1),"u=-1 common Q gcd");
check_zero(subst(subst(EL,ww,wc),aa,-wc),"u=-1 EL route");
check_zero(subst(subst(EM,ww,wc),aa,wc),"u=-1 EM route");

wc4=Mod(tt,5*tt^4-6*tt^2+5);
gquartic=subst(Qres[1],ww,wc4);
for(index=2,6,gquartic=gcd(gquartic,subst(Qres[index],ww,wc4)));
gquartic=gquartic/pollead(gquartic,aa);
quarticcommon=aa^2+(-5*wc4^3+11*wc4)*aa/10+1;
check_zero(gquartic-quarticcommon,"W4 common Q gcd");
aone=(3*wc4^2-5)/(4*wc4);
atwo=(3-5*wc4^2)/(4*wc4);
check_zero(subst(subst(EM,ww,wc4),aa,aone),"W4 EM route");
check_zero(subst(subst(EL,ww,wc4),aa,atwo),"W4 EL route");
print("PASS PARI exact octic/quartic/u=-1 boundary routing");

analyze_case(label,modulus,caseindex)={
  my(wc0,uc0,ac,Lc,Mcfix,hc0,Pc,Qc,Rc,alphac,betac,gamc,openvalues,columns,M7c,K7,Nfirst,Nsecond,Mcontact,rankcontact,Kcontact,f00,f01,f11,disc,constcols,Mconstant,Nspecial,liftcolumn,H4s,H3s,H2s,Dspecial);
  wc0=Mod(tt,modulus); uc0=wc0^2;
  ac=if(caseindex==1,1,if(caseindex==2,-1,if(caseindex==3,-wc0*(2626085*wc0^14+67753107*wc0^12-167139687*wc0^10+396647791*wc0^8-228766929*wc0^6+398117721*wc0^4-168036781*wc0^2+83754213)/14417920,0)));
  openvalues=[wc0,uc0-1,ac*wc0^3-3*ac*wc0-3*uc0+1,-3*ac*uc0+ac+wc0^3-3*wc0,uc0-4*wc0+1,uc0+4*wc0+1];
  for(index=1,#openvalues,if(openvalues[index]==0,error(Str("FAIL: ",label," exact open"))));
  Lc=p-wc0*q; Mcfix=wc0*p-q; hc0=Lc*Mcfix;
  Pc=hc0*p^2; Qc=hc0*q^2;
  Rc=4*wc0*ac*p^3-3*(1+uc0)*ac*p^2*q-3*(1+uc0)*p*q^2+4*wc0*q^3;
  alphac=jac2(Qc,Rc); betac=-jac2(Pc,Rc); gamc=jac2(Pc,Qc);
  columns=vector(8,index,if(index<=3,alphac*mons[index],if(index<=6,betac*mons[index],gamc*mons[index])));
  M7c=matrix(8,8,i,j,hc(columns[j],7,i-1));
  if(matrank(M7c)!=6,error(Str("FAIL: ",label," E7 rank")));
  K7=matker(M7c);
  if(matsize(K7)[2]!=2,error(Str("FAIL: ",label," E7 nullity")));
  Nfirst=tangent_from_vector(K7[,1]);
  Nsecond=tangent_from_vector(K7[,2]);
  Mcontact=contact_matrix_case(Pc,Qc,Rc,Nfirst,Nsecond);
  rankcontact=matrank(Mcontact);
  if(caseindex<=2&&rankcontact!=4,error(Str("FAIL: ",label," rank 4")));
  if(caseindex==3&&rankcontact!=5,error(Str("FAIL: ",label," rank 5")));
  if(caseindex==4&&rankcontact!=3,error(Str("FAIL: ",label," rank 3")));
  if(rankcontact==4,Kcontact=matker(Mcontact));
  if(rankcontact==4&&matsize(Kcontact)[2]!=1,error(Str("FAIL: ",label," contact nullity")));
  if(rankcontact==4&&Kcontact[2,1]^2-Kcontact[1,1]*Kcontact[3,1]==0,error(Str("FAIL: ",label," Veronese kernel")));
  if(rankcontact==3,Kcontact=matker(Mcontact));
  if(rankcontact==3&&matsize(Kcontact)[2]!=2,error(Str("FAIL: ",label," contact nullity")));
  if(rankcontact==3,f00=Kcontact[2,1]^2-Kcontact[1,1]*Kcontact[3,1]);
  if(rankcontact==3,f01=2*Kcontact[2,1]*Kcontact[2,2]-Kcontact[1,1]*Kcontact[3,2]-Kcontact[1,2]*Kcontact[3,1]);
  if(rankcontact==3,f11=Kcontact[2,2]^2-Kcontact[1,2]*Kcontact[3,2]);
  if(rankcontact==3,disc=f01^2-4*f00*f11);
  if(rankcontact==3,check_zero(disc,Str(label," restricted Veronese discriminant")));
  if(rankcontact==3&&f00==0&&f01==0&&f11==0,error(Str("FAIL: ",label," whole kernel Veronese")));
  if(rankcontact==3,Nspecial=[2*p^2+q^2,q^2,0]);
  if(rankcontact==3,check_zero(alphac*Nspecial[1]+betac*Nspecial[2],"special E7 tangent"));
  if(rankcontact==3,liftcolumn=contact_column_case(Pc,Qc,Rc,Nspecial,-wc0,0));
  if(rankcontact==3,check_zero(liftcolumn,"special E6 lift"));
  if(rankcontact==3,H4s=[Pc,Qc,0]~);
  if(rankcontact==3,H3s=[r*Nspecial[1],r*Nspecial[2],Rc]~);
  if(rankcontact==3,H2s=[-wc0*r^2,0,0]~);
  if(rankcontact==3,Dspecial=matdet(z*jacmat(H2s)+z^2*jacmat(H3s)+z^3*jacmat(H4s)));
  if(rankcontact==3,check_zero(polcoeff(polcoeff(Dspecial,5,z),2,r),"special top-only E5"));
  constcols=[alphac*p,alphac*q,betac*p,betac*q,gamc];
  Mconstant=matrix(7,5,i,j,hc(constcols[j],6,i-1));
  if(matrank(Mconstant)!=5,error(Str("FAIL: ",label," constant rank")));
  print("PASS PARI ",label," E7/contact/constant pivots")
};

analyze_case("K1=K2,a=1",subst(Sminus,ww,tt),1);
analyze_case("K1=K2,a=-1",subst(Splus,ww,tt),2);
analyze_case("B=0,P16",subst(P16,ww,tt),3);
analyze_case("B=0,u=-1,a=0",tt^2+1,4);

\\ Full lower replay on the unique u=-1,a=0 Veronese lift.
U0='U0; U1='U1; U2='U2; U3='U3;
V0='V0; V1='V1; V2='V2; V3='V3;
T0='T0; T1='T1; T2='T2;
X0='X0; X1='X1; X2='X2; X3='X3; X4='X4;
Y0='Y0; Y1='Y1; Y2='Y2; Y3='Y3; Y4='Y4;
L00='L00; L01='L01; L02='L02;
L10='L10; L11='L11; L12='L12;
L20='L20; L21='L21; L22='L22;
w0=Mod(tt,tt^2+1);
H4low=[w0*(p^2+q^2)*p^2,w0*(p^2+q^2)*q^2,0]~;
H3low=[U0*p^3+U1*p^2*q+U2*p*q^2+U3*q^3+r*(2*p^2+q^2),V0*p^3+V1*p^2*q+V2*p*q^2+V3*q^3+r*q^2,4*w0*q^3]~;
H2low=[X0*p^2+X1*p*q+X2*q^2+r*(X3*p+X4*q)-w0*r^2,Y0*p^2+Y1*p*q+Y2*q^2+r*(Y3*p+Y4*q),T0*p^2+T1*p*q+T2*q^2]~;
Llow=[L00,L01,L02;L10,L11,L12;L20,L21,L22];
Dlow=matdet(Llow+z*jacmat(H2low)+z^2*jacmat(H3low)+z^3*jacmat(H4low));
Elow=vector(9,index,polcoeff(Dlow,index-1,z));
check_zero(Elow[9],"lower E8");
check_zero(Elow[8],"lower E7");

unknown6=[X3,X4,Y3,Y4,L22,T1];
eq6=cv(Elow[7],6);
M6=matrix(7,6,i,j,polcoeff(lift(eq6[i]),1,unknown6[j]));
if(matrank(M6)!=6,error("FAIL: lower E6 rank"));
sol6=[-3*w0*U0/2+3*w0*U2/4+w0*V2/4,-w0*U1,-w0*U2/4-3*w0*V0/2+w0*V2/4,-w0*V1,-w0*T0,-3*U2+3*V2];
E6done=substvec(Elow[7],unknown6,sol6);
check_zero(E6done,"full lower E6 solution");

E5after=substvec(Elow[6],unknown6,sol6);
expectedE5r=18*q^2*(p^2*(U2+2*V0-V2)+q^2*(-U0+2*U2+V0));
check_zero(polcoeff(E5after,1,r)-expectedE5r,"full lower E5 r coefficient");
highvars=[U0,V2];
highvals=[2*U2+V0,U2+2*V0];
E5constant=substvec(polcoeff(E5after,0,r),highvars,highvals);
eq5=cv(E5constant,5);
unknown5=[L02,L12,L20];
M5=matrix(6,3,i,j,polcoeff(lift(eq5[i]),1,unknown5[j]));
rhs5=-vector(6,i,lift(substvec(eq5[i],unknown5,[0,0,0])))~;
if(matrank(M5)!=3,error("FAIL: lower E5 selected rank"));
pivotrows=[2,3,5];
sol5=matsolve(vecextract(M5,pivotrows,[1,2,3]),vecextract(rhs5,pivotrows));
res5=M5*sol5-rhs5;
expectedres5=[12*V0^2,0,0,24*w0*(-w0*U1*V0/4+w0*U2*V1-3*w0*V0*V1/4+3*w0*V0*V3/2+Y1),0,-12*w0*(w0*U1*U2-w0*U2*V1+3*w0*U3*V0/2+w0*V0*V1-3*w0*V0*V3/2+X1-Y1)]~;
check_zero(res5-lift(expectedres5),"full lower E5 compatibility vector");

e5vars=[U0,V0,V2,X1,Y1,L02,L12,L20];
e5vals=[2*U2,0,U2,-w0*U1*U2,-w0*U2*V1,U2^2-w0*X0,-w0*Y0,-w0*T0*U2];
E5done=substvec(E5after,e5vars,e5vals);
check_zero(E5done,"full lower E5 solution");

E4after=substvec(substvec(Elow[5],unknown6,sol6),e5vars,e5vals);
expectedE4=12*q^2*(-w0*L00*q^2+2*w0*L10*p^2+w0*L10*q^2-2*p^2*U2*Y0+w0*q^2*U2^3+q^2*U2*X0-q^2*U2*Y0);
check_zero(E4after-expectedE4,"full lower E4 formula");
e4vars=[L10,L00];
e4vals=[-w0*U2*Y0,U2^3-w0*U2*X0];
check_zero(substvec(E4after,e4vars,e4vals),"full lower E4 solution");

for(degree=1,3,check_zero(substvec(substvec(substvec(Elow[degree+1],unknown6,sol6),e5vars,e5vals),e4vars,e4vals),Str("full lower E",degree)));
Ldone=substvec(substvec(substvec(Llow,unknown6,sol6),e5vars,e5vals),e4vars,e4vals);
check_zero(Ldone[,1]-U2*Ldone[,3],"forced proportional L columns");
check_zero(matdet(Ldone),"forced singular L");
print("PASS PARI full lower chain forces col_1(L)=U2 col_3(L)");
print("ALL PARI INTERIOR TWO-CONTACT {1,1} CHECKS PASSED");
