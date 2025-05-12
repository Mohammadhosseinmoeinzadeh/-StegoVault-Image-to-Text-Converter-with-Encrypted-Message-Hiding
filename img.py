import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import base64
import io
from cryptography.fernet import Fernet
import piexif
import piexif.helper

class ImageTextConverter:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Image & Text Converter")
        self.window.geometry("500x400")
        self.window.configure(bg='#f8f9fa')
        
        # کلید ثابت برای رمزنگاری
        self.key = b'5KxXWKiPDhQvFdJwuPGHGWnqxXqghtrXDRQxBT5_tYw='
        self.fernet = Fernet(self.key)
        
        self.create_widgets()
        
    def create_widgets(self):
        # Title label
        title_label = tk.Label(
            self.window,
            text="Image & Text Converter",
            font=('Helvetica', 16, 'bold'),
            bg='#f8f9fa',
            fg='#212529'
        )
        title_label.pack(pady=20)
        
        # Image to Text button
        self.img_to_text_btn = tk.Button(
            self.window,
            text="Convert Image to Text File",
            command=self.image_to_text,
            bg='#4CAF50',
            fg='white',
            font=('Helvetica', 10),
            height=2,
            width=30,
            relief='groove',
            cursor='hand2'
        )
        self.img_to_text_btn.pack(pady=20)
        
        # Text to Image button
        self.text_to_img_btn = tk.Button(
            self.window,
            text="Convert Text File to Image",
            command=self.text_to_image,
            bg='#2196F3',
            fg='white',
            font=('Helvetica', 10),
            height=2,
            width=30,
            relief='groove',
            cursor='hand2'
        )
        self.text_to_img_btn.pack(pady=20)
        
        # Read Message button
        self.read_msg_btn = tk.Button(
            self.window,
            text="Read Message from Image",
            command=self.read_message,
            bg='#9C27B0',
            fg='white',
            font=('Helvetica', 10),
            height=2,
            width=30,
            relief='groove',
            cursor='hand2'
        )
        self.read_msg_btn.pack(pady=20)

    def encrypt_text(self, text):
        return self.fernet.encrypt(text.encode()).decode()

    def decrypt_text(self, encrypted_text):
        return self.fernet.decrypt(encrypted_text.encode()).decode()
    
    def save_text_to_image(self, img, text):
        if text:
            # رمزنگاری متن
            encrypted_text = self.encrypt_text(text)
            
            # ذخیره متن در EXIF
            exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
            exif_dict["0th"][piexif.ImageIFD.ImageDescription] = encrypted_text.encode('utf-8')
            exif_bytes = piexif.dump(exif_dict)
            return exif_bytes
        return None
    
    def read_text_from_image(self, img):
        try:
            exif_dict = piexif.load(img.info.get('exif', b''))
            encrypted_text = exif_dict["0th"][piexif.ImageIFD.ImageDescription].decode('utf-8')
            return self.decrypt_text(encrypted_text)
        except:
            return None
        
    def image_to_text(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg")]
        )
        
        if file_path:
            try:
                with Image.open(file_path) as img:
                    # خواندن متن موجود در عکس
                    existing_message = self.read_text_from_image(img)
                    
                    # Convert image to base64
                    img_byte_arr = io.BytesIO()
                    img.save(img_byte_arr, format='PNG')
                    img_byte_arr = img_byte_arr.getvalue()
                    img_str = base64.b64encode(img_byte_arr).decode('utf-8')
                    
                    # Create file content with existing message if any
                    full_text = (
                        "// IMAGE CODE - DO NOT MODIFY\n"
                        f"{img_str}\n\n"
                        "// Write your message below and save the file\n"
                        "---BEGIN TEXT---\n"
                        f"{existing_message if existing_message else ''}\n"
                        "---END TEXT---"
                    )
                    
                    save_path = filedialog.asksaveasfilename(
                        defaultextension=".txt",
                        filetypes=[("Text files", "*.txt")]
                    )
                    
                    if save_path:
                        with open(save_path, 'w', encoding='utf-8') as f:
                            f.write(full_text)
                        
                        if existing_message:
                            messagebox.showinfo("Success", 
                                "Image converted to text file!\n" +
                                "The existing message has been included in the text file.\n" +
                                "You can modify it between ---BEGIN TEXT--- and ---END TEXT---")
                        else:
                            messagebox.showinfo("Success", 
                                "Image converted to text file!\n" +
                                "1. Write your message between ---BEGIN TEXT--- and ---END TEXT---\n" +
                                "2. Save the file")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error converting image: {str(e)}")
    
    def text_to_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Get image data
                lines = content.split('\n')
                img_str = lines[1].strip()
                
                # Get message
                message = ""
                if '---BEGIN TEXT---' in content and '---END TEXT---' in content:
                    message = content.split('---BEGIN TEXT---')[1].split('---END TEXT---')[0].strip()
                
                # Convert to image
                img_bytes = base64.b64decode(img_str)
                img = Image.open(io.BytesIO(img_bytes))
                
                save_path = filedialog.asksaveasfilename(
                    defaultextension=".png",
                    filetypes=[("PNG files", "*.png")]
                )
                
                if save_path:
                    # ذخیره متن در عکس
                    if message:
                        exif_bytes = self.save_text_to_image(img, message)
                        if exif_bytes:
                            img.save(save_path, format='PNG', exif=exif_bytes)
                    else:
                        img.save(save_path, format='PNG')
                        
                    messagebox.showinfo("Success", "File converted to image!")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error during conversion: {str(e)}")
    
    def read_message(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg")]
        )
        
        if file_path:
            try:
                with Image.open(file_path) as img:
                    message = self.read_text_from_image(img)
                    if message:
                        messagebox.showinfo("Hidden Message", 
                            "The hidden message is:\n\n" + message)
                    else:
                        messagebox.showinfo("Info", "No message found in this image")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error reading image: {str(e)}")
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = ImageTextConverter()
    app.run()
