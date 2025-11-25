# Resume Builder AI - FastAPI Edition

A professional resume generation tool with AI assistance, featuring dual interfaces and secure authentication.

## Quick Start

### Prerequisites
- Python 3.7+ installed on your system
- pip package manager

### 1. Set Up Environment

```bash
# Navigate to project directory
cd resume_builder_ai

# Create and activate virtual environment
python -m venv myenv

# Windows
myenv\Scripts\activate

# macOS/Linux
source myenv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Authentication

Your login credentials are stored in `src/db/auth.py`:

```python
# src/db/auth.py
USERS = {
    "username": "password123",
    "password": "mypassword"
}
```

Add or modify usernames and passwords in this dictionary as needed.

### 3. Launch the Application

```bash
# Start the FastAPI server
uvicorn main:app --reload

# Or specify host and port
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The application will be available at `http://localhost:8000`

## 📁 Project Structure

```
resume_builder_ai/
├── 📄 main.py                          # FastAPI application entry point
├── 📦 requirements.txt                  # Python dependencies
│
├── 📂 src/
│   ├── 📂 api/                         # API routes (if needed)
│   ├── 📂 db/
│   │   └── auth.py                     # User credentials dictionary
│   ├── 📂 models/
│   │   └── login.py                    # Pydantic models
│   ├── 📂 services/
│   │   ├── core.py                     # Core business logic
│   │   ├── docx_utils.py               # DOCX generation utilities
│   │   ├── extract_skills.py           # Skills extraction logic
│   │   ├── generate_pdfs.py            # PDF generation
│   │   ├── generate_resume.py          # Main resume generation
│   │   ├── ui.py                       # Gradio UI integration
│   │   └── utils.py                    # Helper functions
│   ├── 📂 static/
│   │   ├── favicon.ico
│   │   └── styles.css                  # Application styles
│   └── 📂 templates/
│       ├── baselayout.html             # Base template
│       ├── login.html                  # Login page
│       ├── create.html                 # Manual resume creation
│       ├── sam.html                    # Dashboard/selection page
│       └── _navheader.html             # Navigation header
│
├── 📂 dataset/                         # Training data and examples
├── 📂 json_files/                      # Generated JSON outputs
├── 📂 yaml_files/                      # Generated YAML outputs
├── 📂 outputs/                         # Generated PDF/DOCX resumes
└── 📂 test/                            # Test files
```

## Application Flow

### 1. Login Screen
- Navigate to `http://localhost:8000`
- Redirects to `/login` if not authenticated
- Enter username and password from `src/db/auth.py`
- Successful login redirects to dashboard

### 2. Dashboard (Post-Login)
After successful authentication, users see two options:

#### Option 1: Gradio Interface (Default AI-Powered)
- **Route**: `/gradio`
- **Description**: Embedded Gradio interface using iframe
- **Features**:
  - AI-powered resume generation
  - Interactive UI with conversational interface
  - Quick resume generation from minimal input

#### Option 2: Manual Form Entry
- **Route**: `/create`
- **Description**: Detailed form-based resume builder
- **Input Fields**:
  - **Personal Information**:
    - Full Name
    - Address
    - Phone Number
    - Email
    - GitHub URL
    - LinkedIn URL
  - **Work Experience** (List):
    - Company Name
    - Position/Title
    - Duration
    - Responsibilities/Achievements
  - **Skills** (List):
    - Technical skills
    - Soft skills
    - Languages, etc.
  - **Projects** (List):
    - Project Name
    - Description
    - Technologies Used
    - Links (if applicable)
  - **Additional Information**:
    - Availability (Full-time/Part-time/Contract)
    - Professional Summary
    - Certifications (optional)
    - Education (optional)

### 3. Resume Generation
- Form submission processes data through `src/services/generate_resume.py`
- Generates both DOCX and PDF formats in Harvard style
- Outputs saved to `outputs/` directory with timestamp
- Format: `{job_title}_{date}_{time}.{docx|pdf}`

## Key Features

### Authentication & Security
- Session-based authentication
- Credentials stored in `src/db/auth.py`
- Protected routes requiring login
- Logout functionality

### Dual Interface Options
1. **Gradio Interface**: Quick, AI-assisted resume generation
2. **Manual Form**: Detailed, customizable resume creation

### Harvard Format Resume
- Professional formatting
- ATS-friendly layout
- Clean, readable design
- PDF and DOCX outputs

### File Management
- Timestamped file naming prevents overwrites
- Organized output directories
- JSON and YAML export options

## API Endpoints

### Public Routes
- `GET /` - Root (redirects to login or dashboard)
- `GET /login` - Login page
- `POST /login` - Handle login submission

### Protected Routes (Require Authentication)
- `GET /dashboard` - Main dashboard with two options
- `GET /gradio` - Gradio interface (iframe)
- `GET /create` - Manual resume creation form
- `POST /generate-resume` - Process form and generate resume
- `GET /download/{filename}` - Download generated files
- `GET /logout` - User logout

## Requirements

Create a `requirements.txt` file with:

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
jinja2==3.1.2
python-multipart==0.0.6
python-docx==1.1.0
reportlab==4.0.7
PyPDF2==3.0.1
pyyaml==6.0.1
gradio==4.7.1
```

## Running in Production

### Using Uvicorn with Workers
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Using Gunicorn with Uvicorn Workers
```bash
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```


## Usage Guide

1. **Start the server**: Run `uvicorn main:app --reload`
2. **Access login**: Navigate to `http://localhost:8000`
3. **Login**: Use credentials from `src/db/auth.py`
4. **Choose interface**:
   - Click "Use Gradio Interface" for AI-assisted generation
   - Click "Create Manually" for detailed form entry
5. **Generate resume**: Fill in information and submit
6. **Download**: Find your resume in `outputs/` directory or download directly

## Tips & Best Practices

- Keep credentials in `src/db/auth.py` secure (consider environment variables)
- Regularly backup your `outputs/` directory
- Use descriptive job titles for better file naming
- Review generated resumes before using
- Keep the application updated with `pip install -U -r requirements.txt`

## Troubleshooting

### Port Already in Use
```bash
# Use a different port
uvicorn main:app --port 8001
```

### Module Not Found Errors
```bash
# Ensure you're in the virtual environment
# Reinstall dependencies
pip install -r requirements.txt
```

### Template Not Found
- Verify `src/templates/` directory exists
- Check template file names match routes

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request with clear description

## License

This project is open source and available under the MIT License.

---

**Author:** Milan Shrestha  
**Version:** 2.0.0 (FastAPI Edition)  
**Last Updated:** November 2025


#TODO: update to using Poetry instead of virtual env