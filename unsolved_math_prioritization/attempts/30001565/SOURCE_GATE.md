# Exact source and prior-work gate: 30001565

## Original statement and edition

Dmitrii V. Pasechnik, joint with Keshav Kini, “A GAP/Sage package for computation with coherent configurations,” Oberwolfach Report38/2010, printed pp2251–2253. The volume is dated2010; EMS records publication on2March2011. The [official report](https://ems.press/content/serial-article-files/46297) was read in full for this contribution, and printed2252–2253/PDF8–9 were rendered and inspected.

The contribution defines a coherent configuration as a disjoint 0–1 basis A_i of a unital transpose-closed matrix algebra. It then discusses the Schurian case A=A(G) of a finite permutation group G. Over C, the centralizer algebra decomposes into M_(m_chi)(C), where m_chi is the multiplicity of the group irreducible chi in the permutation representation. The goal is to compute irreducible *-representations into these m_chi-by-m_chi blocks. Characters and class data are supplied at the step under discussion.

The source constructs the central component pi_chi C[A], known to be a full matrix algebra, and describes a spectral heuristic. It assumes a self-adjoint X with distinct eigenvalues whose polynomial splits into linear factors over a splitting field of G. The final sentence asks whether one can improve the procedure without that assumption.

The exact question does **not** impose a uniform polynomial bit-complexity bound, demand that every step avoid all polynomial factorization, or require that the final standard-* matrices have entries in the original splitting field. On the preceding page even the normalized regular *-representation is explicitly allowed to introduce quadratic irrationals. The actual output goal is a *-representation over C.

The imported title “Without Polynomial Splitting” and the desk assessment's “without factoring the characteristic polynomial” should therefore be read as removal of that particular input spectral assumption, not as a new ban on every factoring oracle, algebraic extension or square root. Nothing here claims a runtime improvement over the practical heuristic.

## Prior gate

The complete pinned record and its dated literature assessment were read. The available individual desk review suggests central idempotents and rational canonical forms but supplies no certificate. The recovered campaign inventory marks no prior user/campaign work. Fresh all-state PR search for the exact ID/code and coherent-configuration wording, matching branch search, and main attempt-path history returned no match. The related-target groups contain no exact ID match. Work is isolated from main at commit d51e36e8ef706a2b740228102390bd3ac183165e.

No substantive author search turn is charged for checking a later known algorithm and its exact specialization. Proposed source-correction disposition remains subject to a separate full review.
