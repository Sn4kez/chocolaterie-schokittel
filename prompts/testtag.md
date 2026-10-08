# Prompts für den Testtag

Jede Phase hat einen Startprompt. Wortlaut im Review-Protokoll festhalten, wenn du abweichst.
Vor Phase 3: `claude` im Repo-Root starten; Claude Code liest `CLAUDE.md` automatisch.

## Phase 3 – Fließbild (30 min)
> Lies `spec/` vollständig. Erzeuge aus den Abschnitten Verfahren (PRC-*) und Energie (ENE-*)
> je ein Verfahrensfließbild nach ISO 10628 als Graphviz DOT in `pfd/`: `m1-schokolade.dot`,
> `m2-fuellung-formen.dot`, `m3-verpacken-blackbox.dot` und `m9-energie.dot`. Jedes Equipment
> bekommt einen Tag nach der Konvention in CLAUDE.md. Rendere mit `tools/render.sh`, sieh dir
> die PNGs an und prüfe: Kommt jeder Stoff- und Energiestrom aus dem Lastenheft vor? Schließt
> die Massenbilanz bei 80 kg/h Fertigprodukt auf ±2 %? Liste Annahmen in `decisions/annahmen.md`.

## Phase 4 – R&I und Listen (120 min)
> Erzeuge aus den Fließbildern und `spec/` R&I-Schemata als unkomprimierte draw.io-XML in `pid/`,
> je Modul eine Datei, mit P&ID-Symbolen nach ISO 10628-2, Armaturen, Messstellen nach AUT-06,
> Regelkreisen, CCPs nach HYG-07 und beheizten Leitungen nach PRC-04. Leite daraus
> `lists/equipment.csv`, `lists/instruments.csv` und `lists/uns-topics.yaml` ab.
> `python tools/check_consistency.py` muss fehlerfrei sein, bevor du fertig meldest.
> Schreibe für jede Entscheidung zwischen Varianten ein ADR.

## Phase 5 – Grundriss und 3D (120 min)
> Schlage Hallenmaße nach RAU-01 vor und begründe sie in einem ADR. Schreibe `layout/floorplan.py`
> (ezdxf), das aus `lists/equipment.csv` einen Grundriss mit Zonen nach HYG-01, Materialfluss nach
> RAU-03, Abständen und Fluchtwegen nach RAU-04 und Türen nach RAU-06 erzeugt. Danach
> `model/plant.py` (CadQuery → STEP) mit Halle, Tanks, Maschinen und Hauptleitungen; prüfe
> Kollisionen und Höhen nach RAU-02. Zum Schluss `model/energy_balance.py` für die drei
> Betriebsfälle nach ENE-06, Ergebnis nach `reviews/energiebilanz.md`.

## Phase 6 – Änderungsdurchlauf (30 min, Stoppuhr!)
Vorher die Datei `09-aenderungsszenario.md` aus dem Ordner außerhalb des Repos nach `spec/` kopieren
und committen. Dann:
> Das Lastenheft wurde um `spec/09-aenderungsszenario.md` ergänzt. Lies es, aktualisiere alle
> betroffenen Artefakte (Fließbilder, R&I, Listen, UNS-Topics, Grundriss, 3D-Modell, Energiebilanz,
> Kostenschätzung, manuelle Tätigkeiten), führe den Konsistenz-Check aus und liste am Ende, welche
> Dateien du warum geändert hast und welche Anforderungen aus CHG-* du nicht erfüllen konntest.

## Kontrolllauf (zweiter Tag, optional)
Gleiche Prompts mit Cline + lokalem Modell im frischen Clone des Commits nach Phase 2.
Vergleich im Artikel: Iterationen, Fehlerklassen, Zeit.
