from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import ContactSubmission, VideoConteudo
from .serializers import ContactSubmissionSerializer
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

class ContactSubmissionCreateView(generics.CreateAPIView):
    queryset = ContactSubmission.objects.all()
    serializer_class = ContactSubmissionSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        
        subject = f"Nova Solicitação de Contato: {instance.name}"
        message_body = f"Nome: {instance.name}\nEmail: {instance.email}\nTelefone: {instance.phone}\nMensagem: {instance.message}"
        
        try:
            send_mail(subject, message_body, settings.DEFAULT_FROM_EMAIL, ['clinicaarque.psi@gmail.com'])
        except Exception as e:
            print(f"Erro e-mail: {e}")

        return Response(serializer.data, status=status.HTTP_201_CREATED)

@csrf_exempt
def api_upload_video(request):
    if request.method == 'GET':
        try:
            videos = VideoConteudo.objects.all().order_by('-criado_em')
            data = []
            for v in videos:
                if v.video_file:
                    url = v.video_file.url
                    url = url.replace("http://", "https://")
                    
                    if "/upload/" in url:
                        url = url.replace("/upload/", "/upload/f_mp4,vc_h264,q_auto/")
                    
                    if not url.endswith(".mp4"):
                        url += ".mp4"
                    
                    data.append({
                        "id": v.id,
                        "titulo": v.titulo,
                        "video_file": url
                    })
            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({'status': 'erro', 'message': str(e)}, status=500)

    if request.method == 'POST':
        try:
            video = request.FILES.get('video_file')
            titulo = request.POST.get('titulo', 'Sem título')
            if video:
                novo = VideoConteudo.objects.create(titulo=titulo, video_file=video)
                return JsonResponse({'status': 'sucesso', 'url': novo.video_file.url}, status=201)
            return JsonResponse({'status': 'erro', 'message': 'Nenhum arquivo'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'erro', 'message': str(e)}, status=500)
            
    return JsonResponse({'status': 'erro', 'message': 'Metodo nao permitido'}, status=405)