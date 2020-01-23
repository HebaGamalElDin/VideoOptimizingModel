# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 04:44:41 2020

@author: HebaGamalElDin
"""
#Import libraries
from ffmpy import FFmpeg
import subprocess
import shlex
import json

#Class Definition
class video_optimize:
    def __init__(self, input_file):
        self.video_in = input_file
        #Standardizing  output Video Format
        self.video_out = input_file.rsplit('.',1)[0]  + 'out.MP4'
    # get resolution of the input video file
    def findVideoResolution(self):
        cmd = "ffprobe -v error -print_format json -show_streams"
        args = shlex.split(cmd)
        args.append(self.video_in)
        # run the ffprobe process, decode stdout into utf-8  JSON File
        ffprobeOutput = subprocess.check_output(args).decode('utf-8')
        ffprobeOutput = json.loads(ffprobeOutput)
        # find height and width
        precent = 75
        height = ffprobeOutput['streams'][0]['height'] 
        width = ffprobeOutput['streams'][0]['width']
        print(width, height)
        #Return Optimized  Video Resolution
        return width* precent /100 , height* precent /100 
     #Optimization FFmpeg Command  method   
    def  optimize(self):
        out_width, out_height = self.findVideoResolution()
        resolution =  str(out_width) + ':'  + str(out_height)
        input_fit  = {self.video_in:None}
        output_fit = {self.video_out:'-n  -preset slow -vcodec libx265 -maxrate 640k  -bufsize 10M -crf 24 -vf scale=%s' %resolution}
        model = FFmpeg(inputs = input_fit, outputs= output_fit)
        print ('The command used for encoding this video is :: ', model.cmd)
        model.run()
        print('All Done!')

#######################################################
        ##Function Call
#######################################################
        
input_file = input('Enter The Original Video.*its format* :: ')
call =video_optimize(input_file)
call.optimize()




