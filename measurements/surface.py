import argparse, sys

ARG_LENGTH = "L"
ARG_HEIGHT = "H"
ARG_WIDTH = "W"

def surfaceArea(length = 0, height = 0, width = 0):
    frontSurface = length * height
    topSurface = length * width
    sideSurface = width * height

    totalSurface = (2*frontSurface) + (2*topSurface) + (2*sideSurface)
    minTotalSurface = totalSurface - (topSurface/2)

    print(f'Total surface: {totalSurface}')
    print(f'Minimum total surface: {minTotalSurface}')

def parseArguments():
    parser=argparse.ArgumentParser()
    parser.add_argument(f'-{ARG_LENGTH}', help="Length")
    parser.add_argument(f'-{ARG_HEIGHT}', help="Height")
    parser.add_argument(f'-{ARG_WIDTH}', help="Width")
    return vars(parser.parse_args())

args = parseArguments()
length = float(args.get(ARG_LENGTH))
height = float(args.get(ARG_HEIGHT))
width = float(args.get(ARG_WIDTH))

print(f'Using length: {length}')
print(f'Using height: {height}')
print(f'Using width: {width}')

surfaceArea(length, height, width)
