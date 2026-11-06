#!/usr/bin/env python3
"""Synthesize every vocabulary prompt with Andrew; resume safely by content hash."""
import asyncio
import json
from pathlib import Path

from generate_audio import (
    BASE_DIR, VOICE, PROVIDER, SEGMENTS_DIR, MANIFEST_JSON, APP_MANIFEST_JSON,
    compute_input_hash, compute_file_sha256, synthesize_segment,
)

CARDS = BASE_DIR / "content/cards.json"
ANKI = "Anki: 480 слов"
DOC = "Чтение документации: 500 слов"


def matches_cached_file(path, entry):
    return bool(entry and path.is_file() and path.stat().st_size > 200
                and entry.get("duration_ms", 0) > 50
                and compute_file_sha256(path) == entry.get("file_sha256"))


async def main():
    cards = json.loads(CARDS.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST_JSON.read_text(encoding="utf-8"))
    by_key = {(m["card_id"], m["role"]): m for m in manifest}
    by_hash = {m["input_hash"]: m for m in manifest if m.get("input_hash")}
    target = [c for c in cards if ANKI in c.get("study_collections", []) or DOC in c.get("study_collections", [])]
    jobs = []
    for card in target:
        parts = [
            ("term_en", "en", card["pronunciation"]["spoken_en"]),
            ("meaning_ru", "ru", card["meaning_ru_short"]),
        ]
        if card["card_id"].startswith("anki.vocab.") and card.get("examples"):
            example = card["examples"][0]
            if example["en"].strip().lower() != card["display_term"].strip().lower():
                parts.extend((("example_en", "en", example["en"]),
                              ("example_ru", "ru", example["ru"])))
        for role, lang, spoken in parts:
            in_hash = compute_input_hash(spoken, role, lang, VOICE)
            path = SEGMENTS_DIR / f"seg_{in_hash[:16]}.mp3"
            old = by_key.get((card["card_id"], role))
            if old and old.get("input_hash") == in_hash and matches_cached_file(path, old):
                continue
            jobs.append((card["card_id"], role, lang, spoken, in_hash, path))

    print(f"Vocabulary cards: {len(target)}; Andrew segments to generate: {len(jobs)}", flush=True)
    SEGMENTS_DIR.mkdir(parents=True, exist_ok=True)
    semaphore = asyncio.Semaphore(12)
    completed = 0
    failed = []
    lock = asyncio.Lock()
    hash_locks = {}

    async def one(job):
        nonlocal completed
        cid, role, lang, spoken, in_hash, path = job
        async with semaphore:
            try:
                async with hash_locks.setdefault(in_hash, asyncio.Lock()):
                    cached = by_hash.get(in_hash)
                    if cached and matches_cached_file(path, cached):
                        duration, sha = cached["duration_ms"], cached["file_sha256"]
                    else:
                        duration, sha = await synthesize_segment(spoken, path)
                    entry = {"segment_id": f"seg_{in_hash[:16]}", "card_id": cid,
                             "role": role, "lang": lang, "spoken_text": spoken,
                             "voice": VOICE, "provider": PROVIDER, "input_hash": in_hash,
                             "file_path": f"audio/segments/{path.name}", "file_sha256": sha,
                             "duration_ms": duration, "validation_status": "ready"}
                    by_hash[in_hash] = entry
                async with lock:
                    by_key[(cid, role)] = entry
                    completed += 1
                    if completed % 25 == 0:
                        publish()
                        print(f"Andrew audio: {completed}/{len(jobs)}", flush=True)
            except Exception as exc:
                failed.append((cid, role, str(exc)))
                print("FAILED", cid, role, str(exc), flush=True)

    def publish():
        untouched = [x for x in manifest if (x["card_id"], x["role"]) not in by_key]
        entries = list(by_key.values()) + untouched
        # A content-addressed file can be shared by several cards. If it was
        # re-synthesized, every manifest reference must receive the new hash.
        current_hashes = {}
        for entry in entries:
            path = BASE_DIR / "app_english_cards/app/src/main/assets" / entry["file_path"]
            if path.is_file():
                current_hashes.setdefault(entry["file_path"], compute_file_sha256(path))
                entry["file_sha256"] = current_hashes[entry["file_path"]]
        payload = json.dumps(entries, ensure_ascii=False, indent=2) + "\n"
        for dest in (MANIFEST_JSON, APP_MANIFEST_JSON):
            tmp = dest.with_suffix(".tmp")
            tmp.write_text(payload, encoding="utf-8")
            tmp.replace(dest)

    await asyncio.gather(*(one(job) for job in jobs))
    publish()
    print(f"DONE {completed} synthesized; {len(failed)} failed", flush=True)
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    asyncio.run(main())
