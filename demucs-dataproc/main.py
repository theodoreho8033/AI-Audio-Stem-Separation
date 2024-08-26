from pydub import AudioSegment
import os
import io
from flask import Flask, request, send_file
import torch
import torchaudio
import aiohttp
import asyncio
from torchaudio.transforms import Fade
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 24 * 1000 * 1000
CHUNK_LEN = 19
OVERLAP_LEN = .1
API_URL = "https://demucs-4gb-8cpu-wfccdzqdja-uw.a.run.app/upload/hdemucs_mmi/10/10"
ALLOWED_EXTENSIONS = {'mp3'}
def split_chunks(audio, sr):
    chunks = []
    _, max_len = audio.shape
    minute = sr * CHUNK_LEN
    overlap = int(sr * OVERLAP_LEN)
    
    cur_idx = 0 
    while  cur_idx+minute+overlap < max_len: 
        chunks.append(audio[:, cur_idx:cur_idx+minute+overlap])
        cur_idx += minute
    
    last_chunk = audio[:,cur_idx:]
    _, last_chunk_len = last_chunk.shape
    if last_chunk_len < sr*10: 
        chunks[-1] = torch.cat((chunks[-1],last_chunk[:, overlap:]), dim = 1)
    else: 
        chunks.append(last_chunk)
    
    for c in chunks:
        print(c.shape[1]/sr)
    
    return chunks, max_len

def combine_audio(audios, audio_lens):
    
    
    
    start = 0 
    sr = 0
    final_len = 0
    
    tensors = [None for i in range(len(audios))]
    for a in audios:
        tens, sr2 = torchaudio.load(a[1], backend = "ffmpeg")
        final_len += tens.shape[1] 
        sr = sr2
        tensors[a[0]] = tens
        audio_file = "./temp_files/" + str(a[0]) + ".mp3" 
        os.remove(audio_file)
    overlap_frames = int(OVERLAP_LEN * sr)
   # final_len -= (len(audios)-2)*overlap_frames
    final = torch.zeros(2,final_len)
    
    chunk_len_samples = int(sr * (CHUNK_LEN + OVERLAP_LEN))
    fade = Fade(fade_in_len=0, fade_out_len=int(overlap_frames), fade_shape="linear")
    end = tensors[0].shape[1] 
    for i in range(len(tensors)-1):
        print(end-start)
        t = tensors[i] 
      
        out = fade(t)
        final[:,start:end] += out 
        if start == 0: 
            fade.fade_in_len = int(overlap_frames)
            start += int(end - overlap_frames)
        else:
            start += t.shape[1]
        end = start + tensors[i+1].shape[1]
    
    print("----")
    print(end-start)
    print(start)
    print(end)
    fade.fade_out_len = 0         
    last = fade(tensors[-1])
    print(last.shape)
    print(final[:,start:].shape)
    final[:,start:end] += last
    
    torchaudio.save("./temp_files/test.mp3", final, sr, format = "mp3")
    return final
            
        
    
def save_audio(tensor, sr, idx):
    chunk_len = sr*15
    audio_file = "./temp_files/" + str(idx) + ".mp3" #io.BytesIO()
    torchaudio.save(audio_file, tensor, sr,  format = "mp3")

    return audio_file

async def get_vocals(session, audio_file, idx, url = API_URL):
    
    data = aiohttp.FormData()
    data.add_field('file',
               open(audio_file, 'rb'),
               filename='upload.mp3')
    print(data)
    async with session.post(url, data = data) as resp: 
        print("req")
        resp_body = await resp.read()
        print("resp")
        return (idx, resp_body)

async def dispatch(audio_files):
    async with aiohttp.ClientSession() as session: 
        tasks = []
        for idx in range(len(audio_files)):
            tasks.append(asyncio.ensure_future(get_vocals(session, "./temp_files/" + str(idx) + ".mp3", idx)))
        
        resps = await asyncio.gather(*tasks)

        return resps
        

@app.route("/testop", methods = ['GET'])
def testop():
    print("test!")
    return os.getcwd()

@app.route("/isalive", methods = ['GET'])
def is_alive():

    return "alive!"




def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload", methods = ['POST'])
async def upload_file():
    file = request.files['file']
    if allowed_file(file.filename):
        nmemoryfile = io.BytesIO(file.read())
        audio, sr = torchaudio.load(nmemoryfile, backend = "ffmpeg")
        chunks, max_len = split_chunks(audio, sr)
        audio_files = [save_audio(chunks[i], sr, i) for i in range(len(chunks))]#[save_audio(chunks[0], sr, 0), save_audio(chunks[1], sr, 1), save_audio(chunks[2], sr, 2)]
        vocals = await dispatch(audio_files)
        combine_audio(vocals, max_len)
        
        return_data = io.BytesIO()
        with open("./temp_files/test.mp3", 'rb') as fo:
            return_data.write(fo.read())
        return_data.seek(0)
        os.remove("./temp_files/test.mp3")
        return send_file(return_data, mimetype='audio/mpeg')
    else:
        return "error"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    
    
    
