# Independent source-question research log

Scope: Farb Question 7.6 only, original source and primary mathematical background. No candidate or other review inputs read. No external individual contacted. Source body assets remain ignored.

## 2026-10-17T20:19:17.319209+00:00 - source conventions (15% estimated completion)

Retrieved the 402-page author-hosted volume; read only printed p.14 (PDF p.21) and printed pp.49-51 (PDF pp.56-58), and visually inspected printed p.51. The filtration uses Gamma_0=Gamma and I_g(k)=ker(Mod_g -> Out(Gamma/Gamma_k)); I_g(1) is Torelli and I_g(2) the Johnson kernel. Spectrum multiplicity counts ambient Mod_g conjugacy classes. Question 7.6 is separate from the simple-spectrum Question 7.7.

Initial approach families: (A) adapt trace-equivalent free words in a convex-cocompact Thurston subgroup in fixed Johnson depth; (B) arithmetic/lattice Veech subgroup and quotient constraints; (C) direct train-track characteristic-polynomial construction. Main apparent difficulty in A: establish a uniform comparison between subgroup and ambient conjugacy. A compact convex core may provide a uniform finite bound through its immersion into the full disk stabilizer quotient. This is an unverified mechanism at this checkpoint.

## 2026-10-17T20:20:49.753207+00:00 - compact-core conjugacy mechanism verified (65% estimated completion)

Proved a uniform fusion lemma: if H is convex cocompact in a discrete Fuchsian overgroup G, choose compact K with HK=Hull(Lambda_H). The finite set S={gamma in G: gamma K intersects K} bounds the number of H-conjugacy classes in a G-conjugacy class of hyperbolic elements of H. Conjugate a base element so its axis meets K; move the image of that basepoint back into K using H. Its ambient conjugator then belongs to S. This removes the principal ambient-conjugacy gap without assuming H has finite index, is malnormal, or that the full disk stabilizer is finitely generated.

Read Horowitz's original Example 8.2, printed pp.648-649 (PDF pp.14-15; visually inspected p.648). Read Leininger 2004 printed pp.1313-1318 (PDF pp.13-18), with relevant Theorems 3.1-3.2 on pp.1314-1315: full disk stabilizer derivative is discrete with finite kernel; hyperbolic derivative gives log dilatation half the hyperbolic translation length; pseudo-Anosov stabilizes a unique Teichmuller disk. The latter forces every ambient conjugator between elements of our subgroup into that same stabilizer.

Current proposed full route: filling separating twists -> free Thurston group in I_g(2) -> iterated commutator and a noncommuting conjugate in fixed deep filtration term -> sufficiently high powers form convex-cocompact rank-two Fuchsian group -> Horowitz trace-equivalent words -> compact-core fusion bound -> unbounded ambient multiplicity. Remaining work: audit filtration indexing and free-group independence, write all lemmas and exact boundaries, verify explicit trace-word formulas computationally, then freeze. No candidate/other-family material has been read.

## 2026-10-17T20:23:38.968853+00:00 - completed derivation and exact checks (100% reconstruction completion estimate)

Full-scope derivation written for every fixed g>=2 and finite k>=3. The main theorem is unbounded ambient-conjugacy multiplicity; it does not assert infinitely many classes at a single length or primitive ambient representatives. The explicit hyperbolic commutator recurrence is verified exactly in 12 finite cases, and Horowitz recursion levels 1-5 pass cyclic conjugacy, root-free, inverse-conjugacy, and three-representation trace checks. Distinct route families and their exact gaps are recorded in DERIVATION.md.

Final self-audit checked filtration indexing, outer representatives, genus 2, hyperbolic versus parabolic commutators, disjoint fixed points, compact-core uniformity independent of length, full disk stabilizer discreteness, uniqueness of the invariant disk, faithful restriction despite finite ambient kernel, common exact length, and fixed Johnson depth while family size grows. No mathematical gap identified; independent adversarial review is still appropriate.

Freeze follows this entry. All authored artifacts will be hashed before any candidate or other-family inputs are received. No external communication, Git state mutation, publication, or other-family reading occurred.
