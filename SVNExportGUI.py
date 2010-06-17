import os
import sys

import wx
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
        
        rurl = self.m_textCtrlURL.GetValue()
        entry_rev = self.m_checkBoxEntryRev.IsChecked()

        self._SetDisabled()
        text = list_entries(get_entries(rurl, entry_rev))

        dlg = wx.MessageDialog(self, text, 'List', wx.OK|wx.ICON_INFORMATION)
        dlg.ShowModal()
        self._SetEnabled()

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
        
        self.rurl = self.m_textCtrlURL.GetValue()
        self.epath = self.m_dirPickerPath.GetPath()
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
