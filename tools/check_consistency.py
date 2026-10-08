#!/usr/bin/env python3
"""Konsistenz-Check: Jeder Tag genau einmal, überall.

Prüft, dass die Tags in den R&I-Schemata (pid/*.drawio), den Listen
(lists/equipment.csv, lists/instruments.csv), den UNS-Topics
(lists/uns-topics.yaml) und – falls vorhanden – im Grundriss-Skript
(layout/*.py) und im 3D-Modell (model/*.py) übereinstimmen.

Aufruf:  python tools/check_consistency.py [--strict]
Exit 0 = konsistent, 1 = Abweichungen, 2 = Eingabefehler.
Mit --strict werden auch Warnungen (fehlende Dateien, Tags nur im Code) zu Fehlern.
"""
from __future__ import annotations

import base64
import csv
import re
import sys
import zlib
from collections import Counter
from pathlib import Path
from urllib.parse import unquote
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

# ISA-5.1-nahe Tags: Buchstaben, Bindestrich, dreistellige Nummer, optionaler Suffix.
# Beispiele: T-101, P-205, HX-901, TIC-101, FQI-205, CIP-201, R-301A
TAG_RE = re.compile(r"\b([A-Z]{1,4}-\d{3}[A-Z]?)\b")
# Leitungsnummern wie CHM-101-DN40 werden gesondert erkannt und nicht als Equipment gezählt.
LINE_RE = re.compile(r"\b[A-Z]{2,4}-\d{3}-DN\d{2,3}\b")

STRICT = "--strict" in sys.argv
errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    (errors if STRICT else warnings).append(msg)


# ---------------------------------------------------------------- draw.io ---
def drawio_text(path: Path) -> str:
    """Liefert den sichtbaren Text aller Zellen einer draw.io-Datei.
    Unterstützt unkomprimierte und komprimierte Diagramme."""
    raw = path.read_text(encoding="utf-8", errors="replace")
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        err(f"{path}: XML nicht lesbar ({exc})")
        return ""
    texts: list[str] = []
    for diagram in root.iter("diagram"):
        model = diagram.find("mxGraphModel")
        if model is None and (diagram.text or "").strip():
            # komprimiert: base64 → deflate → url-encoded XML
            try:
                data = base64.b64decode(diagram.text.strip())
                xml = unquote(zlib.decompress(data, -15).decode("utf-8"))
                model = ET.fromstring(xml)
                warn(f"{path}: Diagramm '{diagram.get('name')}' ist komprimiert gespeichert – "
                     "bitte unkomprimiert speichern (compressed=\"false\"), sonst ist git diff blind.")
            except Exception as exc:  # noqa: BLE001
                err(f"{path}: komprimiertes Diagramm nicht dekodierbar ({exc})")
                continue
        if model is None:
            continue
        for cell in model.iter("mxCell"):
            value = cell.get("value") or ""
            texts.append(re.sub(r"<[^>]+>", " ", value))  # HTML in Labels entfernen
        for obj in model.iter("object"):  # Zellen mit Metadaten
            for key in ("label", "tag", "value"):
                if obj.get(key):
                    texts.append(re.sub(r"<[^>]+>", " ", obj.get(key)))
    return "\n".join(texts)


def tags_in_text(text: str) -> Counter:
    text = LINE_RE.sub(" ", text)  # Leitungsnummern vorher ausblenden
    return Counter(TAG_RE.findall(text))


# ------------------------------------------------------------------- CSV ----
def tags_in_csv(path: Path, column: str = "tag") -> Counter:
    if not path.exists():
        warn(f"{path.relative_to(ROOT)} fehlt")
        return Counter()
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None or column not in reader.fieldnames:
            err(f"{path.relative_to(ROOT)}: Spalte '{column}' fehlt (Kopfzeile: {reader.fieldnames})")
            return Counter()
        values = [(row.get(column) or "").strip() for row in reader]
    bad = [v for v in values if v and not TAG_RE.fullmatch(v)]
    for v in bad:
        err(f"{path.relative_to(ROOT)}: '{v}' entspricht nicht der Tag-Konvention")
    return Counter(v for v in values if v)


# ------------------------------------------------------------------ YAML ----
def tags_in_uns(path: Path) -> Counter:
    """Erwartet Einträge mit 'tag:' oder Topics, die auf den Tag enden."""
    if not path.exists():
        warn(f"{path.relative_to(ROOT)} fehlt")
        return Counter()
    text = "\n".join(
        line for line in path.read_text(encoding="utf-8").splitlines()
        if not line.lstrip().startswith("#")
    )
    found = Counter()
    for m in re.finditer(r"^\s*-?\s*tag:\s*['\"]?([A-Z]{1,4}-\d{3}[A-Z]?)", text, re.M):
        found[m.group(1)] += 1
    if not found:  # Fallback: Tags irgendwo im Topic-Pfad
        found = tags_in_text(text)
    return found


# ---------------------------------------------------------------- Python ----
def tags_in_code(paths: list[Path]) -> Counter:
    found = Counter()
    for p in paths:
        if p.name.startswith("check_"):
            continue
        found.update(set(tags_in_text(p.read_text(encoding="utf-8", errors="replace"))))
    return found


# ------------------------------------------------------------------ main ----
def main() -> int:
    pid_files = sorted((ROOT / "pid").glob("*.drawio"))
    if not pid_files:
        err("pid/: keine .drawio-Datei gefunden")
        return finish()

    pid_tags: Counter = Counter()
    for f in pid_files:
        c = tags_in_text(drawio_text(f))
        for tag, n in c.items():
            if n > 1:
                warn(f"{f.relative_to(ROOT)}: Tag {tag} kommt {n}× vor (Off-Page-Connector?)")
        pid_tags.update(set(c))
    for tag, n in pid_tags.items():
        if n > 1:
            warn(f"Tag {tag} erscheint in {n} R&I-Dateien – nur zulässig als Übergabestelle")

    equipment = tags_in_csv(ROOT / "lists" / "equipment.csv")
    instruments = tags_in_csv(ROOT / "lists" / "instruments.csv")
    lists_all = equipment + instruments
    for tag, n in lists_all.items():
        if n > 1:
            err(f"Tag {tag} steht {n}× in den Listen – jeder Tag genau einmal")

    uns = tags_in_uns(ROOT / "lists" / "uns-topics.yaml")
    code = tags_in_code(sorted((ROOT / "layout").glob("*.py")) + sorted((ROOT / "model").glob("*.py")))

    pid_set, list_set, uns_set, code_set = map(set, (pid_tags, lists_all, uns, code))

    for tag in sorted(pid_set - list_set):
        err(f"{tag} im R&I, aber in keiner Liste")
    for tag in sorted(list_set - pid_set):
        err(f"{tag} in den Listen, aber in keinem R&I")
    if uns_set:
        for tag in sorted(list_set - uns_set):
            err(f"{tag} hat kein UNS-Topic")
        for tag in sorted(uns_set - list_set):
            err(f"UNS-Topic für {tag}, aber Tag unbekannt")
    if code_set:
        for tag in sorted(code_set - list_set):
            warn(f"{tag} im Layout-/Modellcode, aber nicht in den Listen")
        for tag in sorted(set(equipment) - code_set):
            warn(f"Equipment {tag} fehlt im Layout-/Modellcode")

    print(f"R&I-Dateien: {len(pid_files)} · Tags im R&I: {len(pid_set)} · "
          f"Equipment: {len(equipment)} · Instrumente: {len(instruments)} · "
          f"UNS-Topics: {len(uns_set)} · Tags im Code: {len(code_set)}")
    return finish()


def finish() -> int:
    for w in warnings:
        print(f"WARNUNG  {w}")
    for e in errors:
        print(f"FEHLER   {e}")
    if errors:
        print(f"\n{len(errors)} Fehler, {len(warnings)} Warnungen – nicht konsistent.")
        return 1
    print(f"\nKonsistent. {len(warnings)} Warnungen.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
