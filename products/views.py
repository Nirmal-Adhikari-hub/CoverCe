import mimetypes

from django.contrib.auth.decorators import user_passes_test,login_required 
from django.http import FileResponse, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, Http404
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, ProductAttachment
from .forms import ProductForm, ProductUpdateForm, ProductAttachmentInlineFormSet, ProductAttachmentModelFormSet
from azure.storage.blob import generate_blob_sas
from datetime import datetime, timedelta
# from cfehome.settings import PROTECTED_MEDIA_URL

# Create your views here.
def is_admin(user): 
    return user.is_superuser 


@user_passes_test(is_admin)
def product_create_view(request):
    context = {}
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            if request.user.is_authenticated:
                obj.user = request.user
                obj.save()
                messages.success(request, "Product created successfully.")
                return redirect(obj.get_manage_url())
            else:
                form.add_error(None, "User must be logged in.")
    else:
        form = ProductForm()
    
    context['form'] = form
    return render(request, 'products/create.html', context)



def product_list_view(request):
    object_list = Product.objects.all()
    return render(request, 'products/list.html', {"object_list":object_list})


@user_passes_test(is_admin)
def product_manage_detail_view(request, handle=None):
    obj = get_object_or_404(Product, handle=handle)
    attachments = ProductAttachment.objects.filter(product=obj)
    is_manager = False
    if request.user.is_authenticated:
        is_manager = request.user == obj.user
    context = {"object": obj}
    if not is_manager:
        return HttpResponseBadRequest()

    # Check if the form was submitted (POST request)
    if request.method == 'POST':
        formset = ProductAttachmentInlineFormSet(request.POST, request.FILES, queryset=attachments)
        form = ProductUpdateForm(request.POST, request.FILES, instance=obj)
        if form.is_valid() and formset.is_valid():
            instance = form.save(commit=False)
            instance.save()
            formset.save(commit=False)
            for _form in formset:
                is_delete = _form.cleaned_data.get('DELETE')
                try:
                    attachment_obj = _form.save(commit=False)
                except:
                    attachment_obj = None
                if is_delete:
                    if attachment_obj is not None:
                        if attachment_obj.pk:
                            attachment_obj.delete()
                else:
                    if attachment_obj is not None:
                        attachment_obj.product = instance
                        attachment_obj.save()
            messages.info(request, "Product Updated.")  # Show message on successful update
            return redirect(obj.get_manage_url())
    else:
        formset = ProductAttachmentInlineFormSet(queryset=attachments)
        form = ProductUpdateForm(instance=obj)

    context['form'] = form
    context['formset'] = formset
    return render(request, 'products/manager.html', context)



def product_detail_view(request, handle=None):
    obj = get_object_or_404(Product, handle=handle)
    attachments = ProductAttachment.objects.filter(product=obj)
    # attachments = obj.productattachment_self.all()
    is_owner = False
    if request.user.is_authenticated:
        is_owner = request.user.purchase_set.all().filter(product=obj, is_completed=True).exists() # request.user == obj.user
    context = {"object": obj, "is_owner": is_owner, "attachments": attachments}
    # if is_owner:
    #     form = ProductUpdateForm(request.POST or None, request.FILES or None, instance=obj)
    #     if form.is_valid():
    #         obj = form.save(commit=False)
    #         obj.save()
    #         # return redirect('/products/create/')
    #     context['form'] = form
    return render(request, 'products/detail.html', context)


# def product_attachment_download_view(request, handle=None, pk=None):
#     attachment = get_object_or_404(ProductAttachment, product__handle=handle, pk=pk)
#     can_download = attachment.is_free or False
#     if request.user.is_authenticated:
#         can_download = True # check ownership
#     if can_download is False:
#         return HttpResponseBadRequest()
#     # file_url = attachment.file.url
#     # filename = attachment.file.name
#     # content_type, _ = mimetypes.guess_type(filename)
#     # response = FileResponse(file)
#     # response['Content-Type'] = content_type or 'application/octet-stream'
#     # response['Content-Disposition'] = f"attachment; filename={filename}"
#     blob_name = attachment.file.name  # Adjust the path as needed
#     # sas_token = generate_blob_sas(
#     #     account_name=AZURE_ACCOUNT_NAME,
#     #     container_name= AZURE_CONTAINER,
#     #     blob_name=blob_name,
#     #     account_key=AZURE_CONNECTION_STRING,  # Or use a connection string
#     #     permission='r',  # Read permission
#     #     expiry=datetime.utcnow() + timedelta(hours=10),  # Expiry time
#     # )
#     sas_url = f"{PROTECTED_MEDIA_URL}/{blob_name}"

#     # response = FileResponse(sas_url)
#     # response['Content-Disposition'] = f"attachment; filename={attachment.file.name}"
#     print(sas_url)
#     response = FileResponse(sas_url)
#     content_type, _ = mimetypes.guess_type(blob_name)
#     response['Content-Type'] = content_type or 'application/octet-stream'
#     response['Content-Disposition'] = f"attachment; filename={attachment.file.name}"
#     return HttpResponseRedirect(response)


import requests, os

def product_attachment_download_view(request, handle=None, pk=None):
    attachment = get_object_or_404(ProductAttachment, product__handle=handle, pk=pk)
    blob_name = attachment.file.name
    blob_url = f"https://cover6images6commerce.blob.core.windows.net/cover-images-commerce/protected/{blob_name}"
    print(blob_name)

    # Fetch the file content using requests
    response = requests.get(blob_url, stream=True)
    
    if response.status_code == 200:
        filename = os.path.basename(blob_name)
        # Prepare the response with the fetched content
        response = FileResponse(response.raw)
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        messages.success(request, "Product downloaded.")
        return response
    else:
        # Handle error cases
        return HttpResponse("File not found", status=response.status_code)


