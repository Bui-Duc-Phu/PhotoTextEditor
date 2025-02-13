import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk

class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor")
        self.root.state("zoomed")

        self.image_path = ""
        self.output_folder = ""
        self.font_path = "arial.ttf"
        self.image = None
        self.processed_image = None
        self.img_tk = None
        self.processed_img_tk = None

        # Khung công cụ bên trái (300px)
        self.frame_left = tk.Frame(root, width=300)
        self.frame_left.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Khung hiển thị ảnh
        self.frame_right = tk.Frame(root)
        self.frame_right.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        self.canvas = tk.Canvas(self.frame_right, bg="gray")
        self.canvas.pack(expand=True, fill=tk.BOTH)

        # Thanh cuộn (nếu ảnh lớn)
        self.scroll_x = tk.Scrollbar(self.frame_right, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.scroll_y = tk.Scrollbar(self.frame_right, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.config(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)
        self.scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Các trường nhập liệu
        tk.Label(self.frame_left, text="Tỉ lệ chiều rộng (1-100%):\n (bằng x% của chiều rộng)").pack()
        self.scale_width_entry = tk.Entry(self.frame_left)
        self.scale_width_entry.pack()

        tk.Label(self.frame_left, text="Tỉ lệ chiều cao (1-100%):\n (bằng x% của chiều dài)").pack()
        self.scale_height_entry = tk.Entry(self.frame_left)
        self.scale_height_entry.pack()

        tk.Label(self.frame_left, text="Văn bản muốn chèn:").pack()
        self.text_entry = tk.Entry(self.frame_left)
        self.text_entry.pack()

        tk.Label(self.frame_left, text="Cỡ chữ:").pack()
        self.font_size_entry = tk.Entry(self.frame_left)
        self.font_size_entry.pack()

        tk.Label(self.frame_left, text="Mã màu (HEX, ví dụ: #FFFFFF):").pack()
        self.color_entry = tk.Entry(self.frame_left)
        self.color_entry.pack()

        tk.Label(self.frame_left, text="Vị trí cách lề trái (%):").pack()
        self.position_x_entry = tk.Entry(self.frame_left)
        self.position_x_entry.pack()

        tk.Label(self.frame_left, text="Vị trí cách trên (%):").pack()
        self.position_y_entry = tk.Entry(self.frame_left)
        self.position_y_entry.pack()

        # Nút chức năng
        tk.Button(self.frame_left, text="Chọn ảnh", command=self.choose_image).pack(fill=tk.X, pady=5)
        self.image_path_label = tk.Label(self.frame_left, text="", fg="blue", wraplength=250)
        self.image_path_label.pack()

        tk.Button(self.frame_left, text="Chọn thư mục lưu", command=self.choose_output_folder).pack(fill=tk.X, pady=5)
        self.output_path_label = tk.Label(self.frame_left, text="Chưa chọn thư mục", fg="red", wraplength=250)
        self.output_path_label.pack()

        tk.Button(self.frame_left, text="Chọn font", command=self.choose_font).pack(fill=tk.X, pady=5)
        tk.Button(self.frame_left, text="Xử lý ảnh", command=self.process_image).pack(fill=tk.X, pady=5)

    def choose_image(self):
        """Chọn ảnh và hiển thị với khoảng cách 5cm từ thanh công cụ."""
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if self.image_path:
            self.image = Image.open(self.image_path)
            self.image_path_label.config(text=self.image_path)
            self.display_image(self.image)

    def choose_output_folder(self):
        """Chọn thư mục lưu ảnh."""
        self.output_folder = filedialog.askdirectory()
        if self.output_folder:
            self.output_path_label.config(text=self.output_folder, fg="green")

    def choose_font(self):
        """Chọn font chữ."""
        self.font_path = filedialog.askopenfilename(filetypes=[("Font files", "*.ttf")])

    def display_image(self, img):
        """Hiển thị ảnh với khoảng cách 5cm từ thanh công cụ bên trái."""
        if img:
            self.img_tk = ImageTk.PhotoImage(img)
            self.canvas.delete("all")
            self.canvas.create_image(188, 10, image=self.img_tk, anchor=tk.NW)  # 188px = 5cm
            self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def process_image(self):
        """Xử lý ảnh: thay đổi kích thước, thêm text và hiển thị với khoảng cách 5cm."""
        if not self.image_path:
            messagebox.showerror("Lỗi", "Vui lòng chọn ảnh!")
            return
        if not self.output_folder:
            messagebox.showerror("Lỗi", "Vui lòng chọn thư mục lưu ảnh!")
            return

        try:
            image = Image.open(self.image_path)

            # Lấy tỷ lệ ảnh, giữ nguyên nếu không nhập
            scale_width = int(self.scale_width_entry.get()) if self.scale_width_entry.get() else 100
            scale_height = int(self.scale_height_entry.get()) if self.scale_height_entry.get() else 100
            new_width = int(image.width * (scale_width / 100))
            new_height = int(image.height * (scale_height / 100))
            self.processed_image = image.resize((new_width, new_height))

            # Lấy thông tin text
            text = self.text_entry.get().strip()
            font_size = int(self.font_size_entry.get()) if self.font_size_entry.get() else 20
            color = self.color_entry.get().strip() if self.color_entry.get() else "#FFFFFF"
            position_x_percent = int(self.position_x_entry.get()) if self.position_x_entry.get() else 10
            position_y_percent = int(self.position_y_entry.get()) if self.position_y_entry.get() else 10

            if text:  # Chỉ vẽ text nếu có nội dung
                draw = ImageDraw.Draw(self.processed_image)
                font = ImageFont.truetype(self.font_path, font_size)
                position_x = int(new_width * (position_x_percent / 100))
                position_y = int(new_height * (position_y_percent / 100))
                draw.text((position_x, position_y), text, font=font, fill=color)

            # Lưu ảnh sau khi xử lý
            output_filename = os.path.basename(self.image_path).replace(".", "_fix.")
            output_path = os.path.join(self.output_folder, output_filename)
            self.processed_image.save(output_path)

            self.display_image(self.processed_image)
            messagebox.showinfo("Thành công", f"Ảnh đã được lưu tại: {output_path}")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()
