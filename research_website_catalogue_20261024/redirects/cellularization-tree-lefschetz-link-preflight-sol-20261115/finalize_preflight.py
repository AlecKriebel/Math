#!/usr/bin/env python3
"""Finalize private identity evidence, never run scientific or prior packet code."""
from pathlib import Path
from html.parser import HTMLParser
import datetime, hashlib, json, re, subprocess, unicodedata
O=Path(__file__).resolve().parent
P=O.parents[1]
D=P/'redirects/median-gap-preflight-sol-20261115'
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def save(n,v):
 p=O/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def binding(p):
 p=p.resolve();b=p.read_bytes();return {'path':str(p),'bytes':len(b),'SHA256':sha(b)}
def api(n):return json.loads(load(O/'raw'/n)['structuredContent']['content'])
def norm(t):return ' '.join(unicodedata.normalize('NFKC',t).replace('–','-').replace('—','-').casefold().split())

now=datetime.datetime.now(datetime.timezone.utc).isoformat()
inputs=load(O/'INPUT_MANIFEST.json');by={r['path']:r for r in inputs['files']}
for name in ['installation.json','deploy-final-observed.json']:
 p=P/'verification/cellularization-tree-production-integration-root-20261115'/name;by[str(p)]=binding(p)
receipts=[]
for p in sorted((O/'raw').glob('*.json')):
 x=load(p);s=x['structuredContent'];b=s['content'].encode()
 request=s.get('url')
 if p.name=='current-strict-gap-blob.json':request='https://api.github.com/repos/AlecKriebel/Math/git/blobs/7b7411fefe1638f4721bc2180486574497f69ab0'
 receipts.append({'stored_actual_tool_response':binding(p),'request_URL':request,'whole_native_content_bytes':len(b),'whole_native_content_SHA256':sha(b),'returned_isError':x.get('isError'),'response_headers_available':False,'raw_HTTP_status_claimed':None,'transport':'GitHub native plugin returned complete content envelope, not a captured HTTP header stream'})
save('WHOLEBODY_TRANSPORT_RECEIPTS.json',{'UTC':now,'responses':receipts,'all_stored_native_responses_complete':True,'unpersisted_early_observations_not_used_as_evidence':['One preliminary main ref read before start capture','One preliminary strict-gap blob read before saved repeat'],'native_plugin_read_calls_including_two_preliminary_reads':11,'mutation_calls':0,'no_http_headers_invented':True})
start={'commit':api('remote-main-start.json')['object']['sha'],'root':api('remote-root-start.json')['sha'],'docs':api('remote-docs-start.json')['sha']}
end={'commit':api('remote-main-end.json')['object']['sha'],'root':api('remote-root-end.json')['sha'],'docs':api('remote-docs-end.json')['sha']}
assert start['docs']==end['docs'] and api('remote-docs-start.json')==api('remote-docs-end.json')
save('REMOTE_BOUNDARY.json',{'UTC':now,'opening':start,'closing':end,'actual_four_root_docs_tree_responses':['remote-root-start.json','remote-docs-start.json','remote-root-end.json','remote-docs-end.json'],'docs_complete_typed_JSON_equal':True,'moving_main_and_root_accepted_without_shared_control_file_freeze':True,'main_changed_during_parent_checkpoint':start['commit']!=end['commit'],'scope_of_invariance':'Only actual docs subtree and its complete304entries/254blobs; no immobility assertion for root, main, localHEAD, index or ref-control files.'})
# Existing native commit bodies, not fetches or refs/index writes.
for phase,point in [('start',start),('end',end)]:
 r=subprocess.run(['git','cat-file','commit',point['commit']],cwd=P.parent,capture_output=True)
 if r.returncode==0:
  b=r.stdout;assert hashlib.sha1(b'commit '+str(len(b)).encode()+b'\0'+b).hexdigest()==point['commit'];(O/'raw'/('native-commit-'+phase+'.raw')).write_bytes(b)
  assert b.splitlines()[0]==('tree '+point['root']).encode()
 else:raise RuntimeError('Current existing commit body unavailable; do not fetch')

# A second, punctuation-insensitive mechanism tests identity signatures without relying on regex punctuation.
old=load(D/'CURRENT_BLOB_BINDINGS.json');current=load(O/'CURRENT_BLOB_BINDINGS.json');representations=[]
for r in old:
 raw=D/'corpus'/f"{r['blob']}.raw"
 if raw.exists():
  if r['path']=='docs/papers/strict-dirichlet-gap/index.html':raw=O/'private/current-strict-gap.html'
  representations.append((r['path'],'raw_UTF8',str(raw),raw.read_text()))
  if r['path'].endswith('.html'):
   v=D/'corpus'/f"{r['blob']}.visible.txt"
   if r['path']=='docs/papers/strict-dirichlet-gap/index.html':v=O/'private/current-strict-gap.visible.txt'
   representations.append((r['path'],'decoded_HTML',str(v),v.read_text()))
for r in load(O/'REUSED_EXTRACT_BINDINGS.json'):representations.append((r['public_path'],'reused_complete_PDF_text',r['path'],Path(r['path']).read_text()))
needles={'121':['cellularization','cellularisation','nonnilpotentcomponent','proxysmall','23439582','23439581'],'122':['elevenvertextree','fivelistobstruction','treefivelist','listdistancelabell','listdistancelabel','l21label','23440389','23440388'],'127':['periodiclefschetz','symmetricidealchain','23570763','23570762','30004534'],'128':['nullstellensatz','finitetypelinkinvariants','finitetypelinkinvariant','actualinkzeroset','23331295','23331294']}
secondary={}
for rid,ns in needles.items():
 hits=[]
 for path,kind,source,t in representations:
  flat=re.sub(r'[^a-z0-9]','',norm(t));matched=[n for n in ns if n in flat]
  if matched:hits.append({'public_path':path,'representation':kind,'path':source,'matched_needles':matched})
 secondary[rid]=hits
assert all(not v for v in secondary.values())
save('PUNCTUATION_INSENSITIVE_SEARCH.json',{'UTC':now,'mechanism':'NFKC/casefold, remove non-ASCII-alphanumeric punctuation/spacing, literal signature matching','needles':needles,'whole_representations_searched':len(representations),'hits':secondary,'not_an_independent_reviewer':True})

exclusions=[{'public_path':'docs/papers/exceptional-ybe-d4/paper.pdf','why_selected':'Only121broad Hopf hit','identity':'An exceptional four-dimensional unitary Hecke Yang–Baxter operator: a five-word Pauli–Clifford normal form','printed_version':'1.2.0','printed_date':'19August2026','DOI':'10.5281/zenodo.22013710','full_cached_text_pages_read':20,'exact_hit':'Hopf links in the Section9 sample-closure table onphysical17','theorem_and_proof_identity':'16-by-16unitary Hecke Yang–Baxter matrix, fivePauliwords, cubiccertificate, Markov localization, all-strandconjugacy and enhancedHOMFLYPT trace; not completedloopchains/cellularization/Hopfidealvanishing. No targetpaperrecord/title/signature appears.','correspondence':False,'action':'EXCLUDE_UNRELATED_DIRECT_PDF_ASSET; noPDFredirect'}, {'public_path':'docs/research/gamma-theta-conjecture/index.html','why_selected':'Only122broad list-coloring HTMLhit, occurring in both raw and decoded representations','identity':'Thegamma–theta conjecture inone-guardeternaldomination','dated_snapshot':'28July2026','first_public_research_edition':'26July2026','full_raw_HTML_bytes':104054,'full_decoded_visible_characters_read':92166,'literal_subject_status':'Universal conjecture unresolved; order12andorder13parameter3finiteexclusions, otherorder13parametersopen','theorem_and_proof_identity':'One-guardgameparameter equality gamma=gamma-infinity impliescliquecover equality; response-listcoloring is an internal restoration/gluing mechanism with certificates and openbranchlimits, not L(2,1)positive-integergaplabels or an elevenvertextreebadfivelist assignment.','context_not_counterpart':'A whole active-research parent snapshot with links to its own two distinctgamma–thetapapers; neither template/reference nor an unpublishedversion of the fourtargetworks.','complete_HTML_parsed_and_whole_decoded_body_read':True,'correspondence':False,'action':'EXCLUDE_UNRELATED_RESEARCH_PROGRAM; noHTMLredirect'}]
save('EXCLUSIONS.json',{'UTC':now,'items':exclusions,'genuine_candidate_HTML_count':0,'PDF_ZIP_direct_asset_redirects_proposed':[],'unrelated_archive_expansion_or_scientific_verification_performed':False})
identities=load(O/'TARGET_IDENTITIES.json')
records={}
for t,row in zip(identities,[121,122,127,128]):
 rid=t['record_id'];records[rid]={'sheet_row':row,'literal_VERDICT':'BOUNDED_NEGATIVE_NO_GENUINE_CORRESPONDING_OLD_HTML_ARTICLE_LOCATED','title':t['fields']['title'],'native_version':t['fields']['version'],'printed_version':t['fields']['printed_version'],'publication_date':t['fields']['publication_date'],'DOI':t['fields']['doi'],'entire_published_PDF_and_approved_public_copy_read_for_identity':True,'legacy_HTML_URL':None,'proposed_redirect_target':None,'no_target_invented_from_slug':True,'native_asset_equal_docs_paths':t['native_asset_equal_docs_paths'],'redirect_authorized_now':False,'next_action':'No legacy redirect for this verified docs corpus. Preserve publication/browser/native tracker gates and revisit only if materially new genuine oldarticle evidence appears.'}
save('VERDICT.json',{'UTC':now,'literal_VERDICT':'FOUR_BOUNDED_NEGATIVES; NO_REDIRECT_MUTATION_OR_AUTHORITY','records':records,'scope':'Complete authenticated254-blob current GitHubPages docs subtree f5f5fb2fb18196b604d7b568e3e58ccc1bf127b3, searched through260whole representations including76PDFpathoccurrences/854pages; not globalinternetabsence or a survey of allhistory.','remote_opening':start,'remote_closing':end,'redirects_written':[],'science_reopened_or_checkers_run':False,'new_PDF_extractions':0,'full_archives_expanded':0,'source_site_core_Sheet_Gitref_localindex_deploy_contact_mutations':False,'outside_communication_or_outreach_preparation':False,'current_121122_publication_context':'Root has deployed the two actual approved slugs. Briefing states browserverification remains incomplete and AAblank. This lane didnot inspectbrowser or Sheet; literal frozenconfig nulls stayhistorical.','current_127128_editorial_context':'Sealed private editorial packets; allpublicationandbrowser/native gates remainseparate. Noassignedcanonicalinvention.','adversarial_subagent_attempt':'Threadlimitrejected; nochildworkorindependentreviewclaimed. Parentrootadoptionremainsseparate.','completion_percent_this_bounded_preflight':100,'overall_goal_completion_or_new_stage_counts_claimed':False})
save('DELEGATION_DIAGNOSTIC.json',{'UTC':now,'requested_task':'Independent falsification of wholefalsehitidentities and corpusnegativeinference','spawn_attempted':True,'result':'collab spawn failed: agent thread limit reached','child_created':False,'independent_review_claimed':False})
save('NO_MUTATION_LEDGER.json',{'UTC':now,'only_write_root':str(O),'Git_commands_executed':['git cat-file blob <254boundoriginalIDs>, oncepercollectionpass; owncollector executedtwice afteradding existingwholebody proofpaths','git cat-file commit <openingandclosingexplicitremotecommitIDs>'],'Git_read_only':True,'all_network_requests':'NativeGitHubpluginGETsforboundedref/commit/root/docs/currentknownblobidentityonly; seecompletebodyreceipts','network_mutations':[],'no_git_status_head_index_or_ref_snapshot_freeze':True,'no_git_fetch_clone_checkout_add_commit_push_update_ref_or_remote_write':True,'native_scientific_or_old_campaign_execution':False,'new_corpus_clone_or_pdf_reextraction':False,'prior_helpers_read_not_executed':['median-gap-preflight-sol-20261115/collect.py','median-gap-preflight-sol-20261115/verify_readonly.py'],'all_new_artifacts_under_allowed_root':True})
inputs['files']=list(by.values());save('INPUT_MANIFEST.json',inputs)
log=load(O/'RESEARCH_LOG.json');log['checkpoints'].append({'UTC':now,'completion_percent_this_preflight':100,'finding':'Allfour boundednegatives, twofullbodyfalsehits excluded, secondpunctuation-independent searchnegative, opening/closingdocs identical despiteparentmaincheckpoint, noapplicationauthority or mutations. Threadlimits preventedrequestedindependentaudit; notclaimed.'});save('RESEARCH_LOG.json',log)
print(json.dumps({'records':list(records),'current_docs':end['docs'],'current_total_body_bytes':sum(r['bytes'] for r in current),'secondary_hits':{k:len(v) for k,v in secondary.items()},'inputs':len(by),'stored_native_response_bodies':len(receipts)},indent=2))
