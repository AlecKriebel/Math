# Milestone 6B: `Omega_chain` is JC-specific

## Result

**PROVED.** The root path-reversal move `Omega_chain` has a
full-dimensional regular stochastic overlap under JC, but it is generically
separated under both K2P and K3P.

More precisely, let `Omega_2` have physical port order

\[
 (P_1,P_2,Q,X)
\]

in the source and

\[
 (P_2,P_1,X,Q)
\]

in the target.  For each model (M\in\{\mathrm{K2P},\mathrm{K3P}\}),
the two irreducible model closures are distinct.  Since the two networks are
leaf relabellings of the same directed graph, those closures have equal
dimension.  Their intersection is therefore lower-dimensional, and the two
open stochastic models cannot have a full-dimensional regular intersection.

**PROVED.** The same conclusion holds for every `Omega_chain` of length
(k\geq2).  Hence neither `Omega` nor any longer path reversal belongs to
the K2P or K3P observational move system.

This milestone strengthens the current model hierarchy:

| move | JC | K2P | K3P |
|---|---:|---:|---:|
| `Theta` | full-dimensional overlap | separated | separated |
| `Omega_chain` | full-dimensional overlap | separated | separated |
| `C_root` and contextual `C_root` | complete-image equality | complete-image equality | complete-image equality |

The complete K2P/K3P move systems remain unresolved.

## Conventions

Write a Fourier coordinate as (q_{g_1g_2g_3g_4}), where
(g_1\oplus g_2\oplus g_3\oplus g_4=0).  The K2P convention is

\[
 a_e(1)=s_e,\qquad a_e(2)=a_e(3)=t_e.
\]

For K3P write

\[
 a_e(1)=x_e,\qquad a_e(2)=y_e,\qquad a_e(3)=z_e.
\]

The edge indices (0,\ldots,11) are, in order,

\[
 U\!\to V, U\!\to P_1, P_1\!\to P_2, P_2\!\to V,
 S\!\to U, S\!\to X, V\!\to Q, Q\!\to X,
 P_1\!\to L_1, P_2\!\to L_2, Q\!\to L_3, X\!\to L_4.
\]

The inheritance parameters at (V,X) are (l_0,l_1).

## Explicit invariants

For a finite signed term list (mathcal T), put

\[
 I_{\mathcal T}(q)=
 \sum_{(c,M)\in\mathcal T}c\prod_{g\in M}q_g.
\]

The complete term lists are explicit and machine-readable in
`src/omega_k2p_quintic_terms.py`, `src/omega_k3p_sextic_terms.py`, and
`certificates/omega_model_hierarchy.json`.

### K2P

**EXACTLY COMPUTED.** The K2P list has 20 terms, every coefficient is
(\pm1), its coordinate degree is five, and its pendant multidegree is

\[
 (1,3,2,2,1,2,1,1).
\]

Direct sparse-polynomial substitution gives

\[
 I_{\rm K2P}\circ\phi_{\rm source}=0.
\]

On the target, the complete pullback factors as

\[
\begin{aligned}
-{}&l_0l_1^2(l_0-1)^2(l_1-1)(s_2-1)^3\\
&\cdot s_1s_3s_6s_8^2s_9s_{10}s_{11}
t_1^2t_2^2t_3t_4t_5t_6t_8^2t_9^3t_{10}t_{11}^2\\
&\cdot
\left(s_0t_4t_5s_6s_7-t_0s_4s_5t_6t_7\right).
\end{aligned}
\]

This is not the zero polynomial.

### K3P

**EXACTLY COMPUTED.** The K3P list has 52 terms, every coefficient is
(\pm1), its coordinate degree is six, and its pendant multidegree is

\[
(2,1,2,\ 2,2,0,\ 2,1,1,\ 1,1,0).
\]

Direct sparse-polynomial substitution gives

\[
 I_{\rm K3P}\circ\phi_{\rm source}=0.
\]

The target pullback has 648 monomials and the exact factorization

\[
\begin{aligned}
{}&l_0l_1^2(l_0-1)^3(l_1-1)^2\,\mathcal M\,
(x_2y_2-z_2)\\
&\quad\cdot
\left(x_2^3-x_2y_2^2-x_2z_2^2+2y_2z_2-x_2\right)\mathcal B,
\end{aligned}
\]

where

\[
\mathcal M=
z_{11}y_{11}y_{10}x_{10}y_9y_6x_6x_5x_4y_3x_3x_1
\cdot x_{11}^{2}z_9^{2}x_9^{2}y_8^{2}x_8^{2}
\]

and

\[
\begin{aligned}
\mathcal B={}&
y_0y_1z_1y_2x_3z_4z_5x_6y_6x_7y_7
-x_0x_1z_1x_2y_3z_4z_5x_6y_6x_7y_7\\
&-z_0y_1z_1y_2x_3y_4y_5x_6z_6x_7z_7
+z_0x_1z_1x_2y_3x_4x_5y_6z_6y_7z_7\\
&+x_0x_1y_1z_3y_4y_5x_6z_6x_7z_7
-y_0x_1y_1z_3x_4x_5y_6z_6y_7z_7.
\end{aligned}
\]

Thus this pullback is also not the zero polynomial.  The verifier records
all 24 irreducible factors and a SHA-256 digest of the ordered exact
factorization.

## Open stochastic witnesses

**EXACTLY COMPUTED.** For K2P, set every edge pair to
((s_e,t_e)=(1/2,1/2)), except (s_0=1/3), and set
(l_0=l_1=1/2).  Every transition probability is positive, the minimum is
(1/12), and

\[
 I_{\rm K2P}=\frac1{824633720832}\ne0.
\]

**EXACTLY COMPUTED.** For K3P, set every edge triple to
((x_e,y_e,z_e)=(1/3,1/3,1/3)), except
(x_0=1/4) and (x_1=2/5), and set (l_0=l_1=1/2).  Every transition
probability is positive, the minimum is (7/48), and

\[
 I_{\rm K3P}=\frac1{60037854118799648400}\ne0.
\]

These witnesses independently prove that the target pullbacks are
nonzero on the open stochastic domain; no boundary specialization is being
used for the four-port theorem.

## Algebraic separation argument

**PROVED.** A polynomial parameterization has irreducible Zariski closure.
The source invariant vanishes identically on one closure and is nonzero at an
open stochastic point of the other, so the two closures are distinct.

The source and target are obtained from the same directed graph by a leaf
permutation.  Their parameter spaces and coordinate maps are correspondingly
permuted, so their model closures have equal dimension.  Two distinct
irreducible varieties of equal dimension have intersection of strictly lower
dimension.  Therefore a full-dimensional regular stochastic intersection is
impossible.

**EXACTLY COMPUTED.** At the inherited JC common point, nonzero source and
target tangent minors have orders 18 under K2P and 27 under K3P.  Nonzero
combined minors have orders 19 and 29.  These exact minors visibly capture
the character-specific directions in which the two richer-model sheets leave
the JC intersection.  The invariant argument above, rather than tangent
evidence alone, proves the global generic separation.

## Propagation to every chain length

**PROVED.** In `Omega_chain(k)`, marginalize to descendant ports

\[
P_1,\ P_k,\ Q,\ X.
\]

Every suppressed degree-two path has Fourier multiplier

\[
a_{m effective}(h)=\prod_{e\text{ on the path}}a_e(h).
\]

The resulting four-port marginal is exactly `Omega_2`, with some edge
multipliers replaced by these products.  Pulling either separating invariant
back to the (k)-chain gives a polynomial in the original parameters.  If
all unused path multipliers are specialized algebraically to one, that
pullback becomes the already nonzero `Omega_2` pullback.  Hence the all-(k)
pullback is not identically zero.

Because the strict K2P and K3P transition domains are nonempty Euclidean-open
sets, a nonzero real polynomial cannot vanish throughout either domain.
Thus the target chain has an open dense parameter subset on which the
marginal separator is nonzero, whereas it vanishes on the complete source
chain model.  This proves generic separation for every (k\ge2).

## Certificate

**EXACTLY COMPUTED.** Run

```text
PYTHONPATH=src .venv/bin/python src/verify_omega_model_hierarchy.py
```

The verifier checks both full source identities, both target
factorizations, both rational open witnesses, all transition-probability
inequalities, and the six exact tangent minors.  It writes
`certificates/omega_model_hierarchy.json`.

## Remaining scope

**UNRESOLVED.** This milestone does not yet classify `R3`, ordinary triangle
redirection `T`, arbitrary nonroot blobs, or global locality under K2P/K3P.
It proves only that the entire `Omega_chain` family is absent from both richer
move systems.  Together with the inherited `Theta` separation and universal
`C_root` theorem, it gives a strict but still incomplete model hierarchy.

No literature search or numerical assertion enters the theorem.
