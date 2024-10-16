<div align="center">
    <a href="https://ibb.co/PjBGh4W">
        <img src="https://i.ibb.co/vq24Pmd/kuva2.png" alt="kuva2" width="600">
    </a>
</div>
</div>


Konsepti Metsästäjästä on yksinkertainen: Teimme sivun joka pyytää sijaintia, kuten monet suositut sijaintiin perustuvat verkkosivustot. Metsästäjä isännöi valeverkkosivustoa, joka kysyy sijaintilupaa, ja jos kohde myöntää sen, voimme saada:

* Pituusaste
* Leveysaste
* Tarkkuus
* Korkeus - ei aina saatavilla
* Suunta - saatavilla vain jos käyttäjä liikkuu
* Nopeus - saatavilla vain jos käyttäjä liikkuu
* Sijaintitietojen lisäksi saamme myös laitetietoja ilman mitään lupia:

* Yksilöllinen tunnus käyttäen Canvas Fingerprinting -menetelmää
* Laitemalli - ei aina saatavilla
* Käyttöjärjestelmä
* Alusta
* CPU-ytimien määrä - noinarvio
* RAM-muistin määrä - noinarvio
* Näytön resoluutio
* GPU-tiedot
* Selaimen nimi ja versio
* Julkinen IP-osoite
* Paikallinen IP-osoite
* Paikallinen portti

**Automaattinen IP-osoitteen tiedustelu** suoritetaan sen jälkeen, kun yllä oleva tieto on vastaanotettu.

**Tämä työkalu on todiste konseptista ja vain koulutustarkoituksiin. Metsästäjä näyttää, mitä tietoja haitallinen verkkosivusto voi kerätä sinusta ja laitteistasi, ja miksi et pitäisi klikata satunnaisia linkkejä ja sallia kriittisiä lupia, kuten sijaintia jne.**

## Miten tämä eroaa IP-geo-sijainnista

* Muut työkalut ja palvelut tarjoavat IP-geo-sijaintia, joka EI ole tarkka ollenkaan, eikä se anna kohteen sijaintia, vaan se on ISP:n arvioitu sijainti.

* Metsästäjä käyttää HTML API:a ja saa sijaintiluvan, ja sitten se nappaa pituusasteen ja leveysasteen laitteen GPS-laitteiston avulla, joten Seeker toimii parhaiten älypuhelimilla. Jos GPS-laitteistoa ei ole, kuten kannettavassa tietokoneessa, Seeker siirtyy IP-geo-sijaintiin tai etsii välimuistissa olevia koordinaatteja.

* Yleisesti ottaen, jos käyttäjä hyväksyy sijaintiluvan, saamasi tiedon tarkkuus on **noin 30 metrin tarkkuudella**.

* Tarkkuus riippuu useista tekijöistä, joita voit hallita tai et, kuten:
  * Laite - ei toimi kannettavissa tai puhelimissa, joissa GPS on rikki
  * Selaimen - jotkut selaimet estävät JavaScriptit
  * GPS-kalibrointi - jos GPS:ää ei ole kalibroitu, saatat saada epätarkkoja tuloksia, ja tämä on hyvin yleistä.

## Mallit

Saatavilla olevat mallit:

* NearYou
* Google Drive
* WhatsApp
* Telegram
* Zoom
* Google reCAPTCHA

## Testattu
* Kali Linux
* BlackArch Linux
* Ubuntu
* Fedora
* Kali Nethunter
* Termux
* Parrot OS
* OSX - Monterey v.12.0.1

## Asennus

### Kali Linux / Arch Linux / Ubuntu / Fedora / Parrot OS / Termux

```bash
git clone https://github.com/Chae-Tzuyu/Metsastaja.git
cd metsastaja/
chmod +x install.sh
./install.sh
```

### BlackArch Linux

```bash
sudo pacman -S metsastaja
```

### Docker

```bash
docker pull Chae-Tzuyu/metsastaja
```

### OSX
```bash
git clone https://github.com/Chae-Tzuyu/Metsastaja.git
cd seeker/
python3 metsastaja.py
````

In order to run in tunnel mode, install ngrok by running this command in the terminal:
```bash
brew install ngrok/ngrok/ngrok

ngrok http 8080
````

## Usage

```bash
python3 metsastaja.py -h

usage: metsastaja.py [-h] [-k KML] [-p PORT] [-u] [-v] [-t TEMPLATE] [-d] [--telegram token:chatId] [--webhook WEBHOOK]


asetukset:
  -h, --help                            näytä tämä apuviesti ja lopeta
  -k KML, --kml KML                     KML-tiedoston nimi
  -p PORT, --port PORT                  Verkkopalvelimen portti [Oletus: 8080]
  -u, --update                          Tarkista päivitykset
  -v, --version                         Tulostaa version
  -t TEMPLATE, --template TEMPLATE      Valitse automaattisesti malli annetulla indeksillä
  -d, --debugHTTP                       Poista automaattinen http --> https -uudelleenohjaus käytöstä testaus tarkoituksiin 
                                        (toimii vain malleilla, joilla on index_temp.html-tiedosto)
  --telegram                            Lähetä tietoja Telegram-botille, anna Telegram-token ja keskustelu käyttöön
                                        muoto = token:chatId erotettuna kaksoispisteellä
  --webhook                             Lähetä tapahtumia webhook-päätepisteeseen käsiteltäväksi
                                        Huom: päätepisteen on oltava todennusvapaa ja hyväksyttävä POST-pyyntö

#########################
# Ympäristömuuttujat #
#########################

Joitakin yllä olevista vaihtoehdoista voidaan myös ottaa käyttöön ympäristömuuttujien kautta, jotta käyttöönotto olisi helpompaa.
Muut parametrit voidaan antaa ympäristömuuttujien kautta vuorovaikutteisen tilan välttämiseksi.

Muuttujat:
  DEBUG_HTTP            Sama kuin -d, --debugHTTP
  PORT                  Sama kuin -p, --port
  TEMPLATE              Sama kuin -t, --template
  TITLE                 Anna ryhmän otsikko tai sivun otsikko
  REDIRECT              Anna URL, johon käyttäjä ohjataan työn valmistuttua
  IMAGE                 Anna käytettävä kuva, voi olla joko etä (http tai https) tai paikallinen
                        Huom: Etäkuva ladataan paikallisesti käynnistyksen aikana
  DESC                  Anna kohteen kuvaus (ryhmä tai verkkosivusto mallista riippuen)
  SITENAME              Anna verkkosivuston nimi
  DISPLAY_URL           Anna URL, joka näytetään sivulla
  MEM_NUM               Anna ryhmän jäsenten määrä (toistaiseksi Telegram)
  ONLINE_NUM            Anna ryhmän online-jäsenten määrä (toistaiseksi Telegram)
  TELEGRAM              Anna Telegram-token ja keskustelu, jota käytetään tietojen lähettämiseen Telegram-botille
                        muoto = token:chatId erotettuna kaksoispisteellä
  WEBHOOK               Anna webhook-URL, jolle tapahtumat ohjataan 
                        Huom: päätepisteen on oltava todennusvapaa ja hyväksyttävä POST-menetelmä
                        

##################
# Käyttöesimerkit #
##################

# Vaihe 1 : Ensimmäisessä terminaalissa
$ python3 metsastaja.py

# Vaihe 2 : Toisessa terminaalissa käynnistä tunnelipalvelu, kuten ngrok
$ ./ngrok http 8080

###########
# Vaihtoehdot #
###########

# Tulosta KML-tiedosto Google Earthille
$ python3 metsastaja.py -k <tiedostonimi>

# Käytä mukautettua porttia
$ python3 metsastaja.py -p 1337
$ ./ngrok http 1337

# Valitse etukäteen tietty malli
$ python3 metsastaja.py -t 1

################
# Dockerin käyttö #
################

# Vaihe 1
$ docker network create ngroknet

# Vaihe 2
$ docker run --rm -it --net ngroknet --name seeker Chae-Tzuyu/metsastaja

# Vaihe 3
$ docker run --rm -it --net ngroknet --name ngrok wernight/ngrok ngrok http metsastaja:8080
