# Cable Broadcaster Online Deployment Vendor Report

## Executive summary

Cable broadcasters generally deploy online through a multi-vendor stack rather than one platform. A typical system combines cloud infrastructure, live encoding, packaging/origin, linear playout, CDN delivery, OTT applications, entitlement and DRM, ad decisioning and server-side ad insertion, audience/identity controls, QoE measurement, and managed broadcast operations.

For the Ecosystem TV Broadcast category, the recommended strategy is to own the political intelligence, directory, compliance, campaign workflow, data governance, measurement, and reporting layer; use licensed partners for playout, delivery, inventory, SSAI, and consumer-device distribution.

## Vendor map

| Layer | Function | Vendors to evaluate |
|---|---|---|
| Cloud foundation | Compute, storage, network, security, disaster recovery | AWS, Google Cloud, Microsoft Azure |
| Contribution and live encoding | Receives broadcast feeds and produces ABR streams | AWS Elemental MediaLive, Harmonic, Ateme, Imagine Communications, Synamedia |
| Packaging and origin | HLS/DASH/CMAF packaging, DRM, DVR/time-shift, origin failover | AWS MediaPackage, Harmonic VOS360, Synamedia, Broadpeak, Unified Streaming |
| Linear playout | 24/7 channel scheduling, graphics, SCTE-35 markers, playlist operations | Amagi, Harmonic, Imagine, Veset, PlayBox Neo, Cinegy |
| Content delivery | Consumer-scale delivery and multi-CDN resilience | Akamai, CloudFront, Fastly, Cloudflare, Broadpeak |
| OTT/video platform | Catalog, metadata, VOD, publishing, player and application workflow | Comcast Technology Solutions/thePlatform, Brightcove, Kaltura, JW Player, Bitmovin |
| Pay-TV/TV Everywhere | Authentication, entitlement, subscriber and device integration | Synamedia, Comcast Technology Solutions, Evergent, operator-built systems |
| DRM/security | Content protection, license delivery, watermarking, anti-piracy | Synamedia, Verimatrix, Nagra, Irdeto, BuyDRM, EZDRM |
| Ad decisioning | Ad sales rights, inventory, forecasting, targeting, yield | FreeWheel, Google Ad Manager, Magnite, Microsoft Advertising/Xandr, SpringServe, Publica |
| SSAI | Server-side ad insertion and manifest manipulation | Google DAI, FreeWheel plus CTS, Harmonic VOS360 Ad, Broadpeak, AWS MediaTailor, Yospace |
| Audience/data | Identity, licensed segments, consent, activation | LiveRamp, Experian, TransUnion, Epsilon, Comscore, Nielsen |
| Measurement | Ratings, attribution, ad verification, QoE | Nielsen, Comscore, VideoAmp, iSpot, Conviva, Mux, NPAW |
| FAST distribution | Channel creation and distribution to FAST endpoints | Amagi, Wurl, Frequency, Veset, Harmonic, OTTera |
| Consumer endpoints | Final viewer environment and distribution surface | Roku Channel, Samsung TV Plus, Pluto TV, Tubi, LG Channels, Vizio WatchFree+, Fire TV Channels, Plex, Xumo Play |

## Reference architecture

```text
Live studio / master control / satellite / fiber contribution
        │
        ▼
Contribution ingest and redundant transport
        │
        ▼
Cloud or hybrid encoding
(MediaLive / Harmonic / Ateme / Synamedia)
        │
        ├── Cable/IPTV distribution
        ├── TV Everywhere authenticated application
        ├── Direct-to-consumer live application
        ├── VOD / catch-up library
        └── FAST channel feed
                 │
                 ▼
Packaging / origin / DRM / time-shift
        │
        ▼
Ad decisioning and server-side ad insertion
        │
        ▼
CDN or multi-CDN delivery
        │
        ▼
Roku / Fire TV / Apple TV / Samsung / LG / web / mobile / operator set-top boxes
        │
        ▼
QoE monitoring, ad measurement, billing, reporting, identity, and data feedback
```

## Vendor profiles

### AWS Elemental

**Role:** Cloud-native media processing and deployment foundation.

A common workflow is live contribution to AWS, encoding through MediaLive, packaging/origin through MediaPackage, ad insertion through MediaTailor where appropriate, and CDN distribution through CloudFront. AWS positions MediaLive for live-event and 24/7 linear channel encoding.

**Best for:** Proprietary cloud systems, infrastructure-as-code, multi-region resilience, data-platform integration, and teams with capable cloud/broadcast engineering.

**Caution:** AWS does not replace subscriber entitlement, apps, ad-sales operations, broadcast master control, programming operations, or content rights workflow by itself.

### Amagi

**Role:** Cloud playout, FAST-channel operations, scheduling, graphics, monitoring, advertising, analytics, and distribution.

**Best for:** Fast launch of a linear/FAST brand or transition of traditional broadcast workflows to cloud operations.

**Strategic value:** It is a strong benchmark for channel operations because it combines ingest, scheduling, branding, playout, monitoring, monetization, and FAST distribution in a managed cloud operating model.

### Harmonic VOS360

**Role:** Broadcast-grade media processing across cable, IPTV, satellite, terrestrial, streaming, live, and VOD workflows.

**Best for:** Hybrid broadcasters that need video processing across legacy broadcast distribution and OTT.

**Ad note:** Harmonic VOS360 Ad has a published FreeWheel integration for server-side ad insertion and in-stream advertising.

### Synamedia

**Role:** Pay-TV/video-network platform, security, device/subscriber operations, advanced advertising, and hybrid cable/IP video migration.

**Best for:** Cable operators or broadcasters that need deep integration with operator-grade systems, entitlement, DRM, device operations, and IP migration.

### Comcast Technology Solutions

**Role:** Managed video distribution, video publishing/syndication, TV Everywhere, broadcast-to-streaming operations, and advertising integrations.

**Best for:** Large broadcasters, cable networks, and rights holders requiring mature managed-service support, premium monetization, and video distribution operations.

### Brightcove

**Role:** Enterprise online-video platform for video management, VOD, live publishing, players, analytics, and branded applications.

**Best for:** Broadcasters needing an enterprise publishing/application platform rather than a complete cable-headend replacement.

### FreeWheel

**Role:** Premium multiscreen TV ad-tech, including video ad sales, rights, inventory, decisioning, programmatic connectivity, and TV/VOD monetization.

**Best for:** Premium cable/broadcaster advertising, TV Everywhere, VOD, connected-TV, and programmatic monetization.

### Google Ad Manager DAI

**Role:** Dynamic/server-side ad insertion for live and VOD streaming, including ad-pod serving and manifest-oriented delivery.

**Best for:** Broadcasters prioritizing scalable personalized streaming ads and programmatic demand.

## Deployment models

### A. FAST network launch

```text
Content library + live programming
→ Amagi / Wurl / Frequency / Harmonic cloud playout
→ SCTE-35 and ad workflow
→ FAST distribution
→ Roku Channel / Samsung TV Plus / Pluto / Tubi / LG / Vizio / Plex
→ Platform and third-party analytics
```

Use this for rapid launch of a free, ad-supported, scheduled channel.

### B. TV Everywhere

```text
Pay-TV subscriber / single sign-on
→ Authentication and entitlement
→ Live encoder + origin + DRM
→ Web / iOS / Android / Roku / Fire TV / Apple TV apps
→ CDN
→ Ad decisioning and SSAI
```

Use this for authenticated access tied to existing cable or IPTV subscriptions.

### C. Broadcaster-owned DTC service

```text
CMS / programming / MAM
→ Video platform and catalog
→ Live and VOD workflow
→ Identity + subscription + billing
→ DRM and entitlement
→ Apps and web
→ DAI / ad server
→ CDN
→ Product, ad, and QoE analytics
```

Use this where the broadcaster controls the direct viewer relationship, commerce, membership, subscriptions, advertising, or donations.

### D. Large hybrid broadcaster

```text
Legacy master control + satellite/cable plant
├── Affiliate and MVPD feeds
├── Cloud playout
├── OTT encoding/origin/CDN
├── DTC apps
├── TV Everywhere
├── FAST feeds
├── Addressable advertising
└── Shared identity, rights, measurement, CRM, and reporting
```

Use this for established networks that must serve legacy and internet distribution simultaneously.

## Ecosystem recommendation

### Build internally

- Political directory, public records, elections/races, districts, and relationship graph
- Campaign planning, compliance workflow, approval controls, source provenance, and audit logs
- Audience governance, segment metadata, consent/purpose control, suppression, and approval workflow
- Internal reporting, data model, outcome measurement, analyst tools, APIs, and executive dashboard
- Partner normalization layer that ingests licensed delivery, ad, and performance data

### Partner or buy

- Linear playout and master-control operations
- Premium video encoding, packaging, origin, DRM, and multi-CDN delivery
- Licensed CTV/DSP inventory and demand connectivity
- Server-side ad insertion and premium ad decisioning
- FAST endpoint onboarding and operational distribution
- Subscriber billing and TV Everywhere entitlement where a pay-TV integration is required

### Suggested first vendor evaluation wave

1. **Amagi** for FAST/channel-planning and cloud playout requirements.
2. **Harmonic** for broadcast-plus-streaming media processing and enterprise video workflows.
3. **AWS Elemental** for the internal cloud foundation, engineering control, and disaster-recovery model.
4. **FreeWheel** for premium broadcaster ad operations; **Google DAI** for programmatic streaming-ad insertion comparison.
5. **Synamedia** only when pay-TV operator, subscriber, DRM, device, or legacy cable integration becomes central.
6. **Brightcove or CTS** where managed OVP/application/publishing operations outweigh custom engineering needs.

## Decision criteria

Score each vendor by: deployment speed; linear/FAST versus VOD fit; traditional cable/IPTV compatibility; DRM/security; SSAI and ad-sales workflow; partner and endpoint coverage; data/API access; multi-region recovery; monitoring/NOC coverage; pricing model; contract portability; source data ownership; political-ad compliance support; and capacity to preserve a clean boundary between protected audience data and general platform analytics.

## Public sources

- AWS Broadcast & Live Production: https://aws.amazon.com/media/broadcast/
- AWS Elemental MediaLive: https://aws.amazon.com/medialive/
- AWS resilient live-streaming reference: https://aws.amazon.com/blogs/media/build-a-resilient-cross-region-live-streaming-architecture-on-aws/
- Amagi FAST distribution: https://www.amagi.com/blog/how-to-distribute-fast-channel
- Harmonic VOS360: https://www.digitalmediaworld.tv/awards/harmonic-vos360-cloud-saas-platform
- Harmonic / FreeWheel integration: https://investor.harmonicinc.com/news-releases/news-release-details/harmonics-vos360-ad-saas-validated-freewheel-transforming-video
- Synamedia hybrid IP/cable/DTH platform material: https://www.synamedia.com/wp-content/uploads/2019/12/improve-video-experience-with-infinite-entertainment-solution.pdf
- Comcast Technology Solutions / Harmonic: https://www.comcasttechnologysolutions.com/partners/harmonic
- Comcast Technology Solutions / FreeWheel MRM: https://www.comcasttechnologysolutions.com/partners/freewheel-mrm
- Google Ad Manager DAI: https://developers.google.com/ad-manager/dynamic-ad-insertion
- Google DAI feature material: https://admanager.google.com/home/resources/feature-brief-dynamic-ad-insertion/
- FreeWheel / Comcast Advertising: https://comcastadvertising.com/about-us/
- Brightcove / UKTV: https://www.brightcove.com/customers/uktv
