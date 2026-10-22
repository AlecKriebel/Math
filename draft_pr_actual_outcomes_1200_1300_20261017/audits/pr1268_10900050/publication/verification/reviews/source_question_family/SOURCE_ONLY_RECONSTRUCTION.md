# Independent reconstruction of Long's Question 7.2

## Verdict and independence

The answer to the equality question in its printed scope is **no**. A counterexample is

\[
k=\mathbb Q(\sqrt {10}),\qquad R=\mathcal O_k=\mathbb Z[\sqrt {10}].
\]

Writing \(\omega_u\) and \(\omega_p\) for the two clique numbers and \(m\) for the smallest norm of a nonzero prime ideal, the exact values are

\[
\omega_u=2,\qquad \omega_p=2,\qquad m=2.
\]

Consequently \(\omega_p=2<4=\omega_u m\). These are proofs of global maxima, including exclusion of infinite cliques, rather than results of a bounded search.

This report was reconstructed from the two specified primary PDFs and authored before inspecting any candidate submission, PR body, claimed answer, other review, or root mathematical analysis. No external person was contacted. No Git, PR, remote service, or publication mutation was performed. No priority or present-day openness claim is made.

## 1. Source question and exact scope

The versioned primary is [Delp, Hoffoss and Manning, *Problems in groups, geometry, and three-manifolds*, arXiv:1512.04620v1](https://arxiv.org/pdf/1512.04620v1), printed pages 5-6, Section 7. Question 7.1 starts with an integer polynomial irreducible over \(\mathbb Q\), all of whose roots are real, and sets \(k=\mathbb Q(\alpha)\) and \(\mathcal O_k\) to be its full ring of integers. Question 7.2 refers back to this setup. It does **not** assume that \(\mathcal O_k\) is a PID, has class number one, is Euclidean, or satisfies a condition on the image of its units in residue fields. The preceding questions ask how often some of those properties hold; they do not impose them.

Both graphs have every element of \(\mathcal O_k\) as a vertex. Distinct vertices \(x,y\) are adjacent in \(\Gamma_{\rm unit}\) when \(x-y\) is a unit. In \(\Gamma_{\rm prime}\), they are adjacent when \(x-y\) is a unit **or a prime element**. The question displays

\[
\omega(\Gamma_{\rm prime})\leq
\omega(\Gamma_{\rm unit})\min_{\mathfrak p\ {m prime}}|\mathcal O_k/\mathfrak p|
\]

and asks whether equality holds. The meaningful finite norms here are for nonzero prime ideals; including the zero prime of this domain would add an infinite quotient and would not change the minimum.

The prime-element interpretation is fixed by the underlying author primary: [Long and Thistlethwaite, *Lenstra-Hurwitz cliques and the class number one problem*](https://web.math.ucsb.edu/~long/pubpdf/LenstraHurwitz.pdf), first definition on printed page 1 and Section 3 on printed pages 9-10. Its condition (i) requires a nonunit difference to generate a prime ideal. Section 3 calls the cliques satisfying condition (i) alone prime cliques. Thus a prime element here is a nonzero nonunit \(\pi\) such that \((\pi)\) is a prime ideal, equivalently \(\pi\mid ab\) implies \(\pi\mid a\) or \(\pi\mid b\). Replacing this with mere irreducibility would change the question.

The first definition imposes an additional condition (ii) for a **Lenstra-Hurwitz** clique: for each nonunit difference \(\delta\), the map

\[
\mathcal O_k^{\times}\longrightarrow (\mathcal O_k/(\delta))^{\times}
\]

must be onto. Question 7.2's prime graph does not impose that condition. The proof below needs neither it nor any theorem asserting class number one.

### Source mismatch that must not be silently suppressed

The cited Theorem 3.1, printed page 10 of the author PDF, formulates its parameter \(L\) as a minimum among **principal ideals**. Its proof then takes a generator \(q\), calls the quotient a field, and treats \(q\) as prime. This is different wording from Question 7.2's minimum among prime ideals. A minimum over nonzero proper principal ideals, a minimum over principal prime ideals, and a minimum over all nonzero prime ideals are distinct definitions outside a PID. The unqualified principal-ideal wording also needs a proper-ideal convention to exclude the unit ideal of norm one. I do not add a PID hypothesis to the printed question, identify these minima, or use the theorem's proof to change the target. The counterexample concerns exactly the prime-ideal minimum printed in Question 7.2.

For orientation only, in the counterexample the least norm of a nonzero proper principal ideal is \(4\), while the least prime-ideal norm is \(2\). The ideal \((2)\) of norm \(4\) is not prime. Thus the distinction is concrete here, rather than a terminological objection. This observation is proved below and is not needed to obtain the strict inequality.

## 2. Exact field and ring of integers

The polynomial \(X^2-10\) is irreducible over \(\mathbb Q\) (for example, Eisenstein at 2), and its roots \(\pm\sqrt {10}\) are real. It therefore satisfies the printed setup.

Here is a self-contained check of the full ring of integers, to exclude use of a nonmaximal order. Suppose \(\theta=x+y\sqrt {10}\), with rational \(x,y\), is integral. Its trace \(t=2x\) and norm \(n=x^2-10y^2\) are integers. Hence

\[
40y^2=t^2-4n\in\mathbb Z.
\]

If \(y=r/s\) in lowest terms, \(s>0\), then \(s^2\mid40\), so \(s\in\{1,2\}\). We may therefore write \(u=2y\in\mathbb Z\). Integrality of \(n\) implies

\[
t^2-10u^2\equiv0\pmod4.
\]

If \(u\) were odd, the right term \(10u^2\) would be 2 modulo 4, which cannot be a square modulo 4. Thus \(u\) is even, and then \(t\) is even. Both \(x\) and \(y\) are integers. Conversely \(a+b\sqrt {10}\) satisfies the monic integer polynomial

\[
X^2-2aX+(a^2-10b^2),
\]

so every such element is integral. This proves \(R=\mathbb Z[\sqrt {10}]\). The trace/norm argument also covers rational \(\theta\); alternatively a rational algebraic integer is an integer.

We use the signed norm

\[
N(a+b\sqrt {10})=a^2-10b^2.
\]

It is nonzero for nonzero elements, integer valued, and multiplicative. An element of \(R\) is a unit exactly when its norm is \(1\) or \(-1\): necessity follows by taking the norm of an inverse, and sufficiency follows from the conjugate formula for an inverse.

## 3. A prime ideal of norm two which is not principal

Define

\[
\varphi:R\longrightarrow\mathbb F_2,
\qquad \varphi(a+b\sqrt {10})=a\bmod2.
\]

This is a surjective ring map because \((\sqrt {10})^2=10\) maps to zero modulo 2. Its kernel is

\[
P=(2,\sqrt {10})=
\{a+b\sqrt {10}:a\equiv0\pmod2\}.
\]

Therefore \(P\) is a proper maximal, hence prime, ideal and \(|R/P|=2\). Every nonzero prime-ideal quotient has at least two elements, so

\[
m=\min_{\mathfrak p\ne0\ {m prime}}|R/\mathfrak p|=2.
\]

To prove that \(P\) is nonprincipal without a class-number computation, suppose \(P=(a+b\sqrt {10})\). Multiplication by this generator on the integer basis \(1,\sqrt {10}\) has matrix

\[
\begin{pmatrix}a&10b\\b&a\end{pmatrix}.
\]

Its determinant is \(a^2-10b^2\), and the index of its image lattice is the absolute value of this nonzero determinant. Since \([R:P]=2\), we would have

\[
a^2-10b^2=\pm2.
\]

Modulo 5 this requires a square to be 2 or 3, but the squares modulo 5 are exactly \(0,1,4\). This is impossible. Thus \(P\) is nonprincipal. In particular \(R\) is not a PID, which is allowed by the printed scope.

The same residue obstruction excludes norms \(\pm3\). Norms of nonzero nonunits have absolute value at least 2; with absolute values 2 and 3 excluded, they have absolute value at least 4. The element 2 has norm 4, establishing the optional claim about the minimum nonzero proper principal-ideal norm.

## 4. Global clique bound by reduction modulo the nonprincipal ideal

**Lemma.** Let \(R\) be a ring of integers and let \(P\) be a nonprincipal nonzero prime ideal. No unit or prime element lies in \(P\).

**Proof.** A unit cannot belong to a proper ideal. If a prime element \(\pi\) lay in \(P\), then \((\pi)\subseteq P\). The ideal \((\pi)\) is nonzero and prime, and therefore maximal in a ring of integers. Hence \((\pi)=P\), contradicting nonprincipality. For the particular quadratic ring here, one needs no general Dedekind-domain theorem to justify maximality: the determinant formula above makes \(R/(\pi)\) finite, and a finite integral domain is a field. This proves the lemma. \(\square\)

Apply the lemma to the ideal \(P\) in Section 3. If two distinct clique vertices had the same image under \(\varphi\), their nonzero difference would be in \(P\). The difference could then be neither a unit nor a prime element, so the vertices could not be adjacent in \(\Gamma_{\rm prime}\). Reduction modulo \(P\) is consequently injective on every prime clique. Since \(\mathbb F_2\) has only two elements,

\[
\omega_p\leq2.
\]

This argument applies to any clique, with no bound on its coordinates or cardinality assumed. Since \(\Gamma_{\rm unit}\) is a subgraph, \(\omega_u\leq2\) also. The two vertices \(\{0,1\}\) form a unit clique because \(1-0=1\) is a unit. Thus

\[
\omega_p=\omega_u=2.
\]

Together with \(m=2\), this gives the strict inequality claimed at the start and completely refutes universal equality in the printed scope.

## 5. Direct arithmetic verification of the graph obstruction

The following second proof avoids ideals and ideal maximality. It is useful for independently checking the critical use of *prime element*. It shares the same parity/norm mechanism with the first proof and should not be described as statistically independent evidence.

Let \(\delta=a+b\sqrt {10}\ne0\) with \(a\) even. Its norm is even, so it cannot be a unit. Suppose it were a prime element. It divides the nonzero rational integer

\[
N(\delta)=\delta\overline\delta.
\]

Factor \(|N(\delta)|\) into ordinary positive rational primes. The defining divisibility property of \(\delta\) forces it to divide one of those rational primes, say \(p\). (It cannot divide the unit \(-1\).) Reduction of \(p=\delta\gamma\) by \(a+b\sqrt {10}\mapsto a\bmod2\) shows that \(p\) is even, hence \(p=2\). Therefore \(2=\delta\gamma\), so multiplicativity of norms gives

\[
4=|N(\delta)|\,|N(\gamma)|.
\]

The norm of the nonunit \(\delta\) is even and has absolute value greater than one. Its absolute value must be 2 or 4. Section 3's modulo-5 obstruction excludes 2. If it is 4, then \(|N(\gamma)|=1\), so \(\gamma\) is a unit and \(\delta\) is associated to 2.

But 2 is not a prime element: it divides \((\sqrt {10})^2=10\), while it does not divide \(\sqrt {10}\), as is immediate from the coefficient basis. Associates of a nonprime element cannot be prime. This contradiction proves that a nonzero element with even constant coefficient is neither a unit nor a prime element. Coloring a vertex \(a+b\sqrt {10}\) by \(a\bmod2\) is thus a proper two-coloring of \(\Gamma_{\rm prime}\). Every clique has at most two vertices, reproducing the exact graph bound.

## 6. Boundary controls, approach status, and remaining gap

* Differences are taken only between distinct vertices, so zero never qualifies as an edge label. Unit and prime status are invariant under sign; the graphs are undirected.
* The full maximal order is proved above, and the example is totally real, irreducibly defined, and genuinely in the stated field family.
* The prime-ideal minimum is attained by an explicitly given nonzero ideal with a two-element quotient. No comparison with a principal-ideal or principal-prime-ideal minimum is assumed.
* The prime graph includes unit edges. The common witness \(\{0,1\}\) proves both lower bounds even though the chosen nonprincipal ideal supplies the upper bound.
* In this ring, 2 is irreducible but is not prime. Indeed, if \(2=xy\) with neither factor a unit, their absolute norms would both be 2, impossible modulo 5. The witness \(2\mid (\sqrt {10})^2\) and \(2\nmid\sqrt {10}\) proves failure of primality. Under the wrong irreducible-edge interpretation, \(\{0,1,2\}\) would already be a three-vertex clique. The distinction therefore changes actual graph behavior.
* The ideal route is complete; the direct arithmetic route is complete and checks the same obstruction without a class-number theorem; the graph-coloring formulation is a consequence of those routes, not a third independent mechanism. An attempted route via unit enumeration, prime search, or the cited theorem's equality cases is unnecessary and supplies no additional proof.
* There is no mathematical gap in refuting the universal equality as printed. The stronger question restricted to PIDs, and questions about sharpness when a smallest prime ideal is principal, are separate targets and are not resolved or represented as resolved here.
* Mathematical validity is distinct from novelty and whether this negative answer is already recorded elsewhere. No literature-wide priority search, novelty clearance, publication clearance, or assertion of current openness is included.

## 7. Checkable finite artifact and replay contract

`finite_checks.py` performs complete finite residue checks for the two modular obstructions, checks the quotient homomorphism on the full ring modulo 2, and verifies the explicit failure-of-primality witness for 2. It uses exact integers, no random sampling, floating point, prime search, external package, or implicit assertion statement. Essential failures raise explicit exceptions in ordinary, `-O`, and `-OO` Python modes. These finite checks supplement the quantified proofs above; they do not claim that finite enumeration alone proves global clique maxima or the ring-of-integers statement.

From this directory, replay with Python 3.9 or later:

```text
python3 finite_checks.py
python3 -O finite_checks.py
python3 -OO finite_checks.py
```

Each invocation must exit zero and emit the same JSON data, matching `FINITE_CHECK_RESULTS.json`. Any nonzero exit or different result fails replay. `MANIFEST.json` lists authored files only, with relative paths, byte counts and SHA-256 hashes; it excludes itself and `_local/`. The separately retrieved primary bytes and inspection scopes are pinned in `SOURCE_PROVENANCE.json` and are not presented as authored files. Raw PDFs, extracted text and rendered page images remain local scratch under the ignored `_local/` directory.
