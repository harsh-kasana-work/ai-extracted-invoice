
import json
from langchain_groq import ChatGroq
import re
from dotenv import load_dotenv

load_dotenv()


def get_ai_structured_data(text_content):
    # Initialize LLM
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.0,
        max_retries=2,
    )
    messages = [    
    ("system", """You are an intelligent document parsing assistant specialized in extracting structured information from invoices and similar documents. 
Extract information precisely as it appears in the source document, maintaining original formatting of alphanumeric values.
For numeric fields, remove any currency symbols and convert to decimal format.
If a field is not found, return null for that field."""),
    
    ("human", f"""Extract the following fields from the invoice:
- Invoice number
- Invoice date
- Due date (if available)
- Vendor/Supplier name
- Vendor contact information (email, phone, address)
- Line items (as an array of objects with description, quantity, unit price, and amount)
- Subtotal (before tax)
- Tax amount (if specified)
- Total amount

For each line item, capture:
- Item description
- Quantity
- Unit price (without currency symbols)
- Amount (without currency symbols)

Provide the results as a structured JSON object with appropriate nesting.
For tables or line items, return an array of objects.

Example of expected output format:
```json
{{
  "invoice_number": "INV-001",
  "invoice_date": "2023-01-15",
  "due_date": "2023-02-15",
  "vendor_name": "ABC Company",
  "vendor_contact": {{
    "email": "billing@abccompany.com",
    "phone": "555-123-4567",
    "address": ["123 Business St", "Suite 200", "Metropolis, NY 10001"]
  }},
  "line_items": [
    {{
      "description": "Web Development Services",
      "quantity": 40,
      "unit_price": 75.00,
      "amount": 3000.00
    }},
    {{
      "description": "Website Hosting (Annual)",
      "quantity": 1,
      "unit_price": 300.00,
      "amount": 300.00
    }}
  ],
  "subtotal": 3300.00,
  "tax_amount": 231.00,
  "total_amount": 3531.00
}}
```

Text content to process: {text_content}

Return only a valid JSON dictionary with no additional commentary.
""")
    ]

    response = llm.invoke(messages)
    
    # Try to extract just the JSON part if the model includes explanatory text
    try:
        # Find JSON content (assuming it's in the response)
        json_match = re.search(r'```json\s*(.*?)\s*```', response.content, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # Just try to parse the whole response as JSON
            json_str = response.content
            
        # Parse and return the JSON
        return json.loads(json_str)
    except json.JSONDecodeError:
        # If parsing fails, return the raw response
        return {"error": "Failed to parse response", "raw_response": response.content}
