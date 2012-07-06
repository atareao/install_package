#!/usr/bin/python
# -*- utf-8 -*-
#
# Copyright (C) 2012 Lorenzo Carbonell
# lorenzo.carbonell.cerezo@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#

import pygtk
pygtk.require("2.0")
import gtk
import apt
import apt.progress.gtk2
import apt_pkg
from apt.cache import Cache
from apt.cache import LockFailedException

class InstallPackageDialog(gtk.Dialog):
	def __init__(self,gta = None):
		title = 'Install package'
		gtk.Dialog.__init__(self,title,None,gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,(gtk.STOCK_OK,gtk.RESPONSE_ACCEPT))
		self.set_position(gtk.WIN_POS_CENTER_ALWAYS)
		self.set_size_request(400, 200)
		self.set_resizable(False)
		self.connect('destroy', self.close_application)
		#
		vbox0 = gtk.VBox(spacing = 5)
		vbox0.set_border_width(5)
		self.get_content_area().add(vbox0)
		#
		frame2 = gtk.Frame()
		vbox0.add(frame2)
		table2 = gtk.Table(rows = 2, columns = 2, homogeneous = False)
		table2.set_border_width(5)
		table2.set_col_spacings(5)
		table2.set_row_spacings(5)
		frame2.add(table2)
		#
		label11 = gtk.Label('Package to install:')
		label11.set_alignment(0,.5)
		table2.attach(label11,0,1,0,1, xoptions = gtk.EXPAND|gtk.FILL, yoptions = gtk.SHRINK)
		#
		#
		self.entry12 = gtk.Entry()
		self.entry12.connect('key-press-event',self.on_key_press)
		table2.attach(self.entry12,1,2,0,1, xoptions = gtk.EXPAND|gtk.FILL, yoptions = gtk.SHRINK)
		#
		#
		button22 = gtk.Button('Install')
		button22.connect('clicked',self.install_package)
		table2.attach(button22,0,2,1,2, xoptions = gtk.EXPAND|gtk.FILL, yoptions = gtk.SHRINK)
		#
		self.progress = apt.progress.gtk2.GtkAptProgress()
		self.progress._expander.connect('activate',self.on_progress_activate)
		table2.attach(self.progress,0,2,2,3, xoptions = gtk.EXPAND|gtk.FILL, yoptions = gtk.SHRINK)
		#
		self.show_all()

	def on_key_press(self,widget,event):
		if self.entry12.get_text() != '' and (event.keyval == 65293 or event.keyval ==65421):
			self.install_package(None)
			
	def on_progress_activate(self,widget):
		if self.progress._expander.get_expanded():
			self.set_size_request(400, 200)
		else:
			self.set_size_request(800, 650)
		
	def close_application(self,widget):
		self.hide()
		self.destroy()
		
	def install_package(self,widget):
		cache = apt.cache.Cache(self.progress.open)
		package_name = self.entry12.get_text()
		try:
			if cache[package_name].is_installed:
				md = gtk.MessageDialog(parent=self,
				flags= gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
				type=gtk.MESSAGE_WARNING,
				buttons= gtk.BUTTONS_OK,
				message_format='Package %s is already installed'%package_name)
				md.run()
				md.destroy()
			else:
				try:
					cache[package_name].mark_install(auto_fix=True, auto_inst=True, from_user=True)
					self.set_size_request(800, 650)
					self.progress.show_terminal(expanded=True)
					cache.commit(self.progress.fetch, self.progress.install)					
				except LockFailedException,e:
					print e
					md = gtk.MessageDialog(parent=self,
					flags= gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
					type=gtk.MESSAGE_ERROR,
					buttons= gtk.BUTTONS_OK,
					message_format='Must be root to install "%s"'%package_name)
					md.run()
					md.destroy()
					self.progress.show_terminal(expanded=False)
					self.set_size_request(400, 200)
		except KeyError,e:
			print e
			md = gtk.MessageDialog(parent=self,
			flags= gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
			type=gtk.MESSAGE_ERROR,
			buttons= gtk.BUTTONS_OK,
			message_format='There is no package called "%s"'%package_name)
			md.run()
			md.destroy()
		self.progress.show_terminal(expanded=False)
		self.set_size_request(400, 200)

if __name__ == '__main__':
    ipd = InstallPackageDialog()
    ipd.run()
