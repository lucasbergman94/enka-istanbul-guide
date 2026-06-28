#!/usr/bin/env python3
"""Rewrite neighborhood blurbs to neutral/factual (remove opinions) and add
district/mahalle slugs for rental-search deep links. Preserves coordinates."""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "data.json")

DSLUG = {"Sarıyer": "sariyer", "Beşiktaş": "besiktas", "Şişli": "sisli", "Beyoğlu": "beyoglu"}

# name -> (oneLiner, desc, mahalleSlug, caveat-or-None to override)
N = {
 "Çamlıtepe / Hacıosman": ("Residential, by Hacıosman metro", "Residential area beside Hacıosman metro station (M2), with local amenities. Sarıyer district.", "haciosman", ""),
 "Tarabya": ("Bosphorus waterfront area", "Waterfront neighborhood on the Bosphorus with restaurants and a promenade; several former consulate residences. Higher rents.", "tarabya", ""),
 "Kireçburnu": ("Bosphorus waterfront, seafood", "Small waterfront area in Sarıyer known for seafood restaurants.", "kirecburnu", "Further from the service-bus stops."),
 "Darüşşafaka": ("Residential, by Darüşşafaka metro", "Residential area by Darüşşafaka metro station (M2). Includes housing compounds such as Gazeticiler Sitesi.", "darussafaka", ""),
 "Emirgan": ("Bosphorus village with a large park", "Bosphorus neighborhood in Sarıyer with Emirgan Park and waterfront restaurants. Higher rents.", "emirgan", ""),
 "Maslak": ("Business district; limited housing", "Business and office district. Some gated residential compounds nearby.", "maslak", "Limited residential stock in Maslak proper."),
 "Poligon": ("Close to the school", "Residential area in Sarıyer close to the school, with lower-cost options.", "poligon", "Streets vary; check Google Street View."),
 "Reşitpaşa": ("Residential, near Maslak", "Residential area in Sarıyer near Maslak, with lower-cost options.", "resitpasa", "Streets vary; check Google Street View."),
 "Yeniköy": ("Bosphorus village", "Bosphorus neighborhood in Sarıyer. Higher rents.", "yenikoy", ""),
 "İstinye": ("Walkable to school; İstinye Park mall", "Bosphorus neighborhood in Sarıyer with the İstinye Park shopping mall. Walking distance to the school.", "istinye", "The walk to school is uphill."),
 "Baltalimanı": ("Small Bosphorus cove; no metro", "Small Bosphorus cove between Emirgan and Rumelihisarı; mostly older villas and garden apartments.", "baltalimani", "No metro; infrequent buses; main retail is in Emirgan/İstinye (10–15 min)."),
 "Levent": ("Business and shopping hub; M2 metro", "Dense business and shopping area on the M2 metro line, with international restaurants and malls.", "levent", ""),
 "Nisbetiye": ("Low-rise residential near Levent", "Low-rise residential area between Levent and Etiler, with embassies. Walkable.", "nisbetiye", ""),
 "Bebek": ("Bosphorus-front; international community", "Bosphorus-front neighborhood in Beşiktaş with a seafront promenade and cafés; established international community. Higher rents.", "bebek", ""),
 "Etiler": ("Residential; international community", "Residential district in Beşiktaş with restaurants and private schools; established international community.", "etiler", ""),
 "Esentepe": ("Mixed business/residential; near the stop", "Mixed business and residential district near Zincirlikuyu, with high-rise housing and good connectivity (Zorlu Centre nearby).", "esentepe", ""),
 "Balmumcu": ("Residential, central", "Residential area between Zincirlikuyu and Beşiktaş, near Zorlu Centre.", "balmumcu", ""),
 "Arnavutköy": ("Bosphorus village, older housing", "Bosphorus village in Beşiktaş with 19th-century wooden houses and a fishing harbour.", "arnavutkoy", "Older housing stock; car/bus dependent."),
 "Kuruçeşme": ("Bosphorus-front strip", "Narrow Bosphorus-front strip in Beşiktaş with restaurants and clubs.", "kurucesme", "Limited residential stock; higher rents."),
 "Kültür": ("Residential hills near Etiler", "Low-rise residential area in the hills between Etiler and the Bosphorus ridge.", "kultur", ""),
 "Rumelihisarı": ("Bosphorus, by Boğaziçi University", "Bosphorus neighborhood by the historic fortress and Boğaziçi University; waterfront fish restaurants.", "rumelihisari", "Small area, limited retail."),
 "Gayrettepe": ("Well-connected (M2 + metrobüs)", "Mixed business/residential area connected by M2 metro and metrobüs, with mid-range apartments.", "gayrettepe", ""),
 "Dikilitaş": ("Residential near Beşiktaş centre", "Compact residential area between Balmumcu and Beşiktaş centre, near the ferry and metrobüs.", "dikilitas", ""),
 "Akatlar": ("Residential; supermarkets, parks", "Established residential district near 1. Levent with large supermarkets (Migros, CarrefourSA) and parks.", "akatlar", ""),
 "Mecidiyeköy": ("Major transit hub", "Dense, central district and major transit hub (metrobüs, M2 metro, many buses).", "mecidiyekoy", ""),
 "19 Mayıs": ("Residential near Mecidiyeköy", "Residential area northeast of Mecidiyeköy with everyday infrastructure; mid-range rents.", "19-mayis", ""),
 "İzzet Paşa": ("Residential, central", "Small residential area near Şişli/Mecidiyeköy with local shops; central.", "izzet-pasa", ""),
 "Şişli (merkez)": ("Commercial centre; hospitals", "Commercial centre of Şişli with department stores, private hospitals and consulates; mid-range rents.", "merkez", ""),
 "Teşvikiye & Meşrutiyet": ("Upscale, near Nişantaşı", "Upscale residential area near Nişantaşı with boutiques and private clinics; older prestige buildings. Higher rents.", "tesvikiye", ""),
 "Harbiye & Halaskargazi": ("Central, well-connected", "Central area between Taksim, Nişantaşı and Şişli, with good bus and metro access.", "harbiye", ""),
 "Abbasağa & Vişnezade": ("Hillside residential near Beşiktaş", "Hillside residential areas inland from Beşiktaş, with a park, cafés and bars.", "abbasaga", ""),
 "Beşiktaş (merkez)": ("Central; ferry, market, stadium", "Central, busy district with a ferry terminal, fish market and stadium; strong connectivity (ferry to Asia, metrobüs, buses).", "merkez", "Busy; stadium matchdays are loud."),
 "Cihannüma": ("Hilltop residential above Beşiktaş", "Residential area on the ridge above Beşiktaş with views; about a 10-minute walk down to the centre.", "cihannuma", "The walk back up is steep."),
 "Bomonti & Feriköy": ("Residential; organic market; M2 access", "Adjacent residential areas with bars, studios and the Feriköy organic market; M2 access via Osmanbey/Şişli.", "bomonti", ""),
 "İnönü & Gümüşsuyu": ("Steep, central, near Kabataş", "Steep central areas between Taksim and Kabataş, with Bosphorus views and the Kabataş metrobüs/tram interchange.", "gumussuyu", "Steep terrain."),
 "Cihangir": ("Central; café culture; expat-known", "Central Beyoğlu neighborhood known for cafés and an international community; English is widely spoken.", "cihangir", "Steep streets; older buildings; rents have risen."),
}

d = json.load(open(OUT, encoding="utf-8"))
miss = []
for n in d["neighborhoods"]:
    if n["name"] in N:
        ol, desc, mslug, cav = N[n["name"]]
        n["oneLiner"] = ol
        n["desc"] = desc
        n["caveat"] = cav
        n["mahalleSlug"] = mslug
        n["districtSlug"] = DSLUG.get(n["district"], "")
    else:
        miss.append(n["name"])
json.dump(d, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("patched:", len(d["neighborhoods"]) - len(miss), "missing:", miss or "none")
