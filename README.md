# Breeze ChMS API Service

A FastAPI-based service that wraps the Breeze Church Management System API, providing a modern, type-safe interface for interacting with Breeze ChMS.

## Features

- Complete coverage of Breeze ChMS API endpoints
- Modern FastAPI implementation with automatic OpenAPI documentation
- Type-safe request and response models
- Organized endpoint structure following REST best practices
- Error handling and validation

## API Sections

- People Management
- Events Management
- Contributions Management
- Campaigns Management
- Tags Management
- Forms Management
- Volunteers Management
- Profile Management

## Getting Started

1. Clone the repository:
```bash
git clone https://github.com/drtonylove1963/breeze-service.git
cd breeze-service
```

2. Create a `.env` file with your Breeze credentials:
```
breeze_url=your_breeze_url
api_key=your_api_key
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the server:
```bash
python main.py
```

The API will be available at:
- API Documentation: http://localhost:8000/docs
- Alternative Documentation: http://localhost:8000/redoc

## API Documentation

Full API documentation is available through the Swagger UI at `/docs` or ReDoc at `/redoc` when the server is running.
