# from django.shortcuts import render

# # Create your views here.

# import os
# import zipfile
# from django.shortcuts import render
# from django.conf import settings
# from django.core.files.storage import FileSystemStorage
# from django.http import HttpResponse
# from django.utils.text import slugify

# def upload_files(request):
#     if request.method == 'POST':
#         uploaded_files = request.FILES.getlist('files')
#         if len(uploaded_files) > 50:
#             return HttpResponse("You can only upload up to 50 files.")

#         # Store files
#         fs = FileSystemStorage()
#         upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
#         if not os.path.exists(upload_dir):
#             os.makedirs(upload_dir)

#         # Save files and rename them sequentially
#         for i, file in enumerate(uploaded_files):
#             new_name = f"{i + 1}{os.path.splitext(file.name)[1]}"
#             fs.save(os.path.join('uploads', new_name), file)

#         # Zip the files
#         zip_filename = 'renamed_files.zip'
#         zip_filepath = os.path.join(settings.MEDIA_ROOT, zip_filename)
#         with zipfile.ZipFile(zip_filepath, 'w') as zipf:
#             for i in range(len(uploaded_files)):
#                 filename = f"{i + 1}{os.path.splitext(uploaded_files[i].name)[1]}"
#                 file_path = os.path.join(upload_dir, filename)
#                 zipf.write(file_path, os.path.basename(file_path))

#         download_url = fs.url(zip_filename)
#         return render(request, 'uploader/upload.html', {'download_url': download_url})

#     return render(request, 'uploader/upload.html')






import os
import zipfile
import uuid
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse

def upload_files(request):
    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('files')
        if len(uploaded_files) > 50:
            return HttpResponse("You can only upload up to 50 files.")

        # Generate a unique ID for the session
        unique_id = str(uuid.uuid4())

        # Store files in a unique directory
        fs = FileSystemStorage()
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads', unique_id)
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        # Save files and rename them sequentially without extensions
        for i, file in enumerate(uploaded_files):
            new_name = str(i + 1)  # Just the number, no extension
            fs.save(os.path.join('uploads', unique_id, new_name), file)

        # Zip the files with a unique name
        zip_filename = f'renamed_files_{unique_id}.zip'
        zip_filepath = os.path.join(settings.MEDIA_ROOT, zip_filename)
        with zipfile.ZipFile(zip_filepath, 'w') as zipf:
            for i in range(len(uploaded_files)):
                filename = str(i + 1)  # Just the number, no extension
                file_path = os.path.join(upload_dir, filename)
                zipf.write(file_path, os.path.basename(file_path))

        download_url = fs.url(zip_filename)
        return render(request, 'uploader/upload.html', {'download_url': download_url})

    return render(request, 'uploader/upload.html')
