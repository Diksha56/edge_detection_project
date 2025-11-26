import cv2
import os
from tkinter import *
from tkinter import filedialog, ttk
from PIL import Image, ImageTk

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing Tool")

        self.original_image = None
        self.processed_image = None
        self.history_stack = []  

        self.create_widgets()

    def create_widgets(self):

        load_btn = Button(self.root, text="Load Image", command=self.load_image)
        load_btn.grid(row=0, column=0, pady=5)

        save_btn = Button(self.root, text="Save Image", command=self.save_image)
        save_btn.grid(row=0, column=1, pady=5)

        reset_btn = Button(self.root, text="Reset", command=self.reset_image)
        reset_btn.grid(row=0, column=2, pady=5)

        undo_btn = Button(self.root, text="Undo", command=self.undo_image)
        undo_btn.grid(row=0, column=3, pady=5)

        Label(self.root, text="Filter:").grid(row=1, column=0)
        self.filter_opt = ttk.Combobox(self.root, values=["None", "Gaussian", "Median"])
        self.filter_opt.set("None")
        self.filter_opt.grid(row=1, column=1)

        Label(self.root, text="Edge Detection:").grid(row=2, column=0)
        self.edge_opt = ttk.Combobox(self.root, values=["None", "Sobel", "Canny", "Laplacian"])
        self.edge_opt.set("None")
        self.edge_opt.grid(row=2, column=1)

        Label(self.root, text="Kernel Size").grid(row=3, column=0)
        self.kernel_slider = Scale(self.root, from_=1, to=15, orient=HORIZONTAL)
        self.kernel_slider.grid(row=3, column=1)

        Label(self.root, text="Canny Threshold 1").grid(row=4, column=0)
        self.canny_th1 = Scale(self.root, from_=0, to=255, orient=HORIZONTAL)
        self.canny_th1.grid(row=4, column=1)

        Label(self.root, text="Canny Threshold 2").grid(row=5, column=0)
        self.canny_th2 = Scale(self.root, from_=0, to=255, orient=HORIZONTAL)
        self.canny_th2.grid(row=5, column=1)

        apply_btn = Button(self.root, text="Apply", command=self.apply_processing)
        apply_btn.grid(row=6, column=0, columnspan=2, pady=10)

        self.canvas_original = Label(self.root)
        self.canvas_original.grid(row=7, column=0)

        self.canvas_processed = Label(self.root)
        self.canvas_processed.grid(row=7, column=1)

    def load_image(self):
        file_path = filedialog.askopenfilename(initialdir="images", filetypes=[("Images", "*.jpg *.png")])
        if file_path:
            self.original_image = cv2.imread(file_path)
            self.processed_image = self.original_image.copy()
            self.history_stack.clear()
            self.show_images()

    def apply_processing(self):
        if self.processed_image is None:
            return

        self.history_stack.append(self.processed_image.copy())

        img = self.processed_image.copy()

        k = self.kernel_slider.get() or 1
        if k % 2 == 0: k += 1

        if self.filter_opt.get() == "Gaussian":
            img = cv2.GaussianBlur(img, (k, k), 0)

        elif self.filter_opt.get() == "Median":
            img = cv2.medianBlur(img, k)

        if self.edge_opt.get() == "Sobel":
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=k)

        elif self.edge_opt.get() == "Canny":
            t1 = self.canny_th1.get()
            t2 = self.canny_th2.get()
            img = cv2.Canny(img, t1, t2)

        elif self.edge_opt.get() == "Laplacian":
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = cv2.Laplacian(img, cv2.CV_64F)

        self.processed_image = img
        self.show_images()

    def reset_image(self):
        if self.original_image is not None:
            self.processed_image = self.original_image.copy()
            self.history_stack.clear()
            self.show_images()

    def undo_image(self):
        if self.history_stack:
            self.processed_image = self.history_stack.pop()
            self.show_images()

    def save_image(self):
        if self.processed_image is not None:
            file = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg")])
            if file:
                cv2.imwrite(file, self.processed_image)

    def show_images(self):
        def convert(img):
            if len(img.shape) == 2:
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
            else:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            imgtk = ImageTk.PhotoImage(Image.fromarray(img).resize((400, 300)))
            return imgtk

        if self.original_image is not None:
            self.tk_original = convert(self.original_image)
            self.canvas_original.config(image=self.tk_original, text="Original")

        if self.processed_image is not None:
            self.tk_processed = convert(self.processed_image)
            self.canvas_processed.config(image=self.tk_processed, text="Processed")

root = Tk()
app = ImageProcessorApp(root)
root.mainloop()