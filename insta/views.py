import os

from django.http import HttpResponse
from django.shortcuts import render, redirect

from hhtest.settings import BASE_DIR
from insta.form import AddQuote
from .models import Post, VideoPost, Quote
from PIL import ImageDraw
from PIL import Image
from PIL import ImageFont
from django.views.generic.edit import CreateView
import moviepy.editor as mp
from moviepy.video.compositing.CompositeVideoClip import clips_array
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
import json
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import PostSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import urllib.request
import io

class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer

@api_view(['GET', 'POST'])
def post_collection(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = {'description': request.data.get('description'), 'img_url': request.data.get('img_url')}
        serializer = PostSerializer(data=data)
        # description = request.POST.get('description')
        # img_url = request.POST.get('img_url')

        if serializer.is_valid():
            serializer.save()
            if data['description'] and data['img_url']:
                image(data['description'], 'insta.jpg', 'out.png')
                with urllib.request.urlopen(data['img_url']) as url:
                    f = io.BytesIO(url.read())
                photo = Image.open(f)
                photo = photo.resize((1181, 848))
                out = Image.open(os.path.join(BASE_DIR, 'media', 'out.png'), 'r')
                out.paste(photo, (0, 0))
                out.save(os.path.join(BASE_DIR, 'media', 'out.png'))
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def image(txt, img, out):
    texts = txt.splitlines()
    mx = 0
    t = ''
    for text in texts:
        if len(text.strip()) > mx:
            mx = len(text.strip())
            t = text.strip()
    insta = Image.open(os.path.join(BASE_DIR, 'media', img), 'r')
    bg_w, bg_h = insta.size
    for sz in range(50, 150):
        font = ImageFont.truetype(os.path.join(BASE_DIR, 'media', 'NotoSerif-Bold.ttf'), sz)
        (width, baseline), (offset_x, offset_y) = font.font.getsize(t)
        if width > bg_w:
            font = ImageFont.truetype(os.path.join(BASE_DIR, 'media', 'NotoSerif-Bold.ttf'), sz - 4)
            break
    draw = ImageDraw.Draw(insta)
    h = 0
    w = 940 - (len(texts) - 1) * 20
    for text in texts:
        (width, baseline), (offset_x, offset_y) = font.font.getsize(text.strip())
        draw.text(((bg_w - width) / 2, w + h), text.strip(), (255, 255, 255), font=font)
        h += 90
    insta.save(os.path.join(BASE_DIR, 'media', out))


class Create(CreateView):
    model = Post
    template_name = 'home.html'
    success_url = 'newpost'
    fields = ['description', 'img', 'category']


class CreateOctagon(CreateView):
    model = Post
    template_name = 'octagon.html'
    success_url = 'newoctagon'
    fields = ['description', 'img']


def newpost(request):
    template = 'newpost.html'
    context = {}
    if request.method == 'POST':
        txt = request.POST.get('txt')
        if txt:
            image(txt, 'insta.jpg', 'out.png')

        return HttpResponse(json.dumps({}), content_type='application/json')

    last = Post.objects.last()
    if last:
        image(last.description, last.category.img, 'out.png')
        photo = Image.open(os.path.join(BASE_DIR, 'media', last.img.name), 'r')
        photo = photo.resize((1181, 848))
        out = Image.open(os.path.join(BASE_DIR, 'media', 'out.png'), 'r')
        out.paste(photo, (0, 0))
        out.save(os.path.join(BASE_DIR, 'media', 'out.png'))

        Post.objects.all().delete()

    return redirect('home')

    # return render(request, template, context)


def newoctagon(request):
    template = 'newoctagon.html'
    context = {}
    last = Post.objects.last()
    if last:
        image(last.description, 'octagon.jpg', 'newoctagon.jpg')
        photo = Image.open(last.img.url, 'r')
        photo = photo.resize((1181, 848))
        out = Image.open('/media/newoctagon.jpg', 'r')
        out.paste(photo, (0, 0))
        out.save('/media/newoctagon.jpg')
        Post.objects.all().delete()
    return render(request, template, context)


class VideoCreate(CreateView):
    model = VideoPost
    template_name = 'video.html'
    fields = ['description', 'video']


def newvideo(request):
    template = 'newvideo.html'
    context = {}
    last = VideoPost.objects.last()
    image(last.description)
    # out = Image.open('/home/gamer/hhtest/media/out.png', 'r')
    # bg_w, bg_h = out.size
    # img = out.crop((0, 848, bg_w, bg_h))
    # img.save('/home/gamer/hhtest/media/out.png')
    video = mp.VideoFileClip('/home/gamer/hhtest/media/my_stack.mp4')
    # photo = Image.open('/home/gamer/hhtest/media/out.png', 'r')
    # photo = photo.resize((video.size[0], video.size[0] // 3))
    # photo.save('/home/gamer/hhtest/media/out.png')
    img = mp.ImageClip('/home/gamer/hhtest/media/insta.jpg').set_duration(video.duration)
    final_clip = clips_array([[video],
                              [img]])

    final_clip.write_videofile('/home/gamer/hhtest/media/newvideo.mp4')

    return render(request, template, context)


def news(request):
    template_name = 'news.html'
    # html  = urlopen("https://news.sputnik.ru/")
    # json_response = json.load(response)
    # r  = requests.get("http://news.sputnik.ru/?PID=2001")
    # data = r.text
    # context = {'ozodi': html}
    # soup = BeautifulSoup(data)
    # for link in soup.find_all('a'):
    #     print(link.get('href'))
    return render(request, template_name=template_name)


def quote(request):
    template_name = 'quote.html'
    last = Quote.objects.last()
    if last:
        form = AddQuote(instance=last)
    else:
        form = AddQuote()
    if request.method == 'POST':
        if last:
            new_quote = AddQuote(request.POST, request.FILES, instance=last)
        else:
            new_quote = AddQuote(request.POST, request.FILES)
        if new_quote.is_valid():
            new_quote = new_quote.save()
            form = AddQuote(instance=new_quote)
    context = {'form': form}
    if last:
        from PIL import Image, ImageOps, ImageDraw

        #image(last.description, 'quote.png', 'out_quote.png')
        im = Image.open(os.path.join(BASE_DIR, 'media', last.img.name), 'r')
        im = im.resize((400, 400))

        bigsize = (im.size[0] * 3, im.size[1] * 3)
        mask = Image.new('L', bigsize, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(im.size, Image.ANTIALIAS)
        im.putalpha(mask)

        out = Image.open(os.path.join(BASE_DIR, 'media', 'quote.png'), 'r')
        out.paste(im, (120, 980), im)
        out.save(os.path.join(BASE_DIR, 'media', 'out_quote.png'))

        quote = Image.open(os.path.join(BASE_DIR, 'media', 'out_quote.png'), 'r')
        bg_w, bg_h = quote.size
        font = ImageFont.truetype(os.path.join(BASE_DIR, 'media', 'Alegreya-Bold.ttf'), 55)
        font1 = ImageFont.truetype(os.path.join(BASE_DIR, 'media', 'Alegreya-Regular.ttf'), 40)
        draw = ImageDraw.Draw(quote)
        h = 550
        w = 1200
        draw.text((h, w), last.author.upper(), (0, 0, 0), font=font)
        draw.text((h, w + 80), last.position.upper(), (0, 0, 0), font=font1)

        last.description = last.description.upper()
        for sz in range(45, 80):
            h = 450
            w = 0
            for text in last.description.replace('\r\n', ' ').split(' '):
                font = ImageFont.truetype(os.path.join(BASE_DIR, 'media', 'Alegreya-BoldItalic.ttf'), sz)
                (width, baseline), (offset_x, offset_y) = font.font.getsize(text)
                if h + width + 30 > bg_w:
                    h = 420
                    w += 80
                h += width + 30
            if (1100 - w) / 2 <= 200:
                break
        print(w)
        w = (1100 - w) / 2
        h = 450
        print(h)
        print(w)
        print(sz)
        for text in last.description.replace('\r\n', ' ').split(' '):
            font = ImageFont.truetype(os.path.join(BASE_DIR, 'media', 'Alegreya-BoldItalic.ttf'), sz)
            (width, baseline), (offset_x, offset_y) = font.font.getsize(text)
            if h + width + 30 > bg_w:
                h = 450
                w += 80
            draw.text((h, w), text, (255, 255, 255), font=font)
            h += width + 30

        quote.save(os.path.join(BASE_DIR, 'media', 'out_quote.png'))

    return render(request, template_name=template_name, context=context)


def quote_image(txt, img, out):
    texts = txt.splitlines()
    mx = 0
    t = ''
    for text in texts:
        if len(text.strip()) > mx:
            mx = len(text.strip())
            t = text.strip()
    quote = Image.open(os.path.join(BASE_DIR, 'media', img), 'r')
    bg_w, bg_h = quote.size
    for sz in range(50, 150):
        font = ImageFont.truetype(os.path.join(BASE_DIR, 'media', 'NotoSerif-Bold.ttf'), sz)
        (width, baseline), (offset_x, offset_y) = font.font.getsize(t)
        if width > bg_w:
            font = ImageFont.truetype(os.path.join(BASE_DIR, 'media', 'NotoSerif-Bold.ttf'), sz - 4)
            break
    draw = ImageDraw.Draw(quote)
    h = 0
    w = 940 - (len(texts) - 1) * 20
    for text in texts:
        (width, baseline), (offset_x, offset_y) = font.font.getsize(text.strip())
        draw.text(((bg_w - width) / 2, w + h), text.strip(), (255, 255, 255), font=font)
        h += 90
    quote.save(os.path.join(BASE_DIR, 'media', out))
