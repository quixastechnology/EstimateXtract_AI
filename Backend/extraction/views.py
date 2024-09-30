from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import process_pdf
from .vector_db import create_and_store_embeddings  # Import the function to store embeddings

@csrf_exempt
def upload_pdf(request):
    if request.method == 'POST' and request.FILES.get('file'):
        pdf_file = request.FILES['file']
        try:
            # Process the PDF and extract key values
            parsed_data = process_pdf(pdf_file)
            
            # Call the function to store embeddings into ChromaDB
            create_and_store_embeddings(parsed_data)
            
            # Return the parsed data (if needed, for display in the frontend)
            return JsonResponse(parsed_data, safe=False)
        except Exception as e:
            print(f"Error processing PDF: {str(e)}")
            return JsonResponse({"error": f"Error processing PDF: {str(e)}"}, status=500)
    
    return JsonResponse({"error": "Invalid request"}, status=400)
