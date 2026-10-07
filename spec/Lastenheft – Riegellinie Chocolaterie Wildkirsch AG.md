# Lastenheft – Riegellinie Chocolaterie Schokittel AG

Oct 6, 2026 · @Jan

Dieses Lastenheft beschreibt eine vollautomatische Linie für 2.000 gefüllte Schokoriegel pro Stunde im Dreischichtbetrieb, vom 25-kg-Block bis zum verpackten Riegel, als Eingabe für einen KI-Agenten im Vibe-Engineering-Test. Jede Anforderung trägt eine ID und ist prüfbar formuliert.

## 1 Ausgangslage

Die Chocolaterie Schokittel AG sitzt auf 900 m in Appenzell. Gegründet hat sie ein Jan Wokittel, dessen Nachname auf dem ersten Firmenschild zu „Schokittel“ verschrieben wurde – der Fehler blieb, die Marke war geboren. Seit drei Generationen stellt sie den Riegel „Schokittel Alpkräuter“ her: Milch- oder Dunkelschokolade mit einer Creme aus Alpenkräutern vom eigenen Hang. Bisher wird in Handarbeit gegossen; die Nachfrage im Weihnachts- und Ostergeschäft übersteigt die Kapazität um ein Mehrfaches, Fachkräfte für die Nachtschicht sind in Appenzell nicht zu finden.

Der Verwaltungsrat hat beschlossen, eine neue Produktionslinie in einer Neubauhalle neben der Manufaktur zu bauen. Die Linie soll im Dreischichtbetrieb ohne Bedienpersonal laufen („Lights-out“), damit die drei Chocolatiers des Hauses tagsüber Rezepte entwickeln statt nachts Blöcke schmelzen. Strom kommt aus dem eigenen Wasserkraftwerk am Bach, Wasser aus der Quelle; weitere Medien gibt es am Standort nicht.

Dieses Lastenheft ist die Eingabe für die Vorplanung durch einen KI-Agenten. Es beschreibt, **was** die Linie leisten muss, nicht wie; Lösungen schlägt der Agent vor und begründet sie in `decisions/`.

## 2 Ziel, Leitbild und Scope

Ziel ist eine Linie, die 2.000 gefüllte Riegel pro Stunde in zwei Schokoladensorten produziert, rund um die Uhr läuft und tagsüber von einem Team betreut wird, das nicht an der Linie stehen muss.

**Leitbild Lights-out:** Jeder Prozessschritt, der heute eine Hand braucht, ist entweder automatisiert oder in Abschnitt 10 als bewusste Ausnahme benannt. Das gilt für Rohstoffzufuhr, Sortenwechsel, Reinigung, Qualitätskontrolle und Störungsbehandlung erster Stufe. Menschen betreten den Produktionsraum planmäßig nur zur Wartung und zur Rohstoff-Anlieferung in die Schleuse.

**Scope in drei Modulen:**

| Modul | Inhalt | Rolle im Testtag |
| --- | --- | --- |
| M1 Schokoladenküche | Blockannahme, Schmelzen, Lagern flüssig, Temperieren, Kakaobutter-Spülung beim Sortenwechsel | Vollständig ausplanen (PFD, R&I, Layout, 3D) |
| M2 Füllung und Formen | Alpkräuter-Creme kochen und kühlen, One-Shot-Gießen in Formen, Kühltunnel, Entformen, CIP-Station für den Füllungsstrang | Vollständig ausplanen |
| M3 Verpacken und Logistik | Flowpack, Kartonierung, Palettierung, Metalldetektion, Checkweigher | Im ersten Durchlauf als Blackbox mit Schnittstellen (Takt, Format, Energie, Daten); im zweiten Durchlauf ausplanen |

**Nicht im Scope:** Gebäudestatik, Elektro-Detailplanung (Schaltschränke, Kabelwege), Abwasserbehandlung, Verwaltungsräume. Die Halle selbst ist im Scope, soweit sie die Aufstellung bestimmt: Maße, Zonen, Türen, Bodenabläufe, Lastaufnahmen als Vorgabe an die Architektur.

## 3 Produkt und Mengen

Ein Riegel wiegt 40 g: eine Schokoladenhülle von 24 g umschließt 16 g Alpkräuter-Creme. Zwei Sorten laufen als Varianten auf derselben Linie.

| ID | Anforderung |
| --- | --- |
| PRD-01 | Die Linie produziert den Riegel „Schokittel Alpkräuter“ in zwei Varianten: Hülle aus Milchschokolade (V-M) oder dunkler Schokolade 70 % (V-D), Füllung in beiden Fällen Alpkräuter-Creme. |
| PRD-02 | Sollgewicht 40,0 g je Riegel, Toleranz ±1,5 g; Füllungsanteil 40 % ±3 % der Masse. |
| PRD-03 | Nennleistung 2.000 Riegel/h bei 90 % Linienverfügbarkeit, entsprechend 80 kg/h Fertigprodukt, davon 48 kg/h Schokolade und 32 kg/h Füllung. |
| PRD-04 | Betrieb 24 h an 7 Tagen in der Saison (Oktober bis März), 16 h an 5 Tagen außerhalb; die Anlage muss zwischen beiden Modi ohne Umbau wechseln. |
| PRD-05 | Rohstoffe: Schokolade als 25-kg-Blöcke auf Paletten (Milch und Dunkel), Zucker, Glukosesirup, Alpkräuter-Extrakt (flüssig, 20-l-Gebinde), Butter, Quellwasser. |
| PRD-06 | Rohstoffpuffer für einen unbemannten Zeitraum von mindestens 10 h: entsprechend ≥ 480 kg Schokolade je Sorte flüssig oder als automatisch zuführbare Blöcke und ≥ 320 kg Füllung. |
| PRD-07 | Sortenwechsel V-M ↔ V-D höchstens zweimal je 24 h, Wechseldauer ≤ 45 min inklusive Kakaobutter-Spülung, ohne manuellen Eingriff. |
| PRD-08 | Haltbarkeit des Riegels 9 Monate bei ≤ 18 °C; daraus folgt für die Füllung eine Wasseraktivität a\_w ≤ 0,65. |
| PRD-09 | Produkt-Claims auf der Verpackung: „nuss- und glutenfrei“, „Schweizer Schokolade“, „aus Alpenkräutern vom Hang“. Die Linie darf keinen Rohstoff aufnehmen, der diese Claims gefährdet. |

## 4 Verfahren und Prozessparameter

Der Prozess läuft in zwei Strängen, die sich erst beim Gießen treffen: der wasserfreie Schokoladenstrang (M1) und der wässrige Füllungsstrang (M2). Beide Stränge dürfen nirgends außer in der Gießstation Kontakt haben. Die Werte unten sind Vorgaben; wo der Agent abweichen will, begründet er es in `decisions/`.

**Schokoladenstrang (M1)**

| ID | Anforderung |
| --- | --- |
| PRC-01 | Blockannahme: Paletten mit 25-kg-Blöcken werden in einer Schleuse übergeben; Entpalettieren, Entfolieren und Zuführen zum Schmelzer erfolgen automatisch (Robotik zulässig). |
| PRC-02 | Schmelzen: Blockschmelzer mit beheiztem Rost, Produkttemperatur ≤ 45 °C für Milch und ≤ 50 °C für Dunkel; Leistung ≥ 60 kg/h je Sorte. |
| PRC-03 | Lagerung flüssig: ein Lagertank je Sorte, Nutzvolumen ≥ 500 kg, gerührt, doppelwandig, Haltetemperatur 42 °C ±1 K (Milch) und 45 °C ±1 K (Dunkel). |
| PRC-04 | Alle schokoladeführenden Leitungen und Armaturen sind beheizt (Begleitheizung oder Doppelmantel) und auf 40–45 °C gehalten; keine Totstrecken, Gefälle ≥ 2 % zum tiefsten Punkt, vollständig entleerbar. |
| PRC-05 | Temperieren: kontinuierliche Temperiermaschine, Durchsatz ≥ 60 kg/h, Temperierkurve Milch 45 → 27 → 29,5 °C, Dunkel 50 → 28 → 31,5 °C; Temperiergrad wird inline gemessen und geregelt. |
| PRC-06 | Sortenwechsel: Ein gemeinsamer Temperier- und Gießkreis für beide Sorten; Wechsel durch Verdrängen mit Kakaobutter, Spülmenge ≤ 15 kg, Spülbutter wird aufgefangen und wiederverwendet. Restgehalt der Vorsorte im Produkt ≤ 1 %. |
| PRC-07 | Rücklauf: Überschuss aus der Gießstation läuft temperaturgeführt in den Lagertank zurück; Rücklaufanteil ≤ 30 %. |

**Füllungsstrang (M2)**

| ID | Anforderung |
| --- | --- |
| PRC-08 | Ansatz: Zucker, Glukosesirup, Butter, Quellwasser und Alpkräuter-Extrakt werden gravimetrisch dosiert (Genauigkeit ±0,5 %), Chargengröße 100 kg. |
| PRC-09 | Kochen: Kochkessel mit Rührwerk, Produkttemperatur 108 °C ±2 K bis zum Ziel-Trockensubstanzgehalt (Refraktometer inline), Haltezeit 3 min. |
| PRC-10 | Kühlen: Kratzkühler oder Kühlkessel auf 30 °C ±2 K innerhalb von ≤ 20 min, Kräuterextrakt wird nach dem Kochen zudosiert, um Aromaverluste zu begrenzen. |
| PRC-11 | Pufferung: gerührter Vorlagebehälter ≥ 350 kg bei 30 °C, Verweilzeit ≤ 8 h. |
| PRC-12 | Alle füllungsführenden Teile sind CIP-fähig nach EHEDG; Bauform geschlossen; Produktkontaktflächen Ra ≤ 0,8 µm. |

**Gießen, Kühlen, Entformen (M2)**

| ID | Anforderung |
| --- | --- |
| PRC-13 | Gießverfahren One-Shot: Hülle und Füllung werden gleichzeitig in Polycarbonat-Formen dosiert, Taktleistung ≥ 2.000 Riegel/h, Dosiergenauigkeit je Komponente ±0,5 g. |
| PRC-14 | Formen werden vor dem Gießen auf 28 °C ±1 K vorgewärmt und nach dem Gießen gerüttelt (Entlüften). |
| PRC-15 | Kühltunnel: Lufttemperatur 12 °C ±2 K, Verweilzeit 20–25 min, mehrzonig mit Vorkühlzone ≥ 15 °C, um Fettreif zu vermeiden; Taupunkt der Austrittszone unter Produkttemperatur. |
| PRC-16 | Entformen automatisch durch Wenden und Klopfen; Formenrücklauf zur Vorwärmung geschlossen; Formenwaschen außerhalb der Produktionszeit, automatisiert. |
| PRC-17 | Ausschuss (Fehlgüsse, Riegel außerhalb Gewichtstoleranz) wird automatisch ausgeschleust und getrennt nach Sorte gesammelt. |

**Verpacken (M3, Blackbox)**

| ID | Anforderung |
| --- | --- |
| PRC-18 | Übergabe an M3 als Einzelriegel auf Band, 14–16 °C, Takt 2.000/h; M3 umfasst Flowpack, Kartonierung (24 Riegel), Palettierung, Metalldetektor und Checkweigher. |
| PRC-19 | Schnittstellen zu M3 sind im ersten Durchlauf zu definieren: Übergabehöhe, Bandbreite, Energiebedarf, Datenpunkte im Unified Namespace. |

## 5 Hygiene, Reinigung, Allergene, HACCP

Die Halle ist ein Trockenbereich mittlerer Hygienezone; nur der Füllungsstrang und die CIP-Station bilden eine Nasszone mit Bodenabläufen. Wasser darf den Schokoladenstrang nie erreichen.

| ID | Anforderung |
| --- | --- |
| HYG-01 | Zonierung: Zone A Anlieferung/Schleuse (Basis), Zone B Schokoladenküche und Gießen (mittel, trocken), Zone C Füllungsküche und CIP (mittel, nass), Zone D Verpacken (Basis). Übergänge mit Luftführung von höherer zu niedrigerer Zone. |
| HYG-02 | Schokoladenstrang: Trockenreinigung; Sortenwechsel mit Kakaobutter (PRC-06); keine Wasser- oder CIP-Anschlüsse an Bauteilen der Zone B. Halbjährliche Komplettreinigung ist eine geplante Ausnahme vom Lights-out-Betrieb. |
| HYG-03 | Füllungsstrang: vollautomatische CIP-Station mit Lauge, Säure und Heißwasser (Zweitank, Rückführung), Programme ≤ 60 min, Validierung über Leitfähigkeit und Temperatur am Rücklauf; CIP ohne manuelles Umstecken, Trennung Produkt/Reinigungsmedium durch Doppelsitzventile. |
| HYG-04 | Formen: Polycarbonat-Formen werden automatisch gewaschen und getrocknet; Restfeuchte vor Wiederbefüllung = 0 (Trocknung mit konditionierter Luft). |
| HYG-05 | Allergene: Die Linie verarbeitet keine Nüsse und kein Gluten; alle Rohstoffe sind per Spezifikation nuss- und glutenfrei; Wareneingang mit automatischer Chargenfreigabe gegen die Spezifikation im MES. Milch und Soja-Lecithin sind deklarierte Allergene beider Sorten. |
| HYG-06 | Hygienic Design nach EHEDG Doc. 8 und 13 und DIN EN 1672-2: Edelstahl 1.4404 im Produktkontakt, keine Spalten, Schweißnähte produktseitig glatt, Bodenabstand von Maschinen ≥ 300 mm, Wandabstand ≥ 800 mm. |
| HYG-07 | HACCP-Kontrollpunkte: CCP 1 Siebung der flüssigen Schokolade (Maschenweite 2 mm) vor der Temperierung; CCP 2 Kochtemperatur Füllung ≥ 105 °C für ≥ 3 min mit Aufzeichnung; CCP 3 Metalldetektion am Riegel (Fe 1,5 mm, NFe 2,0 mm, SS 2,5 mm) mit automatischer Ausschleusung. Jeder CCP erzeugt einen Datensatz im Unified Namespace. |
| HYG-08 | Schädlings- und Fremdkörperkonzept: geschlossene Anlage, Rohstoff-Schleuse mit Luftschleier, kein Holz und kein Glas in Zone B und C. |
| HYG-09 | Personal betritt Zone B und C planmäßig nicht; Wartungszugänge sind so angeordnet, dass Standardwartung von außerhalb der Hygienezone oder in Produktionspausen erfolgt. |

## 6 Medien, Energie und Raum

Am Standort gibt es Strom aus dem eigenen Wasserkraftwerk und Quellwasser – sonst nichts. Wärme und Kälte werden vor Ort elektrisch erzeugt; die Abwärme des Kühltunnels soll die Schmelzer und Temperierkreise speisen. Die Halle ist ein Neubau, der Agent schlägt die Maße vor.

**Energie und Medien**

| ID | Anforderung |
| --- | --- |
| ENE-01 | Verfügbare Medien: Elektrische Energie 400 V, 50 Hz, Anschlussleistung ≤ 250 kW; Quellwasser 6 °C, Trinkwasserqualität, ≤ 2 m³/h. Keine weiteren Medien. |
| ENE-02 | Wärme für Schmelzer, Lagertanks, Begleitheizung und Temperierung (Niveau 40–55 °C) wird über eine Wärmepumpe bereitgestellt, deren Quelle die Abwärme der Kälteerzeugung ist; Deckungsgrad der Niedertemperaturwärme aus Abwärme ≥ 70 % im Nennbetrieb. |
| ENE-03 | Kälte für Kühltunnel, Füllungskühlung und Formenkonditionierung über einen Glykolkreis −2 °C / +4 °C aus derselben Wärmepumpen-/Kälteanlage; Kälteleistung vom Agenten aus der Energiebilanz abzuleiten. |
| ENE-04 | Prozesswärme > 55 °C (Füllungskochen 108 °C) elektrisch direkt oder über Hochtemperatur-Wärmepumpe; der Agent vergleicht beide Varianten nach Energie und Investition. |
| ENE-05 | Druckluft für Ventilantriebe und Verpackung wird vor Ort erzeugt, ölfrei Klasse 1 nach ISO 8573-1, mit Trocknung auf Drucktaupunkt ≤ −20 °C. |
| ENE-06 | Der Agent erstellt eine geschlossene Energiebilanz (Wärme, Kälte, Strom) für Nennbetrieb, Anfahren nach 10 h Stillstand und Sortenwechsel; Ziel: spezifischer Energiebedarf ≤ 0,9 kWh je kg Fertigprodukt. |
| ENE-07 | Alle Energieflüsse werden gemessen (Strom je Hauptverbraucher, Wärme- und Kältemengenzähler je Kreis) und als Datenpunkte im Unified Namespace veröffentlicht. |
| ENE-08 | Wasser: Verbrauch für CIP und Formenwäsche ≤ 1,5 m³ je 24 h; Spülwasser der letzten Phase wird als Vorspülwasser wiederverwendet. |

**Raum und Aufstellung**

| ID | Anforderung |
| --- | --- |
| RAU-01 | Neubauhalle, eingeschossig, Maße vom Agenten vorzuschlagen und zu begründen; Zielgröße so klein wie möglich bei Einhaltung aller Abstände, Erweiterungsreserve 25 % Fläche für eine zweite Gießlinie. |
| RAU-02 | Lichte Höhe ≥ 5 m in Zone B und C (Lagertanks, Kühltunnel-Rückführung), ≥ 4 m in Zone A und D. |
| RAU-03 | Zonen nach HYG-01 räumlich getrennt; Materialfluss linear von Anlieferung (A) über B/C nach D ohne Kreuzung des Rohstoffwegs mit dem Fertigproduktweg. |
| RAU-04 | Wartungsabstand um jede Maschine ≥ 800 mm an mindestens zwei Seiten, ≥ 1.200 mm vor Schaltschränken und Wartungsfronten; Fluchtwege ≥ 1.200 mm, maximal 35 m Fluchtweglänge. |
| RAU-05 | Böden: Zone C mit Gefälle ≥ 1,5 % zu Bodenabläufen, säurefest; Zone B ohne Bodenabläufe, fugenlos. Angaben an die Architektur als Vorgabe. |
| RAU-06 | Zugänge: eine Rohstoff-Schleuse (Palettentor 2,5 × 3 m mit Luftschleier), ein Fertigwarentor, eine Personalschleuse je Hygienezone, Technikraum für Wärmepumpe, Kälte, Druckluft und IT getrennt vom Produktionsraum. |
| RAU-07 | Der Agent liefert Grundriss (DXF) und 3D-Modell (STEP/IFC) mit allen Maschinen, Tanks, Hauptleitungen, Zonen, Türen und Abständen; Kollisionsfreiheit wird im Modell geprüft. |

## 7 Automatisierung und digitale Architektur

Die Linie läuft unbemannt; die Automatisierung ist deshalb kein Zusatz, sondern Teil des Verfahrens. Architekturprinzip: ereignisgetrieben über einen Unified Namespace statt punkt-zu-punkt, Steuerung als Software statt als Blech, MES aus Bausteinen statt als Monolith.

| ID | Anforderung |
| --- | --- |
| AUT-01 | Automatisierungsgrad: Normalbetrieb, Sortenwechsel, CIP, Formenwäsche, An- und Abfahren sowie Störungsquittierung erster Stufe laufen ohne menschlichen Eingriff; eine Liste aller verbleibenden manuellen Tätigkeiten ist Teil der Lieferung. |
| AUT-02 | Steuerung über virtuelle PLCs (z. B. Siemens S7-1500V, CODESYS Virtual Control), die auf redundanter IT-Infrastruktur im Technikraum laufen; Feldanbindung über PROFINET oder EtherCAT mit Remote-I/O; keine Hardware-SPS je Maschine. Sicherheitsfunktionen (Not-Halt, Schutztüren) bleiben auf zertifizierter Hardware. |
| AUT-03 | Unified Namespace: Alle Prozess-, Energie-, Qualitäts- und Zustandsdaten werden über einen MQTT-Broker (redundant, Sparkplug B) in einer ISA-95-konformen Topic-Struktur veröffentlicht: `schokittel/appenzell/riegellinie/<modul>/<equipment>/<tag>`. OPC UA wird nicht eingesetzt; Maschinen mit OPC-UA-Schnittstelle werden über ein Gateway auf MQTT abgebildet. |
| AUT-04 | MES composable (z. B. Tulip): Rezeptverwaltung, Chargenprotokoll, OEE, Qualitätsfreigaben und CCP-Nachweise als eigenständige Apps, die ausschließlich über den Unified Namespace mit der Linie sprechen. Kein direkter Zugriff eines MES-Bausteins auf eine Steuerung. |
| AUT-05 | Rezepte für V-M und V-D liegen als versionierte Textdateien (YAML) im Repository und werden über das MES auf die virtuellen PLCs ausgerollt; ein Rezeptwechsel ist ein Commit. |
| AUT-06 | Instrumentierung mindestens: Temperatur an jedem Tank, jeder Begleitheizung und jeder Temperierstufe; Durchfluss und Dichte an Schokolade und Füllung vor der Gießstation; Temperiergrad inline; Leitfähigkeit, Temperatur und Durchfluss an jedem CIP-Rücklauf; Gewicht je Riegel; Taupunkt und Temperatur je Kühltunnelzone. Tag-Konvention nach ISA 5.1 (z. B. TIC-201, FQI-305). |
| AUT-07 | Zustandsüberwachung: Vibration und Stromaufnahme an Pumpen und Rührwerken, Laufzeit je Ventil, als Datenpunkte im UNS für vorausschauende Wartung. |
| AUT-08 | Digitaler Zwilling: Das statische Modell entsteht aus den BIM-Daten (IFC) und wird nach OpenUSD überführt; im Betrieb werden UNS-Daten über einen MQTT-USD-Connector auf die Prims des Modells gespiegelt. Simulation (Materialfluss, Begehung, Kollisionsprüfung) läuft in NVIDIA Omniverse. |
| AUT-09 | Fernzugriff: Störungen zweiter Stufe werden an eine Bereitschaft gemeldet (UNS → Alarmierung); Eingriffe über eine gesicherte Fernwartung mit Freigabe durch das MES; der Produktionsraum wird dafür nicht betreten. |
| AUT-10 | IT-Sicherheit nach IEC 62443: Zonen und Conduits zwischen Feld, Steuerung, Broker, MES und Fernzugriff; TLS auf allen MQTT-Verbindungen; Broker und vPLC-Host als separate Zonen. |
| AUT-11 | Datenhaltung: Alle UNS-Daten werden in einer Zeitreihendatenbank (z. B. TimescaleDB oder InfluxDB) ≥ 24 Monate gespeichert; Chargendaten ≥ 5 Jahre (Haltbarkeit plus Rückverfolgung). |

## 8 Normen, Sicherheit, Lieferobjekte und Abnahme

**Normen und Regelwerke**

| ID | Anforderung |
| --- | --- |
| NRM-01 | Hygienic Design: EHEDG-Leitlinien (Doc. 8, 10, 13), DIN EN 1672-2. |
| NRM-02 | Maschinensicherheit: Maschinenrichtlinie 2006/42/EG bzw. Maschinenverordnung (EU) 2023/1230, EN ISO 12100, EN ISO 13849-1 für Sicherheitsfunktionen; Gesamtanlage mit CE-Konformität als verkettete Anlage. |
| NRM-03 | Lebensmittelsicherheit: IFS Food in aktueller Version, HACCP nach Codex Alimentarius; Werkstoffe im Produktkontakt nach EU 1935/2004 und 10/2011. |
| NRM-04 | Darstellung: Fließbilder nach ISO 10628, R&I-Symbole nach ISO 10628-2 / ISA 5.1, Tags nach ISA 5.1, Datenaustausch nach DEXPI, Gebäudemodell IFC 4. |
| NRM-05 | Explosionsschutz: Zucker- und Kakaostaub sind in geschlossenen Anlagenteilen zu bewerten; der Agent weist Zonen nach ATEX 2014/34/EU aus oder begründet, warum keine entstehen. |

**Lieferobjekte des Agenten (Revision A)**

| ID | Lieferobjekt | Format | Abnahmekriterium |
| --- | --- | --- | --- |
| DEL-01 | Verfahrensfließbild M1 + M2, Blackbox M3 | Graphviz DOT → PNG/SVG | Jeder Stoff- und Energiestrom aus Abschnitt 4 und 6 ist enthalten; Massenbilanz schließt auf ±2 % |
| DEL-02 | R&I-Schema M1 + M2 | draw.io-XML (optional DEXPI) | Jedes Equipment und jede Messstelle aus AUT-06 ist mit Tag vorhanden; Symbole nach NRM-04 |
| DEL-03 | Equipment- und Instrumentenliste | CSV | Jeder Tag aus DEL-02 genau einmal, mit Hauptabmessungen und Anschlussleistung; Prüfskript läuft ohne Abweichung |
| DEL-04 | Energiebilanz | Markdown-Tabelle + Python-Skript | Drei Betriebsfälle nach ENE-06, Deckungsgrad nach ENE-02 ausgewiesen |
| DEL-05 | Grundriss mit Zonen, Abständen, Fluchtwegen | ezdxf → DXF | Alle Abstände nach RAU-04 eingehalten; Fluss nach RAU-03 ohne Kreuzung |
| DEL-06 | 3D-Modell Halle + Equipment | CadQuery → STEP, IfcOpenShell → IFC | Kollisionsfrei; Höhen nach RAU-02 |
| DEL-07 | UNS-Topic-Struktur und Datenpunktliste | YAML | Jeder Tag aus DEL-03 hat ein Topic; CCPs nach HYG-07 enthalten |
| DEL-08 | Entscheidungsprotokolle | Markdown (ADR) | Jede Abweichung von einer Vorgabe dieses Lastenhefts ist begründet |
| DEL-09 | Liste verbleibender manueller Tätigkeiten | Markdown | Vollständig nach AUT-01; jede Tätigkeit mit Häufigkeit und Begründung |
| DEL-10 | Grobe Kostenschätzung | Markdown-Tabelle | Je Modul, Genauigkeit ±30 %, Annahmen benannt |

## 9 Änderungsszenario für den Testlauf

In Phase 6 des Tests wird dieses Lastenheft um ein Kapitel ergänzt und der Agent muss alle Artefakte nachziehen. Die Änderung: **Die Linie wird ausschließlich von humanoiden Robotern betreut – auch Wartung, Rohstoff-Anlieferung und Störungsbehebung.** Menschen betreten die Halle nur noch im Ausnahmefall. Das Kapitel wird erst im Test eingefügt; der Agent kennt es vorher nicht.

| ID | Anforderung (wird in Phase 6 ergänzt) |
| --- | --- |
| CHG-01 | Drei humanoide Roboter (Höhe 1,7 m, Reichweite 0,9 m, Traglast 20 kg, Laufzeit 4 h je Ladung) übernehmen alle Tätigkeiten aus DEL-09; Personalschleusen und Umkleiden entfallen. |
| CHG-02 | Ladestationen für die Roboter in jeder Hygienezone, mit Reinigungsschleuse beim Zonenwechsel; Roboter gelten hygienisch wie Personal, ihre Oberflächen sind nach EHEDG abwaschbar. |
| CHG-03 | Arbeitshöhen, Griffe, Ventilhandräder und HMI-Positionen werden für die Roboter-Kinematik ausgelegt, nicht für Menschen; Fluchtwege bleiben nach RAU-04 für den Ausnahmefall erhalten. |
| CHG-04 | Sicherheit: Mensch-Roboter-Kollaboration nach ISO 10218 und ISO/TS 15066 nur in Zone A; in Zone B bis D laufen die Roboter ohne anwesende Menschen, Zutritt eines Menschen stoppt die Roboter. |
| CHG-05 | Jeder Roboter ist ein Teilnehmer im Unified Namespace (Position, Aufgabe, Ladezustand, Fehler) und erhält Aufträge aus dem MES über MQTT. |
| CHG-06 | Erwartete Auswirkungen, die der Agent zu prüfen hat: Grundriss (Schleusen, Ladestationen, Wege), 3D-Modell (Höhen, Zugänge), R&I (Handräder entfallen oder werden motorisiert), Datenpunktliste, Energiebilanz (Ladeleistung), Kostenschätzung. |

Messgrößen für die Auswertung: Zeit bis alle Artefakte konsistent sind, Zahl der Artefakte, die der Agent von selbst anfasst, Zahl der Nachforderungen durch dich.

## 10 Annahmen und offene Punkte

Diese Werte habe ich gesetzt, weil sie im Fragenkatalog nicht festgelegt wurden. Sie sind plausibel für eine Riegellinie dieser Größe, aber frei änderbar – jede Änderung hier ist ein Commit in `spec/`.

- Riegelgewicht 40 g und Füllungsanteil 40 % (PRD-02) – typisch für gefüllte Riegel, frei wählbar.
- One-Shot-Gießen statt Überziehen (PRC-13) – passt zu 2.000 Riegeln/h und zum Lights-out-Ziel, weil es weniger Rücklauf und keine Enrobier-Reinigung braucht. Alternative Überziehlinie wäre eine ADR für den Agenten.
- Temperierkurven, Lagertemperaturen und Kühltunnelwerte (PRC-03, PRC-05, PRC-15) – übliche Richtwerte; der Rezeptentwickler der Chocolaterie würde sie bestätigen.
- Füllungsrezeptur als gekochte Zuckercreme mit a\_w ≤ 0,65 (PRD-08, PRC-09) – nötig für 9 Monate Haltbarkeit ohne Konservierung.
- Energiekennzahl ≤ 0,9 kWh/kg (ENE-06) – ambitionierter Zielwert für eine all-electric Linie mit Abwärmenutzung; dient dem Agenten als Optimierungsziel, nicht als Abnahmekriterium.
- Anschlussleistung ≤ 250 kW (ENE-01) – Annahme zur Leistung des Wasserkraftwerks.
- Zonenmodell mit vier Zonen (HYG-01) – vereinfachtes IFS-Zonierungsmodell.

**Geplante Ausnahmen vom Lights-out-Betrieb:** halbjährliche Komplettreinigung des Schokoladenstrangs, Rohstoff-Anlieferung bis zur Schleuse, Wartung mit Stillstand. Alles Weitere, was der Agent als manuell einstuft, landet in DEL-09 und wird diskutiert.

**Offene Punkte für dich:**

- [ ] Riegelgewicht und Füllungsanteil bestätigen oder ändern
- [ ] Kräuterextrakt: angeliefert (angenommen) oder vor Ort aus getrockneten Kräutern extrahiert?
- [ ] Saisonmodell (PRD-04) gegen die Markenstory prüfen – Oktober bis März angenommen
- [ ] Soll M3 im zweiten Durchlauf wirklich ausgeplant werden oder Blackbox bleiben?
- [ ] Das Roboter-Kapitel vor dem Test aus diesem Dokument herauslösen, damit der Agent es nicht vorab liest
