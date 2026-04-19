import base64

data = base64.b64decode("GTYaKTJsGDw2bj0hF2k+ay83BRZpLGk2BRMZFwoFDi80NGk2azQ9BWspBRwvNCc=")

for key in range(256):
    result = bytes(b ^ key for b in data)
    if all(32 <= c < 127 for c in result):
        print(f"key=0x{key:02x}: {result.decode()}")
