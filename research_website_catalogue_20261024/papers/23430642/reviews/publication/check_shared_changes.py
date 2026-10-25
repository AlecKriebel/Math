from pathlib import Path
import ast,datetime,gzip,hashlib,io,json,sys,tarfile,tempfile,zlib
R=Path(__file__).resolve().parents[4];D=Path(__file__).resolve().parent
checker=R/'verification/final-content-check.py'
parsed=ast.parse(checker.read_text())
names={'tar_gz_integrity','normalized_game_seshadri_abstract'}
selected=ast.Module(body=[x for x in parsed.body if isinstance(x,ast.FunctionDef) and x.name in names],type_ignores=[])
namespace={'gzip':gzip,'tarfile':tarfile,'zlib':zlib};exec(compile(selected,str(checker),'exec'),namespace)
valid=namespace['tar_gz_integrity'];normalize=namespace['normalized_game_seshadri_abstract'];checks={}
original=R/'papers/23430642/sources/supportkit-v1.0.tar.gz';raw=original.read_bytes()
checks['authentic_tar_gz_integrity']=valid(original)
with tempfile.TemporaryDirectory(prefix='rank-one-publication-regression-') as td:
 t=Path(td)
 corruptions={'truncated-footer':raw[:-5],'truncated-body':raw[:len(raw)//2],'bad-gzip-crc':raw[:-8]+bytes([raw[-8]^1])+raw[-7:],'gzip-nontar':gzip.compress(b'not a tar archive'),'bad-compressed-stream':raw[:12]+bytes([raw[12]^255])+raw[13:]}
 unpacked=gzip.decompress(raw);corruptions['bad-tar-header-valid-gzip']=gzip.compress(bytes([unpacked[0]^1])+unpacked[1:])
 for name,data in corruptions.items():
  p=t/(name+'.tar.gz');p.write_bytes(data);checks['reject_'+name]=not valid(p)
 sys.dont_write_bytecode=True;sys.path.insert(0,str(R/'scripts'))
 from published_assets import PublishedAssets
 receipt={'files':[{'name':'supportkit-v1.0.tar.gz','bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}]}
 p=t/'supportkit-v1.0.tar.gz';p.write_bytes(raw)
 checks['resolver_authentic_tar_bytes']=PublishedAssets(t,receipt).resolve(p.name).read_bytes()==raw
 p.write_bytes(raw[:-1]+bytes([raw[-1]^1]))
 try:PublishedAssets(t,receipt).resolve(p.name);checks['resolver_rejects_changed_tar_bytes']=False
 except (ValueError,AssertionError):checks['resolver_rejects_changed_tar_bytes']=True
for rid in ['23430642','23387814']:
 P=R/'papers'/rid;c=json.loads((P/'publication.json').read_text());tex=(P/c['source_binding']['abstract_source']).read_text()
 import re
 body=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tex,re.S).group(1)
 checks[rid+'_full_original_abstract']=normalize(rid,body)==c['abstract']
 checks[rid+'_shortened_abstract_rejected']=normalize(rid,body)!=' '.join(c['abstract'].split()[:-1])
 checks[rid+'_added_editorial_sentence_rejected']=normalize(rid,body)!=c['abstract']+' This is an additional editorial sentence.'
 if rid=='23387814':checks['seshadri_changed_root_formula_rejected']=normalize(rid,body)!=c['abstract'].replace('(2+|K_S²|^(1/4))','((2+|K_S²|)^(1/4))')
preflight=json.loads((D/'preflight.json').read_text())
for p,expected in preflight['shared_before'].items():checks['unchanged_'+Path(p).name]=hashlib.sha256(Path(p).read_bytes()).hexdigest()==expected
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'completion_percent':100,'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'checker_sha256':hashlib.sha256(checker.read_bytes()).hexdigest(),'note':'Fresh corruption/abstract controls, byte-binding controls and unchanged renderer/resolver/live-checker/CSS checks. Existing ZIP, no-primary-supplement and embedded-reader regressions are in verification/game-seshadri-editor-content-check.json. No original source or public file was mutated by these controls.'}
(D/'shared-regression.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert all(checks.values())
