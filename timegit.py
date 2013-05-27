# timegit

import os
import sys
import time
import datetime
import ConfigParser
import matplotlib.pyplot as plt

class TimeGit(object):
    def __init__(self,config_file_name):
        # read config info   
        print config_file_name
        parser = ConfigParser.SafeConfigParser()  
        parser.read(config_file_name)  
        self.git_repo = parser.get('TimeGit', 'git_repo')   
        self.start_date = parser.get('TimeGit', 'start_date') 
        self.data_dir = parser.get('TimeGit', 'data_dir') 
        self.test_module = parser.get('TimeGit', 'test_module') 
        self.test_function = parser.get('TimeGit', 'test_function')   
        self.debug = parser.get('TimeGit', 'debug') 
        
        if self.debug:
            print 'Config params'
            print '  confing_file_name', config_file_name
            print '  git_repo', self.git_repo
            print '  start_data', self.start_date
            print '  data_dir', self.data_dir
            print '  test_module', self.test_module
            print '  test_function', self.test_function
            

    def run(self):
        print 'run'
        
        # get repo info
        # (make) cd to data dir
        cmd = r"git clone https://github.com/MarkHallett/TimeGitExmple.git"
        cmd = r"git log --pretty=format:'%h %ad | %s%d [%an]' --graph --date=short > commits.txt"
        # add data dir to sys.path
        
        new_path = os.path.join(self.data_dir, self.git_repo)
        print 'new_path:',new_path
        os.chdir(new_path)#return
        #print os.system('ls %s' %(new_path))
        #sys.path.append(new_path)
        sys.path.append('.')
        #print os.system('pwd')        
        
        
        commit_ids = [ '5f70391', '1784d1c', 'e43c72e']        
        #commit_ids = [ 'e43c72e',] 
        #commit_ids = [ '70d4bcba1ab', ]
        # for each repo version
        
        times = []
        print '-----------'
        for commit_id in commit_ids:        
            
            print commit_id
            #print 'A',os.system('pwd')
            #os.chdir( new_path)
            #os.system('cd')
            
            #print 'B', os.system('pwd')
            
            cmd =  'git checkout %s' %commit_id
            
            #print cmd
            os.system(cmd)
            

        #    switch to repo version
        #    git checkout 1234567
        #    # for each test file
        #    (check test file exists)
        #    time the run test code in repo
            import timegit_test
            reload(timegit_test)
            start = datetime.datetime.now()
            #start = time.clock()
            
            #reload (timegit_test)
            #print timegit_test
            #import eg_code
            #reload (TimeGitExample)
            timegit_test.run()
            #time.sleep(2)
            run_time = datetime.datetime.now() - start
            print 'run_time', run_time
            seconds = run_time.seconds + run_time.microseconds/1E6
            
            print 'SECONDS',seconds
            times.append(seconds) # + run_time.microseconds)
        
        print 'times',times
        # get results
        x = [1,2,3]
        y = times        
        # display results
        #
        fig = plt.figure()
        plt.title(self.git_repo)
       
        plt.plot(x, y)        
        plt.show()
        
        
        
        print 'Done'
        
        pass
    

# --------------------

def test():
    config_file_name = 'config.cfg'
    
    myTimeGit = TimeGit(config_file_name)
    
    myTimeGit.run()   
    
    
test()
