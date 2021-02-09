# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class frameMain
###########################################################################

class frameMain ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"wxFormbuilder Widget Examples", pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizerFrameMain = wx.BoxSizer( wx.VERTICAL )

		bSizerMainFrame = wx.BoxSizer( wx.VERTICAL )

		self.m_panelMain = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizerMainFrame.Add( self.m_panelMain, 1, wx.EXPAND |wx.ALL, 0 )

		m_listBox3Choices = []
		self.m_listBox3 = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_listBox3Choices, 0 )
		bSizerMainFrame.Add( self.m_listBox3, 0, wx.ALL, 5 )


		bSizerFrameMain.Add( bSizerMainFrame, 1, wx.ALL|wx.EXPAND, 0 )


		self.SetSizer( bSizerFrameMain )
		self.Layout()
		self.menubarMain = wx.MenuBar( 0 )
		self.menuTools = wx.Menu()
		self.menuItemToolsRank = wx.MenuItem( self.menuTools, wx.ID_ANY, u"Rank", wx.EmptyString, wx.ITEM_NORMAL )
		self.menuTools.Append( self.menuItemToolsRank )

		self.menuItemToolsNewEmp = wx.MenuItem( self.menuTools, wx.ID_ANY, u"New Employee", wx.EmptyString, wx.ITEM_NORMAL )
		self.menuTools.Append( self.menuItemToolsNewEmp )

		self.menuItemToolsCancel = wx.MenuItem( self.menuTools, wx.ID_ANY, u"Cancel Overtime", wx.EmptyString, wx.ITEM_NORMAL )
		self.menuTools.Append( self.menuItemToolsCancel )

		self.menubarMain.Append( self.menuTools, u"Tools" )

		self.SetMenuBar( self.menubarMain )


		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_MENU, self.menuItemToolsRankOnMenuSelection, id = self.menuItemToolsRank.GetId() )
		self.Bind( wx.EVT_MENU, self.menuItemToolsNewEmpOnMenuSelection, id = self.menuItemToolsNewEmp.GetId() )
		self.Bind( wx.EVT_MENU, self.menuItemToolsCancelOnMenuSelection, id = self.menuItemToolsCancel.GetId() )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def menuItemToolsRankOnMenuSelection( self, event ):
		event.Skip()

	def menuItemToolsNewEmpOnMenuSelection( self, event ):
		event.Skip()

	def menuItemToolsCancelOnMenuSelection( self, event ):
		event.Skip()


