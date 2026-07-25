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

def generateBaseOutfit(images, recommendation, filename):
    
    top = recommendation["top"]
    bottom = recommendation["bottom"]
    print(top, bottom)
    files = [
        ("image", open("images/user.jpg", "rb")),
        #("image", open("images/blue-quarter-zip.jpg", "rb")),
        #("image", open("images/brown-chinos.jpg", "rb")),
        ("image", open(images[top], "rb")),
        ("image", open(images[bottom], "rb")),
    ] # Multipart-form data
    #mainTop = data["primary_outfit"]["top"]
    #mainBottoms = data["primary_outfit"]["bottom"]
    prompt = f"""
            This is an IMAGE EDIT task.

            Image 1 is the source image. Edit this image only.

            Images 2, 3 and any subsequent images are clothing reference images only. They are NOT identity references and must only be used to recreate the garments.

            OBJECTIVE

            Replace the person's clothing in Image 1 with the garments shown in the clothing reference images while keeping everything else identical.

            PRIORITY 1 – PRESERVE THE PERSON

            The person in Image 1 is the exact person who must appear in the output.

            Do NOT change:
            - face
            - hairstyle
            - facial features
            - skin tone
            - age
            - gender
            - body shape
            - height
            - pose
            - expression
            - accessories
            - shoes
            - background
            - lighting
            - camera angle
            - framing

            Only the clothing may change.

            PRIORITY 2 – RECREATE THE GARMENTS EXACTLY

            Image 2 is the top.

            Replace the person's existing top with the exact garment shown in Image 2.

            Image 3 is the bottom.

            Replace the person's existing bottoms with the exact garment shown in Image 3.

            If additional clothing reference images are supplied (such as a jacket), replace the corresponding clothing item using those references.

            For every garment, preserve exactly:
            - colour
            - fit
            - length
            - cut
            - style
            - logos
            - graphics
            - stitching
            - pockets
            - zips
            - cuffs
            - hems
            - fabric texture

            Do not invent or remove any garment details. Don't add any folds or tuck in the t-shirt!

            Colour accuracy is mandatory. Do not substitute a different colour even if it appears more realistic.

            PRIORITY 3 – REPLACE, DO NOT BLEND

            Completely remove the person's original clothing.

            Do not blend, partially preserve or combine the original clothing with the reference garments.

            The finished outfit must consist only of the garments shown in the reference images.

            PRIORITY 4 – PHOTOREALISM

            Produce a realistic full-body photograph.

            The garments should naturally fit the person's body with only the minimal wrinkles caused by normal wear.

            Do not add unnecessary folds, rolled sleeves, rolled hems, tucks or styling that is not present in the reference images.

            FINAL CHECK

            Before producing the final image, verify that:

            ✓ The person is identical to Image 1.
            ✓ The top exactly matches Image 2.
            ✓ The bottoms exactly match Image 3.
            ✓ Any additional garments exactly match their reference images.
            ✓ Only the clothing has changed.
            """
    

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
    with open(filename, "wb") as f:
        f.write(image) #Gets the binary data

def getUserImage():
    with open("user.jpg", "rb") as f:
        base64Image = base64.b64encode(f.read()).decode("utf-8")
    return base64Image


def generateOuterwear(images, recommendation, filename):
    outerwear = recommendation["outerwear"]
    files = [
        ("image", open(filename, "rb")),
        #("image", open("images/blue-quarter-zip.jpg", "rb")),
        #("image", open("images/brown-chinos.jpg", "rb")),
        ("image", open(images[outerwear], "rb")),
    ] # Multipart-form data
    #mainTop = data["primary_outfit"]["top"]
    #mainBottoms = data["primary_outfit"]["bottom"]
    prompt = f"""
            Edit the first image by adding ONLY the outerwear shown in the second reference image.

            Preserve the exact person and the existing outfit in the first image. Do not change the person's identity, face, hair, glasses, body, pose, accessories, background or composition.

            IMPORTANT: The person's existing bottom-wear must remain EXACTLY as shown in the first image. Do not modify, shorten, replace or regenerate it. If the person is wearing full-length trousers or jeans, they must remain full-length trousers or jeans extending to the ankles.

            Recreate the exact {outerwear} shown in the second reference image. The second image is the authoritative reference for the jacket's appearance. Match its colour, material, shape, length, sleeves, cuffs, collar, pockets, logos, patterns and design as closely as possible. Do not simplify, redesign or substitute the jacket.

            The jacket must have two complete full-length sleeves extending from the shoulders to the wrists.

            Wear the jacket partially unzipped. Keep the two front panels clearly visible so that the design and appearance of the front of the jacket can be seen, while leaving enough space in the centre to show some of the existing top underneath.

            The jacket should naturally cover parts of the existing top where appropriate. Do not otherwise modify the existing top.

            Only add the jacket. Everything outside the area naturally covered by the jacket must remain unchanged from the first image.
            """
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
    with open(filename, "wb") as f:
        f.write(image) #Gets the binary data
