# Approach 2: recover the different through a Kummer tower

The direct upper-break deduction loses information. We therefore analyze the relative-field method underlying the Caruso–Liu proof and Caruso's later principal-ideal modification.

Choose a uniformizer \(\pi\) of \(K\), put \(K_j=K(\pi^{1/p^j})\), and let \(L_j=LK_j\). Here \(K_j/K\) need not be Galois; \(L_j/K_j\) is Galois. All valuations in this note are extensions of \(v_K\).

## A rigorous sufficient relative estimate

The polynomial \(X^{p^j}-\pi\) is Eisenstein, and its root generates \(\mathcal O_{K_j}\) over \(\mathcal O_K\). Its derivative gives

\[
v_K(\mathcal D_{K_j/K})=ej+1-p^{-j}.
\tag{1}
\]

Transitivity of differents gives

\[
v_K(\mathcal D_{L_j/K})=ej+1-p^{-j}
+v_K(\mathcal D_{L_j/K_j}).
\tag{2}
\]

Because \(L\subseteq L_j\), another application of transitivity, with the nonnegative relative different, gives

\[
v_K(\mathcal D_{L/K})\leq v_K(\mathcal D_{L_j/K}).
\tag{3}
\]

Set \(j=s=n+a\). The following implication is therefore completely proved:

\[
\boxed{v_K(\mathcal D_{L_s/K_s})<eb}
\quad\Longrightarrow\quad
v_K(\mathcal D_{L/K})<B.
\tag{4}
\]

More generally the right side follows if \(L_s/K_s\) has Fontaine's property \((P_{eb})\), with the threshold measured in \(v_K\). The precise property is: for every algebraic \(E/K_s\), any \(\mathcal O_{K_s}\)-algebra map

\[
\mathcal O_{L_s}\longrightarrow
\mathcal O_E/\{x:v_K(x)>eb\}
\]

forces a \(K_s\)-embedding of \(L_s\) into \(E\). The consequence for the different is Caruso–Liu Corollary 4.2.2. In the usual \(K_s\)-normalized valuation its threshold is \(p^s eb=er p^n/(p-1)\); the factor \(p^s\) cannot be omitted.

## How the known proof suggests the desired improvement

Caruso–Liu use a monomial \(u^N\) killing the height quotient \(W_n(k)[u]/E(u)^r\). Their relative-field proof yields

\[
v_K(\mathcal D_{L_j/K_j})<\frac{Np^n}{(p-1)p^j}
\]

under its stated strict level condition

\[
j>n+\log_p\frac{N}{e(p-1)}.
\tag{5}
\]

Choosing \(N=ern\) produces the old bound. Choosing \(N=er\), if justified, would produce (4). Approach 3 identifies exactly why that substitution is not generally legitimate in this older method.

Caruso's later proof of Theorem 3.28 instead replaces the two monomial-cutoff Witt quotients with quotients by \(E(u)^r\mathfrak t^r W_n(\mathfrak m_R)\) and \(\mathfrak t^r W_n(\mathfrak m_R)\), using the period \(\mathfrak t\) and the integral \((\varphi,\tau)\)-module structure. Its stated Galois-control condition is

\[
j>n-1+\log_p r.
\tag{6}
\]

Our choice \(j=s\) satisfies (6) strictly because

\[
r\leq(p-1)p^a<p^{a+1}.
\]

This makes the principal-ideal argument a natural candidate for proving the desired relative estimate. However, the displayed conclusion of Theorem 3.28 is the upper-break bound. Its short proof refers back to the earlier method rather than separately stating the relative \((P_m)\) assertion.

The unproved step in this packet is a mixed-characteristic specialization-and-lifting statement at the exact precision \(eb\): the principal Witt ideals must descend to the finite \(K_s\)-level in a way that gives a compatible, injective, Frobenius-equivariant lifting argument over **every** algebraic \(E/K_s\), and not only over the tilt or algebraic closure. The equal-characteristic containment in Caruso Lemma 2.13 is not, by itself, that statement. The source's period \(\mathfrak t\) is not a freely replaceable Teichmüller monomial.

This is not an assertion that Caruso's sketch is wrong or that the missing assertion is unknown in the literature. It is the precise part not fully reconstructed and established here. We therefore do not report (4)'s antecedent as proved in general.

## Endpoint and optimization checks

For the hypothetical relative estimate

\[
v_K(\mathcal D_{L_j/K_j})<
\frac{er p^n}{(p-1)p^j},
\]

the resulting total bound is

\[
F(j)=1+ej+\frac{er p^n/(p-1)-1}{p^j}.
\]

Direct subtraction gives

\[
F(j+1)-F(j)
=e-er p^{n-j-1}+(p-1)p^{-j-1}.
\tag{7}
\]

At \(j=s-1\), this becomes

\[
F(s)-F(s-1)=e(1-r/p^a)+(p-1)p^{-s}.
\tag{8}
\]

It is positive throughout the exceptional band \(r\leq p^a\). Thus a valid lower-level estimate would even improve the target. But its required relative precision there is \(epb\), which is larger than \(e=v_K(p)\) because \(b>1/p\). One cannot infer it from a quotient that only retains information modulo \(p\). For \(r<p^a\), level \(s-1\) meets (6) but fails (5) with \(N=er\); this distinguishes Galois equivariance from the finite-level precision needed for that proof.

At \(b=1\), level \(s\) gives equality rather than strictness in (5). We do not silently replace \(>\) by \(\geq\). That endpoint is already covered by Approach 1, since \(r=(p-1)p^a\geq p^a+1\).

**Outcome:** a precise conditional reduction, exact tower calculation, and explicit specialization/precision gap. No complete relative estimate and no complete proof is claimed from this approach.
