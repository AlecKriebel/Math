# A credited Wishart-moment corollary for OSNAP part(3)

**Source-based result, zero substantive author turns.** In the standard distortion/probability regime0<ε,δ<1 and sparsity convention1≤s≤d≤m, the exact independent sparse-sign model in Bandeira's Open Problem4.4(3) satisfies the claimed bounds. This is a direct corollary of published moment-comparison lemmas of Cai, Han and Zhang(2022), not a new OSNAP theorem. It does not settle the arbitrary-subspace or fixed-column-count parts of the source problem.

The parameters d,m are positive integers; s may be any real number in[1,d], so the result includes integer column-sparsity parameters. Range qualifications and the standalone subunit-s issue are explicit in SOURCE_SCOPE.md.

## 1. The claimed bound with conservative constants

Let z_1,…,z_m∈R^d have jointly independent coordinates taking values±1/√s with probability s/(2m) each and0 otherwise. For example, the absolute constants

    c_1=10,000,    c_2=70,000

suffice for

    P( || Σ_k z_k z_k^T − I_d || ≥ ε ) < δ

whenever

    m ≥ c_1 (d+log(1/δ))/ε²,
    s ≥ c_2 log(d/δ)/ε²,
    1≤s≤d≤m,    0<ε,δ<1.                      (1)

These constants are deliberately unoptimized. Their existence, rather than their numerical sharpness, is the source target.

## 2. Published inputs and exact model match

Cai, Han and Zhang, *On the non-asymptotic concentration of heteroskedastic Wishart-type matrix*, Electronic Journal of Probability27(2022), paper29, DOI10.1214/22-EJP758:

- **Lemma5.4**, pp.24–26: trace-moment comparison for bounded independent entries with a Gaussian Wishart matrix whose two dimensions are rounded variance sums plus the moment order minus1
- **Lemma2.6**, p.5, proof pp.18–19: the explicit Gaussian centered-Wishart operator-norm moment bound used below

[Published PDF](https://par.nsf.gov/servlets/purl/10329210), [arXiv record](https://arxiv.org/abs/2008.12434). The relevant statements and complete proofs were read; the displayed lemma statements and bounded-comparison proof pages were visually checked. Lemma5.4's proof uses symmetry of each entry, though its printed statement does not repeat that hypothesis. Our exact sparse-sign law is symmetric, so that issue does not require any extension of its proof.

Set X_{jk}=√s(z_k)_j. Then X is d×m, its entries are independent, symmetric, bounded by1, and have variance p=s/m. In the paper's notation

    σ_C² = d s/m,    σ_R²=s,    E XX^T=s I_d.

For an even integer q≥2 define

    r=ceil(ds/m)+q−1,    t=ceil(s)+q−1.

Both are positive integers and r≤t since d≤m. Let H be an r×t standard Gaussian matrix. Lemma5.4 gives

    E tr(XX^T−sI)^q ≤ min(d/r,m/t) E tr(HH^T−tI)^q.

Because q is even, the operator-norm q-th power is bounded by the trace q-th power. Conversely the Gaussian trace is bounded by r times its operator-norm q-th power. Keeping the d/r term yields

    E ||XX^T−sI||^q ≤ d E ||HH^T−tI||^q.        (2)

There is no extra factor m or log(m). Lemma2.6 gives

    (E ||HH^T−tI||^q)^{1/q}
       ≤ B := 2√(rt)+r+4(√r+√t)√q+2q.          (3)

Equations(2)–(3) are a direct specialization of the published lemmas.

## 3. Parameter substitution, d≥2

Write L=log(d/δ) and take q=2 ceil(log(2d/δ)). Then q is even, q≥2log(2d/δ), and q≤7L. For the last bound, L≥log2>2/3, log(2d/δ)≤2L, and ceil(x)≤x+1 suffice.

Put x=d/m, y=q/s. From(1),

    x≤10^{−4} ε²,    y≤10^{−4} ε².

Since r≤ds/m+q and t≤s+q, (3) implies

    B/s ≤2√((x+y)(1+y))+(x+y)
          +4(√(x+y)+√(1+y))√y+2y.              (4)

Let a=10^{−4}. Since ε<1 and a≤1, x+y≤2aε² and1+y≤2. The right side of(4) is at most

    (4+4√2)(√a+a) ε
       <10(1/100+1/10,000) ε
       =(101/1000) ε < ε/3.                    (5)

Markov's inequality, (2) and(5) give

    P( ||XX^T−sI||/s ≥ε )
       ≤d (B/(sε))^q
       <d 3^{−q} <d e^{−q}
       ≤δ²/(4d) <δ.

Finally XX^T/s=Σ_k z_kz_k^T, so this is the exact target event, including its strict probability inequality.

## 4. The d=1 edge case

The convention1≤s≤d forces s=1. Write N∼Binomial(m,1/m). Then the Gram deviation is |N−1|. For0<ε<1 its success event is N=1, whose probability is

    (1−1/m)^{m−1} ≥e^{−1}>1/3

for m≥2; at m=1 it is1. The lower bound on s in(1) forces

    δ≥exp(−ε²/c_2)>1−1/c_2>2/3.

Thus failure probability is less than2/3<δ. This treats δ arbitrarily close to1 without replacing log(d/δ) by log(2d/δ) in the statement.

## 5. Why the comparison applies to the sparse signs

The paper compares mixed scalar moments E X^α(X²−p)^β inside a centered-Gram trace expansion. For the present law, odd α give zero. If α>0 is even, the mixed moment is p(1−p)^β. If α=0 and β≥1, it is p(1−p)^β+(1−p)(−p)^β. Except for the vanishing centered first moment, their absolute values are at most p. The corresponding nonzero Gaussian mixed moments E G^α(G²−1)^β are positive integers at least1. They count Gaussian pairings excluding the internally paired centered blocks. These facts verify the entrywise domination used in Lemma5.4, also when an odd centered Bernoulli moment is negative. The shape/label-count comparison is the published argument; no arbitrary-subspace extension is introduced.

## 6. Disposition and limitations

This establishes the standard-range iid-coordinate problem as a **credited known-lemma consequence**. General OSNAP results with fixed column counts, arbitrary U, sub-polylogarithmic factors or different ε-dependence are not the proof. The source's broader parts(1) and(2) remain outside this packet. The lower convention s≥1 and distortion range0<ε<1 must accompany the disposition; SOURCE_SCOPE.md explains the literal subunit-s issue rather than concealing it. No optimal-constant, novelty, or new-discovery claim is made.
