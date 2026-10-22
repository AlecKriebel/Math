from pathlib import Path
OWN=Path(__file__).resolve().parent
for name in ['test_operations_proposal.py','test_source_gate_proposal.py']:
 p=OWN/name;s=p.read_text();s=s.replace("p.add_argument('--core-sha256',required=True);a=p.parse_args()", "p.add_argument('--core-sha256',required=True);p.add_argument('--installed',action='store_true');a=p.parse_args();CORE=P/'accept_pr952.py' if a.installed else CORE")
 s=s.replace("'outer_optimization':sys.flags.optimize", "'outer_optimization':sys.flags.optimize,'installed_actual_source_executed':a.installed")
 s=s.replace("'optimization':sys.flags.optimize", "'optimization':sys.flags.optimize,'installed_actual_source_executed':a.installed")
 p.write_text(s)
p=OWN/'build_log_tests.py';s=p.read_text();pos=s.index("s=s.replace(\"EVENTS=[];")
s=s[:pos]+'''s=s.replace("p.add_argument('--proposal-sha256',required=True);a=p.parse_args();base=", "p.add_argument('--proposal-sha256',required=True);p.add_argument('--installed',action='store_true');a=p.parse_args();base=")
s=s.replace("proposal=(OWN/'PROPOSED_accept_pr952.py').read_bytes()", "proposal_copy=(OWN/'PROPOSED_accept_pr952.py').read_bytes();proposal=CORE.read_bytes() if a.installed else proposal_copy;need(proposal==proposal_copy,'installed/proposal exact source bytes')")
s=s.replace("sha(CORE.read_bytes())==BASE_SHA", "sha(CORE.read_bytes())==(a.proposal_sha256 if a.installed else BASE_SHA)")
s=s.replace("'current_adapter_state_inventory_workflow_edits':0", "'current_adapter_state_inventory_workflow_edits':0,'installed_actual_source_executed':a.installed")
''' +s[pos:]
s=s.replace("filename=OWN/('BASE_accept_pr952.py' if sha(body)==BASE_SHA else 'HISTORICAL_PROPOSAL04_LOG_GAP_accept_pr952.py' if body==historical else 'PROPOSED_accept_pr952.py')", "filename=CORE if a.installed and body==proposal else OWN/('BASE_accept_pr952.py' if sha(body)==BASE_SHA else 'HISTORICAL_PROPOSAL04_LOG_GAP_accept_pr952.py' if body==historical else 'PROPOSED_accept_pr952.py')")
p.write_text(s)
p=OWN/'run_revision_tests.py';s=p.read_text().replace("p.add_argument('--stem',required=True);", "p.add_argument('--stem',required=True);p.add_argument('--installed',action='store_true');p.add_argument('--proposal-sha256');")
s=s.replace("pin=sha(proposal)", "pin=sha(proposal);need(a.proposal_sha256 is None or a.proposal_sha256==pin,'external requested proposal pin')")
s=s.replace("=='888a068e26e0adcc3f493817ef46c46b6bdd5a4f848a4d907e4f4af2b5f592a8'", "==(pin if a.installed else '888a068e26e0adcc3f493817ef46c46b6bdd5a4f848a4d907e4f4af2b5f592a8')")
s=s.replace("str(OWN/script),arg,pin]", "str(OWN/script),arg,pin,*(['--installed'] if a.installed else [])]")
s=s.replace("'installed':False", "'installed':a.installed")
p.write_text(s)
