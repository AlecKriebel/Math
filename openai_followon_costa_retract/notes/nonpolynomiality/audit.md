# Independent adversarial audit of family 047 nonpolynomiality

Checkpoint: 2026-10-06 21:26 PDT (2026-10-07 04:26 UTC).
Scoped audit completion estimate: 100%. This is an estimate of completion
of the assigned source audit, not an independent estimate of a new discovery.

## Scope and verdict

The pinned source defines

\[
A=\mathbb C[p,s,u,F,J]/(H),\quad
x=s^2+u^3+p^2F,\quad
H=x^2F-(1+2sx)J-p^2J^2-pu.
\]

I audited the actual nonpolynomiality chain in sections 3--6, while also
reading the construction, introduction, and consequences. No fatal gap,
hidden coefficient-preservation assumption, or counterexample was found.
The strongest verified deduction from this audit is that the explicit
graded presentation, bundle lift, extraction, and rigidity arguments form
a coherent proof of nonpolynomiality, given the standard regular-ring
facts explicitly used in the source. The stabilization proof is assigned
to a separate agent; this note does not replace its audit. Priority and
novelty are not inferred from this verdict.

The verdict comes from a direct reconstruction of the proof, not from
the project's triage. A second, initially independent agent audited the
line-bundle lift and reached the same scoped conclusion; its note is
`bundle_skeptic/audit.md`.

Source root, read-only throughout:

`/Users/alec/Desktop/math/preprints/An-explicit-failure-of-complex-affine-space-cancellation-September-23-2026`.

SHA-256 of the audited source files:

| File | SHA-256 |
|---|---|
| `03-degeneration.tex` | `01c8fba41829052c46ae2e1c34ace91283808c3bcd5a6adcfa58cdca1ad7424c` |
| `04-bundle.tex` | `37097f3689e0d41315a623c7d94e362141526f642ca8515682751f47a0ea5ae7` |
| `05-reduction.tex` | `8c6e5470bfc09d98f6cca44b461d3894034cc7b90f2bd379e47990753192f6b2` |
| `06-rigidity.tex` | `a15737c05af4fe6ec7f4af2552250bb9366c19f7c47dea3e13f492529fd50bf8` |

## Claim and exact success criterion

The claim audited is `A` not isomorphic to `C^[4]` as a complex algebra.
It suffices to establish the following contradiction chain:

1. Polynomiality supplies a nonzero homogeneous LND of the exact
   associated graded algebra `G`, fixing a nonzero homogeneous element
   of positive valuation degree.
2. That derivation lifts to the affine complement of a line bundle over
   `Spec G`, with the same valuation degree and fiber shift zero.
3. The lift produces a nonzero LND `E` of
   `Rt=C[a,d,b,c,u]/(ac-bd-1)` with fiber shift at most zero and
   `E^2(v)=0`, where `v=a^3 b-a^2u^3-d^2`.
4. No such `E` exists.

This audit would fail if any of those implications required an
unsupported invariant coefficient ring, an unproved surjectivity of the
graded generators, a nilpotence assumption after localization at a
moving element, or a nonsquare test only over an algebraic closure.
Those possible failure modes were checked explicitly below.

## Degeneration: exactness rather than just a candidate presentation

The ring

\[
S=\mathbb C[p,x,y,z,u]/(xy-z(z+1)-p^3u)
\]

injects into `A` because its localization at `p` identifies with that of
`A`, and `S` is a domain. Its quotient

\[
R=S/pS=\mathbb C[x,y,z,u]/(xy-z(z+1))
\]

is a smooth domain. Since `pS` is prime and the localized maximal ideal
is principal, the source's DVR construction and global divisibility
argument are valid. In particular, valuation coefficients of arbitrary
elements of `A` really lie in `R`, rather than merely `Frac(R)`.

The claimed initial generators have weights `(-1,0,0,2,2)`. The kernel
of their substitution into `R[tau,tau^-1]` is exactly `(Htop)`:
localization identifies it with the quadric relation, and contraction
uses the primality and `p`-saturation of `(Htop)`. The fact that this is
the **entire** associated graded ring is then proved by reducing the
maximum weight of a representative whenever its top part lies in the
kernel. The reduction changes the maximum by at least one (the added
term has weight three less than the removed top relation), and the
actual valuation degree supplies a fixed lower bound. Negative weights
therefore do not create an infinite descent.

This exact representative property is enough to bound any derivation's
degree shift from its values on the five generators. The induced top
derivation is nonzero because one generator attains the maximum shift.
Its iterates equal the indicated classes of the original iterates, so
local nilpotence survives without a sign restriction on the shift.

If `A` had polynomial coordinates, at least one coordinate would have
positive valuation degree because the nonpositive part is a proper
subalgebra (`F` has degree two). A partial derivative in a different
coordinate fixes it. Thus the needed positive homogeneous invariant is
established, rather than assumed.

## Bundle lifting: no additive preservation of `R` is used

The charts over `z+1` and `z` are Laurent polynomial charts of a line
bundle minus its zero section. They cover because `z` and `z+1` generate
the unit ideal. The principalization identities

\[
f=C_1v,\qquad g=b^2v,\qquad v=\alpha f+\beta g,
\qquad \alpha C_1+\beta b^2=1
\]

are exact modulo `ac-bd-1`; all four were checked independently by exact
polynomial arithmetic. Flat base change is applied to the actual
degree-zero inclusion `R -> G`, so the result is the displayed domain

\[
Gt=Rt[\tau,V]/(\tau^2V-v).
\]

Every Ga action on the smooth integral affine `Spec G` lifts to this
line bundle by the source's Picard-homotopy argument. The normalization
and cocycle steps are sound: any ratio of line-bundle isomorphisms is a
global unit, and for a domain `C[t]^*=C^*` and `C[s,t]^*=C^*`. Normalizing
at the group identity therefore gives uniqueness and forces the
cocycle. The induced action on the affine complement is algebraic, so
its derivation is locally nilpotent in characteristic zero.

Only the **degree torus** fixes `R` and `Rt`; the additive action is
allowed to move them. Its torus lift extends linearly to the total line
bundle. Conjugating the Ga lift by that torus lift and comparing with a
rescaling of the Ga parameter gives the required homogeneity by
uniqueness. This does not assume `D0(R)` contained in `R` or `Dt(Rt)`
contained in `Rt`.

The independent skeptic checked an actual boundary counterexample if
integrality is omitted: over `C[epsilon]/(epsilon^2)`, the trivial base
Ga action has the nontrivial normalized fiber multiplier
`1+epsilon*t`. This shows why the domain hypothesis matters; the pinned
source satisfies it.

## Extraction: removing the multiplier preserves local nilpotence

The degree pieces of `Gt` are exactly

\[
Gt_e=\begin{cases}
\tau^{-e}Rt&e<0,\\
V^\ell Rt&e=2\ell\ge0,\\
\tau V^{\ell+1}Rt&e=2\ell+1>0.
\end{cases}
\]

All positive pieces have a factor `V`. Factorial closure of an LND's
kernel therefore forces `Dt(V)=0` from the positive invariant.

If `tau` is invariant, localization at `tau` preserves nilpotence, and
`Dt(r)=tau^-j E(r)` gives a nonzero LND `E` on `Rt` of fiber shift zero
with `E(v)=0`.

If `tau` moves, the elementary fact `Dt(tau)` is not divisible by `tau`
forces its degree to be nonnegative even; hence `j=2ell+1` with
`ell>=0`. The exact components give

\[
Dt(r)=\tau V^{\ell+1}E(r),\qquad E(r)\in Rt.
\]

This is first an honest derivation on `Rt`, by cancellation of the
nonzero multiplier. No localization at the moving `tau` is used to
infer nilpotence. If `m=nu_Dt(tau)>=1`, product-additivity of the LND
order gives, whenever `E(r)` is nonzero,

\[
\nu_{Dt}(E(r))=\nu_{Dt}(r)-1-m.
\]

Iterates remain in `Rt` and strictly decrease a nonnegative integer,
proving that `E` is an LND. Its fiber shift is `-2(ell+1)`. Since
`nu_Dt(v)=2m`, a second nonzero `E`-iterate of `v` would have order `-2`,
which is impossible. This establishes `E^2(v)=0` with the required sign.

## Rigidity: independently reconstructed core argument

The auxiliary weights `(0,3,-3,0,2)` on `(a,d,b,c,u)` give a genuine
integer grading because `ac-bd-1` has degree zero. The maximal auxiliary
component `E'` of a nonzero LND is again a nonzero LND. This works even
when the maximal shift is negative: for every homogeneous input, the
component at the sum of maximal shifts is uniquely the iterate of the
maximal component, and the original iterate eventually vanishes.
Projection also preserves the separately fixed fiber shift.

The two auxiliary parts of `v` have degrees `-3` and `6`. Consequently
the component of `E^2(v)` at degree `6+2lambda` is exactly

\[
(E')^2(N),\qquad N=d^2+a^2u^3.
\]

There is no contribution from the lower auxiliary part, so `(E')^2(N)=0`.

Now work in the **original** field

\[
K=\operatorname{Frac}(Rt)=\mathbb C(a,d,b)(u).
\]

Exponentiation gives nonzero polynomials `A(q),D(q),U(q)` in `K[q]`
with constant terms `a,d,u`, satisfying

\[
D(q)^2+A(q)^2U(q)^3=N+qE'(N).
\]

The right side is nonzero and has degree at most one. A common root of
the two summands would have multiplicity at least two in each, hence
in their sum, which is impossible. Thus the abc inputs really are
pairwise coprime; there is no need to assume that `A` and `U` are
coprime to each other.

If either summand is nonconstant, both have the same degree

\[
M=2D_d=2D_a+3D_u\ge2.
\]

Mason--Stothers and the root bound give

\[
M\le D_d+D_a+D_u+\deg N(q)-1
\le D_d+D_a+D_u.
\]

Therefore `D_u=0`, then `D_d=D_a>0`. Cancellation of the highest terms
would yield a square root of `-u^3` in `K`. That is impossible because
the `u`-valuation of a square is even while that of `-u^3` is three.
The algebraic closure is used only to count roots; the leading
coefficients remain in `K`. It follows that `A,D,U` are constant, and

\[
E'(a)=E'(d)=E'(u)=0.
\]

Differentiating the determinant relation gives
`E'(b)=a h`, `E'(c)=d h`, with
`h=c E'(b)-b E'(c)` in `Rt`. Localization at the invariant nonzero
elements of `C0=C[a,d,u]` gives an LND of `Frac(C0)[b]`; the elementary
one-variable LND criterion implies `h` is in `Frac(C0)`. Comparing the
`a` and `d` charts then gives

\[
Rt\cap\operatorname{Frac}(C0)
\subset C0[a^{-1}]\cap C0[d^{-1}]=C0.
\]

Since `a,d` are relatively prime in the polynomial ring `C0`, the last
equality has no hidden denominator assumption. Nonzero `E'` gives
nonzero `h`, but `h` has fiber weight `e-2<0`, impossible in `C[a,d,u]`
whose monomials all have nonnegative fiber weight. This closes the
contradiction.

## Falsification attempts and boundaries

* The actual positive-root LND `E+(b)=a`, `E+(c)=d` fixes `a,d,u` and
  satisfies `E+(v)=a^4`, `E+^2(v)=0`. It has fiber shift `+2`, so it
  confirms that the sign restriction is necessary rather than
  contradicting the proposition.
* The obvious negative-root LND `E-(a)=b`, `E-(d)=c` has shift `-2`, but
  its second value on `v` is
  `6ab^3-2b^2u^3-2c^2`, a nonzero element of the determinant ring.
* The source's own derivation moving `u` to `-tau^2` demonstrates that
  coefficient preservation cannot be silently used. The lifting proof
  explicitly avoids doing so.
* Characteristic zero is required both for LND order additivity and
  exponentiation/abc. The actual base field is `C`.
* The odd exponent three supplies the nonsquare obstruction. A change
  to an even exponent would require a fresh rigidity argument; this
  proof should not be transferred to it by analogy.

The exact checks can be reproduced with `python check_certificates.py`
in this note directory using SymPy. Their output is recorded in
`symbolic_audit.txt`. Computation confirms certificates and explicit
boundary derivations; the generic LND claims above are deductions.

## Remaining gap and promotion limit

No mathematical gap was identified in the assigned nonpolynomiality
chain. The standard general facts used here are regular local rings
being factorial, Picard/divisor-class identification on a regular
affine scheme, the Jacobian criterion, and basic UFD/DVR facts. The
source supplies the relevant Picard-homotopy and polynomial abc
arguments directly, so the central difficulty is not transferred to
an equivalent conjecture.

This is an adversarial source audit by one agent plus an independent
bundle subaudit. It is not a machine-checked formal proof, an exhaustive
automated classification of LNDs, or a priority determination. No
external individual was contacted. No source file, branch, commit,
push, or release was changed by this agent.
