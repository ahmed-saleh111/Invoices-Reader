# To run this code you need to install the following dependencies:
# pip install google-genai


import json
import json_repair
from google import genai
from google.genai import types
from pydantic import BaseModel, Field



def parse_json(text):
    try:
        return json_repair.loads(text)
    except:
        return None

prompt = """Analyze the provided Arabic invoice image. Extract line item details from its table, mapping the following fields:
*   **Item ID**: from 'رقم الصنف'
*   **Item Description**: from 'الوصف'
*   **Unit Price**: from 'السعر'
*   **Quantity**: from 'الكميه'
*   **Tax Amount**: from '15%الضريبة%'
*   **Total Amount**: from 'الاجمالي'

Return the data strictly as a JSON array (direct list) of objects. Use the exact keys shown in the example structure below. Ensure 'Unit Price', 'Quantity', 'Tax Amount', and 'Total Amount' are numeric values (not strings) and exclude currency symbols.

Required JSON Format Example:
{
    "items": [
        {
            "Item ID": "ExampleItemID1",
            "Item Description": "Example Description One",
            "Unit Price": 100.00,
            "Quantity": 2,
            "Tax Amount": 30.00,
            "Total Amount": 230.00
        },
        {
            "Item ID": "ExampleItemID2",
            "Item Description": "Example Description Two",
            "Unit Price": 50.50,
            "Quantity": 1,
            "Tax Amount": 7.58,
            "Total Amount": 58.08
        }
    ]
}

Extract accurately based on the invoice content.
"""

class Invoice(BaseModel):
    Item_ID: str = Field(
        ...,
        min_length=5,
        max_length=12,
        description="The part number or unique identifier for the item listed on the invoice."
    )
    Item_Description: str = Field(
        ...,
        min_length=5,
        description="A textual description of the item, usually including product type and compatibility."
    )
    Unit_Price: float = Field(
        ...,
        description="The price for a single unit of the item, excluding any tax."
    )
    Quantity: int = Field(
        ...,
        description="The number of units of the item purchased."
    )
    Tax: float = Field(
        ...,
        description="The total amount of tax applied to the item."
    )
    Total_Amount: float = Field(
        ...,
        description="The total cost of the item, including tax."
    )

class Items(BaseModel):
    items: list[Invoice] = Field(
        ..., 
        min_items= 1, 
        description="A list containing the invoice entries for each item purchased."
    )

# def parse_response(response_text):
#     class Invoice(BaseModel):  # تعريف داخلي بنفس التغيير
#         Item_ID: str
#         Item_Description: str
#         Unit_Price: float
#         Quantity: int
#         Tax: float
#         Total_Amount: float

#     class Items(BaseModel):
#         items: List[Invoice]

#     parser = JsonOutputParser(pydantic_object=Items)
#     result = parser.invoke(response_text)  # تحليل النص
#     return result

def generate(image_path):
    image_path = image_path

    client = genai.Client(api_key="AIzaSyBOUJLhfHyWKpt-pvOtZxy5V2CX3Ys2Gxc")
    files = [
        client.files.upload(file=image_path),
    ]

    model = "gemini-2.5-flash-preview-04-17"


    user_prompt = "\n".join([     
        "## Pydantic Details:",
        json.dumps(
            Items.model_json_schema(), ensure_ascii=False
        ),
        "",

        "## Story Details:",
        "```json"
    ])


    system_message = "\n".join([
    "You are a helpful assistant specialized in extracting structured data from images of Arabic VAT invoices.",
    "The user will provide an image of an invoice.",
    "Your task is to extract itemized data from the invoice table using the following mappings:",
    "* Item ID → from 'رقم الصنف'",
    "* Item Description → from 'الوصف'",
    "* Unit Price → from 'السعر'",
    "* Quantity → from 'الكميه'",
    "* Tax Amount → from '15%الضريبة%'",
    "* Total Amount → from 'الاجمالي'",
    "Return the extracted information in strict JSON format under a key called 'items'.",
    "Ensure Unit Price, Quantity, Tax Amount, and Total Amount are numeric values (not strings) and exclude currency symbols.",
    "Do not include any explanations, comments, or additional text. Only return the JSON object."
])
    

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_uri(
                    file_uri=files[0].uri,
                    mime_type=files[0].mime_type,
                ),
                types.Part.from_text(text=user_prompt),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=0.2,
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text=system_message),
        ],
        )

    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )
     
    


    json_response = parse_json(response.text)
    print(json_response)
    print(type(json_response))  

if __name__ == "__main__":
    
    image_path = r"111.jpeg"
    generate(image_path)





# x = 'ahmed {"1": "ahmed", "2": "fahad"}'
# # print (json.loads(x))
# print (parse_json(x))