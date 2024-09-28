from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.conf import settings
from .models import Waitlist
from .serializers import WaitlistSerializer

class WaitlistView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')  # Extract the email from the request
        if Waitlist.objects.filter(email=email).exists():
            return Response({"error": "This email is already on the waitlist."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = WaitlistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save the email to the database
            
            # Email template
            email_html_message = '''
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background-color: #f4f4f4; border-radius: 10px;">
                <div style="background-color: #19469D; color: white; padding: 15px; border-radius: 10px 10px 0 0; text-align: center;">
                    <h2 style="margin: 0;">Thank You for Joining Our Waitlist!</h2>
                </div>
                <div style="padding: 20px; background-color: white; border-radius: 0 0 10px 10px;">
                    <p style="font-size: 16px; color: #333;">Hi there,</p>
                    <p style="font-size: 16px; color: #333;">
                        Thank you for joining the waitlist for <strong>Refnet</strong>.
                        We’re excited to have you on board!
                    </p>
                    <p style="font-size: 16px; color: #333;">
                        You will be one of the first to know when we launch, and we can't wait to share our platform with you.
                    </p>
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="https://refnet.onrender.com/" style="display: inline-block; background-color: #19469D; color: white; padding: 10px 20px; border-radius: 5px; text-decoration: none;">Visit Our Website</a>
                    </div>
                    <p style="font-size: 14px; color: #777;text-align: center;">
                        If you have any questions, feel free to reach out to me personally at <a href="mailto:adigungodwin2@gmail.com" style="color: #19469D;">adigungodwin2@gmail.com</a>.
                    </p>
                </div>
                <div style="text-align: center; padding: 2px; font-size: 12px; color: #777;">
                    <p>&copy; 2024 Refnet. All rights reserved.</p>
                    <p>Lagos, Nigeria</p>
                </div>
            </div>
            '''

            # Send confirmation email
            send_mail(
                'Thank you for joining the waitlist',  # Subject
                '',  # Plain text body (optional)
                settings.DEFAULT_FROM_EMAIL,  # From email
                [serializer.validated_data['email']],  # To email
                fail_silently=False,
                html_message=email_html_message  # HTML content
            )

            return Response({"message": "Email added to the waitlist and confirmation sent!"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
