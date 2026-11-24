import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

URL = "https://trends.google.com/trending/rss?geo=US"
OUT = Path("data/trends.json")

def clean(value):
    return re.sub(r"\s+", " ", value or "").strip()

def main():
    req = urllib.request.Request(URL, headers={"User-Agent":"MerchTrendHunter/0.2 trend research"})
    with urllib.request.urlopen(req, timeout=30) as response:
        root = ET.fromstring(response.read())
    channel = root.find("channel")
    rows = []
    if channel is not None:
        for item in channel.findall("item"):
            title = clean(item.findtext("title"))
            if not title:
                continue
            traffic, news_url = "", ""
            for child in list(item):
                tag = child.tag.split("}")[-1]
                if tag == "approx_traffic":
                    traffic = clean(child.text)
                elif tag == "news_item":
                    for node in list(child):
                        if node.tag.split("}")[-1] == "url":
                            news_url = clean(node.text)
                            break
            rows.append({"title":title,"traffic_label":traffic or "Not supplied","published":clean(item.findtext("pubDate")),"news_url":news_url})
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"status":"ok","market":"US","source":URL,"collected_at":datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),"items":rows},ensure_ascii=False,indent=2),encoding="utf-8")
    print(f"Saved {len(rows)} trends")

if __name__ == "__main__":
    main()
