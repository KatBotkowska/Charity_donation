from .forms import ContactForm

def global_contact_form(request):
    return {'contact_form': ContactForm()}

