# NXOS télémétrie avec Telegraf, InfluxDB et Grafana

# Installation de la VM TIG

## Virtual Machine

### Prerequis

image : ubuntu-20.04.4-live-server-amd64.iso

2 voire 4 CPUs / 32G RAM / 200G Disk thin provisioning

### Configuration NTP client

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

### Accès root en SSH

::A compléter::

## InfluxDB

> Utilisation de InfluxDB 1.8. En effet, à partir de la version 2.0 il y a de nombreux changements (Web UI, authentification par token, databases remplacées par buckets, nouveau language de query flux). L'interfaçage de Grafana avec flux reste encore très limité.

Récupération du dernier package InfluxDB 1.8 :

```shell
wget https://dl.influxdata.com/influxdb/releases/influxdb_1.8.10_amd64.deb
```

Installation du package :

```shell
sudo dpkg -i influxdb_1.8.10_amd64.deb
```

Paramétrage du service pour qu’il démarre au boot :

```shell
sudo /bin/systemctl daemon-reload
sudo /bin/systemctl enable influxdb
sudo /bin/systemctl start influxdb
```

Vérification de l’état du service :

```shell
labuser@telemetry:~$ sudo service influxdb status
● influxdb.service - InfluxDB is an open-source, distributed, time series database
     Loaded: loaded (/lib/systemd/system/influxdb.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2022-03-21 16:39:58 CET; 19h ago
       Docs: https://docs.influxdata.com/influxdb/
    Process: 2748 ExecStart=/usr/lib/influxdb/scripts/influxd-systemd-start.sh (code=exited, status=0/SUCCESS)
   Main PID: 2754 (influxd)
      Tasks: 14 (limit: 38430)
     Memory: 97.9M
     CGroup: /system.slice/influxdb.service
             └─2754 /usr/bin/influxd -config /etc/influxdb/influxdb.conf
```

## Telegraf

Configuration du repository pour telecharger le package :

```shell
wget -qO- https://repos.influxdata.com/influxdb.key | sudo tee /etc/apt/trusted.gpg.d/influxdb.asc >/dev/null

source /etc/os-release

echo "deb https://repos.influxdata.com/${ID} ${VERSION_CODENAME} stable" | sudo tee /etc/apt/sources.list.d/influxdb.list

sudo apt-get update
```

Installation du package :

```shell
sudo apt-get install telegraf
```

## Grafana

Installation du package `libfontconfi1`, bibliothèque de configuration de polices générique

```plaintext
sudo apt-get install -y adduser libfontconfig1
```

Récupération du dernier package Grafana :

```shell
wget https://dl.grafana.com/enterprise/release/grafana-enterprise_8.4.4_amd64.deb
```

Installation du package :

```other
sudo dpkg -i grafana-enterprise_8.4.4_amd64.deb
```

Paramétrage du service pour qu’il démarre au boot :

```shell
sudo /bin/systemctl daemon-reload
sudo /bin/systemctl enable grafana-server
sudo /bin/systemctl start grafana-server
```

Vérification de l’état du service :

```shell
labuser@telemetry:~$ sudo service grafana-server status
● grafana-server.service - Grafana instance
     Loaded: loaded (/lib/systemd/system/grafana-server.service; enabled; vendor preset: enabled)
     Active: active (running) since Tue 2022-03-22 12:38:02 CET; 25s ago
       Docs: http://docs.grafana.org
   Main PID: 45597 (grafana-server)
      Tasks: 9 (limit: 38430)
     Memory: 33.4M
     CGroup: /system.slice/grafana-server.service
             └─45597 /usr/sbin/grafana-server --config=/etc/grafana/grafana.ini --pidfile=/run/grafana/grafana-server.pid --packaging=deb cfg:default.paths.logs=/var/log>
```

