import requests
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import font
import queue
import time
# Queue to safely pass data from threads to the main GUI thread
output_queue = queue.Queue()

# Function to safely insert text into the output widget from a different thread
def safe_insert_text(output_widget, text, tag=None):
    output_widget.after(0, output_widget.insert, tk.END, text, tag)

# Function to fetch Instagram posts
def fetch_instagram_posts(access_token, user_id, output_widget):
    url = f"https://graph.instagram.com/{user_id}/media"
    params = {
        "access_token": access_token,
        "fields": "id,caption,media_type,media_url,timestamp"
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            posts = data.get("data", [])
            if posts:
                safe_insert_text(output_widget, "Instagram Posts:\n", "title")
                for post in posts:
                    safe_insert_text(output_widget, f"Timestamp: {post['timestamp']}\n", "timestamp")
                    safe_insert_text(output_widget, f"Caption: {post.get('caption', 'No caption')}\n", "caption")
                    if post['media_type'] == 'IMAGE':
                        safe_insert_text(output_widget, f"Image URL: {post['media_url']}\n", "url")
                    elif post['media_type'] == 'VIDEO':
                        safe_insert_text(output_widget, f"Video URL: {post['media_url']}\n", "url")
                    safe_insert_text(output_widget, "-" * 50 + "\n")
            else:
                safe_insert_text(output_widget, "No posts found on Instagram.\n", "error")
        else:
            safe_insert_text(output_widget, f"Error fetching posts: {response.status_code}\n", "error")
    except requests.exceptions.RequestException as e:
        safe_insert_text(output_widget, f"Network error: {e}\n", "error")

# Function to fetch Reddit posts
def fetch_reddit_posts(client_id, client_secret, user_agent, subreddit, output_widget):
    token_url = "https://www.reddit.com/api/v1/access_token"
    data = {
        "grant_type": "client_credentials"
    }
    auth = (client_id, client_secret)
    headers = {"User-Agent": user_agent}

    try:
        token_response = requests.post(token_url, data=data, auth=auth, headers=headers)
        if token_response.status_code == 200:
            access_token = token_response.json().get("access_token")
        else:
            safe_insert_text(output_widget, f"Error fetching access token: {token_response.status_code}\n", "error")
            return

        api_url = f"https://oauth.reddit.com/r/{subreddit}/hot"
        headers["Authorization"] = f"Bearer {access_token}"
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if "data" in data and "children" in data["data"]:
                safe_insert_text(output_widget, f"Posts from subreddit: {subreddit}\n", "title")
                for post in data["data"]["children"]:
                    post_data = post["data"]
                    safe_insert_text(output_widget, f"Title: {post_data.get('title', 'No title')}\n", "title")
                    safe_insert_text(output_widget, f"Author: {post_data.get('author', 'Unknown')}\n", "author")
                    safe_insert_text(output_widget, f"Upvotes: {post_data.get('ups', 0)}\n", "upvotes")
                    safe_insert_text(output_widget, f"Permalink: https://reddit.com{post_data.get('permalink', '')}\n", "url")
                    safe_insert_text(output_widget, "-" * 50 + "\n")
            else:
                safe_insert_text(output_widget, "No posts found or an error occurred.\n", "error")
        else:
            safe_insert_text(output_widget, f"Error fetching posts: {response.status_code}\n", "error")
    except requests.exceptions.RequestException as e:
        safe_insert_text(output_widget, f"Network error: {e}\n", "error")

# Function to auto-refresh Instagram and Reddit posts
def auto_refresh(instagram_output, reddit_output, instagram_window, reddit_window, thread_index):
    # Refresh Instagram data
    fetch_instagram_posts(instagram_access_token, user_id, instagram_output)

    # Refresh Reddit data
    fetch_reddit_posts(client_id, client_secret, user_agent, subreddit, reddit_output)

    # Schedule the next refresh after 10 seconds
    instagram_window.after(10000, auto_refresh, instagram_output, reddit_output, instagram_window, reddit_window, thread_index)

# GUI Setup
root = tk.Tk()
root.title("Social Media Fetcher")
root.geometry("800x600")
root.config(bg="#FFFFFF")  # White background color

# Custom Font for Title
title_font = font.Font(family="Helvetica", size=24, weight="bold")

# Header Label
header_label = tk.Label(root, text="Social Media Fetcher", font=title_font, bg="#FFFFFF", fg="#C2185B")
header_label.pack(pady=20)

# Entry to input the number of threads using Spinbox
tk.Label(root, text="Enter number of threads:", font=("Arial", 14), bg="#FFFFFF", fg="black").pack(pady=10)

# Spinbox with custom styling
threads_spinbox = tk.Spinbox(root, from_=1, to=50, width=15, font=("Arial", 14), bd=8, relief="ridge", highlightthickness=0,
                             bg="#F8BBD0", fg="black", insertbackground="black", justify="left")
threads_spinbox.pack(pady=40)

# Radio buttons to choose between Sequential and Parallel
fetch_type_var = tk.StringVar(value="Sequential")

# Customizing RadioButton to make it look stylish
def style_radiobutton():
    return {
        "font": ("Arial", 14, "bold"),
        "fg": "black",
        "bg": "#FFFFFF",
        "relief": "flat",
        "width": 15,
        "height": 2,
        "padx": 20,
        "pady": 5,
        "activebackground": "#F48FB1",
        "activeforeground": "white",
        "selectcolor": "#F8BBD0",
        "highlightthickness": 0
    }

# Add the customized Radiobuttons
tk.Radiobutton(root, text="Sequential fetching", variable=fetch_type_var, value="Sequential", **style_radiobutton()).pack(pady=10)
tk.Radiobutton(root, text="Parallel fetching", variable=fetch_type_var, value="Parallel", **style_radiobutton()).pack(pady=10)

# Function to fetch both Instagram and Reddit posts based on user's choice (Sequential or Parallel)
def fetch_posts():
    num_threads = int(threads_spinbox.get())  # Get number of threads from the spinbox widget
    fetch_type = fetch_type_var.get()  # Get the fetch type (Sequential or Parallel)

    def create_windows(thread_index):
        # Instagram Window
        instagram_window = tk.Toplevel(root)
        instagram_window.title(f"Instagram Posts - Thread {thread_index + 1}")
        instagram_window.config(bg="#E1BEE7")  # Light pastel purple
        instagram_output = scrolledtext.ScrolledText(instagram_window, width=80, height=20, wrap=tk.WORD, font=("Arial", 12))
        instagram_output.pack(padx=10, pady=10)

        # Reddit Window
        reddit_window = tk.Toplevel(root)
        reddit_window.title(f"Reddit Posts - Thread {thread_index + 1}")
        reddit_window.config(bg="#B2EBF2")  # Light pastel blue
        reddit_output = scrolledtext.ScrolledText(reddit_window, width=80, height=20, wrap=tk.WORD, font=("Arial", 12))
        reddit_output.pack(padx=10, pady=10)

        return instagram_window, reddit_window, instagram_output, reddit_output

    def run_sequential():
        for i in range(num_threads):
            instagram_window, reddit_window, instagram_output, reddit_output = create_windows(i)

            # Fetch Instagram and Reddit data sequentially
            fetch_instagram_posts(instagram_access_token, user_id, instagram_output)
            fetch_reddit_posts(client_id, client_secret, user_agent, subreddit, reddit_output)

            # Start auto-refresh for each thread
            auto_refresh(instagram_output, reddit_output, instagram_window, reddit_window, i)

            # Delay between threads
            time.sleep(3) 
    def run_parallel():
        for i in range(num_threads):
            instagram_window, reddit_window, instagram_output, reddit_output = create_windows(i)

            # Start threads for Instagram and Reddit
            threading.Thread(target=fetch_instagram_posts, args=(instagram_access_token, user_id, instagram_output), daemon=True).start()
            threading.Thread(target=fetch_reddit_posts, args=(client_id, client_secret, user_agent, subreddit, reddit_output), daemon=True).start()

            # Start auto-refresh for each thread
            auto_refresh(instagram_output, reddit_output, instagram_window, reddit_window, i)

    # Run sequential or parallel based on the selection
    if fetch_type == "Sequential":
        run_sequential()
    elif fetch_type == "Parallel":
        run_parallel()

# Button to fetch posts with rounded corners
fetch_button = tk.Button(root, text="Fetch Posts", font=("Arial", 14, "bold"), bg="#C2185B", fg="white", relief="raised", bd=5, command=fetch_posts, activebackground="#D81B60", activeforeground="white")
fetch_button.pack(pady=30)

# Instagram API credentials
instagram_access_token = "IGQWRQV3JhdjFYbHlHaXB6T0RnWGVzQktxZAlFDYWxYU3ZA3UEJjMVBQMDBqTDFSaFYwSDVnRjBVc2ZAFTHFkSTBIMXdyTExKSndJQThPazIyWG5FMTV0ZAUdGY1Q0d2JDTG9YNEVCelI2eHVxSE1Obk1vbmFvYjBGNUUZD"
user_id = "17841470995138639"


# Reddit API credentials
client_id = "eGr75IVmOzsonvIl3UklxA"
client_secret = "oQZl9CAkaul6EGpw0QuslM2-gysbuw"
user_agent = "Ytest/1.0 by Practical-Traffic456"
subreddit = "learnpython"


# Run the main loop
root.mainloop()
