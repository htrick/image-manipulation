from PIL import Image
import sys, math, random

def main(argv):
    try:
        numCubes = int(argv[1])
        fileName = argv[0]
        original = Image.open(fileName)
    except FileNotFoundError:
        print("File not found")
        return
    except ValueError:
        print("Number of cubes must be an integer, representing the total amount of cubes in the final image")
        return
    except:
        print("Usage: python3 jumble.py <file name> <number of cubes>")
        return

    print("Processing...")

    originalPixels = original.load()
    new = original.copy()
    newPixels = new.load()

    width, height = original.size
    n = int(math.sqrt((width * height) / numCubes))
    cubes = []
    for x in range(0, width - width % n, n):
        for y in range(0, height - height % n, n):
            cubes.append((x, y))

    for x in range(0, width - width % n, n):
        for y in range(0, height - height % n, n):
            xC, yC = cubes.pop(random.randint(0, len(cubes) - 1))
            setCube(newPixels, originalPixels, x, y, n, xC, yC, width, height)

    new.save("jumble_" + fileName)
    print("Saved as 'jumble_" + fileName + "'")

def setCube(image, original, x, y, n, xC, yC, w, h):
    for i in range(x, x + n):
        for j in range(y, y + n):
            # print(i, j, xC + i - x, yC + j - y)
            image[min(i, w - 1), min(j, h - 1)] = original[min(xC + i - x, w - 1), min(yC + j - y, h - 1)]

if __name__ == "__main__":
    main(sys.argv[1:])
