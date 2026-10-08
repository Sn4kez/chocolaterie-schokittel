#!/usr/bin/env bash
# Rendert alle Artefakte nach out/. Quelltext bleibt im Repo, out/ ist gitignored.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p out/pfd out/pid out/layout out/model

echo "▶ Fließbilder (Graphviz)"
for f in pfd/*.dot; do
  [ -e "$f" ] || continue
  dot -Tpng "$f" -o "out/pfd/$(basename "${f%.dot}").png"
  dot -Tsvg "$f" -o "out/pfd/$(basename "${f%.dot}").svg"
done

echo "▶ R&I-Schemata (draw.io)"
DRAWIO=$(command -v drawio || command -v draw.io || true)
for f in pid/*.drawio; do
  [ -e "$f" ] || continue
  if [ -n "$DRAWIO" ]; then
    "$DRAWIO" --export --format pdf --crop --output "out/pid/$(basename "${f%.drawio}").pdf" "$f" \
      || echo "  draw.io-Export fehlgeschlagen (läuft nur mit Display; in CI xvfb-run nutzen)"
  else
    echo "  drawio nicht gefunden – $f wird nicht gerendert"
  fi
done

echo "▶ Grundriss (ezdxf)"
[ -e layout/floorplan.py ] && python layout/floorplan.py && mv -f layout/*.dxf out/layout/ 2>/dev/null || true

echo "▶ 3D-Modell (CadQuery) und Energiebilanz"
[ -e model/plant.py ] && python model/plant.py && mv -f model/*.step out/model/ 2>/dev/null || true
[ -e model/energy_balance.py ] && python model/energy_balance.py || true

echo "▶ Konsistenz-Check"
python tools/check_consistency.py
