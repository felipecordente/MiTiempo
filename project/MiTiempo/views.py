from django.shortcuts import render
from django.http import HttpResponse
from . import leer_json, leer_xml
from django.template import loader
from .models import Pueblo, Usuario, Comentario
import random, string
from django.utils.datastructures import MultiValueDictKeyError
import copy

diccionario = leer_json.main()
estado = 0
# Create your views here.
def control_login(request, cambiar_estado = False):
    contenido = ""
    loggin = False
    name = "none"
    cookie = ""

    if request.POST and request.path == "/" and not cambiar_estado:
        try:
            request.POST['logout']
            usuario = Usuario.objects.get(cookie = request.COOKIES['cookie']).name
            cookie = "0"
            contenido = "Usuario " + usuario + " deslogueado."
        except MultiValueDictKeyError:
            name = request.POST['name']
            password = request.POST['password']
            try:
                usuario = Usuario.objects.get(name = name, password = password)
                contenido = ("Usuario " + name + " autenticado")
                cookie = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(20))
                usuario.cookie = cookie
                usuario.save()
                loggin = True
            except Usuario.DoesNotExist:
                contenido = ("El usuario " + name + " o la contraseña no son correctos.")
    else:
        try:
            cookie = request.COOKIES['cookie']
            try:
                usuario = Usuario.objects.get(cookie = cookie)
                loggin = True
                name = str(usuario.name)
            except Usuario.DoesNotExist:
                contenido = "cookie erronea"
        except KeyError:
            print("No se ha recibido cookie")

    return cookie, loggin, name, contenido

def ordenar_municipios(municipios):
    #array contiene un array de arrays, donde el primer elemento es el num_comentarios
    # y el segundo el id de ese municipio
    array = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
    array_final = [0,0,0,0,0,0,0,0,0,0]
    aux = [0,0]
    aux2 = [0,0]
    for municipio in municipios:
        for i in reversed(range(0,10)):
            if municipio.num_comentarios >= array[i][0]:
                if i == 0:
                    aux[0] = array[0][0]
                    aux[1] = array[0][1]
                    array[0][0] = municipio.num_comentarios
                    array[0][1] = municipio
                    array_final[0] = municipio
                    for j in range(1,10):
                        aux2[0] = array[j][0]
                        aux2[1] = array[j][1]
                        array[j][0] = aux[0]
                        array[j][1] = aux[1]
                        array_final[j] = aux[1]
                        aux[0] = aux2[0]
                        aux[1] = aux2[1]
            if municipio.num_comentarios < array[i][0]:
                for j in range(i+1,10):
                    #primera iteracion
                    if j == (i+1):
                        aux[0] = array[j][0]
                        aux[1] = array[j][1]
                        array[j][0] = municipio.num_comentarios
                        array[j][1] = municipio
                        array_final[j] = municipio
                    else:
                        aux2[0] = array[j][0]
                        aux2[1] = array[j][1]
                        array[j][0] = aux[0]
                        array[j][1] = aux[1]
                        array_final[j] = aux[1]
                        aux[0] = aux2[0]
                        aux[1] = aux2[1]
                break

    return array_final

def pagina_principal(request):
    format = request.GET.get('format')
    if format == "xml":
        municipios = Pueblo.objects.all()
        municipios=ordenar_municipios(municipios)
        template = loader.get_template('pagina_principal.xml')
        xml = template.render({'municipios':municipios,
                                'titulo':"Pagina principal."}, request)
        return HttpResponse(xml, "text/xml")

    cambiar_estado = False
    for x in request.POST:
        if x == "estado":
            cambiar_estado = True
    cookie, loggin, name, contenido = control_login(request,cambiar_estado)

    if request.method == "GET" or cambiar_estado:
        global estado
        municipios = Pueblo.objects.all()
        if cambiar_estado:
            estado = (estado + 1) % 3
        if estado == 0:
            filtrado = "Probabilidad de lluvia mayor a 0%"
        if estado == 1:
            filtrado = "Probabilidad de lluvia igual a 0%"
        if estado == 2:
            filtrado = "10 municipios con más comentarios."
            municipios=ordenar_municipios(municipios)

        usuarios = Usuario.objects.all()
        template = loader.get_template('pagina_principal.html')
        html = template.render({'loggin':loggin,
                                'municipios':municipios,
                                'filtrado':filtrado,
                                'estado':estado,
                                'usuarios':usuarios,
                                'nombre_usuario':name}, request)

        response = (HttpResponse(html))
    else:
        template = loader.get_template('base.html')
        html = template.render({'contenido':contenido, 'loggin':loggin,
                                'nombre_usuario':name}, request)

        response = (HttpResponse(html))

    if cookie != "":
        response.set_cookie('cookie', cookie)
    return(response)

def pagina_info(request):
    _, loggin, name,_ = control_login(request)

    template = loader.get_template('info.html')
    html = template.render({'loggin':loggin,
                            'nombre_usuario':name}, request)
    return (HttpResponse(html))

def pagina_municipios(request):
    _, loggin, name, _ = control_login(request)

    format = request.GET.get('format')
    if format == "xml":
        municipios = Pueblo.objects.all()
        template = loader.get_template('pagina_municipios.xml')
        xml = template.render({'municipios':municipios}, request)
        return HttpResponse(xml, "text/xml")

    temperatura = ""
    if request.method == "POST":
        temperatura = request.POST['temperatura']
        temperatura = temperatura.split('º')[0]
        temperatura = int(temperatura)

    rango_temperaturas = list(range(-10, 51))
    municipios = Pueblo.objects.all()
    template = loader.get_template('pagina_municipios.html')
    html = template.render({'municipios':municipios,
                            'loggin':loggin,
                            'rango_temperaturas':rango_temperaturas,
                            'temperatura':temperatura,
                            'nombre_usuario':name}, request)

    response = (HttpResponse(html))
    return(response)

def pagina_municipio(request, id):
    _, loggin, name,_ = control_login(request)

    try:
        municipio = Pueblo.objects.get(p_id = id)
        url_xml = municipio.url_xml
        municipio.url_html, municipio.prob_lluvia, municipio.descripcion, municipio.temp_max, municipio.temp_min = leer_xml.main(url_xml)
        municipio.save()
        if request.method == "POST":
            comentario_nuevo = request.POST['comentario']
            usuario = Usuario.objects.get(name = name)
            Comentario(texto = comentario_nuevo, pueblo = municipio, usuario = usuario).save()
            municipio.num_comentarios = municipio.num_comentarios + 1
            municipio.save()

        try:
            comentarios = Comentario.objects.filter(pueblo = municipio)
        except Comentario.DoesNotExist:
            print("no hay comentarios")


        template = loader.get_template('pagina_municipio.html')
        html = template.render({'loggin':loggin,
                                'municipio':municipio,
                                'comentarios':comentarios,
                                'nombre_usuario':name}, request)
    except Pueblo.DoesNotExist:
        contenido = "El recurso al que estas intentando acceder no existe."
        template = loader.get_template('base.html')
        html = template.render({'contenido':contenido, 'loggin':loggin,
                                'nombre_usuario':name}, request)

    return (HttpResponse(html))

def pagina_users(request):
    _, loggin, name, _ = control_login(request)

    usuarios = Usuario.objects.all()

    template = loader.get_template('list.html')
    html = template.render({'usuarios':usuarios, 'loggin':loggin,
                            'nombre_usuario':name}, request)

    return(HttpResponse(html))

def add_pueblo(usuario, municipio):
    name = municipio['nombre']
    id = municipio['id'][2:]
    url_xml = "http://www.aemet.es/xml/municipios/localidad_" + id + ".xml"
    altitud = municipio['altitud']
    longitud = municipio['longitud']
    latitud = municipio['latitud']
    num_comentarios = 0
    url_html, prob_precipitacion, descripcion, t_maxima, t_minima = leer_xml.main(url_xml)
    p =  Pueblo(name = name, p_id = id, url_xml = url_xml, url_html = url_html,
                temp_min = t_minima, temp_max = t_maxima, prob_lluvia = prob_precipitacion,
                altitud = altitud, longitud = longitud, latitud = latitud,
                descripcion = descripcion, num_comentarios = num_comentarios)
    p.save()
    usuario.pueblos.add(p)
    return

def pagina_usuario(request, nombre):
    _, loggin, name, _ = control_login(request)

    contenido = ""
    if name == nombre:
        usuario = Usuario.objects.get(name = name)
        if request.method == "POST":
            for x in request.POST:
                if x == "titulo":
                    usuario.titulo_pagina = request.POST['titulo']
                    usuario.save()
                    contenido = "Se ha cambiado el título de la página"
                if x == "municipio":
                    nombre_municipio = request.POST['municipio']
                    try:
                        municipio = diccionario[nombre_municipio]
                        municipio = Pueblo.objects.get(name = municipio['nombre'])
                        usuario.pueblos.add(municipio)
                        contenido = municipio.name + " ha sido seleccionada por " + nombre
                    except Pueblo.DoesNotExist:
                        print("no esta en la base de datos")
                        add_pueblo(usuario, municipio)
                        contenido = "Se añadió " + municipio['nombre'] + " a la base de datos."
                    except KeyError:
                        contenido = nombre_municipio + " no es un municipio(revisa las mayúsculas y las tildes)."
                if x == "color_fondo":
                    color = request.POST['color_fondo']
                    usuario.color_fondo = color
                    usuario.save()
                if x == "color_letra":
                    color = request.POST['color_letra']
                    usuario.color = color
                    usuario.save()
                if x == "tamaño":
                    size = request.POST['tamaño']
                    usuario.size = size
                    usuario.save()
                if x == "eliminar":
                    municipio = request.POST['eliminar']
                    usuario.pueblos.remove(Pueblo.objects.get(name = municipio))

    try:
        usuario = Usuario.objects.get(name = nombre)
        municipios = usuario.pueblos.all()
        format = request.GET.get('format')
        if format == "xml":
            titulo = "Municipios selecionados por " + usuario.name
            template = loader.get_template('pagina_principal.xml')
            xml = template.render({'municipios':municipios,
                                    'titulo':titulo}, request)
            return HttpResponse(xml, "text/xml")

        template = loader.get_template('pagina_usuario_log.html')
        html = template.render({'loggin':loggin,
                                'nombre_usuario':name,
                                'name':nombre,
                                'contenido':contenido,
                                'municipios':reversed(municipios),
                                'titulo_pagina':usuario.titulo_pagina}, request)
    except Usuario.DoesNotExist:
        contenido = "El recurso al que estas intentando acceder no existe."
        template = loader.get_template('base.html')
        html = template.render({'contenido':contenido, 'loggin':loggin,
                                'nombre_usuario':name}, request)
    return(HttpResponse(html))

def servir_css(request):
    _, loggin, name, _ = control_login(request)

    color_fondo = ""
    color_letra = ""
    size = ""
    if loggin:
        usuario = Usuario.objects.get(name = name)
        color_fondo = usuario.color_fondo
        color_letra = usuario.color
        size = usuario.size


    template = loader.get_template('main.css')
    css = template.render({'color_fondo':color_fondo,
                            'color_letra':color_letra,
                            'size':size}, request)

    return (HttpResponse(css, "text/css"))
