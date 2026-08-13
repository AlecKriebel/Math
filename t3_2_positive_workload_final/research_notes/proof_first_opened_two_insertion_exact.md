# Exact sourcewise two-insertion bound for an opened proper cloud

**Proof-only repair atom, 2026-08-11 PDT.**  This note proves only the
unchanged-carrier estimate needed to compare an un-killed proper-cloud
occupation with the first lower reaction.  Direct level-zero clocks are
kept separate from opened-excursion occupation.  Cleanup after a lower
reaction is not treated here.  No orientation enumeration is used and no
certification flag is changed.

## 1. Carrier, base clocks, and units

Fix an exact proper pair

\[
                         aU\rightleftarrows V+I,
             \qquad a\in\{0,1,2\},                               \tag{1.1}
\]

with forward and reverse rates \(\alpha,\beta>0\).  Start from the
no-fast base \((u,v,0)\), assume \(u\ge a\), and put

\[
 x=1+u,qquad v\ge n/2,qquad
 0\le u<L_n={n^{1/3}\over\log(n+e)}.                             \tag{1.2}
\]

The proper opening clock at level zero is

\[
                         \lambda_0=\alpha(u)_{\underline a}>0.    \tag{1.3}
\]

After an opening, let \(Y\) be the proper birth--death chain begun at
\(Y_0=1\) and killed at
\(\tau_0=\inf\{t:Y_t=0\}\).  At level \(i\),

\[
 U=u-ai,qquad V=v+i,qquad
 \lambda_i=\alpha(u-ai)_{\underline a},qquad
 \mu_i=\beta(v+i)i.                                              \tag{1.4}
\]

For \(a=1,2\) its state space is finite; for \(a=0\) it is
\(\mathbb N_0\) and \(\tau_0<\infty\) almost surely.

Let \({\cal E}\) be a fixed finite collection of lower edges with binary
sources.  If edge \(e\) has source \(c_eU+b_eI\), write

\[
 k_e(i)=\kappa_e(u-ai)_{\underline{c_e}}(i)_{\underline{b_e}},
 \qquad K(i)=\sum_{f\in{\cal E}}k_f(i),                           \tag{1.5}
\]

and, on an opened excursion,

\[
 J_e=\int_0^{\tau_0}k_e(Y_t)dt,qquad
 J=\int_0^{\tau_0}K(Y_t)dt.                                     \tag{1.6}
\]

The direct level-zero clock is

\[
 d_e=k_e(0)=\kappa_e(u)_{\underline{c_e}}\mathbf1_{\{b_e=0\}}.   \tag{1.7}
\]

Thus the un-killed effective hazard per unit physical time spent at the
base is

\[
                  A_e=d_e+\lambda_0\mathbb E_1J_e,               \tag{1.8}
\]

not \(\mathbb E_1J_e\) alone.

## 2. Excursion occupation and reversibility

Let \(G(i,j)\) be the expected time spent at \(j\) before \(\tau_0\) when
the proper carrier starts at \(i\ge1\), and put

\[
                         g_j=G(1,j).                              \tag{2.1}
\]

Define the reversible weights by \(\pi_0=1\) and

\[
 {\pi_i\over\pi_0}
 =\rho^i{(u)_{\underline{ai}}
        \over i!(v+1)^{\overline i}},qquad \rho={\alpha\over\beta}. \tag{2.2}
\]

### Lemma 2.1 (exact excursion measure)

For every \(j\ge1\),

\[
                         g_j={\pi_j\over\lambda_0\pi_0}.          \tag{2.3}
\]

Moreover the killed Green kernel is reversible with respect to \(g\):

\[
                         g_iG(i,j)=g_jG(j,i).                     \tag{2.4}
\]

#### Proof

The expected occupation vector \(g\) has one unit of net downward flux
through the edge \(1\to0\).  Hence

\[
 \mu_1g_1=1,qquad
 \mu_{j+1}g_{j+1}=\lambda_jg_j\quad(j\ge1).                      \tag{2.5}
\]

The first identity gives \(g_1=1/\mu_1\); iteration of the second gives
\(g_j=\pi_j/(\lambda_0\pi_0)\), since
\(\pi_1/\pi_0=\lambda_0/\mu_1\).  The killed generator on
\(\{1,2,\ldots\}\) is self-adjoint in \(\ell^2(\pi)\), so its Green
kernel satisfies \(\pi_iG(i,j)=\pi_jG(j,i)\).  Equation (2.4) follows
from (2.3).  For \(a=0\), apply the same argument on a finite truncation
and pass monotonically to the limit. \(\square\)

Combining (1.8) and (2.3) gives

\[
 A_e=\sum_{i\ge0}{\pi_i\over\pi_0}k_e(i),                        \tag{2.6}
\]

and therefore the exact product

\[
 A_e={\kappa_e\rho^{b_e}(u)_{\underline{ab_e+c_e}}
          \over(v+1)^{\overline{b_e}}}
 \sum_{j\ge0}{\rho^j
       (u-ab_e-c_e)_{\underline{aj}}
       \over j!(v+b_e+1)^{\overline j}}.                         \tag{2.7}
\]

Thus (2.7) and the opened quantity \(\mathbb E_1J_e\) have consistent but
different units.

## 3. A pointwise total-hazard potential

Let

\[
                         h(i)=\mathbb E_iJ=(GK)(i).               \tag{3.1}
\]

### Lemma 3.1 (proper-cloud Green majorant)

There is a constant \(C\), independent of \(n,u,v,i\), such that

\[
 h(i)\le\Phi(i):={C\over n}
       \{x^2H_i+xi+i^2\},qquad
 H_i=\sum_{r=1}^i{1\over r}.                                    \tag{3.2}
\]

#### Proof

Binary molecularity and (1.5) give

\[
                         K(i)\le C_K(x+i)^2.                      \tag{3.3}
\]

Put

\[
 D_i=\Phi(i)-\Phi(i-1)
 ={C\over n}\left\{{x^2\over i}+x+2i-1\right\}.                \tag{3.4}
\]

For the proper generator \({\cal L}\),

\[
 -{\cal L}\Phi(i)=\mu_iD_i-\lambda_iD_{i+1}.                    \tag{3.5}
\]

Since \(\mu_i\ge cni\),

\[
 \mu_iD_i\ge cC\{x^2+xi+i^2\}.                                \tag{3.6}
\]

Also \(\lambda_i\le C_0x^2\), and

\[
 D_{i+1}\le {C\over n}\left\{{x^2\over i+1}+x+2i+1\right\}
 \le {C'\over n}\{x^2+xi+i^2\}.                               \tag{3.7}
\]

Because \(x^2/n\le (1+L_n)^2/n=o(1)\), the second term in (3.5) is at
most half the first for all sufficiently large \(n\).  Enlarging the
constant in \(\Phi\) then gives

\[
                         -{\cal L}\Phi(i)\ge K(i).               \tag{3.8}
\]

Dynkin's formula, stopped at \(0\) and at a finite upper truncation, gives
\(\mathbb E_i\int K(Y_t)dt\le\Phi(i)\).  Monotone convergence removes
the upper truncation in the \(a=0\) case. \(\square\)

## 4. Size-biased carrier levels

For a fixed edge with nonzero opened occupation, put

\[
                         q_i=g_i k_e(i),\qquad i\ge1.             \tag{4.1}
\]

### Lemma 4.1 (uniform size-biased moments)

For every fixed \(r\),

\[
                \sum_{i\ge1}q_i i^r\le C_r\sum_{i\ge1}q_i.      \tag{4.2}
\]

#### Proof

For \(i\ge b_e\) at which both terms are nonzero, detailed balance and
the falling-factorial ratios give

\[
 {q_{i+1}\over q_i}
 ={\lambda_i\over\mu_{i+1}}
   {(u-a(i+1))_{\underline{c_e}}\over
      (u-ai)_{\underline{c_e}}}
   {(i+1)_{\underline{b_e}}\over i_{\underline{b_e}}}
 \le {Cx^a\over n(i+1-b_e)}.                                   \tag{4.3}
\]

The \(U\)-ratio is at most one.  Since \(b_e\le2\) and
\(x^a/n=o(1)\), the tail after its first nonzero term is dominated by a
factorial distribution with uniformly bounded parameter.  If \(b_e=0\),
the opened occupation starts at \(i=1\), and the same argument is applied
from that first term.  This proves (4.2). \(\square\)

## 5. The exact two-insertion inequality

### Theorem 5.1

For every lower edge with nonzero opened occupation,

\[
 \boxed{\quad
 \mathbb E_1[J_eJ]
       \le {C(1+u)^2\over n}\,\mathbb E_1J_e .\quad}             \tag{5.1}
\]

The same result, with a larger constant and polynomial power of \(1+u\),
holds after multiplying the distinguished insertion level by any fixed
polynomial reward.

#### Proof

Split the two time variables in \(J_eJ\) by their order.  The part in which
the distinguished \(e\)-insertion occurs first is

\[
 \sum_{i\ge1}g_i k_e(i)h(i).                                    \tag{5.2}
\]

The reverse ordering equals the same quantity.  Indeed, its double Green
sum is

\[
 \sum_{i,j\ge1}g_iK(i)G(i,j)k_e(j),                              \tag{5.3}
\]

and (2.4), followed by interchange of \(i,j\), turns (5.3) into (5.2).
Therefore

\[
             \mathbb E_1[J_eJ]
        =2\sum_{i\ge1}q_i h(i).                                 \tag{5.4}
\]

By Lemmas 3.1 and 4.1, using \(H_i\le i\),

\[
 \sum_iq_i h(i)
 \le {C\over n}\sum_iq_i\{x^2H_i+xi+i^2\}
 \le {Cx^2\over n}\sum_iq_i
 ={Cx^2\over n}\mathbb E_1J_e.                                 \tag{5.5}
\]

This proves (5.1).  A fixed polynomial mark changes only the moment order
in Lemma 4.1. \(\square\)

## 6. First-lower Feynman--Kac consequence

Let

\[
 p_e=\mathbb E_1\int_0^{\tau_0}k_e(Y_t)
       \exp\!\left\{-\int_0^tK(Y_s)ds\right\}dt                  \tag{6.1}
\]

and define the exact first-lower effective hazard

\[
                         \widehat A_e=d_e+\lambda_0p_e.           \tag{6.2}
\]

Then the direct clock cancels exactly, and Theorem 5.1 gives

\[
 \begin{aligned}
 0\le A_e-\widehat A_e
 &=\lambda_0\mathbb E_1\int_0^{\tau_0}k_e(Y_t)
       \left[1-e^{-\int_0^tK(Y_s)ds}\right]dt\\
 &\le\lambda_0\mathbb E_1[J_eJ]\\
 &\le {Cx^2\over n}\lambda_0\mathbb E_1J_e
 \le {Cx^2\over n}A_e.                                         \tag{6.3}
 \end{aligned}
\]

Thus, uniformly below the cutoff,

\[
              \widehat A_e=A_e
                 \left[1+O\!\left({(1+u)^2\over n}\right)\right] \tag{6.4}
\]

source by source, including edges with direct \(b_e=0\) base clocks.  This
is the rigorous unchanged-carrier relative first-kill estimate.  It makes
no assertion about the shifted cleanup carrier.
