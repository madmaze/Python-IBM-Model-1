#!/usr/bin/env python
#http://www-rohan.sdsu.edu/~gawron/mt_plus/mt/course_core/lectures/assignment_five.pdf
#http://www.cs.jhu.edu/~alopez/papers/model1-note.pdf
#http://www.inf.ed.ac.uk/teaching/courses/mt/assignments/assignment2.pdf
#http://www.mt-archive.info/MTMarathon-2010-Lambert-ppt.pdf
import optparse
import sys
from collections import defaultdict
from memorymonitor import MemoryMonitor

memory_mon = MemoryMonitor('madmaze')
startMemory = memory_mon.usage()

def trainfw(itr):
	x=0
	print "Memory increased by", int(memory_mon.usage()) - startMemory
	
	for (n, (f, e)) in enumerate(bitext):
		if n%1000==0:
			print "loading...",n
		for f_i in set(f):
			f_total[f_i] = 0.0

			for e_j in set(e):
				ef_count[(e_j,f_i)] = 0.0
				t_ef[(e_j,f_i)]=1.0

		
	x=0
	print "Memory increased by", int(memory_mon.usage()) - startMemory
	
	for (f, e) in bitext:
			for f_i in set(f): 
				for e_j in set(e):
					oldtef.append(1.0)
					
	print "Memory increased by", int(memory_mon.usage()) - startMemory
	
	print "len tef",len(t_ef)
	print "len oldtef",len(oldtef)
	
	while 0.00001< compT_EF(oldtef, t_ef, x) and x!=itr:
		for f in set(f_total):
			f_total[f]=0.0
		for (e,f) in set(ef_count):
			ef_count[(e,f)]=0.0
			
		for (f,e) in bitext:
			for e_j in set(e):
				se_total=0.0
				for f_i in set(f):
					se_total += t_ef[(e_j,f_i)]  * len(e)
				for f_i in set(f):
					ef_count[(e_j,f_i)] += (t_ef[(e_j,f_i)] * len(e) * len(f))/se_total
					f_total[f_i] += (t_ef[(e_j,f_i)] * len(e) * len(f))/se_total

		print "before dict", x	
		#print len(dict_eng)
		y=0
					
		membefor = int(memory_mon.usage())

		for e_j,f_i in set(t_ef):
			t_ef[(e_j,f_i)] = ef_count[(e_j,f_i)]/f_total[f_i]
		
		
		print "Memory DELTA>>", int(memory_mon.usage()) - membefor
				
		x+=1
		writeOutput('inter-'+str(x))
			
	writeOutput('final-'+str(x))


def compT_EF(t1, t2, x):
	# compute convergence only every 5 itr
	if x == 0:
		return 1
	global oldtef
	global t_ef
	tot=0.0
	cnt=0
	c2=0
	print "len tef",len(t_ef)
	print "len oldtef",len(oldtef)
	for s in t_ef:
		if t_ef[s] > 0:
			if c2<5:
				print s, c2, oldtef[cnt], t_ef[s], oldtef[cnt]-t_ef[s]
			tot+=abs(oldtef[cnt]-t_ef[s])
			c2+=1
		cnt+=1
		
	print "conv?:", tot/c2
	
	oldtef=[]
	for e in t_ef:
		oldtef.append(t_ef[e])
	return (tot/c2)
	
def writeOutput(x):
	global bitext
	global t_ef
	outfile = open(opts.out+'.1.'+x+'.a','w') 
	print "printing to file..."
	for (f, e) in bitext:
	  for (i, f_i) in enumerate(f): 
	    for (j, e_j) in enumerate(e):
	      if t_ef[(e_j,f_i)] >= opts.threshold:
		#sys.stdout.write("%i-%i " % (i,j))
		outfile.write("%i-%i " % (i,j))
	  #sys.stdout.write("\n")
	  outfile.write("\n")
	outfile.close()
	return

def MaxLikelyEst():
	global bitext
	global fe_count
	global e_count
	global p_fe
	for (n, (f, e)) in enumerate(bitext):
		for f_i in f:
			for e_j in e:
				fe_count[(f_i,e_j)] += 1
				e_count[(e_j] += 1
	for (f,e) in fe_count:
		p_fe[(f,e)] = fe_count[(f,e)]/e_count[e]
def ExpMax(MaxItr):
	k=0
	#initialize 0?
	while k < MaxItr:
		
def doThings():
	MaxLikelyEst()
	ExpMax()

if __name__ == "__main__":
	optparser = optparse.OptionParser()
	
	optparser.add_option("-d", "--data", dest="train", default="data/hansards", help="Data filename prefix (default=data)")
	optparser.add_option("-e", "--english", dest="english", default="e", help="Suffix of English filename (default=e)")
	optparser.add_option("-o", "--out", dest="out", default="m1.", help="output prefid (default=m1.)")
	optparser.add_option("-f", "--french", dest="french", default="f", help="Suffix of French filename (default=f)")
	optparser.add_option("-t", "--threshold", dest="threshold", default=0.5, type="float", help="Threshold for aligning with Dice's coefficient (default=0.5)")
	optparser.add_option("-n", "--num_sentences", dest="num_sents", default=sys.maxint, type="int", help="Number of sentences to use for training and alignment")
	(opts, _) = optparser.parse_args()
	
	f_data = "%s.%s" % (opts.train, opts.french)
	e_data = "%s.%s" % (opts.train, opts.english)
	bitext = [[sentence.strip().split() for sentence in pair] for pair in zip(open(f_data), open(e_data))[:opts.num_sents]]
	#se_total = defaultdict(float)
	f_total = defaultdict(float)
	ef_count = defaultdict(float)
	
	#reversing
	e_total = defaultdict(float)
	fe_count = defaultdict(float)
	
	#global probs
	t_ef = defaultdict(float)
	
	dict_eng=defaultdict(int)
	dict_fr=defaultdict(int)
	oldtef=[]
	
	
	doThings()
