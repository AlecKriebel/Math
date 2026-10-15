# Exact domains and provenance

Let H be the 41,253-entry baseline and S the one literal live-control path. Let P be the 97-path checkpoint domain, and F={x in H: x.path ends with /SHARED_GIT_WINDOW_STATUS.json}. Complete baseline parsing proves S is not in H, H intersects P in no path, |F|=19 and bytes(F)=10,288. Thus literal exclusion H minus ({S} union P) equals H, whereas reviewer06's suffix exclusion is H minus F.

The arithmetic is exact: 41,253-19=41,234 and 1,273,600,002-10,288=1,273,589,714. The 19 entries are enumerated with original byte/hash/mode pins in RESULTS.json; no fixture is treated as the live control. This explains the repeated byte figure while falsifying the inherited 41,252-file interpretation.

Reviewer06's executed source archive contains the suffix predicate; its actual result JSON and full native stdout agree on the reduced quantities. Reviewer08's executed archive contains literal exclusions; its actual saved JSON equals the entire parsed native stdout and records 41,253/all bytes/excluded0. The wrong report and read-scope constants do not describe a missing execution-time body check in reviewer08.

Authenticated ROOT metadata and checkpoint sources use literal equality and full-body/mode comparisons. The accepted actual041 validator source is the exact 14,902-byte source41d07aef...; its record584228/7e4c4cbf... reports the full domain and successful actual checkpoint. Since neither literal exclusion applies, its body checks include every F entry. This uses the already completed accepted validation and does not reconstruct, rerun or invent an omitted reviewer06 check.

Scope is count/provenance correction only. Full baseline metadata, executed source predicates, complete relevant result JSON and native output envelopes were authenticated; the 1,273,600,002 held-file bytes and all 844 checkpoint native streams were not newly read or rerun. The earlier closed artifacts remain preserved and the new failed reader is retained. Current maps/logs may refer additively to this correction; no scientific result or publication action is reopened.
