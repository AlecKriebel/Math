# Approach 4: characteristic classes detect the full defect

Status: a necessary-and-sufficient numerical certificate for the natural sequence is proved; the required vanishing is not established under the unrestricted source hypotheses.

Let X=P^n over C, H a smooth hypersurface, A a reduced divisor sharing no component with H, and R=(A|H)_red. Put F=D_X(A), G=D_X(A+H), E=D_H(R), and let i:H -> X. The natural restriction map exists, has kernel F(-H), and has coherent cokernel i_*Q by Approach 3. Thus
[F(-H)]-[G]+[i_*E]=[i_*Q]
in K_0(X). No local freeness of these logarithmic sheaves is assumed; coherent sheaves on smooth X have finite locally free resolutions.

Let h=c_1(O_X(H)), h_H=i^*h, and use rational Chow groups. Grothendieck–Riemann–Roch for the smooth Cartier inclusion gives
Delta = e^(-h) ch(F)-ch(G)+i_*[ch(E)(1-e^(-h_H))/h_H]
      = ch(i_*Q).
The fraction denotes its finite formal power series in the Chow ring; no division by a possibly zero class is intended.

## Exactness criterion

The natural restriction is onto if and only if Delta=0. The forward implication is immediate. Conversely Delta=0 and Hirzebruch–Riemann–Roch imply
chi(X,i_*Q(t))= integral_X Delta e^(t u) td(T_X)=0
for every integer t, where u is the hyperplane class. A nonzero coherent sheaf on a projective scheme has a nonzero Hilbert polynomial with positive leading coefficient: by a prime filtration of its graded section module, the top-dimensional terms have positive generic lengths and positive projective degrees. Equivalently, Serre vanishing and global generation imply that for all sufficiently large t a nonzero sheaf has positive h^0 and no higher cohomology. Therefore Q=0.

More generally, equality of the three Hilbert polynomials
P_G(t)=P_{F(-H)}(t)+P_{i_*E}(t)
is equivalent to exactness. One may compute the polynomial defect directly instead of using a Chern-class conversion.

## Why the tempting shortcuts do not finish the problem

This criterion requires the entire rational Chern character or the entire Hilbert polynomial, together with the already constructed map and kernel. Equality of ranks, determinants or selected low-degree Chern components is insufficient. For instance the skyscraper sheaf of one point in P^3 has ch=(0,0,0,[point]); it is invisible to rank and the first two Chern-character components, although its Hilbert polynomial is the constant one.

Liao's comparison between logarithmic Chern and Chern–Schwartz–MacPherson classes has local-freeness/quasihomogeneity hypotheses in higher dimension. Additivity of CSM classes alone is not an identification of the above K-theory defect, and those hypotheses cannot be silently dropped. The seven-plane example gives an actual nonzero defect. No identity forcing Delta=0 for all source arrangements has been derived. This route supplies a faithful conditional use of characteristic classes, rather than the requested unconditional higher-dimensional theorem.

The GRR, Serre and Hilbert-polynomial inputs are standard imported results; their general proofs are not rederived here. All deductions from them are given above. No novelty claim is made.
