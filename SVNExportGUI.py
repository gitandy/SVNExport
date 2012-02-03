#!/usr/bin/python

import os
import sys
import gettext
import xml.dom.minidom

import wx
import wx.richtext

import wx_svnexport

from svnexport import *

import locale
__lang__ = locale.getdefaultlocale()[0]
del locale

if sys.platform == 'win32':
    os.environ['LANGUAGE'] = __lang__

__encoding__ = 'cp1252'
try:
    if sys.stdout.encoding:
        __encoding__ = sys.stdout.encoding
except:
    pass

import version
__version__ = version.VERSION
del version
__author_name__ = 'Andreas Schawo'
__author_email__ = 'andreas@schawo.de'
__copyright__ = 'Copyright (c) 2010-2012, Andreas Schawo, All rights reserved'
__license__ = '''Copyright (c) 2010-2012, Andreas Schawo <andreas@schawo.de>

All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

   1. Redistributions of source code must retain the above copyright notice,
      this list of conditions and the following disclaimer.
   2. Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation
      and/or other materials provided with the distribution.
   3. Neither the name of the authors nor the names of its contributors may
      be used to endorse or promote products derived from this software without
      specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE AUTHORS 'AS IS' AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.'''      

__encoding__ = 'cp1252'
try:
    if sys.stdout.encoding:
        __encoding__ = sys.stdout.encoding
except:
    pass

gettext.install('SVNExportGUI', 'locale', unicode=1, codeset=__encoding__)
wx_svnexport._ = _

class AuthDialog(wx.Dialog):
    def __init__(self, parent, realm='', user=''):
        wx.Dialog.__init__(self, parent, -1, _('Authentication required'), size = wx.Size( 250,230 ), style = wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        bSizer = wx.BoxSizer( wx.VERTICAL )
		
        self.m_staticTextRealm = wx.StaticText( self, wx.ID_ANY, realm, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer.Add( self.m_staticTextRealm, 0, wx.ALL, 5 )

        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, _('Username'), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer.Add( self.m_staticText1, 0, wx.LEFT|wx.RIGHT|wx.TOP, 5 )
        
        self.m_textCtrlUsername = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer.Add( self.m_textCtrlUsername, 0, wx.ALL|wx.EXPAND, 5 )
        
        self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, _('Password'), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer.Add( self.m_staticText2, 0, wx.LEFT|wx.RIGHT|wx.TOP, 5 )
        
        self.m_textCtrlPwd = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PASSWORD  )
        bSizer.Add( self.m_textCtrlPwd, 0, wx.ALL|wx.EXPAND, 5 )
        
        self.m_checkBoxSavePwd = wx.CheckBox( self, wx.ID_ANY, _('Save password'), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer.Add( self.m_checkBoxSavePwd, 0, wx.ALL, 5 )

        bSizer.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )

        m_sdbSizer1 = wx.StdDialogButtonSizer()
        self.m_sdbSizer1OK = wx.Button( self, wx.ID_OK )
        m_sdbSizer1.AddButton( self.m_sdbSizer1OK )
        self.m_sdbSizer1Cancel = wx.Button( self, wx.ID_CANCEL )
        m_sdbSizer1.AddButton( self.m_sdbSizer1Cancel )
        m_sdbSizer1.Realize();
        bSizer.Add( m_sdbSizer1, 1, wx.EXPAND, 5 )
        
        self.SetSizer( bSizer )
        self.Layout()

    def getUsername(self):
        return self.m_textCtrlUsername.GetValue()

    def getPassword(self):
        return self.m_textCtrlPwd.GetValue()

    def savePassword(self):
        return self.m_checkBoxSavePwd.IsChecked()


class SVNExportFrame( wx_svnexport.Frame ):
    def __init__(self, parent):
        wx_svnexport.Frame.__init__(self, parent)

        iconf = 'svnexport.ico'
        if os.path.isfile(iconf):
            icon = wx.Icon(iconf, wx.BITMAP_TYPE_ICO, 32, 32)
            self.SetIcon(icon)

        self.m_dirPickerPath.SetPath(os.path.join(os.getcwd(), 'export'))
        
        self.Bind(wx.EVT_BUTTON, self.OnList, self.m_buttonList)
        self.Bind(wx.EVT_BUTTON, self.OnExport, self.m_buttonExport)
        self.Bind(wx.EVT_BUTTON, self.OnExit, self.m_buttonExit)
        self.Bind(wx.EVT_CLOSE, self.OnExit, self)
        self.Bind(wx.EVT_MENU, self.OnAbout, self.m_menuAbout)

        self.m_timer = wx.Timer(self, wx.ID_ANY)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.m_timer)

        self.max_urls = 5
        self.__closing__ = False
        
        self.__read_config__()
        
    def __read_config__(self):
        self.config_file = os.path.join(os.path.expanduser('~'), '.svnexport.xml')

        if os.path.isfile(self.config_file):
            try:
                self.config_dom = xml.dom.minidom.parse(self.config_file)

                root = self.config_dom.documentElement

                #Config
                config = self.config_dom.documentElement.getElementsByTagName('gui')[0].getElementsByTagName('config')[0]
                uentryr_node = config.getElementsByTagName('useentryrev')

                if len(uentryr_node) > 0:
                    if uentryr_node[0].hasAttribute('set'):
                        if uentryr_node[0].getAttribute('set').strip() == 'True':
                            self.m_checkBoxEntryRev.SetValue(True)
                
                #Lists
                lists = root.getElementsByTagName('gui')[0].getElementsByTagName('lists')[0]
                #Read the recent urls
                for u in lists.getElementsByTagName('url'):
                    self.m_comboBoxURL.Append(u.childNodes[0].data.strip())

                #Read the last path used
                pathl = lists.getElementsByTagName('path')
                if len(pathl) > 0:
                    self.m_dirPickerPath.SetPath(pathl[0].childNodes[0].data.strip())
            except:
                self.m_statusBar.SetStatusText(_('Damaged config file! Generating empty config...'))
                self.__generate_config__()
        else:
            self.__generate_config__()

    def __generate_config__(self):
        #Create an empty structure
        self.config_dom = xml.dom.minidom.getDOMImplementation().createDocument(None, 'svnexport', None)
        
        root = self.config_dom.documentElement

        gui_node = self.config_dom.createElement('gui')
        root.appendChild(gui_node)

        #Config
        cfg_node = self.config_dom.createElement('config')
        gui_node.appendChild(cfg_node)

        useentryrev_node = self.config_dom.createElement('useentryrev')
        cfg_node.appendChild(useentryrev_node)
        useentryrev_node.setAttribute('set', 'False')
        
        #Lists
        lists_node = self.config_dom.createElement('lists')
        gui_node.appendChild(lists_node)

        with open(self.config_file, 'w') as f:
            self.config_dom.writexml(f)

    def __write_config__(self):
        #Config
        config = self.config_dom.documentElement.getElementsByTagName('gui')[0].getElementsByTagName('config')[0]
        uentryr_node = config.getElementsByTagName('useentryrev')

        if len(uentryr_node) > 0:
            uentryr_node[0].setAttribute('set', str(self.m_checkBoxEntryRev.IsChecked()))
        
        #Lists
        lists = self.config_dom.documentElement.getElementsByTagName('gui')[0].getElementsByTagName('lists')[0]

        pathnode = self.config_dom.createElement('path')
        pathnode.appendChild(self.config_dom.createTextNode(self.m_dirPickerPath.GetPath().encode(__encoding__)))

        pathn_old = lists.getElementsByTagName('path')
        if len(pathn_old) > 0:
            lists.replaceChild(pathnode, pathn_old[0])
        else:
            lists.appendChild(pathnode)

        #Remove all urls
        for u in lists.getElementsByTagName('url'):
            lists.removeChild(u)

        #Set new url list
        for u in self.m_comboBoxURL.GetStrings():
            urlnode = self.config_dom.createElement('url')
            urlnode.appendChild(self.config_dom.createTextNode(u))
            
            lists.appendChild(urlnode)

        #Write config to file
        with open(self.config_file, 'w') as f:
            self.config_dom.writexml(f, encoding=__encoding__)

    def _append_url(self, url):
        url = url.strip()
        
        idx = self.m_comboBoxURL.FindString(url)
        if idx >= 0:
            self.m_comboBoxURL.Delete(idx)
            
        self.m_comboBoxURL.Insert(url, 0)
        self.m_comboBoxURL.SetSelection(0)

        if self.m_comboBoxURL.GetCount() > self.max_urls:
            self.m_comboBoxURL.Delete(self.max_urls)

    def _auth_callback(self, realm, user, may_save):
        realm_parts = realm.split()
        if len(realm_parts) > 1:
            realm = realm_parts[1]

        use_pwd = 0
        password = ''
        save_pwd = False

        dlg = AuthDialog(self, _('Authentication required for Archive:') + '\n' + realm, user)

        if dlg.ShowModal() == wx.ID_OK:
            use_pwd = 1
            user = dlg.getUsername()
            password = dlg.getPassword()
            save_pwd = dlg.savePassword()
            
        return use_pwd, user, password, save_pwd

    def _SetEnabled(self, state=True):
        self.m_buttonList.Enable(state)
        self.m_buttonExport.Enable(state)

    def _SetDisabled(self):
        self._SetEnabled(False)

    def OnAbout(self, evt):
        text = 'SVN-Export\n\n' + 'Version: %s\n\n' %__version__ + __copyright__
        dlg = wx.MessageDialog(self, text, _('About'), wx.OK|wx.ICON_INFORMATION)
        dlg.ShowModal()

    def OnList(self, evt):
        self.m_statusBar.SetStatusText('')
        self.m_gaugeProgress.SetValue(0)
        
        rurl = self.m_comboBoxURL.GetValue()
        if not str(rurl).strip() == '':
            entry_rev = self.m_checkBoxEntryRev.IsChecked()

            self._SetDisabled()
            
            try:
                text = list_entries(get_entries(rurl, entry_rev, auth_callback=self._auth_callback))

                self._append_url(rurl)
            
                dlg = wx.Dialog(self, wx.ID_ANY, _('List of Repository Entries'),
                                style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
                bSizer = wx.BoxSizer(wx.VERTICAL)	
                m_richText = wx.richtext.RichTextCtrl(dlg, wx.ID_ANY, wx.EmptyString,
                                                      wx.DefaultPosition,
                                                      wx.DefaultSize,
                                                      wx.TE_READONLY|wx.HSCROLL|wx.VSCROLL)
                m_richText.WriteText(text)
                bSizer.Add(m_richText, 1, wx.EXPAND, 5)
                stdButtonSizer = dlg.CreateStdDialogButtonSizer(wx.OK)
                bSizer.Add(stdButtonSizer, 0, wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT|wx.ALL, 5)	
                dlg.SetSizer(bSizer)
                dlg.Layout()
                dlg.ShowModal()
            except SVNExportException, e:
                self.m_statusBar.SetStatusText(e.msg)
        
            self._SetEnabled()
        else:
            self.m_statusBar.SetStatusText(_('Repository URL is empty!'))

    def OnTimer(self, evt):
        if len(self._entries) > 0:
            entry = self._entries.pop(0)
            try:
                self.m_statusBar.SetStatusText(export_entry(self.rurl, self.epath, entry, auth_callback=self._auth_callback))
                self.m_gaugeProgress.SetValue(self.m_gaugeProgress.GetValue()+1)
                self.m_timer.Start(1, True)
            except SVNExportException, e:
                self.m_statusBar.SetStatusText(e.msg)
        else:
            self.m_statusBar.SetStatusText(_('Done'))
            self._SetEnabled()
        
    def OnExport(self, evt):
        self.m_statusBar.SetStatusText('')
        
        self.rurl = self.m_comboBoxURL.GetValue()
        if str(self.rurl).strip() == '':
            self.m_statusBar.SetStatusText(_('Repository URL is empty!'))        
            return
        
        self.epath = self.m_dirPickerPath.GetPath()
        if self.epath.strip() == '':
            self.m_statusBar.SetStatusText(_('Export path is empty!'))        
            return

        entry_rev = self.m_checkBoxEntryRev.IsChecked()

        self.m_gaugeProgress.SetValue(0)

        if not os.path.exists(self.epath):
            os.mkdir(self.epath)
        elif not len(os.listdir(self.epath)) == 0:
            self.m_statusBar.SetStatusText(_('Folder "%s" is not empty!') %self.epath)
            return

        try:
            self._entries = list(get_entries(self.rurl, entry_rev))

            self._append_url(self.rurl)

            if len(self._entries) > 0:
                self.m_gaugeProgress.SetRange(len(self._entries))
                self._SetDisabled()
                self.m_timer.Start(1, True)
        except SVNExportException, e:
            self.m_statusBar.SetStatusText(e.msg)
            
    def OnExit(self, evt):
        if self.__closing__:
            evt.Skip()
        else:
            self.__write_config__()
            self.__closing__ = True
            self.Close()


class SVNExportApp(wx.App):
    def OnInit(self):
        frame = SVNExportFrame(None)
        frame.Show(True)
        self.SetTopWindow(frame)
        return True


if __name__ == '__main__':
    app = SVNExportApp(False)
    app.MainLoop()
