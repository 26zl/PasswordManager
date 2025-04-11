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
Last ned hele prosjektet som zip. Deretter åpne det i din prefererte IDE/kode-editor. Installer så pakkene og kjør programmet. 
Du vil da se filene under opprettet.

- `passord.csv`: Lagrede passord
- `hemmelig.nøkkel`: Krypteringsnøkkel

## Hvordan kjøre programmet

### Installer nødvendige pakker 
```sh
pip install cryptography numpy matplotlib
