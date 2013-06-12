# timegit

import os
import sys
import time
import ConfigParser
import argparse
#import matplotlib

class TimeGit(object):
    def __init__(self,args,config_file_name):
        # read config info   
        print config_file_name
        parser = ConfigParser.SafeConfigParser()  
        parser.read(config_file_name)  
        self.git_repo = parser.get('TimeGit', 'git_repo')   
        self.data_dir = parser.get('TimeGit', 'data_dir') 
        
        if args.module:
            self.test_module = args.module
        else:
            self.test_module = parser.get('TimeGit', 'test_module') 
            
        if args.function_call:
            self.test_function = args.function_call
        else:
            self.test_function = parser.get('TimeGit', 'test_function')   
        #self.debug = parser.get('TimeGit', 'debug') 
        
        if 1: #self.debug:
        #    print 'Config params'
        #    print '  confing_file_name', config_file_name
        #    print '  git_repo', self.git_repo
        #    print '  data_dir', self.data_dir
        #    print '  test_module', self.test_module
             print '  config_file_name', config_file_name
             print '  test_module', self.test_module
             print '  test_function', self.test_function

    def _prep(self):
        pass
        # (make) cd to data dir           
        if not os.path.exists(self.data_dir):
           os.mkdir(self.data_dir)
        os.chdir(self.data_dir)
   
       
        repo_path,fileExtension = os.path.splitext(self.git_repo)   
        self.repo_name = repo_path.split('/')[-1] 
        print self.repo_name 
       
        data_dir = os.path.join(self.data_dir,self.repo_name +'_data')
        
        
       
        if os.path.exists(data_dir):
            os.chdir(data_dir) 
            os.chdir(self.repo_name)
        else:
            # data dir does not exist, create it, clone the repo, and get the revisions
            # only needed first time around, delete data dir to refresh
            os.mkdir(data_dir)                                   
        
            print data_dir  
            os.chdir(data_dir)           
       
       
            cmd = r"git clone %s" %self.git_repo
            print cmd
            try:
                os.system(cmd)
            except:
                pass
       
            os.chdir(self.repo_name)
            cmd = r"git log --pretty=format:'%h %ad | %s%d [%an]' --graph --date=short > ../commits.txt"
            print cmd
            os.system(cmd)    


    def _getdatafromgithub(self):
        pass

    def _getgitcommitids(self):
        f = open('../commits.txt')
        commit_ids = []
        for count, line in enumerate(f):
                  rev = line.split(' ')[1] 
                  #print rev
                  commit_ids.append(rev)
        f.close()      
        commit_ids.reverse()
        return commit_ids
              
    def _runtestfunction(self, commit_ids):
        # add data dir to sys.path ??        
        sys.path.append('.')
          
        times = [0.0,] # start from origin
        print '-----------'
          # for each repo version
        for count, commit_id in enumerate(commit_ids):        
            #if count == 3: break
            print '...........'
            print count,commit_id
      
            cmd =  'git checkout %s' %commit_id
            #print cmd
            os.system(cmd) #TODO check return code
  
            # clean up new revision, del pyc and reload modules
            # use walk for os independance
            os.system('find . -name \*.pyc |xargs rm') 
              
            for mod in sys.modules.values():
                if mod:
                    try:
                        reload(mod) 
                    except:
                        pass
                         
            # TODO confing the funtion to run
            try:
                cmd = "import %s" %self.test_module
                exec(cmd)
            except Exception, e:
                print "No timing module (%s) in this revision. %s" %(self.test_module,str(e))
                times.append(0)
                continue
              
            start = time.time()
            try:
                cmd = "%s.%s" %(self.test_module, self.test_function)
                exec(cmd)      
            except:
                print 'No function in this revision. (%s)' %cmd
                times.append(0)
                continue
            run_time = time.time() - start
   
            print 'run_time', run_time
            times.append(run_time)         
        return times
    
    
    def _show(self,times):
        # display results
        # unfortunate but must import here
        import matplotlib.pyplot as plt
        print 'times',times       
        x = range(len(times))
        y = times         

        fig = plt.figure()
        plt.title(self.git_repo)
            
        plt.plot(x, y)        
        plt.show()       
        
    
    def run(self):
        '''
        Short script to extract, run, time, and display the performance
        of code in github
        '''
        
        self._prep()
        self._getdatafromgithub()
        commit_ids = self._getgitcommitids()
        times = self._runtestfunction(commit_ids)  
        self._show(times)
            
        print 'Done'
            

# --------------------

def test(args):
    if args.config_file:
        config_file_name = args.config_file
    else:
        config_file_name = 'config.cfg'
    myTimeGit = TimeGit(args,config_file_name)
    myTimeGit.run()   
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Time git repos')
    parser.add_argument('-c', action='store', dest='config_file',
                    help='config file')
    parser.add_argument('-f', action='store', dest='function_call',
                       help='function call')
    parser.add_argument('-m', action='store', dest='module',
                       help='module')

    # v verbosity
    # g resfesh from git 
    # e errrors (-1, 0, not show)
    # TODO if module.test does not exist dont record
    
    args = parser.parse_args()
    
    print args.function_call
    print 'Done'
    test(args)
