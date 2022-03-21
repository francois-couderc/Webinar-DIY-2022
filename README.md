# Telemetry

# Installation de la VM TIG

## Prerequis

image : ubuntu-20.04.4-live-server-amd64.iso

4 CPUs / 32G RAM / 200G Disk thin provisioning

## Configuration NTP client

Ajouter l’IP du serveur NTP dans `/etc/systemd/timesyncd.conf` :

```shell
[Time]
NTP=192.168.123.254
```

Redémarrer le service NTP :

```shell
sudo systemctl restart systemd-timesyncd.service
```

Changer la timezone à Paris (CET +1) :

```shell
sudo timedatectl set-timezone Europe/Paris
```

Vérification de la synchronisation NTP :

```shell
labuser@telemetry:~$ timedatectl
               Local time: Mon 2022-03-21 09:25:33 CET
           Universal time: Mon 2022-03-21 08:25:33 UTC
                 RTC time: Mon 2022-03-21 08:25:34
                Time zone: Europe/Paris (CET, +0100)
System clock synchronized: yes
              NTP service: active
          RTC in local TZ: no
```

# InfluxDB 2.x

## Installation

Téléchargement :

```shell
wget -qO- https://repos.influxdata.com/influxdb.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/influxdb.gpg > /dev/null

export DISTRIB_ID=$(lsb_release -si); export DISTRIB_CODENAME=$(lsb_release -sc)

echo "deb [signed-by=/etc/apt/trusted.gpg.d/influxdb.gpg] https://repos.influxdata.com/${DISTRIB_ID,,} ${DISTRIB_CODENAME} stable" | sudo tee /etc/apt/sources.list.d/influxdb.list > /dev/null

sudo apt-get update && sudo apt-get install influxdb2
```

Démarrage du service :

```shell
labuser@telemetry:~$ sudo service influxdb start
labuser@telemetry:~$
labuser@telemetry:~$
labuser@telemetry:~$ sudo service influxdb status
● influxdb.service - InfluxDB is an open-source, distributed, time series database
     Loaded: loaded (/lib/systemd/system/influxdb.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2022-03-21 09:40:20 CET; 3s ago
       Docs: https://docs.influxdata.com/influxdb/
    Process: 2090 ExecStart=/usr/lib/influxdb/scripts/influxd-systemd-start.sh (code=exited, status=0/SUCCESS)
   Main PID: 2097 (influxd)
      Tasks: 9 (limit: 38430)
     Memory: 40.1M
     CGroup: /system.slice/influxdb.service
             └─2097 /usr/bin/influxd
```

## Paramétrage de base

Se connecter en http sur la VM avec le port 8086 et remplir le setup initial :

![Image.png](https://res.craft.do/user/full/e518ba39-7261-549d-a2bc-1efbdbb6baa4/doc/0C184547-4BE1-4D4C-B931-A7B3731801F2/28ACD663-6C99-4CBF-B07E-137C37F7885B_2/xfXRcVjBcPDDcWo8BophCvWK1Cwe44xxU4B0AHjZ0cEz/Image.png)

