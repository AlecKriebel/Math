"""Read-only/offline probe of pinned official preview-setting methods.

Extract only the actual official functions with AST; replace surrounding storage,
permission and translation services by plain local objects. No network or tokens.
"""
from pathlib import Path
from types import SimpleNamespace
import ast, copy, hashlib, json

ROOT=Path(__file__).resolve().parents[1]
SOURCES=ROOT/'reviews'/'preview_source_snapshots'
MANIFEST=json.loads((SOURCES/'manifest.json').read_text())
TESTS=[]

class ValidationError(Exception):
    def __init__(self,message,**kw):super().__init__(message);self.messages=message

class InvalidKeyError(Exception):
    def __init__(self,description):super().__init__(description)
    def get_description(self):return str(self)

def method(path,cls,name,setter=False):
    tree=ast.parse(path.read_text());klass=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name==cls)
    candidates=[n for n in klass.body if isinstance(n,ast.FunctionDef) and n.name==name]
    if setter:candidates=[n for n in candidates if any(isinstance(d,ast.Attribute) and d.attr=='setter' for d in n.decorator_list)]
    node=copy.deepcopy(candidates[0]);node.decorator_list=[]
    ns={'ValidationError':ValidationError,'InvalidKeyError':InvalidKeyError,'_':lambda x:x}
    exec(compile(ast.fix_missing_locations(ast.Module(body=[node],type_ignores=[])),str(path),'exec'),ns)
    return ns[name]

def check(name,passed):TESTS.append({'test':name,'passed':bool(passed)})

draft=next(Path(e['local']) for e in MANIFEST if e['repository'].endswith('invenio-drafts-resources'))
manager=next(Path(e['local']) for e in MANIFEST if e['path'].endswith('manager.py'))
component=next(Path(e['local']) for e in MANIFEST if e['path'].endswith('components/files.py'))
schema=ROOT/'reviews/files_source_snapshots/invenio_rdm_records__services__schemas__files.py'
legacy=ROOT/'reviews/oai_source_snapshots/zenodo__zenodo-rdm__site__zenodo_rdm__legacy__deserializers__schemas.py'

tree=ast.parse(legacy.read_text());klass=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='LegacySchema')
files_assign=next(n for n in klass.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='files' for t in n.targets))
legacy_files=ast.literal_eval(files_assign.value.args[0])
check('official legacy file options have enabled only',legacy_files=={'enabled':True})

FileView=type('FileView',(),{'default_preview':property(lambda self:self._default_preview,method(manager,'FilesManager','default_preview',True)),
                           '__contains__':lambda self,key:key in self.entries,'items':lambda self:self.entries.items(),
                           'values':lambda self:self.entries.values()})
class Component:
    service=SimpleNamespace(config=SimpleNamespace(default_files_enabled=True),check_permission=lambda *a,**kw:False)
    files_data_key='files'
    get_record_files=lambda self,record:record.files
    _validate_files_enabled=method(component,'BaseRecordFilesComponent','_validate_files_enabled')
    assign_files_enabled=method(component,'BaseRecordFilesComponent','assign_files_enabled')
    assign_files_default_preview=method(component,'BaseRecordFilesComponent','assign_files_default_preview')
    update_draft=method(draft,'BaseRecordFilesComponent','update_draft')

details=json.loads((ROOT/'receipts/23203732/staging_guard_stop_details.json').read_text())
original=details['public_files'];files=FileView();files.entries=copy.deepcopy(original['entries']);files.enabled=original['enabled'];files.order=copy.deepcopy(original['order']);files._default_preview=original['default_preview']
record=SimpleNamespace(files=files);errors=[];c=Component()
c.update_draft(None,data={'files':copy.deepcopy(legacy_files)},record=record,errors=errors)
check('official update clears absent preview in legacy options',files.default_preview is None and errors==[])
missing=object();dump_value=method(schema,'FilesSchema','get_attribute')(None,files,'default_preview',missing)
check('official file schema omits cleared falsy preview',dump_value is missing)
check('cleared preview leaves exact file objects and order untouched',files.entries==original['entries'] and files.order==original['order'] and files.enabled==original['enabled'])
c.update_draft(None,data={'files':{'enabled':original['enabled'],'default_preview':original['default_preview'],'order':original['order']}},record=record,errors=errors)
check('official update restores original explicit preview',files.default_preview=='paper.pdf' and errors==[])
check('display restoration leaves file objects and order untouched',files.entries==original['entries'] and files.order==original['order'] and files.enabled==original['enabled'])
errors=[];c.update_draft(None,data={'files':{'enabled':True,'default_preview':'missing.pdf'}},record=record,errors=errors)
check('official preview setter rejects nonexistent file key',bool(errors) and files.default_preview=='paper.pdf')

tree=ast.parse(manager.read_text());klass=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='FilesManager')
sync=next(n for n in klass.body if isinstance(n,ast.FunctionDef) and n.name=='sync')
check('official sync publishes draft preview exactly',any(isinstance(n,ast.Assign) and ast.unparse(n)=='self.default_preview = src_files.default_preview' for n in sync.body))
out={'offline_only':True,'record_id':23203732,'source_manifest':MANIFEST,
     'additional_source_sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [schema,legacy]},
     'tests':TESTS,'passed':sum(t['passed'] for t in TESTS),'failed':sum(not t['passed'] for t in TESTS)}
(ROOT/'reviews/PREVIEW_SOURCE_PROBE.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'passed':out['passed'],'failed':out['failed'],'failures':[t['test'] for t in TESTS if not t['passed']]},indent=2))
raise SystemExit(bool(out['failed']))
