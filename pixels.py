from PIL import Image
import sys, math

def main(argv):
    try:
        numPixels = int(argv[1])
        fileName = argv[0]
        original = Image.open(fileName)
    except FileNotFoundError:
        print("File not found")
        return
    except ValueError:
        print("Number of pixels must be an integer, representing the total amount of pixels in the final image")
        return
    except:
        print("Usage: python3 pixels.py <file name> <number of pixels at end>")
        return

    print("Processing...")

    originalPixels = original.load()
    new = original.copy()
    newPixels = new.load()

    width, height = original.size
    n = int(math.sqrt((width * height) / numPixels))
    for x in range(0, width, n):
        for y in range(0, height, n):
            xDelta = min(x + n, width)
            yDelta = min(y + n, height)
            color = getColor(originalPixels, x, y, xDelta, yDelta)
            setColor(newPixels, color, x, y, xDelta, yDelta)

    new.save("pixelated_" + fileName)
    print("Saved as 'pixelated_" + fileName + "'")

def getColor(image, x1, y1, x2, y2):
    red = 0
    green = 0
    blue = 0
    delta = (x2 - x1) * (y2 - y1)
    for i in range(x1, x2):
        for j in range(y1, y2):
            pixel = image[i, j]
            red += pixel[0]
            green += pixel[1]
            blue += pixel[2]
    return (red // delta, green // delta, blue // delta)

def setColor(image, color, x1, y1, x2, y2):
    for i in range(x1, x2):
        for j in range(y1, y2):
            image[i, j] = color

if __name__ == "__main__":
    main(sys.argv[1:])
