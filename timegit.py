# timegit

import os
import sys
import time
import ConfigParser
import argparse
import logging
#import matplotlib

class TimeGit(object):
    def __init__(self,args,config_file_name):
        self.loggerTimeGit = logging.getLogger('TimeGit')
        self.loggerTimeGit.debug('__init__')        
        
        # read config info   
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
        
        self.loggerTimeGit.debug('config_file_name: %s' %config_file_name) 
        self.loggerTimeGit.debug('git_repo: %s' %self.git_repo) 
        self.loggerTimeGit.debug('data_dir: %s' %self.data_dir)
        self.loggerTimeGit.debug('test_module: %s' %self.test_module) 
        self.loggerTimeGit.debug('test_function: %s' %self.test_function) 


    def _prep(self):
        self.loggerTimeGit.debug('_prep') 
        # (make) cd to data dir           
        if not os.path.exists(self.data_dir):
            os.mkdir(self.data_dir)
        os.chdir(self.data_dir)
       
        repo_path,fileExtension = os.path.splitext(self.git_repo)   
        self.repo_name = repo_path.split('/')[-1] 
        self.loggerTimeGit.debug('repo_name: %s' %self.repo_name)      
        data_dir = os.path.join(self.data_dir,self.repo_name +'_data')
        
        if not os.path.isdir(data_dir):
            os.mkdir(data_dir) 
        os.chdir(data_dir)
                
        
    def _getdatafromgithub(self):
        self.loggerTimeGit.debug('_getdatafromgithub')
        #if not os.path.isfile(self.repo_name):     
        cmd = r"git clone %s" %self.git_repo
        self.loggerTimeGit.debug('%s' %cmd)
        
        if os.path.isdir(self.repo_name):
            self.loggerTimeGit.info('dir for (%s) alread exists' %self.repo_name)            
        else:
            try:
                x = os.system(cmd)
                if x:
                    self.loggerTimeGit.warning('rtn %s' %x)  
            
            except Exception, e:
                self.loggerTimeGit.critical( 'Error running %s: %s' %(cmd, str(e)))
                self.loggerTimeGit.exception('zzz')
       
   
    def _getgitcommitids(self):
        self.loggerTimeGit.debug('_getgitcommitids')
        
        # if file commits.txt does not exist       
        commits_file = '../commits.txt'
        os.chdir(self.repo_name)
        
        if os.path.isfile(commits_file):
            self.loggerTimeGit.info('commits file exits')
        else:
            cmd = r"git log --pretty=format:'%h %ad | %s%d [%an]' --graph --date=short > " + commits_file
            self.loggerTimeGit.debug(cmd)
            os.system(cmd)         
        
        # use with
        f = open(commits_file)
        commit_ids = []
        for count, line in enumerate(f):
            rev = line.split(' ')[1] 
            #print rev
            commit_ids.append(rev)
        f.close()      
        commit_ids.reverse()
        return commit_ids

              
    def _runtestfunction(self, commit_ids):
        self.loggerTimeGit.debug('_runtestfunction')
        # add data dir to sys.path ??        
        sys.path.append('.')
          
        times = [0.0,] # start from origin
        
          # for each repo version
        for count, commit_id in enumerate(commit_ids):        
            #if count == 3: break
            self.loggerTimeGit.info('%s commit_id: %s ........' %(count,commit_id))
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
        self.loggerTimeGit.debug('_show')
        # display results
        # unfortunate but must import here
        import matplotlib.pyplot as plt
        self.loggerTimeGit.info( 'times: %s' %times)       
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
        #self._show(times)
                    

# --------------------

def run(args):
    if args.config_file:
        config_file_name = args.config_file
    else:
        config_file_name = 'config.cfg'
    myTimeGit = TimeGit(args,config_file_name)
    myTimeGit.run()   
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Time git repos')
    # basic args
    parser.add_argument('-c', action='store', dest='config_file',
                    help='config file')
    parser.add_argument('-f', action='store', dest='function_call',
                       help='function call')
    parser.add_argument('-m', action='store', dest='module',
                       help='module')
    # optional args
    parser.add_argument('-v', action='store', dest='verbosity',
                         help='verbosity: debug, info, warning, error, critical')
    
    # advanced args
    

    # g resfesh from git 
    # (g gui) may be diff module due to wx import
    # e errrors (-1, 0, not show)
    # TODO if module.test does not exist dont record
    # r refresh
    #(s store times)
    #(a average times)

    
    args = parser.parse_args()

    print 'Verbosity', args.verbosity
    LOG_FILENAME = 'timegit.log'
    LEVELS = { 'debug':logging.DEBUG,
                'info':logging.INFO,
                'warning':logging.WARNING,
                'error':logging.ERROR,
                'critical':logging.CRITICAL,
                }    
    
    #g_logger = logging.getLogger('TimeGitLogger')
    level_name = args.verbosity
    level = LEVELS.get(level_name, logging.NOTSET)
    
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%y-%m-%d %H:%M:%S',
                        filename='timegit.log',
                        filemode='w') 
    
    
    # define a Handler which writes messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(level)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)
    
    
    
    '''
    # Now, we can log to the root logger, or any other logger. First the root...
    logging.info('Jackdaws love my big sphinx of quartz.')
    
    # Now, define a couple of other loggers which might represent areas in your
    # application:
    
    logger1 = logging.getLogger('myapp.area1')
    logger2 = logging.getLogger('myapp.area2')
    
    logger1.debug('Quick zephyrs blow, vexing daft Jim.')
    logger1.info('How quickly daft jumping zebras vex.')
    logger2.warning('Jail zesty vixen who grabbed pay from quack.')
    logger2.error('The five boxing wizards jump quickly.')       
    
    
    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical error message')    
    '''
    
    run(args)
    logging.info('Done')
    
