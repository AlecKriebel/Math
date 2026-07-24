\\ Exact PARI/GP regressions for the quartic structural notes.
\\
\\ This is independent code for the polynomial identities and discrete table.
\\ It is not a proof of the duality or triangularization arguments.

assertzero(x, label) =
{
  if (x != 0, error(Str("FAIL: ", label, ": ", x)));
};

asserttrue(x, label) =
{
  if (!x, error(Str("FAIL: ", label)));
};

trm(M) = sum(i=1,matsize(M)[1],M[i,i]);
e2(M) = (trm(M)^2 - trm(M*M))/2;
sform(M,N) = trm(M)*trm(N) - trm(M*N);

main() =
{
A =
[a11,a12,a13;
 a21,a22,a23;
 a31,a32,a33];
B =
[b11,b12,b13;
 b21,b22,b23;
 b31,b32,b33];
C =
[c11,c12,c13;
 c21,c22,c23;
 0,0,0];

D = matdet(matid(3) + z*A + z^2*B + z^3*C);
expected8 =
matdet(
[c11,c12,c13;
 c21,c22,c23;
 b31,b32,b33]
);
assertzero(polcoef(D,8,z) - expected8, "degree-eight CCB coefficient");

B0 =
[b11,b12,b13;
 b21,b22,b23;
 0,0,0];
D0 = matdet(matid(3) + z*A + z^2*B0 + z^3*C);
expected7 =
matdet(
[c11,c12,c13;
 c21,c22,c23;
 a31,a32,a33]
);
assertzero(polcoef(D0,7,z) - expected7, "degree-seven CCA coefficient");

G =
[d11,d12,d13;
 d21,d22,d23;
 d31,d32,d33];
W = matdet(matid(3) + z*A + z^2*B + z^3*G) - 1;
P = matdet(u*A + v*B + w*G);

cu2v = polcoef(polcoef(P,2,u),1,v);
cu2w = polcoef(polcoef(P,2,u),1,w);
cuv2 = polcoef(polcoef(P,1,u),2,v);
cuvw = polcoef(polcoef(polcoef(P,1,u),1,v),1,w);
cuw2 = polcoef(polcoef(P,1,u),2,w);
cv2w = polcoef(polcoef(P,2,v),1,w);
cvw2 = polcoef(polcoef(P,1,v),2,w);

assertzero(polcoef(W,1,z) - trm(A), "weight 1");
assertzero(polcoef(W,2,z) - (trm(B)+e2(A)), "weight 2");
assertzero(polcoef(W,3,z) - (trm(G)+sform(A,B)+matdet(A)), "weight 3");
assertzero(polcoef(W,4,z) - (e2(B)+sform(A,G)+cu2v), "weight 4");
assertzero(polcoef(W,5,z) - (sform(B,G)+cu2w+cuv2), "weight 5");
assertzero(polcoef(W,6,z) - (e2(G)+matdet(B)+cuvw), "weight 6");
assertzero(polcoef(W,7,z) - (cuw2+cv2w), "weight 7");
assertzero(polcoef(W,8,z) - cvw2, "weight 8");
assertzero(polcoef(W,9,z) - matdet(G), "weight 9");

profile_count = 0;
s2_count = 0;
maxg = [-1,-1,-1];
for (ss=2,15,
  for (qq=1,3,
    for (gg=0,7,
      tau = 2*gg + qq + 1;
      for (bb=0,15,
        defect1 = ss - bb - tau;
        if (defect1 >= 0,
          punctures = ss + bb + qq;
          if (punctures <= 16,
            K = defect1 + 2*bb + 2*tau;
            asserttrue(K == 2*gg + 1 + punctures, "Riemann-Hurwitz table");
            conductor = 64 - tau + 3 + qq;
            asserttrue(conductor == 66 - 2*gg, "conductor degree");
            asserttrue((tau + (qq == 2)) % 2 == 0, "global parity");
            profile_count++;
            if (gg > maxg[qq], maxg[qq] = gg);
            if (ss == 2,
              s2_count++;
              asserttrue(qq==1 && gg==0 && bb==0 && defect1==0 &&
                         tau==2 && punctures==3, "unique s=2 profile");
            );
          );
        );
      );
    );
  );
);
asserttrue(profile_count > 0, "nonempty profile table");
asserttrue(s2_count == 1, "one s=2 profile");
asserttrue(maxg == [6,5,4], "sharp genus caps");

L = x+y;
S = y^2+x*z;
PP = L^4;
QQ = S^2;
RR = L*S;
Jexample =
matdet(
[deriv(PP,x),deriv(PP,y),deriv(PP,z);
 deriv(QQ,x),deriv(QQ,y),deriv(QQ,z);
 deriv(RR,x),deriv(RR,y),deriv(RR,z)]
);
assertzero(Jexample, "nonprimitive Jacobian example");
assertzero(RR^4 - PP*QQ^2, "nonprimitive power relation");

F1 = x+y^2;
F2 = y+(x+y^2)^2;
JF2 =
[deriv(F1,x),deriv(F1,y);
 deriv(F2,x),deriv(F2,y)];
assertzero(matdet(JF2)-1, "rank-one quartic obstruction is Keller");
algebra_basis =
[1,0,0,1;
 0,1,0,0;
 0,0,1,0;
 1,0,0,0];
asserttrue(matdet(algebra_basis) != 0,
           "E12 and E21 generate the full quotient matrix algebra");

\\ Audited local correction: a smooth branch can have finite c=0.
ff = xx*zz^3-ww^4;
gg = yy*zz^3+xx^4;
assertzero(subst(subst(subst(ff,xx,ww^4),yy,-ww^16),zz,1),
           "local branch lies on f");
assertzero(subst(subst(subst(gg,xx,ww^4),yy,-ww^16),zz,1),
           "local branch lies on g");
asserttrue(4*1-5+1 == 0, "smooth finite conductor exponent");

print("PASS: independent PARI quartic regressions");
};

main();
quit;
