# Exact source scope

Problem 30001554 / OWR-4425-009 is Conjecture 27 in Dirk Nowotka's contribution, joint work with Bastian Bischoff, “Word periods under involution,” OWR37/2010, printed pp.2219–2222. The complete contribution and printed equation were read. [Official report](https://ems.press/content/serial-article-files/46296).

The involution is **morphic**: theta(uv)=theta(u)theta(v), theta²=id. It may have fixed letters. The word is nonempty and finite. A theta-border means a **nonempty proper** prefix v such that theta(v) is a suffix; overlaps are allowed. The source uses the usual nonempty-border convention. Kari–Mahalingam, Definition2(12), makes it explicit. Empty words are outside the nonempty tau/minimal-positive-period normalization used here.

An alternating theta-period p is the length of u for which w is a prefix of (u theta(u))^omega. This is more restrictive than arbitrary concatenations of u and theta(u), and is distinct from the weak theta-period. The exact question is n>=3 tau_theta(w) implies tau_theta(w)=pi_theta^alt(w).

The adjacent antimorphic Fine–Wilf question 30001552 has different hypotheses; its reflection argument is not applied to this morphic question. Record30001553 asks for the broader sharp relation; no separate prior campaign attempt was found. Source-family ratios approach3 from below and do not refute this conjecture.

Primary literature checked:
- Kari–Mahalingam, *Involutively bordered words*, IJFCS18(2007),1089–1106, definitions and border structure: https://www.csd.uwo.ca/~lkari/invbor.pdf
- Kari–Kulkarni, *Disjunctivity and other properties of sets of pseudo-bordered words*, Acta Informatica(2017), author version: https://cs.uwaterloo.ca/~lila/pdfs/ai_disjunctivity_5.pdf . Its language and concatenation results, including the border-count bound in Proposition12, do not resolve the stated extremal threshold
- Holub–Nowotka, *The Ehrenfeucht–Silberger problem*, author version: https://oceanrep.geomar.de/20295/1/TheEhrSilProblem.pdf . The credited ordinary-word theorem gives n>7(tau−1)/3 implies tau=pi

The catalog's thesis link identifies Bastian Bischoff, *Wortbegrenzung unter Involution*, Diplomarbeit3095, completed18November2010. It is contemporaneous with the report, not a modern resolution. Its official PDF returned HTTP502 during this audit and its full contents were not read. Search-result indexing was used only to identify that bibliographic limitation. No exhaustive worldwide novelty or unresolved-status claim is made.
