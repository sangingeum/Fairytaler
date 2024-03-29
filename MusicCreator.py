import numpy as np
from optimum.bettertransformer import BetterTransformer
from transformers import BarkModel, AutoProcessor
import torch
from denoiser import pretrained
import nltk
import threading
from TTS.api import TTS

class MusicCreator:
    def __init__(self, use_tacotron=True):
        self.use_tacotron = use_tacotron
        self.device = "cuda"
        nltk.download('punkt')
        if use_tacotron:
            self.model = TTS("tts_models/en/ljspeech/tacotron2-DDC_ph").to(self.device) #"tts_models/en/ljspeech/tacotron2-DDC_ph", 22050, apache-2.0
            self.sample_rate = 22050
        else:
            self.processor = AutoProcessor.from_pretrained("suno/bark-small")
            self.model = BetterTransformer.transform(
                BarkModel.from_pretrained("suno/bark-small",
                                          torch_dtype=torch.float16).to("cuda"), keep_original_model=False)
            self.voice_preset = "v2/en_speaker_9"
            self.sample_rate = self.model.generation_config.sample_rate
        self.denoiser = pretrained.dns64().cuda()
        self.creation_lock = threading.Lock()

    # the result is a generator
    def create(self, prompt: str):
        prompt = prompt.strip().replace("\n", " ").replace("..", ".").strip()
        print(prompt)
        with self.creation_lock:
            with torch.inference_mode():
                sentences = nltk.sent_tokenize(prompt)
                if self.use_tacotron:
                    for sentence in sentences:
                        try:
                            #audio_array = torch.from_numpy(np.array(self.model.tts(text=sentence)).reshape((1, -1))).type(torch.float32).to(self.device)
                            #audio_array = self.denoiser(audio_array[None])[0]
                            #audio_array = audio_array.cpu().numpy().flatten()
                            audio_array = np.array(self.model.tts(text=sentence), dtype=np.float32)
                            yield audio_array, self.sample_rate
                        except:
                            continue
                else:
                    for sentence in sentences:
                        input = self.processor(sentence, voice_preset=self.voice_preset).to(self.device)
                        audio_array = self.model.generate(**input).type(torch.float32).reshape((1, -1))
                        audio_array = self.denoiser(audio_array[None])[0]
                        audio_array = audio_array.cpu().numpy().flatten()
                        yield (audio_array, self.sample_rate)
