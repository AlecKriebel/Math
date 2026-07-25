\\ Exterior-multilinear PARI/GP certificate for all W=w*z^2 triple charts.

must(condition, message) = {
  if(!condition,
    print(Str("FAIL: ", message));
    quit(1)
  )
};

x='x; y='y; z='z;
s='s; w='w; k='k; alpha='alpha;
a0='a0; a1='a1; a2='a2; a3='a3; a4='a4; a5='a5;
b0='b0; b1='b1; b2='b2; b3='b3; b4='b4; b5='b5;
v0='v0; v1='v1; v2='v2; v3='v3; v4='v4;
v5='v5; v6='v6; v7='v7; v8='v8;
l0='l0; l1='l1; l2='l2; l3='l3; l4='l4;
l5='l5; l6='l6; l7='l7; l8='l8;

vars=[x,y,z];
A=a0*x^2+a1*x*y+a2*y^2+a3*x*z+a4*y*z+a5*z^2;
B=b0*x^2+b1*x*y+b2*y^2+b3*x*z+b4*y*z+b5*z^2;
W=w*z^2;
Vgeneral=v0*x^3+v1*x^2*y+v2*x*y^2+v3*y^3 \
       +v4*x^2*z+v5*x*y*z+v6*y^2*z+v7*x*z^2+v8*y*z^2;
L1=l0*x+l1*y+l2*z;
L2=l3*x+l4*y+l5*z;
L3=l6*x+l7*y+l8*z;
P=z^4;
R=z^3;

jac3(first,second,third)=matdet(matrix(3,3,i,j, \
  deriv([first,second,third][i],vars[j])));
coefficient(PP,i,j,h)=polcoef(polcoef(polcoef(PP,i,x),j,y),h,z);

audit_chart(qform,e6mons,e6unknowns,e6expected, \
            e5mons,e5expected,e4expected,label) = {
  my(Q=z*qform,U=4*z*W/3+s*qform);
  my(E8=jac3(P,Q,R));
  my(E7=jac3(P,Q,W)+jac3(U,Q,R)+jac3(P,Vgeneral,R));
  my(E6general,E6,Vsolution,E6solution);
  my(E5solution,E5,e6matrix,e5matrix);
  my(Bsolution,Vafter,L3after,E6after,E5after,E4after);
  my(L2final,Lfinal,E4final);

  must(E8==0,Str(label,": E8"));
  must(E7==0,Str(label,": E7"));

  E6general=jac3(P,Q,L3)+jac3(U,Q,W)+jac3(P,Vgeneral,W) \
    +jac3(A,Q,R)+jac3(U,Vgeneral,R)+jac3(P,B,R);
  E6=vector(#e6mons,i, \
    coefficient(E6general,e6mons[i][1],e6mons[i][2],e6mons[i][3]));
  e6matrix=matrix(#E6,#e6unknowns,i,j,deriv(E6[i],e6unknowns[j]));
  must(matdet(e6matrix)==e6expected*s^8,Str(label,": E6 minor"));

  Vsolution=k*qform+z*(A-a5*z^2)/s-4*z^2*(l6*x+l7*y)/(3*s);
  E6solution=jac3(P,Q,L3)+jac3(U,Q,W)+jac3(P,Vsolution,W) \
    +jac3(A,Q,R)+jac3(U,Vsolution,R)+jac3(P,B,R);
  must(E6solution==0,Str(label,": E6 family"));

  E5solution=jac3(U,Q,L3)+jac3(P,Vsolution,L3) \
    +jac3(A,Q,W)+jac3(U,Vsolution,W)+jac3(P,B,W) \
    +jac3(L1,Q,R)+jac3(A,Vsolution,R)+jac3(U,B,R) \
    +jac3(P,L2,R);
  E5=vector(#e5mons,i, \
    coefficient(E5solution,e5mons[i][1],e5mons[i][2],e5mons[i][3]));
  e5matrix=matrix(#E5,7,i,j,deriv(E5[i], \
    [b0,b1,b2,b3,b4,l6,l7][j]));
  must(matdet(e5matrix)==e5expected*s^7,Str(label,": E5 minor"));

  Bsolution=(a0*k/s)*x^2+(a1*k/s)*x*y+(a2*k/s)*y^2 \
    +((a3*k+l0)/s)*x*z+((a4*k+l1)/s)*y*z+b5*z^2;
  Vafter=k*qform+z*(A-a5*z^2)/s;
  L3after=l8*z;
  E6after=jac3(P,Q,L3after)+jac3(U,Q,W)+jac3(P,Vafter,W) \
    +jac3(A,Q,R)+jac3(U,Vafter,R)+jac3(P,Bsolution,R);
  E5after=jac3(U,Q,L3after)+jac3(P,Vafter,L3after) \
    +jac3(A,Q,W)+jac3(U,Vafter,W)+jac3(P,Bsolution,W) \
    +jac3(L1,Q,R)+jac3(A,Vafter,R)+jac3(U,Bsolution,R) \
    +jac3(P,L2,R);
  must(E6after==0,Str(label,": E6 after E5"));
  must(E5after==0,Str(label,": full E5 solution"));

  E4after=jac3(A,Q,L3after)+jac3(U,Vafter,L3after) \
    +jac3(P,Bsolution,L3after)+jac3(L1,Q,W) \
    +jac3(A,Vafter,W)+jac3(U,Bsolution,W)+jac3(P,L2,W) \
    +jac3(L1,Vafter,R)+jac3(A,Bsolution,R)+jac3(U,L2,R);
  must(E4after==e4expected,Str(label,": complete E4"));

  L2final=k*l0*x/s+k*l1*y/s+l5*z;
  E4final=jac3(A,Q,L3after)+jac3(U,Vafter,L3after) \
    +jac3(P,Bsolution,L3after)+jac3(L1,Q,W) \
    +jac3(A,Vafter,W)+jac3(U,Bsolution,W)+jac3(P,L2final,W) \
    +jac3(L1,Vafter,R)+jac3(A,Bsolution,R)+jac3(U,L2final,R);
  Lfinal=[l0,l1,l2;k*l0/s,k*l1/s,l5;0,0,l8];
  must(E4final==0,Str(label,": final E4"));
  must(matdet(Lfinal)==0,Str(label,": singular L"));
  print(Str("  PASS ",label));
};

q1=x^3+y^2*z+alpha*x*z^2;
q1_e6mons=[[4,0,2],[3,1,2],[3,0,3],[2,2,2], \
  [2,1,3],[2,0,4],[1,1,4],[0,1,5]];
q1_e6unknowns=[v0,v1,v2,v3,v4,v5,v7,v8];
q1_e5mons=[[5,0,0],[3,1,1],[3,0,2],[2,1,2], \
  [2,0,3],[1,1,3],[0,1,4]];
q1_e4=9*(-k*l1+s*l4)*x^2*z^2 \
  -6*(-k*l0+s*l3)*y*z^3 \
  +3*alpha*(-k*l1+s*l4)*z^4;
audit_chart(q1,q1_e6mons,q1_e6unknowns,-459165024, \
  q1_e5mons,629856,q1_e4,"quadratic-y chart");

q2=x^3+x*y*z;
q2_e6mons=[[4,0,2],[3,1,2],[3,0,3],[2,2,2], \
  [2,1,3],[2,0,4],[1,0,5],[0,1,5]];
q2_e6unknowns=[v0,v1,v2,v3,v4,v6,v7,v8];
q2_e5mons=[[5,0,0],[4,0,1],[3,0,2],[2,1,2], \
  [2,0,3],[1,0,4],[0,1,4]];
q2_e4=9*(-k*l1+s*l4)*x^2*z^2 \
  -3*(-k*l0+s*l3)*x*z^3 \
  +3*(-k*l1+s*l4)*y*z^3;
audit_chart(q2,q2_e6mons,q2_e6unknowns,38263752, \
  q2_e5mons,26244,q2_e4,"mixed-xy chart");

q3=x^3+y*z^2;
q3_e6mons=[[4,0,2],[3,1,2],[3,0,3],[2,2,2], \
  [2,1,3],[2,0,4],[1,0,5],[0,0,6]];
q3_e6unknowns=[v0,v1,v2,v3,v4,v5,v6,v7];
q3_e5mons=[[5,0,0],[3,0,2],[2,1,2],[2,0,3], \
  [1,0,4],[0,1,4],[0,0,5]];
q3_e4=9*(-k*l1+s*l4)*x^2*z^2 \
  -3*(-k*l0+s*l3)*z^4;
audit_chart(q3,q3_e6mons,q3_e6unknowns,-114791256, \
  q3_e5mons,104976,q3_e4,"linear-y chart");

print("VERTICAL_TRIPLE_GAMMA0_ELL0_PARI_PASS_6D291C");
quit(0);
