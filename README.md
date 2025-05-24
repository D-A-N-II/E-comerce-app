# BuyPest - Online Pesticide Store

A modern e-commerce application for selling pesticides, built with Flask and modern web technologies.

## Features
- Clean, modern UI inspired by popular e-commerce platforms
- Product listing with categories and filters
- Shopping cart functionality
- Responsive design
- Search functionality
- Indian currency support

## Setup Instructions

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create the `static/images` directory and add product images:
```bash
mkdir -p static/images
```

Add your product images to the static/images directory with names:
- product1.jpg (BugAway Pro Max)
- product2.jpg (WeedClear Ultra)
- product3.jpg (FungusGuard Premium)
- product4.jpg (CropShield Complete)
- product5.jpg (InsectKill Power)
- product6.jpg (WeedMaster Pro)

Recommended image specifications:
- Resolution: 800x800 pixels
- Format: JPG
- File size: < 500KB
- Background: White or light colored
- Clear product visualization

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to:
```
http://localhost:5000
```

## Directory Structure
```
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── static/            # Static files
│   └── images/        # Product images
├── templates/         # HTML templates
│   └── index.html    # Main page template
└── README.md         # This file
```

## Product Categories
- Insecticides
- Herbicides
- Fungicides
- Multi-purpose

## Features to Add
- User authentication
- Order processing
- Payment integration
- Admin panel
- Product reviews
- Stock management 