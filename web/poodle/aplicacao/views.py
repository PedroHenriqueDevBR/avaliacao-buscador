from django.shortcuts import render
from aplicacao.meus_models import Indexador


def home(request):
    if request.method == 'POST':
        busca = request.POST.get('keyword')
        urlinicial = request.POST.get('urlinicial')
        deth = request.POST.get('deth')

        if len(busca) > 0 and len(urlinicial) > 0 and len(deth) > 0:
            deth = int(deth)
            buscador = Indexador()
            buscador.seach(busca, urlinicial, deth)
            resultado = buscador.matchs
            return render(request, 'resultado.html', {'resultados': resultado})

    return render(request, 'index.html')


def resultado(request):
    return render(request, 'resultado.html')
