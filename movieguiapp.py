from tkinter import *
from PIL import Image, ImageTk

# global variables to check seat count and price:
selected_seats = 0

def book_seat(button, movie_name, price):
    global selected_seats

    if button["bg"] == "cyan":
        return  # Prevent rebooking the same seat

    button.config(bg="cyan")  # Change the color to green
    selected_seats += 1  # Increase the seat count
    total_price = selected_seats * price  # Calculate the total price

    # Update the payment display:
    for widget in button.master.grid_slaves():
        if int(widget.grid_info().get("row")) == 5:
            widget.destroy()  # Remove any existing payment label

    payment_label = Label(
        button.master,
        text=f"Movie: {movie_name} | Seats: {selected_seats} | Total: ${total_price}",
        font=("Arial", 12),
        bg=button.master["bg"],
    )
    payment_label.grid(row=5, column=0, columnspan=5, pady=10)  # Display below seats

def create_seat_chart(title, bg_color, movie_name, price):
    seats_window = Toplevel(root)
    seats_window.title(f"Seats available for {title}")
    # seats_window.geometry("265x300")
    seats_window.configure(bg=bg_color)
    
    def make_book_seat_handler(button):
        return lambda: book_seat(button, movie_name, price)
    
    buttons = []
    for r in range(5):
        row_buttons = []
        for c in range(5):
            button = Button(
                seats_window,
                text="|_|",
                font=("Arial", 12),
                width=3,
                bg="white",  # Set initial background to white
            )
            button.config(command=make_book_seat_handler(button))
            button.grid(row=r, column=c, padx=8, pady=8)
            row_buttons.append(button)
        buttons.append(row_buttons)
    
    # Store buttons to prevent garbage collection
    seats_window.buttons = buttons

def next_screen(event):
    movie_window = Toplevel(root)
    movie_window.title("Movies Available")

    movies = [
        ("Alien Romulus", "alien.jpg", "coral", 12),
        ("Devara", "devara.jpg", "aquamarine", 15),
        ("Kalki", "kalki.jpg", "gold", 15),
        ("Pushpa-2", "pushpa.jpg", "maroon", 15)
    ]

    # Load and resize movie images
    movie_pics = []
    for movie in movies:
        img = Image.open(movie[1]).resize((180, 200))
        movie_pics.append(ImageTk.PhotoImage(img))

    # Create movie labels with clickable events
    for i, (title, _, bg_color, price) in enumerate(movies):
        row = i // 2
        col = i % 2
        
        movie_label = Label(movie_window, image=movie_pics[i])
        movie_label.grid(row=row, column=col, padx=15, pady=15)
        
        # Use a closure to capture the correct movie details
        def create_movie_handler(t, bg, p):
            return lambda event: create_seat_chart(t, bg, t, p)
        
        movie_label.bind("<Button-1>", create_movie_handler(title, bg_color, price))

    # Prevent garbage collection of images
    movie_window.movie_pics = movie_pics

root = Tk()
root.title("Movies available")
root.geometry("400x450")
root.configure(bg="cyan")

label = Label(root, text="Movies Showing today", bg="cyan", fg="black", width=200, font=("Arial", 24))
label.pack()

button = Button(root, text="Start", font=("Arial", 24))
button.pack()
button.bind("<Button-1>", next_screen)

root.mainloop()