# Prosjekt i PY1010

# Les meg først

# Passordbehandler

Eier: Laurent Zogaj  
Dato levert: 11. april 2025  

## Beskrivelse
Dette prosjektet er en passordbehandler som gjør det mulig for brukeren å lagre, hente og administrere passord lokalt på datamaskinen.  
Passordene krypteres ved hjelp av biblioteket cryptography med symmetrisk kryptering (Fernet).  
Programmet gir også mulighet til å generere tilfeldige og sikre passord.
Innholdet blir lagret på en csv fil og krypteres/dekrypteres der.

## Ulike funksjoner
- Sikker lagring og henting av passord
- Generering av sterke tilfeldige passord
- Enkel grafisk brukergrensesnitt (GUI)
- Oversiktlig visualisering av lagrede plattformer

## Avhengigheter som må lastes ned
- cryptography
- numpy
- matplotlib

## Filstruktur
Filene under vil bli lagret lokalt på pcen din dersom du velger å kjøre py filen ene og alene.
Dersom du vil se filene som blir opprettet ved kjøring av programmet anbefaler jeg å åpne programmet via mappen jeg har laget "Prosjekt i PY1010" og åpne hele den mappen i en kode editor/IDE.
- `passord.csv`: Lagrede passord
- `hemmelig.nøkkel`: Krypteringsnøkkel

## Hvordan kjøre programmet

### Installer nødvendige pakker 
```sh
pip install cryptography numpy matplotlib
