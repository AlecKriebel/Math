# Independent adversarial review: 30001804 / OWR-5158-001

**Verdict: PASS_SCOPED_CERTIFICATE_REDUCTION.** The algebraic certificate formulas are correct for left modules over arbitrary unital rings. The explicit general-genus surface presentation and the broader module-structure question remain **unsolved**. No new finite-generation, finite-presentation, or priority claim is justified.

Reviewed on 2026-09-30 by a separate gpt-6-astra agent at xhigh reasoning. This is an AI source/proof audit, not human peer review. Final reviewed `PARTIAL_RESULT.md` SHA-256:

`5dfdb8485eb030b05ce81b69268d75625e2633e0888c3d3117172e475d759d40`.

The originally submitted hash was `0ce654eaaccca5227fd9e9cdfa57daa8d1b08ccec0395222dbbb693f8bc79d07`. I requested one narrow clarification: the conditional search must explicitly assume computable ring operations. An exact full-file comparison confirms that this hypothesis sentence is the sole change. No formula or mathematical proof changed; no mandatory correction remains.

## 1. Exact source and surface convention

I read the primary [Oberwolfach report](https://oa.tib.eu/renate/server/api/core/bitstreams/b5c4c1c3-353d-4cd9-b9fc-9915ad312a53/content), including the marked-point convention on printed p.1645, the definitions, Problems1 and2 on p.1649, and the following discussion on p.1650. I visually inspected p.1649. The target combines understanding the module structure with a presentation on Broaddus's designated generator. It does not merely ask whether some finite one-generator presentation exists.

The superscript in $\Sigma_g^1$ denotes one marked point here. It is not a boundary circle whose points must all be fixed. The integral module is reduced curve-complex homology in degree $2g-2$ with the stated mapping-class-group action. The submitted artifact preserves those conventions.

## 2. Imported finite presentation and cyclicity

I independently checked the full relevant passages of [Broaddus, arXiv0711.0011v3](https://arxiv.org/abs/0711.0011), especially §2, Proposition3.6 and its proof, Theorem4.2, its reduction through Propositions4.5–4.6, and Remark4.7. Proposition3.6 and Remark4.7 were also visually inspected. The current arXiv record lists v3 dated3November2011 and publication in Duke Mathematical Journal161(10)(2012),1943–1969, DOI10.1215/00127094-1645634. The full text actually audited is the23-page v3 manuscript, not a newly retrieved typeset journal copy.

Proposition3.6 gives finite oriented0-filling orbit representatives as module generators. Its relations include both the boundaries of1-filling representatives and the signed stabilizer terms

$$(1-\varepsilon_i h_i)e_i.$$

The stabilizers of the underlying filling arc systems are finite cyclic groups; their generator acts on the ordering of arcs with sign $\varepsilon_i$. Thus one signed generator relation per stabilizer suffices, and omitting these relations would incorrectly treat the oriented orbit module as free. The artifact includes them all.

Theorem4.2 gives the specified0-filling cyclic generator, which may be selected as $e_0$ among those orbit representatives. Remark4.7 explicitly observes theoretical calculability of a finite generating set for an annihilator ideal. Its displayed ideal is for the closed-surface group; the analogous existence statement for the marked-surface module already follows from the same finite presentation and cyclicity. The new algebraic certificate format does not turn this known existence result into the requested computed general-genus relation list.

## 3. Noncommutative certificate lemma

Let $F=\bigoplus Re_i$, $N=\sum Rr_j$, and assume $e_i-a_i e_0\in N$, with $a_0=1$. The map $T:F\to R$ defined by $T(e_i)=a_i$ is left-linear, so

$$T\!\left(\sum_i x_i e_i\right)=\sum_i x_i a_i.$$

Every $x$ satisfies $x-T(x)e_0\in N$. Hence $T(N)e_0\subseteq N$, while $re_0\in N$ implies $r=T(re_0)\in T(N)$. Moreover left-linearity gives

$$T(N)=\sum_j RT(r_j)=\sum_j R\left(\sum_i b_{ji}a_i\right).$$

This proves equality with the annihilator, not merely containment. Cyclicity makes $R\to M$, $r\mapsto r[e_0]$, surjective, so the quotient presentation follows. The order $b_{ji}a_i$ is forced; replacing it by $a_i b_{ji}$ is invalid. No commutativity, domain, Noetherian, or coherence assumption on $R$ enters. The annihilator is a left ideal; the argument does not make it two-sided.

Literal certificates $e_i-a_i e_0=\sum_j c_{ij}r_j$ in the finite free module suffice. Their existence is a consequence of the module statement, but a proposed surface presentation must actually supply them or another completeness proof. Checking only that the resulting relators act by zero is not enough. The artifact is appropriately explicit about this distinction.

## 4. An arbitrary cyclic representative

For $c\in F$ with $e_i-a_i c\in N$, one has $x\equiv T(x)c\pmod N$. Thus both $T(N)$ and $1-T(c)$ annihilate $[c]$. Conversely, if $rc\in N$, left-linearity gives $rT(c)\in T(N)$, and

$$r=r(1-T(c))+rT(c)$$

places $r$ in $T(N)+R(1-T(c))$. This proves formula(4) without commuting any factors. It also handles the zero-module boundary case.

The integer control is exact: in $\mathbb Z/2$, $c=3e$ and $a=3$ satisfy $e-ac=-8e\in2\mathbb Ze$, but $T(2e)=6$. The extra term $1-T(c)=-8$ is necessary to obtain $(6,-8)=2\mathbb Z$. Substitution of old relations alone would give the wrong quotient.

For signed stabilizers, substitution gives $(1-\varepsilon_i h_i)a_i$, with precisely that order. Independent integral $\mathbb Z[S_3]$ controls verify the conjugation and orientation signs: when $h=a k a^{-1}$, the correct relation is $(1-\varepsilon h)a=a(1-\varepsilon k)$. Reversing the factors can give a nonzero class even when the correct relation vanishes. These are finite-group diagnostic modules, not computed surface mapping classes.

## 5. Conditional algorithm and the genuine gap

With the clarified effective encoding, computable ring operations, enumerable elements, and recursively enumerable equality, all candidate finite tuples $(a_i,c_{ij})$ can be enumerated. Each finite set of coordinate equalities can be semidecided, and dovetailing avoids being trapped at a false candidate. Cyclicity guarantees some successful tuple. Neither a decision procedure for inequality nor a Noetherian condition is needed.

This is a conditional enumeration result for a supplied effective finite presentation. It gives no bound, no practical implementation for mapping-class groups, and no explicit genus-dependent $a_i$ or relation family. The artifact does not claim otherwise. Those missing surface certificates and the broader structural information are the actual unsolved part.

## 6. Current-source distinction

I read the stated theorem and corollary in [Irmer's2026 published paper](https://www.ms.u-tokyo.ac.jp/journal/c4403d3f4e9f2de5b1eca004b17daed0cf0807b1.pdf), J.Math.Sci.Univ.Tokyo33(2026),1–19. Theorem1.1 concerns explicit generating spheres for a closed surface of genus at least2. Corollary1.2 states faithfulness of the action of the quotient by the center, a qualification absent from the short abstract. The artifact retains that qualification.

Closed- and marked-surface results are related: Broaddus's Lemma2.3 and Corollary2.4 identify the Steinberg module after forgetting the point and show that the marked-surface action factors through the closed-surface group. In particular, faithfulness for the quotient of the closed group does not imply faithfulness of the marked group; the point-pushing subgroup already acts trivially. These relationships do not supply the missing explicit annihilator relations, so the artifact's unresolved classification is still correct. This review does not independently reprove Irmer's full geometric argument; it verifies the source scope used here.

## 7. Exact checks and final verdict

The submitted verifier was replayed in `author_replay/`. All72,079 assertions pass, and its receipt reproduces byte-for-byte for the final hash. The code genuinely checks the indicated $M_2(\mathbb F_2)$ relation modules, left-linearity, reversed-order failure, and integer consistency controls.

The independent script uses $M_2(\mathbb F_3)$, including all6,561 vectors of a two-generator free module, a separate direct-action kernel calculation, an arbitrary-representative check, and the integral signed $S_3$ controls. All6,987 assertions pass. These checks supplement the algebraic proof; they do not enumerate arc orbits or mapping-class relators.

Run:

```sh
python author_replay/verify.py
python independent_checks.py
```

Recommended status: **unsolved, 2/5 approaches**. The scoped certificate result passes, with the one effective-operation clarification resolved. The original general-genus target, practical computation, novelty, and human peer review remain unclaimed.
