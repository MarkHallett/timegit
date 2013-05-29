# timegit

import os
import sys
import time
import datetime
import ConfigParser
#import matplotlib

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
        # get repo info
        # (make) cd to data dir
        cmd = r"git clone https://github.com/MarkHallett/TimeGitExmple.git"
        cmd = r"git log --pretty=format:'%h %ad | %s%d [%an]' --graph --date=short > commits.txt"
        # add data dir to sys.path
        
        new_path = os.path.join(self.data_dir, self.git_repo)
        print 'new_path:',new_path
        # TODO if not exits make path
        os.chdir(new_path)#return
        #print os.system('ls %s' %(new_path))
        #sys.path.append(new_path)
        
        sys.path.append('.')
        #print os.system('pwd')        
        
        times = []
        print '-----------'
        
        commit_ids = [ '5f70391', '1784d1c', 'e43c72e','dd2fc2f','bdf4f4c','0c84f55' ,'3a0fe9d']        
        #commit_ids = [ 'bdf4f4c','0c84f55' ,'3a0fe9d']   
        #commit_ids = [ 'e43c72e',] 
        #commit_ids = [ '70d4bcba1ab', ]
        # for each repo version
        for count, commit_id in enumerate(commit_ids):        
            #continue
            print '...........'
            print count,commit_id
            cmd =  'git checkout %s' %commit_id
            #print cmd
            os.system(cmd) #TODO check return code
            #time.sleep(1)
            #continue
         
            for mod in sys.modules.values():
                #print mod
                if mod:
                    try:
                        reload(mod)
                    except:
                        pass
                    

            #    (check test file exists)
            #    time the run test code in repo
            
            #try:
            #    del(timegit_test)
            #    del(timegit_test.run)
            #except:
            #    pass
            
            import timegit_test
            reload(timegit_test)
            
            start = datetime.datetime.now()
            #start = time.clock()
            timegit_test.run()      
            run_time = datetime.datetime.now() - start
 
            print 'run_time', run_time
            seconds = run_time.seconds + run_time.microseconds/1E6
            
            print 'SECONDS',seconds
            times.append(round(seconds,2)) 
            
        print 'times',times
        x = range(len(times))
        y = times      
        # display results

        # unfortunate but must import here
        import matplotlib.pyplot as plt
        
        fig = plt.figure()
        plt.title(self.git_repo)
       
        plt.plot(x, y)        
        plt.show()
        
        
        #print timegit_test
        #import eg_code
        
        #reload (TimeGitExample)
        timegit_test.run()

        print 'SECONDS',seconds                
        print 'Done'
            

# --------------------

def test():
    config_file_name = 'config.cfg'
    myTimeGit = TimeGit(config_file_name)
    myTimeGit.run()   
    
if __name__ == '__main__':
    test()
