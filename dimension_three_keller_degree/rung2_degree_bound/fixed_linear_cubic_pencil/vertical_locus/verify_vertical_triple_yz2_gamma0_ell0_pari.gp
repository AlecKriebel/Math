\\ Independent PARI/GP certificate for q=x^3+y*z^2, W=w*z^2.

must(condition, message) = {
  if(!condition,
    print(Str("FAIL: ", message));
    quit(1)
  )
};

x='x; y='y; z='z;
s='s; w='w; k='k;
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
q=x^3+y*z^2;
Vgeneral=v0*x^3+v1*x^2*y+v2*x*y^2+v3*y^3 \
       +v4*x^2*z+v5*x*y*z+v6*y^2*z+v7*x*z^2+v8*y*z^2;
L=[l0,l1,l2;l3,l4,l5;l6,l7,l8];
L1=l0*x+l1*y+l2*z;
L2=l3*x+l4*y+l5*z;
L3=l6*x+l7*y+l8*z;
P=z^4;
Q=z*q;
R=z^3;
U=4*z*W/3+s*q;

jac3(first,second,third)=matdet(matrix(3,3,i,j, \
  deriv([first,second,third][i],vars[j])));
coefficient(P,i,j,h)=polcoef(polcoef(polcoef(P,i,x),j,y),h,z);
homogeneous_part(P,degree)=
{
  my(answer=0);
  for(i=0,degree,
    for(j=0,degree-i,
      my(h=degree-i-j);
      answer += coefficient(P,i,j,h)*x^i*y^j*z^h;
    )
  );
  answer;
};

\\ Exterior-multilinear reconstruction, not a replay of the full
\\ weighted-matrix determinant used by the SymPy certificate.
E8=jac3(P,Q,R);
E7=jac3(P,Q,W)+jac3(U,Q,R)+jac3(P,Vgeneral,R);
must(E8==0, "E8 survives");
must(E7==0, "E7 survives");

E6general=jac3(P,Q,L3)+jac3(U,Q,W)+jac3(P,Vgeneral,W) \
  +jac3(A,Q,R)+jac3(U,Vgeneral,R)+jac3(P,B,R);

\\ Complete E6 rank sandwich.
e6_monomials=[[4,0,2],[3,1,2],[3,0,3],[2,2,2],[2,1,3],[2,0,4], \
  [1,1,4],[1,0,5],[0,2,4],[0,1,5],[0,0,6]];
e6=vector(#e6_monomials,i, \
  coefficient(E6general,e6_monomials[i][1],e6_monomials[i][2], \
                  e6_monomials[i][3]));
e6_unknowns=[v0,v1,v2,v3,v4,v5,v6,v7,v8,l6,l7];
e6_matrix=matrix(#e6,#e6_unknowns,i,j,deriv(e6[i],e6_unknowns[j]));
e6_rows=[1,2,3,4,5,6,8,11];
e6_columns=[1,2,3,4,5,6,7,8];
must(matdet(vecextract(e6_matrix,e6_rows,e6_columns)) \
  ==-114791256*s^8,"literal E6 minor");

Vsolution=k*q+z*(A-a5*z^2)/s-4*z^2*(l6*x+l7*y)/(3*s);
E6solution=jac3(P,Q,L3)+jac3(U,Q,W)+jac3(P,Vsolution,W) \
  +jac3(A,Q,R)+jac3(U,Vsolution,R)+jac3(P,B,R);
must(E6solution==0, "displayed E6 family");

\\ The complete E5 system.
E5solution=jac3(U,Q,L3)+jac3(P,Vsolution,L3) \
  +jac3(A,Q,W)+jac3(U,Vsolution,W)+jac3(P,B,W) \
  +jac3(L1,Q,R)+jac3(A,Vsolution,R)+jac3(U,B,R) \
  +jac3(P,L2,R);
e5_monomials=[[5,0,0],[3,0,2],[2,1,2],[2,0,3], \
  [1,0,4],[0,1,4],[0,0,5]];
e5=vector(#e5_monomials,i, \
  coefficient(E5solution,e5_monomials[i][1],e5_monomials[i][2], \
                       e5_monomials[i][3]));
e5_unknowns=[b0,b1,b2,b3,b4,l6,l7];
e5_matrix=matrix(#e5,#e5_unknowns,i,j,deriv(e5[i],e5_unknowns[j]));
must(matdet(e5_matrix)==104976*s^7, "literal E5 determinant");
must(e5[1]==-3*l7*s, "E5 coefficient killing l32");
must(e5[2]+3*e5[6]==4*l6*s, "E5 combination killing l31");

Bsolution=(a0*k/s)*x^2+(a1*k/s)*x*y+(a2*k/s)*y^2 \
        +((a3*k+l0)/s)*x*z+((a4*k+l1)/s)*y*z+b5*z^2;
Vafter_e5=k*q+z*(A-a5*z^2)/s;
L3after=l8*z;
E6after=jac3(P,Q,L3after)+jac3(U,Q,W)+jac3(P,Vafter_e5,W) \
  +jac3(A,Q,R)+jac3(U,Vafter_e5,R)+jac3(P,Bsolution,R);
E5after=jac3(U,Q,L3after)+jac3(P,Vafter_e5,L3after) \
  +jac3(A,Q,W)+jac3(U,Vafter_e5,W)+jac3(P,Bsolution,W) \
  +jac3(L1,Q,R)+jac3(A,Vafter_e5,R)+jac3(U,Bsolution,R) \
  +jac3(P,L2,R);
must(E6after==0, "E6 after E5 solve");
must(E5after==0, "E5 displayed solution");

E4after=jac3(A,Q,L3after)+jac3(U,Vafter_e5,L3after) \
  +jac3(P,Bsolution,L3after)+jac3(L1,Q,W) \
  +jac3(A,Vafter_e5,W)+jac3(U,Bsolution,W)+jac3(P,L2,W) \
  +jac3(L1,Vafter_e5,R)+jac3(A,Bsolution,R)+jac3(U,L2,R);
expected_e4=9*(-k*l1+s*l4)*x^2*z^2 \
  -3*(-k*l0+s*l3)*z^4;
must(E4after==expected_e4, "complete E4 residual");

Lfinal=[l0,l1,l2;k*l0/s,k*l1/s,l5;0,0,l8];
L2final=k*l0*x/s+k*l1*y/s+l5*z;
E4final=jac3(A,Q,L3after)+jac3(U,Vafter_e5,L3after) \
  +jac3(P,Bsolution,L3after)+jac3(L1,Q,W) \
  +jac3(A,Vafter_e5,W)+jac3(U,Bsolution,W)+jac3(P,L2final,W) \
  +jac3(L1,Vafter_e5,R)+jac3(A,Bsolution,R)+jac3(U,L2final,R);
must(E4final==0, "final E4");
must(matdet(Lfinal)==0, "linear matrix not singular");

print("VERTICAL_TRIPLE_YZ2_GAMMA0_ELL0_PARI_PASS_7B16E9");
quit(0);
