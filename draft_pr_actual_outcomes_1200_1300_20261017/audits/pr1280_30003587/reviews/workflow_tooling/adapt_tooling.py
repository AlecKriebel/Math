from pathlib import Path
T=Path('/Users/alec/Documents/Math/draft_pr_actual_outcomes_1200_1300_20261017'); A=T/'audits/pr1280_30003587'; R=A/'reviews/workflow_tooling'; D=R/'deployed'; P=D/'audits/pr1280_30003587/publication'
files=['compile_note.py','prepare_package.py','build_package.py','verification/verify.py','workflow_regression.py','check_public_downloads.py','append_tracker.py','update_pr_publication.py']
oldnames="{'AUDIT.md','EDITORIAL_MAP.json','PROOF.md','PUBLIC_MANIFEST.json','README.md','SOURCE_VERIFICATION.json'}"
newnames="{'ACCEPTANCE.json','CHECK_RESULTS.json','EDITORIAL_CHANGE_MAP.json','INDEPENDENT_AUDIT.md','MANIFEST.json','PROOF.md','README.md','SOURCE_METADATA.json','SOURCE_VERIFICATION.md'}"
replacements=[('fc334f4bd5d8cbc2a241293e2b1419d35c7eead1','f5085a4c954f814cde1bc3be0727ff30373aea95'),('4b27092a448d53b61408355ce44ec38d103a1ce4','a72180cf68ed6c9c54360cfd61b7a6567f5a0a5f'),('a415fdee0014e0bcee273b503891ec19132883ec942823878fc0a3e8a49d2dc6','6ab00d803d8a28f0ac3450dc33c69752561482d2f4bb37e29024707c2ef6c213'),('unsolved_math_prioritization/attempts/2307072','attempts/30003587'),('research/2307072-beurling-annihilator-witnesses','publish-diagonal-30003587-20261011'),('pr1274_2307072','pr1280_30003587'),('2307072','30003587'),('PR1274','PR1280'),('pr1274','pr1280'),('1274','1280'),('Beurling_Annihilator_Counterexample','Diagonal_Actions_Strong_Approximate_Innerness'),('beurling-annihilator-counterexample','diagonal-actions-strong-approximate-innerness'),('beurling-annihilator','diagonal-actions'),('1792267200','1792195200'),(oldnames,newnames),('workflow_identity_revision1','workflow_tooling')]
for name in files+['@pr1274.py','@verify_pr1274_merge.py']:
 src=T/('publication_coordinators/'+name[1:] if name.startswith('@') else 'audits/pr1274_2307072/publication/'+name)
 out=D/('publication_coordinators/'+name[1:].replace('1274','1280') if name.startswith('@') else 'audits/pr1280_30003587/publication/'+name)
 text=src.read_text()
 for x,y in replacements:text=text.replace(x,y)
 out.parent.mkdir(parents=True,exist_ok=True);out.write_text(text)
# Exact original nine-file manifest format, with eight dictionary entries.
v=P/'verification/verify.py';s=v.read_text();a=s.index('def authenticate_edition(root):');b=s.index('\ndef authenticate_current',a)
s=s[:a]+'''def authenticate_edition(root):
    need({p.name for p in root.iterdir()}==NAMES,'edition must contain exactly nine regular files')
    for name in NAMES:need(member(root,name).is_file(),'nonregular edition member '+name)
    manifest=json.loads(member(root,'MANIFEST.json').read_text());entries=manifest.get('files')
    need(manifest.get('schema')=='public-proof-packet-manifest-v1' and manifest.get('problem_id')==str(PROBLEM) and manifest.get('intended_repository_path')==BASE,'exact original MANIFEST target/schema required')
    need(isinstance(entries,dict) and set(entries)==NAMES-{'MANIFEST.json'},'eight nonself dictionary entries required')
    for name,entry in entries.items():
        need(set(entry)=={'bytes','sha256'},'exact original MANIFEST row schema required')
        check_binding(member(root,name),entry)
''' +s[b:]
s=s.replace('len(entries)==6','len(entries)==9').replace('six-file','nine-file').replace("'submitted_files':6,'current_edition_files':6","'submitted_files':9,'current_edition_files':9")
s=s.replace("isinstance(context['source_date_epoch'],str) and context['source_date_epoch'].isdigit()","context['source_date_epoch']=='1792195200'")
v.write_text(s)
# Adapt fixed path counts without changing eleven-metadata checks.
for path in [P/'prepare_package.py',P/'build_package.py',P/'update_pr_publication.py',D/'publication_coordinators/verify_pr1280_merge.py']:
 s=path.read_text().replace('six-file','nine-file').replace('six submitted','nine submitted').replace('six files','nine files').replace('original six','original nine').replace("'current_edition_files':6,'original_submitted_files':6","'current_edition_files':9,'original_submitted_files':9").replace('len(files)!=11','len(files)!=14').replace('len(files)==11','len(files)==14').replace("len(snapshot['files'])!=6","len(snapshot['files'])!=9").replace('eleven publication paths','fourteen publication paths').replace('Exactly eleven final','Exactly fourteen final').replace('all11_merged_files_exact','all14_merged_files_exact').replace('eleven exact blobs','fourteen exact blobs').replace('all11 immutable','all14 immutable')
 s=s.replace('The nine-file PUBLIC_MANIFEST.json binds the five other current edition records through files/path/bytes/sha256.','The original nine-file MANIFEST.json binds the eight other submitted records through files dictionary keys and bytes/sha256.')
 path.write_text(s)
# Compile directly using existing shared cache; cache stays separate from log receipts.
p=P/'compile_note.py';s=p.read_text().replace("if not isinstance(epoch,str) or not epoch.isdigit()","if epoch!='1792195200'")
s=s.replace("scratch=ROOT.parent/'reviews/workflow_tooling/_local/texcache';scratch.mkdir(parents=True,exist_ok=True)","scratch=ROOT.parent/'reviews/workflow_tooling/_local';scratch.mkdir(parents=True,exist_ok=True)\n    texcache=Path('/Users/alec/Documents/Math/draft_pr_actual_outcomes_1200_1300_20261017/audits/pr1274_2307072/reviews/workflow_tooling/_local/texcache')")
s=s.replace('XDG_CACHE_HOME=str(scratch)','XDG_CACHE_HOME=str(texcache)');p.write_text(s)
# Canonical OWR alias with exact outer token boundaries.
p=P/'append_tracker.py';s=p.read_text();a=s.index('# The original problem uses');b=s.index('\ndef row_has_problem_identity',a)
s=s[:a]+"# Canonical OWR-15585-006 and common separator/zero-padding variants.\nOWR_ALIAS=re.compile(r'(?<![a-z0-9])owr[\\s_-]*0*15585[\\s_-]*0*6(?![a-z0-9])',re.IGNORECASE)\n"+s[b:];s=s.replace('AMR_ALIAS','OWR_ALIAS');p.write_text(s)
# Explicit pinned shared kit at runtime, even before the kit import.
p=D/'publication_coordinators/pr1280.py';s=p.read_text();s=s.replace("spec=importlib.util.spec_from_file_location('pr1280_exact_zenodo_kit',REPO/'zenodo_deposit_tool/zenodo.py');", "require(digest(REPO/'zenodo_deposit_tool/zenodo.py')=='a91f961bcabadb15f92bb738c3194f0277cd47f1f87167ac8db8eb7c4fd3b9ca','Pinned shared kit drift');spec=importlib.util.spec_from_file_location('pr1280_exact_zenodo_kit',REPO/'zenodo_deposit_tool/zenodo.py');")
p.write_text(s)
# Previous completion is PR1274; next PR1283.
p=D/'publication_coordinators/verify_pr1280_merge.py';s=p.read_text().replace('COMPLETED_BEFORE=[1205,1211,1216,1225,1241,1261,1262,1268,1271]','COMPLETED_BEFORE=[1205,1211,1216,1225,1241,1261,1262,1268,1271,1274]').replace('1271,1280,1280,1283','1271,1274,1280,1283').replace('current_pr=1280','current_pr=1283').replace('exact9 prior','exact10 prior').replace('next1280','next1283').replace("'AMR alias'","'OWR alias'")
p.write_text(s)
# Fixture original manifest and meaningful explicit checks survive optimization.
p=P/'workflow_regression.py';s=p.read_text();a=s.index('ALIAS_VARIANTS=');b=s.index('\ndef need',a)
s=s[:a]+"ALIAS_VARIANTS={'alias':'oWr15585006','aliasHyphen':'OWR-15585-006','aliasSpace':'oWR 15585 006','aliasUnderscore':'OWR_15585_006','aliasMixed':'oWr - 15585_006','aliasUnpadded':'OWR-15585-6','aliasZeroPad':'OWR_0015585_0006','aliasZeroPadCompact':'OWR00155850006'}\nALIAS_NEAR_COLLISIONS={'nearHyphen':'OWR-15585-0069','nearSpace':'OWR 15585 0069','nearUnderscore':'OWR_15585_0069','nearCompact':'OWR155850069','nearWrongGroup':'OWR-115585-006','nearTrailingLetter':'OWR-15585-006x','nearLeadingLetter':'XOWR-15585-006'}\n"+s[b:]
s=s.replace("v.NAMES-{'PUBLIC_MANIFEST.json'}","v.NAMES-{'MANIFEST.json'}")
s=s.replace("save(submitted/'PUBLIC_MANIFEST.json',{'schema':1,'problem_id':v.PROBLEM,'file_count':6,'files':[{'path':n,**binding(submitted/n)} for n in sorted(v.NAMES-{'MANIFEST.json'})]})","save(submitted/'MANIFEST.json',{'schema':'public-proof-packet-manifest-v1','problem_id':str(v.PROBLEM),'intended_repository_path':v.BASE,'files':{n:binding(submitted/n) for n in sorted(v.NAMES-{'MANIFEST.json'})}})")
s=s.replace('assert 2+2==4',"if 2+2!=4:raise RuntimeError('fixture arithmetic check')").replace("assert len(s['files'])==6","if len(s['files'])!=9:raise RuntimeError('fixture original count')").replace("for e in s['files']: assert (r/e['local']).is_file()","for e in s['files']:\\n if not (r/e['local']).is_file():raise RuntimeError('fixture original file missing')")
s=s.replace("'synthetic_exact':6","'synthetic_exact':9").replace('Synthetic assertion-based fixture','Synthetic explicit-check fixture').replace('AMR0227072','OWR15585006')
s=s.replace('len(files)==11','len(files)==14').replace('range(11)','range(14)').replace('intended6+5','intended9+5').replace("'current_edition':6","'current_edition':9").replace('original6_current6','original9_current9').replace('The six-file PUBLIC_MANIFEST.json binds the five other current edition records through files/path/bytes/sha256.','The original nine-file MANIFEST.json binds the eight other submitted records through files dictionary keys and bytes/sha256.')
s=s.replace("'current_pr']=1280","'current_pr']=1283").replace('(1280 if wanted_accept','(1283 if wanted_accept').replace("len(after['publications'])==10","len(after['publications'])==11").replace('Expected9 to10','Expected10 to11').replace("'https://github.com/AlecKriebel/Math/pull/1280')]:","'https://github.com/AlecKriebel/Math/pull/1283')]:")
p.write_text(s)
print(P)
