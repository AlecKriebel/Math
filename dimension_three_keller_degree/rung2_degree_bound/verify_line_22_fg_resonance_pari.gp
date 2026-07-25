\\ Independent PARI/GP reconstruction of the F=0/G=0 resonance exit.
\\ Run through run_verify_line_22_fg_resonance_pari.sh, whose sentinel check
\\ makes parser/runtime errors fail closed.

x='x; y='y; z='z; s='s;
xyz=[x,y,z];

gradmat(F)=matrix(3,3,i,j,deriv(F[i],[x,y,z][j]));
jac3(f,g,h)=matdet(gradmat([f,g,h]));
wcoef(L,H2,H3,H4,k)={
  my(forms=[L,H2,H3,H4],acc=0,rw,M);
  for(i=0,3,for(j=0,3,for(h=0,3,
    if(i+j+h==k,
      rw=[i,j,h];
      M=matrix(3,3,rr,jj, \
        deriv(forms[rw[rr]+1][rr],xyz[jj]));
      acc+=matdet(M)
    )
  )));
  acc
};
cf(P,i,j,k)=polcoeff(polcoeff(polcoeff(P,i,x),j,y),k,z);
check(label,value)={
  if(value!=0, \
    print(Str("FAIL ",label,": ",value)); \
    quit(1));
  print(Str("  PASS ",label));
};

p=x^2; q=y*z;
t='t; cc='cc;
Fchart=3*t-cc*(2*t+1);
check("endpoint t=-1/2 is impossible", \
  subst(Fchart,t,-1/2)+3/2);
check("endpoint t=0 is exactly c=0",subst(Fchart,t,0)+cc);
check("b=0 specialization", \
  subst(3*ea*eb-2*ea*cc-eb*cc,eb,0)+2*ea*cc);
print("  PASS endpoint t=1 is a=b and lies outside the stratum");

c=3*t/(2*t+1);
D0=(t-1)*(2*t+1);
H4=[(p-t*q)^2,(p-q)^2,0];

\\ General raw E7 matrix and a nonzero 14-by-14 minor.
GU=gu0*x^3+gu1*x^2*y+gu2*x^2*z+gu3*x*y^2+gu4*x*y*z \
   +gu5*x*z^2+gu6*y^3+gu7*y^2*z+gu8*y*z^2+gu9*z^3;
GV=gv0*x^3+gv1*x^2*y+gv2*x^2*z+gv3*x*y^2+gv4*x*y*z \
   +gv5*x*z^2+gv6*y^3+gv7*y^2*z+gv8*y*z^2+gv9*z^3;
GW=gw0*x^2+gw1*x*y+gw2*x*z+gw3*y^2+gw4*y*z+gw5*z^2;
GE7=jac3(H4[1],H4[2],GW)+jac3(H4[1],GV,x*(p-c*q)) \
    +jac3(GU,H4[2],x*(p-c*q));
rawVars=[gu1,gu2,gu3,gu5,gu6,gu7,gu8,gu9, \
         gv1,gv2,gv3,gv5,gv6,gv9];
rawExponents=[ \
  [6,1,0],[6,0,1],[5,2,0],[5,0,2],[4,3,0],[4,2,1],[4,1,2], \
  [4,0,3],[3,3,1],[3,1,3],[2,4,1],[2,3,2],[2,2,3],[2,1,4]];
RawMinor=matrix(14,14,i,j, \
  cf(deriv(GE7,rawVars[j]), \
     rawExponents[i][1],rawExponents[i][2],rawExponents[i][3]));
check("raw E7 rank-14 minor", \
  matdet(RawMinor) \
  +101559956668416*t^6*(t-1)^6/(2*t+1)^14);
check("raw E7 minor at t=1/2", \
  subst(matdet(RawMinor),t,1/2)+387420489/256);

\\ Generic t != 1/2 gauge.
w0='w0; wr='wr; ws='ws; wm='wm; wq='wq; wn='wn;
U3=A*x*q-4*D0*(wm*x*y^2+wn*x*z^2)/3 \
   -4*t*D0*(wr*y^2*z+ws*y*z^2)/(3*(2*t-1));
V3=B*x*q+4*D0*(wr*(x^2*y-y^2*z)+ws*(x^2*z-y*z^2)) \
   /(3*t*(2*t-1));
W=w0*p+wr*x*y+ws*x*z+wm*y^2+wq*q+wn*z^2;
H3=[U3,V3,x*(p-c*q)];
E7=jac3(H4[1],H4[2],W)+jac3(H4[1],V3,H3[3]) \
   +jac3(U3,H4[2],H3[3]);
check("generic gauge E7 identity",E7);

U2=u0*p+u1*x*y+u2*x*z+u3*y^2+u4*q+u5*z^2;
V2=v0*p+v1*x*y+v2*x*z+v3*y^2+v4*q+v5*z^2;
L=[l0*x+l1*y+l2*z,l3*x+l4*y+l5*z,l6*x+l7*y+l8*z];
E6=wcoef(L,[U2,V2,W],H3,H4,6);
check("generic E6 wm square",cf(E6,2,4,0)+16*D0*wm^2/3);
check("generic E6 wn square",cf(E6,2,0,4)-16*D0*wn^2/3);
E6red=subst(subst(E6,wm,0),wn,0);
Cy=t^2*cf(E6red,4,2,0)+t*cf(E6red,2,3,1)+cf(E6red,0,4,2);
Cz=t^2*cf(E6red,4,0,2)+t*cf(E6red,2,1,3)+cf(E6red,0,2,4);
check("generic E6 wr square", \
  Cy+8*t*(t-1)^2*(2*t+1)*wr^2/(3*(2*t-1)^2));
check("generic E6 ws square", \
  Cz-8*t*(t-1)^2*(2*t+1)*ws^2/(3*(2*t-1)^2));

rankVars=[u1,u2,u3,u5,v1,v2,v3,v5];
rankExponents=[ \
  [5,1,0],[5,0,1],[4,2,0],[4,0,2], \
  [3,2,1],[3,1,2],[2,3,1],[2,1,3]];
E6Minor=matrix(8,8,i,j, \
  cf(deriv(E6,rankVars[j]), \
     rankExponents[i][1],rankExponents[i][2],rankExponents[i][3]));
check("generic E6 rank-8 minor", \
  matdet(E6Minor)-26873856*t^4*(t-1)^4/(2*t+1)^8);

\\ Independent t=1/2 gauge.
H4h=[(p-q/2)^2,(p-q)^2,0];
Wh=w0*p+wr*x*y+ws*x*z+wm*y^2+wq*q+wn*z^2;
U3h=A*x*q+4*(wr*x^2*y+ws*x^2*z+wm*x*y^2+wn*x*z^2)/3;
V3h=B*x*q;
H3h=[U3h,V3h,x*(p-3*q/4)];
E7h=jac3(H4h[1],H4h[2],Wh)+jac3(H4h[1],V3h,H3h[3]) \
    +jac3(U3h,H4h[2],H3h[3]);
check("t=1/2 gauge E7 identity",E7h);
E6h=wcoef(L,[U2,V2,Wh],H3h,H4h,6);
check("t=1/2 E6 wm square",cf(E6h,2,4,0)-16*wm^2/3);
check("t=1/2 E6 wn square",cf(E6h,2,0,4)+16*wn^2/3);
E6hred=subst(subst(E6h,wm,0),wn,0);
Cyh=cf(E6hred,4,2,0)/4+cf(E6hred,2,3,1)/2+cf(E6hred,0,4,2);
Czh=cf(E6hred,4,0,2)/4+cf(E6hred,2,1,3)/2+cf(E6hred,0,2,4);
check("t=1/2 E6 wr square",Cyh+2*wr^2/3);
check("t=1/2 E6 ws square",Czh-2*ws^2/3);
E6hMinor=matrix(8,8,i,j, \
  cf(deriv(E6h,rankVars[j]), \
     rankExponents[i][1],rankExponents[i][2],rankExponents[i][3]));
check("t=1/2 E6 rank-8 minor",matdet(E6hMinor)-6561/16);

\\ Invariant lower exit and common E5 kernel.
K=-4*(t-1)*(2*t+1)/3;
U2i=iu0*p+K*il7*x*y+K*il8*x*z+iu4*q;
V2i=iv0*p+iv4*q;
Wi=iw0*p+iwq*q;
Li=[il0*x+il1*y+il2*z,il3*x+il4*y+il5*z,il6*x+il7*y+il8*z];
H3i=[iA*x*q,iB*x*q,x*(p-c*q)];
check("invariant lower E6 solution",wcoef(Li,[U2i,V2i,Wi],H3i,H4,6));
E5i=wcoef(Li,[U2i,V2i,Wi],H3i,H4,5);
yMons=[[4,1,0],[2,2,1],[0,3,2]];
zMons=[[4,0,1],[2,1,2],[0,2,3]];
yVars=[il1,il4,il7]; zVars=[il2,il5,il8];
My=matrix(3,3,i,j,cf(deriv(E5i,yVars[j]), \
  yMons[i][1],yMons[i][2],yMons[i][3]));
Mz=matrix(3,3,i,j,cf(deriv(E5i,zVars[j]), \
  zMons[i][1],zMons[i][2],zMons[i][3]));
for(i=1,3,for(j=1,3, \
  check(Str("E5 common kernel entry ",i,",",j),My[i,j]+Mz[i,j])));
check("E5 fixed rank-two minor", \
  My[1,1]*My[2,2]-My[1,2]*My[2,1] \
  +36*t*(t-1)/(2*t+1)^2);

\\ Exact F <-> G involution.
FF=3*sa*sb-2*sa*sc-sb*sc;
GG=3*sa*sb-sa*sc-2*sb*sc;
check("outer-component involution F to G", \
  (3*sb*sa-2*sb*sc-sa*sc)-GG);

print("PASS: independent PARI/GP finite-outer-critical F=0 and G=0 reconstruction");
quit(0)
