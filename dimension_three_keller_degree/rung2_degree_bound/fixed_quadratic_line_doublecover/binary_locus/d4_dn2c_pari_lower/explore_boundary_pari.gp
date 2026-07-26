\\ Clean-room PARI/GP probe of the D4-DN-2C common-line and origin charts.
\\ The determinant is rebuilt directly from the frozen contact atlas.

p='p; q='q; r='r; w='w; k='k;
coords=[p,q,r];
jacmat(H)=matrix(3,3,i,j,deriv(H[i],coords[j]));
c3(f,ip,iq,ir)=polcoeff(polcoeff(polcoeff(f,ir,r),iq,q),ip,p);
check_zero(value,message)={if(value!=0,print(Str("FAIL: ",message,"; residual = ",value));quit(1))};
check_true(value,message)={if(!value,print(Str("FAIL: ",message));quit(1))};

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

h=(p+q)^2;
P=h*p^2;
Q=h*q^2;
R=h*(p-2*q);
H4=[P,Q,0]~;

build_det(scale)=
{
  my(U1=2*scale*p*(p+q)/3);
  my(V1=-2*scale*q*(p+q)/3);
  my(T1=scale*(p+q));
  my(H3=[U0+r*U1,V0+r*V1,R]~);
  my(H2=[A,B,T0+r*T1]~);
  matdet(L+w*jacmat(H2)+w^2*jacmat(H3)+w^3*jacmat(H4))
};

D=build_det(k);
check_zero(polcoeff(D,9,w),"intersection E9");
check_zero(polcoeff(D,8,w),"intersection E8");
check_zero(polcoeff(D,7,w),"intersection E7");
E6=polcoeff(D,6,w);
E5=polcoeff(D,5,w);
E4=polcoeff(D,4,w);
E3=polcoeff(D,3,w);

low=[a2,a4,a5,b2,b4,b5,l8,u0,u1,u2,u3,v0,v1,v2,v3,t0,t1,t2];
zeros=vector(#low);
exps6=[[6,0,0],[5,1,0],[5,0,1],[4,2,0],[4,1,1],[3,3,0],[3,2,1],[2,4,0],[2,3,1],[1,5,0],[1,4,1],[0,6,0],[0,5,1]];
eq6=vector(#exps6,i,c3(E6,exps6[i][1],exps6[i][2],exps6[i][3]));
M6=matrix(#eq6,#low,i,j,polcoeff(eq6[i],1,low[j]));
rhs6=matrix(#eq6,1,i,j,-substvec(eq6[i],low,zeros));
for(i=1,#eq6,check_zero(eq6[i]-(M6*low~)[i]+rhs6[i,1],Str("intersection E6 linear row ",i)));

rows6=[1,2,3,4,5,6];
cols6=[1,2,3,4,6,8];
freecols6=[5,7,9,10,11,12,13,14,15,16,17,18];
M6p=vecextract(M6,rows6,cols6);
check_zero(matdet(M6p)-186624*k,"intersection frozen E6 pivot");
check_true(matrank(M6)==6,"intersection E6 rank six");
check_true(matrank(matconcat([M6,rhs6]))==6,"intersection E6 augmented rank six");
pivvars6=vecextract(low,cols6);
freevars6=vecextract(low,freecols6);
rhsrows6=vector(#rows6,i,rhs6[rows6[i],1])~;
sol6=matsolve(M6p,rhsrows6-vecextract(M6,rows6,freecols6)*freevars6~);
for(i=1,#eq6,check_zero(substvec(eq6[i],pivvars6,Vec(sol6)),Str("intersection E6 residual row ",i)));

E5s=substvec(E5,pivvars6,Vec(sol6));
E4s=substvec(E4,pivvars6,Vec(sol6));

print("DN2C_INTERSECTION_E5_R2_BEGIN");
for(ip=0,3,{iq=3-ip;value=c3(E5s,ip,iq,2);if(value!=0,print(Str("[",ip,",",iq,",2] ",value)))});
print("DN2C_INTERSECTION_E5_R1_BEGIN");
for(ip=0,4,{iq=4-ip;value=c3(E5s,ip,iq,1);if(value!=0,print(Str("[",ip,",",iq,",1] ",value)))});

eq51=vector(4,i,c3(E5s,i,4-i,1));
M51=matrix(4,#freevars6,i,j,polcoeff(eq51[i],1,freevars6[j]));
rhs51=matrix(4,1,i,j,-substvec(eq51[i],freevars6,vector(#freevars6)));
for(i=1,#eq51,check_zero(eq51[i]-(M51*freevars6~)[i]+rhs51[i,1],Str("intersection E5 r-linear reconstruction row ",i)));
print(Str("DN2C_INTERSECTION_E5_R1_RANK ",matrank(M51)));
print(Str("DN2C_INTERSECTION_E5_R1_AUGMENTED_RANK ",matrank(matconcat([M51,rhs51]))));
trial51=[1,3,7,8];
print(Str("DN2C_INTERSECTION_E5_R1_TRIAL_PIVOT ",matdet(vecextract(M51,[1,2,3,4],trial51))));
rows51=[1,4];
cols51=[1,3];
freecols51=[2,4,5,6,7,8,9,10,11,12];
M51p=vecextract(M51,rows51,cols51);
check_zero(matdet(M51p)+16*k^3/3,"intersection E5 r-linear safe pivot");
pivvars51=vecextract(freevars6,cols51);
freevars51=vecextract(freevars6,freecols51);
rhsrows51=vector(#rows51,i,rhs51[rows51[i],1])~;
sol51=matsolve(M51p,rhsrows51-vecextract(M51,rows51,freecols51)*freevars51~);
for(i=1,#eq51,check_zero(substvec(eq51[i],pivvars51,Vec(sol51)),Str("intersection E5 r-linear residual row ",i)));
E5_51=substvec(E5s,pivvars51,Vec(sol51));
E4_51=substvec(E4s,pivvars51,Vec(sol51));
print("DN2C_INTERSECTION_E5_BINARY_BEGIN");
for(ip=0,5,{iq=5-ip;value=c3(E5_51,ip,iq,0);if(value!=0,print(Str("[",ip,",",iq,",0] ",value)))});
print("DN2C_INTERSECTION_E4_R2_BEGIN");
for(ip=0,2,{iq=2-ip;value=c3(E4_51,ip,iq,2);if(value!=0,print(Str("[",ip,",",iq,",2] ",value)))});
print("DN2C_INTERSECTION_E4_R1_BEGIN");
for(ip=0,3,{iq=3-ip;value=c3(E4_51,ip,iq,1);if(value!=0,print(Str("[",ip,",",iq,",1] ",value)))});

eq50=vector(6,i,c3(E5_51,i-1,6-i,0));
vars50=[a0,a1,a3,b0,b1,b3,l2,l5,l6,l7];
M50=matrix(6,#vars50,i,j,polcoeff(eq50[i],1,vars50[j]));
rhs50=matrix(6,1,i,j,-substvec(eq50[i],vars50,vector(#vars50)));
for(i=1,#eq50,check_zero(eq50[i]-(M50*vars50~)[i]+rhs50[i,1],Str("intersection E5 binary reconstruction row ",i)));
print(Str("DN2C_INTERSECTION_E5_BINARY_RANK ",matrank(M50)));
print(Str("DN2C_INTERSECTION_E5_BINARY_AUGMENTED_RANK ",matrank(matconcat([M50,rhs50]))));
rows50=[2,3,4];
cols50=[1,2,4];
print(Str("DN2C_INTERSECTION_E5_BINARY_TRIAL_PIVOT ",matdet(vecextract(M50,rows50,cols50))));
check_zero(matdet(vecextract(M50,rows50,cols50))-32*k^3,"intersection E5 binary safe pivot");
freecols50=[3,5,6,7,8,9,10];
pivvars50=vecextract(vars50,cols50);
freevars50=vecextract(vars50,freecols50);
rhsrows50=vector(#rows50,i,rhs50[rows50[i],1])~;
sol50=matsolve(vecextract(M50,rows50,cols50),rhsrows50-vecextract(M50,rows50,freecols50)*freevars50~);
res50=vector(#eq50,i,substvec(eq50[i],pivvars50,Vec(sol50)));
print("DN2C_INTERSECTION_E5_BINARY_RESIDUALS_BEGIN");
for(i=1,#res50,print(Str(i," IS_ZERO ",res50[i]==0)));
E4_50=substvec(E4_51,pivvars50,Vec(sol50));
S=v0-v1+v2-v3;
check_zero(c3(E4_50,1,1,2)+2*k^3*S/3,"intersection E4 p q r^2 forces S");
check_zero(c3(E4_50,2,0,2)+2*k^3*S/3,"intersection E4 p^2 r^2 repeats S");
subSvars=[v0];
subSvals=[v1-v2+v3];
res50S=vector(#res50,i,substvec(res50[i],subSvars,subSvals));
print("DN2C_INTERSECTION_E5_AFTER_S_BEGIN");
for(i=1,#res50S,print(Str(i," ",res50S[i])));
Tdiff=t0-t1+t2;
Y=u2-3*u3/2-2*v2+3*v3-4*t1/3+4*t2/3;
Z=v1-2*v2+3*v3-2*t1/3+4*t2/3;
check_zero(res50S[2],"intersection E5 residual 2");
check_zero(res50S[3],"intersection E5 residual 3");
check_zero(res50S[4],"intersection E5 residual 4");
check_zero(res50S[5]+5*res50S[1]-16*k*Tdiff^2/9,"intersection E5 residual 5 square relation");
check_zero(res50S[6]+4*res50S[1]-16*k*Tdiff^2/9,"intersection E5 residual 6 square relation");
check_zero(res50S[1]-2*Y*(k*Z+2*l8),"intersection E5 residual 1 product");

subTvars=[t0];
subTvals=[t1-t2];
E4_ST=substvec(substvec(E4_50,subSvars,subSvals),subTvars,subTvals);

\\ First compatibility branch Y=0.
subYvars=[u2];
subYvals=[3*u3/2+2*v2-3*v3+4*t1/3-4*t2/3];
E4_Y=substvec(E4_ST,subYvars,subYvals);
print("DN2C_INTERSECTION_BRANCH_Y_E4_R1_BEGIN");
for(ip=0,3,{iq=3-ip;value=c3(E4_Y,ip,iq,1);if(value!=0,print(Str("[",ip,",",iq,",1] ",value)))});
check_zero(c3(E4_Y,0,3,1)-2*(k*Z+2*l8)^2/3,"intersection Y branch forces second E5 factor");

\\ Second compatibility branch k*Z+2*l8=0.  Since k!=0 on I*, solving
\\ for l8 does not remove an additional divisor.
subBvars=[l8];
subBvals=[-k*Z/2];
E4_B=substvec(E4_ST,subBvars,subBvals);
print("DN2C_INTERSECTION_BRANCH_B_E4_R1_BEGIN");
for(ip=0,3,{iq=3-ip;value=c3(E4_B,ip,iq,1);if(value!=0,print(Str("[",ip,",",iq,",1] ",value)))});

eq41B=vector(4,i,c3(E4_B,i-1,4-i,1));
vars41B=[b1,b3,l5,l6,l7];
M41B=matrix(4,#vars41B,i,j,polcoeff(eq41B[i],1,vars41B[j]));
rhs41B=matrix(4,1,i,j,-substvec(eq41B[i],vars41B,vector(#vars41B)));
for(i=1,#eq41B,check_zero(eq41B[i]-(M41B*vars41B~)[i]+rhs41B[i,1],Str("intersection B E4 r-linear reconstruction row ",i)));
check_true(matrank(M41B)==1,"intersection B E4 r-linear rank one");
check_true(matrank(matconcat([M41B,rhs41B]))==1,"intersection B E4 r-linear augmented rank one");
rows41B=[2];
cols41B=[3];
check_zero(matdet(vecextract(M41B,rows41B,cols41B))-2*k,"intersection B E4 r-linear safe pivot");
freecols41B=[1,2,4,5];
pivvars41B=vecextract(vars41B,cols41B);
freevars41B=vecextract(vars41B,freecols41B);
rhsrows41B=vector(#rows41B,i,rhs41B[rows41B[i],1])~;
sol41B=matsolve(vecextract(M41B,rows41B,cols41B),rhsrows41B-vecextract(M41B,rows41B,freecols41B)*freevars41B~);
for(i=1,#eq41B,check_zero(substvec(eq41B[i],pivvars41B,Vec(sol41B)),Str("intersection B E4 r-linear residual row ",i)));
E4_B1=substvec(E4_B,pivvars41B,Vec(sol41B));

eq40B=vector(5,i,c3(E4_B1,i-1,5-i,0));
vars40B=[l0,l1,l3,l4];
M40B=matrix(5,#vars40B,i,j,polcoeff(eq40B[i],1,vars40B[j]));
rhs40B=matrix(5,1,i,j,-substvec(eq40B[i],vars40B,vector(#vars40B)));
for(i=1,#eq40B,check_zero(eq40B[i]-(M40B*vars40B~)[i]+rhs40B[i,1],Str("intersection B E4 binary reconstruction row ",i)));
print(Str("DN2C_INTERSECTION_BRANCH_B_E4_BINARY_RANK ",matrank(M40B)));
print(Str("DN2C_INTERSECTION_BRANCH_B_E4_BINARY_AUGMENTED_RANK ",matrank(matconcat([M40B,rhs40B]))));
print("DN2C_INTERSECTION_BRANCH_B_E4_BINARY_BEGIN");
for(i=1,#eq40B,print(Str(i," ",eq40B[i])));
rows40B=[2,5];
cols40B=[1,3];
freecols40B=[2,4];
check_zero(matdet(vecextract(M40B,rows40B,cols40B))+4*k^2,"intersection B E4 binary safe pivot");
pivvars40B=vecextract(vars40B,cols40B);
freevars40B=vecextract(vars40B,freecols40B);
rhsrows40B=vector(#rows40B,i,rhs40B[rows40B[i],1])~;
sol40B=matsolve(vecextract(M40B,rows40B,cols40B),rhsrows40B-vecextract(M40B,rows40B,freecols40B)*freevars40B~);
res40B=vector(#eq40B,i,substvec(eq40B[i],pivvars40B,Vec(sol40B)));
print("DN2C_INTERSECTION_BRANCH_B_E4_BINARY_RESIDUALS_BEGIN");
for(i=1,#res40B,print(Str(i," ",res40B[i])));

detdesc=matdet(L);
detdesc=substvec(detdesc,pivvars6,Vec(sol6));
detdesc=substvec(detdesc,pivvars51,Vec(sol51));
detdesc=substvec(detdesc,pivvars50,Vec(sol50));
detdesc=substvec(detdesc,subSvars,subSvals);
detdesc=substvec(detdesc,subTvars,subTvals);
detdesc=substvec(detdesc,subBvars,subBvals);
detdesc=substvec(detdesc,pivvars41B,Vec(sol41B));
detdesc=substvec(detdesc,pivvars40B,Vec(sol40B));
Wcompat=polcoeff(res40B[1]/k,1,u2);
check_zero(res40B[1]-k*Wcompat*Y,"intersection B E4 compatibility factors as k*W*Y");
check_zero(res40B[2],"intersection B E4 residual 2");
check_zero(res40B[3]+3*res40B[1],"intersection B E4 residual 3 ratio");
check_zero(res40B[4]+2*res40B[1],"intersection B E4 residual 4 ratio");
check_zero(res40B[5],"intersection B E4 residual 5");

detdescY=substvec(detdesc,subYvars,subYvals);
print(Str("DN2C_INTERSECTION_BRANCH_BY_DETL_ZERO ",detdescY==0));

E3descY=E3;
E3descY=substvec(E3descY,pivvars6,Vec(sol6));
E3descY=substvec(E3descY,pivvars51,Vec(sol51));
E3descY=substvec(E3descY,pivvars50,Vec(sol50));
E3descY=substvec(E3descY,subSvars,subSvals);
E3descY=substvec(E3descY,subTvars,subTvals);
E3descY=substvec(E3descY,subBvars,subBvals);
E3descY=substvec(E3descY,pivvars41B,Vec(sol41B));
E3descY=substvec(E3descY,pivvars40B,Vec(sol40B));
E3descY=substvec(E3descY,subYvars,subYvals);
print("DN2C_INTERSECTION_BRANCH_BY_E3_PROFILE_BEGIN");
exps3=[[0,0,3],[0,1,2],[0,2,1],[0,3,0],[1,0,2],[1,1,1],[1,2,0],[2,0,1],[2,1,0],[3,0,0]];
for(i=1,#exps3,{value=c3(E3descY,exps3[i][1],exps3[i][2],exps3[i][3]);print(Str(exps3[i]," ZERO ",value==0," LENGTH ",#Str(value)))});
e3p3=c3(E3descY,3,0,0);
print(Str("DN2C_INTERSECTION_BRANCH_BY_E3_P3 ",e3p3));
Hcompat=polcoeff(e3p3/k,1,l6)/polcoeff(Wcompat,1,l6);
check_zero(e3p3-k*Wcompat*Hcompat,"intersection BY E3 p3 factors as k*W*H");
print(Str("DN2C_INTERSECTION_BRANCH_BY_E3_H ",Hcompat));
check_zero(polcoeff(Hcompat,1,b1)+1,"intersection H coefficient of b1");
subHvars=[b1];
subHvals=[subst(Hcompat,b1,0)];
check_zero(substvec(Hcompat,subHvars,subHvals),"intersection H branch solve");
E3_H=substvec(E3descY,subHvars,subHvals);
eq3H=vector(3,i,c3(E3_H,i-1,4-i,0));
vars3H=[a3,l2,l1,l4];
M3H=matrix(3,#vars3H,i,j,polcoeff(eq3H[i],1,vars3H[j]));
rhs3H=matrix(3,1,i,j,-substvec(eq3H[i],vars3H,vector(#vars3H)));
for(i=1,#eq3H,check_zero(eq3H[i]-(M3H*vars3H~)[i]+rhs3H[i,1],Str("intersection H E3 reconstruction row ",i)));
print(Str("DN2C_INTERSECTION_BRANCH_BYH_E3_RANK ",matrank(M3H)));
print(Str("DN2C_INTERSECTION_BRANCH_BYH_E3_AUGMENTED_RANK ",matrank(matconcat([M3H,rhs3H]))));
rows3H=[1,3];
cols3H=[1,2];
print(Str("DN2C_INTERSECTION_BRANCH_BYH_E3_TRIAL_PIVOT ",matdet(vecextract(M3H,rows3H,cols3H))));
check_zero(M3H[1,2]-3*Wcompat,"intersection H E3 safe one-pivot");
rows3H1=[1];
cols3H1=[2];
freecols3H1=[1,3,4];
pivvars3H=vecextract(vars3H,cols3H1);
freevars3H=vecextract(vars3H,freecols3H1);
rhsrows3H=vector(#rows3H1,i,rhs3H[rows3H1[i],1])~;
sol3H=matsolve(vecextract(M3H,rows3H1,cols3H1),rhsrows3H-vecextract(M3H,rows3H1,freecols3H1)*freevars3H~);
res3H=vector(#eq3H,i,substvec(eq3H[i],pivvars3H,Vec(sol3H)));
print("DN2C_INTERSECTION_BRANCH_BYH_E3_RESIDUALS_BEGIN");
for(i=1,#res3H,print(Str(i," ",res3H[i])));
check_zero(res3H[1],"intersection H E3 residual 1");
check_zero(res3H[2]+k*Wcompat^2/2,"intersection H E3 residual 2 forces W");
check_zero(res3H[3]+k*Wcompat^2/2,"intersection H E3 residual 3 repeats W");

detdescH=substvec(detdescY,subHvars,subHvals);
detdescH=substvec(detdescH,pivvars3H,Vec(sol3H));
print(Str("DN2C_INTERSECTION_BRANCH_BYH_DETL_LENGTH ",#Str(detdescH)));
print(Str("DN2C_INTERSECTION_BRANCH_BY_DETL_LENGTH ",#Str(detdescY)));
spec0vars=[v1,v2,v3,t1,t2,b1,l6];
spec0vals=[0,0,0,0,0,b3,l7];
E3spec0=substvec(E3descY,spec0vars,spec0vals);
detSpec0=substvec(detdescY,spec0vars,spec0vals);
print(Str("DN2C_INTERSECTION_BRANCH_BY_SPEC0_DETL ",detSpec0));
print("DN2C_INTERSECTION_BRANCH_BY_SPEC0_E3_BEGIN");
for(i=1,#exps3,{value=c3(E3spec0,exps3[i][1],exps3[i][2],exps3[i][3]);if(value!=0,print(Str(exps3[i]," ",value)))});

specAvars=[v1,v2,v3,t1,t2,b1];
specAvals=[0,0,0,0,0,b3];
E3specA=substvec(E3descY,specAvars,specAvals);
detSpecA=substvec(detdescY,specAvars,specAvals);
print(Str("DN2C_INTERSECTION_BRANCH_BY_SPECA_DETL ",detSpecA));
print("DN2C_INTERSECTION_BRANCH_BY_SPECA_E3_BEGIN");
for(i=1,#exps3,{value=c3(E3specA,exps3[i][1],exps3[i][2],exps3[i][3]);if(value!=0,print(Str(exps3[i]," ",value)))});

specBvars=[v1,v2,v3,t1,t2,l6];
specBvals=[0,0,0,0,0,l7];
E3specB=substvec(E3descY,specBvars,specBvals);
detSpecB=substvec(detdescY,specBvars,specBvals);
print(Str("DN2C_INTERSECTION_BRANCH_BY_SPECB_DETL ",detSpecB));
print("DN2C_INTERSECTION_BRANCH_BY_SPECB_E3_BEGIN");
for(i=1,#exps3,{value=c3(E3specB,exps3[i][1],exps3[i][2],exps3[i][3]);if(value!=0,print(Str(exps3[i]," ",value)))});

check_zero(polcoeff(Wcompat,1,l6)+4/3,"intersection W coefficient of l6");
subWvars=[l6];
subWvals=[3*subst(Wcompat,l6,0)/4];
check_zero(substvec(Wcompat,subWvars,subWvals),"intersection W branch solve");
detdescW=substvec(detdesc,subWvars,subWvals);
print(Str("DN2C_INTERSECTION_BRANCH_BW_DETL_ZERO ",detdescW==0));
check_zero(detdescW,"intersection W branch forces determinant of L zero");
print("D4_DN2C_PUNCTURED_INTERSECTION_EXCLUDED");

\\ Fresh zero-contact origin E6 solve.
D0=build_det(0);
check_zero(polcoeff(D0,7,w),"origin E7");
E60=polcoeff(D0,6,w);
E50=polcoeff(D0,5,w);
E40=polcoeff(D0,4,w);
eq60=vector(#exps6,i,c3(E60,exps6[i][1],exps6[i][2],exps6[i][3]));
M60=matrix(#eq60,#low,i,j,polcoeff(eq60[i],1,low[j]));
rhs60=matrix(#eq60,1,i,j,-substvec(eq60[i],low,zeros));
rows60=[1,2,3,4,5];
cols60=[1,2,3,4,6];
freecols60=[5,7,8,9,10,11,12,13,14,15,16,17,18];
M60p=vecextract(M60,rows60,cols60);
check_zero(matdet(M60p)-31104,"origin frozen E6 pivot");
check_true(matrank(M60)==5,"origin E6 rank five");
check_true(matrank(matconcat([M60,rhs60]))==5,"origin E6 augmented rank five");
pivvars60=vecextract(low,cols60);
freevars60=vecextract(low,freecols60);
rhsrows60=vector(#rows60,i,rhs60[rows60[i],1])~;
sol60=matsolve(M60p,rhsrows60-vecextract(M60,rows60,freecols60)*freevars60~);
for(i=1,#eq60,check_zero(substvec(eq60[i],pivvars60,Vec(sol60)),Str("origin E6 residual row ",i)));
E50s=substvec(E50,pivvars60,Vec(sol60));
E40s=substvec(E40,pivvars60,Vec(sol60));

print("DN2C_ORIGIN_E5_R2_BEGIN");
for(ip=0,3,{iq=3-ip;value=c3(E50s,ip,iq,2);if(value!=0,print(Str("[",ip,",",iq,",2] ",value)))});
print("DN2C_ORIGIN_E4_R1_BEGIN");
for(ip=0,3,{iq=3-ip;value=c3(E40s,ip,iq,1);if(value!=0,print(Str("[",ip,",",iq,",1] ",value)))});

check_zero(c3(E40s,3,0,1)+3*b4^2,"origin E4 p^3 r square");
check_zero(c3(E40s,0,3,1)-2*(3*b4+2*l8)^2/3,"origin E4 q^3 r square");
origin_forced_vars=[b4,l8];
origin_forced_vals=[0,0];
for(i=1,#sol60,check_zero(substvec(sol60[i],origin_forced_vars,origin_forced_vals),Str("origin E6 pivot variable collapses ",i)));

\\ Exact target-linear plane reduction after all nonlinear r-coefficients
\\ vanish.  Adjugate normalization avoids divisions in the certificate.
A0=a0*p^2+a1*p*q+a3*q^2;
B0=b0*p^2+b1*p*q+b3*q^2;
Hbin=[A0+U0+P,B0+V0+Q,T0+R]~;
Fbin=L*[p,q,r]~+Hbin;
Jbin=jacmat(Hbin);
Mbin=L+Jbin;
detL=matdet(L);
adjL=[l4*l8-l5*l7,l2*l7-l1*l8,l1*l5-l2*l4;l5*l6-l3*l8,l0*l8-l2*l6,l2*l3-l0*l5;l3*l7-l4*l6,l1*l6-l0*l7,l0*l4-l1*l3];
check_zero(adjL*L-detL*matid(3),"origin adjugate target normalization");
Ftrans=adjL*Fbin;
check_zero(deriv(Ftrans[1],r),"origin normalized first coordinate binary");
check_zero(deriv(Ftrans[2],r),"origin normalized second coordinate binary");
check_zero(deriv(Ftrans[3],r)-detL,"origin normalized third r slope");
Mtrans=adjL*Mbin;
planeDet=Mtrans[1,1]*Mtrans[2,2]-Mtrans[1,2]*Mtrans[2,1];
check_zero(planeDet-detL*matdet(Mbin),"origin exact plane Jacobian identity");
print("D4_DN2C_ORIGIN_BINARY_COLLAPSE_PLANE_EXIT");

print("D4_DN2C_BOUNDARY_E5_PROBE_PASS");
quit(0);
