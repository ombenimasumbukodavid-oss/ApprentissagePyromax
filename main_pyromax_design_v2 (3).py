import os
import random

from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen


# ============================================================
# APPRENTISSAGE PYROMAX — interface éditoriale moderne
# Palette : bleu nuit, ardoise, blanc cassé et accent menthe.
# Les fichiers de données existants sont conservés.
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FICHIER_CITATIONS = os.path.join(BASE_DIR, "citations_pyromax.txt")
FICHIER_CONFIG = os.path.join(BASE_DIR, "config_pyromax.txt")

BG = (0.035, 0.055, 0.085, 1)
SURFACE = (0.065, 0.09, 0.13, 1)
CARD = (0.085, 0.115, 0.16, 1)
CARD_LIGHT = (0.105, 0.14, 0.19, 1)
ACCENT = (0.35, 0.88, 0.72, 1)       # menthe, utilisé avec modération
ACCENT_DARK = (0.10, 0.28, 0.25, 1)
TEXT = (0.94, 0.96, 0.98, 1)
MUTED = (0.60, 0.67, 0.75, 1)
RED = (1.0, 0.42, 0.43, 1)
GREEN = (0.38, 0.86, 0.64, 1)

FONT_REGULAR = "C:/Windows/Fonts/segoeui.ttf"
FONT_BOLD = "C:/Windows/Fonts/seguisb.ttf"
if not os.path.exists(FONT_REGULAR):
    FONT_REGULAR = "Roboto"
if not os.path.exists(FONT_BOLD):
    FONT_BOLD = "Roboto"


# ----------------------- Données locales -----------------------

def initialiser_fichiers():
    if not os.path.exists(FICHIER_CITATIONS):
        citations = [
            "Un lâcheur ne gagne jamais. Un gagnant ne lâche jamais !",
            "Chaque échec est une leçon. Chaque effort est un progrès.",
            "La discipline construit ce que la motivation commence.",
            "Ne cherche pas à impressionner. Cherche à progresser.",
            "Tes actions d'aujourd'hui préparent tes réussites de demain.",
            "Les rêves deviennent réalité pour ceux qui osent agir.",
        ]
        with open(FICHIER_CITATIONS, "w", encoding="utf-8") as fichier:
            fichier.write("\n".join(citations) + "\n")
    if not os.path.exists(FICHIER_CONFIG):
        sauvegarder_taille_police(22)


def charger_citations():
    initialiser_fichiers()
    with open(FICHIER_CITATIONS, "r", encoding="utf-8") as fichier:
        return [ligne.strip() for ligne in fichier if ligne.strip()]


def sauvegarder_citation(texte):
    with open(FICHIER_CITATIONS, "a", encoding="utf-8") as fichier:
        fichier.write(texte.strip().replace("\n", " ") + "\n")


def charger_taille_police():
    initialiser_fichiers()
    try:
        with open(FICHIER_CONFIG, "r", encoding="utf-8") as fichier:
            taille = float(fichier.read().strip())
        return max(14, min(34, taille))
    except (OSError, ValueError):
        return 22.0


def sauvegarder_taille_police(taille):
    with open(FICHIER_CONFIG, "w", encoding="utf-8") as fichier:
        fichier.write(str(float(taille)))


# ----------------------- Composants graphiques -----------------

class Surface(BoxLayout):
    def __init__(self, couleur=SURFACE, rayon=18, bordure=None, **kwargs):
        super().__init__(**kwargs)
        self._couleur = couleur
        self._rayon = rayon
        self._bordure = bordure
        with self.canvas.before:
            Color(*self._couleur)
            self._forme = RoundedRectangle(
                pos=self.pos, size=self.size, radius=[dp(self._rayon)]
            )
            if self._bordure:
                Color(*self._bordure)
                self._ligne = Line(
                    rounded_rectangle=(self.x, self.y, self.width, self.height, dp(self._rayon)),
                    width=1
                )
            else:
                self._ligne = None
        self.bind(pos=self._actualiser, size=self._actualiser)

    def _actualiser(self, *_):
        self._forme.pos = self.pos
        self._forme.size = self.size
        if self._ligne:
            self._ligne.rounded_rectangle = (
                self.x, self.y, self.width, self.height, dp(self._rayon)
            )


class ActionButton(Button):
    def __init__(self, couleur=CARD_LIGHT, couleur_texte=TEXT,
                 taille=15, emphase=False, **kwargs):
        super().__init__(**kwargs)
        self._couleur = couleur
        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)
        self.color = couleur_texte
        self.font_name = FONT_BOLD if emphase else FONT_REGULAR
        self.font_size = sp(taille)
        self.bold = False
        with self.canvas.before:
            self._fill = Color(*self._couleur)
            self._shape = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(13)])
        self.bind(pos=self._sync, size=self._sync)

    def _sync(self, *_):
        self._shape.pos = self.pos
        self._shape.size = self.size

    def on_press(self):
        self._fill.rgba = tuple(max(0, c * 0.84) if i < 3 else c
                                for i, c in enumerate(self._couleur))

    def on_release(self):
        self._fill.rgba = self._couleur


def txt(texte, taille=14, couleur=TEXT, **kwargs):
    return Label(
        text=texte, font_name=kwargs.pop("font_name", FONT_REGULAR),
        font_size=sp(taille), color=couleur,
        halign=kwargs.pop("halign", "left"),
        valign=kwargs.pop("valign", "middle"),
        **kwargs
    )


def eyebrow(texte):
    return txt(texte.upper(), 10, ACCENT, font_name=FONT_BOLD,
               size_hint_y=None, height=dp(23))


def configure_label(instance, *_):
    instance.text_size = (max(dp(20), instance.width - dp(8)),
                          max(dp(20), instance.height - dp(8)))


def add_header(page, rubrique, titre, sous_titre=None):
    top = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(45), spacing=dp(10))
    logo = Surface(couleur=ACCENT_DARK, rayon=13, size_hint=(None, None),
                   size=(dp(43), dp(43)), padding=0)
    logo.add_widget(txt("P.", 19, ACCENT, font_name=FONT_BOLD, halign="center"))
    top.add_widget(logo)
    labels = BoxLayout(orientation="vertical", spacing=0)
    labels.add_widget(txt("APPRENTISSAGE PYROMAX", 11, MUTED, font_name=FONT_BOLD))
    labels.add_widget(txt(rubrique, 10, ACCENT, font_name=FONT_BOLD))
    top.add_widget(labels)
    page.add_widget(top)
    page.add_widget(txt(titre, 27, TEXT, font_name=FONT_BOLD,
                        size_hint_y=None, height=dp(43)))
    if sous_titre:
        page.add_widget(txt(sous_titre, 13, MUTED,
                            size_hint_y=None, height=dp(28)))


# ----------------------- Accueil -------------------------------

class EcranPrincipal(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.derniere_citation = None
        page = Surface(couleur=BG, rayon=0, orientation="vertical",
                       padding=[dp(22), dp(19), dp(22), dp(12)], spacing=dp(12))
        add_header(page, "TON ESPACE DE PROGRESSION", "Une idée peut tout changer.",
                   "Quelques mots. Une réflexion. Un pas en avant.")

        # Carte de citation : alignement à gauche, numéro et accent latéral.
        self.carte_citation = Surface(
            orientation="vertical", couleur=CARD, rayon=22,
            padding=[dp(20), dp(17), dp(18), dp(17)], spacing=dp(8),
            size_hint_y=1, bordure=(0.16, 0.22, 0.27, 1)
        )
        ligne = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(27), spacing=dp(8))
        ligne.add_widget(txt("✦  PENSÉE DU JOUR", 10, ACCENT, font_name=FONT_BOLD))
        ligne.add_widget(txt("•  PRENDS UN INSTANT", 9, MUTED, halign="right"))
        self.carte_citation.add_widget(ligne)
        self.carte_citation.add_widget(Surface(couleur=ACCENT, rayon=3,
                                               size_hint=(None, None), size=(dp(35), dp(4))))
        self.citation_label = txt("", 23, TEXT, font_name=FONT_BOLD, valign="top")
        self.citation_label.bind(size=configure_label)
        self.carte_citation.add_widget(self.citation_label)
        bas = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(28), spacing=dp(8))
        bas.add_widget(txt("PYROMAX  /  GRANDIR AU QUOTIDIEN", 9, MUTED, font_name=FONT_BOLD))
        bas.add_widget(txt("↗", 16, ACCENT, halign="right", font_name=FONT_BOLD))
        self.carte_citation.add_widget(bas)
        page.add_widget(self.carte_citation)

        bouton_suivant = ActionButton(
            text="↻    Découvrir une autre pensée",
            couleur=ACCENT, couleur_texte=BG, taille=15, emphase=True,
            size_hint_y=None, height=dp(52)
        )
        bouton_suivant.bind(on_release=self.changer_citation)
        page.add_widget(bouton_suivant)

        page.add_widget(eyebrow("TON ESPACE PERSONNEL"))
        actions = BoxLayout(orientation="horizontal", spacing=dp(10),
                            size_hint_y=None, height=dp(106))
        gestion = Surface(orientation="vertical", couleur=SURFACE, rayon=16,
                          padding=[dp(13), dp(12)], spacing=dp(4),
                          bordure=(0.15, 0.20, 0.26, 1))
        gestion.add_widget(txt("▤", 24, ACCENT, font_name=FONT_BOLD))
        gestion.add_widget(txt("Mes citations", 14, TEXT, font_name=FONT_BOLD))
        gestion.add_widget(txt("Ta collection  →", 11, MUTED))
        gestion.bind(on_touch_up=lambda instance, touch: self.aller_gestion()
                     if instance.collide_point(*touch.pos) else None)
        actions.add_widget(gestion)

        param = Surface(orientation="vertical", couleur=SURFACE, rayon=16,
                        padding=[dp(13), dp(12)], spacing=dp(4),
                        bordure=(0.15, 0.20, 0.26, 1))
        param.add_widget(txt("⚙", 24, ACCENT, font_name=FONT_BOLD))
        param.add_widget(txt("Affichage", 14, TEXT, font_name=FONT_BOLD))
        param.add_widget(txt("Adapter le texte  →", 11, MUTED))
        param.bind(on_touch_up=lambda instance, touch: self.aller_parametres()
                   if instance.collide_point(*touch.pos) else None)
        actions.add_widget(param)
        page.add_widget(actions)

        footer = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(30))
        footer.add_widget(txt("DISCIPLINE  •  CONSCIENCE  •  ACTION", 9, MUTED, font_name=FONT_BOLD))
        footer.add_widget(txt("●", 9, ACCENT, halign="right"))
        page.add_widget(footer)
        self.add_widget(page)
        self.changer_citation(None)

    def on_enter(self, *_):
        self.citation_label.font_size = sp(charger_taille_police())

    def changer_citation(self, *_):
        citations = charger_citations()
        if not citations:
            self.citation_label.text = "Ajoute une première pensée dans ta collection."
            return
        choix = [c for c in citations if c != self.derniere_citation]
        if not choix:
            choix = citations
        self.derniere_citation = random.choice(choix)
        self.citation_label.text = self.derniere_citation

    def aller_gestion(self, *_):
        self.manager.current = "gestion"

    def aller_parametres(self, *_):
        self.manager.current = "parametres"


# ----------------------- Gestion des citations -----------------

class EcranGestion(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        page = Surface(couleur=BG, rayon=0, orientation="vertical",
                       padding=[dp(20), dp(18), dp(20), dp(12)], spacing=dp(10))
        add_header(page, "COLLECTION PERSONNELLE", "Mes citations",
                   "Garde les idées qui méritent de rester.")
        compose = Surface(orientation="vertical", couleur=CARD, rayon=18,
                          padding=dp(14), spacing=dp(10),
                          size_hint_y=None, height=dp(188),
                          bordure=(0.16, 0.22, 0.27, 1))
        compose.add_widget(eyebrow("AJOUTER UNE PENSÉE"))
        self.saisie = TextInput(
            hint_text="Écris ou colle ta citation ici…", multiline=True,
            size_hint_y=1, font_name=FONT_REGULAR, font_size=sp(15),
            padding=[dp(12), dp(10)], background_normal="", background_active="",
            background_color=SURFACE, foreground_color=TEXT, hint_text_color=MUTED,
            cursor_color=ACCENT, selection_color=(0.35, 0.88, 0.72, 0.3)
        )
        compose.add_widget(self.saisie)
        ajouter = ActionButton(text="＋  Enregistrer la citation",
                               couleur=ACCENT, couleur_texte=BG, taille=14,
                               emphase=True, size_hint_y=None, height=dp(43))
        ajouter.bind(on_release=self.ajouter_citation)
        compose.add_widget(ajouter)
        page.add_widget(compose)
        self.message = txt("", 12, GREEN, size_hint_y=None, height=dp(24))
        page.add_widget(self.message)
        page.add_widget(eyebrow("TA COLLECTION"))
        self.liste = Label(text="", color=TEXT, font_name=FONT_REGULAR,
                           font_size=sp(14), halign="left", valign="top",
                           size_hint_y=None, markup=True)
        self.liste.bind(width=self._adapter_liste, texture_size=self._taille_liste)
        scroll = ScrollView(do_scroll_x=False, bar_width=dp(3), scroll_type=["bars", "content"])
        scroll.add_widget(self.liste)
        page.add_widget(scroll)
        retour = ActionButton(text="←   Retour à l’accueil", couleur=SURFACE,
                              couleur_texte=TEXT, size_hint_y=None, height=dp(46))
        retour.bind(on_release=self.retour_accueil)
        page.add_widget(retour)
        self.add_widget(page)

    def _adapter_liste(self, instance, *_):
        instance.text_size = (max(dp(20), instance.width - dp(12)), None)

    def _taille_liste(self, instance, *_):
        instance.height = max(dp(35), instance.texture_size[1] + dp(18))

    def on_enter(self, *_):
        self.rafraichir_liste()
        self.message.text = ""

    def rafraichir_liste(self):
        citations = charger_citations()
        if citations:
            self.liste.text = "\n\n".join(
                f"[color=#59E0B8]▌[/color]  {c}" for c in citations
            )
        else:
            self.liste.text = "Aucune citation pour le moment."

    def ajouter_citation(self, *_):
        texte = self.saisie.text.strip()
        if not texte:
            self.message.color = RED
            self.message.text = "Écris une citation avant de l’enregistrer."
            return
        sauvegarder_citation(texte)
        self.saisie.text = ""
        self.message.color = GREEN
        self.message.text = "✓  Citation enregistrée."
        self.rafraichir_liste()

    def retour_accueil(self, *_):
        self.manager.current = "accueil"


# ----------------------- Paramètres ----------------------------

class EcranParametres(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        page = Surface(couleur=BG, rayon=0, orientation="vertical",
                       padding=[dp(22), dp(19), dp(22), dp(14)], spacing=dp(12))
        add_header(page, "CONFORT DE LECTURE", "Personnalisation",
                   "Un affichage adapté à ta façon de lire.")
        page.add_widget(eyebrow("APERÇU"))
        self.apercu = Surface(orientation="vertical", couleur=CARD, rayon=20,
                              padding=dp(20), spacing=dp(8), size_hint_y=None,
                              height=dp(205), bordure=(0.16, 0.22, 0.27, 1))
        self.apercu.add_widget(txt("✦  UNE PENSÉE À RETENIR", 10, ACCENT,
                                   font_name=FONT_BOLD, size_hint_y=None, height=dp(24)))
        self.apercu_label = txt("« La discipline construit\nce que la motivation commence. »",
                                charger_taille_police(), TEXT, font_name=FONT_BOLD,
                                valign="middle")
        self.apercu_label.bind(size=configure_label)
        self.apercu.add_widget(self.apercu_label)
        page.add_widget(self.apercu)

        self.info = txt("", 14, ACCENT, font_name=FONT_BOLD,
                        size_hint_y=None, height=dp(32))
        page.add_widget(self.info)
        row = BoxLayout(orientation="horizontal", spacing=dp(10),
                        size_hint_y=None, height=dp(50))
        moins = ActionButton(text="−   Réduire", couleur=SURFACE, couleur_texte=TEXT,
                             size_hint_x=1, taille=14, emphase=True)
        moins.bind(on_release=self.reduire)
        plus = ActionButton(text="＋   Agrandir", couleur=ACCENT, couleur_texte=BG,
                            size_hint_x=1, taille=14, emphase=True)
        plus.bind(on_release=self.agrandir)
        row.add_widget(moins)
        row.add_widget(plus)
        page.add_widget(row)
        note = Surface(couleur=SURFACE, rayon=14, padding=dp(13),
                       size_hint_y=None, height=dp(72))
        note.add_widget(txt("✓  Ton choix est sauvegardé automatiquement et sera conservé au prochain lancement.",
                            12, MUTED, valign="middle"))
        page.add_widget(note)
        page.add_widget(WidgetSpacer())
        retour = ActionButton(text="←   Retour à l’accueil", couleur=SURFACE,
                              couleur_texte=TEXT, size_hint_y=None, height=dp(46))
        retour.bind(on_release=self.retour_accueil)
        page.add_widget(retour)
        self.add_widget(page)
        self.actualiser()

    def actualiser(self):
        taille = charger_taille_police()
        self.info.text = f"Taille du texte  ·  {int(taille)}"
        self.apercu_label.font_size = sp(taille)

    def on_enter(self, *_):
        self.actualiser()

    def agrandir(self, *_):
        sauvegarder_taille_police(min(34, charger_taille_police() + 2))
        self.actualiser()

    def reduire(self, *_):
        sauvegarder_taille_police(max(14, charger_taille_police() - 2))
        self.actualiser()

    def retour_accueil(self, *_):
        self.manager.current = "accueil"


class WidgetSpacer(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(size_hint_y=1, **kwargs)


# ----------------------- Application ---------------------------

class PyromaxApp(App):
    title = "Apprentissage Pyromax"

    def build(self):
        Window.clearcolor = BG
        Window.minimum_width = 340
        Window.minimum_height = 600
        initialiser_fichiers()
        gestionnaire = ScreenManager()
        gestionnaire.add_widget(EcranPrincipal(name="accueil"))
        gestionnaire.add_widget(EcranGestion(name="gestion"))
        gestionnaire.add_widget(EcranParametres(name="parametres"))
        return gestionnaire


if __name__ == "__main__":
    PyromaxApp().run()
