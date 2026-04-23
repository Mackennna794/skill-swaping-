# Skill Swap Platform

A modular, structured, and beginner-friendly Skill Swapping application built with Streamlit and SQLite.

## Core Features
* **Authentication:** Secure registration and login with SHA-256 hashed passwords. Session states ensure safe navigation.
* **Profile Management:** Set bios and choose standard "Skills Offered" and "Skills Wanted" from predefined tags.
* **Dashboard:** Discover users, filter by tags, and read average ratings inside a clean card-based UI.
* **Messaging System:** Send messages directly from the dashboard. View sent and received histories in the inbox. Includes spam prevention against duplicate messages.
* **Review System:** Rate users (1-5 stars) and leave text feedback.

## Setup Instructions

1.  **Create Project Folder**
    Make sure your files follow the structure exactly (with a `pages/` folder for the inner Streamlit pages).

2.  **Install Requirements**
    Run the following in your VS Code terminal:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Application**
    Execute the app using Streamlit:
    ```bash
    streamlit run app.py
    ```
    *Note: The SQLite database (`skill_swap.db`) will be created automatically upon the first run.*