from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import ProfileUser

# Definisikan Inline Admin agar Profile bisa diedit langsung di halaman User
class ProfileInline(admin.StackedInline):
    model = ProfileUser
    can_delete = False
    verbose_name_plural = 'Data Profil Pegawai'
    # Field yang muncul saat edit user
    fields = ('nip', 'nuptk', 'jabatan', 'status_pegawai', 'no_telepon', 'foto_profil')

# Extend UserAdmin standar Django
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    
    # Menambahkan kolom custom di list User
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_jabatan', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'groups', 'profile__jabatan', 'profile__status_pegawai')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'profile__nip')

    # Method helper untuk mengambil data dari Profile ke list display User
    def get_jabatan(self, obj):
        return obj.profile.jabatan if hasattr(obj, 'profile') else '-'
    get_jabatan.short_description = 'Jabatan'

# Unregister original User admin dan register dengan custom UserAdmin kita
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Optional: Register ProfileUser secara terpisah jika ingin akses langsung
# (Biasanya tidak perlu karena sudah di Inline, tapi disediakan saja)
@admin.register(ProfileUser)
class ProfileUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'nip', 'jabatan', 'status_pegawai', 'no_telepon')
    list_filter = ('jabatan', 'status_pegawai')
    search_fields = ('user__username', 'user__first_name', 'nip', 'nuptk')