#!/usr/bin/env python3
import pathlib, hashlib, json, datetime

B = pathlib.Path(__file__).resolve().parent
old = B / 'attributed_prior_result_preparation_20261004'
new = B / 'attributed_prior_result_preparation_v2_20261004'
new.mkdir(exist_ok=False)
names = ['CURRENT_RESULT.md', 'CURRENT_PRIORITY_SPECIALIZATION.md', 'PR_BODY.md', 'DISPOSITION_PROPOSAL.json']
before = {n: hashlib.sha256((old / n).read_bytes()).hexdigest() for n in names}
expected = dict(zip(names, ['b5bc4eded149aad619162703d04b09786ffa03aa15ff5811e317147a8cdb5120', '6b22354490a357005f0956a30b632d33a2391c113d01bd92aa59a6cf728d7ace', '1f451d9edd70ebd4e1706f86f08c880acb01fe1f56d7170c9d2ce7ee10838f95', '65a90ece120697a09edae6cb8dd10034aac97723acddb874db3a21c6f27086f5']))
assert before == expected
result = (old / names[0]).read_text().replace(
    'A new tournament proof\nand the even estimate remain mathematically valid; novelty of those additions\nhas not been established.',
    'The alternate tournament proof remains mathematically valid; novelty of its\nmechanism has not been established. The even estimate also follows from earlier\ningredients: Fiedler–Stoimenow formula (1) and the classical even-valence lemma\n(see the checked deduction in `CURRENT_PRIORITY_SPECIALIZATION.md`). An earlier\nexplicit printing of the exact even formula has not been located.')
priority = (old / names[1]).read_text().replace(
    "The candidate's even estimate and distinct tournament mechanism are verified\nmathematics, but their novelty remains unestablished.",
    "The candidate's distinct tournament mechanism is verified mathematics, but\nits novelty remains unestablished. Its even estimate has a separate checked\ncorollary from older ingredients, as follows.\n\nLet m be the number of intersecting chord pairs. The same Fiedler–Stoimenow\nformula (1), with at most one unit contribution per unordered triple and at\nmost one unit contribution per linked pair, gives\n\\(4|v_3|\\le {n\\choose3}+m\\). Stoimenow, *Positive Knots, Closed Braids and\nthe Jones Polynomial* (2003), printed page 245, Lemma 3.2 (even valence),\nstates that each chord of a classical Gauss diagram intersects an even number\nof other chords; its short proof invokes the Jordan curve theorem. The lemma\nhas no positivity or reducedness hypothesis (those occur in the separate\nfollowing Lemma 3.3). For even n≥2, every such degree is at most n−2, so\n\\(m\\le n(n-2)/2\\). Consequently\n\n\\[\n|v_3|\\le\\tfrac14\\left({n\\choose3}+\\tfrac{n(n-2)}2\\right)\n= n(n^2-4)/24.\n\\]\n\nThe case n=0 is zero directly. Thus the candidate's even estimate follows\nfrom earlier published ingredients as well. This is a checked corollary; an\nearlier explicit printing of the exact even formula has not been located.\nIt does not use the stronger, uncertified page-8 extremality assertion.\n[Stoimenow 2003 primary source](https://numdam.org/item/ASNSP_2003_5_2_2_237_0.pdf).")
body = (old / names[2]).read_text().replace(
    'Novelty of the alternate tournament\nproof and even estimate remains unestablished.',
    'Novelty of the alternate tournament\nmechanism remains unestablished. The even estimate also follows from older\ningredients: the same prior formula and Stoimenow’s 2003 classical even-valence\nlemma, giving linked-pair count at most n(n−2)/2 for even n. An earlier explicitly\nprinted exact even formula has not been located.\n[Even-valence source, Lemma 3.2, p.245](https://numdam.org/item/ASNSP_2003_5_2_2_237_0.pdf).')
assert result != (old / names[0]).read_text()
assert priority != (old / names[1]).read_text()
assert body != (old / names[2]).read_text()
proposal = json.loads((old / names[3]).read_text())
proposal.update(even_refinement_prior_ingredient_corollary_verified=True,
                earlier_explicit_even_formula_located=False,
                distinct_tournament_mechanism_novelty_established=False)
for n, text in zip(names, [result, priority, body, json.dumps(proposal, indent=2) + '\n']):
    (new / n).write_text(text)
rows = [{'name': n, 'bytes': (new/n).stat().st_size, 'sha256': hashlib.sha256((new/n).read_bytes()).hexdigest()} for n in names]
record = {'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'stage': 'PROSPECTIVE_REVIEW_PACKET_NOT_NATIVE_ACCEPTANCE',
          'immutable_original_head': '78f4a7fadac0fd24e147a617956cb409eb6a579e',
          'previous_packet_directory': str(old), 'previous_packet_pins_unchanged': before,
          'changes': 'Only additive checked attribution for even refinement from earlier ingredients; no candidate change, native acceptance, merge or publication',
          'files': rows, 'fresh_adversarial_review_pending': True}
(new/'MANIFEST.json').write_text(json.dumps(record, indent=2) + '\n')
assert {n: hashlib.sha256((old/n).read_bytes()).hexdigest() for n in names} == before
print(json.dumps(record, indent=2))
