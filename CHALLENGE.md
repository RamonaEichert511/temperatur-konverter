# Abschluss-Challenge: Pipeline debuggen

| Nr. | Symptom / Risiko | Ursache | Korrektur |
|---|---|---|---|
| 1 | Die Setup-Action erhält möglicherweise 3.1 statt 3.10 und kann fehlschlagen. | Die Versionsangabe steht ohne Anführungszeichen und wird als Zahl interpretiert. | Version als Text angeben, etwa "3.10", oder die zentrale Variable über env verwenden. |
| 2 | Die Tests können nicht starten, weil pytest fehlt. | Der Test-Step steht vor der Installation der Abhängigkeiten. | Zuerst Abhängigkeiten installieren, danach Tests ausführen. |
| 3 | Die Installation scheitert, weil die angegebene Datei nicht gefunden wird. | Im Dateinamen requirement.txt fehlt das s. | Den Dateinamen zu requirements.txt korrigieren. |
| 4 | Der Build findet src/ nicht und ist nicht an erfolgreiche Tests gekoppelt. | Im Build-Job fehlen Checkout und die Abhängigkeit vom Test-Job. | Repository-Code mit Checkout holen und needs: test ergänzen. |
| 5 | Deployment kann ohne erfolgreiche Tests, auf unerlaubten Branches und ohne Freigabe laufen; der Secret-Wert wird zur Ausgabe verwendet. | needs, if und environment fehlen; echo gibt das Secret aus. | Test-Abhängigkeit, Branch-/Event-Bedingung und geschütztes Environment ergänzen; Secret nur im benötigten Step verwenden und seinen Wert nicht ausgeben. |
| 6 | Der Cache wird bei Änderungen der Abhängigkeiten nicht passend erneuert. | Der feste Schlüssel pip-cache berücksichtigt weder Betriebssystem noch Inhalt der requirements.txt. | Den Schlüssel aus runner.os und hashFiles('requirements.txt') bilden. |