from django import forms
from django.contrib.auth.models import User
from .models import USUARIO, PEDIDO

# Formulario de Login
class LoginForm(forms.Form):
    cuenta = forms.CharField(max_length=50)
    contrasena = forms.CharField(widget=forms.PasswordInput)

# Formulario de Registro
class RegistroForm(forms.ModelForm):
    class Meta:
        model = USUARIO
        fields = ['nombre', 'cuenta', 'contrasena', 'rol']
        
    contrasena = forms.CharField(widget=forms.PasswordInput)
    confirmarContrasena = forms.CharField(widget=forms.PasswordInput)
    cuenta = forms.CharField(max_length=50)
    rol = forms.ChoiceField(choices=[(1, 'MESERO'), (2, 'CHEF')])

    def clean(self):
        cleaned_data = super().clean()
        contrasena = cleaned_data.get('contrasena')
        confirmarContrasena = cleaned_data.get('confirmarContrasena')
        cuenta = cleaned_data.get('cuenta').upper()

        # Verificar si las contraseñas coinciden
        if contrasena != confirmarContrasena:
            self.add_error(None, 'Las contraseñas no coinciden.')

        # Verificar si la cuenta ya existe
        if USUARIO.objects.filter(cuenta__iexact=cuenta).exists():
            self.add_error(None, 'El nombre de usuario ya está en uso.') 

        cleaned_data['cuenta'] = cuenta
        return cleaned_data
    
    def save(self, commit=True):
        cuenta = self.cleaned_data['cuenta']  # Aseguramos que la cuenta esté en mayúsculas

        # Creamos un nuevo User en Django para almacenar la contraseña
        user = User.objects.create_user(
            username=cuenta,
            password=self.cleaned_data['contrasena']
        )
        
        # Crear el objeto USUARIO relacionado
        usuario = super().save(commit=False)
        usuario.user = user
        if commit:
            usuario.save()
        return usuario
    
# Formulario para los Pedidos
class PedidoForm(forms.ModelForm):
    class Meta:
        model = PEDIDO
        fields = ['mesa', 'platillo']
        widgets = {
            'mesa': forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Número de Mesa'}),
            'platillo': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Nombre del Platillo'}),
        }