# Independent scope, proof, and priority audit of the variable-base counterexample

## Findings

The construction is a **full negative answer to the universal variable-base completeness assertion** in the original question. Its parameters satisfy the original hypotheses, including positivity, irrational ratio, repetitions as separate positions, and exponent zero. Every indexed term is even, so arbitrarily large odd integers remain unrepresentable. No defect was found in the full 9,813-byte proof audited here.

The negative answer is also a **direct consequence of identified published 2006 mathematics**. The exact quartic family and the required positive multiplier occur in Artūras Dubickas's papers. Scaling by two, shifting past the initial exceptional exponents, and taking a one-step shifted second stream give the answer immediately. The finite shift 20 makes this consequence explicit and independently checkable. This review does not establish that the application to the named problem was previously printed, nor does it establish novelty of that application or of the quantitative shift. The theorem-specific implication is proved below; it is not inferred from a tracker label or from generic similarity.

The fixed-base-2 question remains separate. Its survival does not make the negative answer to the variable-base assertion partial. A classification of every base in the interval is a stronger task and is not supplied.

## Exact original scope

I freshly downloaded the originals and visually read Graham's printed page 36 (PDF page 15), including question 12, and printed page 24 (PDF page 3), including the subset-sum and completeness definitions. The coefficients are positive reals with irrational ratio; the displayed sequence includes their floors before any multiplication. The follow-on question permits a base between 1 and 2. The sumset uses a separate zero-or-one coefficient at each position and finite support; completeness concerns all sufficiently large integers. [Graham, *On sums of integers taken from a fixed sequence* (1971)](https://mathweb.ucsd.edu/~ronspubs/71_08_integer_sums.pdf).

I independently confirmed the formulation on printed page 58 (PDF page 54) of the book, together with its definitions on printed pages 53–54 (PDF pages 49–50). These are the pages actually visually inspected, not a cover-to-cover reading claim. There is no added requirement that the streams be disjoint, that the multipliers be multiplicatively independent, or that their ratio avoid irrational powers of the chosen base. [Erdős–Graham, *Old and New Problems and Results in Combinatorial Number Theory* (1980)](https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf).

The question is phrased as an investigation, rather than a formally quantified theorem. The universal affirmative assertion under test can be written precisely as follows: for every \(\gamma\in(1,2)\) and every \(a,b>0\) with \(a/b\notin\mathbb Q\), the sequence

\[
s_{2n+1}=\lfloor a\gamma^n\rfloor,\qquad
s_{2n+2}=\lfloor b\gamma^n\rfloor\quad(n\ge0)
\]

has a threshold \(T\) such that every integer \(M\ge T\) equals \(\sum_{j\in F}s_j\) for some finite set of positions \(F\). Equal numerical values at different positions remain separately usable. A single admissible triple for which all terms are even disproves this assertion. It does not answer every possible follow-up about the interval of bases.

## Independent proof check

Put \(P(X)=X^4-X^3-X^2-X-1\), let \(g\) be its positive root, and set

\[
c=\frac1{(g-1)P'(g)},\qquad a=2cg^{20},\qquad b=ga.
\]

**Root and sign checks.** Descartes' rule counts one positive root with multiplicity; the exact endpoint signs give \(48/25<g<193/100\). For \(Q(t)=P(-t)\),

\[
Q'(t)=4t^3+3(t-1/3)^2+2/3>0\quad(t\ge0).
\]

The endpoint signs at \(77/100\) and \(39/50\) therefore give exactly one negative root \(-u\), with \(77/100<u<39/50\). Both real roots are simple; the other two roots must be a distinct nonreal conjugate pair \(z=x+iy,\bar z\), with \(y>0\). A repeated nonreal root would force its conjugate to repeat and exceed degree four.

Vieta gives \(x=(1-g+u)/2\) and \(|z|^2=1/(gu)\). Consequently

\[
-2/25<x<-7/100,\quad
5000/7527<|z|^2<2500/3696<25/36,
\]
\[
y^2>5000/7527-4/625>16/25.
\]

Thus the three roots other than \(g\) have modulus below \(5/6\), and \(y>4/5\). Also
\(P'(g)=(g+u)|g-z|^2>0\), so \(c,a,b>0\). A rational root of this monic integer polynomial would be an integer; \(1<g<2\) excludes that possibility. Hence \(a/b=1/g\) is irrational.

For application of the older theorems, the minimal-polynomial condition also holds. Modulo 2, \(P\) has no root and has remainder \(X+1\) upon division by the only monic irreducible quadratic \(X^2+X+1\). A reducible quartic without a linear factor would have such a quadratic factor. Thus \(P\) is irreducible over \(\mathbb Q\), and \(g\) is a Pisot number with minimal polynomial satisfying \(P(1)=-3\). Irreducibility is not required for the direct four-root proof itself.

**Trace check.** For every root \(r\), put \(c_r=1/((r-1)P'(r))\) and \(S_m=\sum_r c_r r^m\). Partial fractions at \(X=1\), with the sign reversal between \(1-r\) and \(r-1\), give \(S_0=S_1=S_2=S_3=+1/3\). Every root obeys the quartic recurrence, so

\[
S_m=k_m+1/3,\quad k_0=k_1=k_2=k_3=0,\quad
k_{m+4}=k_{m+3}+k_{m+2}+k_{m+1}+k_m+1.
\]

This proves the residue and integrality for all indices by induction. The residue is not zero, and the inhomogeneous term is \(+1\). An independent field-arithmetic computation gives

\[
c=(50-341g+48g^2+80g^3)/1689,
\]

and independently recovers these trace values.

**Coefficient and shift check.** The root separation bounds give

\[
|(-u-1)P'(-u)|=(1+u)(g+u)|-u-z|^2>32/25,
\]
\[
|(z-1)P'(z)|=|z-1||z-g||z+u||z-\bar z|>32/25.
\]

For the second line, the first two factors exceed one since \(x<0\) and \(g>1\); the last two exceed \(4/5\) and \(8/5\). Each nonleading \(|c_r|<1\). Therefore the real error \(E_m=\sum_{r\ne g}c_r r^m\) satisfies \(|E_m|<3(5/6)^m\). The exact inequality \(18\cdot5^{20}<6^{20}\) gives \(|E_m|<1/6\) for every \(m\ge20\). It follows that

\[
cg^m=k_m+1/3-E_m,\qquad
2k_m+1/3<2cg^m<2k_m+1.
\]

Hence \(\lfloor2cg^m\rfloor=2k_m\) for every \(m\ge20\). Taking \(m=20+n\) and \(21+n\) covers both streams for every \(n\ge0\), including their first positions. Any finite sum is even, irrespective of repeated values. This is the full obstruction required.

## Published mechanism and direct implication

The Glasgow paper's Theorem 1(iv), printed page 332, places Pisot or Salem numbers with minimal-polynomial value at 1 at most \(-3\) in the class admitting an all-even floor sequence with a nonzero multiplier. The same page explicitly treats \(X^{d-1}-X^{d-2}-\cdots-X-1\), including the current quartic at \(d=5\). Its printed-page-334 proof uses the Pisot multiplier \(1/(P'(g)(g-1))\), limiting residue \(1/|P(1)|\), and an exponent shift. Both pages were freshly visually inspected. An existential nonzero multiplier alone would not settle the present positive-parameter problem. [Dubickas, *Even and odd integral parts of powers of a real number*, Glasgow Mathematical Journal 48 (2006), 331–336, DOI 10.1017/S0017089506003090](https://doi.org/10.1017/S0017089506003090).

The sign and limit are explicit in the earlier mechanism: Theorem 4 is on printed page 154, and its printed-page-156 proof takes \(c=1/(P'(g)(g-1))>0\) and proves \(\{cg^m\}\to1/|P(1)|\). I freshly visually read those pages. In the current case the limit is \(1/3\), strictly between zero and one half. This supplies exactly the missing sign and limit hypotheses. [Dubickas, *On the limit points of the fractional parts of powers of Pisot numbers*, Archivum Mathematicum 42 (2006), 151–158](https://dml.cz/handle/10338.dmlcz/107991).

Here is the complete deduction from that older positive-parameter result, without the quantitative error bound. Choose an integer \(N\ge1\) such that \(0<\{cg^m\}<1/2\) for every \(m\ge N\). Such an \(N\) exists by convergence to \(1/3\). Define \(a=2cg^N\) and \(b=ga\). If \(cg^m=j_m+f_m\) with integer \(j_m\) and \(0<f_m<1/2\), then \(\lfloor2cg^m\rfloor=2j_m\). Thus both streams are even for every exponent from zero onward. The positive parameters and irrational ratio were checked above. This establishes a direct old-theory consequence, not merely an analogy with an old construction.

Scaling, sign, and indexing all matter. Fractional parts below one half imply even floors after multiplication by two; the same multiplier is not silently reused without that factor. A negative multiplier is not corrected just by negation: for nonintegral \(t\), \(\lfloor-t\rfloor=-\lfloor t\rfloor-1\), which reverses parity. Finally, at base 2 the one-step shift makes the ratio rational; at this irrational base it makes the ratio admissible. None of these steps assumes the conclusion.

The explicit value of \(N\), the self-contained bounds, and the presentation as an answer to this particular question can be useful exposition. They do not establish a new mathematical mechanism. No exhaustive priority claim, or claim that a named-problem answer was explicitly published before this submission, follows from the bounded source review.

## Reproducibility, falsification, and exact remaining limits

The separate standard-library verifier performs 817 exact checks without importing candidate code or a numerical algebra library. It independently solves for \(((X-1)P'(X))^{-1}\) in the quotient field, computes multiplication-map traces at indices 0–275, bisects the positive root 600 times, and encloses 256 consecutive floors at indices 20–275 by rational inequalities. It checks the rational inequalities in the proof and all six displayed pairs. Ordinary and optimized Python executions have byte-identical output in `VERIFICATION.json`.

Meaningful failure controls succeed: the unshifted floor at index 3 is 1; omitting the factor two produces an odd floor at index 24; doubling that factor again produces an odd floor at index 20; and negating the positive even-floor multiplier produces an odd floor. These controls test the vulnerabilities relevant to the argument. Finite sampling is not the proof of all-future parity; the trace induction and uniform strict bound above are that proof.

Input identities and fresh primary-source hashes are recorded separately in `INPUT_PINS.json` and `SOURCE_PINS.json`. The freshly retrieved PDFs match the submitted source metadata byte-for-byte. The source PDFs and page renders remain private audit evidence and are not public report attachments.

**Disposition:** full variable-base negative answer verified; exact construction sound; direct implication of named 2006 positive-parameter theory verified; novelty of the named-problem application and of the explicit quantitative presentation unestablished. No mathematical repair is required. No claim is made here about current external problem status, publication readiness, exhaustive historical priority, or the unsolved fixed-base question.
