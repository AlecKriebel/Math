# Hostile exact-byte audit of the stopped-service rank-two seven

Audit date: 2026-08-12 PDT.

## 1. Exact scope and verdict

This is a proof-first audit of the current bytes of
*rank_two_mixed_profile_7_stopped_service_theorem.md*. The audit fixes one
pair, one arbitrary strongly connected top graph on its displayed support,
one positive rate vector, and one closed irreducible class. Constants may
depend on those fixed data. It does not enumerate orientations or
populations. Finite computation is used only to confirm the identity and
incidence geometry of the seven supports.

The audited bytes are

~~~text
theorem       e8045791f98334d706e058adab0f838f4bf902a71b08bc1b24a4f3493474355b
source        2130fe04800e26911d470bdb20e2703f9c12834ef3c7d4bacd9ab96fc28f1fc5
focused test  bcc7397253e36db766deea3d96be8890dd4aa15932f48523650792e503698f13
selector      d5a5df33b1791c0af533fdba2d947aa178bedec169d4eff99392363c1e09d248
~~~

The emitted finite data are

~~~text
seven-pair fingerprint  93717536ce82eceefe6909c62568afab31e06695dada8b69defb93335d576957
finite-row fingerprint  aefff460ba993878d2961f752463cd2acd87c677fbba43cfc05408523943b98c
payload fingerprint     0c06d14f1ad53c357d0c3ba0127e0c0ce3bac12db8c866523dedd3b5fb401eee
~~~

**STRICT PASS at this exact seven-pair scope.** The current theorem proves
classwise positive recurrence for each of the seven supports, for every fixed
strong top orientation and positive rate vector. Its stopping time is a
physical all-reactions-retained stopping time, its endpoint accounting is
exhaustive, and the generator and stopped parts use the same proper scalar.
No analytic, derivative-order, endpoint, duration, rate, orientation, or
fixed-class counterexample was found.

This verdict does not assert the global T3-2 union. The current source
correctly leaves its global flag false.

## 2. Finite identity, and nothing more

The focused six-test suite passes. It confirms exactly seven positive and
zero signed supports, eight dormant nonservice vertices, rank two of every
top linkage, preservation of total population by the top linkage, presence
of \(AB\), and the stated service-zero source menus. It also confirms

\[
 (306,34)=(7,0)+(299,34).
\]

Those facts identify the analytic cases; they do not prove recurrence.
No finite graph search is used below. The two orientation-sensitive steps
are instead the killed-carrier argument and the directed-cut argument, both
of which follow from strong connectivity itself.

## 3. Pointwise complement of the dormant wedges

Let

\[
 n=A+B+C,\qquad h=1+n,\qquad
 G=1+K_F+\sum_i\log(x_i!),\qquad
 V=G^4+\lambda h^6.
\]

The top linkage preserves \(n\). The lower linkage gives exactly

\[
 {\cal L}h^6
 =\alpha\{(h+1)^6-h^6\}
  +\delta C\{(h-1)^6-h^6\}
 \le K h^5-cCh^5.                                      \tag{3.1}
\]

The three pointwise cases in the target are complete.

* On the failed all-active tier, rank two and homogeneity imply
  \(A,B,C=\Theta(N)\). A top jump has bounded factorial-log increment on
  the flat tier. Thus a top rate \(O(N^2)\) times a fourth-power first
  difference \(O(G^3)\) gives
  \(({\cal L}G^4)^+=O(N^5\log^3N)\). The constant lower birth is smaller,
  while the lower death contribution to \(G^4\) is nonpositive. Equation
  (3.1) supplies \(-\Theta(N^6)\), a full polynomial order of margin.
* On a passing cone, the exact identity is
  \[
   {\cal L}G^4
   =4G^3{\cal L}G+6G^2\sum_r\lambda_r(\Delta_rG)^2
    +4G\sum_r\lambda_r(\Delta_rG)^3
    +\sum_r\lambda_r(\Delta_rG)^4.
  \]
  The corrected-factorial passing estimate is
  \({\cal L}G\le-A_Ng_N\), where \(g_N\to\infty\), whereas
  \(|\Delta_rG|=O(\log n)\). Since \(G\asymp n\log n\), every convexity
  remainder is \(o(G^3A_Ng_N)\). This directly rederives the powered
  estimate used by the target; it is not inherited merely from the
  thirteen-pair audit, whose pair scope is different.
* If \(C\) is bounded and the state is outside the dormant wedges, the
  service-zero menu gives either an enabled pure quadratic source or the
  universal \(AB\) source. Compactness away from the omitted pure vertices
  gives \(A_N\ge ch^2\). Hence the negative powered-factorial term is at
  least \(ch^5\log^3(h)g_N\), which absorbs the \(O(h^5)\) lower-birth
  cost. If \(C\to\infty\), (3.1) is eventually negative and the passing
  factorial term is nonpositive after its remainders are absorbed.

There are no two-active failed descriptors. The feasible one-active failures
are precisely the dormant wedges; infeasible descriptors cannot occur in the
fixed affine class. The bad-sequence argument therefore yields
\({\cal L}V\le-1\) off the wedges and a finite set. No compactness over rate
vectors is needed or claimed.

## 4. Arbitrary-orientation activation

Fix a dormant vertex and relabel it \(X\), with the service species and the
remaining species the two carrier coordinates. Kill every carrier edge whose
target is an inactive quadratic. If a nonempty carrier subset had no killing
edge and no carrier edge leaving it, it would be a closed proper vertex set
in the full top graph. Strong connectivity rules this out. Thus the killed
two-state matrix \(Q\) is transient for every strong orientation, and

\[
 q=(-Q)^{-1}{\bf1}>0,\qquad v={\bf1}-\varepsilon q>0.
\]

For a carrier with positive killing rate, its reward is positive already at
\(\varepsilon=0\). For one with zero killing rate,
\(-\varepsilon Qq=\varepsilon{\bf1}\) supplies the positive reward. After
fixing sufficiently small \(\varepsilon\), the weighted carrier mass \(R\)
satisfies

\[
 {\cal L}_TR\ge cXR-KR^2.                               \tag{4.1}
\]

Inside \(0<R\le\eta n\), one has \(X=n-O(R)\). The physical death costs
only \(O(R)\), and the constant birth is favorable. Bounded jumps and the
quadratic source menu give

\[
 {\cal L}R\ge cnR,\qquad \Gamma R\le CnR.               \tag{4.2}
\]

For fixed small \(\theta>0\), the exponential expansion gives

\[
 {\cal L}e^{-\theta R}\le-c\theta nR e^{-\theta R}.      \tag{4.3}
\]

At \(R=0\), the top and death clocks are disabled and the constant-rate
\(0\to C\) clock supplies one seed. Stop at activation, return to \(R=0\),
or either population-shell exit. Equation (4.3) shows that the conditional
probability of not returning to the dormant base is bounded below by a fixed
positive number. A shell exit is terminal for this trial; on the no-shell
branch, nonreturn is exactly activation. A simultaneous base-return/shell
crossing is assigned to the population-shell endpoint, so it cannot start a
trial outside the localization.

On \(r_0\le R\le\eta n\), Taylor expansion of \(\log R\) and (4.2) give
\({\cal L}\log R\ge cn\). Below \(r_0\), there are finitely many carrier
phases and every enabled carrier race has order \(n\); transience of \(Q\)
excludes a closed nonabsorbing phase. Dynkin on dyadic bands, followed by
the strong Markov property, proves an exponential tail on the physical
\(O(\log n/n)\) time scale. This proves almost-sure termination of each fast
trial rather than assuming it.

The birth count in a stopped trial is not conditionally Poisson. The target
correctly uses

\[
 \mathbb E\exp\{sJ-\alpha(e^s-1)\rho_n\}\le1.            \tag{4.4}
\]

Cauchy--Schwarz with parameter \(2s\), followed by the trial-time exponential
tail, gives a uniform exponential moment for \(J\). Dormant seed waits are
ordinary exponential waits and contribute exactly one seed each. The fixed
positive nonreturn probability makes the number of trials geometric, so the
total activation birth count \(K\) has a uniform exponential moment and the
activation duration has moments of every order. This also covers an arbitrary
initial point of a wedge: the first trial starts without a new seed when
\(R>0\).

An upward population exit needs order-\(N_0\) births and is exponentially
rare. Before a downward exit, the service-death compensator accumulated in
one fast trial is \(O(\eta\log N_0)\). Split the geometric trial count at
\(\varepsilon N_0/\log N_0\). Above the split its probability is
\(e^{-cN_0/\log N_0}\); below it, the duration and death-counting martingales
make order-\(N_0\) deaths exponentially unlikely after \(\varepsilon\) is
chosen. This proves the needed superpolynomial downward-exit bound without
deleting the death clock.

## 5. Integrated service and the physical window

On \(C=0\) with both nonservice coordinates positive, every present
service-free source is enabled. A strongly connected top graph has a cut
edge from that set to a \(C\)-containing complex, so \(\dot C>0\). At a pure
vertex, a present pure quadratic source either creates \(C\) or creates the
other nonservice species, after which the same cut applies. The only points
which can remain in the face are the eight certified dormant vertices.

If a top-fluid orbit from the compact activation shell had finite
\(\int_0^\infty C(t)\,dt\), boundedness of the polynomial vector field and
Barbalat imply \(C(t)\to0\). Its omega-limit would be a connected invariant
subset of the finite dormant set, hence one vertex. The fluid version of
(4.1), \(\dot R\ge cR-KR^2\), excludes approach to that vertex from a
nonvertex orbit. Thus every activation orbit has infinite integrated
service. Continuity in the initial condition and compactness of the
activation shell give a single finite \(T\) with any prescribed uniform
service integral.

Run all clocks for physical time \(T/N_a\). Top rates are \(O(N_a^2)\), so
the density martingale has quadratic variation \(O(N_a^{-1})\); the falling-
factorial correction is \(O(N_a^{-1})\) on the density time scale. The lower
counts are \(O(1)\) and hence perturb density by \(o(1)\). Stopped martingale
estimates and Gronwall give the stated lattice-uniform fluid convergence.

The service deaths have random compensator

\[
 \Lambda_{\rm win}=\delta\int_0^T Z_C(t)\,dt
 \le\delta T+{\delta T\over N_a}B_{\rm win}.             \tag{5.1}
\]

The constant birth clock and the stopped death-counting martingale give
uniform exponential moments for both window counts. Fluid convergence
therefore implies \(\mathbb ED_{\rm win}\ge\delta M-o(1)\), uniformly over
all activation lattice endpoints. Removing service-shell exits costs
exponentially small truncated moments.

With \(\delta M>\sup\mathbb EK+4\), the regular-event calculation uses only

\[
 \mathbb E[K;{\cal R}]\le\mathbb EK,\qquad
 \mathbb E[D_{\rm win};{\cal R}]\ge\delta M-o(1).
\]

It never substitutes the false conditional inequality
\(\mathbb E[K\mid{\cal R}]\le\mathbb EK\). Hence, for
\(\overline\Delta=K+B_{\rm win}-D_{\rm win}\),

\[
 \mathbb E[\overline\Delta;{\cal R}]\le-3,\qquad
 \sup_{N_0}\mathbb Ee^{s|\overline\Delta|}<\infty.       \tag{5.2}
\]

## 6. Exact endpoint and derivative ledger

The physical count identities are

\[
 N_a=N_0+K-D_{\rm pre},\qquad
 N_{\rm end}=N_0+K-D_{\rm pre}+B_{\rm win}-D_{\rm win}. \tag{6.1}
\]

Thus \(N_{\rm end}\le N_0+\overline\Delta\). This does not remove
pre-service deaths from the chain; it uses their sign only after the exact
identity is established. The deterministic envelope

\[
 {\cal P}(m)=\{1+K_F+\log(m!)\}^4+\lambda(1+m)^6
\]

retains every top redistribution because
\(\sum_i\log(y_i!)\le\log(m!)\).

The load-bearing derivative orders are:

| term | audited order |
|---|---:|
| all-active positive top \(G^4\) drift | \(N^5\log^3N\) |
| all-active negative service \(h^6\) drift | \(-N^6\) |
| regular sixth-power first difference | \(6N_0^5\mathbb E[\overline\Delta;{\cal R}]\) |
| regular sixth-power Taylor remainder | \(O(N_0^4)\) |
| positive change of the factorial fourth power | \(O(N_0^3\log^4N_0)\) |
| initial multinomial reconcentration gap | \(O(N_0^4\log^3N_0)\) |

The exponential moment in (5.2) justifies the event-weighted Taylor
expansion. Its first term is negative of order \(N_0^5\), while every
displayed positive cost is strictly smaller. There is no missing factor of
\(N_0\), \(C\), \(G\), or \(\lambda\); fixed \(\lambda>0\) is absorbed into
the negative constant.

The localization alternatives also have the right sign or tail. An
activation-stage downward first crossing has population at most
\(N_0/2+1\) and hence an order-\(N_0^6\) scalar decrease. Its upward first
crossing has population at most \(2N_0+1\), and its polynomial endpoint cost
is absorbed by the exponential birth tail. In the service window, on
\(K\le N_0/4\), a downward crossing of \(N_a/2\) remains a strict fractional
decrease from \(N_0\), while an upward crossing of \(2N_a\) needs order-
\(N_0\) births. The event \(K>N_0/4\) is absorbed by the exponential moment
of \(K\). Duration contributions are lower order on downward branches and
exponentially weighted on upward branches. Giving population localization
priority at simultaneous crossings makes these branches disjoint and
exhaustive.

Consequently the exact episode satisfies

\[
 \mathbb E_x\{V(X_\tau)-V(x)+\tau\}\le-1
\]

outside a finite wedge sublevel. The geometric trial bound proves that
activation or a shell endpoint occurs almost surely, and the service window
then has a finite deterministic horizon. Thus \(\tau<\infty\) almost surely
for the exact stopping rule.

## 7. Common-scalar gluing and fixed classes

The pointwise complement and stopped wedges use the identical globally
proper \(V\). The sole population-increasing reaction has constant rate
\(\alpha\), so total population is bounded above pathwise by its initial
value plus a rate-\(\alpha\) Poisson process. On each finite population shell
the state space and all rates are finite. Hence the chain is nonexplosive and
the localization limits used above are legitimate.

Restrict to a fixed closed irreducible class \(\Gamma\). Enlarge the finite
exceptional set, if needed, by one reference state of \(\Gamma\); this
ensures a nonempty finite target without changing either drift hypothesis.
The common-entropy physical-time gluing theorem at exact bytes

~~~text
7550c81b6a2a3085a34deaa9654517b7b00bb46bbd9e76898ee2220f6d53d194
~~~

gives finite mean hitting of that target. Local finiteness and irreducibility
then give a finite mean return time, so \(\Gamma\) is positive recurrent.

This closes the target's actual theorem contract. It does not require a
rate-uniform Foster constant, a deleted-reaction comparison, stationarity of
the top chain, or an unweighted terminal population moment beyond the
positive-overshoot and polynomial envelope estimates explicitly proved.

## 8. The real derivative/provenance mismatch

The pre-existing file
*rank_two_mixed_profile_7_stopped_service_independent_audit.md* cannot certify
the current target. It pins

~~~text
old theorem       9f8622ae324ac1ea099a75dca834bbacafadd353e311cb8d20bf35d299ca00a1
old source        bee3003a034763efb2958ab1410a59d6bde258c1e5590925d9acdbf6baac1366
old focused test  929b54c732d6f988546192d4307bf63c150b0760d809b5e86357104baeb0e38c
old payload       15920ec2ab510bab87b4e4b778cd998f7bbf7622b606bda383014dd5d6add2e3
~~~

and explicitly describes a claim-neutral snapshot with false promoted
flags. The current source and payload instead set the five seven-pair local
audit, analytic, and recurrence flags true. The unchanged finite-row
fingerprint shows that the support geometry did not change, but it does not
bridge this status and exact-byte difference. This is a genuine derivative
mismatch in the prior attestation, not an analytic defect in the current
theorem.

The present audit supersedes that old attestation only for the current files
and payload pinned in Section 1. It finds no calculus or scaling derivative
mismatch in the current proof.

## 9. Replay and publication check

The only executable replay used for this verdict was

~~~text
PYTHONPATH=src python3 -B -m unittest \
  tests.test_rank_two_mixed_profile_7_stopped_service -v
~~~

It passed all six focused tests. This audit deliberately performed no
orientation or population enumeration.
