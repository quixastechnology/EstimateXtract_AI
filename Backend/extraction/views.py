from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import process_pdf

@csrf_exempt
def upload_pdf(request):
    if request.method == 'POST' and request.FILES.get('file'):
        pdf_file = request.FILES['file']
        try:
            # Process the PDF and extract structured data
            extracted_data = process_pdf(pdf_file)  # Pass the file object directly
            return JsonResponse(extracted_data, safe=False)  # Return the cleaned and structured data
        except Exception as e:
            print(f"Error processing PDF: {str(e)}")  # Log the error for debugging
            return JsonResponse({"error": f"Error processing PDF: {str(e)}"}, status=500)
    
    return JsonResponse({"error": "Invalid request"}, status=400)
