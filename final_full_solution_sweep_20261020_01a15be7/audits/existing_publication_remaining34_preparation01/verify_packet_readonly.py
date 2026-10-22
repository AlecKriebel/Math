"""Caller-pinned complete preparation verification; no service, actor, CASE or writes."""
from pathlib import Path
import argparse,json,gzip,hashlib,types,stat,os
O=Path(__file__).resolve().parent;D=O.parent/'existing_publication_remaining_rows_inventory01'
SOURCE_SHA='4d896dea9f3998297e3493915dab2864d0a16f68a4ad3a6aeb1e83be344265d0'
def sha(b):return hashlib.sha256(b).hexdigest()
def gz(path):return json.loads(gzip.decompress(path.read_bytes()))
def module(path,name):
 ns={'__file__':str(path),'__name__':name};exec(compile(path.read_bytes(),str(path),'exec',optimize=0),ns);return ns

def replay():
 adoption=O.parent/'ROOT_REMAINING_EXISTING_ROWS_DATED_INVENTORY_ADOPTION.json';assert sha(adoption.read_bytes())=='945892b3a0c5d0af81a81a78bc3255234d9b05c9642c6d3f105065e204b6b339'
 old=module(D/'verify_closed_preparation.py','_old_readonly_closure');old['verify'](D,'11c3a6b59f16f8d2a1d87af3151325f30ca3824a77548b7c5ca15521a4107b4d')
 boot=module(O/'source/bootstrap.py','_inert_source_bootstrap');mods,verify=boot['load_verified'](SOURCE_SHA);verify();C=mods['ops_core'];P=mods['protocol'];assert P.PRODUCTION_ADAPTER_INCLUDED is False
 plan=json.loads((O/'PROPOSAL.json').read_bytes());P.validate(plan);frozen={i['pr']:i for i in json.loads((D/'FROZEN_PROPOSALS.json').read_bytes())['items']};items={i['pr']:i for i in plan['items']};assert len(items)==34 and sum(len(i['associated_prs'])for i in items.values())==35
 revision=json.loads((O/'PR1263_EXPLICIT_MINIMAL_LITERAL_REVISION.json').read_bytes());assert sha((O/'PR1263_EXPLICIT_MINIMAL_LITERAL_REVISION.json').read_bytes())=='8f9847f6c7dad5383d115570990d3842de05b6931cb383e166de8196e54c2d1b';assert revision['root_literal_revision_adopted']is False and revision['fresh_independent_literal_revision_accepted']is False
 for pr,item in items.items():
  assert C.typed_equal(item['original_root_adopted_row'],frozen[pr]['row'])
  if pr!=1263:assert C.typed_equal(item['row'],frozen[pr]['row'])
  else:
   r=list(frozen[pr]['row']);assert r[3].count(revision['exact_replacement']['old'])==1;r[3]=r[3].replace(revision['exact_replacement']['old'],revision['exact_replacement']['new']);assert C.typed_equal(r,item['row'])and C.typed_equal(r,revision['proposed_four_cells'])
  assert sha(C.canonical(item['row']))==item['row_sha256']
 semantic,original=mods['custody'].semantic_baseline(O);comp=json.loads((O/'SEMANTIC_LOSSLESS_COMPACTION_RECEIPT.json').read_bytes());assert sha(original)==comp['original_file_sha256'];failed=mods['custody'].failed_semantic_original(O);oldfailure=json.loads((O/'FAILED_BUILD01_EXACT_CUSTODY.json').read_bytes());assert sha(failed)==next(x['sha256']for x in oldfailure['files']if x['original_path']=='private/SEMANTIC_DECISIONS.json.gz')
 for x in oldfailure['files']:
  if'exact_recoverable_capture'in x:
   b=gzip.decompress((O/x['exact_recoverable_capture']).read_bytes());assert len(b)==x['bytes']and sha(b)==x['sha256']
 assert len(semantic['decisions'])==2341 and len(semantic['intrabatch'])==1122 and semantic['blanket_author_waivers']is False
 cf=gz(O/'private/CF_TYPED_MATCHER_SEMANTICS02.json.gz');assert len(cf['decisions'])==3127 and cf['unread_new_carriers']==[]and cf['all_pairs_considered']==24752
 idx=gz(O/'private/FULL_CARRIER_REFERENCE_INDEX.json.gz')['carriers'];assert len(idx)==728
 known={(x['pr'],x['carrier_index']):x for x in cf['decisions']};assert len(known)==3127
 base={x['key']:x['full_carrier']for x in gz(D/'private/closing_FULL_CARRIERS.json.gz')};owned=gz(D/'private/terminal_owned_complete_pass1.json.gz')['records'];local=gz(D/'private/terminal_LOCAL_SCIENTIFIC_CARRIERS.json.gz')['items'];numeric=gz(O/'private/numeric_complete.json.gz');assert len(numeric['values'])==237
 observed=set()
 for i,c in enumerate(idx):
  src=c['source'];body=owned[src['records_key']]if'records_key'in src else local[src['items_index']]if'items_index'in src else numeric['values'][236]if c['key']=='sheet:237'else base[c['key']];digest=sha(C.canonical(body));assert digest==c['body_sha256']
  for item in plan['items']:
   hits=mods['identity_gate'].matched(body,item)
   if not hits:continue
   key=(item['pr'],i);d=known[key];assert d['body_sha256']==digest and C.typed_equal(d['matched'],hits)and d['target_four_cells_sha256']==item['row_sha256']and bool(d['scientific_reason'])and d['scope_witness']is not None;assert not d['classification'].startswith('HOLD');observed.add(key)
 assert observed==set(known)
 pairs={(d['pr'],d['other_pr'])for d in semantic['intrabatch']};assert pairs=={(a,b)for a in items for b in items if a!=b}
 expectations=module(O/'audit_control_expectations.py','_readonly_control_expectations');controls=json.loads((O/'CONTROL_RESULTS05.json').read_bytes());expectations['validate'](controls);assert controls['actual_source_hash']==SOURCE_SHA and controls['all_passed']is True and controls['world_count']==40
 audit=json.loads((O/'ACTIVE_CONTROL_EXPECTATION_AUDIT.json').read_bytes());assert all(x['rejected']is True for x in audit['hash_consistent_false_expected_output_controls'])and audit['wrong_caller_source_manifest_pin_actively_rejected']is True
 custody=module(O/'verify_custody_physical_readonly.py','_readonly_custody');status=custody['verify'](False);assert status['custody_inventories']==129
 physical=json.loads((O/'PHYSICAL_CUSTODY_REPLAY_RESULTS.json').read_bytes());assert len(physical['physical_replay'])==129 and physical['physical_replay_requested']is True and all(x['full_zero_namespace_and_directory_metadata_exact']is True for x in physical['physical_replay'])
 closing=json.loads((O/'CLOSING_NUMERIC_DATED_OBSERVATION.json').read_bytes());b=gzip.decompress((O/closing['complete_observation']['path']).read_bytes());assert sha(b)==closing['complete_observation']['raw_sha256'];last=json.loads(b);assert len(last['values'])==closing['rows']==238 and C.typed_equal(last['values'][:237],numeric['values'])
 for p in closing['fresh_raw']:
  b=gzip.decompress((O/p['path']).read_bytes());assert len(b)==p['raw_bytes']and sha(b)==p['raw_sha256']
 delta=json.loads((O/'CLOSING_1372_EXACT_SCOPE_DISTINCTIONS_PROPOSED.json').read_bytes());assert delta['new_ledger_row']==238 and delta['doi']=='10.5281/zenodo.23576280'and len(delta['decisions'])==16 and delta['root_adopted']is False and delta['action_readiness']is False
 for d in delta['decisions']:assert d['target_four_cells_sha256']==items[d['pr']]['row_sha256']and bool(d['scientific_reason'])and d['root_adopted']is False
 out=json.loads((O/'OUTCOME_AND_HOLDS.json').read_bytes());assert out['readiness']is False and out['root_action_adopted']is False and out['production_actor_installed']is False and out['no_row_gap']['literal_four_cells']is None
 current=sum(p.lstat().st_blocks*512 for p in[O,*O.rglob('*')]);assert current<=10*1024*1024 and os.statvfs(O).f_bavail*os.statvfs(O).f_frsize>=150*1024*1024
 return{'status':'PASS_READONLY_PREPARATION_REPLAY_WITH_PRODUCTION_HOLD','families':34,'associated_PRs':35,'CF_positive_pairs':3127,'intrabatch_pairs':1122,'fake_controls':40,'custody_inventories':129,'closing_rows':238,'physical_bytes':current,'source_manifest_sha256':SOURCE_SHA,'production_actor_or_authorization_bridge_certified':False,'readiness':False,'action_authority':False}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--expected-sha256',required=True);a=p.parse_args();closure=module(O/'verify_closed_preparation.py','_whole_readonly_closure');sealed=closure['verify'](O,a.expected_sha256);print(json.dumps({'closure':sealed,'replay':replay()},sort_keys=True))
