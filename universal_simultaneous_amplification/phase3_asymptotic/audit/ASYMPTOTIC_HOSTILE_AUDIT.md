# Hostile audit of phase3_asymptotic/REPORT.md

Date: 2026-08-01 (America/Los_Angeles)

No literature search or external contact was used. This audit was derived
from the update rule and the finite-state chains. Labels below mean:

* **[PROVED]** the claim follows under the report's stated hypotheses;
* **[GAP -- REPAIRABLE]** the claim appears correct, but a proof lemma or
  quantifier is absent;
* **[ERROR -- WORDING/SCOPE]** the main theorem is not refuted, but the prose
  says more than its proof establishes; and
* **[UNSUPPORTED]** the statement is a research heuristic rather than a
  consequence of the proved filters.

## Executive verdict

I found no counterexample to either principal result:

1. eventual amplification at every fixed fitness forces the support degree of
   a uniformly sampled vertex to diverge in probability; and
2. a fixed, irreducible, positive-proportion, dense finite-type blow-up with
   unequal limiting weighted degrees has strictly smaller dB establishment
   probability than the complete-graph limit at every fixed \(r>1\).

The central mathematics is sound. The branching-to-fixation step is only a
proof sketch, however. It needs a stopped-generator lemma, and the stated
\(O(K^2/n)\) error is not justified by the assumption \(n_a/n\to q_a\).
The correct error must also contain

\[
 \eta_n=\max_a\left|\frac{n_a}{n}-q_a\right|.
\]

There are also three material scope overstatements: "for all fixed fitness
values" in the repeated-gadget paragraph, "nonzero limiting gap" when only a
positive liminf gap is proved, and the assertion that every remaining
positive family must have individually significant edges. None invalidates
the two main obstructions, but each should be repaired before publication.

## 1. Fitness monotonicity and the strong-selection upper bound

### **[PROVED] Attractiveness of dB**

After the dead vertex \(v\) is selected, only its new type matters. Its mutant
probability is

\[
 p_r(S,v)=\frac{rM_S(v)}{rM_S(v)+d_v-M_S(v)}.
\]

If \(S\subseteq T\), then \(M_S(v)\le M_T(v)\), and this expression is
nondecreasing in both \(M\) and \(r\). Using the same dead vertex and uniform
threshold in both chains therefore preserves inclusion. This remains true
when \(v\in T\setminus S\), because death first removes \(v\) and \(w_{vv}=0\).
Thus the coupling in lines 51--56 is valid.

### **[PROVED] Formula used in (1)**

The strong-selection limit can be recovered directly. If the sole initial
mutant is \(i\), then before a non-holding change the relevant death is either
\(i\), causing extinction, or one of its \(s_i\) support neighbors, causing an
adjacent second mutant. These \(s_i+1\) vertices have equal death rates, so
expansion occurs with probability \(s_i/(s_i+1)\). Once two adjacent mutants
exist, the infinite-fitness process cannot lose a mutant: every mutant has a
mutant neighbor, and connectedness then forces eventual fixation. Hence

\[
 \lim_{r\to\infty}\rho_{\rm dB}(G,r)
 =\frac1n\sum_i\frac{s_i}{s_i+1}
 =1-\frac1n\sum_i\frac1{s_i+1}.
\]

Monotonicity in \(r\) gives (1). No weight-uniformity assumption is hidden in
this step.

## 2. The support-degree quantifier

### **[PROVED, with an implicit growth hypothesis] Proposition 2.1**

Write \(n=|V(G_n)|\) and explicitly assume \(n\to\infty\). For every fixed
\(R>1\), eventual dB amplification at fitness \(R\) and (3) give

\[
 \limsup_{n\to\infty}a_n
 \le \lim_{n\to\infty}
 \left(1-\rho_{\rm dB}(K_n,R)\right)
 =\frac1R.
\]

Since this holds for arbitrarily large fixed \(R\), while \(a_n\ge0\), it
follows that \(a_n\to0\). This order of quantifiers is legitimate: no
fitness-uniform threshold is used. Line 105 should be replaced by this limsup
argument to make that fact explicit.

For \(f_n(K)=n^{-1}\#\{i:s_i\le K\}\),

\[
 a_n\ge \frac{f_n(K)}{K+1},
\]

so (5) and divergence in probability are correct.

### **[PROVED, but distinguish two meanings of positive fraction]**

If \(\limsup f_n(K)>0\), the family cannot amplify eventually at every fixed
fitness: choose a subsequence with \(f_n(K)\ge c>0\), then choose a fixed
\(r>(K+1)/c\). Along that subsequence, the strong-limit upper bound is
eventually below the complete baseline. If instead
\(\liminf f_n(K)>0\), the same fixed \(r\) gives eventual suppression for all
sufficiently large \(n\), not merely failure on a subsequence. The report
should say which interpretation of "positive asymptotic fraction" it uses.

For uniformly bounded support degree \(D\), one has
\(a_n\ge1/(D+1)\), so every fixed \(r>D+1\) eventually suppresses. This proves
failure of the all-fixed-fitness requirement.

### **[PROVED] Paths and windmills, in the mission-level sense**

Paths have \(D=2\), so they are excluded from the desired all-fixed-fitness
family, and the bound gives eventual dB suppression for every fixed \(r>3\).
For a windmill with \(2m\) leaves,

\[
 \frac1{2m+1}\left(
   \frac{2m}{2m+1}+2m\frac23
 \right)\longrightarrow\frac23,
\]

so the asserted conclusion for every fixed \(r>3\) is correct and independent
of all positive spoke and pair weight magnitudes.

### **[ERROR -- WORDING/SCOPE] "rules this out for all fixed fitness values"**

Lines 336--339 can be read as saying that the support argument proves
suppression at each fixed \(r>1\). It does not. For a positive fraction \(c\)
of degree-at-most-\(K\) vertices, the argument only forces suppression once
\(1/r<c/(K+1)\), with a liminf assumption for an eventual statement. It says
nothing pointwise at smaller \(r\). The safe replacement is:

> This rules the construction out as a family that amplifies eventually at
> every fixed fitness; for windmills it proves eventual suppression for every
> fixed \(r>3\).

Likewise, "fixed satellite gadgets" are excluded only when a positive fraction
of vertices retains bounded total support degree. A repeated fixed gadget
with a growing number of arbitrarily weak support-completion edges incident
to a typical vertex is not excluded by Proposition 2.1.

## 3. Exact rare-mutant generator

The report's branching process is the correct one. An exact rate calculation
makes both the result and the missing error term transparent. Poissonize
deaths so each vertex dies at rate one; this leaves hitting probabilities
unchanged. Let \(x_a\) be the number of type-\(a\) mutants and set

\[
 d_b^{(n)}
 =\sum_c\frac{n_c-\mathbf 1_{c=b}}n\omega_{cb},
 \qquad
 m_b(x)=\sum_c\frac{x_c}{n}\omega_{cb}.
\]

For a resident type-\(b\) target, the exact rate of a \(b\)-mutant birth is

\[
 \lambda_{b,n}^+(x)
 =(n_b-x_b)
 \frac{r m_b(x)}
 {d_b^{(n)}+(r-1)m_b(x)}.
\tag{A1}
\]

For a mutant type-\(b\) target, put
\(\widetilde m_b(x)=m_b(x)-\omega_{bb}/n\), subtracting the dead vertex from
its own class. The exact rate at which a type-\(b\) mutant is lost is

\[
 \lambda_{b,n}^-(x)
 =x_b\frac{d_b^{(n)}-\widetilde m_b(x)}
 {d_b^{(n)}+(r-1)\widetilde m_b(x)}.
\tag{A2}
\]

Irreducibility and \(q_a>0\) imply
\(\delta_*=\min_b\delta_b>0\). Uniformly on \(|x|\le K\), (A1)--(A2) give

\[
 \lambda_{b,n}^+(x)\longrightarrow
 r\sum_a x_a\frac{q_b\omega_{ab}}{\delta_b}
 =r\sum_a x_aA_{ab},
 \qquad
 \lambda_{b,n}^-(x)\longrightarrow x_b.
\tag{A3}
\]

This is exactly the count generator of independent type-\(a\) individuals
dying at rate one and producing type-\(b\) children at rate \(rA_{ab}\).

### **[ERROR -- RATE CLAIM, theorem unaffected]**

Under only \(n_a/n\to q_a\), the uniform stopped-generator error is

\[
 O_K(\eta_n+n^{-1}),
 \qquad
 \eta_n=\max_a|n_a/n-q_a|,
\]

with an \(O_r(K^2/n)\) collision and competition component. It need not be
\(O(K^2/n)\): the hypotheses permit
\(n_1/n-q_1\asymp n^{-1/2}\). Lines 217--219 should instead say that all
errors are \(o_K(1)\), or impose the stronger rounding hypothesis
\(n_a=nq_a+O(1)\).

## 4. Branching survival, stationarity, and Jensen

### **[PROVED, one omitted Perron--Frobenius sentence]**

Symmetry gives

\[
 \sum_aq_aA_{ab}
 =\frac{q_b}{\delta_b}\sum_aq_a\omega_{ab}
 =q_b,
\]

so (8) is correct. Moreover \(A\) is irreducible, and the strictly positive
left eigenvector \(q\) at eigenvalue one shows that the Perron root of \(A\)
is one. Therefore \(rA\) is supercritical for every \(r>1\), and every
survival coordinate \(s_a\) is strictly positive. The report uses \(s_a>0\)
but should state this justification.

The first-event equation (7) is also correct. If
\(q_a^{\rm ext}=1-s_a\), a birth leaves the parent alive and adds one child,
so conditioning on the first event gives

\[
 q_a^{\rm ext}
 =\frac{1+r\sum_bA_{ab}q_a^{\rm ext}q_b^{\rm ext}}
 {1+r\sum_bA_{ab}},
\]

which rearranges to (7).

Strict convexity and stationarity then give

\[
 1-\bar s\ge\frac1{1+r\bar s},
\]

and, because \(\bar s>0\), this is equivalent to
\(\bar s\le1-1/r\). I found no reversal or orientation error in \(A\).

### **[PROVED, but equality needs one displayed averaging step]**

Jensen equality forces \((As)_a\) to be constant, hence (7) forces
\(s_a=c>0\) for every \(a\). It follows that all row sums
\(t_a=\sum_bA_{ab}\) equal one common value. The missing step is

\[
 \sum_aq_at_a=\sum_{a,b}q_aA_{ab}=\sum_bq_b=1,
\]

so the common value is one. With
\(P_{ab}=q_b\omega_{ab}/\delta_a\) and \(h_a=1/\delta_a\),

\[
 (Ph)_a=\frac{t_a}{\delta_a}=h_a.
\]

The irreducible finite stochastic maximum principle makes \(h\) constant.
Conversely, constant \(\delta_a\) gives \(t_a=1\), and the survival vector is
\(s_a=1-1/r\). Thus the equality characterization is correct.

## 5. From stopped establishment to fixation

### **[GAP -- REPAIRABLE] Stopped-chain convergence must be stated**

"Transition rates converge" alone does not prove convergence of an
unbounded-time hitting probability. Here the needed lemma is elementary
because \(K\) is fixed:

1. Stop both count chains on \(|x|=0\) or \(|x|=K\). Their common interior
   state space is finite for all sufficiently large \(n\).
2. Equations (A1)--(A3) give entrywise convergence of the killed generators.
3. The limiting killed branching chain reaches one boundary almost surely.
   On the finite band \(1\le|x|\le K-1\), death rates are positive and all
   rates are bounded, so every fixed block of events has a uniformly positive
   chance of enough consecutive deaths to hit zero.
4. Hence the limiting interior generator is invertible. The finite Dirichlet
   systems for hitting \(K\) before zero depend continuously on their
   generator entries, so their solutions converge.

The singleton type distribution satisfies \(n_a/n\to q_a\), so convergence
also holds after initial averaging. Since fixation must pass through total
count \(K\), for every fixed \(K\),

\[
 \limsup_n\rho_{\rm dB}(G_n,r)\le p_K,
\]

where \(p_K\) is the averaged branching probability of hitting \(K\).

Finally, \(p_K\downarrow\bar s\). The linear-rate branching process is
nonexplosive. An extinct path has a finite maximum population, while a path
that survives but stays forever below some \(K\) has probability zero by the
same finite-band absorption argument. Thus reaching every \(K\) is survival
modulo a null event. With this lemma inserted, (10) is rigorous.

### **[PROVED after the preceding repair] Eventual finite-type suppression**

If the limiting degrees are unequal, strict Jensen gives

\[
 \gamma_r=1-\frac1r-\bar s>0.
\]

Since the complete baseline tends to \(1-1/r\), (10) implies

\[
 \liminf_{n\to\infty}
 \left(
 \rho_{\rm dB}(K_n,r)-\rho_{\rm dB}(G_n,r)
 \right)
 \ge\gamma_r>0.
\tag{A4}
\]

Therefore Theorem 3.1's eventual suppression conclusion is correct for each
fixed \(r>1\).

### **[GAP -- WORDING] "nonzero limiting gap"**

The report proves (A4), not convergence of \(\rho_{\rm dB}(G_n,r)\) or
existence of a limit of the gap. The safe phrase is "a positive asymptotic
gap" or "a gap with positive liminf." A separate
establishment-implies-fixation theorem would be needed to identify an actual
limit.

## 6. Bd regularity claim

### **[PROVED] Exact weighted regularity ties Bd**

If every weighted degree is \(d\), then symmetry of every mutant/resident cut
gives

\[
 \frac{\Pr(|S|\text{ decreases by }1\mid S)}
 {\Pr(|S|\text{ increases by }1\mid S)}
 =\frac1r.
\]

Holding probabilities may depend on \(S\), but the embedded mutant-count chain
has constant down/up ratio \(1/r\). Its absorption probability from one mutant
is the complete-graph Bd value. Lines 265--268 are correct. The report also
correctly refrains from applying this exact claim to graphs that are only
asymptotically regular.

## 7. Scope of excluded families

### **[ERROR -- SCOPE] "non-isothermal dense finite-type" needs all qualifiers**

Theorem 3.1 applies to:

* a fixed number of classes;
* every class having a positive limiting proportion;
* a fixed class-weight matrix after a common normalization; and
* an irreducible limiting matrix.

It does not cover every sequence one might informally call a dense finite-type
blow-up. Two concrete families outside the proof are:

* two positive-proportion dense classes whose cross-class weight is \(1/n^2\)
  while within-class weights are \(1/n\), so every finite graph is connected
  but the limiting class kernel is reducible; and
* a two-class construction in which one class has size
  \(\lfloor\sqrt n\rfloor\), so its limiting proportion is zero.

These are not counterexamples to Theorem 3.1, and this audit makes no claim
that they amplify. They are counterexamples to reading lines 28--32 or
381--382 as excluding all finite-type candidates without qualification. Those
summaries should say "fixed irreducible-kernel, positive-proportion dense
finite-type blow-ups with unequal limiting degrees."

The preferred two-class family is covered when its proportions tend to two
positive constants and its nonzero orbit-weight ratios tend to a fixed
irreducible kernel. If "fixed limiting parameters" permits a cross ratio
tending to zero, the stated theorem does not cover that boundary case.

### **[PROVED with its caveat] Repeated bounded-support gadgets**

A repeated gadget is excluded precisely when a positive fraction of its
vertices keeps bounded total support degree after the gadgets are connected.
It is not excluded merely because its internal module size is fixed. If a
typical gadget vertex receives a diverging number of tiny external edges, the
support condition is passed and a different argument is required. Lines
125--128 include essentially this caveat; the abbreviated status statement in
lines 381--382 should retain it.

## 8. The alleged narrow candidate corridor

### **[UNSUPPORTED] Individually significant edges are not a proved necessity**

Item 3 in lines 359--360 follows from neither obstruction. For example,
consider complete support with every edge of order \(1/n\), all weights equal
except \(w_{12}=2/n\). This family:

* has support degree \(n-1\);
* has an asymptotically regular one-type dense limit;
* is not exactly weighted-regular at finite \(n\); and
* has no individually macroscopic edge.

The proved filters do not determine the sign of its lower-order dB
comparison. This example is not asserted to amplify; it shows that the
theorems have not forced a successful family to be non-diffuse. Item 3 should
be explicitly labelled a heuristic design guess.

Consequently the final open class is broader than the "mesoscopic,
non-diffuse" wording in lines 378--379. It also includes diffuse,
asymptotically isothermal but not exactly regular perturbations whose sign is
decided below leading branching order. Mesoscopic modules are a reasonable
next search target, not the uniquely isolated corridor.

## 9. Counterexample search summary

I tried the following attacks and found no theorem-level counterexample:

* varying positive edge magnitudes cannot defeat (1), because only positive
  support enters its right side;
* choosing fitness after population size would break the support limsup
  argument, but that is the opposite quantifier from the one under study;
* unequal row sums of \(A\) do not break Jensen, because symmetry supplies
  \(q^TA=q^T\);
* multiple positive branching fixed points do not matter, because the actual
  survival vector obeys (7), strict convexity applies to it, and
  irreducibility makes it positive;
* long waiting below \(K\) does not break stopped-chain convergence once the
  finite killed-generator lemma is supplied; and
* equality with unequal limiting degrees is impossible by the harmonic
  maximum principle.

The only counterexamples found are to overbroad scope descriptions, not to
Proposition 2.1 or Theorem 3.1.

## 10. Required publication repairs

Before treating Section 3 as a complete proof, I recommend:

1. state \(n=|V(G_n)|\to\infty\) in Proposition 2.1 and replace line 105 by
   the fixed-\(R\) limsup proof;
2. distinguish limsup-positive from liminf-positive fractions of bounded
   degree;
3. replace "for all fixed fitness values" by the mission-level quantifier, or
   by the explicit threshold \(r>3\) for windmills;
4. add exact rates (A1)--(A2) or an equivalent stopped-generator lemma;
5. replace the bare \(O(K^2/n)\) claim by
   \(O_K(\eta_n+n^{-1})=o_K(1)\), unless stronger class-size rounding is
   assumed;
6. state \(\rho(A)=1\), hence positivity of the survival vector for \(r>1\);
7. add the finite killed-chain continuity and nonexplosion arguments before
   (10);
8. include \(\sum_aq_at_a=1\) in the Jensen equality proof;
9. say "positive liminf gap" instead of "nonzero limiting gap"; and
10. retain the positive-proportion, fixed-kernel, and irreducibility
    hypotheses in every summary, while labelling the non-diffuse corridor as
    heuristic.

With these repairs, the support-degree proposition and the dense finite-type
dB obstruction meet a first-principles proof standard. They remain partial
asymptotic obstructions and do not resolve the full
fixed-fitness/growing-population question.
