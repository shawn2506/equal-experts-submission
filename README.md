# **EQUAL EXPERTS ASSIGNMENT**

Welcome to the **DOUBLEE** Python module.
This project provides a lightweight FastAPI-based HTTP server that fetches Gists for any GitHub username.

---

## **📚 Table of Contents**

1. [Description](#description)
2. [Setup – Running Locally](#setup---how-to-run-the-script)

   * [Examples](#examples)
   * [Test Cases](#test-cases)
3. [Usage – Configuration & Details](#usage---configuration-options-and-additional-functionality)

---

## **📝 Description**

**Author:** Shawn Dsouza
**Date:** 2025-11-17
**Script Name:** `main.py`

This project runs a **FastAPI server** locally on:

```
http://localhost:8080
```

The API internally queries:

```
https://api.github.com/users/{username}/gists
```

You can test the application by accessing:

```
http://localhost:8080/{username}
```

Example usernames:

* `octocat`
* `shawn2506`

---

## **⚙️ Setup – How to Run the Script**

### **1. Create a virtual environment**

```sh
uv venv
```

### **2. Install dependencies**

```sh
uv pip install -r requirements.txt
```

### **3. Run the script locally**

```sh
uv run python main.py --reload --port 8080
```

### **4. Test endpoint**

```sh
curl http://localhost:8080/octocat
curl http://localhost:8080/shawn2506
```

---

## **🐳 Running as a Container**

Navigate to the project root and run:

```sh
podman build -t project:0.01 -f Dockerfile
podman run -p 8080:8080 localhost/project:0.01
```

---

## **🧪 Test Cases**

Tests are written using **pytest**.

Run the tests:

```sh
pytest tests.py
```

### **Example Output**

```
============================== test session starts ===============================
platform darwin -- Python 3.12.2, pytest-8.3.4, pluggy-1.5.0
rootdir: /Users/shawn2506/Documents/Projects/personal/demo/doublee
collected 3 items

tests.py ...                                                               [100%]

=============================== 3 passed in 0.74s ===============================
```

---

## **🔧 Usage – Configuration Options and Additional Functionality**

The application provides a simple API wrapper for GitHub Gists for any username.
It runs a FastAPI server that forwards requests to GitHub’s public API.