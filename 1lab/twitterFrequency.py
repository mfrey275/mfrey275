# coding: utf-8

import sys
import re
from collections import defaultdict
from math import log
import random

## EXTRA CREDIT ##
def rand(hist):
	rnum = random.uniform(0,1)
	for x in hist:  
		rnum -= hist[x]
		if rnum < 0: return x
	return x

## PART 1 ##
def clean(line):
	#use the following syntax for all your replacements so that unicode is properly treated
	#line = re.sub(u'replace_regexp','with_regexp',line)
        line = re.sub(u"@\w+", "@@@", line) #replace twitter handle with "@@@"
        line = re.sub(u"https://t.co/\w+", "www", line) #replace url with "www"
        line = re.sub(u"#\w+", "###", line) #replace hastags with "###"
        line = re.sub(u"[^\w\s\@\#]+|[^\w\s\@\#]+|--|…", " ", line) #remove punctuation
        line = re.sub(u"\s+$|^\s+", "", line) #remove leading & trailing whitespace
        line = line.lower()
        return line

## PART 2 ##
def normalize(hist):
	# this is a void function that normalizes the counts in hist
	# given a dictionary of word-frequency pairs, this function modifies the frequencies so that they sum to 1
	values = hist.values()
	total = sum(values)
	for key, value in hist.copy().items():
                hist.update({key:value/total})

def get_freqs(f):
	wordfreqs = defaultdict(lambda: 0) #creates empty dictionary
	lenfreqs = defaultdict(lambda: 0) #this becomes a dict of frequency distribution of each line

	for line in f.readlines():
		line = clean(line)
		words = re.split(u'\s+|\s+[-]+\s+', line)
		lenfreqs[len(words)]+=1
		for word in words:
			wordfreqs[word.encode('utf8')]+=1
	
	normalize(wordfreqs)
	normalize(lenfreqs)
	return (wordfreqs,lenfreqs)

## PART 3 ##
def save_histogram(hist,filename):
	outfilename = re.sub("\.txt$","_out.txt",filename)
	outfile = open(outfilename,'w')
	print("Printing Histogram for", filename, "to", outfilename)
	rank = 1
	for word, count in sorted(hist.items(), key = lambda pair: pair[1], reverse = True):
                logrank = log(rank)
                logfreq = log(count)
                output = "%-13.6f\t%s\t%f\t%f\n" % (count,word,logfreq,logrank) #inconsistent use of tabs and spaces in indentation
                outfile.write(output)
                rank += 1

## PART 4 ##
	# return a list of the N most frequent words in hist
def get_top(hist,N):
        top_dict = sorted(hist.items(), key = lambda pair: pair[1], reverse = True)
        top_dict = top_dict[0:N]
        top_list = []
        for ele in top_dict:
                top_list.append(ele[0])
        #for i, w in enumerate(top_list):
                #data = "{:<4}-- {}".format(i,w)
                #print(data)
        return top_list

def filter(hist,stop):
        for word in stop:
                if word in hist: hist.pop(word)
        normalize(hist)

def main():
	file1 = open(sys.argv[1],encoding="utf8")
	(wordf1, lenf1) = get_freqs(file1)
	stopwords = get_top(wordf1, 200)
	save_histogram(wordf1,sys.argv[1])
	
	for fn in sys.argv[2:]:
		file = open(fn,encoding="utf8")
		(wordfreqs, lenfreqs) = get_freqs(file)
		filter(wordfreqs, stopwords)
		save_histogram(wordfreqs,fn)

		'''
		## EXTRA CREDIT ##
		print("Printing random tweets from",fn)
		for x in range(5):
			n = rand(lenfreqs) #creates an array of specific shape and fills it with random values
			print(n, "random words:")
			for i in range(n):
				print(' ',rand(wordfreqs), end='')
			print()
		'''

## This is special syntax that tells python what to do (call main(), in this case) if this  script is called directly
## this gives us the flexibility so that we could also import this python code in another script and use the functions
## we defined here
if __name__ == "__main__":
    main()
