from django.db import models

# Create your models here.
class Pueblo(models.Model):
    name = models.CharField(max_length = 30)
    p_id = models.CharField(max_length = 10)
    url_xml = models.CharField(max_length = 500)
    url_html = models.CharField(max_length = 500)
    temp_min = models.IntegerField()
    temp_max = models.IntegerField()
    prob_lluvia = models.IntegerField()
    altitud = models.CharField(max_length = 200)
    longitud = models.CharField(max_length = 200)
    latitud = models.CharField(max_length = 200)
    descripcion = models.CharField(max_length = 400)
    num_comentarios = models.IntegerField()

    def  __str__(self):
        return self.name

class Usuario(models.Model):
    name = models.CharField(max_length = 10)
    password = models.CharField(max_length = 20)
    titulo_pagina = models.CharField(max_length = 100, default="Página usuario")
    size = models.IntegerField(default = 15)
    color = models.CharField(max_length = 50, default = "#1d7ffd")
    color_fondo = models.CharField(max_length = 50, default = "lightblue")
    pueblos = models.ManyToManyField(Pueblo, blank=True)
    cookie = models.CharField(max_length = 20, blank=True)

    def  __str__(self):
        return self.name

class Comentario(models.Model):
    texto = models.CharField(max_length = 1000)
    pueblo = models.ForeignKey(Pueblo, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def  __str__(self):
        return self.texto
