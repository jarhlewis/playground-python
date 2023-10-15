def surfaceArea(length = 0, height = 0, width = 0):
    frontSurface = length * height
    topSurface = length * width
    sideSurface = width * height

    totalSurface = (2*frontSurface) + (2*topSurface) + (2*sideSurface)
    minTotalSurface = totalSurface - (topSurface/2)

    print(f'Total surface: {totalSurface}')
    print(f'Minimum total surface: {minTotalSurface}')

surfaceArea(1.92, 0.60, 0.63)
