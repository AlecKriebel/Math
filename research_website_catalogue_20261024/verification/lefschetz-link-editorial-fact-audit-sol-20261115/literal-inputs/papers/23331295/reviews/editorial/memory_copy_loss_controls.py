"""Eight bounded editorial loss controls, memory only; no source programme runs."""
from pathlib import Path
import copy
import json
import re
import validate_candidate as v


def run(root):
    pub, page, assets = v.load(root)
    positive = v.validate(root, pub, page, assets)
    results = []
    def reject(label, p, h, a):
        try: v.validate(root, p, h, a)
        except ValueError as error: results.append({'case': label, 'literal_rejection': str(error)})
        else: raise ValueError('accepted editorial loss: ' + label)
    p = copy.deepcopy(pub); p['abstract'] = p['abstract'][:90]
    reject('full_original_abstract_truncated', p, page, assets)
    p = copy.deepcopy(pub); del p['result'][3]
    reject('global_finite_order_whole_domain_paragraph_lost', p, page, assets)
    p = copy.deepcopy(pub); p['printed_version'] = '1.0'; p['printed_version_field_present'] = True
    reject('native_version_invented_as_printed_version', p, page, assets)
    a = dict(assets); del a['nullstellensatz.tex']
    reject('actual_additional_standalone_TeX_missing', pub, page, a)
    text = page.decode(); match = re.search(r'<script type="application/ld\+json">([\s\S]*?)</script>', text)
    schema = json.loads(match.group(1)); schema['encoding'].reverse()
    bad = (text[:match.start(1)] + json.dumps(schema,ensure_ascii=False) + text[match.end(1):]).encode()
    reject('native_TeX_ZIP_PDF_encoding_order_reversed', pub, bad, assets)
    p = copy.deepcopy(pub); p['license'] = 'MIT'; p['code_license'] = 'MIT'
    reject('invented_MIT_default', p, page, assets)
    p = copy.deepcopy(pub); p['review_metadata']['new_root_primary_access_update_separate_from_immutable_peer_limits']['root_new_all46page_or_predecessor_absence_certificate'] = True
    reject('root_selected_2010_reading_inflated_to_all46pages_or_absence', p, page, assets)
    v.need(page.count(b'<article>')==1, 'unique article loss anchor')
    reject('hidden_entire_article', pub, page.replace(b'<article>',b'<article hidden>',1), assets)
    return {'literal_custom_status':'EIGHT_MEANINGFUL_EDITORIAL_COPY_IDENTITY_ASSET_AND_SOURCE_SCOPE_LOSSES_REJECTED',
            'positive':positive,'cases':results,'positive_files_or_originals_modified':False,'native_or_owner_scientific_programmes_run':False}


if __name__=='__main__':
    print(json.dumps(run(Path(__file__).resolve().parent),indent=2))
