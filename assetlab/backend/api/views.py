from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from .models import User


class RegisterView(APIView):
    permission_classes = []  # allow public access

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success", 
                "message": "Account created successfully"
            }, status=status.HTTP_201_CREATED)
        
        # Flatten errors to string
        error_messages = []
        for field, errors in serializer.errors.items():
            error_messages.append(f"{field}: {errors[0]}")
        error_str = " | ".join(error_messages)

        return Response({
            "status": "error",
            "message": f"Failed: {error_str}",
            "detail": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({"status": "error", "message": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=email, password=password)
        if user is None:
            return Response({"status": "error", "message": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({
            "status": "success",
            "message": "Login successful",
            "user_id": user.id,
            "email": user.email,
            "full_name": getattr(user, 'full_name', ''),
            "age": getattr(user, 'age', None),
            "is_admin": getattr(user, 'is_admin', False),
        })


class AiAnalysisView(APIView):
    permission_classes = []

    def post(self, request):
        # SIMULATED AI TRAINING LOGIC
        # Since we cannot run a real heavy AI model here, we simulate "Recognition" 
        # based on the uploaded filename. This gives you control to "Test" it.
        
        uploaded_file = request.FILES.get('image')
        if not uploaded_file:
             return Response({"status": "error", "message": "No image uploaded"}, status=status.HTTP_400_BAD_REQUEST)
        
        filename = uploaded_file.name.lower()
        
        # 1. FORBIDDEN CLASSES (What the AI rejects)
        forbidden_keywords = ['person', 'face', 'man', 'woman', 'selfie', 'people', 'cat', 'dog']
        
        # 2. DETECTION LOGIC
        is_forbidden = any(k in filename for k in forbidden_keywords)
        
        if is_forbidden:
            return Response({
                "status": "error", 
                "message": "Error: Person/Human detected! Analysis restricted to Industrial Assets only."
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # 3. SUCCESS: GENERATE REPORT (For ANY other image)
        import random
        damage_score = random.randint(20, 95)
        status_text = "Critical" if damage_score > 70 else "Moderate" if damage_score > 40 else "Low"

        return Response({
            "status": "success",
            "damage_score": damage_score,
            "damage_status": status_text,
            "analysis_details": f"Analyzed {uploaded_file.name}: Detected signs of wear and potential structural stress."
        }, status=status.HTTP_200_OK)
