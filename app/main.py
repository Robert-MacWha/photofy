import events

import ttkbootstrap as ttk

WIDTH = 750
HEIGHT = 560
file_path = ""
pen_size = 3
pen_color = "black"

events.on_start()

root = ttk.Window(themename="cosmo")
root.title("Photofy")
# root.geometry("510x580+300+110")
root.resizable(0, 0)
icon = ttk.PhotoImage(file='icons/icon.png')
root.iconphoto(False, icon)

# the left frame to contain the 4 buttons
left_frame = ttk.Frame(root, width=200, height=600)
left_frame.pack(side="left", fill="y")

# the right canvas for displaying the image
canvas = ttk.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack()

# loading the icons for the 4 buttons
image_icon = ttk.PhotoImage(file = 'icons/add.png')
flip_icon = ttk.PhotoImage(file = 'icons/flip.png')
rotate_icon = ttk.PhotoImage(file = 'icons/rotate.png')
color_icon = ttk.PhotoImage(file = 'icons/color.png')
erase_icon = ttk.PhotoImage(file = 'icons/erase.png')
save_icon = ttk.PhotoImage(file = 'icons/save.png')

# button for adding/opening the image file
image_button = ttk.Button(left_frame, image=image_icon, bootstyle="light", command=lambda : events.open_image(canvas, WIDTH, HEIGHT))
image_button.pack(pady=5)
# button for flipping the image file
flip_button = ttk.Button(left_frame, image=flip_icon, bootstyle="light", command=lambda : events.flip_image(canvas, WIDTH, HEIGHT))
flip_button.pack(pady=5)
# button for rotating the image file
rotate_button = ttk.Button(left_frame, image=rotate_icon, bootstyle="light", command=lambda : events.rotate_image(canvas, WIDTH, HEIGHT))
rotate_button.pack(pady=5)
# button for choosing pen color
color_button = ttk.Button(left_frame, image=color_icon, bootstyle="light", command=lambda : events.changeColor())
color_button.pack(pady=5)
# button for erasing the lines drawn over the image file
erase_button = ttk.Button(left_frame, image=erase_icon, bootstyle="light", command = lambda : events.eraseLines(canvas))
erase_button.pack(pady=5)
# button for saving the image file
save_button = ttk.Button(left_frame, image=save_icon, bootstyle="light", command=lambda : events.saveImage())
save_button.pack(pady=5)

canvas.bind("<B1-Motion>", lambda e : events.draw(e, canvas))

root.mainloop()