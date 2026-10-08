# Riegellinie Chocolaterie Schokittel AG – Vibe-Engineering-Test

Vorplanung einer vollautomatischen Linie für 2.000 gefüllte Schokoriegel/h,
mit der Hilfe diverser KI-Agenten aus dem Lastenheft in `spec/`.
Alles im Repository ist Text: Spezifikation, Entscheidungen, Quellcode der
Zeichnungen und Modelle. Gerenderte Dateien baut `tools/render.sh`.

| Ordner | Inhalt |
| --- | --- |
| `spec/` | Lastenheft, eine Datei je Block, mit REQ-IDs |
| `decisions/` | Architecture Decision Records und Annahmen |
| `pfd/` | Verfahrensfließbilder als Graphviz DOT |
| `pid/` | R&I-Schemata als draw.io-XML |
| `lists/` | Equipment-, Instrumentenliste, UNS-Topics |
| `layout/` | Grundriss als Python/ezdxf |
| `model/` | 3D-Modell (CadQuery) und Energiebilanz |
| `reviews/` | Prüfprotokolle je Iteration |
| `tools/` | Konsistenz-Check und Render-Skript |
| `prompts/` | Prompts der Testphasen, zur Dokumentation |

Start: `pip install -r tools/requirements.txt`, dann `claude` im Repo-Root.
