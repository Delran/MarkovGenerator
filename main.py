# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 19:26:39 2020

@author: Tibère Borel
"""

from markovgenerator import MarkovGenerator

def printStrList( strList ):
    print("--- Printing list :")
    if isinstance( strList, list ):
        for string in strList:
            print(string)
    print("--- End list --- \n")


def main():

    csvPath = 'communes-01012019.csv'
    depth = 10
    maxMarkovLength = 50
        
    toPrint = 20
    
    #Creating the generator from csv file
    generator = MarkovGenerator( csvPath, depth, maxMarkovLength )

    #Getting a single random string
    print( generator.getMarkovString() )

    #Getting random strings and priting them
    printStrList( generator.getMarkovList( toPrint ) )
    
    #Changing algorithm depth
    generator.changeDepth(5)
    
    printStrList( generator.getMarkovList( toPrint ) )
    
    #Reverting to previous depth, no reloading !
    generator.changeDepth( depth )
    
    printStrList( generator.getMarkovList( toPrint ) )

    

if __name__ == "__main__":
    main()
