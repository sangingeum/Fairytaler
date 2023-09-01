from diffusers import DiffusionPipeline
from compel import Compel, ReturnedEmbeddingsType
import torch

class ImageCreator:
    def __init__(self):
        self.pipe = DiffusionPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0"
            , torch_dtype=torch.float16
            , use_safetensors=True
            , variant="fp16")
        self.pipe.to("cuda")
        self.compel = Compel(tokenizer=[self.pipe.tokenizer, self.pipe.tokenizer_2]
                        , text_encoder=[self.pipe.text_encoder, self.pipe.text_encoder_2]
                        , returned_embeddings_type=ReturnedEmbeddingsType.PENULTIMATE_HIDDEN_STATES_NON_NORMALIZED
                        , requires_pooled=[False, True])
        self.default_prompt = "photorealistic, 32k, shot on Canon EOS-1D X Mark III, photorealistic painting, "

    def create(self, prompt, negative_prompt, save_path="image.jpg"):
        prompt = self.default_prompt + prompt
        conditioning, pooled = self.compel(prompt)
        image = self.pipe(prompt_embeds=conditioning, pooled_prompt_embeds=pooled, num_inference_steps=50, negative_prompt=negative_prompt).images[0]
        image.save(save_path)
        image.show()
