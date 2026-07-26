\\ Hostile PARI/GP reconstruction of the full D3-BS-N2-Z descent.
\\ Starting data only:
\\   H4=(p^4,p^2*q^2,0), (H3)_3=p^2*q,
\\   det(L+z*JH2+z^2*JH3+z^3*JH4).

FAULT=if(getenv("D3_BS_AUDIT_FAULT")=="1",1,0);
fail(msg)={print("FAIL ",msg);quit(1);};
check0(x,msg)={if(x!=0,fail(Str(msg,": residual=",x)));};
checkeq(x,y,msg)=check0(x-y,msg);
coeffmon(f,ez,ep,eq,er)={my(g=f);for(i=1,ez,g=deriv(g,z));for(i=1,ep,g=deriv(g,p));for(i=1,eq,g=deriv(g,q));for(i=1,er,g=deriv(g,r));g=subst(subst(subst(subst(g,z,0),p,0),q,0),r,0);g/(ez!*ep!*eq!*er!);};
coeffz(f,ez)={my(g=f);for(i=1,ez,g=deriv(g,z));subst(g,z,0)/ez!;};
coeffpq(f,ep,eq)={my(g=f);for(i=1,ep,g=deriv(g,p));for(i=1,eq,g=deriv(g,q));g=subst(subst(g,p,0),q,0);g/(ep!*eq!);};
det3(M)=M[1,1]*(M[2,2]*M[3,3]-M[2,3]*M[3,2])-M[1,2]*(M[2,1]*M[3,3]-M[2,3]*M[3,1])+M[1,3]*(M[2,1]*M[3,2]-M[2,2]*M[3,1]);
suball(x,V,W)={for(i=1,#V,x=subst(x,V[i],W[i]));x;};
weighted(U,V,T)={my(H2=[A,B,T],H3=[U,V,p^2*q],H4=[p^4,p^2*q^2,0],M);M=matrix(3,3,i,j,L[i,j]+z*deriv(H2[i],[p,q,r][j])+z^2*deriv(H3[i],[p,q,r][j])+z^3*deriv(H4[i],[p,q,r][j]));det3(M);};
coefmatrix(E,d,V)={my(T=List());for(er=0,d,for(iq=0,d-er,listput(T,[d-er-iq,iq,er])));matrix(#T,#V,i,j,deriv(coeffmon(E,0,T[i][1],T[i][2],T[i][3]),V[j]));};

p='p;q='q;r='r;z='z;
aa='aa;bb='bb;cc='cc;kk='kk;ss='ss;dd='dd;
u0='u0;u1='u1;u2='u2;u3='u3;
v0='v0;v1='v1;v2='v2;v3='v3;
t0='t0;t1='t1;t2='t2;
a0='a0;a1='a1;a2='a2;a3='a3;a4='a4;a5='a5;
b0='b0;b1='b1;b2='b2;b3='b3;b4='b4;b5='b5;
l0='l0;l1='l1;l2='l2;l3='l3;l4='l4;l5='l5;l6='l6;l7='l7;l8='l8;

\\ Complete E7 syzygy spaces, independently from the determinant descent.
al=-2*p^3*q^2;be=-4*p^5;ga=8*p^5*q;
rru='rru;rrv='rrv;
rel2=al*rru+be*rrv;
M2=[deriv(coeffpq(rel2,5,0),rru),deriv(coeffpq(rel2,5,0),rrv);deriv(coeffpq(rel2,3,2),rru),deriv(coeffpq(rel2,3,2),rrv)];
checkeq(matrank(M2),2,"E7 r2 kernel rank");
up='up;uq='uq;vp='vp;vq='vq;tc='tc;
rel1=al*(up*p+uq*q)+be*(vp*p+vq*q)+ga*tc;
vars1=[up,uq,vp,vq,tc];
M1=matrix(7,5,i,j,deriv(coeffpq(rel1,6-(i-1),i-1),vars1[j]));
checkeq(matrank(M1),4,"E7 r1 rank");
check0(al*0+be*(2*q)+ga,"E7 r1 displayed generator");
xu0='xu0;xu1='xu1;xu2='xu2;xv0='xv0;xv1='xv1;xv2='xv2;xt0='xt0;xt1='xt1;
rel0=al*(xu0*p^2+xu1*p*q+xu2*q^2)+be*(xv0*p^2+xv1*p*q+xv2*q^2)+ga*(xt0*p+xt1*q);
vars0=[xu0,xu1,xu2,xv0,xv1,xv2,xt0,xt1];
M0=matrix(8,8,i,j,deriv(coeffpq(rel0,7-(i-1),i-1),vars0[j]));
checkeq(matrank(M0),5,"E7 r0 rank");
check0(al*(-2*p^2)+be*q^2,"E7 r0 generator 1");
check0(be*(2*p*q)+ga*p,"E7 r0 generator 2");
check0(be*(2*q^2)+ga*q,"E7 r0 generator 3");
checkeq(matrank([-2,0,0;0,0,0;0,0,0;0,0,0;0,2,0;1,0,2;0,1,0;0,0,1]),3,"E7 r0 generator independence");

U0=u0*p^3+u1*p^2*q+u2*p*q^2+u3*q^3;
V0=v0*p^3+v1*p^2*q+v2*p*q^2+v3*q^3;
T0=t0*p^2+t1*p*q+t2*q^2;
A=a0*p^2+a1*p*q+a2*p*r+a3*q^2+a4*q*r+a5*r^2;
B=b0*p^2+b1*p*q+b2*p*r+b3*q^2+b4*q*r+b5*r^2;
L=[l0,l1,l2;l3,l4,l5;l6,l7,l8];
S=aa*p+bb*q+cc*r;
U=U0-2*kk*p^2*r;
V=V0+2*aa*p*q*r+(2*bb+kk)*q^2*r+cc*q*r^2;
T=T0+(aa*p+bb*q)*r+cc*r^2/2;
D=weighted(U,V,T);
E6=coeffz(D,6);E5=coeffz(D,5);E4=coeffz(D,4);E3=coeffz(D,3);
check0(coeffz(D,9),"raw E9");
check0(coeffz(D,8),"raw E8");
check0(coeffz(D,7),"complete E7 parameterization");
checkeq(coeffmon(D,6,3,0,3),4*cc^2,"E6 c-square");

pv=[b2,b4,b5,a2,a4,a5];
pw=[aa*v1-3*kk*v0/2,2*l8-2*aa*t1+2*aa*v2+bb*v1+2*kk*t0,aa^2,-8*aa*t2+aa*u1+6*aa*v3-4*bb*t1+4*bb*v2-2*kk*t1-3*kk*u0/2+3*kk*v2,2*aa*u2-8*bb*t2+bb*u1+6*bb*v3-8*kk*t2+6*kk*v3,2*bb^2+4*bb*kk+3*kk^2];
E6c=subst(E6,cc,0);
checkeq(coeffmon(E6c,0,6,0,0),-4*(b2-pw[1]),"unit E6 pivot b2");
checkeq(coeffmon(E6c,0,5,1,0),-4*(b4-pw[2]),"unit E6 pivot b4");
checkeq(coeffmon(E6c,0,5,0,1),-8*(b5-pw[3]),"unit E6 pivot b5");
checkeq(coeffmon(E6c,0,4,2,0),-2*(a2-pw[4]),"unit E6 pivot a2");
checkeq(coeffmon(E6c,0,3,3,0),-2*(a4-pw[5]),"unit E6 pivot a4");
checkeq(coeffmon(E6c,0,3,2,1),-4*(a5-pw[6]),"unit E6 pivot a5");
E6p=suball(subst(E6,cc,0),pv,pw);
E6want=16*aa*(bb+kk)*p^4*q*r+(6*aa*u3+(4*bb+3*kk)*u2)*p^2*q^4+6*u3*(bb+kk)*p*q^5;
checkeq(E6p,E6want,"complete E6 pivot replay");
E5p=suball(subst(E5,cc,0),pv,pw);
checkeq(coeffmon(E5p,0,1,2,2),-24*(bb+kk)^3,"E5 b+k cube");
checkeq(subst(coeffmon(E5p,0,3,0,2),kk,-bb),-12*aa^2*bb,"E5 a^2*b");
checkeq(subst(coeffmon(E6p,0,2,4,0),kk,-bb),bb*u2+6*aa*u3,"E6 b*u2+6*a*u3");

\\ Scaling r -> r/ss covers each nonzero component.
checkeq(subst(U,r,r/ss),U0-2*(kk/ss)*p^2*r,"scaling U");
checkeq(subst(subst(V,cc,0),r,r/ss),V0+2*(aa/ss)*p*q*r+((2*bb+kk)/ss)*q^2*r,"scaling V");
checkeq(subst(subst(T,cc,0),r,r/ss),T0+((aa/ss)*p+(bb/ss)*q)*r,"scaling T");
checkeq(det3([l0,l1,l2/ss;l3,l4,l5/ss;l6,l7,l8/ss]),det3(L)/ss,"scaling det L");

\\ Chart I: aa=1, bb=kk=cc=0, u3=0.
cIv=[aa,bb,kk,cc,u3];cIw=[1,0,0,0,0];
pIv=[b2,b4,b5,a2,a4,a5];pIw=[v1,2*l8-2*t1+2*v2,1,-8*t2+u1+6*v3,2*u2,0];
E6I=suball(suball(E6,cIv,cIw),pIv,pIw);
check0(E6I,"Chart I E6 replay");
E5I=suball(suball(E5,cIv,cIw),pIv,pIw);
checkeq(coeffmon(E5I,0,2,2,1),4*u2,"Chart I E5 u2");
checkeq(coeffmon(E5I,0,3,1,1),8*(2*t2-3*v3),"Chart I E5 t2/v3");
i8=t1-v2/2;
ci2v=[u2,t2];ci2w=[0,3*v3/2];
pI5v=[l8,b1,b3,a1,a3];
pI5w=[i8,l5-i8*v1+t1*v1+9*v0*v3/2,l7+i8*t1-i8*v2-3*t0*v3-t1^2+t1*v2+3*v1*v3/2,l2-i8*u1+6*i8*v3+t1*u1-12*t1*v3+9*u0*v3/2+3*v2*v3,3*u1*v3/2];
E5Ib=suball(suball(suball(E5,cIv,cIw),pIv,pIw),ci2v,ci2w);
checkeq(matrank(coefmatrix(E5Ib,5,pI5v)),5,"Chart I E5 pivot rank");
E5Ir=suball(E5Ib,pI5v,pI5w);
check0(E5Ir,"Chart I E5 replay");
E4Ir=suball(suball(suball(suball(E4,cIv,cIw),pIv,pIw),ci2v,ci2w),pI5v,pI5w);
checkeq(coeffmon(E4Ir,0,2,0,2),12*v3,"Chart I E4 v3");
pI4v=[v3,l7,l4,l1];pI4w=[0,i8*v2/2,l5*v2/2,l2*v2/2];
checkeq(matrank(coefmatrix(subst(E4Ir,v3,0),4,[l7,l4,l1])),3,"Chart I E4 pivot rank");
check0(suball(E4Ir,pI4v,pI4w),"Chart I E4 replay");
detI=suball(suball(suball(suball(suball(det3(L),cIv,cIw),pIv,pIw),ci2v,ci2w),pI5v,pI5w),pI4v,pI4w);
check0(detI,"Chart I determinant collapse");

\\ Chart II: aa=0, bb=1, kk=-1, cc=0, u2=0.
cIIv=[aa,bb,kk,cc,u2];cIIw=[0,1,-1,0,0];
pIIv=[b2,b4,b5,a2,a4,a5];pIIw=[3*v0/2,2*l8-2*t0+v1,0,-2*t1+3*u0/2+v2,u1,1];
check0(suball(suball(E6,cIIv,cIIw),pIIv,pIIw),"Chart II E6 replay");
E5II=suball(suball(E5,cIIv,cIIw),pIIv,pIIw);
checkeq(coeffmon(E5II,0,4,0,1),3*v0,"Chart II E5 v0");
checkeq(coeffmon(E5II,0,2,2,1),-3*(4*t1-u0-2*v2)/2,"Chart II E5 u0");
checkeq(coeffmon(E5II,0,0,5,0),3*u3*(t1-v2),"Chart II E5 split");
cII2v=[v0,u0];cII2w=[0,4*t1-2*v2];
pII5v=[b0,b1,a0,a1];
pII5w=[l5-l8*v1+t0*v1,2*l6+4*l8*t1-4*l8*v2-8*t0*t1+6*t0*v2+t1*v1,l2+8*l8*t2-l8*u1-6*l8*v3-8*t0*t2+t0*u1+6*t0*v3+6*t1^2-8*t1*v2+3*v2^2,8*t1*t2+t1*u1-6*t1*v3-8*t2*v2+6*v2*v3];
E5IIb=suball(suball(suball(E5,cIIv,cIIw),pIIv,pIIw),cII2v,cII2w);
checkeq(matrank(coefmatrix(E5IIb,5,pII5v)),4,"Chart II E5 pivot rank");
E5IIr=suball(E5IIb,pII5v,pII5w);
checkeq(E5IIr,6*u3*(l8-t0)*p*q^4+3*u3*(t1-v2)*q^5,"Chart II E5 replay");

\\ Chart II, u3 nonzero.
nzv=[v2,l8];nzw=[t1,t0];
E4nz=suball(suball(suball(suball(suball(E4,cIIv,cIIw),pIIv,pIIw),cII2v,cII2w),pII5v,pII5w),nzv,nzw);
checkeq(coeffmon(E4nz,0,0,4,0),3*u3*(-l6+t0*t1),"Chart II u3!=0 pivot");
nzpv=[l6,l3,l0];nzpw=[t0*t1,l5*t1,l2*t1];
checkeq(matrank(coefmatrix(E4nz,4,nzpv)),3,"Chart II u3!=0 E4 pivot rank");
check0(suball(E4nz,nzpv,nzpw),"Chart II u3!=0 E4 replay");
detnz=suball(suball(suball(suball(suball(suball(det3(L),cIIv,cIIw),pIIv,pIIw),cII2v,cII2w),pII5v,pII5w),nzv,nzw),nzpv,nzpw);
check0(detnz,"Chart II u3!=0 determinant collapse");

\\ Chart II, u3=0 and dd=t1-v2.
zv=[u3,v2];zw=[0,t1-dd];
E4z=suball(suball(suball(suball(suball(E4,cIIv,cIIw),pIIv,pIIw),cII2v,cII2w),pII5v,pII5w),zv,zw);
checkeq(coeffmon(E4z,0,3,0,1),8*(-l8+t0)^2,"Chart II u3=0 square");
E4zl=subst(E4z,l8,t0);
checkeq(coeffmon(E4zl,0,3,1,0),-8*dd*(-l6+t0*t1),"Chart II d!=0 pivot 1");
checkeq(coeffmon(E4zl,0,1,3,0),-24*dd^2*(t2-v3),"Chart II d!=0 pivot 2");
dnpv=[l6,t2,a3,l3,l0];
dnpw=[t0*t1,v3,v3*(u1-v3),l5*(t1+dd)-t0*dd*v1,-4*b3*dd+12*dd^3+dd*l2+4*dd*l7-dd*t0*u1-2*dd*t0*v3+4*dd*v1*v3+l2*t1];
checkeq(matrank(coefmatrix(E4zl,4,dnpv)),5,"Chart II d!=0 E4 pivot rank");
check0(suball(E4zl,dnpv,dnpw),"Chart II d!=0 E4 replay");
E3dn=suball(subst(suball(suball(suball(suball(suball(E3,cIIv,cIIw),pIIv,pIIw),cII2v,cII2w),pII5v,pII5w),zv,zw),l8,t0),dnpv,dnpw);
want=12*dd^3;if(FAULT,want=-want);
checkeq(coeffmon(E3dn,0,0,2,1),want,"Chart II d!=0 E3 cube");

\\ Chart II, d=0.
E4d0=subst(E4zl,dd,0);
d0pv=[l3,l0];d0pw=[l5*t1+l6*v1-t0*t1*v1,l2*t1-(l6-t0*t1)*(8*t2-u1-6*v3)];
checkeq(matrank(coefmatrix(E4d0,4,d0pv)),2,"Chart II d=0 E4 pivot rank");
check0(suball(E4d0,d0pv,d0pw),"Chart II d=0 E4 replay");
E3d0=suball(subst(subst(suball(suball(suball(suball(suball(E3,cIIv,cIIw),pIIv,pIIw),cII2v,cII2w),pII5v,pII5w),zv,zw),l8,t0),dd,0),d0pv,d0pw);
gap=-l6+t0*t1;
checkeq(coeffmon(E3d0,0,3,0,0),-4*gap^2,"Chart II d=0 E3 square");
detd0=suball(subst(subst(suball(suball(suball(suball(suball(det3(L),cIIv,cIIw),pIIv,pIIw),cII2v,cII2w),pII5v,pII5w),zv,zw),l8,t0),dd,0),d0pv,d0pw);
check0(subst(detd0,l6,t0*t1),"Chart II d=0 determinant factor");

\\ E7 origin: the whole E6 block and its rank-six solve.
E6o=suball(E6,[aa,bb,cc,kk],[0,0,0,0]);
check0(suball(E6o,[b2,b4,b5,a2,a4,a5],[0,2*l8,0,0,0,0]),"origin E6 replay");
checkeq(coeffmon(E6o,0,4,2,0),-2*a2,"origin a2 pivot");
checkeq(coeffmon(E6o,0,3,3,0),-2*a4,"origin a4 pivot");
checkeq(coeffmon(E6o,0,3,2,1),-4*a5,"origin a5 pivot");
checkeq(coeffmon(E6o,0,6,0,0),-4*b2,"origin b2 pivot");
checkeq(coeffmon(E6o,0,5,1,0),-4*b4+8*l8,"origin b4/l8 pivot");
checkeq(coeffmon(E6o,0,5,0,1),-8*b5,"origin b5 pivot");

print("D3_BS_N2_Z_HOSTILE_EXACT_PASS");
quit(0);
