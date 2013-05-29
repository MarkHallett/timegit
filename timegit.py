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
        '''
        
        
        '''
        # get repo info
        
        # (make) cd to data dir   
        #cwd = os.path.getcwd()
        
        if not os.path.exists(self.data_dir):
            os.mkdir(self.data_dir)
        os.chdir(self.data_dir)
        
        working_dir = os.path.join(self.data_dir,self.git_repo+'_data')
        if os.path.exists(working_dir):
            os.chdir(working_dir) 
            os.chdir(self.git_repo)
        else:
            os.mkdir(working_dir)                                   
         
            print working_dir  
            os.chdir(working_dir)           
        
        # TODO, put in test for second run
            cmd = r"git clone https://github.com/MarkHallett/%s.git" %self.git_repo
            print cmd
            try:
                os.system(cmd)
            except:
                pass
        
            os.chdir(self.git_repo)
            cmd = r"git log --pretty=format:'%h %ad | %s%d [%an]' --graph --date=short > ../commits.txt"
            print cmd
            os.system(cmd)
        
    
        # read the file containing the git revisions
        # change to with
        f = open('../commits.txt')
        
        commit_ids = []
        for count, line in enumerate(f):
            rev = line.split(' ')[1] 
            #print rev
            commit_ids.append(rev)
        f.close()
        #print commit_ids
        commit_ids.reverse()
        #print commit_ids
        
        #return
        # add data dir to sys.path ??
        #return        
        sys.path.append('.')
         
        
        times = [0.0,] # quick way to put on origin
        print '-----------'
        
        #commit_ids = [ '5f70391', '1784d1c', 'e43c72e','dd2fc2f','bdf4f4c','0c84f55' ,'3a0fe9d']        
        #commit_ids = [ 'bdf4f4c','0c84f55' ,'3a0fe9d']   
        #commit_ids = [ 'e43c72e',] 
        #commit_ids = [ '70d4bcba1ab', ]
        # for each repo version
        for count, commit_id in enumerate(commit_ids):        
            #if count == 3: break
            #continue
            print '...........'
            print count,commit_id
    
            cmd =  'git checkout %s' %commit_id
            #print cmd
            os.system(cmd) #TODO check return code

            # clean up new revision, del pyc and reload modules
            os.system('find . -name \*.pyc |xargs rm') 
            
            for mod in sys.modules.values():
                #print mod
                if mod:
                    try:
                        reload(mod) 
                    except:
                        pass
                       
            # TODO confing the funtion to run
            try:
                import timegit_test
            except Exception, e:
                print "No timing module in this revision %s" %(str(e))
                times.append(-1)
                continue
            
            start = datetime.datetime.now()
            #start = time.clock()
            try:
                timegit_test.run()      
            except:
                print 'No function in this revision'
                time.append(-1)
                continue
            run_time = datetime.datetime.now() - start
 
            print 'run_time', run_time
            seconds = run_time.seconds + run_time.microseconds/1E6
            
            print 'SECONDS',seconds
            times.append(seconds) 
            
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
            
        print 'Done'
            

# --------------------

def test():
    config_file_name = 'config.cfg'
    myTimeGit = TimeGit(config_file_name)
    myTimeGit.run()   
    
if __name__ == '__main__':
    test()
