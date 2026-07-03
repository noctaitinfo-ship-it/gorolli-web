# client.gorolli.com/find — public search route: implementation requirements

**Status: NOT yet implementable from this repo.** client.gorolli.com is a FlutterFlow app on FlutterFlow prod hosting. Its pages, auth gates and metadata are defined in the FlutterFlow project — not in `gorolli-web`. This document is the exact build spec. The homepage side is already prepared and flips with one constant (§6).

## 0 · Verified current state (probed 2026-07-03)
- `/` and `/find` serve the identical SPA shell → path-based routing, catch-all; no dedicated find page exists yet (or it is not distinguishable from outside).
- `<title>GoRolli2</title>`, `meta description "Built with FlutterFlow."`, OG title `GoRolli2`, OG image = FlutterFlow splash gradient, **`meta robots noindex`**.
- `manifest.json`: name/short_name `GoRolli2`, description `A new Flutter project.`, Flutter-default blue `#0175C2`, `.jpg` launcher icon.
- No `robots.txt` (shell is served for it).
- Consequence: every renter the homepage sends over lands on a tab called "GoRolli2 — Built with FlutterFlow". Fix is FlutterFlow settings work, ~1 hour total including the page.

## 1 · Route
Create page **FindPage** in the FlutterFlow client project:
- Route path: **`/find`** (Page Settings → Route Settings → Path). Verify web URLs use path strategy (they do today).
- **No auth guard**: Page Settings → uncheck "Requires Authentication". Anonymous visitors must see the map/search.
- Page parameters (Page Settings → Route Settings → Parameters, all optional, type String except lat/lng double):
  | Param | Type | Meaning |
  |---|---|---|
  | `lang` | String | UI language code (et, en, de, fi, lv, lt, pl, …) |
  | `city` | String | Free-text city/address to search by |
  | `lat` | double | Map center latitude (comes rounded to 3 decimals) |
  | `lng` | double | Map center longitude (rounded to 3 decimals) |

Examples that must work:
`/find?lang=et` · `/find?lang=fi` · `/find?lang=de` · `/find?lang=et&city=Tartu` · `/find?lang=et&lat=58.378&lng=26.729`

## 2 · Page On Load actions (in order)
1. **Language**: if `lang` param present and supported → action **Set App Language** = `lang`. Unknown/missing → keep existing detection (device/app default). Must match the 32-language codes used by the homepage (he/zh arrive as `he`/`zh` — map internally if the app uses `iw`/`zh-CN`).
2. **Map center**:
   - `lat` & `lng` present → center map widget there, default radius (5 km), run nearby query.
   - else `city` present → put value in the search field and run the existing city/geocode search (same logic the app's search screen uses).
   - else → default view (country-level or IP-based, whatever the client app already does — do not invent new logic).
3. Load trailers with the **same backend queries the mobile client uses** (same Firestore/API collections, same availability logic). No web-specific fork.

## 3 · What the page shows (reuse existing client components)
Categories, radius control, available trailers with price, and each trailer's booking entry point — the existing client search/map experience. This is a routing + auth-gate task, not a new UI.

**Login gating**: browsing, map, categories, prices = anonymous. Auth is requested only when the user starts a booking (on the booking action, deep-link back to the same trailer after login). Never before search.

**Privacy (must match homepage promise "täpne aadress pärast broneeringut")**: public pins/list show approximate locations only (server-rounded coords, per the `/api/home/nearby` contract in REDESIGN-NOTES §3 — no IDs/addresses/host names in anonymous responses). Exact address is revealed only inside a valid booking flow.

## 4 · Metadata fixes (FlutterFlow → Settings)
| Where | Set to |
|---|---|
| App Details → App Name | `GoRolli` (kills "GoRolli2" in manifest + apple-mobile-web-app-title) |
| Web Publishing → Page Title | `GoRolli — leia haagis lähedalt` |
| Web Publishing → Description | `Leia haagis lähedalt. Broneeri veebis või äpis.` |
| Web Publishing → OG/social image | branded GoRolli image (reuse `https://www.gorolli.com/screenshots/host-t1.png` or a dedicated 1200×630) |
| Web Publishing → Favicon | GoRolli favicon (the yellow trailer mark, not the default jpg) |
| Web Publishing → "Exclude from search engines" / noindex | **OFF** if `/find` should rank (recommended: index `/find`, since it's the public landing); keep account/booking pages noindexed if per-page SEO is available |
| Theme color | `#0A1F3D` (navy, matches gorolli.com) instead of Flutter blue |

Republish web after changing — FlutterFlow regenerates `index.html` + `manifest.json` from these settings.

**Edge fallback (only if FlutterFlow settings prove too limited, e.g. for per-language titles):** a Cloudflare Worker/Snippet on `client.gorolli.com/*` using HTMLRewriter can override `<title>`, description, OG tags and strip `noindex` at the edge without touching FlutterFlow. Don't do this first — settings are the clean path. (Per project rules: no Cloudflare changes made by this pass; this is documentation.)

## 5 · Explicit non-goals (protect existing behavior)
- No changes to existing client app pages, map logic, categories, booking flow or data model.
- No app-install interstitial, no smart-app-banner gating, no store links as the primary action on `/find`. App promotion stays secondary (footer/banner-after-search at most).

## 6 · Homepage flip (this repo — do AFTER /find is live)
1. `index.html`: set `var GR_FIND_PATH='/find';` (finder script — one line, already scaffolded).
2. `index.html` `grAppLinks` (PRESERVED block — this becomes its first sanctioned edit; test the full language checklist after): the client-link rewrite currently resets every client URL to the root. Replace the client line with a path-preserving rewrite so the hero CTA keeps `/find` while other client links keep their own paths:
   ```js
   document.querySelectorAll('a[href^="https://client.gorolli.com"]').forEach(function(a){
     var u=new URL(a.href); u.searchParams.set('lang',lang); a.href=u.toString();
   });
   ```
   (Apply the same pattern to the host line for symmetry, or leave host as-is — host links are all root.)
3. Hero CTA static hrefs → `https://client.gorolli.com/find?lang=xx`: `index.html` (1) + 7 static pages (1 each). Leave the app-card "Ava veebis" buttons on the root.
4. Re-run REDESIGN-NOTES §5 + §I7 checklists (especially: language switch still rewrites all links, `?lang` present, `/find` preserved).

## 7 · Test steps (client web, after FlutterFlow publish)
1. Incognito, phone + desktop: open `/find?lang=et` → map/search visible, **no login wall**, Estonian UI.
2. `/find?lang=fi`, `/find?lang=de` → Finnish/German UI.
3. `/find?lang=et&lat=58.378&lng=26.729` → map centered on Tartu area, nearby trailers listed with prices.
4. `/find?lang=et&city=Tartu` → city search applied.
5. Unknown params (`/find?lang=xx&city=%%%`) → page still loads with defaults, no crash.
6. Tap a trailer → details show approximate location only; start booking → NOW login appears; after login you land back in the same booking.
7. View-source of `/find`: title `GoRolli — leia haagis lähedalt`, GoRolli description/OG, **no noindex**; manifest name `GoRolli`.
8. Compare listed trailers/availability against the mobile client app — must match.
9. Regression: existing logged-in web flows (login, bookings, profile) unchanged.
