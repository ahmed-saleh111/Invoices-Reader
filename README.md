# Arabic Invoice Analyzer

A FastAPI-based web service that analyzes Arabic VAT invoices using Google's Gemini AI to extract structured data from invoice images.

![Sample Invoice](111.webp)

## Features

- **AI-Powered OCR**: Uses Google Gemini 2.5 Flash model to analyze Arabic invoice images
- **Structured Data Extraction**: Extracts itemized invoice data with proper field mapping
- **REST API**: Simple HTTP endpoint for invoice processing
- **File Upload Support**: Handles various image formats
- **Arabic Language Support**: Specialized for Arabic VAT invoices

## Environment Setup

### Prerequisites

- Python 3.8+
- Google AI API Key

### Installation

1. **Clone or download the project**
   ```bash
   cd ahmed_invoice
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv env_invoice
   
   # On Windows
   env_invoice\Scripts\activate
   
   # On macOS/Linux
   source env_invoice/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install fastapi uvicorn google-genai json-repair pydantic
   ```

4. **Set up Google AI API Key**
   - Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Replace the API key in `invoices2.py` line 76:
     ```python
     client = genai.Client(api_key="YOUR_API_KEY_HERE")
     ```

## Usage

### Running the API Server

```bash
python api.py
```

The server will start on `http://localhost:5000`

### API Endpoint

**POST** `/analyze-invoice`

Upload an invoice image file to extract structured data.

#### Request
- **Method**: POST
- **Content-Type**: multipart/form-data
- **Parameter**: `file` (image file)

#### Example using curl
```bash
curl -X POST "http://localhost:5000/analyze-invoice" \
     -F "file=@your_invoice.jpg"
```

#### Example using Python requests
```python
import requests

url = "http://localhost:5002/analyze-invoice"
files = {"file": open("invoice.jpg", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

### Direct Script Usage

You can also run the invoice analyzer directly:

```bash
python invoices2.py
```

Make sure to update the image path in the `__main__` section.

## Expected Output

The API returns a JSON response with extracted invoice data in the following format:

| Field | Arabic Field | Type | Description |
|-------|--------------|------|-------------|
| `Item ID` | رقم الصنف | String | Product/item identifier |
| `Item Description` | الوصف | String | Product description |
| `Unit Price` | السعر | Float | Price per unit (excluding tax) |
| `Quantity` | الكميه | Integer | Number of units |
| `Tax Amount` | 15%الضريبة% | Float | VAT/tax amount |
| `Total Amount` | الاجمالي | Float | Total cost including tax |

### Sample Response

```json
{
  "items": [
    {
      "Item ID": "PART12345",
      "Item Description": "فلتر هواء للسيارة",
      "Unit Price": 150.00,
      "Quantity": 2,
      "Tax Amount": 45.00,
      "Total Amount": 345.00
    },
    {
      "Item ID": "PART67890",
      "Item Description": "زيت محرك صناعي",
      "Unit Price": 85.50,
      "Quantity": 1,
      "Tax Amount": 12.83,
      "Total Amount": 98.33
    }
  ]
}
```

### Error Response

In case of processing errors:

```json
{
  "error": "Error message description"
}
```

## File Structure

```
ahmed_invoice/
├── api.py              # FastAPI web server
├── invoices2.py        # Core invoice processing logic
├── 111.webp           # Sample invoice image

```

## Technical Details

### AI Model Configuration

- **Model**: Google Gemini 2.5 Flash Preview
- **Temperature**: 0.2 (for consistent results)
- **Response Format**: JSON
- **Language**: Optimized for Arabic text recognition

### Data Validation

The system uses Pydantic models for data validation ensuring:
- Item IDs are 5-12 characters long
- Descriptions have minimum 5 characters
- Numeric fields are properly typed
- At least one item is extracted per invoice

### Security Features

- Temporary file cleanup after processing
- Unique filename generation using UUID
- Input file validation

## Troubleshooting

### Common Issues

1. **API Key Error**: Ensure your Google AI API key is valid and has sufficient quota
2. **Image Quality**: Use high-resolution, clear images for better OCR results
3. **Arabic Text**: Ensure the invoice contains clear Arabic text in the expected format
4. **File Format**: Supported formats include JPG, PNG, WEBP

### Dependencies Issues

If you encounter dependency conflicts:

```bash
pip install --upgrade fastapi uvicorn google-genai json-repair pydantic
```

## License

This project is for educational and commercial use. Make sure to comply with Google AI API terms of service.

## Support

For issues or questions, please check the error logs and ensure all dependencies are properly installed.
