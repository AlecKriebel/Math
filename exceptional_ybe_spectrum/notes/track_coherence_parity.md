# Track A2: coherence, quaternionic, and parity audit

**Date:** 2026-07-28

**Status:** exact negative delimitations plus one new exact invariant of the
published family; no unconditional four-divisibility theorem

## Executive conclusion

Write
\[
d=2s.
\]
The complete Hecke-tower multiplicity calculation gives
\[
m_{\lambda,n}=D_\lambda s^n.
\]
I tested the main ways in which one might try to promote this to
\(2\mid s\).

The conclusion is deliberately adversarial:

1. **Frobenius--Schur and quaternionic Schur-index arguments do not apply to
   an arbitrary localization.**  The generating object \(X\) is not
   self-dual, the matrices are complex rather than real, and a localization
   represents only the endomorphism-algebra tower.  It does not supply the
   cups, duality maps, or invariant tensors needed to preserve an
   FS indicator.
2. **The quaternionic algebra used by Rowell has no residual parity
   obstruction over \(\mathbb C\).**  At every fixed level it has a
   trace-preserving representation of dimension \((2s)^n\) for every
   integer \(s\).  Its complex Clifford blocks split, and their module sizes
   do not require \(s\) to be even.
3. **All one-sided tower coherence exists for every \(s\).**  There are
   faithful representations
   \[
   \pi_n:H_n(3,6)\longrightarrow M_{(2s)^n}
   \]
   with
   \[
   \pi_{n+1}(\iota_n(x))=\pi_n(x)\otimes I_{2s}
   \]
   after recursive unitary identifications.  Thus \(K_0\), Bratteli,
   central-rank, Perron--Frobenius, and one-sided inclusion arguments cannot
   distinguish odd and even \(s\).
4. **The missing datum is the second spatial shift.**  A local matrix must
   realize the two three-strand generators simultaneously as
   \[
   P_{12}=P\otimes I_d,\qquad P_{23}=I_d\otimes P.
   \]
   This is strictly stronger than an abstract representation or a
   one-sided compatible tower.  Since the Yang--Baxter equation is a
   three-site relation, this is also the earliest and only independent
   finite tensor-local obstruction: once it holds, every higher braid
   relation follows.
5. The published \(d=4\) witness has a previously useful exact signature.
   Its left and right one-site leg commutants are
   \[
   \mathcal C_L\cong M_2(\mathbb C),\qquad
   \mathcal C_R\cong\mathbb C^4.
   \]
   After identity stabilization by \(\mathbb C^m\), they become
   \[
   M_{2m}(\mathbb C),\qquad
   \bigoplus_{j=1}^4M_m(\mathbb C).
   \]
   This explains the factor \(4\) in the *known construction mechanism*.
   It is not yet proved to be forced for an arbitrary solution.

Accordingly, a genuine divisibility proof must extract a parity-bearing
algebra or cell system from the simultaneous tensor placement at three
sites.  It cannot come only from the abstract Jones--Wenzl tower.

## 1. One-sided tensor-tower coherence permits every \(s\)

Let
\[
A_n=H_n(3,6).
\]
Its simple modules are \(S_{\lambda,n}\), with admissible Young-graph
branching, and the required multiplicities in a hypothetical
\(d=2s\) tensor-space realization are
\[
m_{\lambda,n}=D_\lambda s^n.
\tag{1}
\]
The quantum dimensions satisfy
\[
\sum_{\nu:\lambda\nearrow\nu}D_\nu=2D_\lambda.
\tag{2}
\]

### Proposition 1.1

For every integer \(s\geq1\), there are faithful finite-dimensional
representations
\[
\pi_n:A_n\to\operatorname{End}(K_n),\qquad
\dim K_n=(2s)^n,
\]
with the Markov character, and unitary identifications
\[
K_{n+1}\cong K_n\otimes\mathbb C^{2s}
\]
under which
\[
\pi_{n+1}(\iota_n(x))=\pi_n(x)\otimes I_{2s}.
\tag{3}
\]

### Proof

Take
\[
K_n=\bigoplus_\lambda
S_{\lambda,n}\otimes\mathbb C^{D_\lambda s^n}.
\]
The established trace formula shows that this has dimension \((2s)^n\)
and has the required Markov character.  All multiplicities are positive,
so the representation is faithful.

Under restriction from \(A_{n+1}\) to \(A_n\), the multiplicity of
\(S_{\lambda,n}\) is
\[
\sum_{\nu:\lambda\nearrow\nu}D_\nu s^{n+1}
=2D_\lambda s^{n+1}
=(2s)D_\lambda s^n.
\]
This is exactly its multiplicity in \(K_n\otimes\mathbb C^{2s}\).
Finite-dimensional semisimple representations with the same simple
multiplicities are unitarily equivalent.  Choose one such unitary at each
step and use it recursively.  This proves (3).
\(\square\)

### Scope of the countermodel

Proposition 1.1 is a complete countermodel to any proposed obstruction
using only:

- central-idempotent ranks;
- the Bratteli diagram or its \(K_0\) group;
- inclusion multiplicities;
- Perron--Frobenius dimension vectors;
- compatibility with the **right tensor factor** in (3).

It does **not** construct an \(R\)-matrix.  The chosen unitary at level
\(n+1\) need not make the shifted copy of \(A_n\) act as
\[
I_{2s}\otimes\pi_n(A_n).
\]
Nor is the ambient partial trace automatically the Jones conditional
expectation on the whole of \(A_{n+1}\).  Those are cell/commuting-square
conditions not determined by the multiplicity vectors.

## 2. The quaternionic algebra does not impose \(2\mid s\)

Rowell embeds \(A_n\) into the complex algebra \(Q_n\) generated by
\[
u_1,v_1,\ldots,u_{n-1},v_{n-1}
\]
with
\[
u_i^2=v_i^2=-1
\]
and prescribed signed commutation relations.  Its dimension is
\[
\dim_\mathbb C Q_n=2^{2n-2}.
\]
The radical of the defining alternating form is trivial when \(3\nmid n\)
and has order \(4\) when \(3\mid n\).  Consequently,
\[
Q_n\cong
\begin{cases}
M_{2^{n-1}}(\mathbb C),&3\nmid n,\\[2mm]
\displaystyle\bigoplus_{j=1}^4M_{2^{n-2}}(\mathbb C),&3\mid n.
\end{cases}
\tag{4}
\]
This is the complex, split form of the quaternionic construction.

At a fixed level, the canonical coefficient trace of \(Q_n\) has a
representation on a space of dimension \((2s)^n\) for every \(s\):

- if \(3\nmid n\), take \(2s^n\) copies of the unique
  \(2^{n-1}\)-dimensional simple module;
- if \(3\mid n\), take \(s^n\) copies of each of the four
  \(2^{n-2}\)-dimensional simple modules.

The dimensions are respectively
\[
2s^n\,2^{n-1}=2^ns^n=(2s)^n
\]
and
\[
4s^n\,2^{n-2}=2^ns^n=(2s)^n.
\]
With equal block multiplicities in the second case, normalized matrix
trace is exactly the canonical trace.  Restriction along
\(A_n\hookrightarrow Q_n\) therefore has the required Markov trace and the
multiplicities (1).

This fixed-level construction does not provide the two spatial shifts
required of an ordinary localizer.  It does prove that neither the
quaternionic algebra nor its complex module dimensions can force \(s\) to
be even.

## 3. Why Frobenius--Schur parity is unavailable

The categorical generator is not self-dual.  Rowell lists the six
dimension-two objects as three dual pairs
\[
\{X_i,X_i^*\}_{i=1}^3.
\]
In particular,
\[
\operatorname{Hom}(\mathbf1,X\otimes X)=0,
\]
so the usual second Frobenius--Schur indicator of \(X\) does not furnish
a symmetric or symplectic form on a local model.

More fundamentally, an ordinary localization in the sense used here is a
faithful morphism of the **endomorphism-algebra tower**.  It is not a rigid
monoidal functor on the full fusion category.  It does not provide:

- evaluation and coevaluation morphisms;
- a chosen image of a trivalent invariant tensor;
- conjugate equations;
- a real or quaternionic antiunitary on the one-site space.

The rank of the categorical unit block at three strands makes the
distinction concrete.  Since \(D_{\mathbf1}=1\), that block has matrix rank
\[
s^3
\]
in a \(d=2s\) localization.  A full tensor functor would send the single
copy of \(\mathbf1\subset X^{\otimes3}\) to a rank-one summand.  For
\(s>1\), the localization plainly does something different.

Thus a categorical FS or associator obstruction can be used only after a
new theorem upgrading every matrix localization to an appropriate module
or cell functor.  The existing \(d=4\) localization, together with the
absence of a fiber functor for the full category, already shows that such
an upgrade cannot simply be a fiber functor.

## 4. Why a real Brauer-class argument also fails

The term “quaternionic” in the older construction refers to generators
with quaternion-like relations.  It does not put the present problem over
\(\mathbb R\):

- the local spaces and matrices are complex;
- no conjugation commuting with an arbitrary solution is part of the
  defining relations;
- \(\operatorname{Br}(\mathbb C)=0\), so every finite-dimensional central
  simple complex algebra is a matrix algebra.

There is indeed a canonical complex Clifford algebra on the generic
three-strand sector.  The two-projection decomposition gives
\[
c=3s^3
\]
generic two-dimensional blocks, hence a generic sector of dimension
\[
6s^3.
\]
The canonical anticommuting reflections generate
\[
\operatorname{Cl}_2(\mathbb C)\cong M_2(\mathbb C)
\]
there, with module multiplicity \(3s^3\).  This is integral for every
\(s\).  To obtain \(2\mid s\), one would have to prove that a copy of
\(\operatorname{Cl}_2(\mathbb C)\) descends to an independently defined
\(s\)-dimensional multiplicity factor.  No such factorization follows
from the abstract two-projection relation.

In particular, the frequently tempting step
\[
\text{“three-strand Clifford action”}
\Longrightarrow
\text{“Clifford action on }\mathbb C^s\text{”}
\]
is an unsupported assumption.

## 5. Determinants and central braid phases add no parity

Let \(\beta\in B_n\) have exponent sum \(w(\beta)\).  Tensor locality gives
\[
\det\rho_n(\beta)
=\det(R)^{d^{n-2}w(\beta)}.
\tag{5}
\]
But each generator in the abstract \(A_n\)-representation has the two
eigenvalues \(-1,q\), each with multiplicity \(d^n/2\).  Therefore
\[
\det\rho_n(\sigma_i)
=(-1)^{d^n/2}q^{d^n/2}
=\det(R)^{d^{n-2}}.
\]
Multiplicativity proves (5) abstractly for every braid word.  Full twists
and other central braid elements therefore cannot add a determinant
congruence beyond the two-strand half-rank condition.

## 6. The first genuine spatial obstruction is already at three sites

At the abstract level, the three-strand representation exists for every
\(s\).  With
\[
p=P_{12},\qquad r=P_{23},
\]
its canonical block multiplicities are
\[
\dim(\operatorname{ran}p\cap\operatorname{ran}r)=s^3,
\]
\[
\dim(\ker p\cap\ker r)=s^3,
\]
and
\[
3s^3
\]
generic two-dimensional blocks, all with squared principal-angle cosine
\(1/3\).

The unresolved constraint is not this block decomposition.  It is the
simultaneous spatial identity
\[
p=P\otimes I_{2s},\qquad r=I_{2s}\otimes P
\tag{6}
\]
for one and the same \(P\in M_{(2s)^2}\).

This gives a useful stopping rule for higher-strand obstruction searches:

> A genuinely new \(n\ge4\) braid relation cannot be the first obstruction.
> For a fixed two-site \(P\), all higher relations follow from the
> three-site equation and far commutativity.  Any “higher coherence”
> theorem must ultimately descend to an invariant of the spatial
> realization (6), not merely to another abstract central-idempotent rank.

The correct finite problem is therefore an orbit/connection problem for
the pair in (6).  A flat biunitary or Ocneanu-cell formulation remains a
credible route, but its cell equations must encode both tensor embeddings.
The Bratteli graph and dimension vector alone do not.

## 7. Exact leg algebras of the published solution

For a two-site reflection \(H\), define the one-site leg commutants
\[
\mathcal C_L(H)
=\{a\in M_d:[a\otimes I_d,H]=0\},
\]
\[
\mathcal C_R(H)
=\{a\in M_d:[I_d\otimes a,H]=0\}.
\]
Because \(P\), \(H\), and \(R\) are affine polynomials in one another,
they have the same leg commutants.

The exact computation for the published \(d=4\) matrix gives
\[
\boxed{
\mathcal C_L(H)\cong M_2(\mathbb C),\qquad
\mathcal C_R(H)\cong\mathbb C^4.
}
\tag{7}
\]
The first relative commutant of the associated Yang--Baxter endomorphism,
\[
\mathcal M_1
=\{a\in M_4:R^*(a\otimes I_4)R=I_4\otimes a\},
\]
is scalar:
\[
\mathcal M_1=\mathbb C I_4.
\tag{8}
\]
Thus (7) is not merely reducibility of the Yang--Baxter endomorphism.

The exact replay is:

```text
/Users/alec/Documents/Math/.venv/bin/python \
  scripts/coherence_leg_commutant_d4.py
```

with recorded output in
`results/coherence_leg_commutant_d4.txt`.

### Stabilization

Let \(W=\mathbb C^m\), and stabilize by the identity \(R\)-matrix on \(W\).
After the standard reshuffling, the new operator is
\[
R' = R_{V_1V_2}\otimes I_{W_1W_2}
\]
on \((V\otimes W)^{\otimes2}\).

Expand \(a\in\operatorname{End}(V\otimes W)\) as
\[
a=\sum_j a_j\otimes b_j
\]
with the \(b_j\) linearly independent.  Then
\[
[a\otimes I,R']=0
\]
if and only if every \(a_j\in\mathcal C_L(R)\).  The same argument applies
on the right.  Hence the equalities, not merely inclusions,
\[
\mathcal C_L(R')=\mathcal C_L(R)\otimes M_m,
\qquad
\mathcal C_R(R')=\mathcal C_R(R)\otimes M_m.
\]
Using (7),
\[
\boxed{
\mathcal C_L(R')\cong M_{2m},\qquad
\mathcal C_R(R')\cong\bigoplus_{j=1}^4M_m.
}
\tag{9}
\]

This is a precise algebraic explanation of why the known stabilization
family has local dimension \(4m\).  In particular, its right leg carries
four equal central blocks of rank \(m\).

### Why this is not yet the divisibility theorem

Nothing established for an arbitrary exceptional solution says that
\(\mathcal C_R\) has four central blocks, or even that either leg
commutant is non-scalar.  Scalar partial traces do not determine leg
commutants.  Tensor flip exchanges the two algebra types in (7), and
braid-character equivalence is much weaker than preservation of their
concrete one-site embeddings.

There is also direct numerical warning against universalizing (7).  The
independent unrestricted complex \(d=4\) calibration in the falsifier track
converged to a different near-zero-residual solution.  Its measured
channel spectra and fixed/leg-algebra dimensions differ from those of the
sparse witness.  Because that second point is numerical rather than
exactified, it is not a classification result; it is recorded here only as
an assumption check.  None of the exact conclusions in this note depends
on it.

A valid sufficient statement would be:

> If every exceptional solution had, in one of its leg commutants, four
> nonzero central summands of equal representation rank, then \(4\mid d\).

Equation (9) verifies that hypothesis for the published family.  Proving
it universally is the missing theorem, not a consequence of current
trace or multiplicity data.

## 8. Additive constructions do not bypass the issue

The standard sum of \(R\)-matrices acts as \(R\) and \(S\) on the pure
summands and as tensor flip on the mixed summands.  If both summands are
nonzero, that mixed flip has eigenvalues \(+1\) and \(-1\).  Since the
exceptional spectrum is
\[
\{-1,e^{i\pi/3}\}
\]
and does not contain \(+1\), a nontrivial \(R\)-matrix sum cannot remain in
the exceptional two-eigenvalue class.

Thus a \(d=6\) solution cannot be obtained by the naive additive sum of a
\(d=4\) solution and a two-dimensional component.  This rules out one
construction mechanism but gives no nonexistence theorem.

## 9. Assumption ledger

| Proposed parity mechanism | Exact audit |
|---|---|
| Central ranks / Markov weights | Permit every \(s\) by (1) |
| One-sided tower embedding | Exists for every \(s\), Proposition 1.1 |
| Determinants / full twists | Fixed by the two-strand spectrum |
| Quaternionic algebra \(Q_n\) | Complex split modules exist at each level for every \(s\) |
| FS indicator of \(X\) | \(X\not\cong X^*\); no symplectic form is supplied |
| Fiber-functor obstruction | Localization is not a fiber functor; \(d=4\) already demonstrates the distinction |
| Three-strand Clifford sector | Has dimension \(6s^3\); imposes no parity on \(s\) |
| Flat connection / simultaneous shifts | **Still viable; not captured by multiplicities** |
| Four-block leg algebra | Exact for the known family; universality unproved |

## 10. Highest-value next steps

1. Recast (6) as an explicit finite biunitary-connection problem and
   retain the full cell data, not only the inclusion matrices.
2. Derive the leg algebras \(\mathcal C_L,\mathcal C_R\) invariantly from
   the three-site central projections, if possible.  Test whether four
   equal right-leg blocks are forced or are a special feature of the
   generalized-factorization witness.
3. For \(d=6\), enumerate possible finite-dimensional \(C^*\)-algebra
   types for both leg commutants and test each type against the spatial
   three-site equations.  A proof that both leg commutants must be scalar
   at \(s\) odd would not be a contradiction; a parity proof needs a
   forced non-scalar algebra with incompatible representation ranks.
4. Do not invoke a module-category or FS obstruction until an explicit
   functor from arbitrary local matrix data to the required rigid/cell
   structure has been proved.

The present audit therefore narrows the target sharply:

\[
\boxed{
\text{Any }4\mid d\text{ theorem must use the relative tensor position of }
P\otimes I\text{ and }I\otimes P.
}
\]

Neither the exceptional Hecke representation tower nor its quaternionic
realization contains the needed parity by itself.
