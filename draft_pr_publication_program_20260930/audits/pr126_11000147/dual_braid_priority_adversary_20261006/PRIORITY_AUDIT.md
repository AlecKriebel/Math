# PR126: independent band-generator priority adversary

Original head: `a1df84a64fa96d53f3a8c6fec9db8bc48bd1533c`. Target: 11000147 / AMR-109-0147. This is an independent mathematical-content/priority audit, not a new discovery attempt. Original effort remains 1/5; added central proof-search turns: 0.

## Verdict and limits

The exact pair-to-triple mechanism is encoded in a published 1998 braid-group presentation. Combining it with the Anosov pair explicitly described in Wajnryb's source yields the entire narrow closed-torus existence result. There is no new algebraic obstruction or theorem needed to make this transfer, and faithfulness plays no role. The candidate is mathematically correct under the source's explicit genus-one convention, but a substantive new mathematical theorem has not been established by it.

This is a **published mathematical-content obstruction to promoting the result as a novel resolution**. It is not evidence that BKL explicitly stated Wajnryb's later question or its answer. No express earlier announcement of the exact Wajnryb triple answer was located by this bounded search. The first application of the old identities to that named question, and the first appearance of these exact integer matrices, remain unconfirmed. An `already_solved` project disposition, if chosen, must say that it concerns a direct consequence of prior published content, rather than falsely asserting a located earlier named solution.

## Full legitimate primary anchor and exact substitution

Joan Birman, Ki Hyoung Ko, Sang Jin Lee, *A New Approach to the Word and Conjugacy Problems in the Braid Groups*, Advances in Mathematics **139** (1998), 322–353. The complete published PDF is author-hosted at <https://www.math.columbia.edu/~jb/bkl-newpres.pdf>. Its SHA-256 is `3a80d7836dd218638addf22d4f6205fb67206db770f817abfc2c23e4b8b029e9` (653,301 bytes). The title page verifies the 1998 journal publication; arXiv:math/9712211 records v1 on 2 December 1997 and v2 on 7 April 1998. I inspected the complete relevant definitions, proposition, and proof, and visually checked printed pp.325,327,328.

Definition Eq.(4), printed p.325 / PDF page4, gives for n=3

\[
a_{32}=\sigma_2,\qquad a_{21}=\sigma_1,\qquad
 a_{31}=\sigma_2\sigma_1\sigma_2^{-1}.
\]

Proposition2.1, Eq.(8), printed p.327 / PDF page6, specializes to

\[
a_{32}a_{21}=a_{31}a_{32}=a_{21}a_{31}.
\]

Let G be any group with distinct a,b satisfying aba=bab. The Artin presentation of B3 gives a homomorphism

\[
\phi:B_3\longrightarrow G,\qquad \phi(\sigma_2)=a,\quad \phi(\sigma_1)=b.
\]

There is no injectivity assumption. Setting c=phi(a31)=aba^{-1}, the published relation becomes exactly

\[
ab=ca=bc. \tag{*}
\]

The candidate's c is therefore the image of the old third band generator, with the correct conjugation direction. BKL's proof on p.328 also explicitly derives the ordinary adjacent-generator braid relation from Eq.(8); the three-generator consequence can be checked with these short rewrites:

\[
aba=(bc)a=b(ca)=bab;
\]
\[
aca=a(ca)=a(ab)=a^2b,
\quad cac=(ca)c=(ab)c=a(bc)=a^2b;
\]
\[
bcb=(bc)b=ab^2,
\quad cbc=c(bc)=c(ab)=(ca)b=ab^2.
\]

Thus every pair braids in every quotient. This proves more than an analogy with a braid presentation: the required identities are literal homomorphic images of its published equations.

## Distinctness and dynamics survive without faithfulness

It would be wrong simply to infer that distinct B3 generators have distinct images. Here cancellation supplies the missing check. If c=a, then aba^{-1}=a implies b=a. If c=b, then aba^{-1}=b implies ab=ba; together with aba=bab this forces a=b. Both contradict the initial distinct pair. For any pair u,v satisfying uvu=vuv, commutativity would imply u=v by cancellation. Hence all three images are distinct and pairwise noncommuting.

The third image c is conjugate to b. Consequently any conjugacy-invariant property possessed by the initial pair is preserved, including the pseudo-Anosov mapping-class property. On the closed torus the candidate uses actual linear maps, and conjugacy by the linear torus diffeomorphism gives an actual Anosov map. No choice of unrelated mapping-class representatives, faithful Artin representation, minimal generating set, nonconjugacy, or prescribed higher genus is needed or proved.

## Exact target bridge and independent binding check

Wajnryb, *Relations in the mapping class group*, Chapter8, Section2, manuscript printed p.124 / PDF page131 of <https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf>, states the triple question and immediately credits the referee with suitable length-three pseudo-Anosov pairs, including the torus prescription x^2=-I, y^3=I. The chapter introduction on printed p.122 allows compact surfaces; the torus is explicit, not a substituted negative-Euler-characteristic target. The full legitimate source has SHA-256 `f37c6a1dbc875105c2b294196de1a03a88595b75e8705e6077e9d48f066e402a`. I independently inspected the question's entire page visually.

The submitted X and Y are an instance of that source prescription:

\[
X=\begin{pmatrix}0&1\\-1&0\end{pmatrix},\qquad
Y=\begin{pmatrix}-2&-1\\3&1\end{pmatrix},\quad
X^2=-I,\quad Y^3=I,\quad A=XY,\quad B=YX.
\]

Under phi(sigma2)=A and phi(sigma1)=B, Eq.(4) gives exactly the submitted C. The three Eq.(8) products satisfy

\[
AB=CA=BC=\begin{pmatrix}2&-3\\1&-1\end{pmatrix}.
\]

Each of A,B,C has determinant1 and trace4, so the claimed hyperbolic images and their induced actual torus maps follow. The common product AB has trace1; it is not asserted to be Anosov. The source pair plus the old presentation therefore leave no unsolved central mathematical step for this bounded claim.

`verify_published_binding.py` checks this exact substitution, the symbolic word rewrites, distinctness, noncommutation, and the source factorization. Normal and optimized executions passed with identical substantive results. Explicit negative controls reject a false word rewrite and the opposite-conjugation choice as an incorrect binding to this particular band-generator formula. The latter is not a claim that every other conjugate construction fails to braid. The arbitrary-group proof is the symbolic/cancellation argument above; matrix computations are only a binding check.

## Corroboration and excluded false matches

- Birman–Menasco, *A Note on Closed 3-Braids*, Communications in Contemporary Mathematics10, Suppl.1 (2008), 1033–1047, author PDF <https://www.math.columbia.edu/~jb/3-braids.pdf>, Section2.1, Eq.(2.1), printed p.1036 / PDF page4, explicitly gives the three-generator B3 band presentation, including a3=sigma1^{-1}sigma2sigma1, equivalent to sigma2sigma1sigma2^{-1}. This independently corroborates the precise old three-generator mechanism; it is not an express answer to Wajnryb's question. SHA-256 `b62aec268ac9862a3269243eb1ee465a9ddfca41b0904929a6bb031ca250fb01`. Its 2008 date was verified from the published title page; a provisional local filename labeled2011 was corrected without changing bytes.
- BKL and Birman–Menasco credit Xu's 1992 B3 work. I have not audited Xu's original full text and do not assert an exact 1992 theorem locator. The 1998 primary anchor suffices for this obstruction.
- Mortada, arXiv:1008.0124v3 (23September2011), full21-page primary PDF, introduction and Theorems1.1–1.4 concern the preceding two-element Artin-relation question. They do not state this pseudo-Anosov triple answer. Text search finds no `pseudo` occurrence. This is a scoped exclusion, not proof that an answer never appeared elsewhere.
- Baader–Feller–Ryffel, *Bouquets of curves in surfaces*, publisher PDF, Theorem1 on p.90, has pairwise braid and cycle relations for positive Dehn twists. It concerns a different class of maps and is not evidence of an earlier pseudo-Anosov triple answer.

Searches used exact question wording and Wajnryb/pseudo-Anosov/Anosov combined with triple, pairwise, everypair, braid relation, triangular Artin groups, and band generators. No retrieved primary source expressly announced the exact named triple answer. Search absence is not priority certification.

## Scientific contribution advice

The concrete matrices, direct actual-map exposition, and verification package can have pedagogical or reproducibility value. Their exact-instance first priority and the first-recognition priority for applying BKL to Wajnryb are unestablished. They do not substantiate a new group lemma or a new mechanism for producing Anosov pairs. A first-application or expository note would require a deliberately qualified scholarly framing; it cannot be represented as a certified novel open-problem breakthrough on this audit evidence.

For the user's requirement of a novel full resolution, my advice is to withhold promotion/publication as novel and use a carefully scoped prior-content disposition if the root's independent disposition review concurs. No repair of wording can make the universal mechanism new. A genuinely stronger higher-genus, faithful, or larger-set theorem would be a new research target, beyond this PR's verified result; this audit has not undertaken it.

No Git, index, main branch, native catalog, PR, author branch, publication, tracker, or external-outreach operations were performed. Public source PDFs and page renders stay in ignored private storage; only this analysis and verification artifacts are intended for the audit checkpoint.
