# -*- coding: utf-8 -*-
#  prefs.py: -*- Python -*-  DESCRIPTIVE TEXT.

from PyQt5.QtCore import pyqtSignal, QSettings
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QFontDialog


from . prefsBA import Ui_PrefsBA
from . import help
from . windowutils import WindowUtils


class Preferences(WindowUtils,QDialog, Ui_PrefsBA):

    prefsSaved = pyqtSignal()

    def __init__(self, parent, autoload=0):
        super(Preferences,self).__init__()
        self.parent = parent
        self.setupUi(self)

        #PrefsBA.__init__(self, parent)

        self.settings = QSettings()

        if autoload:
            self.load()

    def load(self):
        for preference in self.settings.childKeys():
            try:
                setting = self.settings.value(preference)
                if preference == 'Font':
                    self.parent.setfont(setting.toPyObject())
                if preference == 'Match Font':
                    self.parent.setMatchFont(setting.toPyObject())
                if preference == 'Email Server':
                    self.emailServerEdit.setText(setting.toPyObject())
                if preference == 'Recent Files Count':
                    self.recentFilesSpinBox.setValue(int(setting.toPyObject()))
            except Exception as e:
                print("Loading of configuration key", preference, "failed.")
                self.settings.remove(preference)


    def save(self):
        self.settings.setValue('Font', self.parent.getfont())
        self.settings.setValue('Match Font', self.parent.getMatchFont())
        self.settings.setValue('Email Server', self.emailServerEdit.text())
        self.settings.setValue('Recent Files Count', self.recentFilesSpinBox.text())

        self.settings.sync()
        self.prefsSaved.emit()

    def setFontButtonText(self, button, font):
        #self.fontButton.setText("%s %s" % (str(font.family()),font.pointSize() ))
        button.setText("%s %s" % (str(font.family()),font.pointSize() ))

    def showPrefsDialog(self):
        f = self.parent.getfont()
        self.fontButton.setFont(f)
        self.setFontButtonText(self.fontButton, f)

        f = self.parent.getMatchFont()
        self.fontButtonMatch.setFont(f)
        self.setFontButtonText(self.fontButtonMatch, f)

        self.show()

    def font_slot(self):
        (font, ok) = QFontDialog.getFont(self.fontButton.font())
        if ok:
            self.fontButton.setFont(font)
            self.setFontButtonText(self.fontButton, font)

    def match_font_slot(self):
        (font, ok) = QFontDialog.getFont(self.fontButtonMatch.font())
        if ok:
            self.fontButtonMatch.setFont(font)
            self.setFontButtonText(self.fontButtonMatch, font)

    def apply_slot(self):
        self.parent.setfont(self.fontButton.font())
        self.parent.setMatchFont(self.fontButtonMatch.font())
        self.save()

    def accept(self):
        self.apply_slot()
        QDialog.accept(self)

    def help_slot(self):
        self.helpWindow = help.Help(self, "prefs.html")

