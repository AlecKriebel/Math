# Source-only baseline, sealed before candidate access

UTC: 2026-10-03 14:55 UTC. Completion estimate: 8%.

Fresh access: independently opened https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf with web tool; read original Section 3 including printed pages 125–126 (zero-based PDF pages131–132) and Auroux printed131 (PDF137 zero-based). No candidate prose, code, artifacts, or earlier reviewer reports read. Directory inventory of shared primary files only.

Wajnryb fixes quotient Q=A_5 / <<(a1a2a3a4)^5 = a5a4a3a2a1^2a2a3a4a5>>. Exact input alphabet consists of the five standard positive generators. Target is (a1a2a3a4)^10, also named Delta_4^4. He asks both whether every positive word equal to this target has length40,30,20, and whether every such tuple is Hurwitz equivalent to respectively Delta_4^4, Delta_5^2=(a1a2a3a4a5)^6, or h^2 where h=a5a4a3a2a1^2a2a3a4a5. The original is an unrestricted question for all fixed-alphabet positive words equal in Q, not a bounded sample.

Auroux defines Hurwitz moves on factor tuples as (...,u,v,...) -> (...,uvu^-1,u,...), allowing inverses. Global simultaneous conjugation is an additional equivalence relation, not included in the basic definition. Length is preserved by Hurwitz. A complete answer should distinguish strict Hurwitz from its extension by global conjugation and specify whether equality is in the presented quotient or a possibly weaker mapping class image.

Independent necessary success criteria: exact quotient identification or a provably faithful relevant model; independent finite upper bound; a complete equality detector or a safe rejection test plus constructive proof for every survivor; completeness of all positive generator words up to that bound; strict orbit classification and proof that orbit classes differ; account for known full-surface length and presentation results without implying new priority. General arbitrary Dehn-twist factorizations are outside fixed alphabet but any excluded length claim needs an explicit domain. All computational state/edge data must be independently regenerated and compared in full, not accepted by hashes.

Potential obstruction before reading candidate: quotient relator alone erases length modulo10 (20=10), so gives only residue obstruction, not boundedness. A surface image alone can safely reject equality but cannot safely accept it without faithfulness or constructive quotient proof. A DAG over paths needs all outgoing transitions and full equality state records, not just endpoint sampling.
