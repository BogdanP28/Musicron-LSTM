
from mido import MidiFile, MidiTrack, Message
from mido.midifiles import MetaMessage
from os import listdir
import os
import numpy as np
import pandas as pd
import shutil

def getNoteCurrentOnOf(mid, comp_factor, transpose, type):
    print('getNoteCurrentOnOf')
    getNoteCurrentOnOf = []
    velocity =[]
    for track in mid.tracks:
        if(track.name==type):
            current_time = 0
            for message in track:
                    if not isinstance(message, MetaMessage):
                        current_time += int(message.time/comp_factor)
                        bol = False
                        if (message.type == 'note_on'):
                            if(message.velocity!=0):
                                note_onoff = 1
                                bol = True
                            else:
                                note_onoff = 0
                                bol = True
                        if (message.type == 'note_off'):
                            note_onoff = 0
                            bol = True
                        if (message.type == 'velocity'):
                            print("here")
                            
                        if(bol==True):
                            getNoteCurrentOnOf.append([message.note+(12-transpose), current_time, note_onoff])
                            velocity.append(message.velocity)    
    return getNoteCurrentOnOf

def getNoteStartLength(getNoteCurrentOnOf):
    print(getNoteStartLength)
    note_on_length_array = []
    first_time = False
    aux = 0
    b = [x[1] for x in getNoteCurrentOnOf]
    aux = b[0]
    if aux != 0:
        first_time = True

    for i, message in enumerate(getNoteCurrentOnOf):
        if message[2] == 1: 
            start_time = message[1]
            for event in getNoteCurrentOnOf[i:]: 
                if event[0] == message[0] and event[2] == 0:
                    length = event[1] - start_time
                    break
                
            note_on_length_array.append([message[0], start_time, length])

    if first_time == True:
        i = 0
        for note,timer,length in note_on_length_array:
            timer = timer - aux
            note_on_length_array[i]=[note, timer, length]
            i = i+1
    return note_on_length_array

def create_nparray(piano_roll2: list[int], size:tuple[int]) -> np.ndarray:
    tester = np.zeros(shape=size)
    for idx, item in enumerate(piano_roll2):
        tester[idx] = item
    return tester

def createMidiFromPianoRoll(n,piano_roll, directory, mel_test_file, threshold, res_factor=1):
    tmp_pr = []
    #cv2 = list(map(list,zip(*piano_roll)))
    out =  np.concatenate(piano_roll).tolist()
    #for item in piano_roll:
    #    tmp_pr.append(*item)
    '''
    piano_roll2 = np.array(piano_roll[0])
    tmp1 = np.array(piano_roll[1])
    piano_roll2 = np.concatenate((piano_roll2, tmp1))
    '''
    from random import randint
        #print('here')
    piano_roll = create_nparray(out, (len(out), 48))
    ticks_per_beat = int(n)
    mid = MidiFile(type=0, ticks_per_beat=ticks_per_beat)
    track = MidiTrack()
    mid.tracks.append(track)
    mid_files = []
    delta_times = [0]
    for k in range(piano_roll.shape[1]):#initial starting values
        if piano_roll[0, k].any() == 1:
            track.append(Message('note_on', note=k+33, velocity=randint(50,100), time=0))
            delta_times.append(0)
            aux = k
    counter = 0  
    for j in range(piano_roll.shape[0]-1):#all values between first and last one
        #set_note = 0 #Check, if for the current timestep a note has already been changed (set to note_on or note_off)
       
        for k in range(piano_roll.shape[1]):
            if (piano_roll[j+1, k] == 1 and piano_roll[j, k] == 0) or (piano_roll[j+1, k] == 0 and piano_roll[j, k] == 1):#only do something if note_on or note_off are to be set
                #if set_note == 0:
                time = j+1 - sum(delta_times)          
                delta_times.append(time)
                counter = counter + 1
                #else:
                    #time = 0
                #print(piano_roll[j,k])
                if piano_roll[j+1, k] == 1 and piano_roll[j, k] == 0:
                    set_note = 1
                    track.append(Message('note_on', note=k+33, velocity=randint(50,100), time=time))
 
                if piano_roll[j+1, k] == 0 and piano_roll[j, k] == 1:
                    set_note=1
                    track.append(Message('note_off', note=k+33, velocity=0, time=time))
           
                           
    mid.save('%s//%s_%s.mid' %(directory, mel_test_file, threshold))
    mid_files.append('%s.mid' %(mel_test_file))

track = MidiTrack()
print('here')