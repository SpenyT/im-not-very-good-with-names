# Server README

## Animal Identifier API - Backend Architecture

This is the backend server for the Animal Identifier application, built with Django and Python. The server handles image classification, information enrichment, and API endpoints for the frontend application.

---

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Project Structure](#project-structure)
- [Django Apps](#django-apps)
- [API Endpoints](#api-endpoints)
- [Setup and Installation](#setup-and-installation)
- [Configuration](#configuration)
- [Data Flow](#data-flow)
- [Dependencies](#dependencies)

---

## Architecture Overview

The backend follows a modular Django architecture with three primary applications that work together to process user requests:

```
User Image Upload → API Gateway → Classifier → Enrichment → Formatted Response
```

1. **API Gateway** (`animal_identifier_api`): Main Django project handling routing and configuration
2. **Classifier**: Deep learning model inference for species identification
3. **Enrichment**: LLM-powered RAG system for retrieving detailed species information
4. **Common**: Shared utilities and helper functions

---

## Project Structure

```
Server/
├── README.md                      # This file
├── animal_identifier_api/         # Main Django project
│   ├── settings.py               # Django configuration
│   ├── urls.py                   # Root URL configuration
│   ├── wsgi.py                   # WSGI application entry point
│   └── asgi.py                   # ASGI application entry point
├── classifier/                    # Image classification app
│   ├── apps.py                   # Image classification app
│   ├── models.py                 # Database models
│   ├── views.py                  # API endpoints for classification
│   ├── serializers.py            # Data serialization
│   └── services/                 # logic files
├── enrichment/                    # Information enrichment app
│   ├── models.py                 # Database models for species data
│   ├── views.py                  # API endpoints for enrichment
│   └── services/                 # LLM integration and RAG implementation
└── common/                        # Shared utilities
    ├── utils.py                  # Helper functions
    ├── exceptions.py             # Custom exceptions
    └── validators.py             # Input validators
```

---

## Django Apps

### 1. `animal_identifier_api` (Main Project)

The core Django project that orchestrates all components.

**Key Responsibilities:**
- Django settings and configuration management
- Root URL routing to application endpoints
- Middleware configuration (CORS, authentication, etc.)
- Database connection management
- Static file and media handling

**Key Files:**
- `settings.py`: Environment-specific configurations, installed apps, middleware stack
- `urls.py`: Routes requests to appropriate app endpoints
- `wsgi.py`/`asgi.py`: Production server interfaces

---

### 2. `classifier` App

Handles the core image classification functionality using deep learning models.

**Key Responsibilities:**
- Receives and validates uploaded animal images
- Preprocesses images for model inference (resizing, normalization, etc.)
- Runs the trained classification model (ResNet/EfficientNet)
- Returns predicted species with confidence scores
- Handles model loading and caching for performance

**Technical Details:**

**Image Processing Pipeline:**
```python
1. Image Upload (JPEG/PNG)
   ↓
2. Validation (format, size, content)
   ↓
3. Preprocessing (resize to 224x224, normalize) # subject to change
   ↓
4. Model Inference (TensorFlow/PyTorch)
   ↓
5. Post-processing (softmax, top-k predictions)
   ↓
6. Response (species + confidence score)
```

**Key Components:**
- **`inference.py`**: Contains the model inference logic # subject to change
  - Model loading and initialization
  - Image preprocessing functions
  - Prediction generation with confidence thresholds
  - Error handling for invalid images or failed predictions

- **`views.py`**: REST API endpoints
  - `POST /api/classify/`: Accepts multipart form data with image
  - Input validation and error responses
  - Async processing for large images (optional)

- **`ml_models/`**: Directory containing trained model weights # subject to change
  - Serialized model files (.h5, .pth, .pb)
  - Model configuration files
  - Class label mappings (species index → scientific name)

**Model Architecture:** # subject to change
- Base architecture: ResNet-50 / EfficientNet-B0 (fine-tuned)
- Input: RGB images (224x224x3)
- Output: Probability distribution over animal species classes
- Number of classes: [Your model's class count]

---

### 3. `enrichment` App

Implements a Retrieval-Augmented Generation (RAG) system to provide detailed educational information about identified species.

**Key Responsibilities:**
- Receives species identification from classifier
- Queries vector database for relevant species information
- Uses LLM to generate comprehensive, educational descriptions
- Structures output with taxonomic data, habitat, diet, conservation status, etc.
- Caches responses for common species

**Technical Details:** # subject to change

**RAG Pipeline:**
```python
1. Species Name Input (e.g., "Panthera tigris")
   ↓
2. Vector Database Query
   ↓
3. Retrieve Relevant Documents (top-k similarity)
   ↓
4. Context Assembly (combine retrieved documents)
   ↓
5. LLM Prompt Construction
   ↓
6. Generate Enriched Response
   ↓
7. Structure Output (scientific name, common name, facts)
```

**Key Components:** # subject to change

- **`rag_pipeline.py`**: RAG implementation 
  - Vector embedding generation for queries
  - Similarity search in knowledge base
  - Document retrieval and ranking
  - Context window management for LLM input

- **`llm_handler.py`**: LLM integration layer
  - API client for LLM service (OpenAI, Anthropic, or local model)
  - Prompt template management
  - Response parsing and validation
  - Rate limiting and error handling
  - Streaming support for real-time responses

- **`knowledge_base/`**: Vector store and source documents
  - Vector embeddings (FAISS/Chroma/Pinecone)
  - Source documents (Wikipedia, scientific papers, wildlife databases)
  - Metadata (sources, reliability scores, timestamps)

**Information Output Structure:** # subject to change
```json
{
  "scientific_name": "Panthera tigris",
  "common_name": "Tiger",
  "taxonomy": {
    "kingdom": "Animalia",
    "phylum": "Chordata",
    "class": "Mammalia",
    "order": "Carnivora",
    "family": "Felidae"
  },
  "habitat": "Tropical forests, grasslands...",
  "diet": "Carnivorous - deer, wild boar...",
  "conservation_status": "Endangered",
  "interesting_facts": [...],
  "sources": [...]
}
```

---

### 4. `common` App

Shared utilities and helper functions used across the project.

**Key Components:**
- **`utils.py`**: Generic helper functions
  - Image format conversion
  - File size validation
  - Logging utilities
  - Performance monitoring helpers

- **`exceptions.py`**: Custom exception classes
  - `InvalidImageException`
  - `ModelInferenceException`
  - `EnrichmentException`

- **`validators.py`**: Input validation functions
  - Image format validators
  - File size checkers
  - Species name validators

---

## API Endpoints

### Classification Endpoints

#### `POST /api/classify/`
Classify an uploaded animal image.

**Request:**
```http
POST /api/classify/
Content-Type: multipart/form-data

image: [binary file data]
```

**Response:**
```json
{
  "success": true,
  "predictions": [
    {
      "species": "Panthera tigris",
      "common_name": "Tiger",
      "confidence": 0.96
    },
    {
      "species": "Panthera leo",
      "common_name": "Lion",
      "confidence": 0.03
    }
  ],
  "processing_time_ms": 234
}
```

---

### Enrichment Endpoints

#### `GET /api/enrich/{species_name}/`
Retrieve detailed information about a species.

**Request:**
```http
GET /api/enrich/Panthera%20tigris/
```

**Response:**
```json
{
  "success": true,
  "data": {
    "scientific_name": "Panthera tigris",
    "common_name": "Tiger",
    "taxonomy": { ... },
    "habitat": "...",
    "diet": "...",
    "conservation_status": "Endangered",
    "interesting_facts": [...],
    "sources": [...]
  }
}
```

---

### Combined Endpoint (subject to change)

#### `POST /api/identify/` 
One-stop endpoint that performs classification and enrichment in a single request.

**Request:**
```http
POST /api/identify/
Content-Type: multipart/form-data

image: [binary file data]
```

**Response:**
```json
{
  "success": true,
  "classification": {
    "species": "Panthera tigris",
    "confidence": 0.96
  },
  "information": {
    "scientific_name": "Panthera tigris",
    "common_name": "Tiger",
    "taxonomy": { ... },
    "habitat": "...",
    "diet": "...",
    "conservation_status": "Endangered",
    "interesting_facts": [...]
  }
}
```

---

## Setup and Installation # subject to change

### Prerequisites

- Python 3.9+
- pip
- Virtual environment tool (venv/virtualenv)
- PostgreSQL/MySQL (or SQLite for development)

### Installation Steps 

```bash
# 1. Clone the repository and navigate to server directory
cd Server/

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env with your configuration

# 5. Run migrations
python manage.py migrate

# 6. Download model weights
python manage.py download_models  # Custom management command

# 7. Build vector database (first time only)
python manage.py build_knowledge_base

# 8. Run development server
python manage.py runserver
```

---

## Configuration

### Environment Variables

Create a `.env` file in the server root with the following variables:

```bash
# Django Settings

```

---

## Data Flow

### Complete Request Flow

```
1. User uploads image via frontend
   ↓
2. Request hits Django API Gateway
   ↓
3. Image validation (format, size)
   ↓
4. Classifier app receives image
   ↓
5. Image preprocessing
   ↓
6. Model inference → Species prediction
   ↓
7. Species name passed to Enrichment app
   ↓
8. Vector DB query for relevant documents
   ↓
9. LLM generates enriched description
   ↓
10. Structured response assembled
   ↓
11. JSON response returned to frontend
   ↓
12. Frontend displays results to user
```

### Error Handling Flow

- Invalid image → 400 Bad Request with error message
- Model failure → 500 Internal Server Error, logged for debugging
- LLM API failure → Returns classification only, enrichment marked as unavailable
- Database failure → Graceful degradation with cached responses

---

## Dependencies

### Core Framework
- **Django 4.2+**: Web framework
- **Django REST Framework**: API development
- **django-cors-headers**: CORS support

### Machine Learning
- **TensorFlow 2.x** or **PyTorch 2.x**: Deep learning framework
- **numpy**: Numerical operations

### LLM & RAG
- **TBD**

### Database
- **TBD**

### Utilities
- **python-dotenv**: Environment variable management
- **TBD**

---

## Performance Considerations

### Optimization Strategies

1. **Model Caching**: Models are loaded once at startup and kept in memory
2. **Response Caching**: Common species information cached in Redis (1 hour TTL)
3. **Async Processing**: Long-running LLM calls can be processed asynchronously
4. **Image Compression**: Large images automatically resized before processing
5. **Connection Pooling**: Database connections pooled for concurrent requests

### Monitoring

- Request timing logged for all endpoints
- Model inference time tracked separately
- LLM API call latency monitored
- Error rates tracked per endpoint

---

## Development

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test classifier
python manage.py test enrichment

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```
---

## Deployment

### Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Configure production database
- [ ] Set up proper secret key management
- [ ] Configure static file serving (Nginx/CDN)
- [ ] Set up SSL certificates
- [ ] Configure logging to file/service
- [ ] Configure rate limiting
- [ ] Set up backup strategy
- [ ] Load test API endpoints

---
