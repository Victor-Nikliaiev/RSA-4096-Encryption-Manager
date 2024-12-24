[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![PySide6](https://img.shields.io/badge/Framework-PySide6-green.svg)](https://doc.qt.io/qtforpython/)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-black.svg)](https://github.com/your-repo-link)


# RSA-4096 Encryption Manager v1.0

## Overview
The **RSA-4096 Encryption Manager v1.0** is a medium-sized, moderately complex desktop application designed to provide a secure, efficient, and user-friendly solution for file encryption, decryption, and key management. This project leverages advanced cryptographic algorithms and a modern GUI to meet the needs of both casual users and professionals seeking secure file handling.

Built using **PySide6**, the app showcases a modular architecture, dynamic user experience features, and localization support, making it a versatile tool for global audiences.

---

## Features

### Core Functionalities

1. **File Encryption**
   - **Description**: Securely encrypt files to protect sensitive information using robust cryptographic algorithms.
   - **Tools Used**:
     - **Python's `cryptography` library**: Implements encryption and secure key generation.
     - **PySide6**: Provides GUI components for file selection and displaying encryption results.

2. **File Decryption**
   - **Description**: Allows users to decrypt previously encrypted files to access their original content with accuracy.
   - **Tools Used**:
     - **`cryptography` library**: Ensures reliable decryption matching the encryption process.
     - **PySide6 Widgets**: Creates a user-friendly interface for inputting decryption keys and file selection.

3. **Key Management**
   - **Description**: Enables generating, exporting, and securely managing cryptographic keys.
   - **Tools Used**:
     - **`cryptography` key generation functions**: Supports public-private and symmetric keys.
     - **PySide6 File Dialogs**: Facilitates exporting keys to user-defined locations.

---

### User Experience Features

4. **Modern UI Design**
   - **Description**: A visually appealing and intuitive interface for enhanced user interaction.
   - **Tools Used**:
     - **PySide6 Designer**: Designs UI layouts and integrates custom components.
     - **Global Stylesheets**: Ensures consistency across the application's themes.

5. **Drag-and-Drop Functionality**
   - **Description**: Allows users to drag files directly into the application for quick and easy processing.
   - **Tools Used**:
     - **PySide6 Drag-and-Drop APIs**: Simplifies file selection and enhances usability.

6. **Localization Support**
   - **Description**: Offers multi-language support to cater to global audiences.
   - **Tools Used**:
     - **PySide6 Translation Tools**: Manages `.ts` and `.qm` files for localization.
     - **Dynamic Translation Loading**: Applies language changes in real-time.

---

### Additional Features

7. **Glowing Animated Logo**
   - **Description**: Enhances the application's aesthetics with a visually engaging, glowing logo.
   - **Tools Used**:
     - **PySide6 Animation Framework**: Creates smooth and dynamic animations.
     - **Custom QSS Styles**: Adds glowing effects to the logo.

8. **Error Handling**
   - **Description**: Provides detailed error messages and alerts to guide users through potential issues.
   - **Tools Used**:
     - **Python Try-Except Blocks**: Handles backend exceptions like invalid keys or unsupported file formats.
     - **PySide6 Message Dialogs**: Displays user-friendly prompts for error resolution.

9. **Performance Optimization**
   - **Description**: Efficiently handles large files and complex operations without compromising performance.
   - **Tools Used**:
     - **Threading in PySide6**: Runs time-consuming tasks in the background.
     - **Buffered File Handling**: Processes large files in chunks for optimized memory usage.

---

## Project Structure

The application follows a modular structure, ensuring clarity, scalability, and maintainability:

- **`main.py`**: The entry point for initializing the application.
- **`backend`**: Contains core cryptographic logic and processing algorithms.
- **`components`**: Modular and reusable UI components shared across the application.
- **`screens`**: Dedicated screens for encryption, decryption, and key management functionalities.
- **`tools`**: Utility scripts supporting drag-and-drop, error handling, and other reusable functionality.
- **`assets`**: Houses static resources like icons, stylesheets, and images.
- **`translations`**: Manages localization files for multi-language support.

---

## Installation

### Prerequisites
- Python 3.8 or higher
- Virtual environment (recommended)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/Victor-Nikliaiev/encryption_app
   cd encryption_app
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

---

## Localization

To add or update translations:

1. Generate `.ts` files:
   ```bash
   pyside6-lupdate -extensions py,ui -recursive . -ts ./translations/<language>.ts
   ```

2. Edit translations using PySide6 Linguist:
   ```bash
   pyside6-linguist ./translations/<language>.ts
   ```

3. Compile `.qm` files:
   ```bash
   pyside6-lrelease ./translations/<language>.ts -qm ./translations/<language>.qm
   ```

---

## Contributing

You are most welcome for contributions to enhance the RSA-4096 Encryption Manager v1.0:

1. Fork the repository and create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Implement your feature or fix and commit changes:
   ```bash
   git commit -m "Description of your changes"
   ```

3. Push your changes:
   ```bash
   git push origin feature/your-feature-name
   ```

4. Submit a pull request.

---

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute as per the terms.

---

## Acknowledgments

- **Qt for Python (PySide6)**: Powers the application’s user interface.
- **Open Source Libraries**: The `cryptography` library and others enhance functionality.
- **Contributors**: Thanks to everyone who contributed to this project.

For more details, visit the [GitHub Repository](https://github.com/Victor-Nikliaiev/encryption_app).

