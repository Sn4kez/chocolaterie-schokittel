---
id: spec-09-aenderungsszenario
title: Änderungsszenario – Betrieb ausschließlich durch humanoide Roboter
version: 1.0
status: released
note: Erst in Phase 6 des Tests nach spec/ kopieren. Der Agent darf diese Datei vorher nicht kennen.
---

# 9 Änderungsszenario

Die Linie wird ausschließlich von humanoiden Robotern betreut – auch Wartung, Rohstoff-Anlieferung
und Störungsbehebung. Menschen betreten die Halle nur noch im Ausnahmefall. Alle Artefakte sind
nachzuziehen.

| ID | Anforderung |
| --- | --- |
| CHG-01 | Drei humanoide Roboter (Höhe 1,7 m, Reichweite 0,9 m, Traglast 20 kg, Laufzeit 4 h je Ladung) übernehmen alle Tätigkeiten aus DEL-09; Personalschleusen und Umkleiden entfallen. |
| CHG-02 | Ladestationen für die Roboter in jeder Hygienezone, mit Reinigungsschleuse beim Zonenwechsel; Roboter gelten hygienisch wie Personal, ihre Oberflächen sind nach EHEDG abwaschbar. |
| CHG-03 | Arbeitshöhen, Griffe, Ventilhandräder und HMI-Positionen werden für die Roboter-Kinematik ausgelegt, nicht für Menschen; Fluchtwege bleiben nach RAU-04 für den Ausnahmefall erhalten. |
| CHG-04 | Sicherheit: Mensch-Roboter-Kollaboration nach ISO 10218 und ISO/TS 15066 nur in Zone A; in Zone B bis D laufen die Roboter ohne anwesende Menschen, Zutritt eines Menschen stoppt die Roboter. |
| CHG-05 | Jeder Roboter ist ein Teilnehmer im Unified Namespace (Position, Aufgabe, Ladezustand, Fehler) und erhält Aufträge aus dem MES über MQTT. Tags: R-301, R-302, R-303. |
| CHG-06 | Zu prüfen und nachzuziehen: Grundriss (Schleusen, Ladestationen, Wege), 3D-Modell (Höhen, Zugänge), R&I (Handräder entfallen oder werden motorisiert), Datenpunktliste, Energiebilanz (Ladeleistung), Kostenschätzung, Liste manueller Tätigkeiten. |
