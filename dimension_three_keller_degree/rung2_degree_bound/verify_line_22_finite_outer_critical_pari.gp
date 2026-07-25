\\ Independent PARI/GP checks for WORKING_LINE_22_FINITE_OUTER_CRITICAL.md.
\\
\\ This is deliberately not a translation of the SymPy matrix-rank code.
\\ It recomputes determinant coefficients directly in PARI and checks the
\\ decisive displayed identities on the three certified loci.

x='x; y='y; z='z; s='s;

gradmat(F) = matrix(3, 3, i, j, deriv(F[i], [x,y,z][j]));
jac3(f,g,h) = matdet(gradmat([f,g,h]));
wcoef(L,H2,H3,H4,k) = polcoeff( \
  matdet(gradmat(L+s*H2+s^2*H3+s^3*H4)), k, s);
delta(f) = z*deriv(f,z)-y*deriv(f,y);
cf(P,i,j,k) = polcoeff(polcoeff(polcoeff(P,i,x),j,y),k,z);
check(label, value) = {
  if (value != 0, \
    print(Str("FAIL ", label, ": ", value)); \
    quit(1));
  print(Str("  PASS ", label));
};

p=x^2; q=y*z;
a='a; b='b; c='c;

\\ -------------------------------------------------------------------------
\\ 1. Full-moduli finite-companion E7 identity.

U3g=ou0*x^3+ou1*x^2*y+ou2*x^2*z+ou3*x*y^2+ou4*x*y*z \
    +ou5*x*z^2+ou6*y^3+ou7*y^2*z+ou8*y*z^2+ou9*z^3;
V3g=ov0*x^3+ov1*x^2*y+ov2*x^2*z+ov3*x*y^2+ov4*x*y*z \
    +ov5*x*z^2+ov6*y^3+ov7*y^2*z+ov8*y*z^2+ov9*z^3;
W2g=ow0*x^2+ow1*x*y+ow2*x*z+ow3*y^2+ow4*y*z+ow5*z^2;
H41=(p-a*q)^2; H42=(p-b*q)^2; R=x*(p-c*q);
E7=jac3(H41,H42,W2g)+jac3(H41,V3g,R)+jac3(U3g,H42,R);
E7display=2*( \
  4*x*(a-b)*(p-a*q)*(p-b*q)*delta(W2g) \
 +(p-b*q)*((3*b-2*c)*p-b*c*q)*delta(U3g) \
 +(p-a*q)*((2*c-3*a)*p+a*c*q)*delta(V3g));
check("open E7 displayed identity", E7-E7display);

\\ The normalized E6 vanishes after the ten forced coefficients are removed,
\\ and E5 is exactly the six-term expression in the note.
AA='AA; BB='BB;
H4o=[H41,H42,0];
H3o=[AA*x*q,BB*x*q,x*(p-c*q)];
H2o=[u0*p+u4*q,v0*p+v4*q,w0*p+wq*q];
Lo=[l0*x+l1*y+l2*z,l3*x+l4*y+l5*z,l6*x];
check("open normalized E6", wcoef(Lo,H2o,H3o,H4o,6));
E5o=wcoef(Lo,H2o,H3o,H4o,5);
E5oExpected= \
  2*(3*a*l4-3*b*l1+2*c*l1-2*c*l4)*x^4*y \
 -2*(3*a*l5-3*b*l2+2*c*l2-2*c*l5)*x^4*z \
 -2*(3*a^2*l4-a*c*l4-3*b^2*l1+b*c*l1)*x^2*y^2*z \
 +2*(3*a^2*l5-a*c*l5-3*b^2*l2+b*c*l2)*x^2*y*z^2 \
 +2*c*(a^2*l4-b^2*l1)*y^3*z^2 \
 -2*c*(a^2*l5-b^2*l2)*y^2*z^3;
check("open normalized E5 six-term formula", E5o-E5oExpected);

\\ -------------------------------------------------------------------------
\\ 2. Noncritical c=0 triple branch.

t='t;
fac=4*(t-1)/(3*t);
H4t=[(p-t*q)^2,(p-q)^2,0];
H3t=[uk*x*q, \
  vk*x*q+fac*sy*(x^2*y-y^2*z)+fac*sz*(x^2*z-y*z^2), \
  x^3];
U2t=tu0*p+tu1*x*y+tu2*x*z+tu3*y^2+tu4*q+tu5*z^2;
V2t=tv0*p+tv1*x*y+tv2*x*z+tv3*y^2+tv4*q+tv5*z^2;
W2t=tw0*p+sy*x*y+sz*x*z+twq*q;
Lt=[tl0*x+tl1*y+tl2*z,tl3*x+tl4*y+tl5*z,tl6*x+tl7*y+tl8*z];
E6t=wcoef(Lt,[U2t,V2t,W2t],H3t,H4t,6);
check("c=0 coefficient y^4 z^2", \
  cf(E6t,0,4,2)-8*t*(t-1)*sy^2/3);
check("c=0 coefficient y^2 z^4", \
  cf(E6t,0,2,4)+8*t*(t-1)*sz^2/3);

\\ -------------------------------------------------------------------------
\\ 3. Marked-critical finite-other-point orbit.

H4m=[p^2,(p-q)^2,0];
Vm=mv0*x^3+mv1*x^2*y+mv2*x^2*z+mv3*x*y^2+mv4*x*y*z \
   +mv5*x*z^2+mv6*y^3+mv7*y^2*z+mv8*y*z^2+mv9*z^3;
Wm=mw0*p+mwy*x*y+mwz*x*z+mwyy*y^2+mwq*q+mwzz*z^2;
Um=4*x*Wm/3+msigma*x^3+mB*x*q;
E7m=jac3(p^2,(p-q)^2,Wm)+jac3(p^2,Vm,x^3) \
    +jac3(Um,(p-q)^2,x^3);
check("marked E7 factorization", \
  E7m-2*x*p*(p-q)*delta(3*Um-4*x*Wm));

\\ On total resonance, first check the B!=0 normalized representative.
Ur=4*(mwy*x^2*y+mwz*x^2*z)/3;
Vr=mC*x*q;
Wr=mw0*p+mwy*x*y+mwz*x*z+mwq*q;
U2r=ru0*p+ru1*x*y+ru2*x*z+2*mwy^2*y^2/9+ru4*q \
    +2*mwz^2*z^2/9;
V2r=rv0*p+rv1*x*y+rv2*x*z+rv3*y^2+rv4*q+rv5*z^2;
Lr=[rl0*x+rl1*y+rl2*z,rl3*x+rl4*y+rl5*z, \
    rl6*x+(9*ru1+8*mw0*mwy+8*mwy*mwq)*y/12 \
         +(9*ru2+8*mw0*mwz+8*mwz*mwq)*z/12];
E6r=wcoef(Lr,[U2r,V2r,Wr],[Ur,Vr,x^3],H4m,6);
check("marked resonant normalized E6", E6r);
E5r=wcoef(Lr,[U2r,V2r,Wr],[Ur,Vr,x^3],H4m,5);
check("marked resonant y^4 z cube", \
  cf(E5r,0,4,1)-8*mwy^3/9);
check("marked resonant y z^4 cube", \
  cf(E5r,0,1,4)+8*mwz^3/9);

\\ At B=mwq=0 the same cubes survive with completely arbitrary V3.
Wr0=mw0*p+mwy*x*y+mwz*x*z;
Lr0=[rl0*x+rl1*y+rl2*z,rl3*x+rl4*y+rl5*z, \
     rl6*x+(9*ru1+8*mw0*mwy)*y/12 \
          +(9*ru2+8*mw0*mwz)*z/12];
E6r0=wcoef(Lr0,[subst(U2r,mwq,0),V2r,Wr0],[Ur,Vm,x^3],H4m,6);
check("marked endpoint arbitrary-V E6", E6r0);
E5r0=wcoef(Lr0,[subst(U2r,mwq,0),V2r,Wr0],[Ur,Vm,x^3],H4m,5);
check("marked endpoint arbitrary-V y^4 z cube", \
  cf(E5r0,0,4,1)-8*mwy^3/9);
check("marked endpoint arbitrary-V y z^4 cube", \
  cf(E5r0,0,1,4)+8*mwz^3/9);

\\ Uniform invariant-V exit.
A='A; D='D;
U2f=fu0*p+fuy*x*y+fuz*x*z+fuq*q;
V2f=fv0*p+fvy*x*y+fvz*x*z+fvyy*y^2+fvq*q+fvzz*z^2;
W2f=fw0*p+fwq*q;
Lf=[fl0*x+fl1*y+fl2*z,fl3*x+fl4*y+fl5*z, \
    fl6*x+3*fuy*y/4+3*fuz*z/4];
H3f=[A*x*q,D*x*q,x^3];
check("marked invariant-V E6",wcoef(Lf,[U2f,V2f,W2f],H3f,H4m,6));
E5f=wcoef(Lf,[U2f,V2f,W2f],H3f,H4m,5);
check("marked invariant-V E5 y^3 z^2", \
  cf(E5f,0,3,2)+3*A*fuy/2);
check("marked invariant-V E5 y^2 z^3", \
  cf(E5f,0,2,3)-3*A*fuz/2);
E4f=subst(wcoef(Lf,[U2f,V2f,W2f],H3f,H4m,4),A,0);
check("marked invariant-V E4 y^3 z square", \
  cf(E4f,0,3,1)+3*fuy^2/2);
check("marked invariant-V E4 y z^3 square", \
  cf(E4f,0,1,3)-3*fuz^2/2);

\\ The exceptional B=0, mwq!=0, Delta=0 chart.  E6,E5,E4 vanish after
\\ their forced substitutions, while E3 retains two squares.
rq='rq; r0='r0;
ca='ca; cb='cb; cg='cg; cd='cd; cr='cr;
Sy=ca+cb; Sz=cg+cd;
V3e=ev0*x^3+ca*x^2*y+cg*x^2*z+cr*x*y*z \
    +cb*y^2*z+cd*y*z^2;
H3e=[4*rq*x*q/3,V3e,x^3];
ueq=(4*rq^2-8*r0*rq)/9;
U2e=eu0*p+2*cb*rq*x*y/3+2*cd*rq*x*z/3+ueq*q;
evy=2*Sy*(r0+rq)/3+cr*cb/2;
evz=2*Sz*(r0+rq)/3+cr*cd/2;
V2e=evv0*p+evy*x*y+evz*x*z+cb^2*y^2/4+evvq*q+cd^2*z^2/4;
W2e=r0*p+rq*q;
el1=-(4*rq^2*ca+8*r0*rq*cb)/18;
el2=-(4*rq^2*cg+8*r0*rq*cd)/18;
el6=3*eu0/2+4*r0^2/3-2*r0*rq/3-cr*rq/2;
Le=[el0*x+el1*y+el2*z,el3*x+el4*y+el5*z, \
    el6*x+cb*rq*y/2+cd*rq*z/2];
check("marked exceptional E6",wcoef(Le,[U2e,V2e,W2e],H3e,H4m,6));
check("marked exceptional E5",wcoef(Le,[U2e,V2e,W2e],H3e,H4m,5));
check("marked exceptional E4",wcoef(Le,[U2e,V2e,W2e],H3e,H4m,4));
E3e=wcoef(Le,[U2e,V2e,W2e],H3e,H4m,3);
check("marked exceptional E3 xy^2 square", \
  cf(E3e,1,2,0)-4*rq^3*Sy^2/9);
check("marked exceptional E3 xz^2 square", \
  cf(E3e,1,0,2)+4*rq^3*Sz^2/9);

print("PASS: independent PARI/GP finite-outer-critical line-(2,2) identities");
quit
