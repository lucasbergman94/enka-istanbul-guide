# ENKA Istanbul - New Teacher Guide

A guide + interactive map for **new teachers moving to ENKA Schools Istanbul**.

**Live site:** https://lucasbergman94.github.io/guia-ist/

## Pages
- **`index.html`** - the guide: contacts, a message board, and click-to-expand sections
  (documents, work-visa steps, housing, arrival, daily life, FAQ, glossary, links).
- **`map.html`** - interactive housing & commute map: school + 9 bus stops + ~36
  neighborhoods. Click a neighborhood for a modal (neutral notes + "explore nearby" Google
  Maps links + rental searches). Type an address (or "use my location") to find the nearest
  stop and get two routes (home → stop, stop → school). Filters by price / stop / walk-to-school.

## How to edit (no code needed for these)
- **Message board:** edit `messages.json` (array of `{date, title, body, pinned}`).
- **Contacts:** edit `contacts.json`.
- **Neighborhoods:** edit `data.json` (or edit `data_src.json` + run `python3 geocode.py`,
  then `python3 patch_neutral.py`). After editing, commit and push.

## Notes
- No API keys: tiles from OpenStreetMap; routing via Google Maps deep links; address lookup
  via OpenStreetMap Nominatim.
- Live rental listings can't be embedded (Sahibinden/Hepsiemlak block automated access), so
  the map deep-links to a filtered search on those sites instead.
- Pin locations are auto-geocoded and may be slightly off - verify before deciding.
- Bus schedule/times: confirm with the school.

Built with Leaflet. Content is factual; specifics should be confirmed with HR.
