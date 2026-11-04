from rest_framework.serializers import ValidationError

def validate_video_link(value):
    if "youtube.com" not in value:
        raise ValidationError("Ссылка должна вести только на youtube.com!")