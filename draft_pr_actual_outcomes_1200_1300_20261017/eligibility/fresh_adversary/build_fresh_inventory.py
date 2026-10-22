"""Fresh outcome-language gate. No proof, literature, or live PR operations."""
import collections
import hashlib
import json
import pathlib
import re
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = pathlib.Path(__file__).resolve().parent
metadata_bytes = (ROOT / 'PR_OUTCOME_METADATA.json').read_bytes()
metadata = json.loads(metadata_bytes)['data']['repository']

# Anchors were selected by reading every PR's substantive body and the captured
# acceptance/README outcome declarations. A generic priority disclaimer is never
# an exclusion. These anchors are matched against the original body, preserving
# its exact whitespace in the recorded quotation.
ANCHORS = {
1200: 'The unrestricted same-partition target remains unresolved by this work.',
1201: 'the family k=4,r>=2 is unresolved by these audited results.',
1202: 'The unrestricted Chung–Ross target remains unresolved by this work.',
1203: 'The general Schubert-support left-weak convexity conjecture remains unresolved by this work.',
1204: 'The general nonnormal conjecture remains unresolved by this work.',
1205: 'The original OWR2021 canonical-W exponent converse is false.',
1206: 'The original graph-coloring conjecture remains unresolved by this work.',
1207: 'Accepted correction to a published arrangement theorem',
1208: 'The full local recurrence remains unresolved by this work.',
1209: 'The original infinite four-total-shift question remains unresolved.',
1210: 'This is an internal AI audit of existing attributed arguments, not our new solution',
1211: "This disproves Kohl's stated universal tree-equality conjecture under its original arbitrary-list quantifiers.",
1212: 'Both full source questions remain unresolved by this work.',
1213: 'The uniform O((log A)^2) target remains unresolved.',
1214: 'Both general targets remain unresolved here.',
1215: 'The unrestricted determinant-approximation target remains unresolved by this work.',
1216: 'The complete analytic counterexample already uses p(z)=z.',
1217: "Alper Ferudun's version 1.1, dated September 30, 2026, proves the exact Propp-Kenyon target",
1218: 'The full original subexponential-in-d question is unresolved by this work.',
1219: 'The result belongs to Gökalp Alpan and Maxim Zinchenko',
1220: 'No new compact arbitrary-order formula or complete resolution of the open-ended AIM problem is accepted.',
1221: 'The original existential question remains unresolved by this work.',
1222: 'The theorem is credited to the inspected September manuscript by Shisheng Li',
1223: 'The general arbitrary-partition, arbitrary-dimensional bounded-interval classification remains unresolved.',
1224: 'General harmonic rigidity is not accepted from the inspected February 25 proof',
1225: 'Accepted full precise theorem',
1226: 'The original estimation problem is not declared fully solved.',
1227: 'Whether the game length is linear or sublinear remains unresolved by this work.',
1228: 'The existing Price/GPT-5.5 Pro disproof gives',
1229: 'It is partial research, not a solution: the universally forced threshold remains 3 or 4.',
1230: 'This is an exact prior result covered by Arakawa, van Ekeren and Moreau',
1231: 'Credit the prior construction and arguments to',
1232: 'No unqualified original resolution, novelty, perfect correctness/privacy, insider robustness, infinite-domain uniform group or general polynomial-size encoding claim.',
1233: 'No novelty or unqualified original-formulation resolution is claimed.',
1234: 'The unrestricted arbitrary-prime problem remains unresolved',
1235: 'No standalone verdict is given on an affine convex-hull triangulation interpretation; these notions must not be conflated.',
1236: 'Arbitrary complete local extensions and the general real-analytic no-tangency conjecture remain unresolved by this work.',
1237: 'Acceptance is confined to the computable-bound interpretation as a consequence of prior results.',
1238: 'The optimum 2 versus 3 remains unresolved.',
1239: 'No efficient algorithm, broader structural classification, novelty, priority, current worldwide openness, all-dimensional minimality, or unqualified resolution of the original qualitative workshop question is claimed.',
1240: 'The original problem remains PARTIAL: useful recoupling theory is still required.',
1241: 'for every fixed g >= 2 and k >= 3, pseudo-Anosov log-dilatation multiplicity in I_g(k) is unbounded when counted up to ambient orientation-preserving Mod_g-conjugacy.',
1242: 'This is not a full-target solution',
1243: 'Both original inner and outer two-rational-caustic existence questions remain UNRESOLVED.',
1244: 'The separate arithmetic zigzag question remains unresolved by this audit.',
1245: 'Only the complex smoothness component receives full acceptance.',
1246: 'No full-target solution, sharp constant, novelty, priority, or exhaustive current-openness claim is made.',
1247: 'The original quantum-comparison question remains UNRESOLVED',
1248: 'The arbitrary-n problem remains PARTIAL',
1249: 'The general conjecture is unresolved by this work.',
1250: 'The unrestricted conjecture remains unresolved in this investigation.',
1251: 'The universal triangle conjecture remains unresolved by this work',
1252: 'General complete-host 3–1–0 recognition remains unresolved by this work.',
1253: 'equality in the connected closed three-manifold lower bound is covered by the established results of Bagchi and Datta–Murai',
1254: 'The all-knots full-signature approximation question remains unresolved by this work.',
1255: 'The exact all-n ML, dual-ML and SSL degree recurrences and bundled original target remain unresolved.',
1256: 'Original all-n target unresolved by this work.',
1257: 'The historical question’s intended category and worldwide novelty remain unresolved.',
1258: 'No novelty, priority, new restriction theorem or whole-paper acceptance is claimed.',
1259: 'This is a complete alternative proof of a previously announced result',
1260: 'Prior negative resolution and attribution',
1261: 'satisfies 0 <= H_r - min_K f <= C_{K,f}/r^2 for every integer r >= 1.',
1262: 'This is a credited consequence of Sah–Sawhney\'s quantitative LLT',
1263: "Alper Ferudun's prior negative answer to Heinig's spanning near-square question",
1264: "Eremenko's original Problem 2 remains UNRESOLVED.",
1265: "Theorem 1.2, proves the prior range `1 < s <= 2`, including inverse-square repulsion.",
1266: 'The sharp coefficient −1/2 remains unresolved.',
1267: 'The partition theorem is credited to Ulrich Görtz',
1268: 'The accepted mathematical outcome is a complete negative counterexample in the source scope described above.',
1269: 'The broader classification remains unresolved.',
1270: 'are credited for the disproof and primitive family',
1271: "This draft records a literature-derived negative resolution of problem 30003042 / OWR-14213-008: Karpenko's gamma-filtration nonmembership conjecture fails at n = 8.",
1272: 'This packet reconstructs the established rational-density naturality argument',
1273: 'This is an authored exposition and analytic audit of their existing result',
1274: 'Adds a self-contained negative answer to Hayman–Lingham Problem 7.72',
1275: 'The counterexample is credited to Ho.',
1276: "This is a checked rederivation of Alper Ferudun's prior interval/square construction",
1277: 'Prior published disproof',
1278: 'This is not a full resolution of Erdős Problem 1110',
1279: 'a known positive resolution due to Robert Šámal',
1280: 'every finite abelian diagonal quasi-free action is strongly approximately inner.',
1281: 'fundamental-group dichotomy was already stated by',
1282: 'The original problem remains unresolved.',
1283: 'Complete existence classification for Problem 30005434',
1284: 'The criterion is sufficient, not necessary, and does not give a full combinatorial classification.',
1285: 'No novelty, arbitrary-rank obstruction, all-degree obstruction, or resolution of the full original question is claimed.',
1286: 'The construction is established prior literature',
1287: 'Theorem 1.9, already states this result.',
1288: 'The unrestricted AIM problem is not declared solved.',
1289: 'It does not independently audit the full 56-page geometric proof or its prerequisites, establish all-characteristic closure, or extend the result to bad primes.',
1290: 'This does not settle all of Ollivier’s Problem E',
1291: 'This result does not resolve other unspecified interpretations or the unrestricted-dimensional problem.',
1292: 'This negative phenomenon is prior work of Santosh Ghimire',
1293: 'not a resolution of the unrestricted source problem.',
1294: 'The construction is credited to Alper Ferudun',
1295: 'verify the counterexample already given in Rabinoff\'s contribution',
1296: 'The theorem and construction are attributed to Alper Ferudun',
1297: 'This does not resolve the intended absolutely-simple conjecture.',
1298: 'No result in other dimensions, current general-problem status, or novelty is claimed.',
1299: 'not an unconditional refutation of the historical conjecture',
1300: 'This does not prove or refute the intended corrected higher-dimensional conjecture',
}

ADMIT = {1205,1211,1216,1225,1241,1261,1268,1271,1274,1280,1283}
# Explicit prior-result descriptions can coexist with an unresolved residual;
# these are all exclusions, never assertions that the whole target was solved.
PRIOR = {1201,1207,1210,1217,1219,1220,1222,1226,1227,1228,
         1230,1231,1232,1233,1236,1237,1244,1245,1246,1247,
         1253,1258,1259,1260,1263,1265,1267,1270,1272,1273,
         1275,1276,1277,1279,1281,1286,1287,1289,1292,1294,1295,1296}

def exact_match(text, needle):
    regex = r'\s+'.join(re.escape(part) for part in needle.split())
    m = re.search(regex, text)
    if not m:
        raise ValueError(f'Quotation does not match: {needle!r}')
    return m.group()

def source_dir(n):
    return ROOT / 'eligibility' / ('review_1200_1250/pr_'+str(n) if n<=1250 else 'review_1251_1300/'+str(n))

artifacts = []
records = []
for n in range(1200,1301):
    x = metadata[f'p{n}']
    d = source_dir(n)
    body = x['body']
    quote = exact_match(body, ANCHORS[n])
    if n in ADMIT:
        disposition = 'admit_explicit_full_original_target_claim'
        reason = 'Explicit full original-target theorem or counterexample claim; generic novelty disclaimers do not exclude it. Truth and priority remain for later audit.'
    elif n == 1262:
        disposition = 'recommend_admit_pending_parent_adjudication'
        reason = 'Acceptance explicitly declares original_target_resolved_by_argument=true. Prior credit identifies an imported LLT, while the present sharp modular reduction and necessity are separately described. Credited ingredients alone are insufficient to exclude it.'
    elif n == 1235:
        disposition = 'defer_no_explicit_full_original_scope_resolution'
        reason = 'Accepted integral-point counterexamples rule out a conical cover, but the recorded outcome explicitly withholds an affine-convex-hull triangulation verdict. No unambiguous full original-target claim is recorded; do not infer or investigate scope in an excluded record.'
    elif n in PRIOR:
        disposition = 'skip_explicit_prior_or_scoped_prior_outcome'
        reason = 'Recorded outcome is expressly credited prior-result reconstruction/coverage, sometimes with unresolved original-target components. This does not assert all parts of a bundled problem were previously solved.'
    else:
        disposition = 'skip_incomplete_restricted_or_conditional_original_target'
        reason = 'The recorded outcome does not claim a complete original-target resolution; its stated restriction, condition, unresolved residual, or interpretation caveat is decisive.'
    if n == 1289:
        reason = 'The rank-one non-character theorem is called a standard example. More decisively, captured README states the original geometric answer is already announced in the OWR contribution and given by Achar–Sobaje; no full general geometric proof or all-characteristic closure is claimed. Doty–Henke/Martin ingredient credit alone is not used for exclusion.'
    evidence = [{
        'source': 'PR_OUTCOME_METADATA.json:/data/repository/p'+str(n)+'/body',
        'exact_snippet': quote,
    }]
    if n == 1262:
        evidence.extend([
            {'source': str((d/'ACCEPTANCE.json').relative_to(ROOT)), 'json_pointer': '/original_target_resolved_by_argument', 'value': True},
            {'source': str((d/'ACCEPTANCE.json').relative_to(ROOT)), 'json_pointer': '/prior_credit/status', 'value': 'CREDITED_COROLLARY_OF_PRIOR_QUANTITATIVE_LLT'},
            {'source': str((d/'README.md').relative_to(ROOT)), 'exact_snippet': exact_match((d/'README.md').read_text(), 'The present reduction uses concentration and finite central-window summation for sufficiency and an independently derived CLT/Fourier obstruction for necessity.')},
        ])
    if n == 1235:
        evidence.append({'source': str((d/'ACCEPTANCE.json').relative_to(ROOT)), 'json_pointer': '/affine_convex_hull_triangulation_verdict', 'value': 'NOT_ESTABLISHED'})
    if n == 1289:
        evidence.append({'source': str((d/'README.md').relative_to(ROOT)), 'exact_snippet': exact_match((d/'README.md').read_text(), 'asks Question 1 on printed p. 1275 and announces a geometric answer on p. 1276, later in the same contribution.')})
    file_captures = []
    for f in sorted(d.iterdir()):
        if f.name.endswith(('.receipt.json','.github.json')):
            receipt = json.loads(f.read_text())
            raw_name = re.sub(r'\.(?:receipt|github)\.json$', '', f.name)
            raw = d / raw_name
            if not raw.exists():
                continue
            b = raw.read_bytes()
            blob = hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
            expected_blob = receipt.get('sha', receipt.get('github_blob_sha'))
            if expected_blob is not None:
                assert expected_blob == blob, (n, raw.name, expected_blob, blob)
            if 'sha256' in receipt:
                assert receipt['sha256'] == hashlib.sha256(b).hexdigest()
            if 'size' in receipt:
                assert receipt['size'] == len(b)
            a = {'capture': str(raw.relative_to(ROOT)), 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest(), 'git_blob_sha1': blob, 'receipt': str(f.relative_to(ROOT))}
            file_captures.append(a)
            artifacts.append(a)
    assert file_captures, n
    records.append({
        'pr': n, 'title': x['title'], 'url': x.get('url',f'https://github.com/AlecKriebel/Math/pull/{n}'),
        'head_oid': x.get('headRefOid'),
        'disposition': disposition, 'eligible_recommendation': n in ADMIT or n==1262,
        'reason': reason, 'evidence': evidence,
        'body_sha256': hashlib.sha256(body.encode()).hexdigest(),
        'captured_outcome_files': file_captures,
        'proof_audit_or_priority_research_performed': False,
    })

assert len(records)==101 and {x['pr'] for x in records}==set(range(1200,1301))
counts = dict(collections.Counter(x['disposition'] for x in records))
report = {
    'schema': 'fresh-adversarial-actual-outcome-eligibility-v1',
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'scope': 'PR #1200–#1300 inclusive, actual recorded outcomes; stale QUEUE not used',
    'method': 'Read substantive PR body outcome/claim/limitation sections for all 101 records, cross-check immutable captured acceptance and README/RESULT outcome declarations; exact identity blocks were not used as semantic evidence. No proof correctness review or scholarly retrieval was performed for any excluded PR.',
    'metadata_sha256': hashlib.sha256(metadata_bytes).hexdigest(),
    'counts': counts,
    'uncontroversial_admitted_prs': sorted(ADMIT),
    'recommended_additional_admission': [1262],
    'recommended_all_admitted_prs': sorted(ADMIT|{1262}),
    'parent_adjudication_required': [1262],
    'scope_unresolved_not_admitted': [1235],
    'independence_limit': 'Parent supplied earlier 11-PR candidate set and two borderline cases. Every body was then independently examined. Previous inventory was read for comparison only after substantive outcome review; no previous classification was treated as evidence of the result.',
    'checkpoint': {'eligibility_audit_percent': 100, 'mathematical_publication_work_percent': 0},
    'capture_identity_check_count': len(artifacts),
    'records': records,
}
(OUT/'FRESH_ALL_101_DISPOSITIONS.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
(OUT/'CAPTURE_IDENTITY_CHECKS.json').write_text(json.dumps(artifacts,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['counts','uncontroversial_admitted_prs','recommended_additional_admission','capture_identity_check_count']},indent=2))
