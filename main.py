import os
import shutil
import subprocess

from espeakng import ESpeakNG
from fastapi import FastAPI, UploadFile, File
from starlette.responses import StreamingResponse

app = FastAPI()


class SDPAPP:
    def __init__(self):
        self.image_folder = "images"
        self.audio_folder = "audio"
        os.makedirs(self.image_folder, exist_ok=True)
        os.makedirs(self.audio_folder, exist_ok=True)

    def process_image(self, file: UploadFile):
        # Save image in images folder
        image_path = os.path.join(self.image_folder, file.filename)
        with open(image_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        return {"message": "Image saved successfully", "filename": file.filename}

    def get_price(self):
        # Example price
        return "10 manat 28 qəpik"

    def generate_audio(self, text: str):
        # Generate audio from the text and save it in the audio folder using subprocess
        audio_filename = "price_audio.wav"
        audio_path = os.path.join(self.audio_folder, audio_filename)

        # command = [
        #     "espeak-ng",
        #     "-v", "az",  # Set the language to Azerbaijani
        #     "-w", audio_path,  # Output file path
        #     text  # Text to convert to speech
        # ]

        # es = ESpeakNG()

        # es.say(text)

        # subprocess.run(command, check=True)  # Execute the command

        return audio_path


sdp_app = SDPAPP()

@app.get("/")
async def root():
    return {"state": "running!"}

@app.post("/image/")
async def process_image(file: UploadFile = File(...)):
    return sdp_app.process_image(file)


@app.get("/price/")
def get_price():
    return {"price": sdp_app.get_price()}


@app.get("/audio/")
def generate_audio():
    price_text = sdp_app.get_price()
    audio_path = sdp_app.generate_audio(price_text)
    # Open the generated audio file in binary mode for streaming
    audio_file = open(audio_path, "rb")

    # Stream the audio file back to the mobile app
    return StreamingResponse(audio_file, media_type="audio/wav",
                             headers={"Content-Disposition": "attachment; filename=price_audio.wav"})