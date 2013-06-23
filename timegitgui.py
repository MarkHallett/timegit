# timegitgui.py



import wx


# Some classes to use for the notebook pages.  Obviously you would
# want to use something more meaningful for your application, these
# are just for illustration.

class PageOne(wx.Panel):
    def __init__(self, parent):
        p = wx.Panel.__init__(self, parent)
        

        
        t2 = wx.StaticText(self, -1, "Module", (15,20))
        b2 = wx.TextCtrl(self,-1, "test", pos=(120,20))        

        t3 = wx.StaticText(self, -1, "Function Call", (15,50))
        z3 = wx.TextCtrl(self,-1, "run()", pos=(120,50))        #zz = wx.StaticText(self, -1, "This", pos = (10,12) )
                      

class PageTwo(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        box = wx.StaticBox(self, -1, 'Verbosity')
        box.SetMaxSize((100,130))
        #box.Border(30)
        r1 = wx.RadioButton(self,-1, "Debug", style=wx.RB_GROUP)
        r2 = wx.RadioButton(self,-1, "Info")
        r3 = wx.RadioButton(self,-1, "Warning")
        r4 = wx.RadioButton(self,-1, "Error")
        r5 = wx.RadioButton(self,-1, "Critical")
      
        sizer = wx.StaticBoxSizer(box,wx.VERTICAL)
        sizer.Add(r1)
        sizer.Add(r2)
        sizer.Add(r3)
        sizer.Add(r4)
        sizer.Add(r5)
        self.SetSizer(sizer)

class PageThree(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "This is a PageThree object", (60,60))


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="TimeGit", size = (500,500) )

        b = 10
        p = wx.Panel(self)
        
        # top row
        b1 = wx.StaticText(p,-1,'Config file'  ) 
        b2 = wx.TextCtrl(p,-1,'./Config.cfg'  )
        b3 = wx.Button(p,-1,'Browse'  )  
        
        sizerR1 = wx.BoxSizer(wx.HORIZONTAL)
        sizerR1.Add(b1, 0, flag = wx.ALL, border = b)
        sizerR1.Add(b2, 3, flag = wx.EXPAND | wx.ALL, border = b)
        sizerR1.Add(b3, 0, flag = wx.ALIGN_RIGHT | wx.ALL, border = b)
        
        # 2nd top row
        b21= wx.StaticText(p,-1,'Git repo'  ) 
        b22 = wx.TextCtrl(p,-1,'eg git'  )
      
        sizerR20 = wx.BoxSizer(wx.HORIZONTAL)
        sizerR20.Add(b21, 0, flag = wx.ALL, border = b)
        sizerR20.Add(b22, 3, flag = wx.EXPAND | wx.ALL, border = b)
        
        # 3rd top row
        b31= wx.StaticText(p,-1,'Data dir'  ) 
        b32 = wx.TextCtrl(p,-1,'eg ../data'  )
        b33 = wx.Button(p,-1,'Browse'  )  
                   
        sizerR30 = wx.BoxSizer(wx.HORIZONTAL)
        sizerR30.Add(b31, 0, flag = wx.ALL, border = b)
        sizerR30.Add(b32, 3, flag = wx.EXPAND | wx.ALL, border = b) 
        sizerR30.Add(b33, 0, flag = wx.ALIGN_RIGHT | wx.ALL, border = b)
        
        # Here we create a panel and a notebook on the panel
        
        nb = wx.Notebook(p)
           
        # create the page windows as children of the notebook
        page1 = PageOne(nb)
        page2 = PageTwo(nb)
        page3 = PageThree(nb)
      
        # add the pages to the notebook with the label to show on the tab
        nb.AddPage(page1, "Basic")
        nb.AddPage(page2, "Optional")
        nb.AddPage(page3, "Advanced")
      
        # bottom row
        b4 = wx.Button(p,-1,'Cancel'  ) 
        b6 = wx.Button(p,-1,'Run'  )  
              
        sizerR3 = wx.BoxSizer(wx.HORIZONTAL)
        sizerR3.Add(b4,0, flag = wx.ALIGN_LEFT)
        #sizerR3.Add(b5,1)
        sizerR3.Add((1,1,),1, border = b)
        sizerR3.Add(b6, 0, flag = wx.ALIGN_RIGHT)        
        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(sizerR1, flag = wx.ALL | wx.EXPAND, border = b )
        sizer.Add(sizerR20, flag = wx.LEFT | wx.RIGHT | wx.EXPAND, border = b )
        sizer.Add(sizerR30, flag = wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, border = b )
        sizer.Add(nb, 1, flag = wx.ALL | wx.EXPAND, border = b )
        sizer.Add(sizerR3, flag = wx.EXPAND|wx.ALL, border = b)
        p.SetSizer(sizer)     

        
        
        
if __name__ == "__main__":
    app = wx.App()
    x = MainFrame()
    x.Center()
    x.Show()
    app.MainLoop()