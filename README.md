# PassordBehandler

**Eier:** Laurent Zogaj  
**Dato levert:** 11. april 2025  

## Beskrivelse
Dette prosjektet er en passordbehandler som gjør det mulig for brukeren å lagre, hente og administrere passord lokalt på datamaskinen.  

Passordene krypteres ved hjelp av biblioteket cryptography med symmetrisk kryptering (Fernet). Programmet gir også mulighet til å generere tilfeldige og sikre passord. Innholdet blir lagret på en csv fil og krypteres/dekrypteres der.

## Hovedfunksjoner
- Sikker lagring og henting av passord
- Generering av sterke tilfeldige passord
- Enkel grafisk brukergrensesnitt (GUI)
- Oversiktlig visualisering av lagrede plattformer

## Avhengigheter
Følgende pakker må installeres:
```
pip install cryptography numpy matplotlib
```

## Filstruktur
Programmet oppretter følgende filer:
- `passord.csv`: Lagrede passord (kryptert)
- `hemmelig.nøkkel`: Krypteringsnøkkel

## Bruksanvisning
1. Installer avhengigheter som beskrevet ovenfor
2. Last ned repoet i sin helhet.
3. Kjør `password_manager.py`. 
4. Første gang programmet kjøres vil det opprette en krypteringsnøkkel
5. Bruk GUI for å legge til, se og administrere passord etc.

## Sikkerhet
- Alle passord krypteres med Fernet-kryptering før lagring
- Krypteringsnøkkelen lagres separat i `hemmelig.nøkkel`
- Innholdet i CSV-filen er uleselig uten riktig dekrypteringsnøkkel

## Videre funksjoner
Fremtidige utvidelser planlagt for prosjektet:
- Bedre håndtering av krypterings nøkkel
- Legge til masterpassord for tilgang til programmet
- Legge til søtte for JSON også
- SQLite-integrasjon 
- Base64-implementering for ytterligere sikkerhetslag
- Støtte for flere språk
- Og generell kode forbedring
