from optimum.bettertransformer import BetterTransformer
from transformers import BarkModel, AutoProcessor
import torch
from denoiser import pretrained
import nltk
import threading

class MusicCreator:
    def __init__(self):
        nltk.download('punkt')
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
        prompt = prompt.strip().replace("\n", " ").replace("[System]", "").replace("..", ".").strip()
        print(prompt)
        sentences = nltk.sent_tokenize(prompt)
        with self.creation_lock:
            with torch.inference_mode():
                for sentence in sentences:
                    input = self.processor(sentence, voice_preset=self.voice_preset).to("cuda")
                    audio_array = self.model.generate(**input).type(torch.float32).reshape((1, -1))
                    audio_array = self.denoiser(audio_array[None])[0]
                    audio_array = audio_array.cpu().numpy().flatten()
                    yield (audio_array, self.sample_rate)
