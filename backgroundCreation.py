from re import T
import sys
import os
from PIL import Image, ImageDraw, ImageFilter

DEBUG = 1

class Collage:
    #Init function
    def __init__(self) -> None:
        self.photoCount = None
        self.dimensions = None
        self.testDirectoryPath = "SamplePhotos"
        pass

    #Function that returns how many photos are in the collage
    def getPhotoCount(self) -> int:
        return self.photoCount

    #Blurs an image - WIP
    #Reference: https://stackoverflow.com/questions/50787948/feathered-edges-on-image-with-pillow
    def blurImage(self,im) -> Image:
        RADIUS = 2

        # Paste image on white background
        diam = 2*RADIUS
        back = Image.new('RGBA', (im.size[0]+diam, im.size[1]+diam), (255,255,255,0))
        back.paste(im, (RADIUS, RADIUS))

        # Create paste mask
        mask = Image.new('L', back.size, 0)
        draw = ImageDraw.Draw(mask)
        x0, y0 = 0, 0
        x1, y1 = back.size
        for d in range(diam+RADIUS):
            x1, y1 = x1-1, y1-1
            alpha = 255 if d<RADIUS else int(255*(diam+RADIUS-d)/diam)
            draw.rectangle([x0, y0, x1, y1], outline=alpha)
            x0, y0 = x0+1, y0+1

        # Blur image and paste blurred edge according to mask
        blur = back.filter(ImageFilter.GaussianBlur(RADIUS/2))
        back.paste(blur, mask=mask)
        blur.show()
        return blur

    #creates the Collage 
    def createCollage(self) -> Image:
        #use this to keep track of the images
        self.photoCount = 0 
        collage = Image.new("RGBA", (1284,2778), color=(255,255,255,255))
        photoDirectory = os.listdir(self.testDirectoryPath)
        if DEBUG:
            print("photoDirectory:" + ' , '.join(photoDirectory))
        for i in range(0,1284,642):
            for j in range(0,2778,926):
                try:
                    photo = Image.open(self.testDirectoryPath + "/"+ photoDirectory[self.photoCount]).convert("RGBA")
                    frac = 0.70
                    photo = photo.crop((photo.size[0]*((1-frac)/2),photo.size[1]*((1-frac)/2),photo.size[0]-((1-frac)/2)*photo.size[0],photo.size[1]-((1-frac)/2)*photo.size[1]))    
                    photo = photo.resize((642,926))  
                    
                    collage.paste(photo, (i,j))
                    self.photoCount+=1
                    if DEBUG:
                        print("PhotoCount: " + str(self.photoCount))
                        print("\nImage Bounds: ")
                        print(photo.getbbox())
                except Exception as e:
                    print("Error:" + str(e))
        if DEBUG:
            collage.show()
            collage.save("collage.png")
        return collage

    #set dimensions
    def setDimensions(self) -> None:
        pass

    #get dimensions
    def getDimensions(self) -> list:
        return self.dimensions

if DEBUG:
    if __name__ =="__main__":
        newCollage = Collage()
        currentCollage = newCollage.createCollage()