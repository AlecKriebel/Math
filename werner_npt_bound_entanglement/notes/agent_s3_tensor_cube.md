# The local \(S_3\) bad block under the tensor-cube constraint

## Research checkpoint

**2026-07-28 14:25 PDT.**  This note refines the three-replica
obstruction for the four-copy candidate
\[
H_1(P)=e_2+6e_4-3o_3\stackrel{?}{\geq}0.
\tag{1}
\]
It does **not** prove (1), four-copy endpoint positivity, or an all-copy
theorem.

The exact advances are:

1. the \((\mathrm{sign},\mathrm{sign},\mathrm{trivial},
   \mathrm{standard})\) block is written as an explicit cubic covariant
   of the code isometry;
2. that covariant factors through the common decomposable bivector
   \(\omega=u\wedge v\), yielding explicit incidence, Plücker, Gram,
   and rank-one-flattening relations;
3. a qutrit code is given for which the bad block has exact weight
   \(1/18\), so its contribution to the three-replica operator is
   \(-2/9\), or \(-1/36\) after the normalization in (1);
4. a complete exact local-sector ledger for that code reveals a second,
   larger obstruction: the
   \((\mathrm{standard},\mathrm{standard},\mathrm{trivial},
   \mathrm{standard})\) block contributes \(-28/9\).

Thus the bad block is neither a fictitious abstract sector nor something
annihilated by decomposability.  The tensor-cube equations must transfer
positive mass between inequivalent local Young types.  Moreover, a
certificate controlling only the originally isolated bad block would
still be incomplete because of the three-standard block
\((\mathrm{standard},\mathrm{standard},\mathrm{trivial},
\mathrm{standard})\).

## 1. Three-replica operator and local central projectors

Let \(P=UU^\dagger\) be a rank-two orthogonal projection on
\[
H=A\otimes B\otimes C\otimes D,
\qquad
U:\mathbb C^2\longrightarrow H,
\qquad
Ue_0=u,\quad Ue_1=v,
\tag{2}
\]
where \(u,v\) are orthonormal.  For \(S\subseteq\{A,B,C,D\}\), define
\[
J_S=\frac13\sum_{\tau\ {\rm transposition\ in}\ S_3}
       V_{\tau,S},
\tag{3}
\]
where \(V_{\tau,S}\) applies \(\tau\) to the three replicas at all sites
in \(S\).  The operator representing (1) is
\[
\mathcal O
=6J_{ABCD}+\sum_{|S|=2}J_S-3\sum_{|S|=3}J_S.
\tag{4}
\]
For \(\rho=P/2\),
\[
H_1(P)=\operatorname{Tr}(\rho^{\otimes3}\mathcal O)
      =\frac18\operatorname{Tr}(P^{\otimes3}\mathcal O).
\tag{5}
\]

At one physical site \(X\), put
\[
\begin{aligned}
S_X&=\frac16\sum_{\pi\in S_3}V_{\pi,X},\\
A_X&=\frac16\sum_{\pi\in S_3}\operatorname{sgn}(\pi)V_{\pi,X},\\
M_X&=I-S_X-A_X.
\end{aligned}
\tag{6}
\]
These are the central projectors onto the trivial, sign, and standard
isotypic components.  Projectors at distinct sites commute.  They also
commute with \(\mathcal O\): centrality makes each one commute with
every local permutation appearing in every \(V_{\tau,S}\).

The local Schur--Weyl decomposition is
\[
X^{\otimes3}
\simeq
\operatorname{Sym}^3X\otimes[3]
\ \oplus\
S_{21}X\otimes[21]
\ \oplus\
\bigwedge^3X\otimes[111].
\tag{7}
\]
For the logical space \(K=\mathbb C^2\), the last summand is absent:
\[
\bigwedge^3K=0.
\tag{8}
\]

## 2. Exact action on the bad block

Consider
\[
E_{AB|C|D}=A_AA_BS_CM_D.
\tag{9}
\]
On this block the local \(S_3\) types are
\[
([111],[111],[3],[21]).
\tag{10}
\]
Their tensor product under the simultaneous replica permutation is
standard, not sign.

Let \(\pi\) denote the standard two-dimensional representation.  The
average of its three transpositions vanishes:
\[
\frac13\sum_{\tau}\pi(\tau)=0.
\tag{11}
\]
Hence all terms of (4) whose subset contains \(D\) vanish on (9).
Among the pair terms not containing \(D\),
\[
J_{AB}=I,\qquad J_{AC}=-I,\qquad J_{BC}=-I.
\tag{12}
\]
The only triple not containing \(D\) is \(ABC\), and
\[
J_{ABC}=I.
\tag{13}
\]
Consequently
\[
\boxed{\quad
\mathcal O E_{AB|C|D}=-4E_{AB|C|D}.
\quad}
\tag{14}
\]
This proves the negative eigenvalue without choosing a matrix model for
the standard representation.

## 3. The actual tensor-cube covariant

The abstract block (9) is too large: an admissible vector must come from
the single map \(U^{\otimes3}\).  The restriction can be made explicit.
Define
\[
\omega=u\otimes v-v\otimes u\in H^{\otimes2}
\tag{15}
\]
and the two standard logical vectors
\[
\eta_0=\omega_{12}\otimes u_3,
\qquad
\eta_1=\omega_{12}\otimes v_3.
\tag{16}
\]
They have
\[
\langle\eta_r,\eta_s\rangle=2\delta_{rs}.
\tag{17}
\]
The replica-permutation orbit of \(\eta_0\) is the standard subspace in
the span of the three words with two \(u\)'s and one \(v\); the orbit of
\(\eta_1\) is the standard subspace with one \(u\) and two \(v\)'s.
Together these are the whole logical standard isotypic component.

Put
\[
\Pi_{AAS}=A_AA_BS_C.
\tag{18}
\]
Because \(\eta_r\) is globally standard while the product of the first
three local characters in (18) is
\(\mathrm{sign}^2\mathrm{trivial}=\mathrm{trivial}\),
\(\Pi_{AAS}\eta_r\) is automatically standard at \(D\).  Therefore
\[
M_D\Pi_{AAS}\eta_r=\Pi_{AAS}\eta_r.
\tag{19}
\]

### Proposition 1: exact bad-weight formula

The tensor-cube weight in the negative block is
\[
\boxed{\quad
b_{AB|C|D}(U)
:=\operatorname{Tr}\!\left(P^{\otimes3}E_{AB|C|D}\right)
=\|\Pi_{AAS}\eta_0\|^2+\|\Pi_{AAS}\eta_1\|^2.
\quad}
\tag{20}
\]

#### Proof

Pull \(E_{AB|C|D}\) back through the isometry \(U^{\otimes3}\).  The
result commutes with the logical \(S_3\) action.  It vanishes on every
logical trivial summand, because its physical range is globally
standard, and the logical sign summand is zero by (8).

Here is an elementary trace calculation that also fixes the
normalization.  In the orbit with two \(u\)'s and one \(v\), set
\[
\begin{aligned}
p_1&=E_{AB|C|D}(u\otimes u\otimes v),\\
p_2&=E_{AB|C|D}(u\otimes v\otimes u),\\
p_3&=E_{AB|C|D}(v\otimes u\otimes u).
\end{aligned}
\tag{21}
\]
The symmetric sum is killed because the range of \(E_{AB|C|D}\) is
globally standard, so \(p_1+p_2+p_3=0\).  Replica-permutation symmetry
gives a common squared norm \(q\) and a common real off-diagonal inner
product \(c\).  Squaring the preceding sum gives \(3q+6c=0\), whence
\(c=-q/2\).  Therefore
\[
\|p_2-p_3\|^2=3q
=\sum_{j=1}^3\|p_j\|^2.
\tag{22}
\]
But \(p_2-p_3=E_{AB|C|D}\eta_0=\Pi_{AAS}\eta_0\), by (19).
Repeating the same argument in the orbit with one \(u\) and two \(v\)'s
gives the \(\eta_1\) term.  The \(uuu\) and \(vvv\) words are globally
trivial and are killed.  Thus the right side of (20) is exactly the
trace over all eight logical basis words. \(\square\)

Equation (20) is the useful refinement of the abstract sector
calculation: the bad component is not arbitrary.  It is the local Young
projection of the two cubic tensors
\[
u\otimes(u\wedge v),\qquad v\otimes(u\wedge v).
\tag{23}
\]

## 4. Coordinate equations: exact lifted tensor-cube constraints

Choose a basis of \(H\), use composite indices \(i,j,k,\ldots\), and
write \(U_i^0=u_i,\ U_i^1=v_i\).  Set
\[
\omega_{ij}
=\epsilon_{rs}U_i^rU_j^s
=u_iv_j-v_iu_j.
\tag{24}
\]
The following equations are immediate expansions and hold for every
code isometry.

### 4.1 Alternation, Plücker, and incidence equations

\[
\omega_{ij}=-\omega_{ji},
\tag{25}
\]
\[
\boxed{\quad
\omega_{ij}\omega_{k\ell}
-\omega_{ik}\omega_{j\ell}
+\omega_{i\ell}\omega_{jk}=0
\quad}
\tag{26}
\]
for all \(i,j,k,\ell\), and
\[
\boxed{\quad
U_i^r\omega_{jk}
-U_j^r\omega_{ik}
+U_k^r\omega_{ij}=0,
\qquad r=0,1.
\quad}
\tag{27}
\]
Equation (26) is the decomposable-bivector Plücker relation.
Equation (27) is the incidence relation
\[
u\wedge\omega=v\wedge\omega=0.
\tag{28}
\]
Both follow by substituting (24); no geometric theorem is needed.

### 4.2 Hermitian Gram equations

The isometry conditions and their first useful consequences are
\[
\sum_i\overline{U_i^r}U_i^s=\delta_{rs},
\tag{29}
\]
\[
\boxed{\quad
\sum_j\omega_{ij}\overline{\omega_{kj}}
=u_i\overline{u_k}+v_i\overline{v_k}=P_{ik},
\qquad
\sum_{i,j}|\omega_{ij}|^2=2.
\quad}
\tag{30}
\]
In addition,
\[
\sum_i\overline{U_i^0}\omega_{ij}=U_j^1,
\qquad
\sum_i\overline{U_i^1}\omega_{ij}=-U_j^0.
\tag{31}
\]
Thus the bivector and the rank-two projection cannot be varied
independently.

### 4.3 Common-factor and rank-one-flattening equations

Define the lifted cubic tensor
\[
T^r_{ij;k}=\omega_{ij}U_k^r.
\tag{32}
\]
The two bad covariants in (20) are fixed linear Young projections of
\(T^0,T^1\).  Besides the linear alternation and incidence equations,
the flattening
\[
(ij)\ \big|\ (k,r)
\tag{33}
\]
has rank one.  Equivalently,
\[
\boxed{\quad
T^r_{ij;k}T^s_{\ell m;n}
-T^s_{ij;n}T^r_{\ell m;k}=0
\quad}
\tag{34}
\]
for every choice of indices.  Also,
\[
\sum_{i,j}T^r_{ij;k}\overline{T^s_{ij;\ell}}
=2U_k^r\overline{U_\ell^s}.
\tag{35}
\]

For completeness, the coordinate formula for the unstripped bad
covariant is
\[
\begin{aligned}
(B_r)_{\mathbf a,\mathbf b,\mathbf c,\mathbf d}
=\frac1{216}
\sum_{\sigma,\tau,\gamma\in S_3}
&\operatorname{sgn}(\sigma)\operatorname{sgn}(\tau)\\
{}\times&
\omega_{x_1x_2}U_{x_3}^r,
\end{aligned}
\tag{36}
\]
where
\[
x_q=
\bigl(a_{\sigma(q)},b_{\tau(q)},c_{\gamma(q)},d_q\bigr).
\tag{37}
\]
Then \(B_r=\Pi_{AAS}\eta_r\) and
\[
b_{AB|C|D}(U)=\|B_0\|^2+\|B_1\|^2.
\tag{38}
\]

Equations (24)--(37) are an exact lifted system obeyed by the
admissible bad block.  Eliminating \(U,\omega,T\) to equations in the
projected coordinates \(B_r\) alone is not helpful: the Young
projection in (36) is noninvertible, and the resulting relations
necessarily couple \(B_r\) to complementary local Young components.

## 5. Why these equations do not kill the block

The obstruction is already visible at the representation level.  The
bad multiplicity space is
\[
\bigwedge^3A\otimes\bigwedge^3B
\otimes\operatorname{Sym}^3C\otimes S_{21}D.
\tag{39}
\]
The relevant \(S_3\) character product is
\[
[111]\otimes[111]\otimes[3]\otimes[21]=[21].
\tag{40}
\]
Its multiplicity against the logical standard representation is one.
Indeed, sign squared and trivial do nothing, leaving the standard
representation, whose inner product with itself is one.  Hence there
is one allowed cubic equivariant coupling; no linear
representation-theoretic identity forces it to vanish.

The hierarchy of relations is also instructive.

* At cubic order, (27) is the global alternating relation.  It is the
  coordinate form of the already-used fact \(\bigwedge^3K=0\).
* The genuinely new common-bivector relations (26) and (34) are
  nonlinear in the cubic covariants.
* Therefore replacing the global sign block by zero and asking for a
  positive operator on the remaining cubic space cannot exploit the
  new information.  A successful identity has to contain ideal
  multipliers or cross terms between different local Young types.
* Since the target is Hermitian of bidegree \((3,3)\) in
  \((U,\overline U)\), the quartic holomorphic Plücker equations do not
  enter a bihomogeneous degree-\((3,3)\) certificate without using the
  nonhomogeneous Stiefel equations (29) or raising the degree.  This
  explains why a constant PSD correction on the cubic representation
  space is too small a search class.

In particular, an SOS ansatz must have a form schematically like
\[
\operatorname{Tr}(P^{\otimes3}\mathcal O)
=\sum_j\|R_j(U)\|^2
+\sum_\alpha
 2\operatorname{Re}\!\left(h_\alpha(U,\overline U)
 f_\alpha(U)\right)
+\sum_{r,s}g_{rs}(U,\overline U)
\left((U^\dagger U)_{rs}-\delta_{rs}\right),
\tag{41}
\]
where the \(f_\alpha\)'s include incidence, Plücker, or
rank-one-flattening generators.  An ansatz with only a PSD operator plus
the global antisymmetrizer omits precisely the second and third kinds of
terms.

There is also a useful reduced-state version of (20).  The
all-antisymmetric \(D\) term vanishes because
\(A_AA_BS_CA_D\) has global sign type, so
\[
\boxed{\quad
b_{AB|C|D}
=\operatorname{Tr}\!\left[
   (\operatorname{Tr}_D P)^{\otimes3}A_AA_BS_C
 \right]
-\operatorname{Tr}\!\left[
   P^{\otimes3}A_AA_BS_CS_D
 \right].
\quad}
\tag{42}
\]
This is the invariant form of the decomposition \(M_D=I-S_D-A_D\).

## 6. An exact code that populates the bad block

Take all four local spaces to contain the qutrit basis
\(\{|0\rangle,|1\rangle,|2\rangle\}\), and define
\[
\begin{aligned}
u&=\frac{
|0,0,1,0\rangle+|1,1,1,0\rangle}{\sqrt2},\\
v&=|2,2,1,1\rangle.
\end{aligned}
\tag{43}
\]
These vectors are orthonormal.  The \(C\) site is the pure spectator
\(|1\rangle\).

Let
\[
|\mathrm{Alt}\rangle
=\frac1{\sqrt6}\sum_{\pi\in S_3}
\operatorname{sgn}(\pi)|\pi(0,1,2)\rangle.
\tag{44}
\]
A direct expansion of (16) gives
\[
\boxed{\quad
\Pi_{AAS}\eta_0
=|\mathrm{Alt}\rangle_A|\mathrm{Alt}\rangle_B
 |111\rangle_C
 \otimes\frac{|010\rangle_D-|100\rangle_D}{6},
\quad}
\tag{45}
\]
and
\[
\Pi_{AAS}\eta_1=0.
\tag{46}
\]
The displayed factors in (45) are mutually normalized except for the
last one.  Therefore Proposition 1 gives
\[
\boxed{\quad
b_{AB|C|D}(U)=\frac{2}{36}=\frac1{18}.
\quad}
\tag{47}
\]
By (14), the contribution of this block is
\[
\operatorname{Tr}\!\left(P^{\otimes3}
 E_{AB|C|D}\mathcal O\right)
=-4\left(\frac1{18}\right)=-\frac29.
\tag{48}
\]
Its contribution to \(H_1(P)\) is \(-1/36\).

An equivalent check avoids (45).  For each of the three logical words
with two \(u\)'s and one \(v\),
\[
\begin{aligned}
\langle A_AA_B\rangle&=\frac1{36},\\
\langle A_AA_BS_D\rangle&=\frac1{108},\\
\langle A_AA_BA_D\rangle&=0.
\end{aligned}
\tag{49}
\]
Thus its standard-\(D\) weight is \(1/54\), and the three placements
sum to \(1/18\).  The last equality in (49) is also forced by the
absence of the global logical sign representation.

No optimality is claimed for the value \(1/18\).  Its role is to prove
that the bad covariant is genuinely nonzero on the Stiefel/Plücker
variety.

## 7. The exact compensation ledger

The same code shows that controlling (9) alone is not enough.  Because
\(C\) is a pure spectator, only the \(S_C\) sector occurs.  In the
following table, a three-letter word records the types at \(A,B,D\);
\(S,A,M\) mean trivial, sign, and standard.  Put
\[
w_\lambda
=\operatorname{Tr}(P^{\otimes3}E_\lambda),
\qquad
h_\lambda
=\operatorname{Tr}(P^{\otimes3}E_\lambda\mathcal O).
\tag{50}
\]
All omitted blocks have zero weight.

On this spectator sector, direct substitution in (4) gives the reduced
operator
\[
\mathcal O_{\rm red}
=3J_{ABD}-2(J_{AB}+J_{AD}+J_{BD})+J_A+J_B+J_D.
\tag{51}
\]

\[
\begin{array}{c|c|c@{\qquad}c|c|c}
\lambda&w_\lambda&h_\lambda&
\lambda&w_\lambda&h_\lambda\\ \hline
SSS&61/36&0&
SSM&7/18&0\\
SMS&7/18&0&
SMM&7/9&7/6\\
AAS&1/36&1/9&
AAM&1/18&-2/9\\
AMS&1/18&1/9&
AMM&1/9&1/6\\
MSS&7/18&0&
MSM&7/9&7/6\\
MAS&1/18&1/9&
MAM&1/9&1/6\\
MMS&25/18&7/3&
MMM&16/9&-28/9
\end{array}
\tag{52}
\]
The checksums are
\[
\sum_\lambda w_\lambda=8=\operatorname{Tr}P^{\otimes3},
\qquad
\sum_\lambda h_\lambda=2.
\tag{53}
\]
The two negative entries sum to
\[
-\frac29-\frac{28}{9}=-\frac{10}{3},
\tag{54}
\]
while all positive entries sum to \(16/3\), leaving \(2\).
Even the closest sectorwise repair fails: \(\mathcal O=4I\) on \(AAS\)
and \(\mathcal O=-4I\) on \(AAM\), but
\[
4w_{AAS}-4w_{AAM}
=4\left(\frac1{36}\right)-4\left(\frac1{18}\right)
=-\frac19.
\]
Thus compensation for the named bad block already has to cross the
fixed \(AA\) prefix.

The total can also be verified without any representation
decomposition.  After removing the spectator \(C\), direct partial
traces give
\[
\begin{array}{c|ccc}
X&A&B&D\\ \hline
\|\operatorname{Tr}_X P\|_2^2&3/2&3/2&2
\end{array},
\tag{55}
\]
and
\[
\begin{array}{c|ccc}
X&AB&AD&BD\\ \hline
\|\operatorname{Tr}_X P\|_2^2&2&3/2&3/2.
\end{array}
\tag{56}
\]
Hence
\[
Q_3(P_{ABD})
=2-\frac12(5)+\frac14(5)-\frac18(4)
=\frac14.
\tag{57}
\]
The pure-factor reduction gives \(H_1(P)=1/4\), agreeing with
\[
\frac18\sum_\lambda h_\lambda=\frac14.
\tag{58}
\]

The \(MMM\) entry is important.  It is not a scalar eigenblock of
\(\mathcal O\); several standard multiplicity spaces are coupled
inside it.  Nevertheless, an actual tensor cube has expectation
\(-28/9\) there.  The next SOS search must therefore couple at least the
\(AAM\) and \(MMM\) negative components to the positive
\(SMM,MSM,MMS\), and mixed-sign components.

## 8. Consequences for the next certificate search

The calculations above rule out three narrow strategies.

1. **Deleting only the global sign sector.**  The \(AAM\) block is
   globally standard and has eigenvalue \(-4\).
2. **Declaring the \(AAM\) covariant zero by decomposability.**  The
   exact code (43) gives it weight \(1/18\).
3. **Repairing only the originally isolated bad block.**  The same
   exact code has the larger negative \(MMM\) contribution \(-28/9\).

They also identify a concrete finite algebraic target.  Introduce all
local Young projections of the common tensors
\[
T^0=(u\wedge v)\otimes u,\qquad
T^1=(u\wedge v)\otimes v,
\tag{59}
\]
retain the Stiefel equations (29), and search for a Hermitian Gram
identity modulo (26), (27), and (34).  Projecting away the companion
Young components before imposing these equations loses the relations
needed for compensation.

A particularly useful restricted question is whether the negative
part of \(\mathcal O\) on the direct sum of the \(AAM\) and \(MMM\)
components admits a norm-dominating equivariant map into the positive
components for tensors of the special form (59).  The ledger (52)
provides a sparse exact boundary test for every proposed map.

## 9. Minimal exact verifier for the sector ledger

The following standard-library script constructs the three-replica
vectors sparsely over the rational numbers.  The only omitted
amplitudes are the common factors \(2^{-k/2}\) from \(k\) copies of
\(u\); their squared factor \(2^{-k}\) is inserted explicitly.  It
checks every entry of (52), not just the final checksum.

```python
from collections import defaultdict
from fractions import Fraction as F
from itertools import permutations, product

PERMS = list(permutations(range(3)))

def parity(p):
    inv = sum(p[i] > p[j] for i in range(3) for j in range(i + 1, 3))
    return -1 if inv % 2 else 1

def add(x, y, scale=F(1)):
    out = defaultdict(F)
    out.update(x)
    for key, value in y.items():
        out[key] += scale * value
    return {key: value for key, value in out.items() if value}

def inner(x, y):
    return sum(value * y.get(key, F(0)) for key, value in x.items())

def permute_site(x, site, p):
    out = defaultdict(F)
    for key, value in x.items():
        new_key = []
        for replica in range(3):
            row = list(key[replica])
            row[site] = key[p[replica]][site]
            new_key.append(tuple(row))
        out[tuple(new_key)] += value
    return dict(out)

def central(x, site, kind):
    if kind == "M":
        return add(x, add(central(x, site, "S"),
                          central(x, site, "A")), F(-1))
    out = {}
    for p in PERMS:
        coefficient = F(parity(p) if kind == "A" else 1, 6)
        out = add(out, permute_site(x, site, p), coefficient)
    return out

def transposition_average(x, sites):
    out = {}
    for p in ((1, 0, 2), (2, 1, 0), (0, 2, 1)):
        term = x
        for site in sites:
            term = permute_site(term, site, p)
        out = add(out, term, F(1, 3))
    return out

def operator(x):
    # Site order is A,B,D.  This is equation (51).
    terms = (
        (3, (0, 1, 2)),
        (-2, (0, 1)), (-2, (0, 2)), (-2, (1, 2)),
        (1, (0,)), (1, (1,)), (1, (2,)),
    )
    out = {}
    for coefficient, sites in terms:
        out = add(out, transposition_average(x, sites), F(coefficient))
    return out

# Integer-amplitude supports; normalization is inserted below.
COLUMNS = {
    0: ((0, 0, 0), (1, 1, 0)),  # sqrt(2) u on A,B,D
    1: ((2, 2, 1),),             # v
}

def logical_word(bits):
    return {
        tuple(choices): F(1)
        for choices in product(*(COLUMNS[bit] for bit in bits))
    }

ledger = {}
for kinds in product("SAM", repeat=3):
    weight = F(0)
    expectation = F(0)
    for bits in product((0, 1), repeat=3):
        vector = logical_word(bits)
        projected = vector
        for site, kind in enumerate(kinds):
            projected = central(projected, site, kind)
        normalization = F(1, 2 ** bits.count(0))
        weight += normalization * inner(projected, projected)
        expectation += normalization * inner(projected,
                                               operator(projected))
    if weight or expectation:
        ledger["".join(kinds)] = (weight, expectation)

expected = {
    "SSS": (F(61, 36), 0),       "SSM": (F(7, 18), 0),
    "SMS": (F(7, 18), 0),        "SMM": (F(7, 9), F(7, 6)),
    "AAS": (F(1, 36), F(1, 9)),  "AAM": (F(1, 18), F(-2, 9)),
    "AMS": (F(1, 18), F(1, 9)),  "AMM": (F(1, 9), F(1, 6)),
    "MSS": (F(7, 18), 0),        "MSM": (F(7, 9), F(7, 6)),
    "MAS": (F(1, 18), F(1, 9)),  "MAM": (F(1, 9), F(1, 6)),
    "MMS": (F(25, 18), F(7, 3)), "MMM": (F(16, 9), F(-28, 9)),
}
assert ledger == expected
assert sum(x[0] for x in ledger.values()) == 8
assert sum(x[1] for x in ledger.values()) == 2
```

## 10. Exact status

Established:

* the exact cubic formula (20) for the admissible bad-block weight;
* explicit incidence, Plücker, Gram, and common-factor equations;
* a proof that the bad cubic coupling has multiplicity one and is not
  representation-theoretically forbidden;
* an exact qutrit code with bad-block weight \(1/18\);
* the complete local central-sector ledger (52), including the
  additional \(MMM\) obstruction.

Not established:

* an SOS identity modulo the tensor-cube relations;
* a sharp upper bound on the bad-block weight;
* \(H_1(P)\geq0\) for arbitrary rank-two projections;
* four-copy or all-copy endpoint positivity.
