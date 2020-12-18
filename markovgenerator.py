# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 09:08:26 2020

@author: Tibère Borel
"""
import csv
import random

'''
Random French towns name generation using Makrov algorithm

This generator has been stress tested with depth up to ten
It should be able to withstand any given depth,
Be aware that the algorithm will not use names with length
inferior to the given depth when populating occurences maps

It supports multiple loaded depths without reloading already
loaded depths.

Use changeDepth(depth) to change the depth after the creation
of the generator

Use getMarkovString() to generate a single random string

Use getMarkovString() to generate a list of random strings

Acces MarkovGenerator::maxLengeth to change the maximum length
of the random strings
'''

#-----------------------------------------------------------------#
#                        Markov Generator                         #
#-----------------------------------------------------------------#

class MarkovGenerator:

    # _csvPath   -> string : path to the csv file containing the town names
    # _depth     ->    int : depth used for markov algorithm
    # _maxLength ->    int : safety, the markov algorithm should stop by itself
    def __init__(self, _csvPath, _depth, _maxLength):

    #Class attributes
    #private
        #Zero initialized
        self.__occurences={}
        self.__totalOccurences={}
        self.__firstStr={}
        self.__totalFirstStr={}
        self.__towns = []
        self.__populatedDepths = []

    #public
        self.maxLength = _maxLength

        #Getting all town names from the CV file
        with open(_csvPath, encoding='UTF-8') as csv_handle:
            reader = csv.reader(csv_handle, delimiter=',')
            for row in reader:
                #Row eight is the name of the town
                town_name = row[8].lower()
                self.__towns.append( town_name )

        #We now can populate occurences maps
        #it will use the now defined self.__depth
        self.changeDepth(_depth)
    # End init ------------------------------


    # Start populateMap ---------------------
    #Populating maps using self.depth
    def __populateMap( self ):

        #New map of starting words for this depth
        self.__firstStr[self.__depth] = {}
        self.__totalFirstStr[self.__depth] = 0

        #Getting depth self.__firstStrMaps into dedicated variables
        self.__firstStrDepth = self.__firstStr[self.__depth]

        #Iterating through each town name
        for word in self.__towns:

            strLen = len(word)

            if strLen < self.__depth:
                continue

            strTmp = word[0:self.__depth]

            if strTmp not in self.__firstStrDepth:
                #Start at 0 as this will be used as an index
                self.__firstStrDepth[strTmp] = 0
            else:
                self.__firstStrDepth[strTmp] += 1
            self.__totalFirstStr[self.__depth] += 1

            #Iterating through each chars of the town name
            for it in range(0, strLen - self.__depth):


                keyStr = word[it:self.__depth+it]

                if keyStr not in self.__occurences:
                    self.__occurences[keyStr] = {}
                    #Start at 0 as this will be used as an index
                    self.__totalOccurences[keyStr] = 0

                strMap = self.__occurences[keyStr]

                nextChar = word[it + self.__depth]

                if nextChar not in strMap:
                    strMap[nextChar] = 0
                else:
                    strMap[nextChar]+= 1

                self.__totalOccurences[keyStr] += 1

            #Keying the last world of size self.__depth with
            #'\0' this will allow us to end prematurely
            #the string generation with a coherent ending
            tmpStr = word[strLen-self.__depth:strLen]
            if tmpStr not in self.__occurences:
                self.__occurences[tmpStr] = {}
                self.__totalOccurences[tmpStr] = 0
            tmpMap = self.__occurences[tmpStr]
            tmpChar = '\0'
            if tmpChar not in tmpMap:
                tmpMap[tmpChar] = 0
            else:
                tmpMap[tmpChar] += 1
            self.__totalOccurences[tmpStr] += 1
    # End populateMap -------------------------


    # Start generateMarkov --------------------
    #Generate the random string
    #Function will use self.depth and self.maxLength
    def __generateMarkov( self ):
        #We get a random word in the starting word pool
        #This will assure that the string starts with something coherent
        markovStr = ""
        rand = random.randrange( 0, self.__totalFirstStr[self.__depth] )
        markovStr += self.getWordAtIndex( rand, self.__firstStr[self.__depth] )

        #Start iterating at depth as the string as already n depth chars
        for i in range( self.__depth, self.maxLength ):

            #Getting the last n = depth char to use as key in the occurences maps
            strCheck = markovStr[i-self.__depth:i]
            #Draw a random number between 0 and the number of occurence of this word
            rand = random.randrange( 0, self.__totalOccurences[strCheck] )
            tmpChar = self.getWordAtIndex( rand, self.__occurences[strCheck] )

            #Getting a '\0' means that the algorithm has chosen to end the string here
            if tmpChar == '\0':
                break
            #Otherwise we continue until maxLength is reached
            markovStr += tmpChar

        return markovStr
    # End generateMarkov ------------------------


    '''
    getWordAtIndex( index, map )

    Get the letter at the given random index
    This works by drawing a random number between
    0 and the total number of any occurences found
    after this letter
    We then iterate through the occurences to find
    the occurence a the random "index"

    Ex :
    Consider and occurence map as follows :
    {'l': 4739, 'a': 2006, 'b': 3432, 'v': 2272 }

    We have a total of 12449 occurences
    If we draw anything between 0 and 4738 then this
    the function will return 'l'
    If we draw anything between 4739 and 6744 then this
    the function will return 'a'

    This functions doesn't know the total number of self.__occurences
    it will return an empty string if the _index is out of range.
    '''
    def getWordAtIndex( self, _index, _inmap ):
        #Iterating through the occurence map
        #_map = dict(sorted(_inmap.items(), key=lambda item: item[1], reverse=True))
        tmp = 0;
        for key in _inmap:
            #increment the number of self.__occurences for this key and continue
            tmp += _inmap[key] + 1

            #If the combined number of self.__occurences we encountered
            #is superior to the index, then we passed it, the kay can be returned
            if tmp >= _index:
                return key


        #Should never be reached
        raise "Reached getWordAtIndex() end"
    # End generateMarkov -----------------------


    # Start changeDepth ------------------------
    #Setter for depth, maps need to be populated with given depth
    def changeDepth( self, _depth ):
        self.__depth = _depth

        #Only populate if necessary
        if _depth not in self.__populatedDepths:
            self.__populateMap()
            self.__populatedDepths.append(_depth)
    # End changeDepth --------------------------
    
    
    # Start getMarkovString --------------------
    #Generate and returns a single random string
    def getMarkovString( self ):

        markov = self.__generateMarkov()
        #We don't want a name that already exists
        while markov in self.__towns:
            markov = self.__generateMarkov()
        #Capitalize for flair
        markov = markov.capitalize()
        return markov
    # End getMarkovString ----------------------


    # Start getMarkovList ----------------------
    #Generate and returns a list of _nb random strings
    def getMarkovList( self, _nb ):

        markovs = []
        for i in range(0, _nb):
            markovs.append( self.getMarkovString() )
        return markovs
    # End getMarkovList -----------------------
    
#-----------------------------------------------------------------#
#                      End Markov Generator                       #
#-----------------------------------------------------------------#