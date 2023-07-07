from django.contrib import admin
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html

from snippets.models import Manager, Driver, Trip, TripHistory, TripDrowsiness, TripHandsOff, Device

from django_admin_geomap import ModelAdmin




from django.urls import reverse
from django.utils.html import format_html


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    def get_exclude(self, request, obj=None):
        # Exclui o campo 'password' apenas durante a visualização
        if obj:
            return ('password',)
        return ()
    pass

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        # Obtém a lista de readonly_fields da classe pai
        readonly_fields = super().get_readonly_fields(request, obj)

        # Adiciona 'password' à lista de campos readonly_fields somente na visualização
        if obj:
            readonly_fields += ('trips_count','manager')
        return readonly_fields

    def get_exclude(self, request, obj=None):
        # Exclui o campo 'password' apenas durante a visualização
        if obj:
            return ('password',)
        return ()
    pass

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):

    list_display = ("id", "count_hist", "custom_actions")

    def get_exclude(self, request, obj=None):
        # Exclui o campo 'driver_id' para o manager na visualização
        if request.user.is_superuser or request.user.has_perm('snippets.add_driver'):
            if obj:
                return ('device_id',)
        return ()

    def get_readonly_fields(self, request, obj=None):
        # Obtém a lista de readonly_fields da classe pai
        readonly_fields = super().get_readonly_fields(request, obj)
        if not(self.request.user.is_superuser or self.request.user.has_perm('snippets.add_driver')):    #se for um motorista...
            # Adiciona 'password' à lista de campos readonly_fields somente na visualização
            if obj:
                readonly_fields += ('start','end','driver','real_start','real_end','is_started','is_ended')
        else: #se for um gerente...
            if obj:
                readonly_fields += ('real_start','real_end','is_started','is_ended')
        return readonly_fields


    def get_queryset(self, request):
        # Obtém o queryset padrão do ModelAdmin
        queryset = super().get_queryset(request)
        
        # Verifica se o usuário é um superusuário ou um manager
        if request.user.is_superuser or request.user.has_perm('snippets.add_driver'):   #somente superusers ou managers tem acesso total a todas as trips (managers aqui sao identificados se o usuario autenticado no momento possui a permissao de add_driver)
            return queryset
        
        currentDriver = Driver.objects.get(username=request.user.get_username())
        querysetTrips = Trip.objects.filter(driver=currentDriver)    
        
        return querysetTrips

    def count_hist(self, obj):
        count = TripHistory.objects.filter(trip=obj).count()
        url = (
            reverse("admin:snippets_triphistory_changelist")
            + "?"
            + urlencode({"trip__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} Histories</a>', url, count)

    count_hist.short_description = "Trip History"

    def count_drowsy(self, obj):
        count = TripDrowsiness.objects.filter(trip=obj).count()
        url = (
            reverse("admin:snippets_tripdrowsiness_changelist")
            + "?"
            + urlencode({"trip__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} Alerts</a>', url, count)

    count_drowsy.short_description = "Trip Drowsiness Alerts"

    def count_handsoff(self, obj):
        count = TripHandsOff.objects.filter(trip=obj).count()
        url = (
            reverse("admin:snippets_triphandsoff_changelist")
            + "?"
            + urlencode({"trip__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} Alerts</a>', url, count)
    
    count_handsoff.short_description = "Trip Hands Off Alerts"


    def get_actions(self, request):
        self.request = request
        return super().get_actions(request)
    

    def custom_actions(self, obj):
        if not(self.request.user.is_superuser or self.request.user.has_perm('snippets.add_driver')):    #se for um motorista...
            start_url = reverse("start-trip", args=[obj.id])
            end_url = reverse("end-trip", args=[obj.id])
            start_disabled = ""  # inicialmente, o botão Start está ativado
            end_disabled = ""  # inicialmente, o botão End está ativado

            # Verificar se a viagem já foi iniciada ou finalizada
            if obj.is_started:  # substitua "trip.is_started" pelo atributo correto que indica se a viagem já foi iniciada
                start_disabled = "disabled"  # desativar o botão Start
            if obj.is_ended:  # substitua "trip.is_ended" pelo atributo correto que indica se a viagem já foi encerrada
                end_disabled = "disabled"  # desativar o botão End

            return format_html(
                '<a class="button" href="{}" {}>Start</a>&nbsp;'
                '<a class="button" href="{}" {}>End</a>',
                start_url, start_disabled,
                end_url, end_disabled
            )
    custom_actions.short_description = "Actions"
    custom_actions.allow_tags = True    

@admin.register(TripHistory)
class TripHistoryAdmin(ModelAdmin, admin.ModelAdmin):
    list_display = ("id", 'speed', 'hands_state', 'drowsy_state', 'acc')
    geomap_autozoom = "100"

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("id","device_number")

   

admin.site.site_header = 'AutoFleet'
#admin.site.register(TripHistory, TripHistoryAdmin)