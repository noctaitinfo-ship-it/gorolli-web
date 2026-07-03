# GoRolli Public Live Map — product + implementation plan

**Product logic confirmed:** homepage = marketplace front door. Renter sees real trailers on a real map, picks one, and continues straight into booking on client web. App = retention bonus, never the gate.

**Honesty rule (in force today):** the public inventory API and the client `/find` route do **not** exist yet. Until they do, the homepage keeps the labeled illustrative preview + direct route to client web (`live_map:false`). No fake pins, ever.

**Feasibility split:** gorolli-web alone CANNOT deliver this. It needs (A) a public read-only API in the app backend, (B) the `/find` (+ deep-link) page in the FlutterFlow client app, (C) the Map Lite widget in gorolli-web. Only (C) lives in this repo.

---

## 1 · Public API (backend work — same source of truth as the apps)

Implemented next to the existing app backend (FlutterFlow apps → Firebase: a Cloud Function reading the SAME Firestore collections the mobile apps use; no separate inventory, ever), fronted by Cloudflare edge cache.

```
GET /api/public/trailers/nearby?lat=58.378&lng=26.729&r=10000&lang=et&category=open
GET /api/public/trailers/bbox?north=..&south=..&east=..&west=..&category=..&lang=et   (Phase 3 pan/zoom)
```

Response (superset of the old /api/home/nearby contract in REDESIGN-NOTES §3, which this SUPERSEDES — summary fields keep the existing flag-gated homepage code working unchanged; `trailers[]` powers Map Lite):

```json
{
  "count": 12,
  "updated_at": "2026-07-03T14:00:00Z",
  "ttl_seconds": 15,
  "min_price": {"amount": 5, "currency": "EUR"},
  "nearest_km": 1.4,
  "trailers": [
    {
      "id": "opaque_public_id",
      "type": "closed",
      "category": "box",
      "lat": 58.37, "lng": 26.72, "approx": true,
      "price_from": 5, "currency": "EUR",
      "distance_km": 1.4,
      "available_now": true,
      "image_url": "https://…/public-thumb.jpg",
      "rating": 4.8,
      "booking_url": "https://client.gorolli.com/find?lang=et&trailer_id=opaque_public_id&open=booking"
    }
  ]
}
```

Server rules:
- Anonymous, GET-only, CORS `Access-Control-Allow-Origin: https://www.gorolli.com`.
- `Cache-Control: public, s-maxage=15, stale-while-revalidate=30` → Cloudflare caches per (rounded lat/lng, r, category, lang).
- Coordinates rounded server-side to ~300 m grid with a per-trailer **stable** jitter (pin must not jump between refreshes).
- Max 50 pins (100 hard cap); if more, return densest/nearest 50 + honest `count`.
- `id` is an opaque public id (random doc id or HMAC of internal id) — never sequential/internal ids.
- `lang` localizes only server-provided display strings if any; category codes stay stable (`open|closed|boat|camper|construction`).
- Rate limiting at Cloudflare (e.g. 30 req/min/IP) — cache makes real load trivial.

## 2 · Client web route (FlutterFlow work — extends client-web-find-requirements.md)

`/find` accepts, in addition to `lang/city/lat/lng`:
- **`trailer_id`** (opaque public id) → on load: focus that trailer, open its detail sheet.
- **`open=booking`** → after focusing, continue straight into the booking flow; auth prompt appears HERE (booking start), and after login the user returns to the SAME trailer/booking (FlutterFlow: preserve pending route + params through auth).
- Unknown/expired `trailer_id` → plain `/find` view centered on `lat/lng` if present — never an error page, never app install.

## 3 · Selected-trailer preservation (homepage → booking)

The API returns a ready `booking_url` per trailer (server-composed, always current). The homepage bottom sheet's "Book this trailer" CTA is a plain `<a href="{booking_url}">` with `lang` swapped by the existing language system. One source of truth for the deep-link format = the backend; the homepage never assembles trailer URLs beyond appending `lang`. If `booking_url` is missing → fall back to `/find?lang=xx&lat&lng`.

## 4 · Homepage Map Lite (gorolli-web work — Phase 3)

- **No iframe.** A lightweight widget inside the existing `.mappanel` container, flag-gated by `GOROLLI_FLAGS.live_map`.
- Library: Leaflet (~42 KB gz) **lazy-loaded only after the user taps "Show trailers"** (user intent = the current CTA). Before intent: today's inline SVG preview (zero JS) stays — first paint unchanged. Tiles: MapTiler/Stadia free tier or self-hosted Protomaps on R2 — NOT raw openstreetmap.org tiles (usage policy).
- Flow: tap CTA → geolocation ask → granted: init map centered on user, fetch `nearby`, render ≤50 pins + category filter pills (from `i18n/finder-strings.json`: `cat_all cat_open cat_closed cat_boat cat_camper cat_construction`) → tap pin → bottom sheet (type, ≈distance, price from, `available_now`, public thumb, rating, **Book this trailer** → `booking_url`).
- GPS denied → city input (existing state) → `/find?lang&city=…`. No geolocation before the tap, same as today.
- Pan/zoom → `bbox` endpoint, debounced 600 ms; refresh every 15 s ONLY while `document.visibilityState==='visible'` (pause on hidden tab); all UI strings from the i18n dictionary and marked `notranslate` (Google Translate must not touch the live widget).
- Map area is additive: existing hero, CTA-as-link JS-off fallback, and the `.mstate` machine remain the degradation path.

## 5 · Caching / 500+ concurrent users

Load math: 500 visible tabs polling /15 s ≈ 33 req/s at the edge; coords rounded to 3 decimals + fixed radius buckets → most requests share cache keys in a city → **>95 % Cloudflare cache hit**, origin sees ~a few req/s per hot city per TTL window. Cloud Function stays cold-start-class cheap. Pan/zoom bbox requests are debounced and also cached. No websockets, no server push — TTL polling is enough for "live" inventory.

## 6 · Privacy (public map = shop window, not the ledger)

Public: approximate pin (server-rounded + stable jitter), opaque id, type/category, price from, availability boolean, approved public photo, ≈distance, public rating.
Never before a valid booking: exact address/coords, owner phone/email/private name, documents, availability internals. Exact address is revealed only inside the booking flow after auth — same rule the homepage already promises ("täpne aadress pärast broneeringut").

## 7 · Fallbacks (never a dead end, never an install wall)

| Failure | Behavior |
|---|---|
| API down / 4xx/5xx / timeout | CTA becomes plain link → `client.gorolli.com/find?lang=xx` (root until /find exists) |
| GPS denied | city input → `/find?lang&city=…` |
| No geolocation support | direct to client web |
| 0 trailers nearby | wider-radius re-query + honest host invite (existing state) |
| Tiles fail to load | pins on plain background + same CTAs; or fall back to client web |
| JS disabled | static page, CTA is a real `<a>` (unchanged today) |
| live_map flag off | today's behavior: labeled illustrative preview + direct route |

## 8 · Language behavior (all 32)

Homepage UI incl. map pills/sheet: `GR_I18N` + `i18n/finder-strings.json` (now includes the 8 map keys ×32); rest of page keeps Google Translate fallback. Every language switch already rewrites `?lang=` on all client/host links and `&hl=` on Play links — `booking_url` gets its `lang` swapped by the same mechanism. Finnish user: FI hero + FI pills/sheet instantly, FI via GT elsewhere, `client.gorolli.com/find?lang=fi&trailer_id=…`, Play `&hl=fi`. Map place-name labels follow the tile provider (MapTiler supports a language parameter; OSM shows local endonyms) — documented limitation, not a blocker.

## 9 · Phases

| Phase | What | Where | Status |
|---|---|---|---|
| **1** | Safe preview + direct route to client web, honest labels, flag off | gorolli-web | ✅ LIVE in branch files now |
| **2** | Public no-login `/find` (lang/city/lat/lng) + metadata fix | FlutterFlow client | Spec ready (`client-web-find-requirements.md`); ~1 day |
| **3** | Public API + Map Lite on homepage (lazy Leaflet, pins, filters, sheet) | Backend + gorolli-web | API spec above; homepage scaffold (state machine, flag, i18n strings) already in place; ~2–4 days backend + ~2 days web |
| **4** | Booking deep-link (`trailer_id` + `open=booking`) end-to-end incl. auth-return | FlutterFlow client + API | Spec above; ~1–2 days |

Gate for flipping `live_map:true`: Phases 2+3 tested (API cached, CORS, ≤50 pins, stable jitter verified; /find live). Gate for Phase 4 CTA: deep-link auth-return tested on iPhone Safari + Chrome Android.

## 10 · What changed in the repo today (safe, zero-behavior)

- This plan file.
- `i18n/finder-strings.json`: +8 map-UI keys × 32 languages (52 keys total).
- `index.html`: two comment/contract strings updated to the new endpoint name (`/api/public/trailers/nearby`) — flag still `false`, no logic touched.
- `client-web-find-requirements.md`: `/find` params extended with `trailer_id` + `open=booking`.
- `REDESIGN-NOTES.md`: §3 marked superseded by this plan.
