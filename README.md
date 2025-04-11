# Prosjekt i PY1010

# Passordbehandler

Eier: Laurent Zogaj  
Dato levert: 11. april 2025  

## Beskrivelse
Dette prosjektet er en passordbehandler som gjør det mulig for brukeren å lagre, hente og administrere passord lokalt på datamaskinen.  
Passordene krypteres ved hjelp av biblioteket cryptography med symmetrisk kryptering (Fernet).  
Programmet gir også mulighet til å generere tilfeldige og sikre passord.

## Funksjoner
- Sikker lagring og henting av passord
- Generering av sterke tilfeldige passord
- Enkel grafisk brukergrensesnitt (GUI)
- Oversiktlig visualisering av lagrede plattformer

## Avhengigheter
- cryptography
- numpy
- matplotlib

## Filstruktur
- `passord.csv`: Lagrede passord
- `hemmelig.nøkkel`: Krypteringsnøkkel

## Hvordan kjøre programmet

### Installer nødvendige pakker 
```sh
pip install cryptography numpy matplotlib