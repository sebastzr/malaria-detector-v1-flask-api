from static.cnn.scripts.label_image import *
#from scripts.label_image import * #debug

def runCNN(filePath):
    time, labels, results = core(filePath)
    #labels = json.dumps(labels)
    results = results.tolist()
    #results = json.dumps(results)
    data = {
        'time' : time,
        'labels' : labels,
        'results' : results
    }

    r = 0
    l = 0
    for (enum, i) in enumerate(results):
        if (i > r):
            r = i
            l = enum

    r = r * 100.0

    r = round(r, 1)

    data = {
        'label' : labels[l],
        'result' : r
    }
    return data

#print(runCNN('test_photos/photo.jpg')) #debug