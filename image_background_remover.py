import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw
from rembg import remove
import numpy as np
from copy import deepcopy


class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Background Remover with Fine-Tuning")
        self.root.geometry("800x600")

        self.input_image = None
        self.output_image = None
        self.mask = None
        self.is_background_removed = False
        self.erase_mode = False  # Track whether eraser mode is active
        self.history = []  # Store previous states for "Back" functionality

        # Title
        title_label = tk.Label(root, text="Click to Remove or Restore Background", font=("Helvetica", 16))
        title_label.pack(pady=10)

        # Canvas to display image
        self.canvas = tk.Canvas(root, width=300, height=300)
        self.canvas.pack(pady=10)

        # Buttons
        self.select_button = tk.Button(root, text="Select Image", command=self.select_image)
        self.select_button.pack(pady=5)

        self.process_button = tk.Button(root, text="Remove Background", state="disabled",
                                        command=self.remove_background)
        self.process_button.pack(pady=5)

        self.back_button = tk.Button(root, text="Back", state="disabled", command=self.undo_last_action)
        self.back_button.pack(pady=5)

        self.erase_mode_button = tk.Button(root, text="Toggle Erase Mode", state="disabled",
                                           command=self.toggle_erase_mode)
        self.erase_mode_button.pack(pady=5)

        self.save_button = tk.Button(root, text="Save Image", state="disabled", command=self.save_image)
        self.save_button.pack(pady=5)

        # Bind click and drag events
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)

    def select_image(self):
        image_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]
        )
        if image_path:
            self.input_image = Image.open(image_path).convert("RGBA")
            self.display_image(self.input_image)
            self.is_background_removed = False
            self.process_button.config(state="normal")
            self.save_button.config(state="disabled")
            self.history.clear()  # Clear history when a new image is loaded

    def display_image(self, image):
        self.tk_image = ImageTk.PhotoImage(image.resize((300, 300)))
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def on_click(self, event):
        if self.is_background_removed:
            if self.erase_mode:
                # Erase area near the clicked point
                self.erase_area(event.x, event.y)
            else:
                # Restore area near the clicked point
                self.restore_area(event.x, event.y)
        else:
            # Trigger background removal
            self.remove_background()

    def on_drag(self, event):
        if self.is_background_removed and self.erase_mode:
            self.erase_area(event.x, event.y)

    def remove_background(self):
        try:
            # Initial background removal using rembg
            output = remove(self.input_image)
            self.output_image = output
            self.mask = Image.new("L", self.input_image.size, 0)  # Initialize a mask

            # Fill the mask with 255 to keep the entire background removed initially
            np_mask = np.array(output)[:, :, 3] > 0  # Alpha channel as mask
            self.mask.putdata(np_mask.flatten().astype(np.uint8) * 255)

            self.is_background_removed = True
            self.history.append(deepcopy(self.output_image))  # Save the initial background removal state
            self.display_image(self.output_image)
            self.save_button.config(state="normal")
            self.back_button.config(state="normal")
            self.erase_mode_button.config(state="normal")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to remove background: {e}")

    def restore_area(self, x, y, radius=15):
        # Scale x and y coordinates to the original image size
        scale_x = self.input_image.width / 300
        scale_y = self.input_image.height / 300
        x, y = int(x * scale_x), int(y * scale_y)

        # Save current state to history before making changes
        self.history.append(deepcopy(self.output_image))

        # Draw a white circle on the mask to restore this area
        draw = ImageDraw.Draw(self.mask)
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=255)

        # Apply the updated mask to the original image to restore this area
        np_img = np.array(self.input_image)
        np_mask = np.array(self.mask)
        np_img[:, :, 3] = np.where(np_mask == 255, np_img[:, :, 3], 0)  # Set alpha outside mask to 0
        self.output_image = Image.fromarray(np_img)

        # Display the updated image
        self.display_image(self.output_image)

    def erase_area(self, x, y, radius=15):
        # Scale x and y coordinates to the original image size
        scale_x = self.input_image.width / 300
        scale_y = self.input_image.height / 300
        x, y = int(x * scale_x), int(y * scale_y)

        # Save current state to history before making changes
        self.history.append(deepcopy(self.output_image))

        # Draw a black circle on the mask to erase this area
        draw = ImageDraw.Draw(self.mask)
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=0)

        # Apply the updated mask to the original image to erase this area
        np_img = np.array(self.input_image)
        np_mask = np.array(self.mask)
        np_img[:, :, 3] = np.where(np_mask == 255, np_img[:, :, 3], 0)  # Set alpha outside mask to 0
        self.output_image = Image.fromarray(np_img)

        # Display the updated image
        self.display_image(self.output_image)

    def undo_last_action(self):
        if self.history:
            self.output_image = self.history.pop()  # Revert to the last saved state
            self.display_image(self.output_image)
            # If there are no more states to revert to, disable the back button
            if not self.history:
                self.back_button.config(state="disabled")

    def toggle_erase_mode(self):
        self.erase_mode = not self.erase_mode
        if self.erase_mode:
            self.erase_mode_button.config(text="Erase Mode: ON")
        else:
            self.erase_mode_button.config(text="Erase Mode: OFF")

    def save_image(self):
        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")],
            title="Save Image As"
        )
        if save_path:
            self.output_image.save(save_path)
            messagebox.showinfo("Success", "Image saved successfully!")


# Run the application
root = tk.Tk()
app = ImageEditorApp(root)
root.mainloop()
