# -*- coding: utf-8 -*-
"""
Apprentissage Pyromax — interface Kivy verticale.
Lancer avec : python main.py
Optionnel : placer pyromax_background.jpg dans le même dossier.
"""
from pathlib import Path
import random

from kivy.app import App
from kivy.metrics import dp, sp
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup

# Palette Pyromax : noir bleu, ivoire et or.
GOLD = (1.00, 0.73, 0.20, 1)
GOLD_LIGHT = (1.00, 0.84, 0.43, 1)
INK = (0.015, 0.035, 0.055, 1)
PANEL = (0.025, 0.065, 0.085, 0.92)
PANEL_ALT = (0.035, 0.085, 0.105, 0.96)
WHITE = (0.96, 0.96, 0.94, 1)
MUTED = (0.68, 0.73, 0.76, 1)
BG_IMAGE = Path(__file__).with_name("pyromax_background.jpg")

QUOTES = [
    ("Chaque petit pas compte, même celui que personne ne voit.", "PYRO"),
    ("La discipline construit ce que la motivation commence.", "APPRENTISSAGE PYROMAX"),
    ("N’attends pas d’être prêt : commence et apprends en chemin.", "PYRO"),
    ("Ton avenir change lorsque tes habitudes changent.", "APPRENTISSAGE PYROMAX"),
    ("Une erreur devient une leçon quand tu décides d’en tirer quelque chose.", "PYRO"),
    ("Les grandes réussites commencent souvent par une petite décision.", "PYRO"),
]

def rounded_background(widget, color=PANEL, radius=dp(18), border=True):
    """Dessine un fond arrondi lié à la taille/position du widget."""
    with widget.canvas.before:
        if border:
            Color(GOLD[0], GOLD[1], GOLD[2], 0.82)
            widget._border_shape = RoundedRectangle(
                pos=widget.pos, size=widget.size, radius=[radius]
            )
        Color(*color)
        widget._bg_shape = RoundedRectangle(
            pos=widget.pos, size=widget.size, radius=[max(0, radius - dp(1))]
        )

    def update(*_):
        if hasattr(widget, "_border_shape"):
            widget._border_shape.pos = widget.pos
            widget._border_shape.size = widget.size
        widget._bg_shape.pos = widget.pos
        widget._bg_shape.size = widget.size

    widget.bind(pos=update, size=update)


class GoldButton(Button):
    def __init__(self, gold=True, **kwargs):
        kwargs.setdefault("background_normal", "")
        kwargs.setdefault("background_down", "")
        kwargs.setdefault("background_color", (0, 0, 0, 0))
        kwargs.setdefault("color", INK if gold else WHITE)
        kwargs.setdefault("font_size", sp(14))
        kwargs.setdefault("bold", True)
        super().__init__(**kwargs)
        self.gold = gold
        with self.canvas.before:
            self._button_color = Color(*(GOLD if gold else PANEL_ALT))
            self._button_shape = RoundedRectangle(
                pos=self.pos, size=self.size, radius=[dp(16)]
            )
            if not gold:
                self._line_color = Color(GOLD[0], GOLD[1], GOLD[2], 0.72)
                self._line = Line(
                    rounded_rectangle=(self.x, self.y, self.width, self.height, dp(16)),
                    width=1.1
                )
        self.bind(pos=self._update_shape, size=self._update_shape)

    def _update_shape(self, *_):
        self._button_shape.pos = self.pos
        self._button_shape.size = self.size
        if hasattr(self, "_line"):
            self._line.rounded_rectangle = (
                self.x, self.y, self.width, self.height, dp(16)
            )


class Panel(BoxLayout):
    def __init__(self, color=PANEL, radius=dp(20), border=True, **kwargs):
        super().__init__(**kwargs)
        rounded_background(self, color=color, radius=radius, border=border)


class PyromaxApp(App):
    title = "Apprentissage Pyromax"

    def build(self):
        # Fenêtre de développement verticale. La taille peut être redimensionnée.
        Window.size = (430, 850)
        Window.minimum_width = 320
        Window.minimum_height = 560
        self.current_quote = random.choice(QUOTES)
        self.saved_quotes = []
        self.notes = []
        self.text_scale = 1.0

        self.root_area = FloatLayout()
        with self.root_area.canvas.before:
            Color(*INK)
            self.base_bg = Rectangle(pos=self.root_area.pos, size=self.root_area.size)
        self.root_area.bind(pos=self._update_base_bg, size=self._update_base_bg)

        if BG_IMAGE.exists():
            # Image plein écran en arrière-plan ; l'interface reste constituée
            # de vrais widgets Kivy placés au-dessus.
            from kivy.uix.image import Image
            self.bg_image = Image(
                source=str(BG_IMAGE), allow_stretch=True, keep_ratio=False,
                size_hint=(1, 1), pos_hint={"x": 0, "y": 0},
                opacity=0.40
            )
            self.root_area.add_widget(self.bg_image)
            with self.bg_image.canvas.before:
                Color(0.005, 0.018, 0.03, 0.60)
                self.bg_tint = Rectangle(pos=self.bg_image.pos, size=self.bg_image.size)
            self.bg_image.bind(pos=self._update_tint, size=self._update_tint)

        self.main_layout = BoxLayout(
            orientation="vertical", spacing=dp(10),
            padding=[dp(14), dp(12), dp(14), dp(10)],
            size_hint=(1, 1), pos_hint={"x": 0, "y": 0}
        )
        self.root_area.add_widget(self.main_layout)
        self.show_home()
        return self.root_area

    def _update_base_bg(self, *_):
        self.base_bg.pos = self.root_area.pos
        self.base_bg.size = self.root_area.size

    def _update_tint(self, *_):
        self.bg_tint.pos = self.bg_image.pos
        self.bg_tint.size = self.bg_image.size

    def clear_main(self):
        self.main_layout.clear_widgets()

    def make_header(self):
        header = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=dp(70),
            spacing=dp(10), padding=[dp(4), dp(2), dp(4), dp(2)]
        )
        logo = Label(
            text="🔥", font_size=sp(34), color=GOLD,
            size_hint_x=None, width=dp(48)
        )
        titles = BoxLayout(orientation="vertical", spacing=dp(0))
        titles.add_widget(Label(
            text="[b]Apprentissage[/b]", markup=True, color=WHITE,
            font_size=sp(18), halign="left", valign="middle",
            size_hint_y=None, height=dp(27), text_size=(Window.width, None)
        ))
        titles.add_widget(Label(
            text="[b]PYROMAX[/b]", markup=True, color=GOLD,
            font_size=sp(26), halign="left", valign="middle",
            size_hint_y=None, height=dp(34), text_size=(Window.width, None)
        ))
        header.add_widget(logo)
        header.add_widget(titles)
        self.main_layout.add_widget(header)
        self.main_layout.add_widget(Label(
            text="DES PENSÉES QUI ÉCLAIRENT TON CHEMIN",
            color=GOLD_LIGHT, font_size=sp(9), bold=True,
            size_hint_y=None, height=dp(20), halign="left",
            text_size=(Window.width - dp(35), None)
        ))

    def title_label(self, text, size=18, color=WHITE, height=dp(38), bold=True):
        return Label(
            text=text, color=color, font_size=sp(size), bold=bold,
            size_hint_y=None, height=height, halign="left", valign="middle",
            text_size=(Window.width - dp(42), None)
        )

    def show_home(self):
        self.clear_main()
        self.make_header()
        self.main_layout.add_widget(self.title_label("Bienvenue sur", 16, WHITE, dp(27), False))
        self.main_layout.add_widget(self.title_label("Apprentissage PYROMAX", 25, GOLD, dp(42)))
        self.main_layout.add_widget(self.title_label("PENSÉE DU JOUR", 11, GOLD_LIGHT, dp(25)))

        quote_panel = Panel(
            orientation="vertical", padding=[dp(16), dp(15), dp(16), dp(12)],
            spacing=dp(7), size_hint_y=None, height=dp(225),
            color=(0.008, 0.025, 0.04, 0.93), radius=dp(22), border=True
        )
        quote_panel.add_widget(Label(
            text="❝", color=GOLD, font_size=sp(42),
            size_hint_y=None, height=dp(42), halign="left"
        ))
        self.quote_label = Label(
            text=self.current_quote[0], color=WHITE, font_size=sp(22),
            italic=True, halign="center", valign="middle",
            text_size=(Window.width - dp(90), None)
        )
        quote_panel.add_widget(self.quote_label)
        quote_panel.add_widget(Label(
            text=f"—  {self.current_quote[1]}  —", color=GOLD_LIGHT,
            font_size=sp(11), bold=True, size_hint_y=None, height=dp(24)
        ))
        self.main_layout.add_widget(quote_panel)

        next_button = GoldButton(
            text="⟳   Découvrir une autre pensée     ›",
            size_hint_y=None, height=dp(56), font_size=sp(14)
        )
        next_button.bind(on_release=self.next_quote)
        self.main_layout.add_widget(next_button)

        self.main_layout.add_widget(self.title_label("EXPLORE TON ESPACE", 11, GOLD_LIGHT, dp(25)))
        tiles = BoxLayout(
            orientation="horizontal", spacing=dp(8),
            size_hint_y=None, height=dp(112)
        )
        tile_specs = [
            ("❝", "Citations", "Mots qui motivent", self.show_citations),
            ("▤", "Apprentissage", "Grandir chaque jour", self.show_learning),
            ("✎", "Mes notes", "Tes réflexions", self.show_notes),
        ]
        for icon, title, subtitle, action in tile_specs:
            tile = Panel(
                orientation="vertical", padding=[dp(4), dp(8), dp(4), dp(5)],
                spacing=dp(2), color=(0.01, 0.035, 0.05, 0.95),
                radius=dp(15), border=True
            )
            tile.add_widget(Label(text=icon, color=GOLD, font_size=sp(24), size_hint_y=None, height=dp(34)))
            tile.add_widget(Label(text=title, color=WHITE, font_size=sp(11), bold=True, size_hint_y=None, height=dp(25)))
            tile.add_widget(Label(text=subtitle, color=MUTED, font_size=sp(8), size_hint_y=None, height=dp(22)))
            tile.bind(on_touch_down=lambda inst, touch, fn=action: fn() if inst.collide_point(*touch.pos) else None)
            tiles.add_widget(tile)
        self.main_layout.add_widget(tiles)

        self.main_layout.add_widget(self.title_label("UN LÂCHEUR NE GAGNE JAMAIS.", 10, GOLD, dp(20)))
        self.main_layout.add_widget(self.title_label("UN GAGNANT NE LÂCHE JAMAIS.", 10, MUTED, dp(20), False))

        # Navigation inférieure : boutons réellement cliquables.
        nav = BoxLayout(
            orientation="horizontal", spacing=dp(6),
            size_hint_y=None, height=dp(55)
        )
        for icon, name, action in [
            ("⌂", "Accueil", self.show_home),
            ("❝", "Citations", self.show_citations),
            ("▤", "Leçons", self.show_learning),
            ("⚙", "Réglages", self.show_settings),
        ]:
            b = GoldButton(
                text=f"{icon}\n{name}", gold=False,
                font_size=sp(10), size_hint_x=1
            )
            b.bind(on_release=lambda _btn, fn=action: fn())
            nav.add_widget(b)
        self.main_layout.add_widget(nav)

    def next_quote(self, *_):
        options = [q for q in QUOTES if q != self.current_quote]
        self.current_quote = random.choice(options or QUOTES)
        self.show_home()

    def show_simple_page(self, heading, subtitle, back=True):
        self.clear_main()
        self.make_header()
        self.main_layout.add_widget(self.title_label(heading, 24, GOLD, dp(42)))
        self.main_layout.add_widget(self.title_label(subtitle, 12, MUTED, dp(45), False))
        if back:
            b = GoldButton(text="‹   Retour à l'accueil", size_hint_y=None, height=dp(48))
            b.bind(on_release=lambda *_: self.show_home())
            self.main_layout.add_widget(b)

    def show_citations(self, *_):
        self.show_simple_page("Citations enregistrées", "Garde ici les pensées qui t'aident à avancer.")
        scroll = ScrollView()
        content = BoxLayout(orientation="vertical", spacing=dp(8), padding=[0, dp(6)], size_hint_y=None)
        content.bind(minimum_height=content.setter("height"))
        quotes = list(dict.fromkeys(self.saved_quotes + [self.current_quote]))
        for quote, author in quotes:
            card = Panel(orientation="vertical", padding=dp(12), spacing=dp(5), size_hint_y=None, height=dp(100))
            card.add_widget(Label(text=f"« {quote} »", color=WHITE, font_size=sp(15), italic=True))
            card.add_widget(Label(text=f"— {author}", color=GOLD, font_size=sp(10), size_hint_y=None, height=dp(20)))
            content.add_widget(card)
        scroll.add_widget(content)
        self.main_layout.add_widget(scroll)
        save_btn = GoldButton(text="☆   Enregistrer la pensée du jour", size_hint_y=None, height=dp(48))
        save_btn.bind(on_release=self.save_quote)
        self.main_layout.add_widget(save_btn)

    def save_quote(self, *_):
        if self.current_quote not in self.saved_quotes:
            self.saved_quotes.append(self.current_quote)
        self.show_citations()

    def show_learning(self, *_):
        self.show_simple_page("Apprentissage", "Une leçon à la fois. Applique-la dans ta vie.")
        lessons = [
            ("01", "La constance", "Un petit effort répété finit par produire un vrai changement."),
            ("02", "La responsabilité", "Concentre-toi sur ce que tu peux décider et améliorer."),
            ("03", "L'environnement", "Choisis les influences qui t'aident à progresser."),
        ]
        for number, title, detail in lessons:
            card = Panel(orientation="vertical", padding=dp(12), spacing=dp(4), size_hint_y=None, height=dp(105))
            card.add_widget(Label(text=f"[color=#FFC738]{number}[/color]  [b]{title}[/b]", markup=True, color=WHITE, font_size=sp(16), halign="left"))
            card.add_widget(Label(text=detail, color=MUTED, font_size=sp(12), halign="left"))
            self.main_layout.add_widget(card)

    def show_notes(self, *_):
        self.show_simple_page("Mes notes", "Écris une idée ou une leçon à garder.")
        self.note_input = TextInput(
            hint_text="Écris ta note ici…", multiline=True,
            background_color=(0.02, 0.06, 0.08, 1), foreground_color=WHITE,
            hint_text_color=MUTED, cursor_color=GOLD, padding=dp(12),
            size_hint_y=None, height=dp(140)
        )
        self.main_layout.add_widget(self.note_input)
        save = GoldButton(text="＋   Ajouter cette note", size_hint_y=None, height=dp(48))
        save.bind(on_release=self.add_note)
        self.main_layout.add_widget(save)
        for note in self.notes[-4:]:
            self.main_layout.add_widget(Label(text="• " + note, color=WHITE, size_hint_y=None, height=dp(32)))

    def add_note(self, *_):
        note = self.note_input.text.strip()
        if note:
            self.notes.append(note)
        self.show_notes()

    def show_settings(self, *_):
        self.show_simple_page("Paramètres", "Personnalise ton expérience Pyromax.")
        self.main_layout.add_widget(self.title_label("Taille du texte", 15, WHITE, dp(35)))
        row = BoxLayout(orientation="horizontal", spacing=dp(10), size_hint_y=None, height=dp(48))
        smaller = GoldButton(text="A−", gold=False)
        bigger = GoldButton(text="A+", gold=False)
        smaller.bind(on_release=lambda *_: self.change_text(-1))
        bigger.bind(on_release=lambda *_: self.change_text(1))
        row.add_widget(smaller)
        row.add_widget(bigger)
        self.main_layout.add_widget(row)
        self.main_layout.add_widget(Label(
            text="Apprentissage Pyromax\nApprendre • Grandir • Réussir",
            color=GOLD_LIGHT, font_size=sp(13), halign="center"
        ))

    def change_text(self, delta):
        self.text_scale = max(0.8, min(1.3, self.text_scale + delta * 0.1))
        Popup(
            title="Taille du texte",
            content=Label(text=f"Échelle sélectionnée : {self.text_scale:.1f}×"),
            size_hint=(0.8, 0.28)
        ).open()


if __name__ == "__main__":
    PyromaxApp().run()
