# Resume Builder AI

A streamlined tool for generating professional resumes using structured YAML input and a clean web interface.

## Quick Start

### Prerequisites
- Python 3.7+ installed on your system

### 1. Set Up Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/resume_builder_ai.git
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

### 2. Configure Your Resume

```bash
# Copy the sample template
cp sample_resume_skeleton.yaml resume_skeleton.yaml

# Edit with your personal information
# Follow the structure provided in the sample file
```

### 3. Launch the Application

**Windows:**
```bash
./run_ui.bat
```

**macOS/Linux:**
```bash
./run_ui.sh
```

This will start a local web server and open your browser to the resume builder interface.

## 📁 Project Structure

```
resume_builder_ai/
├── 📄 run_ui.bat              # Windows launcher
├── 📄 run_ui.sh               # Unix launcher  
├── 🐍 ui.py                   # Web interface
├── 🐍 generate_resume.py      # Resume generation logic
├── 📝 sample_resume_skeleton.yaml  # Template file
├── 📝 resume_skeleton.yaml    # Your resume data
├── 📦 requirements.txt        # Python dependencies
├── 📂 outputs/               # Generated PDFs
└── 📂 myenv/                 # Virtual environment
```

## Usage

1. **Edit your data**: Modify `resume_skeleton.yaml` with your personal information
2. **Run the app**: Execute the appropriate launcher script for your OS
3. **Generate PDF**: Use the web interface to create and download your resume
4. **Find output**: Generated resumes are saved in the `outputs/` directory

## Requirements

All Python dependencies are managed through `requirements.txt`. The application uses:
- Flask for the web interface
- ReportLab/WeasyPrint for PDF generation
- PyYAML for configuration parsing

## Tips

- Keep your YAML structure consistent with the sample file
- Regularly backup your `resume_skeleton.yaml` file
- Generated PDFs are timestamped to avoid overwrites

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the [MIT License](LICENSE).

---

**Author:** Milan Shrestha