# RPI-HomeWatch

Überwachen Sie einen Raum Ihrer Wahl im eigenen Heim...

Diese Dokumentation finden sie auch in der MSWord-Datei.

## Benötigte Bauteile

-	Raspberry Pi (RPI; 1, 2 oder 3)
(mit Anschlussmöglichkeit einer Kamera → USB theoretisch auch möglich, es gibt aber elegantere Varianten)
-	Kamera zum Anschließen
-	Einen externen Computer, als Empfänger, am besten das haushaltsübliche Windows
-	Netzwerkkabel  (Ethernet)
Zur erstmaligen Einrichtung mindestens:
-	Einen HDMI-fähigen-Monitor
-	HDMI-Kabel
-	Tastatur
-	Maus

## Raspian installieren
Das Betriebssystem (OS) „Raspian“ ist speziell vom Hersteller für die Hardware entwickelt worden, basiert auf der Linux-Variante Debian und bietet dem normalen Nutzer eine voll funktionsfähige Desktop-Erfahrung. <br />
Sollten Sie eine SD-Karte mit NOOBS und Raspian vorliegen haben, können Sie dieses direkt auf dem Pi installieren.

![NOOBS Install IMG](https://www.chip.de/ii/2/5/5/5/3/9/0/5/0320ca025068cc50.jpg)

Sollte dies nicht der Fall sein, empfiehlt es sich das Raspian System direkt auf eine leere SD/microSD Karte zu installieren,  <br /> wobei Sie ab Modell RPI 3B+ einen USB-Stick verwenden sollten, da dieser weitaus weniger empfindlich ist und ohne großartige Änderungen vom Stick bootet. <br />
Ob sie das Betriebssystem nun auf USB oder SD/microSD schreiben, hierfür eignet sich das Programm „Etcher“ bzw. das ehemals empfohlene Tool „win32diskimager“. Beide erfordern auf dem System Administratorrechte, denn das zu beschreibende Laufwerk wird automatisch formatiert. Den Link zum Download des Systems selbst finden Sie auf der Hersteller-Projektwebseite. Welche Version des Betriebssystems Sie installieren bleibt Ihnen überlassen, wobei es sich nach Möglichkeit empfiehlt, das neueste zu verwenden.

## Raspian kennenlernen
Im Beispiel verwenden wir die OS Version vom März 2018. Wir haben die Version direkt auf einen 32 GB USB 3.0 Stick kopiert und haben somit zunächst eine Sprachumgebung („Locale“). <br />
Wir wollen zunächst sicherstellen, dass die deutsche Sprache korrekt eingestellt ist (im Beispielfall ist sie es wie bereits erwähnt ja nicht) und dann das bereits erwähnte VNC-Protokoll aktivieren. <br />
Das Menü erreichen Sie über die rote Himbeere, die sich im Auslieferungszustand im oberen, linken Rand befindet. Es lässt sich auch mit der Windows-Taste, die bei Linux „Superkey“ genannt wird öffnen, sowie auch schließen. Hier wählen wir den Menüpunkt „Preferences“ 

![Raspbian Menu](http://justpic.info/images4/ed22/2018110113_12_17192.168.1.22raspberrypiVNCViewer.png)

Hier wählen wir nun „Raspberry Pi Configuration“, um das schlanke Einstellungsmenü aufzurufen.

![Raspbian Menu Config](http://justpic.info/images4/3f1d/2018110113_14_56192.168.1.22raspberrypiVNCViewer.png)

Im Einstellungs-Tab „Localisation“ klicken auf „Set Locale…“

![Raspbian Menu SetLocale](http://justpic.info/images4/52f8/2018110113_19_17192.168.1.22raspberrypiVNCViewer.png)

Im folgenden Fenster wollen Sie die Einstellungen wie im Bild festlegen:	

![Raspbian SetLocale](http://justpic.info/images4/eb2a/2018110114_01_13192.168.1.22raspberrypiVNCViewer.png)


Danach starten sie den RPI neu um die Änderungen zu übernehmen. <br />

Es kann sein, dass Warnungen angezeigt werden, welche nicht übersetzt wurden, <br />
u.a. gibt es eine SSH-Warnung, die, sofern der Pi – physisch oder auch virtuell nicht öffentlich zugänglich ist ignoriert werden kann. Ansonsten ist es empfehlenswert das Passwort zu ändern. Wir kommen später zu der Anleitung.

## Terminal-Basics
-	Wird auf ein neuen Befehl gewartet, so ist $-Symbol in der letzten Zeile das Zeichen am weitesten rechts
    -	Wenn ein Befehl fertig ist, wartet das Terminal auf den nächsten Befehl.
-	Wenn nach Befehlsbestätigung (Enter-Taste) kein Text angezeigt wird, ist es wahrscheinlich, dass ein Befehl ausgeführt wurde, der keine Ausgabe hatte.
 
## Text-Bearbeitungsprogramm (Windows)
Vermutlich sollten Sie der aus Gründen der extremen Erleichterung der Arbeit sämtliche Dateiänderungen am Windows-Rechner vornehmen, um den Überblick zu behalten. <br />
Sie benötigen aber ei n Programm, welches
-	einfache & zeichengenaue Markierungen zulässt (die schließt Wordpad aus)
-	Dateien mit Linux-Zeilenbeendungszeichnen lesen und speichern kann (dies schließt Editor/notepad.exe aus)
Als sehr gutes Programm für solche Zwecke hat sich Notepad++ gezeigt. <br />

## Raspberry Pi fernsteuern
Um den Raspberry Pi auch nachher ohne Maus und Tastatur angeschlossen steuern zu können, wollen wir zunächst eine Desktop-Fernsteuerungs-Software, genannt VNC („Virtual Network Computing“ = Virtuelles Netzwerk Rechnen) auf dem Raspberry Pi aktivieren. Sofern Maus und Tastatur stets ohne Schwierigkeiten angeschlossen werden können ist dieser Schritt nicht zwingend erforderlich, er wird lediglich empfohlen, denn es erleichtert die Arbeit  und vermeidet das wechseln zwischen Monitoren. Zusätzlich kann es auch hilfreich sein dass SSH-Protokoll zu aktivieren, um die Kommandozeile des Pis komfortabler nutzen zu können und gewisse Befehle leichter eingeben zu können. <br />
Wir wollen im Beispiel mal demonstrieren, wie beides geht. <br />
Aktivieren Sie wie im Bild also SSH und VNC.

![Raspbian Config Enable VNCnSSH](http://justpic.info/images4/d076/2018110115_15_58192.168.1.22raspberrypiVNCViewer.png)

Bestätigen Sie die Änderungen mit „OK“
Nun können Sie die grafische Oberfläche mit einem VNC-Client ansteuern und textbasierte Befehle via SSH-Client.
Für Windows, empfehlen sich:
-	RealVNC-Viewer und
-	KiTTY als SSH Client 

In beiden lediglich an die dafür vorgesehene Stelle die IP-Adresse des Pis angeben und die Verbinden-Schaltfläche drücken oder mit Enter-Taste bestätigen. <br />
Falls sie die IP Adresse noch erfahren müssen können Sie die Datei `ipaddress`, auf den Benutzerordner kopieren, und dann die folgenden Befehle ausführen um ihr IP im Terminal/SSH ausführen, um so leicht wie möglich ablesen zu können.

    chmod +x ipaddress
    ./ipaddress
Wenn letzterer keinen Text anzeigt und das Terminal erwartet sofort eine neue Befehlseingabe, dann ist vermutlich gar kein Netzwerk aktiv. <br />

## Root-Rechte ohne Passwort
Es gibt im Stammverzeichnis des Projekts eine Datei mit dem Namen motionmagic.py
Diese Datei sorgt dafür, dass Sie unter der untenstehenden Voraussetzung das Überwachungs-Programm motion auch von unterwegs steuern können. <br />
Sollten Sie diese verwenden wollen ist es erforderlich, dass der aktive Benutzer auf dem Raspberry Pi root (Admin-) Rechte hat, die ohne Passworteingabe erfolgen. <br />
Hierbei muss folgende die Rechte-Datei bearbeitet werden. <br />
Sie fangen eine Bearbeitung mit dem Befehl sudo visudo an.

![Raspbian visudo](http://justpic.info/images4/b977/2018110708_08_33192.168.1.22raspberrypiVNCViewer.png)

Die Zeile unter `#User privileges specification` soll exact so aussehen wie im Bild. <br />
Mit Strg+O speichern sie die Datei und mit Strg+X verlassen Sie den Bearbeitungs-Modus… <br />
Wenn nun auf einen neuen Befehl gewartet wird haben Sie alles richtig gemacht, <br />
liest man stattdessen u.a. „Was jetzt?“ steht, brechen Sie den endgültigen Speichervorgang mit „x“ (Bestätigung mit Enter-Taste) ab.


## Beispiel-Bildatei
![Cam-Img](shot.jpg)
![Cam-Img](shot.jpg)
