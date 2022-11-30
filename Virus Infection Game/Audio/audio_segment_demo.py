#audio lecture
#audio segment demo
#wrapper around pydub libary
#written by Tara Stentz (tstentz)

from pydub import AudioSegment

#changes a file into a sound object
def soundFromFile(filename):
    return AudioSegment.from_wav(filename)

#writes a sound object into a file
def exportToFile(sound, filename):
    sound.export(filename, format="wav")
    return filename

#takes in a file and returns the length
def getLen(filename):
    return len(soundFromFile(filename))

#can take in positive and negative amounts
def changeVolume(filename, amount, resultFilename):
    sound = soundFromFile(filename)
    newSound = sound + amount
    return exportToFile(newSound, resultFilename)

#adds two sound files together
def concatNotes(filename1, filename2, resultFilename):
    sound1 = soundFromFile(filename1)
    sound2 = soundFromFile(filename2)
    return exportToFile(sound1 + sound2, resultFilename)

#repeats a sound a given amount of times
def repeatSound(filename, amount, resultFilename):
    sound = soundFromFile(filename)
    return exportToFile(sound * amount, resultFilename)

#gets a slice of a sound, start and end times are in milliseconds
def getSection(filename, start, end, resultFilename):
    sound = soundFromFile(filename)
    newSound = sound[start:end]
    return exportToFile(newSound, resultFilename)


#basic code frame work inspired by http://pydub.com
#and http://stackoverflow.com/questions/4039158/mixing-two-audio-files-together-with-python

#(*args) means you can put in as many sound file arguments as you like
#for example: overlayFile('result.wav', '15.wav', '112.wav')
def overlayFiles(resultFilename, *args):
    sound1 = AudioSegment.from_wav(args[0])
    if(len(args) > 1):
        for index in range(1, len(args)):
            sound2 = AudioSegment.from_wav(args[index])
            sound1 = sound1.overlay(sound2)
    return exportToFile(sound1, resultFilename)




