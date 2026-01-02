import requests
from bs4 import BeautifulSoup
import os

URL = "https://www.iskur.gov.tr/ilanlar/kurum-disi-kamu-isci-alim-ilanlari/?idId=mersin&il=Mersin"

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

FILE = "ilanlar.txt"

def send(msg):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": msg}
    )

def fetch():
    r = requests.get(URL, timeout=30)
    soup = BeautifulSoup(r.text, "html.parser")
    ilanlar = []
    for a in soup.select("table tbody tr td:nth-child(2) a"):
        ilanlar.append(
            a.text.strip() + "\nhttps://www.iskur.gov.tr" + a["href"]
        )
    return set(ilanlar)

old = set()
if os.path.exists(FILE):
    old = set(open(FILE).read().split("\n\n"))

new = fetch()
diff = new - old

if diff:
    for i in diff:
        send("🟢 YENİ İŞKUR İLANI\n\n" + i)
    open(FILE, "w").write("\n\n".join(new))
