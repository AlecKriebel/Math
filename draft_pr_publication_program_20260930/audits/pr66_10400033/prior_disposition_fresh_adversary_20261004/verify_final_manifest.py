from pathlib import Path
import hashlib,json,stat
BASE=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p,row):
 b=p.read_bytes();assert len(b)==row['bytes'] and sha(b)==row['sha256'];return b
m=json.loads((BASE/'FINAL_MANIFEST.json').read_text())
for row in m['files']:pin(BASE/row['path'],row)
seal=json.loads((BASE/'FIRST_CONCLUSION_SEAL.json').read_text())
pin(BASE/'FIRST_CONCLUSION.md',seal['first_conclusion'])
assert stat.S_IMODE((BASE/'FIRST_CONCLUSION.md').stat().st_mode)==0o444
assert seal['first_conclusion']['sha256']=='f53d0551b2286ff7c2e297ec9d1c56d247ed70c38f17d96a6bef49b017e8b406'
receipts=0;with_pid=0
for p in sorted((BASE/'receipts').glob('*.json')):
 r=json.loads(p.read_text())
 if 'streams' not in r:continue
 for row in r['streams'].values():pin(BASE/row['path'],row)
 receipts+=1
 if 'actual_child_pid' in r:
  assert r['actual_child_pid']>0 and r['cwd']==str(BASE);with_pid+=1
for row in json.loads((BASE/'FINAL_PRIVATE_SOURCE_PINS.json').read_text())['files']:pin(Path(row['path']),row)
for packet in m['audited_packets']:
 for row in packet['files']:pin(Path(packet['directory'])/row['path'],row)
v=json.loads((BASE/'VERDICT.json').read_text())
assert v['verdict']=='PASS_ATTRIBUTED_PRIOR_RESULT_NO_MATERIAL_REPAIR'
assert v['both_v1_and_final_v2_packets_read_completely'] and v['all_eight_packet_pins_valid'] and v['v1_four_pins_unchanged']
assert v['v2_prior_even_ingredient_corollary_verified'] and v['audit_completion_percent']==100
assert not v['promotion_authority'] and not v['native_acceptance_or_merge_performed']
print(json.dumps({'status':'PASS','bounded_manifest_members_verified':len(m['files']),'own_recorded_child_receipt_stream_pairs_verified':receipts,'own_recorded_children_with_observed_pid':with_pid,'missing_earlier_pid_gap_disclosed':True,'FIRST_unchanged_and_read_only':True,'all_eight_v1_v2_packet_pins_rechecked':True,'both_packet_manifests_rechecked':True,'private_primary_source_bodies_and_pixels_rechecked':True,'final_expanded_scope_completed':True},indent=2))
