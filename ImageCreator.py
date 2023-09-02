from diffusers import StableDiffusionPipeline, DPMSolverSinglestepScheduler
from compel import Compel
import torch
from diffusers import AutoencoderKL

class ImageCreator:
    def __init__(self):
        self.pipe = StableDiffusionPipeline.from_pretrained("digiplay/AbsoluteReality_v1.8.1", torch_dtype=torch.float16).to("cuda")
        self.pipe.scheduler = DPMSolverSinglestepScheduler.from_config(self.pipe.scheduler.config)
        self.pipe.vae = AutoencoderKL.from_pretrained("stabilityai/sd-vae-ft-mse", torch_dtype=torch.float16).to("cuda")
        self.compel = Compel(tokenizer=self.pipe.tokenizer, text_encoder=self.pipe.text_encoder)
        self.default_prompt = "photorealistic, 32k, shot on Canon EOS-1D X Mark III, photorealistic painting, "
        self.default_negative_prompt = "painting, drawing, sketch, cartoon, anime, manga, text, watermark, signature, label, "
    def create(self, prompt, negative_prompt, save_path="image.jpg"):
        prompt = self.default_prompt + prompt
        negative_prompt = self.default_negative_prompt + negative_prompt
        conditioning = self.compel.build_conditioning_tensor(prompt)
        negative_conditioning = self.compel.build_conditioning_tensor(negative_prompt)
        [conditioning, negative_conditioning] = self.compel.pad_conditioning_tensors_to_same_length([conditioning, negative_conditioning])
        image = self.pipe(prompt_embeds=conditioning,
                          num_inference_steps=30,
                          negative_prompt_embeds=negative_conditioning).images[0]
        image.save(save_path)
        image.show()
        