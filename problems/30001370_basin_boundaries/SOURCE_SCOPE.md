# Source and exact target: 30001370 / OWR-4132-003

## Primary target

Gerhard Keller (joint work with Jean-Baptiste Bardet and Roland Zweimüller),
“Self-consistent Perron-Frobenius operators for globally coupled maps,” in
*Mini-Workshop: Spectrum of Transfer Operators – Recent Developments and
Applications*, Oberwolfach Report 49/2009, printed pp. 2713–2715.
Publisher: https://ems.press/journals/owr/articles/4132 .
Full report: https://ems.press/content/serial-article-files/46250 .
The volume year is 2009; the publisher records publication on 1 September 2010.
The three contribution pages (physical PDF pages 15–17) were read and rendered.

Set I=[−1/2,1/2] and D={u in L1(I): u≥0 a.e., integral u=1}. All closures,
neighborhoods and boundaries below are relative to D with its L1 topology.
For 0<A≤0.4 and 6<B≤16, let G(m)=A tanh(Bm/A),
phi(u)=integral x u(x) dx, and r(u)=G(phi(u)). Define

    f_r(x)=((r+4)x+r+1)/(2rx+2),
    T_r(x)=f_r(x) on x<−r/4, and f_r(x)−1 on x>−r/4,
    F(u)=P_{T_{r(u)}}u.

Changing the value of T_r at its cut does not change the transfer operator.
Here P_T is the pushforward operator on densities. The source's Theorem 2
states that F has exactly three fixed densities u_−,1,u_+, every density
converges in L1 to one of them, and the two noncentral basins B_−,B_+ are open.
The contribution then asks whether W={u:F^n u→1} equals each of their relative
boundaries. It records density of B_− union B_+ as already proved. Neither a
boundary in the ambient L1 space nor restriction to smooth densities is the
question. In particular, D has empty ambient interior, which is irrelevant.

## Credited earlier paper and the restricted result already available

J.-B. Bardet, G. Keller, R. Zweimüller, *Stochastically stable globally coupled
maps with bistable thermodynamic limit*, Commun. Math. Phys. 292 (2009),
237–270, DOI https://doi.org/10.1007/s00220-009-0854-9 .
The fully readable primary preprint inspected here is arXiv:0812.4040v1,
21 December 2008: https://arxiv.org/pdf/0812.4040 . It is not represented as
an inspected copy of the final journal version. An earlier ESI copy,
https://www.esi.ac.at/preprints/esi2075.pdf , was also retrieved but its text
layer is largely unavailable. The arXiv copy supplies all the relevant proofs.

In that paper, D' consists of the mixtures of

    w_y(x)=(1−y²/4)/(1−xy)²,   −2/3≤y≤2/3.

It is a compact analytic class, not a dense subset of D. Proposition 4 and
Lemma 13 prove the common-boundary assertion for W intersect D', by order
on the mixing measures. Theorem 2, Proposition 3 and §5.1 give global
convergence and openness of B_±. The external parameter shadows in §5.1
must not be called nonlinear F-orbits without checking their feedback.
Lemma 14 and Proposition 5 in §5.3 concern directional/BV-to-L1 derivatives;
they do not supply an L1 nonlinear stable-manifold theorem. Example 1 of
the preprint permits a larger B-range; this project retains the report's
6<B≤16 target throughout.

## Retrieval and prior-attempt gate (2 October 2026)

The requested https://www.unsolvedmath.com/problems/30001370 did not yield
a usable page. The authorized pinned catalog at revision
37e53eabe540fb458758e198be61634bd02ee008 supplied the record and no prior
research result. Its imported statement agrees with the basin question,
but the parameters, space and topology are recovered from the full primary
report, rather than guessed from the title.

At live main efd29c05204703acca9a0860812f54b94fae54b1, QUEUE rank 383 is
queued, 0/5. Exact-ID all-state pull-request, branch and commit searches
found no earlier attempt. Main code search found only catalog/assignment
metadata. A 443-ref local repository inventory and all-ref subject/path
searches found no overlapping proof. Alias searches for basin boundaries,
self-consistent transfer operators and Keller produced only unrelated
harmonic-measure and Jacobian work. No neighboring attempt is recounted.

A bounded later-literature check covered the primary authors' publication
pages, Tanzi's 2023 review (10.1007/s40574-023-00350-2), Galatolo's 2022
work (10.1007/s00220-022-04444-4), Bahsoun–Liverani's 2025 work
(10.1016/j.aim.2025.110115), and the 2026 cone-contraction paper
(10.1007/s10955-026-03586-2). None of the inspected material supplied the
exact full-D boundary result. This is a limited search, not a novelty or
universal current-status certification.

## Public scope

Public artifacts contain original mathematical exposition, proofs and checks.
Raw source PDFs, source renders and imported catalog records stay local.
Source retrieval, literature comparison and packaging consume no author turns.
The first checkpoint below consumes one substantive mathematical turn.
