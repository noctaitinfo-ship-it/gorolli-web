from pathlib import Path
from html import escape
from datetime import date
import re

BASE = "https://www.gorolli.com"
CLIENT = "https://client.gorolli.com"
HOST = "https://host.gorolli.com"

langs = [
    ("en", "English", "en"),
    ("et", "Eesti", "et"),
    ("de", "Deutsch", "de"),
    ("pl", "Polski", "pl"),
    ("lv", "Latviešu", "lv"),
    ("fi", "Suomi", "fi"),
    ("lt", "Lietuvių", "lt"),
    ("ru", "Русский", "ru"),
    ("sv", "Svenska", "sv"),
    ("da", "Dansk", "da"),
    ("uk", "Українська", "uk"),
    ("es", "Español", "es"),
    ("fr", "Français", "fr"),
    ("it", "Italiano", "it"),
    ("nl", "Nederlands", "nl"),
    ("pt", "Português", "pt"),
    ("cs", "Čeština", "cs"),
    ("sk", "Slovenčina", "sk"),
    ("hu", "Magyar", "hu"),
    ("ro", "Română", "ro"),
    ("bg", "Български", "bg"),
    ("tr", "Türkçe", "tr"),
    ("el", "Ελληνικά", "el"),
    ("hr", "Hrvatski", "hr"),
    ("sl", "Slovenščina", "sl"),
    ("sr", "Српски", "sr"),
    ("ar", "العربية", "ar"),
    ("he", "עברית", "he"),
    ("hi", "हिन्दी", "hi"),
    ("zh", "中文", "zh"),
    ("ja", "日本語", "ja"),
    ("ko", "한국어", "ko"),
]

T = {
"en": {"title":"GoRolli — Trailer Rental App | Rent a Trailer Near You","desc":"GoRolli is a trailer rental and sharing platform. Rent a trailer near you in minutes, or earn by listing your own. One app, on Android and iOS.","h1":"Trailer rental made simple","lead":"GoRolli is a peer-to-peer trailer rental platform. Find and book a trailer near you in minutes — cargo trailers, boat trailers or caravans — or list your own trailer and earn. Everything in one app.","rent":"Rent a trailer nearby","rentp":"See available trailers nearby, clear prices and book in minutes. Choose the right type and pay securely in the app.","host":"Earn with your trailer","hostp":"List the trailer in your yard and earn passive income. You control price and availability.","play":"Get it on Google Play","store":"App Store","webc":"Open Client app in browser","webh":"Open Host app in browser","how":"How it works","steps":["Open the GoRolli client or host app.","Customers search and book nearby; hosts list trailers and manage availability.","Pick up, use and return — payments and invoices run through the app."],"kw":"Popular searches: trailer rental, rent a trailer, trailer sharing platform.","foot":"Terms · Privacy"},
"et": {"title":"GoRolli — haagise rendi app | Haagise rent lähedalt","desc":"GoRolli on haagise rendi ja jagamise platvorm. Rendi haagis lähedalt mõne minutiga või teeni oma haagisega. Üks app Androidile ja iOS-ile.","h1":"Haagise rent lihtsalt","lead":"GoRolli on haagiste jagamis- ja rendiplatvorm. Leia ja broneeri haagis enda lähedalt mõne minutiga — kaubahaagis, paadihaagis või haagissuvila — või lisa oma haagis ja teeni tulu.","rent":"Rendi haagis lähedalt","rentp":"Vaata lähedal olevaid vabu haagiseid, hindu ja broneeri minutitega. Vali sobiv tüüp ja maksa turvaliselt appis.","host":"Teeni oma haagisega","hostp":"Lisa oma haagis platvormile ja teeni passiivset tulu. Hind ja saadavus on sinu kontrollis.","play":"Lae alla Google Play","store":"App Store","webc":"Ava kliendi app brauseris","webh":"Ava hosti app brauseris","how":"Kuidas see töötab","steps":["Ava GoRolli kliendi või hosti app.","Klient otsib ja broneerib lähedalt; host lisab haagise ja haldab saadavust.","Võta vastu, kasuta ja tagasta — maksed ja arved liiguvad appis."],"kw":"Populaarsed otsingud: haagise rent, järelkäru rent, haagise jagamise platvorm.","foot":"Tingimused · Privaatsus"},
"de": {"title":"GoRolli — Anhänger mieten App | Anhängervermietung in der Nähe","desc":"GoRolli ist eine Plattform zur Anhängervermietung. Mieten Sie einen Anhänger in der Nähe in wenigen Minuten oder verdienen Sie mit Ihrem eigenen. Eine App für Android und iOS.","h1":"Anhänger mieten — einfach gemacht","lead":"GoRolli ist eine Peer-to-Peer-Plattform für Anhängervermietung. Finden und buchen Sie einen Anhänger in Ihrer Nähe in wenigen Minuten — Lastenanhänger, Bootsanhänger oder Wohnwagen — oder bieten Sie Ihren eigenen Anhänger an und verdienen Sie dazu.","rent":"Anhänger in der Nähe mieten","rentp":"Verfügbare Anhänger in der Nähe ansehen, klare Preise sehen und in Minuten buchen. Wählen Sie den passenden Typ und zahlen Sie sicher in der App.","host":"Mit Ihrem Anhänger verdienen","hostp":"Bieten Sie Ihren Anhänger an und verdienen Sie passives Einkommen. Sie legen Preis und Verfügbarkeit fest.","play":"Laden im Google Play","store":"App Store","webc":"Client-App im Browser öffnen","webh":"Host-App im Browser öffnen","how":"So funktioniert es","steps":["Öffnen Sie die GoRolli Kunden- oder Host-App.","Mieter suchen und buchen in der Nähe; Gastgeber verwalten Anhänger und Verfügbarkeit.","Abholen, nutzen und zurückgeben — Zahlungen und Rechnungen laufen über die App."],"kw":"Beliebte Suchen: Anhänger mieten, Anhängervermietung.","foot":"AGB · Datenschutz"},
"pl": {"title":"GoRolli — aplikacja do wynajmu przyczep","desc":"GoRolli to platforma wynajmu i udostępniania przyczep. Wynajmij przyczepę w pobliżu lub zarabiaj na własnej.","h1":"Prosty wynajem przyczep","lead":"GoRolli pomaga znaleźć i zarezerwować przyczepę w pobliżu w kilka minut albo wystawić własną przyczepę i zarabiać.","rent":"Wynajmij przyczepę w pobliżu","rentp":"Zobacz dostępne przyczepy, ceny i zarezerwuj bezpiecznie w aplikacji.","host":"Zarabiaj na swojej przyczepie","hostp":"Dodaj swoją przyczepę, ustaw cenę i dostępność oraz zarabiaj pasywnie.","play":"Pobierz z Google Play","store":"App Store","webc":"Otwórz aplikację klienta w przeglądarce","webh":"Otwórz aplikację hosta w przeglądarce","how":"Jak to działa","steps":["Otwórz aplikację klienta lub hosta GoRolli.","Klienci rezerwują w pobliżu; host zarządza przyczepami.","Odbiór, użycie i zwrot — płatności działają w aplikacji."],"kw":"Popularne wyszukiwania: wynajem przyczep, wypożyczalnia przyczep.","foot":"Warunki · Prywatność"},
"lv": {"title":"GoRolli — piekabju nomas lietotne","desc":"GoRolli ir piekabju nomas un koplietošanas platforma. Iznomā piekabi tuvumā vai pelni ar savu piekabi.","h1":"Piekabju noma vienkārši","lead":"GoRolli palīdz ātri atrast un rezervēt piekabi tuvumā vai pievienot savu piekabi un pelnīt.","rent":"Iznomā piekabi tuvumā","rentp":"Skati pieejamās piekabes, cenas un rezervē droši lietotnē.","host":"Pelni ar savu piekabi","hostp":"Pievieno savu piekabi, nosaki cenu un pieejamību.","play":"Lejupielādēt Google Play","store":"App Store","webc":"Atvērt klienta lietotni pārlūkā","webh":"Atvērt hosta lietotni pārlūkā","how":"Kā tas darbojas","steps":["Atver GoRolli klienta vai hosta lietotni.","Klienti rezervē tuvumā; hosti pārvalda piekabes.","Saņem, izmanto un atgriez — maksājumi notiek lietotnē."],"kw":"Populāri meklējumi: piekabju noma, iznomāt piekabi.","foot":"Noteikumi · Privātums"},
"fi": {"title":"GoRolli — peräkärryn vuokraussovellus","desc":"GoRolli on peräkärryjen vuokraus- ja jakamisalusta. Vuokraa peräkärry läheltä tai ansaitse omalla peräkärrylläsi.","h1":"Peräkärryn vuokraus helposti","lead":"GoRolli auttaa löytämään ja varaamaan peräkärryn läheltä muutamassa minuutissa tai tarjoamaan oman peräkärryn vuokralle.","rent":"Vuokraa peräkärry läheltä","rentp":"Näe vapaat peräkärryt, hinnat ja varaa turvallisesti sovelluksessa.","host":"Ansaitse peräkärrylläsi","hostp":"Lisää oma peräkärry, määritä hinta ja saatavuus.","play":"Lataa Google Play","store":"App Store","webc":"Avaa asiakassovellus selaimessa","webh":"Avaa host-sovellus selaimessa","how":"Näin se toimii","steps":["Avaa GoRolli asiakas- tai host-sovellus.","Asiakkaat varaavat läheltä; hostit hallitsevat peräkärryjä.","Nouda, käytä ja palauta — maksut hoituvat sovelluksessa."],"kw":"Suositut haut: peräkärryn vuokraus, vuokraa peräkärry.","foot":"Ehdot · Tietosuoja"},
"lt": {"title":"GoRolli — priekabų nuomos programėlė","desc":"GoRolli yra priekabų nuomos ir dalijimosi platforma. Išsinuomokite priekabą netoliese arba uždirbkite su savo priekaba.","h1":"Paprasta priekabų nuoma","lead":"GoRolli padeda greitai rasti ir rezervuoti priekabą netoliese arba įkelti savo priekabą ir uždirbti.","rent":"Išsinuomokite priekabą netoliese","rentp":"Matykite laisvas priekabas, kainas ir rezervuokite saugiai programėlėje.","host":"Uždirbkite su savo priekaba","hostp":"Įkelkite savo priekabą, nustatykite kainą ir prieinamumą.","play":"Atsisiųsti Google Play","store":"App Store","webc":"Atidaryti kliento programą naršyklėje","webh":"Atidaryti hosto programą naršyklėje","how":"Kaip tai veikia","steps":["Atidarykite GoRolli kliento arba hosto programą.","Klientai rezervuoja netoliese; hostai valdo priekabas.","Pasiimkite, naudokite ir grąžinkite — mokėjimai vyksta programėlėje."],"kw":"Populiarios paieškos: priekabų nuoma, išsinuomoti priekabą.","foot":"Sąlygos · Privatumas"},
}

fallbacks = {
"ru":("Простой прокат прицепов","Арендуйте прицеп рядом или зарабатывайте на собственном прицепе.","Арендовать прицеп","Зарабатывать как владелец","Открыть клиентское приложение","Открыть приложение владельца"),
"sv":("Enkel släpvagnsuthyrning","Hyr en släpvagn nära dig eller tjäna pengar med din egen.","Hyr släpvagn","Tjäna med din släpvagn","Öppna kundappen","Öppna värdappen"),
"da":("Nem trailerudlejning","Lej en trailer i nærheden eller tjen penge med din egen.","Lej trailer","Tjen med din trailer","Åbn kundeappen","Åbn host-appen"),
"uk":("Проста оренда причепів","Орендуйте причіп поруч або заробляйте на власному причепі.","Орендувати причіп","Заробляти з причепом","Відкрити клієнтський застосунок","Відкрити host-застосунок"),
"es":("Alquiler de remolques fácil","Alquila un remolque cerca o gana dinero con el tuyo.","Alquilar remolque","Gana con tu remolque","Abrir app de cliente","Abrir app de anfitrión"),
"fr":("Location de remorques simplifiée","Louez une remorque près de vous ou gagnez avec la vôtre.","Louer une remorque","Gagner avec votre remorque","Ouvrir l’app client","Ouvrir l’app hôte"),
"it":("Noleggio rimorchi semplice","Noleggia un rimorchio vicino a te o guadagna con il tuo.","Noleggia un rimorchio","Guadagna con il tuo rimorchio","Apri app cliente","Apri app host"),
"nl":("Eenvoudig aanhangwagen huren","Huur een aanhangwagen in de buurt of verdien met je eigen aanhangwagen.","Aanhangwagen huren","Verdien met je aanhangwagen","Open klant-app","Open host-app"),
"pt":("Aluguer de reboques simples","Alugue um reboque perto de si ou ganhe com o seu.","Alugar reboque","Ganhe com o seu reboque","Abrir app de cliente","Abrir app de anfitrião"),
"cs":("Jednoduchý pronájem přívěsů","Pronajměte si přívěs poblíž nebo vydělávejte se svým vlastním.","Pronajmout přívěs","Vydělávat s přívěsem","Otevřít klientskou aplikaci","Otevřít host aplikaci"),
"sk":("Jednoduchý prenájom prívesov","Prenajmite si príves nablízku alebo zarábajte so svojím.","Prenajať príves","Zarábať s prívesom","Otvoriť klientsku aplikáciu","Otvoriť host aplikáciu"),
"hu":("Egyszerű utánfutó-bérlés","Bérelj utánfutót a közelben, vagy keress a sajátoddal.","Utánfutó bérlése","Keress az utánfutóddal","Ügyfél app megnyitása","Host app megnyitása"),
"ro":("Închiriere simplă de remorci","Închiriază o remorcă aproape de tine sau câștigă cu a ta.","Închiriază remorcă","Câștigă cu remorca ta","Deschide aplicația client","Deschide aplicația host"),
"bg":("Лесен наем на ремаркета","Наемете ремарке наблизо или печелете със своето.","Наем на ремарке","Печелете с ремаркето си","Отвори клиентското приложение","Отвори host приложението"),
"tr":("Kolay römork kiralama","Yakındaki bir römorku kiralayın veya kendi römorkunuzla kazanın.","Römork kirala","Römorkunuzla kazanın","Müşteri uygulamasını aç","Host uygulamasını aç"),
"el":("Απλή ενοικίαση τρέιλερ","Νοικιάστε ένα τρέιλερ κοντά σας ή κερδίστε με το δικό σας.","Ενοικίαση τρέιλερ","Κερδίστε με το τρέιλερ σας","Άνοιγμα εφαρμογής πελάτη","Άνοιγμα εφαρμογής host"),
"hr":("Jednostavan najam prikolica","Unajmite prikolicu u blizini ili zaradite sa svojom.","Najam prikolice","Zaradite s prikolicom","Otvori klijentsku aplikaciju","Otvori host aplikaciju"),
"sl":("Preprost najem prikolic","Najemite prikolico v bližini ali zaslužite s svojo.","Najem prikolice","Zaslužite s prikolico","Odpri aplikacijo za stranke","Odpri host aplikacijo"),
"sr":("Једноставно изнајмљивање приколица","Изнајмите приколицу у близини или зарађујте са својом.","Изнајми приколицу","Зарадите са приколицом","Отвори клијентску апликацију","Отвори host апликацију"),
"ar":("تأجير المقطورات بسهولة","استأجر مقطورة قريبة منك أو اربح من مقطورتك الخاصة.","استئجار مقطورة","اربح من مقطورتك","فتح تطبيق العميل","فتح تطبيق المضيف"),
"he":("השכרת נגררים בקלות","שכרו נגרר קרוב אליכם או הרוויחו מהנגרר שלכם.","השכרת נגרר","להרוויח מהנגרר שלך","פתח אפליקציית לקוח","פתח אפליקציית מארח"),
"hi":("आसान ट्रेलर किराया","अपने पास ट्रेलर किराए पर लें या अपने ट्रेलर से कमाएँ।","ट्रेलर किराए पर लें","अपने ट्रेलर से कमाएँ","क्लाइंट ऐप खोलें","होस्ट ऐप खोलें"),
"zh":("轻松租赁拖车","在附近租一辆拖车，或用自己的拖车赚钱。","租拖车","用你的拖车赚钱","打开客户应用","打开车主应用"),
"ja":("かんたんトレーラーレンタル","近くのトレーラーを借りる、または自分のトレーラーで収益化。","トレーラーを借りる","トレーラーで収益化","クライアントアプリを開く","ホストアプリを開く"),
"ko":("간편한 트레일러 대여","가까운 트레일러를 빌리거나 내 트레일러로 수익을 얻으세요.","트레일러 대여","내 트레일러로 수익 얻기","고객 앱 열기","호스트 앱 열기"),
}

for code, _, _ in langs:
    if code not in T:
        h1, lead, rent, host, webc, webh = fallbacks[code]
        T[code] = {
            "title": f"GoRolli — {h1}",
            "desc": lead,
            "h1": h1,
            "lead": lead,
            "rent": rent,
            "rentp": lead,
            "host": host,
            "hostp": lead,
            "play": "Google Play",
            "store": "App Store",
            "webc": webc,
            "webh": webh,
            "how": "How it works",
            "steps": ["Open GoRolli.", "Choose client or host mode.", "Use the service in your language."],
            "kw": "GoRolli trailer rental app.",
            "foot": "Terms · Privacy",
        }

hreflangs = '\n'.join(
    [f'<link rel="alternate" hreflang="{code}" href="{BASE}/{code}">' for code, _, _ in langs]
    + [f'<link rel="alternate" hreflang="x-default" href="{BASE}/en">']
)

lang_nav_template = ""
for code, name, native in langs:
    lang_nav_template += f'<a href="{BASE}/{code}" data-code="{code}">{escape(native)}</a>\n'

css = """
:root{--yellow:#FDC51A;--ink:#0B0C16;--ink2:#12142A;--muted:#9aa0b5;--line:rgba(255,255,255,.12)}
*{box-sizing:border-box}body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,Arial,sans-serif;background:#0B0C16;color:#eef0f7;line-height:1.5}
a{text-decoration:none;color:inherit}.wrap{max-width:1120px;margin:0 auto;padding:0 22px}
header{padding:20px 0}.bar{display:flex;align-items:center;gap:10px}.mark{width:38px}.wm{font-size:24px;font-weight:900}
main{padding:28px 0 54px}.hero{padding:38px 0 30px;text-align:center}.hero h1{font-size:44px;line-height:1.08;margin:0 0 14px;letter-spacing:-1px}.lead{color:#b6bbca;max-width:840px;margin:0 auto;font-size:18px}
.cards{display:grid;grid-template-columns:1fr 1fr;gap:22px;margin-top:34px}.card{background:#12142A;border:1px solid var(--line);border-radius:20px;padding:28px}.card h2{margin:0 0 10px;font-size:24px}.card p{color:#b6bbca}
.btn{display:inline-flex;margin:8px 8px 0 0;padding:12px 16px;border-radius:12px;background:var(--yellow);color:#1a1300;font-weight:800}.btn.ghost{background:rgba(255,255,255,.07);color:#fff;border:1px solid var(--line)}
.how{margin-top:28px;background:#0e1020;border:1px solid var(--line);border-radius:18px;padding:24px}.how h2{margin-top:0}.how li{margin:8px 0;color:#c5cad8}
.kw{color:#9aa0b5;margin-top:22px}.langnav{display:flex;flex-wrap:wrap;gap:8px;margin-top:28px}.langnav a{padding:7px 10px;border:1px solid var(--line);border-radius:9px;color:#b6bbca}.langnav a.on{background:var(--yellow);color:#1a1300;border-color:var(--yellow)}
footer{border-top:1px solid var(--line);padding:26px 0;color:#9aa0b5;font-size:14px}
@media(max-width:760px){.hero h1{font-size:32px}.cards{grid-template-columns:1fr}.btn{width:100%;justify-content:center}}
"""

for code, name, native in langs:
    d = T[code]
    direction = ' dir="rtl"' if code in {"ar", "he"} else ""
    nav = lang_nav_template.replace(f'data-code="{code}"', f'data-code="{code}" class="on"')
    steps = "".join(f"<li>{escape(x)}</li>" for x in d["steps"])
    html = f"""<!DOCTYPE html>
<html lang="{code}"{direction}>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="index, follow">
<meta name="googlebot" content="index, follow">
<title>{escape(d["title"])}</title>
<meta name="description" content="{escape(d["desc"])}">
<meta name="theme-color" content="#0A1F3D">
<link rel="canonical" href="{BASE}/{code}">
{hreflangs}
<meta property="og:type" content="website">
<meta property="og:url" content="{BASE}/{code}">
<meta property="og:title" content="{escape(d["title"])}">
<meta property="og:description" content="{escape(d["desc"])}">
<meta property="og:image" content="{BASE}/screenshots/host-t1.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="/favicon.png">
<script type="application/ld+json">
{{"@context":"https://schema.org","@graph":[
{{"@type":"Organization","@id":"{BASE}/#org","name":"GoRolli","url":"{BASE}/","logo":"{BASE}/favicon.png","sameAs":["https://www.tiktok.com/@gorolli","https://www.facebook.com/profile.php?id=61581508063664"]}},
{{"@type":"WebSite","@id":"{BASE}/#website","name":"GoRolli","url":"{BASE}/","publisher":{{"@id":"{BASE}/#org"}},"inLanguage":[{",".join('"' + c + '"' for c,_,_ in langs)}]}},
{{"@type":"MobileApplication","name":"GoRolli","operatingSystem":"Android, iOS, Web","applicationCategory":"TravelApplication","url":"{BASE}/{code}","installUrl":"{CLIENT}?lang={code}","publisher":{{"@id":"{BASE}/#org"}},"offers":{{"@type":"Offer","price":"0","priceCurrency":"EUR"}}}}
]}}
</script>
<style>{css}</style>
</head>
<body>
<header><div class="wrap"><div class="bar"><svg class="mark" viewBox="0 0 66 58" aria-hidden="true"><path fill="#FDC51A" d="M16 31 C14 21 20 13 30 13 L45 13 C54 13 61 20 61 30 C61 36 57 41 51 41 L20 41 C18 41 16 37 16 31 Z"/><circle cx="29" cy="43" r="13.5" fill="#FDC51A"/><circle cx="29" cy="43" r="5" fill="#0A1F3D"/></svg><span class="wm">GoRolli</span></div></div></header>
<main><div class="wrap">
<section class="hero"><h1>{escape(d["h1"])}</h1><p class="lead">{escape(d["lead"])}</p></section>
<div class="cards">
  <div class="card cust"><h2>{escape(d["rent"])}</h2><p>{escape(d["rentp"])}</p>
    <a class="btn" href="https://play.google.com/store/apps/details?id=com.mycompany.Hotelio" rel="noopener">{escape(d["play"])}</a>
    <a class="btn ghost" href="https://apps.apple.com/us/search?term=GoRolli" rel="noopener">{escape(d["store"])}</a>
    <a class="btn ghost" href="{CLIENT}?lang={code}">{escape(d["webc"])}</a>
  </div>
  <div class="card host"><h2>{escape(d["host"])}</h2><p>{escape(d["hostp"])}</p>
    <a class="btn" href="https://play.google.com/store/apps/details?id=com.mycompany.gorollihostapp" rel="noopener">{escape(d["play"])}</a>
    <a class="btn ghost" href="https://apps.apple.com/us/search?term=GoRolli" rel="noopener">{escape(d["store"])}</a>
    <a class="btn ghost" href="{HOST}?lang={code}">{escape(d["webh"])}</a>
  </div>
</div>
<div class="how"><h2>{escape(d["how"])}</h2><ol>{steps}</ol></div>
<p class="kw">{escape(d["kw"])}</p>
<nav class="langnav" aria-label="Languages">
{nav}</nav>
</div></main>
<footer><div class="wrap">© 2026 GoRolli · {escape(d["foot"])} · <a href="/privacy">Privacy</a></div></footer>
</body>
</html>
"""
    Path(f"{code}.html").write_text(html, encoding="utf-8", newline="\n")

today = date.today().isoformat()
urls = [("", "weekly", "1.0"), ("privacy", "monthly", "0.3")] + [(code, "weekly", "0.9") for code,_,_ in langs]
sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for path, freq, priority in urls:
    loc = f"{BASE}/{path}" if path else f"{BASE}/"
    sitemap.append(f"  <url><loc>{loc}</loc><lastmod>{today}</lastmod><changefreq>{freq}</changefreq><priority>{priority}</priority></url>")
sitemap.append("</urlset>")
Path("sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8", newline="\n")

print("Generated 32 language pages and sitemap.xml")