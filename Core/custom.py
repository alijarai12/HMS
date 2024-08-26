from custom_response.response import CustomResponse 
from rest_framework.response import Response
from rest_framework import status

def get_response(request,model,serializer,pagination_class,filter_queryset,filter_by_hotel,pk=None):
    response = CustomResponse()
    if pk == None:
            queryset = model.objects.all()
            filterqueryset = filter_queryset(filter_by_hotel(queryset))
            
            pagination = pagination_class       
            paginatiedqueryset = pagination.paginate_queryset(filterqueryset, request)
            
            Serializer = serializer(paginatiedqueryset, many=True)
            response_data = {
                'next': pagination.get_next_link(),
                'previous': pagination.get_previous_link(),
                'count': pagination.page.paginator.count,    
                'data': Serializer.data   
            }
            
            if Serializer:
                return Response(response.successResponse( 'Data View', response_data), status=status.HTTP_200_OK)
            return Response(response.errorResponse( 'Error Response'), status=status.HTTP_400_BAD_REQUEST)
    else:
            try:
                queryset = model.objects.get(id=pk)
            except:
                return Response(response.errorResponse('Not found'), status=status.HTTP_400_BAD_REQUEST)
            serializer = serializer(queryset)
            return Response(response.successResponse( 'Data View', serializer.data), status=status.HTTP_200_OK)