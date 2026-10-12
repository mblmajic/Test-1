"""Lecture et classement des superficies de bureaux.

Règle de bloc (paramétrable) : superficie intérieure >= borne_min et < borne_max_exclue.
Exemple bloc « 220 à 229 m² » : borne_min=220, borne_max_exclue=230
(220 et 229,5 inclus ; 230 exclu).

Le module ne devine jamais une superficie intérieure : quand le texte mélange
surface totale, terrasse, plage de surfaces ou plusieurs lots, il renvoie
« À vérifier » avec la raison.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field, asdict

ELIGIBLE = "Compatible"
A_VERIFIER = "À vérifier"
EXCLU = "Exclu"

_NUM = r"(\d{1,3}(?:[   .]\d{3})+|\d+)(?:[.,](\d+))?"
_M2 = r"\s*(?:m²|m2|m\b|mètres? carrés?|metres? carres?|mq)"

RE_SURFACE = re.compile(_NUM + _M2, re.I)
RE_RANGE = re.compile(
    r"(?:de|entre)?\s*" + _NUM + r"\s*(?:m²|m2|m)?\s*(?:à|a|-|–|et|jusqu'?à)\s*" + _NUM + _M2,
    re.I,
)
RE_PARTIR = re.compile(r"(?:à partir de|a partir de|des|dès)\s*" + _NUM + _M2, re.I)

MOTS_INTERIEUR = ("habitable", "interieure", "intérieure", "utile", "couverte", "plancher", "bureau de", "plateau de")
MOTS_ANNEXE = {
    "terrasse": "terrasse",
    "balcon": "balcon",
    "jardin": "jardin",
    "terrain": "terrain",
    "parking": "parking",
    "sous-sol": "sous-sol",
    "mezzanine": "mezzanine",
    "parties communes": "parties communes",
}
MOTS_TOTAL = ("totale", "total", "globale", "hors oeuvre", "hors œuvre", "dont")
MOTS_HORS_BUREAU = {
    "coworking": "coworking / espace partagé",
    "co-working": "coworking / espace partagé",
    "domiciliation": "domiciliation",
    "cession de bail": "cession de bail / droit au bail",
    "droit au bail": "cession de bail / droit au bail",
    "pas de porte": "pas de porte",
    "fonds de commerce": "fonds de commerce",
    "local commercial": "local commercial (usage bureau à confirmer)",
    "magasin": "magasin",
    "entrepot": "entrepôt",
    "entrepôt": "entrepôt",
    "hangar": "hangar",
    "immeuble": "immeuble entier",
    "villa": "villa (usage bureau à confirmer)",
    "terrain": "terrain",
}
MOTS_PLUSIEURS_LOTS = ("plateaux", "lots", "plusieurs bureaux", "divisible", "modulable", "étages", "etages")


def _norm(texte: str) -> str:
    texte = unicodedata.normalize("NFKC", texte or "")
    return re.sub(r"\s+", " ", texte).strip()


def _val(entier: str, dec: str | None) -> float:
    entier = re.sub(r"[   .]", "", entier)
    return float(f"{entier}.{dec}") if dec else float(entier)


@dataclass
class Mesure:
    valeur: float
    extrait: str
    position: int
    qualificatif: str = ""  # interieure | totale | annexe:<type> | inconnue


@dataclass
class Classement:
    statut: str
    superficie_interieure: float | None
    nature: str
    raisons: list[str] = field(default_factory=list)
    mesures: list[dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def extraire_mesures(texte: str) -> list[Mesure]:
    texte = _norm(texte)
    mesures: list[Mesure] = []
    for m in RE_SURFACE.finditer(texte):
        v = _val(m.group(1), m.group(2))
        if v < 5 or v > 100000:
            continue
        avant = texte[max(0, m.start() - 40): m.start()].lower()
        apres = texte[m.end(): m.end() + 25].lower()
        proche = avant[-30:]
        qual = "inconnue"
        annexe_avant = next((typ for mot, typ in MOTS_ANNEXE.items() if mot in avant[-20:]), None)
        if any(w in proche for w in MOTS_INTERIEUR) and not annexe_avant:
            qual = "interieure"
        elif annexe_avant:
            qual = f"annexe:{annexe_avant}"
        elif re.match(r"\s*(?:\)|,)?\s*(?:dont|y compris|incluant|terrasse (?:comprise|incluse))", apres):
            qual = "totale"
        elif any(w in proche for w in MOTS_TOTAL):
            qual = "totale"
        extrait = texte[max(0, m.start() - 40): m.end() + 25]
        mesures.append(Mesure(v, extrait, m.start(), qual))
    return mesures


def classer(
    titre: str,
    description: str = "",
    surface_structuree: float | None = None,
    *,
    borne_min: float,
    borne_max_exclue: float,
    transaction_attendue: str | None = None,
    transaction_observee: str | None = None,
) -> Classement:
    """Classe une annonce pour un bloc [borne_min, borne_max_exclue[."""
    texte = _norm(f"{titre} . {description}")
    bas = texte.lower()
    raisons: list[str] = []
    mesures = extraire_mesures(texte)
    mdicts = [asdict(m) for m in mesures]

    # Usage
    usages = sorted({lib for mot, lib in MOTS_HORS_BUREAU.items() if mot in bas})
    bureau = any(w in bas for w in ("bureau", "plateau", "open space", "open-space", "cabinet"))
    if not bureau:
        raisons.append("usage bureau non mentionné")
    if usages:
        raisons.append("usage à confirmer : " + ", ".join(usages))

    if transaction_attendue and transaction_observee and transaction_attendue != transaction_observee:
        return Classement(EXCLU, None, "transaction différente", [f"transaction observée {transaction_observee}"], mdicts)

    # Plages et lots multiples
    plage = RE_RANGE.search(texte) or RE_PARTIR.search(texte)
    if plage:
        raisons.append(f"plage de superficies : « {plage.group(0).strip()} »")
    if any(w in bas for w in MOTS_PLUSIEURS_LOTS):
        raisons.append("plusieurs lots ou surface modulable possibles")

    annexes = [m for m in mesures if m.qualificatif.startswith("annexe:")]
    interieures = [m for m in mesures if m.qualificatif == "interieure"]
    totales = [m for m in mesures if m.qualificatif == "totale"]
    inconnues = [m for m in mesures if m.qualificatif == "inconnue"]

    candidate: float | None = None
    nature = "non déterminée"
    if interieures:
        valeurs = sorted({m.valeur for m in interieures})
        candidate = valeurs[0] if len(valeurs) == 1 else None
        nature = "intérieure (libellé explicite)"
        if len(valeurs) > 1:
            raisons.append(f"plusieurs surfaces intérieures : {valeurs}")
    elif surface_structuree is not None and not annexes and not totales:
        candidate = float(surface_structuree)
        nature = "champ structuré de la source (intérieure présumée, sans annexe mentionnée)"
    else:
        valeurs = sorted({m.valeur for m in inconnues + ([] if surface_structuree is None else [Mesure(float(surface_structuree), "champ structuré", -1)])})
        if len(valeurs) == 1:
            candidate = valeurs[0]
            nature = "surface annoncée (seule valeur, sans libellé)"
        elif len(valeurs) > 1:
            raisons.append(f"plusieurs surfaces sans libellé : {valeurs}")
    if annexes:
        raisons.append("annexe mentionnée : " + ", ".join(f"{m.qualificatif[7:]} {m.valeur:g} m²" for m in annexes))
        if not interieures:
            nature = "surface annoncée pouvant inclure une annexe"
    if totales and not interieures:
        raisons.append("surface qualifiée de totale/globale : " + ", ".join(f"{m.valeur:g}" for m in totales))
        candidate = candidate if candidate is not None else (totales[0].valeur if len(totales) == 1 else None)
        nature = "surface totale (intérieure non isolée)"

    if candidate is None:
        if not mesures and surface_structuree is None:
            raisons.append("aucune superficie lisible")
        return Classement(A_VERIFIER, None, nature, raisons, mdicts)

    dans_bloc = borne_min <= candidate < borne_max_exclue
    # Une surface totale hors bloc peut cacher un intérieur dans le bloc (et inversement) :
    # seule une surface intérieure hors bloc permet d'exclure.
    if not dans_bloc:
        if annexes and candidate >= borne_max_exclue:
            raisons.append(f"surface annoncée {candidate:g} m² hors bloc mais annexe à déduire")
            return Classement(A_VERIFIER, None, nature, raisons, mdicts)
        if plage and plage_couvre(plage, borne_min, borne_max_exclue):
            return Classement(A_VERIFIER, None, nature, raisons, mdicts)
        return Classement(EXCLU, candidate, nature, raisons + [f"{candidate:g} m² hors bloc [{borne_min:g};{borne_max_exclue:g}["], mdicts)

    if raisons:
        return Classement(A_VERIFIER, candidate, nature, raisons, mdicts)
    return Classement(ELIGIBLE, candidate, nature, [], mdicts)


def plage_couvre(m: re.Match, borne_min: float, borne_max_exclue: float) -> bool:
    nums = [g for g in m.groups() if g is not None]
    try:
        bas = _val(nums[0], None)
        haut = _val(nums[2], None) if len(nums) >= 3 and m.re is RE_RANGE else float("inf")
    except (ValueError, IndexError):
        return True
    return bas < borne_max_exclue and haut >= borne_min


def prefiltre_carte(texte: str, borne_min: float, borne_max_exclue: float, marge: float = 0.0) -> bool:
    """Vrai si une carte de liste mérite l'ouverture de la fiche (une surface dans le bloc,
    éventuellement élargi d'une marge pour les annexes, ou aucune surface lisible)."""
    mesures = extraire_mesures(texte)
    if not mesures:
        return True
    return any(borne_min - 0.0 <= m.valeur < borne_max_exclue + marge for m in mesures)
