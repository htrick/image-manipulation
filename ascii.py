from PIL import Image, ImageEnhance
import sys, math

def main(argv):
    percentage = 0.03
    try:
        if len(argv) > 1:
            percentage = float(argv[1])
            if percentage < 0.01 or percentage > 5:
                raise ValueError
        fileName = argv[0]
        original = Image.open(fileName)
    except FileNotFoundError:
        print("File not found")
        return
    except ValueError:
        print("Percentage must be an number between 0.01 and 5; default is 0.03")
        return
    except:
        print("Usage: python3 ascii.py <file name> [optional percentage size of characters]")
        return

    print("Processing...   (this takes a while)")

    new = original.copy().convert("L")
    new = ImageEnhance.Contrast(new).enhance(2)
    newPixels = new.load()

    width, height = original.size
    n = int(math.sqrt(percentage / 100 * width * height))
    for x in range(0, width, n):
        for y in range(0, height, n):
            xDelta = min(x + n, width)
            yDelta = min(y + n, height)
            bestMatch = compareToCharacters(newPixels, x, y, xDelta, yDelta)
            drawCharacter(newPixels, bestMatch, x, y, xDelta, yDelta)

    new.save("ascii_" + fileName)
    print("Saved as 'ascii_" + fileName + "'")

def compareToCharacters(image, x1, y1, x2, y2):
    minDiff = 100000000
    bestChar = 32
    for code in range(32, 127):
        charImage = Image.open("ascii/" + str(code) + ".png").convert("L").load()
        totalDiff = 0
        for x in range(0, 10):
            for y in range(0, 10):
                xImage = x1 + int((x2 - x1) * x / 10)
                yImage = y1 + int((y2 - y1) * y / 10)
                totalDiff += abs(charImage[x, y] - image[xImage, yImage])
        if totalDiff < minDiff:
            minDiff = totalDiff
            bestChar = code
    return bestChar

def drawCharacter(image, character, x1, y1, x2, y2):
    charImage = Image.open("ascii/" + str(character) + ".png").convert("L").load()
    for x in range(x1, x2):
        for y in range(y1, y2):
            xChar = int((x - x1) / (x2 - x1) * 10)
            yChar = int((y - y1) / (y2 - y1) * 10)
            image[x, y] = charImage[xChar, yChar]

if __name__ == "__main__":
    main(sys.argv[1:])
