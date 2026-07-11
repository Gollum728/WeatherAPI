from google import genai
from dotenv import load_dotenv # Used to get data from the .env file
import base64
import requests
import os


load_dotenv()
LLM_KEY = os.getenv("LLM_API_KEY")
CF_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT")
CF_API_KEY = os.getenv("CLOUDFLARE_API")
POLLINATIONS_KEY = os.getenv("POLLINATIONS_API_KEY")


client = genai.Client(api_key = LLM_KEY)

def showImageWithGemini(data):
    mainTop = data["primary_outfit"]["top"]
    mainBottoms = data["primary_outfit"]["bottom"]
    prompt = f"Generate a picture of a person wearing {mainTop} and {mainBottoms}. "
    """
    if len(data["primary_outfit"]["packeClothes"]) > 0: # TO BE ADDED IN A SEPARATE FUNCTION!!
        prompt+=f"Generate a se"
    """
    imageResponse = client.models.generate_content(
        model = "gemini-2.5-flash-image-preview-image",
        contents= [prompt],
    )

    for part in imageResponse.parts:
        if part.text is not None:
            print(part.text)
        elif part.inline_data is not None:
            image = part.as_image()
            image.save("generated_image.png")
    return image


def showImageWithCloudflare(data):
    #mainTop = data["primary_outfit"]["top"]
    #mainBottoms = data["primary_outfit"]["bottom"]
    prompt = "Replace the clothing of the person in the image with a cream linen shirt and grey shorts. Keep the exact same person, face, hairstyle, skin tone, body shape, pose and background. Only change the clothing to a cream linen shirt and grey shorts. Photorealistic photograph. Realistic face. Realistic human proportions. Do not change identity."
    userImage = getUserImage()
    print(type(userImage))
    url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/ai/run/@cf/runwayml/stable-diffusion-v1-5-img2img"
    imageResponse = requests.post(
        url,
        headers={
            "Authorization":f"Bearer {CF_API_KEY}"
        },
        json={
            "prompt":prompt,
            "image_b64" : userImage,
        },
    )
    print(imageResponse.status_code)
    print(imageResponse.headers.get("content-type"))
    print(imageResponse.text[:500])
    with open("outfit.png", "wb") as f:
        f.write(imageResponse.content) #Gets the binary data

def showImageWithPollinations(images, recommendation):
    print(images["Top"])
    print(images["Bottom"])
    top = recommendation["primary_outfit"]["top"]
    bottom = recommendation["primary_outfit"]["bottom"]
    files = [
        ("image", open("images/user.jpg", "rb")),
        #("image", open("images/blue-quarter-zip.jpg", "rb")),
        #("image", open("images/brown-chinos.jpg", "rb")),
        ("image", open(images["Top"], "rb")),
        ("image", open(images["Bottom"], "rb")),
    ] # Multipart-form data
    #mainTop = data["primary_outfit"]["top"]
    #mainBottoms = data["primary_outfit"]["bottom"]
    prompt = f"""Completely remove the person's existing top and bottom. Do not preserve any part of the current clothing. Replace them only with the garments shown in the reference images
                The first image is the person to edit. Keep this exact person, including their face, hairstyle, skin tone, body shape, pose, camera angle and background. Do not change their identity.
                Replace the person's current top with the exact garment shown in the second reference image, which is a {top}. Match the sleeve length, collar, fit, colour, fabric and design as closely as possible.
                The third image is the reference for the bottom. Replace the person's current bottom with the bottom shown in the third image, which are {bottom}.
                Recreate the clothing as accurately as possible, including its colour, design, logos, fit and style. Only change the clothing. Don't add any folds to the clothes, keep them exactly how they are presented in the images!
                Keep everything else exactly the same. Produce a photorealistic, full-body image showing the person's shoes and both feet.
                Preserve the original full-body composition and the output must show the person from head to toe. Do not crop or zoom the person, keep the image as it was!!"""
    #userImage = getUserImage()
    #testPrompt = "Replace the person's top with the sweatshirt shown in the reference image. Replace the bottoms with blue jeans"
    #print(type(userImage))
    postImage = requests.post( # Post used for editing image
        "https://gen.pollinations.ai/v1/images/edits",
        headers = {
            "Authorization" : f"Bearer {POLLINATIONS_KEY}"
        },
        data = {
            "prompt" : prompt,
            "model" : "nanobanana",
            "quality" : "high",
            #"image" : [userImageURL,"https://res.cloudinary.com/dytqwfesq/image/upload/v1782763960/PXL_20260629_200815120_em4hrt.jpg"],
            "size" : "832x1216"
        },
        files = files,
    )
    #Main image is as a b64 image or a URL
    #print(postImage.status_code)
    #print(postImage.text)
    response = postImage.json()
    b64Image = response["data"][0]["b64_json"] # Data is stored this way so am using dictionary manipluation to access it
    image = base64.b64decode(b64Image)
    with open("outfit.png", "wb") as f:
        f.write(image) #Gets the binary data

def getUserImage():
    with open("user.jpg", "rb") as f:
        base64Image = base64.b64encode(f.read()).decode("utf-8")
    return base64Image