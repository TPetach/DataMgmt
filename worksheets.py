import wx, sqlite3, datetime
import os, sys, re, cPickle
import scidb

menu_titles = [ "Open",
                "Properties",
                "Rename",
                "Delete" ]

menu_title_by_id = {}
#for title in menu_titles:
for id in range(len(menu_titles)):
    menu_title_by_id[ id + 101 ] = menu_titles[id]

treePopMenuItems = {101:'Add Book',
                    201:'Add Sheet', 202:'Delete this Book',
                    301:'Add Column', 302:'Delete this Sheet',
                    402:'Delete this Column'}

class SetupWorksheetsPanel(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        self.InitUI()

    def InitUI(self):
        #horizontal split means the split goes across
        #vertical split means the split goes up and down
        hSplit = wx.SplitterWindow(self, -1)
        setupPanel = wx.Panel(hSplit, -1)
        vSplit = wx.SplitterWindow(setupPanel, -1)
        treeViewPanel = wx.Panel(vSplit, -1)

        self.dsTree = wx.TreeCtrl(treeViewPanel, 1, wx.DefaultPosition, (-1,-1), wx.TR_HAS_BUTTONS|wx.TR_LINES_AT_ROOT)
        self.dsRootID = self.dsTree.AddRoot('DataSets')
        print "dsRootID:", self.dsRootID
        # for every tree item except the root, the PyData is a 2-tuple: ([Table Name], [Record ID in that table])
        self.dsTree.SetPyData(self.dsRootID, ('(no table)',0))
        self.dsTree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, id=1)
        self.tree_item_clicked = None
        # 1. Register source's EVT_s to invoke pop-up menu launcher
        wx.EVT_TREE_ITEM_RIGHT_CLICK(self.dsTree, -1, self.dsTreeRightClick)

        trPnlSiz = wx.BoxSizer(wx.VERTICAL)
        trPnlSiz.Add(self.dsTree, 1, wx.EXPAND)
        treeViewPanel.SetSizer(trPnlSiz)

        detailsPanel = wx.Panel(vSplit, -1)
        self.detailsLabel = wx.StaticText(detailsPanel, -1, "This will have the details")
        vSplit.SplitVertically(treeViewPanel, detailsPanel)
        hSiz = wx.BoxSizer(wx.HORIZONTAL)
        hSiz.Add(vSplit, 1, wx.EXPAND)
        setupPanel.SetSizer(hSiz)
        
        previewPanel = wx.Panel(hSplit, -1)
        wx.StaticText(previewPanel, -1, "This will be where you preview the dataset as a grid.")
        hSplit.SplitHorizontally(setupPanel, previewPanel)

        vSiz = wx.BoxSizer(wx.VERTICAL)
        vSiz.Add(hSplit, 1, wx.EXPAND)
        self.SetSizer(vSiz)

    def OnSelChanged(self, event):
        print "OnSelChanged"
        item = event.GetItem()
        self.detailsLabel.SetLabel(self.dsTree.GetItemText(item))
#        print "ItemData:", self.dsTree.GetItemData(item)
        ckPyData = self.dsTree.GetPyData(item)
        print "PyData:", ckPyData

    def dsTreeRightClick(self, event):
        self.tree_item_clicked = right_click_context = event.GetItem()
        ckPyData = self.dsTree.GetPyData(self.tree_item_clicked)
        print "PyData from Right Click:", ckPyData
        menu = wx.Menu()
#        for (id,title) in menu_title_by_id.items():
        for (id,title) in treePopMenuItems.items():
            
            ### 3. Launcher packs menu with Append. ###
            print id, title
            menu.Append( id, title )
            ### 4. Launcher registers menu handlers with EVT_MENU, on the menu. ###
            wx.EVT_MENU( menu, id, self.MenuSelectionCb )

        ### 5. Launcher displays menu with call to PopupMenu, invoked on the source component, passing event's GetPoint. ###
        self.PopupMenu( menu, event.GetPoint() )
        menu.Destroy() # destroy to avoid mem leak

    def MenuSelectionCb( self, event ):
        # do something
        operation = menu_title_by_id[ event.GetId() ]
        print "operation:", operation
#        target = self.tree_item_clicked
        target = self.dsTree.GetItemText(self.tree_item_clicked)
        print "target:", target
                    
    def onButton(self, event, strLabel):
        """"""
        print ' You clicked the button labeled "%s"' % strLabel

#    def onClick_BtnNotWorkingYet(self, event, strLabel):
#        wx.MessageBox('"Hello" is not implemented yet', 'Info', 
#            wx.OK | wx.ICON_INFORMATION)

class SetupWorksheetsFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title)
        self.InitUI()
        self.SetSize((750, 600))
#        self.Centre()
        self.Show(True)

    def InitUI(self):
        framePanel = SetupWorksheetsPanel(self, wx.ID_ANY)

def main():
    app = wx.App(redirect=False)
    SetupWorksheetsFrame(None, wx.ID_ANY, 'Set Up Worksheets')
    app.MainLoop() 

if __name__ == '__main__':
    main()
