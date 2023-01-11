
#main.py

#from flask import Flask

from flask import Flask,render_template,request
import os
import io
import warnings
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation


from supabase import create_client
from dotenv import load_dotenv
import os
import random
import datetime


app = Flask(__name__)


os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'
os.environ['STABILITY_KEY'] = 'sk-GjrMONDmQFIxB5jDYiG1VVm53aLsDJL4AWDi3C1helRsmfNt'

# Our Host URL should not be prepended with "https" nor should it have a trailing slash.
#os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'

# Sign up for an account at the following link to get an API Key.
# https://beta.dreamstudio.ai/membership

# Click on the following link once you have created an account to be taken to your API Key.
# https://beta.dreamstudio.ai/membership?tab=apiKeys

# Paste your API Key below.

#os.environ['STABILITY_KEY'] = 'sk-GjrMONDmQFIxB5jDYiG1VVm53aLsDJL4AWDi3C1helRsmfNt'


# Set up our connection to the API.
stability_api = client.StabilityInference(
    key=os.environ['STABILITY_KEY'], # API Key reference.
    verbose=True, # Print debug messages.
    engine="stable-diffusion-v1-5", # Set the engine to use for generation. 
    # Available engines: stable-diffusion-v1 stable-diffusion-v1-5 stable-diffusion-512-v2-0 stable-diffusion-768-v2-0 
    # stable-diffusion-512-v2-1 stable-diffusion-768-v2-1 stable-inpainting-v1-0 stable-inpainting-512-v2-0
)

usertitle = "default"
userprompt = "expansive landscape rolling greens with blue daisies and weeping willow trees under a blue alien sky, artstation, masterful, ghibli"

# Set up our initial generation parameters.
answers = stability_api.generate(
#prompt="expansive landscape rolling greens with blue daisies and weeping willow trees under a blue alien sky, artstation, masterful, ghibli",
#prompt="Neymar da Silva Santos, focused, marvel superhero cartoon style, photorealistic, detailed , 8k, 3d",
prompt = userprompt, 
#seed=992446758, # If a seed is provided, the resulting generated image will be deterministic.
            # What this means is that as long as all generation parameters remain the same, you can always recall the same image simply by generating it again.
            # Note: This isn't quite the case for Clip Guided generations, which we'll tackle in a future example notebook.
#seed = random.seed(a=1000000, version=2),
seed = 992446758,
steps=30, # Amount of inference steps performed on image generation. Defaults to 30. 
cfg_scale=8.0, # Influences how strongly your generation is guided to match your prompt.
            # Setting this value higher increases the strength in which it tries to match your prompt.
            # Defaults to 7.0 if not specified.
width=512, # Generation width, defaults to 512 if not included.
height=512, # Generation height, defaults to 512 if not included.
samples=1, # Number of images to generate, defaults to 1 if not included.
sampler=generation.SAMPLER_K_DPMPP_2M # Choose which sampler we want to denoise our generation with.
                                            # Defaults to k_dpmpp_2m if not specified. Clip Guidance only supports ancestral samplers.
                                            # (Available Samplers: ddim, plms, k_euler, k_euler_ancestral, k_heun, k_dpm_2, k_dpm_2_ancestral, k_dpmpp_2s_ancestral, k_lms, k_dpmpp_2m)
)

    

img_name = ""


# Set up our warning to print to the console if the adult content classifier is tripped.
# If adult content classifier is not tripped, save generated images.
for resp in answers:
    for artifact in resp.artifacts:
        if artifact.finish_reason == generation.FILTER:
            warnings.warn(
            "Your request activated the API's safety filters and could not be processed."
            "Please modify the prompt and try again.")
        #if artifact.type == generation.ARTIFACT_IMAGE:
            #img = Image.open(io.BytesIO(artifact.binary))
            #img.save(str(artifact.seed)+ ".png") #Save our generated images with their seed number as the filename.
            #print("Your Image saved as :  " +str(artifact.seed)+ ".png")
            #img_name = str(artifact.seed)+ ".png"


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        print(request.form["title"])
        print(request.form["prompt"])
       
        usertitle = request.form["title"]
        userprompt = request.form["prompt"]
        

        now_time = datetime.datetime.now()

        now_num = now_time.day*100000 + now_time.hour*10000 + now_time.minute*100 + now_time.second

        # Set up our initial generation parameters.
        answers = stability_api.generate(
        #prompt="expansive landscape rolling greens with blue daisies and weeping willow trees under a blue alien sky, artstation, masterful, ghibli",
        #prompt="Neymar da Silva Santos, focused, marvel superhero cartoon style, photorealistic, detailed , 8k, 3d",
        prompt = userprompt, 
        #seed=992446758, # If a seed is provided, the resulting generated image will be deterministic.
                    # What this means is that as long as all generation parameters remain the same, you can always recall the same image simply by generating it again.
                    # Note: This isn't quite the case for Clip Guided generations, which we'll tackle in a future example notebook.
        #seed = random.seed(a=1000000, version=2),
        seed = now_num,
        steps=30, # Amount of inference steps performed on image generation. Defaults to 30. 
        cfg_scale=8.0, # Influences how strongly your generation is guided to match your prompt.
                   # Setting this value higher increases the strength in which it tries to match your prompt.
                   # Defaults to 7.0 if not specified.
        width=512, # Generation width, defaults to 512 if not included.
        height=512, # Generation height, defaults to 512 if not included.
        samples=1, # Number of images to generate, defaults to 1 if not included.
        sampler=generation.SAMPLER_K_DPMPP_2M # Choose which sampler we want to denoise our generation with.
                                                 # Defaults to k_dpmpp_2m if not specified. Clip Guidance only supports ancestral samplers.
                                                 # (Available Samplers: ddim, plms, k_euler, k_euler_ancestral, k_heun, k_dpm_2, k_dpm_2_ancestral, k_dpmpp_2s_ancestral, k_lms, k_dpmpp_2m)
        )

    

        img_name = ""

        # Set up our warning to print to the console if the adult content classifier is tripped.
        # If adult content classifier is not tripped, save generated images.
        for resp in answers:
            for artifact in resp.artifacts:
                if artifact.finish_reason == generation.FILTER:
                    warnings.warn(
                    "Your request activated the API's safety filters and could not be processed."
                    "Please modify the prompt and try again.")
                if artifact.type == generation.ARTIFACT_IMAGE:
                    img = Image.open(io.BytesIO(artifact.binary))
                    img.save("tmp/" + str(artifact.seed)+ ".png") #Save our generated images with their seed number as the filename.
                    #img.save(usertitle + ".png")
                    print("Your Image saved as :  " +str(artifact.seed)+ ".png")
                    img_name = str(artifact.seed)+ ".png"
        
        supa_url = "https://ekodaqvkctdbgkvdbfrp.supabase.co"
        supa_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVrb2RhcXZrY3RkYmdrdmRiZnJwIiwicm9sZSI6ImFub24iLCJpYXQiOjE2NjMyNjQ1MTUsImV4cCI6MTk3ODg0MDUxNX0.C6nXaYCs0ieotVgdVPG8Gn9PjJq5iO8geMjGY71Avmk"

        #img_name = str(artifact.seed)+ ".png"

        print("Your AIGC Image Name = " + img_name)
        supabase = create_client(supa_url, supa_key)

        #file = open("992446758.png", "r")
        # data = supabase.storage().from_("public/training-data").download("test.txt")
        # print(data)

        supabase.storage().from_("ai-images").upload(img_name, "tmp/"+img_name)

        return render_template("result.html", img_name=img_name, usertitle=usertitle, userprompt=userprompt)

    return render_template("home.html")


@app.route('/form')
def form():
    return render_template('form.html')
 
@app.route('/data/', methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        #return f"The URL /data is accessed directly. Try going to '/form' to submit form"
        #return f" Test This"
        return render_template("result.html")
    if request.method == 'POST':
        form_data = request.form

        return render_template('data.html',form_data = form_data)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8081, debug=True)