# Research log

## 2026-07-27 21:40--22:15 PDT

- Read the accepted C-079, C-082, and C-083 notes and reconstructed the
  exact old complement and response lists without treating a missing
  family response as a graph nonedge.
- Proved the positive-tail neighborhood-independence lemma: once
  \(p\in P_a\) and \(pq\in E(H)\), the \(a\)-omitting part of
  \(N_H(q)\) is independent in \(H\).
- Applied this at the full vertex \(x\), using the old positive tail
  \(r-x\), to show that every link neighbor of the first escape \(w\)
  is \(a\)-positive.
- Classified every outside common neighbor of the first cap and escape.
  The forced five-vertex complement is exactly two triangles sharing the
  escape vertex.  This bow-tie has no \(K_4\), no forced dominating pair,
  and no forced odd fan.
- Identified the safe old return: when the link-positive vertex is \(r\),
  returning to \(v_0\) gives C-079, while returning to \(v_1\) reuses the
  same cap over the even path \(v_0-v_1-w\).
- Classified common anchor neighbors of the cap and escape.  At most one
  can occur, and its occurrence forces the escape to have the singleton
  response list consisting of the other non-\(a\) anchor.

## 2026-07-27 22:15--22:30 PDT

- Coupled the exact geometry to the second omitted color \(c\).
- Proved by a literal attack chain that no vertex can be adjacent in the
  complement to all three of \(r,s,q\).  The proof starts from
  \(S-a+x\), forces \(\{x,v_0,v_1\}\), and defeats every response to an
  attack at \(s\).
- Concluded that the \(c\)-caps on \(rs\) and \(sq\) are distinct and lie
  on opposite sides of the missing cross adjacency: every first cap sees
  \(q\) in \(G\), and every second cap sees \(r\) in \(G\).
- Checked exact distinctness from the previously forced \(a\)-cap and
  \(a\)-escape.  This gives the exact-list order floor \(n\ge13\).
- Applied \(\gamma=3\) to the full vertex and the \(sq\)-cap.  Its escape
  is either the old \(a\)-escape \(w\), forcing \(L(w)=\{b\}\), or a fifth
  new vertex, giving \(n\ge14\).

## 2026-07-27 22:30--22:40 PDT

- Constructed and independently checked the gamma-two safe-return control
  `JFzvvn{~fM?`.
- Defined its family deterministically as the greatest safe kernel after
  banning the direct swaps outside the prescribed lists.
- Verified 109 retained states, deletion rounds \(20,4,5,5,2\), all 872
  unoccupied-attack obligations, exact response lists, no complement
  \(K_4\), no C-079 embedding, and parameters
  \((2,3,3,3)\).
- Wrote the self-contained proof note, verifier, and pinned JSON result.
- Exact replay:

  ```text
  python3 math/working/separated_port_two_color_ladder/verify.py \
    > /tmp/separated_port_two_color_ladder_result.json
  cmp /tmp/separated_port_two_color_ladder_result.json \
    math/working/separated_port_two_color_ladder/result.json
  shasum -a 256 \
    math/working/separated_port_two_color_ladder/verify.py \
    math/working/separated_port_two_color_ladder/result.json
  ```

- Pinned hashes:

  ```text
  a2f5a63f15f6c2808cd190b83fcc07b172eddcca385b679c0cbf92eacb4fb059  verify.py
  4faceb740ee28d22db17c8544e21b80e6720a858f637df996250c7859169a1e0  result.json
  34ad69cf11195558c2743fcb6332c2d4cef0750f7eb95be715aa892fd9733eb6  sorted 109-state family
  ```

- No claims registry, state file, README, or public page was edited.
