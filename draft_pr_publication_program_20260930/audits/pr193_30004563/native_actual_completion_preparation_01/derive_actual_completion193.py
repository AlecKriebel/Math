"""Pure accepted-completion reconciliation for PR193.
No I/O, API, Git, native/PR mutation or hidden clock. Root's adapter must supply
the exact rederived38-file phase100 map and a genuine prior actual factual
acceptance receipt with its trusted byte/hash pin. No receipt for this new
checkpoint is assumed or required; the prior actual receipt is the authority.
"""
import datetime, hashlib, json, re

HEAD='b9a399eeac816dbb8f0e50e81b498c26e5acef81'
NATIVE='unsolved_math_prioritization/attempts/30004563/'
EXPECTED_STATUS='ACTUAL_PR193_FACTUAL100_FULL_PARENT_SCOPE_COMBINED_CURRENT_IDENTITIES_ACCEPTED'
CURRENT_STATUS='ACTUAL_PR193_FACTUAL100_ACCEPTED_COMPLETE_FROM_PRIOR_ROOT_RECEIPT'
CHANGED=('CURRENT_PROOF.md','README.md','SOURCE_AUDIT.md','FINAL_DISPOSITION.md',
         'readiness.json','continuity.json','source_manifest.json','PUBLICATION.json',
         'RESEARCH_LOG.md','frozen_artifacts.json')

# Same three pure low-level definitions already reused from accepted191.
def require(x,msg):
 if not x:raise RuntimeError(msg)
def encoded(value):return (json.dumps(value,indent=2)+'\n').encode()
def byte_pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}

def utc(value):
 require(isinstance(value,str),'Explicit UTC required')
 try:t=datetime.datetime.fromisoformat(value.replace('Z','+00:00'))
 except ValueError:raise RuntimeError('Invalid UTC timestamp')
 require(t.utcoffset()==datetime.timedelta(0),'Timestamp not UTC')
 return t
def sha40(value):return isinstance(value,str) and re.fullmatch(r'[0-9a-f]{40}',value) is not None
def sha64(value):return isinstance(value,str) and re.fullmatch(r'[0-9a-f]{64}',value) is not None

def derive_actual_completion(*,phase100,factual_acceptance,factual_utc):
 """Return exact38-file map,10 updates/inventories and truthful current PR text.
factual_acceptance={receipt_bytes:<genuine Root prior JSON bytes>,
                    receipt_pin:{bytes:<length>,sha256:<trusted actual hash>}}
The completion adapter binds receipt to the actual100 preparation/selected map.
This function does not infer remote freshness or acceptance from a candidate.
"""
 require(phase100['phase']==100 and phase100['original_head']==HEAD,'Exact accepted-source phase100 derivation required')
 files=dict(phase100['native_files']);inv=phase100['native_inventory']
 require(len(files)==38 and set(files)==set(inv),'Exact phase100 inventory38')
 for n,b in files.items():
  require(n.startswith(NATIVE) and isinstance(b,bytes) and byte_pin(b)==inv[n],'Phase100 path/bytes/inventory mismatch')
 require(len([n for n in files if n.startswith(NATIVE+'publication/')])==15,'Exact15 publication files required')
 require(set(factual_acceptance)=={'receipt_bytes','receipt_pin'},'Genuine prior Root receipt bytes/pin required')
 raw=factual_acceptance['receipt_bytes'];pin=factual_acceptance['receipt_pin']
 require(isinstance(raw,bytes) and isinstance(pin,dict),'Actual receipt bytes/pin types')
 actual=byte_pin(raw)
 require(actual['bytes']==pin.get('bytes') and actual['sha256']==pin.get('sha256'),'Actual factual receipt pin mismatch')
 receipt_pin={k:actual[k] for k in ('bytes','sha256')};r=json.loads(raw);f100=phase100['facts']
 require(r['PR']==193 and r['original_head']==HEAD and r['accepted'] is True,'Wrong/not-accepted actual Root factual receipt')
 require(r['status']==EXPECTED_STATUS,'Not full-parent/combined-current factual100 acceptance')
 require(r['every_selected_identity_checked_at_actual_observed_MAIN'] is True,'Actual combined current identities were not checked')
 require(r['actual_factual_MAIN_accepted'] is True and r['actual_original_PR_merged'] is True,'Actual factual/merge acceptance missing')
 require(sha40(r['factual_commit']) and sha40(r['sole_parent']) and sha40(r['main_observed']) and sha40(r['actual_tree']),'Actual factual commit/parent/current-tree identities')
 require(r['original_merge_commit']==phase100['actual_merge_commit'] and sha40(r['original_merge_commit']),'Actual original merge mismatch')
 require(r['DOI']==f100['DOI'] and r['tracker_range']==f100['tracker_range'],'Actual factual DOI/tracker mismatch')
 require(r['fully_completed_count']==41 and r['published_count']==25 and r['last_completed_PR']==193 and r['case_percent']==100,'Actual factual41/25/PR193/100 mismatch')
 require(isinstance(r['selected_files'],int) and r['selected_files']>=38 and sha64(r['selected_map_sha256']),'Actual combined selected-map identity')
 require(r['goal_complete'] is False,'Programme goal is not globally complete')
 require(utc(factual_utc)>=utc(r['UTC'])>=utc(f100['UTC']),'Reconciliation precedes prior actual factual acceptance')
 prior={'receipt_name':'ROOT_FINAL_FACTUAL_ACCEPTANCE.json','receipt_pin':receipt_pin,
        'UTC':r['UTC'],'status':r['status'],'factual_commit':r['factual_commit'],
        'sole_parent':r['sole_parent'],'original_merge_commit':r['original_merge_commit'],
        'main_observed':r['main_observed'],'actual_tree':r['actual_tree'],
        'selected_files':r['selected_files'],'selected_map_sha256':r['selected_map_sha256'],
        'every_selected_identity_checked_at_actual_observed_MAIN':True}
 updates={'UTC':factual_utc,'status':CURRENT_STATUS,'case_percent':100,
          'actual_original_PR_merged':True,'actual_merge_commit':r['original_merge_commit'],
          'actual_factual_MAIN_accepted':True,'completed':True,'goal_complete':False,
          'fully_completed_count':41,'published_count':25,'last_completed_PR':193,
          'actual_accepted_factual_commit':r['factual_commit'],
          'prior_actual_factual_acceptance':prior,
          'record_semantics':'Actual prior Root factual100 acceptance; this reconciliation does not attest its own future commit.'}
 def current_json(j):
  j.update(updates)
  if 'current_status' in j:j['current_status']=CURRENT_STATUS
  for key in ('factual_postimage_not_adopted_until_actual_MAIN_acceptance',
              'factual_postimage_programme_counts','programme_counters_unchanged_until_actual_factual_acceptance'):
   j.pop(key,None)
  if 'remaining_required' in j:j['remaining_required']='None for this PR result; overall programme goal remains incomplete.'
  if 'fresh_MAIN_parent' in j:j['original_merge_MAIN_parent']=j.pop('fresh_MAIN_parent')
  if 'fresh_QUEUE_preimage' in j:j['original_merge_QUEUE_preimage']=j.pop('fresh_QUEUE_preimage')
  if 'proposed_integrated_queue_status' in j:j['integrated_queue_status']=j.pop('proposed_integrated_queue_status')
  if 'proposed_integrated_effort' in j:j['integrated_effort']=j.pop('proposed_integrated_effort')
  return j
 facts=current_json(dict(f100))
 old_sentence=phase100['factual_sentence']
 actual_sentence=('The two NEW whole-package adversaries completed clean and Root authenticated the final exact package. '
                  'The note is actually published at '+f100['DOI_URL']+'; tracker row '+r['tracker_range']+' was appended/read back with foreign rows retained. '
                  'Original-HEAD merge '+r['original_merge_commit']+' and factual100 commit '+r['factual_commit']+' were actually accepted. '
                  'Root verified the full parent scope and every combined selected identity at actual observed MAIN '+r['main_observed']+'. '
                  'This PR is completed at100%, with programme totals41completed/25published; the overall programme goal remains incomplete. '
                  'The prior actual Root factual acceptance receipt, not this reconciliation checkpoint, is the authority.')
 for rel in ('CURRENT_PROOF.md','README.md','SOURCE_AUDIT.md'):
  text=files[NATIVE+rel].decode()
  require(text.count(old_sentence)==1,'Unique prospective100 current sentence required '+rel)
  text=text.replace(old_sentence,actual_sentence)
  if rel=='README.md':
   old='Original-HEAD merge was actually accepted. This factual100 postimage still requires separate actual-main factual acceptance; the helper does not assert that later acceptance.'
   require(text.count(old)==1,'Unique prospective100 README closing paragraph')
   text=text.replace(old,'Original-HEAD merge and the separate factual100 MAIN postimage were actually accepted. Current completion facts are recorded from that prior genuine Root receipt; this reconciliation does not attest itself.')
  files[NATIVE+rel]=text.encode()
 disposition=files[NATIVE+'FINAL_DISPOSITION.md'].decode()
 require(disposition.count(old_sentence)==1,'Unique prospective disposition sentence')
 leading=disposition.split(old_sentence,1)[0]
 files[NATIVE+'FINAL_DISPOSITION.md']=(leading+actual_sentence+'\n\nOriginal submitted HEAD: '+HEAD+'. Integrated queue remains claimed_solved / 2/5; earlier historical effort remains unknown. Actual acceptance provenance and receipt pin are recorded in PUBLICATION.json. Science, all15 publication files, original19 custody and the mathematical proof core remain unchanged.\n').encode()
 for rel in ('readiness.json','continuity.json','source_manifest.json','PUBLICATION.json'):
  files[NATIVE+rel]=encoded(current_json(json.loads(files[NATIVE+rel])))
 # Preserve chronological95/100 log entries and append actual prior acceptance.
 files[NATIVE+'RESEARCH_LOG.md']+=('\n## '+factual_utc+' — actual factual100 acceptance recorded from prior Root receipt\n\n'+actual_sentence+' Original submitted effort2/5 retained; earlier historical effort unknown. No scientific/support/original bytes changed. Actual receipt SHA256 '+receipt_pin['sha256']+'.\n').encode()
 freeze=current_json(json.loads(files[NATIVE+'frozen_artifacts.json']))
 freeze['current_native_files']={n[len(NATIVE):]:byte_pin(b) for n,b in sorted(files.items()) if n!=NATIVE+'frozen_artifacts.json'}
 files[NATIVE+'frozen_artifacts.json']=encoded(freeze)
 allowed={NATIVE+n for n in CHANGED}
 require(set(files)==set(phase100['native_files']),'Native inventory38 changed')
 require(all(files[n]==b for n,b in phase100['native_files'].items() if n not in allowed),'Scientific/publication/custody/historical bytes changed')
 def core(b):return b.split(b'## Theorem and precise scope',1)[1].split(b'## Verification, geometry and attribution',1)[0]
 require(core(files[NATIVE+'CURRENT_PROOF.md'])==core(phase100['native_files'][NATIVE+'CURRENT_PROOF.md']),'Mathematical core changed')
 for rel in ('CURRENT_PROOF.md','README.md','SOURCE_AUDIT.md','FINAL_DISPOSITION.md'):
  text=files[NATIVE+rel].decode()
  require(old_sentence not in text and 'prospective programme41/25' not in text and 'actual-main factual acceptance remains required' not in text,'Prospective current prose survives '+rel)
 for rel in ('readiness.json','continuity.json','source_manifest.json','PUBLICATION.json','frozen_artifacts.json'):
  j=json.loads(files[NATIVE+rel])
  require(j['completed'] is True and j['actual_factual_MAIN_accepted'] is True and j['status']==CURRENT_STATUS,'Current actual completion aliases '+rel)
  require('current_status' not in j or j['current_status']==CURRENT_STATUS,'Current-status alias '+rel)
  require(not any(k in j for k in ('factual_postimage_not_adopted_until_actual_MAIN_acceptance','factual_postimage_programme_counts','proposed_integrated_queue_status','proposed_integrated_effort')),'Prospective flag/queue alias survives')
 pr_body=f100['scope']+'\n\n'+actual_sentence+'\n\nCurrent proof: '+NATIVE+'CURRENT_PROOF.md. Historical10^17 candidate/checker/certificate/review remain distinct from the final10^16 publication support. Publication verifier derives from the algebra/analysis audit implementation; no additional code-independence claim. Original19 custody, mathematical core and all15 final publication files remain fixed. Integrated queue status/effort remain claimed_solved / 2/5. Actual publication, tracker, original-HEAD merge and separate factual100 MAIN acceptance are complete; the prior genuine Root factual receipt is the completion authority.\n'
 return {'phase':'actual_accepted_completion','original_head':HEAD,'facts':facts,
         'native_files':files,'native_inventory':{n:byte_pin(b) for n,b in sorted(files.items())},
         'native_updates':{n:files[n] for n in sorted(allowed)},
         'native_update_inventory':{n:byte_pin(files[n]) for n in sorted(allowed)},
         'PR_title':phase100['PR_title'],'PR_body':pr_body,'factual_sentence':actual_sentence,
         'prior_actual_acceptance_receipt_pin':receipt_pin,'QUEUE_unchanged_from_actual_main_required':True,
         'actual_factual_MAIN_accepted':True,'completed':True,
         'no_mutation_performed':True,'no_receipt_for_own_reconciliation_commit_assumed':True}

