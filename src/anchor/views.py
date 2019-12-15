# encoding=utf-8
# 表示するメッセージを記入、テンプレートを呼び出す

from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

from .forms import PhotoForm
from .models import Photo


def index(request):
    template = loader.get_template('anchor/index.html')
    context = {'form': PhotoForm()}
    return HttpResponse(template.render(context, request))


def predict(request):
    if not request.method == "POST":
        return
        redirect('anchor:index')

    form = PhotoForm(request.POST, request.FILES)
    if not form.is_valid():
        raise ValueError("Formが不正です")

    photo = Photo(image=form.cleaned_data['image'])
    result, predicted = photo.predict()

    label = {
        'Fuji': 'フジテレビ',
        'Asahi': 'テレビ朝日',
        'Japan': '日本テレビ',
        'NHK': 'NHK',
        'TBS': 'TBS',
    }

    template = loader.get_template('anchor/result.html')

    if predicted == None:
        context = {
            'photo_name': photo.image.name,
            'photo_data': photo.image_src(),
            'predicted': "顔が認識できませんでした",
            'Asahi': None,
            'Fuji': None,
            'Japan': None,
            'NHK': None,
            'TBS': None,
        }

        return HttpResponse(template.render(context, request))

    context = {
        'photo_name': photo.image.name,
        'photo_data': photo.image_src(),
        'predicted': label[predicted],
        'Asahi': str(round(result[0]*100, 1)) + '%',
        'Fuji': str(round(result[1]*100, 1)) + '%',
        'Japan': str(round(result[2]*100, 1)) + '%',
        'NHK': str(round(result[3]*100, 1)) + '%',
        'TBS': str(round(result[4]*100, 1)) + '%',
    }
    return HttpResponse(template.render(context, request))
