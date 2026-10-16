# Independent stabilization and split-map audit

Checkpoint: 2026-10-06 21:26 America/Los_Angeles (2026-10-07T04:26Z).
Auditor: independent stabilization subagent. Scope: family 047, Section 2,
including extraction of actual polynomial split maps and the special fiber.

## Finding and exact remaining gap

**PASS within this scope.** The pinned construction proves, without relying
on an unspecified stabilization isomorphism, that

\[
A=\mathbb C[p,s,u,F,J]/(H),\quad
x=s^2+u^3+p^2F,\quad
H=x^2F-(1+2sx)J-p^2J^2-pu
\]

is a smooth integral four-dimensional algebra and a retract of a polynomial
algebra in five variables. The algebraic retraction and the five-component
idempotent below are polynomial also at `p=0`.

**This does not prove nonpolynomiality.** The Costa counterexample still
requires the independent validation of Sections 3–6 of family 047. No result
about those sections, no claim of novel nonpolynomiality, and no Lean proof
claim is made in this audit.

Best-guess completion: stabilization/split-map subtask **100%**;
full mathematical Costa counterexample **40%** based on this subtask alone;
publication package **0%** from this subtask alone. These estimates are not
proof evidence; the root log may use better global estimates.

## Pinned evidence

Source clone inspected read-only: `/Users/alec/Desktop/math`.
`git rev-parse HEAD` returned `adc7f1241b42e322a6451854ab7e4b4c146bf78a`.

| File | SHA-256 |
|---|---|
| `preprints/An-explicit-failure-of-complex-affine-space-cancellation-September-23-2026/build/sections/02-construction.tex` | `fd10c0e2eb35a5572f43263ba88ea893551415c1807f6f6c8ad6158e64caa882` |
| `lean/docs/047.md` | `133fd3537a8cd213bf611b4bd2c7f71853aecd506adb8686dd1049e8b85324aa` |
| family 047 `paper.pdf` | `91a1a2f28c960cba25dd268e0f5515f0cff31463e4342098bbd89f857dd82023` |

The README identifies the upstream author as OpenAI and date as September
23, 2026. The construction is attributed in the source to the
El Kahoui–Ouali residual-coordinate method, the Dutta–Lahiri theorem, and
Edo–Vénéreau transfer criterion. The extraction below is an explicit
consequence of that supplied construction, not an independent cancellation
breakthrough.

## Domain, dimension, and smoothness

Inverting `p`, the change from `(s,u,F,J)` to `(x,y,z,u)` has inverse

\[
y=s+x(x-u^3),\quad z=sx+p^2J,
\qquad s=y-x(x-u^3),\quad
F=p^{-2}(x-s^2-u^3),\quad J=p^{-2}(z-sx).
\]

The verified identity

\[
xy-z(z+1)=p^2(H+pu)
\]

therefore makes `H` a coordinate over `C[p,p^{-1}]`, with unit coefficient
`-p` of `u`. Consequently `A[p^{-1}]=C[p,p^{-1},x,y,z]`. The polynomial
`H` is irreducible there. Its reduction modulo `p` is

\[
L=x_0^2F-(1+2sx_0)J,\qquad x_0=s^2+u^3,
\]

which is nonzero, so `p` does not divide `H`. In the polynomial UFD, any
extra irreducible factor made invertible by localizing at `p` would have
to be `p`, which was excluded. Thus `H` is irreducible and prime. `A` is
an integral domain, `p` is nonzero, and its fraction field has transcendence
degree four. These facts justify every cancellation of a power of `p`
below.

Smoothness can be checked without the polynomial-cylinder theorem. For
`p!=0` the above coordinate change makes the hypersurface smooth. At
`p=0`, its partial derivatives in `F,J` are respectively `x_0^2` and
`-(1+2sx_0)`. They cannot vanish simultaneously: if `x_0=0`, the second
is `-1`. The complex Jacobian criterion therefore proves that `Spec A`
is smooth. This statement involves all closed points; the finite-type
complex hypersurface has empty singular locus.

## First coordinate isomorphism, with both directions

Work initially in `P[w]=C[p,s,u,F,J,w]` and abbreviate `x=s^2+u^3+p^2F`.
For a polynomial indeterminate `w`, define

\[
D(u,w)=-3u^2w+3p^2uw^2-p^4w^3.
\]

The polynomial automorphism `Phi` is

\[
\begin{aligned}
\Phi(p)&=p,&\Phi(w)&=w,&\Phi(u)&=u-p^2w,\\
\Phi(s)&=s+p^2xD(u,w),\\
\Phi(F)&=F-(1+2sx)D(u,w)-p^2x^2D(u,w)^2,\\
\Phi(J)&=J-x^2D(u,w).
\end{aligned}
\]

Its inverse uses the same formulas with `w` replaced by `-w`. The exact
identity `D(u,w)+D(u-p^2w,-w)=0` verifies one composition; exchanging the
sign of `w` verifies the other. The checking script independently checks
both orders on all four moving generators. `p,w` are fixed.

The identities `Phi(x)=x`, `Phi(y)=y`, and `Phi(z)=z` hold as polynomials,
and `Phi(H)=H+p^3w`. Equivalently these formulas realize the locally
nilpotent derivation

\[
\Delta p=0,\quad \Delta u=-p^2,\quad
\Delta s=-3p^2xu^2,\quad
\Delta F=(6sx+3)u^2,\quad \Delta J=3x^2u^2,
\]

for which `Delta x=0` and `Delta H=p^3`. This is not an assumed formal
exponential: the finite polynomial formulas above suffice.

Hence the algebra-map direction is

\[
\bar\Phi:A[w]\longrightarrow
T=P[w]/(H+p^3w),\qquad [f]_{H}\longmapsto[\Phi(f)]_{H+p^3w}.
\]

It is an isomorphism, and `T` is a domain with nonzero `p`.

## Second coordinate isomorphism, with both directions

Use independent polynomial coordinates `(p,s,u,m,e)` for
`R_5=C[p,s,u,m,e]`. The symbol `m` distinguishes an independent coordinate
from the polynomial `M` in the original ring. In `P` put

\[
\begin{aligned}
x_0&=s^2+u^3,\\
L&=x_0^2F-(1+2sx_0)J,\\
M&=(1-2sx_0)F+4s^2J.
\end{aligned}
\]

The determinant is one, and the inverse is

\[
F(L)=4s^2L+(1+2sx_0)M,\qquad
J(L)=(2sx_0-1)L+x_0^2M.
\]

To avoid any division in the formulas, set

\[
\begin{aligned}
a&=4s^2,& b&=1+2sx_0,&c&=2sx_0-1,&d&=x_0^2,\\
C&=M^2(2x_0+6sx_0^2+4s^2x_0^3-x_0^4),\\
q_1&=M\bigl(4x_0ab-2s(ad+bc)-2cd\bigr),\\
q_2&=2x_0a^2-2sac-c^2,\\
Q(L)&=2x_0F(L)^2-2sF(L)J(L)-J(L)^2
      =C+q_1L+q_2L^2,\\
Q_1(L)&=q_1+q_2L,\qquad L_*=pu-p^2C.
\end{aligned}
\]

Thus

\[
H(L)=L-pu+p^2Q(L)+p^4F(L)^3.
\]

Define `h=u-pQ(L)-p^3F(L)^3-p^2w` and

\[
e_0=-w-pF(L)^3-Q_1(L)h.
\]

The exact polynomial certificate is

\[
p^3e_0-(L-L_*)=(p^2Q_1(L)-1)(H(L)+p^3w).
\]

The algebra isomorphism `q:R_5->T` fixes `p,s,u`, sends `m` to `M`, and
sends `e` to the class of `e_0`. Its inverse `g:T->R_5` uses

\[
\begin{aligned}
\ell&=pu-p^2C+p^3e,\\
f&=a\ell+bm,\qquad j=c\ell+dm,\\
W&=-e-(u-pC+p^2e)Q_1(\ell)-pf^3.
\end{aligned}
\]

Here every `M` in the coefficient formulas is replaced by `m`.
Explicitly `g(L)=ell`, `g(F)=f`, `g(J)=j`, and `g(w)=W`.
The identity `H(ell)+p^3W=0` makes `g` well-defined, and direct symbolic
substitution gives `g(e_0)=e`, hence `gq=id`.

For the other composition, the certificate gives `qg(L)=L` in `T`.
The two relation identities give
`p^3(qg(w)-w)=0`, hence `qg(w)=w` because `T` is a domain and `p!=0`.
This latter step is valid at `p=0` as a global ring equality; it does not
invert `p` in the answer. A checkable ideal certificate before passage
to the quotient is also available. Put `R=p^2Q_1(L)-1` and
`Ht=H(L)+p^3w`, so `L_*+p^3e_0=L+R Ht`. If
`H(L)=h_0+h_1L+h_2L^2+h_3L^3`, let

\[
K(Z,L)=h_1+h_2(Z+L)+h_3(Z^2+ZL+L^2).
\]

The script verifies `H(Z)-H(L)=(Z-L)K(Z,L)`, and therefore

\[
p^3(W(e_0)-w)=-Ht\bigl(1+R K(L+R Ht,L)\bigr).
\]

This explicitly locates the remaining composite in the defining ideal
up to the justified power-of-`p` cancellation.

## Split maps and five polynomial components

Set `theta=barPhi^{-1} q:R_5->A[w]`. Let `i:A->A[w]` be coefficient
inclusion and `epsilon:A[w]->A` evaluation at `w=0`. The exact algebra
maps are

\[
\jmath=g\bar\Phi i:A\longrightarrow R_5,\qquad
r=\epsilon\bar\Phi^{-1}q:R_5\longrightarrow A.
\]

The retraction `r` sends `(p,s,u,m,e)` to

\[
\bigl(p,s,u,M,e_A\bigr),\qquad
 e_A=-pF^3-Q_1(L)\bigl(u-pQ(L)-p^3F^3\bigr)\in A.
\]

This follows because evaluating `Phi^{-1}` at `w=0` gives the identity.
The inclusion `jmath` is explicit: compute `ell,f,j,W` above, put

\[
\begin{aligned}
X&=s^2+u^3+p^2f,\\
D&=-3u^2W+3p^2uW^2-p^4W^3,\\
S&=s+p^2XD,\quad U=u-p^2W,\\
\mathcal F&=f-(1+2sX)D-p^2X^2D^2,\\
\mathcal J&=j-X^2D.
\end{aligned}
\]

Then `jmath(p,s,u,F,J)=(p,S,U,mathcal F,mathcal J)`. In particular
`H(p,S,U,mathcal F,mathcal J)=0`; this follows from the certified
`Phi(H)=H+p^3w` and `H(ell)+p^3W=0`.

The five-component algebraic idempotent `rho=jmath r:R_5->R_5` is
obtained using exactly the same coefficient formulas on
`(S,U,mathcal F,mathcal J)`. Define

\[
\begin{aligned}
X_0'&=S^2+U^3,\\
L'&=(X_0')^2\mathcal F-(1+2SX_0')\mathcal J,\\
M'&=(1-2SX_0')\mathcal F+4S^2\mathcal J,\\
Q'&=2X_0'\mathcal F^2-2S\mathcal F\mathcal J-\mathcal J^2,\\
Q_1'&=q_1(S,U,M')+q_2(S,U)L',\\
E'&=-p\mathcal F^3-Q_1'\bigl(U-pQ'-p^3\mathcal F^3\bigr).
\end{aligned}
\]

The explicit point map of affine five-space is

\[
(p,s,u,m,e)\longmapsto(p,S,U,M',E').
\]

The associated pullback on coordinate functions is the same component
substitution `rho`. Algebra-map compositions give

\[
r\jmath=\epsilon\bar\Phi^{-1}qg\bar\Phi i
=\epsilon i=\operatorname{id}_A,
\qquad \rho^2=\jmath(r\jmath)r=\rho.
\]

Thus `jmath` is injective, `r` is surjective, and `im rho=jmath(A)`.
On schemes, these reverse direction: `Spec r:Spec A->A^5` is the closed
embedding, `Spec jmath:A^5->Spec A` is its left inverse, and their
composite on affine five-space is the displayed point map.

## Special fiber and verification scope

Every displayed expression is polynomial; there are no hidden inverses
of `p`. The special fiber also has a short check. Write
`q_1=kappa(s,u) m` and set `W0=-e-u kappa m`. Modulo `p`, the five
components become

\[
(0,s,u,m+3u^2W_0,-u\kappa(s,u)(m+3u^2W_0)).
\]

At the image, `W0=0`, so this map is visibly idempotent. It has no
exception at `s=0`, `u=0`, `x_0=0`, or `m=0`.

`verification/stabilization/check_stabilization.py` verifies **32 exact
symbolic polynomial identities** over the integers and **7 exact rational
point checks** for the actual factored endomorphism, including `p=0`.
The global idempotence assertion rests on the proved inverse-map
compositions, not on finitely many point checks. Both orders of `Phi`
and its inverse are checked. The generic coefficient calculation is
valid after `X=x_0` substitution and includes all degeneracies because
no coefficient is inverted.

The script is portable and accepts optional `--upstream-root` to verify
the pinned construction hash. It does not need the source clone for
its mathematical checks. It ran with Python 3.14.6 and SymPy 1.14.0
(mpmath 1.3.0 installed as a dependency). `result.json` is the captured
PASS transcript. The disposable local `venv/` is excluded from Git and
must be excluded from any deposit.

Reproduce from this verification directory:

```sh
python3 -m venv venv
venv/bin/pip install -r requirements.txt
venv/bin/python check_stabilization.py
# Optional source-hash validation:
venv/bin/python check_stabilization.py --upstream-root /path/to/pinned/math
```
