import demucs.separate 
from datetime import datetime
import pandas as pd
import tracemalloc

#model, seg, len

#models = [ "hdemucs_mmi", "htdemucs"] #["htdemucs", "htdemucs_ft", "htdemucs_6s", "hdemucs_mmi", "mdx_extra"]
m = "htdemucs"
tracks = ["sec5.mp3" , "sec10.mp3", "sec15.mp3", "sec30.mp3", "sec60.mp3", "sec180.mp3"] #["sec5.mp3" , "sec10.mp3", "sec15.mp3", "sec30.mp3"] #["sec5.mp3" , "sec10.mp3", "sec15.mp3", "sec30.mp3", "sec60.mp3"]
segments = [str(i) for i in [5,7,10,15]]
#[str(i) for i in [5,7,10,15]]

dcts = {'track' : [], 'segment':[], 'model' : [], 'cpu_time(ms)' :[], 'cpu_ram(mb)' : [], 'cpu_time/track_time' : [], "cpu_ram/track_time" : []}
tracemalloc.start()
for track in tracks:
    segs = segments
    if track == "sec5.mp3":
        segs = ["5"]
    elif track == "sec10.mp3":
        segs = ["5","7", "10"]
    for s in segs: 
        
        if m=="htdemucs" and int(s) > 8:
            continue 
        else:
            startTime = datetime.now()
           
            tracemalloc.reset_peak()
                
            demucs.separate.main(["--mp3", "--two-stems", "vocals", "-n", m, "--segment", s, "-d", "cpu", "-o", "./test_outs/","./segments/" + track])
            endTime = datetime.now()
            current, peak = tracemalloc.get_traced_memory()
               # print([m,s,track,str(peak)])
           
           
                
            time = endTime-startTime
            idx1 = track.index("c")
            idx2 = track.index(".")
                
            track_time = float(track[idx1+1:idx2])*1000
            dcts["track"].append(track)
            dcts["segment"].append(s)
            dcts["model"].append(m)
            dcts["cpu_time(ms)"].append(time.total_seconds()*1000)
            dcts["cpu_ram(mb)"].append(float(peak)* .000001)
            dcts['cpu_time/track_time'].append(time.total_seconds()*1000/track_time)
            dcts['cpu_ram/track_time'].append(float(peak)* .000001/(track_time/1000))
print(dcts)
tracemalloc.stop()
df = pd.DataFrame.from_dict(dcts)
df.to_csv('./model_results/'+m+'_out.csv', index=False)  
#demucs.separate.main(["--mp3", "--two-stems", "vocals", "-n", "htdemucs", "--segment", "3", "-d", "cpu", "-o", "./test_outs/","./test_inputs/10s.mp3"])