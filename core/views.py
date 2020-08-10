from django.views.generic.base import TemplateView
from django.shortcuts import render
from .forms import TMCForm
import datetime
import requests
import json


class HomePageView(TemplateView):
    template_name = "core/tmc.html"
    status_code = 200
    
    #Funcion a consultar en TMC
    def f_fecha(self, fecha):
        if fecha>=datetime.datetime(fecha.year, fecha.month, 15):
            return datetime.datetime(fecha.year, fecha.month, 15)
        else:
            return datetime.datetime(fecha.year, fecha.month-1, 15)
    
    #Funcion obteher el tipo de TMC
    def f_tipos(self,dia,uf):        
        #Se devuelve lista por haber varios codigos con misma definicion
        if dia<90: 
            if 5000<uf:
                return [11, 25]
            elif uf<=5000:    
                return [26]
        elif dia>=90:
            if uf<=50:
                return [45]
            elif 50<uf<=200:
                return [44] 
            elif 200<uf<=5000:
                return [8, 27, 35]
            elif 5000<uf:
                return [9, 29, 34]             
    
    #Funcion que retorna el valor de TMC
    def f_TMC(self,request):
        montoUF = float(request.POST.get('montoUF',''))
        plazo = int(request.POST.get('plazo',''))
        fechaSolicitud= datetime.datetime.strptime(request.POST.get('fechaSolicitud',''), '%Y-%m-%d')
        fechaSolicitud = self.f_fecha(fechaSolicitud)

        req = "https://api.sbif.cl/api-sbifv3/recursos_api/tmc/"+str(fechaSolicitud.year)+"/"+str(fechaSolicitud.month)+"?apikey=9c84db4d447c80c74961a72245371245cb7ac15f&formato=json"
                
        try:
            resp = requests.get(req)
            jresp = json.loads(resp.content)
        except:
            #En caso de fallar consulta a api devuelve None
            self.status_code = 599
            return None
                
        #Se itera lista posible de tipo por repeticion en sus definiciones
        TMCList = []
        self.status_code = 404
        for tipo in self.f_tipos(plazo, montoUF):                
            try:
                TMCList = list(filter(lambda x:x["Tipo"]==str(tipo),jresp["TMCs"]))
                self.status_code = 200
            except:
                print(tipo)
        return TMCList[0]['Valor'].replace(".",",")
    
    #Funcion que visualiza la vista en caso de consultar
    def post(self, request, *args, **kwargs):
        TMC = "No Encontrado"
        tcm_form = TMCForm(data=request.POST)
        if tcm_form.is_valid():
            TMC = self.f_TMC(request)        
        return render(request,self.template_name,{'form':tcm_form, 'tmc':TMC, 'status_code': self.status_code} )
    
    #Funcion que visualiza la vista
    def get(self, request, *args, **kwargs):
        return render(request,self.template_name,{'form':TMCForm(), 'tmc':'0', 'status_code': 200} )