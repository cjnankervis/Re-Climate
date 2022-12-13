## Catalog fields

| Element         | Type          | Description                                                  |
| --------------- | ------------- | ------------------------------------------------------------ |
| type            | string        | **REQUIRED.** Set to `Catalog` if this Catalog only implements the Catalog spec. |
| stac_version    | string        | **REQUIRED.** The STAC version the Catalog implements. |
| stac_extensions | \[string]     | A list of extension identifiers the Catalog implements.                 |
| id              | string        | **REQUIRED.** Identifier for the Catalog.                    |
| title           | string        | A short descriptive one-line title for the Catalog.          |
| description     | string        | **REQUIRED.** Detailed multi-line description to fully explain the Catalog. [CommonMark 0.29](http://commonmark.org/) syntax MAY be used for rich text representation. |
| links           | [[Link Object](#link-object)] | **REQUIRED.** A list of references to other documents.       |
