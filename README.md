# Temperaturkonverter

Eine kleine Python-Anwendung zur Umrechnung von Celsius in Fahrenheit und Fahrenheit in Celsius. Automatisierte Tests prüfen die Berechnungen. GitHub Actions testet und paketiert die Anwendung und veröffentlicht sie nach Freigabe als GitHub Release.

## Funktionen

- `celsius_zu_fahrenheit(celsius)` rechnet Celsius in Fahrenheit um.
- `fahrenheit_zu_celsius(fahrenheit)` rechnet Fahrenheit in Celsius um.

Die Anwendung stellt Python-Funktionen bereit. Sie besitzt keine grafische Oberfläche oder interaktive Eingabe.

## Projektstruktur

- `src/konverter.py`: Umrechnungsfunktionen
- `tests/test_konverter.py`: drei automatisierte Tests
- `requirements.txt`: benötigtes Testwerkzeug pytest
- `.github/workflows/pipeline.yml`: CI/CD-Workflow
- `README.md`: Projektdokumentation

## Pipeline und Architektur

| Job | Aufgabe | Trigger / Bedingung | Abhängigkeit | Environment | Artifact |
|---|---|---|---|---|---|
| test | Python einrichten, Cache nutzen, Abhängigkeiten installieren und Tests ausführen | Push und Pull Request | Keine | Keines | Keines |
| build | Anwendung paketieren und Artifact hochladen | Nach erfolgreichen Tests | test | Keines | Erzeugt temperatur-konverter-paket |
| deploy | Artifact herunterladen und Release veröffentlichen | Nur Push auf main, nach erfolgreichem Build und Freigabe | build | production | Verwendet temperatur-konverter-paket |

Der Workflow verwendet Python 3.12. Die Version wird zentral über `PYTHON_VERSION` festgelegt.

Der pip-Cache berücksichtigt das Betriebssystem und den Inhalt von `requirements.txt`. Er beschleunigt die Installation durch Wiederverwendung heruntergeladener Pakete.

Das ZIP wird einmal im Test-Job gebaut. Der Deployment-Job übernimmt dieses Ergebnis und baut es nicht erneut.

## Trigger und Schutzregeln

Der Workflow startet bei Push und Pull Request.

Auf Arbeitsbranches und bei Pull Requests wird das Deployment übersprungen. Bei fehlgeschlagenen Tests werden der Build-Job und anschließend der Deployment-Job übersprungen.

Das Environment `production` verlangt eine manuelle Freigabe und erlaubt Deployments ausschließlich vom Branch `main`.

## Secrets und Variablen

| Name | Typ | Verwendung |
|---|---|---|
| `PYTHON_VERSION` | Workflow-Umgebungsvariable | Legt die Python-Version fest |
| `DEPLOY_TARGET` | Repository-Variable | Bezeichnet das Deployment-Ziel |
| `DEPLOY_TOKEN` | Repository-Secret | Fantasiewert zum Demonstrieren des sicheren Secret-Zugriffs |
| `GITHUB_TOKEN` | Von GitHub bereitgestelltes Token | Authentifiziert die Erstellung des Releases |

Die Secret-Prüfung bestätigt nur, dass ein Wert vorhanden ist. Secret-Werte werden nicht ausgegeben oder in das Anwendungspaket aufgenommen.

Der Workflow erhält grundsätzlich `contents: read`. Der Deployment-Job erhält gezielt `contents: write` und `actions: read`.

## Deployment

Nach einem erfolgreichen Push-Lauf auf `main` und der Environment-Freigabe erstellt die Pipeline ein GitHub Release.

Die Version hat das Format `v1.0.<Laufnummer>`. Der Release-Tag verweist auf den Commit des Workflow-Laufs.

Unter „Releases“ ist das Paket `temperatur-konverter.zip` als Asset verfügbar. Es enthält den Anwendungscode, die README und die Abhängigkeitsdatei.

Dieses Übungsprojekt veröffentlicht ein Paket; es betreibt keinen Server.

## Lokal einrichten

Voraussetzung: Python 3.10 oder neuer. Die Pipeline verwendet Python 3.12.

Nach dem Klonen im Hauptordner des Projekts ausführen:

```bash
python -m venv .venv
```

Umgebung unter macOS oder Linux aktivieren:

```bash
source .venv/bin/activate
```

Alternativ unter Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Abhängigkeiten installieren:

```bash
python -m pip install -r requirements.txt
```

Falls außerhalb der aktivierten Umgebung nur `python3` verfügbar ist, diesen Befehl beim Erstellen der Umgebung verwenden.

## Anwendung ausprobieren

Im Hauptordner bei aktivierter Umgebung ausführen:

```bash
python -c "from src.konverter import celsius_zu_fahrenheit; print(celsius_zu_fahrenheit(0))"
```

Erwartete Ausgabe: `32.0`.

## Tests ausführen

```bash
python -m pytest -v
```

Die drei Tests prüfen:

- 0 °C ergeben 32 °F.
- 212 °F ergeben 100 °C.
- −40 °C ergeben −40 °F.

Erwartetes Ergebnis: `3 passed`.

## Paket lokal bauen

Aus dem Hauptordner ausführen:

```bash
python -c "from pathlib import Path; Path('build').mkdir(exist_ok=True)"
python -m zipfile -c build/temperatur-konverter.zip src/ README.md requirements.txt
```

Das Ergebnis liegt unter `build/temperatur-konverter.zip`.

## Durchgeführte Pipeline-Prüfungen

- Erfolgreicher Testlauf lokal und in GitHub Actions.
- Wiederherstellung des Dependency-Caches.
- Übergabe des Build-Artifacts an den zweiten Job.
- Deployment wartet auf Environment-Freigabe.
- Automatisches Release mit ZIP-Asset.
- Pull Request: Tests erfolgreich, Deployment übersprungen.
- Absichtlich falsche Test-Erwartung: Testlauf fehlgeschlagen, keine Veröffentlichung.
- Nach Reparatur und Merge: erfolgreicher Lauf und Veröffentlichung nach Freigabe.