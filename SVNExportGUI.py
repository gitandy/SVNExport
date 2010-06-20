import os
import sys
import xml.dom.minidom

import wx
import wx.richtext
import wx_svnexport

from svnexport import *

__version__ = 'v0.1'
__author_name__ = 'Andreas Schawo'
__author_email__ = 'andreas@schawo.de'
__copyright__ = 'Copyright (c) 2010, Andreas Schawo, All rights reserved'
__license__ = '''Copyright (c) 2010, Andreas Schawo <andreas@schawo.de>

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

class SVNExportFrame( wx_svnexport.Frame ):
    def __init__(self, parent):
        wx_svnexport.Frame.__init__(self, parent)

        try:
            icon = wx.Icon('svnexport.ico', wx.BITMAP_TYPE_ICO, 32, 32)
            self.SetIcon(icon)
        except:
            pass

        self.m_dirPickerPath.SetPath(os.path.join(os.getcwd(), 'export'))
        
        self.Bind(wx.EVT_BUTTON, self.OnList, self.m_buttonList)
        self.Bind(wx.EVT_BUTTON, self.OnExport, self.m_buttonExport)
        self.Bind(wx.EVT_BUTTON, self.OnExit, self.m_buttonExit)
        self.Bind(wx.EVT_MENU, self.OnAbout, self.m_menuAbout)

        self.m_timer = wx.Timer(self, wx.ID_ANY)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.m_timer)

        self.max_urls = 5

        self.__read_config__()
        
    def __read_config__(self):
        self.config_file = os.path.join(os.path.expanduser('~'), '.svnexport.xml')

        if os.path.isfile(self.config_file):
            self.config_dom = xml.dom.minidom.parse(self.config_file)

            root = self.config_dom.documentElement

            lists = root.getElementsByTagName('gui')[0].getElementsByTagName('lists')[0]
            #Read the recent urls
            for u in lists.getElementsByTagName('url'):
                self.m_comboBoxURL.Append(u.childNodes[0].data.strip())
            #self.m_comboBoxURL.SetSelection(0)

            #Read the last path used
            pathl = lists.getElementsByTagName('path')
            if len(pathl) > 0:
                self.m_dirPickerPath.SetPath(pathl[0].childNodes[0].data.strip())
        else:
            #Create an empty structure
            self.config_dom = xml.dom.minidom.getDOMImplementation().createDocument(None, 'svnexport', None)
            
            root = self.config_dom.documentElement

            gui_node = self.config_dom.createElement('gui')
            lists_node = self.config_dom.createElement('lists')

            root.appendChild(gui_node)
            gui_node.appendChild(lists_node)

            with open(self.config_file, 'w') as f:
                self.config_dom.writexml(f)

    def __write_config__(self):        
        lists = self.config_dom.documentElement.getElementsByTagName('gui')[0].getElementsByTagName('lists')[0]

        pathnode = self.config_dom.createElement('path')
        pathnode.appendChild(self.config_dom.createTextNode(self.m_dirPickerPath.GetPath()))

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
            self.config_dom.writexml(f, addindent='  ', newl='\n')

    def _append_url(self, url):
        url = url.strip()
        
        idx = self.m_comboBoxURL.FindString(url)
        if idx >= 0:
            self.m_comboBoxURL.Delete(idx)
            
        #if not url in self.m_comboBoxURL.GetStrings():
        self.m_comboBoxURL.Insert(url, 0)

        if self.m_comboBoxURL.GetCount() > self.max_urls:
            self.m_comboBoxURL.Delete(self.max_urls)

    def _SetEnabled(self, state=True):
        self.m_buttonList.Enable(state)
        self.m_buttonExport.Enable(state)

    def _SetDisabled(self):
        self._SetEnabled(False)

    def OnAbout(self, evt):
        text = 'SVN-Export\n\n' + 'Version: %s\n\n' %__version__ + __copyright__
        dlg = wx.MessageDialog(self, text, 'About', wx.OK|wx.ICON_INFORMATION)
        dlg.ShowModal()

    def OnList(self, evt):
        self.m_statusBar.SetStatusText('')
        self.m_gaugeProgress.SetValue(0)
        
        rurl = self.m_comboBoxURL.GetValue()
        if not str(rurl).strip() == '':
            self._append_url(rurl)
            
            entry_rev = self.m_checkBoxEntryRev.IsChecked()

            self._SetDisabled()
            text = list_entries(get_entries(rurl, entry_rev))

            dlg = wx.Dialog(self, wx.ID_ANY, 'List of Repository Entries',
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
        
            self._SetEnabled()
        else:
            self.m_statusBar.SetStatusText('Repository URL is empty!')

    def OnTimer(self, evt):
        if len(self._entries) > 0:
            entry = self._entries.pop(0)
            self.m_statusBar.SetStatusText(export_entry(self.rurl, self.epath, entry))
            self.m_gaugeProgress.SetValue(self.m_gaugeProgress.GetValue()+1)
            self.m_timer.Start(1, True)
        else:
            self.m_statusBar.SetStatusText('Done')
            self._SetEnabled()
        
    def OnExport(self, evt):
        self.m_statusBar.SetStatusText('')
        
        self.rurl = self.m_comboBoxURL.GetValue()
        if str(self.rurl).strip() == '':
            self.m_statusBar.SetStatusText('Repository URL is empty!')        
            return

        self._append_url(self.rurl)
        
        self.epath = self.m_dirPickerPath.GetPath()
        if str(self.epath).strip() == '':
            self.m_statusBar.SetStatusText('Export path is empty!')        
            return

        entry_rev = self.m_checkBoxEntryRev.IsChecked()

        self.m_gaugeProgress.SetValue(0)

        if not os.path.exists(self.epath):
            os.mkdir(self.epath)
        elif not len(os.listdir(self.epath)) == 0:
            self.m_statusBar.SetStatusText('Folder "%s" is not empty!' %self.epath)
            return

        self._entries = list(get_entries(self.rurl, entry_rev))

        if len(self._entries) > 0:
            self.m_gaugeProgress.SetRange(len(self._entries))
            self._SetDisabled()
            self.m_timer.Start(1, True)
        
    def OnExit(self, evt):
        self.__write_config__()
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
