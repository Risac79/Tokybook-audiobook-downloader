# **TokyoBook Audiobook Downloader**  

This script allows you to **automatically download** audiobook chapters from [TokyoBook](https://tokybook.com/) in one go.  
It extracts `.mp3` chapter links from a given audiobook page and downloads them into a **folder named after the book**.  

---

## **📥 Features**  
✅ Supports **TokyoBook.com** audiobooks  
✅ Creates a folder **named after the book**  
✅ Extracts and downloads **all chapters automatically**  
✅ Displays a **progress bar** while downloading  

---

## **🚀 How to Use**

### **1️⃣ Chmod script**
After cloning the repo, make the script executable:
```bash
chmod +x download_book.sh
```
### **2️⃣ Run the Script**  

Simply execute the script:  
```sh
./download_book url
```
For example:
```sh
./download_book https://tokybook.com/providence-the-beginning-after-the-end-book-11
```

The chapters will be downloaded into a **folder named after the audiobook**.

---

## **🔍 How It Works**
1. **Automatically deactivates existing venv**, creates a new one and installs all requirements.
2. **Scrapes the audiobook page** to get the book title and chapter links.  
3. **Creates a folder** named after the audiobook.  
4. **Downloads each chapter** as an `.mp3` file with a progress bar.
5. **Retries chapters 30 times** when chapter fails to download.
6. **Deactivates** created venv.  

---

## **📌 Notes**
- The script **only works with** [TokyoBook](https://tokybook.com/) audiobooks.  
- Chapter filenames are saved as **`chapter 1.mp3`, `chapter 2.mp3`, etc.**  
- If the book title contains **invalid characters**, they will be replaced automatically.  
- If you **re-run the script**, it may overwrite existing files if they already exist in the folder.  

---

### **👨‍💻 Author**  
Developed with ❤️ using Python. Contributions and suggestions are welcome!  
Further fiddled with by Risac.
