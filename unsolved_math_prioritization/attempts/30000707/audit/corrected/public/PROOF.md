# Scoped results for OWR-1460-014

## Status and exact target

**UNSOLVED.** These are partial deductions, not a resolution or a priority claim.
The source is Norbert Steinmetz's Problem 2, Oberwolfach Report 9/2007,
printed p.542, with the definitions on p.541. Let distinct nonconstant
meromorphic functions on the whole complex plane share four distinct values
$a_1,a_2,a_3,\infty$ ignoring multiplicity. Set

\[
 P(w)=\prod_{j=1}^3(w-a_j),\quad
 \psi_1=\frac{f'(f-g)}{P(f)},\quad
 \psi_2=\frac{g'(f-g)}{P(g)}.
\]

For $Q=z$ and $Q=z^2$, separately, classify solutions of
$\psi_1=e^Q,\ \psi_2=e^{-Q}$, with the equivalence described in the report.
We impose neither bounded spherical derivative nor periodicity nor finite
order as an extra assumption. CM means equality of multiplicities at every
preimage; an omitted value is shared CM. All identities are meromorphic
identities, including their removable singularities.

The exact gap is to exclude (or construct) a pair for which each of the three
finite shared values fails CM sharing. The reductions below do not exclude
such a pair. In particular, a recent claimed finite-order 3IM+1CM theorem is
not used as an established dependency; see DEPENDENCY_CHECK.md.

## 1. Local divisor constraints

Write $E=e^{Q(z)}$, so $E$ never vanishes.

### Proposition 1

Every common pole is simple for both functions and their leading residues
are different. At every finite shared value, if its multiplicities are
$m,n$, then $\min(m,n)=1$, and
\[
 E(z_0)^2=m/n. \tag{1}
\]
When $m=n=1$, the leading coefficients of $f-a_j$ and $g-a_j$ differ.
There are no other finite critical values of either function, and no
coincidence $f(z_0)=g(z_0)$ at a finite value outside the shared list.

**Proof.** At a common pole with orders $m,n$, suppose $m>n$. The orders of
$\psi_1,\psi_2$ are respectively $m-1$ and $2n-m-1$. Both must be zero,
which would require $m=1$ and $n=m$, a contradiction. Interchange $f,g$ if
$n>m$. If $m=n$ and the leading pole coefficients differ, both orders are
$m-1$, hence $m=n=1$. If those coefficients agree, the cancellation in
$f-g$ makes both orders at least $m$, impossible.

At a finite shared value $a$, write
$f-a=A t^m+\cdots$, $g-a=B t^n+\cdots$ with $t=z-z_0$ and $AB\ne0$.
Since $P'(a)\ne0$, each auxiliary function has order
$\operatorname{ord}(f-g)-1$. Thus $\operatorname{ord}(f-g)=1$ and
$\min(m,n)=1$. Furthermore
\[
 \frac{\psi_1}{\psi_2}
 =\frac{f'/P(f)}{g'/P(g)}\longrightarrow m/n,
\]
proving (1). The remaining assertions follow because a derivative zero or
an extra finite coincidence would be a zero of an auxiliary function. A
pole of the other function cannot intervene because poles are shared. ∎

### Corollary 1 (poles and integer loci)

The value $\infty$ is automatically shared CM. At every finite shared point,
for some integer $k\ge1$ and $\ell\in\mathbb Z$,
\[
 Q(z_0)=\pm\tfrac12\log k+\pi i\ell. \tag{2}
\]
If the residues at a common pole are $A,B$, then for some $s\in\{1,-1\}$,
\[
 A=s-E(z_0)^{-1},\qquad B=E(z_0)-s. \tag{3}
\]
In particular $E(z_0)\ne s$ for the chosen sign.

Indeed, the local auxiliary values are $-(A-B)/A^2=E$ and
$-(A-B)/B^2=E^{-1}$. Consequently $B=sEA$, and solving gives (3).

These facts alone do not force $k=1$ in (2).

## 2. Growth and sector confinement

We use the established Nevanlinna estimates stated and proved in Steinmetz,
*Reminiscence of an Open Problem*, arXiv:1102.3383v1, §6, pp.12–14
(published Southeast Asian Bulletin of Mathematics 36 (2012), 399–417).
Put $T(r)=\max(T(r,f),T(r,g))$ and
$\Phi=\psi_1/\psi_2$. We also use the same paper's §1, printed p.2,
formula (Na) in the $q=4$ case of the Five-Value-Theorem:
$T(r,f)=T(r)+S_f(r)$ and $T(r,g)=T(r)+S_g(r)$, with each remainder
$O(\log(rT(r)))$ outside a set of finite linear measure. This comparison
requires only four distinct values shared IM, so it applies to the exact
hypotheses here, including infinity; it assumes neither finite order nor
any additional CM value. At least one function is transcendental, since
otherwise $\Phi=e^{2Q}$ would be rational. Hence
$T(r)/\log r\to\infty$, the usual characteristic criterion for
transcendence, and these remainders are $o(T(r))$. Formula (Na) also
excludes a mixed rational/transcendental pair, since a rational function
has characteristic $O(\log r)$ while each individual characteristic is
$T(r)+o(T(r))$ off the exceptional set. Both functions are transcendental.

The §6 theorem says that for four shared values with
$\infty$ shared CM, either the classical four-value conclusion holds, or
\[
 \frac5{209}T(r)\le T(r,\Phi)+S(r)\le2T(r)+S(r),\qquad S(r)=o(T(r)), \tag{4}
\]
outside a set of finite linear measure. This is an explicitly attributed
external standard input, not a new theorem proved by the controls.

Here $\Phi=e^{2z^d}$, $d=1$ or $2$, and
$T(r,\Phi)=2r^d/\pi$. In the non-CM case, (4) gives
\[
 T(r)\asymp r^d. \tag{5}
\]
For completeness, the exceptional set causes no gap: absorb the $o(T)$
term off that set to obtain $T(r)\le C r^d$. Its tail has measure less than
one, so every sufficiently large interval $[r,r+1]$ contains a point where
the bound holds. Monotonicity of $T$ extends it to all sufficiently large
$r$. The reverse inequality follows similarly from (4). Formula (Na)
then gives $T(r,f)\asymp r^d$ and $T(r,g)\asymp r^d$ off the union of
the finite-linear-measure exceptional sets. These individual bounds extend
to every sufficiently large $r$: use a good point in $[r,r+1]$ for each
upper bound and one in $[r-1,r]$ for each lower bound, and use monotonicity
of each characteristic. The tail measure of the union is less than one,
so these good points exist. Each individual function consequently has
exact order $d$. The classical CM case is classified in §3 and has order
one in the first system; it is impossible in the second. Thus both functions
in every possible first-system solution have finite order one, and both
functions in every hypothetical second-system solution have finite order two.

A useful additional elementary consequence is
\[
 |\Re Q(z_0)|\le\tfrac d2\log|z_0|+C \tag{6}
\]
for all sufficiently distant finite shared points. To prove it, a zero of
multiplicity $m$ at $|z_0|=r$ contributes $m\log2$ to
$N(2r,1/(f-a_j))$. The first main theorem and (5) bound this by $C_1r^d$;
the same applies to $n$. By Proposition 1, one of $m,n$ equals one, and
(1) gives (6). Hence those points concentrate near the Stokes directions
$\Re z^d=0$, but (6) does not bound all their multiplicities by one.

## 3. Complete classification when there is another CM value

### Proposition 2

If at least one finite shared value is shared CM, then:

* For $Q=z$, there is $b\in\mathbb C$ such that
  \[
  \{a_1,a_2,a_3\}=\{b-1,b,b+1\},\quad
  f=b-e^{-z},\quad g=b-e^z. \tag{7}
  \]
* For $Q=z^2$, there is no solution.

**Proof.** Proposition 1 supplies CM sharing of $\infty$. Gundersen's
classical 2CM+2IM theorem (Trans. Amer. Math. Soc. 277 (1983), 545–567,
with its correction in 304 (1987), 847–850; recalled and reproved in
Steinmetz §§2–3) then supplies all four CM values. The classical
four-value theorem says that two of the shared values are omitted, and
that $g=M\circ f$ for the involution fixing the other two and interchanging
the omitted pair.

If $\infty$ is not one of the omitted values, it is fixed by $M$. A
nonidentity Möbius involution fixing $\infty$ has form $M(w)=2b-w$.
The other fixed value is $b$, and the omitted pair is $b\pm k$, $k\ne0$.
Thus $P(w)=(w-b)((w-b)^2-k^2)$ and $g=2b-f$. Direct substitution gives
$\psi_1=\psi_2$, contrary to $e^Q\not\equiv e^{-Q}$.

If $\infty$ is omitted, the other omitted value is finite, call it $b$.
The two fixed values are $b\pm k$ and
$(f-b)(g-b)=k^2$, where $k\ne0$. Since $f-b$ is entire and zero-free,
there exists an entire $h$ with
\[
 f=b+ke^h,\quad g=b+ke^{-h}.
\]
Direct calculation, including removable continuations, gives
\[
 \psi_1=(h'/k)e^{-h},\qquad \psi_2=(h'/k)e^h. \tag{8}
\]
Their product implies $(h'/k)^2=1$, hence $h'/k=\epsilon\in\{1,-1\}$
with constant sign. The first identity in the prescribed system now gives
$e^{-h}=\epsilon e^Q$ and therefore $h'=-Q'$. Thus $Q'$ is a nonzero
constant. This excludes $Q=z^2$. For $Q=z$ we have $\epsilon k=-1$;
substitution yields (7), and the shared values have $k^2=1$.
Conversely, (7) shares exactly the indicated values with multiplicities
and gives the prescribed auxiliaries. ∎

The source's suggested representative $(e^{-z},e^z)$ lies in the same
Möbius/affine equivalence class. With the literal definitions its two
auxiliaries have minus signs. The negative pair in (7) with $b=0$ is an
exact representative of the displayed system. This is a normalization
check, not a claim that the source's equivalence-class assertion is false.

## 4. Differential elimination and local pole rigidity

Set $u=e^{-Q}$ and retain $P$ monic cubic. Away from the discrete set
where the expressions require continuation, the first equation determines
\[
 g=f-e^Q P(f)/f'. \tag{9}
\]
Substitution in the second, followed by the exact cubic Taylor identity,
yields the following necessary scalar equation:
\[
 P(f)f''-\left(Q'P(f)+\frac u2P(f)P''(f)\right)f'
 +(u^2-1)P'(f)(f')^2 +(u-u^3)(f')^3+P(f)^2=0. \tag{10}
\]
On any open set where $f'P(f)(f-g)\ne0$, (9) and (10) are also sufficient
for the two differential identities. They do not by themselves enforce
global meromorphic continuation or sharing of the four values.

There is a useful formal pole constraint. Fix $z_0$ and a sign $s$ in (3),
write $a=e^{Q(z_0)}$, and insert
$f=A/t+\sum_{k\ge0}F_kt^k$, $g=B/t+\sum_{k\ge0}G_kt^k$
into $f'(f-g)=e^QP(f)$, $g'(f-g)=e^{-Q}P(g)$. The coefficient matrix
for $F_k,G_k$ at order $t^{k-2}$ is
\[
 \begin{pmatrix}
 k(A-B)-A-3aA^2&A\\
 -B&k(A-B)+B-3a^{-1}B^2
 \end{pmatrix}.
\]
Its determinant is
\[
 \frac{(a-s)^4}{a^2}(k+2)(k+3), \tag{11}
\]
nonzero for every integer $k\ge0$. Therefore any actual meromorphic pole
germ is uniquely determined by $z_0$, the sign and the fixed parameters.
No claim of convergence of a formal series or existence of any such pole
germ follows from this argument. In particular, periodic coefficients do
not imply a periodic global solution: translating a pole need not produce
another pole of that same solution. This is the precise obstruction in
this differential-equation approach.

## 5. A rigorous low-degree rational-exponential exclusion

### Proposition 3

Suppose a solution of the first system has $f(z)=R(e^z)$,
$g(z)=S(e^z)$ with rational $R,S$ of degree at most two. Then it is (7).
There is no noncanonical pair in this ansatz.

**Proof.** Put $x=e^z$. The equations become rational identities
\[
 R'(R-S)=P(R),\qquad x^2S'(R-S)=P(S). \tag{12}
\]
At $x=\infty$, comparing orders proves that $R$ tends to a finite root $a$
of $P$, while $S=-x+O(1)$. Here are all the alternatives: if both have
poles of unequal orders $m,n$, the powers in the two auxiliaries would
require $\max(m,n)-2m=1$ and $\max(m,n)-2n=-1$, which forces $m=0$.
Equal orders, including cancellation in $R-S$, give the same exponent in
both auxiliaries and cannot work. If only $R$ has a pole, its first
auxiliary decays. If neither has a pole, the first auxiliary is bounded
or decays, whether or not either limit is a root of $P$. In the remaining
case, $S\sim Bx^n$ gives second auxiliary $-n B^{-1}x^{-n}$, hence
$n=1$, $B=-1$. The first auxiliary then forces $R$ to tend to a root.
If $R-a\sim Cx^{-r}$, comparison gives $P'(a)=-r$.

The corresponding comparison at $x=0$ proves
$R=-1/x+O(1)$ and $S$ tends to a root of $P$. In $\mathbb C^*$ all poles
are common and simple by Proposition 1. Thus both rational degrees are
one plus the number of these common poles.

Translate the dependent variables to arrange $R(\infty)=0$. Then
$P(w)=w^3+pw^2+qw$.

With no common pole, $R=-1/x$, $S=-x+B$. The two identities (12) give
$q=-1$, $p=-B$ and $p=-2B$. Thus $B=p=0$, giving (7).

With one common pole at $c\in\mathbb C^*$, residue formula (3) gives
\[
 R=-\frac1x+\frac{sc-1}{x-c},\qquad
 S=-x+B+\frac{c^2-sc}{x-c},\quad s=\pm1,\quad c\ne s. \tag{13}
\]
The transformation
$(R(x),S(x),P(w))\mapsto(-R(-x),-S(-x),-P(-w))$
preserves (12) and sends the $s=-1$ case to $s=1$. It suffices to use
$s=1$, so $c\ne0,1$.

Let $N_1,N_2$ be the numerators in (12) after moving right to left,
with respective denominators $x^2(x-c)^2$ and $(x-c)^2$.
The leading coefficient of $N_2$ is $-2B-p$, so $p=-2B$.
At infinity $R\sim(c-2)/x$ unless $c=2$.
If $c=2$, $R\sim2/x^2$ and $q=P'(0)=-2$.
The coefficients of $x$ and $1$ in $N_1$ are then $4(B-1)$ and
$4(B+2)$, contradictory.

Otherwise $q=-1$. The constant coefficient of $N_1$ gives
$B=-c-1+2/c$. After substitution, its $x^2$ and $x$ coefficients are
\[
 -2(c-1)(c^3-c^2-4c+6)/c,
 \qquad -4(c-1)(c^2-2).
\]
Since $c\ne1$, they force $c^2=2$ and $c^3-c^2-4c+6=0$.
The latter then becomes $4-2c=0$, forcing $c=2$, incompatible with
$c^2=2$. There is no actual common pole. ∎

If a first-system solution is $2\pi i$-periodic, Steinmetz's established
§6 periodic theorem and §2 above make it rational in $e^z$. Proposition 3
excludes its degrees one and two unless it is canonical. Degrees at least
three and nonperiodic finite-type functions remain unclassified.

For the second system, the analogous ansatz $f=R(e^{z^2})$,
$g=S(e^{z^2})$ cannot work at any degree: $f,g$ are even, so $\psi_1$ is
odd, whereas $e^{z^2}$ is nonzero and even. Equivalently, simultaneous
composition with $z^2$ brings an unavoidable chain-rule factor $2z$.
There is no reason supplied here that a general second-system solution
must belong to that ansatz.

## What is and is not established

The first-system canonical family, the conditional CM classification,
local constraints, finite-order reduction, scalar elimination, and
rational degree-two exclusion have proofs above. The exact controls verify
only their encoded algebra and stated finite negative controls. They do
not prove the missing 3IM+1CM rigidity, certify all cited analytic theory,
or exhaust meromorphic functions. No full solution, novelty, first
priority, paper, DOI, or independent discovery shared with Problem 1 is
claimed. The work is substantially AI-assisted and unrefereed.
