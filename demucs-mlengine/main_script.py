import demucs.separate 
from flask import Flask, request,send_from_directory
import os
app = Flask(__name__)
print("test")



@app.route("/isalive", methods = ['GET'])
def is_alive():

    return "alive!"


@app.route("/upload/<model>/<segment>/<len>", methods = ['POST'])
def upload_file(model, segment, len):
    if model not in ["htdemucs", "hdemucs_mmi"]:
        return "invalid model"
    elif (model == 'htdemucs' and segment not in ["5","7"]) or segment not in ["5", "7", "10", "15"]:
        return "invalid segment"

    f = request.files['file']
    
    in_file = './uploads/upload.mp3'
    outdir = './outs/'
    f.save(in_file)


    demucs.separate.main(["--mp3", 
                          "--two-stems", "vocals", 
                          "-n", model, 
                          "--segment", segment, 
                          "-d", "cpu",
                          "-o", outdir,
                          in_file])

    final_outs = outdir + model + "/upload/"
    
    return send_from_directory(final_outs, 'vocals.mp3')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))