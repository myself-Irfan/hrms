document.getElementById('id_is_active')?.addEventListener('change', function(e) {
        if (!this.checked) {
            if (!confirm('Are you sure you want to deactivate this user? They will not be able to log in.')) {
                this.checked = true;
            }
        }
    });