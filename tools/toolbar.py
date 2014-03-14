#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2012, 2014 Emilio Coppola
#
# This file is part of Stellar.
#
# Stellar is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Stellar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Stellar.  If not, see <http://www.gnu.org/licenses/>.

from PyQt4 import QtCore, QtGui
import os, sys, subprocess

class ToolBar(QtGui.QToolBar):
    def __init__(self, main):
        super(ToolBar, self).__init__(main)
        self.main = main

        # func, img, title
        funcs = [[self.open_folder, 'stellar_1.png', 'Stellar'], 
                [self.open_folder, 'open.png', 'Open'],
                [self.run_project, 'run.png', 'Run'],
                [self.main.treeView.add_file, 'addfile.png', 'Add file'],
                [self.main.treeView.add_directory, 'addfolder.png', 'Add folder'],
                [QtGui.qApp.quit, 'close.png', 'Exit'],
                [self.open_folder, 'documentation.png', 'Documentation'],
                [self.toggle_console, 'output.png', 'Show output']]

        for i,x in enumerate(funcs):
            action = QtGui.QAction(QtGui.QIcon(os.path.join('images', x[1])), x[2], self)
            action.triggered.connect(x[0])
            self.addAction(action)
            if i == 5:
                spacer = QtGui.QWidget() 
                spacer.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding) 
                self.addWidget(spacer)

        self.setMovable(False) 


    def toggle_console(self):
        self.main.c_displayed = not self.main.c_displayed
        self.main.output.setVisible(self.main.c_displayed)

    def open_folder(self):
        target = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory"))
        if target:
            self.root = self.treeView.fileSystemModel.setRootPath(target)
            self.treeView.setRootIndex(self.root)

    def run_project(self):
        self.main.statusBar().showMessage('Running project...', 2000)
        eel = self.main.eeldir
        f = 'main'
        os.chdir(self.main.projectdir)
        args = [eel, f]
        if sys.platform=="win32":
            eelbox = subprocess.Popen([eel, f], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            out = eelbox.stdout.read()
            self.main.output.setText(out)
            self.main.output.moveCursor(QtGui.QTextCursor.End)
            self.main.statusBar().showMessage('Done!', 2000)
