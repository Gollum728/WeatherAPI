"""
One-off script to add white padding around all wardrobe images.
Run once after photographing new clothes.
Do not run repeatedly on the same images, as padding will be added each time.
"""
def increasePadding(image):
    if image != "Image":
        img = Image.open(image)
        newWidth = int(img.width * 1.8)
        newHeight = int(img.height * 1.8)

        canvas = Image.new("RGB", (newWidth, newHeight), "white")
        x = (newWidth - img.width) // 2 # Calculates horizontal centering
        y = (newHeight - img.height) // 2 # Calculates vertical centering

        canvas.paste(img, (x,y))
        canvas.save(img.filename)
