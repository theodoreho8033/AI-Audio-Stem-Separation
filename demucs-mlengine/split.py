from pydub import AudioSegment
import os 
print(os.getcwd())
sound = AudioSegment.from_mp3("./full_track/track.mp3")

#sec120=[:120*1000]

sec60 = sound[60*1000:120*1000]
sec30 = sound[30*1000:60*1000]
sec15 = sound[15*1000:30*1000]
sec10 = sound[15*1000:25*1000]
sec5 = sound[15*1000:20*1000]

sec60.export("./segments/sec60.mp3", format = "mp3" )
sec30.export("./segments/sec30.mp3", format = "mp3")
sec15.export("./segments/sec15.mp3", format = "mp3" )
sec10.export("./segments/sec10.mp3", format = "mp3")
sec5.export("./segments/sec5.mp3", format = "mp3")
