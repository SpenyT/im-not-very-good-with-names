from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def ping(request):
    """
    Simple ping endpoint to test if enrichment app is working.

    GET /api/enrichment/ping/
    """
    return Response({
        'status': 'success',
        'message': 'Enrichment app is running!',
        'app': 'enrichment'
    })
