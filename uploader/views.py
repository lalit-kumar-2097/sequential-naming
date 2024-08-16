import os
import zipfile
import uuid
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import default_storage
from django.http import HttpResponse

def upload_files(request):
    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('files')
        if len(uploaded_files) > 50:
            return HttpResponse("You can only upload up to 50 files.")

        # Generate a unique ID for the session
        unique_id = str(uuid.uuid4())

        # Directories for files with and without extensions
        dir_with_ext = os.path.join(settings.MEDIA_ROOT, 'uploads', f'{unique_id}_with_ext')
        dir_without_ext = os.path.join(settings.MEDIA_ROOT, 'uploads', f'{unique_id}_without_ext')

        # Create the directories if they don't exist
        os.makedirs(dir_with_ext, exist_ok=True)
        os.makedirs(dir_without_ext, exist_ok=True)

        # Save files and rename them sequentially
        file_urls = []
        for i, file in enumerate(uploaded_files):
            # New names with and without extensions
            base_name = str(i + 1)
            ext = os.path.splitext(file.name)[1]
            new_name_with_ext = f"{base_name}{ext}"
            new_name_without_ext = base_name

            # Save files to both directories
            safe_path_with_ext = os.path.join(dir_with_ext, new_name_with_ext)
            safe_path_without_ext = os.path.join(dir_without_ext, new_name_without_ext)

            with open(safe_path_with_ext, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            with open(safe_path_without_ext, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            # Store the relative URL for the file with the extension
            file_urls.append(os.path.join('uploads', f'{unique_id}_with_ext', new_name_with_ext))

        # Zip the files in the directory without extensions
        zip_filename = f'renamed_files_{unique_id}.zip'
        zip_filepath = os.path.join(settings.MEDIA_ROOT, zip_filename)
        with zipfile.ZipFile(zip_filepath, 'w') as zipf:
            for i in range(len(uploaded_files)):
                filename = str(i + 1)
                file_path = os.path.join(dir_without_ext, filename)
                zipf.write(file_path, os.path.basename(file_path))

        # Generate download URL for the zip file
        download_url = default_storage.url(zip_filename)
        
        # Prepend MEDIA_URL to each file URL
        file_urls = [default_storage.url(file_url) for file_url in file_urls]

        return render(request, 'uploader/upload.html', {
            'download_url': download_url,
            'file_urls': file_urls,
        })

    return render(request, 'uploader/upload.html')

