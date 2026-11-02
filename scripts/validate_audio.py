#!/usr/bin/env python3
"""
scripts/validate_audio.py

Audits and validates generated speech files and audio manifest conforming to
Sections 9.6, 10, and acceptance scenarios C01-C10 of GEMINI_TECH_SPEC_ENGLISH_V3.md.
Produces reports/audio_validation.json and reports/audio_validation.md.
"""

import hashlib
import json
from pathlib import Path
from pydub import AudioSegment

BASE_DIR = Path(__file__).resolve().parent.parent
MANIFEST_PATH = BASE_DIR / "content/audio_manifest.json"
REPORT_JSON = BASE_DIR / "reports/audio_validation.json"
REPORT_MD = BASE_DIR / "reports/audio_validation.md"
ASSETS_DIR = BASE_DIR / "app_english_cards/app/src/main/assets"

def compute_file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def validate():
    print("=== STARTING AUDIO VALIDATION ===")
    assert MANIFEST_PATH.exists(), f"Manifest {MANIFEST_PATH} does not exist"

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    print(f"Total manifest records: {len(manifest)}")

    valid_count = 0
    missing_count = 0
    corrupt_count = 0
    hash_mismatch_count = 0

    benchmark_ids = [
        "python.str.rsplit.directional",
        "python.builtins.zip",
        "python.builtins.issubclass",
        "python.builtins.getattr",
        "python.builtins.filter",
        "django.queryset.filter"
    ]
    benchmark_status = {bid: [] for bid in benchmark_ids}

    records_report = []

    for item in manifest:
        seg_id = item["segment_id"]
        cid = item["card_id"]
        role = item["role"]
        rel_path = item["file_path"]
        expected_hash = item["file_sha256"]
        file_path = ASSETS_DIR / rel_path

        if not file_path.exists():
            missing_count += 1
            records_report.append({
                "segment_id": seg_id,
                "card_id": cid,
                "role": role,
                "status": "missing",
                "file": rel_path
            })
            continue

        # Verify hash
        actual_hash = compute_file_sha256(file_path)
        if actual_hash != expected_hash:
            hash_mismatch_count += 1
            records_report.append({
                "segment_id": seg_id,
                "card_id": cid,
                "role": role,
                "status": "hash_mismatch",
                "file": rel_path
            })
            continue

        # Verify decode and duration
        try:
            audio = AudioSegment.from_file(str(file_path), format="mp3")
            duration_ms = len(audio)
            peak_dbfs = audio.max_dBFS

            valid_count += 1
            records_report.append({
                "segment_id": seg_id,
                "card_id": cid,
                "role": role,
                "status": "valid",
                "duration_ms": duration_ms,
                "peak_dbfs": round(peak_dbfs, 2)
            })

            if cid in benchmark_status:
                benchmark_status[cid].append({
                    "role": role,
                    "duration_ms": duration_ms,
                    "peak_dbfs": round(peak_dbfs, 2)
                })

        except Exception as e:
            corrupt_count += 1
            records_report.append({
                "segment_id": seg_id,
                "card_id": cid,
                "role": role,
                "status": f"corrupt: {e}",
                "file": rel_path
            })

    summary = {
        "total_manifest_entries": len(manifest),
        "valid_files": valid_count,
        "missing_files": missing_count,
        "hash_mismatches": hash_mismatch_count,
        "corrupt_files": corrupt_count,
        "benchmark_coverage": benchmark_status
    }

    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    with open(REPORT_MD, "w", encoding="utf-8") as f:
        f.write("# Отчет валидации аудиофайлов и манифеста\n\n")
        f.write(f"- **Всего записей в манифесте:** {len(manifest)}\n")
        f.write(f"- **Успешно декодировано и проверено:** {valid_count}\n")
        f.write(f"- **Отсутствующих файлов:** {missing_count}\n")
        f.write(f"- **Несовпадений контрольных сумм:** {hash_mismatch_count}\n")
        f.write(f"- **Поврежденных файлов:** {corrupt_count}\n\n")
        f.write("## Покрытие эталонных карточек\n\n")
        for bid, segs in benchmark_status.items():
            f.write(f"### `{bid}`\n")
            if segs:
                for s in segs:
                    f.write(f"- Роль: `{s['role']}`, длительность: {s['duration_ms']} мс, пик: {s['peak_dbfs']} dBFS\n")
            else:
                f.write("- *Сегменты еще не сгенерированы*\n")
            f.write("\n")

    print(f"Audio validation report saved to {REPORT_JSON} and {REPORT_MD}")
    print(f"Summary: {valid_count} valid, {missing_count} missing, {corrupt_count} corrupt")

if __name__ == "__main__":
    validate()
