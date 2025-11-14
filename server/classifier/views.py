from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def ping(request):
    """
    Simple ping endpoint to test if classifier app is working.

    GET /api/classify/ping/
    """
    return Response({
        'status': 'success',
        'message': 'Classifier app is running!',
        'app': 'classifier'
    })
