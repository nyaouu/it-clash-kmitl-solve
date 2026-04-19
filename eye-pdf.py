import fitz  # PyMuPDF

def solve_color_stego(pdf_path):
    doc = fitz.open(pdf_path)
    binary_str = ""

    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if b['type'] == 0:
                for line in b["lines"]:
                    for span in line["spans"]:
                        text = span["text"]
                        
                        # กรองช่องว่างออกตามที่คุณบอก "ไม่ต้องสนใจ ช่องว่าง"
                        # เพราะช่องว่างอาจจะมีสี #000000 ทำให้บิตเกิน
                        clean_text = text.replace(" ", "").replace("\t", "").replace("\n", "")
                        
                        if not clean_text:
                            continue
                            
                        color_hex = f"#{span['color']:06x}"
                        
                        # ทุกๆ 1 ตัวอักษร (ที่ไม่ใช่ช่องว่าง) คือ 1 บิต
                        for char in clean_text:
                            if color_hex == "#000000":
                                binary_str += "0"
                            elif color_hex == "#000005":
                                binary_str += "1"

    doc.close()

    # แปลง Binary เป็น Text (8 บิต = 1 ตัวอักษร)
    flag = ""
    for i in range(0, len(binary_str), 8):
        byte = binary_str[i:i+8]
        if len(byte) == 8:
            flag += chr(int(byte, 2))
            
    return binary_str, flag

# รันเพื่อหาคำตอบ
binary_raw, hidden_msg = solve_color_stego("file.pdf")

print(f"Binary String: {binary_raw}") # แสดงตัวอย่างบิต
print(f"Hidden Flag: {hidden_msg}")
