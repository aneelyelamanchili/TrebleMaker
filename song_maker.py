'''
Created by: Brian Richard, Jonathan Zhang, Aneel Yelamanchili
on July 28 2014
bcr53@cornell.edu, jyz22@cornell.edu, ajy35@cornell.edu
'''
import random
from MidiFile import MIDIFile
#imports random library for various random selections
#imports midi for music "jazz"

class Melody:
    '''this class and its methods quasi-randomly generate notes in a major scale as a line of melody'''
    
    def __init__(self, sect = 1, notes = []):
        self.notes = notes
        self.melloc = 0
        self.sections = sect
        self.instrs = dict([('piano',0), ('harpsichord',6), ('glock',9), ('vibes',11), #dictionary of instruments that we could use
                            ('marimba',12), ('organ',19), ('guitar',24), ('bass',32),
                            ('violin',40), ('cello',42), ('harp',46), ('timps',47),
                            ('voice',54), ('trumpet',56), ('tuba',58), ('horn',60),
                            ('alto sax', 65), ('oboe',68), ('bassoon',70), ('clarinet',71),
                            ('flute',73), ('recorder',74), ('bottle',75), ('whistle',78),
                            ('fifths',96), ('koto',107),
                            ('bagpipe',109), ('taiko',116), ('toms',117), ('breath',121),
                            ('bird',123), ('applause',126)])
        
    def buildNotes(self):
        for i in range(self.sections):
            randnum = random.randint(55, 67)   #picks a starting key on the piano that is towards the center
            if randnum == 57:                 #the key 57 does not sound too grand so we switched to a middle C
                randnum = 60
            elif randnum == 66:               # the key 66 doesn't sound too great either
                randnum = 65
            x = randnum
            for j in range(16):               #creates sections with a length of 16 beats
                randjump = random.choice([-7, -5, 0, 2, 2, 2, 4, 5, 7, 9, 11])    #randomly picks a jump which is within the octave and will not sound horendous
                #this note is what is played in the music
                if randjump == 57:
                    randjump = 60
                if randjump == 66:
                    randjump = 65
                if j == 0:
                    tempnote = (0, 0, randnum, self.melloc, 1, 100)
                    #0 is track, 0 is channel, 1 is length, 100 is volume percentage
                    self.melloc += 1    #1 is length
                    self.notes.append(tempnote)
                else:
                    randnum = randnum + randjump
                    #print('new note' + str(randnum))    this was used to check if the note changed
                    tempnote = (0, 0, randnum, self.melloc, 1, 100)          #creates a tuple with the values that are used in the addNote function
                    randnum = x  #resets randnum to the value which it started with
                    #print('did it change' + str(randnum))     used to see if the initial value was changing
                    self.melloc = int(self.melloc) + 1           #updates the melody location
                    self.notes.append(tempnote)        #appends the tuple to a list of all the tuples in the melody
                splitchoice = random.choice([0, 0, 0, 1])          #used to randomly select if a note  should be split into smaller intervals
                if splitchoice == 1:
                    #as you can see, it is much more likely that it will not split
                    self.melloc = self.melloc - 1       #subtracts one from the melody location/length
                    self.notes.pop()     #removes the last note
                    summation = 0
                    #count = 0
                    choices = [.25, .5]         #options for eigth and sixteenth note
                    while summation < 1:        #runs until the notes created add up to one beat or a quarter note
                        randjump = random.choice([ -5, 0, 2, 2, 2, 4, 5])   #again chooses a random length to add to to the note that will still sound pleasant
                        randnum = randnum + randjump          
                        intervalchoice = random.choice(choices)    #chooses between the lengths prescribed
                        #count += 1
                        summation = summation + intervalchoice    #adds the length of the note to the sum (which cannot exceed 1)
                        if summation > .5 and .5 in choices:     #if the note length is greater than .5, i.e. it is .75, it restricts the note options to a 1/16 note
                            choices.remove(.5)
                        tempnote = (0, 0, randnum, self.melloc, intervalchoice, 100)      #creates a tuple with the the current location, and length generated
                        randnum = x      #resets the randnum
                        self.melloc = self.melloc + intervalchoice    #updates the locaiton in the melody
                        self.notes.append(tempnote)      #adds the note (tuple) to the list of notes
                        
    def change_instr(self, instr, midfile):  #defining setting the instrument
        midfile.addProgramChange(0, 0, self.melloc, instr)

    def buildMelody(self, midfile):
        self.change_instr(self.instrs['piano'], midfile)  #set instrument here
        for i in range(len(self.notes)): #self.notes is a list of tuples, each tuple contains the attributes of a note
            midfile.addNote(self.notes[i][0], self.notes[i][1], self.notes[i][2], self.notes[i][3], self.notes[i][4], self.notes[i][5])
            #note, no pun intended, that the values that are being inputed are the equivalent six value that were stored in the tuple
        midfile.addNote(0, 0, self.notes[-16][2], self.melloc, 4, 100)
        #adds a nice whole note to the end to make the song end nicely, the note is the same as the randnum that was selected for the last section
        #building a melody into a midifile by inputting each note that was stored in the list [self.notes]

class Harmony:
    '''This class builds harmonic lines based off of the notes in the melody built above'''
    
    def __init__(self, mel, notes = []):
        self.refmel = mel  #import melody to write harmony off of
        self.notes = notes #notes in harmony
        self.harloc = 0

    def buildNotes(self):
        self.harloc = 0      #resetting to beginning of music staff for every extra harmony
        for i in range(len(self.refmel.notes)): #building harmony length based off of length of melody
            randjump = random.choice([-5, -5, -8, 4, 4, -2])
            templist = []
            lastint = 0
            for j in range(len(self.refmel.notes)):
                #checks every note in the melody
                if int(self.refmel.notes[i][3])%2 == 0 and int(self.refmel.notes[i][2]) != lastint:
                    #if the current number is divisible by two, then it adds a harmony note, also since taking the int of a decimal trunkates the value
                    #so it checks to see if the value its checking is the same as the last one
                    randnum = [self.refmel.notes[i][2] + randjump, self.refmel.notes[i][3]]
                    #creates a list with the note value and the note length
                    templist.append(randnum)     #appends the list to the templist that is used later
                    lastint = int(self.refmel.notes[i][2])
            for j in range(len(templist)):
                tempnote = (0, 1, templist[j][0], templist[j][1], 2, 65)
                self.notes.append(tempnote)
                self.harloc += 1
        
    def buildHarmony(self, midfile):
        for i in range(len(self.notes)):
            midfile.addNote(self.notes[i][0], self.notes[i][1], self.notes[i][2], self.notes[i][3], self.notes[i][4], self.notes[i][5])
        #midfile.addNote(0, 1, self.notes[-16][2], self.harloc, 4, 100)
