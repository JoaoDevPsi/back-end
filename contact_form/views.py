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

# View para o formulário de contato (Antiga)
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

# Função para o Upload de Vídeo (Nova)
@csrf_exempt
def api_upload_video(request):
    if request.method == 'POST':
        try:
            video = request.FILES.get('video_file') or request.FILES.get('video')
            titulo = request.POST.get('titulo', 'Vídeo sem título')

            if video:
                novo = VideoConteudo.objects.create(titulo=titulo, video_file=video)
                return JsonResponse({'status': 'sucesso', 'url': novo.video_file.url}, status=201)
            
            return JsonResponse({'status': 'erro', 'message': 'Nenhum arquivo enviado'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'erro', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'erro', 'message': 'Metodo nao permitido'}, status=405)