import base64

data = open('challenge.txt').read().strip()

bytes_data = bytes([int(data[i:i+8], 2) for i in range(0, len(data), 8)])
png_data = base64.b64decode(bytes_data)

open('output.png', 'wb').write(png_data)
