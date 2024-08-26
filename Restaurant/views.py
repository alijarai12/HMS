from .models import *
from Core.utils import *
from.serializers import*
from Core.permissions import *
from rest_framework import status
from django.shortcuts import render
from rest_framework.response import Response
from HMS.CustomPagination import CustomPagination
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from .utils import *
from Core .mixins import GetObjectMixin
from rest_framework.permissions import AllowAny
from custom_response.response import CustomResponse
from django_filters.rest_framework import DjangoFilterBackend


class TableList(HotelFilterMixin,GenericAPIView):
    permission_classes = [CustomModelPermission]
    pagination_class = CustomPagination()
    queryset_model = Table
    search_fields = ['table_no','latest_table_token']
    filterset_fields = ['hotel_id']

    def get(self, request):
        initial_tables_queryset = Table.objects.all()
        # tables = self.filter_by_hotel(initial_tables_queryset)
        tables = self.filter_queryset(self.filter_by_hotel(initial_tables_queryset))

        # tables = Table.objects.filter(hotel_id=request.user.hotel_id)
        paginator = self.pagination_class
        paginated_queryset = paginator.paginate_queryset(tables, request)
        serializer = GetTableSerializer(paginated_queryset, many=True)
        response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count': paginator.page.paginator.count,
            'data': serializer.data
        }
        response = CustomResponse()

        if tables:
            return Response(response.successResponse("data view", response_data), status=status.HTTP_200_OK)
        else:
            return Response(response.errorResponse("data not found"), status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request, format=None):
        serializer = TableSerializer(data=request.data)
        response=CustomResponse()
        
        if serializer.is_valid():
            serializer.save()
            response_data = {'data': serializer.data}
            return Response(response.successResponse('Table created successfully',response_data), status=status.HTTP_201_CREATED)
        return Response(response.errorResponse('Validation Error!',serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    

class TableDetail(GetObjectMixin, GenericAPIView):
    permission_classes = [HotelAssociatedObj, CustomModelPermission]
    queryset_model = Table

        
    def get(self, request, pk):
        table = self.get_queryset_object(Table, pk=pk)
        response = CustomResponse()
        if not table:
            return Response(response.errorResponse('Data is not found,'), status=status.HTTP_404_NOT_FOUND)
        serializer = GetTableSerializer(table)
        return Response(response.successResponse('table Details', serializer.data), status=status.HTTP_200_OK)

    def put(self, request, pk):
        table = self.get_queryset_object(Table, pk)
        response = CustomResponse()
        if not table:
            return Response(response.errorResponse('Data is not found,'), status=status.HTTP_404_NOT_FOUND)
        serializer = TableSerializer(table, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("Table Updated Successfully", serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse("Validation Error!", serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        table = self.get_queryset_object(Table, pk)
        response = CustomResponse()
        if not table:
            return Response(response.errorResponse('Data is not found,'), status=status.HTTP_404_NOT_FOUND)
        table.delete()
        return Response(response.errorResponse("Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)


class TableReservationList(HotelIDFilterMixin, GenericAPIView):
    permission_classes = [HotelAssociatedObjj,CustomModelPermission]
    queryset_model = TableReservation
    pagination_class = CustomPagination()
    search_fields = ['name']
    filterset_fields = ['guest', 'table']

    def get(self, request):
        tableres_querysets = TableReservation.objects.all()
        # table_reservations = self.filter_by_hotel(tableres_querysets)
        table_reservations = self.filter_queryset(self.filter_by_hotel(tableres_querysets))
        paginator = self.pagination_class
        paginated_queryset = paginator.paginate_queryset(table_reservations, request)
        serializer = GetTableReservationSerializer(paginated_queryset, many=True)
        response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count': paginator.page.paginator.count,
            'data': serializer.data
        }
        response = CustomResponse()
        if table_reservations:
            return Response(response.successResponse("data view", response_data), status=status.HTTP_200_OK)
        return Response(response.errorResponse('No data found'), status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        """
        Before creating a reservation,
        checks for any conflicting bookings around the specified time."""
        response = CustomResponse()
        existing_reservation = check_table_availability(request.data)
        if existing_reservation:
            return Response(response.errorResponse('Reservation already exists for this table and time!'), status=status.HTTP_400_BAD_REQUEST)

        serializer = TableReservationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'data': serializer.data
            }
            return Response(response.successResponse('data created', response_data), status=status.HTTP_201_CREATED)
        return Response(response.errorResponse('Validation Error!', serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    

class TableReservationDetail(GetObjectMixin, GenericAPIView):
    permission_classes = [HotelAssociatedObjj,CustomModelPermission]
    queryset_model = TableReservation

    # def get_queryset_object(self, pk):
    #     try:
    #         return TableReservation.objects.get(pk=pk)
    #     except TableReservation.DoesNotExist:
    #         return None

    def get(self,request, pk):
        table_reservation=self.get_queryset_object(self.queryset_model,pk)
        response = CustomResponse()

        if not table_reservation:
            return Response(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)
        serializer=GetTableReservationSerializer(table_reservation)
        return Response(response.successResponse('Table Reservation Details',serializer.data),status=status.HTTP_200_OK)


    def put(self, request, pk ):
        table_reservation=self.get_queryset_object(self.queryset_model,pk)
        response=CustomResponse()
        if not table_reservation:
           return Response(response.errorResponse('Data is not found'),status=status.HTTP_404_NOT_FOUND)
        serializer=TableReservationSerializer(table_reservation,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("Table_Reservation Updated Successfully", serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse("Validation Error!", serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        table_reservation=self.get_queryset_object(self.queryset_model,pk)
        response=CustomResponse()
        if not table_reservation:
           return Response(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)        
        table_reservation.delete()
        return Response(response.errorResponse("Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)



class MenuList(HotelFilterMixin,GenericAPIView):
    permission_classes = [CustomModelPermission]
    queryset_model = Menu
    pagination_class = CustomPagination()
    search_fields = ['menuType']
    filterset_fields = ['hotel_id']

    def get(self,request):
        menus_querysets=Menu.objects.all()
        # menus = self.filter_by_hotel(menus_querysets)
        menus = self.filter_queryset(self.filter_by_hotel(menus_querysets))
        paginator = self.pagination_class
        paginated_queryset = paginator.paginate_queryset(menus, request)
        serializer=GetMenuSerializer(paginated_queryset,many=True)
        response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count': paginator.page.paginator.count,
            'data': serializer.data
        }
        response=CustomResponse()
        if menus:
            return Response(response.successResponse("data view", response_data), status=status.HTTP_200_OK)
        return Response(response.errorResponse('No data found'), status=status.HTTP_404_NOT_FOUND)
        # return Response(response.errorResponse(404, "data not found"),status=status.HTTP_404_NOT_FOUND)
    

    def post(self, request, format=None):
        serializer = MenuSerializer(data=request.data)
        response=CustomResponse()
        if serializer.is_valid():
            serializer.save()
            response_data={
            'data':serializer.data
        }
            return Response(response.successResponse('Menu item created',response_data), status=status.HTTP_201_CREATED)
        return Response(response.errorResponse("Validation Error!", serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    

class MenuDetail(GetObjectMixin, GenericAPIView):
    permission_classes = [HotelAssociatedObj, CustomModelPermission]
    queryset_model = Menu

    # def get_queryset_object(self, pk):
    #     try:
    #         return Menu.objects.get(pk=pk)
    #     except Menu.DoesNotExist:
    #         return None

    def get(self,request, pk):
        menu=self.get_queryset_object(self.queryset,pk)
        response = CustomResponse()

        if not menu:
            return Response(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)
        serializer=GetMenuSerializer(menu)
        return Response(response.successResponse('Menu Details',serializer.data),status=status.HTTP_200_OK)


    def put(self, request, pk ):
        menu=self.get_queryset_object(self.queryset,pk)
        response=CustomResponse()
        if not menu:
           return Response(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)
        serializer=MenuSerializer(menu,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("Menu Updated Successfully", serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse("Validation Error!", serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        menu=self.get_queryset_object(self.queryset,pk)
        response=CustomResponse()
        if not menu:
           return Response(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)        
        menu.delete()
        return Response(response.errorResponse("Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)
    

class FoodList(ForeignKeyValidationMixin,HotelFilterMixin,GenericAPIView):
    permission_classes = [CustomModelPermission]
    queryset_model = Food
    pagination_class = CustomPagination()
    search_fields = ['food_name','ingredients','unit']
    filterset_fields = ['menu','hotel_id']
    foreign_keys = {'Restaurant':'Menu'}

    def get(self,request):
        foods_querysets=Food.objects.all()
        # foods = self.filter_by_hotel(foods_querysets)
        foods = self.filter_queryset(self.filter_by_hotel(foods_querysets))
        paginator = self.pagination_class
        paginated_queryset = paginator.paginate_queryset(foods, request)
        serializer=GetFoodSerializer(paginated_queryset,many=True)
        
        response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count': paginator.page.paginator.count,
            'data': serializer.data
        }
        response=CustomResponse()
        if foods:
            return Response(response.successResponse("data view", response_data), status=status.HTTP_200_OK)
        else:
            return Response(response.errorResponse('No data found'), status=status.HTTP_404_NOT_FOUND)

    

    def post(self, request, format=None):
        serializer = FoodSerializer(data=request.data)
        response=CustomResponse()

        valid, message = self.validate_foreign_keys(request)
        if not valid:
            return Response(response.errorResponse(message), status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save()
            response_data={
            'data':serializer.data
        }
            return Response(response.successResponse('data created',response_data), status=status.HTTP_201_CREATED)
        return Response(response.errorResponse("Validation Error!", serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    

class FoodDetail(GetObjectMixin, GenericAPIView):
    permission_classes = [HotelAssociatedObj, CustomModelPermission]
    queryset_model = Food

    # def get_queryset_object(self, pk):
    #     try:
    #         return Food.objects.get(pk=pk)
    #     except Food.DoesNotExist:
    #         return None

    def get(self,request, pk):
        food=self.get_queryset_object(self.queryset_model, pk)
        response = CustomResponse()

        if not food:
            return Response(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)
        serializer=GetFoodSerializer(food)
        return Response(response.successResponse('Food Details',serializer.data),status=status.HTTP_200_OK)


    def put(self, request, pk ):
        food=self.get_queryset_object(self.queryset_model,pk)
        response=CustomResponse()
        if not food:
           return Response(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)
        serializer=FoodSerializer(food,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("Food Updated Successfully", serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse("Validation Error!", serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, pk):
        food=self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not food:
           return Response(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)        
        food.delete()
        return Response(response.errorResponse("Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)
    

class OrderItemList(HotelFilterMixin,GenericAPIView):
    permission_classes = [CustomModelPermission]
    queryset_model = OrderItem
    pagination_class = CustomPagination()
    search_fields = ['notes','latest_table_token']
    filterset_fields = ['table_id','food','hotel_id']
   

    def get(self,request):
        orditm_querysets = None
        user = request.user
        if user.groups.filter(name='Kitchen') or user.groups.filter(name='Counter').exists(): # checking weather the employee is kitchen user or not
            # User is from the "Kitchen" role, display every order item list
            orditm_querysets = OrderItem.objects.all()
            # print('orders:', orders)
        else:
            orditm_querysets=OrderItem.objects.filter(order_status='Completed')

        if orditm_querysets is not None:
            order_items = self.filter_queryset(self.filter_by_hotel(orditm_querysets))
        else:
            order_items = OrderItem.objects.none()  
        paginator = self.pagination_class
        paginated_queryset = paginator.paginate_queryset(order_items, request)
        serializer=GetOrderItemSerializer(paginated_queryset,many=True)
        response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count': paginator.page.paginator.count,
            'data': serializer.data
        }

        response=CustomResponse()
        if order_items:
            return Response(response.successResponse("data view", response_data), status=status.HTTP_200_OK)
        else:
            return Response(response.errorResponse('No data found'), status=status.HTTP_404_NOT_FOUND)
            
    

    def post(self, request):
        # Get the hotel ID from the authenticated user
        
        hotel_id = request.user.hotel_id.id
        # print(request.user.hotel_id)

        # Include the hotel ID in the request data
        request.data['hotel_id'] = hotel_id

        #request.data['order_placed_by'] = request.user.employeeinfos
        table_id = request.data.get('table_id')
        # hotel_id = request.data.get('hotel_id')
        items = request.data.get('items')
        while True:
            # Generate a random order number (you can adjust the range as needed)
            random_number = random.randint(1000, 9999)
            order_no = f"KOT-{random_number}"

            # Check if the order number already exists
            if OrderItem.objects.filter(order_no=order_no).exists():
                continue
            break

        for i in items:
            i['hotel_id'] = request.data['hotel_id']
            i['table_id'] = table_id
            i['order_placed_by']=request.user.employeeinfos.id
            i['order_no'] = order_no
            serializer = OrderItemSerializer(data=i)
            response=CustomResponse()
            if serializer.is_valid():
                serializer.save()
                # kot = KOT.objects.prefetch_related('order_item').get(id=kot.id)
                # kot_serializer = GetKOTSerializer(kot)
                response_data={'data':serializer.data}
            else:
                return Response(response.errorResponse("Validation Error!", serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        return Response(response.successResponse('data created',response_data), status=status.HTTP_201_CREATED)



class OrderItemDetail(GetObjectMixin, GenericAPIView):
    permission_classes = [HotelAssociatedObj, CustomModelPermission]
    queryset_model = OrderItem

    # def get_queryset_object(self, pk):
    #     try:
    #         return OrderItem.objects.get(pk=pk)
    #     except OrderItem.DoesNotExist:
    #         return None

    def get(self,request, pk):
        order_item=self.get_queryset_object(self.queryset_model, pk)
        response = CustomResponse()

        if not order_item:
            return Response(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)
        serializer=GetOrderItemSerializer(order_item)
        return Response(response.successResponse('Food Details',serializer.data),status=status.HTTP_200_OK)


    def put(self, request, pk ):
        # Get the hotel ID from the authenticated user
        hotel_id = request.user.hotel_id.id
        
        # Include the hotel ID in the request data
        request.data['hotel_id'] = hotel_id
        order_item=self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not order_item:
           return Response(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)
        serializer=OrderItemSerializer(order_item,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("Order Updated Successfully", serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse("Validation Error!", serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        order_item=self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not order_item:
           return Response(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)        
        order_item.delete()
        return Response(response.errorResponse("Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)
    


class RestaurantInvoiceList(HotelFilterMixin,GenericAPIView):
    permission_classes = [CustomModelPermission]
    queryset_model = RestaurantInvoice
    pagination_class = CustomPagination()
    search_fields = ['for_guest']
    filterset_fields = ['hotel_id','order','guest','restaurant_transaction']

    def get(self,request):
        restro_invoices=RestaurantInvoice.objects.all()
        # print(restro_invoices)
        # restro_invoices = self.filter_by_hotel(restro_invoices_querysets)
        restro_invoices = self.filter_queryset(self.filter_by_hotel(restro_invoices))
        paginator = self.pagination_class
        paginated_queryset = paginator.paginate_queryset(restro_invoices, request)
        serializer=GetRestaurantInvoiceSerializer(paginated_queryset,many=True)
        response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count': paginator.page.paginator.count,
            'data': serializer.data
        }
        response=CustomResponse()
        if restro_invoices:
            return Response(response.successResponse("data view", response_data), status=status.HTTP_200_OK)
        else:
            return Response(response.errorResponse('No data found'), status=status.HTTP_404_NOT_FOUND)
            # return Response(response.errorResponse(404, "data not found"),status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request):        
        for_guest = request.data.get('for_guest')
        order_list = request.data.get('order')
        hotel_id = request.user.hotel_id.id
        request.data['hotel_id'] = hotel_id
        request.data['confirmed_by'] = request.user.employeeinfos.id
        recieved_amount = request.data.get('received_amount')
        payment_method = request.data.get('payment_method')
        bank_details = request.data.get('bank_details')
        response=CustomResponse()
        if for_guest == True:
            for i in order_list:
                request.data['order'] = i
                serializer = RestaurantInvoiceGuestSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(response.errorResponse('Error Occured',serializer.errors), status=status.HTTP_400_BAD_REQUEST)
            complete_orders_and_free_table(order_list[0])
            return Response(response.successResponse('data created',serializer.data), status=status.HTTP_201_CREATED)
        has_membership = request.data.get('has_membership')
        if has_membership == True:
            member = request.data.get('membership_id') 
            r_t_data = {"membership":member,"hotel_id":hotel_id,'recieved_amount':recieved_amount,'payment_method':payment_method,'bank_details':bank_details}
            r_t_serializer = RestaurantTransactionSerializer(data=request.data)
            if r_t_serializer.is_valid():
                r_t_obj_serializer = r_t_serializer.save()
            else:
                return Response(response.errorResponse('Error Occured',r_t_serializer.errors), status=status.HTTP_400_BAD_REQUEST)
            for i in order_list:
                r_i_data = {"order":i,"hotel_id":hotel_id,"restaurant_transaction":r_t_obj_serializer.id}
                r_i_serializer = RestaurantInvoiceSerializer(data=r_i_data)
                if r_i_serializer.is_valid():
                    r_i_serializer.save()
                    response_data={
                    'data':r_i_serializer.data
                }
                else:
                    return Response(response.errorResponse('Error Occured',r_i_serializer.errors), status=status.HTTP_400_BAD_REQUEST)
            complete_orders_and_free_table(order_list[0])
            r_t_obj = RestaurantTransaction.objects.get(id=r_t_obj_serializer.id)
            get_restaurant_transaction_serializer = GetRestaurantTransactionSerializer(r_t_obj)
            return Response(response.successResponse('data created',get_restaurant_transaction_serializer.data), status=status.HTTP_201_CREATED)    
        else:
            guest_name = request.data.get('guest_name')
            guest_number = request.data.get('guest_number')
            r_t_data = {"guest_name":guest_name,"guest_number":guest_number,"hotel_id":hotel_id,'recieved_amount':recieved_amount,'payment_method':payment_method,'bank_details':bank_details}
            r_t_serializer = RestaurantTransactionSerializer(data=request.data)
            if r_t_serializer.is_valid():
                r_t_obj_serializer = r_t_serializer.save()
            else:
                return Response(response.errorResponse('Error Occured',r_t_serializer.errors), status=status.HTTP_400_BAD_REQUEST)
            for i in order_list:
                r_i_data = {"order":i,"hotel_id":hotel_id,"restaurant_transaction":r_t_obj_serializer.id}
                r_i_serializer = RestaurantInvoiceSerializer(data=r_i_data)
                if r_i_serializer.is_valid():
                    r_i_serializer.save()
                    response_data={
                    'data':r_i_serializer.data
                }
                else:
                    return Response(response.errorResponse('Error Occured',r_i_serializer.errors), status=status.HTTP_400_BAD_REQUEST)
            complete_orders_and_free_table(order_list[0])
            r_t_obj = RestaurantTransaction.objects.get(id=r_t_obj_serializer.id)
            get_restaurant_transaction_serializer = GetRestaurantTransactionSerializer(r_t_obj)
            return Response(response.successResponse('data created',get_restaurant_transaction_serializer.data), status=status.HTTP_201_CREATED)

            


class RestraurantInvoiceDetail(GetObjectMixin, GenericAPIView):
    permission_classes = [HotelAssociatedObj, CustomModelPermission]
    queryset_model = RestaurantInvoice

    # def get_queryset_object(self, pk):
    #     try:
    #         return RestaurantInvoice.objects.get(pk=pk)
    #     except RestaurantInvoice.DoesNotExist:
    #         return None

    def get(self,request, pk):
        restro_invoice=self.get_queryset_object(self.queryset_model, pk)
        response = CustomResponse()

        if not restro_invoice:
            return Response(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)
        serializer=GetRestaurantInvoiceSerializer(restro_invoice)
        return Response(response.successResponse('Invoice Details',serializer.data),status=status.HTTP_200_OK)


    def put(self, request, pk ):
        restro_invoice=self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not restro_invoice:
           return Response(response.errorResponse('Data is not found,','Not Found'),status=status.HTTP_404_NOT_FOUND)
        serializer=RestaurantInvoiceSerializer(restro_invoice,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("Invoice Updated Successfully", serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse("Validation Error!", serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        restro_invoice=self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not restro_invoice:
           return Response(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)        
        restro_invoice.delete()
        return Response(response.errorResponse("Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)
    

class RestaurantTransactionList(HotelFilterMixin,GenericAPIView):
    permission_classes = [CustomModelPermission]
    queryset_model = RestaurantTransaction
    pagination_class = CustomPagination()
    search_fields = ['guest_name','discount_reason','payment_status']
    filterset_fields = ['confirmed_by','payment_method','bank_details','membership','hotel_id']

    def get(self,request):
        restro_trasaction_queryset=RestaurantTransaction.objects.prefetch_related('restaurant_invoice').all()
        restro_trasactions=self.filter_queryset(self.filter_by_hotel(restro_trasaction_queryset))
        paginator = self.pagination_class
        paginated_queryset = paginator.paginate_queryset(restro_trasactions, request)
        serializer=GetRestaurantTransactionSerializer(paginated_queryset,many=True)
        response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count': paginator.page.paginator.count,
            'data': serializer.data
        }
        response=CustomResponse()
        if restro_trasactions:
            return Response(response.successResponse("Restaurant Transaction Lists:", response_data), status=status.HTTP_200_OK)
        else:
            return Response(response.errorResponse('No data found'), status=status.HTTP_404_NOT_FOUND)

    

    def post(self, request, format=None):
        serializer = RestaurantTransactionSerializer(data=request.data)
        response=CustomResponse()
        if serializer.is_valid():
            serializer.save()
            response_data={
            'data':serializer.data
        }
            return Response(response.successResponse('data created',response_data), status=status.HTTP_201_CREATED)
        return Response(response.errorResponse("Validation Error!", serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    


class RestraurantTransactionDetail(GetObjectMixin, GenericAPIView):
    permission_classes = [HotelAssociatedObj, CustomModelPermission]
    queryset_model = RestaurantTransaction
    filterset_fields = ['id', 'hotel_id', 'PaymentMethod__id']
    search_fields = ['guest_name', 'guest_number']

    # def get_queryset_object(self, pk):
    #     try:
    #         return RestaurantTransaction.objects.get(pk=pk)
    #     except RestaurantTransaction.DoesNotExist: 
    #         return None

    def get(self,request, pk):
        restro_transaction=self.get_queryset_object(self.queryset_model, pk)
        response = CustomResponse()

        if not restro_transaction:
            return Response(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)
        serializer=GetRestaurantTransactionSerializer(restro_transaction)
        return Response(response.successResponse('Restaurant Transaction Details',serializer.data),status=status.HTTP_200_OK)


    def put(self, request, pk ):
        restro_transaction=self.get_queryset_object(self.queryset_model, pk)
        response=CustomResponse()
        if not restro_transaction:
           return Response(response.errorResponse('Data is not found,'),status=status.HTTP_404_NOT_FOUND)
        serializer=RestaurantTransactionSerializer(restro_transaction,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse("Restraction Transaction Updated Successfully", serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse("Validation Error!", serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        restro_transaction=self.get_queryset_object(self.queryset_model,pk)
        response=CustomResponse() 
        if not restro_transaction:
           return Response(response.errorResponse('Data is not found,','Not Found'),status=status.HTTP_404_NOT_FOUND)        
        restro_transaction.delete()
        return Response(response.errorResponse("Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)


class TableOrdersListView(GetObjectMixin,HotelFilterMixin,GenericAPIView):
    permission_classes = [HotelAssociatedObj,CustomModelPermission]
    queryset_model = Table
    pagination_class = CustomPagination()
    search_fields = ['latest_table_token','order_status']
    filterset_fields = ['table_no','hotel_id']

    # def get_queryset_object(self, pk):
    #     try:
    #         return Table.objects.get(id=pk)
    #     except Table.DoesNotExist:
    #         return None
        
    def get(self, request, pk):
            table = self.get_queryset_object(self.queryset_model, pk)
            response = CustomResponse()

            if not table:
                return Response(response.errorResponse('Table not found.'), status=status.HTTP_404_NOT_FOUND)

            order_items = OrderItem.objects.filter(table_id=table, latest_table_token=table.latest_table_token).exclude(order_status='Cancelled')
            order_items = self.filter_by_hotel(order_items)

            if not order_items:
                return Response(response.errorResponse('No data found'), status=status.HTTP_404_NOT_FOUND)


            paginator = self.pagination_class
            paginated_queryset = paginator.paginate_queryset(order_items, request)
            serializer = GetTableOrdersListSerializers(paginated_queryset, many=True)
            response_data = {
                'next': paginator.get_next_link(),
                'previous': paginator.get_previous_link(),
                'count': paginator.page.paginator.count,
                'data': serializer.data
            }
            return Response(response.successResponse('Table Order List', response_data), status=status.HTTP_200_OK)



class DashboardApiListView(GenericAPIView):
    permission_classes = [IsAuthenticated, AdminUserPermission]
    def get(self,request,pk):
        data = DashboardDataSerializer()
        return Response(data.get_data(hotel_id=request.user.hotel_id,year=pk))
    


class GetVatAndDiscount(HotelFilterMixin,GenericAPIView):
    permission_classes = [CustomModelPermission]
    queryset_model = TaxAndDiscount
    search_fields = []
    filterset_fields = ['hotel_id']

    def get(self, request):
        response = CustomResponse()
        discount_query = self.filter_queryset(self.filter_by_hotel(TaxAndDiscount.objects.all()))
        if discount_query:
            serializer = GetVatAndDiscountSerializer(discount_query, many=True)
            return Response(response.successResponse('Discount record found', serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse('No data found'), status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request):
        response = CustomResponse()
        serializer = VatAndDiscountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse('Vat and Discount created successfully', serializer.data), status=status.HTTP_201_CREATED)
        return Response(response.errorResponse('Validation Error!', serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    


class GetVatAndDiscountDetail(GetObjectMixin, GenericAPIView):
    permission_classes = [HotelAssociatedObj, CustomModelPermission]
    queryset_model = TaxAndDiscount

    # def get_queryset_object(self, pk):
    #     try:
    #         return TaxAndDiscount.objects.get(pk=pk)
    #     except TaxAndDiscount.DoesNotExist:
    #         return None
        
    def get(self, request, pk):
        ds_object = self.get_queryset_object(self.queryset_model, pk)
        response = CustomResponse()
        if not ds_object:
            return Response(response.errorResponse('Data not found'),status=status.HTTP_404_NOT_FOUND)
        serializer=GetVatAndDiscountSerializer(ds_object)
        return Response(response.successResponse('Discount Details',serializer.data),status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        ds_object = self.get_queryset_object(self.queryset_model, pk)
        response = CustomResponse()
        if not ds_object:
            return Response(response.errorResponse('Data not found'), status=status.HTTP_404_NOT_FOUND)
        serializer = VatAndDiscountSerializer(ds_object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse('Data updated successfully', serializer.data), status=status.HTTP_200_OK)
        return Response(response.errorResponse('Validation error', serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        response = CustomResponse()
        ds_object = self.get_queryset_object(self.queryset_model, pk)
        if not ds_object:
            return Response(response.errorResponse('Data not found'), status=status.HTTP_404_NOT_FOUND)
        ds_object.delete()
        return Response(response.errorResponse("Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)




class AnonymousMenuAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    pagination_class = CustomPagination()
    filterset_fields = ['menuType']
    search_fields =  ['menuType']
   


    def get(self, request, hotel_id):
        response = CustomResponse()
        menu_data = Menu.objects.filter(hotel_id=1)
        paginator = self.pagination_class
        paginated_queryset = paginator.paginate_queryset(menu_data, request)
        serializer = GetMenuSerializer(paginated_queryset, many=True)
        response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count': paginator.page.paginator.count,
            'data': serializer.data
        }

        return Response(response.successResponse('Menu List!', response_data), status=status.HTTP_200_OK)

class AnonymousFoodAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    pagination_class = CustomPagination()
    filterset_fields = ['food_name']
    search_fields = ['food_name']

    def get(self, request, hotel_id):
        response = CustomResponse()
        food_data = Food.objects.filter(hotel_id=1)
        response = CustomResponse()
        paginator = self.pagination_class
        paginated_queryset = paginator.paginate_queryset(food_data, request)
        serializer = GetFoodSerializer(paginated_queryset, many=True)
        response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count': paginator.page.paginator.count,
            'data': serializer.data
        }

        return Response(response.successResponse('FoodList', response.successResponse('Food List!', response_data)), status=status.HTTP_200_OK)


class AnonymousTableAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    pagination_class = CustomPagination()
    filterset_fields = ['table_no' , 'seating_capacity']
    search_fields = ['table_no', 'seating_capacity']

    def get(self, request, hotel_id):
        response = CustomResponse()
        table_data = Table.objects.filter(hotel_id=1)

        response = CustomResponse()
        paginator = self.pagination_class
        paginated_queryset = paginator.paginate_queryset(table_data, request)
        serializer = GetTableSerializer(paginated_queryset, many=True)
        response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count': paginator.page.paginator.count,
            'data': serializer.data
        }
        return Response(response.successResponse('Table', response.successResponse('Table List!', response_data)), status=status.HTTP_200_OK)
    

class AnonymousTableReservationAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    pagination_class = CustomPagination()
    filterset_fields = ['name', 'bookingDateTime']
    search_fields = ['name', 'bookingDateTime']

    def get(self, request, hotel_id):
        table_reservation_data = TableReservation.objects.filter(table__hotel_id=1)

        response = CustomResponse()

        table_data = TableReservation.objects.filter(table__hotel_id=1)

        response = CustomResponse()
        paginator = self.pagination_class
        paginated_queryset = paginator.paginate_queryset(table_reservation_data, request)
        serializer = GetTableReservationSerializer(paginated_queryset, many=True)
        response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count': paginator.page.paginator.count,
            'data': serializer.data
        }
        return Response(response.successResponse('Table Reservation List!', response_data), status=status.HTTP_200_OK)
    

class AnonymousBannerView(GenericAPIView):  
    permission_classes = [AllowAny]
    pagination_class = CustomPagination()
  
    def get(self, request):
        response = CustomResponse()
        banner_data = Banners.objects.all()

        response = CustomResponse()
        paginator = self.pagination_class
        paginated_queryset = paginator.paginate_queryset(banner_data, request)
        serializer = BannersSerializer(paginated_queryset, many=True)
        response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count': paginator.page.paginator.count,
            'data': serializer.data
        }
        return Response(response.successResponse('Banner List!', response_data), status=status.HTTP_200_OK)


class AnonymousContactView(GenericAPIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'email']

    def get(self, request):
        response = CustomResponse()
        contact_data = Contact.objects.all()

        response = CustomResponse()
        paginator = self.pagination_class
        paginated_queryset = paginator.paginate_queryset(contact_data, request)
        serializer = ContactSerializer(paginated_queryset, many=True)
        response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count': paginator.page.paginator.count,
            'data': serializer.data
        }

        return Response(response.successResponse('Contact List!', response_data), status=status.HTTP_200_OK)

class AnonymousOfferview(GenericAPIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination()

    def get(self, request):
        response = CustomResponse()

        offer_data = Offer.objects.all()

        response = CustomResponse()
        paginator = self.pagination_class
        paginated_queryset = paginator.paginate_queryset(offer_data, request)
        serializer = OfferSerializer(paginated_queryset, many=True)
        response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count': paginator.page.paginator.count,
            'data': serializer.data
        }

        return Response(response.successResponse('Offer List!', response_data), status=status.HTTP_200_OK)

class OpeningHoursView(GenericAPIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination()

    def get(self, request):

        response = CustomResponse()

        openinghours_data = OpeningHours.objects.all()

        response = CustomResponse()
        paginator = self.pagination_class
        paginated_queryset = paginator.paginate_queryset(openinghours_data, request)
        serializer = OpeningHoursSerializer(paginated_queryset, many=True)
        response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count': paginator.page.paginator.count,
            'data': serializer.data
        }

        return Response(response.successResponse('Opening Hours List!', response_data), status=status.HTTP_200_OK)
    

class AnonymousSubscriptionView(GenericAPIView):
    permission_classes = [AllowAny]
    # pagination_class = CustomPagination()
    serializer_class = [SubscriptionsSerializer]

    def post(self, request):
        response = CustomResponse()
        serializer_data = self.serializer_class(data=request.data)
        
        # Check if the serializer is valid
        if serializer_data.is_valid():
            serializer_data.save()
            return Response(response.successResponse('Subscription Added ', serializer_data.data), status=status.HTTP_200_OK)
        else:
            return Response(response.errorResponse('Validation Error!', serializer_data.errors), status=status.HTTP_400_BAD_REQUEST)
    
    

class AnonymousGalleryView(GenericAPIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination()

    def get(self, request):

        response = CustomResponse

        gallery_data = Gallary.objects.all()

        response = CustomResponse()
        paginator = self.pagination_class
        paginated_queryset = paginator.paginate_queryset(gallery_data, request)
        serializer = GallarySerializer(paginated_queryset, many=True)
        response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count': paginator.page.paginator.count,
            'data': serializer.data
        }

        return Response(response.successResponse('Gallery List!', response_data), status=status.HTTP_200_OK)


class IliveMembershipApiView(GetObjectMixin, GenericAPIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination()
    serializer_class = GetMembershipSerializer
    search_fields = ['name']
    filterset_fields = ['id', 'hotel_id']

    def get(self, request):
        response = CustomResponse()

        membership_data = Membership.objects.all()
        filter_obj = self.filter_queryset(membership_data)

        paginator = self.pagination_class
        paginated_queryset = paginator.paginate_queryset(filter_obj, request)

        serializer = self.serializer_class(paginated_queryset, many = True)
        response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count':paginator.page.paginator.count,
            'data': serializer.data
        }

        if filter_obj:
            return Response(response.successResponse("data view", response_data), status=status.HTTP_200_OK)
        return Response(response.errorResponse("data not found"), status=status.HTTP_404_NOT_FOUND)

class FloorApiView(GenericAPIView, GetObjectMixin, HotelFilterMixin):
    pagination_class = CustomPagination()
    serializer_class = FloorSerializer
    search_fields = ['name']

    def get(self, request):
        response = CustomResponse ()

        floor_data = Floor.objects.prefetch_related('tables').all()
        # floor = self.filter_by_hotel(floor_data)
        filter_obj = self.filter_by_hotel(floor_data)

        paginator = self.pagination_class
        paginated_queryset = paginator.paginate_queryset(filter_obj, request)
         
        serializer = GetFloorSerilizer(paginated_queryset, many=True)
        

        response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count':paginator.page.paginator.count,
            'data': serializer.data
        }


        if filter_obj:
            return Response(response.successResponse("data view", response_data), status=status.HTTP_200_OK)
        return Response(response.errorResponse("data not found"), status=status.HTTP_404_NOT_FOUND)


    def post(self, request):
        response = CustomResponse()     
        serializer_data = FloorSerializer(data=request.data)
        
        # Check if the serializer is valid
        if serializer_data.is_valid():
            serializer_data.save()
            response_data = {'data': serializer_data.data}
            return Response(response.successResponse('Floor Added', response_data.get('data')), status=status.HTTP_201_CREATED)
        else:
            return Response(response.errorResponse('Validation Error!', serializer_data.errors), status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        response = CustomResponse()

        try:
            # Get the Floor object to update
            floor = Floor.objects.get(pk=pk)
        except Floor.DoesNotExist:
            return Response(response.errorResponse('Floor not found'), status=status.HTTP_404_NOT_FOUND)

        serializer_data = self.serializer_class(floor, data=request.data, partial=True)

        if serializer_data.is_valid():
            serializer_data.save()
            return Response(response.successResponse('Floor Updated', serializer_data.data), status=status.HTTP_200_OK)
        else:
            return Response(response.errorResponse('Validation Error!', serializer_data.errors), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        response = CustomResponse()

        try:
            # Get the Floor object to delete
            floor = Floor.objects.get(pk=pk)
        except Floor.DoesNotExist:
            return Response(response.errorResponse('Floor not found'), status=status.HTTP_404_NOT_FOUND)

        floor.delete()
        return Response(response.successResponse('Floor Deleted'), status=status.HTTP_204_NO_CONTENT)

  
class TotalCreditView(HotelFilterMixin,GenericAPIView):
    serializer_class = TotalCreditSerilizer
    pagination_class = CustomPagination()
    

    def get(self, request):
        response = CustomResponse ()
        
        credit_data = TotalCredit.objects.all()
        credit_obj = self.filter_by_hotel(credit_data)
        
        paginator = self.pagination_class
        paginated_queryset = paginator.paginate_queryset(credit_obj, request)
         
        serilizer = self.serializer_class(paginated_queryset, many=True)

        response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count':paginator.page.paginator.count,
            'data': serilizer.data
        }
        if credit_obj:
            return Response(response.successResponse('Credit view', response_data), status=status.HTTP_200_OK)
        return Response(response.errorResponse("data not found"), status=status.HTTP_404_NOT_FOUND)
    
class CreditDetailsView(HotelFilterMixin,GenericAPIView):
    
    serializer_class = CreditDetailsSerillizers
    pagination_class = CustomPagination()
    search_fields =['credit_paid']


    def get(self, request):
        
        response = CustomResponse()
        creditdetail_data = CreditDetails.objects.filter(total_credit__hotel_id=self.request.user.hotel_id.id)    
        creditdetail_obj = self.filter_queryset(creditdetail_data)

        paginator = self.pagination_class
        paginated_queryset = paginator.paginate_queryset(creditdetail_data, request)
        
        serilizer = GetCreditDetailsSerillizers(paginated_queryset, many=True)

        response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count':paginator.page.paginator.count,
            'data': serilizer.data
        }

        return Response(response.successResponse("Credit Details", response_data), status=status.HTTP_200_OK)


    def post(self, request): 

        response = CustomResponse()      
   
        f_m = request.data.get('for_membership')
        if f_m == True:
            membership = request.data.get('membership')
            try:
                t_c = TotalCredit.objects.filter(membership=membership).latest('id')
            except:
                return Response(response.errorResponse(400, 'Not found!','Credit for this membership not found!'), status=status.HTTP_400_BAD_REQUEST)
            
        else:
            number = request.data.get('guest_number')
            try:
                t_c = TotalCredit.objects.filter(guestnumber=number).latest('id')
            except:
                return Response(response.errorResponse(400, 'Not found!','Credit for this guest number not found!'), status=status.HTTP_400_BAD_REQUEST)
        
        request.data['total_credit'] = t_c.id
        serializer = self.serializer_class(data=request.data)
               
        if serializer.is_valid():
            serializer.save()
            return Response(response.successResponse('Data Created', serializer.data), status=status.HTTP_201_CREATED)
        else:
            return Response(response.errorResponse('Validation Error!', serializer.errors), status=status.HTTP_400_BAD_REQUEST)


class IliveContactInfoView(GetObjectMixin, GenericAPIView):
    permission_classes= [AllowAny]
    serializer_class = GetInformationSerillizers
    pagination_class = CustomPagination()
    response = CustomResponse()
    def get(self, request,):
        
        menu_data = Hotel.objects.filter(id=1)
        paginator = self.pagination_class
        paginated_queryset = paginator.paginate_queryset(menu_data, request)
        serializer = GetInformationSerillizers(paginated_queryset, many=True)
        response_data = {
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'count': paginator.page.paginator.count,
            'data': serializer.data
        }
        return Response(('Contactlist', response_data), status=status.HTTP_200_OK)
    
    def post(self, request):
        
        serilizer = self.serializer_class(data=request.data)
        if serilizer.is_valid():
            return Response(self.response.successResponse(200, 'contact info created successfully', serilizer.data), status=status.HTTP_200_OK)
        return Response(self.response.errorResponse(400, 'Validation Error!', serilizer.errors), status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        info_detail = self.get_queryset_object(Hotel, pk)
        
        if not info_detail:
           return Response(self.response.errorResponse(404,'Data is not found,','Not Found'),status=status.HTTP_404_NOT_FOUND)
        serializer=self.serializer_class(info_detail,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(self.response.successResponse(200, "contact Updated Successfully", serializer.data), status=status.HTTP_200_OK)
        return Response(self.response.errorResponse(400, "Validation Error!", serializer.errors), status=status.HTTP_400_BAD_REQUEST)
     
    def delete(self, request, pk):
        info_detail=self.get_queryset_object(Hotel,pk)
        if not info_detail:
           return Response(self.response.errorResponse(404,'Data Not Found'),status=status.HTTP_404_NOT_FOUND)        
        info_detail.delete()
        return Response(self.response.errorResponse(204, "Deleted Successfully"), status=status.HTTP_204_NO_CONTENT)

