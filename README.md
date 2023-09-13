# Fairytaler
 An interactive story generator based on GPT-3.5.    
 The goal of this project is to make an interative, infinitely replayable text-based game.

## Requirements

### Packages
To play this game, you need to install all the necessary libraries by executing the following command.

```
$pip install -r requirements.txt
```
Note that ```requirements.txt``` is in the repository.


Additionally, You need to install a CUDA-enabled Torch library form [here](https://pytorch.org/get-started/locally/).

### Environment Variable
To play this game, you'll need an OpenAI API key.    
The game utilizes an environment variable named ```OPENAI_API_KEY``` as the key for authentication.      
Refer to [this page](https://platform.openai.com/docs/api-reference/authentication) for more details.

### System

You need enough VRAM and DRAM capacity to load models and perform inferences with them.

## Images

### main
![main](readme_images/main.PNG)
### new game
![main](readme_images/new_game.PNG)
### EX1 : Cyberpunk
![main](readme_images/cb1.PNG)
![main](readme_images/cb2.PNG)
### EX1 : Baldur's gate
![main](readme_images/md1.PNG)
![main](readme_images/md2.PNG)