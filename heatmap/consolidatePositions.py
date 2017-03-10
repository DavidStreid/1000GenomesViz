import os
import sys
import re
import json

'''
Converts file in the following format to JSON -
    INPUT
        Population,Sample,Mut,Severity,col,row
        ACB,HG02052,chrMT-990-C,2.0,110,23
        ACB,HG02325,chrMT-1007-A,1.0,2,45
    OUTPUT
        {"count": 32, "pos": "15784", "change": "C", "severity": "-1.0"}
        {"count": 4, "pos": "15431", "change": "A", "severity": "-1.0"}
        {"count": 1, "pos": "15470", "change": "C", "severity": "-1.0"}
$ python consolidatePositions.py . consolidatedPositions/
'''

if(len(sys.argv) < 3):
    print "ERROR: Specify an input and output directory"
    sys.exit()

heatMapDirectory = sys.argv[1]
targetDirectory = sys.argv[2]

for filename in os.listdir(heatMapDirectory):
    searchObj = re.search( r'_heatmap.csv', filename, re.M|re.I) #Only heatmap data
    if(searchObj):
        with open(filename,'r') as i:
            lines = i.readlines()
            data = lines[1:]
            count = 1
            if(data):   # If file contains non-header information
                posDic = {}

                pop = data[0].split(',')[0] # Population should be same for each file

                for d in data:              # Iterate through non-header information
                    mutData = d.split(',')  
                    posData = mutData[2].split('-') # split on dashes (E.g. chrMT-1007-A)
                    loc = posData[1]                # basepair position
                    mut = posData[2]                # base change
                    if(posDic.has_key(loc)):        # Get frequency at position
                        posDic[loc][0] += 1
                    else:
                        posDic[loc] = [1, mutData[3], mut]  #[count, severity, base change]

                '''
                Write to file
                Bulk queries take very simple, but exact formats (don't forget the new lines)
                    action_and_meta_data\n
                    optional_source\n
                '''
                file = targetDirectory + '/' + pop + '_mutFreq.json'
                target = open(file, 'w')
                target.write('{ "index" : { "_index" : "heatmap", "_type" : "mutFreq", "_id" : "' + pop + '"} }' + '\n')
                target.write('{"mutList":[')
                for k, v in posDic.items()[:-1]:     
                    target.write(json.dumps({'pos': str(k), 'count': v[0], 'severity': v[1], 'change': v[2]}).replace(" ", "") + ',')
                target.write(json.dumps({'pos': str(k), 'count': v[0], 'severity': v[1], 'change': v[2]}).replace(" ", ""))
                target.write(']}\n')

                # TODO - Write the CURL request to index file

