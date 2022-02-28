import os
import _pickle as cPickle
import numpy as np
from scipy.io.wavfile import read
from sklearn import mixture
import python_speech_features
from sklearn import preprocessing
import warnings
warnings.filterwarnings("ignore")

genders = ["female","male"]


for x in range(2):
    #path to testing data
    sourcepath = genders[x] + "_clips\\"
    #path to saved models
    modelpath  = os.getcwd()

    gmm_files = [os.path.join(modelpath,fname) for fname in
                  os.listdir(modelpath) if fname.endswith('.gmm')]
    models    = [cPickle.load(open(fname,'rb')) for fname in gmm_files]
    genders   = [fname.split("\\")[-1].split(".gmm")[0] for fname
                   in gmm_files]
    files     = [os.path.join(sourcepath,f) for f in os.listdir(sourcepath)
                  if f.endswith(".wav")]
    mistakecount = 0
    for f in files:
        sr, audio  = read(f)
        features = python_speech_features.mfcc(audio, sr, 0.025, 0.01, 13, nfft=2048, appendEnergy=False)
        feat = np.asarray(())
        for i in range(features.shape[0]):
            temp = features[i, :]
            if np.isnan(np.min(temp)):
                continue
            else:
                if feat.size == 0:
                    feat = temp
                else:
                    feat = np.vstack((feat, temp))
        features = feat
        features = preprocessing.scale(features)

        scores     = None
        log = np.zeros(len(models))
        for i in range(len(models)):
            gmm    = models[i]         #checking with each model one by one
            scores = np.array(gmm.score(features))
            log[i] = scores.sum()
        result = np.argmax(log)
        if(result != x):
            mistakecount += 1
        if(genders[result]=='male'):
            print("M")
        else:
            print("K")