\\ Independent PARI/GP reconstruction of the six CH/CS endpoint exclusions.

die(msg) = { print(Str("FAIL: ",msg)); quit(1); };
check(flag,msg) = { if(!flag,die(msg)); };
checkeq(got,want,msg) = { if(got!=want,die(Str(msg,": got ",got,", want ",want))); };

x='x; y='y; z='z; ww='ww;
A='A; B='B; C='C; D='D; T='T; S='S;
xyz=[x,y,z];

homexps(n) =
{
  my(out=List());
  forstep(i=n,0,-1,forstep(j=n-i,0,-1,listput(out,[i,j,n-i-j])));
  Vec(out);
};

monoms(n) =
{
  my(exps=homexps(n));
  vector(#exps,i,x^exps[i][1]*y^exps[i][2]*z^exps[i][3]);
};

coeffxyz(f,e) = { polcoeff(polcoeff(polcoeff(f,e[1],x),e[2],y),e[3],z); };
jacvec(hh) = { matrix(3,3,i,j,deriv(hh[i],xyz[j])); };

subst_many(f,vv,values) =
{
  my(g=f);
  check(#vv==#values,"subst_many length mismatch");
  for(i=1,#vv,g=subst(g,vv[i],values[i]));
  g;
};

m2=monoms(2);
aa=[a0,a1,a2,a3,a4,a5];
bb=[b0,b1,b2,b3,b4,b5];
ll=[l0,l1,l2,l3,l4,l5,l6,l7,l8];
L=matrix(3,3,i,j,ll[3*(i-1)+j]);

detw(h,U,V,R,W) =
{
  my(H2=[sum(i=1,6,aa[i]*m2[i]),sum(i=1,6,bb[i]*m2[i]),W]);
  matdet(L+ww*jacvec(H2)+ww^2*jacvec([U,V,R])+ww^3*jacvec([h^2,h*x^2,0]));
};

checktop(dd,label) =
{
  for(j=7,9,checkeq(polcoeff(dd,j,ww),0,Str(label," E",j)));
};

\\ RT-reducible/CS and RT-smooth/CS.
check_rt_cs(slice) =
{
  my(h=if(slice==1,y*z,x^2+y*z));
  my(dd=detw(h,A*x*y*z,B*x*y*z,x^3,T*y*z));
  my(forced6=[a1,a2,a3,a5,b1,b2,b3,b5,l7,l8]);
  my(d6=subst_many(polcoeff(dd,6,ww),forced6,vector(#forced6)));
  my(e5=subst_many(polcoeff(dd,5,ww),forced6,vector(#forced6)));
  checktop(dd,Str("RT/CS ",slice));
  checkeq(d6,0,Str("RT/CS E6 ",slice));
  checkeq(coeffxyz(e5,[2,2,1]),-6*l4,Str("RT/CS l4 ",slice));
  checkeq(coeffxyz(e5,[2,1,2]),6*l5,Str("RT/CS l5 ",slice));
  checkeq(subst_many(matdet(L),concat(forced6,[l1,l2,l4,l5]),vector(14)),0,Str("RT/CS singular ",slice));
};
check_rt_cs(1);
check_rt_cs(2);

\\ RT-reducible/CH and RT-smooth/CH.
check_rt_ch(slice) =
{
  my(h=if(slice==1,y*z,x^2+y*z));
  my(U=A*x^3-2*C*y*h-2*D*z*h);
  my(V=B*x^3+C*x^2*y+D*x^2*z);
  my(dd_a0=detw(h,subst(U,A,0),V,x*h,T*x^2));
  my(vars6=[a1,a2,a3,a5,b1,b2,b3,b5]);
  my(vals6=[2*C*(3*B-4*T),2*D*(3*B-4*T),3*C^2,3*D^2,2*l7,2*l8,0,0]);
  my(e5a=subst_many(polcoeff(dd_a0,5,ww),vars6,vals6));
  my(dd_cd0=detw(h,subst_many(U,[C,D],[0,0]),subst_many(V,[C,D],[0,0]),x*h,T*x^2));
  my(vals_cd0=[0,0,0,0,2*l7,2*l8,0,0]);
  my(cfac=6*B-8*T);
  my(forced5=[l1,l2,l4,l5]);
  my(values5=[cfac*l7,cfac*l8,0,0]);
  checktop(dd_a0,Str("RT/CH A0 ",slice));
  checkeq(subst_many(polcoeff(dd_a0,6,ww),vars6,vals6),0,Str("RT/CH A0 E6 ",slice));
  checkeq(coeffxyz(e5a,[2,3,0]),-12*C^3,Str("RT/CH C cube ",slice));
  checkeq(coeffxyz(e5a,[2,0,3]),12*D^3,Str("RT/CH D cube ",slice));
  checkeq(subst_many(polcoeff(dd_cd0,6,ww),vars6,vals_cd0),0,Str("RT/CH CD0 E6 ",slice));
  checkeq(subst_many(matdet(L),concat(vars6,forced5),concat(vals_cd0,values5)),0,Str("RT/CH singular ",slice));
};
check_rt_ch(1);
check_rt_ch(2);

\\ RO-smooth/CS.
h=y^2+x*z;
dd_ros=detw(h,2*A*z*h,A*x^2*z+B*x*h+2*C*y*h/3,x^3,C*x*y+S*h);
checktop(dd_ros,"RO/CS");
vars_ros=[a1,a2,a4,a5,b1,b2,b4,b5,l7,l8];
vals_ros=[0,a3,0,A^2,0,A*B+b3,2*A*C/3,0,-B*C/2,(6*A*S-C^2)/6];
checkeq(subst_many(polcoeff(dd_ros,6,ww),vars_ros,vals_ros),0,"RO/CS E6");
e5ros=subst_many(polcoeff(dd_ros,5,ww),vars_ros,vals_ros);
checkeq(coeffxyz(e5ros,[2,0,3]),-2*C^3/9,"RO/CS C cube");
forced_ros=[C,l1,l2,l4,l5];
values_ros=[0,0,A*a3,0,A*b3];
checkeq(subst_many(subst_many(matdet(L),vars_ros,vals_ros),forced_ros,values_ros),0,"RO/CS singular");

\\ RO-smooth/CH, A=0 component.
U=A*x^3-2*C*y*h-2*D*z*h+2*T*z*h;
V=B*x^3+C*x^2*y+(D+T)*x^2*z;
dd_roa=detw(h,subst(U,A,0),V,x*h,T*x*z);
checktop(dd_roa,"RO/CH A0");
vars_roh=[a1,a2,a4,a5,b1,b2,b4,b5];
vals_roa=[6*B*C,6*B*D-3*C^2+a3,2*C*(3*D-T),3*D^2-2*D*T+T^2,2*l7,b3+2*l8,0,0];
checkeq(subst_many(polcoeff(dd_roa,6,ww),vars_roh,vals_roa),0,"RO/CH A0 E6");
e5roa=subst_many(polcoeff(dd_roa,5,ww),vars_roh,vals_roa);
q=a0-9*B^2;
checkeq(coeffxyz(e5roa,[5,0,0]),2*C*q,"RO/CH Cq");
checkeq(coeffxyz(e5roa,[4,1,0]),-4*(D*q+6*B*C^2),"RO/CH Dq");
checkeq(coeffxyz(e5roa,[3,2,0])-coeffxyz(e5roa,[4,0,1]),12*C*(6*B*D-C^2),"RO/CH C chain");
e5roc=subst(e5roa,C,0);
checkeq(coeffxyz(e5roc,[0,5,0]),4*((D-T)*b3+l5),"RO/CH D chain 1");
checkeq(coeffxyz(e5roc,[1,3,1]),8*((D-T)*b3-2*D*l8+l5),"RO/CH D chain 2");
checkeq(coeffxyz(e5roc,[2,1,2]),4*(6*D^3+(D-T)*b3-4*D*l8+l5),"RO/CH D chain 3");

\\ RO-smooth/CH, C=D=0 component and its genuine E5 survivor.
dd_roc=detw(h,subst_many(U,[C,D],[0,0]),subst_many(V,[C,D],[0,0]),x*h,T*x*z);
vals_roc=[0,a3,0,T^2,2*l7,b3+2*l8,0,0];
checkeq(subst_many(polcoeff(dd_roc,6,ww),vars_roh,vals_roc),0,"RO/CH CD0 E6");
e5roc=subst_many(polcoeff(dd_roc,5,ww),vars_roh,vals_roc);
checkeq(coeffxyz(e5roc,[5,0,0]),3*A*l7,"RO/CH A l7");
checkeq(coeffxyz(e5roc,[4,1,0]),-6*A*l8,"RO/CH A l8");
forced_ro5=[l1,l2,l4,l5];
values_ro5=[6*B*l7,6*B*l8+T*a3,0,T*b3];
det_ro5=subst_many(subst_many(matdet(L),vars_roh,vals_roc),forced_ro5,values_ro5);
checkeq(det_ro5,T*l7*(6*B*b3*l6+a3*l3-b3*l0),"RO/CH E5 determinant");
e4roc=subst_many(subst_many(polcoeff(dd_roc,4,ww),vars_roh,vals_roc),forced_ro5,values_ro5);
e4roc=subst(e4roc,A,0);
checkeq(coeffxyz(e4roc,[1,1,2]),-8*l8^2,"RO/CH E4 l8 square");
checkeq(coeffxyz(e4roc,[2,1,1]),-4*(2*b0*l8-2*l6*l8-l7^2),"RO/CH E4 l7 square");

\\ Sharp through-E5 witness.
sharpL=[1,0,0;0,0,1;0,1,0];
sharpH2=[z^2,2*x*y+x*z+y^2,x*z];
sharpH3=[2*z*h,x^2*z,x*h];
sharpD=matdet(sharpL+ww*jacvec(sharpH2)+ww^2*jacvec(sharpH3)+ww^3*jacvec([h^2,h*x^2,0]));
checkeq(matdet(sharpL),-1,"sharp det L");
for(j=5,9,checkeq(polcoeff(sharpD,j,ww),0,Str("sharp E",j)));
checkeq(polcoeff(sharpD,4,ww),4*x*y*h,"sharp E4");

print("SIX_ENDPOINTS_E5_E4_PARI_PASS_682F1B");
print("independent PARI reconstruction confirms the sharp RO/H E5 survivor and E4 obstruction");
quit;
