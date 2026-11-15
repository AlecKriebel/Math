"""Pure custody/static verification. No Git mutation, network or JS replay."""
from pathlib import Path
import json,hashlib,argparse
from redirect_contract import validate,DEST
E=Path(__file__).resolve().parent
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(ok,s):
 if not ok:raise ValueError(s)
def gb(data):return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--current-local',action='store_true');args=ap.parse_args();c=load(E/'EXPECTED_SCOPED_CHANGE.json');p=Path(c['candidate_path']);data=p.read_bytes()
 need(p.stat().st_size==c['candidate_bytes']==913 and sha(p)==c['candidate_sha256'] and gb(data)==c['candidate_git_blob'],'exact concrete candidate')
 need({str(x.relative_to(E/'candidate')) for x in (E/'candidate').rglob('*') if x.is_file()}=={c['only_allowed_change_path']},'exact one-path draft')
 validate(data.decode());need(c['mode']=='DRAFT_ONLY_NO_APPLICATION_AUTHORITY' and c['PDF_ZIP_or_upload_kit_deletions'] is False and c['index_or_sitemap_edits'] is False,'draft-only one-file boundary')
 old=(E/'cache/released-old-article.html').read_bytes();need(len(old)==c['expected_original_bytes'] and hashlib.sha256(old).hexdigest()==c['expected_original_sha256'] and gb(old)==c['expected_original_git_blob'],'expected exact old blob')
 template=(E/'cache/existing-template.html').read_bytes();need(gb(template)=='80cba99376f73ebf07698af3ead938d212885c30' and hashlib.sha256(template).hexdigest()=='1fe14e929d5fd0cfa6a759e914cdc312e7ceb7fef2e4202a9bfe82093504bbbb','actual existing released HTML redirect template')
 remote=json.loads(load(E/'cache/remote-ref.tool.json')['structuredContent']['content']);commit=json.loads(load(E/'cache/released-current-commit.tool.json')['structuredContent']['content']);tree=json.loads(load(E/'cache/released-current-root-tree.tool.json')['structuredContent']['content'])
 need(remote['object']['sha']==commit['sha']==c['observed_remote_main'] and commit['tree']['sha']==tree['sha']==c['observed_remote_root_tree'],'actual remote immutable ref/commit/tree observation')
 need(next(x for x in tree['tree'] if x['path']=='docs')['sha']==c['released_docs_tree'] and tree['truncated'] is False,'current released docs tree7a24 distinct from local6cc')
 for x in load(E/'SOURCE_AND_IDENTITY_BINDINGS.json')['original_evidence_files']:
  q=Path(x['path']);need(q.stat().st_size==x['bytes'] and sha(q)==x['sha256'],'original evidence unchanged')
 authority=load(E/'ADDITIVE_PUBLICATION_AUTHORITY.json');need(sha(Path(authority['path']))==authority['sha256']=='c2d5ce17c1f5922406b76604414f36a3288c270bf5afef46271af6f217f02951','new additive authority')
 need(authority['whole_original']==load(Path(authority['path'])) and authority['draft_only_lane_unchanged'] is True and authority['old_preflight_false_flags_not_rewritten'] is True,'whole new authority with historical distinction')
 need(authority['whole_original']['only_genuine111_legacy_redirect_application_authorized_after_recording_this_authority'] is True,'only genuine111 later authority')
 for x in load(E/'HTTP_OBSERVATIONS.json'):
  q=Path(x['body_path']);need(x['status']==200 and q.stat().st_size==x['bytes'] and sha(q)==x['sha256'],'captured actual HTTP200 bytes')
 need((E/'cache/current-legacy.html').read_bytes()==old,'actual old live bytes still released old body at observation')
 need('id="result"' in (E/'cache/live-replacement.html').read_text() and 'rel="canonical" href="'+DEST+'"' in (E/'cache/live-replacement.html').read_text(),'replacement canonical and result anchor')
 for x in load(E/'SOURCE_AND_IDENTITY_BINDINGS.json')['same_complete_PDF_ZIP_assets']:
  q=Path(x['path']);need(q.stat().st_size==x['bytes'] and sha(q)==x['sha256'] and gb(q.read_bytes())==x['expected_legacy_git_blob'],'unchanged same-v1.1 assets')
 tests=load(E/'URL_CONTROLS.json');need(tests['status']=='PASS_PURE_REDIRECT_URL_PARSER_CONTROLS' and len(tests['positive_cases'])==8 and len(tests['changed_script_controls_rejected'])==3 and tests['actual_browser_navigation'] is False,'tiny native URL parser evidence')
 need(len(load(E/'STATIC_CONTROLS.json')['rejected'])==3 and (E/'URL_CONTROLS.stderr').read_bytes()==b'','static fallback controls and no errors')
 if args.current_local:
  for x in load(E/'LOCAL_PRESERVATION_BEFORE.json')['protected_git_control_and_local_article_files']:
   q=Path(x['path']);need(q.stat().st_size==x['bytes'] and sha(q)==x['sha256'],'untouched local Git controls/article')
 if (E/'SEAL.json').exists():
  need(sha(E/'MANIFEST.json')==load(E/'SEAL.json')['manifest_sha256'],'draft manifest/seal')
  for x in load(E/'MANIFEST.json')['files']:
   q=Path(x['path']);need(q.stat().st_size==x['bytes'] and sha(q)==x['sha256'],'sealed owned draft artifact')
 print(json.dumps({'status':'PASS_DRAFT_ONLY_PURE_CUSTODY','candidate_paths':1,'candidate_bytes':913,'expected_old_blob':c['expected_original_git_blob'],'native_URL_positive_cases':8,'URL_script_faults_rejected':3,'static_fallback_faults_rejected':3,'current_local_preservation_checked':args.current_local,'application_done':False,'network_requests':0,'Git_or_site_mutations':0,'JS_or_old_campaign_replays':0},indent=2))
if __name__=='__main__':main()
