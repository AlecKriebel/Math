"""Read-only core eight-round check after sealing; never loads accepted_package or approves."""
import sys
if not(sys.flags.isolated and sys.flags.no_site and not sys.flags.optimize and sys.dont_write_bytecode):raise RuntimeError('Use -I -S -B')
from pathlib import Path
import hashlib,json,os
R=Path('/Users/alec/Documents/Math');P=R/'draft_pr_claimed_solved_900_1000_20261012';A=P/'audits/pr946_6000001';D=A/'preprint';O=Path(__file__).resolve().parent
os.environ.update(GIT_CONFIG_COUNT='1',GIT_CONFIG_KEY_0='gc.auto',GIT_CONFIG_VALUE_0='0',TMPDIR=str(O/'private/tmp'))
b=(P/'accept_pr946.py').read_bytes()
if hashlib.sha256(b).hexdigest()!='8e1a0d7b3ca6e5d72e76415541b393fbfbe52e307368bc86b9e7982d5be27cd7':raise RuntimeError('core external pin')
N={'__name__':'_eight_round_readonly_','__file__':str(P/'accept_pr946.py')};exec(compile(b,N['__file__'],'exec',dont_inherit=True,optimize=0),N)
ctx=N['capture_inventory']('f4742eca6ddd628ecac1e704fed772a17837d42d4d0fdef42c73d3cda3bed254');freeze=N['freeze_check'](N['read_regular'](D/'FREEZE.json'),'9af8f2570af53b6a6658a7998ac08927829c8747be7c764a8d2c392dc6c6afe1',ctx)
_,originals=N['original_check']();N['archive_check'](freeze,originals)
old=['2f1a4ba73839b83280e9daba44fbe79e70b52a80761deded5314e0db99c7e834','e0361044f313b540f8a46b6a417a00a1777e22a33439e9a097aa0f9e7b54c3e6','28f08795caf265a412463b3b30880f29bcbc615eb84baf4b92010d1720326370','7fb99b465473a17ad54a363c4ee6f410023b3857343a5df2c356a705d50180d0','4d60602995d799a0850c4657b3401ad9c353460800f1fbd752c532b73b6963b2','1c75fc274754826a9d189a7e5e5ac206782deddd0a91dc75d0636d9aa787de71','eb55f996d2149104316d840103b641b104e60b371a7d6bef5202aa117406898d']
specs=[f'{i:02d}:'+h for i,h in enumerate(old,1)]+['08:'+sys.argv[1]]
rows,last=N['review_check'](specs,freeze,'9af8f2570af53b6a6658a7998ac08927829c8747be7c764a8d2c392dc6c6afe1',ctx,originals)
op=N['read_regular'](A/'publication_operator.py',pin={'bytes':9912,'sha256':'d085ec080ee6c2f1239f49f724e7a71ef6d86b3d994fbe9b4039371181a61aef'});N['need'](N['exact'](last['inspected_publication_operator'],N['fingerprint'](op)),'latest separate operator identity');N['original_check']();N['archive_check'](freeze,originals)
result={'status':'PASS_READONLY_EIGHT_ROUND_CORE_CHECK','utc':N['utc_now'](),'review_count':len(rows),'reviews':rows,'all_prior_resolution_count':len(last['prior_issue_resolution']),'originals_checked':33,'archive_checked':True,'approval_created_or_extended':False,'accepted_package_called':False,'external_mutations':0}
(O/'private/SEALED_CHAIN_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['status','review_count','all_prior_resolution_count','originals_checked','approval_created_or_extended','external_mutations']}))
