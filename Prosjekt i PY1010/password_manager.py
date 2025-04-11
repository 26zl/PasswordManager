"""
Passordbehandler
----------------

Eier: Laurent Zogaj
Dato levert: 11. april 2025

Beskrivelse:
Dette prosjektet er en passordbehandler som gjør det mulig for brukeren å lagre, hente og administrere passord på en sikker måte lokalt på datamaskinen. 
Passordene krypteres ved hjelp av biblioteket cryptography med symmetrisk kryptering (Fernet). 
Programmet gir også mulighet til å generere tilfeldige og sikre passord.

Avhengigheter:
- tkinter (for GUI)
- cryptography (for kryptering/dekryptering)
- numpy (vektorisert plotting)
- matplotlib (plotting av data)
- secrets (for sikker passordgenerering)
- string (for tegnsett)
- csv (for lagring av passord i CSV-format)
- datetime (for tidsstempling av passord)
- os (for filhåndtering)
- sys (for systemfunksjoner)

Filstruktur:
Disse vil bli opprettet i det du starter applikasjonen og lagrer passord
- passord.csv: lagret passorddata
- hemmelig.nøkkel: krypteringsnøkkel

Viktig:
Dette er en kun en prototype-applikasjon.
"""

# Imports
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
import numpy as np
import secrets
import string
import os
import sys
import csv
import datetime
from cryptography.fernet import Fernet

# --- Konstanter ---
LAGRE_FIL = "passord.csv"  # Selve filen som lagrer passordene
NØKKEL_FIL = "hemmelig.nøkkel"  # Filen som inneholder krypteringsnøkkelen

# --- Globale variabler ---
lagrede_passord = {}  # Lager en tom dictionary for å lagre passordene
nøkkel = None  # Holder krypteringsnøkkelen


# --- Kryptering ---
# Her henter vi eller lager nøkkelen
def hent_lage_nøkkel():
    if os.path.exists(NØKKEL_FIL):
        with open(NØKKEL_FIL, "rb") as f:
            return f.read()
    ny_nøkkel = Fernet.generate_key()
    with open(NØKKEL_FIL, "wb") as f:
        f.write(ny_nøkkel)
    return ny_nøkkel

# Her krypterer vi passordet
def krypter_passord(passord):
    try:
        f = Fernet(nøkkel)
        if not isinstance(passord, str):
            passord = str(passord)
        return f.encrypt(passord.encode("utf-8"))
    except Exception as error:
        messagebox.showerror("Feil", f"Kunne ikke kryptere passord: {error}")
        return None
    
# Her dekrypterer vi passordet
def dekrypter_passord(kryptert):
    try:
        f = Fernet(nøkkel)
        if isinstance(kryptert, str):
            kryptert = kryptert.encode("utf-8")
        return f.decrypt(kryptert).decode("utf-8")
    except Exception as error:
        messagebox.showerror("Feil", f"Kunne ikke dekryptere passord: {error}")
        return None


# --- Passord Generering ---
# Generering av passord med secrets istedenfor random. Fordelen er at det gir sikrere genererte passord
def generer_passord():
    lengde = secrets.randbelow(18) + 8
    tegn = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(tegn) for _ in range(lengde))

# --- Lagring og Henting ---
# Lagrer passordene i en CSV-fil
def lagre_passord(data):
    try:
        if not os.path.exists(NØKKEL_FIL):
            messagebox.showerror("Feil", "Nøkkelfil mangler.")
            return False
        
        with open(LAGRE_FIL, "w", newline='', encoding='utf-8') as f:
            felt = ["platform", "brukernavn", "kryptert_passord", "dato"]
            writer = csv.DictWriter(f, fieldnames=felt)
            writer.writeheader()

            for platform, info in data.items(): 
                if not isinstance(info, dict):
                    continue
                
                passord_data = info.get("passord", b"")
                if isinstance(passord_data, bytes):
                    kryptert_passord = passord_data.decode("utf-8", errors="replace")
                else:
                    kryptert_passord = str(passord_data)
                
                dato = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if isinstance(info, dict) and "dato" in info:
                    dato = info["dato"]
                
                rad = {
                    "platform": platform,
                    "brukernavn": info.get("brukernavn", ""),
                    "kryptert_passord": kryptert_passord,
                    "dato": dato
                }
                writer.writerow(rad)
        return True
    except Exception as error:
        messagebox.showerror("Lagringsfeil", f"Kunne ikke lagre: {error}")
        return False
    
# Her henter vi passordene fra CSV-filen
def hent_passord():
    passord_data = {}
    if not os.path.exists(LAGRE_FIL):
        return passord_data
    try:
        with open(LAGRE_FIL, "r", encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for rad in reader:
                if "platform" not in rad or "kryptert_passord" not in rad:
                    continue
                    
                kryptert = rad["kryptert_passord"]
                if not isinstance(kryptert, bytes):
                    try:
                        kryptert = kryptert.encode("utf-8")
                    except:
                        continue
                        
                passord_data[rad["platform"]] = {
                    "brukernavn": rad.get("brukernavn", ""),
                    "passord": kryptert,
                    "dato": rad.get("dato", "")
                }
        return passord_data
    except Exception as error:
        messagebox.showerror("Feil", f"Kunne ikke lese fil: {error}")
        return {}

# --- GUI-funksjoner ---
# Legger til passord i dictionary og lagrer det i CSV-filen
def legg_til_felt():
    platform = platform_entry.get().strip()
    bruker = brukernavn_entry.get().strip()
    passord = passord_entry.get().strip()

    if not all([platform, bruker, passord]):
        messagebox.showwarning("Feil", "Alle feltene må fylles ut.")
        return
    if len(passord) < 8 or len(passord) > 25:
        messagebox.showerror("Feil", "Passordet må være mellom 8 og 25 tegn langt.")
        return
        
    kryptert = krypter_passord(passord)
    if not kryptert:
        return
        
    lagrede_passord[platform] = {
        "brukernavn": bruker,
        "passord": kryptert,
        "dato": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    if lagre_passord(lagrede_passord):
        messagebox.showinfo("Lagring", "Passord lagret.")
        clear_felt()
    else:
        messagebox.showerror("Feil", "Kunne ikke lagre passord.")

# Henter passord fra dictionary og dekrypterer det
def hent_felt():
    platform = platform_entry.get().strip()
    data = None
    
    if platform in lagrede_passord:
        data = lagrede_passord[platform]
    else:
        for navn, info in lagrede_passord.items():
            if isinstance(navn, str) and isinstance(platform, str):
                if navn.lower() == platform.lower():
                    platform = navn
                    data = info
                    break
    
    if not data:
        messagebox.showwarning("Feil", "Ingen data funnet.")
        return
    
    passord = dekrypter_passord(data["passord"])
    if passord:
        messagebox.showinfo("Passord", f"Platform: {platform}\nBruker: {data['brukernavn']}\nPassord: {passord}")
        platform_entry.delete(0, tk.END)
        platform_entry.insert(0, platform)

# Viser diagram over platformer og antallet av dem
def plot_lengths():
    if not lagrede_passord:
        messagebox.showwarning("Tomt", "Ingen plattformer å vise.")
        return
        
    plattformer = list(lagrede_passord.keys())
    plt.figure(figsize=(8, 6))
    plt.pie([1] * len(plattformer), labels=plattformer, autopct='%1.1f%%')
    plt.title(f"Oversikt over {len(plattformer)} plattformer")
    plt.tight_layout()
    plt.show()

# Genererer et tilfeldig passord og fyller det inn i passordfeltet
def generer_og_fyll():
    passord_entry.delete(0, tk.END)
    passord_entry.insert(0, generer_passord())

# Clearer inputfeltene
def clear_felt():
    platform_entry.delete(0, tk.END)
    brukernavn_entry.delete(0, tk.END)
    passord_entry.delete(0, tk.END)

# Nød funksjon for å slette alt
def slett_alt():
    if messagebox.askyesno("Bekreft sletting", "Er du sikker på at du vil slette alle data?"):
        if not os.path.exists(LAGRE_FIL) and not os.path.exists(NØKKEL_FIL):
            messagebox.showerror("Feil", "Ingen data funnet å slette.")
            return
            
        lagrede_passord.clear()
        
        if os.path.exists(LAGRE_FIL):
            os.remove(LAGRE_FIL)
        if os.path.exists(NØKKEL_FIL):
            os.remove(NØKKEL_FIL)
            
        messagebox.showinfo("Slettet", "Alle data er fjernet.")
        sys.exit(0) 

# Informasjon om passordbehandleren og hvordan man bruker den
def vis_info():
    info_vindu = tk.Toplevel(window)
    info_vindu.title("Informasjon om Passordbehandleren")
    info_vindu.geometry("500x400")
    
    # Scrollbar
    tekst = scrolledtext.ScrolledText(info_vindu, wrap=tk.WORD)
    tekst.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Sentrer teksten 
    tekst.tag_configure("center", justify='center')

    # Informasjonstekst
    informasjon_text = """
    PASSORDBEHANDLER - BRUKSANVISNING
    ================================
    
    Denne passordbehandleren hjelper deg med å lagre og håndtere dine passord på en sikker måte.
    
    FUNKSJONER:
    -----------
    
    1. LAGRE PASSORD
       Fyll inn platform (f.eks. Facebook, Gmail), brukernavn og passord, 
       og trykk på "Lagre" for å lagre informasjonen 'sikkert'.
    
    2. HENTE PASSORD
       Skriv inn platformnavn og trykk "Hent" for å vise brukernavn og passord.
    
    3. GENERERE PASSORD
       Trykk på "Generer" for å lage et tilfeldig, sterkt passord.
    
    4. VISUALISERE PLATFORMER BRUKT
       Trykk på "Vis Platform" for å se en graf over platformer
    
    5. "NØDKNAPP!!" SLETTE ALL DATA
       Trykk på "Slett Alt" for å fjerne alle lagrede passord.
    
    SIKKERHET:
    ----------
    
    - Alle passord lagres kryptert på din datamaskin
    - Bruk et sterkt, unikt passord for hver platform
    - Regelmessig oppdater viktige passord for økt sikkerhet

    -NB!: Passordbehandleren er på ingen måte klar og mangler viktig funksjonalitet, dette er bare en basic versjon.
    -Vennligst vær forsiktig med å bruke denne i produksjon, da det er en demo og ikke er ment for reell bruk.
    """
    
    # Setter inn teksten
    tekst.insert(tk.END, informasjon_text, "center")
    tekst.config(state=tk.DISABLED)
    
    ttk.Button(info_vindu, text="Lukk", command=info_vindu.destroy).pack(pady=10)

# --- Hovedprogram / GUI ---
nøkkel = hent_lage_nøkkel()  # Initialiser nøkkel
lagrede_passord = hent_passord()  # Laster inn eksisterende passord

window = tk.Tk()
window.title("Passordbehandler")

style = ttk.Style()
style.theme_use("clam")

# Ramme
main_frame = ttk.Frame(window, padding=10)
main_frame.pack(fill=tk.BOTH, expand=True)

# Infoknapp oppe
ttk.Button(main_frame, text="Informasjon", command=vis_info).pack(pady=(0, 10))

# Inputfelt ramme
input_frame = ttk.LabelFrame(main_frame, padding=10)
input_frame.pack(fill=tk.X)

# Feltene for input
felt_frame = ttk.Frame(input_frame)
felt_frame.pack(fill=tk.X)

ttk.Label(felt_frame, text="Platform:").grid(row=0, column=0, sticky="E", padx=5, pady=5)
platform_entry = ttk.Entry(felt_frame, width=30)
platform_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(felt_frame, text="Brukernavn:").grid(row=1, column=0, sticky="E", padx=5, pady=5)
brukernavn_entry = ttk.Entry(felt_frame, width=30)
brukernavn_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(felt_frame, text="Passord:").grid(row=2, column=0, sticky="E", padx=5, pady=5)
passord_entry = ttk.Entry(felt_frame, width=30, show="*")
passord_entry.grid(row=2, column=1, padx=5, pady=5)
ttk.Button(felt_frame, text="Generer", command=generer_og_fyll).grid(row=2, column=2, padx=5)

# Knapperad
knapp_frame = ttk.Frame(input_frame)
knapp_frame.pack(fill=tk.X, pady=10)

# Ulike knapper
ttk.Button(knapp_frame, text="Hent", command=hent_felt).pack(side=tk.LEFT, expand=True, padx=5)
ttk.Button(knapp_frame, text="Lagre", command=legg_til_felt).pack(side=tk.LEFT, expand=True, padx=5)
ttk.Button(knapp_frame, text="Vis platformer", command=plot_lengths).pack(side=tk.LEFT, expand=True, padx=5)

# Knapper nede
bunn_frame = ttk.Frame(main_frame)
bunn_frame.pack(fill=tk.X, pady=10)
ttk.Button(bunn_frame, text="Slett Alt", command=slett_alt).pack()

window.mainloop()