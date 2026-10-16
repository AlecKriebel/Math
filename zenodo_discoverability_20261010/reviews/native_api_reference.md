Official source: https://raw.githubusercontent.com/inveniosoftware/docs-invenio-rdm/master/docs/reference/rest_api_drafts_records.md

### Update a draft record

`PUT /api/records/{id}/draft`

**Parameters**

| Name       | Type   | Location | Description                                                  |
| ---------- | ------ | -------- | ------------------------------------------------------------ |
| `id`       | string | path     | Identifier of the record, e.g.  `4d0ns-ntd89`                |
| `access`   | object | body     | [Access options](metadata.md#access) for the record. |
| `files`    | object | body     | [Files options](#files-options) for the record. |
| `metadata` | object | body     | [Metadata](metadata.md#metadata) of the record. |
| `custom_fields` | object | body     | [Custom fields](../operate/customize/metadata/custom_fields/records.md#declaring-custom-fields) metadata for the record. (v10 and newer) |

**Request**

```http
PUT /api/records/{id}/draft HTTP/1.1
Content-Type: application/json

{
  "access": {
    "record": "restricted",
    "files": "restricted"
  },
  "files": {
    "enabled": false
  },
  "metadata": {
    "creators": [
      {
        "person_or_org": {
          "family_name": "Brown",
          "given_name": "Troy",
          "type": "personal"
        }
      },
      {
        "person_or_org": {
          "family_name": "Collins",
          "given_name": "Thomas",
          "identifiers": [
            {"scheme": "orcid", "identifier": "0000-0002-1825-0097"}
          ],
          "name": "Collins, Thomas",
          "type": "personal"
        },
        "affiliations": [
          {
            "id": "01ggx4157",
            "name": "Entity One"
          }
        ]
      }
    ],
    "publication_date": "2020-06-01",
    "resource_type": { "id": "image-photo" },
    "title": "An Updated Romans story"
  }
}
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json


{
  "access": {
    "record": "restricted",
    "files": "restricted",
    "embargo": {
      "reason": null,
      "active": false
    }
  },
  "created": "2020-11-27 10:52:23.945755",
  "expires_at": "2020-11-27 10:52:23.945868",
  "files": {
    "enabled": false
  },
  "id": "{id}",
  "is_published": false,
  "links": {
    "latest": "{scheme+hostname}/api/records/{id}/versions/latest",
    "versions": "{scheme+hostname}/api/records/{id}/versions",
    "self_html": "{scheme+hostname}/uploads/{id}",
    "publish": "{scheme+hostname}/api/records/{id}/draft/actions/publish",
    "latest_html": "{scheme+hostname}/records/{id}/latest",
    "self": "{scheme+hostname}/api/records/{id}/draft",
    "files": "{scheme+hostname}/api/records/{id}/draft/files",
    "access_links": "{scheme+hostname}/api/records/{id}/access/links"
  },
  "metadata": {
    "resource_type": {
      "id": "image-photo",
      "title": {
        "en": "Photo"
      }
    },
    "title": "An Updated Romans story",
    "publication_date": "2020-06-01",
    "creators": [
      "person_or_org": {
        "family_name": "Brown",
        "given_name": "Troy",
        "type": "personal"
      },
      {
        "person_or_org": {
          "family_name": "Collins",
          "given_name": "Thomas",
          "identifiers": [
            {"scheme": "orcid", "identifier": "0000-0002-1825-0097"}
          ],
          "name": "Collins, Thomas",
          "type": "personal"
        },
        "affiliations": [
          {
            "id": "01ggx4157",
            "name": "European Organization for Nuclear Research"
          }
        ]
      }
    ],
  },
  "parent": {
    "id": "{parent-id}",
    "access": {
      "owned_by": {
        "user": {user-id}
      },
      "links": []
    }
  },
  "pids": {},
  "revision_id": 3,
  "updated": "2020-11-27 10:52:23.969244",
  "versions": {
    "index": 1,
    "is_latest": false,
    "is_latest_draft": true
  }
}
```


### Edit a published record (Create a draft record from a published record)

`POST /api/records/{id}/draft`

**Parameters**

| Name | Type   | Location | Description                                   |
| ---- | ------ | -------- | --------------------------------------------- |
| `id` | string | path     | Identifier of the record, e.g.  `4d0ns-ntd89` |

**Request**

```http
POST /api/records/{id}/draft HTTP/1.1
```

**Response**

```http
HTTP/1.1 201 CREATED
Content-Type: application/json


{
  "access": {
    "record": "restricted",
    "files": "restricted",
    "embargo": {
      "reason": null,
      "active": false
    }
  },
  "created": "2020-11-27 10:52:23.945755",
  "expires_at": "2020-11-27 10:52:23.945868",
  "files": {
    "enabled": false
  },
  "id": "{id}",
  "is_published": false,
  "links": {
    "latest": "{scheme+hostname}/api/records/{id}/versions/latest",
    "versions": "{scheme+hostname}/api/records/{id}/versions",
    "self_html": "{scheme+hostname}/uploads/{id}",
    "publish": "{scheme+hostname}/api/records/{id}/draft/actions/publish",
    "latest_html": "{scheme+hostname}/records/{id}/latest",
    "self": "{scheme+hostname}/api/records/{id}/draft",
    "files": "{scheme+hostname}/api/records/{id}/draft/files",
    "access_links": "{scheme+hostname}/api/records/{id}/access/links"
  },
  "metadata": {
    "resource_type": {
      "id": "image-photo",
      "title": {
        "en": "Photo"
      }
    },
    "title": "An Updated Romans story",
    "publication_date": "2020-06-01",
    "creators": [
      "person_or_org": {
        "family_name": "Brown",
        "given_name": "Troy",
        "type": "personal"
      },
      {
        "person_or_org": {
          "family_name": "Collins",
          "given_name": "Thomas",
          "identifiers": [
            {"scheme": "orcid", "identifier": "0000-0002-1825-0097"}
          ],
          "name": "Collins, Thomas",
          "type": "personal"
        },
        "affiliations": [
          {
            "id": "01ggx4157",
            "name": "European Organization for Nuclear Research"
          }
        ]
      }
    ],
  },
  "parent": {
    "id": "{parent-id}",
    "access": {
      "owned_by": {
        "user": {user-id}
      },
      "links": []
    }
  },
  "pids": {},
  "revision_id": 3,
  "updated": "2020-11-27 10:52:23.969244",
  "versions": {
    "index": 1,
    "is_latest": true,
    "is_latest_draft": true
  }
}
```
