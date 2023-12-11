import base64
from django.http import HttpResponse
from django.shortcuts import render
from .forms import QRCodeForm
from io import BytesIO
import qrcode
import re 


def modify_google_drive_url(url):
    """
    Transform the Google Drive sharing URL to a direct download link.
    """
    # Pattern for Google Drive sharing URLs
    pattern = r"https://drive\.google\.com/file/d/(.+?)/view\?usp=sharing"
    replacement_pattern = r"https://drive\.google\.com/uc?export=download&id=\1"
    return re.sub(pattern, replacement_pattern, url)



def qr_code_request(request):
    if request.method == 'POST':
        form = QRCodeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['data']
            size = form.cleaned_data['size']
            border = form.cleaned_data['border']
            fill_color = form.cleaned_data['fill_color']
            back_color = form.cleaned_data['back_color']
            transparent_background = form.cleaned_data['transparent_background']
            is_google_drive_link = form.cleaned_data.get('is_google_drive_link', False)
            
            if is_google_drive_link:
                data = modify_google_drive_url(data)

            # Create the QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=size,
                border=border,
            )
            qr.add_data(data)
            qr.make(fit=True)

            # Set back_color to None for a transparent background
            if transparent_background:
                back_color = None

            img = qr.make_image(fill_color=fill_color, back_color=back_color)

            # Save QR code to a BytesIO object
            img_bytes = BytesIO()
            img.save(img_bytes, format='PNG')
            # Instead of returning a downloadable response, embed the image in base64
            img_bytes.seek(0)
            base64_image = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
            img_bytes.close()

            # Embed the base64 image in the context
            qr_code_data = f"data:image/png;base64,{base64_image}"

            return render(request, 'qrapp/qr_form.html', {
                'form': form,
                'qr_code_data': qr_code_data,  # Pass the base64 image data to the template
            })
    else:
        form = QRCodeForm()

    return render(request, 'qrapp/qr_form.html', {'form': form})
