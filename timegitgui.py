# timegitgui.py
# temp

import os
import wx
import logging
import ConfigParser
import timegit
import subprocess

# Some classes to use for the notebook pages.  Obviously you would
# want to use something more meaningful for your application, these
# are just for illustration.

class PageOne(wx.Panel):
    def __init__(self, parent, module, function_call):

        p = wx.Panel.__init__(self, parent)
        
        t2 = wx.StaticText(self, -1, "Module", (15,20))
        self.module = wx.TextCtrl(self,-1, module, pos=(120,20))        

        t3 = wx.StaticText(self, -1, "Function Call", (15,50))
        self.function_call = wx.TextCtrl(self,-1, function_call, pos=(120,50))        #zz = wx.StaticText(self, -1, "This", pos = (10,12) )

    def setArgs(self,test_module, test_function):                 
        self.module.SetValue(test_module)
        self.function_call.SetValue(test_function)
    
class PageTwo(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        v = wx.StaticText(self,-1, "Verbosity     ")
        
        r1 = wx.RadioButton(self,-1, "Debug", style=wx.RB_GROUP)
        r2 = wx.RadioButton(self,-1, "Info")
        r3 = wx.RadioButton(self,-1, "Warning")
        r4 = wx.RadioButton(self,-1, "Error")
        r5 = wx.RadioButton(self,-1, "Critical")
      
        sizerV = wx.BoxSizer(wx.HORIZONTAL)
        sizerV.Add(v,0)
        sizerV.Add(r1,0)
        sizerV.Add(r2,0)
        sizerV.Add(r3,0)
        sizerV.Add(r4,0)
        sizerV.Add(r5,0)
        self.SetSizer(sizerV)
        
        r3.SetValue(True)
       
        

class PageThree(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "Not done yet", (20,20))


class MainFrame(wx.Frame):
    def __init__(self):
        logger = logging.getLogger('timegitgui')
        logger.info('hi from xx')
        
        wx.Frame.__init__(self, None, title="TimeGit", size = (640,400) )
        b = 10
        p = wx.Panel(self)
        
        # top row
        b1 = wx.StaticText(p,-1,'Config file'  ) 

        self.config_file_dir = os.getcwd()
        self.config_filename = 'config.cfg'
        self.config_file_name = os.path.join(self.config_file_dir, self.config_filename)

        self.getConfigArgsFromFile()
        
        textCtrlText = self.config_file_name
        self.b2 = wx.TextCtrl(p,4, textCtrlText) 
        wx.EVT_KILL_FOCUS(self.b2, self.OnConfigExit)        
        
        #self.b2.SetBackgroundColour((237,237,237))
        
        b3 = wx.Button(p,3,'Browse'  )  
        self.Bind(wx.EVT_BUTTON, self.OnBrowseConfigFile, id=3)
        
        sizerR1 = wx.BoxSizer(wx.HORIZONTAL)
        sizerR1.Add(b1, 0, flag = wx.ALL, border = b)
        sizerR1.Add(self.b2, 3, flag = wx.EXPAND | wx.ALL, border = b)
        sizerR1.Add(b3, 0, flag = wx.ALIGN_RIGHT | wx.ALL, border = b)
        
        # 2nd top row
        b21= wx.StaticText(p,-1,'Git repo'  ) 
        self.b22 = wx.TextCtrl(p,-1, self.git_repo ,style = wx.TE_READONLY )
        self.b22.SetBackgroundColour((237,237,237))
      
        sizerR20 = wx.BoxSizer(wx.HORIZONTAL)
        sizerR20.Add(b21, 0, flag = wx.ALL, border = b)
        sizerR20.Add(self.b22, 3, flag = wx.EXPAND | wx.ALL, border = b)
        
        # 3rd top row
        b31= wx.StaticText(p,-1,'Data dir'  ) 
        self.b32 = wx.TextCtrl(p,-1,self.data_dir  )
        b33 = wx.Button(p,4,'Browse'  )  
        self.Bind(wx.EVT_BUTTON, self.OnBrowseDataDir, id=4)
                   
        sizerR30 = wx.BoxSizer(wx.HORIZONTAL)
        sizerR30.Add(b31, 0, flag = wx.ALL, border = b)
        sizerR30.Add(self.b32, 3, flag = wx.EXPAND | wx.ALL, border = b) 
        sizerR30.Add(b33, 0, flag = wx.ALIGN_RIGHT | wx.ALL, border = b)
        
        # Here we create a panel and a notebook on the panel
        
        nb = wx.Notebook(p)
           
        # create the page windows as children of the notebook
        self.page1 = PageOne(nb,self.test_module, self.test_function)
        page2 = PageTwo(nb)
        page3 = PageThree(nb)
        #page4 = PageThree(nb)
        #page5 = PageThree(nb)
      
        # add the pages to the notebook with the label to show on the tab
        nb.AddPage(self.page1, "Basic")
        nb.AddPage(page2, "Optional")
        nb.AddPage(page3, "Advanced")
        #nb.AddPage(page4, "Log")
        #nb.AddPage(page5, "Output")
      
        # bottom row
        b4 = wx.Button(p,1,'Close')
        self.Bind(wx.EVT_BUTTON, self.OnClose, id=1)
        b6 = wx.Button(p,6,'Run'  )  
        self.Bind(wx.EVT_BUTTON, self.OnRun, id=6)
              
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
        
    def OnConfigExit(self,e):      
        self.config_file_name = self.b2.GetValue()
        if os.path.isfile(self.config_file_name):        
            self.getConfigArgsFromFile()
            self.SetArgs()        

    def getConfigArgsFromFile(self): 
        #print 'getConfigArgs', self.config_file_name
        
        if 1: # file exists
        # read ./config.cfg
        #if file_name == None:
        #    print 
            #file_name == './congig.cg
            try: # TODO
                parser = ConfigParser.SafeConfigParser()  
                parser.read(self.config_file_name)  
                self.git_repo = parser.get('TimeGit', 'git_repo')
                self.data_dir = parser.get('TimeGit', 'data_dir') 
                self.test_module = parser.get('TimeGit', 'test_module') 
                self.test_function = parser.get('TimeGit', 'test_function') 
                self.verbosity = parser.get('TimeGitOptional', 'verbosity') 
            except Exception,e:
                pass
            
    def SetArgs(self):
        #getConfigArgsFromFile     
        self.b22.SetValue(self.git_repo)
        self.b32.SetValue(self.data_dir) # to be tested
        self.page1.setArgs(self.test_module,self.test_function)

    def ReadArgs(self):
        #self.git_repo ='xx'
        #self.data_dir = 'yy'
        #self.test_module = 'zz'
        #self.test_function = 'aa'
             
        #self.config_file_name = 'aaa'
        #self.page1.module = 'bbb'
        #self.page1.function_call = 'ccc'
        
        pass
      
        
    def OnBrowseConfigFile(self,e):
        """ Open a file"""
        
        if os.path.isdir(self.b2.GetValue()):
            self.dirname = self.b2.GetValue()
        elif os.path.isdir(os.path.dirname(self.b2.GetValue())):
            self.dirname = os.path.dirname(self.b2.GetValue())
        else:
            self.dirname = os.getcwd() # TODO get path from b2
        
        dlg = wx.FileDialog(self, "Choose a config file", self.dirname, '', "*.cfg", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            self.config_file_name = os.path.join(self.dirname, self.filename)
            self.b2.SetValue(self.config_file_name)
            #self.getConfigArgsFromFile()
            self.getConfigArgsFromFile()
            self.SetArgs()            
            
        dlg.Destroy()
        
    def OnBrowseDataDir(self,e):
        self.dirname = os.getcwd()
        data_dir = os.path.dirname(os.getcwd())
        data_dir = os.path.join(data_dir,'timegitdata')
        dlg = wx.DirDialog(self, "Choose a data directory:" , data_dir) # TODO Use dir in the box, (box on exit do)
        if dlg.ShowModal() == wx.ID_OK:
            #print "You chose %s" % dlg.GetPath()
            self.b32.SetValue(dlg.GetPath() )            
        dlg.Destroy()        
        
    def OnClose(self,event):
        self.Close(True)
        
    def OnRun(self,event):
        class Args():
            def __init__(self, git_repo, data_dir, module, function_call):
                self.config_file = None
                self.git_repo = git_repo
                self.data_dir = data_dir
                self.module = module
                self.function_call = function_call
        logger.info('hi from run')
        
        git_repo = self.b22.GetValue()
        data_dir = self.b32.GetValue()
        module = self.page1.module.GetValue()
        function_call = self.page1.function_call.GetValue()
        
        #cmd = "python timegit.py -c %s -m %s -f '%s'" %(self.config_filename, module, function_call)
        #logger.info(cmd)
        #wd = "/Users/markhallett/Google Drive/git/timegit/timegit"
        
        '''
        proc = subprocess.Popen(cmd, 
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE, 
                         shell=True) 
        #,
        #                 cwd=wd )
        
        rtn = proc.wait()
        '''
        
        args = Args( git_repo, data_dir, module, function_call  )
        timegit.run(args)
        
        
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(levelname)-8s %(name)-12s %(message)s',
                            datefmt='%y-%m-%d %H:%M:%S',
                            filename='timegitgui.log',
                            filemode='w')   
    
    logger = logging.getLogger('timegitgui')
    logger.info('TEST')
    
    eg = timegit.test()
    eg.run()
        
    app = wx.App()
    x = MainFrame()
    x.Center()
    x.Show()
    app.MainLoop()
