import cv2
import os
from Mediapipe_holistic import  framestocoord
import numpy as np
import torch
from torch import nn

def converttoimages():

    main_arr = []
    os.mkdir('tmpframes/')

    for videoname in os.listdir('tmp/'):
        print(videoname)
        cap = cv2.VideoCapture('tmp' + '/' + videoname)
        success, image = cap.read()
        count = 0

        destination_folder = 'tmpframes/' + videoname[:-4]
        os.mkdir(destination_folder)

        while success:
            cv2.imwrite(destination_folder + '/img_{}.png'.format(str(count).zfill(5)), image)  # save frame as JPEG file
            success, image = cap.read()
            count += 1

        print(videoname + ' Done: {} frames'.format(count))

    for video in os.listdir('tmpframes/'):
        folder = 'tmpframes/' + video
        arr_ = []
        for frame in os.listdir(folder):
            path = folder + '/' + frame
            data = framestocoord(path)
            if  data is None:
                continue
            elif data.shape[0] != 120:
                continue
            else:
                arr_.append(data)

        def pad(array_, current_length):
            diff = 1000 - current_length
            pad = nn.ConstantPad2d((0, 0, 0, diff), 0)
            return pad(torch.from_numpy(array_))

        arr = np.array(arr_)
        current_length = arr.shape[0]

        if current_length < 1000:
            arr= pad(arr, current_length)

        main_arr.append(arr)

    return main_arr

