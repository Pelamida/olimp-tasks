from PIL import Image

x_down = [] #для х-координат пикселей того же цвета, находящ. под рассм. строкой

def line(y, x, spot_colour, painting_colour): #раскрашивает строку по коорд. левого пикселя
    global pixels, x_down
    x_start = x
    count = 0
    while pixels[y][x] == spot_colour: #проход по пикселям вправо от данного
        pixels[y][x] = painting_colour
        count += 1
        if y != height-1:        #поиск пикселей того же цвета на ряд ниже
            if pixels[y+1][x] == spot_colour:
                x_down.append(x)
        x += 1
        if x == width:
            break
        
    x = x_start - 1
        
    while pixels[y][x] == spot_colour: #то же самое, но влево
        pixels[y][x] = painting_colour
        count += 1
        if y != height-1:
            if pixels[y+1][x] == spot_colour:
                x_down.append(x)
        x -= 1
        if x == -1:
            break
    x_down.sort()
    return count
    
def spot(y, x, spot_colour, painting_colour): #раскрашивает пятно по левому верхнему пикселю
    global pixels, x_down                     #возвращает количество закрашенных пикселей
    count = 0
    x_down.append(x)
    while x_down != []:
        x_there = x_down
        x_down = []
        for i in range(len(x_there)):
            count += line(y, x_there[i], spot_colour, painting_colour)
        y += 1
        if y == height:
            break
    return count

def rotate(): #поворачивает массив по часовой стрелке
    global pixels, width, height
    pixels = [list(i) for i in zip(*reversed(pixels))]
    width, height = height, width

image_path = 'forest.bmp'

# Open the image
img = Image.open(image_path)

# Convert the image to grayscale
img = img.convert('L')

# Get the image data as a 2D array
pixels = list(img.getdata())
width, height = img.size
pixels = [pixels[i:i+width] for i in range(0, len(pixels), width)]

    
k = 0           #обход по крайним пикселям картинки
while k != 4:
    for i in range(width):
        if pixels[0][i] == 255:  
            spot(0, i, 255, 254)
    rotate()
    k += 1
    
for i in range(1, height-1):      #поиск белого пикселя
    for j in range(1, width-1):   #нашли - перекрасили
        if pixels[i][j] == 255:
            count = spot(i, j, 255, 250)
            if count >= 30:         #если перекрасили больше 30 пикселей
                spot(i, j, 250, 72)  #то снова перекрасим, теперь в 72 цвет

# Create a new image with the processed pixel data
new_img = Image.new('L', (width, height))
new_pixels = [pixel for row in pixels for pixel in row]
new_img.putdata(new_pixels)

    # Save the modified image to a new file
new_image_path = image_path.replace('.bmp', '_modified.bmp')
new_img.save(new_image_path)
print(f"Modified image saved as '{new_image_path}'")

