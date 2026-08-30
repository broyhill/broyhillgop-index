# Political Hierarchy and Directory Model

## Modeling rule

Government geography, electoral contests, political organizations, and platform accounts are separate hierarchies. They overlap and must not be forced into one rigid tree. Use typed relationships, effective dates, election-cycle context, geometry versioning, source provenance, and confidence scores.

## Geographic hierarchy

```text
Country
└── State / territory
    ├── Congressional district
    ├── State senate district
    ├── State house district
    ├── County / county equivalent
    │   ├── Municipality
    │   ├── Township
    │   ├── Ward
    │   ├── Precinct
    │   └── Special district
    ├── Judicial district
    ├── School district
    └── Media geography
        ├── DMA
        └── ZIP / postal geography
```

Store boundaries as versioned geometries. Districts, counties, ZIPs, precincts, and media markets overlap; use many-to-many relations such as `contains`, `overlaps`, `intersects`, and `served_by`.

## Electoral hierarchy

```text
Election cycle
└── Election
    ├── Primary
    ├── Runoff
    ├── General
    └── Special election
        └── Contest
            ├── Office
            ├── Jurisdiction / district
            ├── Candidates
            ├── Candidate committees
            ├── Party committees
            ├── PACs / super PACs
            ├── Independent expenditures
            └── Results
```

## Entity catalog

- Person
- Elected official
- Candidate
- Staff member
- Office
- Government body
- Political party
- Candidate committee
- Party committee
- PAC / super PAC
- Advocacy organization
- Ballot committee
- Ballot measure
- Issue
- Endorsement
- Donor
- Expenditure
- Vendor
- Media outlet
- Creative
- Audience
- Campaign
- Filing
- Event
- Source document

## Relationship catalog

```text
PERSON             HOLDS_OFFICE        OFFICE
PERSON             CANDIDATE_IN        CONTEST
PERSON             AFFILIATED_WITH     PARTY
PERSON             CONTROLS            COMMITTEE
COMMITTEE          SUPPORTS            CANDIDATE
COMMITTEE          OPPOSES             CANDIDATE
COMMITTEE          SUPPORTS            BALLOT_MEASURE
ORGANIZATION       ADVOCATES_FOR       ISSUE
DISTRICT           OVERLAPS            COUNTY
DISTRICT           CONTAINED_IN        STATE
CONTEST            ELECTS_TO           OFFICE
DONOR              CONTRIBUTED_TO      COMMITTEE
COMMITTEE          PAID                VENDOR
CREATIVE           SPONSORED_BY        COMMITTEE
CAMPAIGN           TARGETS             AUDIENCE
CAMPAIGN           TARGETS             GEOGRAPHY
IMPRESSION         SERVED_TO           HOUSEHOLD_REFERENCE
CONVERSION         ATTRIBUTED_TO       CAMPAIGN
ENTITY             VERIFIED_BY         SOURCE
```

Every relationship should support: `valid_from`, `valid_to`, `election_cycle_id`, `jurisdiction_id`, `source_id`, `source_url`, `confidence`, `recorded_at`, `last_verified_at`, and a change/audit record.

## Platform access hierarchy

```text
Platform owner
└── Organization owner
    ├── Agency administrator
    ├── Political client administrator
    ├── Media buyer
    ├── Audience analyst
    ├── Creative producer
    ├── Compliance reviewer
    ├── Data analyst
    ├── Finance user
    ├── Read-only client
    └── API application
```

Use row-level tenant isolation plus object-level permissions. Agency operators may be granted cross-client access only through explicit client assignments and logged justifications.
