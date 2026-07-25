# A semiregular \(C_{37}\) conference-lift frontier at order 334

## Why this would solve \(H(668)\)

A normalized symmetric conference matrix of order 334 has the form

\[
C=\begin{pmatrix}0&\mathbf 1^T\\ \mathbf 1&S\end{pmatrix},
\qquad
C^2=333I_{334}.
\]

Its \(333\times333\) core therefore satisfies

\[
S\mathbf1=0,\qquad S^2=333I_{333}-J_{333}.
\]

The standard conference doubling construction would turn such a matrix
into a Hadamard matrix of order 668.  Equivalently,
\((J-I-S)/2\) would be a conference graph with parameters

```text
(v,k,lambda,mu) = (333,166,82,83).
```

The existing `conference_333_group_obstruction/` theorem excludes cores
developed regularly over a group of order 333.  It does **not** exclude a
core with only a semiregular \(C_{37}\) action and nine vertex orbits.  This
folder studies that strictly broader family.

## The obvious order-10/order-38 product fails

The factorization \(333=9\cdot37\) suggests combining normalized symmetric
conference cores of sizes 9 and 37.  Let

\[
B_m^2=mI-J,\qquad B_n^2=nI-J,
\qquad B_mJ=JB_m=B_nJ=JB_n=0.
\]

The raw tensor \(B_m\otimes B_n\) has forbidden off-diagonal zeros.  The
natural Turyn-style correction fills them:

\[
W=B_m\otimes B_n+I_m\otimes J_n-J_m\otimes I_n.
\]

It has the required zero-diagonal/sign pattern, but exact multiplication
gives

\[
W^2=mnI-J_m\otimes J_n+
(n-m)(I_m\otimes J_n-J_m\otimes I_n).
\]

The extra term vanishes only when \(m=n\).  For \(m=9,n=37\), its
coefficient is 28, so this obvious mixed product cannot produce the desired
333-vertex core.  This excludes only the displayed repair, not all possible
product constructions.

## Exact zero-frequency quotient

Index the 333 core vertices by nine fibers of size 37 and require every
`37 x 37` block to be circulant.  Let \(T\) be the symmetric `9 x 9`
matrix of block row sums.  Fourier transformation on \(C_{37}\) gives the
necessary trivial-character equations

\[
T\mathbf1=0,\qquad T^2=333I_9-37J_9.
\]

Diagonal entries of \(T\) are even sums of 36 signs; off-diagonal entries
are odd sums of 37 signs.

Unlike the earlier Cayley quotient, this system is feasible.  The
certificate contains the explicit matrix

```text
   0 -11  -3   7  -3   7  -3   7  -1
 -11  -4   7  -1   7  -1   7  -1  -3
  -3   7   0 -11  -3   7  -3   7  -1
   7  -1 -11  -4   7  -1   7  -1  -3
  -3   7  -3   7   0 -11  -3   7  -1
   7  -1   7  -1 -11  -4   7  -1  -3
  -3   7  -3   7  -3   7   0 -11  -1
   7  -1   7  -1   7  -1 -11  -4  -3
  -1  -3  -1  -3  -1  -3  -1  -3  16
```

It is not a solver accident.  The verifier reconstructs it from four
norm-\(333=18^2+3^2\) planes on an explicit orthogonal basis of the
\(A_8\) lattice obtained from the Sylvester Hadamard matrix of order eight.

After a global sign and a permutation, the same quotient has a hidden
`1+4+4` normal form

```text
[-16]        1^4                     3^4
 1^4   0 I + 3(J-I)         11 I - 7(J-I)
 3^4  11 I - 7(J-I)          4 I + 1(J-I).
```

The verifier derives the first row rather than assuming it: diagonal
entry `-16`, row sum zero, and squared norm 296 force the other entries to
be `1^4,3^4`.  Inside this diagonal-\(S_4\) block algebra, the displayed
completion is unique.  This normal form is signed/permutation equivalent
to the certified \(A_8\) quotient, not a second equivalence class.

The corresponding equitable adjacency quotient has row sum 166 and
satisfies

\[
B^2+B=83I_9+83\cdot37J_9.
\]

Thus the new conference lane survives its first exact necessary condition.

## Complete classification of the quotient layer

The zero-frequency system is now exhausted, rather than represented by one
seed.  An orderly exact enumeration gives

```text
196,560,000 fully labeled matrices;
625 classes under simultaneous row/column permutation;
314 classes after also identifying global sign.
```

The enumeration starts from all 411 possible unordered row types, or
2,109,524 ordered rows, and directly rechecks the full square equation for
every terminal matrix.  Independent canonicalization reproduces all 625
classes and the labeled total by orbit-stabilizer.

There are 111 diagonal multisets, but no quotient has all nine diagonal
entries zero.  This closes the alternative `(0,9)` trace branch globally:
up to residue/nonresidue interchange, every lift of every feasible quotient
must obey the `6/3` diagonal-incidence law derived below.  The displayed
`1+4+4` quotient and its negative are the unique maximally symmetric
sign-class, with automorphism order 24.

Modulo two, the 625 integral quotient classes collapse to only three
adjacency-quotient types under fiber permutation, and only two after
complement.  Their integral preimage counts are `206,213,206`; the binary
automorphism orders are `24,20,24`.  This collapse is what makes the
all-quotient characteristic-two bound nearly as small as the fixed-seed
bound.

The exact theorem, exceptional representatives, parity graphs, asserted
enumerator, and independent audits are recorded in `QUOTIENT_CENSUS.md`.

## Three exact lift obstructions

### Paley three-class blocks

Suppose each circulant block is constant on displacement zero, the 18
nonzero quadratic residues, and the 18 nonresidues of \(\mathbf F_{37}\).
The trivial Fourier block then has diagonal entries in
`\{0,+/-36\}` and off-diagonal entries in
`\{+/-1,+/-35,+/-37\}`.

Every row must have squared norm \(333-37=296\).  Any entry of magnitude at
least 35 already exceeds that norm, so all residue/nonresidue contributions
would have to cancel.  The remaining eight off-diagonal signs have squared
norm only eight.  This entire three-class family is impossible, even when
the `9 x 9` coupling is not group-developed.

### Uniform \(S_4\) block types

The displayed quotient consists of four paired `A/B` fibers and one final
fiber.  If the actual circulant blocks depend only on the nine equality
types preserved by the full \(S_4\) action on those pairs, the nontrivial
three-dimensional representation gives a repeated `2 x 2` Fourier block.

Its two difference sequences have zero-frequency values \(3\) and \(-18\),
so Parseval requires time-domain energy 333.  Binary block entries bound
that energy by

\[
1+36\cdot4+37\cdot4=293.
\]

The uniform \(S_4\) lift is therefore impossible.

### Translation symmetry on the four pairs

A broader ansatz lets block types vary with the difference in a regular
group of order four (`C4` or `C2 x C2`).  The three nonprincipal
pair-character sectors force \(a_g(t)+b_g(t)=2r(t)\), independent of \(g\),
with

\[
\sum_t r(t)=-2.
\]

The remaining `3 x 3` trivial sector has trace \(8r(t)+f(t)\).  Galois
conjugacy and the equation \(K^2=333I_3\) force this trace to be either
\(\pm3\chi(t)\) or \(\pm9\chi(t)\), where \(\chi\) is the quadratic
character modulo 37.  The first possibility misses the pointwise alphabet
`\{-9,-7,-1,1,7,9\}`.  The second forces \(r=\pm\chi\), whose sum is zero,
contradicting \(-2\).

Hence every regular order-four pair-translation lift is also impossible.

The normal form sharpens the symmetry conclusion.  Its three diagonal
\(S_4\)-orbits have sizes `1,4,4`, whose subset sums
`\{0,1,4,5,8,9\}` cannot realize the general trace-law incidences `3,6`.
Moreover, invariance under even one simultaneous transposition of two
paired labels gives a `2 x 2` anti-invariant Fourier sector with
zero-frequency row `(-3,18)`.  Parseval requires energy 333, while binary
difference sequences allow at most 293.  The same calculation in a
nonprincipal \(C_3\) sector excludes any simultaneous 3-cycle on three
paired labels.

## A trace law for every general lift

The quotient also forces a useful condition without imposing any symmetry
on the 45 circulant blocks.  Let \(g(t)\) be the number of the nine diagonal
adjacency blocks that contain a nonzero displacement \(t\).

For a nonzero \(C_{37}\) Fourier frequency, the `9 x 9` adjacency block has
the two restricted conference-graph eigenvalues

\[
r,s=\frac{-1\pm3\sqrt{37}}2.
\]

Cyclotomic Galois conjugacy makes the multiplicity of \(r\) equal to \(m\)
on one quadratic class of frequencies and \(9-m\) on the other.  Fourier
inversion of the trace gives

\[
g(t)=\frac{9\pm3(2m-9)}2
\]

on the two nonzero quadratic classes.  The bounds \(0\leq g(t)\leq9\)
first leave only \(m=3,4,5,6\), hence incidence pairs `(0,9)` or `(3,6)`.
The `(0,9)` branch would make every diagonal block one complete quadratic
class and hence force all nine entries of \(T\)'s diagonal to be zero.
The complete 625-class quotient census proves that no such quotient
exists.  Therefore, after swapping residues and nonresidues if necessary,
every candidate lift of every feasible quotient must obey

```text
each nonzero quadratic residue occurs in exactly 6 diagonal blocks;
each nonresidue occurs in exactly 3 diagonal blocks.
```

This is a general reduction for the fully symmetry-broken lift, not a
construction of one.

## Size of the complete remaining lift

The verifier also counts the whole fixed-margin ambient space, rather than
only one next layer.  There are 1,494 raw membership bits: 1,332 in the 36
unordered off-diagonal circulant blocks and 162 inverse-pair bits in the
nine diagonal blocks.

Fixing all quotient block sizes leaves a search space between
\(2^{1340}\) and \(2^{1341}\).  Imposing the `6/3` trace law reduces the
diagonal part by a factor strictly between \(2^{42}\) and \(2^{43}\).
After using a nonresidue decimation to fix the orientation, the remaining
ambient space still lies between

\[
2^{1297}\quad\hbox{and}\quad2^{1298}.
\]

The all-quotient audit performs the same exact count for every one of the
625 permutation classes.  The individual trace-law exponents range only
from `1297.60492221007667` to `1297.90621474626255`.  Summing one canonical
search space per quotient class gives

```text
log2(all 625 trace-law spaces) = 1307.10873431446430.
```

The rank-16 first-moment law below divides each class by exactly \(37^{16}\),
so the corresponding all-quotient union has logarithm
`1223.75748046440094`.  These are exact combinatorial censuses before the
remaining Fourier equations, not estimates of the number of conference
graphs.  They rule out direct enumeration as a serious strategy: further
mathematics must couple the blocks before any bounded solver is useful.

## Exact finite-field relaxation censuses

Characteristics two and three turn the nonzero Fourier equations into
finite classical-geometry problems that can be counted exactly.

In characteristic two,

\[
\mathbf F_2[C_{37}]\cong \mathbf F_2\times\mathbf F_{2^{36}},
\]

and inversion on the field factor is the unitary involution over
\(q=2^{18}\).  The nontrivial Fourier component satisfies

\[
D^2+D=I.
\]

For a primitive \(\omega\in\mathbf F_4\) in the fixed field,
\(E=D+\omega^2I\) is a Hermitian idempotent.  It is therefore the orthogonal
projection onto a nondegenerate subspace of a nine-dimensional unitary
space.  The `6/3` trace orientation forces its rank to be four; the opposite
orientation has rank five and the same count.  Hence the complete
orientation-fixed mod-two relaxation has exactly

\[
\frac{|U(9,q)|}{|U(4,q)|\,|U(5,q)|}
\]

points.  This is a 217-digit integer with logarithm
\(719.9999944965866\) base two, so it lies strictly between \(2^{719}\)
and \(2^{720}\).  Fixing the quotient modulo two—the trivial Fourier
factor—and the degree-36 field component determines all 37 binary
coefficients by the Chinese remainder theorem.  Thus every integral lift
of the exact quotient injects into this counted set, although most counted
points have the wrong integer block margins.  It is an exact modular
relaxation, not a count of conference graphs.

The complete quotient census shows that only two trivial-factor parity
types remain after fiber permutation and complement.  Consequently every
integral lift in the entire 625-class lane injects, up to those
equivalences, into at most twice the fixed-type count.  The complete
all-quotient modular upper bound is therefore

\[
2^{720}<2\,\frac{|U(9,q)|}{|U(4,q)|\,|U(5,q)|}<2^{721}.
\]

This is the requested complete remaining-search estimate at the strongest
currently counted relaxation.  It is still an upper bound, not an exact
integral candidate count.

Reducing the group-ring characteristic identity modulo two also gives the
support identity

\[
\det(\lambda I+D(x))
=\lambda^9+C(x)(\lambda^8+\lambda^4+1)+\lambda^5+\lambda,
\]

where \(C\) is the oriented quadratic-class indicator.  Equivalently,

\[
e_1=e_5=e_9=C,\qquad e_4=e_8=\delta,\qquad
e_2=e_3=e_6=e_7=0.
\]

Characteristic three gives an independent, weaker audit.  Here

\[
\mathbf F_3[C_{37}]
\cong\mathbf F_3\times\mathbf F_{3^{18}}\times\mathbf F_{3^{18}},
\]

and each degree-18 factor is unitary over \(q=3^9\).  On either factor
\(N=D-I\) is a Hermitian square-zero matrix.  Its rank is at most four, and
the rank-\(r\) count is the product of the number of totally isotropic
\(r\)-spaces and the number of nonsingular Hermitian forms on such a space.
Squaring the sum over \(r=0,\ldots,4\) gives the exact ternary relaxation,
between \(2^{1141}\) and \(2^{1142}\).

The characteristic-two census is the strongest complete bound currently
known for this lane.  It cuts the fixed-quotient frontier by roughly 578
further bits beyond the trace-only census, but even the symmetry-reduced
all-quotient bound near \(2^{721}\) rules out flat enumeration.

## A characteristic-37 moment filtration

There is a second, independent general reduction.  Work in the
nonsemisimple group algebra

\[
\mathbf F_{37}[y]/(y^{37}),\qquad x=1+y.
\]

For a hypothetical block adjacency matrix \(D(x)\), put
\(N(y)=D(1+y)-18I\).  Since \(18^2+18=9\pmod {37}\) and

\[
1+x+\cdots+x^{36}=y^{36},
\]

the complete strongly-regular equation becomes

\[
N(y)^2=9y^{36}J.
\]

The constant coefficient is \(N_0=B-18I=-T/2\pmod {37}\).  It has rank
four and satisfies \(N_0^2=0\).  Star symmetry makes the first coefficient
\(N_1\) skew-symmetric, with its 36 entries equal to the first moments of
the 36 off-diagonal block subsets.  The coefficient of \(y\) imposes

\[
N_0N_1+N_1N_0=0.
\]

Exact elimination over \(\mathbf F_{37}\) gives rank 16, leaving a
20-dimensional moment kernel.

This rank has an exact census interpretation.  For every fixed block size
between 1 and 36, translating a subset of \(\mathbf F_{37}\) makes its
first moment uniform over all 37 residues.  The 16 independent equations
therefore reduce the ambient census by exactly

\[
37^{16},
\]

a factor between \(2^{83}\) and \(2^{84}\).  Combined with the trace law,
the complete ambient space now lies between \(2^{1214}\) and \(2^{1215}\).
That is still far beyond enumeration, but the remaining coefficients
\(y^2,\ldots,y^{36}\) provide a concrete algebraic lifting hierarchy rather
than an undifferentiated Boolean search.

The certificate includes a concrete block-membership witness for the next
layers.  It simultaneously satisfies the quotient margins, the `6/3`
diagonal trace law, star symmetry, and zero binomial moments in degrees
one, two, and three.  Consequently the equations through \(y^3\) replay
exactly.  Its first failure is at \(y^4\), where 79 of the 81 matrix entries
have nonzero residual.

This is deliberately recorded as a negative calibration as well as a
milestone: multiple low modular layers can be lifted, but they are not yet
selective enough to indicate convergence to a conference graph.

There is an explicit full formal completion for every admissible first
moment.  Put \(z=\log(1+y)\) in
\(\mathbf F_{37}[y]/(y^{37})\).  Exact elimination shows that every
admissible first moment \(X\) has the form

\[
X=[N_0,A]
\]

for a symmetric `9 x 9` matrix \(A\).  With \(q=z^{18}\), the
trace-corrected formula

\[
N(y)=e^{-zA}\bigl(N_0+qJ+19y^{36}J\bigr)e^{zA}
\]

has star symmetry and satisfies the full equation

\[
N(y)^2=9y^{36}J.
\]

The \(qJ\) term works because \(N_0J=JN_0=0\), \(J^2=9J\), and
\(z^{36}=y^{36}\) in the truncated ring.  The square-invisible socle term
`19*y^36*J` corrects the conjugacy-invariant trace to
\(23y^{36}+9z^{18}\), one of the two genuine `3/6` trace branches.  Changing
the sign of \(q\) gives the other branch.  The verifier also recovers the
exact cyclic-basis identity

\[
z^{18}=6\sum_{t\ne0}\chi(t)x^t,
\]

where \(\chi\) is the quadratic character of \(\mathbf F_{37}\).

This changes the interpretation of the filtration.  The rank-16
first-moment gate is the only obstruction coming from formal matrix
algebra encountered by this construction: every such moment profile has
an explicit coefficient completion solving all 37 modular layers.  This
does not classify all formal solutions.  The hard remaining condition is
simultaneous realizability of those coefficients by actual `0/1` block
supports.

## Constant-generator families through rank two are impossible

The formal solution is not automatically close to a binary lift.  Two of
its simplest subfamilies can now be excluded exactly.

If \(A\) is diagonal, every nonzero-lag diagonal coefficient remains either
`13` or `25` in \(\mathbf F_{37}\), rather than `0` or `1`.

Now let \(A\) be a nonzero symmetric rank-one matrix.  When
\(u^Tu\ne0\), write

\[
A=\alpha\frac{uu^T}{u^Tu},\qquad
h=\mathbf1^Tu,\qquad
w=\mathbf1-\frac{h}{u^Tu}u.
\]

At a nonexceptional lag \(r=t/\alpha\), the \(i\)-th diagonal coefficient
has the form

\[
19+6\eta\left(
  \chi(r)a_i+
  \bigl(\chi(r-1)+\chi(r+1)\bigr)b_i
\right),
\]

where

\[
a_i=w_i^2+\frac{h^2u_i^2}{(u^Tu)^2},
\qquad
b_i=\frac{h\,w_i u_i}{u^Tu},
\qquad \eta\in\{\pm1\}.
\]

The six character patterns

```text
(-1,2), (1,0), (-1,0), (1,-2), (1,2), (-1,-2)
```

all occur, already at normalized lags `2,3,5,7,10,14`.  Requiring the six
displayed coefficients to lie in `0/1` forces
\(a_i\in\{3,-3\}\) and \(b_i=0\).  But if \(h=0\), then \(a_i=1\).
If \(h\ne0\), the equation \(b_i=0\) says coordinatewise that \(u_i=0\)
or \(w_i=0\), and either alternative again gives \(a_i=1\).  This is a
contradiction.

The remaining rank-one case has \(u^Tu=0\), so
\(A=\lambda uu^T\) is square-zero.  Its conjugation corrections have zero
identity coefficient on the diagonal.  The zero-lag diagonal therefore
stays

```text
0, 2, 0, 2, 0, 2, 0, 2, 29  (mod 37),
```

which is already nonbinary in five positions.

Thus every constant diagonal generator and every constant symmetric
rank-one generator in the displayed exponential family is impossible.

The rank-two case is also closed across the complete quotient census, but
needs a different finite classification.  Split semisimple generators are
excluded independently of the quotient by checking all 35 projective
eigenvalue ratios and all \(37^2\) local projector-coordinate triples.  The
remaining rational/Jordan types are:

1. an irreducible quadratic block;
2. a nonzero \(J_2\) block;
3. a nonzero eigenline together with \(J_2(0)\);
4. \(J_3(0)\); and
5. \(J_2(0)\oplus J_2(0)\).

For each type, the companion verifier constructs the similarity-invariant
over-code

\[
W(A)=V(A)+z^{18}V(A),
\]

where \(V(A)\) spans products of entries of \(e^{-zA}\) and \(e^{zA}\).
Every possible diagonal correction lies in this over-code, even after
forgetting the special matrices \(N_0,J\) and symmetry constraints.  Its
exact intersection with
\(\{0\}\times\{18,19\}^{36}\) is computed from information coordinates.
All 19 irreducible projective classes and both pure nilpotent types yield
only the QR/NR words of weight 18.  Since the quotient census has no
all-zero diagonal, these types fail for every quotient.  The two remaining
Jordan families yield weights only from 16 through 20.  Exactly two of the
625 quotient classes meet that necessary condition; they are negatives of
one another and form one sign-class with diagonal profile

```text
(-4,-4,0,0,0,0,0,4,4).
```

Restoring information deliberately forgotten by \(W(A)\) closes this last
case.  After normalizing the nonzero eigenvalue, both a nonzero \(J_2\)
block and a nonzero eigenline plus \(J_2(0)\) have
\(A=P+N\), where \(P^2=P\), \(N^2=0\), and either \(PN=N\) or \(PN=0\).
For every symmetric constant matrix \(M\), the diagonal of
\(e^{-zA}Me^{zA}\) lies in a five-function space.  The full reduced
diagonal word must consequently lie in

\[
\eta z^{18}+U,\qquad \eta\in\{1,-1\},
\]

where \(U\) is an explicit seven-dimensional cyclic code.  Its information
coordinates are `0,...,6`, so each affine coset needs only 64 assignments.
Exhausting all 37 possible coefficients finds binary words only in the
spurious cosets \(\eta=3\) and \(\eta=-3\); both genuine trace orientations
\(\eta=\pm1\) are empty.  No off-diagonal test is needed.

Consequently any binary point in this single-constant-\(A\) exponential
family must use a genuinely coordinate-mixing symmetric generator of rank
at least three.  This does not exclude a higher-\(y\) conjugator, a more
general formal parametrization, or the general semiregular \(C_{37}\) lift.
The complete proofs and scopes are in
`RANK_TWO_CONJUGATION_OBSTRUCTION.md` and
`RANK_TWO_JORDAN_OBSTRUCTION.md`.

## A group-ring characteristic identity

The same spectral multiplicity argument gives a compact necessary identity
over \(\mathbf Z[C_{37}]\).  If \(g=\operatorname{tr}D\), then every lift
must satisfy

\[
\det(YI-D)=(Y^2+Y-83)^4\bigl(Y-(4+g)\bigr).
\]

At frequency zero the extra root is 166; at nonzero frequencies it is the
restricted root whose multiplicity is five.  Two useful aggregate
consequences are

\[
e_2(D)=-342\,\delta-4g,
\qquad
\det D=83^4(4\delta+g).
\]

These are redundant with the complete strongly-regular equation but can
serve as lower-dimensional pruning identities in a support-realizability
solver.

## Current frontier

The result is mixed but useful:

- the entire zero-frequency layer is classified into 625 permutation
  classes, with a genuinely nongroup-developed quotient available;
- three natural Paley or pair-symmetric lifts are exactly impossible; and
- every general lift obeys the exact `6/3` diagonal-incidence law; and
- every general lift obeys 16 independent mod-37 first-moment equations;
  and
- every lift in the full quotient census injects, up to fiber permutation
  and complement, into an all-quotient characteristic-two relaxation
  between \(2^{720}\) and \(2^{721}\);
  and
- all later mod-37 matrix equations are formally integrable, isolating
  exact `0/1` support realizability as the remaining modular difficulty;
  and
- constant diagonal and all constant symmetric generators of ranks one and
  two in the explicit exponential family are impossible across all 625
  quotient classes, so a viable constant generator must genuinely mix
  coordinates and have rank at least three;
  and
- a lift with the displayed quotient must break every paired-label
  transposition, every paired-label 3-cycle, and all regular order-four
  symmetry on the four paired fibers.

The general `45`-block \(C_{37}\)-circulant lift remains open.  No conference
matrix, strongly regular graph, Legendre pair, or Hadamard matrix is claimed.
`LITERATURE_AUDIT.md` separates the standard orbit/multicirculant framework
from the quotient-specific results and records the provisional publication
boundary, including why Mathon's superficially matching
\(pq^2+1=334\) construction does not apply.

Run the dependency-free verification from this folder:

```text
python3 verify_z37_lift_frontier.py
python3 verify_rank_two_conjugation_obstruction.py
python3 verify_rank_two_jordan_obstruction.py
```

The complete quotient replay additionally compiles
`census_z37_quotients.cpp`; see `QUOTIENT_CENSUS.md` for the exact commands
and the two independent audit programs.
