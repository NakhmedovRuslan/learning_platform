from rest_framework.serializers import ValidationError

video_hosting = "youtube.com"

def validate_video_link(value):
    if value.lower() != video_hosting:
        raise ValidationError("Ссылка должна вести только на youtube.com!")