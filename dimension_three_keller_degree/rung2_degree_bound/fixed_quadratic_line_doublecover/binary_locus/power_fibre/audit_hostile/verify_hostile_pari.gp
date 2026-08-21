\\ Independent exact reconstruction of the exceptional power-fibre algebra.
\\
\\ This file deliberately does not import the primary SymPy expansion.  It
\\ builds a completely general homogeneous family and expands the determinant
\\ with the six-term Leibniz formula in PARI/GP.

default(parisizemax, 1200000000);

FAULT_SIGN = if(getenv("AUDIT_FAULT_SIGN") == "1", 1, 0);
FAULT_COEFF = if(getenv("AUDIT_FAULT_COEFF") == "1", 1, 0);
FAULT_ORBIT = if(getenv("AUDIT_FAULT_ORBIT") == "1", 1, 0);

fail(msg) =
{
  print("FAIL ", msg);
  quit(1);
};

check0(value, msg) =
{
  if(value != 0, fail(Str(msg, ": residual = ", value)));
  print("PASS ", msg);
};

checkeq(left, right, msg) = check0(left - right, msg);

det3(M) =
{
  M[1,1]*M[2,2]*M[3,3]
  + M[1,2]*M[2,3]*M[3,1]
  + M[1,3]*M[2,1]*M[3,2]
  - M[1,3]*M[2,2]*M[3,1]
  - M[1,2]*M[2,1]*M[3,3]
  - M[1,1]*M[2,3]*M[3,2];
};

jrow(f) = [deriv(f,p), deriv(f,q), deriv(f,r)];

cpqr(f, ip, iq, ir) =
  polcoeff(polcoeff(polcoeff(f, ip, p), iq, q), ir, r);
cpq(f, ip, iq) = polcoeff(polcoeff(f, ip, p), iq, q);
cr(f, ir) = polcoeff(f, ir, r);
\\ Close substitutions under themselves.  This is intentional: many branch
\\ formulae contain parameters that are set on the same boundary, and a single
\\ simultaneous substitution would recreate the classic dependent-formula
\\ hazard this audit is meant to catch.
S(f, vars, vals) =
{
  my(g=f, h, k=1);
  while(k <= #vars+2,
    h=substvec(g,vars,vals);
    if(h==g, return(g));
    g=h;
    k++;
  );
  g;
};

\\ -------------------------------------------------------------------------
\\ 1. Full family and complete E7 solve.
\\ -------------------------------------------------------------------------

main_v9() =
{
T = c0*p^2 + c1*p*q + c2*q^2 + tp*p*r + tq*q*r + tt*r^2;

Ug = (u0*p^3 + u1*p^2*q + u2*p*q^2 + u3*q^3
   + ug4*p^2*r + ug5*p*q*r + ug6*q^2*r
   + ug7*p*r^2 + ug8*q*r^2 + ug9*r^3);

V = (v0*p^3 + v1*p^2*q + v2*p*q^2 + v3*q^3
  + v4*p^2*r + v5*p*q*r + v6*q^2*r
  + v7*p*r^2 + v8*q*r^2 + v9*r^3);

A = x0*p^2 + x1*p*q + x2*q^2 + ap*p*r + aq*q*r + aa*r^2;
B = y0*p^2 + y1*p*q + y2*q^2 + bp*p*r + bq*q*r + bb*r^2;

H4s = if(FAULT_SIGN, -1, 1);
P4 = p^4;
Q4 = H4s*p^2*q^2;
R3 = p^3;

L = matrix(3,3);
L[1,1]=l11; L[1,2]=l12; L[1,3]=l13;
L[2,1]=l21; L[2,2]=l22; L[2,3]=l23;
L[3,1]=l31; L[3,2]=l32; L[3,3]=l33;

J2 = matrix(3,3,i,j,[jrow(A),jrow(B),jrow(T)][i][j]);
J3g = matrix(3,3,i,j,[jrow(Ug),jrow(V),jrow(R3)][i][j]);
J4 = matrix(3,3,i,j,[jrow(P4),jrow(Q4),[0,0,0]][i][j]);
Mg = matrix(3,3,i,j,L[i,j] + z*J2[i,j] + z^2*J3g[i,j] + z^3*J4[i,j]);
Dg = det3(Mg);

E7g = polcoeff(Dg, 7, z);
expected_E7g = 2*p^4*q*(4*p*deriv(T,r) - 3*deriv(Ug,r));
checkeq(E7g, expected_E7g, "Leibniz reconstruction of the generic E7 identity");
check0(polcoeff(Dg,9,z), "weight nine vanishes");
check0(polcoeff(Dg,8,z), "weight eight vanishes");

K7 = 4*p*deriv(T,r) - 3*deriv(Ug,r);
checkeq(cpqr(K7,2,0,0), 4*tp-3*ug4, "E7 p^2 coefficient");
checkeq(cpqr(K7,1,1,0), 4*tq-3*ug5, "E7 pq coefficient");
checkeq(cpqr(K7,0,2,0), -3*ug6, "E7 q^2 coefficient");
checkeq(cpqr(K7,1,0,1), 8*tt-6*ug7, "E7 pr coefficient");
checkeq(cpqr(K7,0,1,1), -6*ug8, "E7 qr coefficient");
checkeq(cpqr(K7,0,0,2), -9*ug9, "E7 r^2 coefficient");

rho = if(FAULT_COEFF, 5/3, 4/3);
D = S(Dg,
      [ug4,ug5,ug6,ug7,ug8,ug9],
      [rho*tp,rho*tq,0,rho*tt,0,0]);
E7 = polcoeff(D,7,z);
check0(E7, "parameterized E7 family is identically zero");

E6 = polcoeff(D,6,z);
E5 = polcoeff(D,5,z);
E4 = polcoeff(D,4,z);
E3 = polcoeff(D,3,z);
detL = det3(L);

\\ -------------------------------------------------------------------------
\\ 2. The v9 != 0 branch, including every pivot boundary.
\\ -------------------------------------------------------------------------

checkeq(cr(E6,3), 16/3*p^2*q*tt^2,
        "v9 branch: E6[r^3] forces tt=0");

E6tt = S(E6,[tt],[0]);
checkeq(cpq(cr(E6tt,2),4,0),3*v9*(3*u1-4*c1),
        "v9 branch: E6 p^4 r^2");
checkeq(cpq(cr(E6tt,2),3,1),6*v9*(3*u2-4*c2),
        "v9 branch: E6 p^3 q r^2");
checkeq(cpq(cr(E6tt,2),2,2),27*v9*u3,
        "v9 branch: E6 p^2 q^2 r^2");

Vtop = [tt,u1,u2,u3];
Wtop = [0,4/3*c1,4/3*c2,0];
E5top = S(E5,Vtop,Wtop);
checkeq(cr(E5top,4),-4*tq*v9*(p*tp+q*tq),
        "v9 branch: E5[r^4] forces tq=0");

E6topq0 = S(E6,Vtop,Wtop);
E6topq0 = S(E6topq0,[tq],[0]);
checkeq(cr(E6topq0,1),-4/3*p^4*q*(9*aa-2*tp^2),
        "v9 branch: E6[r] forces aa=2 tp^2/9");

Vpre = [tt,u1,u2,u3,tq,aa,aq,ap];
Wpre = [0,4/3*c1,4/3*c2,0,0,2/9*tp^2,4/9*c1*tp,
        (12*l33+tp*(9*u0-8*c0))/9];
E6pre = S(E6,Vpre,Wpre);
expected = 2/3*p^2*q*(
  p^3*(-9*ap-8*c0*tp+12*l33+9*tp*u0)
 +p^2*q*(-9*aq+4*c1*tp)
 +4*c2*p*q^2*tp);
E6before = S(E6,[tt,u1,u2,u3,tq,aa],
                  [0,4/3*c1,4/3*c2,0,0,2/9*tp^2]);
checkeq(cr(E6before,0),expected,
        "v9 branch: complete E6[r^0] pivot polynomial");
checkeq(E6pre,8/3*c2*tp*p^3*q^3,
        "v9 branch: sole residual E6 equation is c2*tp=0");

E5pre = S(E5,Vpre,Wpre);
E5pre_tp0 = S(E5pre,[tp],[0]);
checkeq(cpq(cr(E5pre_tp0,2),0,3),-8*c2^2*v9,
        "v9 branch: tp=0 forces c2=0");

Vbase = concat(Vpre,[c2,x1,x2]);
Wbase = concat(Wpre,[0,
  4/3*l32-c1*(8*c0-9*u0)/9,
  2/9*c1^2+4*tp^3/(81*v9)]);
E5base = S(E5,Vbase,Wbase);
check0(cr(E5base,2), "v9 branch: complete E5[r^2] solution");

\\ tp != 0.  Normalize c0=c1=0 only after the division-free top solve.
E5n = S(E5base,[c0,c1],[0,0]);
checkeq(cpq(cr(E5n,1),3,1),
        16*tp*(9*l33*v9+tp^2*v7)/(27*v9),
        "v9*tp branch: E5 forces v7");
checkeq(cpq(cr(E5n,1),2,2),16*tp^3*v8/(27*v9),
        "v9*tp branch: E5 forces v8");
checkeq(cpq(cr(E5n,0),4,1),
        2*(-81*l13*v9-36*l31*tp*v9+81*l33*u0*v9
           +4*tp^3*v4+54*tp*v9*x0)/(27*v9),
        "v9*tp branch: E5 forces l13");
checkeq(cpq(cr(E5n,0),3,2),8*tp*(9*l32*v9+tp^2*v5)/(27*v9),
        "v9*tp branch: E5 forces v5");
checkeq(cpq(cr(E5n,0),2,3),8*tp^3*(-2*tp+3*v6)/(81*v9),
        "v9*tp branch: E5 forces v6");

Vn = [v7,v8,v6,v5,l13];
Wn = [-9*l33*v9/tp^2,0,2/3*tp,-9*l32*v9/tp^2,
      -4/9*l31*tp+l33*u0+4*tp^3*v4/(81*v9)+2/3*tp*x0];
E6n = S(S(S(E6,Vbase,Wbase),[c0,c1],[0,0]),Vn,Wn);
E5nsol = S(E5n,Vn,Wn);
check0(E6n, "v9*tp branch: E6 remains zero after full E5 solve");
check0(E5nsol, "v9*tp branch: full E5 solution");
E4n = S(S(S(E4,Vbase,Wbase),[c0,c1],[0,0]),Vn,Wn);
checkeq(cr(E4n,3),-8/27*q*tp^4,
        "v9*tp branch terminal E4 obstruction");

\\ tp=0.  The E5 constant-r polynomial includes both c1*l33 and l13.
E5z = S(E5base,[tp],[0]);
checkeq(cr(E5z,0),2/3*p^3*q*(
  p*(-8*c0*l33-9*l13+9*l33*u0)+4*c1*l33*q),
  "v9,tp=0: complete E5[r^0] boundary polynomial");

E4c1 = S(E4,[tt,tq,tp,c2,u1,u2,u3,aa,aq,ap,x1,x2,l33,l13],
  [0,0,0,0,4/3*c1,0,0,0,0,0,
   4/3*l32-c1*(8*c0-9*u0)/9,2/9*c1^2,0,0]);
checkeq(cpq(cr(E4c1,2),0,2),4/3*c1^3*v9,
        "v9,tp=0,c1!=0 terminal E4 obstruction");

\\ On c1=0, E4[r^2] first fixes l12, and only then E4[r] fixes l33.
E4c10pre = S(E4,
 [tt,tq,tp,c1,c2,u1,u2,u3,aa,aq,ap,x1,x2,l13],
 [0,0,0,0,0,0,0,0,0,0,4/3*l33,4/3*l32,0,
  l33*(u0-8/9*c0)]);
checkeq(cpq(cr(E4c10pre,2),2,0),
        -v9*(-8*c0*l32-9*l12+9*l32*u0),
        "v9,tp=c1=0: E4[r^2] forces l12");
E4c10 = S(E4c10pre,[l12],[l32*(u0-8/9*c0)]);
checkeq(cr(E4c10,1),8/3*p^2*q*l33^2,
        "v9,tp=c1=0: E4[r] forces l33=0");

E3last = S(E3,
 [tt,tq,tp,c1,c2,u1,u2,u3,aa,aq,ap,x1,x2,l13,l12,l33],
 [0,0,0,0,0,0,0,0,0,0,0,4/3*l32,0,0,
  l32*(u0-8/9*c0),0]);
linlast = 8*c0^2*p-9*c0*u0*p-6*l31*p+6*l32*q+9*x0*p;
checkeq(cr(E3last,2),-2/3*l32*v9*linlast,
        "v9,tp=c1=0: final E3 factor");
checkeq(cpq(linlast,0,1),6*l32,
        "v9,tp=c1=0: noncancellable q coefficient");
check0(S(detL,[l12,l13,l32,l33],[0,0,0,0]),
       "v9 final zero-l32 leaf has singular L");
};

main_v9();

\\ -------------------------------------------------------------------------
\\ 3. q and p+q orbits on v9=0.
\\ -------------------------------------------------------------------------

check_q_orbit(ep) =
{
  my(eq, OV, OW, e5r3, expect5, TV, TW, e6r0, SV, SW, e5r2,
     BV, BW, e5r1, CV, CW, e5r0, e4r1pre, ZV, ZW, e4r1, base,
     e4sol, e4r0, z33, e3r1z, nz, e4nz, e3r2, e4pq, e4q2,
     e3p, e3q, prefinal, raw40, raw31, finalV, finalW, final30);

  eq = if(ep==1 && FAULT_ORBIT, 2, 1);
  OV=[v9,v7,v8,tt]; OW=[0,ep,eq,0];
  e5r3=cr(S(E5,OV,OW),3);
  if(ep==0,
    expect5=-2/3*(p^2*(9*aa-2*tp^2)+2*q^2*tq^2),
    expect5=-2/3*(p^2*(9*aa-2*tp^2+4*tp*tq)
                       +4*p*q*tq^2+2*q^2*tq^2));
  checkeq(e5r3,expect5,Str("orbit ",if(ep,"p+q","q"),
          ": E5[r^3] top split"));

  TV=concat(OV,[tq,aa,u1,u2,u3]);
  TW=concat(OW,[0,2/9*tp^2,4/3*c1,4/3*c2,0]);
  check0(cr(S(E6,TV,TW),1),Str("orbit ",if(ep,"p+q","q"),
         ": complete E6[r] solution"));
  check0(cr(S(E5,TV,TW),3),Str("orbit ",if(ep,"p+q","q"),
         ": complete E5[r^3] solution"));

  e6r0=cr(S(E6,TV,TW),0);
  checkeq(cpq(e6r0,5,1),2/3*(-9*ap-8*c0*tp+12*l33+9*tp*u0),
          Str("orbit ",if(ep,"p+q","q"),": E6 ap pivot"));
  checkeq(cpq(e6r0,4,2),2/3*(-9*aq+4*c1*tp),
          Str("orbit ",if(ep,"p+q","q"),": E6 aq pivot"));
  checkeq(cpq(e6r0,3,3),8/3*c2*tp,
          Str("orbit ",if(ep,"p+q","q"),": E6 c2*tp pivot"));

  SV=concat(TV,[ap,aq]);
  SW=concat(TW,[(12*l33+tp*(9*u0-8*c0))/9,4/9*c1*tp]);
  e5r2=cr(S(E5,SV,SW),2);
  checkeq(cpq(e5r2,2,1),-8/9*tp^3-16/3*ep*c2*tp,
          Str("orbit ",if(ep,"p+q","q"),": E5 forces tp=0"));

  BV=[v9,v7,v8,tt,tq,tp,aa,u1,u2,u3,ap,aq];
  BW=[0,ep,1,0,0,0,0,4/3*c1,4/3*c2,0,4/3*l33,0];
  e5r1=cr(S(E5,BV,BW),1);
  checkeq(cpq(e5r1,0,4),-16/3*c2^2,
          Str("orbit ",if(ep,"p+q","q"),": E5 forces c2=0"));

  CV=concat(BV,[c2,u2,x1,x2]);
  CW=concat(BW,[0,0,4/3*l32-c1*(8*c0-9*u0)/9,2/9*c1^2]);
  check0(cr(S(E5,CV,CW),1),Str("orbit ",if(ep,"p+q","q"),
         ": complete E5[r] solution"));
  e5r0=cr(S(E5,CV,CW),0);
  checkeq(e5r0,2/3*p^3*q*(
      p*(-8*c0*l33-9*l13+9*l33*u0)+4*c1*l33*q),
      Str("orbit ",if(ep,"p+q","q"),": complete E5[r^0]"));
  e4r1pre=cr(S(E4,CV,CW),1);
  checkeq(cpq(e4r1pre,0,3),8/9*c1^3,
      Str("orbit ",if(ep,"p+q","q"),": E4 forces c1=0"));

  ZV=[v9,v7,v8,tt,tq,tp,aa,u1,u2,u3,ap,aq,c1,c2,x1,x2,l13];
  ZW=[0,ep,1,0,0,0,0,0,0,0,4/3*l33,0,0,0,4/3*l32,0,
      l33*(u0-8/9*c0)];
  e4r1=cr(S(E4,ZV,ZW),1);
  base=-8*c0*l32-9*l12+9*l32*u0;

  check0(ep*(cpq(e4r1,3,0)+2/3*base),
         "p+q orbit: first E4[r] pivot");
  check0(ep*(cpq(e4r1,2,1)+2/3*(base-4*l33^2)),
         "p+q orbit: second E4[r] pivot");
  e3r1z=cr(S(E3,
    concat(ZV,[l33,l13,l12]),
    concat(ZW,[0,0,l32*(u0-8/9*c0)])),1);
  check0(ep*(cpq(e3r1z,0,2)+8/3*l32^2),
         "p+q orbit: E3 forces l32=0");
  check0(S(detL,[l12,l13,l32,l33],[0,0,0,0]),
         "p+q orbit: terminal L is singular");

  check0((1-ep)*(cpq(e4r1,2,1)+2/3*(base-4*l33^2)),
         "q orbit: E4[r] fixes l12");
  e4sol=S(S(E4,ZV,ZW),[l12],
          [l32*(u0-8/9*c0)-4/9*l33^2]);
  e4r0=cr(e4sol,0);
  check0((1-ep)*(cpq(e4r0,4,0)+4/3*v4*l33^2),
         "q orbit: l33!=0 forces v4=0");

  z33=S(E3,
    concat(ZV,[l33,l13,l12]),
    concat(ZW,[0,0,l32*(u0-8/9*c0)]));
  e3r1z=cr(z33,1);
  check0((1-ep)*(cpq(e3r1z,0,2)+8/3*l32^2),
         "q orbit: l33=0 forces l32=0");
  check0(S(detL,[l12,l13,l32,l33],[0,0,0,0]),
         "q orbit: l33=0 terminal L is singular");

  nz=S(e4sol,[v4],[0]);
  e4nz=cr(nz,0);
  e3r2=cr(S(S(E3,ZV,ZW),
      [l12,v4],[l32*(u0-8/9*c0)-4/9*l33^2,0]),2);
  e4pq=cpq(e4nz,3,1); e4q2=cpq(e4nz,2,2);
  e3p=cpq(e3r2,1,0); e3q=cpq(e3r2,0,1);
  check0((1-ep)*(e3p-e4pq/2-2*l33^2*v5),
         "q orbit: l33!=0 forces v5=0");
  check0((1-ep)*(e4q2+2*e3q-4*l33^2*v6),
         "q orbit: l33!=0 forces v6=0");
  check0((1-ep)*(2*e4q2+e3q-4*l33*l32),
         "q orbit: l33!=0 forces l32=0");

  prefinal = S(S(E4,ZV,ZW),
    [l12,v4,v5,v6,l32],
    [-4/9*l33^2,0,0,0,0]);
  raw40=cr(prefinal,0);
  check0((1-ep)*(cpq(raw40,3,1)
    -4*l33*(8*c0^2-9*c0*u0-6*l31+9*x0)/9),
    "q orbit: E4 fixes l31");
  raw31=cr(S(S(E3,ZV,ZW),
    [l12,v4,v5,v6,l32,l31],
    [-4/9*l33^2,0,0,0,0,
     (8*c0^2-9*c0*u0+9*x0)/6]),1);
  check0((1-ep)*(cpq(raw31,2,0)-4/3*l33^2*(-2*bb+v1)),
         "q orbit: E3 fixes bb");
  check0((1-ep)*(cpq(raw31,1,1)-8/9*l33^2*(-2*c0+3*v2)),
         "q orbit: E3 fixes v2");
  check0((1-ep)*(cpq(raw31,0,2)-4*l33^2*v3),
         "q orbit: E3 fixes v3");

  finalV=concat(ZV,[l12,v4,v5,v6,l32,l31,bb,v2,v3]);
  finalW=concat(ZW,[-4/9*l33^2,0,0,0,0,
    (8*c0^2-9*c0*u0+9*x0)/6,v1/2,2/3*c0,0]);
  check0((1-ep)*cr(S(E4,finalV,finalW),0),"q orbit: final E4 equations");
  check0((1-ep)*cr(S(E3,finalV,finalW),2),"q orbit: final E3[r^2] equations");
  check0((1-ep)*cr(S(E3,finalV,finalW),1),"q orbit: final E3[r] equations");
  final30=cr(S(E3,finalV,finalW),0);
  check0((1-ep)*(cpq(final30,1,2)-8/9*l33^3),
         "q orbit: l33!=0 terminal E3 obstruction");
};

check_q_orbit(0);
check_q_orbit(1);

\\ -------------------------------------------------------------------------
\\ 4. The p orbit, with all tp/aa pivot boundaries.
\\ -------------------------------------------------------------------------

main_p_and_zero() =
{
PV=[v9,v7,v8,tt]; PW=[0,1,0,0];
checkeq(cr(S(E5,PV,PW),3),-8/3*p*tq*(p*tp+q*tq),
        "p orbit: E5[r^3] forces tq=0");

PTV=concat(PV,[tq,u1,u2,u3]);
PTW=concat(PW,[0,4/3*c1,aa+4/3*c2-2/9*tp^2,0]);
check0(cr(S(E6,PTV,PTW),1),"p orbit: complete E6[r] solution");
pe6=cpq(cr(S(E6,PTV,PTW),0),3,3);
pe5=cpq(cr(S(E5,PTV,PTW),2),2,1);
checkeq(pe5+2*pe6,-2/9*tp*(27*aa-2*tp^2),
        "p orbit: exhaustive tp/aa split");

PNV=[v9,v7,v8,tt,tq,c0,c1,aa,c2,u1,u2,u3,ap,aq];
PNW=[0,1,0,0,0,0,0,2/27*tp^2,
     -tp^2/9+tp*v6/3,0,4/9*tp*v6-8/27*tp^2,0,
     4/3*l33-4/27*tp^2*v4+tp*u0,-4/27*tp^2*v5];
check0(cr(S(E6,PNV,PNW),1),"p,tp!=0: E6[r] solution");
check0(cr(S(E6,PNV,PNW),0),"p,tp!=0: complete E6 solution");
check0(cr(S(E5,PNV,PNW),2),"p,tp!=0: complete E5[r^2] solution");
p51=cr(S(E5,PNV,PNW),1);
checkeq(cpq(p51,1,3),-16/81*tp^2*(tp^2-tp*v6+3*v6^2),
        "p,tp!=0: E5 necessary coefficient");
p43=cr(S(E4,PNV,PNW),3);
checkeq(cpq(p43,1,0),-8/27*tp^3*v5,
        "p,tp!=0: E4 forces v5=0");
checkeq(cpq(p43,0,1),-8/243*tp^3*(tp+6*v6),
        "p,tp!=0: E4 forces v6=-tp/6");
checkeq(S(cpq(p51,1,3),[v6],[-tp/6]),-20/81*tp^4,
        "p,tp!=0: terminal E5 obstruction");

PZV=[v9,v7,v8,tt,tq,tp,u1,u2,u3,ap,aq];
PZW=[0,1,0,0,0,0,4/3*c1,aa+4/3*c2,0,
     aa*v4+4/3*l33,aa*v5];
checkeq(cr(S(E6,PZV,PZW),0),6*aa*p^3*q^3*v6,
        "p,tp=0: sole residual E6 equation is aa*v6=0");
checkeq(cpq(cr(S(E6,PZV,PZW),0),3,3),6*aa*v6,
        "p,tp=0: aa*v6 pivot");

PAV=concat(PZV,[v6,c1,c2,u1,u2,x1,x2,v3]);
PAW=concat(PZW,[0,0,0,0,aa,aa*v1+4/3*l32,
                aa*(v2-bb),0]);
pa43=cr(S(E4,PZV,PZW),3);
pa43=S(pa43,[v6],[0]);
checkeq(cpq(pa43,1,0),2*aa*c1,
        "p,tp=0,aa!=0: E4 forces c1=0");
checkeq(cpq(pa43,0,1),4*aa*c2,
        "p,tp=0,aa!=0: E4 forces c2=0");
check0(cr(S(E5,PAV,PAW),1),"p,aa!=0: complete E5[r] solution");
pa42=cr(S(E4,PAV,PAW),2);
checkeq(cpq(pa42,1,1),-2*aa*l33,
        "p,aa!=0: E4 forces l33=0");
checkeq(cpq(pa42,2,0),6*aa*(bb*v5-bq),
        "p,aa!=0: E4 fixes bq");

PALV=concat(PAV,[l33,ap,bq,l13]);
PALW=concat(PAW,[0,aa*v4,bb*v5,aa*(bp-bb*v4)]);
check0(cr(S(E5,PALV,PALW),0),"p,aa!=0: complete E5[r^0] solution");
pa41=cr(S(E4,PALV,PALW),1);
checkeq(cpq(pa41,1,2),2*aa*l32,
        "p,aa!=0: E4 forces l32=0");

PAEV=concat(PALV,[l32,x1,y2,l12]);
PAEW=concat(PALW,[0,aa*v1,bb*(v2-bb),aa*(y1-bb*v1)]);
check0(cr(S(E4,PAEV,PAEW),1),"p,aa!=0: complete E4[r] solution");
pa40=cr(S(E4,PAEV,PAEW),0);
checkeq(cpq(pa40,3,1),6*aa*(bb^2*v4-bb*bp+l23),
        "p,aa!=0: E4 fixes l23");
pa31=cr(S(E3,concat(PAEV,[l23]),
                   concat(PAEW,[bb*(bp-bb*v4)])),1);
checkeq(cpq(pa31,2,0),6*aa*(bb*(y1-bb*v1)-l22),
        "p,aa!=0: E3 fixes l22");
PAFV=concat(PAEV,[l23,l22]);
PAFW=concat(PAEW,[bb*(bp-bb*v4),bb*(y1-bb*v1)]);
check0(S(detL,PAFV,PAFW),"p,aa!=0: forced L is singular");

\\ aa=0 boundary.
P0V=[v9,v7,v8,tt,tq,tp,aa,u1,u2,u3,ap,aq];
P0W=[0,1,0,0,0,0,0,4/3*c1,4/3*c2,0,4/3*l33,0];
p051=cr(S(E5,P0V,P0W),1);
checkeq(cpq(p051,1,3),-16/3*c2^2,
        "p,tp=aa=0: E5 forces c2=0");
P0SV=concat(P0V,[c2,u2,x1,x2]);
P0SW=concat(P0W,[0,0,4/3*l32-c1*(8*c0-9*u0)/9,2/9*c1^2]);
check0(cr(S(E5,P0SV,P0SW),1),"p,tp=aa=0: complete E5[r] solution");
p050=cr(S(E5,P0SV,P0SW),0);
checkeq(cpq(p050,3,2),8/3*c1*l33,
        "p,tp=aa=0: E5 c1*l33 boundary");
P0C1V=concat(P0SV,[l33,ap,l13]);
P0C1W=concat(P0SW,[0,0,0]);
checkeq(cpq(cr(S(E4,P0C1V,P0C1W),1),1,2),8/9*c1^3,
        "p,tp=aa=0,c1!=0 terminal E4 obstruction");

P0ZV=[v9,v7,v8,tt,tq,tp,aa,u1,u2,u3,ap,aq,c1,c2,x1,x2,l13];
P0ZW=[0,1,0,0,0,0,0,0,0,0,4/3*l33,0,0,0,4/3*l32,0,
      l33*(u0-8/9*c0)];
checkeq(cpq(cr(S(E4,P0ZV,P0ZW),1),2,1),8/3*l33^2,
        "p,tp=aa=c1=0: E4 forces l33=0");
P0lastV=concat(P0ZV,[l33,ap,l13,l12]);
P0lastW=concat(P0ZW,[0,0,0,l32*(u0-8/9*c0)]);
checkeq(cpq(cr(S(E3,P0lastV,P0lastW),1),1,1),-8/3*l32^2,
        "p,tp=aa=c1=0: E3 forces l32=0");
check0(S(detL,[l12,l13,l32,l33],[0,0,0,0]),
       "p,tp=aa=c1=0: terminal L is singular");

\\ -------------------------------------------------------------------------
\\ 5. Zero orbit top collapse.
\\ -------------------------------------------------------------------------

ZOV=[v9,v7,v8,tt]; ZOW=[0,0,0,0];
checkeq(cr(S(E6,ZOV,ZOW),1),
  -4/3*p^2*q*(9*aa*p^2-2*(tp*p+tq*q)^2),
  "zero orbit: complete E6[r] identity");
ZTV=concat(ZOV,[tq,aa]);
ZTW=concat(ZOW,[0,2/9*tp^2]);
checkeq(cr(S(E5,ZTV,ZTW),2),-8/9*p^2*q*tp^3,
        "zero orbit: E5 forces tp=0");

print("ALL HOSTILE PARI ALGEBRA CHECKS PASSED");
};

main_p_and_zero();
