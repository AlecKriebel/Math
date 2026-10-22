# Approach 5: global certificates on selected mixed pencils

**Result:** four explicit binary families satisfy the desired dimension-12 cubic inequality for all real parameters. The universal inequality remains unproved.

Put \(V=V_{6,6}\), first block \(e_1,\ldots,e_6\), second block \(e_7,\ldots,e_{12}\). Let \(H\) be the four-dimensional tensor of Approach 3, embedded by each of the following ordered coordinate lists:

\[
(1,2,3,4),\quad(1,7,8,9),\quad(1,2,7,8),\quad(1,7,2,8).
\]

These define four specific two-dimensional linear spans. No arbitrary four-plane embedding, angle, rotation, or simultaneous multiple perturbation is silently included.

We have \(T=\|V\|^2=396/5\), \(Q(V)=11V\), \(\|H\|^2=24\), and \(Q(H)=6H\). Direct coordinate contraction gives \(\ell=\langle V,H\rangle\) equal to \(0,0,44/5,-22/5\), respectively. Symmetry of the trilinear form proves

\[
\|V+tH\|^2=T+2\ell t+24t^2,
\]
\[
\langle Q(V+tH),V+tH\rangle
=11T+33\ell t+18\ell t^2+144t^3.
\]

Therefore the proposed cubic bound on this pencil is equivalent to nonnegativity of

\[
P_\ell(t)=\frac{55}{36}(T+2\ell t+24t^2)^3
-(11T+33\ell t+18\ell t^2+144t^3)^2.
\]

Exact expansion gives

\[
P_0(t)=\frac{96t^2}{5}(20t^4+10890t^2-13068t+35937),
\]
\[
P_{44/5}(t)=\frac{16t^2}{225}
(5400t^4+11880t^3+1890504t^2-392524t+6217101),
\]
\[
P_{-22/5}(t)=\frac{4t^2}{225}
(21600t^4-23760t^3+14239764t^2-24090616t+46969659).
\]

Every quartic in parentheses is strictly positive on the real line. This has an elementary rational certificate: for a quartic \(q(t)=At^4+Bt^3+Ct^2+Dt+E\), subtract
\(A(t^2+B t/(2A))^2\). The remainder is a quadratic with positive leading coefficient and negative discriminant in all three cases. The exact discriminants are recomputed in `results.json`. For the first quartic one may also write

\[
20t^4+10890(t-3/5)^2+160083/5.
\]

Thus \(P_\ell(t)\ge0\), with equality only at \(t=0\). Scaling covers every point \(xV+yH\) with \(x\ne0\), and the case \(x=0\) follows from \(3/2<55/36\). This proves the full target absolute cubic estimate on these four spans.

## Precisely what is left

The finite-dimensional maximization is over all unit Weyl operators. At a global maximizer \(W\), symmetry of the trilinear form gives
\(Q(W)=\beta_n W\) after \(\|W\|=1\). Candidate eigenoperators and their pencils do not classify all such critical points or all competing global maxima.

By Approaches 1–3, the proposed threshold is equivalent, under the stated parity interpretation, to proving for **every** dimension \(n\ge12\)

\[
\beta_n^2\le\frac{2(n-1)(n-2)}{n^2}\quad(n\text{ even}),\qquad
\beta_n^2<\frac{2(n-1)(n-2)}{n^2}\quad(n\text{ odd}).
\]

For even dimensions the reverse inequality already holds, so the required bound is sharp. For odd dimensions, Approach 2 gives a strict lower-endpoint margin, and the strict cubic bound is exactly what supplies the strict upper-endpoint margin. The widths necessarily tend to zero by (6) and (8).

Neither the critical-point condition, the complete diagonal local calculation, the explicit low-dimensional obstruction, nor the pencil certificates establish these global inequalities. Xu's inspected near-round theorem does not supply them either. A counterexample would be any Weyl operator exceeding the displayed bound (or attaining it in a relevant odd dimension); none is constructed here. The five-route investigation stops with these honest partial results, not with a claim that numerical or symbolic sampling proves \(n_0=12\).
