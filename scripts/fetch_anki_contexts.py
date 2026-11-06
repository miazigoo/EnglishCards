#!/usr/bin/env python3
"""Collect short English/Russian sentence pairs for Anki words from Tatoeba.

The examples are suggestions for editorial review; source IDs and license are
stored with every pair. This script does not alter canonical cards.
"""
import concurrent.futures
import json
import re
import threading
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / "content/cards.json"
OUT = ROOT / "content/anki_context_candidates.json"
LOCK = threading.Lock()


def choose(card):
    term = card["display_term"]
    query = f'"{term}"' if " " in term else f"={term}"
    params = {"from": "eng", "to": "rus", "query": query,
              "trans_filter": "limit", "trans_to": "rus", "trans_link": "direct",
              "word_count_min": 4, "word_count_max": 16}
    for attempt in range(3):
        try:
            response = requests.get("https://tatoeba.org/en/api_v0/search", params=params, timeout=25)
            response.raise_for_status()
            rows = response.json().get("results", [])
            scored = []
            for row in rows:
                en = row.get("text", "").strip()
                if row.get("correctness", 0) < 0 or not row.get("license", "").startswith("CC BY"):
                    continue
                if not re.search(r"(?<![A-Za-z])" + re.escape(term) + r"(?![A-Za-z])", en, re.I):
                    continue
                for group in row.get("translations", []):
                    for translated in group:
                        ru = translated.get("text", "").strip()
                        if translated.get("lang") != "rus" or translated.get("correctness", 0) < 0:
                            continue
                        if not ru or len(ru) > 150:
                            continue
                        gloss = card["meaning_ru_short"].split(";")[0].split(" или ")[0]
                        roots = [w[:4].lower() for w in re.findall(r"[а-яё]{5,}", gloss.lower())]
                        semantic = int(any(root in ru.lower() for root in roots))
                        wc = len(en.split())
                        score = semantic * 20 - abs(wc - 8) - abs(len(ru) - 55) / 30
                        scored.append((score, {
                            "en": en, "ru": ru, "semantic_match": bool(semantic),
                            "source": "Tatoeba", "source_url": f"https://tatoeba.org/en/sentences/show/{row['id']}",
                            "source_id": row["id"], "translation_id": translated["id"],
                            "license": row["license"], "author": row.get("user", {}).get("username"),
                        }))
            if scored:
                scored.sort(key=lambda x: x[0], reverse=True)
                return card["card_id"], scored[0][1]
            return card["card_id"], None
        except Exception as exc:
            if attempt == 2:
                return card["card_id"], {"error": str(exc)}
            time.sleep(1.5 * (attempt + 1))


def main():
    cards = [c for c in json.loads(CARDS.read_text(encoding="utf-8"))
             if c["card_id"].startswith("anki.vocab.")]
    saved = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    todo = [c for c in cards if c["card_id"] not in saved]
    print("Anki words", len(cards), "to fetch", len(todo), flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        futures = [pool.submit(choose, c) for c in todo]
        for index, future in enumerate(concurrent.futures.as_completed(futures), 1):
            cid, value = future.result()
            with LOCK:
                saved[cid] = value
                if index % 20 == 0 or index == len(todo):
                    OUT.write_text(json.dumps(saved, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                    print("Fetched", index, "of", len(todo), "pairs", sum(bool(v and v.get("en")) for v in saved.values()), flush=True)


if __name__ == "__main__":
    main()
