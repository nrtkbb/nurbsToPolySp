# -*- coding: utf-8 -*-
import pymel.core as pm


class OptionsWindow(object):
    """
    optionsWindow base class.
    """
    @classmethod
    def showUI(cls):
        win = cls()
        win.create()
        return win
 
    def __init__(self):
        self.name = u'optionsWindow'
        self.title = u'Options Window'
        self.supportsToolAction = False
        self.actionName = u'Apply and Close'
 
    def create(self):
        if pm.window(self.name, ex=True):
            pm.deleteUI(self.name)
        self.window = pm.window(
            self.name,
            title=self.title,
            menuBar=True
        )
        self.commonMenu()
        with self.window:
            self.mainForm = pm.formLayout()
            with self.mainForm:
                self.commonButtons(self.mainForm)
                self.optionsBorder = pm.tabLayout(
                    scrollable=True,
                    tabsVisible=False,
                    height=1,
                    childResizable=True
                )
                with self.optionsBorder:
                    self.optionsForm = pm.formLayout()
                    with self.optionsForm:
                        self.displayOptions()
        pm.formLayout(self.mainForm, edit=True,
                      attachForm=(
                          (self.optionsBorder, 'top', 0),
                          (self.optionsBorder, 'left', 0),
                          (self.optionsBorder, 'right', 0)
                      ),
                      attachControl=(
                          (self.optionsBorder, 'bottom', 5, self.applyBtn)
                      )
        )
 
    def commonMenu(self):
        self.editMenu = pm.menu(label='Edit')
        self.editMenuSave = pm.menuItem(
            label='Save Settings',
            command=self.editMenuSaveCmd
        )
        self.editMenuReset = pm.menuItem(
            label='Reset Settings',
            command=self.editMenuResetCmd
        )
        self.editMenuDiv = pm.menuItem(divider=True)
        self.editMenuRadio = pm.radioMenuItemCollection()
        self.editMenuTool = pm.menuItem(
            label='As Tool',
            radioButton=True,
            enable=self.supportsToolAction,
            command=self.editMenuToolCmd
        )
        self.editMenuAction = pm.menuItem(
            label='As Action',
            radioButton=True,
            enable=self.supportsToolAction,
            command=self.editMenuActionCmd
        )
        self.helpMenu = pm.menu(label='Help')
        self.helpMenuItem = pm.menuItem(
            label='Help on %s' % self.title,
            command=self.helpMenuCmd
        )
 
    def helpMenuCmd(self, *args):
        pm.launch(web='https://github.com/nrtkbb/')
 
    def commonButtons(self, form):
        self.cmnBtnSize = dict(height=26)
        self.actionBtn = pm.button(
            label=self.actionName,
            height=self.cmnBtnSize['height'],
            command=self.actionBtnCmd
        )
        self.applyBtn = pm.button(
            label='Apply',
            height=self.cmnBtnSize['height'],
            command=self.applyBtnCmd
        )
        self.closeBtn = pm.button(
            label='Close',
            height=self.cmnBtnSize['height'],
            command=self.closeBtnCmd
        )
        pm.formLayout(form, edit=True,
                      attachForm=(
                          (self.actionBtn, 'left', 5),
                          (self.actionBtn, 'bottom', 5),
                          (self.applyBtn, 'bottom', 5),
                          (self.closeBtn, 'bottom', 5),
                          (self.closeBtn, 'right', 5)
                      ),
                      attachPosition=(
                          (self.actionBtn, 'right', 1, 33),
                          (self.closeBtn, 'left', 0, 67)
                      ),
                      attachControl=(
                          (self.applyBtn, 'left', 4, self.actionBtn),
                          (self.applyBtn, 'right', 4, self.closeBtn )
                      ),
                      attachNone=(
                          (self.actionBtn, 'top'),
                          (self.applyBtn, 'top'),
                          (self.closeBtn, 'top')
                      )
        )
 
    def displayOptions(self):
        pass
 
    def editMenuSaveCmd(self, *args):
        pass
 
    def editMenuResetCmd(self, *args):
        pass
 
    def editMenuToolCmd(self, *args):
        pass
 
    def editMenuActionCmd(self, *args):
        pass
 
    def actionBtnCmd(self, *args):
        self.applyBtnCmd()
        self.closeBtnCmd()
 
    def applyBtnCmd(self, *args):
        pass
 
    def closeBtnCmd(self, *args):
        pm.deleteUI(self.name, window=True)
