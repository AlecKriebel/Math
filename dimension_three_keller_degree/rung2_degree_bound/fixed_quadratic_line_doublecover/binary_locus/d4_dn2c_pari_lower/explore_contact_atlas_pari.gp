\\ Direct PARI/GP reconstruction of the D4-DN-2C E7 kernel and E6 contact
\\ projection.  No eliminant or table is imported from another program.

p='p; q='q; r='r; w='w;
coords=[p,q,r];
jacmat(H)=matrix(3,3,i,j,deriv(H[i],coords[j]));
c3(f,ip,iq,ir)=polcoeff(polcoeff(polcoeff(f,ir,r),iq,q),ip,p);
check_zero(value,message)={if(value!=0,print(Str("FAIL: ",message,"; residual = ",value));quit(1))};
check_true(value,message)={if(!value,print(Str("FAIL: ",message));quit(1))};

\\ Raw top forms.
h=(p+q)^2;
P=h*p^2;
Q=h*q^2;
R=h*(p-2*q);
alpha=deriv(Q,p)*deriv(R,q)-deriv(Q,q)*deriv(R,p);
beta=-(deriv(P,p)*deriv(R,q)-deriv(P,q)*deriv(R,p));
gam0=deriv(P,p)*deriv(Q,q)-deriv(P,q)*deriv(Q,p);
check_zero(alpha+6*p*q*(p+q)^3,"raw alpha");
check_zero(beta-6*p*(p+q)^3*(p+2*q),"raw beta");
check_zero(gam0-8*p*q*(p+q)^4,"raw gamma");

\\ ----------------------------------------------------------------------
\\ Raw E7 block matrices.
\\ ----------------------------------------------------------------------

ru3='ru3; rv3='rv3;
up2='up2; uq2='uq2; vp2='vp2; vq2='vq2; tt2='tt2;
up20='up20; upq0='upq0; uq20='uq20;
vp20='vp20; vpq0='vpq0; vq20='vq20; tp0='tp0; tq0='tq0;

rawU=ru3*r^3+r^2*(up2*p+uq2*q)+r*(up20*p^2+upq0*p*q+uq20*q^2);
rawV=rv3*r^3+r^2*(vp2*p+vq2*q)+r*(vp20*p^2+vpq0*p*q+vq20*q^2);
rawT=tt2*r^2+r*(tp0*p+tq0*q);
rawE7=alpha*deriv(rawU,r)+beta*deriv(rawV,r)+gam0*deriv(rawT,r);
rawE7=rawE7/(2*p*(p+q)^3);

vars72=[ru3,rv3];
eq72=vector(2,i,c3(rawE7,i-1,1-(i-1),2));
M72=matrix(#eq72,#vars72,i,j,polcoeff(eq72[i],1,vars72[j]));
check_true(matrank(M72)==2,"E7 r^2 block rank two");

vars71=[up2,uq2,vp2,vq2,tt2];
eq71=vector(3,i,c3(rawE7,i-1,2-(i-1),1));
M71=matrix(#eq71,#vars71,i,j,polcoeff(eq71[i],1,vars71[j]));
check_true(matrank(M71)==3,"E7 r^1 block rank three");

vars70=[up20,upq0,uq20,vp20,vpq0,vq20,tp0,tq0];
eq70=vector(4,i,c3(rawE7,i-1,3-(i-1),0));
M70=matrix(#eq70,#vars70,i,j,polcoeff(eq70[i],1,vars70[j]));
check_true(matrank(M70)==4,"E7 r^0 block rank four");

\\ Verify an explicit six-parameter kernel whose dimension equals the raw
\\ nullity 0+2+4.
cd='cd; cz='cz; ca='ca; cb='cb; cx='cx; cy='cy;
U2=(cd+4*cz/3)*p+(2*cd+4*cz/3)*q;
V2=cd*q;
T2=cz;
U1=(cx+4*ca/3)*p^2+(cy+2*cx+4*(ca+cb)/3)*p*q+(2*cy+4*cb/3)*q^2;
V1=cx*p*q+cy*q^2;
T1=ca*p+cb*q;
paramE7=alpha*deriv(r^2*U2+r*U1,r)+beta*deriv(r^2*V2+r*V1,r)+gam0*deriv(r^2*T2+r*T1,r);
check_zero(paramE7,"six-parameter E7 kernel");
paramvars=[cd,cz,ca,cb,cx,cy];
paramcoeffs=[cd+4*cz/3,2*cd+4*cz/3,cd,cz,cx+4*ca/3,cy+2*cx+4*(ca+cb)/3,2*cy+4*cb/3,cx,cy,ca,cb];
Pmat=matrix(#paramcoeffs,#paramvars,i,j,polcoeff(paramcoeffs[i],1,paramvars[j]));
check_true(matrank(Pmat)==6,"six E7 parameters independent");
print("D4_DN2C_PARI_E7_KERNEL_PASS_0_2_4");

\\ ----------------------------------------------------------------------
\\ Full determinant with all lower variables.
\\ ----------------------------------------------------------------------

u0='u0; u1='u1; u2='u2; u3='u3;
v0='v0; v1='v1; v2='v2; v3='v3;
t0='t0; t1='t1; t2='t2;
a0='a0; a1='a1; a2='a2; a3='a3; a4='a4; a5='a5;
b0='b0; b1='b1; b2='b2; b3='b3; b4='b4; b5='b5;
l0='l0; l1='l1; l2='l2; l3='l3; l4='l4; l5='l5;
l6='l6; l7='l7; l8='l8;

U0=u0*p^3+u1*p^2*q+u2*p*q^2+u3*q^3;
V0=v0*p^3+v1*p^2*q+v2*p*q^2+v3*q^3;
T0=t0*p^2+t1*p*q+t2*q^2;
A=a0*p^2+a1*p*q+a2*p*r+a3*q^2+a4*q*r+a5*r^2;
B=b0*p^2+b1*p*q+b2*p*r+b3*q^2+b4*q*r+b5*r^2;
L=[l0,l1,l2;l3,l4,l5;l6,l7,l8];
H4=[P,Q,0]~;
H3=[U0+r*U1+r^2*U2,V0+r*V1+r^2*V2,R]~;
H2=[A,B,T0+r*T1+r^2*T2]~;
D=matdet(L+w*jacmat(H2)+w^2*jacmat(H3)+w^3*jacmat(H4));
check_zero(polcoeff(D,7,w),"parameterized E7 in literal determinant");
E6=polcoeff(D,6,w);

check_zero(c3(E6,3,0,3)+6*cd^2,"E6 p^3 r^3");
check_zero(c3(E6,2,1,3)-16*cz*(3*cd+cz)/3,"E6 p^2 q r^3");
check_zero(c3(E6,1,2,3)-2*(3*cd+4*cz)*(9*cd+4*cz)/3,"E6 p q^2 r^3");
check_zero(c3(E6,0,3,3)-4*(3*cd+2*cz)^2/3,"E6 q^3 r^3");

\\ From this point cd=cz=0 is forced set-theoretically.
E60=substvec(E6,[cd,cz],[0,0]);
contact=[ca,cb,cx,cy];

\\ Only a5,b5 occur in the six r-linear equations.
eq61=vector(6,i,c3(E60,i-1,5-(i-1),1));
rrvars=[a5,b5];
M61=matrix(6,2,i,j,polcoeff(eq61[i],1,rrvars[j]));
rhs61=matrix(6,1,i,j,-substvec(eq61[i],rrvars,[0,0]));
for(i=1,#eq61,check_zero(eq61[i]-(M61*rrvars~)[i]+rhs61[i,1],Str("E6 r-linear reconstruction row ",i)));
M61expected=[0,0;-12,24;-36,84;-36,108;-12,60;0,12];
check_true(M61==M61expected,"contact coefficient matrix reconstructed");
check_true(matrank(M61)==2,"contact coefficient matrix rank two");
trialrows=[2,6];
trialpivot=matdet(vecextract(M61,trialrows,[1,2]));
check_true(trialpivot==-144,"contact solve pivot");
sol61=matsolve(vecextract(M61,trialrows,[1,2]),vecextract(rhs61,trialrows,[1]));
sol61v=[sol61[1,1],sol61[2,1]];
res61=vector(6,i,substvec(eq61[i],rrvars,sol61v));

gcontact=2*cb+3*cy;
fcontact=8*ca^2-16*ca*cb+24*ca*cx-24*ca*cy-24*cb*cx+27*cx^2-54*cx*cy+9*cy^2;
fcontact0=subst(fcontact,cb,-3*cy/2);
check_zero(res61[1]-2*gcontact^2/3,"contact doubled hyperplane");
check_zero(res61[2],"contact solved-row residual 2");
check_zero(res61[6],"contact solved-row residual 6");
check_zero(subst(res61[3],cb,-3*cy/2)-fcontact0/3,"contact quadratic residual 3");
check_zero(subst(res61[4],cb,-3*cy/2)-2*fcontact0/3,"contact quadratic residual 4");
check_zero(subst(res61[5],cb,-3*cy/2)-fcontact0/3,"contact quadratic residual 5");

\\ Thus the reduced contact locus is gcontact=fcontact=0.  Over
\\ Q(eta), eta^2=-2, the quadratic splits into two distinct hyperplanes.
ee='ee;
et=Mod(ee,ee^2+2);
ellplus=9*cx+(4+2*et)*ca+(-3+3*et)*cy;
ellminus=9*cx+(4-2*et)*ca+(-3-3*et)*cy;
check_zero(ellplus*ellminus-3*fcontact0,"contact quadratic conjugate split");
check_true(ellplus!=ellminus,"contact hyperplanes distinct");

k='k; s='s;
xplus=(-(4+2*et)*k+(3-3*et)*s)/9;
xminus=(-(4-2*et)*k+(3+3*et)*s)/9;
pluscontact=[k,-3*s/2,xplus,s];
minuscontact=[k,-3*s/2,xminus,s];
linecontact=[k,k,-2*k/3,-2*k/3];
check_zero(substvec(gcontact,contact,pluscontact),"plus plane satisfies g");
check_zero(substvec(ellplus,contact,pluscontact),"plus plane satisfies ellplus");
check_zero(substvec(gcontact,contact,minuscontact),"minus plane satisfies g");
check_zero(substvec(ellminus,contact,minuscontact),"minus plane satisfies ellminus");
delta=2*k+3*s;
check_zero(xplus-xminus+2*et*delta/9,"two planes meet exactly on delta zero");
for(i=1,4,check_zero(subst(pluscontact[i],s,-2*k/3)-linecontact[i],Str("plus-line contact coordinate ",i)));
for(i=1,4,check_zero(subst(minuscontact[i],s,-2*k/3)-linecontact[i],Str("minus-line contact coordinate ",i)));
for(i=1,4,check_zero(subst(linecontact[i],k,0),Str("line-origin contact coordinate ",i)));
for(i=1,6,check_zero(substvec(res61[i],contact,pluscontact),Str("plus contact compatibility ",i)));
for(i=1,6,check_zero(substvec(res61[i],contact,minuscontact),Str("minus contact compatibility ",i)));
print("D4_DN2C_PARI_E6_RADICAL_TWO_PLANES_PASS");

\\ The complete post-contact E6 polynomial has exactly the six r-linear
\\ and seven binary coefficients below.  This literal reconstruction
\\ prevents an omitted monomial or boundary equation.
eq60=vector(7,i,c3(E60,i-1,6-(i-1),0));
eq13=concat(eq61,eq60);
E60recon=sum(i=1,6,eq61[i]*p^(i-1)*q^(6-i)*r)+sum(i=1,7,eq60[i]*p^(i-1)*q^(7-i));
check_zero(E60-E60recon,"complete 13-coefficient E6 census");
low18=[a2,a4,a5,b2,b4,b5,l8,u0,u1,u2,u3,v0,v1,v2,v3,t0,t1,t2];
check_true(#low18==18 && #Set(low18)==18,"all 18 lower variables listed distinctly");

eqplus=vector(13,i,substvec(eq13[i],contact,pluscontact));
Mplus=matrix(13,18,i,j,polcoeff(eqplus[i],1,low18[j]));
eqminus=vector(13,i,substvec(eq13[i],contact,minuscontact));
Mminus=matrix(13,18,i,j,polcoeff(eqminus[i],1,low18[j]));
eqline=vector(13,i,substvec(eq13[i],contact,linecontact));
Mline=matrix(13,18,i,j,polcoeff(eqline[i],1,low18[j]));
eqorigin=vector(13,i,substvec(eq13[i],contact,[0,0,0,0]));
Morigin=matrix(13,18,i,j,polcoeff(eqorigin[i],1,low18[j]));

rowsplus=[2,3,8,9,10,11,12]; colsplus=[1,2,3,4,6,8,9];
rowsline=[2,3,8,9,10,11]; colsline=[1,2,3,4,6,8];
rowsorigin=[2,3,8,9,10]; colsorigin=[1,2,3,4,6];
check_true(matrank(Mplus)==7,"plus-plane full E6 rank seven");
check_true(matrank(Mminus)==7,"minus-plane full E6 rank seven");
check_true(matrank(Mline)==6,"intersection-line full E6 rank six");
check_true(matrank(Morigin)==5,"origin full E6 rank five");
check_zero(matdet(vecextract(Mplus,rowsplus,colsplus))-93312*(et-1)*delta^2,"plus-plane exact pivot");
check_zero(matdet(vecextract(Mminus,rowsplus,colsplus))+93312*(et+1)*delta^2,"minus-plane exact pivot");
check_zero(matdet(vecextract(Mline,rowsline,colsline))-186624*k,"intersection-line exact pivot");
check_zero(matdet(vecextract(Morigin,rowsorigin,colsorigin))+31104,"origin exact pivot");
for(j=1,18,check_true(sum(i=1,13,if(Mplus[i,j]!=0,1,0))>0,Str("generic contact matrix retains lower column ",j)));

certify_chart(eqs,MM,rows,cols,label)=
{
  my(nr=#eqs,nv=#low18,zero18,rhs,recon,piv,sol,xsol,res);
  zero18=vector(nv,i,0);
  rhs=vector(nr,i,-substvec(eqs[i],low18,zero18))~;
  recon=MM*low18~;
  for(i=1,nr,check_zero(eqs[i]-recon[i]+rhs[i],Str(label," linear reconstruction row ",i)));
  piv=vecextract(MM,rows,cols);
  sol=matsolve(piv,vecextract(rhs,rows));
  xsol=vector(nv,i,0);
  for(j=1,#cols,xsol[cols[j]]=sol[j]);
  res=MM*xsol~-rhs;
  for(i=1,nr,check_zero(res[i],Str(label," full-system residual row ",i)));
  1
};
check_true(certify_chart(eqplus,Mplus,rowsplus,colsplus,"plus plane"),"plus-plane chart solve");
check_true(certify_chart(eqminus,Mminus,rowsplus,colsplus,"minus plane"),"minus-plane chart solve");
check_true(certify_chart(eqline,Mline,rowsline,colsline,"intersection line"),"intersection-line chart solve");
check_true(certify_chart(eqorigin,Morigin,rowsorigin,colsorigin,"origin"),"origin chart solve");

\\ The two plane charts with delta nonzero, their common line with k
\\ nonzero, and its k=0 origin are disjoint and exhaustive.
print("D4_DN2C_DIRECT_PARI_CONTACT_ATLAS_PASS");
quit(0);
