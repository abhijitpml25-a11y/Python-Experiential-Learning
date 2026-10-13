# CalcLab — Python Scientific Calculator

A responsive scientific calculator built with **Python, Flask, HTML, CSS and JavaScript** for the Experiential Learning Python project.

## Features

- Basic arithmetic: addition, subtraction, multiplication, division, modulo and floor division
- Mathematical expressions with parentheses and exponentiation (`^` or `**`)
- Scientific functions: `sqrt`, `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `log`, `ln`, `abs`, `factorial`, `exp`
- Constants: `pi`, `e`, `tau`
- Trigonometric functions use degrees
- Clear input validation and readable error messages
- Recent calculations saved in the browser with local storage
- Responsive layout for desktop and mobile
- Safe, allow-listed expression evaluation (does not use Python `eval`)
- Health-check endpoint at `/health`

## Run locally

Requires Python 3.10 or newer.

```bash
python -m venv .venv
```

Activate it:

**Windows PowerShell**
```powershell
.venv\Scripts\Activate.ps1
```

**macOS/Linux**
```bash
source .venv/bin/activate
```

Install and run:

```bash
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000.

## Example expressions

| Expression | Result |
|---|---:|
| `12 + 8 * 2` | `28` |
| `(12 + 8) / 4` | `5` |
| `sqrt(81)` | `9` |
| `sin(30)` | `0.5` |
| `log(100)` | `2` |
| `2^8` | `256` |
| `factorial(5)` | `120` |
| `pi * 2` | approximately `6.28318530718` |

## Deploy to Render

1. Extract the ZIP file.
2. Create a new public repository on GitHub, for example `python-experiential-learning-calculator`.
3. Open a terminal in the extracted project folder and run:

   ```bash
   git init
   git add .
   git commit -m "Initial Flask scientific calculator"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
   git push -u origin main
   ```

   Replace the remote URL with your actual GitHub repository URL. Create the empty repository on GitHub first; do not add a README there if you already use this project's README.

4. Sign in to Render and choose **New + → Web Service**.
5. Connect the GitHub repository.
6. Use these settings:
   - **Runtime:** Python
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `gunicorn app:app`
7. Click **Deploy Web Service**. Render will install dependencies and build the site.
8. Open the Render URL shown on the service page. Visit `/health` to confirm the service returns `{"status":"ok"}`.

The included `render.yaml` also describes the service configuration for Render Blueprint deployments.

## API

`POST /calculate`

Request JSON:
```json
{"expression": "sqrt(81) + sin(30)"}
```

Successful response:
```json
{"ok": true, "expression": "sqrt(81) + sin(30)", "result": 9.5}
```

Invalid expressions return HTTP `400` with an `error` message.

## Project structure

```text
Experiential_Learning_Python_Calculator/
├── app.py
├── requirements.txt
├── Procfile
├── render.yaml
├── README.md
├── .gitignore
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
└── tests/
    └── test_calculator.py
```

## Academic project details

- **Project:** Calculator in Python
- **Course / Code:** CM25002
- **Student:** Amit Japulkar
