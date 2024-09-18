# README for Text Steganography App

## Project Overview

This project is a **Text Steganography App** designed as a blog website where users can create and read blogs with hidden messages. The application uses Flask for the backend and Bootstrap for the frontend, providing a responsive and user-friendly interface. The AES algorithm is employed to encode blog content, ensuring that sensitive information is securely embedded within the text, and the main message encrypting and decrypting algorithm is in stego.py.

## Features

1. **User Roles**:
   - **Agent User**: Can view blogs with hidden messages and create new blogs containing secret information.
   - **Admin**: Has full control to create, read, update, and delete (CRUD) users and blogs.

2. **Blog Creation**:
   - Users can write blogs, and the content can include hidden messages encoded using AES encryption.

3. **Steganography**:
   - The `stego.py` module handles the embedding of secret information within the blog text, ensuring that only authorized users can access the hidden messages.

4. **User Management**:
   - Admins can manage user accounts, allowing for the addition, modification, or removal of users.

5. **Responsive Design**:
   - The application utilizes Bootstrap to ensure a seamless experience across various devices.

6. **API Integration**:
   - The backend exposes APIs for blog management and user authentication, facilitating interaction with the frontend.
  
## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, Bootstrap
- **Encryption**: AES algorithm for encoding blog content
- **Steganography**: `stego.py` for embedding hidden messages
- **Database**: MySQL - Workbench

## Installation Instructions

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   ```

2. **Navigate to the Project Directory**:
   ```bash
   cd text-steganography-app
   ```

3. **Install Required Packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the Database**:
   - Uncomment the script in models.py, `with app.app_context():` section to create sample database, and then comment them.
   - Run migrations if applicable.

5. **Run the Application**:
   ```bash
   python app.py
   ```

6. **Access the Application**:
   - Open your web browser and go to `http://localhost:5000`.

## Usage

- **User Registration and Login**: Users can register and log in to their accounts.
- **Create Blog**: Logged-in users can create new blogs with hidden messages.
- **View Blogs**: All users can read blogs, while only agent users and admins can see hidden messages.
- **Admin Dashboard**: Admin users can manage users and blogs through a dedicated dashboard.

## Video demo

https://drive.google.com/file/d/1dQ4YPSJJaphWjC4Y-wPjn04B67xFuPWc/view?usp=sharing

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

---

Feel free to adjust any sections as needed to better fit your project!
