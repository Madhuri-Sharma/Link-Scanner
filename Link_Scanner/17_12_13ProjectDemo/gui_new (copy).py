from Tkinter import *
from depth_class import *
#####################
import time
import threading
try: import tkinter
except ImportError:
    import Tkinter as tkinter
    import ttk
    import Queue as queue
else:
    from tkinter import ttk
    import queue
import time
import subprocess
import os
########################
class Application(Frame):
    def say_hi(self):
        print "call here fuction of search"

    def createWidgets(self):
        self.label1 = Label( self, text="Enter URL")
        self.E1 = Entry(self, bd =5)
        self.label1.pack()
        self.E1.pack()
        self.submit = Button(self, text ="Submit", command =self.start)
        self.submit.pack(side =BOTTOM)
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "Black"
        self.QUIT["command"] =  self.quit

        self.QUIT.pack({"side": "left"})

        self.hi_there = Button(self)
        self.hi_there["text"] = "Report"
        self.hi_there["command"] = self.viewReport

        self.hi_there.pack({"side": "left"})
        ###########################
        self.int_var = tkinter.IntVar()
        progbar = ttk.Progressbar(self, maximum=4)
        # associate self.int_var with the progress value
        progbar['variable'] = self.int_var
        

        self.label = ttk.Label(self, text='0/5')
        progbar.pack()
        self.label.pack()
        #########################

        
        

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
    def viewReport(self):
        import platform
        if platform.system() =='Windows':
            #pdf = "C:\Documents and Settings\Administrator\Desktop\MMW_BM_report.pdf"
            pdf="tuto3.pdf"
            acrobatPath = r'C:\Program Files\Adobe\Reader 8.0\Reader\AcroRd32.exe'
            subprocess.Popen("%s %s" % (acrobatPath, pdf))
        if platform.system() =='Linux':
            pdf = "C:\Documents and Settings\Administrator\Desktop\MMW_BM_report.pdf"
            acrobatPath = r'C:\Program Files\Adobe\Reader 8.0\Reader\AcroRd32.exe'
            subprocess.Popen("%s %s" % (acrobatPath, pdf))
	    #evince MMW_BM_report.pdf
        

    def show_report(self):
        
        i=0
     
        while i<len(self.__l.result):
            r=[]
            r=self.__l.result[i]
            for x in range(len(r)):
                self.l5["text"]=r[x]
            self.l5.pack()
        i=i+1
        
        
        
    def start(self):
        url = self.E1.get()
        
        self.submit['state']='disable'
        self.int_var.set(0) # empty the Progressbar
        self.label['text'] = '0/5'
        # create then start a secondary thread to run arbitrary()
        #self.__l=linkScan(url,4)
        k = keepSmile(url)
        self.secondary_thread = threading.Thread(target=k.arbitrary)
        self.secondary_thread.start()
        # check the Queue in 50ms
        self.after(50, self.check_que)
        
        #self.__l=linkScan(url,4)
        #self.__l.linkScanner()
    def check_que(self):
        while True:
            global que
            try: x = que.get_nowait()
            except queue.Empty:
                self.after(25, self.check_que)
                break
            else: # continue from the try suite
                if x==1:
                    level="link Extracter"
                if x==2:
                    level="link checker"
                if x==3:
                    level="Pattern Matcher"
                if x==4:
                    level="Generate report"
                if x==5:
                    level="complete"
                labelText = level+'{}/5'.format(x)
                self.label['text'] = labelText
                self.int_var.set(x)
                if x == 5:
                    self.submit['state'] = 'normal'
                    break
        
        
    '''
    def getURL(self):
        url = self.E1.get()
        start_time = time.time()
	start_clock=time.clock()
	#block = "This is a simple example"
	#print "This is an example search on the string \"", block, "\"."
	#l=["ple","example","simple"," imple"]
	pat=["http:","https:","<script>",".exe"]
	#for i in l:
	#	print i,"  :", BMSearch(block, i)
	L2 = get_all_links(get_page(url))
	index=[] # to store the links which contains the pattern
	broken = [] # to store the links which are broken
	for r in L2:
	    for p in pat:
		print r,": ",BMSearch(r,p)
		if BMSearch(r,p)!=-1:
		     add_to_index(index,p,r)
	for br in L2:
	    lc = LinkChecker(br)
	    if lc.check():
   		 print "Check is sussessful"
   		 if not lc.follow():
       		 	print("there were problems")
       		 	print("\n".join(lc.failed))
        		print("\n".join(lc.other))
    		 else:
        		print("website OK")
	    else:
		 broken.append(br)
    		 print("cannot open website or homepage is not html")
		
	print "----------------------------------------------------------------------------"	
	print index
	print"-----------------------------------------------------------------------------"
	print pprint(index)
	print "CPU Time:"
	print time.clock()-start_clock, "seconds"
	print "Execution Time:"
	print time.time() - start_time, "seconds"
	print "broken links:"
	print broken
	return url
    '''
from PDF import *
class keepSmile:
    def __init__(self,url):
        self.url = url
        
        
    def func_a(self):
        time.sleep(1) # simulate some work
    def func_b(self):
        time.sleep(0.3)
    def func_c(self):
        time.sleep(0.9)
    def func_d(self):
        i=0
        time.sleep(0.6)
        while i < 1000:
            i=i+1
            print i
    def GenrateReport(self):
        title='Link Scanner -- Finding Broken links and Patterns'
        PDFInput = []
        PDFInput = self.__l.putResult()
        self.Report = PDF()
        self.Report.setdata(PDFInput,self.ExeTime,self.Processortime,title,'komal')
        #self.Report.set_title(title)
        #self.Report.set_author('Jules Verne')
        self.Report.print_chapter()
        self.Report.output('tuto3.pdf','F')
        self.Report.displaydata()
    def arbitrary(self):
        start_time = time.time()
        start_clock=time.clock()
        self.__l=linkScan(self.url,4)
        self.__l.crawl()
        que.put(1)
        self.__l.scan()
        que.put(2)
        self.__l.pattern_search()
        que.put(3)
        self.ExeTime= time.time() - start_time,"seconds"
        self.Processortime=time.clock()-start_clock,"seconds"
        self.GenrateReport()
        que.put(4)
        self.func_d()
        que.put(5)
        print self.__l.putResult()
        
##############
que = queue.Queue()
#############
root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()
#http://www.ittc.ku.edu/~niehaus/classes/448-s04/448-standard/simple_gui_examples/
