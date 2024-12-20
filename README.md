# Social Media Fetcher

This project provides a GUI-based tool for fetching posts from Instagram and Reddit using their respective APIs. The application is implemented in Python, leveraging threading for parallel fetching and a user-friendly interface built with Tkinter.

## Features

- **Fetch Instagram Posts**: Retrieve media posts from a user's Instagram account, including captions, timestamps, and media URLs.
- **Fetch Reddit Posts**: Retrieve hot posts from a specified subreddit, including titles, authors, upvotes, and links.
- **Sequential or Parallel Fetching**: Choose between sequential or multi-threaded fetching for better performance.
- **Auto-Refresh**: Automatically refreshes data every 10 seconds to keep the feed updated.
- **Customizable Threads**: User-defined number of threads for parallel fetching.
- **User-Friendly Interface**: Stylish GUI with color-coded themes for Instagram and Reddit windows.

## How It Works

1. **API Integration**:
   - **Instagram**: Uses the Instagram Graph API to fetch posts for a given user ID.
   - **Reddit**: Uses Reddit's OAuth-based API to fetch hot posts from a subreddit.
2. **Threading**:
   - Supports multi-threading for parallel fetching of Instagram and Reddit posts.
3. **Auto-Refresh**:
   - Scheduled auto-refresh updates the fetched data every 10 seconds.

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Required libraries:
  - `requests`
  - `tkinter` (comes pre-installed with Python)
  - `threading`
  - `queue`

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Install the required libraries:
   ```bash
   pip install requests
   ```
3. Update the API credentials in the script:
   - **Instagram**:
     - `instagram_access_token`: Replace with a valid access token.
     - `user_id`: Replace with the user ID for the Instagram account.
   - **Reddit**:
     - `client_id`, `client_secret`, and `user_agent`: Replace with valid Reddit API credentials.
     - `subreddit`: Specify the subreddit to fetch posts from.

## Usage

1. Run the script:
   ```bash
   python social_media_fetcher.py
   ```
2. Enter the number of threads and select the fetching type (Sequential or Parallel).
3. Click "Fetch Posts" to start fetching Instagram and Reddit posts.
4. View the fetched posts in separate windows for Instagram and Reddit.

## GUI Components

- **Header**: Displays the application title with a custom font.
- **Thread Input**: Spinbox for specifying the number of threads.
- **Fetch Type**: Radio buttons to choose between sequential and parallel fetching.
- **Fetch Button**: Stylish button to initiate the fetching process.
- **Output Windows**: Separate scrollable text areas for displaying fetched Instagram and Reddit posts.

## Example Output

### Instagram
```
Instagram Posts:
Timestamp: 2024-12-20T12:34:56
Caption: Beautiful sunset over the mountains.
Image URL: https://example.com/media/123
--------------------------------------------------
```

### Reddit
```
Posts from subreddit: learnpython
Title: How to start with Python?
Author: python_enthusiast
Upvotes: 123
Permalink: https://reddit.com/r/learnpython/123
--------------------------------------------------
```

## Customization

- **Auto-Refresh Interval**: Modify the `10000` ms parameter in the `auto_refresh` function to change the refresh rate.
- **GUI Themes**: Customize the color schemes for Instagram and Reddit windows.
- **Thread Limits**: Adjust the range of the spinbox for thread selection.

## Limitations

- Requires valid API credentials for Instagram and Reddit.
- API rate limits may affect performance.
