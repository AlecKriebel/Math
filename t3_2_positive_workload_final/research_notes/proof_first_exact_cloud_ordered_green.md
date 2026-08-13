# Ordered Green proof for exact-cloud killing and dirty cleanup

**Proof-first scoped lemma, 2026-08-11 PDT.**  This note repairs the units
mismatch in the rejected draft
*proof_first_exact_cloud_repair_lemmas.md*.  Direct reactions at the
no-fast base and hazards accumulated during an opened proper excursion are
kept separate.  The sourcewise first-kill error is proved by a reversible
ordered-Green identity.  Dirty cleanup is proved by a new shifted-carrier
potential; it is not identified with the original excursion.

This note is claim-neutral.  It changes no certification flag.

## 1. Carrier, local time, and exact effective hazards

Fix

\[
 \{aU,V+I\},\qquad a\in\{0,1,2\},
 \qquad 0\le u<L_n,\quad v\ge n/2,
\]

where \(L_n=n^{1/3+o(1)}\) and \(L_n^2/n=o(1)\).  During a proper
excursion the cofactor level \(Y\) has rates

\[
 \lambda_i=\alpha(u-ai)_{\underline a},
 \qquad \mu_i=\beta(v+i)i.                                      \tag{1.1}
\]

Let \(\tau_0\) be the first hit of zero after an opening, and let
\({\cal G}(i,j)=\mathbb E_i\int_0^{\tau_0}{\bf1}_{\{Y_t=j\}}dt\)
be the killed Green kernel on the positive levels.  Its reversible weights
are

\[
 {\pi_i\over\pi_0}
 =\rho^i{(u)_{\underline{ai}}\over
            i!(v+1)^{\overline i}},qquad \rho=\alpha/\beta.     \tag{1.2}
\]

Write \(\lambda_0=\alpha(u)_{\underline a}\).  Flow through the killed
edge \(1\to0\), followed by reversibility, gives the exact occupation
identity

\[
 g_i:=\mathbb E_1\int_0^{\tau_0}{\bf1}_{\{Y_t=i\}}dt
 ={\pi_i\over\pi_0\lambda_0},qquad i\ge1,                      \tag{1.3}
\]

whenever \(\lambda_0>0\).  If \(\lambda_0=0\), no opened excursion
exists and every formula below has zero excursion part.

For a lower edge \(e\), let

\[
 k_e(i)=\kappa_e(u-ai)_{\underline{c_e}}
                    (i)_{\underline{b_e}},qquad c_e+b_e\le2,   \tag{1.4}
\]

and put \(K=\sum_fk_f\).  The direct base clock is

\[
 d_e=k_e(0)=\kappa_e(u)_{\underline{c_e}}
                  {\bf1}_{\{b_e=0\}}.                           \tag{1.5}
\]

Define \(J_e=\int_0^{\tau_0}k_e(Y_t)dt\) and
\(J=\int_0^{\tau_0}K(Y_t)dt\), with the excursion started at level one.
Per unit physical time spent at level zero, the un-killed effective rate is

\[
 A_e=d_e+\lambda_0\mathbb E_1J_e
     =\sum_{i\ge0}{\pi_i\over\pi_0}k_e(i).                       \tag{1.6}
\]

The exact first-lower rate is

\[
 \widehat A_e=d_e+\lambda_0\mathbb E_1
 \int_0^{\tau_0}k_e(Y_t)
       \exp\!\left\{-\int_0^tK(Y_s)ds\right\}dt.                \tag{1.7}
\]

Thus direct base clocks cancel from the killing error:

\[
 0\le A_e-\widehat A_e
 \le\lambda_0\mathbb E_1[J_eJ].                                \tag{1.8}
\]

## 2. A pointwise downward-carrier potential

For a carrier with invariant spectator total \(s=U+aI\), active base
\(w\ge n/3\), and lower hazard \(K_s(i)\), binary molecularity gives

\[
                         K_s(i)\le C\{(1+s)^2+i^2\}.             \tag{2.1}
\]

Let \({\cal L}_{s,w}\) be its proper birth--death generator, killed at
zero.  Put

\[
 \Phi_s(i)={C_0\over n}
   \left\{(1+s)^2\sum_{r=1}^i{1\over r}+i^2\right\},
 \qquad \Phi_s(0)=0.                                            \tag{2.2}
\]

### Lemma 2.1 (shifted cleanup potential)

For \(C_0\) sufficiently large and all large \(n\),

\[
                 {\cal L}_{s,w}\Phi_s(i)\le-K_s(i),qquad i\ge1. \tag{2.3}
\]

Consequently

\[
 R_{s,w}K_s(i):=\mathbb E_i\int_0^{\tau_0}K_s(Y_t)dt
 \le {C\over n}\{(1+s)^2\log(i+1)+i^2\}.                       \tag{2.4}
\]

For every fixed \(p\), if a lower firing is stopped and charged with any
degree-\(p\) polynomial endpoint reward, the analogous potential satisfies

\[
 R_{s,w}K_{s,p}(i)
 \le {C_p\over n}(1+s+i)^{p+2}\{1+\log(i+1)\},                  \tag{2.5}
\]

where, for a fixed polynomial endpoint reward \(R_p\),

\[
 K_{s,p}(i)=\sum_f k_f(i)R_p(\operatorname{post}_f(i)),
 \qquad R_p(\operatorname{post}_f(i))\le C_p(1+s+i)^p,          \tag{2.5a}
\]

and the boundary-causing reaction is included in
\(\operatorname{post}_f(i)\).

#### Proof

The downward differences of (2.2) are

\[
 \Phi_s(i)-\Phi_s(i-1)
 ={C_0\over n}\{(1+s)^2/i+2i-1\}.                              \tag{2.6}
\]

Since \(\mu_i\ge cni\), the death contribution to
\({\cal L}_{s,w}\Phi_s\) is at most

\[
 -cC_0\{(1+s)^2+i^2\}.                                        \tag{2.7}
\]

The birth rate is at most \(C(1+s)^a\), and its positive contribution is
at most

\[
 {C C_0(1+s)^a\over n}
 \{(1+s)^2/(i+1)+2i+1\}.                                       \tag{2.8}
\]

Below the cutoff, \((1+s)^a/n=o(1)\).  Equations (2.1), (2.7), and
(2.8), with \(C_0\) enlarged, prove (2.3).  Stopped Dynkin gives (2.4).
For (2.5), put \(P=1+s\) and define the downward increments

\[
 D_p(i)={C_p\over ni}(P+i)^{p+2},\qquad
 \Phi_{s,p}(i)=\sum_{r=1}^iD_p(r).                              \tag{2.9}
\]

Then \(\mu_iD_p(i)\ge cC_p(P+i)^{p+2}\), while the birth contribution
is at most

\[
 {C C_pP^a\over n}\,{(P+i+1)^{p+2}\over i+1}.                  \tag{2.10}
\]

Its ratio to the death term is \(O(P^a/n)=o(1)\).  Thus
\(-{\cal L}_{s,w}\Phi_{s,p}\ge K_{s,p}\) after increasing \(C_p\),
and

\[
 \Phi_{s,p}(i)
 \le {C_p\over n}(P+i)^{p+2}\{1+\log(i+1)\}.                  \tag{2.11}
\]

Stopped Dynkin proves (2.5). \(\square\)

## 3. Ordered reversible two-insertion identity

### Lemma 3.1 (sourcewise first-kill error)

For every feasible distinguished edge \(e\),

\[
 \mathbb E_1[J_eJ]
 \le {C(1+u)^2\over n}\mathbb E_1J_e.                           \tag{3.1}
\]

Hence

\[
 0\le A_e-\widehat A_e
 \le {C(1+u)^2\over n}A_e.                                     \tag{3.2}
\]

#### Proof

Split the double integral in \(J_eJ\) at the ordering of its two times.
The future-ordered part equals

\[
 F_e=\sum_{i\ge1}g_i k_e(i)\,R_{u,v}K(i).                       \tag{3.3}
\]

The past-ordered part is the same.  Indeed, the killed Green kernel is
reversible, \(\pi_i{\cal G}(i,j)=\pi_j{\cal G}(j,i)\), while
\(g_i=(\pi_i)/(\pi_0\lambda_0)\); interchanging \(i,j\) turns one
ordered double sum into the other.  Therefore

\[
                         \mathbb E_1[J_eJ]=2F_e.                 \tag{3.4}
\]

If \(\mathbb E_1J_e=0\), the excursion error is identically zero and there
is nothing to prove.  Otherwise normalize the weights \(g_i k_e(i)\) to a
probability \(\nu_e\).  If
\(i=b_e+j\), cancellation of falling factorials gives

\[
 \nu_e(j)\ \propto\
 {\rho^j(u-w_a(e))_{\underline{aj}}
  \over j!(v+b_e+1)^{\overline j}}.                             \tag{3.5}
\]

Its consecutive ratio is at most

\[
                   {C(1+u)^a\over n(j+1)}.                      \tag{3.6}
\]

Thus \(j\) is dominated in every increasing fixed moment by a Poisson
variable of mean \(C(1+u)^a/n=o(1)\).  Since \(b_e\le2\),

\[
 \mathbb E_{\nu_e}\{\log(i+1)+i^2\}\le C.                     \tag{3.7}
\]

Equations (2.4), (3.3), and (3.7) imply

\[
 F_e\le {C(1+u)^2\over n}\sum_i g_i k_e(i)
       ={C(1+u)^2\over n}\mathbb E_1J_e,                       \tag{3.8}
\]

and (3.1) follows after absorbing the factor two.  Finally, (1.8) and
\(\lambda_0\mathbb E_1J_e\le A_e\) give (3.2). \(\square\)

## 4. Dirty cleanup at the shifted invariant

Suppose the first lower edge has source \(y=c_yU+b_yI\), target
\(z=c_zU+b_zI\), and fires at pre-level \(i=b_y+j\).  Immediately after
that firing the proper cleanup carrier has

\[
 s=u-w_a(y)+w_a(z),\qquad
 w'=v+b_y-b_z,qquad I'=j+b_z.                                  \tag{4.1}
\]

These are the correct shifted parameters: the cleanup is not the original
carrier restarted at base \(u\).  All shifts are bounded and
\(s\le u+4\), \(w'\ge n/3\) for large \(n\).

Conditional on the identity of the first edge, its firing mechanism is a
mixture of two disjoint branches.  On the **direct base branch** one has
\(b_y=0\) and pre-level \(i=0\).  If \(b_z=0\), cleanup has already ended.
If \(b_z>0\), start the shifted carrier deterministically at
\(I'=b_z\), with the parameters in (4.1), and apply (2.4)--(2.5) directly.

On the **opened branch**, the un-killed edge-size-biased level has exactly
the weights (3.5); by (3.2), its true first-edge law is dominated by this
law up to a factor \(1+o(1)\).  Applying (2.4) at the shifted parameters
and averaging over \(j\), then combining the two branches, gives

\[
 \mathbb P\{\hbox{a second lower firing before cleanup}\mid e\}
 \le {C(1+u)^2\over n}.                                         \tag{4.2}
\]

Using (2.5) instead proves, for every fixed \(p\),

\[
 \mathbb E[(1+U_E+I_E+|V_E-v|)^p;
       \hbox{second lower firing}\mid e]
 \le {C_p(1+u)^{p+3}\over n}.                                  \tag{4.3}
\]

The second firing is included in the endpoint in (4.3).  No subsequent
cleanup or fictitious return is assumed.

## 5. Consequence and audit boundary

Equations (3.2) and (4.3) are the two uniform estimates missing from the
cloud-averaging draft.  Integrated against its killed polynomial Green
operator they give an endpoint-weighted defect cost
\(C_p(1+u)^{c_p}/n\), hence \(n^{-1+o(1)}\) from a subpower start.

This note does not itself prove the equality-trace Green bound, duration,
entropy, fourth-power Taylor estimate, or global marked gluing.  Those
remain separate audit obligations.  No certification flag changes.
