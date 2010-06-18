###########################################################################
## Python code generated with wxFormBuilder (version Jun 11 2009)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx

###########################################################################
## Class Frame
###########################################################################

class Frame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__  ( self, parent, id = wx.ID_ANY, title = u"SVN-Export", pos = wx.DefaultPosition, size = wx.Size( 362,310 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL, name = u"SVN-Export" )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_MENU ) )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"URL to repository", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		bSizer1.Add( self.m_staticText1, 0, wx.LEFT|wx.TOP, 5 )
		
		m_comboBoxURLChoices = []
		self.m_comboBoxURL = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, m_comboBoxURLChoices, 0 )
		bSizer1.Add( self.m_comboBoxURL, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Path to export to", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		bSizer1.Add( self.m_staticText2, 0, wx.LEFT|wx.TOP, 5 )
		
		self.m_dirPickerPath = wx.DirPickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_USE_TEXTCTRL )
		bSizer1.Add( self.m_dirPickerPath, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_checkBoxEntryRev = wx.CheckBox( self, wx.ID_ANY, u"Use entry revision instead of repository", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1.Add( self.m_checkBoxEntryRev, 0, wx.ALL, 5 )
		
		
		bSizer1.AddSpacer( ( 0, 0 ) )
		
		self.m_gaugeProgress = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size( -1,20 ), wx.GA_HORIZONTAL )
		self.m_gaugeProgress.SetValue( 0 ) 
		bSizer1.Add( self.m_gaugeProgress, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer1.AddSpacer( ( 0, 0 ) )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer4.AddSpacer( ( 0, 0 ) )
		
		bSizer2.Add( bSizer4, 1, wx.EXPAND, 5 )
		
		self.m_buttonList = wx.Button( self, wx.ID_ANY, u"List", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.m_buttonList, 0, wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		self.m_buttonExport = wx.Button( self, wx.ID_ANY, u"Export", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.m_buttonExport, 0, wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		self.m_buttonExit = wx.Button( self, wx.ID_ANY, u"Exit", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.m_buttonExit, 0, wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		bSizer1.Add( bSizer2, 1, wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT|wx.EXPAND, 5 )
		
		self.SetSizer( bSizer1 )
		self.Layout()
		self.m_statusBar = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
		self.m_menubar1 = wx.MenuBar( 0 )
		self.m_menuHelp = wx.Menu()
		self.m_menuAbout = wx.MenuItem( self.m_menuHelp, wx.ID_ANY, u"About", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuHelp.AppendItem( self.m_menuAbout )
		
		self.m_menubar1.Append( self.m_menuHelp, u"?" )
		
		self.SetMenuBar( self.m_menubar1 )
		
	
	def __del__( self ):
		pass
	

